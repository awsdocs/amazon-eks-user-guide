# Amazon EKS control plane logging<a name="control-plane-logs"></a>

Amazon EKS control plane logging provides audit and diagnostic logs directly from the Amazon EKS control plane to CloudWatch Logs in your account\. These logs make it easy for you to secure and run your clusters\. You can select the exact log types you need, and logs are sent as log streams to a group for each Amazon EKS cluster in CloudWatch\.

You can start using Amazon EKS control plane logging by choosing which log types you want to enable for each new or existing Amazon EKS cluster\. You can enable or disable each log type on a per\-cluster basis using the AWS Management Console, AWS CLI \(version 1\.16\.139 or higher\), or through the Amazon EKS API\. When enabled, logs are automatically sent from the Amazon EKS cluster to CloudWatch Logs in the same account\.

When you use Amazon EKS control plane logging, you're charged standard Amazon EKS pricing for each cluster that you run\. You are charged the standard CloudWatch Logs data ingestion and storage costs for any logs sent to CloudWatch Logs from your clusters\. You are also charged for any AWS resources, such as Amazon EC2 instances or Amazon EBS volumes, that you provision as part of your cluster\.

The following cluster control plane log types are available\. Each log type corresponds to a component of the Kubernetes control plane\. To learn more about these components, see [Kubernetes Components](https://kubernetes.io/docs/concepts/overview/components/) in the Kubernetes documentation\.
+ **Kubernetes API server component logs \(`api`\)** – Your cluster's API server is the control plane component that exposes the Kubernetes API\. For more information, see [kube\-apiserver](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/) in the Kubernetes documentation\.
+ **Audit \(`audit`\)** – Kubernetes audit logs provide a record of the individual users, administrators, or system components that have affected your cluster\. For more information, see [Auditing](https://kubernetes.io/docs/tasks/debug-application-cluster/audit/) in the Kubernetes documentation\.
+ **Authenticator \(`authenticator`\)** – Authenticator logs are unique to Amazon EKS\. These logs represent the control plane component that Amazon EKS uses for Kubernetes [Role Based Access Control](https://kubernetes.io/docs/admin/authorization/rbac/) \(RBAC\) authentication using IAM credentials\. For more information, see [Cluster authentication](managing-auth.md)\.
+ **Controller manager \(`controllerManager`\)** – The controller manager manages the core control loops that are shipped with Kubernetes\. For more information, see [kube\-controller\-manager](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/) in the Kubernetes documentation\.
+ **Scheduler \(`scheduler`\)** – The scheduler component manages when and where to run pods in your cluster\. For more information, see [kube\-scheduler](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-scheduler/) in the Kubernetes documentation\.

## Enabling and disabling control plane logs<a name="enabling-control-plane-log-export"></a>

By default, cluster control plane logs aren't sent to CloudWatch Logs\. You must enable each log type individually to send logs for your cluster\. CloudWatch Logs ingestion, archive storage, and data scanning rates apply to enabled control plane logs\. For more information, see [CloudWatch pricing](http://aws.amazon.com/cloudwatch/pricing/)\.

When you enable a log type, the logs are sent with a log verbosity level of `2`\. 

**To enable or disable control plane logs with the console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the name of the cluster to display your cluster information\.

1. Select the **Configuration** tab\.

1. Under **Logging**, choose **Update**\.

1. For each individual log type, choose whether the log type should be **Enabled** or **Disabled**\. By default, each log type is **Disabled**\.

1. Choose **Update** to finish\.

**To enable or disable control plane logs with the AWS CLI**

1. Check your AWS CLI version with the following command\.

   ```
   aws --version
   ```

   If your AWS CLI version is below 1\.16\.139, you must first update to the latest version\. To install or upgrade the AWS CLI, see [Installing the AWS command line interface](https://docs.aws.amazon.com/cli/latest/userguide/installing.html) in the *AWS Command Line Interface User Guide*\.

1. Update your cluster's control plane log export configuration with the following AWS CLI command\. Substitute your cluster name and desired endpoint access values\.
**Note**  
The following command sends all available log types to CloudWatch Logs\.

   ```
   aws eks --region <region-code> update-cluster-config --name <prod> \
   --logging '{"clusterLogging":[{"types":["api","audit","authenticator","controllerManager","scheduler"],"enabled":true}]}'
   ```

   Output:

   ```
   {
       "update": {
           "id": "<883405c8-65c6-4758-8cee-2a7c1340a6d9>",
           "status": "InProgress",
           "type": "LoggingUpdate",
           "params": [
               {
                   "type": "ClusterLogging",
                   "value": "{\"clusterLogging\":[{\"types\":[\"api\",\"audit\",\"authenticator\",\"controllerManager\",\"scheduler\"],\"enabled\":true}]}"
               }
           ],
           "createdAt": 1553271814.684,
           "errors": []
       }
   }
   ```

1. Monitor the status of your log configuration update with the following command, using the cluster name and the update ID that were returned by the previous command\. Your update is complete when the status appears as `Successful`\.

   ```
   aws eks --region <region-code> describe-update --name <prod> --update-id <883405c8-65c6-4758-8cee-2a7c1340a6d9>
   ```

   Output:

   ```
   {
       "update": {
           "id": "<883405c8-65c6-4758-8cee-2a7c1340a6d9>",
           "status": "Successful",
           "type": "LoggingUpdate",
           "params": [
               {
                   "type": "ClusterLogging",
                   "value": "{\"clusterLogging\":[{\"types\":[\"api\",\"audit\",\"authenticator\",\"controllerManager\",\"scheduler\"],\"enabled\":true}]}"
               }
           ],
           "createdAt": 1553271814.684,
           "errors": []
       }
   }
   ```

## Viewing cluster control plane logs<a name="viewing-control-plane-logs"></a>

After you have enabled any of the control plane log types for your Amazon EKS cluster, you can view them on the CloudWatch console\.

To learn more about viewing, analyzing, and managing logs in CloudWatch, see the [Amazon CloudWatch Logs User Guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/)\.

**To view your cluster control plane logs on the CloudWatch console**

1. Open the CloudWatch console at [https://console\.aws\.amazon\.com/cloudwatch/home\#logs:prefix=/aws/eks](https://console.aws.amazon.com/cloudwatch/home#logs:prefix=/aws/eks)\. This URL displays your current available log groups and filters them with the `/aws/eks` prefix\.

1. Choose the cluster that you want to view logs for\. The log group name format is `/aws/eks/<cluster-name>/cluster`\.

1. Choose the log stream to view\. The following list describes the log stream name format for each log type\.
**Note**  
As log stream data grows, the log stream names are rotated\. When multiple log streams exist for a particular log type, you can view the latest log stream by looking for the log stream name with the latest **Last Event Time**\.
   + **Kubernetes API server component logs \(`api`\)** – `kube-apiserver-<nnn...>`
   + **Audit \(`audit`\)** – `kube-apiserver-audit-<nnn...>`
   + **Authenticator \(`authenticator`\)** – `authenticator-<nnn...>`
   + **Controller manager \(`controllerManager`\)** – `kube-controller-manager-<nnn...>`
   + **Scheduler \(`scheduler`\)** – `kube-scheduler-<nnn...>`