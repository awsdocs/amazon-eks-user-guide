# Creating a VPC for your Amazon EKS cluster<a name="create-public-private-vpc"></a>

Amazon Virtual Private Cloud \(Amazon VPC\) enables you to launch AWS resources into a virtual network that you've defined\. This virtual network closely resembles a traditional network that you'd operate in your own data center, with the benefits of using the scalable infrastructure of AWS\. For more information, see the [Amazon VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/) and [De\-mystifying cluster networking for Amazon EKS nodes](http://aws.amazon.com/blogs/containers/de-mystifying-cluster-networking-for-amazon-eks-worker-nodes)\.

If you want to use an existing VPC, then it must meet specific requirements for use with Amazon EKS\. For more information, see [Cluster VPC considerations](network_reqs.md)\. This topic guides you through creating a VPC for your cluster using one of the following configurations:
+ **Public and private subnets** – This VPC has two public and two private [subnets](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html)\. One public and one private subnet are deployed to the same [Availability Zone](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-regions-availability-zones)\. The other public and private subnets are deployed to a second Availability Zone in the same Region\. We recommend this option for all production deployments\. This option allows you to deploy your nodes to private subnets and allows Kubernetes to deploy load balancers to the public subnets that can load balance traffic to pods running on nodes in the private subnets\.

  [Public IP addresses](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#vpc-public-ipv4-addresses) are automatically assigned to resources deployed to one of the public subnets, but public IP addresses are not assigned to any resources deployed to the private subnets\. The nodes in private subnets can communicate with the cluster and other AWS services, and pods can communicate outbound to the internet through a [NAT gateway](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html) that is deployed in each Availability Zone\. A [security group](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html) is deployed that denies all inbound traffic and allows all outbound traffic\. The subnets are tagged so that Kubernetes is able to deploy load balancers to them\. For more information about subnet tagging, see [Subnet tagging requirement](network_reqs.md#vpc-subnet-tagging)\. For more information about this type of VPC, see [VPC with public and private subnets \(NAT\)](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario2.html)\.
+ **Only public subnets** – This VPC has three public subnets that are deployed into different Availability Zones in the region\. All nodes are automatically assigned public IP addresses and can send and receive internet traffic through an internet gateway\. A [security group](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html) is deployed that denies all inbound traffic and allows all outbound traffic\. The subnets are tagged so that Kubernetes can deploy load balancers to them\. For more information about subnet tagging, see [Subnet tagging requirement](network_reqs.md#vpc-subnet-tagging)\. For more information about this type of VPC, see [VPC with a single public subnet](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario1.html)\.
+ **Only private subnets** – This VPC has three private subnets that are deployed into different Availability Zones in the Region\. All nodes can optionally send and receive internet traffic through a NAT instance or NAT gateway\. A [security group](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html) is deployed that denies all inbound traffic and allows all outbound traffic\. The subnets are tagged so that Kubernetes can deploy internal load balancers to them\. For more information about subnet tagging, see [Subnet tagging requirement](network_reqs.md#vpc-subnet-tagging)\. For more information about this type of VPC, see [VPC with a private subnet only and AWS Site\-to\-Site VPN access](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario4.html)\.
**Important**  
There are additional requirements if the VPC does not have outbound internet access, such as via a NAT Instance, NAT Gateway, VPN, or Direct Connect\. You must bypass the EKS cluster introspection by providing the cluster certificate authority and cluster API endpoint to the nodes\. You also may need to configure VPC endpoints listed in [Modifying cluster endpoint access](cluster-endpoint.md#modify-endpoint-access)\.

**Important**  
If you deployed a VPC using `eksctl` or by using either of the Amazon EKS AWS CloudFormation VPC templates:  
On or after March 26, 2020 – Public IPv4 addresses are automatically assigned by public subnets to new nodes deployed to public subnets\.
Before March 26, 2020 – Public IPv4 addresses are not automatically assigned by public subnets to new nodes deployed to public subnets\.
 This change impacts new node groups deployed to public subnets in the following ways:  
[Managed node groups](create-managed-node-group.md) – If the node group is deployed to a public subnet on or after April 22, 2020, the public subnet must have automatic assignment of public IP addresses enabled\. For more information, see [Modifying the public IPv4 addressing attribute for your subnet](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#subnet-public-ip)\.
[Linux](launch-workers.md), [Windows](launch-windows-workers.md), or [Arm](eks-optimized-ami.md#arm-ami) self\-managed node groups – If the node group is deployed to a public subnet on or after March 26, 2020, the public subnet must have automatic assignment of public IP addresses enabled or the nodes must be launched with a public IP address\. For more information, see [Modifying the public IPv4 addressing attribute for your subnet](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#subnet-public-ip) or [Assigning a public IPv4 address during instance launch](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#vpc-public-ip)\.

## Creating a VPC for your Amazon EKS cluster<a name="create-vpc"></a>

You can create a VPC with [public and private subnets](#vpc-public-private), only [public subnets](#vpc-public-only), or only [private subnets](#vpc-private-only)\.<a name="vpc-public-private"></a>

**To create your cluster VPC with public and private subnets**

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. From the navigation bar, select a Region that supports Amazon EKS\.

1. Choose **Create stack**, **With new resources \(standard\)**\.

1. For **Choose a template**, select **Specify an Amazon S3 template URL**\.

1. Paste the URL that corresponds to the Region that your cluster is in into the text area and choose **Next**:
   + All Regions other than China Regions\.

     ```
     https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-vpc-private-subnets.yaml
     ```
   + Beijing and Ningxia China Regions\.

     ```
     https://s3.cn-north-1.amazonaws.com.cn/amazon-eks/cloudformation/2020-10-29/amazon-eks-vpc-private-subnets.yaml
     ```

1. On the **Specify Details** page, fill out the parameters accordingly, and then choose **Next**\.
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it **eks\-vpc**\.
   + **VpcBlock**: Choose a CIDR range for your VPC\. Each worker node, pod, and load balancer that you deploy is assigned an IP address from this block\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it\. For more information, see [VPC and subnet sizing](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html#VPC_Sizing) in the Amazon VPC User Guide\. You can also add additional CIDR blocks to the VPC once it's created\.
   + **PublicSubnet01Block**: Specify a CIDR block for public subnet 1\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it
   + **PublicSubnet02Block**: Specify a CIDR block for public subnet 2\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it
   + **PrivateSubnet01Block**: Specify a CIDR block for private subnet 1\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it
   + **PrivateSubnet02Block**: Specify a CIDR block for private subnet 2\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it

1. \(Optional\) On the **Options** page, tag your stack resources\. Choose **Next**\.

1. On the **Review** page, choose **Create**\.

1. When your stack is created, select it in the console and choose **Outputs**\.

1. Record the **SecurityGroups** value for the security group that was created\. When you add nodes to your cluster, you must specify the ID of the security group\. The security group is applied to the elastic network interfaces that are created by Amazon EKS in your subnets that allows the control plane to communicate with your nodes\. These network interfaces have `Amazon EKS <cluster name>` in their description\.

1. Record the **VpcId** for the VPC that was created\. You need this when you launch your node group template\.

1. Record the **SubnetIds** for the subnets that were created and whether you created them as public or private subnets\. When you add nodes to your cluster, you must specify the IDs of the subnets that you want to launch the nodes into\.<a name="vpc-public-only"></a>

**To create your cluster VPC with only public subnets**

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. From the navigation bar, select a Region that supports Amazon EKS\.

1. Choose **Create stack**, **With new resources \(standard\)**\.

1. For **Choose a template**, select **Specify an Amazon S3 template URL**\.

1. Paste the URL that corresponds to the Region that your cluster is in into the text area and choose **Next**:
   + All Regions other than China Regions\.

     ```
     https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-vpc-sample.yaml
     ```
   + Beijing and Ningxia China Regions\.

     ```
     https://s3.cn-north-1.amazonaws.com.cn/amazon-eks/cloudformation/2020-10-29/amazon-eks-vpc-sample.yaml
     ```

1. On the **Specify Details** page, fill out the parameters accordingly, and then choose **Next**\.
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it **eks\-vpc**\.
   + **VpcBlock**: Choose a CIDR block for your VPC\. Each worker node, pod, and load balancer that you deploy is assigned an IP address from this block\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it\. For more information, see [VPC and subnet sizing](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html#VPC_Sizing) in the Amazon VPC User Guide\. You can also add additional CIDR blocks to the VPC once it's created\.
   + **Subnet01Block**: Specify a CIDR block for subnet 1\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it
   + **Subnet02Block**: Specify a CIDR block for subnet 2\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it
   + **Subnet03Block**: Specify a CIDR block for subnet 3\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it

1. \(Optional\) On the **Options** page, tag your stack resources\. Choose **Next**\.

1. On the **Review** page, choose **Create**\.

1. When your stack is created, select it in the console and choose **Outputs**\.

1. Record the **SecurityGroups** value for the security group that was created\. When you add nodes to your cluster, you must specify the ID of the security group\. The security group is applied to the elastic network interfaces that are created by Amazon EKS in your subnets that allows the control plane to communicate with your nodes\. These network interfaces have `Amazon EKS <cluster name>` in their description\.

1. Record the **VpcId** for the VPC that was created\. You need this when you launch your node group template\.

1. Record the **SubnetIds** for the subnets that were created\. When you add nodes to your cluster, you must specify the IDs of the subnets that you want to launch the nodes into\.<a name="vpc-private-only"></a>

**To create your cluster VPC with only private subnets**

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. From the navigation bar, select a Region that supports Amazon EKS\.

1. Choose **Create stack**, **With new resources \(standard\)**\.

1. For **Choose a template**, select **Specify an Amazon S3 template URL**\.

1. Paste the URL that corresponds to the Region that your cluster is in into the text area and choose **Next**:
   + All Regions other than China Regions\.

     ```
     https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-fully-private-vpc.yaml 
     ```
   + Beijing and Ningxia China Regions\.

     ```
     https://s3.cn-north-1.amazonaws.com.cn/amazon-eks/cloudformation/2020-10-29/amazon-eks-fully-private-vpc.yaml 
     ```

1. On the **Specify Details** page, fill out the parameters accordingly, and then choose **Next**\.
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it **eks\-vpc**\.
   + **VpcBlock**: Choose a CIDR block for your VPC\. Each worker node, pod, and load balancer that you deploy is assigned an IP address from this block\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it\. For more information, see [VPC and subnet sizing](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html#VPC_Sizing) in the Amazon VPC User Guide\. You can also add additional CIDR blocks to the VPC once it's created\.
   + **PrivateSubnet01Block**: Specify a CIDR block for subnet 1\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it
   + **PrivateSubnet02Block**: Specify a CIDR block for subnet 2\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it
   + **PrivateSubnet03Block**: Specify a CIDR block for subnet 3\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it

1. \(Optional\) On the **Options** page, tag your stack resources\. Choose **Next**\.

1. On the **Review** page, choose **Create**\.

1. When your stack is created, select it in the console and choose **Outputs**\.

1. Record the **SecurityGroups** value for the security group that was created\. When you add nodes to your cluster, you must specify the ID of the security group\. The security group is applied to the elastic network interfaces that Amazon EKS creates in your subnets to allow the control plane to communicate with your nodes\. These network interfaces have `Amazon EKS <cluster name>` in their description\.

1. Record the **VpcId** for the VPC that was created\. You need this when you launch your node group template\.

1. Record the **SubnetIds** for the subnets that were created\. When you add nodes to your cluster, you must specify the IDs of the subnets that you want to launch the nodes into\.

## Next steps<a name="vpc-next-steps"></a>

After you have created your VPC, you can try the [Getting started with Amazon EKS](getting-started.md) walkthrough\.