# Troubleshooting IAM<a name="security_iam_troubleshoot"></a>

This topic covers some common errors that you may see while using Amazon EKS with IAM and how to work around them\.

## AccessDeniedException<a name="iam-error"></a>

If you receive an `AccessDeniedException` when calling an AWS API operation, then the [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) credentials that you're using don't have the required permissions to make that call\. 

```
An error occurred (AccessDeniedException) when calling the DescribeCluster operation: 
User: arn:aws:iam::111122223333:user/user_name is not authorized to perform: 
eks:DescribeCluster on resource: arn:aws:eks:region:111122223333:cluster/my-cluster
```

In the previous example message, the user does not have permissions to call the Amazon EKS `DescribeCluster` API operation\. To provide Amazon EKS admin permissions to an IAM principal, see [Amazon EKS identity\-based policy examples](security_iam_id-based-policy-examples.md)\.

For more general information about IAM, see [Controlling access using policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_controlling.html) in the *IAM User Guide*\.

## Can't see **Nodes** on the **Compute** tab or anything on the **Resources** tab and you receive an error in the AWS Management Console<a name="security-iam-troubleshoot-cannot-view-nodes-or-workloads"></a>

You may see a console error message that says `Your current user or role does not have access to Kubernetes objects on this EKS cluster`\. Make sure that the [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) user that you're using the AWS Management Console with has the necessary permissions\. For more information, see [Required permissions](view-kubernetes-resources.md#view-kubernetes-resources-permissions)\.

## aws\-auth `ConfigMap` does not grant access to the cluster<a name="security-iam-troubleshoot-ConfigMap"></a>

The [AWS IAM Authenticator](https://github.com/kubernetes-sigs/aws-iam-authenticator) doesn't permit a path in the role ARN used in the `ConfigMap`\. Therefore, before you specify `rolearn`, remove the path\. For example, change `arn:aws:iam::111122223333:role/team/developers/eks-admin` to `arn:aws:iam::111122223333:role/eks-admin`\.

## I am not authorized to perform iam:PassRole<a name="security_iam_troubleshoot-passrole"></a>

If you receive an error that you're not authorized to perform the `iam:PassRole` action, your policies must be updated to allow you to pass a role to Amazon EKS\.

Some AWS services allow you to pass an existing role to that service instead of creating a new service role or service\-linked role\. To do this, you must have permissions to pass the role to the service\.

The following example error occurs when an IAM user named `marymajor` tries to use the console to perform an action in Amazon EKS\. However, the action requires the service to have permissions that are granted by a service role\. Mary does not have permissions to pass the role to the service\.

```
User: arn:aws:iam::123456789012:user/marymajor is not authorized to perform: iam:PassRole
```

In this case, Mary's policies must be updated to allow her to perform the `iam:PassRole` action\.

If you need help, contact your AWS administrator\. Your administrator is the person who provided you with your sign\-in credentials\.

## I want to allow people outside of my AWS account to access my Amazon EKS resources<a name="security_iam_troubleshoot-cross-account-access"></a>

You can create a role that users in other accounts or people outside of your organization can use to access your resources\. You can specify who is trusted to assume the role\. For services that support resource\-based policies or access control lists \(ACLs\), you can use those policies to grant people access to your resources\.

To learn more, consult the following:
+ To learn whether Amazon EKS supports these features, see [How Amazon EKS works with IAM](security_iam_service-with-iam.md)\.
+ To learn how to provide access to your resources across AWS accounts that you own, see [Providing access to an IAM user in another AWS account that you own](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_aws-accounts.html) in the *IAM User Guide*\.
+ To learn how to provide access to your resources to third\-party AWS accounts, see [Providing access to AWS accounts owned by third parties](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_third-party.html) in the *IAM User Guide*\.
+ To learn how to provide access through identity federation, see [Providing access to externally authenticated users \(identity federation\)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_federated-users.html) in the *IAM User Guide*\.
+ To learn the difference between using roles and resource\-based policies for cross\-account access, see [How IAM roles differ from resource\-based policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_compare-resource-policies.html) in the *IAM User Guide*\.

## Pod containers receive the following error: `An error occurred (SignatureDoesNotMatch) when calling the GetCallerIdentity operation: Credential should be scoped to a valid region`<a name="security-iam-troubleshoot-wrong-sts-endpoint"></a>

Your containers receive this error if your application is explicitly making requests to the AWS STS global endpoint \(`https://sts.amazonaws`\) and your Kubernetes service account is configured to use a regional endpoint\. You can resolve the issue with one of the following options:
+ Update your application code to remove explicit calls to the AWS STS global endpoint\. 
+ Update your application code to make explicit calls to regional endpoints such as `https://sts.us-west-2.amazonaws.com`\. Your application should have redundancy built in to pick a different AWS Region in the event of a failure of the service in the AWS Region\. For more information, see [Managing AWS STS in an AWS Region](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_enable-regions.html) in the IAM User Guide\.
+ Configure your service accounts to use the global endpoint\. All versions earlier than `1.22` used the global endpoint by default, but version `1.22` and later clusters use the regional endpoint by default\. For more information, see [Configure the AWS Security Token Service endpoint for a service account](configure-sts-endpoint.md)\.