# Updating the `kube-proxy` add\-on<a name="managing-kube-proxy"></a>

`Kube-proxy` maintains network rules on each Amazon EC2 node\. It enables network communication to your pods\. `Kube-proxy` is not deployed to Fargate nodes\. For more information, see [https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/) in the Kubernetes documentation\. There are two types of the `kube-proxy` container image available for each Amazon EKS cluster version:
+ **Default** – This image type is based on a Debian\-based Docker image that is maintained by the Kubernetes upstream community\.
+ **Minimal** – This image type is based on a [minimal base image](https://gallery.ecr.aws/eks-distro-build-tooling/eks-distro-minimal-base-iptables) maintained by Amazon EKS Distro, which contains minimal packages and doesn't have shells\. For more information, see [Amazon EKS Distro](https://distro.eks.amazonaws.com/)\.<a name="kube-proxy-latest-versions-table"></a>


**Latest available `kube-proxy` container image version for each Amazon EKS cluster version**  

| Image type | `1.24` | `1.23` | `1.22` | `1.21` | `1.20` | `1.19` | 
| --- | --- | --- | --- | --- | --- | --- | 
| kube\-proxy \(default type\) | v1\.24\.7\-eksbuild\.1 | v1\.23\.8\-eksbuild\.2 | v1\.22\.11\-eksbuild\.2 | v1\.21\.14\-eksbuild\.2 | v1\.20\.15\-eksbuild\.2 | v1\.19\.16\-eksbuild\.2 | 
| kube\-proxy \(minimal type\) | v1\.24\.9\-minimal\-eksbuild\.1 | v1\.23\.15\-minimal\-eksbuild\.1 | v1\.22\.16\-minimal\-eksbuild\.3 | v1\.21\.14\-minimal\-eksbuild\.4 | v1\.20\.15\-minimal\-eksbuild\.4 | v1\.19\.16\-minimal\-eksbuild\.3 | 

You can see which version is installed on your cluster with the following command\.

```
kubectl describe daemonset kube-proxy --namespace kube-system | grep Image | cut -d ":" -f 3
```

The example output is as follows\.

```
v1.23.7-minimal-eksbuild.1
```

**Prerequisites**
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\.
+ If your cluster is `1.21` or later, make sure that your Amazon VPC CNI plugin for Kubernetes and CoreDNS add\-ons are at the minimum versions listed in [Service account tokens](service-accounts.md#boundserviceaccounttoken-validated-add-on-versions)\.

**Considerations**
+ `Kube-proxy` on an Amazon EKS cluster has the same [compatibility and skew policy as Kubernetes](https://kubernetes.io/releases/version-skew-policy/#kube-proxy)\.
+ `Kube-proxy` must be the same minor version as `kubelet` on your Amazon EC2 nodes\.
+ `Kube-proxy` can't be later than the version of your cluster's control plane\.
+ The `kube-proxy` version on your Amazon EC2 nodes can't be more than two minor versions earlier than your control plane\. For example, if your control plane is running Kubernetes 1\.24, then the `kube-proxy` minor version can't be earlier than 1\.22\.
+ If you recently updated your cluster to a new Kubernetes minor version, then update your Amazon EC2 nodes to the same minor version before updating `kube-proxy` to the same minor version as your nodes\.
+ If you deployed a version `1.22` and earlier cluster, the *default* image type was deployed with your cluster, by default\. If you deployed a version `1.23` and later cluster, the *minimal* image type was deployed with your cluster, by default\.

**To update your `kube-proxy` add\-on version**

1. Determine whether you have the Amazon EKS or self\-managed type of the add\-on installed on your cluster\. Replace *my\-cluster* with the name of your cluster\. If you don't know the difference between the two types of add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name kube-proxy --query addon.addonVersion --output text
   ```

   The output returned is different, depending on the add\-on type installed on your cluster\.
   + **Amazon EKS add\-on**

     ```
     v1.23.7-eksbuild.1
     ```
   + **Self\-managed add\-on**

     ```
     An error occurred (ResourceNotFoundException) when calling the DescribeAddon operation: No addon: kube-proxy found in cluster: my-cluster
     ```

1. Update your `kube-proxy` add\-on using the procedure for the type of add\-on that you have installed on your cluster\.
**Important**  
If you want to use the minimal image type with a version `1.22` and earlier cluster, then you can't use the Amazon EKS add\-on type\. You must use the self\-managed add\-on type to use the minimal image type with `1.22` and earlier clusters\.

------
#### [ Amazon EKS add\-on ]

   Follow the procedure in [Updating an add\-on](managing-add-ons.md#updating-an-add-on)\. When using that procedure, you're asked to provide the following information:
   + **Add\-on name** – Specify `kube-proxy`\.
   + **Version** – If you use the AWS Management Console to update the add\-on, you can select any available version shown in the console\. The version numbers in the console might not match a version in the [Latest available `kube-proxy` container image version table](#kube-proxy-latest-versions-table) because the Amazon EKS add\-on type's version doesn't always match a `kube-proxy` container image version\. If you use any other tool to update the add\-on, you can specify the version in the [Latest available `kube-proxy` container image version for each Amazon EKS cluster version](#kube-proxy-latest-versions-table) table for your cluster's version, but those versions also might not match a version in the table\. If you want to use the minimal image type with a version `1.22` and earlier cluster, then you can't use the Amazon EKS add\-on type\. You must use the self\-managed add\-on type to use the minimal image type with `1.22` and earlier clusters\.

     
   + **IAM role** – An IAM role isn't used for this add\-on\.

   You can also [create](managing-add-ons.md#creating-an-add-on) or [delete](managing-add-ons.md#removing-an-add-on) the add\-on\. When creating or deleting the add\-on, you can use the same information listed for updating the add\-on\.

------
#### [ Self\-managed add\-on ]

   If you want to install the Amazon EKS type of the add\-on, see [Creating an add\-on](managing-add-ons.md#creating-an-add-on)\. When following the procedure in that topic, specify the add\-on with the name `kube-proxy`\. Complete the following procedure to update the self\-managed add\-on\.

**To update the `kube-proxy` add\-on**

   1. Check the container image version of your current `kube-proxy` installation\.

      ```
      kubectl describe daemonset kube-proxy -n kube-system | grep Image
      ```

      The example output is as follows\.

      ```
      Image:    602401143452.dkr.ecr.region-code.amazonaws.com/eks/kube-proxy:vv1.23.7-minimal-eksbuild.1
      ```

   1. Update the `kube-proxy` add\-on by replacing `602401143452` and *`region-code`* with the values from your output\. Replace *v1\.23\.13\-minimal\-eksbuild\.2* with the `kube-proxy` version listed in the [Latest available `kube-proxy` container image version for each Amazon EKS cluster version](#kube-proxy-latest-versions-table) table\. You can specify a version number for the *default* or *minimal* image type\.

      ```
      kubectl set image daemonset.apps/kube-proxy -n kube-system kube-proxy=602401143452.dkr.ecr.region-code.amazonaws.com/eks/kube-proxy:v1.23.13-minimal-eksbuild.2
      ```

      The example output is as follows\.

      ```
      daemonset.apps/kube-proxy image updated
      ```

   1. Check the container image version again to confirm that it was updated to the version that you specified in the previous step\.

      ```
      kubectl describe daemonset kube-proxy -n kube-system | grep Image | cut -d ":" -f 3
      ```

      The example output is as follows\.

      ```
      v1.23.13-minimal-eksbuild.2
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

   1. If your cluster was originally created with Kubernetes version `1.14` or later, then you can skip this step because `kube-proxy` already includes this `Affinity Rule`\. If you originally created an Amazon EKS cluster with Kubernetes version `1.13` or earlier and intend to use Fargate nodes in your cluster, then edit your `kube-proxy` manifest to include a `NodeAffinity` rule to prevent `kube-proxy` pods from scheduling on Fargate nodes\. This is a one\-time edit\. Once you've added the `Affinity Rule` to your manifest, you don't need to add it each time that you update the add\-on\. Edit your `kube-proxy` `DaemonSet`\.

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

------