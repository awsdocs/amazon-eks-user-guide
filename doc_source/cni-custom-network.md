# Deploy pods in alternate subnets with custom networking<a name="cni-custom-network"></a>

**Applies to**: Linux `IPv4` Fargate nodes, Linux nodes with Amazon EC2 instances 

By default, when the Amazon VPC CNI plugin for Kubernetes creates secondary [elastic network interfaces](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html) \(network interfaces\) for your Amazon EC2 node, it creates them in the same subnet as the node's primary network interface\. It also associates the same security groups to the secondary network interface that are associated to the primary network interface\. For one or more of the following reasons, you might want the plugin to create secondary network interfaces in a different subnet or want to associate different security groups to the secondary network interfaces, or both: 
+ There's a limited number of `IPv4` addresses that are available in the subnet that the primary network interface is in\. This might limit the number of Pods that you can create in the subnet\. By using a different subnet for secondary network interfaces, you can increase the number of available `IPv4` addresses available for Pods\.
+ For security reasons, your Pods might need to use a different subnet or security groups than the node's primary network interface\.
+ The nodes are configured in public subnets, and you want to place the Pods in private subnets\. The route table associated to a public subnet includes a route to an internet gateway\. The route table associated to a private subnet doesn't include a route to an internet gateway\.

## Considerations<a name="cni-custom-network-considerations"></a>

The following are considerations for using the feature\.
+ With custom networking enabled, no IP addresses assigned to the primary network interface are assigned to Pods\. Only IP addresses from secondary network interfaces are assigned to `Pods`\.
+ If your cluster uses the `IPv6` family, you can't use custom networking\.
+ If you plan to use custom networking only to help alleviate `IPv4` address exhaustion, you can create a cluster using the `IPv6` family instead\. For more information, see [Assign IPv6 addresses to clusters, pods, and services](cni-ipv6.md)\.
+ Even though Pods deployed to subnets specified for secondary network interfaces can use different subnet and security groups than the node's primary network interface, the subnets and security groups must be in the same VPC as the node\.
+ For Fargate, subnets are controlled through the Fargate profile\. For more information, see [Define which Pods use AWS Fargate when launched](fargate-profile.md)\.