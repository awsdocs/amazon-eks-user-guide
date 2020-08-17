# Amazon EBS CSI driver<a name="ebs-csi"></a>

The [Amazon EBS Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver) provides a CSI interface that allows Amazon EKS clusters to manage the lifecycle of Amazon EBS volumes for persistent volumes\.

This topic shows you how to deploy the Amazon EBS CSI Driver to your Amazon EKS cluster and verify that it works\. We recommend using version v0\.5\.0 of the driver\.

**Note**  
This driver is only supported on Kubernetes version 1\.14 and later Amazon EKS clusters and nodes\. The driver is not supported on Fargate or Arm nodes\. Alpha features of the Amazon EBS CSI Driver are not supported on Amazon EKS clusters\. The driver is in Beta release\. It is well tested and supported by Amazon EKS for production use\. Support for the driver will not be dropped, though details may change\. If the schema or schematics of the driver changes, instructions for migrating to the next version will be provided\.

For detailed descriptions of the available parameters and complete examples that demonstrate the driver's features, see the [Amazon EBS Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver) project on GitHub\.

**To deploy the Amazon EBS CSI driver to an Amazon EKS cluster**

1. Create an IAM policy called `Amazon_EBS_CSI_Driver` for your node instance profile that allows the Amazon EBS CSI Driver to make calls to AWS APIs on your behalf\. Use the following AWS CLI commands to create the IAM policy in your AWS account\. You can view the policy document [on GitHub](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/v0.5.0/docs/example-iam-policy.json)\.

   1. Download the policy document from GitHub\.

      ```
      curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-ebs-csi-driver/v0.5.0/docs/example-iam-policy.json
      ```

   1. Create the policy\.

      ```
      aws iam create-policy --policy-name Amazon_EBS_CSI_Driver \
          --policy-document file://example-iam-policy.json
      ```

   Take note of the policy ARN that is returned\.

1. Get the IAM role name for your nodes\. Use the following command to print the `aws-auth` configmap\.

   ```
   kubectl -n kube-system describe configmap aws-auth
   ```

   Output:

   ```
   Name:         aws-auth
   Namespace:    kube-system
   Labels:       <none>
   Annotations:  <none>
   
   Data
   ====
   mapRoles:
   ----
   - groups:
     - system:bootstrappers
     - system:nodes
     rolearn: arn:aws:iam::111122223333:role/eksctl-alb-nodegroup-ng-b1f603c5-NodeInstanceRole-GKNS581EASPU
     username: system:node:{{EC2PrivateDNSName}}
   
   Events:  <none>
   ```

   Record the role name for any `rolearn` values that have the `system:nodes` group assigned to them\. In the previous example output, the role name is *eksctl\-alb\-nodegroup\-ng\-b1f603c5\-NodeInstanceRole\-GKNS581EASPU*\. You should have one value for each node group in your cluster\.

1. Attach the new `Amazon_EBS_CSI_Driver` IAM policy to each of the node IAM roles you identified earlier with the following command, substituting the red text with your own AWS account number and node IAM role name\.

   ```
   aws iam attach-role-policy \
   --policy-arn arn:aws:iam::111122223333:policy/Amazon_EBS_CSI_Driver \
   --role-name eksctl-alb-nodegroup-ng-b1f603c5-NodeInstanceRole-GKNS581EASPU
   ```

1. Deploy the Amazon EBS CSI Driver with the following command\.
**Note**  
This command requires version 1\.14 or later of `kubectl`\. You can see your `kubectl` version with the following command\. To install or upgrade your `kubectl` version, see [Installing `kubectl`](install-kubectl.md)\.  

   ```
   kubectl version --client --short
   ```

   ```
   kubectl apply -k "github.com/kubernetes-sigs/aws-ebs-csi-driver/deploy/kubernetes/overlays/stable/?ref=master"
   ```

**To deploy a sample application and verify that the CSI driver is working**

This procedure uses the [Dynamic volume provisioning](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/tree/master/examples/kubernetes/dynamic-provisioning) example from the [Amazon EBS Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver) GitHub repository to consume a dynamically\-provisioned Amazon EBS volume\.

1. Clone the [Amazon EBS Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver) GitHub repository to your local system\.

   ```
   git clone https://github.com/kubernetes-sigs/aws-ebs-csi-driver.git
   ```

1. Navigate to the `dynamic-provisioning` example directory\.

   ```
   cd aws-ebs-csi-driver/examples/kubernetes/dynamic-provisioning/
   ```

1. Deploy the `ebs-sc` storage class, `ebs-claim` persistent volume claim, and `app` sample application from the `specs` directory\.

   ```
   kubectl apply -f specs/
   ```

1. Describe the `ebs-sc` storage class\.

   ```
   kubectl describe storageclass ebs-sc
   ```

   Output:

   ```
   Name:            ebs-sc
   IsDefaultClass:  No
   Annotations:     kubectl.kubernetes.io/last-applied-configuration={"apiVersion":"storage.k8s.io/v1","kind":"StorageClass","metadata":{"annotations":{},"name":"ebs-sc"},"provisioner":"ebs.csi.aws.com","volumeBindingMode":"WaitForFirstConsumer"}
   
   Provisioner:           ebs.csi.aws.com
   Parameters:            <none>
   AllowVolumeExpansion:  <unset>
   MountOptions:          <none>
   ReclaimPolicy:         Delete
   VolumeBindingMode:     WaitForFirstConsumer
   Events:                <none>
   ```

   Note that the storage class uses the `WaitForFirstConsumer` volume binding mode\. This means that volumes are not dynamically provisioned until a pod makes a persistent volume claim\. For more information, see [Volume Binding Mode](https://kubernetes.io/docs/concepts/storage/storage-classes/#volume-binding-mode) in the Kubernetes documentation\.

1. Watch the pods in the default namespace and wait for the `app` pod to become ready\.

   ```
   kubectl get pods --watch
   ```

1. List the persistent volumes in the default namespace\. Look for a persistent volume with the `default/ebs-claim` claim\.

   ```
   kubectl get pv
   ```

   Output:

   ```
   NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM               STORAGECLASS   REASON   AGE
   pvc-37717cd6-d0dc-11e9-b17f-06fad4858a5a   4Gi        RWO            Delete           Bound    default/ebs-claim   ebs-sc                  30s
   ```

1. Describe the persistent volume\.

   ```
   kubectl describe pv pvc-37717cd6-d0dc-11e9-b17f-06fad4858a5a
   ```

   Output:

   ```
   Name:              pvc-37717cd6-d0dc-11e9-b17f-06fad4858a5a
   Labels:            <none>
   Annotations:       pv.kubernetes.io/provisioned-by: ebs.csi.aws.com
   Finalizers:        [kubernetes.io/pv-protection external-attacher/ebs-csi-aws-com]
   StorageClass:      ebs-sc
   Status:            Bound
   Claim:             default/ebs-claim
   Reclaim Policy:    Delete
   Access Modes:      RWO
   VolumeMode:        Filesystem
   Capacity:          4Gi
   Node Affinity:
     Required Terms:
       Term 0:        topology.ebs.csi.aws.com/zone in [regiona]
   Message:
   Source:
       Type:              CSI (a Container Storage Interface (CSI) volume source)
       Driver:            ebs.csi.aws.com
       VolumeHandle:      vol-0d651e157c6d93445
       ReadOnly:          false
       VolumeAttributes:      storage.kubernetes.io/csiProvisionerIdentity=1567792483192-8081-ebs.csi.aws.com
   Events:                <none>
   ```

   The Amazon EBS volume ID is listed as the `VolumeHandle`\.

1. Verify that the pod is successfully writing data to the volume\.

   ```
   kubectl exec -it app cat /data/out.txt
   ```

   Output:

   ```
   Wed Jul 8 13:52:09 UTC 2020
   Wed Jul 8 13:52:14 UTC 2020
   Wed Jul 8 13:52:19 UTC 2020
   Wed Jul 8 13:52:24 UTC 2020
   Wed Jul 8 13:52:29 UTC 2020
   Wed Jul 8 13:52:34 UTC 2020
   ```

1. When you finish experimenting, delete the resources for this sample application to clean up\.

   ```
   kubectl delete -f specs/
   ```