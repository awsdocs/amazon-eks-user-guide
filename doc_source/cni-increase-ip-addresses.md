# Assign more IP addresses to Amazon EKS nodes with prefixes<a name="cni-increase-ip-addresses"></a>

**Applies to**: Linux and Windows nodes with Amazon EC2 instances

**Applies to**: Public and private subnets 

Each Amazon EC2 instance supports a maximum number of elastic network interfaces and a maximum number of IP addresses that can be assigned to each network interface\. Each node requires one IP address for each network interface\. All other available IP addresses can be assigned to `Pods`\. Each `Pod` requires its own IP address\. As a result, you might have nodes that have available compute and memory resources, but can't accommodate additional `Pods` because the node has run out of IP addresses to assign to `Pods`\.

You can increase the number of IP addresses that nodes can assign to `Pods` by assigning IP prefixes, rather than assigning individual secondary IP addresses to your nodes\. Each prefix includes several IP addresses\. If you don't configure your cluster for IP prefix assignment, your cluster must make more Amazon EC2 application programming interface \(API\) calls to configure network interfaces and IP addresses necessary for Pod connectivity\. As clusters grow to larger sizes, the frequency of these API calls can lead to longer Pod and instance launch times\. This results in scaling delays to meet the demand of large and spiky workloads, and adds cost and management overhead because you need to provision additional clusters and VPCs to meet scaling requirements\. For more information, see [Kubernetes Scalability thresholds](https://github.com/kubernetes/community/blob/master/sig-scalability/configs-and-limits/thresholds.md) on GitHub\.

## Compatibility with Amazon VPC CNI plugin for Kubernetes features<a name="cni-increase-ip-addresses-compatability"></a>

You can use IP prefixes with the following features:
+ IPv4 Source Network Address Translation \- For more information, see [Enable outbound internet access for pods](external-snat.md)\.
+  IPv6 addresses to clusters, Pods, and services \- For more information, see [Assign IPv6 addresses to clusters, pods, and services](cni-ipv6.md)\.
+ Restricting traffic using Kubernetes network policies \- For more information, see [Limit pod traffic with Kubernetes network policies](cni-network-policy.md)\.

The following list provides information about the Amazon VPC CNI plugin settings that apply\. For more information about each setting, see [amazon\-vpc\-cni\-k8s](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/README.md) on GitHub\.
+ `WARM_IP_TARGET`
+ `MINIMUM_IP_TARGET`
+ `WARM_PREFIX_TARGET`

## Considerations<a name="cni-increase-ip-addresses-considerations"></a>

Consider the following when you use this feature:
+ Each Amazon EC2 instance type supports a maximum number of Pods\. If your managed node group consists of multiple instance types, the smallest number of maximum Pods for an instance in the cluster is applied to all nodes in the cluster\.
+ By default, the maximum number of `Pods` that you can run on a node is 110, but you can change that number\. If you change the number and have an existing managed node group, the next AMI or launch template update of your node group results in new nodes coming up with the changed value\.
+ When transitioning from assigning IP addresses to assigning IP prefixes, we recommend that you create new node groups to increase the number of available IP addresses, rather than doing a rolling replacement of existing nodes\. Running Pods on a node that has both IP addresses and prefixes assigned can lead to inconsistency in the advertised IP address capacity, impacting the future workloads on the node\. For the recommended way of performing the transition, see [Replace all nodes during migration from Secondary IP mode to Prefix Delegation mode or vice versa](https://github.com/aws/aws-eks-best-practices/blob/master/content/networking/prefix-mode/index_windows.md#replace-all-nodes-during-migration-from-secondary-ip-mode-to-prefix-delegation-mode-or-vice-versa) in the Amazon EKS best practices guide\.
+ The security group scope is at the node\-level \- For more information, see [Security group](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html)\.
+ IP prefixes assigned to a network interface support high Pod density per node and have the best launch time\.
+ IP prefixes and IP addresses are associated with standard Amazon EC2 elastic network interfaces\. Pods requiring specific security groups are assigned the primary IP address of a branch network interface\. You can mix Pods getting IP addresses, or IP addresses from IP prefixes with Pods getting branch network interfaces on the same node\.
+ For clusters with Linux nodes only\.
  + After you configure the add\-on to assign prefixes to network interfaces, you can't downgrade your Amazon VPC CNI plugin for Kubernetes add\-on to a version lower than `1.9.0` \(or `1.10.1`\) without removing all nodes in all node groups in your cluster\.
  + If you're also using security groups for Pods, with `POD_SECURITY_GROUP_ENFORCING_MODE`=`standard` and `AWS_VPC_K8S_CNI_EXTERNALSNAT`=`false`, when your Pods communicate with endpoints outside of your VPC, the node's security groups are used, rather than any security groups you've assigned to your Pods\. 

    If you're also using [security groups for Pods](security-groups-for-pods.md), with `POD_SECURITY_GROUP_ENFORCING_MODE`=`strict`, when your `Pods` communicate with endpoints outside of your VPC, the `Pod's` security groups are used\.