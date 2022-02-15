# Creating a VPC for your Amazon EKS cluster<a name="creating-a-vpc"></a>

Amazon Virtual Private Cloud \(Amazon VPC\) enables you to launch AWS resources into a virtual network that you've defined\. This virtual network closely resembles a traditional network that you'd operate in your own data center, with the benefits of using the scalable infrastructure of AWS\. For more information, see the [Amazon VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/) and [De\-mystifying cluster networking for Amazon EKS nodes](http://aws.amazon.com/blogs/containers/de-mystifying-cluster-networking-for-amazon-eks-worker-nodes)\.

If you want to use an existing VPC, then it must meet specific requirements for use with Amazon EKS\. For more information, see [Cluster VPC and subnet considerations](network_reqs.md)\. This topic guides you through creating a VPC for your cluster using one of the following configurations:
+ **Public and private subnets** – This VPC has two public and two private [subnets](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html)\. One public and one private subnet are deployed to the same [Availability Zone](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-regions-availability-zones)\. The other public and private subnets are deployed to a second Availability Zone in the same AWS Region\. We recommend this option for all production deployments\. This option allows you to deploy your nodes to private subnets and allows Kubernetes to deploy load balancers to the public subnets that can load balance traffic to pods running on nodes in the private subnets\.

  [Public IPv4 addresses](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#vpc-public-ipv4-addresses) are automatically assigned to nodes deployed to public subnets, but public IPv4 addresses are not assigned to nodes deployed to private subnets\. If you choose, you can also assign IPv6 addresses to nodes in public and private subnets\. The nodes in private subnets can communicate with the cluster and other AWS services, and pods can communicate outbound to the internet through a [NAT gateway](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html) \(IPv4\) or [egress\-only Internet gateway](https://docs.aws.amazon.com/vpc/latest/userguide/egress-only-internet-gateway.html) \(IPv6\) that is deployed in each Availability Zone\. A [security group](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html) is deployed that denies all inbound traffic and allows all outbound traffic\. The subnets are tagged so that Kubernetes is able to deploy load balancers to them\. For more information about subnet tagging, see [Subnet tagging](network_reqs.md#vpc-subnet-tagging)\. 

  For more information about this type of VPC, see [VPC with public and private subnets \(NAT\)](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario2.html)\.
+ **Only public subnets** – This VPC has three public subnets that are deployed into different Availability Zones in the region\. All nodes are automatically assigned public IPv4 addresses and can send and receive internet traffic through an internet gateway\. A [security group](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html) is deployed that denies all inbound traffic and allows all outbound traffic\. The subnets are tagged so that Kubernetes can deploy load balancers to them\. For more information about subnet tagging, see [Subnet tagging](network_reqs.md#vpc-subnet-tagging)\. For more information about this type of VPC, see [VPC with a single public subnet](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario1.html)\.
+ **Only private subnets** – This VPC has three private subnets that are deployed into different Availability Zones in the AWS Region\. All nodes can optionally send and receive internet traffic through a NAT instance or NAT gateway\. A [security group](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html) is deployed that denies all inbound traffic and allows all outbound traffic\. The subnets are tagged so that Kubernetes can deploy internal load balancers to them\. For more information about subnet tagging, see [Subnet tagging](network_reqs.md#vpc-subnet-tagging)\. For more information about this type of VPC, see [VPC with a private subnet only and AWS Site\-to\-Site VPN access](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario4.html)\.
**Important**  
There are additional requirements if the VPC does not have outbound internet access, such as via a NAT Instance, NAT Gateway, Egress\-only internet gateway, VPN, or Direct Connect\. You must bypass the EKS cluster introspection by providing the cluster certificate authority and cluster API endpoint to the nodes\. You also may need to configure VPC endpoints listed in [Modifying cluster endpoint access](cluster-endpoint.md#modify-endpoint-access)\.

**Important**  
If you deployed a VPC using `eksctl` or by using either of the Amazon EKS AWS CloudFormation VPC templates:  
On or after March 26, 2020 – Public IPv4 addresses are automatically assigned by public subnets to new nodes deployed to public subnets\.
Before March 26, 2020 – Public IPv4 addresses are not automatically assigned by public subnets to new nodes deployed to public subnets\.
This change impacts new node groups deployed to public subnets in the following ways:  
[Managed node groups](create-managed-node-group.md) – If the node group is deployed to a public subnet on or after April 22, 2020, the public subnet must have automatic assignment of public IP addresses enabled\. For more information, see [Modifying the public IPv4 addressing attribute for your subnet](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#subnet-public-ip)\.
[Linux](launch-workers.md), [Windows](launch-windows-workers.md), or [Arm](eks-optimized-ami.md#arm-ami) self\-managed node groups – If the node group is deployed to a public subnet on or after March 26, 2020, the public subnet must have automatic assignment of public IP addresses enabled or the nodes must be launched with a public IP address\. For more information, see [Modifying the public IPv4 addressing attribute for your subnet](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#subnet-public-ip) or [Assigning a public IPv4 address during instance launch](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#vpc-public-ip)\.

## Creating a VPC for your Amazon EKS cluster<a name="create-vpc"></a>

You can create a VPC with public and private subnets, only public subnets, or only private subnets\. Select the tab with the description of the type of VPC that you'd like to create\.

------
#### [ Public and private subnets ]<a name="vpc-public-private"></a>

**To create your cluster VPC with public and private subnets**

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. From the navigation bar, select an AWS Region that supports Amazon EKS\.

1. Choose **Create stack**, **With new resources \(standard\)**\.

1. Under **Prerequisite \- Prepare template**, make sure that **Template is ready** is selected and then under **Specify template**, select **Amazon S3 URL**\.

1. You can create an IPv4 network or an IPv6 network\. Paste one of the following URLs into the text area under **Amazon S3 URL** and choose **Next**:
   + IPv4

     ```
     https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-10-29/amazon-eks-vpc-private-subnets.yaml
     ```
   + IPv6

     ```
     https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-10-29/amazon-eks-ipv6-vpc-public-private-subnets.yaml
     ```

1. On the **Specify stack details** page, fill out the parameters accordingly, and then choose **Next**\.
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it **eks\-vpc**\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can't be longer than 128 characters\.
   + **VpcBlock**: Choose an IPv4 CIDR range for your VPC\. Each node, pod, and load balancer that you deploy is assigned an IPv4 address from this block\. The default IPv4 values provide enough IP addresses for most implementations, but if it doesn't, then you can change it\. For more information, see [VPC and subnet sizing](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html#VPC_Sizing) in the Amazon VPC User Guide\. You can also add additional CIDR blocks to the VPC once it's created\. If you're creating an IPv6 VPC, IPv6 CIDR ranges are automatically assigned for you from Amazon’s Global Unicast Address space\.
   + **PublicSubnet01Block**: Specify an IPv4 CIDR block for public subnet 1\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it\.\. If you're creating an IPv6 VPC, this block is specified for you within the template\.
   + **PublicSubnet02Block**: Specify an IPv4 CIDR block for public subnet 2\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it\. If you're creating an IPv6 VPC, this block is specified for you within the template\.
   + **PrivateSubnet01Block**: Specify an IPv4 CIDR block for private subnet 1\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it\. If you're creating an IPv6 VPC, this block is specified for you within the template\.
   + **PrivateSubnet02Block**: Specify an IPv4 CIDR block for private subnet 2\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it\. If you're creating an IPv6 VPC, this block is specified for you within the template\.

1. \(Optional\) On the **Configure stack options** page, tag your stack resources and then choose **Next**\.

1. On the **Review** page, choose **Create stack**\.

1. When your stack is created, select it in the console and choose **Outputs**\.

1. Record the **SecurityGroups** value for the security group that was created\. When you add nodes to your cluster, you must specify the ID of the security group\. The security group is applied to the elastic network interfaces that are created by Amazon EKS in your subnets that allows the control plane to communicate with your nodes\. These network interfaces have `Amazon EKS cluster name` in their description\.

1. Record the **VpcId** for the VPC that was created\. You need this when you launch your node group template\.

1. Record the **SubnetIds** for the subnets that were created and whether you created them as public or private subnets\. When you add nodes to your cluster, you must specify the IDs of the subnets that you want to launch the nodes into\.

1. If you created an IPv4 VPC, don't complete this step\. If you created an IPv6 VPC, then you must enable the auto\-assign IPv6 address option for the public subnets that were created by the template\. That setting is already enabled for the private subnets\. To enable the setting, complete the following steps\.

   1. Open the Amazon VPC console at [https://console\.aws\.amazon\.com/vpc/](https://console.aws.amazon.com/vpc/)\.

   1. In the navigation pane, choose **Subnets**

   1. Select one of your public subnets \(***stack\-name*/SubnetPublic01** or ***stack\-name*/SubnetPublic02** contains the word **public**\) and choose **Actions**, **Edit subnet settings**\.

   1. Choose the **Enable auto\-assign IPv6 address** check box and then choose **Save**\.

   1. Complete the previous steps again for your other public subnet\.

------
#### [ Only public subnets ]<a name="vpc-public-only"></a>

**To create your cluster VPC with only public subnets**

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. From the navigation bar, select an AWS Region that supports Amazon EKS\.

1. Choose **Create stack**, **With new resources \(standard\)**\.

1. Under **Prepare template**, make sure that **Template is ready** is selected and then under **Template source**, select **Amazon S3 URL**\.

1. Paste the following URL into the text area under **Amazon S3 URL** and choose **Next**:

   ```
   https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-10-29/amazon-eks-vpc-sample.yaml
   ```

1. On the **Specify Details** page, fill out the parameters accordingly, and then choose **Next**\.
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it **eks\-vpc**\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can't be longer than 128 characters\.
   + **VpcBlock**: Choose a CIDR block for your VPC\. Each node, pod, and load balancer that you deploy is assigned an IPv4 address from this block\. The default IPv4 values provide enough IP addresses for most implementations, but if it doesn't, then you can change it\. For more information, see [VPC and subnet sizing](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html#VPC_Sizing) in the Amazon VPC User Guide\. You can also add additional CIDR blocks to the VPC once it's created\.
   + **Subnet01Block**: Specify a CIDR block for subnet 1\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it\.
   + **Subnet02Block**: Specify a CIDR block for subnet 2\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it\.
   + **Subnet03Block**: Specify a CIDR block for subnet 3\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it\.

1. \(Optional\) On the **Options** page, tag your stack resources\. Choose **Next**\.

1. On the **Review** page, choose **Create**\.

1. When your stack is created, select it in the console and choose **Outputs**\.

1. Record the **SecurityGroups** value for the security group that was created\. When you add nodes to your cluster, you must specify the ID of the security group\. The security group is applied to the elastic network interfaces that are created by Amazon EKS in your subnets that allows the control plane to communicate with your nodes\. These network interfaces have `Amazon EKS cluster name` in their description\.

1. Record the **VpcId** for the VPC that was created\. You need this when you launch your node group template\.

1. Record the **SubnetIds** for the subnets that were created\. When you add nodes to your cluster, you must specify the IDs of the subnets that you want to launch the nodes into\.

1. \(Optional\) Any cluster that you deploy to this VPC is able to assign private IPv4 addresses to your pods and services\. If you want any clusters deployed to this VPC to assign private IPv6 addresses to your pods and services, then you must make updates to your VPC, subnet, route tables, and security groups\. For more information, see [Migrate existing VPCs from IPv4 to IPv6](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-migrate-ipv6.html) in the Amazon VPC User Guide\. Amazon EKS requires that your subnets have the `Auto-assign` IPv6 addresses option enabled \(it's disabled by default\)\.

------
#### [ Only private subnets ]<a name="vpc-private-only"></a>

**To create your cluster VPC with only private subnets**

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. From the navigation bar, select an AWS Region that supports Amazon EKS\.

1. Choose **Create stack**, **With new resources \(standard\)**\.

1. Under **Prepare template**, make sure that **Template is ready** is selected and then under **Template source**, select **Amazon S3 URL**\.

1. Paste the following URL into the text area under **Amazon S3 URL** and choose **Next**:

   ```
   https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-10-29/amazon-eks-fully-private-vpc.yaml
   ```

1. On the **Specify Details** page, fill out the parameters accordingly, and then choose **Next**\.
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it **eks\-vpc**\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can't be longer than 128 characters\.
   + **VpcBlock**: Choose a CIDR block for your VPC\. Each node, pod, and load balancer that you deploy is assigned an IPv4 address from this block\. The default IPv4 values provide enough IP addresses for most implementations, but if it doesn't, then you can change it\. For more information, see [VPC and subnet sizing](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html#VPC_Sizing) in the Amazon VPC User Guide\. You can also add additional CIDR blocks to the VPC once it's created\.
   + **PrivateSubnet01Block**: Specify a CIDR block for subnet 1\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it\.
   + **PrivateSubnet02Block**: Specify a CIDR block for subnet 2\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it\.
   + **PrivateSubnet03Block**: Specify a CIDR block for subnet 3\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it\.

1. \(Optional\) On the **Options** page, tag your stack resources\. Choose **Next**\.

1. On the **Review** page, choose **Create**\.

1. When your stack is created, select it in the console and choose **Outputs**\.

1. Record the **SecurityGroups** value for the security group that was created\. When you add nodes to your cluster, you must specify the ID of the security group\. The security group is applied to the elastic network interfaces that Amazon EKS creates in your subnets to allow the control plane to communicate with your nodes\. These network interfaces have `Amazon EKS cluster name` in their description\.

1. Record the **VpcId** for the VPC that was created\. You need this when you launch your node group template\.

1. Record the **SubnetIds** for the subnets that were created\. When you add nodes to your cluster, you must specify the IDs of the subnets that you want to launch the nodes into\.

1. \(Optional\) Any cluster that you deploy to this VPC is able to assign private IPv4 addresses to your pods and services\. If you want any clusters deployed to this VPC to assign private IPv6 addresses to your pods and services, then you must make updates to your VPC, subnet, route tables, and security groups\. For more information, see [Migrate existing VPCs from IPv4 to IPv6](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-migrate-ipv6.html) in the Amazon VPC User Guide\. Amazon EKS requires that your subnets have the `Auto-assign` IPv6 addresses option enabled \(it's disabled by default\)\.

------