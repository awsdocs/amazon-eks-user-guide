# Launching self\-managed Windows nodes<a name="launch-windows-workers"></a>

This topic helps you to launch an Auto Scaling group of Windows nodes that register with your Amazon EKS cluster\. After the nodes join the cluster, you can deploy Kubernetes applications to them\.

**Important**  
Amazon EKS nodes are standard Amazon EC2 instances, and you are billed for them based on normal Amazon EC2 instance prices\. For more information, see [Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/)\.

**Important**  
Do not use `eksctl` to create a cluster or nodes in an AWS Region where you have AWS Outposts, AWS Wavelength, or AWS Local Zones enabled\. Create a cluster and self\-managed nodes using the Amazon EC2 API or AWS CloudFormation instead\. For more information, see [Launching self\-managed Amazon Linux nodes](launch-workers.md) and [Launching self\-managed Windows nodes](#launch-windows-workers)\.

You must enable Windows support for your cluster and we recommend that you review important considerations before you launch a Windows node group\. For more information, see [Enabling Windows support](windows-support.md#enable-windows-support)\. 

You can launch self\-managed Windows nodes with `eksctl` or the AWS Management Console\.

------
#### [ eksctl ]<a name="launch-windows-nodes-eksctl"></a>

**To launch self\-managed Windows nodes using `eksctl`**

This procedure assumes that you have installed `eksctl`, and that your `eksctl` version is at least `0.40.0`\. You can check your version with the following command:

```
eksctl version
```

 For more information on installing or upgrading `eksctl`, see [Installing or upgrading `eksctl`](eksctl.md#installing-eksctl)\.
**Note**  
This procedure only works for clusters that were created with `eksctl`\.

1. \(Optional\) If the **AmazonEKS\_CNI\_Policy** managed IAM policy is attached to your [Amazon EKS node IAM role](create-node-role.md), we recommend assigning it to an IAM role that you associate to the Kubernetes `aws-node` service account instead\. For more information, see [Configuring the VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.

1. This procedure assumes that you have an existing cluster named `my-cluster` in the `us-west-2` Region\. For a different existing cluster, change the values\. If you don't already have an Amazon EKS cluster and an Amazon Linux 2 node group to add a Windows node group to, then we recommend that you follow the [Getting started with Amazon EKS – `eksctl`](getting-started-eksctl.md) guide instead\. The guide provides a complete end\-to\-end walkthrough for creating an Amazon EKS cluster with Amazon Linux and Windows nodes\.

   Create your node group with the following command\. Replace the *<example values>* with your own values\.

   ```
   eksctl create nodegroup \
     --region <us-west-2> \
     --cluster <my-cluster> \
     --name <ng-windows> \
     --node-type <t2.large> \
     --nodes <3> \
     --nodes-min <1> \
     --nodes-max <4> \
     --node-ami-family <WindowsServer2019FullContainer>
   ```
**Note**  
If nodes fail to join the cluster, see [Nodes fail to join cluster](troubleshooting.md#worker-node-fail) in the Troubleshooting guide\.
For more information on the available options for `eksctl` commands, enter the following command\.  

     ```
     eksctl <command> -help
     ```

   Output:

   You'll see several lines of output as the nodes are created\. One of the last lines of output is the following example line\.

   ```
   [✔]  created 1 nodegroup(s) in cluster "<my-cluster>"
   ```

1. \(Optional\) Deploy a [sample application](windows-support.md#windows-sample-application) to test your cluster and Windows nodes\.

1. \(Optional\) If you plan to assign IAM roles to all of your Kubernetes service accounts so that pods only have the minimum permissions that they need, and no pods in the cluster require access to the Amazon EC2 instance metadata service \(IMDS\) for other reasons, such as retrieving the current Region, then we recommend blocking pod access to IMDS\. For more information, see [IAM roles for service accounts](iam-roles-for-service-accounts.md) and [Restricting access to the IMDS and Amazon EC2 instance profile credentials](best-practices-security.md#restrict-ec2-credential-access)\.

------
#### [ AWS Management Console ]<a name="launch-windows-nodes-console"></a>

**To launch self\-managed Windows nodes using the AWS Management Console**

These procedures have the following prerequisites:
+ You have an existing Amazon EKS cluster and a Linux node group\. If you don't have these resources, we recommend that you follow one of our [Getting started with Amazon EKS](getting-started.md) guides to create them\. The guides provide a complete end\-to\-end walkthrough for creating an Amazon EKS cluster with Linux nodes\.
+ You have created a VPC and security group that meet the requirements for an Amazon EKS cluster\. For more information, see [Cluster VPC considerations](network_reqs.md) and [Amazon EKS security group considerations](sec-group-reqs.md)\. The [Getting started with Amazon EKS](getting-started.md) guide creates a VPC that meets the requirements, or you can also follow [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md) to create one manually\.

1. Wait for your cluster status to show as `ACTIVE`\. If you launch your nodes before the cluster is active, the nodes will fail to register with the cluster and you will have to relaunch them\.

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)

1. Choose **Create stack**\.

1. For **Specify template**, select **Amazon S3 URL**, copy the following URL, paste it into **Amazon S3 URL**, and select **Next** twice\.

   ```
   https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-windows-nodegroup.yaml
   ```

1. On the **Quick create stack** page, fill out the following parameters accordingly:
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it **<cluster\-name>\-nodes**\.
   + **ClusterName**: Enter the name that you used when you created your Amazon EKS cluster\.
**Important**  
This name must exactly match the name you used in [Step 1: Create your Amazon EKS cluster](getting-started-console.md#eks-create-cluster); otherwise, your nodes cannot join the cluster\.
   + **ClusterControlPlaneSecurityGroup**: Choose the **SecurityGroups** value from the AWS CloudFormation output that you generated when you created your [VPC](create-public-private-vpc.md)\.
   + **NodeGroupName**: Enter a name for your node group\. This name can be used later to identify the Auto Scaling node group that is created for your nodes\.
   + **NodeAutoScalingGroupMinSize**: Enter the minimum number of nodes that your node Auto Scaling group can scale in to\.
   + **NodeAutoScalingGroupDesiredCapacity**: Enter the desired number of nodes to scale to when your stack is created\.
   + **NodeAutoScalingGroupMaxSize**: Enter the maximum number of nodes that your node Auto Scaling group can scale out to\.
   + **NodeInstanceType**: Choose an instance type for your nodes\.
**Note**  
The supported instance types for the latest version of the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) are shown [here](https://github.com/aws/amazon-vpc-cni-k8s/blob/release-1.7/pkg/awsutils/vpc_ip_resource_limit.go)\. You may need to update your CNI version to take advantage of the latest supported instance types\. For more information, see [Amazon VPC CNI plugin for Kubernetes upgrades](cni-upgrades.md)\.
   + **NodeImageIdSSMParam**: Pre\-populated with the Amazon EC2 Systems Manager parameter of the current recommended Amazon EKS optimized Windows Core AMI ID\. If you want to use the full version of Windows, then replace <Core> with `Full`\.
   + **NodeImageId**: \(Optional\) If you are using your own custom AMI \(instead of the Amazon EKS optimized AMI\), enter a node AMI ID for your Region\. If you specify a value here, it overrides any values in the **NodeImageIdSSMParam** field\.
   + **NodeVolumeSize**: Specify a root volume size for your nodes, in GiB\.
   + **KeyName**: Enter the name of an Amazon EC2 SSH key pair that you can use to connect using SSH into your nodes with after they launch\. If you don't already have an Amazon EC2 key pair, you can create one in the AWS Management Console\. For more information, see [Amazon EC2 key pairs](https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/ec2-key-pairs.html) in the *Amazon EC2 User Guide for Windows Instances*\.
**Note**  
If you do not provide a key pair here, the AWS CloudFormation stack creation fails\.
   + **BootstrapArguments**: Specify any optional arguments to pass to the node bootstrap script, such as extra `kubelet` arguments using `-KubeletExtraArgs`\. 
   + **DisableIMDSv1**: Each node supports the Instance Metadata Service Version 1 \(IMDSv1\) and IMDSv2 by default, but you can disable IMDSv1\. Select **true** if you don't want any nodes in the node group, or any pods scheduled on the nodes in the node group to use IMDSv1\. For more information about IMDS, see [Configuring the instance metadata service](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html)\.
   + **VpcId**: Select the ID for the [VPC](create-public-private-vpc.md) that you created\.
   + **NodeSecurityGroups**: Select the security group that was created for your Linux node group when you created your [VPC](create-public-private-vpc.md)\. If your Linux nodes have more than one security group attached to them \(for example, if the Linux node group was created with `eksctl`\), specify all of them here\.
   + **Subnets**: Choose the subnets that you created\. If you created your VPC using the steps described at [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md), then specify only the private subnets within the VPC for your nodes to launch into\.
**Important**  
If any of the subnets are public subnets, then they must have the automatic public IP address assignment setting enabled\. If the setting is not enabled for the public subnet, then any nodes that you deploy to that public subnet will not be assigned a public IP address and will not be able to communicate with the cluster or other AWS services\. If the subnet was deployed before March 26, 2020 using either of the [Amazon EKS AWS CloudFormation VPC templates](create-public-private-vpc.md), or by using `eksctl`, then automatic public IP address assignment is disabled for public subnets\. For information about how to enable public IP address assignment for a subnet, see [ Modifying the Public IPv4 Addressing Attribute for Your Subnet](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#subnet-public-ip)\. If the node is deployed to a private subnet, then it is able to communicate with the cluster and other AWS services through a NAT gateway\.
**Important**  
Ensure that the subnets you select are tagged with the cluster name\. For more information, see [Subnet tagging](network_reqs.md#vpc-subnet-tagging)\. If you have subnets in AWS Outposts, AWS Wavelength, or an AWS Local Zone, they likely are not currently tagged\.

1. Acknowledge that the stack might create IAM resources, and then choose **Create stack**\.

1. When your stack has finished creating, select it in the console and choose **Outputs**\.

1. Record the **NodeInstanceRole** for the node group that was created\. You need this when you configure your Amazon EKS Windows nodes\.

**To enable nodes to join your cluster**

1. Download, edit, and apply the AWS IAM Authenticator configuration map\.

   1. Download the configuration map:

      ```
      curl -o aws-auth-cm-windows.yaml https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/aws-auth-cm-windows.yaml
      ```

   1. Open the file with your favorite text editor\. Replace the *`<ARN of instance role (not instance profile) of **Linux** node>`* and *`<ARN of instance role (not instance profile) of **Windows** node>`* snippets with the **NodeInstanceRole** values that you recorded for your Linux and Windows nodes, and save the file\.
**Important**  
Do not modify any other lines in this file\.

      ```
      apiVersion: v1
      kind: ConfigMap
      metadata:
        name: aws-auth
        namespace: kube-system
      data:
        mapRoles: |
          - rolearn: <ARN of instance role (not instance profile) of **Linux** node>
            username: system:node:{{EC2PrivateDNSName}}
            groups:
              - system:bootstrappers
              - system:nodes
          - rolearn: <ARN of instance role (not instance profile) of **Windows** node>
            username: system:node:{{EC2PrivateDNSName}}
            groups:
              - system:bootstrappers
              - system:nodes
              - eks:kube-proxy-windows
      ```

   1. Apply the configuration\. This command may take a few minutes to finish\.

      ```
      kubectl apply -f aws-auth-cm-windows.yaml
      ```
**Note**  
If you receive any authorization or resource type errors, see [Unauthorized or access denied \(`kubectl`\)](troubleshooting.md#unauthorized) in the troubleshooting section\.

      If nodes fail to join the cluster, then see [Nodes fail to join cluster](troubleshooting.md#worker-node-fail) in the Troubleshooting guide\.

1. Watch the status of your nodes and wait for them to reach the `Ready` status\.

   ```
   kubectl get nodes --watch
   ```

1. \(Optional\) Deploy a [sample application](windows-support.md#windows-sample-application) to test your cluster and Windows nodes\.

1. \(Optional\) If the **AmazonEKS\_CNI\_Policy** managed IAM policy is attached to your [Amazon EKS node IAM role](create-node-role.md), we recommend assigning it to an IAM role that you associate to the Kubernetes `aws-node` service account instead\. For more information, see [Configuring the VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.

1. \(Optional\) If you plan to assign IAM roles to all of your Kubernetes service accounts so that pods only have the minimum permissions that they need, and no pods in the cluster require access to the Amazon EC2 instance metadata service \(IMDS\) for other reasons, such as retrieving the current Region, then we recommend blocking pod access to IMDS\. For more information, see [IAM roles for service accounts](iam-roles-for-service-accounts.md) and [Restricting access to the IMDS and Amazon EC2 instance profile credentials](best-practices-security.md#restrict-ec2-credential-access)\.

------