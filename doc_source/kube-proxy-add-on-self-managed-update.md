# Updating the Kubernetes `kube-proxy` add\-on<a name="kube-proxy-add-on-self-managed-update"></a>

1. Confirm that you have the self\-managed type of the add\-on installed on your cluster\. Replace *my\-cluster* with the name of your cluster\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name kube-proxy --query addon.addonVersion --output text
   ```

   If an error message is returned, you have the self\-managed type of the add\-on installed on your cluster\. The remaining steps in this topic are for updating the self\-managed type of the add\-on\. If a version number is returned, you have the Amazon EKS type of the add\-on installed on your cluster\. To update it, use the procedure in [Updating an Amazon EKS add\-on](updating-an-add-on.md), rather than using the procedure in this topic\. If you're not familiar with the differences between the add\-on types, see [Amazon EKS add\-ons](eks-add-ons.md)\.

1. See which version of the container image is currently installed on your cluster\.

   ```
   kubectl describe daemonset kube-proxy -n kube-system | grep Image
   ```

   An example output is as follows\.

   ```
   Image:    602401143452.dkr.ecr.region-code.amazonaws.com/eks/kube-proxy:v1.29.1-eksbuild.2
   ```

   In the example output, *v1\.29\.1\-eksbuild\.2* is the version installed on the cluster\.

1. Update the `kube-proxy` add\-on by replacing `602401143452` and *`region-code`* with the values from your output\. in the previous step Replace *`v1.30.0-eksbuild.3`* with the `kube-proxy` version listed in the [Latest available self\-managed `kube-proxy` container image version for each Amazon EKS cluster version](managing-kube-proxy.md#kube-proxy-latest-tags) table\. You can specify a version number for the *default* or *minimal* image type\.

   ```
   kubectl set image daemonset.apps/kube-proxy -n kube-system kube-proxy=602401143452.dkr.ecr.region-code.amazonaws.com/eks/kube-proxy:v1.30.0-eksbuild.3
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
   v1.30.0-eksbuild.3
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