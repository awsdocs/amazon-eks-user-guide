# CNI Metrics Helper<a name="cni-metrics-helper"></a>

The CNI metrics helper is a tool that you can use to scrape elastic network interface and IP address information, aggregate metrics at the cluster level, and publish the metrics to Amazon CloudWatch\.

When managing an Amazon EKS cluster, you may want to know how many IP addresses have been assigned and how many are available\. The CNI metrics helper helps you to:
+ Track these metrics over time
+ Troubleshoot and diagnose issues related to IP assignment and reclamation
+ Provide insights for capacity planning

When a worker node is provisioned, the CNI plugin automatically allocates a pool of secondary IP addresses from the node’s subnet to the primary elastic network interface \(`eth0`\)\. This pool of IP addresses is known as the *warm pool*, and its size is determined by the worker node’s instance type\. For example, a `c4.large` instance can support three elastic network interfaces and nine IP addresses per interface\. The number of IP addresses available for a given pod is one less than the maximum \(of ten\) because one of the IP addresses is reserved for the elastic network interface itself\. For more information, see [IP Addresses Per Network Interface Per Instance Type](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#AvailableIpPerENI) in the *Amazon EC2 User Guide for Linux Instances*\.

As the pool of IP addresses is depleted, the plugin automatically attaches another elastic network interface to the instance and allocates another set of secondary IP addresses to that interface\. This process continues until the node can no longer support additional elastic network interfaces\.

The following metrics are collected for your cluster and exported to CloudWatch:
+ The maximum number of elastic network interfaces that the cluster can support
+ The number of elastic network interfaces have been allocated to pods
+ The number of IP addresses currently assigned to pods
+ The total and maximum numbers of IP addresses available
+ The number of ipamD errors

## Deploying the CNI Metrics Helper<a name="install-metrics-helper"></a>

The CNI metrics helper requires `cloudwatch:PutMetricData` permissions to send metric data to CloudWatch\. This section helps you to create an IAM policy with those permissions, apply it to your worker node instance role, and then deploy the CNI metrics helper\.

**To create an IAM policy for the CNI metrics helper**

1. Create a file called `allow_put_metrics_data.json` and populate it with the following policy document\.

   ```
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": "cloudwatch:PutMetricData",
         "Resource": "*"
       }
     ]
   }
   ```

1. Create an IAM policy called `CNIMetricsHelperPolicy` for your worker node instance profile that allows the CNI metrics helper to make calls to AWS APIs on your behalf\. Use the following AWS CLI command to create the IAM policy in your AWS account\.

   ```
   aws iam create-policy --policy-name CNIMetricsHelperPolicy \
   --description "Grants permission to write metrics to CloudWatch" \
   --policy-document file://allow_put_metrics_data.json
   ```

   Take note of the policy ARN that is returned\.

1. Get the IAM role name for your worker nodes\. Use the following command to print the `aws-auth` configmap\.

   ```
   kubectl -n kube-system describe configmap aws-auth
   ```

   Output:

   ```
   Name:         aws-auth
   Namespace:    kube-system
   Labels:       <none>
   Annotations:  <none>
   
   Data
   ====
   mapRoles:
   ----
   - groups:
     - system:bootstrappers
     - system:nodes
     rolearn: arn:aws:iam::111122223333:role/eksctl-prod-nodegroup-standard-wo-NodeInstanceRole-GKNS581EASPU
     username: system:node:{{EC2PrivateDNSName}}
   
   Events:  <none>
   ```

   Record the role name for any `rolearn` values that have the `system:nodes` group assigned to them\. In the above example output, the role name is *eksctl\-prod\-nodegroup\-standard\-wo\-NodeInstanceRole\-GKNS581EASPU*\. You should have one value for each node group in your cluster\.

1. Attach the new `CNIMetricsHelperPolicy` IAM policy to each of the worker node IAM roles you identified earlier with the following command, substituting the red text with your own AWS account number and worker node IAM role name\.

   ```
   aws iam attach-role-policy \
   --policy-arn arn:aws:iam::111122223333:policy/CNIMetricsHelperPolicy \
   --role-name eksctl-prod-nodegroup-standard-wo-NodeInstanceRole-GKNS581EASPU
   ```

**To deploy the CNI metrics helper**
+ Apply the CNI metrics helper manifest with the following command\.

  ```
  kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.5/config/v1.5/cni-metrics-helper.yaml
  ```

## Creating a Metrics Dashboard<a name="create-metrics-dashboard"></a>

After you have deployed the CNI metrics helper, you can view the CNI metrics in the CloudWatch console\. This topic helps you to create a dashboard for viewing your cluster's CNI metrics\.

**To create a CNI metrics dashboard**

1. Open the CloudWatch console at [https://console\.aws\.amazon\.com/cloudwatch/](https://console.aws.amazon.com/cloudwatch/)\.

1. In the left navigation, choose **Metrics**\.

1. Under **Custom Namespaces**, choose **Kubernetes**\.

1. Choose **CLUSTER\_ID**\.

1. On the **All metrics** tab, select the metrics you want to add to the dashboard\.

1. Choose **Actions**, and then **Add to dashboard**\.

1. In the **Select a dashboard** section, choose **Create new** and enter a name for your dashboard, such as "EKS\-CNI\-metrics"\.

1. In the **Select a widget type** section, choose **Number**\.

1. In the **Customize the widget title** section, enter a logical name for your dashboard title, such as "EKS CNI metrics"\.

1. Choose **Add to dashboard** to finish\. Now your CNI metrics are added to a dashboard that you can monitor, as shown below\.  
![\[EKS CNI metrics\]](http://docs.aws.amazon.com/eks/latest/userguide/images/EKS_CNI_metrics.png)