# Amazon EFS CSI driver<a name="efs-csi"></a>

The [Amazon EFS Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-efs-csi-driver) provides a CSI interface that allows Kubernetes clusters running on AWS to manage the lifecycle of Amazon EFS file systems\.

This topic shows you how to deploy the Amazon EFS CSI Driver to your Amazon EKS cluster and verify that it works\.

**Note**  
Alpha features of the Amazon EFS CSI Driver are not supported on Amazon EKS clusters\.

For detailed descriptions of the available parameters and complete examples that demonstrate the driver's features, see the [Amazon EFS Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-efs-csi-driver) project on GitHub\.

**To deploy the Amazon EFS CSI driver to an Amazon EKS cluster**
+ Deploy the Amazon EFS CSI driver\. If your cluster contains nodes \(it can also include AWS Fargate pods\), then deploy the driver with the following command\.
**Note**  
This command requires `kubectl` version 1\.14 or later\. You can see your `kubectl` version with the following command\. To install or upgrade your `kubectl` version, see [Installing `kubectl`](install-kubectl.md)\.  

  ```
  kubectl version --client --short
  ```

  ```
  kubectl apply -k "github.com/kubernetes-sigs/aws-efs-csi-driver/deploy/kubernetes/overlays/stable/ecr/?ref=release-1.0"
  ```

  If your cluster contains only Fargate pods \(no nodes\), then deploy the driver with the following command\.

  ```
  kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-efs-csi-driver/master/deploy/kubernetes/base/csidriver.yaml
  ```
**Note**  
Starting with the 1\.0\.0 release, encryption of data in transit using TLS is enabled by default\. Using [encryption in transit](http://aws.amazon.com/blogs/aws/new-encryption-of-data-in-transit-for-amazon-efs/), data will be encrypted during its transition over the network to the Amazon EFS service\. To disable it and mount volumes using NFSv4, set the `volumeAttributes` field `encryptInTransit` to `"false"` in your persistent volume manifest\. For an example manifest, see [Encryption in Transit example](https://github.com/kubernetes-sigs/aws-efs-csi-driver/blob/master/examples/kubernetes/encryption_in_transit/specs/pv.yaml) on GitHub\.
Only static volume provisioning is supported\. This means that an Amazon EFS file system needs to be created outside of Amazon EKS before being used by pods in your cluster\.

**Amazon EFS access points**  
The Amazon EFS CSI driver supports [Amazon EFS access points](https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html), which are application\-specific entry points into an Amazon EFS file system that make it easier to share a file system between multiple pods\. Access points can enforce a user identity for all file system requests that are made through the access point, and enforce a root directory for each pod\. For more information, see [Amazon EFS access points](https://github.com/kubernetes-sigs/aws-efs-csi-driver/blob/master/examples/kubernetes/access_points/README.md) on GitHub\.

**To create an Amazon EFS file system for your Amazon EKS cluster**

1. Locate the VPC ID for your Amazon EKS cluster\. You can find this ID in the Amazon EKS console, or you can use the following AWS CLI command\.

   ```
   aws eks describe-cluster --name <cluster_name> --query "cluster.resourcesVpcConfig.vpcId" --output text
   ```

   Output:

   ```
   vpc-<exampledb76d3e813>
   ```

1. Locate the CIDR range for your cluster's VPC\. You can find this in the Amazon VPC console, or you can use the following AWS CLI command\.

   ```
   aws ec2 describe-vpcs --vpc-ids vpc-<exampledb76d3e813> --query "Vpcs[].CidrBlock" --output text
   ```

   Output:

   ```
   192.168.0.0/16
   ```

1. Create a security group that allows inbound NFS traffic for your Amazon EFS mount points\.

   1. Open the Amazon VPC console at [https://console\.aws\.amazon\.com/vpc/](https://console.aws.amazon.com/vpc/)\.

   1. Choose **Security Groups** in the left navigation panel, and then choose **Create security group**\.

   1. Enter a name and description for your security group, and choose the VPC that your Amazon EKS cluster is using\.

   1. Under **Inbound rules**, select **Add rule**\.

   1. Under **Type**, select **NFS**\.

   1.  Under **Source**, select **Custom**, and paste the VPC CIDR range that you obtained in the previous step\.

   1. Choose **Create security group**\.

1. Create the Amazon EFS file system for your Amazon EKS cluster\.

   1. Open the Amazon Elastic File System console at [https://console\.aws\.amazon\.com/efs/](https://console.aws.amazon.com/efs/)\.

   1. Choose **File systems** in the left navigation pane, and then choose **Create file system**\.

   1. On the **Create file system** page, choose **Customize**\.

   1. On the **File system settings** page, you don't need to enter or select any information, but can if desired, and then select **Next**\.

   1. On the **Network access** page, for **Virtual Private Cloud \(VPC\)**, choose your VPC\.
**Note**  
If you don't see your VPC, at the top right of the console, make sure that the region that your VPC is in is selected\.

   1. Under **Mount targets**, if a default security group is already listed, select the **X** in the top right corner of the box with the default security group name to remove it from each mount point, select the security group that you created in a previous step for each mount target, and then select **Next**\.

   1. On the **File system policy** page, select **Next**\.

   1. On the **Review and create** page, select **Create**\.
**Important**  
By default, new Amazon EFS file systems are owned by `root:root`, and only the `root` user \(UID 0\) has read\-write\-execute permissions\. If your containers are not running as `root`, you must change the Amazon EFS file system permissions to allow other users to modify the file system\. For more information, see [Working with users, groups, and permissions at the Network File System \(NFS\) level](https://docs.aws.amazon.com/efs/latest/ug/accessing-fs-nfs-permissions.html) in the *Amazon Elastic File System User Guide*\.

**To deploy a sample application and verify that the CSI driver is working**

This procedure uses the [Multiple Pods Read Write Many](https://github.com/kubernetes-sigs/aws-efs-csi-driver/tree/master/examples/kubernetes/multiple_pods) example from the [Amazon EFS Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-efs-csi-driver) GitHub repository to consume a statically provisioned Amazon EFS persistent volume and access it from multiple pods with the `ReadWriteMany` access mode\.

1. Clone the [Amazon EFS Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-efs-csi-driver) GitHub repository to your local system\.

   ```
   git clone https://github.com/kubernetes-sigs/aws-efs-csi-driver.git
   ```

1. Navigate to the `multiple_pods` example directory\.

   ```
   cd aws-efs-csi-driver/examples/kubernetes/multiple_pods/
   ```

1. Retrieve your Amazon EFS file system ID\. You can find this in the Amazon EFS console, or use the following AWS CLI command\.

   ```
   aws efs describe-file-systems --query "FileSystems[*].FileSystemId" --output text
   ```

   Output:

   ```
   fs-<582a03f3>
   ```

1. Edit the `specs/pv.yaml` file and replace the `volumeHandle` value with your Amazon EFS file system ID\.

   ```
   apiVersion: v1
   kind: PersistentVolume
   metadata:
     name: efs-pv
   spec:
     capacity:
       storage: <5Gi>
     volumeMode: Filesystem
     accessModes:
       - ReadWriteMany
     persistentVolumeReclaimPolicy: Retain
     storageClassName: efs-sc
     csi:
       driver: efs.csi.aws.com
       volumeHandle: fs-<582a03f3>
   ```
**Note**  
Because Amazon EFS is an elastic file system, it does not enforce any file system capacity limits\. The actual storage capacity value in persistent volumes and persistent volume claims is not used when creating the file system\. However, since storage capacity is a required field in Kubernetes, you must specify a valid value, such as, <5Gi> in this example\. This value does not limit the size of your Amazon EFS file system\.

1. Deploy the `efs-sc` storage class, `efs-claim` persistent volume claim, `efs-pv` persistent volume, and `app1` and `app2` sample applications from the `specs` directory\.

   ```
   kubectl apply -f specs/
   ```

1. Watch the pods in the default namespace and wait for the `app1` and `app2` pods' `STATUS` become `Running`\.

   ```
   kubectl get pods --watch
   ```
**Note**  
It may take a few minutes for the pods to reach the `Running` status\.

1. List the persistent volumes in the default namespace\. Look for a persistent volume with the `default/efs-claim` claim\.

   ```
   kubectl get pv
   ```

   Output:

   ```
   NAME     CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM               STORAGECLASS   REASON   AGE
   efs-pv   5Gi        RWX            Retain           Bound    default/efs-claim   efs-sc                  2m50s
   ```

1. Describe the persistent volume\.

   ```
   kubectl describe pv efs-pv
   ```

   Output:

   ```
   Name:            efs-pv
   Labels:          <none>
   Annotations:     kubectl.kubernetes.io/last-applied-configuration:
                      {"apiVersion":"v1","kind":"PersistentVolume","metadata":{"annotations":{},"name":"efs-pv"},"spec":{"accessModes":["ReadWriteMany"],"capaci...
                    pv.kubernetes.io/bound-by-controller: yes
   Finalizers:      [kubernetes.io/pv-protection]
   StorageClass:    efs-sc
   Status:          Bound
   Claim:           default/efs-claim
   Reclaim Policy:  Retain
   Access Modes:    RWX
   VolumeMode:      Filesystem
   Capacity:        5Gi
   Node Affinity:   <none>
   Message:
   Source:
       Type:              CSI (a Container Storage Interface (CSI) volume source)
       Driver:            efs.csi.aws.com
       VolumeHandle:      fs-<582a03f3>
       ReadOnly:          false
       VolumeAttributes:  <none>
   Events:                <none>
   ```

   The Amazon EFS file system ID is listed as the `VolumeHandle`\.

1. Verify that the `app1` pod is successfully writing data to the volume\.

   ```
   kubectl exec -ti app1 -- tail /data/out1.txt
   ```

   Output:

   ```
   Thu Jul 23 21:44:02 UTC 2020
   Thu Jul 23 21:44:07 UTC 2020
   Thu Jul 23 21:44:12 UTC 2020
   Thu Jul 23 21:44:17 UTC 2020
   Thu Jul 23 21:44:22 UTC 2020
   Thu Jul 23 21:44:27 UTC 2020
   ```

1. Verify that the `app2` pod is shows the same data in the volume\.

   ```
   kubectl exec -ti app2 -- tail /data/out1.txt
   ```

   Output:

   ```
   Thu Jul 23 21:44:47 UTC 2020
   Thu Jul 23 21:44:52 UTC 2020
   Thu Jul 23 21:44:57 UTC 2020
   Thu Jul 23 21:45:02 UTC 2020
   Thu Jul 23 21:45:07 UTC 2020
   Thu Jul 23 21:45:12 UTC 2020
   ```

1. When you finish experimenting, delete the resources for this sample application to clean up\.

   ```
   kubectl delete -f specs/
   ```