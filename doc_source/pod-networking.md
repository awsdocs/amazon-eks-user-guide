# Pod networking in Amazon EKS using the Amazon VPC CNI plugin for Kubernetes<a name="pod-networking"></a>

Amazon EKS supports native Amazon VPC networking using the Amazon VPC Container Network Interface \(CNI\) plugin for Kubernetes\. This plugin:
+ creates elastic network interfaces \(network interfaces\) and attaches them to your Amazon EC2 nodes\.
+ assigns a private `IPv4` or `IPv6` address from your VPC to each pod and service\.

The plugin is an open\-source project that is maintained on GitHub\. We recommend familiarizing yourself with the plugin by reading [amazon\-vpc\-cni\-k8s](https://github.com/aws/amazon-vpc-cni-k8s) and [Proposal: CNI plugin for Kubernetes networking over Amazon VPC](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/docs/cni-proposal.md) on GitHub\. Several of the CNI configuration variables in `amazon-vpc-cni-k8s` are expanded on in [Choosing pod networking use cases](pod-networking-use-cases.md)\. The plugin is fully supported for use on Amazon EKS and self\-managed Kubernetes clusters on AWS\.

**Topics**
+ [Managing the Amazon VPC CNI plugin for Kubernetes](managing-vpc-cni.md)
+ [Configuring the Amazon VPC CNI plugin for Kubernetes to use IAM roles for service accounts](cni-iam-role.md)
+ [Choosing pod networking use cases](pod-networking-use-cases.md)
+ [Metrics helper](cni-metrics-helper.md)
+ [Alternate compatible CNI plugins](alternate-cni-plugins.md)