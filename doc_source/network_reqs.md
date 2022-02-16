# Cluster VPC and subnet considerations<a name="network_reqs"></a>

Amazon EKS recommends running a cluster in a VPC with public and private subnets so that Kubernetes can create public load balancers in the public subnets that load balance traffic to pods running on nodes that are in private subnets\. This configuration is not required, however\. You can run a cluster in a VPC with only private or only public subnets, depending on your networking and security requirements\. For more information about clusters deployed to a VPC with only private subnets, see [Private clusters](private-clusters.md)\. 

When you create an Amazon EKS cluster, you specify the VPC subnets where Amazon EKS can place Elastic network interfaces\. Amazon EKS requires subnets in at least two Availability Zone, and creates up to four network interfaces across these subnets to facilitate control plane communication to your nodes\. This communication channel supports Kubernetes functionality such as `kubectl exec` and `kubectl logs`\. The Amazon EKS created [cluster security group](sec-group-reqs.md#cluster-sg) and any additional security groups that you specify when you create your cluster are applied to these network interfaces\. Each Amazon EKS created network interface has Amazon EKS `cluster name` in its description\.

Make sure that the subnets that you specify during cluster creation have enough available IP addresses for the Amazon EKS created network interfaces\. If you're going to deploy a cluster that uses the IPv4 family, we recommend creating small \(`/28`\), dedicated subnets for Amazon EKS created network interfaces, and only specifying these subnets as part of cluster creation\. Other resources, such as nodes and load balancers, should be launched in separate subnets from the subnets specified during cluster creation\.

**Important**  
Nodes and load balancers can be launched in any subnet in your cluster’s VPC, including subnets not registered with Amazon EKS during cluster creation\. Subnets do not require any tags for nodes\. For Kubernetes load balancing auto discovery to work, subnets must be tagged as described in [Subnet tagging](#vpc-subnet-tagging)\. 
Subnets associated with your cluster cannot be changed after cluster creation\. If you need to control exactly which subnets the Amazon EKS created network interfaces are placed in, then specify only two subnets during cluster creation, each in a different Availability Zone\.
Do not select a subnet in AWS Outposts, AWS Wavelength, or an AWS Local Zone when creating your cluster\.
Clusters created using v1\.14 or earlier contain a `kubernetes.io/cluster/cluster-name` tag on your VPC\. This tag was only used by Amazon EKS and can be safely removed\.
An updated range caused by adding CIDR blocks to an existing cluster can take as long as five hours to appear\.
If you want Kubernetes to assign IPv6 addresses to pods and services, then you must have IPv4 and IPv6 CIDR blocks assigned to your VPC and subnets\. For more information, see [Associate an IPv6 CIDR block with your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html#vpc-associate-ipv6-cidr) in the Amazon VPC User Guide\. Your route tables and security groups must also include IPv6 addresses\. For more information, see [Migrate to IPv6](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-migrate-ipv6.html) in the Amazon VPC User Guide\.
Nodes must be able to communicate with the control plane and other AWS services\. If your nodes are deployed in a private subnet and you want pods to have outbound access to the internet, then the private subnet must meet one of the following requirements:   
Subnets with only IPv4 CIDR blocks must have a default route to a [NAT gateway](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)\. The NAT gateway must be assigned a public IPv4 address to provide internet access for the nodes\.  
Subnets with IPv6 CIDR blocks must have a default route to an [egress\-only internet gateway](https://docs.aws.amazon.com/vpc/latest/userguide/egress-only-internet-gateway.html)\.
Is configured with the necessary settings and requirements in [Private clusters](private-clusters.md)\.

Your VPC must have DNS hostname and DNS resolution support, or your nodes can't register with your cluster\. For more information, see [Using DNS with Your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns.html) in the Amazon VPC User Guide\. 

## VPC IP addressing<a name="vpc-cidr"></a>

If you want pods deployed to nodes in public subnets to have outbound internet access, then your public subnets must be configured to auto\-assign public IPv4 addresses or IPv6 addresses\. Determine whether your public subnets are configured to auto\-assign public IPv4 addresses or IPv6 addresses with the following command\. Replace the *`example values`* with your own values\. 

------
#### [ IPv4 ]

```
aws ec2 describe-subnets \
    --filters "Name=vpc-id,Values=VPC-ID" | grep 'SubnetId\|MapPublicIpOnLaunch'
```

------
#### [ IPv6 ]

```
aws ec2 describe-subnets \
    --filters "Name=vpc-id,Values=VPC-ID" | grep 'SubnetId\|AssignIpv6AddressOnCreation'
```

------

Output

------
#### [ IPv4 ]

```
"MapPublicIpOnLaunch": true,
"SubnetId": "subnet-ID1",
"MapPublicIpOnLaunch": false,
"SubnetId": "subnet-ID2",
...
```

------
#### [ IPv6 ]

```
"SubnetId": "subnet-ID1",
"AssignIpv6AddressOnCreation": true,
"SubnetId": "subnet-ID2",
"AssignIpv6AddressOnCreation": false,
...
```

------

For any subnets that have `MapPublicIpOnLaunch` or `AssignIpv6AddressOnCreation` set to `false`, change the setting to `true`\.

------
#### [ IPv4 ]

```
aws ec2 modify-subnet-attribute --subnet-id subnet-ID2 --map-public-ip-on-launch 
```

------
#### [ IPv6 ]

```
aws ec2 modify-subnet-attribute --subnet-id subnet-ID2 --assign-ipv6-address-on-creation
```

------

**Important**  
If you used an [Amazon EKS AWS CloudFormation template](creating-a-vpc.md) to deploy your VPC before March 26, 2020, then you need to change the setting for your public subnets\.   
You can define both private \(RFC 1918\), and public \(non\-RFC 1918\) classless inter\-domain routing \(CIDR\) IPv4 ranges within the VPC used for your Amazon EKS cluster\. For more information, see [Adding IPv4 CIDR blocks to a VPC](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html#vpc-resize) in the Amazon VPC User Guide\. When choosing the CIDR blocks for your VPC and subnets, make sure that the blocks contain enough IPv4 addresses for all of the Amazon EC2 nodes and pods that you plan to deploy\. There should be at least one IP address for each of your pods\. You can conserve IP address use by implementing a transit gateway with a shared services VPC\. For more information, see [Isolated VPCs with shared services](https://docs.aws.amazon.com/vpc/latest/tgw/transit-gateway-isolated-shared.html) and [Amazon EKS VPC routable IP address conservation patterns in a hybrid network](http://aws.amazon.com/blogs/containers/eks-vpc-routable-ip-address-conservation/)\.

## Subnet tagging<a name="vpc-subnet-tagging"></a>

For 1\.18 and earlier clusters, Amazon EKS adds the following tag to all subnets passed in during cluster creation\. Amazon EKS does not add the tag to subnets passed in when creating 1\.19 clusters\. If the tag exists on subnets used by a cluster created on a version earlier than 1\.19, and you update the cluster to 1\.19, the tag is not removed from the subnets\.
+ **Key** – `kubernetes.io/cluster/cluster-name`
+ **Value** – `shared`

You can optionally use this tag to control where Elastic Load Balancers are provisioned, in addition to the required subnet tags for using automatically provisioned Elastic Load Balancers\. For more information about load balancer subnet tagging, see [Application load balancing on Amazon EKS](alb-ingress.md) and [Network load balancing on Amazon EKS](network-load-balancing.md)\.

## Increase available IPv4 addresses for your VPC<a name="vpc-increase-ip-addresses"></a>

If your Amazon VPC is running out of IPv4 addresses, you can associate a secondary CIDR to an existing VPC\. For more information, see [Add IPv4 CIDR blocks to a VPC](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html#vpc-resize) in the Amazon VPC User Guide\. With the new associated CIDR, you can create subnets using a subset of the newly associated CIDR\. After creating the new subnet or subnets, you can create additional node groups, either managed or self\-managed, that use the newly associated CIDR and subnets\.