# Learn about VPC CNI modes and configuration<a name="pod-networking-use-cases"></a>

The Amazon VPC CNI plugin for Kubernetes provides networking for Pods\. Use the following table to learn more about the available networking features\.


| Networking feature | Learn more | 
| --- | --- | 
| Configure your cluster to assign IPv6 addresses to clusters, Pods, and services | [Assign IPv6 addresses to clusters, pods, and services](cni-ipv6.md) | 
| Use IPv4 Source Network Address Translation for Pods | [Enable outbound internet access for pods](external-snat.md) | 
| Restrict network traffic to and from your Pods | [Restrict Pod network traffic with Kubernetes network policies](cni-network-policy-configure.md) | 
| Customize the secondary network interface in nodes | [Deploy pods in alternate subnets with custom networking](cni-custom-network.md) | 
| Increase IP addresses for your node | [Assign more IP addresses to Amazon EKS nodes with prefixes](cni-increase-ip-addresses.md) | 
| Use security groups for Pod network traffic | [Assign security groups to individual pods](security-groups-for-pods.md) | 
| Use multiple network interfaces for Pods | [Attach multiple network interfaces to Pods with Multus](pod-multiple-network-interfaces.md) | 