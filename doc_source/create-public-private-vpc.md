# Tutorial: Creating a VPC with Public and Private Subnets for Your Amazon EKS Cluster<a name="create-public-private-vpc"></a>

This tutorial guides you through creating a VPC with two public subnets and two private subnets, which are provided with internet access through a NAT gateway\. You can use this VPC for your Amazon EKS cluster\. We recommend a network architecture that uses private subnets for your worker nodes, and public subnets for Kubernetes to create public load balancers within\. 

**Topics**
+ [Step 1: Create an Elastic IP Address for Your NAT Gateway](#create-EIP)
+ [Step 2: Run the VPC Wizard](#run-VPC-wizard)
+ [Step 3: Create Additional Subnets](#create-add-subnets)
+ [Step 4: Tag your Private Subnets](#vpc-tag-private-subnets)
+ [Step 5: Create a Control Plane Security Group](#vpc-create-sg)
+ [Next Steps](#vpc-next-steps)

## Step 1: Create an Elastic IP Address for Your NAT Gateway<a name="create-EIP"></a>

Worker nodes in private subnets require a NAT gateway for outbound internet access\. A NAT gateway requires an Elastic IP address in your public subnet, but the VPC wizard does not create one for you\. Create the Elastic IP address before running the VPC wizard\.

**To create an Elastic IP address**

1. Open the Amazon VPC console at [https://console\.aws\.amazon\.com/vpc/](https://console.aws.amazon.com/vpc/)\.

1. In the left navigation pane, choose **Elastic IPs**\.

1. Choose **Allocate new address**, **Allocate**, **Close**\.

1. Note the **Allocation ID** for your newly created Elastic IP address; you enter this later in the VPC wizard\.

## Step 2: Run the VPC Wizard<a name="run-VPC-wizard"></a>

The VPC wizard automatically creates and configures most of your VPC resources for you\.

**To run the VPC wizard**

1. In the left navigation pane, choose **VPC Dashboard**\.

1. Choose **Start VPC Wizard**, **VPC with Public and Private Subnets**, **Select**\.

1. For **VPC name**, give your VPC a unique name\.

1. For **Elastic IP Allocation ID**, choose the ID of the Elastic IP address that you created earlier\.

1. Choose **Create VPC**\.

1. When the wizard is finished, choose **OK**\. Note the Availability Zone in which your VPC subnets were created\. Your additional subnets should be created in a different Availability Zone\.

## Step 3: Create Additional Subnets<a name="create-add-subnets"></a>

The wizard creates a VPC with a single public and a single private subnet in a single Availability Zone\. For greater availability, you should create at least one more of each subnet type in a different Availability Zone so that your VPC has both public and private subnets across two zones\.

**To create an additional private subnet**

1. In the left navigation pane, choose **Subnets**, **Create Subnet**\.

1. For **Name tag**, enter a name for your subnet, such as **Private subnet**\.

1. For **VPC**, choose the VPC that you created earlier\.

1. For **Availability Zone**, choose a different zone than your original subnets in the VPC\.

1. For **IPv4 CIDR block**, enter a valid CIDR block\. For example, the wizard creates CIDR blocks in 10\.0\.0\.0/24 and 10\.0\.1\.0/24 by default\. You could use **10\.0\.3\.0/24** for your second private subnet\.

1. Choose **Yes, Create**\.

**To create an additional public subnet**

1. In the left navigation pane, choose **Subnets**, **Create Subnet**\.

1. For **Name tag**, enter a name for your subnet, such as **Public subnet**\.

1. For **VPC**, choose the VPC that you created earlier\.

1. For **Availability Zone**, choose the same zone as the additional private subnet that you created in the previous procedure\.

1. For **IPv4 CIDR block**, enter a valid CIDR block\. For example, the wizard creates CIDR blocks in 10\.0\.0\.0/24 and 10\.0\.1\.0/24 by default\. You could use **10\.0\.2\.0/24** for your second public subnet\.

1. Choose **Yes, Create**\.

1. Select the public subnet that you just created and choose **Route Table**, **Edit**\.

1. By default, the private route table is selected\. Choose the other available route table so that the **0\.0\.0\.0/0** destination is routed to the internet gateway \(**igw\-*xxxxxxxx***\) and choose **Save**\.

1. With your second public subnet still selected, choose **Subnet Actions**, **Modify auto\-assign IP settings**\.

1. Select **Enable auto\-assign public IPv4 address** and choose **Save**, **Close**\.

## Step 4: Tag your Private Subnets<a name="vpc-tag-private-subnets"></a>

Private subnets in your VPC should be tagged accordingly so that Kubernetes knows that it can use them for internal load balancers:


| Key | Value | 
| --- | --- | 
|  `kubernetes.io/role/internal-elb`  |  `1`  | 

**To tag your private subnets**

1. Select one of your private subnets and choose **Tags**, **Add/Edit Tags**\.

1. Choose **Create Tag**\.

1. For **Key**, enter `kubernetes.io/role/internal-elb`\.

1. For **Value**, enter `1`\.

1. Choose **Save**, and repeat this procedure for any additional private subnets in your VPC\.

## Step 5: Create a Control Plane Security Group<a name="vpc-create-sg"></a>

When you create an Amazon EKS cluster, your cluster control plane creates elastic network interfaces in your subnets to enable communication with the worker nodes\. You should create a security group that is dedicated to your Amazon EKS cluster control plane, so that you can apply inbound and outbound rules to govern what traffic is allowed across that connection\. When you create the cluster, you specify this security group, and that is applied to the elastic network interfaces that are created in your subnets\.

The worker node AWS CloudFormation template used in [Step 3: Launch and Configure Amazon EKS Worker Nodes](getting-started.md#eks-launch-workers) creates a worker node security group, and it applies the necessary rules to allow communication with the control plane automatically, but you must specify the control plane security group when you create a stack from that template\.

**To create a control plane security group**

1. In the left navigation pane, for **Filter by VPC**, select your VPC and choose **Security Groups**, **Create Security Group**\.
**Note**  
If you don't see your new VPC here, refresh the page to pick it up\.

1. Fill in the following fields and choose **Yes, Create**:
   + For **Name tag**, provide a name for your security group\. For example, `<cluster-name>-control-plane`\.
   + For **Description**, provide a description of your security group to help you identify it later\.
   + For **VPC**, choose the VPC that you are using for your Amazon EKS cluster\.

## Next Steps<a name="vpc-next-steps"></a>

After you have created your VPC, you can try the [Getting Started with Amazon EKS](getting-started.md) walkthrough, but you can skip the [Create your Amazon EKS Cluster VPC](getting-started.md#vpc-create) section and use these subnets and security groups for your cluster\.