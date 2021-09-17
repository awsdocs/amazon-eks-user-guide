# Logging and monitoring in Amazon EKS<a name="logging-monitoring"></a>

Amazon EKS control plane logging provides audit and diagnostic logs directly from the Amazon EKS control plane to CloudWatch Logs in your account\. These logs make it easy for you to secure and run your clusters\. You can select the exact log types you need, and logs are sent as log streams to a group for each Amazon EKS cluster in CloudWatch\. For more information, see [Amazon EKS Control Plane Logging](control-plane-logs.md)\.

**Note**  
When you check the Amazon EKS authenticator logs in Amazon CloudWatch, you'll see entries that contain text similar to the following example text\.  

```
level=info msg="mapping IAM role" groups="[]" role="arn:aws:iam::<111122223333:>role/<XXXXXXXXXXXXXXXXXX>-NodeManagerRole-<XXXXXXXX>" username="eks:node-manager"
```
Entries that contain this text are expected\. The `username` is an Amazon EKS internal service role that performs specific operations for managed node groups and Fargate\.

Amazon EKS is integrated with AWS CloudTrail, a service that provides a record of actions taken by a user, role, or an AWS service in Amazon EKS\. CloudTrail captures all API calls for Amazon EKS as events\. The calls captured include calls from the Amazon EKS console and code calls to the Amazon EKS API operations\. For more information, see [Logging Amazon EKS API calls with AWS CloudTrail](logging-using-cloudtrail.md)\.

The Kubernetes API server exposes a number of metrics that are useful for monitoring and analysis\. For more information, see [Control plane metrics with Prometheus](prometheus.md)\.

To configure Fluent Bit for custom Amazon CloudWatch logs, see [this page\.](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Container-Insights-setup-logs.html) 