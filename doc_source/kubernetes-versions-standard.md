# Review release notes for Kubernetes versions on standard support<a name="kubernetes-versions-standard"></a>

This topic gives important changes to be aware of for each Kubernetes version in standard support\. When upgrading, carefully review the changes that have occurred between the old and new versions for your cluster\.

**Note**  
For `1.24` and later clusters, officially published Amazon EKS AMIs include `containerd` as the only runtime\. Kubernetes versions earlier than `1.24` use Docker as the default runtime\. These versions have a bootstrap flag option that you can use to test out your workloads on any supported cluster with `containerd`\. For more information, see [Amazon EKS ended support for `Dockershim`](dockershim-deprecation.md)\.

## Kubernetes 1\.30<a name="kubernetes-1.30"></a>

Kubernetes `1.30` is now available in Amazon EKS\. For more information about Kubernetes `1.30`, see the [official release announcement](https://kubernetes.io/blog/2024/04/17/kubernetes-v1-30-release/)\.

**Important**  
Starting with Amazon EKS version `1.30` or newer, any newly created managed node groups will automatically default to using Amazon Linux 2023 \(AL2023\) as the node operating system\. Previously, new node groups would default to Amazon Linux 2 \(AL2\)\. You can continue to use AL2 by choosing it as the AMI type when creating a new node group\.   
For more information about Amazon Linux, see [Comparing AL2 and AL2023](https://docs.aws.amazon.com/linux/al2023/ug/compare-with-al2.html) in the Amazon Linux User Guide\. 
For more information about specifiying the operating system for a managed node group, see [Creating a managed node group](create-managed-node-group.md)\.
+ With Amazon EKS `1.30`, the `topology.k8s.aws/zone-id` label is added to worker nodes\. You can use Availability Zone IDs \(AZ IDs\) to determine the location of resources in one account relative to the resources in another account\. For more information, see [Availability Zone IDs for your AWS resources](https://docs.aws.amazon.com/ram/latest/userguide/working-with-az-ids.html) in the *AWS RAM User Guide*\. 
+ Starting with `1.30`, Amazon EKS no longer includes the `default` annotation on the `gp2` `StorageClass` resource applied to newly created clusters\. This has no impact if you are referencing this storage class by name\. You must take action if you were relying on having a default `StorageClass` in the cluster\. You should reference the `StorageClass` by the name `gp2`\. Alternatively, you can deploy the Amazon EBS recommended default storage class by setting the `defaultStorageClass.enabled` parameter to true when installing `v1.31.0` or later of the `aws-ebs-csi-driver add-on`\. 
+ The minimum required IAM policy for the Amazon EKS cluster IAM role has changed\. The action `ec2:DescribeAvailabilityZones` is required\. For more information, see [Amazon EKS cluster IAM role](service_IAM_role.md)\.

For the complete Kubernetes `1.30` changelog, see [https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.30.md](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.30.md)\.

## Kubernetes 1\.29<a name="kubernetes-1.29"></a>

Kubernetes `1.29` is now available in Amazon EKS\. For more information about Kubernetes `1.29`, see the [official release announcement](https://kubernetes.io/blog/2023/12/13/kubernetes-v1-29-release/)\.

**Important**  
The deprecated `flowcontrol.apiserver.k8s.io/v1beta2` API version of `FlowSchema` and `PriorityLevelConfiguration` are no longer served in Kubernetes `v1.29`\. If you have manifests or client software that uses the deprecated beta API group, you should change these before you upgrade to `v1.29`\.
+ The `.status.kubeProxyVersion` field for node objects is now deprecated, and the Kubernetes project is proposing to remove that field in a future release\. The deprecated field is not accurate and has historically been managed by `kubelet` \- which does not actually know the `kube-proxy` version, or even whether `kube-proxy` is running\. If you've been using this field in client software, stop \- the information isn't reliable and the field is now deprecated\.
+ In Kubernetes `1.29` to reduce potential attack surface, the `LegacyServiceAccountTokenCleanUp` feature labels legacy auto\-generated secret\-based tokens as invalid if they have not been used for a long time \(1 year by default\), and automatically removes them if use is not attempted for a long time after being marked as invalid \(1 additional year by default\)\. To identify such tokens, a you can run: 

  ```
  kubectl get cm kube-apiserver-legacy-service-account-token-tracking -n kube-system
  ```

For the complete Kubernetes `1.29` changelog, see [https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.29.md#changelog-since-v1280](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.29.md#changelog-since-v1280)\.

## Kubernetes 1\.28<a name="kubernetes-1.28"></a>

Kubernetes `1.28` is now available in Amazon EKS\. For more information about Kubernetes `1.28`, see the [official release announcement](https://kubernetes.io/blog/2023/08/15/kubernetes-v1-28-release/)\.
+ Kubernetes `v1.28` expanded the supported skew between core node and control plane components by one minor version, from `n-2 `to `n-3`, so that node components \(`kubelet` and `kube-proxy`\) for the oldest supported minor version can work with control plane components \(`kube-apiserver`, `kube-scheduler`, `kube-controller-manager`, `cloud-controller-manager`\) for the newest supported minor version\.
+ Metrics `force_delete_pods_total` and `force_delete_pod_errors_total` in the `Pod GC Controller` are enhanced to account for all forceful pods deletion\. A reason is added to the metric to indicate whether the pod is forcefully deleted because it's terminated, orphaned, terminating with the out\-of\-service taint, or terminating and unscheduled\.
+ The `PersistentVolume (PV)` controller has been modified to automatically assign a default `StorageClass` to any unbound `PersistentVolumeClaim` with the `storageClassName` not set\. Additionally, the `PersistentVolumeClaim` admission validation mechanism within the API server has been adjusted to allow changing values from an unset state to an actual `StorageClass `name\.

For the complete Kubernetes `1.28` changelog, see [https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.28.md#changelog-since-v1270](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.28.md#changelog-since-v1270)\.