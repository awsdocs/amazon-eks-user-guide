# CSI snapshot controller<a name="csi-snapshot-controller"></a>

The Container Storage Interface \(CSI\) snapshot controller enables the use of snapshotting functionality in compatible CSI drivers, such as the Amazon EBS CSI driver\.

Here are some things to consider when using the CSI snapshot controller\. 
+ The snapshot controller must be installed alongside a CSI driver with snapshotting functionality\. The Amazon EBS CSI driver supports creating Amazon EBS snapshots of Amazon EBS CSI managed volumes\. For installation instructions, see [Amazon EBS CSI driver](ebs-csi.md)\.
+ Kubernetes doesn't support snapshots of volumes being served via CSI migration, such as Amazon EBS volumes using a `StorageClass` with provisioner `kubernetes.io/aws-ebs`\. Volumes must be created with a `StorageClass` that references the CSI driver provisioner, `ebs.csi.aws.com`\. For more information about CSI migration, see [Amazon EBS CSI migration frequently asked questions](ebs-csi-migration-faq.md)\.

We recommend that you install the CSI snapshot controller through the Amazon EKS managed add\-on\. To add an Amazon EKS add\-on to your cluster, see [Creating an add\-on](managing-add-ons.md#creating-an-add-on)\. For more information about add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\.

Alternatively, if you want a self\-managed installation of the Amazon EBS CSI snapshot controller, see [Usage](https://github.com/kubernetes-csi/external-snapshotter/blob/master/README.md#usage) in the upstream Kubernetes `external-snapshotter` on GitHub\.