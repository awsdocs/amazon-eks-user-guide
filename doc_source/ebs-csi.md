# Amazon EBS CSI driver<a name="ebs-csi"></a>

The Amazon Elastic Block Store \(Amazon EBS\) Container Storage Interface \(CSI\) driver allows Amazon Elastic Kubernetes Service \(Amazon EKS\) clusters to manage the lifecycle of Amazon EBS volumes for persistent volumes\.

Here are some things to consider about using the Amazon EBS CSI driver\.
+ The Amazon EBS CSI plugin requires IAM permissions to make calls to AWS APIs on your behalf\. For more information, see [Creating the Amazon EBS CSI driver IAM role](csi-iam-role.md)\.
+ You can't mount Amazon EBS volumes to Fargate Pods\.
+ You can run the Amazon EBS CSI controller on Fargate nodes, but the Amazon EBS CSI node DaemonSet can only run on Amazon EC2 instances\.
+ Alpha features of the Amazon EBS CSI driver aren't supported on Amazon EKS clusters\.

The Amazon EBS CSI driver isn't installed when you first create a cluster\. To use the driver, you must add it as an Amazon EKS add\-on or as a self\-managed add\-on\.
+ For instructions on how to add it as an Amazon EKS add\-on, see [Managing the Amazon EBS CSI driver as an Amazon EKS add\-on](managing-ebs-csi.md)\.
+ For instructions on how to add it as a self\-managed installation, see the [Amazon EBS Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver) project on GitHub\.

After you installed the CSI driver with either method, you can test the functionality with a sample application\. For more information, see [Deploy a sample application and verify that the CSI driver is working](ebs-sample-app.md)\.