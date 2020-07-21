# Amazon EFS CSI driver<a name="efs-csi"></a>

The [Amazon EFS Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-efs-csi-driver) provides a CSI interface that allows Amazon EKS clusters to manage the lifecycle of Amazon EFS file systems\.

This topic shows you how to deploy the Amazon EFS CSI Driver to your Amazon EKS cluster and verify that it works\.

**Note**  
This driver is supported on Kubernetes version 1\.14 and later Amazon EKS clusters and nodes\. The driver is not supported on Fargate\. Alpha features of the Amazon EFS CSI Driver are not supported on Amazon EKS clusters\. The driver is in Beta release\. It is well tested and supported by Amazon EKS for production use\. Support for the driver will not be dropped, though details may change\. If the schema or schematics of the driver changes, instructions for migrating to the next version will be provided\.

For detailed descriptions of the available parameters and complete examples that demonstrate the driver's features, see the [Amazon EFS Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-efs-csi-driver) project on GitHub\.

**To deploy the Amazon EFS CSI driver to an Amazon EKS cluster**
+ Deploy the Amazon EFS CSI Driver with the following command\.
**Note**  
This command requires `kubectl` version 1\.14 or later\. You can see your `kubectl` version with the following command\. To install or upgrade your `kubectl` version, see [Installing `kubectl`](install-kubectl.md)\.  

  ```
  kubectl version --client --short
  ```

  ```
  kubectl apply -k "github.com/kubernetes-sigs/aws-efs-csi-driver/deploy/kubernetes/overlays/stable/?ref=master"
  ```
**Note**  
The previous command deploys version `0.3.0` of the driver, which does not support TLS mount options in your pod specs\.

**To create an Amazon EFS file system for your Amazon EKS cluster**

1. Locate the VPC ID for your Amazon EKS cluster\. You can find this ID in the Amazon EKS console, or you can use the following AWS CLI command\.

   ```
   aws eks describe-cluster --name cluster_name --query "cluster.resourcesVpcConfig.vpcId" --output text
   ```

   Output:

   ```
   vpc-exampledb76d3e813
   ```

1. Locate the CIDR range for your cluster's VPC\. You can find this in the Amazon VPC console, or you can use the following AWS CLI command\.

   ```
   aws ec2 describe-vpcs --vpc-ids vpc-exampledb76d3e813 --query "Vpcs[].CidrBlock" --output text
   ```

   Output:

   ```
   192.168.0.0/16
   ```

1. Create a security group that allows inbound NFS traffic for your Amazon EFS mount points\.

   1. Open the Amazon VPC console at [https://console\.aws\.amazon\.com/vpc/](https://console.aws.amazon.com/vpc/)\.

   1. Choose **Security Groups** in the left navigation pane, and then **Create security group**\.

   1. Enter a name and description for your security group, and choose the VPC that your Amazon EKS cluster is using\.

   1. Choose **Create** and then **Close** to finish\.

1. Add a rule to your security group to allow inbound NFS traffic from your VPC CIDR range\.

   1. Choose the security group that you created in the previous step\.

   1. Choose the **Inbound Rules** tab and then choose **Edit rules**\.

   1. Choose **Add Rule**, fill out the following fields, and then choose **Save rules**\.
      + **Type**: NFS
      + **Source**: Custom\. Paste the VPC CIDR range\.
      + **Description**: Add a description, such as "Allows inbound NFS traffic from within the VPC\."

1. Create the Amazon EFS file system for your Amazon EKS cluster\.

   1. Open the Amazon Elastic File System console at [https://console\.aws\.amazon\.com/efs/](https://console.aws.amazon.com/efs/)\.

   1. Choose **Create file system**\.

   1. On the **Configure file system access** page, choose the VPC that your Amazon EKS cluster is using\.

   1. For **Security groups**, add the security group that you created in the previous step to each mount target and choose **Next step**\.

   1.  Configure any optional settings for your file system, and then choose **Next step** and **Create File System** to finish\.
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
   fs-582a03f3
   ```

1. Edit the `specs/pv.yaml` file and replace the `volumeHandle` value with your Amazon EFS file system ID\.

   ```
   apiVersion: v1
   kind: PersistentVolume
   metadata:
     name: efs-pv
   spec:
     capacity:
       storage: 5Gi
     volumeMode: Filesystem
     accessModes:
       - ReadWriteMany
     persistentVolumeReclaimPolicy: Retain
     storageClassName: efs-sc
     csi:
       driver: efs.csi.aws.com
       volumeHandle: fs-582a03f3
   ```
**Note**  
Because Amazon EFS is an elastic file system, it does not enforce any file system capacity limits\. The actual storage capacity value in persistent volumes and persistent volume claims is not used when creating the file system\. However, since storage capacity is a required field in Kubernetes, you must specify a valid value, such as, *5Gi* in this example\. This value does not limit the size of your Amazon EFS file system\.

1. Deploy the `efs-sc` storage class, `efs-claim` persistent volume claim, `efs-pv` persistent volume, and `app1` and `app2` sample applications from the `specs` directory\.

   ```
   kubectl apply -f specs/
   ```

1. Watch the pods in the default namespace and wait for the `app1` and `app2` pods to become ready\.

   ```
   kubectl get pods --watch
   ```

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
       VolumeHandle:      fs-582a03f3
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
   Wed Sep 18 20:30:48 UTC 2019
   Wed Sep 18 20:30:53 UTC 2019
   Wed Sep 18 20:30:58 UTC 2019
   Wed Sep 18 20:31:03 UTC 2019
   Wed Sep 18 20:31:08 UTC 2019
   Wed Sep 18 20:31:13 UTC 2019
   ```

1. Verify that the `app2` pod is shows the same data in the volume\.

   ```
   kubectl exec -ti app2 -- tail /data/out1.txt
   ```

   Output:

   ```
   Wed Sep 18 20:30:48 UTC 2019
   Wed Sep 18 20:30:53 UTC 2019
   Wed Sep 18 20:30:58 UTC 2019
   Wed Sep 18 20:31:03 UTC 2019
   Wed Sep 18 20:31:08 UTC 2019
   Wed Sep 18 20:31:13 UTC 2019
   ```

1. When you finish experimenting, delete the resources for this sample application to clean up\.

   ```
   kubectl delete -f specs/
   ```