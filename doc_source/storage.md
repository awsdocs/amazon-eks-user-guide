# Storage<a name="storage"></a>

This chapter covers storage options for Amazon EKS clusters\.

The [Storage Classes](storage-classes.md) topic uses the in\-tree Amazon EBS storage provisioner\. For Kubernetes 1\.14 and above clusters, the [Amazon EBS CSI Driver](ebs-csi.md) is available for managing storage\.

**Note**  
The existing [in\-tree Amazon EBS plugin](https://kubernetes.io/docs/concepts/storage/volumes/#awselasticblockstore) is still supported, but by using a CSI driver, you benefit from the decoupling of Kubernetes upstream release cycle and CSI driver release cycle\. Eventually, the in\-tree plugin will be deprecated in favor of the CSI driver\.

**Topics**
+ [Storage Classes](storage-classes.md)
+ [Amazon EBS CSI Driver](ebs-csi.md)