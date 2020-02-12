# Creating a Managed Node Group<a name="create-managed-node-group"></a>

This topic helps you to launch an Amazon EKS managed node group of Linux worker nodes that register with your Amazon EKS cluster\. After the nodes join the cluster, you can deploy Kubernetes applications to them\.

[Managed Node Groups](managed-node-groups.md) are supported on Amazon EKS clusters beginning with Kubernetes version 1\.14 and [platform version](platform-versions.md) `eks.3`\. Existing clusters can update to version 1\.14 to take advantage of this feature\. For more information, see [Updating an Amazon EKS Cluster Kubernetes Version](update-cluster.md)\. Existing 1\.14 clusters will be automatically updated to `eks.3` over time to support this feature\.

If this is your first time launching an Amazon EKS managed node group, we recommend that you follow one of our [Getting Started with Amazon EKS](getting-started.md) guides instead\. The guides provide complete end\-to\-end walkthroughs for creating an Amazon EKS cluster with worker nodes\.

**Important**  
Amazon EKS worker nodes are standard Amazon EC2 instances, and you are billed for them based on normal Amazon EC2 prices\. For more information, see [Amazon EC2 Pricing](https://aws.amazon.com/ec2/pricing/)\.

**To launch your managed node group**

1. Wait for your cluster status to show as `ACTIVE`\. You cannot create a managed node group for a cluster that is not yet `ACTIVE`\.

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the name of the cluster that you want to create your managed node group in\.

1. On the cluster page, choose **Add node group**\.

1. On the **Configure node group** page, fill out the parameters accordingly, and then choose **Next**\.
   + **Name** — Enter a unique name for your managed node group\.
   + **Node IAM role name** — Choose the node instance role to use with your node group\. For more information, see [Amazon EKS Worker Node IAM Role](worker_node_IAM_role.md)\.
**Important**  
We recommend using a role that is not currently in use by any self\-managed node group, or that you plan to use with a new self\-managed node group\. For more information, see [Deleting a Managed Node Group](delete-managed-node-group.md)\.
   + **Subnets** — Choose the subnets to launch your managed nodes into\. 
**Important**  
If you are running a stateful application across multiple Availability Zones that is backed by Amazon EBS volumes and using the Kubernetes [Cluster Autoscaler](cluster-autoscaler.md), you should configure multiple node groups, each scoped to a single Availability Zone\. In addition, you should enable the `--balance-similar-node-groups` feature\.
   + **Remote Access** — \(Optional\) You can enable SSH access to the nodes in your managed node group\. Enabling SSH allows you to connect to your instances and gather diagnostic information if there are issues\. Complete the following steps to enable remote access\.
**Note**  
We highly recommend enabling remote access when you create your node group\. You cannot enable remote access after the node group is created\.

     1. Select the check box to **Allow remote access to nodes**\.

     1. For **SSH key pair**, choose an Amazon EC2 SSH key to use\. For more information, see [Amazon EC2 Key Pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) in the Amazon EC2 User Guide for Linux Instances\.

     1. For **Allow remote access from**, choose **All** to allow SSH access from anywhere on the Internet \(0\.0\.0\.0/0\), or select a security group to allow SSH access from instances that belong to that security group\.
   + **Tags** — \(Optional\) You can choose to tag your Amazon EKS managed node group\. These tags do not propagate to other resources in the node group, such as Auto Scaling groups or instances\. For more information, see [Tagging Your Amazon EKS Resources](eks-using-tags.md)\.
   + **Kubernetes labels** — \(Optional\) You can choose to apply Kubernetes labels to the nodes in your managed node group\.

1. On the **Set compute configuration** page, fill out the parameters accordingly, and then choose **Next**\.
   + **AMI type** — Choose **Amazon Linux 2 \(AL2\_x86\_64\)** for non\-GPU instances, or **Amazon Linux 2 GPU Enabled \(AL2\_x86\_64\_GPU\)** for GPU instances\.
   + **Instance type** — Choose the instance type to use in your managed node group\. Larger instance types can accommodate more pods\.
   + **Disk size** — Enter the disk size \(in GiB\) to use for your worker node root volume\.

1. On the **Setup scaling policies** page, fill out the parameters accordingly, and then choose **Next**\.
**Note**  
Amazon EKS does not automatically scale your node group in or out\. However, you can configure the Kubernetes [Cluster Autoscaler](cluster-autoscaler.md) to do this for you\.
   + **Minimum size** — Specify the minimum number of worker nodes that the managed node group can scale in to\.
   + **Maximum size** — Specify the maximum number of worker nodes that the managed node group can scale out to\.
   + **Desired size** — Specify the current number of worker nodes that the managed node group should maintain at launch\.

1. On the **Review and create** page, review your managed node group configuration and choose **Create**\.

1. Watch the status of your nodes and wait for them to reach the `Ready` status\.

   ```
   kubectl get nodes --watch
   ```

1. \(GPU workers only\) If you chose a GPU instance type and the Amazon EKS\-optimized AMI with GPU support, you must apply the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) as a DaemonSet on your cluster with the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/1.0.0-beta/nvidia-device-plugin.yml
   ```

Now that you have a working Amazon EKS cluster with worker nodes, you are ready to start installing Kubernetes add\-ons and deploying applications to your cluster\. The following documentation topics help you to extend the functionality of your cluster\.
+ [Cluster Autoscaler](cluster-autoscaler.md) — Configure the Kubernetes [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler) to automatically adjust the number of nodes in your node groups\.
+ [Launch a Guest Book Application](eks-guestbook.md) — Create a sample guest book application to test your cluster and Linux worker nodes\.
+ [Deploy a Windows Sample Application](windows-support.md#windows-sample-application) — Deploy a sample application to test your cluster and Windows worker nodes\.
+ [Tutorial: Deploy the Kubernetes Web UI \(Dashboard\)](dashboard-tutorial.md) — This tutorial guides you through deploying the [Kubernetes dashboard](https://github.com/kubernetes/dashboard) to your cluster\.
+ [Using Helm with Amazon EKS](helm.md) — The `helm` package manager for Kubernetes helps you install and manage applications on your cluster\. 
+ [Installing the Kubernetes Metrics Server](metrics-server.md) — The Kubernetes metrics server is an aggregator of resource usage data in your cluster\.
+ [Control Plane Metrics with Prometheus](prometheus.md) — This topic helps you deploy Prometheus into your cluster with `helm`\.