# Cross\-account IAM permissions<a name="cross-account-access"></a>

You can configure cross\-account IAM permissions either by creating an identity provider from another account's cluster or by using chained `AssumeRole` operations\. In the following examples, *Account A* owns an Amazon EKS cluster that supports IAM roles for service accounts\. Pods that are running on that cluster must assume IAM permissions from *Account B*\.

**Example Create an identity provider from another account's cluster**  

**Example**  
In this example, Account A provides Account B with the OpenID Connect \(OIDC\) issuer URL from their cluster\. Account B follows the instructions in [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md) and [Configure a Kubernetes service account to assume an IAM role](associate-service-account-role.md) using the OIDC issuer URL from Account A's cluster\. Then, a cluster administrator annotates the service account in Account A's cluster to use the role from Account B \(*444455556666*\)\.  

```
apiVersion: v1
kind: ServiceAccount
metadata:
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::444455556666:role/account-b-role
```

**Example Use chained `AssumeRole` operations**  

**Example**  
In this example, Account B creates an IAM policy with the permissions to give to Pods in Account A's cluster\. Account B \(*444455556666*\) attaches that policy to an IAM role with a trust relationship that allows `AssumeRole` permissions to Account A \(*111122223333*\)\.  

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::111122223333:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {}
    }
  ]
}
```
Account A creates a role with a trust policy that gets credentials from the identity provider created with the cluster's OIDC issuer address\.  

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::111122223333:oidc-provider/oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE"
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
            "Resource": "arn:aws:iam::444455556666:role/account-b-role"
        }
    ]
}
```
The application code for Pods to assume Account B's role uses two profiles: `account_b_role` and `account_a_role`\. The `account_b_role` profile uses the `account_a_role` profile as its source\. For the AWS CLI, the `~/.aws/config` file is similar to the following\.  

```
[profile account_b_role]
source_profile = account_a_role
role_arn=arn:aws:iam::444455556666:role/account-b-role

[profile account_a_role]
web_identity_token_file = /var/run/secrets/eks.amazonaws.com/serviceaccount/token 
role_arn=arn:aws:iam::111122223333:role/account-a-role
```
To specify chained profiles for other AWS SDKs, consult the documentation for the SDK that you're using\. For more information, see [Tools to Build on AWS](https://aws.amazon.com/developer/tools/)\.