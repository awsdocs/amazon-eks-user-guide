# Amazon EBS CSI driver<a name="ebs-csi"></a>

The Amazon Elastic Block Store \(Amazon EBS\) Container Storage Interface \(CSI\) driver provides a CSI interface that allows Amazon Elastic Kubernetes Service \(Amazon EKS\) clusters to manage the lifecycle of Amazon EBS volumes for persistent volumes\.

The Amazon EBS CSI driver isn't installed when you first create a cluster\. To use the driver, you must add it as an Amazon EKS add\-on or as a self\-managed add\-on\.
+ For instructions on how to add it as an Amazon EKS add\-on, see [Managing the Amazon EBS CSI driver as an Amazon EKS add\-on](managing-ebs-csi.md)\.
+ For instructions on how to add it as a self\-managed add\-on, see [Adding the Amazon EBS CSI add\-on](managing-ebs-csi.md#adding-ebs-csi-eks-add-on)\.