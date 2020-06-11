# Launching Amazon EKS Windows worker nodes<a name="launch-windows-workers"></a>

This topic helps you to launch an Auto Scaling group of Windows worker nodes that register with your Amazon EKS cluster\. After the nodes join the cluster, you can deploy Kubernetes applications to them\.

**Important**  
Amazon EKS worker nodes are standard Amazon EC2 instances, and you are billed for them based on normal Amazon EC2 prices\. For more information, see [Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/)\.

You must enable Windows support for your cluster and we recommend that you review important considerations before you launch a Windows worker node group\. For more information, see [Enabling Windows support](windows-support.md#enable-windows-support)\. 

Choose the tab below that corresponds to your desired worker node creation method:

------
#### [ eksctl ]

If you don't already have an Amazon EKS cluster and a Linux worker node group to add a Windows worker node group to, then we recommend that you follow the [Getting started with `eksctl`](getting-started-eksctl.md) guide instead\. The guide provides a complete end\-to\-end walkthrough for creating an Amazon EKS cluster with Linux and Windows worker nodes\. If you have an existing Amazon EKS cluster and a Linux worker node group to add a Windows worker node group to, then complete the following steps to add the Windows worker node group\.

**To launch Windows worker nodes with `eksctl`**

This procedure assumes that you have installed `eksctl`, and that your `eksctl` version is at least `0.21.0`\. You can check your version with the following command:

```
eksctl version
```

 For more information on installing or upgrading `eksctl`, see [Installing or upgrading `eksctl`](eksctl.md#installing-eksctl)\.
**Note**  
This procedure only works for clusters that were created with `eksctl`\.

1. Create your worker node group with the following command\. Replace the *example values* with your own values\.

   ```
   eksctl create nodegroup \
   --region region-code \
   --cluster windows \
   --name windows-ng \
   --node-type t2.large \
   --nodes 3 \
   --nodes-min 1 \
   --nodes-max 4 \
   --node-ami-family WindowsServer2019FullContainer
   ```
**Note**  
For more information on the available options for eksctl create nodegroup, see the project [README on GitHub](https://github.com/weaveworks/eksctl/blob/master/README.md) or view the help page with the following command\.  

   ```
   eksctl create nodegroup --help
   ```

   Output:

   You'll see several lines of output as the worker nodes are created\. The last line of output is similar to the following example line\.

   ```
   [ℹ]  all nodegroups have up-to-date configuration
   ```

1. \(Optional\) [Deploy a Windows sample application](windows-support.md#windows-sample-application) — Deploy a sample application to test your cluster and Windows worker nodes\.

------
#### [ AWS Management Console ]

**To launch your worker nodes with the AWS Management Console**

These procedures have the following prerequisites:
+ You have an existing Amazon EKS cluster and a Linux worker node group\. If you don't have these resources, we recommend that you follow one of our [Getting started with Amazon EKS](getting-started.md) guides to create them\. The guides provide a complete end\-to\-end walkthrough for creating an Amazon EKS cluster with Linux worker nodes\.
+ You have created a VPC and security group that meet the requirements for an Amazon EKS cluster\. For more information, see [Cluster VPC considerations](network_reqs.md) and [Amazon EKS security group considerations](sec-group-reqs.md)\. The [Getting started with Amazon EKS](getting-started.md) guide creates a VPC that meets the requirements, or you can also follow [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md) to create one manually\.

1. Wait for your cluster status to show as `ACTIVE`\. If you launch your worker nodes before the cluster is active, the worker nodes will fail to register with the cluster and you will have to relaunch them\.

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)

1. Choose **Create stack**\.

1. For **Specify template**, select **Amazon S3 URL**, then copy the following URL, paste it into **Amazon S3 URL**, and select **Next** twice\.

   ```
   https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-06-10/amazon-eks-windows-nodegroup.yaml
   ```

1. On the **Quick create stack** page, fill out the following parameters accordingly:
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it ***cluster\-name*\-worker\-nodes**\.
   + **ClusterName**: Enter the name that you used when you created your Amazon EKS cluster\.
**Important**  
This name must exactly match the name you used in [Step 1: Create your Amazon EKS cluster](getting-started-console.md#eks-create-cluster); otherwise, your worker nodes cannot join the cluster\.
   + **ClusterControlPlaneSecurityGroup**: Choose the **SecurityGroups** value from the AWS CloudFormation output that you generated with [Create your Amazon EKS cluster VPC](getting-started-console.md#vpc-create)\.
   + **NodeGroupName**: Enter a name for your node group\. This name can be used later to identify the Auto Scaling node group that is created for your worker nodes\.
   + **NodeAutoScalingGroupMinSize**: Enter the minimum number of nodes that your worker node Auto Scaling group can scale in to\.
   + **NodeAutoScalingGroupDesiredCapacity**: Enter the desired number of nodes to scale to when your stack is created\.
   + **NodeAutoScalingGroupMaxSize**: Enter the maximum number of nodes that your worker node Auto Scaling group can scale out to\.
   + **NodeInstanceType**: Choose an instance type for your worker nodes\.
**Note**  
The supported instance types for the latest version of the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) are shown [here](https://github.com/aws/amazon-vpc-cni-k8s/blob/release-1.6/pkg/awsutils/vpc_ip_resource_limit.go)\. You may need to update your CNI version to take advantage of the latest supported instance types\. For more information, see [Amazon VPC CNI plugin for Kubernetes upgrades](cni-upgrades.md)\.
**Important**  
Some instance types might not be available in all Regions\.
   + **NodeImageIdSSMParam**: Pre\-populated with the Amazon EC2 Systems Manager parameter of the current recommended Amazon EKS\-Optimized Windows Core AMI ID\. If you want to use the full version of Windows, then replace *Core* with `Full`\.
   + **NodeImageId**: \(Optional\) If you are using your own custom AMI \(instead of the Amazon EKS\-optimized AMI\), enter a worker node AMI ID for your Region\. If you specify a value here, it overrides any values in the **NodeImageIdSSMParam** field\.
   + **NodeVolumeSize**: Specify a root volume size for your worker nodes, in GiB\.
   + **KeyName**: Enter the name of an Amazon EC2 SSH key pair that you can use to connect using SSH into your worker nodes with after they launch\. If you don't already have an Amazon EC2 keypair, you can create one in the AWS Management Console\. For more information, see [Amazon EC2 key pairs](https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/ec2-key-pairs.html) in the *Amazon EC2 User Guide for Windows Instances*\.
**Note**  
If you do not provide a keypair here, the AWS CloudFormation stack creation fails\.
   + **BootstrapArguments**: Specify any optional arguments to pass to the worker node bootstrap script, such as extra `kubelet` arguments using `-KubeletExtraArgs`\. 
   + **VpcId**: Select the ID for the VPC that you created in [Create your Amazon EKS cluster VPC](getting-started-console.md#vpc-create)\.
   + **NodeSecurityGroups**: Select the security group that was created for your Linux worker node group in [Create your Amazon EKS cluster VPC](getting-started-console.md#vpc-create)\. If your Linux worker nodes have more than one security group attached to them \(for example, if the Linux worker node group was created with `eksctl`\), specify all of them here\.
   + **Subnets**: Choose the subnets that you created in [Create your Amazon EKS cluster VPC](getting-started-console.md#vpc-create)\. If you created your VPC using the steps described at [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md), then specify only the private subnets within the VPC for your worker nodes to launch into\.
**Important**  
If any of the subnets are public subnets, then they must have the automatic public IP address assignment setting enabled\. If the setting is not enabled for the public subnet, then any worker nodes that you deploy to that public subnet will not be assigned a public IP address and will not be able to communicate with the cluster or other AWS services\. If the subnet was deployed before 03/26/2020 using either of the [Amazon EKS AWS CloudFormation VPC templates](create-public-private-vpc.md), or by using `eksctl`, then automatic public IP address assignment is disabled for public subnets\. For information about how to enable public IP address assignment for a subnet, see [ Modifying the Public IPv4 Addressing Attribute for Your Subnet](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#subnet-public-ip)\. If the worker node is deployed to a private subnet, then it is able to communicate with the cluster and other AWS services through a NAT gateway\.

1. Acknowledge that the stack might create IAM resources, and then choose **Create stack**\.

1. When your stack has finished creating, select it in the console and choose **Outputs**\.

1. Record the **NodeInstanceRole** for the node group that was created\. You need this when you configure your Amazon EKS Windows worker nodes\.

**To enable worker nodes to join your cluster**

1. Download, edit, and apply the AWS IAM Authenticator configuration map\.

   1. Use the following command to download the configuration map:

      ```
      curl -o aws-auth-cm-windows.yaml https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-06-10/aws-auth-cm-windows.yaml
      ```

   1. Open the file with your favorite text editor\. Replace the *<ARN of instance role \(not instance profile\) of \*\*Linux\*\* worker node>* and *<ARN of instance role \(not instance profile\) of \*\*Windows\*\* worker node>* snippets with the **NodeInstanceRole** values that you recorded for your Linux and Windows worker nodes, and save the file\.
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
          - rolearn: <ARN of instance role (not instance profile) of **Linux** worker node>
            username: system:node:{{EC2PrivateDNSName}}
            groups:
              - system:bootstrappers
              - system:nodes
          - rolearn: <ARN of instance role (not instance profile) of **Windows** worker node>
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

1. Watch the status of your nodes and wait for them to reach the `Ready` status\.

   ```
   kubectl get nodes --watch
   ```

1. \(Optional\) [Deploy a Windows sample application](windows-support.md#windows-sample-application) — Deploy a sample application to test your cluster and Windows worker nodes\.

------