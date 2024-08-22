# Limit pod traffic with Kubernetes network policies<a name="cni-network-policy"></a>

By default, there are no restrictions in Kubernetes for IP addresses, ports, or connections between any Pods in your cluster or between your Pods and resources in any other network\. You can use Kubernetes *network policy* to restrict network traffic to and from your Pods\. For more information, see [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) in the Kubernetes documentation\.

If you have version `1.13` or earlier of the Amazon VPC CNI plugin for Kubernetes on your cluster, you need to implement a third party solution to apply Kubernetes network policies to your cluster\. Version `1.14` or later of the plugin can implement network policies, so you don't need to use a third party solution\. In this topic, you learn how to configure your cluster to use Kubernetes network policy on your cluster without using a third party add\-on\.

Network policies in the Amazon VPC CNI plugin for Kubernetes are supported in the following configurations\.
+ Amazon EKS clusters of version `1.25` and later\.
+ Version 1\.14 or later of the Amazon VPC CNI plugin for Kubernetes on your cluster\.
+ Cluster configured for `IPv4` or `IPv6` addresses\.
+ You can use network policies with [security groups for Pods](security-groups-for-pods.md)\. With network policies, you can control all in\-cluster communication\. With security groups for Pods, you can control access to AWS services from applications within a Pod\.
+ You can use network policies with *custom networking* and *prefix delegation*\.

## Considerations<a name="cni-network-policy-considerations"></a>
+ When applying Amazon VPC CNI plugin for Kubernetes network policies to your cluster with the Amazon VPC CNI plugin for Kubernetes , you can apply the policies to Amazon EC2 Linux nodes only\. You can't apply the policies to Fargate or Windows nodes\.
+ If your cluster is currently using a third party solution to manage Kubernetes network policies, you can use those same policies with the Amazon VPC CNI plugin for Kubernetes\. However you must remove your existing solution so that it isn't managing the same policies\.
+ You can apply multiple network policies to the same Pod\. When two or more policies that select the same Pod are configured, all policies are applied to the Pod\.
+ The maximum number of unique combinations of ports for each protocol in each `ingress:` or `egress:` selector in a network policy is 24\.
+ For any of your Kubernetes services, the service port must be the same as the container port\. If you're using named ports, use the same name in the service spec too\.
+ The network policy feature creates and requires a `PolicyEndpoint` Custom Resource Definition \(CRD\) called `policyendpoints.networking.k8s.aws`\. `PolicyEndpoint` objects of the Custom Resource are managed by Amazon EKS\. You shouldn't modify or delete these resources\.
+ If you run pods that use the instance role IAM credentials or connect to the EC2 IMDS, be careful to check for network policies that would block access to the EC2 IMDS\. You may need to add a network policy to allow access to EC2 IMDS\. For more information, see [Instance metadata and user data](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html) in the Amazon EC2 User Guide\.

  Pods that use *IAM roles for service accounts* don't access EC2 IMDS\.
+ The Amazon VPC CNI plugin for Kubernetes doesn't apply network policies to additional network interfaces for each pod, only the primary interface for each pod \(`eth0`\)\. This affects the following architectures:
  + `IPv6` pods with the `ENABLE_V4_EGRESS` variable set to `true`\. This variable enables the `IPv4` egress feature to connect the IPv6 pods to `IPv4` endpoints such as those outside the cluster\. The `IPv4` egress feature works by creating an additional network interface with a local loopback IPv4 address\.
  + When using chained network plugins such as Multus\. Because these plugins add network interfaces to each pod, network policies aren't applied to the chained network plugins\.