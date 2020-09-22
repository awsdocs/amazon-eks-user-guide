# Launching self\-managed Amazon Linux nodes<a name="launch-workers"></a>

This topic helps you to launch an Auto Scaling group of Linux nodes that register with your Amazon EKS cluster\. After the nodes join the cluster, you can deploy Kubernetes applications to them\. You can launch self\-managed Amazon Linux 2 nodes with [`eksctl`](#launch-al-nodes-eksctl) or the [AWS Management Console](#launch-al-nodes-console)\.<a name="launch-al-nodes-eksctl"></a>

**To launch self\-managed Linux nodes using `eksctl`**

This procedure only works for clusters that were created with `eksctl`\.
**Note**  
This procedure requires `eksctl` version `0.28.0` or later\. You can check your version with the following command:  

```
eksctl version
```
For more information on installing or upgrading `eksctl`, see [Installing or upgrading `eksctl`](eksctl.md#installing-eksctl)\.

1. The following command assumes that you have an existing cluster named `my-cluster` in the `us-west-2` Region\. For a different existing cluster, change the values\. If you don't have an existing cluster then you must first [create a cluster](create-cluster.md)\. If you want to deploy on Amazon EC2 Arm instances, then replace `t3.medium` with an Arm instance type\. If specifying an Arm Amazon EC2 instance type, then review the considerations in [Amazon EKS optimized Arm Amazon Linux AMIs](eks-optimized-ami.md#arm-ami) before deploying\.

   Create your node group with the following command\. Replace the *example values* with your own values\.

   ```
   eksctl create nodegroup \
   --cluster my-cluster \
   --version auto \
   --name al-nodes \
   --node-type t3.medium \
   --node-ami auto \
   --nodes 3 \
   --nodes-min 1 \
   --nodes-max 4
   ```

   If nodes fail to join the cluster, then see [Nodes fail to join cluster](troubleshooting.md#worker-node-fail) in the Troubleshooting guide\.

   Output:

   You'll see several lines of output as the nodes are created\. One of the last lines of output is the following example line\.

   ```
   [✔]  created 1 nodegroup(s) in cluster "my-cluster"
   ```

1. \(Optional\) Deploy a [sample application](sample-deployment.md) to test your cluster and Linux nodes\.<a name="launch-al-nodes-console"></a>

**To launch self\-managed nodes using the AWS Management Console**

This procedure has the following prerequisites:
+ An existing VPC and security group that meet the requirements for an Amazon EKS cluster\. For more information, see [Cluster VPC considerations](network_reqs.md) and [Amazon EKS security group considerations](sec-group-reqs.md)\. The [Getting started with Amazon EKS](getting-started.md) guide creates a VPC that meets the requirements, or you can also follow [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md) to create one manually\.
+ An existing Amazon EKS cluster that uses a VPC and security group that meet the requirements of an Amazon EKS cluster\. For more information, see [Creating an Amazon EKS cluster](create-cluster.md)\.

1. Wait for your cluster status to show as `ACTIVE`\. If you launch your nodes before the cluster is active, the nodes will fail to register with the cluster and you will have to relaunch them\.

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)

1. Choose **Create stack**\.

1. For **Specify template**, select **Amazon S3 URL**, then copy the following URL, paste it into **Amazon S3 URL**, and select **Next** twice\.

   ```
   https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-08-12/amazon-eks-nodegroup.yaml
   ```

1. On the **Quick create stack** page, fill out the following parameters accordingly:
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it ***<cluster\-name>*\-nodes**\.
   + **ClusterName**: Enter the name that you used when you created your Amazon EKS cluster\.
**Important**  
This name must exactly match the name you used in [Step 1: Create your Amazon EKS cluster](getting-started-console.md#eks-create-cluster); otherwise, your nodes cannot join the cluster\.
   + **ClusterControlPlaneSecurityGroup**: Choose the **SecurityGroups** value from the AWS CloudFormation output that you generated with [Create your Amazon EKS cluster VPC](getting-started-console.md#vpc-create)\.
   + **NodeGroupName**: Enter a name for your node group\. This name can be used later to identify the Auto Scaling node group that is created for your nodes\.
   + **NodeAutoScalingGroupMinSize**: Enter the minimum number of nodes that your node Auto Scaling group can scale in to\.
   + **NodeAutoScalingGroupDesiredCapacity**: Enter the desired number of nodes to scale to when your stack is created\.
   + **NodeAutoScalingGroupMaxSize**: Enter the maximum number of nodes that your node Auto Scaling group can scale out to\.
   + **NodeInstanceType**: Choose an instance type for your nodes\. Before choosing an Arm instance type, make sure to review the considerations in [Amazon EKS optimized Arm Amazon Linux AMIs](eks-optimized-ami.md#arm-ami)\.
**Note**  
The supported instance types for the latest version of the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) are shown [here](https://github.com/aws/amazon-vpc-cni-k8s/blob/release-1.6/pkg/awsutils/vpc_ip_resource_limit.go)\. You may need to update your CNI version to take advantage of the latest supported instance types\. For more information, see [Amazon VPC CNI plugin for Kubernetes upgrades](cni-upgrades.md)\.
**Important**  
Some instance types might not be available in all Regions\.
   + **NodeImageIdSSMParam**: Pre\-populated with the Amazon EC2 Systems Manager parameter of the current recommended Amazon EKS optimized Amazon Linux AMI ID for a Kubernetes version\. If you want to use the Amazon EKS optimized accelerated AMI, then replace *amazon\-linux\-2* with `amazon-linux-2-gpu`\. If you want to use the Amazon EKS optimized Arm AMI, then replace *amazon\-linux\-2* with `amazon-linux-2-arm64`\. If you want to use a different Kubernetes minor version supported with Amazon EKS, then you can replace **1\.x** with a different [supported version](kubernetes-versions.md)\. We recommend specifying the same Kubernetes version as your cluster\.
**Note**  
The Amazon EKS node AMI is based on Amazon Linux 2\. You can track security or privacy events for Amazon Linux 2 at the [Amazon Linux Security Center](https://alas.aws.amazon.com/alas2.html) or subscribe to the associated [RSS feed](https://alas.aws.amazon.com/AL2/alas.rss)\. Security and privacy events include an overview of the issue, what packages are affected, and how to update your instances to correct the issue\.
   + **NodeImageId**: \(Optional\) If you are using your own custom AMI \(instead of the Amazon EKS optimized AMI\), enter a node AMI ID for your Region\. If you specify a value here, it overrides any values in the **NodeImageIdSSMParam** field\. 
   + **NodeVolumeSize**: Specify a root volume size for your nodes, in GiB\.
   + **KeyName**: Enter the name of an Amazon EC2 SSH key pair that you can use to connect using SSH into your nodes with after they launch\. If you don't already have an Amazon EC2 keypair, you can create one in the AWS Management Console\. For more information, see [Amazon EC2 key pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) in the *Amazon EC2 User Guide for Linux Instances*\.
**Note**  
If you do not provide a keypair here, the AWS CloudFormation stack creation fails\.
   + **BootstrapArguments**: Specify any optional arguments to pass to the node bootstrap script, such as extra  `kubelet`  arguments\. For more information, view the [bootstrap script usage information](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) on GitHub\. 
**Note**  
If you are launching nodes into a private VPC without outbound internet access, then you need to include the following arguments\.  

       ```
       --apiserver-endpoint cluster-endpoint --b64-cluster-ca cluster-certificate-authority
       ```
If you want to assign IP addresses to pods that are from a different CIDR block than the block that includes the IP address for the node, then you may need to add a CIDR block to your VPC and specify an argument to support the capability\. For more information, see [CNI custom networking](cni-custom-network.md)\.
   + **DisableIMDSv1**: Each node supports the Instance Metadata Service Version 1 \(IMDSv1\) and IMDSv2 by default, but you can disable IMDSv1\. Select **true** if you don't want any nodes in the node group, or any pods scheduled on the nodes in the node group to use IMDSv1\. For more information about IMDS, see [Configuring the instance metadata service](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html)\.
   + **VpcId**: Enter the ID for the VPC that you created in [Create your Amazon EKS cluster VPC](getting-started-console.md#vpc-create)\.
   + **Subnets**: Choose the subnets that you created in [Create your Amazon EKS cluster VPC](getting-started-console.md#vpc-create)\. If you created your VPC using the steps described at [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md), then specify only the private subnets within the VPC for your nodes to launch into\.
**Important**  
If any of the subnets are public subnets, then they must have the automatic public IP address assignment setting enabled\. If the setting is not enabled for the public subnet, then any nodes that you deploy to that public subnet will not be assigned a public IP address and will not be able to communicate with the cluster or other AWS services\. If the subnet was deployed before March 26, 2020 using either of the [Amazon EKS AWS CloudFormation VPC templates](create-public-private-vpc.md), or by using `eksctl`, then automatic public IP address assignment is disabled for public subnets\. For information about how to enable public IP address assignment for a subnet, see [ Modifying the Public IPv4 Addressing Attribute for Your Subnet](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#subnet-public-ip)\. If the node is deployed to a private subnet, then it is able to communicate with the cluster and other AWS services through a NAT gateway\.
**Important**  
If the subnets do not have internet access, then make sure that you're aware of the considerations and extra steps in [Private clusters](private-clusters.md)\.

1. Acknowledge that the stack might create IAM resources, and then choose **Create stack**\.

1. When your stack has finished creating, select it in the console and choose **Outputs**\.

1. Record the **NodeInstanceRole** for the node group that was created\. You need this when you configure your Amazon EKS nodes\.

**To enable nodes to join your cluster**
**Note**  
If you launched nodes inside a private VPC without outbound internet access, then you must enable nodes to join your cluster from within the VPC\.

1. Download, edit, and apply the AWS IAM Authenticator configuration map\.

   1. Use the following command to download the configuration map:

      ```
      curl -o aws-auth-cm.yaml https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-08-12/aws-auth-cm.yaml
      ```

   1. Open the file with your text editor\. Replace the *<ARN of instance role \(not instance profile\)>* snippet with the **NodeInstanceRole** value that you recorded in the previous procedure, and save the file\.
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
          - rolearn: <ARN of instance role (not instance profile)>
            username: system:node:{{EC2PrivateDNSName}}
            groups:
              - system:bootstrappers
              - system:nodes
      ```

   1. Apply the configuration\. This command may take a few minutes to finish\.

      ```
      kubectl apply -f aws-auth-cm.yaml
      ```
**Note**  
If you receive any authorization or resource type errors, see [Unauthorized or access denied \(`kubectl`\)](troubleshooting.md#unauthorized) in the troubleshooting section\.

      If nodes fail to join the cluster, then see [Nodes fail to join cluster](troubleshooting.md#worker-node-fail) in the Troubleshooting guide\.

1. Watch the status of your nodes and wait for them to reach the `Ready` status\.

   ```
   kubectl get nodes --watch
   ```

1. \(GPU nodes only\) If you chose a GPU instance type and the Amazon EKS optimized accelerated AMI, you must apply the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) as a DaemonSet on your cluster with the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.6.0/nvidia-device-plugin.yml
   ```

1. \(Optional\) Deploy a [sample application](sample-deployment.md) to test your cluster and Linux nodes\.