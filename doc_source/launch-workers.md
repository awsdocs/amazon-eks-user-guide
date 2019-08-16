# Launching Amazon EKS Worker Nodes<a name="launch-workers"></a>

This topic helps you to launch an Auto Scaling group of worker nodes that register with your Amazon EKS cluster\. After the nodes join the cluster, you can deploy Kubernetes applications to them\.

If this is your first time launching Amazon EKS worker nodes, we recommend that you follow one of our [Getting Started with Amazon EKS](getting-started.md) guides instead\. They provide complete end\-to\-end walkthroughs for creating an Amazon EKS cluster with worker nodes\.

**Important**  
Amazon EKS worker nodes are standard Amazon EC2 instances, and you are billed for them based on normal Amazon EC2 prices\. For more information, see [Amazon EC2 Pricing](https://aws.amazon.com/ec2/pricing/)\.

Choose the tab below that corresponds to your desired worker node creation method:

------
#### [ eksctl ]

**To launch worker nodes with `eksctl`**

This procedure assumes that you have installed `eksctl`, and that your `eksctl` version is at least `0.1.37`\. You can check your version with the following command:

```
eksctl version
```

 For more information on installing or upgrading `eksctl`, see [Installing or Upgrading `eksctl`](eksctl.md#installing-eksctl)\.
**Note**  
This procedure only works for clusters that were created with `eksctl`\.
+ Create your worker node group with the following command\. Substitute the red text with your own values\.

  ```
  eksctl create nodegroup \
  --cluster default \
  --version auto \
  --name standard-workers \
  --node-type t3.medium \
  --node-ami auto \
  --nodes 3 \
  --nodes-min 1 \
  --nodes-max 4
  ```
**Note**  
For more information on the available options for eksctl create nodegroup, see the project [README on GitHub](https://github.com/weaveworks/eksctl/blob/master/README.md) or view the help page with the following command\.  

  ```
  eksctl create nodegroup --help
  ```

  Output:

  ```
  [ℹ]  using region us-west-2
  [ℹ]  will use version 1.12 for new nodegroup(s) based on control plane version
  [ℹ]  nodegroup "standard-workers" will use "ami-0923e4b35a30a5f53" [AmazonLinux2/1.12]
  [ℹ]  1 nodegroup (standard-workers) was included
  [ℹ]  will create a CloudFormation stack for each of 1 nodegroups in cluster "default"
  [ℹ]  1 task: { create nodegroup "standard-workers" }
  [ℹ]  building nodegroup stack "eksctl-default-nodegroup-standard-workers"
  [ℹ]  deploying stack "eksctl-default-nodegroup-standard-workers"
  [ℹ]  adding role "arn:aws:iam::111122223333:role/eksctl-default-nodegroup-standard-NodeInstanceRole-12C2JO814XSEE" to auth ConfigMap
  [ℹ]  nodegroup "standard-workers" has 0 node(s)
  [ℹ]  waiting for at least 1 node(s) to become ready in "standard-workers"
  [ℹ]  nodegroup "standard-workers" has 3 node(s)
  [ℹ]  node "ip-192-168-52-42.us-west-2.compute.internal" is ready
  [ℹ]  node "ip-192-168-7-27.us-west-2.compute.internal" is not ready
  [ℹ]  node "ip-192-168-76-138.us-west-2.compute.internal" is not ready
  [✔]  created 1 nodegroup(s) in cluster "default"
  [ℹ]  checking security group configuration for all nodegroups
  [ℹ]  all nodegroups have up-to-date configuration
  ```

------
#### [ AWS Management Console ]

**To launch your worker nodes with the AWS Management Console**

These procedures have the following prerequisites:
+ You have created a VPC and security group that meet the requirements for an Amazon EKS cluster\. For more information, see [Cluster VPC Considerations](network_reqs.md) and [Cluster Security Group Considerations](sec-group-reqs.md)\. The [Getting Started with Amazon EKS](getting-started.md) guide creates a VPC that meets the requirements, or you can also follow [Creating a VPC for Your Amazon EKS Cluster](create-public-private-vpc.md) to create one manually\.
+ You have created an Amazon EKS cluster and specified that it use the VPC and security group that meet the requirements of an Amazon EKS cluster\. For more information, see [Creating an Amazon EKS Cluster](create-cluster.md)\.

1. Wait for your cluster status to show as `ACTIVE`\. If you launch your worker nodes before the cluster is active, the worker nodes will fail to register with the cluster and you will have to relaunch them\.

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. From the navigation bar, select a Region that supports Amazon EKS\.

1. Choose **Create stack**\.

1. For **Choose a template**, select **Specify an Amazon S3 template URL**\.

1. Paste the following URL into the text area and choose **Next**\.

   ```
   https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-02-11/amazon-eks-nodegroup.yaml
   ```
**Note**  
If you intend to only deploy worker nodes to private subnets, you should edit this template in the AWS CloudFormation designer and modify the `AssociatePublicIpAddress` parameter in the `NodeLaunchConfig` to be `false`\.  

   ```
   AssociatePublicIpAddress: 'false'
   ```

1. On the **Specify Details** page, fill out the following parameters accordingly, and choose **Next**:
   + **Stack name** – Choose a stack name for your AWS CloudFormation stack\. For example, you can call it ***<cluster\-name>*\-worker\-nodes**\.
   + **ClusterName** – Enter the name that you used when you created your Amazon EKS cluster\.
**Important**  
This name must exactly match your Amazon EKS cluster name\. Otherwise, your worker nodes will be unable to join it\.
   + **ClusterControlPlaneSecurityGroup** – Enter the security group or groups that you used when you created your Amazon EKS cluster\. This AWS CloudFormation template creates a worker node security group that allows traffic to and from the cluster control plane security group specified\.
**Important**  
The worker node AWS CloudFormation template modifies the security group that you specify here, so **Amazon EKS strongly recommends that you use a dedicated security group for each cluster control plane \(one per cluster\)**\. If this security group is shared with other resources, you might block or disrupt connections to those resources\.
   + **NodeGroupName** – Enter a name for your node group\. This name can be used later to identify the Auto Scaling node group that is created for your worker nodes\.
   + **NodeAutoScalingGroupMinSize** – Enter the minimum number of nodes to which your worker node Auto Scaling group can scale in\.
   + **NodeAutoScalingGroupDesiredCapacity** – Enter the desired number of nodes to scale to when your stack is created\.
   + **NodeAutoScalingGroupMaxSize** – Enter the maximum number of nodes to which your worker node Auto Scaling group can scale out\. This value must be at least one node greater than your desired capacity so that you can perform a rolling update of your worker nodes without reducing your node count during the update\.
   + **NodeInstanceType** – Choose an instance type for your worker nodes\. The instance type and size that you choose determines how many IP addresses are available per worker node for the containers in your pods\. For more information, see [IP Addresses Per Network Interface Per Instance Type](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#AvailableIpPerENI) in the *Amazon EC2 User Guide for Linux Instances*\.
**Note**  
The supported instance types for the latest version of the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) are shown [here](https://github.com/aws/amazon-vpc-cni-k8s/blob/release-1.5/pkg/awsutils/vpc_ip_resource_limit.go)\. You may need to update your CNI version to take advantage of the latest supported instance types\. For more information, see [Amazon VPC CNI Plugin for Kubernetes Upgrades](cni-upgrades.md)\.
**Important**  
Some instance types might not be available in all regions\.
   + **NodeImageId** – Enter the current Amazon EKS worker node AMI ID for your Region\. The AMI IDs for the latest Amazon EKS\-optimized AMI \(with and without [GPU support](gpu-ami.md)\) are shown in the following table\. Be sure to choose the correct AMI ID for your desired Kubernetes version and AWS region\.
**Note**  
The Amazon EKS\-optimized AMI with GPU support only supports P2 and P3 instance types\. Be sure to specify these instance types in your worker node AWS CloudFormation template\. By using the Amazon EKS\-optimized AMI with GPU support, you agree to [NVIDIA's end user license agreement \(EULA\)](https://www.nvidia.com/en-us/about-nvidia/eula-agreement/)\.

------
#### [ Kubernetes version 1\.13\.8 ]    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/launch-workers.html)

------
#### [ Kubernetes version 1\.12\.10 ]    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/launch-workers.html)

------
#### [ Kubernetes version 1\.11\.10 ]    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/launch-workers.html)

------
**Note**  
The Amazon EKS worker node AMI is based on Amazon Linux 2\. You can track security or privacy events for Amazon Linux 2 at the [Amazon Linux Security Center](https://alas.aws.amazon.com/alas2.html) or subscribe to the associated [RSS feed](https://alas.aws.amazon.com/AL2/alas.rss)\. Security and privacy events include an overview of the issue, what packages are affected, and how to update your instances to correct the issue\.
   + **KeyName** – Enter the name of an Amazon EC2 SSH key pair that you can use to connect using SSH into your worker nodes with after they launch\. If you don't already have an Amazon EC2 keypair, you can create one in the AWS Management Console\. For more information, see [Amazon EC2 Key Pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) in the *Amazon EC2 User Guide for Linux Instances*\.
**Note**  
If you do not provide a keypair here, the AWS CloudFormation stack creation fails\.
   + **BootstrapArguments** – Specify any optional arguments to pass to the worker node bootstrap script, such as extra kubelet arguments\. For more information, view the bootstrap script usage information at [https://github\.com/awslabs/amazon\-eks\-ami/blob/master/files/bootstrap\.sh](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) 
   + **VpcId** – Enter the ID for the VPC that your worker nodes should launch into\.
   + **Subnets** – Choose the subnets within the preceding VPC that your worker nodes should launch into\. If you are launching worker nodes into only private subnets, do not include public subnets here\.

1. On the **Options** page, you can choose to tag your stack resources\. Choose **Next**\.

1. On the **Review** page, review your information, acknowledge that the stack might create IAM resources, and then choose **Create**\.

1. When your stack has finished creating, select it in the console and choose **Outputs**\.

1. Record the **NodeInstanceRole** for the node group that was created\. You need this when you configure your Amazon EKS worker nodes\.

**To enable worker nodes to join your cluster**

1. Download, edit, and apply the AWS IAM Authenticator configuration map\.

   1. Use the following command to download the configuration map:

      ```
      curl -o aws-auth-cm.yaml https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-02-11/aws-auth-cm.yaml
      ```

   1. Open the file with your favorite text editor\. Replace the *<ARN of instance role \(not instance profile\)>* snippet with the **NodeInstanceRole** value that you recorded in the previous procedure, and save the file\.
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
If you receive the error `"aws-iam-authenticator": executable file not found in $PATH`, your kubectl isn't configured for Amazon EKS\. For more information, see [Installing `aws-iam-authenticator`](install-aws-iam-authenticator.md)\.  
If you receive any other authorization or resource type errors, see [Unauthorized or Access Denied \(`kubectl`\)](troubleshooting.md#unauthorized) in the troubleshooting section\.

1. Watch the status of your nodes and wait for them to reach the `Ready` status\.

   ```
   kubectl get nodes --watch
   ```

1. \(GPU workers only\) If you chose a P2 or P3 instance type and the Amazon EKS\-optimized AMI with GPU support, you must apply the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) as a DaemonSet on your cluster with the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/1.0.0-beta/nvidia-device-plugin.yml
   ```

------