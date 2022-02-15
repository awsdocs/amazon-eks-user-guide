# Amazon EKS identity\-based policy examples<a name="security_iam_id-based-policy-examples"></a>

By default, IAM users and roles don't have permission to create or modify Amazon EKS resources\. They also can't perform tasks using the AWS Management Console, AWS CLI, or AWS API\. An IAM administrator must create IAM policies that grant users and roles permission to perform specific API operations on the specified resources they need\. The administrator must then attach those policies to the IAM users or groups that require those permissions\.

To learn how to create an IAM identity\-based policy using these example JSON policy documents, see [Creating policies on the JSON tab](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html#access_policies_create-json-editor) in the *IAM User Guide*\.

When you create an Amazon EKS cluster, the AWS Identity and Access Management \(IAM\) entity user or role, such as a [federated user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers.html) that creates the cluster, is automatically granted `system:masters` permissions in the cluster's role\-based access control \(RBAC\) configuration in the Amazon EKS control plane\. This IAM entity doesn't appear in any visible configuration, so make sure to keep track of which IAM entity originally created the cluster\. To grant additional AWS users or roles the ability to interact with your cluster, you must edit the `aws-auth` `ConfigMap` within Kubernetes and create a Kubernetes `rolebinding` or `clusterrolebinding` with the name of a `group` that you specify in the `aws-auth` `ConfigMap`\.

For additional information about working with the ConfigMap, see [Enabling IAM user and role access to your cluster](add-user-role.md)\.

**Topics**
+ [Policy best practices](#security_iam_service-with-iam-policy-best-practices)
+ [Using the Amazon EKS console](#security_iam_id-based-policy-examples-console)
+ [View nodes and workloads for all clusters in the AWS Management Console](#policy_example3)
+ [Allow users to view their own permissions](#security_iam_id-based-policy-examples-view-own-permissions)
+ [Update a Kubernetes cluster](#policy_example1)
+ [List or describe all clusters](#policy_example2)

## Policy best practices<a name="security_iam_service-with-iam-policy-best-practices"></a>

Identity\-based policies are very powerful\. They determine whether someone can create, access, or delete Amazon EKS resources in your account\. These actions can incur costs for your AWS account\. When you create or edit identity\-based policies, follow these guidelines and recommendations:
+ **Get started using AWS managed policies** – To start using Amazon EKS quickly, use AWS managed policies to give your employees the permissions they need\. These policies are already available in your account and are maintained and updated by AWS\. For more information, see [Get started using permissions with AWS managed policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#bp-use-aws-defined-policies) in the *IAM User Guide*\.
+ **Grant least privilege** – When you create custom policies, grant only the permissions required to perform a task\. Start with a minimum set of permissions and grant additional permissions as necessary\. Doing so is more secure than starting with permissions that are too lenient and then trying to tighten them later\. For more information, see [Grant least privilege](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#grant-least-privilege) in the *IAM User Guide*\.
+ **Enable MFA for sensitive operations** – For extra security, require IAM users to use multi\-factor authentication \(MFA\) to access sensitive resources or API operations\. For more information, see [Using multi\-factor authentication \(MFA\) in AWS](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa.html) in the *IAM User Guide*\.
+ **Use policy conditions for extra security** – To the extent that it's practical, define the conditions under which your identity\-based policies allow access to a resource\. For example, you can write conditions to specify a range of allowable IP addresses that a request must come from\. You can also write conditions to allow requests only within a specified date or time range, or to require the use of SSL or MFA\. For more information, see [IAM JSON policy elements: Condition](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html) in the *IAM User Guide*\.

## Using the Amazon EKS console<a name="security_iam_id-based-policy-examples-console"></a>

To access the Amazon EKS console, you must have a minimum set of permissions\. These permissions must allow you to list and view details about the Amazon EKS resources in your AWS account\. If you create an identity\-based policy that is more restrictive than the minimum required permissions, the console won't function as intended for entities \(IAM users or roles\) with that policy\.

**Important**  
If you see an **Error loading Namespaces** error in the console, or don't see anything on the **Overview** or **Workloads** tabs, see [Can't see workloads or nodes and receive an error in the AWS Management Console](troubleshooting_iam.md#security-iam-troubleshoot-cannot-view-nodes-or-workloads) to resolve the issue\. If you don't resolve the issue, you can still view and manage aspects of your Amazon EKS cluster on the **Configuration** tab\.

To ensure that those entities can still use the Amazon EKS console, create a policy with your own unique name, such as `AmazonEKSAdminPolicy`\. Attach the policy to the entities\. For more information, see [Adding permissions to a user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_change-permissions.html#users_change_permissions-add-console) in the *IAM User Guide*\.

**Important**  
The following example policy will allow you to view information on the **Configuration** tab in the console\. To view information on the **Nodes** and **Workloads** in the AWS Management Console, you need additional IAM permissions, as well as Kubernetes permissions\. For more information, see the [View nodes and workloads for all clusters in the AWS Management Console](#policy_example3) example policy\.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "eks:*"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "iam:PassRole",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "iam:PassedToService": "eks.amazonaws.com"
                }
            }
        }
    ]
}
```

You don't need to allow minimum console permissions for users that are making calls only to the AWS CLI or the AWS API\. Instead, allow access to only the actions that match the API operation that you're trying to perform\.

## View nodes and workloads for all clusters in the AWS Management Console<a name="policy_example3"></a>

This example shows how you can create a policy that allows a user to [View nodes](view-nodes.md) and [View workloads](view-workloads.md) for all clusters\.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "eks:DescribeNodegroup",
                "eks:ListNodegroups",
                "eks:DescribeCluster",
                "eks:ListClusters",
                "eks:AccessKubernetesApi",
                "ssm:GetParameter",
                "eks:ListUpdates",
                "eks:ListFargateProfiles"
            ],
            "Resource": "*"
        }
    ]
}
```

**Important**  
The policy must be attached to a user or role that is mapped to a Kubernetes user or group in the `aws-auth` configmap\. The user or group must be a `subject` in a `rolebinding` or `clusterrolebinding` that is bound to a Kubernetes `role` or `clusterrole` that has the necessary permissions to view the Kubernetes resources\. For more information about adding IAM users or roles to the `aws-auth` configmap, see [Enabling IAM user and role access to your cluster](add-user-role.md)\. To create roles and role bindings, see [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) in the Kubernetes documentation\. You can download the following example manifests that create a `clusterrole` and `clusterrolebinding` or a `role` and `rolebinding`:  
**View Kubernetes resources in all namespaces** – The group name in the file is `eks-console-dashboard-full-access-group`, which is the group that your IAM user or role needs to be mapped to in the `aws-auth` configmap\. You can change the name of the group before applying it to your cluster, if desired, and then map your IAM user or role to that group in the configmap\. To download the file, select the appropriate link for the AWS Region that your cluster is in\.  
[All AWS Regions other than Beijing and Ningxia China](https://amazon-eks.s3.us-west-2.amazonaws.com/docs/eks-console-full-access.yaml)
[Beijing and Ningxia China AWS Regions](https://amazon-eks.s3.cn-north-1.amazonaws.com.cn/docs/eks-console-full-access.yaml)
**View Kubernetes resources in a specific namespace** – The namespace in this file is `default`, so if you want to specify a different namespace, edit the file before applying it to your cluster\. The group name in the file is `eks-console-dashboard-restricted-access-group`, which is the group that your IAM user or role needs to be mapped to in the `aws-auth` configmap\. You can change the name of the group before applying it to your cluster, if desired, and then map your IAM user or role to that group in the configmap\. To download the file, select the appropriate link for the AWS Region that your cluster is in\.  
[All AWS Regions other than Beijing and Ningxia China](https://amazon-eks.s3.us-west-2.amazonaws.com/docs/eks-console-restricted-access.yaml)
[Beijing and Ningxia China AWS Regions](https://amazon-eks.s3.cn-north-1.amazonaws.com.cn/docs/eks-console-restricted-access.yaml)

## Allow users to view their own permissions<a name="security_iam_id-based-policy-examples-view-own-permissions"></a>

This example shows how you might create a policy that allows IAM users to view the inline and managed policies that are attached to their user identity\. This policy includes permissions to complete this action on the console or programmatically using the AWS CLI or AWS API\.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ViewOwnUserInfo",
            "Effect": "Allow",
            "Action": [
                "iam:GetUserPolicy",
                "iam:ListGroupsForUser",
                "iam:ListAttachedUserPolicies",
                "iam:ListUserPolicies",
                "iam:GetUser"
            ],
            "Resource": ["arn:aws:iam::*:user/${aws:username}"]
        },
        {
            "Sid": "NavigateInConsole",
            "Effect": "Allow",
            "Action": [
                "iam:GetGroupPolicy",
                "iam:GetPolicyVersion",
                "iam:GetPolicy",
                "iam:ListAttachedGroupPolicies",
                "iam:ListGroupPolicies",
                "iam:ListPolicyVersions",
                "iam:ListPolicies",
                "iam:ListUsers"
            ],
            "Resource": "*"
        }
    ]
}
```

## Update a Kubernetes cluster<a name="policy_example1"></a>

This example shows how you can create a policy that allows a user to update the Kubernetes version of any *dev* cluster for an account, in any region\.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "eks:UpdateClusterVersion",
            "Resource": "arn:aws:eks:*:<111122223333>:cluster/<dev>"
        }
    ]
}
```

## List or describe all clusters<a name="policy_example2"></a>

This example shows how you can create a policy that allows a user read\-only access to list or describe all clusters\. An account must be able to list and describe clusters to use the `update-kubeconfig` AWS CLI command\.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "eks:DescribeCluster",
                "eks:ListClusters"
            ],
            "Resource": "*"
        }
    ]
}
```