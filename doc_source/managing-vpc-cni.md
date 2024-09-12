# Assign IPs to Pods with the Amazon VPC CNI<a name="managing-vpc-cni"></a>

The Amazon VPC CNI plugin for Kubernetes add\-on is deployed on each Amazon EC2 node in your Amazon EKS cluster\. The add\-on creates [elastic network interfaces](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html) and attaches them to your Amazon EC2 nodes\. The add\-on also assigns a private `IPv4` or `IPv6` address from your VPC to each Pod and service\.

A version of the add\-on is deployed with each Fargate node in your cluster, but you don't update it on Fargate nodes\. [Other compatible CNI plugins](alternate-cni-plugins.md) are available for use on Amazon EKS clusters, but this is the only CNI plugin supported by Amazon EKS\.

The following table lists the latest available version of the Amazon EKS add\-on type for each Kubernetes version\.

## Amazon VPC CNI versions<a name="vpc-cni-latest-available-version"></a>


| Kubernetes version | `1.30` | `1.29` | `1.28` | `1.27` | `1.26` | `1.25` | `1.24` | `1.23` | 
| --- | --- | --- | --- | --- | --- | --- | --- | --- | 
| Amazon EKS type of VPC CNI version | v1\.18\.3\-eksbuild\.3 | v1\.18\.3\-eksbuild\.3 | v1\.18\.3\-eksbuild\.3 | v1\.18\.3\-eksbuild\.3 | v1\.18\.3\-eksbuild\.3 | v1\.18\.3\-eksbuild\.3 | v1\.18\.3\-eksbuild\.3 | v1\.18\.3\-eksbuild\.3 | 

**Important**  
If you're self\-managing this add\-on, the versions in the table might not be the same as the available self\-managed versions\. For more information about updating the self\-managed type of this add\-on, see [Updating the self\-managed Amazon EKS add\-on](vpc-add-on-self-managed-update.md)\.

**Important**  
To upgrade to VPC CNI v1\.12\.0 or later, you must upgrade to VPC CNI v1\.7\.0 first\. We recommend that you update one minor version at a time\.

## Considerations<a name="manage-vpc-cni-add-on-on-considerations"></a>

 The following are considerations for using the feature\.
+ Versions are specified as `major-version.minor-version.patch-version-eksbuild.build-number`\.
+ Check version compatibility for each feature\. Some features of each release of the Amazon VPC CNI plugin for Kubernetes require certain Kubernetes versions\. When using different Amazon EKS features, if a specific version of the add\-on is required, then it's noted in the feature documentation\. Unless you have a specific reason for running an earlier version, we recommend running the latest version\.