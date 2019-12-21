# Identity and Access Management for Amazon EKS<a name="security-iam"></a>

AWS Identity and Access Management \(IAM\) is an AWS service that helps an administrator securely control access to AWS resources\. IAM administrators control who can be *authenticated* \(signed in\) and *authorized* \(have permissions\) to use Amazon EKS resources\. IAM is an AWS service that you can use with no additional charge\.

**Topics**
+ [Audience](#security_iam_audience)
+ [Authenticating With Identities](#security_iam_authentication)
+ [Managing Access Using Policies](#security_iam_access-manage)
+ [How Amazon EKS Works with IAM](security_iam_service-with-iam.md)
+ [Amazon EKS Identity\-Based Policy Examples](security_iam_id-based-policy-examples.md)
+ [Using Service\-Linked Roles for Amazon EKS](using-service-linked-roles.md)
+ [Amazon EKS Service IAM Role](service_IAM_role.md)
+ [Amazon EKS Worker Node IAM Role](worker_node_IAM_role.md)
+ [Pod Execution Role](pod-execution-role.md)
+ [IAM Roles for Service Accounts](iam-roles-for-service-accounts.md)
+ [Troubleshooting Amazon EKS Identity and Access](security_iam_troubleshoot.md)

## Audience<a name="security_iam_audience"></a>

How you use AWS Identity and Access Management \(IAM\) differs, depending on the work you do in Amazon EKS\.

**Service user** – If you use the Amazon EKS service to do your job, then your administrator provides you with the credentials and permissions that you need\. As you use more Amazon EKS features to do your work, you might need additional permissions\. Understanding how access is managed can help you request the right permissions from your administrator\. If you cannot access a feature in Amazon EKS, see [Troubleshooting Amazon EKS Identity and Access](security_iam_troubleshoot.md)\.

**Service administrator** – If you're in charge of Amazon EKS resources at your company, you probably have full access to Amazon EKS\. It's your job to determine which Amazon EKS features and resources your employees should access\. You must then submit requests to your IAM administrator to change the permissions of your service users\. Review the information on this page to understand the basic concepts of IAM\. To learn more about how your company can use IAM with Amazon EKS, see [How Amazon EKS Works with IAM](security_iam_service-with-iam.md)\.

**IAM administrator** – If you're an IAM administrator, you might want to learn details about how you can write policies to manage access to Amazon EKS\. To view example Amazon EKS identity\-based policies that you can use in IAM, see [Amazon EKS Identity\-Based Policy Examples](security_iam_id-based-policy-examples.md)\.

## Authenticating With Identities<a name="security_iam_authentication"></a>

Authentication is how you sign in to AWS using your identity credentials\. For more information about signing in using the AWS Management Console, see [The IAM Console and Sign\-in Page](https://docs.aws.amazon.com/IAM/latest/UserGuide/console.html) in the *IAM User Guide*\.

You must be *authenticated* \(signed in to AWS\) as the AWS account root user, an IAM user, or by assuming an IAM role\. You can also use your company's single sign\-on authentication, or even sign in using Google or Facebook\. In these cases, your administrator previously set up identity federation using IAM roles\. When you access AWS using credentials from another company, you are assuming a role indirectly\. 

To sign in directly to the [AWS Management Console](https://console.aws.amazon.com/), use your password with your root user email or your IAM user name\. You can access AWS programmatically using your root user or IAM user access keys\. AWS provides SDK and command line tools to cryptographically sign your request using your credentials\. If you don’t use AWS tools, you must sign the request yourself\. Do this using *Signature Version 4*, a protocol for authenticating inbound API requests\. For more information about authenticating requests, see [Signature Version 4 Signing Process](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html) in the *AWS General Reference*\.

Regardless of the authentication method that you use, you might also be required to provide additional security information\. For example, AWS recommends that you use multi\-factor authentication \(MFA\) to increase the security of your account\. To learn more, see [Using Multi\-Factor Authentication \(MFA\) in AWS](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa.html) in the *IAM User Guide*\.

### AWS Account Root User<a name="security_iam_authentication-rootuser"></a>

  When you first create an AWS account, you begin with a single sign\-in identity that has complete access to all AWS services and resources in the account\. This identity is called the AWS account *root user* and is accessed by signing in with the email address and password that you used to create the account\. We strongly recommend that you do not use the root user for your everyday tasks, even the administrative ones\. Instead, adhere to the [best practice of using the root user only to create your first IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#create-iam-users)\. Then securely lock away the root user credentials and use them to perform only a few account and service management tasks\. 

### IAM Users and Groups<a name="security_iam_authentication-iamuser"></a>

An *[IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html)* is an identity within your AWS account that has specific permissions for a single person or application\. An IAM user can have long\-term credentials such as a user name and password or a set of access keys\. To learn how to generate access keys, see [Managing Access Keys for IAM Users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) in the *IAM User Guide*\. When you generate access keys for an IAM user, make sure you view and securely save the key pair\. You cannot recover the secret access key in the future\. Instead, you must generate a new access key pair\.

An [https://docs.aws.amazon.com/IAM/latest/UserGuide/id_groups.html](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_groups.html) is an identity that specifies a collection of IAM users\. You can't sign in as a group\. You can use groups to specify permissions for multiple users at a time\. Groups make permissions easier to manage for large sets of users\. For example, you could have a group named *IAMAdmins* and give that group permissions to administer IAM resources\.

Users are different from roles\. A user is uniquely associated with one person or application, but a role is intended to be assumable by anyone who needs it\. Users have permanent long\-term credentials, but roles provide temporary credentials\. To learn more, see [When to Create an IAM User \(Instead of a Role\)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id.html#id_which-to-choose) in the *IAM User Guide*\.

### IAM Roles<a name="security_iam_authentication-iamrole"></a>

An *[IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)* is an identity within your AWS account that has specific permissions\. It is similar to an IAM user, but is not associated with a specific person\. You can temporarily assume an IAM role in the AWS Management Console by [switching roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-console.html)\. You can assume a role by calling an AWS CLI or AWS API operation or by using a custom URL\. For more information about methods for using roles, see [Using IAM Roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html) in the *IAM User Guide*\.

IAM roles with temporary credentials are useful in the following situations:
+ **Temporary IAM user permissions** – An IAM user can assume an IAM role to temporarily take on different permissions for a specific task\. 
+ **Federated user access** –  Instead of creating an IAM user, you can use existing identities from AWS Directory Service, your enterprise user directory, or a web identity provider\. These are known as *federated users*\. AWS assigns a role to a federated user when access is requested through an [identity provider](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers.html)\. For more information about federated users, see [Federated Users and Roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_access-management.html#intro-access-roles) in the *IAM User Guide*\. 
+ **Cross\-account access** – You can use an IAM role to allow someone \(a trusted principal\) in a different account to access resources in your account\. Roles are the primary way to grant cross\-account access\. However, with some AWS services, you can attach a policy directly to a resource \(instead of using a role as a proxy\)\. To learn the difference between roles and resource\-based policies for cross\-account access, see [How IAM Roles Differ from Resource\-based Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_compare-resource-policies.html) in the *IAM User Guide*\.
+ **AWS service access** –  A service role is an IAM role that a service assumes to perform actions in your account on your behalf\. When you set up some AWS service environments, you must define a role for the service to assume\. This service role must include all the permissions that are required for the service to access the AWS resources that it needs\. Service roles vary from service to service, but many allow you to choose your permissions as long as you meet the documented requirements for that service\. Service roles provide access only within your account and cannot be used to grant access to services in other accounts\. You can create, modify, and delete a service role from within IAM\. For example, you can create a role that allows Amazon Redshift to access an Amazon S3 bucket on your behalf and then load data from that bucket into an Amazon Redshift cluster\. For more information, see [Creating a Role to Delegate Permissions to an AWS Service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html) in the *IAM User Guide*\. 
+ **Applications running on Amazon EC2** –  You can use an IAM role to manage temporary credentials for applications that are running on an EC2 instance and making AWS CLI or AWS API requests\. This is preferable to storing access keys within the EC2 instance\. To assign an AWS role to an EC2 instance and make it available to all of its applications, you create an instance profile that is attached to the instance\. An instance profile contains the role and enables programs that are running on the EC2 instance to get temporary credentials\. For more information, see [Using an IAM Role to Grant Permissions to Applications Running on Amazon EC2 Instances](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html) in the *IAM User Guide*\. 

To learn whether to use IAM roles, see [When to Create an IAM Role \(Instead of a User\)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id.html#id_which-to-choose_role) in the *IAM User Guide*\.

## Managing Access Using Policies<a name="security_iam_access-manage"></a>

You control access in AWS by creating policies and attaching them to IAM identities or AWS resources\. A policy is an object in AWS that, when associated with an identity or resource, defines their permissions\. AWS evaluates these policies when an entity \(root user, IAM user, or IAM role\) makes a request\. Permissions in the policies determine whether the request is allowed or denied\. Most policies are stored in AWS as JSON documents\. For more information about the structure and contents of JSON policy documents, see [Overview of JSON Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json) in the *IAM User Guide*\.

An IAM administrator can use policies to specify who has access to AWS resources, and what actions they can perform on those resources\. Every IAM entity \(user or role\) starts with no permissions\. In other words, by default, users can do nothing, not even change their own password\. To give a user permission to do something, an administrator must attach a permissions policy to a user\. Or the administrator can add the user to a group that has the intended permissions\. When an administrator gives permissions to a group, all users in that group are granted those permissions\.

IAM policies define permissions for an action regardless of the method that you use to perform the operation\. For example, suppose that you have a policy that allows the `iam:GetRole` action\. A user with that policy can get role information from the AWS Management Console, the AWS CLI, or the AWS API\.

### Identity\-Based Policies<a name="security_iam_access-manage-id-based-policies"></a>

Identity\-based policies are JSON permissions policy documents that you can attach to an identity, such as an IAM user, role, or group\. These policies control what actions that identity can perform, on which resources, and under what conditions\. To learn how to create an identity\-based policy, see [Creating IAM Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html) in the *IAM User Guide*\.

Identity\-based policies can be further categorized as *inline policies* or *managed policies*\. Inline policies are embedded directly into a single user, group, or role\. Managed policies are standalone policies that you can attach to multiple users, groups, and roles in your AWS account\. Managed policies include AWS managed policies and customer managed policies\. To learn how to choose between a managed policy or an inline policy, see [Choosing Between Managed Policies and Inline Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html#choosing-managed-or-inline) in the *IAM User Guide*\.

### Resource\-Based Policies<a name="security_iam_access-manage-resource-based-policies"></a>

Resource\-based policies are JSON policy documents that you attach to a resource such as an Amazon S3 bucket\. Service administrators can use these policies to define what actions a specified principal \(account member, user, or role\) can perform on that resource and under what conditions\. Resource\-based policies are inline policies\. There are no managed resource\-based policies\.

### Access Control Lists \(ACLs\)<a name="security_iam_access-manage-acl"></a>

Access control policies \(ACLs\) control which principals \(account members, users, or roles\) have permissions to access a resource\. ACLs are similar to resource\-based policies, although they are the only policy type that does not use the JSON policy document format\. Amazon S3, AWS WAF, and Amazon VPC are examples of services that support ACLs\. To learn more about ACLs, see [Access Control List \(ACL\) Overview](https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html) in the *Amazon Simple Storage Service Developer Guide*\.

### Other Policy Types<a name="security_iam_access-manage-other-policies"></a>

AWS supports additional, less\-common policy types\. These policy types can set the maximum permissions granted to you by the more common policy types\. 
+ **Permissions boundaries** – A permissions boundary is an advanced feature in which you set the maximum permissions that an identity\-based policy can grant to an IAM entity \(IAM user or role\)\. You can set a permissions boundary for an entity\. The resulting permissions are the intersection of entity's identity\-based policies and its permissions boundaries\. Resource\-based policies that specify the user or role in the `Principal` field are not limited by the permissions boundary\. An explicit deny in any of these policies overrides the allow\. For more information about permissions boundaries, see [Permissions Boundaries for IAM Entities](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html) in the *IAM User Guide*\.
+ **Service control policies \(SCPs\)** – SCPs are JSON policies that specify the maximum permissions for an organization or organizational unit \(OU\) in AWS Organizations\. AWS Organizations is a service for grouping and centrally managing multiple AWS accounts that your business owns\. If you enable all features in an organization, then you can apply service control policies \(SCPs\) to any or all of your accounts\. The SCP limits permissions for entities in member accounts, including each AWS account root user\. For more information about Organizations and SCPs, see [How SCPs Work](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_about-scps.html) in the *AWS Organizations User Guide*\.
+ **Session policies** – Session policies are advanced policies that you pass as a parameter when you programmatically create a temporary session for a role or federated user\. The resulting session's permissions are the intersection of the user or role's identity\-based policies and the session policies\. Permissions can also come from a resource\-based policy\. An explicit deny in any of these policies overrides the allow\. For more information, see [Session Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#policies_session) in the *IAM User Guide*\. 

### Multiple Policy Types<a name="security_iam_access-manage-multiple-policies"></a>

When multiple types of policies apply to a request, the resulting permissions are more complicated to understand\. To learn how AWS determines whether to allow a request when multiple policy types are involved, see [Policy Evaluation Logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html) in the *IAM User Guide*\.