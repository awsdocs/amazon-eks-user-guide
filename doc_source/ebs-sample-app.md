# Deploy a sample application and verify that the CSI driver is working<a name="ebs-sample-app"></a>

You can test the CSI driver functionality with a sample application\. This topic shows one example, but you can also do the following:
+ Deploy a sample application that uses the external snapshotter to create volume snapshots\. For more information, see [Volume Snapshots](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/tree/master/examples/kubernetes/snapshot) on GitHub\.
+ Deploy a sample application that uses volume resizing\. For more information, see [Volume Resizing](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/examples/kubernetes/resizing/README.md) on GitHub\.

This procedure uses the [Dynamic volume provisioning](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/tree/master/examples/kubernetes/dynamic-provisioning) example from the [Amazon EBS Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver) GitHub repository to consume a dynamically provisioned Amazon EBS volume\.

1. Clone the [Amazon EBS Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver) GitHub repository to your local system\.

   ```
   git clone https://github.com/kubernetes-sigs/aws-ebs-csi-driver.git
   ```

1. Navigate to the `dynamic-provisioning` example directory\.

   ```
   cd aws-ebs-csi-driver/examples/kubernetes/dynamic-provisioning/
   ```

1. \(Optional\) The `manifests/storageclass.yaml` file provisions `gp2` Amazon EBS volumes by default\. To use `gp3` volumes instead, add `type: gp3` to `manifests/storageclass.yaml`\.

   ```
   echo "parameters:
     type: gp3" >> manifests/storageclass.yaml
   ```

1. Deploy the `ebs-sc` storage class, `ebs-claim` persistent volume claim, and `app` sample application from the `manifests` directory\.

   ```
   kubectl apply -f manifests/
   ```

1. Describe the `ebs-sc` storage class\.

   ```
   kubectl describe storageclass ebs-sc
   ```

   An example output is as follows\.

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
**Note**  
The storage class uses the `WaitForFirstConsumer` volume binding mode\. This means that volumes aren't dynamically provisioned until a Pod makes a persistent volume claim\. For more information, see [Volume Binding Mode](https://kubernetes.io/docs/concepts/storage/storage-classes/#volume-binding-mode) in the Kubernetes documentation\.

1. Watch the Pods in the default namespace\. After a few minutes, the `app` Pod's status changes to `Running`\.

   ```
   kubectl get pods --watch
   ```

   Enter `Ctrl`\+`C` to return to a shell prompt\.

1. List the persistent volumes in the default namespace\. Look for a persistent volume with the `default/ebs-claim` claim\.

   ```
   kubectl get pv
   ```

   An example output is as follows\.

   ```
   NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM               STORAGECLASS   REASON   AGE
   pvc-37717cd6-d0dc-11e9-b17f-06fad4858a5a   4Gi        RWO            Delete           Bound    default/ebs-claim   ebs-sc                  30s
   ```

1. Describe the persistent volume\. Replace `pvc-37717cd6-d0dc-11e9-b17f-06fad4858a5a` with the value from the output in the previous step\.

   ```
   kubectl describe pv pvc-37717cd6-d0dc-11e9-b17f-06fad4858a5a
   ```

   An example output is as follows\.

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
       Term 0:        topology.ebs.csi.aws.com/zone in [region-code]
   Message:
   Source:
       Type:              CSI (a Container Storage Interface (CSI) volume source)
       Driver:            ebs.csi.aws.com
       VolumeHandle:      vol-0d651e157c6d93445
       ReadOnly:          false
       VolumeAttributes:      storage.kubernetes.io/csiProvisionerIdentity=1567792483192-8081-ebs.csi.aws.com
   Events:                <none>
   ```

   The Amazon EBS volume ID is the value for `VolumeHandle` in the previous output\.

1. Verify that the Pod is writing data to the volume\.

   ```
   kubectl exec -it app -- cat /data/out.txt
   ```

   An example output is as follows\.

   ```
   Wed May 5 16:17:03 UTC 2021
   Wed May 5 16:17:08 UTC 2021
   Wed May 5 16:17:13 UTC 2021
   Wed May 5 16:17:18 UTC 2021
   [...]
   ```

1. After you're done, delete the resources for this sample application\.

   ```
   kubectl delete -f manifests/
   ```