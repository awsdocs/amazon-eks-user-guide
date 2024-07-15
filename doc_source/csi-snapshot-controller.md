# Use snapshot controller with CSI storage<a name="csi-snapshot-controller"></a>

When using a Container Storage Interface \(CSI\), snapshot functionality allows for point\-in\-time copies of your data\. For this capability to work in Kubernetes, you need both a CSI driver with snapshot support \(such as the Amazon EBS CSI driver\) and a CSI snapshot controller\. The snapshot controller is available either as an Amazon EKS managed add\-on or as a self\-managed installation\.

Here are some things to consider when using the CSI snapshot controller\.
+ The snapshot controller must be installed alongside a CSI driver with snapshot functionality\. For example, the Amazon EBS CSI driver implements snapshotting as a separate container named `csi-snapshotter`\. This container can create Amazon EBS snapshots of Amazon EBS CSI managed volumes\. For installation instructions of the Amazon EBS CSI driver, see [Use Amazon EBS storage](ebs-csi.md)\.
+ Kubernetes doesn't support snapshots of volumes being served via CSI migration, such as Amazon EBS volumes using a `StorageClass` with provisioner `kubernetes.io/aws-ebs`\. Volumes must be created with a `StorageClass` that references the CSI driver provisioner, `ebs.csi.aws.com`\. For more information about CSI migration, see [Amazon EBS CSI migration frequently asked questions](ebs-csi-migration-faq.md)\.

We recommend that you install the CSI snapshot controller through the Amazon EKS managed add\-on\. To add an Amazon EKS add\-on to your cluster, see [Creating an add\-on](managing-add-ons.md#creating-an-add-on)\. For more information about add\-ons, see [Use AWSAPIs to install/update cluster components with EKS add\-ons](eks-add-ons.md)\.

Alternatively, if you want a self\-managed installation of the Amazon EBS CSI snapshot controller, see [Usage](https://github.com/kubernetes-csi/external-snapshotter/blob/master/README.md#usage) in the upstream Kubernetes `external-snapshotter` on GitHub\.