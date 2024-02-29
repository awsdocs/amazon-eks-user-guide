# Amazon EKS local cluster VPC and subnet requirements and considerations<a name="eks-outposts-vpc-subnet-requirements"></a>

When you create a local cluster, you specify a VPC and at least one private subnet that runs on Outposts\. This topic provides an overview of the VPC and subnets requirements and considerations for your local cluster\.

## VPC requirements and considerations<a name="outposts-vpc-requirements"></a>

When you create a local cluster, the VPC that you specify must meet the following requirements and considerations:
+ Make sure that the VPC has enough IP addresses for the local cluster, any nodes, and other Kubernetes resources that you want to create\. If the VPC that you want to use doesn't have enough IP addresses, increase the number of available IP addresses\. You can do this by [associating additional Classless Inter\-Domain Routing \(CIDR\) blocks](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html#add-ipv4-cidr) with your VPC\. You can associate private \(RFC 1918\) and public \(non\-RFC 1918\) CIDR blocks to your VPC either before or after you create your cluster\. It can take a cluster up to 5 hours for a CIDR block that you associated with a VPC to be recognized\.
+ The VPC can't have assigned IP prefixes or IPv6 CIDR blocks\. Because of these constraints, the information that's covered in [Increase the amount of available IP addresses for your Amazon EC2 nodes](cni-increase-ip-addresses.md) and [`IPv6` addresses for clusters, Pods, and services](cni-ipv6.md) isn't applicable to your VPC\.
+ The VPC has a DNS hostname and DNS resolution enabled\. Without these features, the local cluster fails to create, and you need to enable the features and recreate your cluster\. For more information, see [DNS attributes for your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns.html) in the Amazon VPC User Guide\.
+ To access your local cluster over your local network, the VPC must be associated with your Outpost's local gateway route table\. For more information, see [VPC associations](https://docs.aws.amazon.com/outposts/latest/userguide/outposts-local-gateways.html#vpc-associations) in the AWS Outposts User Guide\.

## Subnet requirements and considerations<a name="outposts-subnet-requirements"></a>

When you create the cluster, specify at least one private subnet\. If you specify more than one subnet, the Kubernetes control plane instances are evenly distributed across the subnets\. If more than one subnet is specified, the subnets must exist on the same Outpost\. Moreover, the subnets must also have proper routes and security group permissions to communicate with each other\. When you create a local cluster, the subnets that you specify must meet the following requirements:
+ The subnets are all on the same logical Outpost\.
+ The subnets together have at least three available IP addresses for the Kubernetes control plane instances\. If three subnets are specified, each subnet must have at least one available IP address\. If two subnets are specified, each subnet must have at least two available IP addresses\. If one subnet is specified, the subnet must have at least three available IP addresses\. 
+ The subnets have a route to the Outpost rack's [local gateway](https://docs.aws.amazon.com/outposts/latest/userguide/outposts-local-gateways.html) to access the Kubernetes API server over your local network\. If the subnets don't have a route to the Outpost rack's local gateway, you must communicate with your Kubernetes API server from within the VPC\.
+ The subnets must use IP address\-based naming\. Amazon EC2 [resource\-based naming](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-naming.html#instance-naming-rbn) isn't supported by Amazon EKS\.

## Subnet access to AWS services<a name="subnet-access-to-services"></a>

The local cluster's private subnets on Outposts must be able to communicate with Regional AWS services\. You can achieve this by using a [NAT gateway](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html) for outbound internet access or, if you want to keep all traffic private within your VPC, using [interface VPC endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/create-interface-endpoint.html)\. 

**Using a NAT gateway**  
The local cluster's private subnets on Outposts must have an associated route table that has a route to a NAT gateway in a public subnet that is in the Outpost's parent Availability Zone\. The public subnet must have a route to an [internet gateway](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html)\. The NAT gateway enables outbound internet access and prevents unsolicited inbound connections from the internet to instances on the Outpost\.

**Using interface VPC endpoints**  
If the local cluster's private subnets on Outposts don't have an outbound internet connection, or if you want to keep all traffic private within your VPC, then you must create the following interface VPC endpoints and [gateway endpoint](https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html) in a Regional subnet before creating your cluster\.<a name="vpc-subnet-requirements-vpc-endpoints"></a>


| Endpoint | Endpoint type | 
| --- | --- | 
| com\.amazonaws\.region\-code\.ssm | Interface | 
| com\.amazonaws\.region\-code\.ssmmessages | Interface | 
| com\.amazonaws\.region\-code\.ec2messages | Interface | 
| com\.amazonaws\.region\-code\.ec2 | Interface | 
| com\.amazonaws\.region\-code\.secretsmanager | Interface | 
| com\.amazonaws\.region\-code\.logs | Interface | 
| com\.amazonaws\.region\-code\.sts | Interface | 
| com\.amazonaws\.region\-code\.ecr\.api | Interface | 
| com\.amazonaws\.region\-code\.ecr\.dkr | Interface | 
| com\.amazonaws\.region\-code\.s3 | Gateway | 

The endpoints must meet the following requirements:
+ Created in a private subnet located in your Outpost's parent Availability Zone
+ Have private DNS names enabled
+ Have an attached security group that permits inbound HTTPS traffic from the CIDR range of the private outpost subnet\.

Creating endpoints incurs charges\. For more information, see [AWS PrivateLink pricing](https://aws.amazon.com/privatelink/pricing/)\. If your Pods need access to other AWS services, then you need to create additional endpoints\. For a comprehensive list of endpoints, see [AWS services that integrate with AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/aws-services-privatelink-support.html)\.

## Create a VPC<a name="outposts-create-vpc"></a>

You can create a VPC that meets the previous requirements using one of the following AWS CloudFormation templates:
+ **[Template 1](https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2022-09-20/amazon-eks-local-outposts-vpc-subnet.yaml)** – This template creates a VPC with one private subnet on the Outpost and one public subnet in the AWS Region\. The private subnet has a route to an internet through a NAT Gateway that resides in the public subnet in the AWS Region\. This template can be used to create a local cluster in a subnet with egress internet access\.
+ **[Template 2](https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2023-03-20/amazon-eks-local-outposts-fully-private-vpc-subnet.yaml)** – This template creates a VPC with one private subnet on the Outpost and the minimum set of VPC Endpoints required to create a local cluster in a subnet that doesn't have ingress or egress internet access \(also referred to as a private subnet\)\.