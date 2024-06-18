# Multiple network interfaces for Pods<a name="pod-multiple-network-interfaces"></a>

Multus CNI is a container network interface \(CNI\) plugin for Amazon EKS that enables attaching multiple network interfaces to a Pod\. For more information, see the [Multus\-CNI](https://github.com/k8snetworkplumbingwg/multus-cni) documentation on GitHub\. 

In Amazon EKS, each Pod has one network interface assigned by the Amazon VPC CNI plugin\. With Multus, you can create a multi\-homed Pod that has multiple interfaces\. This is accomplished by Multus acting as a "meta\-plugin"; a CNI plugin that can call multiple other CNI plugins\. AWS support for Multus comes configured with the Amazon VPC CNI plugin as the default delegate plugin\.

**Considerations**
+ Amazon EKS won't be building and publishing single root I/O virtualization \(SR\-IOV\) and Data Plane Development Kit \(DPDK\) CNI plugins\. However, you can achieve packet acceleration by connecting directly to Amazon EC2 Elastic Network Adapters \(ENA\) through Multus managed host\-device and `ipvlan` plugins\.
+ Amazon EKS is supporting Multus, which provides a generic process that enables simple chaining of additional CNI plugins\. Multus and the process of chaining is supported, but AWS won't provide support for all compatible CNI plugins that can be chained, or issues that may arise in those CNI plugins that are unrelated to the chaining configuration\.
+ Amazon EKS is providing support and life cycle management for the Multus plugin, but isn't responsible for any IP address or additional management associated with the additional network interfaces\. The IP address and management of the default network interface utilizing the Amazon VPC CNI plugin remains unchanged\.
+ Only the Amazon VPC CNI plugin is officially supported as the default delegate plugin\. You need to modify the published Multus installation manifest to reconfigure the default delegate plugin to an alternate CNI if you choose not to use the Amazon VPC CNI plugin for primary networking\.
+ Multus is only supported when using the Amazon VPC CNI as the primary CNI\. We do not support the Amazon VPC CNI when used for higher order interfaces, secondary or otherwise\.
+ To prevent the Amazon VPC CNI plugin from trying to manage additional network interfaces assigned to Pods, add the following tag to the network interface:

  **key**: `node.k8s.amazonaws.com/no_manage`

  **value**: `true`
+ Multus is compatible with network policies, but the policy has to be enriched to include ports and IP addresses that may be part of additional network interfaces attached to Pods\.

For an implementation walk through, see the [Multus Setup Guide](https://github.com/aws-samples/eks-install-guide-for-multus/blob/main/README.md) on GitHub\.