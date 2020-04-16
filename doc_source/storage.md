# Storage<a name="storage"></a>

This chapter covers storage options for Amazon EKS clusters\.

The [Storage classes](storage-classes.md) topic uses the in\-tree Amazon EBS storage provisioner\. The [Amazon EBS CSI driver](ebs-csi.md) is available for managing storage in Kubernetes 1\.14 and later clusters\.

**Note**  
The existing [in\-tree Amazon EBS plugin](https://kubernetes.io/docs/concepts/storage/volumes/#awselasticblockstore) is still supported, but by using a CSI driver, you benefit from the decoupling of Kubernetes upstream release cycle and CSI driver release cycle\. Eventually, the in\-tree plugin will be deprecated in favor of the CSI driver\.

**Topics**
+ [Storage classes](storage-classes.md)
+ [Amazon EBS CSI driver](ebs-csi.md)
+ [Amazon EFS CSI driver](efs-csi.md)
+ [Amazon FSx for Lustre CSI driver](fsx-csi.md)