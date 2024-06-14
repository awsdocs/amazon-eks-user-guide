# Amazon Detective<a name="integration-detective"></a>

[Amazon Detective](https://aws.amazon.com/detective/) helps you analyze, investigate, and quickly identify the root cause of security findings or suspicious activities\. Detective automatically collects log data from your AWS resources\. It then uses machine learning, statistical analysis, and graph theory to generate visualizations that help you to conduct faster and more efficient security investigations\. The Detective prebuilt data aggregations, summaries, and context help you to quickly analyze and determine the nature and extent of possible security issues\. For more information, see the [https://docs.aws.amazon.com/detective/latest/adminguide/what-is-detective.html](https://docs.aws.amazon.com/detective/latest/adminguide/what-is-detective.html)\.

Detective organizes Kubernetes and AWS data into findings such as:
+ Amazon EKS cluster details, including the IAM identity that created the cluster and the service role of the cluster\. You can investigate the AWS and Kubernetes API activity of these IAM identities with Detective\.
+ Container details, such as the image and security context\. You can also review details for terminated Pods\.
+ Kubernetes API activity, including both overall trends in API activity and details on specific API calls\. For example, you can show the number of successful and failed Kubernetes API calls that were issued during a selected time range\. Additionally, the section on newly observed API calls might be helpful to identify suspicious activity\.

Amazon EKS audit logs is an optional data source package that can be added to your Detective behavior graph\. You can view the available optional source packages, and their status in your account\. For more information, see [Amazon EKS audit logs for Detective](https://docs.aws.amazon.com/detective/latest/adminguide/source-data-types-EKS.html) in the *Amazon Detective User Guide*\.

## Use Amazon Detective with Amazon EKS<a name="integration-detective"></a>

**To review findings for an Amazon EKS cluster**

Before you can review findings, Detective must be enabled for at least 48 hours in the same AWS Region that your cluster is in\. For more information, see [Setting up Amazon Detective](https://docs.aws.amazon.com/detective/latest/adminguide/detective-setup.html) in the *Amazon Detective User Guide*\.

1. Open the Detective console at [https://console\.aws\.amazon\.com/detective/](https://console.aws.amazon.com/detective/)\.

1. From the left navigation pane, select **Search**\.

1. Select **Choose type** and then select **EKS cluster**\.

1. Enter the cluster name or ARN and then choose **Search**\.

1. In the search results, choose the name of the cluster that you want to view activity for\. For more information about what you can view, see [Overall Kubernetes API activity involving an Amazon EKS cluster](https://docs.aws.amazon.com/detective/latest/userguide/profile-panel-drilldown-kubernetes-api-volume.html) in the *Amazon Detective User Guide*\.