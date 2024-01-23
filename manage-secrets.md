# Using AWS Secrets Manager secrets with Kubernetes<a name="manage-secrets"></a>

To show secrets from Secrets Manager and parameters from Parameter Store as files mounted in Amazon EKS Pods, you can use the AWS Secrets and Configuration Provider \(ASCP\) for the [Kubernetes Secrets Store CSI Driver](https://secrets-store-csi-driver.sigs.k8s.io/)\.

With the ASCP, you can store and manage your secrets in Secrets Manager and then retrieve them through your workloads running on Amazon EKS\. You can use IAM roles and policies to limit access to your secrets to specific Kubernetes Pods in a cluster\. The ASCP retrieves the Pod identity and exchanges the identity for an IAM role\. ASCP assumes the IAM role of the Pod, and then it can retrieve secrets from Secrets Manager that are authorized for that role\.

If you use Secrets Manager automatic rotation for your secrets, you can also use the Secrets Store CSI Driver rotation reconciler feature to ensure you are retrieving the latest secret from Secrets Manager\.

For more information, see [Using Secrets Manager secrets in Amazon EKS](https://docs.aws.amazon.com/secretsmanager/latest/userguide/integrating_csi_driver.html) in the AWS Secrets Manager User Guide\.