# Creating a VPC for your Amazon EKS cluster<a name="creating-a-vpc"></a>

You can use Amazon Virtual Private Cloud \(Amazon VPC\) to launch AWS resources into a virtual network that you've defined\. This virtual network closely resembles a traditional network that you might operate in your own data center\. However, it comes with the benefits of using the scalable infrastructure of Amazon Web Services\. We recommend that you have a thorough understanding of the Amazon VPC service before deploying production Amazon EKS clusters\. For more information, see the [Amazon VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/)\.

An Amazon EKS cluster, nodes, and Kubernetes resources are deployed to a VPC\. If you want to use an existing VPC with Amazon EKS, that VPC must meet the requirements that are described in [Amazon EKS VPC and subnet requirements and considerations](network_reqs.md)\. This topic describes how to create a VPC that meets Amazon EKS requirements using an Amazon EKS provided AWS CloudFormation template\. Once you've deployed a template, you can view the resources created by the template to know exactly what resources it created, and the configuration of those resources\.

**Prerequisite**  
To create a VPC for Amazon EKS, you must have the necessary IAM permissions to create Amazon VPC resources\. These resources are VPCs, subnets, security groups, route tables and routes, and internet and NAT gateways\. For more information, see [Create a VPC with a public subnet example policy](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-policy-examples.html#vpc-public-subnet-iam) in the Amazon VPC User Guide and the full list of [Actions, resources, and condition keys for Amazon EC2](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonec2.html#amazonec2-actions-as-permissions) in the [Service Authorization Reference](https://docs.aws.amazon.com/service-authorization/latest/reference/reference.html)\.

You can create a VPC with public and private subnets, only public subnets, or only private subnets\.

------
#### [ Public and private subnets ]

This VPC has two public and two private subnets\. A public subnet's associated route table has a route to an internet gateway\. However, the route table of a private subnet doesn't have a route to an internet gateway\. One public and one private subnet are deployed to the same Availability Zone\. The other public and private subnets are deployed to a second Availability Zone in the same AWS Region\. We recommend this option for most deployments\.

With this option, you can deploy your nodes to private subnets\. This option allows Kubernetes to deploy load balancers to the public subnets that can load balance traffic to Pods that run on nodes in the private subnets\. Public `IPv4` addresses are automatically assigned to nodes that are deployed to public subnets, but public `IPv4` addresses aren't assigned to nodes deployed to private subnets\.

You can also assign `IPv6` addresses to nodes in public and private subnets\. The nodes in private subnets can communicate with the cluster and other AWS services\. Pods can communicate to the internet through a NAT gateway using `IPv4` addresses or outbound\-only Internet gateway using `IPv6` addresses deployed in each Availability Zone\. A security group is deployed that has rules that deny all inbound traffic from sources other than the cluster or nodes but allows all outbound traffic\. The subnets are tagged so that Kubernetes can deploy load balancers to them\.

**To create your VPC**

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. From the navigation bar, select an AWS Region that supports Amazon EKS\.

1. Choose **Create stack**, **With new resources \(standard\)**\.

1. Under **Prerequisite \- Prepare template**, make sure that **Template is ready** is selected and then under **Specify template**, select **Amazon S3 URL**\.

1. You can create a VPC that supports only `IPv4`, or a VPC that supports `IPv4` and `IPv6`\. Paste one of the following URLs into the text area under **Amazon S3 URL** and choose **Next**:
   + `IPv4`

     ```
     https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-vpc-private-subnets.yaml
     ```
   + `IPv4` and `IPv6`

     ```
     https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-ipv6-vpc-public-private-subnets.yaml
     ```

1. On the **Specify stack details** page, enter the parameters, and then choose **Next**\.
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can use the template name you used in the previous step\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can't be longer than 100 characters\.
   + **VpcBlock**: Choose an `IPv4` CIDR range for your VPC\. Each node, Pod, and load balancer that you deploy is assigned an `IPv4` address from this block\. The default `IPv4` values provide enough IP addresses for most implementations, but if it doesn't, then you can change it\. For more information, see [VPC and subnet sizing](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html#VPC_Sizing) in the Amazon VPC User Guide\. You can also add additional CIDR blocks to the VPC once it's created\. If you're creating an `IPv6` VPC, `IPv6` CIDR ranges are automatically assigned for you from Amazon's Global Unicast Address space\.
   + **PublicSubnet01Block**: Specify an `IPv4` CIDR block for public subnet 1\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it\. If you're creating an `IPv6` VPC, this block is specified for you within the template\.
   + **PublicSubnet02Block**: Specify an `IPv4` CIDR block for public subnet 2\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it\. If you're creating an `IPv6` VPC, this block is specified for you within the template\.
   + **PrivateSubnet01Block**: Specify an `IPv4` CIDR block for private subnet 1\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it\. If you're creating an `IPv6` VPC, this block is specified for you within the template\.
   + **PrivateSubnet02Block**: Specify an `IPv4` CIDR block for private subnet 2\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it\. If you're creating an `IPv6` VPC, this block is specified for you within the template\.

1. \(Optional\) On the **Configure stack options** page, tag your stack resources and then choose **Next**\.

1. On the **Review** page, choose **Create stack**\.

1. When your stack is created, select it in the console and choose **Outputs**\.

1. Record the **VpcId** for the VPC that was created\. You need this when you create your cluster and nodes\.

1. Record the **SubnetIds** for the subnets that were created and whether you created them as public or private subnets\. You need at least two of these when you create your cluster and nodes\.

1. If you created an `IPv4` VPC, skip this step\. If you created an `IPv6` VPC, you must enable the auto\-assign `IPv6` address option for the public subnets that were created by the template\. That setting is already enabled for the private subnets\. To enable the setting, complete the following steps:

   1. Open the Amazon VPC console at [https://console\.aws\.amazon\.com/vpc/](https://console.aws.amazon.com/vpc/)\.

   1. In the left navigation pane, choose **Subnets**

   1. Select one of your public subnets \(***stack\-name*/SubnetPublic01** or ***stack\-name*/SubnetPublic02** contains the word **public**\) and choose **Actions**, **Edit subnet settings**\.

   1. Choose the **Enable auto\-assign `IPv6` address** check box and then choose **Save**\.

   1. Complete the previous steps again for your other public subnet\.

------
#### [ Only public subnets ]

This VPC has three public subnets that are deployed into different Availability Zones in an AWS Region\. All nodes are automatically assigned public `IPv4` addresses and can send and receive internet traffic through an [internet gateway](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html)\. A [security group](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html) is deployed that denies all inbound traffic and allows all outbound traffic\. The subnets are tagged so that Kubernetes can deploy load balancers to them\.

**To create your VPC**

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. From the navigation bar, select an AWS Region that supports Amazon EKS\.

1. Choose **Create stack**, **With new resources \(standard\)**\.

1. Under **Prepare template**, make sure that **Template is ready** is selected and then under **Template source**, select **Amazon S3 URL**\.

1. Paste the following URL into the text area under **Amazon S3 URL** and choose **Next**:

   ```
   https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-vpc-sample.yaml
   ```

1. On the **Specify Details** page, enter the parameters, and then choose **Next**\.
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it **`amazon-eks-vpc-sample`**\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can't be longer than 100 characters\.
   + **VpcBlock**: Choose a CIDR block for your VPC\. Each node, Pod, and load balancer that you deploy is assigned an `IPv4` address from this block\. The default `IPv4` values provide enough IP addresses for most implementations, but if it doesn't, then you can change it\. For more information, see [VPC and subnet sizing](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html#VPC_Sizing) in the Amazon VPC User Guide\. You can also add additional CIDR blocks to the VPC once it's created\.
   + **Subnet01Block**: Specify a CIDR block for subnet 1\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it\.
   + **Subnet02Block**: Specify a CIDR block for subnet 2\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it\.
   + **Subnet03Block**: Specify a CIDR block for subnet 3\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it\.

1. \(Optional\) On the **Options** page, tag your stack resources\. Choose **Next**\.

1. On the **Review** page, choose **Create**\.

1. When your stack is created, select it in the console and choose **Outputs**\.

1. Record the **VpcId** for the VPC that was created\. You need this when you create your cluster and nodes\.

1. Record the **SubnetIds** for the subnets that were created\. You need at least two of these when you create your cluster and nodes\.

1. \(Optional\) Any cluster that you deploy to this VPC can assign private `IPv4` addresses to your Pods and services\. If you want to deploy clusters to this VPC to assign private `IPv6` addresses to your Pods and services, make updates to your VPC, subnet, route tables, and security groups\. For more information, see [Migrate existing VPCs from `IPv4` to `IPv6`](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-migrate-ipv6.html) in the Amazon VPC User Guide\. Amazon EKS requires that your subnets have the `Auto-assign` `IPv6` addresses option enabled\. By default, it's disabled\.

------
#### [ Only private subnets ]

This VPC has three private subnets that are deployed into different Availability Zones in the AWS Region\. Resources that are deployed to the subnets can't access the internet, nor can the internet access resources in the subnets\. The template creates [VPC endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/privatelink-access-aws-services.html) using AWS PrivateLink for several AWS services that nodes typically need to access\. If your nodes need outbound internet access, you can add a public [NAT gateway](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html) in the Availability Zone of each subnet after the VPC is created\. A [security group](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html) is created that denies all inbound traffic, except from resources deployed into the subnets\. A security group also allows all outbound traffic\. The subnets are tagged so that Kubernetes can deploy internal load balancers to them\. If you're creating a VPC with this configuration, see [Private cluster requirements](private-clusters.md) for additional requirements and considerations\.

**To create your VPC**

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. From the navigation bar, select an AWS Region that supports Amazon EKS\.

1. Choose **Create stack**, **With new resources \(standard\)**\.

1. Under **Prepare template**, make sure that **Template is ready** is selected and then under **Template source**, select **Amazon S3 URL**\.

1. Paste the following URL into the text area under **Amazon S3 URL** and choose **Next**:

   ```
   https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-fully-private-vpc.yaml
   ```

1. On the **Specify Details** page, enter the parameters and then choose **Next**\.
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it **`amazon-eks-fully-private-vpc`**\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can't be longer than 100 characters\.
   + **VpcBlock**: Choose a CIDR block for your VPC\. Each node, Pod, and load balancer that you deploy is assigned an `IPv4` address from this block\. The default `IPv4` values provide enough IP addresses for most implementations, but if it doesn't, then you can change it\. For more information, see [VPC and subnet sizing](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html#VPC_Sizing) in the Amazon VPC User Guide\. You can also add additional CIDR blocks to the VPC once it's created\.
   + **PrivateSubnet01Block**: Specify a CIDR block for subnet 1\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it\.
   + **PrivateSubnet02Block**: Specify a CIDR block for subnet 2\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it\.
   + **PrivateSubnet03Block**: Specify a CIDR block for subnet 3\. The default value provides enough IP addresses for most implementations, but if it doesn't, then you can change it\.

1. \(Optional\) On the **Options** page, tag your stack resources\. Choose **Next**\.

1. On the **Review** page, choose **Create**\.

1. When your stack is created, select it in the console and choose **Outputs**\.

1. Record the **VpcId** for the VPC that was created\. You need this when you create your cluster and nodes\.

1. Record the **SubnetIds** for the subnets that were created\. You need at least two of these when you create your cluster and nodes\.

1. \(Optional\) Any cluster that you deploy to this VPC can assign private `IPv4` addresses to your Pods and services\. If you want deploy clusters to this VPC to assign private `IPv6` addresses to your Pods and services, make updates to your VPC, subnet, route tables, and security groups\. For more information, see [Migrate existing VPCs from `IPv4` to `IPv6`](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-migrate-ipv6.html) in the Amazon VPC User Guide\. Amazon EKS requires that your subnets have the `Auto-assign` `IPv6` addresses option enabled \(it's disabled by default\)\.

------