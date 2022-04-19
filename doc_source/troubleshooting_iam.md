# Troubleshooting IAM<a name="troubleshooting_iam"></a>

This topic covers some common errors that you may see while using Amazon EKS with IAM and how to work around them\.

## AccessDeniedException<a name="iam-error"></a>

If you receive an `AccessDeniedException` when calling an AWS API operation, then the AWS Identity and Access Management \(IAM\) user or role credentials that you are using do not have the required permissions to make that call\. 

```
An error occurred (AccessDeniedException) when calling the DescribeCluster operation: 
User: arn:aws:iam::111122223333:user/user_name is not authorized to perform: 
eks:DescribeCluster on resource: arn:aws:eks:region:111122223333:cluster/my-cluster
```

In the above example message, the user does not have permissions to call the Amazon EKS `DescribeCluster` API operation\. To provide Amazon EKS admin permissions to a user, see [Amazon EKS identity\-based policy examples](security_iam_id-based-policy-examples.md)\.

For more general information about IAM, see [Controlling access using policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_controlling.html) in the *IAM User Guide*\.

## Can't see workloads or nodes and receive an error in the AWS Management Console<a name="security-iam-troubleshoot-cannot-view-nodes-or-workloads"></a>

You may see a console error message that says `Your current user or role does not have access to Kubernetes objects on this EKS cluster`\. Make sure that the IAM entity \(user or role\) that you’re signed into the AWS Management Console with meets all of the following requirements:
+ Has an IAM policy attached to it that includes the `eks:AccessKubernetesApi` action\. For an example IAM policy, see [View nodes and workloads for all clusters in the AWS Management Console](security_iam_id-based-policy-examples.md#policy_example3)\. If you're using the IAM policy visual editor in the AWS Management Console and you don't see the `eks:AccessKubernetesApi` **Permission** listed, edit the policy's JSON and add `eks:AccessKubernetesApi` to the list of `Action`s in the JSON\.
+ Has a mapping to a Kubernetes user or group in the `aws-auth` configmap\. For more information about adding IAM users or roles to the `aws-auth` configmap, see [Enabling IAM user and role access to your cluster](add-user-role.md)\. If the user or role isn't mapped, the console error may include **Unauthorized: Verify you have access to the Kubernetes cluster**\.
+ The Kubernetes user or group that the IAM account or role is mapped to in the configmap must be a `subject` in a `rolebinding` or `clusterrolebinding` that is bound to a Kubernetes `role` or `clusterrole` that has the necessary permissions to view the Kubernetes resources\. If the user or group doesn't have the necessary permissions, the console error may include **Unauthorized: Verify you have access to the Kubernetes cluster**\. To create roles and bindings, see [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) in the Kubernetes documentation\. You can download the example manifests that create a `clusterrole` and `clusterrolebinding` or a `role` and `rolebinding` by following the instructions in the **Important** section of [View nodes and workloads for all clusters in the AWS Management Console](security_iam_id-based-policy-examples.md#policy_example3)\.

## aws\-auth ConfigMap does not grant access to the cluster<a name="security-iam-troubleshoot-ConfigMap"></a>

[AWS IAM Authenticator](https://github.com/kubernetes-sigs/aws-iam-authenticator) does not permit a path in the role ARN used in the configuration map\. Therefore, before you specify `rolearn`, remove the path\. For example, change `arn:aws:iam::111122223333:role/team/developers/eks-admin` to `arn:aws:iam::111122223333:role/eks-admin`\.

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

When you create an access key pair, you are prompted to save the access key ID and secret access key in a secure location\. The secret access key is available only at the time you create it\. If you lose your secret access key, you must add new access keys to your IAM user\. You can have a maximum of two access keys\. If you already have two, you must delete one key pair before creating a new one\. To view instructions, see [Managing access keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey) in the *IAM User Guide*\.

## I'm an administrator and want to allow others to access Amazon EKS<a name="security_iam_troubleshoot-admin-delegate"></a>

To allow others to access Amazon EKS, you must create an IAM entity \(user or role\) for the person or application that needs access\. They will use the credentials for that entity to access AWS\. You must then attach a policy to the entity that grants them the correct permissions in Amazon EKS\.

To get started right away, see [Creating your first IAM delegated user and group](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started_create-delegated-user.html) in the *IAM User Guide*\.

## I want to allow people outside of my AWS account to access my Amazon EKS resources<a name="security_iam_troubleshoot-cross-account-access"></a>

You can create a role that users in other accounts or people outside of your organization can use to access your resources\. You can specify who is trusted to assume the role\. For services that support resource\-based policies or access control lists \(ACLs\), you can use those policies to grant people access to your resources\.

To learn more, consult the following:
+ To learn whether Amazon EKS supports these features, see [How Amazon EKS works with IAM](security_iam_service-with-iam.md)\.
+ To learn how to provide access to your resources across AWS accounts that you own, see [Providing access to an IAM user in another AWS account that you own](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_aws-accounts.html) in the *IAM User Guide*\.
+ To learn how to provide access to your resources to third\-party AWS accounts, see [Providing access to AWS accounts owned by third parties](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_third-party.html) in the *IAM User Guide*\.
+ To learn how to provide access through identity federation, see [Providing access to externally authenticated users \(identity federation\)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_federated-users.html) in the *IAM User Guide*\.
+ To learn the difference between using roles and resource\-based policies for cross\-account access, see [How IAM roles differ from resource\-based policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_compare-resource-policies.html) in the *IAM User Guide*\.