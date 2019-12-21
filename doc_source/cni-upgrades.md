# Amazon VPC CNI Plugin for Kubernetes Upgrades<a name="cni-upgrades"></a>

When you launch an Amazon EKS cluster, we apply a recent version of the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) to your cluster \(the absolute latest version of the plugin is available [on GitHub](https://github.com/aws/amazon-vpc-cni-k8s/releases) for a short grace period before new clusters are switched over to use it\)\. However, Amazon EKS does not automatically upgrade the CNI plugin on your cluster when new versions are released\. You must upgrade the CNI plugin manually to get the latest version on existing clusters\.

The latest recommended CNI version available [on GitHub](https://github.com/aws/amazon-vpc-cni-k8s/releases) is 1\.5\.5\. You can view the different releases available for the plugin, and read the release notes for each version [on GitHub](https://github.com/aws/amazon-vpc-cni-k8s/releases)\.

Use the following procedures to check your CNI version and upgrade to the latest version\.

**To check your Amazon VPC CNI Plugin for Kubernetes version**
+ Use the following command to print your cluster's CNI version:

  ```
  kubectl describe daemonset aws-node --namespace kube-system | grep Image | cut -d "/" -f 2
  ```

  Output:

  ```
  amazon-k8s-cni:1.5.4
  ```

  In this example output, the CNI version is 1\.5\.4, which is earlier than the current recommended version, 1\.5\.5\. Use the following procedure to upgrade the CNI\.

**To upgrade the Amazon VPC CNI Plugin for Kubernetes**
+ Use the following command to upgrade your CNI version to the latest recommended version:

  ```
  kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.5/config/v1.5/aws-k8s-cni.yaml
  ```