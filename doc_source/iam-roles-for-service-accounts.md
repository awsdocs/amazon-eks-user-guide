# IAM roles for service accounts<a name="iam-roles-for-service-accounts"></a>

With IAM roles for service accounts on Amazon EKS clusters, you can associate an IAM role with a Kubernetes service account\. This service account can then provide AWS permissions to the containers in any pod that uses that service account\. With this feature, you no longer need to provide extended permissions to the node IAM role so that pods on that node can call AWS APIs\.

Applications must sign their AWS API requests with AWS credentials\. This feature provides a strategy for managing credentials for your applications, similar to the way that Amazon EC2 instance profiles provide credentials to Amazon EC2 instances\. Instead of creating and distributing your AWS credentials to the containers or using the Amazon EC2 instance’s role, you can associate an IAM role with a Kubernetes service account\. The applications in the pod’s containers can then use an AWS SDK or the AWS CLI to make API requests to authorized AWS services\.

The IAM roles for service accounts feature provides the following benefits:
+ **Least privilege —** By using the IAM roles for service accounts feature, you no longer need to provide extended permissions to the node IAM role so that pods on that node can call AWS APIs\. You can scope IAM permissions to a service account, and only pods that use that service account have access to those permissions\. This feature also eliminates the need for third\-party solutions such as `kiam` or `kube2iam`\.
+ **Credential isolation —** A container can only retrieve credentials for the IAM role that is associated with the service account to which it belongs\. A container never has access to credentials that are intended for another container that belongs to another pod\.
+ **Auditability —** Access and event logging is available through CloudTrail to help ensure retrospective auditing\.

To get started, see [Enabling IAM roles for service accounts on your cluster](enable-iam-roles-for-service-accounts.md)\.

For an end\-to\-end walkthrough using `eksctl`, see [Walkthrough: Updating the VPC CNI plugin to use IAM roles for service accounts](iam-roles-for-service-accounts-cni-walkthrough.md)\.