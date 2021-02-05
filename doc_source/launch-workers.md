# Launching self\-managed Amazon Linux nodes<a name="launch-workers"></a>

This topic helps you to launch an Auto Scaling group of Linux nodes that register with your Amazon EKS cluster\. After the nodes join the cluster, you can deploy Kubernetes applications to them\. You can launch self\-managed Amazon Linux 2 nodes with `eksctl` or the AWS Management Console\.

**To launch self\-managed Linux nodes using `eksctl`**

This procedure has the following prerequisites:
+ An existing Amazon EKS cluster that was created using `eksctl`\.
+ `eksctl` version `0.37.0` or later\. For more information about installing or upgrading `eksctl`, see [Installing or upgrading `eksctl`](eksctl.md#installing-eksctl)\.
**Important**  
Do not use `eksctl` to create a cluster or nodes in an AWS Region where you have AWS Outposts, AWS Wavelength, or AWS Local Zones enabled\. Create a cluster and self\-managed nodes using the Amazon EC2 API or AWS CloudFormation instead\. For more information, see [Launching self\-managed Amazon Linux nodes](#launch-workers) and [Launching self\-managed Windows nodes](launch-windows-workers.md)\.

1. \(Optional\) If the **AmazonEKS\_CNI\_Policy** managed IAM policy is attached to your [Amazon EKS node IAM role](create-node-role.md), we recommend assigning it to an IAM role that you associate to the Kubernetes `aws-node` service account instead\. For more information, see [Configuring the VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.

1. The following command creates a node group in an existing cluster\. Replace the `<example values>` \(including `<>`\) with your own values\. The nodes are created with the same Kubernetes version as the control plane, by default\. 

   If you want to deploy on Amazon EC2 Arm instances, then replace `t3.medium` with an Arm instance type\. If specifying an Arm Amazon EC2 instance type, then review the considerations in [Amazon EKS optimized Arm Amazon Linux AMIs](eks-optimized-ami.md#arm-ami) before deploying\. For a complete list of supported values for `--node-type`, see the list in `[amazon\-eks\-nodegroup\.yaml](https://github.com/awslabs/amazon-eks-ami/blob/master/amazon-eks-nodegroup.yaml)` on GitHub\.

   Replace `<my-key>` with the name of your Amazon EC2 key pair or public key\. This key is used to SSH into your nodes after they launch\. If you don't already have an Amazon EC2 key pair, you can create one in the AWS Management Console\. For more information, see [Amazon EC2 key pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) in the *Amazon EC2 User Guide for Linux Instances*\.

   Create your node group with the following command\.

   ```
   eksctl create nodegroup \
     --cluster <my-cluster> \
     --name <al-nodes> \
     --node-type <t3.medium> \
     --nodes <3> \
     --nodes-min <1> \
     --nodes-max <4> \
     --ssh-access \
     --ssh-public-key <my-key>
   ```

   For a complete list of all available options and defaults, enter the following command\.

   ```
   eksctl create nodegroup --help
   ```

   If nodes fail to join the cluster, then see [Nodes fail to join cluster](troubleshooting.md#worker-node-fail) in the Troubleshooting guide\.

   Output:

   You'll see several lines of output as the nodes are created\. One of the last lines of output is the following example line\.

   ```
   [✔]  created 1 nodegroup(s) in cluster "<my-cluster>"
   ```

1. \(Optional\) If you plan to assign IAM roles to all of your Kubernetes service accounts so that pods only have the minimum permissions that they need, and no pods in the cluster require access to the Amazon EC2 instance metadata service \(IMDS\) for other reasons, such as retrieving the current Region, then we recommend blocking pod access to IMDS\. For more information, see [IAM roles for service accounts](iam-roles-for-service-accounts.md) and [Restricting access to the IMDS and Amazon EC2 instance profile credentials](best-practices-security.md#restrict-ec2-credential-access)\.

**To launch self\-managed Linux nodes using the AWS Management Console**

This procedure has the following prerequisites:
+ An existing VPC and security group that meet the requirements for an Amazon EKS cluster\. For more information, see [Cluster VPC considerations](network_reqs.md) and [Amazon EKS security group considerations](sec-group-reqs.md)\. The [Getting started with Amazon EKS](getting-started.md) guide creates a VPC that meets the requirements, or you can also follow [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md) to create one manually\.
+ An existing Amazon EKS cluster that uses a VPC and security group that meet the requirements of an Amazon EKS cluster\. For more information, see [Creating an Amazon EKS cluster](create-cluster.md)\.

1. Wait for your cluster status to show as `ACTIVE`\. If you launch your nodes before the cluster is active, the nodes will fail to register with the cluster and you will have to relaunch them\.

1. Download the latest version of the AWS CloudFormation template\.

   ```
   curl -o amazon-eks-nodegroup.yaml https://github.com/awslabs/amazon-eks-ami/blob/master/amazon-eks-nodegroup.yaml
   ```

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. Choose **Create stack** and then select **With new resources \(standard\)**\.

1. For **Specify template**, select **Upload a template file** and then select **Choose file**\. Select the `amazon-eks-nodegroup.yaml` file that you downloaded in step 2 and then select **Next**\.

1. On the **Specify stack details** page, fill out the following parameters accordingly:
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it **cluster\-name\-nodes**\.
   + **ClusterName**: Enter the name that you used when you created your Amazon EKS cluster\.
**Important**  
This name must exactly match the name you used in [Step 1: Create your Amazon EKS cluster](getting-started-console.md#eks-create-cluster); otherwise, your nodes cannot join the cluster\.
   + **ClusterControlPlaneSecurityGroup**: Choose the **SecurityGroups** value from the AWS CloudFormation output that you generated when you created your [VPC](create-public-private-vpc.md)\.
   + **NodeGroupName**: Enter a name for your node group\. This name can be used later to identify the Auto Scaling node group that is created for your nodes\.
   + **NodeAutoScalingGroupMinSize**: Enter the minimum number of nodes that your node Auto Scaling group can scale in to\.
   + **NodeAutoScalingGroupDesiredCapacity**: Enter the desired number of nodes to scale to when your stack is created\.
   + **NodeAutoScalingGroupMaxSize**: Enter the maximum number of nodes that your node Auto Scaling group can scale out to\.
   + **NodeInstanceType**: Choose an instance type for your nodes\. You can also [view the list](https://github.com/awslabs/amazon-eks-ami/blob/master/amazon-eks-nodegroup.yaml) in the `amazon-eks-nodegroup.yaml` file on GitHub\. Before choosing an Arm instance type, make sure to review the considerations in [Amazon EKS optimized Arm Amazon Linux AMIs](eks-optimized-ami.md#arm-ami)\.
**Note**  
The supported instance types for the latest version of the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) are shown [here](https://github.com/aws/amazon-vpc-cni-k8s/blob/release-1.7/pkg/awsutils/vpc_ip_resource_limit.go)\. You may need to update your CNI version to take advantage of the latest supported instance types\. For more information, see [Amazon VPC CNI plugin for Kubernetes upgrades](cni-upgrades.md)\.
**Important**  
Some instance types might not be available in all Regions\.
   + **NodeImageIdSSMParam**: Pre\-populated with the Amazon EC2 Systems Manager parameter of a recent Amazon EKS optimized Amazon Linux AMI ID for a Kubernetes version\. If you want to use a different Kubernetes minor version supported with Amazon EKS, then you can replace `1.x` with a different [supported version](kubernetes-versions.md)\. We recommend specifying the same Kubernetes version as your cluster\.

     If you want to use the Amazon EKS optimized accelerated AMI, then replace `amazon-linux-2` with `amazon-linux-2-gpu`\. If you want to use the Amazon EKS optimized Arm AMI, then replace `amazon-linux-2` with `amazon-linux-2-arm64`\.
**Note**  
The Amazon EKS node AMI is based on Amazon Linux 2\. You can track security or privacy events for Amazon Linux 2 at the [Amazon Linux Security Center](https://alas.aws.amazon.com/alas2.html) or subscribe to the associated [RSS feed](https://alas.aws.amazon.com/AL2/alas.rss)\. Security and privacy events include an overview of the issue, what packages are affected, and how to update your instances to correct the issue\.
   + **NodeImageId**: \(Optional\) If you are using your own custom AMI \(instead of the Amazon EKS optimized AMI\), enter a node AMI ID for your Region\. If you specify a value here, it overrides any values in the **NodeImageIdSSMParam** field\. 
   + **NodeVolumeSize**: Specify a root volume size for your nodes, in GiB\.
   + **KeyName**: Enter the name of an Amazon EC2 SSH key pair that you can use to connect using SSH into your nodes with after they launch\. If you don't already have an Amazon EC2 key pair, you can create one in the AWS Management Console\. For more information, see [Amazon EC2 key pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) in the *Amazon EC2 User Guide for Linux Instances*\.
**Note**  
If you do not provide a key pair here, the AWS CloudFormation stack creation fails\.
   + **BootstrapArguments**: Specify any optional arguments to pass to the node bootstrap script, such as extra  `kubelet`  arguments\. For more information, view the [bootstrap script usage information](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) on GitHub\. 
**Note**  
If you are launching nodes into a private VPC without outbound internet access, then you need to include the following arguments\.  

       ```
       --apiserver-endpoint <cluster-endpoint> --b64-cluster-ca <cluster-certificate-authority>
       ```
If you want to assign IP addresses to pods that are from a different CIDR block than the block that includes the IP address for the node, then you may need to add a CIDR block to your VPC and specify an argument to support the capability\. For more information, see [CNI custom networking](cni-custom-network.md)\.
   + **DisableIMDSv1**: Each node supports the Instance Metadata Service Version 1 \(IMDSv1\) and IMDSv2 by default, but you can disable IMDSv1\. Select **true** if you don't want any nodes in the node group, or any pods scheduled on the nodes in the node group to use IMDSv1\. For more information about IMDS, see [Configuring the instance metadata service](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html)\. For more information about restricting access to it on your nodes, see [Restricting access to the IMDS and Amazon EC2 instance profile credentials](best-practices-security.md#restrict-ec2-credential-access)\.
   + **VpcId**: Enter the ID for the [VPC](create-public-private-vpc.md) that you created\.
   + **Subnets**: Choose the subnets that you created for your VPC\. If you created your VPC using the steps described in [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md), then specify only the private subnets within the VPC for your nodes to launch into\.
**Important**  
If any of the subnets are public subnets, then they must have the automatic public IP address assignment setting enabled\. If the setting is not enabled for the public subnet, then any nodes that you deploy to that public subnet will not be assigned a public IP address and will not be able to communicate with the cluster or other AWS services\. If the subnet was deployed before March 26, 2020 using either of the [Amazon EKS AWS CloudFormation VPC templates](create-public-private-vpc.md), or by using `eksctl`, then automatic public IP address assignment is disabled for public subnets\. For information about how to enable public IP address assignment for a subnet, see [ Modifying the Public IPv4 Addressing Attribute for Your Subnet](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#subnet-public-ip)\. If the node is deployed to a private subnet, then it is able to communicate with the cluster and other AWS services through a NAT gateway\.
**Important**  
If the subnets do not have internet access, then make sure that you're aware of the considerations and extra steps in [Private clusters](private-clusters.md)\.
Ensure that the subnets you select are tagged with the cluster name\. For more information, see [Subnet tagging requirement](network_reqs.md#vpc-subnet-tagging)\. If you have subnets in AWS Outposts, AWS Wavelength, or an AWS Local Zone, they likely are not currently tagged\.

1. Acknowledge that the stack might create IAM resources, and then choose **Create stack**\.

1. When your stack has finished creating, select it in the console and choose **Outputs**\.

1. Record the **NodeInstanceRole** for the node group that was created\. You need this when you configure your Amazon EKS nodes\.

**To enable nodes to join your cluster**
**Note**  
If you launched nodes inside a private VPC without outbound internet access, then you must enable nodes to join your cluster from within the VPC\.

1. Download, edit, and apply the AWS IAM Authenticator configuration map\.

   1. Use the command that corresponds to the Region that your cluster is in to download the configuration map:
      + All Regions other than China \(Beijing\) and China \(Ningxia\)

        ```
        curl -o aws-auth-cm.yaml https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/aws-auth-cm.yaml
        ```
      + China \(Beijing\) and China \(Ningxia\)

        ```
        curl -o aws-auth-cm.yaml https://s3.cn-north-1.amazonaws.com.cn/amazon-eks/cloudformation/2020-10-29/aws-auth-cm.yaml
        ```

   1. Open the file with your text editor\. Replace the `<ARN of instance role (not instance profile)>` snippet with the **NodeInstanceRole** value that you recorded in the previous procedure, and save the file\.
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

1. \(Optional\) If the **AmazonEKS\_CNI\_Policy** managed IAM policy is attached to your [Amazon EKS node IAM role](create-node-role.md), we recommend assigning it to an IAM role that you associate to the Kubernetes `aws-node` service account instead\. For more information, see [Configuring the VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.

1. \(Optional\) If you plan to assign IAM roles to all of your Kubernetes service accounts so that pods only have the minimum permissions that they need, and no pods in the cluster require access to the Amazon EC2 instance metadata service \(IMDS\) for other reasons, such as retrieving the current Region, then we recommend blocking pod access to IMDS\. For more information, see [IAM roles for service accounts](iam-roles-for-service-accounts.md) and [Restricting access to the IMDS and Amazon EC2 instance profile credentials](best-practices-security.md#restrict-ec2-credential-access)\.