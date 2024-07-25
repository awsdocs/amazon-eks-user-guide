# Amazon CloudWatch Observability agent<a name="amazon-cloudwatch-observability"></a>

The Amazon CloudWatch Observability agent Amazon EKS add\-on the monitoring and observability service provided by AWS\. This add\-on installs the CloudWatch Agent and enables both CloudWatch Application Signals and CloudWatch Container Insights with enhanced observability for Amazon EKS\. For more information, see [Amazon CloudWatch Agent](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent.html)\.

The Amazon EKS add\-on name is `amazon-cloudwatch-observability`\.

## Required IAM permissions<a name="amazon-cloudwatch-observability-iam-permissions"></a>

This add\-on uses the [IAM roles for service accounts](iam-roles-for-service-accounts.md#iam-roles-for-service-accounts.title) capability of Amazon EKS\. The permissions in the [AWSXrayWriteOnlyAccess](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AWSXrayWriteOnlyAccess) and [CloudWatchAgentServerPolicy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy) AWS managed policies are required\. You can create an IAM role, attach the managed policies to it, and annotate the Kubernetes service account used by the add\-on with the following command\. Replace `my-cluster` with the name of your cluster and `AmazonEKS_Observability_role` with the name for your role\. This command requires that you have [https://eksctl.io](https://eksctl.io) installed on your device\. If you need to use a different tool to create the role, attach the policy to it, and annotate the Kubernetes service account, see [Assign IAM roles to Kubernetes service accounts](associate-service-account-role.md)\.

```
eksctl create iamserviceaccount \
    --name cloudwatch-agent \
    --namespace amazon-cloudwatch \
    --cluster my-cluster \
    --role-name AmazonEKS_Observability_Role \
    --role-only \
    --attach-policy-arn arn:aws:iam::aws:policy/AWSXrayWriteOnlyAccess \
    --attach-policy-arn arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy \
    --approve
```

## Additional information<a name="amazon-cloudwatch-observability-information"></a>

For more information, see [Install the CloudWatch agent](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/install-CloudWatch-Observability-EKS-addon.html)\.