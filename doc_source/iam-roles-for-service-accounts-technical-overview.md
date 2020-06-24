# IAM roles for service accounts technical overview<a name="iam-roles-for-service-accounts-technical-overview"></a>

In 2014, AWS Identity and Access Management added support for federated identities using OpenID Connect \(OIDC\)\. This feature allows you to authenticate AWS API calls with supported identity providers and receive a valid OIDC JSON web token \(JWT\)\. You can pass this token to the AWS STS `AssumeRoleWithWebIdentity` API operation and receive IAM temporary role credentials\. You can use these credentials to interact with any AWS service, like Amazon S3 and DynamoDB\. 

Kubernetes has long used service accounts as its own internal identity system\. Pods can authenticate with the Kubernetes API server using an auto\-mounted token \(which was a non\-OIDC JWT\) that only the Kubernetes API server could validate\. These legacy service account tokens do not expire, and rotating the signing key is a difficult process\. In Kubernetes version 1\.12, support was added for a new `ProjectedServiceAccountToken` feature, which is an OIDC JSON web token that also contains the service account identity, and supports a configurable audience\.

Amazon EKS now hosts a public OIDC discovery endpoint per cluster containing the signing keys for the `ProjectedServiceAccountToken` JSON web tokens so external systems, like IAM, can validate and accept the OIDC tokens issued by Kubernetes\.

## IAM role configuration<a name="iam-role-configuration"></a>

In IAM, you create an IAM role with a trust relationship that is scoped to your cluster's OIDC provider, the service account namespace, and \(optionally\) the service account name, and then attach the IAM policy that you want to associate with the service account\. You can add multiple entries in the `StringEquals` and `StringLike` conditions below to use multiple service accounts or namespaces with the role\.
+ To scope a role to a specific service account:

  ```
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Federated": "arn:aws:iam::AWS_ACCOUNT_ID:oidc-provider/OIDC_PROVIDER"
        },
        "Action": "sts:AssumeRoleWithWebIdentity",
        "Condition": {
          "StringEquals": {
            "OIDC_PROVIDER:sub": "system:serviceaccount:SERVICE_ACCOUNT_NAMESPACE:SERVICE_ACCOUNT_NAME"
          }
        }
      }
    ]
  }
  ```
+ To scope a role to an entire namespace \(to use the namespace as a boundary\):

  ```
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Federated": "arn:aws:iam::AWS_ACCOUNT_ID:oidc-provider/OIDC_PROVIDER"
        },
        "Action": "sts:AssumeRoleWithWebIdentity",
        "Condition": {
          "StringLike": {
            "OIDC_PROVIDER:sub": "system:serviceaccount:SERVICE_ACCOUNT_NAMESPACE:*"
          }
        }
      }
    ]
  }
  ```

## Service account configuration<a name="service-account-configuration"></a>

In Kubernetes, you define the IAM role to associate with a service account in your cluster by adding the `eks.amazonaws.com/role-arn` annotation to the service account\.

```
apiVersion: v1
kind: ServiceAccount
metadata:
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::AWS_ACCOUNT_ID:role/IAM_ROLE_NAME
```

## Pod configuration<a name="pod-configuration"></a>

The [Amazon EKS Pod Identity Webhook](https://github.com/aws/amazon-eks-pod-identity-webhook) on the cluster watches for pods that are associated with service accounts with this annotation and applies the following environment variables to them\.

```
AWS_ROLE_ARN=arn:aws:iam::AWS_ACCOUNT_ID:role/IAM_ROLE_NAME
AWS_WEB_IDENTITY_TOKEN_FILE=/var/run/secrets/eks.amazonaws.com/serviceaccount/token
```

**Note**  
Your cluster does not need to use the mutating web hook to configure the environment variables and token file mounts; you can choose to configure pods to add these environment variables manually\.

[Supported versions of the AWS SDK](iam-roles-for-service-accounts-minimum-sdk.md) look for these environment variables first in the credential chain provider\. The role credentials are used for pods that meet this criteria\.

**Note**  
When a pod uses AWS credentials from an IAM role associated with a service account, the AWS CLI or other SDKs in the containers for that pod use the credentials provided by that role exclusively\. They no longer inherit any IAM permissions from the worker node IAM role\.

By default, only containers that run as `root` have the proper file system permissions to read the web identity token file\. You can provide these permissions by having your containers run as `root`, or by providing the following security context for the containers in your manifest\. The `fsGroup` ID is arbitrary, and you can choose any valid group ID\. For more information about the implications of setting a security context for your pods, see [Configure a Security Context for a Pod or Container](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) in the Kubernetes documentation\.

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  template:
    metadata:
      labels:
        app: my-app
    spec:
      serviceAccountName: my-app
      containers:
      - name: my-app
        image: my-app:latest
      securityContext:
        fsGroup: 1337
...
```

The `kubelet` requests and stores the token on behalf of the pod\. By default, the `kubelet` refreshes the token it if it is older than 80 percent of its total TTL, or if the token is older than 24 hours\. You can modify the expiration duration for any account, except the default service account, with settings in your pod spec\. For more information, see [Service Account Token Volume Projection](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#service-account-token-volume-projection) in the Kubernetes documentation\.

## Cross\-account IAM permissions<a name="cross-account-access"></a>

You can configure cross\-account IAM permissions either by creating an identity provider from another account's cluster or by using chained AssumeRole operations\. In the following examples, Account A owns an Amazon EKS cluster that supports IAM roles for service accounts\. Pods running on that cluster need to assume IAM permissions from Account B\.

**Example : Create an identity provider from another account's cluster**  

**Example**  
In this example, Account A would provide Account B with the OIDC issuer URL from their cluster\. Account B follows the instructions in [Enabling IAM roles for service accounts on your cluster](enable-iam-roles-for-service-accounts.md) and [Creating an IAM role and policy for your service account](create-service-account-iam-policy-and-role.md) using the OIDC issuer URL from Account A's cluster\. Then a cluster administrator annotates the service account in Account A's cluster to use the role from Account B\.  

```
apiVersion: v1
kind: ServiceAccount
metadata:
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::ACCOUNT_B_AWS_ACCOUNT_ID:role/IAM_ROLE_NAME
```

**Example : Use chained `AssumeRole` operations**  

**Example**  
In this example, Account B creates an IAM policy with the permissions to give to pods in Account A's cluster\. Account B attaches that policy to an IAM role with a trust relationship that allows `AssumeRole` permissions to Account A \(`111111111111`\), as shown below\.  

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::111111111111:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {}
    }
  ]
}
```
Account A creates a role with a trust policy that gets credentials from the identity provider created with the cluster's OIDC issuer URL, as shown below\.  

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::111111111111:oidc-provider/oidc.eks.region-code.amazonaws.com/id/EXAMPLEC061A78C479E31025A21AC4CDE191335D05820BE5CE"
      },
      "Action": "sts:AssumeRoleWithWebIdentity"
    }
  ]
}
```
Account A attaches a policy to that role with the following permissions to assume the role that Account B created\.  

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Resource": "arn:aws:iam::222222222222:role/account-b-role"
        }
    ]
}
```
The application code for pods to assume Account B's role uses two profiles: `account_b_role` and `account_a_role`\. The `account_b_role` profile uses the `account_a_role` profile as its source\. For the AWS CLI, the `~/.aws/config` file would look like the following example\.  

```
[profile account_b_role]
source_profile = account_a_role
role_arn=arn:aws:iam::222222222222:role/account-b-role

[profile account_a_role]
web_identity_token_file = /var/run/secrets/eks.amazonaws.com/serviceaccount/token 
role_arn=arn:aws:iam::111111111111:role/account-a-role
```
To specify chained profiles for other AWS SDKs, consult their documentation\.