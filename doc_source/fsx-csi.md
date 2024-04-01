# Amazon FSx for Lustre CSI driver<a name="fsx-csi"></a>

The [FSx for Lustre Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-fsx-csi-driver) provides a CSI interface that allows Amazon EKS clusters to manage the lifecycle of FSx for Lustre file systems\. For more information, see the [FSx for Lustre User Guide](https://docs.aws.amazon.com/fsx/latest/LustreGuide/what-is.html)\.

This topic shows you how to deploy the FSx for Lustre CSI driver to your Amazon EKS cluster and verify that it works\. We recommend using the latest version of the driver\. For available versions, see [CSI Specification Compatibility Matrix](https://github.com/kubernetes-sigs/aws-fsx-csi-driver/blob/master/docs/README.md#csi-specification-compatibility-matrix) on GitHub\.

**Note**  
The driver isn't supported on Fargate\.

For detailed descriptions of the available parameters and complete examples that demonstrate the driver's features, see the [FSx for Lustre Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-fsx-csi-driver) project on GitHub\.

**Prerequisites**

You must have:
+ Version `2.12.3` or later or version `1.27.160` or later of the AWS Command Line Interface \(AWS CLI\) installed and configured on your device or AWS CloudShell\. To check your current version, use `aws --version | cut -d / -f2 | cut -d ' ' -f1`\. Package managers such `yum`, `apt-get`, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI\. To install the latest version, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with aws configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the *AWS Command Line Interface User Guide*\. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version\. To update it, see [Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the *AWS CloudShell User Guide*\.
+ Version `0.175.0` or later of the `eksctl` command line tool installed on your device or AWS CloudShell\. To install or update `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.
+ The `kubectl` command line tool is installed on your device or AWS CloudShell\. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster\. For example, if your cluster version is `1.28`, you can use `kubectl` version `1.27`, `1.28`, or `1.29` with it\. To install or upgrade `kubectl`, see [Installing or updating `kubectl`](install-kubectl.md)\.

The following procedures help you create a simple test cluster with the FSx for Lustre CSI driver so that you can see how it works\. We don't recommend using the testing cluster for production workloads\. For this tutorial, we recommend using the `example values`, except where it's noted to replace them\. You can replace any `example value` when completing the steps for your production cluster\. We recommend completing all steps in the same terminal because variables are set and used throughout the steps and won't exist in different terminals\.

**To deploy the FSx for Lustre CSI driver to an Amazon EKS cluster**

1. Set a few variables to use in the remaining steps\. Replace `my-csi-fsx-cluster` with the name of the test cluster you want to create and `region-code` with the AWS Region that you want to create your test cluster in\.

   ```
   export cluster_name=my-csi-fsx-cluster
   export region_code=region-code
   ```

1. Create a test cluster\.

   ```
   eksctl create cluster \
     --name $cluster_name \
     --region $region_code \
     --with-oidc \
     --ssh-access \
     --ssh-public-key my-key
   ```

   Cluster provisioning takes several minutes\. During cluster creation, you'll see several lines of output\. The last line of output is similar to the following example line\.

   ```
   [✓]  EKS cluster "my-csi-fsx-cluster" in "region-code" region is ready
   ```

1. Create a Kubernetes service account for the driver and attach the `AmazonFSxFullAccess` AWS\-managed policy to the service account with the following command\. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-West\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:`\.

   ```
   eksctl create iamserviceaccount \
     --name fsx-csi-controller-sa \
     --namespace kube-system \
     --cluster $cluster_name \
     --attach-policy-arn arn:aws:iam::aws:policy/AmazonFSxFullAccess \
     --approve \
     --role-name AmazonEKSFSxLustreCSIDriverFullAccess \
     --region $region_code
   ```

   You'll see several lines of output as the service account is created\. The last lines of output are similar to the following\.

   ```
   [ℹ]  1 task: { 
       2 sequential sub-tasks: { 
           create IAM role for serviceaccount "kube-system/fsx-csi-controller-sa",
           create serviceaccount "kube-system/fsx-csi-controller-sa",
       } }
   [ℹ]  building iamserviceaccount stack "eksctl-my-csi-fsx-cluster-addon-iamserviceaccount-kube-system-fsx-csi-controller-sa"
   [ℹ]  deploying stack "eksctl-my-csi-fsx-cluster-addon-iamserviceaccount-kube-system-fsx-csi-controller-sa"
   [ℹ]  waiting for CloudFormation stack "eksctl-my-csi-fsx-cluster-addon-iamserviceaccount-kube-system-fsx-csi-controller-sa"
   [ℹ]  created serviceaccount "kube-system/fsx-csi-controller-sa"
   ```

   Note the name of the AWS CloudFormation stack that was deployed\. In the previous example output, the stack is named `eksctl-my-csi-fsx-cluster-addon-iamserviceaccount-kube-system-fsx-csi-controller-sa`\.

1. Deploy the driver with the following command\. Replace `release-X.XX` with your desired branch\. The master branch isn't supported because it may contain upcoming features incompatible with the currently released stable version of the driver\. We recommend using the latest released version\. For a list of active branches, see [https://github.com/kubernetes-sigs/aws-fsx-csi-driver/branches/active](https://github.com/kubernetes-sigs/aws-fsx-csi-driver/branches/active) on GitHub\.
**Note**  
You can view the content being applied in [https://github.com/kubernetes-sigs/aws-fsx-csi-driver/tree/master/deploy/kubernetes/overlays/stable](https://github.com/kubernetes-sigs/aws-fsx-csi-driver/tree/master/deploy/kubernetes/overlays/stable) on GitHub\.

   ```
   kubectl apply -k "github.com/kubernetes-sigs/aws-fsx-csi-driver/deploy/kubernetes/overlays/stable/?ref=release-X.XX"
   ```

   An example output is as follows\.

   ```
   serviceaccount/fsx-csi-controller-sa created
   serviceaccount/fsx-csi-node-sa created
   clusterrole.rbac.authorization.k8s.io/fsx-csi-external-provisioner-role created
   clusterrole.rbac.authorization.k8s.io/fsx-external-resizer-role created
   clusterrolebinding.rbac.authorization.k8s.io/fsx-csi-external-provisioner-binding created
   clusterrolebinding.rbac.authorization.k8s.io/fsx-csi-resizer-binding created
   deployment.apps/fsx-csi-controller created
   daemonset.apps/fsx-csi-node created
   csidriver.storage.k8s.io/fsx.csi.aws.com created
   ```

1. Note the ARN for the role that was created\. If you didn't note it earlier and don't have it available anymore in the AWS CLI output, you can do the following to see it in the AWS Management Console\.

   1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

   1. Ensure that the console is set to the AWS Region that you created your IAM role in and then select **Stacks**\.

   1. Select the stack named `eksctl-my-csi-fsx-cluster-addon-iamserviceaccount-kube-system-fsx-csi-controller-sa`\.

   1. Select the **Outputs** tab\. The **Role1** ARN is listed on the **Outputs \(1\)** page\.

1. Patch the driver deployment to add the service account that you created earlier with the following command\. Replace the ARN with the ARN that you noted\. Replace `111122223333` with your account ID\. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-West\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:`\.

   ```
   kubectl annotate serviceaccount -n kube-system fsx-csi-controller-sa \
     eks.amazonaws.com/role-arn=arn:aws:iam::111122223333:role/AmazonEKSFSxLustreCSIDriverFullAccess --overwrite=true
   ```

   An example output is as follows\.

   ```
   serviceaccount/fsx-csi-controller-sa annotated
   ```

**To deploy a Kubernetes storage class, persistent volume claim, and sample application to verify that the CSI driver is working**

This procedure uses the [FSx for Lustre Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-fsx-csi-driver) GitHub repository to consume a dynamically\-provisioned FSx for Lustre volume\.

1. Note the security group for your cluster\. You can see it in the AWS Management Console under the **Networking** section or by using the following AWS CLI command\.

   ```
   aws eks describe-cluster --name $cluster_name --query cluster.resourcesVpcConfig.clusterSecurityGroupId
   ```

1. Create a security group for your Amazon FSx file system according to the criteria shown in [Amazon VPC Security Groups](https://docs.aws.amazon.com/fsx/latest/LustreGuide/limit-access-security-groups.html#fsx-vpc-security-groups) in the Amazon FSx for Lustre User Guide\. For the **VPC**, select the VPC of your cluster as shown under the **Networking** section\. For "the security groups associated with your Lustre clients", use your cluster security group\. You can leave the outbound rules alone to allow **All traffic**\.

1. Download the storage class manifest with the following command\.

   ```
   curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-fsx-csi-driver/master/examples/kubernetes/dynamic_provisioning/specs/storageclass.yaml
   ```

1. Edit the parameters section of the `storageclass.yaml` file\. Replace every `example value` with your own values\.

   ```
   parameters:
     subnetId: subnet-0eabfaa81fb22bcaf
     securityGroupIds: sg-068000ccf82dfba88
     deploymentType: PERSISTENT_1
     automaticBackupRetentionDays: "1"
     dailyAutomaticBackupStartTime: "00:00"
     copyTagsToBackups: "true"
     perUnitStorageThroughput: "200"
     dataCompressionType: "NONE"
     weeklyMaintenanceStartTime: "7:09:00"
     fileSystemTypeVersion: "2.12"
   ```
   + **`subnetId`** – The subnet ID that the Amazon FSx for Lustre file system should be created in\. Amazon FSx for Lustre isn't supported in all Availability Zones\. Open the Amazon FSx for Lustre console at [https://console\.aws\.amazon\.com/fsx/](https://console.aws.amazon.com/fsx/) to confirm that the subnet that you want to use is in a supported Availability Zone\. The subnet can include your nodes, or can be a different subnet or VPC:
     + You can check for the node subnets in the AWS Management Console by selecting the node group under the **Compute** section\.
     + If the subnet that you specify isn't the same subnet that you have nodes in, then your VPCs must be [connected](https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/amazon-vpc-to-amazon-vpc-connectivity-options.html), and you must ensure that you have the necessary ports open in your security groups\.
   + **`securityGroupIds`** – The ID of the security group you created for the file system\.
   + **`deploymentType` \(optional\)** – The file system deployment type\. Valid values are `SCRATCH_1`, `SCRATCH_2`, `PERSISTENT_1`, and `PERSISTENT_2`\. For more information about deployment types, see [Create your Amazon FSx for Lustre file system](https://docs.aws.amazon.com/fsx/latest/LustreGuide/getting-started-step1.html)\.
   + **other parameters \(optional\)** – For information about the other parameters, see [Edit StorageClass](https://github.com/kubernetes-sigs/aws-fsx-csi-driver/tree/master/examples/kubernetes/dynamic_provisioning#edit-storageclass) on GitHub\.

1. Create the storage class manifest\.

   ```
   kubectl apply -f storageclass.yaml
   ```

   An example output is as follows\.

   ```
   storageclass.storage.k8s.io/fsx-sc created
   ```

1. Download the persistent volume claim manifest\.

   ```
   curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-fsx-csi-driver/master/examples/kubernetes/dynamic_provisioning/specs/claim.yaml
   ```

1. \(Optional\) Edit the `claim.yaml` file\. Change `1200Gi` to one of the following increment values, based on your storage requirements and the `deploymentType` that you selected in a previous step\.

   ```
   storage: 1200Gi
   ```
   + `SCRATCH_2` and `PERSISTENT` – **1\.2 TiB**, **2\.4 TiB**, or increments of 2\.4 TiB over 2\.4 TiB\.
   + `SCRATCH_1` – **1\.2 TiB**, **2\.4 TiB**, **3\.6 TiB**, or increments of 3\.6 TiB over 3\.6 TiB\.

1. Create the persistent volume claim\.

   ```
   kubectl apply -f claim.yaml
   ```

   An example output is as follows\.

   ```
   persistentvolumeclaim/fsx-claim created
   ```

1. Confirm that the file system is provisioned\.

   ```
   kubectl describe pvc
   ```

   An example output is as follows\.

   ```
   Name:          fsx-claim
   Namespace:     default
   StorageClass:  fsx-sc
   Status:        Bound
   [...]
   ```
**Note**  
The `Status` may show as `Pending` for 5\-10 minutes, before changing to `Bound`\. Don't continue with the next step until the `Status` is `Bound`\. If the `Status` shows `Pending` for more than 10 minutes, use warning messages in the `Events` as reference for addressing any problems\.

1. Deploy the sample application\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-fsx-csi-driver/master/examples/kubernetes/dynamic_provisioning/specs/pod.yaml
   ```

1. Verify that the sample application is running\.

   ```
   kubectl get pods
   ```

   An example output is as follows\.

   ```
   NAME      READY   STATUS              RESTARTS   AGE
   fsx-app   1/1     Running             0          8s
   ```

1. Verify that the file system is mounted correctly by the application\.

   ```
   kubectl exec -ti fsx-app -- df -h
   ```

   An example output is as follows\.

   ```
   Filesystem                   Size  Used Avail Use% Mounted on
   overlay                       80G  4.0G   77G   5% /
   tmpfs                         64M     0   64M   0% /dev
   tmpfs                        3.8G     0  3.8G   0% /sys/fs/cgroup
   192.0.2.0@tcp:/abcdef01      1.1T  7.8M  1.1T   1% /data
   /dev/nvme0n1p1                80G  4.0G   77G   5% /etc/hosts
   shm                           64M     0   64M   0% /dev/shm
   tmpfs                        6.9G   12K  6.9G   1% /run/secrets/kubernetes.io/serviceaccount
   tmpfs                        3.8G     0  3.8G   0% /proc/acpi
   tmpfs                        3.8G     0  3.8G   0% /sys/firmware
   ```

1. Verify that data was written to the FSx for Lustre file system by the sample app\.

   ```
   kubectl exec -it fsx-app -- ls /data
   ```

   An example output is as follows\.

   ```
   out.txt
   ```

   This example output shows that the sample app successfully wrote the `out.txt` file to the file system\.

**Note**  
Before deleting the cluster, make sure to delete the FSx for Lustre file system\. For more information, see [Clean up resources](https://docs.aws.amazon.com/fsx/latest/LustreGuide/getting-started-step4.html) in the *FSx for Lustre User Guide*\.