# Fargate metrics<a name="monitoring-fargate-usage"></a>

**Important**  
AWS Fargate with Amazon EKS isn't available in AWS GovCloud \(US\-East\) and AWS GovCloud \(US\-West\)\.

You can collect system metrics and CloudWatch usage metrics for AWS Fargate\.

## Application metrics<a name="fargate-application-metrics"></a>

For applications running on Amazon EKS and AWS Fargate, you can use the AWS Distro for OpenTelemetry \(ADOT\)\. ADOT allows you to collect system metrics and send them to CloudWatch Container Insights dashboards\. To get started with ADOT for applications running on Fargate, see [Using CloudWatch Container Insights with AWS Distro for OpenTelemetry](https://aws-otel.github.io/docs/getting-started/container-insights) in the ADOT documentation\.

## Usage metrics<a name="fargate-usage-metrics"></a>

You can use CloudWatch usage metrics to provide visibility into your account's usage of resources\. Use these metrics to visualize your current service usage on CloudWatch graphs and dashboards\.

AWS Fargate usage metrics correspond to AWS service quotas\. You can configure alarms that alert you when your usage approaches a service quota\. For more information about Fargate service quotas, see [Amazon EKS service quotas](service-quotas.md)\.

AWS Fargate publishes the following metrics in the `AWS/Usage` namespace\.


|  Metric  |  Description  | 
| --- | --- | 
|  `ResourceCount`  |  The total number of the specified resource running on your account\. The resource is defined by the dimensions associated with the metric\.  | 

The following dimensions are used to refine the usage metrics that are published by AWS Fargate\.


|  Dimension  |  Description  | 
| --- | --- | 
|  `Service`  |  The name of the AWS service containing the resource\. For AWS Fargate usage metrics, the value for this dimension is `Fargate`\.  | 
|  `Type`  |  The type of entity that's being reported\. Currently, the only valid value for AWS Fargate usage metrics is `Resource`\.  | 
|  `Resource`  |  The type of resource that's running\. Currently, AWS Fargate returns information on your Fargate On\-Demand usage\. The resource value for Fargate On\-Demand usage is `OnDemand`\.  Fargate On\-Demand usage combines Amazon EKS Pods using Fargate, Amazon ECS tasks using the Fargate launch type and Amazon ECS tasks using the `FARGATE` capacity provider\.   | 
|  `Class`  |  The class of resource being tracked\. Currently, AWS Fargate doesn't use the class dimension\.  | 

### Creating a CloudWatch alarm to monitor Fargate resource usage metrics<a name="service-quota-alarm"></a>

AWS Fargate provides CloudWatch usage metrics that correspond to the AWS service quotas for Fargate On\-Demand resource usage\. In the Service Quotas console, you can visualize your usage on a graph\. You can also configure alarms that alert you when your usage approaches a service quota\. For more information, see [Fargate metrics](#monitoring-fargate-usage)\.

Use the following steps to create a CloudWatch alarm based on the Fargate resource usage metrics\.

**To create an alarm based on your Fargate usage quotas \(AWS Management Console\)**

1. Open the Service Quotas console at [https://console\.aws\.amazon\.com/servicequotas/](https://console.aws.amazon.com/servicequotas/)\.

1. In the left navigation pane, choose **AWS services**\.

1. From the **AWS services** list, search for and select **AWS Fargate**\.

1. In the **Service quotas** list, choose the Fargate usage quota you want to create an alarm for\.

1. In the Amazon CloudWatch alarms section, choose **Create**\.

1. For **Alarm threshold**, choose the percentage of your applied quota value that you want to set as the alarm value\.

1. For **Alarm name**, enter a name for the alarm and then choose **Create**\.