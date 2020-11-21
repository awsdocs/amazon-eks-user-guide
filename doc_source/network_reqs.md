# Cluster VPC considerations<a name="network_reqs"></a>

Amazon EKS recommends running a cluster in a VPC with public and private subnets so that Kubernetes can create public load balancers in the public subnets that load balance traffic to pods running on nodes that are in private subnets\.

When you create an Amazon EKS cluster, you specify the VPC subnets for your cluster to use, which influences where Amazon EKS places elastic network interfaces\. Amazon EKS requires subnets in at least two Availability Zones, and will create up to 4 network interfaces across these subnets to facilitate control plane communication to your nodes\. This communication channel supports Kubernetes functionality such as  `kubectl exec`  and  `kubectl logs`  \. Be sure that the subnets that you specify have enough available IP addresses for the EKS created network interfaces\. The EKS created [cluster security group](sec-group-reqs.md#cluster-sg), as well as any additional security groups that you specify when you create your cluster are applied to these network interfaces\. 

**Note**  
Internet\-facing load balancers require a public subnet in your cluster\. By default, nodes also require outbound internet access to the Amazon EKS APIs for cluster introspection and node registration at launch time\. For clusters without outbound internet access, see [Private clusters](private-clusters.md)\.  
To pull container images, they require access to the Amazon S3 and Amazon ECR APIs \(and any other container registries, such as DockerHub\)\. For more information, see [Amazon EKS security group considerations](sec-group-reqs.md) and [AWS IP Address Ranges](https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html) in the *AWS General Reference*\.

As a convenience, Amazon EKS will automatically tag any subnet passed in during cluster creation in accordance with the [subnet tagging requirement](#vpc-subnet-tagging), so that Kubernetes can discover subnets that will host resources for your cluster, such as nodes and load balancers\. 

**Note** 
Subnets associated with your cluster cannot be changed after cluster creation. If you need to control exactly in which subnets the EKS created network interfaces are placed, then only pass in two subnets during cluster creation, each in a different Availability Zone. Worker nodes and load balancers can be launched in additional subnets not registered with your EKS cluster, as long as those subnets comply with the [subnet tagging requirement](#vpc-subnet-tagging).

**Note**
Do not select a subnet in AWS Outposts, AWS Wavelength or an AWS Local Zone when creating your cluster. After cluster creation, you can tag the AWS Outposts, AWS Wavelength or AWS Local Zone subnets according to the [subnet tagging requirement](#vpc-subnet-tagging).

It is possible to specify only public or private subnets when you create your cluster, but there are some limitations associated with these configurations:
+ **Private\-only**: Everything runs in a private subnet and Kubernetes cannot create internet\-facing load balancers for your pods\.
+ **Public\-only**: Everything runs in a public subnet, including your nodes\.

Your VPC must have DNS hostname and DNS resolution support\. Otherwise, your nodes cannot register with your cluster\. For more information, see [Using DNS with Your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns.html) in the *Amazon VPC User Guide*\.

## VPC IP addressing<a name="vpc-cidr"></a>

Nodes must be able to communicate with the control plane and other AWS services\. If your nodes are deployed in a private subnet, then you must have either:
+ Set up a default route for the subnet to a [NAT gateway](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)\. The NAT gateway must be assigned a public IP address to provide internet access for the nodes\. 
+ Configured several necessary settings for the subnet and taken the necessary actions listed in [Private clusters](private-clusters.md)\. 

If self\-managed nodes are deployed to a public subnet, the subnet must be configured to auto\-assign public IP addresses\. Otherwise, your node instances must be assigned a public IP address when they're [launched](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#vpc-public-ip)\. If managed nodes are deployed to a public subnet, the subnet must be configured to auto\-assign public IP addresses\. This is because, if they are not, then the nodes aren't assigned a public IP address\. Determine whether your public subnets are configured to auto\-assign public IP addresses with the following command\.

```
aws ec2 describe-subnets \
    --filters "Name=vpc-id,Values=<VPC-ID>" | grep 'SubnetId\|MapPublicIpOnLaunch'
```

The output is as follows\.

```
"MapPublicIpOnLaunch": <false>,
"SubnetId": "<subnet-aaaaaaaaaaaaaaaaa>",
"MapPublicIpOnLaunch": <false>,
"SubnetId": "<subnet-bbbbbbbbbbbbbbbbb>",
```

For any subnets that have `MapPublicIpOnLaunch` set to `false`, change the setting to `true`\.

```
aws ec2 modify-subnet-attribute --map-public-ip-on-launch --subnet-id <subnet-aaaaaaaaaaaaaaaaa>
```

**Important**  
If you used an [Amazon EKS AWS CloudFormation template](create-public-private-vpc.md) to deploy your VPC before March 26, 2020, then you need to change the setting for your public subnets\.

You can define both private \(RFC 1918\), and public \(non\-RFC 1918\) CIDR ranges within the VPC used for your Amazon EKS cluster\. For more information, see [Adding IPv4 CIDR blocks to a VPC](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html#vpc-resize) in the *Amazon VPC User Guide*\. When choosing the classless inter\-domain routing \(CIDR\) blocks for your VPC and subnets, make sure that the blocks contain enough IP addresses for all of the Amazon EC2 nodes and pods that you plan to deploy\. There should be at least one IP address for each of your pods\. You can conserve IP address use by implementing a transit gateway with a shared services VPC\. For more information, see [Isolated VPCs with shared services](https://docs.aws.amazon.com/vpc/latest/tgw/transit-gateway-isolated-shared.html) and [EKS VPC routable IP address conservation patterns in a hybrid network\.](http://aws.amazon.com/blogs/containers/eks-vpc-routable-ip-address-conservation/)

## VPC tagging requirement<a name="vpc-tagging"></a>

When you create an Amazon EKS cluster that is earlier than version 1\.15, Amazon EKS tags the VPC containing the subnets you specify in the following way:


| Key | Value | 
| --- | --- | 
|  `kubernetes.io/cluster/<cluster-name>`  |  `shared`  | 
+ **Key**: The `<cluster-name>` value matches your Amazon EKS cluster's name\. 
+ **Value**: The `shared` value allows more than one cluster to use this VPC\.

This tag is not required or created by Amazon EKS for 1\.15 or later clusters\. If you deploy a 1\.15 or later cluster to a VPC that already has this tag, the tag is not removed\.

## Subnet tagging requirement<a name="vpc-subnet-tagging"></a>

When you create your Amazon EKS cluster, Amazon EKS tags the subnets you specify in the following way so that Kubernetes can discover them:


| Key | Value | 
| --- | --- | 
| `kubernetes.io/cluster/<cluster-name>` | `shared` | 
+ **Key**: The `<cluster-name>` value matches your Amazon EKS cluster\. 
+ **Value**: The `shared` value allows more than one cluster to use this subnet\.

### Private subnet tagging requirement for internal load balancers<a name="vpc-private-subnet-tagging"></a>

Private subnets must be tagged as follows so that Kubernetes knows it can use the subnets for internal load balancers\. If you use `eksctl` or an Amazon EKS AWS CloudFormation template to create your VPC after March 26, 2020, then the subnets are tagged appropriately when they're created\. For more information about the Amazon EKS AWS CloudFormation VPC templates, see [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md)\.


| Key | Value | 
| --- | --- | 
|  `kubernetes.io/role/internal-elb`  |  `1`  | 

### Public subnet tagging option for external load balancers<a name="vpc-public-subnet-tagging"></a>

Public subnets must be tagged as follows so that Kubernetes knows to use only those subnets for external load balancers instead of choosing a public subnet in each Availability Zone \(in lexicographical order by subnet ID\)\. If you use `eksctl` or an Amazon EKS AWS CloudFormation template to create your VPC after March 26, 2020, then the subnets are tagged appropriately when they're created\. For more information about the Amazon EKS AWS CloudFormation VPC templates, see [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md)\.


| Key | Value | 
| --- | --- | 
| `kubernetes.io/role/elb` | `1` | 
