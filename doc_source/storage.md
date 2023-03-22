# Storage<a name="storage"></a>

This chapter covers storage options for Amazon EKS clusters\.

The [Storage classes](storage-classes.md) topic uses the in\-tree Amazon EBS storage provisioner\. 

**Note**  
The existing [in\-tree Amazon EBS plugin](https://kubernetes.io/docs/concepts/storage/volumes/#awselasticblockstore) is still supported, but by using a CSI driver, you benefit from the decoupling of Kubernetes upstream release cycle and CSI driver release cycle\. Eventually, the in\-tree plugin will be discontinued in favor of the CSI driver\. However, the CSI driver isn't supported on Fargate\.

**Topics**
+ [Storage classes](storage-classes.md)
+ [Amazon EBS CSI driver](ebs-csi.md)
+ [Amazon EFS CSI driver](efs-csi.md)
+ [Amazon FSx for Lustre CSI driver](fsx-csi.md)
+ [Amazon FSx for NetApp ONTAP CSI driver](fsx-ontap.md)
+ [Amazon File Cache CSI driver](file-cache-csi.md)