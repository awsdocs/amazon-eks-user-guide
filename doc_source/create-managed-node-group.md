# Creating a managed node group<a name="create-managed-node-group"></a>

This topic helps you to launch an Amazon EKS managed node group of Linux nodes that register with your Amazon EKS cluster\. After the nodes join the cluster, you can deploy Kubernetes applications to them\.

[Managed node groups](managed-node-groups.md) are supported on Amazon EKS clusters beginning with Kubernetes version 1\.14 and [platform version](platform-versions.md) `eks.3`\. Existing clusters can update to version 1\.14 or later to take advantage of this feature\. For more information, see [Updating an Amazon EKS cluster Kubernetes version](update-cluster.md)\.

If this is your first time launching an Amazon EKS managed node group, we recommend that you follow one of our [Getting started with Amazon EKS](getting-started.md) guides instead\. The guides provide complete end\-to\-end walkthroughs for creating an Amazon EKS cluster with nodes\.

**Important**  
Amazon EKS nodes are standard Amazon EC2 instances, and you are billed for them based on normal Amazon EC2 prices\. For more information, see [Amazon EC2 Pricing](https://aws.amazon.com/ec2/pricing/)\.

You can create a managed node group with [`eksctl`](#create-managed-node-group-eksctl) or the [AWS Management Console](#launch-managed-node-group-console2)\.<a name="create-managed-node-group-eksctl"></a>

**To create a managed node group with `eksctl`**

This procedure requires `eksctl` version `0.30.0` or later\. You can check your version with the following command:

```
eksctl version
```

For more information on installing or upgrading `eksctl`, see [Installing or upgrading `eksctl`](eksctl.md#installing-eksctl)\.

Do not use `eksctl` to create a cluster or nodes in an AWS Region where you have AWS Outposts, AWS Wavelength, or AWS Local Zones enabled\. Create a cluster and self\-managed nodes using the Amazon EC2 API or AWS CloudFormation instead\. For more information, see [To launch self\-managed nodes using the AWS Management Console](launch-workers.md#launch-al-nodes-console) and [To launch self\-managed Windows nodes using the AWS Management Console](launch-windows-workers.md#launch-windows-nodes-console)\.

You can create your node group with or without a launch template\. A launch template allows for greater customization of a node group, to include deploying a custom AMI\. Complete one of the following steps\. If you plan to use [Security groups for pods](security-groups-for-pods.md), then make sure to specify a supported Amazon EC2 instance type\. For more information, see [Amazon EC2 supported instances and branch network interfaces](security-groups-for-pods.md#supported-instance-types)\. If specifying an Arm Amazon EC2 instance type, then review the considerations in [Amazon EKS optimized Arm Amazon Linux AMIs](eks-optimized-ami.md#arm-ami) before deploying\.

1. Create your managed node group **without** a launch template with the following `eksctl` command, replacing the `<example values>` \(including the `<>`\) with your own values\. When you don't specify your own launch template, the Amazon EKS API creates a default Amazon EC2 launch template in your account and deploys the node group using the default launch template\.

   ```
   eksctl create nodegroup \
     --cluster <my-cluster> \
     --region <us-west-2> \
     --name <my-mng> \
     --node-type <m5.large> \
     --nodes <3> \
     --nodes-min <2> \
     --nodes-max <4> \
     --ssh-access \
     --ssh-public-key <my-public-key.pub> \
     --managed
   ```

1. Create your managed node group **with** a launch template\. The launch template must already exist and must meet the requirements specified in [Launch template configuration basics](launch-templates.md#launch-template-basics)\.

   1. Create a file named `<node-group-lt.yaml>` with the following contents, replacing the `<example values>` \(including the `<>`\) with your own values\. Several settings that you specify when deploying without a launch template are moved into the launch template\. If you don't specify a `version`, the template's default version is used\.

      ```
      apiVersion: eksctl.io/v1alpha5
      kind: ClusterConfig
      metadata:
        name: <my-cluster>
        region: <region-code>
      managedNodeGroups:
      - name: <node-group-lt>
        launchTemplate:
          id: lt-<id>
          version: "<1>"
      ```

   1. Deploy the nodegroup with the following command\.

      ```
      eksctl create nodegroup --config-file node-group-lt.yaml
      ```<a name="launch-managed-node-group-console2"></a>

**To create your managed node group using the AWS Management Console**

1. Wait for your cluster status to show as `ACTIVE`\. You cannot create a managed node group for a cluster that is not yet `ACTIVE`\.

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the name of the cluster that you want to create your managed node group in\.

1. On the cluster page, select the **Compute** tab, and then choose **Add Node Group**\.

1. On the **Configure node group** page, fill out the parameters accordingly, and then choose **Next**\.
   + **Name** – Enter a unique name for your managed node group\.
   + **Node IAM role name** – Choose the node instance role to use with your node group\. For more information, see [Amazon EKS node IAM role](create-node-role.md)\.
**Important**  
We recommend using a role that is not currently in use by any self\-managed node group, or that you plan to use with a new self\-managed node group\. For more information, see [Deleting a managed node group](delete-managed-node-group.md)\.
   + **Use launch template** – \(Optional\) Choose if you want to use an existing launch template and then select a **Launch template version** \(Optional\)\. If you don't select a version, then Amazon EKS uses the template's default version\. Launch templates allow for more customization of your node group, including allowing you to deploy a custom AMI\. The launch template must meet the requirements in [Launch template support](launch-templates.md)\. If you don't use your own launch template, the Amazon EKS API creates a default Amazon EC2 launch template in your account and deploys the node group using the default launch template\.
   + **Kubernetes labels** – \(Optional\) You can choose to apply Kubernetes labels to the nodes in your managed node group\.
   + **Tags** – \(Optional\) You can choose to tag your Amazon EKS managed node group\. These tags do not propagate to other resources in the node group, such as Auto Scaling groups or instances\. For more information, see [Tagging your Amazon EKS resources](eks-using-tags.md)\.

1. On the **Set compute and scaling configuration** page, fill out the parameters accordingly, and then choose **Next**\.

**Node group compute configuration**
   + **AMI type** – Choose **Amazon Linux 2 \(AL2\_x86\_64\)** for non\-GPU instances, **Amazon Linux 2 GPU Enabled \(AL2\_x86\_64\_GPU\)** for GPU instances, or** Amazon Linux 2 \(AL2\_ARM\_64\)** for Arm\.

     If you are deploying Arm instances, be sure to review the considerations in [Amazon EKS optimized Arm Amazon Linux AMIs](eks-optimized-ami.md#arm-ami) before deploying\.

     If you specified a launch template on the previous page, and specified an AMI in the launch template, then you cannot select a value\. The value from the template is displayed\. The AMI specified in the template must meet the requirements in [Using a custom AMI](launch-templates.md#launch-template-custom-ami)\.
   + **Instance type** – Choose the instance type to use in your managed node group\. The console displays a set of commonly used instance types\. If you need to create a managed node group with an instance type that is not displayed, then use `eksctl`, the AWS CLI, AWS CloudFormation, or an SDK to create the node group\. If you specified a launch template on the previous page, then you cannot select a value because it must be specified in the launch template\. The value from the launch template is displayed\.

     Each Amazon EC2 instance type supports a maximum number of elastic network interfaces \(ENIs\) and each ENI supports a maximum number of IP addresses\. Since each worker node and pod is assigned its own IP address it's important to choose an instance type that will support the maximum number of pods that you want to run on each worker node\. For a list of the number of ENIs and IP addresses supported by instance types, see [ IP addresses per network interface per instance type](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#AvailableIpPerENI)\. For example, the `m5.large` instance type supports a maximum of 30 IP addresses for the worker node and pods\. Some instance types might not be available in all Regions\.

     If you plan to use [Security groups for pods](security-groups-for-pods.md), then make sure to specify a supported Amazon EC2 instance type\. For more information, see [Amazon EC2 supported instances and branch network interfaces](security-groups-for-pods.md#supported-instance-types)\. If specifying an Arm Amazon EC2 instance type, then review the considerations in [Amazon EKS optimized Arm Amazon Linux AMIs](eks-optimized-ami.md#arm-ami) before deploying\.
   + **Disk size** – Enter the disk size \(in GiB\) to use for your node's root volume\.

     If you specified a launch template on the previous page, then you cannot select a value because it must be specified in the launch template\.

**Node group scaling configuration**
**Note**  
Amazon EKS does not automatically scale your node group in or out\. However, you can configure the Kubernetes [Cluster Autoscaler](cluster-autoscaler.md) to do this for you\.
   + **Minimum size** – Specify the minimum number of nodes that the managed node group can scale in to\.
   + **Maximum size** – Specify the maximum number of nodes that the managed node group can scale out to\.
   + **Desired size** – Specify the current number of nodes that the managed node group should maintain at launch\.

1. On the **Specify networking** page, fill out the parameters accordingly, and then choose **Next**\.
   + **Subnets** – Choose the subnets to launch your managed nodes into\. 
**Important**  
If you are running a stateful application across multiple Availability Zones that is backed by Amazon EBS volumes and using the Kubernetes [Cluster Autoscaler](cluster-autoscaler.md), you should configure multiple node groups, each scoped to a single Availability Zone\. In addition, you should enable the `--balance-similar-node-groups` feature\.
**Important**  
If you choose a public subnet, then the subnet must have `MapPublicIpOnLaunch` set to true for the instances to be able to successfully join a cluster\. If the subnet was created using `eksctl` or the [Amazon EKS vended AWS CloudFormation templates](create-public-private-vpc.md) on or after March 26, 2020, then this setting is already set to true\. If the subnets were created with `eksctl` or the AWS CloudFormation templates before March 26, 2020, then you need to change the setting manually\. For more information, see [Modifying the public IPv4 addressing attribute for your subnet](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#subnet-public-ip)\.
Do not select a subnet in AWS Outposts, AWS Wavelength, or an AWS Local Zone\. You can't deploy managed nodes to a subnet in AWS Outposts, AWS Wavelength, or an AWS Local Zone\. You can only deploy [self\-managed nodes](worker.md) to AWS Outposts, AWS Wavelength, or AWS Local Zone subnets\.
   + **Allow remote access to nodes** \(Optional, but default\)\. Enabling SSH allows you to connect to your instances and gather diagnostic information if there are issues\. Complete the following steps to enable remote access\. We highly recommend enabling remote access when you create your node group\. You cannot enable remote access after the node group is created\.

     If you chose to use a launch template, then this option isn't shown\. To enable remote access to your nodes, specify a key pair in the launch template and ensure that the proper port is open to the nodes in the security groups that you specify in the launch template\. For more information, see [Using custom security groups](launch-templates.md#launch-template-security-groups)\.
   + For **SSH key pair** \(Optional\), choose an Amazon EC2 SSH key to use\. For more information, see [Amazon EC2 key pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) in the Amazon EC2 User Guide for Linux Instances\. If you chose to use a launch template, then you can't select one\.
   + For **Allow remote access from**, if you want to limit access to specific instances, then select the security groups that are associated to those instances\. If you don't select specific security groups, then SSH access is allowed from anywhere on the internet \(0\.0\.0\.0/0\)\.

1. On the **Review and create** page, review your managed node group configuration and choose **Create**\.

   If nodes fail to join the cluster, then see [Nodes fail to join cluster](troubleshooting.md#worker-node-fail) in the Troubleshooting guide\.

1. Watch the status of your nodes and wait for them to reach the `Ready` status\.

   ```
   kubectl get nodes --watch
   ```

1. \(GPU nodes only\) If you chose a GPU instance type and the Amazon EKS optimized accelerated AMI, then you must apply the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) as a DaemonSet on your cluster with the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.6.0/nvidia-device-plugin.yml
   ```

1. \(Optional\) [Deploy a sample Linux application](sample-deployment.md) – Deploy a sample application to test your cluster and Linux nodes\.

1. \(Optional\) After you add Linux worker nodes to your cluster, follow the procedures in [Windows support](windows-support.md) to add Windows support to your cluster and to add Windows worker nodes\. All Amazon EKS clusters must contain at least one Linux worker node, even if you only want to run Windows workloads in your cluster\.

Now that you have a working Amazon EKS cluster with nodes, you are ready to start installing Kubernetes add\-ons and deploying applications to your cluster\. The following documentation topics help you to extend the functionality of your cluster\.
+ [Cluster Autoscaler](cluster-autoscaler.md) – Configure the Kubernetes Cluster Autoscaler to automatically adjust the number of nodes in your node groups\.
+ [Deploy a sample Linux application](sample-deployment.md) – Deploy a sample application to test your cluster and Linux nodes\.
+ [Deploy a Windows sample application](windows-support.md#windows-sample-application) – Deploy a sample application to test your cluster and Windows nodes\.
+ [Cluster management](eks-managing.md) – Learn how to use important tools for managing your cluster\.