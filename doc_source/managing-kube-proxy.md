# Working with the Kubernetes `kube-proxy` add\-on<a name="managing-kube-proxy"></a>

**Important**  
We recommend adding the Amazon EKS type of the add\-on to your cluster instead of using the self\-managed type of the add\-on\. If you're not familiar with the difference between the types, see [Amazon EKS add\-ons](eks-add-ons.md)\. For more information about adding an Amazon EKS add\-on to your cluster, see [Creating an add\-on](managing-add-ons.md#creating-an-add-on)\. If you're unable to use the Amazon EKS add\-on, we encourage you to submit an issue about why you can't to the [Containers roadmap GitHub repository](https://github.com/aws/containers-roadmap/issues)\.

The `kube-proxy` add\-on is deployed on each Amazon EC2 node in your Amazon EKS cluster\. It maintains network rules on your nodes and enables network communication to your Pods\. The add\-on isn't deployed to Fargate nodes in your cluster\. For more information, see [https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/) in the Kubernetes documentation\.

The following table lists the latest version of the Amazon EKS add\-on type for each Kubernetes version\.<a name="kube-proxy-versions"></a>


| Kubernetes version | `1.29` | `1.28` | `1.27` | `1.26` | `1.25` | `1.24` | `1.23` | 
| --- | --- | --- | --- | --- | --- | --- | --- | 
|  | v1\.29\.1\-eksbuild\.2 | v1\.28\.6\-eksbuild\.2 | v1\.27\.10\-eksbuild\.2 | v1\.26\.13\-eksbuild\.2 | v1\.25\.16\-eksbuild\.3 | v1\.24\.17\-eksbuild\.8 | v1\.23\.17\-eksbuild\.9 | 

**Important**  
An earlier version of the documentation was incorrect\. `kube-proxy` versions `v1.28.5`, `v1.27.9`, and `v1.26.12` aren't available\.  
If you're self\-managing this add\-on, the versions in the table might not be the same as the available self\-managed versions\.

There are two types of the `kube-proxy` container image available for each Amazon EKS cluster version:
+ **Default** – This image type is based on a Debian\-based Docker image that is maintained by the Kubernetes upstream community\.
+ **Minimal** – This image type is based on a [minimal base image](https://gallery.ecr.aws/eks-distro-build-tooling/eks-distro-minimal-base-iptables) maintained by Amazon EKS Distro, which contains minimal packages and doesn't have shells\. For more information, see [Amazon EKS Distro](https://distro.eks.amazonaws.com/)\.<a name="kube-proxy-latest-versions-table"></a><a name="kube-proxy-latest-tags"></a>


**Latest available self\-managed `kube-proxy` container image version for each Amazon EKS cluster version**  

| Image type | `1.29` | `1.28` | `1.27` | `1.26` | `1.25` | `1.24` | `1.23` | 
| --- | --- | --- | --- | --- | --- | --- | --- | 
| kube\-proxy \(default type\) | Only minimal type is available | Only minimal type is available | Only minimal type is available | Only minimal type is available | Only minimal type is available | v1\.24\.10\-eksbuild\.2 | v1\.23\.16\-eksbuild\.2 | 
| kube\-proxy \(minimal type\) | v1\.29\.1\-minimal\-eksbuild\.2 | v1\.28\.6\-minimal\-eksbuild\.2 | v1\.27\.10\-minimal\-eksbuild\.2 | v1\.26\.13\-minimal\-eksbuild\.2 | v1\.25\.16\-minimal\-eksbuild\.3 | v1\.24\.17\-minimal\-eksbuild\.4 | v1\.23\.17\-minimal\-eksbuild\.5 | 

**Important**  
The default image type isn't available for Kubernetes version `1.25` and later\. You must use the minimal image type\.
When you [update an Amazon EKS add\-on type](managing-add-ons.md#updating-an-add-on), you specify a valid Amazon EKS add\-on version, which might not be a version listed in this table\. This is because [Amazon EKS add\-on](eks-add-ons.md#add-ons-kube-proxy) versions don't always match container image versions specified when updating the self\-managed type of this add\-on\. When you update the self\-managed type of this add\-on, you specify a valid container image version listed in this table\. 

 Prerequisites
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\.

**Considerations**
+ `Kube-proxy` on an Amazon EKS cluster has the same [compatibility and skew policy as Kubernetes](https://kubernetes.io/releases/version-skew-policy/#kube-proxy)\. Learn how to [Retrieve addon version compatibility](managing-add-ons.md#addon-compat)\.
+ `Kube-proxy` must be the same minor version as `kubelet` on your Amazon EC2 nodes\. 
+ `Kube-proxy` can't be later than the minor version of your cluster's control plane\.
+ If you recently updated your cluster to a new Kubernetes minor version, then update your Amazon EC2 nodes to the same minor version *before* updating `kube-proxy` to the same minor version as your nodes\.

**To update the `kube-proxy` self\-managed add\-on**

1. Confirm that you have the self\-managed type of the add\-on installed on your cluster\. Replace *my\-cluster* with the name of your cluster\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name kube-proxy --query addon.addonVersion --output text
   ```

   If an error message is returned, you have the self\-managed type of the add\-on installed on your cluster\. The remaining steps in this topic are for updating the self\-managed type of the add\-on\. If a version number is returned, you have the Amazon EKS type of the add\-on installed on your cluster\. To update it, use the procedure in [Updating an add\-on](managing-add-ons.md#updating-an-add-on), rather than using the procedure in this topic\. If you're not familiar with the differences between the add\-on types, see [Amazon EKS add\-ons](eks-add-ons.md)\.

1. See which version of the container image is currently installed on your cluster\.

   ```
   kubectl describe daemonset kube-proxy -n kube-system | grep Image
   ```

   An example output is as follows\.

   ```
   Image:    602401143452.dkr.ecr.region-code.amazonaws.com/eks/kube-proxy:v1.25.6-minimal-eksbuild.2
   ```

   In the example output, *v1\.25\.6\-minimal\-eksbuild\.2* is the version installed on the cluster\.

1. Update the `kube-proxy` add\-on by replacing `602401143452` and *`region-code`* with the values from your output\. in the previous step Replace *`v1.26.2-minimal-eksbuild.2`* with the `kube-proxy` version listed in the [Latest available self\-managed `kube-proxy` container image version for each Amazon EKS cluster version](#kube-proxy-latest-tags) table\. You can specify a version number for the *default* or *minimal* image type\.

   ```
   kubectl set image daemonset.apps/kube-proxy -n kube-system kube-proxy=602401143452.dkr.ecr.region-code.amazonaws.com/eks/kube-proxy:v1.26.2-minimal-eksbuild.2
   ```

   An example output is as follows\.

   ```
   daemonset.apps/kube-proxy image updated
   ```

1. Confirm that the new version is now installed on your cluster\.

   ```
   kubectl describe daemonset kube-proxy -n kube-system | grep Image | cut -d ":" -f 3
   ```

   An example output is as follows\.

   ```
   v1.26.2-minimal-eksbuild.2
   ```

1. If you're using `x86` and `Arm` nodes in the same cluster and your cluster was deployed before August 17, 2020\. Then, edit your `kube-proxy` manifest to include a node selector for multiple hardware architectures with the following command\. This is a one\-time operation\. After you've added the selector to your manifest, you don't need to add it each time you update the add\-on\. If your cluster was deployed on or after August 17, 2020, then `kube-proxy` is already multi\-architecture capable\.

   ```
   kubectl edit -n kube-system daemonset/kube-proxy
   ```

   Add the following node selector to the file in the editor and then save the file\. For an example of where to include this text in the editor, see the [CNI manifest](https://github.com/aws/amazon-vpc-cni-k8s/blob/release-1.11/config/master/aws-k8s-cni.yaml#L265-#L269) file on GitHub\. This enables Kubernetes to pull the correct hardware image based on the node's hardware architecture\.

   ```
   - key: "kubernetes.io/arch"
     operator: In
     values:
     - amd64
     - arm64
   ```

1. If your cluster was originally created with Kubernetes version `1.14` or later, then you can skip this step because `kube-proxy` already includes this `Affinity Rule`\. If you originally created an Amazon EKS cluster with Kubernetes version `1.13` or earlier and intend to use Fargate nodes in your cluster, then edit your `kube-proxy` manifest to include a `NodeAffinity` rule to prevent `kube-proxy` Pods from scheduling on Fargate nodes\. This is a one\-time edit\. Once you've added the `Affinity Rule` to your manifest, you don't need to add it each time that you update the add\-on\. Edit your `kube-proxy` `DaemonSet`\.

   ```
   kubectl edit -n kube-system daemonset/kube-proxy
   ```

   Add the following `Affinity Rule` to the `DaemonSet` `spec` section of the file in the editor and then save the file\. For an example of where to include this text in the editor, see the [CNI manifest](https://github.com/aws/amazon-vpc-cni-k8s/blob/release-1.11/config/master/aws-k8s-cni.yaml#L270-#L273) file on GitHub\.

   ```
   - key: eks.amazonaws.com/compute-type
     operator: NotIn
     values:
     - fargate
   ```