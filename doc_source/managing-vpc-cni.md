# Updating the Amazon VPC CNI plugin for Kubernetes self\-managed add\-on<a name="managing-vpc-cni"></a>

**Important**  
This topic will be removed from this guide on July 1, 2023\. We recommend adding the Amazon EKS type of the add\-on to your cluster instead of using the self\-managed type of the add\-on\. If you're not familiar with the difference between the types, see [Amazon EKS add\-ons](eks-add-ons.md)\. For more information about adding an Amazon EKS add\-on, to your cluster, see [Creating an add\-on](managing-add-ons.md#creating-an-add-on)\.

The Amazon VPC CNI plugin for Kubernetes add\-on is deployed on each Amazon EC2 node in your Amazon EKS cluster\. The add\-on creates elastic network interfaces \(network interfaces\) and attaches them to your Amazon EC2 nodes\. The add\-on also assigns a private `IPv4` or `IPv6` address from your VPC to each pod and service\. Your pods and services have the same IP address inside the pod as they do on the VPC network\.

A version of the add\-on is deployed with each Fargate node in your cluster, but you don't update it on Fargate nodes\. For more information about the version of the add\-on deployed to Amazon EC2 nodes, see [amazon\-vpc\-cni\-k8s](https://github.com/aws/amazon-vpc-cni-k8s) and [Proposal: CNI plugin for Kubernetes networking over Amazon VPC](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/docs/cni-proposal.md) on GitHub\. Several of the configuration variables for the plugin are expanded on in [Choosing pod networking use cases](pod-networking-use-cases.md)\. [Other compatible CNI plugins](alternate-cni-plugins.md) are available for use on Amazon EKS clusters, but this is the only CNI plugin supported by Amazon EKS\.<a name="manage-vpc-cni-add-on-on-prerequisites"></a>

**Prerequisites**
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\.
+ If your cluster is `1.21` or later, make sure that your `kube-proxy` and CoreDNS add\-ons are at the minimum versions listed in [Service account tokens](service-accounts.md#boundserviceaccounttoken-validated-add-on-versions)\.
+ An existing AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see [Creating an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ An IAM role with the [AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor) IAM policy \(if your cluster uses the `IPv4` family\) or an [IPv6 policy](cni-iam-role.md#cni-iam-role-create-ipv6-policy) \(if your cluster uses the `IPv6` family\) attached to it\. For more information, see [Configuring the Amazon VPC CNI plugin for Kubernetes to use IAM roles for service accounts](cni-iam-role.md)\.
+ If you are using version `1.7.0` or later of the CNI plugin and you use custom pod security policies, see [Delete the default Amazon EKS pod security policy](pod-security-policy.md#psp-delete-default)[Pod security policy](pod-security-policy.md)\.

**Considerations**
+ Versions are specified as `major-version.minor-version.patch-version-eksbuild.build-number`\.
+ We require that you only update one *minor* version at a time\. For example, if your current minor version is `1.10` and you want to update to `1.12`, then you need to update to `1.11` first, then update to `1.12`\.
+ All versions work with all Amazon EKS supported Kubernetes versions, though not all features of each release work with all Kubernetes versions\. When using different Amazon EKS features, if a specific version of the add\-on is required, then it's noted in the feature documentation\. Unless you have a specific reason for running an earlier version, we recommend running the latest version\.

**To update the Amazon VPC CNI plugin for Kubernetes self\-managed add\-on**

1. Confirm that you have the self\-managed type of the add\-on installed on your cluster\. Replace *my\-cluster* with the name of your cluster\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name vpc-cni --query addon.addonVersion --output text
   ```

   If an error message is returned, you have the self\-managed type of the add\-on installed on your cluster\. The remaining steps in this topic are for updating the self\-managed type of the add\-on\. If a version number is returned, you have the Amazon EKS type of the add\-on installed on your cluster\. To update it, use the procedure in [Updating an add\-on](managing-add-ons.md#updating-an-add-on), rather than using the procedure in this topic\. If you're not familiar with the differences between the add\-on types, see [Amazon EKS add\-ons](eks-add-ons.md)\.

1. See which version of the container image is currently installed on your cluster\.

   ```
   kubectl describe daemonset aws-node --namespace kube-system | grep amazon-k8s-cni: | cut -d : -f 3
   ```

1. Backup your current settings so you can configure the same settings once you've updated your version\.

   ```
   kubectl get daemonset aws-node -n kube-system -o yaml > aws-k8s-cni-old.yaml
   ```

1. To see the available versions and familiarize yourself with the changes in the version that you want to update to, see `[releases](https://github.com/aws/amazon-vpc-cni-k8s/releases)` on GitHub\.

1. If you don't have any custom settings, then run the command under `To apply this release:` heading on GitHub for the [release](https://github.com/aws/amazon-vpc-cni-k8s/releases) that you want to update to\.

   If you have custom settings, download the manifest file with the following command, instead of applying it\. Change *url\-of\-manifest\-from\-github* to the URL for the release on GitHub that you're installing\.

   ```
   curl -O url-of-manifest-from-github/aws-k8s-cni.yaml
   ```

   If necessary, modify the file with the custom settings from the backup you made and then apply the modified file to your cluster\. If your nodes don't have access to the private Amazon EKS Amazon ECR repositories that the images are pulled from \(see the lines that start with `image:` in the manifest\), then you'll have to download the images, copy them to your own repository, and modify the manifest to pull the images from your repository\. For more information, see [Copy a container image from one repository to another repository](copy-image-to-repository.md)\.

   ```
   kubectl apply -f aws-k8s-cni.yaml
   ```

1. Confirm that the new version is now installed on your cluster\.

   ```
   kubectl describe daemonset aws-node --namespace kube-system | grep amazon-k8s-cni: | cut -d : -f 3
   ```