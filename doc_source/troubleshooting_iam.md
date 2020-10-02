# Troubleshooting IAM<a name="troubleshooting_iam"></a>

This topic covers some common errors that you may see while using Amazon EKS with IAM and how to work around them\.

## AccessDeniedException<a name="iam-error"></a>

If you receive an `AccessDeniedException` when calling an AWS API operation, then the AWS Identity and Access Management \(IAM\) user or role credentials that you are using do not have the required permissions to make that call\. 

```
An error occurred (AccessDeniedException) when calling the DescribeCluster operation: 
User: arn:aws:iam::<111122223333>:user/<user_name> is not authorized to perform: 
eks:DescribeCluster on resource: arn:aws:eks<:region>:<111122223333>:cluster/<cluster_name>
```

In the above example message, the user does not have permissions to call the Amazon EKS `DescribeCluster` API operation\. To provide Amazon EKS admin permissions to a user, see [Amazon EKS identity\-based policy examples](security_iam_id-based-policy-examples.md)\.

For more general information about IAM, see [Controlling access using policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_controlling.html) in the *IAM User Guide*\.

## aws\-auth ConfigMap does not grant access to the cluster<a name="security-iam-troubleshoot-ConfigMap"></a>

[AWS IAM authenticator](https://github.com/kubernetes-sigs/aws-iam-authenticator) does not permit a path in the role ARN used in the configuration map\. Therefore, before you specify `rolearn`, remove the path\. For example, change `arn:aws:iam::<123456789012>:role/<team>/<developers>/<eks-admin>` to `arn:aws:iam::<123456789012>:role/<eks-admin>`\.

## I Am not authorized to perform iam:PassRole<a name="security_iam_troubleshoot-passrole"></a>

If you receive an error that you're not authorized to perform the `iam:PassRole` action, then you must contact your administrator for assistance\. Your administrator is the person that provided you with your user name and password\. Ask that person to update your policies to allow you to pass a role to Amazon EKS\.

Some AWS services allow you to pass an existing role to that service, instead of creating a new service role or service\-linked role\. To do this, you must have permissions to pass the role to the service\.

The following example error occurs when an IAM user named `marymajor` tries to use the console to perform an action in Amazon EKS\. However, the action requires the service to have permissions granted by a service role\. Mary does not have permissions to pass the role to the service\.

```
User: arn:aws:iam::123456789012:user/marymajor is not authorized to perform: iam:PassRole
```

In this case, Mary asks her administrator to update her policies to allow her to perform the `iam:PassRole` action\.

## I want to view my access keys<a name="security_iam_troubleshoot-access-keys"></a>

After you create your IAM user access keys, you can view your access key ID at any time\. However, you can't view your secret access key again\. If you lose your secret key, you must create a new access key pair\. 

Access keys consist of two parts: an access key ID \(for example, `AKIAIOSFODNN7EXAMPLE`\) and a secret access key \(for example, `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`\)\. Like a user name and password, you must use both the access key ID and secret access key together to authenticate your requests\. Manage your access keys as securely as you do your user name and password\.

**Important**  
 Do not provide your access keys to a third party, even to help [find your canonical user ID](https://docs.aws.amazon.com/general/latest/gr/acct-identifiers.html#FindingCanonicalId)\. By doing this, you might give someone permanent access to your account\. 

When you create an access key pair, you are prompted to save the access key ID and secret access key in a secure location\. The secret access key is available only at the time you create it\. If you lose your secret access key, you must add new access keys to your IAM user\. You can have a maximum of two access keys\. If you already have two, you must delete one key pair before creating a new one\. To view instructions, see [Managing Access Keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey) in the *IAM User Guide*\.

## I'm an administrator and want to allow others to access Amazon EKS<a name="security_iam_troubleshoot-admin-delegate"></a>

To allow others to access Amazon EKS, you must create an IAM entity \(user or role\) for the person or application that needs access\. They will use the credentials for that entity to access AWS\. You must then attach a policy to the entity that grants them the correct permissions in Amazon EKS\.

To get started right away, see [Creating Your First IAM Delegated User and Group](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started_create-delegated-user.html) in the *IAM User Guide*\.

## I want to allow people outside of my AWS account to access my Amazon EKS resources<a name="security_iam_troubleshoot-cross-account-access"></a>

You can create a role that users in other accounts or people outside of your organization can use to access your resources\. You can specify who is trusted to assume the role\. For services that support resource\-based policies or access control lists \(ACLs\), you can use those policies to grant people access to your resources\.

To learn more, consult the following:
+ To learn whether Amazon EKS supports these features, see [How Amazon EKS works with IAM](security_iam_service-with-iam.md)\.
+ To learn how to provide access to your resources across AWS accounts that you own, see [Providing Access to an IAM User in Another AWS Account That You Own](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_aws-accounts.html) in the *IAM User Guide*\.
+ To learn how to provide access to your resources to third\-party AWS accounts, see [Providing Access to AWS Accounts Owned by Third Parties](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_third-party.html) in the *IAM User Guide*\.
+ To learn how to provide access through identity federation, see [Providing Access to Externally Authenticated Users \(Identity Federation\)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_federated-users.html) in the *IAM User Guide*\.
+ To learn the difference between using roles and resource\-based policies for cross\-account access, see [How IAM Roles Differ from Resource\-based Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_compare-resource-policies.html) in the *IAM User Guide*\.