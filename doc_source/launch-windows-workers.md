# Launching Amazon EKS Windows Worker Nodes<a name="launch-windows-workers"></a>

This topic helps you to launch an Auto Scaling group of Windows worker nodes that register with your Amazon EKS cluster\. After the nodes join the cluster, you can deploy Kubernetes applications to them\.

**Important**  
Amazon EKS worker nodes are standard Amazon EC2 instances, and you are billed for them based on normal Amazon EC2 prices\. For more information, see [Amazon EC2 Pricing](https://aws.amazon.com/ec2/pricing/)\.

You must enable Windows support for your cluster and we recommend that you review important considerations before you launch a Windows worker node group\. For more information, see [Enabling Windows Support](windows-support.md#enable-windows-support)\. 

Choose the tab below that corresponds to your desired worker node creation method:

------
#### [ eksctl ]

If you don't already have an Amazon EKS cluster and a Linux worker node group to add a Windows worker node group to, then we recommend that you follow the [Getting Started with `eksctl`](getting-started-eksctl.md) guide instead\. The guide provides a complete end\-to\-end walkthrough for creating an Amazon EKS cluster with Linux and Windows worker nodes\. If you have an existing Amazon EKS cluster and a Linux worker node group to add a Windows worker node group to, then complete the following steps to add the Windows worker node group\.

**To launch Windows worker nodes with `eksctl`**

This procedure assumes that you have installed `eksctl`, and that your `eksctl` version is at least `0.11.0`\. You can check your version with the following command:

```
eksctl version
```

 For more information on installing or upgrading `eksctl`, see [Installing or Upgrading `eksctl`](eksctl.md#installing-eksctl)\.
**Note**  
This procedure only works for clusters that were created with `eksctl`\.

1. Create your worker node group with the following command\. Replace the *example values* with your own values\.

   ```
   eksctl create nodegroup \
   --region us-west-2 \
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

   ```
   [ℹ]  using region us-west-2
   [ℹ]  1 nodegroup(s) that already exist (ng-9d1cc1f2) will be excluded
   [ℹ]  nodegroup "windows-ng" will use "ami-0c7f1b5f1bebccac2" [WindowsServer2019FullContainer/1.14]
   [ℹ]  1 nodegroup (windows-ng) was included (based on the include/exclude rules)
   [ℹ]  combined exclude rules: ng-9d1cc1f2
   [ℹ]  no nodegroups present in the current set were excluded by the filter
   [ℹ]  will create a CloudFormation stack for each of 1 nodegroups in cluster "windows"
   [ℹ]  1 task: { create nodegroup "windows-ng" }
   [ℹ]  building nodegroup stack "eksctl-windows-nodegroup-windows-ng"
   [ℹ]  deploying stack "eksctl-windows-nodegroup-windows-ng"
   [ℹ]  adding role "arn:aws:iam::123456789012:role/eksctl-windows-nodegroup-windows-NodeInstanceRole-1E4JMZRAT9AEZ" to auth ConfigMap
   [ℹ]  nodegroup "windows-ng" has 0 node(s)
   [ℹ]  waiting for at least 1 node(s) to become ready in "windows-ng"
   [ℹ]  nodegroup "windows-ng" has 1 node(s)
   [ℹ]  node "ip-192-168-88-105.us-west-2.compute.internal" is ready
   [✔]  created 1 nodegroup(s) in cluster "windows"
   [ℹ]  checking security group configuration for all nodegroups
   [ℹ]  all nodegroups have up-to-date configuration
   ```

1. \(Optional\) [Deploy a Windows Sample Application](windows-support.md#windows-sample-application) — Deploy a sample application to test your cluster and Windows worker nodes\.

------
#### [ AWS Management Console ]

**To launch your worker nodes with the AWS Management Console**

These procedures have the following prerequisites:
+ You have an existing Amazon EKS cluster and a Linux worker node group\. If you don't have these resources, we recommend that you follow one of our [Getting Started with Amazon EKS](getting-started.md) guides to create them\. The guides provide a complete end\-to\-end walkthrough for creating an Amazon EKS cluster with Linux worker nodes\.
+ You have created a VPC and security group that meet the requirements for an Amazon EKS cluster\. For more information, see [Cluster VPC Considerations](network_reqs.md) and [Amazon EKS Security Group Considerations](sec-group-reqs.md)\. The [Getting Started with Amazon EKS](getting-started.md) guide creates a VPC that meets the requirements, or you can also follow [Creating a VPC for Your Amazon EKS Cluster](create-public-private-vpc.md) to create one manually\.

1. Wait for your cluster status to show as `ACTIVE`\. If you launch your worker nodes before the cluster is active, the worker nodes will fail to register with the cluster and you will have to relaunch them\.

1. Choose a **Launch workers** link that corresponds to your region and AMI type\. This opens the AWS CloudFormation console and pre\-populates several fields for you\.

------
#### [ Kubernetes version 1\.14\.6 ]    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/launch-windows-workers.html)

------
**Note**  
If you intend to only deploy worker nodes to private subnets, you should edit this template in the AWS CloudFormation designer and modify the `AssociatePublicIpAddress` parameter in the `NodeLaunchConfig` to be `false`\.  

   ```
   AssociatePublicIpAddress: 'false'
   ```

1. On the **Quick create stack** page, fill out the following parameters accordingly:
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it ***<cluster\-name>*\-worker\-nodes**\.
   + **ClusterName**: Enter the name that you used when you created your Amazon EKS cluster\.
**Important**  
This name must exactly match the name you used in [Step 1: Create Your Amazon EKS Cluster](getting-started-console.md#eks-create-cluster); otherwise, your worker nodes cannot join the cluster\.
   + **ClusterControlPlaneSecurityGroup**: Choose the **SecurityGroups** value from the AWS CloudFormation output that you generated with [Create your Amazon EKS Cluster VPC](getting-started-console.md#vpc-create)\.
   + **NodeGroupName**: Enter a name for your node group\. This name can be used later to identify the Auto Scaling node group that is created for your worker nodes\.
   + **NodeAutoScalingGroupMinSize**: Enter the minimum number of nodes that your worker node Auto Scaling group can scale in to\.
   + **NodeAutoScalingGroupDesiredCapacity**: Enter the desired number of nodes to scale to when your stack is created\.
   + **NodeAutoScalingGroupMaxSize**: Enter the maximum number of nodes that your worker node Auto Scaling group can scale out to\.
   + **NodeInstanceType**: Choose an instance type for your worker nodes\.
**Note**  
The supported instance types for the latest version of the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) are shown [here](https://github.com/aws/amazon-vpc-cni-k8s/blob/release-1.5/pkg/awsutils/vpc_ip_resource_limit.go)\. You may need to update your CNI version to take advantage of the latest supported instance types\. For more information, see [Amazon VPC CNI Plugin for Kubernetes Upgrades](cni-upgrades.md)\.
**Important**  
Some instance types might not be available in all regions\.
   + **NodeImageIdSSMParam**: Pre\-populated based on the version that you launched your worker nodes with in step 2\. This value is the Amazon EC2 Systems Manager Parameter Store parameter to use for your worker node AMI ID\. For example, the `aws/service/ami-windows-latest/Windows_Server-2019-English-Core-EKS-1.14_Optimized/image_id` parameter is for the latest recommended Kubernetes version 1\.14 Amazon EKS\-optimized Windows AMI\. If you want to use the full version of Windows, then replace *Core* with `Full`\.
   + **NodeImageId**: \(Optional\) If you are using your own custom AMI \(instead of the Amazon EKS\-optimized AMI\), enter a worker node AMI ID for your Region\. If you specify a value here, it overrides any values in the **NodeImageIdSSMParam** field\.
   + **NodeVolumeSize**: Specify a root volume size for your worker nodes, in GiB\.
   + **KeyName**: Enter the name of an Amazon EC2 SSH key pair that you can use to connect using SSH into your worker nodes with after they launch\. If you don't already have an Amazon EC2 keypair, you can create one in the AWS Management Console\. For more information, see [Amazon EC2 Key Pairs](https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/ec2-key-pairs.html) in the *Amazon EC2 User Guide for Windows Instances*\.
**Note**  
If you do not provide a keypair here, the AWS CloudFormation stack creation fails\.
   + **BootstrapArguments**: Specify any optional arguments to pass to the worker node bootstrap script, such as extra `kubelet` arguments using `-KubeletExtraArgs`\. 
   + **VpcId**: Select the ID for the VPC that you created in [Create your Amazon EKS Cluster VPC](getting-started-console.md#vpc-create)\.
   + **NodeSecurityGroups**: Select the security group that was created for your Linux worker node group in [Create your Amazon EKS Cluster VPC](getting-started-console.md#vpc-create)\. If your Linux worker nodes have more than one security group attached to them \(for example, if the Linux worker node group was created with `eksctl`\), specify all of them here\.
   + **Subnets**: Choose the subnets that you created in [Create your Amazon EKS Cluster VPC](getting-started-console.md#vpc-create)\. If you created your VPC using the steps described at [Creating a VPC for Your Amazon EKS Cluster](create-public-private-vpc.md), then specify only the private subnets within the VPC for your worker nodes to launch into\.

1. Acknowledge that the stack might create IAM resources, and then choose **Create stack**\.

1. When your stack has finished creating, select it in the console and choose **Outputs**\.

1. Record the **NodeInstanceRole** for the node group that was created\. You need this when you configure your Amazon EKS Windows worker nodes\.

**To enable worker nodes to join your cluster**

1. Download, edit, and apply the AWS IAM Authenticator configuration map\.

   1. Use the following command to download the configuration map:

      ```
      curl -o aws-auth-cm-windows.yaml https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-11-15/aws-auth-cm-windows.yaml
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
If you receive the error `"aws-iam-authenticator": executable file not found in $PATH`, your kubectl isn't configured for Amazon EKS\. For more information, see [Installing `aws-iam-authenticator`](install-aws-iam-authenticator.md)\.  
If you receive any other authorization or resource type errors, see [Unauthorized or Access Denied \(`kubectl`\)](troubleshooting.md#unauthorized) in the troubleshooting section\.

1. Watch the status of your nodes and wait for them to reach the `Ready` status\.

   ```
   kubectl get nodes --watch
   ```

1. \(Optional\) [Deploy a Windows Sample Application](windows-support.md#windows-sample-application) — Deploy a sample application to test your cluster and Windows worker nodes\.

------