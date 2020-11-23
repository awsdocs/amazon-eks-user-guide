# Cluster VPC considerations<a name="network_reqs"></a>

When you create an Amazon EKS cluster, you specify the VPC subnets which influences where Amazon EKS places elastic network interfaces\. Amazon EKS requires subnets in at least two Availability Zones, and will create up to 4 network interfaces across these subnets to facilitate control plane communication to your nodes\. This communication channel supports Kubernetes functionality such as  `kubectl exec`  and  `kubectl logs`  \. The EKS created [cluster security group](sec-group-reqs.md#cluster-sg), as well as any additional security groups that you specify when you create your cluster are applied to these network interfaces\. 

Be sure that the subnets that you specify during cluster creation have enough available IP addresses for the EKS created network interfaces\. We recommend creating small (/29), dedicated subnets for EKS created network interfaces, and only specifying these subnets as part of cluster creation. Other resources such as worker nodes and load balancers should be launched in separate subnets from the ones specified during cluster creation. 

**Note**
Worker nodes and load balancers can be launched in any subnet in your VPC, including subnets not registered with EKS during cluster creation. Subnets do not require any tags for worker nodes. For Kubernetes load balancing auto discovery to work, subnets must be tagged in accordance with the [load balancing subnet tagging requirement](#vpc-subnet-tagging)\.

**Note** 
Subnets associated with your cluster cannot be changed after cluster creation. If you need to control exactly in which subnets the EKS created network interfaces are placed, then only pass in two subnets during cluster creation, each in a different Availability Zone\.

**Note**
There is a known issue where Amazon EKS cannot communicate with worker nodes launched in subnets from additional CIDR blocks added to a VPC after the cluster was first created. Please file a support ticket if you are experiencing this issue, so EKS can manually update your cluster to recognize the additional CIDR blocks added to the VPC. This doc page will be updated when a fix has been deployed so tickets are no longer required.

**Note**
Do not select a subnet in AWS Outposts, AWS Wavelength or an AWS Local Zone when creating your cluster.

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

This tag is not required or created by Amazon EKS for 1\.15 or later clusters\. If you deploy a 1\.15 or later cluster to a VPC that already has this tag, the tag is not removed\. However, you can safely remove this tag from any VPC used by an Amazon EKS cluster running version 1\.15 or later.

## Load balancing subnet tagging requirement<a name="vpc-subnet-tagging"></a>

Amazon EKS recommends running a cluster in a VPC with public and private subnets so that Kubernetes can create public load balancers in the public subnets that load balance traffic to pods running on nodes that are in private subnets\.

The Kubernetes service controller and the AWS load balancer controller can auto discover subnets to be used when provisioning Elastic Load Balancers in response to service or ingress objects. Your subnets must have the following tag requirements met in order for auto discovery to work. There are a total two tags required per subnet for each cluster.

**Note**
Application load balancers require at least two subnets in different Availability Zones. Network load balancers requires at least one subnet. The controllers will choose one subnet from each Availability Zone. In the case of multiple tagged subnets found in an Availability Zone, the controllers will choose the first subnet in lexicographical order by the subnet IDs.

**Note**
If you explicitly specify subnet IDs as an annotation on a service or ingress object, then Kubernetes and the AWS load balancer controller will use those subnets directly to create the load balancer. Subnet tagging is not required if you choose to use this method for provisioning load balancers, and you can skip this section.

### Cluster name tagging requirement for load balancers<a name="vpc-load-balancer-subnet-tagging"></a>

Subnets must be tagged with the cluster name as follows for auto discovery to work properly\.

| Key | Value | 
| --- | --- | 
| `kubernetes.io/cluster/<cluster-name>` | `shared` | 
+ **Key**: The `<cluster-name>` value matches your Amazon EKS cluster\. 
+ **Value**: The `shared` value allows more than one cluster to use this subnet\.

**Note**
Currently, Amazon EKS automatically adds the above tag to any subnet passed in during cluster creation. This behavior will be removed in an upcoming Amazon EKS release, and you should not rely on EKS to tag your subnets for load balancer subnet auto discovery\. 

### Private subnet tagging requirement for internal load balancers<a name="vpc-private-subnet-tagging"></a>

Private subnets must be tagged as follows so that Kubernetes and the AWS load balancer controller know it can use the subnets for internal load balancers\. If you use `eksctl` or an Amazon EKS AWS CloudFormation template to create your VPC after March 26, 2020, then the subnets are tagged appropriately when they're created\. For more information about the Amazon EKS AWS CloudFormation VPC templates, see [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md)\.


| Key | Value | 
| --- | --- | 
|  `kubernetes.io/role/internal-elb`  |  `1`  | 

### Public subnet tagging option for external load balancers<a name="vpc-public-subnet-tagging"></a>

Public subnets must be tagged as follows so that Kubernetes and the AWS load balancer controller know it can use the subnets for internet-facing load balancers. If you use `eksctl` or an Amazon EKS AWS CloudFormation template to create your VPC after March 26, 2020, then the subnets are tagged appropriately when they're created\. For more information about the Amazon EKS AWS CloudFormation VPC templates, see [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md)\.


| Key | Value | 
| --- | --- | 
| `kubernetes.io/role/elb` | `1` | 

**Note**
The Kubernetes service controller will examine the route table of subnets tagged with the cluster name tag to attempt to determine if the subnet is private or public if role tags are not explicitly added. However, we recommend you do not rely on this behavior, and instead explcitly add the private/public role tags as outlined above. The AWS load balancer controller will not examine route tables, and explictly requires the private/public role tags to be present for auto discovery to work\.
