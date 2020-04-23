# Creating a VPC for your Amazon EKS cluster<a name="create-public-private-vpc"></a>

Amazon Virtual Private Cloud \(Amazon VPC\) enables you to launch AWS resources into a virtual network that you've defined\. This virtual network closely resembles a traditional network that you'd operate in your own data center, with the benefits of using the scalable infrastructure of AWS\. For more information, see the [Amazon VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/) and [De\-mystifying cluster networking for Amazon EKS worker nodes](http://aws.amazon.com/blogs/containers/de-mystifying-cluster-networking-for-amazon-eks-worker-nodes)\.

If you want to use an existing VPC, then it must meet specific requirements for use with Amazon EKS\. For more information, see [Cluster VPC considerations](network_reqs.md)\. This topic guides you through creating a VPC for your cluster using one of the following configurations:
+ **Public and private subnets** – This VPC has two public and two private [subnets](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html)\. One public and one private subnet are deployed to the same [Availability Zone](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-regions-availability-zones)\. The other public and private subnets are deployed to a second Availability Zone in the same Region\. We recommend this option for all production deployments\. This option allows you to deploy your worker nodes to private subnets and allows Kubernetes to deploy load balancers to the public subnets that can load balance traffic to pods running on worker nodes in the private subnets\.

  [Public IP addresses](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#vpc-public-ipv4-addresses) are automatically assigned to resources deployed to one of the public subnets, but public IP addresses are not assigned to any resources deployed to the private subnets\. The worker nodes in private subnets can communicate with the cluster and other AWS services, and pods can communicate outbound to the internet through a [NAT gateway](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html) that is deployed in each Availability Zone\. A [security group](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html) is deployed that denies all inbound traffic and allows all outbound traffic\. The subnets are tagged so that Kubernetes is able to deploy load balancers to them\. For more information about subnet tagging, see [Subnet tagging requirement](network_reqs.md#vpc-subnet-tagging)\. For more information about this type of VPC, see [VPC with public and private subnets \(NAT\)](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario2.html)\.
+ **Only public subnets** – This VPC has three public subnets that are deployed into different Availability Zones in the region\. All worker nodes are automatically assigned public IP addresses and can send and receive internet traffic through an internet gateway\. A [security group](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html) is deployed that denies all inbound traffic and allows all outbound traffic\. The subnets are tagged so that Kubernetes can deploy load balancers to them\. For more information about subnet tagging, see [Subnet tagging requirement](network_reqs.md#vpc-subnet-tagging)\. For more information about this type of VPC, see [VPC with a single public subnet](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario1.html)\.

**Important**  
If you deployed a VPC using `eksctl` or by using either of the Amazon EKS AWS CloudFormation VPC templates:  
On or after 03/26/2020 – Public IPv4 addresses are automatically assigned by public subnets to new worker nodes deployed to public subnets\.
Before 03/26/2020 – Public IPv4 addresses are not automatically assigned by public subnets to new worker nodes deployed to public subnets\.
 This change impacts new node groups deployed to public subnets in the following ways:  
[Managed node groups](create-managed-node-group.md) – If the node group is deployed to a public subnet on or after 04/22/2020, the public subnet must have automatic assignment of public IP addresses enabled\. For more information, see [Modifying the public IPv4 addressing attribute for your subnet](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#subnet-public-ip)\.
[Linux](launch-workers.md), [Windows](launch-windows-workers.md), or [Arm](arm-support.md#launch-arm-worker-nodes) self\-managed node groups – If the node group is deployed to a public subnet on or after 03/26/2020, the public subnet must have automatic assignment of public IP addresses enabled or the worker nodes must be launched with a public IP address\. For more information, see [Modifying the public IPv4 addressing attribute for your subnet](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#subnet-public-ip) or [Assigning a public IPv4 address during instance launch](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#vpc-public-ip)\.

Choose the tab below that represents your desired VPC configuration\.

## Creating a VPC for your Amazon EKS cluster<a name="create-vpc"></a>

------
#### [ Public and private subnets ]

**To create your cluster VPC with public and private subnets**

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. From the navigation bar, select a Region that supports Amazon EKS\.

1. Choose **Create stack**\.

1. For **Choose a template**, select **Specify an Amazon S3 template URL**\.

1. Paste the following URL into the text area and choose **Next**:

   ```
   https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-04-21/amazon-eks-vpc-private-subnets.yaml
   ```

1. On the **Specify Details** page, fill out the parameters accordingly, and then choose **Next**\.
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it **eks\-vpc**\.
   + **VpcBlock**: Choose a CIDR range for your VPC\. You can keep the default value\.
   + **PublicSubnet01Block**: Specify a CIDR range for public subnet 1\. We recommend that you keep the default value so that you have plenty of IP addresses for load balancers to use\.
   + **PublicSubnet02Block**: Specify a CIDR range for public subnet 2\. We recommend that you keep the default value so that you have plenty of IP addresses for load balancers to use\.
   + **PrivateSubnet01Block**: Specify a CIDR range for private subnet 1\. We recommend that you keep the default value so that you have plenty of IP addresses for pods and load balancers to use\.
   + **PrivateSubnet02Block**: Specify a CIDR range for private subnet 2\. We recommend that you keep the default value so that you have plenty of IP addresses for pods and load balancers to use\.

1. \(Optional\) On the **Options** page, tag your stack resources\. Choose **Next**\.

1. On the **Review** page, choose **Create**\.

1. When your stack is created, select it in the console and choose **Outputs**\.

1. Record the **SecurityGroups** value for the security group that was created\. When you add worker nodes to your cluster, you must specify the ID of the security group\. The security group is applied to the cross\-account elastic network interfaces that are created in your subnets that allow the Amazon EKS control plane to communicate with your worker nodes\.

1. Record the **VpcId** for the VPC that was created\. You need this when you launch your worker node group template\.

1. Record the **SubnetIds** for the subnets that were created and whether you created them as public or private subnets\. When you add worker nodes to your cluster, you must specify the IDs of the subnets that you want to launch the worker nodes into\.

------
#### [ Only public subnets ]

**To create your cluster VPC with only public subnets**

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. From the navigation bar, select a Region that supports Amazon EKS\.

1. Choose **Create stack**\.

1. For **Choose a template**, select **Specify an Amazon S3 template URL**\.

1. Paste the following URL into the text area and choose **Next**:

   ```
   https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-04-21/amazon-eks-vpc-sample.yaml
   ```

1. On the **Specify Details** page, fill out the parameters accordingly, and then choose **Next**\.
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it **eks\-vpc**\.
   + **VpcBlock**: Choose a CIDR range for your VPC\. You can keep the default value\.
   + **Subnet01Block**: Specify a CIDR range for subnet 1\. We recommend that you keep the default value so that you have plenty of IP addresses for pods and load balancers to use\.
   + **Subnet02Block**: Specify a CIDR range for subnet 2\. We recommend that you keep the default value so that you have plenty of IP addresses for pods and load balancers to use\.
   + **Subnet03Block**: Specify a CIDR range for subnet 3\. We recommend that you keep the default value so that you have plenty of IP addresses for pods and load balancers to use\.

1. \(Optional\) On the **Options** page, tag your stack resources\. Choose **Next**\.

1. On the **Review** page, choose **Create**\.

1. When your stack is created, select it in the console and choose **Outputs**\.

1. Record the **SecurityGroups** value for the security group that was created\. When you add worker nodes to your cluster, you must specify the ID of the security group\. The security group is applied to the cross\-account elastic network interfaces that are created in your subnets that allow the Amazon EKS control plane to communicate with your worker nodes\.

1. Record the **VpcId** for the VPC that was created\. You need this when you launch your worker node group template\.

1. Record the **SubnetIds** for the subnets that were created\. When you add worker nodes to your cluster, you must specify the IDs of the subnets that you want to launch the worker nodes into\.

------

## Next steps<a name="vpc-next-steps"></a>

After you have created your VPC, you can try the [Getting started with Amazon EKS](getting-started.md) walkthrough, but you can skip the [Create your Amazon EKS cluster VPC](getting-started-console.md#vpc-create) section and use these subnets and security groups for your cluster\.