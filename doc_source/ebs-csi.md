# Amazon EBS CSI driver<a name="ebs-csi"></a>

The Amazon Elastic Block Store \(Amazon EBS\) Container Storage Interface \(CSI\) driver allows Amazon Elastic Kubernetes Service \(Amazon EKS\) clusters to manage the lifecycle of Amazon EBS volumes for persistent volumes\.

Here are some things to consider about using the Amazon EBS CSI driver\.
+ The Amazon EBS CSI plugin requires IAM permissions to make calls to AWS APIs on your behalf\. For more information, see [Creating the Amazon EBS CSI driver IAM role for service accounts](csi-iam-role.md)\.
+ You can run the Amazon EBS CSI controller on Fargate, but you can't mount volumes to Fargate Pods\.
+ Alpha features of the Amazon EBS CSI driver aren't supported on Amazon EKS clusters\.
+ 
**Important**  
If you have a `1.22` or earlier cluster that you currently run Pods on that use Amazon EBS volumes, and you don't currently have this driver installed on your cluster, then be sure to install this driver to your cluster *before* updating the cluster to `1.23`\. If you don't install this driver before updating your cluster to `1.23`, you might experience workload interruption\. For more information or to get answers to frequently asked questions about this requirement, see [Kubernetes 1\.23](kubernetes-versions.md#kubernetes-1.23) or [Amazon EBS CSI migration frequently asked questions](ebs-csi-migration-faq.md)\.

The Amazon EBS CSI driver isn't installed when you first create a cluster\. To use the driver, you must add it as an Amazon EKS add\-on or as a self\-managed add\-on\.
+ For instructions on how to add it as an Amazon EKS add\-on, see [Managing the Amazon EBS CSI driver as an Amazon EKS add\-on](managing-ebs-csi.md)\.
+ For instructions on how to add it as a self\-managed add\-on, see the [Amazon EBS Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver) project on GitHub\.

After you installed the CSI driver with either method, you can test the functionality with a sample application\. For more information, see [Deploy a sample application and verify that the CSI driver is working](ebs-sample-app.md)\.