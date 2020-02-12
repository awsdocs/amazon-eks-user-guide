# IAM Roles for Service Accounts<a name="iam-roles-for-service-accounts"></a>

With IAM roles for service accounts on Amazon EKS clusters, you can associate an IAM role with a Kubernetes service account\. This service account can then provide AWS permissions to the containers in any pod that uses that service account\. With this feature, you no longer need to provide extended permissions to the worker node IAM role so that pods on that node can call AWS APIs\.

Applications must sign their AWS API requests with AWS credentials\. This feature provides a strategy for managing credentials for your applications, similar to the way that Amazon EC2 instance profiles provide credentials to Amazon EC2 instances\. Instead of creating and distributing your AWS credentials to the containers or using the Amazon EC2 instance’s role, you can associate an IAM role with a Kubernetes service account\. The applications in the pod’s containers can then use an AWS SDK or the AWS CLI to make API requests to authorized AWS services\.

The IAM roles for service accounts feature provides the following benefits:
+ **Least privilege —** By using the IAM roles for service accounts feature, you no longer need to provide extended permissions to the worker node IAM role so that pods on that node can call AWS APIs\. You can scope IAM permissions to a service account, and only pods that use that service account have access to those permissions\. This feature also eliminates the need for third\-party solutions such as `kiam` or `kube2iam`\.
+ **Credential isolation —** A container can only retrieve credentials for the IAM role that is associated with the service account to which it belongs\. A container never has access to credentials that are intended for another container that belongs to another pod\.
+ **Auditability —** Access and event logging is available through CloudTrail to help ensure retrospective auditing\.

To get started, see [Enabling IAM Roles for Service Accounts on your Cluster](enable-iam-roles-for-service-accounts.md)\.

For an end\-to\-end walkthrough using `eksctl`, see [Walkthrough: Updating a DaemonSet to Use IAM for Service Accounts](iam-roles-for-service-accounts-cni-walkthrough.md)\.

**Topics**
+ [IAM Roles for Service Accounts Technical Overview](iam-roles-for-service-accounts-technical-overview.md)
+ [Using a Supported AWS SDK](iam-roles-for-service-accounts-minimum-sdk.md)
+ [Enabling IAM Roles for Service Accounts on your Cluster](enable-iam-roles-for-service-accounts.md)
+ [Creating an IAM Role and Policy for your Service Account](create-service-account-iam-policy-and-role.md)
+ [Specifying an IAM Role for your Service Account](specify-service-account-role.md)
+ [Restricting Access to Amazon EC2 Instance Profile Credentials](restrict-ec2-credential-access.md)
+ [Walkthrough: Updating a DaemonSet to Use IAM for Service Accounts](iam-roles-for-service-accounts-cni-walkthrough.md)