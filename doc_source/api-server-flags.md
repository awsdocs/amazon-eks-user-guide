# Viewing API server flags in the Amazon CloudWatch console<a name="api-server-flags"></a>

You can use the control plane logging feature for Amazon EKS clusters to view the API server flags that were enabled when a cluster was created\. For more information, see [Amazon EKS control plane logging](control-plane-logs.md)\. This topic shows you how to view the API server flags for an Amazon EKS cluster in the Amazon CloudWatch console\.

When a cluster is first created, the initial API server logs include the flags that were used to start the API server\. If you enable API server logs when you launch the cluster, or shortly thereafter, these logs are sent to CloudWatch Logs and you can view them there\.

**To view API server flags for a cluster**

1. If you have not already done so, enable API server logs for your Amazon EKS cluster\.

   1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

   1. Choose the name of the cluster to display your cluster information\.

   1. On the **Logging** tab, choose **Manage logging**\.

   1. For **API server**, make sure that the log type is **Enabled**\.

   1. Choose **Save changes** to finish\.

1. Open the CloudWatch console at [https://console\.aws\.amazon\.com/cloudwatch/](https://console.aws.amazon.com/cloudwatch/)

1. Choose **Logs**, then **Log groups** in the side menu\. Choose the cluster of which you want to see the logs, then choose the **Log streams** tab\.

1. In the list of log streams, find the earliest version of the `kube-apiserver-<example-ID-288ec988b77a59d70ec77>` log stream\. Use the **Last Event Time** column to determine the log stream ages\.

1. Scroll up to the earliest events \(the beginning of the log stream\)\. You should see the initial API server flags for the cluster\.
**Note**  
If you don't see the API server logs at the beginning of the log stream, then it is likely that the API server log file was rotated on the server before you enabled API server logging on the server\. Any log files that are rotated before API server logging is enabled cannot be exported to CloudWatch\.   
However, you can create a new cluster with the same Kubernetes version and enable the API server logging when you create the cluster\. Clusters with the same platform version have the same flags enabled, so your flags should match the new cluster's flags\. When you finish viewing the flags for the new cluster in CloudWatch, you can delete the new cluster\.