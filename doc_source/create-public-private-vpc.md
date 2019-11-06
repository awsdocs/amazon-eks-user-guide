# Creating a VPC for Your Amazon EKS Cluster<a name="create-public-private-vpc"></a>

Amazon Virtual Private Cloud \(Amazon VPC\) enables you to launch AWS resources into a virtual network that you've defined\. This virtual network closely resembles a traditional network that you'd operate in your own data center, with the benefits of using the scalable infrastructure of AWS\. For more information, see the [Amazon VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/)\.

This topic guides you through creating a VPC for your cluster with either 3 public subnets, or two public subnets and two private subnets, which are provided with internet access through a NAT gateway\. You can use this VPC for your Amazon EKS cluster\. We recommend a network architecture that uses private subnets for your worker nodes, and public subnets for Kubernetes to create public load balancers within\.

Choose the tab below that represents your desired VPC configuration\.

------
#### [ Only public subnets ]

**To create your cluster VPC with only public subnets**

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. From the navigation bar, select a Region that supports Amazon EKS\.

1. Choose **Create stack**\.

1. For **Choose a template**, select **Specify an Amazon S3 template URL**\.

1. Paste the following URL into the text area and choose **Next**:

   ```
   https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-10-08/amazon-eks-vpc-sample.yaml
   ```

1. On the **Specify Details** page, fill out the parameters accordingly, and then choose **Next**\.
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it **eks\-vpc**\.
   + **VpcBlock**: Choose a CIDR range for your VPC\. You can keep the default value\.
   + **Subnet01Block**: Specify a CIDR range for subnet 1\. We recommend that you keep the default value so that you have plenty of IP addresses for pods to use\.
   + **Subnet02Block**: Specify a CIDR range for subnet 2\. We recommend that you keep the default value so that you have plenty of IP addresses for pods to use\.
   + **Subnet03Block**: Specify a CIDR range for subnet 3\. We recommend that you keep the default value so that you have plenty of IP addresses for pods to use\.

1. \(Optional\) On the **Options** page, tag your stack resources\. Choose **Next**\.

1. On the **Review** page, choose **Create**\.

1. When your stack is created, select it in the console and choose **Outputs**\.

1. Record the **SecurityGroups** value for the security group that was created\. You need this when you create your EKS cluster; this security group is applied to the cross\-account elastic network interfaces that are created in your subnets that allow the Amazon EKS control plane to communicate with your worker nodes\.

1. Record the **VpcId** for the VPC that was created\. You need this when you launch your worker node group template\.

1. Record the **SubnetIds** for the subnets that were created\. You need this when you create your EKS cluster; these are the subnets that your worker nodes are launched into\.

------
#### [ Public and private subnets ]

**To create your cluster VPC with public and private subnets**

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. From the navigation bar, select a Region that supports Amazon EKS\.

1. Choose **Create stack**\.

1. For **Choose a template**, select **Specify an Amazon S3 template URL**\.

1. Paste the following URL into the text area and choose **Next**:

   ```
   https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-10-08/amazon-eks-vpc-private-subnets.yaml
   ```

1. On the **Specify Details** page, fill out the parameters accordingly, and then choose **Next**\.
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it **eks\-vpc**\.
   + **VpcBlock**: Choose a CIDR range for your VPC\. You can keep the default value\.
   + **PublicSubnet01Block**: Specify a CIDR range for public subnet 1\. We recommend that you keep the default value so that you have plenty of IP addresses for pods to use\.
   + **PublicSubnet02Block**: Specify a CIDR range for public subnet 2\. We recommend that you keep the default value so that you have plenty of IP addresses for pods to use\.
   + **PrivateSubnet01Block**: Specify a CIDR range for private subnet 1\. We recommend that you keep the default value so that you have plenty of IP addresses for pods to use\.
   + **PrivateSubnet02Block**: Specify a CIDR range for private subnet 2\. We recommend that you keep the default value so that you have plenty of IP addresses for pods to use\.

1. \(Optional\) On the **Options** page, tag your stack resources\. Choose **Next**\.

1. On the **Review** page, choose **Create**\.

1. When your stack is created, select it in the console and choose **Outputs**\.

1. Record the **SecurityGroups** value for the security group that was created\. You need this when you create your EKS cluster; this security group is applied to the cross\-account elastic network interfaces that are created in your subnets that allow the Amazon EKS control plane to communicate with your worker nodes\.

1. Record the **VpcId** for the VPC that was created\. You need this when you launch your worker node group template\.

1. Record the **SubnetIds** for the subnets that were created\. You need this when you create your EKS cluster; these are the subnets that your worker nodes are launched into\.

1. Tag your private subnets so that Kubernetes knows that it can use them for internal load balancers\.

   1. Open the Amazon VPC console at [https://console\.aws\.amazon\.com/vpc/](https://console.aws.amazon.com/vpc/)\.

   1. Choose **Subnets** in the left navigation\.

   1. Select one of the private subnets for your Amazon EKS cluster's VPC \(you can filter them with the string `PrivateSubnet`\), and choose the **Tags** tab, and then **Add/Edit Tags**\.

   1. Choose **Create Tag** and add the following key and value, and then choose **Save**\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/create-public-private-vpc.html)

   1. Repeat these substeps for each private subnet in your VPC\.

------

## Next Steps<a name="vpc-next-steps"></a>

After you have created your VPC, you can try the [Getting Started with Amazon EKS](getting-started.md) walkthrough, but you can skip the [Create your Amazon EKS Cluster VPC](getting-started-console.md#vpc-create) section and use these subnets and security groups for your cluster\.