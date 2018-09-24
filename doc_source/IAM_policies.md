# Amazon EKS IAM Policies, Roles, and Permissions<a name="IAM_policies"></a>

By default, IAM users don't have permission to create or modify Amazon EKS resources, or perform tasks using the Amazon EKS API\. \(This means that they also can't do so using the Amazon EKS console or the AWS CLI\.\) To allow IAM users to create or modify clusters, you must create IAM policies that grant IAM users permissions to use the specific resources and API actions that they need, and then attach those policies to the IAM users or groups that require those permissions\.

When you attach a policy to a user or group of users, it allows or denies the users permission to perform the specified tasks on the specified resources\. For more information, see [Permissions and Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/PermissionsAndPolicies.html) in the *IAM User Guide*\. For more information about managing and creating custom IAM policies, see [Managing IAM Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/ManagingPolicies.html)\.

Likewise, Amazon EKS makes calls to other AWS services on your behalf, so the service must authenticate with your credentials\. This authentication is accomplished by creating an IAM role and policy that can provide these permissions and then associating that role with your compute environments when you create them\. For more information, see [Amazon EKS Service IAM Role](service_IAM_role.md) and also [IAM Roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-toplevel.html) in the *IAM User Guide*\.

**Getting Started**

An IAM policy must grant or deny permissions to use one or more Amazon EKS actions\.

**Topics**
+ [Policy Structure](iam-policy-structure.md)
+ [Creating Amazon EKS IAM Policies](EKS_IAM_user_policies.md)
+ [Amazon EKS Service IAM Role](service_IAM_role.md)