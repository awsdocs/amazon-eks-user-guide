# IAM roles for service accounts<a name="iam-roles-for-service-accounts"></a>

You can associate an IAM role with a Kubernetes service account\. This service account can then provide AWS permissions to the containers in any pod that uses that service account\. With this feature, you no longer need to provide extended permissions to the [Amazon EKS node IAM role](create-node-role.md) so that pods on that node can call AWS APIs\.

Applications must sign their AWS API requests with AWS credentials\. This feature provides a strategy for managing credentials for your applications, similar to the way that Amazon EC2 instance profiles provide credentials to Amazon EC2 instances\. Instead of creating and distributing your AWS credentials to the containers or using the Amazon EC2 instance’s role, you can associate an IAM role with a Kubernetes service account\. The applications in the pod’s containers can then use an AWS SDK or the AWS CLI to make API requests to authorized AWS services\.

**Important**  
Even if you assign an IAM role to a Kubernetes service account, the pod still also has the permissions assigned to the [Amazon EKS node IAM role](create-node-role.md), unless you block pod access to the IMDS\. For more information, see [Restricting access to the IMDS and Amazon EC2 instance profile credentials](best-practices-security.md#restrict-ec2-credential-access)\.

The IAM roles for service accounts feature provides the following benefits:
+ **Least privilege —** By using the IAM roles for service accounts feature, you no longer need to provide extended permissions to the node IAM role so that pods on that node can call AWS APIs\. You can scope IAM permissions to a service account, and only pods that use that service account have access to those permissions\. This feature also eliminates the need for third\-party solutions such as `kiam` or `kube2iam`\.
+ **Credential isolation —** A container can only retrieve credentials for the IAM role that is associated with the service account to which it belongs\. A container never has access to credentials that are intended for another container that belongs to another pod\.
+ **Auditability —** Access and event logging is available through CloudTrail to help ensure retrospective auditing\.

**Enable service accounts to access AWS resources in three steps**

1. **[Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)** – You only need to do this once for a cluster\.

1. **[Create an IAM role and attach an IAM policy to it with the permissions that your service accounts need](create-service-account-iam-policy-and-role.md)** – We recommend creating separate roles for each unique collection of permissions that pods need\.

1. **[Associate an IAM role with a service account](specify-service-account-role.md)** – Complete this task for each Kubernetes service account that needs access to AWS resources\.