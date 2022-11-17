# Launching self\-managed Amazon Linux nodes<a name="launch-workers"></a>

This topic describes how you can launch Auto Scaling groups of Linux nodes that register with your Amazon EKS cluster\. After the nodes join the cluster, you can deploy Kubernetes applications to them\. You can also launch self\-managed Amazon Linux 2 nodes with `eksctl` or the AWS Management Console\. If you need to launch nodes on AWS Outposts, see [Launching self\-managed Amazon Linux nodes on an Outpost](eks-outposts-self-managed-nodes.md)\.

**Prerequisites**
+ An existing Amazon EKS cluster\. To deploy one, see [Creating an Amazon EKS cluster](create-cluster.md)\. If you have subnets in the AWS Region where you have AWS Outposts, AWS Wavelength, or AWS Local Zones enabled, those subnets must not have been passed in when you created your cluster\.
+ \(Optional, but recommended\) The Amazon VPC CNI plugin for Kubernetes add\-on configured with its own IAM role that has the necessary IAM policy attached to it\. For more information, see [Configuring the Amazon VPC CNI plugin for Kubernetes to use IAM roles for service accounts](cni-iam-role.md)\.
+ Familiarity with the considerations listed in [Choosing an Amazon EC2 instance type](choosing-instance-type.md)\. Depending on the instance type you choose, there may be additional prerequisites for your cluster and VPC\.

------
#### [ eksctl ]

**Prerequisite**  
Version `0.118.0` or later of the `eksctl` command line tool installed on your device or AWS CloudShell\. To install or update `eksctl`, see [Installing or updating `eksctl`](eksctl.md)\.

**To launch self\-managed Linux nodes using `eksctl`**

1. \(Optional\) If the **AmazonEKS\_CNI\_Policy** managed IAM policy is attached to your [Amazon EKS node IAM role](create-node-role.md), we recommend assigning it to an IAM role that you associate to the Kubernetes `aws-node` service account instead\. For more information, see [Configuring the Amazon VPC CNI plugin for Kubernetes to use IAM roles for service accounts](cni-iam-role.md)\.

1. The following command creates a node group in an existing cluster\. Replace *al\-nodes* with a name for your node group\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can't be longer than 100 characters\.\. Replace my\-cluster with the name of your cluster\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can't be longer than 100 characters\.\. Replace the remaining `example value` with your own values\. The nodes are created with the same Kubernetes version as the control plane, by default\. 

   Before choosing a value for `--node-type`, review [Choosing an Amazon EC2 instance type](choosing-instance-type.md)\.

   Replace `my-key` with the name of your Amazon EC2 key pair or public key\. This key is used to SSH into your nodes after they launch\. If you don't already have an Amazon EC2 key pair, you can create one in the AWS Management Console\. For more information, see [Amazon EC2 key pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) in the *Amazon EC2 User Guide for Linux Instances*\.

   Create your node group with the following command\.
**Important**  
If you want to deploy a node group to AWS Outposts, Wavelength, or Local Zone subnets, there are additional considerations:  
The subnets must not have been passed in when you created the cluster\.
You must create the node group with a config file that specifies the subnets and `[volumeType](https://eksctl.io/usage/schema/#nodeGroups-volumeType): gp2`\. For more information, see [Create a nodegroup from a config file](https://eksctl.io/usage/managing-nodegroups/#creating-a-nodegroup-from-a-config-file) and [Config file schema](https://eksctl.io/usage/schema/) in the `eksctl` documentation\.

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
   + can assign a significantly higher number of IP addresses to pods than the default configuration, see [Increase the amount of available IP addresses for your Amazon EC2 nodes](cni-increase-ip-addresses.md)\.
   + can assign `IPv4` addresses to pods from a different CIDR block than that of the instance, see [Tutorial: Custom networking](cni-custom-network.md)\.
   + can assign `IPv6` addresses to pods and services, see [Tutorial: Assigning `IPv6` addresses to pods and services](cni-ipv6.md)\.
   + use the `containerd` runtime, you must deploy the node group using a `config` file\. For more information, see [Enable the `containerd` runtime bootstrap flag](eks-optimized-ami.md#containerd-bootstrap)\.
   + don't have outbound internet access, see [Private cluster requirements](private-clusters.md)\.

   For a complete list of all available options and defaults, enter the following command\.

   ```
   eksctl create nodegroup --help
   ```

   If nodes fail to join the cluster, then see [Nodes fail to join cluster](troubleshooting.md#worker-node-fail) in the Troubleshooting guide\.

   The example output is as follows\. Several lines are output while the nodes are created\. One of the last lines of output is the following example line\.

   ```
   [✔]  created 1 nodegroup(s) in cluster "my-cluster"
   ```

1. We recommend blocking pod access to IMDS if the following conditions are true:
   + You plan to assign IAM roles to all of your Kubernetes service accounts so that pods only have the minimum permissions that they need\.
   + No pods in the cluster require access to the Amazon EC2 instance metadata service \(IMDS\) for other reasons, such as retrieving the current AWS Region\.

   For more information, see [Restrict access to the instance profile assigned to the worker node](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node)\.

------
