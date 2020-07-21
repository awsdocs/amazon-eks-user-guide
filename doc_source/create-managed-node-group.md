# Creating a managed node group<a name="create-managed-node-group"></a>

This topic helps you to launch an Amazon EKS managed node group of Linux nodes that register with your Amazon EKS cluster\. After the nodes join the cluster, you can deploy Kubernetes applications to them\.

[Managed node groups](managed-node-groups.md) are supported on Amazon EKS clusters beginning with Kubernetes version 1\.14 and [platform version](platform-versions.md) `eks.3`\. Existing clusters can update to version 1\.14 or later to take advantage of this feature\. For more information, see [Updating an Amazon EKS cluster Kubernetes version](update-cluster.md)\.

If this is your first time launching an Amazon EKS managed node group, we recommend that you follow one of our [Getting started with Amazon EKS](getting-started.md) guides instead\. The guides provide complete end\-to\-end walkthroughs for creating an Amazon EKS cluster with nodes\.

**Important**  
Amazon EKS nodes are standard Amazon EC2 instances, and you are billed for them based on normal Amazon EC2 prices\. For more information, see [Amazon EC2 Pricing](https://aws.amazon.com/ec2/pricing/)\.

Select the tab with the name of the tool that you'd like to create your managed node group with\.

------
#### [ eksctl ]

**To create a managed node group with `eksctl`**

This procedure requires `eksctl` version `0.24.0` or later\. You can check your version with the following command:

```
eksctl version
```

For more information on installing or upgrading `eksctl`, see [Installing or upgrading `eksctl`](eksctl.md#installing-eksctl)\.
+ Create your managed node group with the following `eksctl` command, replacing the *variable text* with your own values\. 

  ```
  eksctl create nodegroup \
    --cluster my-cluster \
    --region us-west-2 \
    --name my-mng \
    --node-type m5.large \
    --nodes 3 \
    --nodes-min 2 \
    --nodes-min 4 \
    --ssh--access \
    --ssh-public-key my-public-key.pub \
    --managed
  ```

------
#### [ AWS Management Console ]

**To launch your managed node group using the AWS Management Console**

1. Wait for your cluster status to show as `ACTIVE`\. You cannot create a managed node group for a cluster that is not yet `ACTIVE`\.

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the name of the cluster that you want to create your managed node group in\.

1. On the cluster page, select the **Compute** tab, and then choose **Add Node Group**\.

1. On the **Configure node group** page, fill out the parameters accordingly, and then choose **Next**\.
   + **Name** – Enter a unique name for your managed node group\.
   + **Node IAM role name** – Choose the node instance role to use with your node group\. For more information, see [Amazon EKS node IAM role](worker_node_IAM_role.md)\.
**Important**  
We recommend using a role that is not currently in use by any self\-managed node group, or that you plan to use with a new self\-managed node group\. For more information, see [Deleting a managed node group](delete-managed-node-group.md)\.
   + **Subnets** – Choose the subnets to launch your managed nodes into\. 
**Important**  
If you are running a stateful application across multiple Availability Zones that is backed by Amazon EBS volumes and using the Kubernetes [Cluster Autoscaler](cluster-autoscaler.md), you should configure multiple node groups, each scoped to a single Availability Zone\. In addition, you should enable the `--balance-similar-node-groups` feature\.
**Important**  
If you choose a public subnet, then the subnet must have `MapPublicIpOnLaunch` set to true for the instances to be able to successfully join a cluster\. If the subnet was created using `eksctl` or the [Amazon EKS\-vended AWS CloudFormation templates](create-public-private-vpc.md) on or after 03/26/2020, then this setting is already set to true\. If the subnets were created with `eksctl` or the AWS CloudFormation templates before 03/26/2020, then you need to change the setting manually\. For more information, see [Modifying the public IPv4 addressing attribute for your subnet](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#subnet-public-ip)\.
   + **Remote Access** – \(Optional\) You can enable SSH access to the nodes in your managed node group\. Enabling SSH allows you to connect to your instances and gather diagnostic information if there are issues\. Complete the following steps to enable remote access\.
**Note**  
We highly recommend enabling remote access when you create your node group\. You cannot enable remote access after the node group is created\.

     1. Select the check box to **Allow remote access to nodes**\.

     1. For **SSH key pair**, choose an Amazon EC2 SSH key to use\. For more information, see [Amazon EC2 key pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) in the Amazon EC2 User Guide for Linux Instances\.

     1. For **Allow remote access from**, choose **All** to allow SSH access from anywhere on the Internet \(0\.0\.0\.0/0\), or select a security group to allow SSH access from instances that belong to that security group\.
   + **Tags** – \(Optional\) You can choose to tag your Amazon EKS managed node group\. These tags do not propagate to other resources in the node group, such as Auto Scaling groups or instances\. For more information, see [Tagging your Amazon EKS resources](eks-using-tags.md)\.
   + **Kubernetes labels** – \(Optional\) You can choose to apply Kubernetes labels to the nodes in your managed node group\.

1. On the **Set compute configuration** page, fill out the parameters accordingly, and then choose **Next**\.
   + **AMI type** – Choose **Amazon Linux 2 \(AL2\_x86\_64\)** for non\-GPU instances, or **Amazon Linux 2 GPU Enabled \(AL2\_x86\_64\_GPU\)** for GPU instances\.
   + **Instance type** – Choose the instance type to use in your managed node group\. Each Amazon EC2 instance type supports a maximum number of elastic network interfaces \(ENIs\) and each ENI supports a maximum number of IP addresses\. Since each worker node and pod is assigned its own IP address it's important to choose an instance type that will support the maximum number of pods that you want to run on each worker node\. For a list of the number of ENIs and IP addresses supported by instance types, see [ IP addresses per network interface per instance type](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#AvailableIpPerENI)\. For example, the `t3.medium` instance type supports a maximum of 18 IP addresses for the worker node and pods\. Some instance types might not be available in all Regions\.
   + **Disk size** – Enter the disk size \(in GiB\) to use for your node's root volume\.

1. On the **Setup scaling policies** page, fill out the parameters accordingly, and then choose **Next**\.
**Note**  
Amazon EKS does not automatically scale your node group in or out\. However, you can configure the Kubernetes [Cluster Autoscaler](cluster-autoscaler.md) to do this for you\.
   + **Minimum size** – Specify the minimum number of nodes that the managed node group can scale in to\.
   + **Maximum size** – Specify the maximum number of nodes that the managed node group can scale out to\.
   + **Desired size** – Specify the current number of nodes that the managed node group should maintain at launch\.

1. On the **Review and create** page, review your managed node group configuration and choose **Create**\.
**Note**  
If nodes fail to join the cluster, see [Nodes fail to join cluster](troubleshooting.md#worker-node-fail) in the Troubleshooting guide\.

1. Watch the status of your nodes and wait for them to reach the `Ready` status\.

   ```
   kubectl get nodes --watch
   ```

1. \(GPU nodes only\) If you chose a GPU instance type and the Amazon EKS\-optimized accelerated AMI, then you must apply the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) as a DaemonSet on your cluster with the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/1.0.0-beta6/nvidia-device-plugin.yml
   ```

1. \(Optional\) [Deploy a sample Linux application](sample-deployment.md) – Deploy a sample application to test your cluster and Linux nodes\.

------

Now that you have a working Amazon EKS cluster with nodes, you are ready to start installing Kubernetes add\-ons and deploying applications to your cluster\. The following documentation topics help you to extend the functionality of your cluster\.
+ [Cluster Autoscaler](cluster-autoscaler.md) – Configure the Kubernetes Cluster Autoscaler to automatically adjust the number of nodes in your node groups\.
+ [Deploy a sample Linux application](sample-deployment.md) – Deploy a sample application to test your cluster and Linux nodes\.
+ [Deploy a Windows sample application](windows-support.md#windows-sample-application) – Deploy a sample application to test your cluster and Windows nodes\.
+ [Cluster management](eks-managing.md) – Learn how to use important tools for managing your cluster\.