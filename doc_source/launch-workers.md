# Launching self\-managed Amazon Linux nodes<a name="launch-workers"></a>

This topic describes how you can launch Auto Scaling groups of Linux nodes that register with your Amazon EKS cluster\. After the nodes join the cluster, you can deploy Kubernetes applications to them\. You can also launch self\-managed Amazon Linux nodes with `eksctl` or the AWS Management Console\. If you need to launch nodes on AWS Outposts, see [Launching self\-managed Amazon Linux nodes on an Outpost](eks-outposts-self-managed-nodes.md)\.

**Prerequisites**
+ An existing Amazon EKS cluster\. To deploy one, see [Creating an Amazon EKS cluster](create-cluster.md)\. If you have subnets in the AWS Region where you have AWS Outposts, AWS Wavelength, or AWS Local Zones enabled, those subnets must not have been passed in when you created your cluster\.
+ An existing IAM role for the nodes to use\. To create one, see [Amazon EKS node IAM role](create-node-role.md)\. If this role doesn't have either of the policies for the VPC CNI, the separate role that follows is required for the VPC CNI pods\.
+ \(Optional, but recommended\) The Amazon VPC CNI plugin for Kubernetes add\-on configured with its own IAM role that has the necessary IAM policy attached to it\. For more information, see [Configuring the Amazon VPC CNI plugin for Kubernetes to use IAM roles for service accounts \(IRSA\)](cni-iam-role.md)\.
+ Familiarity with the considerations listed in [Choosing an Amazon EC2 instance type](choosing-instance-type.md)\. Depending on the instance type you choose, there may be additional prerequisites for your cluster and VPC\.

------
#### [ eksctl ]

**Note**  
`eksctl` doesn't support Amazon Linux 2023 at this time\. 

**Prerequisite**  
Version `0.175.0` or later of the `eksctl` command line tool installed on your device or AWS CloudShell\. To install or update `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.

**To launch self\-managed Linux nodes using `eksctl`**

1. \(Optional\) If the **AmazonEKS\_CNI\_Policy** managed IAM policy is attached to your [Amazon EKS node IAM role](create-node-role.md), we recommend assigning it to an IAM role that you associate to the Kubernetes `aws-node` service account instead\. For more information, see [Configuring the Amazon VPC CNI plugin for Kubernetes to use IAM roles for service accounts \(IRSA\)](cni-iam-role.md)\.

1. The following command creates a node group in an existing cluster\. Replace `al-nodes` with a name for your node group\. The node group name can't be longer than 63 characters\. It must start with letter or digit, but can also include hyphens and underscores for the remaining characters\. Replace `my-cluster` with the name of your cluster\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can't be longer than 100 characters\. Replace the remaining `example value` with your own values\. The nodes are created with the same Kubernetes version as the control plane, by default\. 

   Before choosing a value for `--node-type`, review [Choosing an Amazon EC2 instance type](choosing-instance-type.md)\.

   Replace `my-key` with the name of your Amazon EC2 key pair or public key\. This key is used to SSH into your nodes after they launch\. If you don't already have an Amazon EC2 key pair, you can create one in the AWS Management Console\. For more information, see [Amazon EC2 key pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) in the *Amazon EC2 User Guide for Linux Instances*\.

   Create your node group with the following command\.
**Important**  
If you want to deploy a node group to AWS Outposts, Wavelength, or Local Zone subnets, there are additional considerations:  
The subnets must not have been passed in when you created the cluster\.
You must create the node group with a config file that specifies the subnets and `[volumeType](https://eksctl.io/usage/schema/#nodeGroups-volumeType): gp2`\. For more information, see [Create a nodegroup from a config file](https://eksctl.io/usage/nodegroups/#creating-a-nodegroup-from-a-config-file) and [Config file schema](https://eksctl.io/usage/schema/) in the `eksctl` documentation\.

   ```
   eksctl create nodegroup \
     --cluster my-cluster \
     --name al-nodes \
     --node-type t3.medium \
     --nodes 3 \
     --nodes-min 1 \
     --nodes-max 4 \
     --ssh-access \
     --managed=false \
     --ssh-public-key my-key
   ```

   To deploy a node group that:
   + can assign a significantly higher number of IP addresses to Pods than the default configuration, see [Increase the amount of available IP addresses for your Amazon EC2 nodes](cni-increase-ip-addresses.md)\.
   + can assign `IPv4` addresses to Pods from a different CIDR block than that of the instance, see [Custom networking for pods](cni-custom-network.md)\.
   + can assign `IPv6` addresses to Pods and services, see [`IPv6` addresses for clusters, Pods, and services](cni-ipv6.md)\.
   + use the `containerd` runtime, you must deploy the node group using a `config` file\. For more information, see [Test migration from Docker to `containerd`](eks-optimized-ami.md#containerd-bootstrap)\.
   + don't have outbound internet access, see [Private cluster requirements](private-clusters.md)\.

   For a complete list of all available options and defaults, enter the following command\.

   ```
   eksctl create nodegroup --help
   ```

   If nodes fail to join the cluster, then see [Nodes fail to join cluster](troubleshooting.md#worker-node-fail) in the Troubleshooting guide\.

   An example output is as follows\. Several lines are output while the nodes are created\. One of the last lines of output is the following example line\.

   ```
   [✔]  created 1 nodegroup(s) in cluster "my-cluster"
   ```

1. \(Optional\) Deploy a [sample application](sample-deployment.md) to test your cluster and Linux nodes\.

1. We recommend blocking Pod access to IMDS if the following conditions are true:
   + You plan to assign IAM roles to all of your Kubernetes service accounts so that Pods only have the minimum permissions that they need\.
   + No Pods in the cluster require access to the Amazon EC2 instance metadata service \(IMDS\) for other reasons, such as retrieving the current AWS Region\.

   For more information, see [Restrict access to the instance profile assigned to the worker node](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node)\.

------
#### [ AWS Management Console ]

**Step 1: To launch self\-managed Linux nodes using the AWS Management Console**

1. Download the latest version of the AWS CloudFormation template\.

   ```
   curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2022-12-23/amazon-eks-nodegroup.yaml
   ```

1. Wait for your cluster status to show as `ACTIVE`\. If you launch your nodes before the cluster is active, the nodes fail to register with the cluster and you will have to relaunch them\.

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. Choose **Create stack** and then select **With new resources \(standard\)**\.

1. For **Specify template**, select **Upload a template file** and then select **Choose file**\.

1. Select the `amazon-eks-nodegroup.yaml` file that you downloaded\.

1. Select **Next**\.

1. On the **Specify stack details** page, enter the following parameters accordingly, and then choose **Next**:
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it **`my-cluster-nodes`**\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can't be longer than 100 characters\.
   + **ClusterName**: Enter the name that you used when you created your Amazon EKS cluster\. This name must equal the cluster name or your nodes can't join the cluster\.
   + **ClusterControlPlaneSecurityGroup**: Choose the **SecurityGroups** value from the AWS CloudFormation output that you generated when you created your [VPC](creating-a-vpc.md)\.

     The following steps show one operation to retrieve the applicable group\.

     1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

     1. Choose the name of the cluster\.

     1. Choose the **Networking** tab\.

     1. Use the **Additional security groups** value as a reference when selecting from the **ClusterControlPlaneSecurityGroup** dropdown list\.
   + **NodeGroupName**: Enter a name for your node group\. This name can be used later to identify the Auto Scaling node group that's created for your nodes\. The node group name can't be longer than 63 characters\. It must start with letter or digit, but can also include hyphens and underscores for the remaining characters\.
   + **NodeAutoScalingGroupMinSize**: Enter the minimum number of nodes that your node Auto Scaling group can scale in to\.
   + **NodeAutoScalingGroupDesiredCapacity**: Enter the desired number of nodes to scale to when your stack is created\.
   + **NodeAutoScalingGroupMaxSize**: Enter the maximum number of nodes that your node Auto Scaling group can scale out to\.
   + **NodeInstanceType**: Choose an instance type for your nodes\. For more information, see [Choosing an Amazon EC2 instance type](choosing-instance-type.md)\.
   + **NodeImageIdSSMParam**: Pre\-populated with the Amazon EC2 Systems Manager parameter of a recent Amazon EKS optimized AMI for a variable Kubernetes version\. To use a different Kubernetes minor version supported with Amazon EKS, replace `1.XX` with a different [supported version](kubernetes-versions.md)\. We recommend specifying the same Kubernetes version as your cluster\.

     You can also replace `amazon-linux-2` with a different AMI type\. For more information, see [Retrieving Amazon EKS optimized Amazon Linux AMI IDs](retrieve-ami-id.md)\.
**Note**  
The Amazon EKS node AMI is based on Amazon Linux\. You can track security or privacy events for Amazon Linux 2 at the [Amazon Linux Security Center](https://alas.aws.amazon.com/alas2.html) or subscribe to the associated [RSS feed](https://alas.aws.amazon.com/AL2/alas.rss)\. Security and privacy events include an overview of the issue, what packages are affected, and how to update your instances to correct the issue\.
   + **NodeImageId**: \(Optional\) If you're using your own custom AMI \(instead of the Amazon EKS optimized AMI\), enter a node AMI ID for your AWS Region\. If you specify a value here, it overrides any values in the **NodeImageIdSSMParam** field\. 
   + **NodeVolumeSize**: Specify a root volume size for your nodes, in GiB\.
   + **NodeVolumeType**: Specify a root volume type for your nodes\.
   + **KeyName**: Enter the name of an Amazon EC2 SSH key pair that you can use to connect using SSH into your nodes with after they launch\. If you don't already have an Amazon EC2 key pair, you can create one in the AWS Management Console\. For more information, see [Amazon EC2 key pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) in the *Amazon EC2 User Guide for Linux Instances*\.
**Note**  
If you don't provide a key pair here, the AWS CloudFormation stack creation fails\.
   + **BootstrapArguments**: Specify any optional arguments to pass to the node bootstrap script, such as extra `kubelet` arguments\. For more information, view the [bootstrap script usage information](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) on GitHub\.

     To deploy a node group that:
     + can assign a significantly higher number of IP addresses to Pods than the default configuration, see [Increase the amount of available IP addresses for your Amazon EC2 nodes](cni-increase-ip-addresses.md)\.
     + can assign `IPv4` addresses to Pods from a different CIDR block than that of the instance, see [Custom networking for pods](cni-custom-network.md)\.
     + can assign `IPv6` addresses to Pods and services, see [`IPv6` addresses for clusters, Pods, and services](cni-ipv6.md)\.
     + use the `containerd` runtime, you must deploy the node group using a `config` file\. For more information, see [Test migration from Docker to `containerd`](eks-optimized-ami.md#containerd-bootstrap)\.
     + don't have outbound internet access, see [Private cluster requirements](private-clusters.md)\.
   + **DisableIMDSv1**: By default, each node supports the Instance Metadata Service Version 1 \(IMDSv1\) and IMDSv2\. You can disable IMDSv1\. To prevent future nodes and Pods in the node group from using MDSv1, set **DisableIMDSv1** to **true**\. For more information about IMDS, see [Configuring the instance metadata service](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html)\. For more information about restricting access to it on your nodes, see [Restrict access to the instance profile assigned to the worker node](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node)\.
   + **VpcId**: Enter the ID for the [VPC](creating-a-vpc.md) that you created\.
   + **Subnets**: Choose the subnets that you created for your VPC\. If you created your VPC using the steps that are described in [Creating a VPC for your Amazon EKS cluster](creating-a-vpc.md), specify only the private subnets within the VPC for your nodes to launch into\. You can see which subnets are private by opening each subnet link from the **Networking** tab of your cluster\.
**Important**  
If any of the subnets are public subnets, then they must have the automatic public IP address assignment setting enabled\. If the setting isn't enabled for the public subnet, then any nodes that you deploy to that public subnet won't be assigned a public IP address and won't be able to communicate with the cluster or other AWS services\. If the subnet was deployed before March 26, 2020 using either of the [Amazon EKS AWS CloudFormation VPC templates](creating-a-vpc.md), or by using `eksctl`, then automatic public IP address assignment is disabled for public subnets\. For information about how to enable public IP address assignment for a subnet, see [Modifying the public `IPv4` addressing attribute for your subnet](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#subnet-public-ip)\. If the node is deployed to a private subnet, then it's able to communicate with the cluster and other AWS services through a NAT gateway\.
If the subnets don't have internet access, make sure that you're aware of the considerations and extra steps in [Private cluster requirements](private-clusters.md)\.
If you select AWS Outposts, Wavelength, or Local Zone subnets, the subnets must not have been passed in when you created the cluster\.

1. Select your desired choices on the **Configure stack options** page, and then choose **Next**\.

1. Select the check box to the left of **I acknowledge that AWS CloudFormation might create IAM resources\.**, and then choose **Create stack**\.

1. When your stack has finished creating, select it in the console and choose **Outputs**\.

1. Record the **NodeInstanceRole** for the node group that was created\. You need this when you configure your Amazon EKS nodes\.

**Step 2: To enable nodes to join your cluster**
**Note**  
If you launched nodes inside a private VPC without outbound internet access, make sure to enable nodes to join your cluster from within the VPC\.

1. Check to see if you already have an `aws-auth` `ConfigMap`\.

   ```
   kubectl describe configmap -n kube-system aws-auth
   ```

1. If you are shown an `aws-auth` `ConfigMap`, then update it as needed\.

   1. Open the `ConfigMap` for editing\.

      ```
      kubectl edit -n kube-system configmap/aws-auth
      ```

   1. Add a new `mapRoles` entry as needed\. Set the `rolearn` value to the **NodeInstanceRole** value that you recorded in the previous procedure\.

      ```
      [...]
      data:
        mapRoles: |
          - rolearn: <ARN of instance role (not instance profile)>
            username: system:node:{{EC2PrivateDNSName}}
            groups:
              - system:bootstrappers
              - system:nodes
      [...]
      ```

   1. Save the file and exit your text editor\.

1. If you received an error stating "`Error from server (NotFound): configmaps "aws-auth" not found`, then apply the stock `ConfigMap`\.

   1. Download the configuration map\.

      ```
      curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/aws-auth-cm.yaml
      ```

   1. In the `aws-auth-cm.yaml` file, set the `rolearn` value to the **NodeInstanceRole** value that you recorded in the previous procedure\. You can do this with a text editor, or by replacing `my-node-instance-role` and running the following command:

      ```
      sed -i.bak -e 's|<ARN of instance role (not instance profile)>|my-node-instance-role|' aws-auth-cm.yaml
      ```

   1. Apply the configuration\. This command may take a few minutes to finish\.

      ```
      kubectl apply -f aws-auth-cm.yaml
      ```

1. Watch the status of your nodes and wait for them to reach the `Ready` status\.

   ```
   kubectl get nodes --watch
   ```

   Enter `Ctrl`\+`C` to return to a shell prompt\.
**Note**  
If you receive any authorization or resource type errors, see [Unauthorized or access denied \(`kubectl`\)](troubleshooting.md#unauthorized) in the troubleshooting topic\.

   If nodes fail to join the cluster, then see [Nodes fail to join cluster](troubleshooting.md#worker-node-fail) in the Troubleshooting guide\.

1. \(GPU nodes only\) If you chose a GPU instance type and the Amazon EKS optimized accelerated AMI, you must apply the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) as a DaemonSet on your cluster\. Replace `vX.X.X` with your desired [NVIDIA/k8s\-device\-plugin](https://github.com/NVIDIA/k8s-device-plugin/releases) version before running the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/vX.X.X/nvidia-device-plugin.yml
   ```

**Step 3: Additional actions**

1. \(Optional\) Deploy a [sample application](sample-deployment.md) to test your cluster and Linux nodes\.

1. \(Optional\) If the **AmazonEKS\_CNI\_Policy** managed IAM policy \(if you have an `IPv4` cluster\) or the `AmazonEKS_CNI_IPv6_Policy` \(that you [created yourself](cni-iam-role.md#cni-iam-role-create-ipv6-policy) if you have an `IPv6` cluster\) is attached to your [Amazon EKS node IAM role](create-node-role.md), we recommend assigning it to an IAM role that you associate to the Kubernetes `aws-node` service account instead\. For more information, see [Configuring the Amazon VPC CNI plugin for Kubernetes to use IAM roles for service accounts \(IRSA\)](cni-iam-role.md)\.

1. We recommend blocking Pod access to IMDS if the following conditions are true:
   + You plan to assign IAM roles to all of your Kubernetes service accounts so that Pods only have the minimum permissions that they need\.
   + No Pods in the cluster require access to the Amazon EC2 instance metadata service \(IMDS\) for other reasons, such as retrieving the current AWS Region\.

   For more information, see [Restrict access to the instance profile assigned to the worker node](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node)\.

------