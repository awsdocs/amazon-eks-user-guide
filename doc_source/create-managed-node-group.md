# Creating a managed node group<a name="create-managed-node-group"></a>

This topic describes how you can launch an Amazon EKS managed node group of Linux nodes that register with your Amazon EKS cluster\. After the nodes join the cluster, you can deploy Kubernetes applications to them\.

If this is your first time launching an Amazon EKS managed node group, we recommend that you follow one of our [Getting started with Amazon EKS](getting-started.md) guides instead\. The guides provide walkthroughs for creating an Amazon EKS cluster with nodes\.

**Important**  
Amazon EKS nodes are standard Amazon EC2 instances\. You're billed based on the normal Amazon EC2 prices\. For more information, see [Amazon EC2 Pricing](https://aws.amazon.com/ec2/pricing/)\.
You can't create managed nodes in an AWS Region where you have AWS Outposts, AWS Wavelength, or AWS Local Zones enabled\. You can create self\-managed nodes in an AWS Region where you have AWS Outposts, or AWS Wavelength, or AWS Local Zones enabled\. For more information, see [Launching self\-managed Amazon Linux nodes](launch-workers.md), or[Launching self\-managed Windows nodes](launch-windows-workers.md), and [Launching self\-managed Bottlerocket nodes](launch-node-bottlerocket.md)\.

**Prerequisite**  
An existing cluster\. If you don't have an existing cluster, we recommend that you follow one of the [Getting started with Amazon EKS](getting-started.md) guides to create your cluster and node group\.

You can create a managed node group with `eksctl` or the AWS Management Console\.

------
#### [ eksctl ]<a name="create-managed-node-group-eksctl"></a>

**To create a managed node group with `eksctl`**

This procedure requires `eksctl` version `0.63.0` or later\. You can check your version with the following command:

```
eksctl version
```

For more information on installing or upgrading `eksctl`, see [Installing or upgrading `eksctl`](eksctl.md#installing-eksctl)\.

You can create your node group with or without a launch template\. A launch template allows for greater customization of a node group, to include deploying a custom AMI\. If you plan to use [Security groups for pods](security-groups-for-pods.md), then make sure to specify a supported Amazon EC2 instance type\. For more information, see [Amazon EC2 supported instances and branch network interfaces](security-groups-for-pods.md#supported-instance-types)\. If specifying an Arm Amazon EC2 instance type, then review the considerations in [Amazon EKS optimized Arm Amazon Linux AMIs](eks-optimized-ami.md#arm-ami) before deploying\.

1. \(Optional\) If the **AmazonEKS\_CNI\_Policy** managed IAM policy is attached to your [Amazon EKS node IAM role](create-node-role.md), we recommend assigning it to an IAM role that you associate to the Kubernetes `aws-node` service account instead\. For more information, see [Configuring the Amazon VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.

1. Create your managed node group with or without using a custom launch template\. For a complete list of all available options and defaults, enter the following command\.

   ```
   eksctl create nodegroup --help
   ```

   Replace the *`<example values>`* \(including the *`<>`*\) with your own values\. 
   + **Without a launch template** – `eksctl` creates a default Amazon EC2 launch template in your account and deploys the node group using a launch template that it creates based on options that you specify\. For a complete list of supported values for `--node-type`, see the list in `[amazon\-eks\-nodegroup\.yaml](https://github.com/awslabs/amazon-eks-ami/blob/master/amazon-eks-nodegroup.yaml)` on GitHub\. Replace `<my-key>` with the name of your Amazon EC2 key pair or public key\. This key is used to SSH into your nodes after they launch\. If you don't already have an Amazon EC2 key pair, you can create one in the AWS Management Console\. For more information, see [Amazon EC2 key pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) in the *Amazon EC2 User Guide for Linux Instances*\.

     If you plan to assign IAM roles to all of your Kubernetes service accounts so that pods only have the minimum permissions that they need, and no pods in the cluster require access to the Amazon EC2 instance metadata service \(IMDS\) for other reasons, such as retrieving the current Region, then we recommend blocking pod access to IMDS\. For more information, see [IAM roles for service accounts](iam-roles-for-service-accounts.md) and [Restricting access to the IMDS and Amazon EC2 instance profile credentials](best-practices-security.md#restrict-ec2-credential-access)\. If you want to block pod access to IMDS, then add the `--disable-pod-imds` option to the following command\.

     ```
     eksctl create nodegroup \
       --cluster <my-cluster> \
       --region <region-code> \
       --name <my-mng> \
       --node-type <m5.large> \
       --nodes <3> \
       --nodes-min <2> \
       --nodes-max <4> \
       --ssh-access \
       --ssh-public-key <my-key> \
       --managed
     ```

     Your instances can optionally assign a significantly higher number of IP addresses to pods, assign IP addresses to pods from a different CIDR block than the instance's, and be deployed to a cluster without internet access\. For more information, see [Increase the amount of available IP addresses for your Amazon EC2 nodes](cni-increase-ip-addresses.md), [CNI custom networking](cni-custom-network.md), and [Private clusters](private-clusters.md) for additional options to add to the previous command\.
   + **With a launch template** – The launch template must already exist and must meet the requirements specified in [Launch template configuration basics](launch-templates.md#launch-template-basics)\. If you plan to assign IAM roles to all of your Kubernetes service accounts so that pods only have the minimum permissions that they need, and no pods in the cluster require access to the Amazon EC2 instance metadata service \(IMDS\) for other reasons, such as retrieving the current Region, then we recommend blocking pod access to IMDS\. For more information, see [IAM roles for service accounts](iam-roles-for-service-accounts.md) and [Restricting access to the IMDS and Amazon EC2 instance profile credentials](best-practices-security.md#restrict-ec2-credential-access)\. If you want to block pod access to IMDS, then specify the necessary settings in the launch template\.

     1. Create a file named *`eks-nodegroup.yaml`* with the following contents\. Several settings that you specify when deploying without a launch template are moved into the launch template\. If you don't specify a `version`, the template's default version is used\.

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

        For a complete list of `eksctl` config file settings, see [Config file schema](https://eksctl.io/usage/schema/) in the `eksctl` documentation\. Your instances can optionally assign a significantly higher number of IP addresses to pods, assign IP addresses to pods from a different CIDR block than the instance's, use the `containerd` runtime, and be deployed to a cluster without outbound internet access\. For more information, see [Increase the amount of available IP addresses for your Amazon EC2 nodes](cni-increase-ip-addresses.md), [CNI custom networking](cni-custom-network.md), [Enable the `containerd` runtime bootstrap flag](eks-optimized-ami.md#containerd-bootstrap), and [Private clusters](private-clusters.md) for additional options to add to the config file\.

     1. Deploy the nodegroup with the following command\.

        ```
        eksctl create nodegroup --config-file eks-nodegroup.yaml
        ```

------
#### [ AWS Management Console ]<a name="launch-managed-node-group-console"></a>

**To create your managed node group using the AWS Management Console**

1. Wait for your cluster status to show as `ACTIVE`\. You cannot create a managed node group for a cluster that is not yet `ACTIVE`\.

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the name of the cluster that you want to create your managed node group in\.

1. Select the **Configuration** tab\.

1. On the **Configuration** tab, select the **Compute** tab, and then choose **Add Node Group**\.

1. On the **Configure node group** page, fill out the parameters accordingly, and then choose **Next**\.
   + **Name** – Enter a unique name for your managed node group\.
   + **Node IAM role name** – Choose the node instance role to use with your node group\. For more information, see [Amazon EKS node IAM role](create-node-role.md)\.
**Important**  
We recommend using a role that is not currently in use by any self\-managed node group, or that you plan to use with a new self\-managed node group\. For more information, see [Deleting a managed node group](delete-managed-node-group.md)\.
   + **Use launch template** – \(Optional\) Choose if you want to use an existing launch template and then select a **Launch template version** \(Optional\)\. If you don't select a version, then Amazon EKS uses the template's default version\. Launch templates allow for more customization of your node group, including allowing you to deploy a custom AMI, assign a significantly higher number of IP addresses to pods, assign IP addresses to pods from a different CIDR block than the instance's, enable the `containerd` runtime for your instances, and deploying nodes to a cluster without outbound internet access\. For more information, see [Increase the amount of available IP addresses for your Amazon EC2 nodes](cni-increase-ip-addresses.md), [CNI custom networking](cni-custom-network.md), [Enable the `containerd` runtime bootstrap flag](eks-optimized-ami.md#containerd-bootstrap), and [Private clusters](private-clusters.md)\. 

     The launch template must meet the requirements in [Launch template support](launch-templates.md)\. If you don't use your own launch template, the Amazon EKS API creates a default Amazon EC2 launch template in your account and deploys the node group using the default launch template\. 

     If you implement [IAM roles for service accounts](iam-roles-for-service-accounts.md), assign necessary permissions directly to all pods that require access to AWS services, and no pods in your cluster require access to IMDS for other reasons, such as retrieving the current Region, then you can also disable access to IMDS for pods that don't use host networking in a launch template\. For more information, see [Restricting access to the IMDS and Amazon EC2 instance profile credentials](best-practices-security.md#restrict-ec2-credential-access)\.
   + **Kubernetes labels** – \(Optional\) You can choose to apply Kubernetes labels to the nodes in your managed node group\.
   + **Kubernetes taints** – \(Optional\) You can choose to apply Kubernetes taints with the effect of either `No_Schedule`, `Prefer_No_Schedule`, or `No_Execute` to the nodes in your managed node group\.
   + **Tags** – \(Optional\) You can choose to tag your Amazon EKS managed node group\. These tags do not propagate to other resources in the node group, such as Auto Scaling groups or instances\. For more information, see [Tagging your Amazon EKS resources](eks-using-tags.md)\.
   + **Node group update configuration** – \(Optional\) You can select the number or percentage of nodes to be updated in parallel\. Select either **Number** or **Percentage** to enter a value\. These nodes will not be available during the update\. 

1. On the **Set compute and scaling configuration** page, fill out the parameters accordingly, and then choose **Next**\.
   + **AMI type** – Choose **Amazon Linux 2 \(AL2\_x86\_64\)** for non\-GPU instances, **Amazon Linux 2 GPU Enabled \(AL2\_x86\_64\_GPU\)** for GPU instances, or** Amazon Linux 2 \(AL2\_ARM\_64\)** for Arm\.

     If you are deploying Arm instances, be sure to review the considerations in [Amazon EKS optimized Arm Amazon Linux AMIs](eks-optimized-ami.md#arm-ami) before deploying\.

     If you specified a launch template on the previous page, and specified an AMI in the launch template, then you cannot select a value\. The value from the template is displayed\. The AMI specified in the template must meet the requirements in [Specifying an AMI](launch-templates.md#launch-template-custom-ami)\.
   + **Capacity type** – Select a capacity type\. For more information about choosing a capacity type, see [Managed node group capacity types](managed-node-groups.md#managed-node-group-capacity-types)\. You cannot mix different capacity types within the same node group\. If you want to use both capacity types, create separate node groups, each with their own capacity and instance types\.
   + **Instance type** – One or more instance type is specified by default\. To remove a default instance type, select the `X` on the right side of the instance type\. Choose the instance types to use in your managed node group\. The console displays a set of commonly used instance types\. For the complete set of supported instance types, see the list in `[amazon\-eks\-nodegroup\.yaml](https://github.com/awslabs/amazon-eks-ami/blob/master/amazon-eks-nodegroup.yaml)` on GitHub\. If you need to create a managed node group with an instance type that is not displayed, then use `eksctl`, the AWS CLI, AWS CloudFormation, or an SDK to create the node group\. If you specified a launch template on the previous page, then you cannot select a value because it must be specified in the launch template\. The value from the launch template is displayed\. If you selected **Spot** for **Capacity type**, then we recommend specifying multiple instance types to enhance availability\. For more information about selecting instance types, see **Considerations** in [Managed node group capacity types](managed-node-groups.md#managed-node-group-capacity-types)\.

     Each Amazon EC2 instance type supports a maximum number of elastic network interfaces \(ENIs\) and each ENI supports a maximum number of IP addresses\. Since each worker node and pod is assigned its own IP address it's important to choose an instance type that will support the maximum number of pods that you want to run on each worker node\. For a list of the number of ENIs and IP addresses supported by instance types, see [ IP addresses per network interface per instance type](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#AvailableIpPerENI)\. For example, the `m5.large` instance type supports a maximum of 30 IP addresses for the worker node and pods\. Some instance types might not be available in all Regions\.

     If you plan to use [Security groups for pods](security-groups-for-pods.md), then make sure to specify a supported Amazon EC2 instance type\. For more information, see [Amazon EC2 supported instances and branch network interfaces](security-groups-for-pods.md#supported-instance-types)\. If specifying an Arm Amazon EC2 instance type, then review the considerations in [Amazon EKS optimized Arm Amazon Linux AMIs](eks-optimized-ami.md#arm-ami) before deploying\.
   + **Disk size** – Enter the disk size \(in GiB\) to use for your node's root volume\.

     If you specified a launch template on the previous page, then you cannot select a value because it must be specified in the launch template\.
   + **Minimum size** – Specify the minimum number of nodes that the managed node group can scale in to\.
   + **Maximum size** – Specify the maximum number of nodes that the managed node group can scale out to\.
   + **Desired size** – Specify the current number of nodes that the managed node group should maintain at launch\.
**Note**  
Amazon EKS does not automatically scale your node group in or out\. However, you can configure the Kubernetes [Cluster Autoscaler](cluster-autoscaler.md) to do this for you\.
   + For **Maximum unavailable**, select one of the following options and specify a **Value**: 
     + **Number** – Select and specify the number of nodes in your nodegroup that can be updated in parallel\. These nodes will be unavailable during update\.
     + **Percentage** – Select and specify the percentage of nodes in your nodegroup that can be updated in parallel\. These nodes will be unavailable during update\. This is useful if you have a large number of nodes in your node group\.

1. On the **Specify networking** page, fill out the parameters accordingly, and then choose **Next**\.
   + **Subnets** – Choose the subnets to launch your managed nodes into\. 
**Important**  
If you are running a stateful application across multiple Availability Zones that is backed by Amazon EBS volumes and using the Kubernetes [Cluster Autoscaler](cluster-autoscaler.md), you should configure multiple node groups, each scoped to a single Availability Zone\. In addition, you should enable the `--balance-similar-node-groups` feature\.
**Important**  
If you choose a public subnet, and your cluster has only the public API server endpoint enabled, then the subnet must have `MapPublicIPOnLaunch` set to `true` for the instances to successfully join a cluster\. If the subnet was created using `eksctl` or the [Amazon EKS vended AWS CloudFormation templates](create-public-private-vpc.md) on or after March 26, 2020, then this setting is already set to `true`\. If the subnets were created with `eksctl` or the AWS CloudFormation templates before March 26, 2020, then you need to change the setting manually\. For more information, see [Modifying the public IPv4 addressing attribute for your subnet](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#subnet-public-ip)\.
If you use a launch template and specify multiple network interfaces, Amazon EC2 will not auto\-assign a public IPv4 address, even if `MapPublicIpOnLaunch` is set to `true`\. For nodes to join the cluster in this scenario, you must either enable the cluster's private API server endpoint, or launch nodes in a private subnet with outbound internet access provided through an alternative method, such as a NAT Gateway\. For more information, see [Amazon EC2 instance IP addressing](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-instance-addressing.html) in the Amazon EC2 User Guide for Linux Instances\.
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
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.8.0/nvidia-device-plugin.yml
   ```

1. \(Optional\) After you add Linux worker nodes to your cluster, follow the procedures in [Windows support](windows-support.md) to add Windows support to your cluster and to add Windows worker nodes\. All Amazon EKS clusters must contain at least one Linux worker node, even if you only want to run Windows workloads in your cluster\.

------

Now that you have a working Amazon EKS cluster with nodes, you're ready to start installing Kubernetes add\-ons and deploying applications to your cluster\. The following documentation topics help you to extend the functionality of your cluster\.
+ The IAM entity \(user or role\) that created the cluster is added to the Kubernetes RBAC authorization table as the administrator \(with `system:masters` permissions\)\. Initially, only that IAM user can make calls to the Kubernetes API server using `kubectl`\. If you want other users to have access to your cluster, then you must add them to the `aws-auth` `ConfigMap`\. For more information, see [Managing users or IAM roles for your cluster](add-user-role.md)\.
+ [Restrict access to IMDS](best-practices-security.md#restrict-ec2-credential-access) – If you plan to assign IAM roles to all of your Kubernetes service accounts so that pods only have the minimum permissions that they need, and no pods in the cluster require access to the Amazon EC2 instance metadata service \(IMDS\) for other reasons, such as retrieving the current Region, then we recommend blocking pod access to IMDS\. For more information, see [IAM roles for service accounts](iam-roles-for-service-accounts.md) and [Restricting access to the IMDS and Amazon EC2 instance profile credentials](best-practices-security.md#restrict-ec2-credential-access)\. 
+ [Cluster Autoscaler](cluster-autoscaler.md) – Configure the Kubernetes Cluster Autoscaler to automatically adjust the number of nodes in your node groups\.
+ [Deploy a sample Linux workload](sample-deployment.md) – Deploy a sample Linux application to test your cluster and Linux nodes\.
+ [Cluster management](eks-managing.md) – Learn how to use important tools for managing your cluster\.