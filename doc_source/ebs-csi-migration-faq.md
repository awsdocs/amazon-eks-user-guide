# Amazon EBS CSI migration frequently asked questions<a name="ebs-csi-migration-faq"></a>

**Important**  
 If you have Pods running on a version `1.22` or earlier cluster, then you must install the [Amazon EBS CSI driver](ebs-csi.md) before updating your cluster to version `1.23` to avoid service interruption\. 

 The Amazon EBS container storage interface \(CSI\) migration feature moves responsibility for handling storage operations from the Amazon EBS in\-tree EBS storage provisioner to the [Amazon EBS CSI driver](ebs-csi.md)\. 

## What are CSI drivers?<a name="csi-migration-faq-csi-drivers"></a>

CSI drivers:
+ replace the Kubernetes "in\-tree" storage drivers that exist in the Kubernetes project source code\.
+ work with storage providers, such as Amazon EBS\.
+ provide a simplified plugin model that make it easier for storage providers like AWS to release features and maintain support without depending on the Kubernetes release cycle\.

For more information, see [Introduction](https://kubernetes-csi.github.io/docs/introduction.html) in the Kubernetes CSI documentation\.

## What is CSI migration?<a name="csi-migration-faq-what-is"></a>

The Kubernetes CSI Migration feature moves responsibility for handling storage operations from the existing in\-tree storage plugins, such as `kubernetes.io/aws-ebs`, to corresponding CSI drivers\. Existing `StorageClass`, `PersistentVolume` and `PersistentVolumeClaim` \(PVC\) objects continue to work, as long as the corresponding CSI driver is installed\. When the feature is enabled:
+ Existing workloads that utilize PVCs continue to function as they always have\.
+ Kubernetes passes control of all storage management operations to CSI drivers\.

For more information, see [Kubernetes`1.23`: Kubernetes In\-Tree to CSI Volume Migration Status Update](https://kubernetes.io/blog/2021/12/10/storage-in-tree-to-csi-migration-status-update/) on the Kubernetes blog\.

To help you migrate from the in\-tree plugin to CSI drivers, the `CSIMigration` and `CSIMigrationAWS` flags are enabled by default on Amazon EKS version `1.23` and later clusters\. These flags enable your cluster to translate the in\-tree APIs to their equivalent CSI APIs\. These flags are set on the Kubernetes control plane managed by Amazon EKS and in the `kubelet` settings configured in Amazon EKS optimized AMIs\. **If you have Pods using Amazon EBS volumes in your cluster, you must install the Amazon EBS CSI driver before updating your cluster to version `1.23`\.** If you don't, volume operations such as provisioning and mounting might not work as expected\. For more information, see [Amazon EBS CSI driver](ebs-csi.md)\.

**Note**  
The in\-tree `StorageClass` provisioner is named `kubernetes.io/aws-ebs`\. The Amazon EBS CSI `StorageClass` provisioner is named `ebs.csi.aws.com`\.

## Can I mount `kubernetes.io/aws-ebs StorageClass` volumes in version `1.23` and later clusters?<a name="csi-migration-faq-mounting-volumes"></a>

Yes, as long as the [Amazon EBS CSI driver](ebs-csi.md) is installed\. For newly created version `1.23` and later clusters, we recommend installing the Amazon EBS CSI driver as part of your cluster creation process\. We also recommend only using `StorageClasses` based on the `ebs.csi.aws.com` provisioner\.

If you've updated your cluster control plane to version `1.23` and haven't yet updated your nodes to `1.23`, then the `CSIMigration` and `CSIMigrationAWS` `kubelet` flags aren't enabled\. In this case, the in\-tree driver is used to mount `kubernetes.io/aws-ebs` based volumes\. The Amazon EBS CSI driver must still be installed however, to ensure that Pods using `kubernetes.io/aws-ebs` based volumes can be scheduled\. The driver is also required for other volume operations to succeed\. 

## Can I provision `kubernetes.io/aws-ebs StorageClass` volumes on Amazon EKS `1.23` and later clusters?<a name="csi-migration-faq-aws-ebs-volumes"></a>

Yes, as long as the [Amazon EBS CSI driver](ebs-csi.md) is installed\.

## Will the `kubernetes.io/aws-ebs StorageClass` provisioner ever be removed from Amazon EKS?<a name="csi-migration-faq-aws-ebs-provisioner"></a>

The `kubernetes.io/aws-ebs` `StorageClass` provisioner and `awsElasticBlockStore` volume type are no longer supported, but there are no plans to remove them\. These resources are treated as a part of the Kubernetes API\.

## How do I install the Amazon EBS CSI driver?<a name="csi-migration-faq-ebs-csi-driver"></a>

We recommend installing the [Amazon EBS CSI driver Amazon EKS add\-on](ebs-csi.md)\. When an update is required to the Amazon EKS add\-on, you initiate the update and Amazon EKS updates the add\-on for you\. If you want to manage the driver yourself, you can install it using the open source [Helm chart](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/tree/master/charts/aws-ebs-csi-driver)\.

**Important**  
The Kubernetes in\-tree Amazon EBS driver runs on the Kubernetes control plane\. It uses IAM permissions assigned to the [Amazon EKS cluster IAM role](service_IAM_role.md) to provision Amazon EBS volumes\. The Amazon EBS CSI driver runs on nodes\. The driver needs IAM permissions to provision volumes\. For more information, see [Creating the Amazon EBS CSI driver IAM role](csi-iam-role.md)\.

## How can I check whether the Amazon EBS CSI driver is installed in my cluster?<a name="csi-migration-faq-check-driver"></a>

To determine whether the driver is installed on your cluster, run the following command:

```
kubectl get csidriver ebs.csi.aws.com
```

To check if that installation is managed by Amazon EKS, run the following command:

```
aws eks list-addons --cluster-name my-cluster
```

## Will Amazon EKS prevent a cluster update to version `1.23` if I haven't already installed the Amazon EBS CSI driver?<a name="csi-migration-faq-update-prevention"></a>

No\.

## What if I forget to install the Amazon EBS CSI driver before I update my cluster to version 1\.23? Can I install the driver after updating my cluster?<a name="csi-migration-faq-driver-after-cluster-update"></a>

Yes, but volume operations requiring the Amazon EBS CSI driver will fail after your cluster update until the driver is installed\. 

## What is the default `StorageClass` applied in newly created Amazon EKS version `1.23` and later clusters?<a name="csi-migration-faq-default-storageclass"></a>

The default `StorageClass` behavior remains unchanged\. With each new cluster, Amazon EKS applies a `kubernetes.io/aws-ebs` based `StorageClass` named `gp2`\. We don't plan to ever remove this `StorageClass` from newly created clusters\. Separate from the cluster default `StorageClass`, if you create an `ebs.csi.aws.com` based `StorageClass` without specifying a volume type, the Amazon EBS CSI driver will default to using `gp3`\.

## Will Amazon EKS make any changes to `StorageClasses` already present in my existing cluster when I update my cluster to version `1.23`?<a name="csi-migration-faq-existing-storageclasses"></a>

No\.

## How do I migrate a persistent volume from the `kubernetes.io/aws-ebs``StorageClass` to `ebs.csi.aws.com` using snapshots?<a name="csi-migration-faq-migrate-using-snapshots"></a>

To migrate a persistent volume, see [Migrating Amazon EKS clusters from gp2 to gp3 EBS volumes](https://aws.amazon.com/blogs/containers/migrating-amazon-eks-clusters-from-gp2-to-gp3-ebs-volumes/) on the AWS blog\.

## How do I modify an Amazon EBS volume using annotations?<a name="csi-migration-faq-migrate-using-annotations"></a>

Starting with `aws-ebs-csi-driver` `v1.19.0-eksbuild.2`, you can modify Amazon EBS volumes using annotations within their `PersistentVolumeClaim`s \(PVC\)\. The new [volume modification](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/docs/modify-volume.md) feature is implemented as an additional sidecar, called `volumemodifier`\. For more information, see [Simplifying Amazon EBS volume migration and modification on Kubernetes using the EBS CSI Driver](https://aws.amazon.com/blogs/storage/simplifying-amazon-ebs-volume-migration-and-modification-using-the-ebs-csi-driver/) on the AWS blog\.

## Is migration supported for Windows workloads?<a name="csi-migration-faq-windows"></a>

Yes\. If you're installing the Amazon EBS CSI driver using the open source Helm chart, set `node.enableWindows` to `true`\. This is set by default if installing the Amazon EBS CSI driver as an Amazon EKS add\-on\. When creating `StorageClasses`, set the `fsType` to a Windows file system, such as `ntfs`\. Volume operations for Windows workloads are then migrated to the Amazon EBS CSI driver the same as they are for Linux workloads\.