# Amazon VPC CNI plugin for Kubernetes upgrades<a name="cni-upgrades"></a>

When you launch an Amazon EKS cluster, we apply a recent version of the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) to your cluster\. The absolute latest version of the plugin is available on [GitHub](https://github.com/aws/amazon-vpc-cni-k8s/releases) for a short grace period before new clusters are switched over to use it\. Amazon EKS does not automatically upgrade the CNI plugin on your cluster when new versions are released\. To get a newer version of the CNI plugin on existing clusters, you must manually upgrade the plugin\.

The latest version that we recommend  is version 1\.5\.7\. You can view the different releases available for the plugin, and read the release notes for each version [on GitHub](https://github.com/aws/amazon-vpc-cni-k8s/releases)\.

Use the following procedures to check your CNI plugin version and upgrade to the latest recommended version\.

**To check your Amazon VPC CNI plugin for Kubernetes version**
+ Use the following command to print your cluster's CNI version:

  ```
  kubectl describe daemonset aws-node --namespace kube-system | grep Image | cut -d "/" -f 2
  ```

  Output:

  ```
  amazon-k8s-cni:1.5.5
  ```

  In this example output, the CNI version is 1\.5\.5, which is earlier than the current recommended version, 1\.5\.7\. Use the following procedure to upgrade the CNI\.

**To upgrade the Amazon VPC CNI plugin for Kubernetes**
+ Use the following command to upgrade your CNI version to the latest recommended version:

  ```
  kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.5/config/v1.5/aws-k8s-cni.yaml
  ```