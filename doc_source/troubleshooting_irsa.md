# Troubleshooting IRSA<a name="troubleshooting_iam"></a>

This topic covers some common errors that you may see while using [Amazon EKS with IRSA (IAM Roles for Service Accounts)](iam-roles-for-service-accounts.md) and how to work around them.

## Review Logs

Review how to access [Kubernetes logs.](https://kubernetes.io/docs/concepts/cluster-administration/logging/)

In short, retrieve logs for the relevant container or node.

```
kubectl logs <name_of_pod> [-c <name_of_container>]
```

## First Steps

1. [Verify SDK version.](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts-minimum-sdk.html)
2. [Restart pods.](https://kubernetes.io/docs/reference/kubectl/cheatsheet/#deleting-resources)
3. Verify formatting of ARN values.

## No OpenIDConnect provider found

If you receive an `WebIdentityErr` or `InvalidIdentityToken` message, your cluster may not have a properly configured OIDC provider.

**Check if you have an OIDC provider**

1. Check your cluster's OIDC provider URL:

```
aws eks describe-cluster --name cluster_name --query "cluster.identity.oidc.issuer" --output text
```

Example output:

```
https://oidc.eks.us-west-2.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E
```

2. List the IAM OIDC providers in your account. Replace `EXAMPLED539D4633E53DE1B716D3041E`  with the value returned from the previous command:

```
aws iam list-open-id-connect-providers | grep EXAMPLED539D4633E53DE1B716D3041E
```

Using the example output below, determine if your cluster has an OIDC provider.

Expected output:
```
"Arn": "arn:aws:iam::111122223333:oidc-provider/oidc.eks.us-west-2.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E"
```

If your cluster does not have an OIDC provider, [create one.](https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html)

If your cluster has an OIDC provider, proceed to verifying the trust relationship between the OIDC provider and IAM.

**Check OIDC Trust Relationship**

1. Get trust relations of IRSA IAM Role

To verify trust relations, run following command with your role name:
```
$ aws iam get-role --role-name <EKS-IRSA>
```
Note: Replace EKS-IRSA with your [IAM role name.](https://docs.aws.amazon.com/eks/latest/userguide/create-service-account-iam-policy-and-role.html#create-service-account-iam-role)

2. In the output JSON, look for the AssumeRolePolicyDocument section.

Example output:
```
{
    "Role": {
        "Path": "/",
        "RoleName": "EKS-IRSA",
        "RoleId": "AROAQ55NEXAMPLELOEISVX",
        "Arn": "arn:aws:iam::ACCOUNT_ID:role/EKS-IRSA",
        "CreateDate": "2021-04-22T06:39:21+00:00",
        "AssumeRolePolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Federated": "arn:aws:iam::ACCOUNT_ID:oidc-provider/oidc.eks.AWS_REGION.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E"
                    },
                    "Action": "sts:AssumeRoleWithWebIdentity",
                    "Condition": {
                        "StringEquals": {
                            "oidc.eks.AWS_REGION.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E:aud": "sts.amazonaws.com",
                            "oidc.eks.AWS_REGION.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E:sub": "system:serviceaccount:SERVICE_ACCOUNT_NAMESPACE:SERVICE_ACCOUNT_NAME"
                        }
                    }
                }
            ]
        },
        "MaxSessionDuration": 3600,
        "RoleLastUsed": {
            "LastUsedDate": "2021-04-22T07:01:15+00:00",
            "Region": "AWS_REGION"
        }
    }
}
```

Compare the OIDC urls (`oidc.eks.AWS_REGION.amazonaws.com/id/E53DE...`) to the URL retrieved above (see "Check if you have an OIDC provider").

Note: Check that you have specified the correct AWS Region, Kubernetes service account name, and Kubernetes namespace.

## Service Account Errors

**Check if you created a service account**

Use the following command:
```
kubectl get sa -n <YOUR_NAMESPACE>
```
Note: Replace YOUR_NAMESPACE with your Kubernetes namespace.

Example output:
```
NAME      SECRETS   AGE
default   1         28d
irsa      1         66m
```
If you don't have a service account, see [Associate and IAM Role.](https://docs.aws.amazon.com/eks/latest/userguide/specify-service-account-role.html)

**Verify service account has IAM role annotations**

Use the following command:
```
kubectl describe sa <irsa> -n <YOUR_NAMESPACE>
```
Note: Replace IRSA with your Kubernetes service account name. Replace YOUR_NAMESPACE with your Kubernetes namespace.

Example output:
```
Name:                irsa
Namespace:           default
Labels:              none
Annotations:         eks.amazonaws.com/role-arn: arn:aws:iam::ACCOUNT_ID:role/IAM_ROLE_NAME
Image pull secrets:  none
Mountable secrets:   irsa-token-v5rtc
Tokens:              irsa-token-v5rtc
Events:              none
```

Verify (1) annotation is properly formatted, (2) the referenced role exists, and (3) the IAM role for IRSA has permission to assume the referenced role.


**Verify serviceAccountName in your pod**
Use the following command:
```
kubectl get pod <POD_NAME>  -o yaml -n <YOUR_NAMESPACE>| grep -i serviceAccountName:
```
Note: Replace POD_NAME and YOUR_NAMESPACE with your Kubernetes pod and namespace.

Example output:
```
serviceAccountName: irsa
```

Does the service account name defined for the pod exist? Are the service account and the pod in the same namespace?

## Filesystem Permission Denied

Your containers must run as root to access the service account token. 

If your containers aren't running as root, then you can receive the following errors:

```
Error: PermissionError: [Errno 13] Permission denied: ‘/var/run/secrets/eks.amazonaws.com/serviceaccount/token
```
Or:
```
WebIdentityErr: failed fetching WebIdentity token: caused by: WebIdentityErr: unable to read file at /var/run/secrets/eks.amazonaws.com/serviceaccount/token\ncaused by: open /var/run/secrets/eks.amazonaws.com/serviceaccount/token: permission denied
```

[[Jim: do we have an existing page that covers privileged pods?]]

## OIDC Audience Error

If you created the OIDC provider with the incorrect audience, then you receive the following error:
```
Error - An error occurred (InvalidIdentityToken) when calling the AssumeRoleWithWebIdentity operation: Incorrect token audience
```

**Verify OIDC provider `ClientIDList`**

```
aws iam get-open-id-connect-provider --open-id-connect-provider-arn arn:aws:iam::ACCOUNT_ID:oidc-provider/oidc.eks.AWS_REGION.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E
```

Example output:
```
{
    "Url": "oidc.eks.AWS_REGION.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E",
    "ClientIDList": [
        "sts.amazonaws.com"
    ],
    "ThumbprintList": [
        "9e99a48a9960b14926bb7f3b02e22da2b0ab7280"
    ],
    "CreateDate": "2021-01-21T04:29:09.788000+00:00",
    "Tags": []
}
```

The value of "ClientIDList" must be "sts.amazonaws.com".

If this value is incorrect, delete and [recreate the OIDC provider](https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html).

## Thumbprint Match Error

IAM uses a certificate thumbprint to validate requests from OIDC. 

If the thumbprint that's configured in the IAM OIDC is not correct, you can receive the following error:
```
failed to retrieve credentials caused by: InvalidIdentityToken: OpenIDConnect provider's HTTPS certificate doesn't match configured thumbprint
```

To automatically configure the correct thumbprint, use eksctl to [create the IAM identity provider.](https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html)

## Verify Identity Webhook

If you accidentally deleted or changed your webhook configuration, then IRSA stops working.

Run the following command to verify that your webhook configuration exists and is valid:
```
kubectl get mutatingwebhookconfiguration pod-identity-webhook  -o yaml
```

## Learn More

To learn more, consult the following:
+ To learn more about Service Accounts, review the [Kubernetes Documentation](https://kubernetes.io/docs/reference/access-authn-authz/service-accounts-admin/).
+ To learn more about how AWS IAM interacts with Kubernetes, review [IAM roles for service accounts](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html)\.
+ To learn how to define access to resources, see [the *IAM User Guide*](https://docs.aws.amazon.com/IAM/latest/UserGuide/)\.
+ To learn how to provide access through identity federation, see [Providing access to externally authenticated users \(identity federation\)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_federated-users.html) in the *IAM User Guide*\.


