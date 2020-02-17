# Getting Started with the AWS Management Console<a name="getting-started-console"></a>

This getting started guide helps you to create all of the required resources to get started with Amazon EKS in the AWS Management Console\. In this guide, you manually create each resource in the Amazon EKS or AWS CloudFormation consoles, and the workflow described here gives you complete visibility into how each resource is created and how they interact with each other\.

You can also choose to use the `eksctl` CLI to create your cluster and worker nodes\. For more information, see [Getting Started with `eksctl`](getting-started-eksctl.md)\.

## Amazon EKS Prerequisites<a name="eks-prereqs"></a>

Before you can create an Amazon EKS cluster, you must create an IAM role that Kubernetes can assume to create AWS resources\. For example, when a load balancer is created, Kubernetes assumes the role to create an Elastic Load Balancing load balancer in your account\. This only needs to be done one time and can be used for multiple EKS clusters\.

You must also create a VPC and a security group for your cluster to use\. Although the VPC and security groups can be used for multiple EKS clusters, we recommend that you use a separate VPC for each EKS cluster to provide better network isolation\.

This section also helps you to install the kubectl binary and configure it to work with Amazon EKS\.

### Create your Amazon EKS Service Role<a name="role-create"></a>

You can create the role using the AWS Management Console or AWS CloudFormation\. Select the tab with the name of the tool that you'd like to use to create the role\.

------
#### [ AWS Management Console ]

**To create your Amazon EKS service role in the IAM console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. Choose **Roles**, then **Create role**\.

1. Choose **EKS** from the list of services, then **EKS** for your use case, and then **Next: Permissions**\.

1. Choose **Next: Tags**\.

1. \(Optional\) Add metadata to the role by attaching tags as key–value pairs\. For more information about using tags in IAM, see [Tagging IAM Entities](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html) in the *IAM User Guide*\. 

1. Choose **Next: Review**\.

1. For **Role name**, enter a unique name for your role, such as `eksServiceRole`, then choose **Create role**\.

------
#### [ AWS CloudFormation ]

**To create your Amazon EKS service role with AWS CloudFormation**

1. Save the following AWS CloudFormation template to a text file on your local system\.

   ```
   ---
   AWSTemplateFormatVersion: '2010-09-09'
   Description: 'Amazon EKS Service Role'
   
   
   Resources:
   
     eksServiceRole:
       Type: AWS::IAM::Role
       Properties:
         AssumeRolePolicyDocument:
           Version: '2012-10-17'
           Statement:
           - Effect: Allow
             Principal:
               Service:
               - eks.amazonaws.com
             Action:
             - sts:AssumeRole
         ManagedPolicyArns:
           - arn:aws:iam::aws:policy/AmazonEKSServicePolicy
           - arn:aws:iam::aws:policy/AmazonEKSClusterPolicy
   
   Outputs:
   
     RoleArn:
       Description: The role that Amazon EKS will use to create AWS resources for Kubernetes clusters
       Value: !GetAtt eksServiceRole.Arn
       Export:
         Name: !Sub "${AWS::StackName}-RoleArn"
   ```

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. Choose **Create stack**\.

1. For **Specify template**, select **Upload a template file**, and then choose **Choose file**\.

1. Choose the file you created earlier, and then choose **Next**\.

1. For **Stack name**, enter a name for your role, such as `eksServiceRole`, and then choose **Next**\.

1. On the **Configure stack options** page, choose **Next**\.

1. On the **Review** page, review your information, acknowledge that the stack might create IAM resources, and then choose **Create stack**\.

------

### Create your Amazon EKS Cluster VPC<a name="vpc-create"></a>

This section guides you through creating a VPC for your cluster with either 3 public subnets, or two public subnets and two private subnets, which are provided with internet access through a NAT gateway\. We recommend a network architecture that uses private subnets for your worker nodes, and public subnets for Kubernetes to create public load balancers within\.

Choose the tab below that represents your desired VPC configuration\.

------
#### [ Only public subnets ]

**To create your cluster VPC with only public subnets**

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. From the navigation bar, select a Region that supports Amazon EKS\.

1. Choose **Create stack**\.

1. For **Choose a template**, select **Specify an Amazon S3 template URL**\.

1. Paste the following URL into the text area and choose **Next**:

   ```
   https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-11-15/amazon-eks-vpc-sample.yaml
   ```

1. On the **Specify Details** page, fill out the parameters accordingly, and then choose **Next**\.
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it **eks\-vpc**\.
   + **VpcBlock**: Choose a CIDR range for your VPC\. You can keep the default value\.
   + **Subnet01Block**: Specify a CIDR range for subnet 1\. We recommend that you keep the default value so that you have plenty of IP addresses for pods to use\.
   + **Subnet02Block**: Specify a CIDR range for subnet 2\. We recommend that you keep the default value so that you have plenty of IP addresses for pods to use\.
   + **Subnet03Block**: Specify a CIDR range for subnet 3\. We recommend that you keep the default value so that you have plenty of IP addresses for pods to use\.

1. \(Optional\) On the **Options** page, tag your stack resources\. Choose **Next**\.

1. On the **Review** page, choose **Create**\.

1. When your stack is created, select it in the console and choose **Outputs**\.

1. Record the **SecurityGroups** value for the security group that was created\. You need this when you create your EKS cluster; this security group is applied to the cross\-account elastic network interfaces that are created in your subnets that allow the Amazon EKS control plane to communicate with your worker nodes\.

1. Record the **VpcId** for the VPC that was created\. You need this when you launch your worker node group template\.

1. Record the **SubnetIds** for the subnets that were created\. You need this when you create your EKS cluster; these are the subnets that your worker nodes are launched into\.

------
#### [ Public and private subnets ]

**To create your cluster VPC with public and private subnets**

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. From the navigation bar, select a Region that supports Amazon EKS\.

1. Choose **Create stack**\.

1. For **Choose a template**, select **Specify an Amazon S3 template URL**\.

1. Paste the following URL into the text area and choose **Next**:

   ```
   https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-11-15/amazon-eks-vpc-private-subnets.yaml
   ```

1. On the **Specify Details** page, fill out the parameters accordingly, and then choose **Next**\.
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it **eks\-vpc**\.
   + **VpcBlock**: Choose a CIDR range for your VPC\. You can keep the default value\.
   + **PublicSubnet01Block**: Specify a CIDR range for public subnet 1\. We recommend that you keep the default value so that you have plenty of IP addresses for pods to use\.
   + **PublicSubnet02Block**: Specify a CIDR range for public subnet 2\. We recommend that you keep the default value so that you have plenty of IP addresses for pods to use\.
   + **PrivateSubnet01Block**: Specify a CIDR range for private subnet 1\. We recommend that you keep the default value so that you have plenty of IP addresses for pods to use\.
   + **PrivateSubnet02Block**: Specify a CIDR range for private subnet 2\. We recommend that you keep the default value so that you have plenty of IP addresses for pods to use\.

1. \(Optional\) On the **Options** page, tag your stack resources\. Choose **Next**\.

1. On the **Review** page, choose **Create**\.

1. When your stack is created, select it in the console and choose **Outputs**\.

1. Record the **SecurityGroups** value for the security group that was created\. You need this when you create your EKS cluster; this security group is applied to the cross\-account elastic network interfaces that are created in your subnets that allow the Amazon EKS control plane to communicate with your worker nodes\.

1. Record the **VpcId** for the VPC that was created\. You need this when you launch your worker node group template\.

1. Record the **SubnetIds** for the subnets that were created\. You need this when you create your EKS cluster; these are the subnets that your worker nodes are launched into\.

1. Tag your private subnets so that Kubernetes knows that it can use them for internal load balancers\.

   1. Open the Amazon VPC console at [https://console\.aws\.amazon\.com/vpc/](https://console.aws.amazon.com/vpc/)\.

   1. Choose **Subnets** in the left navigation\.

   1. Select one of the private subnets for your Amazon EKS cluster's VPC \(you can filter them with the string `PrivateSubnet`\), and choose the **Tags** tab, and then **Add/Edit Tags**\.

   1. Choose **Create Tag** and add the following key and value, and then choose **Save**\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/getting-started-console.html)

   1. Repeat these substeps for each private subnet in your VPC\.
   
1. Tag your public subnets so that Kubernetes knows that it can use them for public load balancers\.

   1. Open the Amazon VPC console at [https://console\.aws\.amazon\.com/vpc/](https://console.aws.amazon.com/vpc/)\.

   1. Choose **Subnets** in the left navigation\.

   1. Select one of the public subnets for your Amazon EKS cluster's VPC \(you can filter them with the string `PublicSubnet`\), and choose the **Tags** tab, and then **Add/Edit Tags**\.

   1. Choose **Create Tag** and add the following key and value, and then choose **Save**\.    
[\[See the AWS documentation website for more details\]](https://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html)

   1. Repeat these substeps for each public subnet in your VPC\.

------

### Install and Configure kubectl for Amazon EKS<a name="get-started-kubectl"></a>

Kubernetes uses a command\-line utility called `kubectl` for communicating with the cluster API server\.

**To install kubectl for Amazon EKS**
+ You have multiple options to download and install kubectl for your operating system\.
  + The `kubectl` binary is available in many operating system package managers, and this option is often much easier than a manual download and install process\. You can follow the instructions for your specific operating system or package manager in the [Kubernetes documentation](https://kubernetes.io/docs/tasks/tools/install-kubectl/) to install\.
  + Amazon EKS also vends kubectl binaries that you can use that are identical to the upstream kubectl binaries with the same version\. To install the Amazon EKS\-vended binary for your operating system, see [Installing `kubectl`](install-kubectl.md)\.

### Install the Latest AWS CLI<a name="custom-aws-cli"></a>

To use `kubectl` with your Amazon EKS clusters, you must install a binary that can create the required client security token for cluster API server communication\. The aws eks get\-token command, available in version 1\.16\.308 or greater of the AWS CLI, supports client security token creation\. To install or upgrade the AWS CLI, see [Installing the AWS Command Line Interface](https://docs.aws.amazon.com/cli/latest/userguide/installing.html) in the *AWS Command Line Interface User Guide*\.

**Important**  
Package managers such yum, apt\-get, or Homebrew for macOS are often behind several versions of the AWS CLI\. To ensure that you have the latest version, see [Installing the AWS Command Line Interface](https://docs.aws.amazon.com/cli/latest/userguide/installing.html) in the *AWS Command Line Interface User Guide*\.

You can check your AWS CLI version with the following command:

```
aws --version
```

**Note**  
Your system's Python version must be 2\.7\.9 or greater\. Otherwise, you receive `hostname doesn't match` errors with AWS CLI calls to Amazon EKS\. For more information, see [What are "hostname doesn't match" errors?](http://docs.python-requests.org/en/master/community/faq/#what-are-hostname-doesn-t-match-errors) in the Python Requests FAQ\.

If you are unable to install version 1\.16\.308 or greater of the AWS CLI on your system, you must ensure that the AWS IAM Authenticator for Kubernetes is installed on your system\. For more information, see [Installing `aws-iam-authenticator`](install-aws-iam-authenticator.md)\.

## Step 1: Create Your Amazon EKS Cluster<a name="eks-create-cluster"></a>

Now you can create your Amazon EKS cluster\. This section helps you to create a cluster with the latest version of Kubernetes that is available in Amazon EKS to take advantage of all of the latest features\. Some features are not available on older versions of Kubernetes\.

**Important**  
When an Amazon EKS cluster is created, the IAM entity \(user or role\) that creates the cluster is added to the Kubernetes RBAC authorization table as the administrator \(with `system:master` permissions\. Initially, only that IAM user can make calls to the Kubernetes API server using kubectl\. For more information, see [Managing Users or IAM Roles for your Cluster](add-user-role.md)\. If you use the console to create the cluster, you must ensure that the same IAM user credentials are in the AWS SDK credential chain when you are running kubectl commands on your cluster\.  
If you install and configure the AWS CLI, you can configure the IAM credentials for your user\. If the AWS CLI is configured properly for your user, then `eksctl` and the [AWS IAM Authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator) can find those credentials as well\. For more information, see [Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) in the *AWS Command Line Interface User Guide*\.

**To create your cluster with the console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose **Create cluster**\.
**Note**  
If your IAM user does not have administrative privileges, you must explicitly add permissions for that user to call the Amazon EKS API operations\. For more information, see [Amazon EKS Identity\-Based Policy Examples](security_iam_id-based-policy-examples.md)\.

1. On the **Create cluster** page, fill in the following fields and then choose **Create**:
   + **Cluster name**: A unique name for your cluster\.
   + **Kubernetes version**: The version of Kubernetes to use for your cluster\. By default, the latest available version is selected\.
**Important**  
This getting started guide requires that you choose the latest available Kubernetes version\.
   + **Role name**: Select the IAM role that you created with [Create your Amazon EKS Service Role](#role-create)\.
   + **VPC**: The VPC you created with [Create your Amazon EKS Cluster VPC](#vpc-create)\. You can find the name of your VPC in the drop\-down list\.
   + **Subnets**: The **SubnetIds** values \(comma\-separated\) from the AWS CloudFormation output that you generated with [Create your Amazon EKS Cluster VPC](#vpc-create)\. Specify all subnets that will host resources for your cluster \(such as private subnets for worker nodes and public subnets for load balancers\)\. By default, the available subnets in the VPC specified in the previous field are preselected\.
   + **Security Groups**: The **SecurityGroups** value from the AWS CloudFormation output that you generated with [Create your Amazon EKS Cluster VPC](#vpc-create)\. This security group has **ControlPlaneSecurityGroup** in the drop\-down name\.
**Important**  
The worker node AWS CloudFormation template modifies the security group that you specify here, so **Amazon EKS strongly recommends that you use a dedicated security group for each cluster control plane \(one per cluster\)**\. If this security group is shared with other resources, you might block or disrupt connections to those resources\.
   + **Endpoint private access**: Choose whether to enable or disable private access for your cluster's Kubernetes API server endpoint\. If you enable private access, Kubernetes API requests that originate from within your cluster's VPC will use the private VPC endpoint\. For more information, see [Amazon EKS Cluster Endpoint Access Control](cluster-endpoint.md)\.
   + **Endpoint public access**: Choose whether to enable or disable public access for your cluster's Kubernetes API server endpoint\. If you disable public access, your cluster's Kubernetes API server can only receive requests from within the cluster VPC\. For more information, see [Amazon EKS Cluster Endpoint Access Control](cluster-endpoint.md)\.
   + **Logging** – For each individual log type, choose whether the log type should be **Enabled** or **Disabled**\. By default, each log type is **Disabled**\. For more information, see [Amazon EKS Control Plane Logging](control-plane-logs.md)
   + **Tags** – \(Optional\) Add any tags to your cluster\. For more information, see [Tagging Your Amazon EKS Resources](eks-using-tags.md)\.
**Note**  
You might receive an error that one of the Availability Zones in your request doesn't have sufficient capacity to create an Amazon EKS cluster\. If this happens, the error output contains the Availability Zones that can support a new cluster\. Retry creating your cluster with at least two subnets that are located in the supported Availability Zones for your account\. For more information, see [Insufficient Capacity](troubleshooting.md#ICE)\.

1. On the **Clusters** page, choose the name of your newly created cluster to view the cluster information\.

1. The **Status** field shows **CREATING** until the cluster provisioning process completes\. Cluster provisioning usually takes between 10 and 15 minutes\.

## Step 2: Create a `kubeconfig` File<a name="eks-configure-kubectl"></a>

In this section, you create a `kubeconfig` file for your cluster with the AWS CLI update\-kubeconfig command\. If you do not want to install the AWS CLI, or if you would prefer to create or update your kubeconfig manually, see [Create a `kubeconfig` for Amazon EKS](create-kubeconfig.md)\.

**To create your `kubeconfig` file with the AWS CLI**

1. Ensure that you have at least version 1\.16\.308 of the AWS CLI installed\. To install or upgrade the AWS CLI, see [Installing the AWS Command Line Interface](https://docs.aws.amazon.com/cli/latest/userguide/installing.html) in the *AWS Command Line Interface User Guide*\.
**Note**  
Your system's Python version must be 2\.7\.9 or greater\. Otherwise, you receive `hostname doesn't match` errors with AWS CLI calls to Amazon EKS\. For more information, see [What are "hostname doesn't match" errors?](http://docs.python-requests.org/en/master/community/faq/#what-are-hostname-doesn-t-match-errors) in the Python Requests FAQ\.

   You can check your AWS CLI version with the following command:

   ```
   aws --version
   ```
**Important**  
Package managers such yum, apt\-get, or Homebrew for macOS are often behind several versions of the AWS CLI\. To ensure that you have the latest version, see [Installing the AWS Command Line Interface](https://docs.aws.amazon.com/cli/latest/userguide/installing.html) in the *AWS Command Line Interface User Guide*\.

1. Use the AWS CLI update\-kubeconfig command to create or update your kubeconfig for your cluster\.
   + By default, the resulting configuration file is created at the default kubeconfig path \(`.kube/config`\) in your home directory or merged with an existing kubeconfig at that location\. You can specify another path with the `--kubeconfig` option\.
   + You can specify an IAM role ARN with the `--role-arn` option to use for authentication when you issue kubectl commands\. Otherwise, the IAM entity in your default AWS CLI or SDK credential chain is used\. You can view your default AWS CLI or SDK identity by running the aws sts get\-caller\-identity command\.
   + For more information, see the help page with the aws eks update\-kubeconfig help command or see [update\-kubeconfig](https://docs.aws.amazon.com/cli/latest/reference/eks/update-kubeconfig.html) in the *AWS CLI Command Reference*\.
**Note**  
To run the following command, your account must be assigned the `eks:DescribeCluster` IAM permission for the cluster name that you specify\.

   ```
   aws eks --region region update-kubeconfig --name cluster_name
   ```

1. Test your configuration\.

   ```
   kubectl get svc
   ```
**Note**  
If you receive the error `"aws-iam-authenticator": executable file not found in $PATH`, your kubectl isn't configured for Amazon EKS\. For more information, see [Installing `aws-iam-authenticator`](install-aws-iam-authenticator.md)\.  
If you receive any other authorization or resource type errors, see [Unauthorized or Access Denied \(`kubectl`\)](troubleshooting.md#unauthorized) in the troubleshooting section\.

   Output:

   ```
   NAME             TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
   svc/kubernetes   ClusterIP   10.100.0.1   <none>        443/TCP   1m
   ```

## Step 3: Launch a Managed Node Group<a name="eks-launch-workers"></a>

Now that your VPC and Kubernetes control plane are created, you can launch and configure a managed node group\.

**Important**  
Amazon EKS worker nodes are standard Amazon EC2 instances, and you are billed for them based on normal Amazon EC2 instance prices\. For more information, see [Amazon EC2 Pricing](https://aws.amazon.com/ec2/pricing/)\.

The Amazon EKS worker node `kubelet` daemon makes calls to AWS APIs on your behalf\. Worker nodes receive permissions for these API calls through an IAM instance profile and associated policies\. Before you can launch worker nodes and register them into a cluster, you must create an IAM role for those worker nodes to use when they are launched\. For more information, see [Amazon EKS Worker Node IAM Role](worker_node_IAM_role.md)\. You can create the role using the AWS Management Console or AWS CloudFormation\. Select the tab with the name of the tool that you'd like to use to create the role\.

**Note**  
We recommend that you create a new worker node IAM role for each cluster\. Otherwise, a node from one cluster could authenticate with another cluster that it does not belong to\.

------
#### [ AWS Management Console ]

**To create your Amazon EKS worker node role in the IAM console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. Choose **Roles**, then **Create role**\.

1. Choose **EC2** from the list of services, then **Next: Permissions**\.

1. In the **Filter policies** box, enter **AmazonEKSWorkerNodePolicy**\. Check the box to the left of **AmazonEKSWorkerNodePolicy\.**

1. In the **Filter policies** box, enter **AmazonEKS\_CNI\_Policy**\. Check the box to the left of **AmazonEKS\_CNI\_Policy\.**

1. In the **Filter policies** box, enter **AmazonEC2ContainerRegistryReadOnly**\. Check the box to the left of **AmazonEC2ContainerRegistryReadOnly\.**

1. Choose **Next: Tags**\.

1. \(Optional\) Add metadata to the role by attaching tags as key–value pairs\. For more information about using tags in IAM, see [Tagging IAM Entities](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html) in the *IAM User Guide*\. 

1. Choose **Next: Review**\.

1. For **Role name**, enter a unique name for your role, such as **NodeInstanceRole**\. For **Role description**, replace the current text with descriptive text such as **Amazon EKS \- Node Group Role**, then choose **Create role**\.

------
#### [ AWS CloudFormation ]

**To create your Amazon EKS worker node role using AWS CloudFormation**

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. Choose **Create stack** and then choose **With new resources \(standard\)**\.

1. For **Specify template**, select **Amazon S3 URL**\.

1. Paste the following URL into the **Amazon S3 URL** text area and choose **Next** twice:

   ```
   https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-11-15/amazon-eks-nodegroup-role.yaml
   ```

1. On the **Specify stack details** page, for **Stack name** enter a name such as **eks\-node\-group\-instance\-role** and choose **Next**\.

1. \(Optional\) On the **Configure stack options** page, you can choose to tag your stack resources\. Choose **Next**\.

1. On the **Review** page, check the box in the **Capabilities** section and choose **Create stack**\.

1. When your stack is created, select it in the console and choose **Outputs**\.

1. Record the **NodeInstanceRole** value for the IAM role that was created\. You need this when you create your node group\.

------

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

**\(Optional\) To launch Windows worker nodes**  
Add Windows support to your cluster and launch Windows worker nodes\. For more information, see [Windows Support](windows-support.md)\. All Amazon EKS clusters must contain at least one Linux worker node, even if you only want to run Windows workloads in your cluster\.

## Next Steps<a name="gs-next-steps"></a>

Now that you have a working Amazon EKS cluster with worker nodes, you are ready to start installing Kubernetes add\-ons and deploying applications to your cluster\. The following documentation topics help you to extend the functionality of your cluster\.
+ [Cluster Autoscaler](cluster-autoscaler.md) — Configure the Kubernetes [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler) to automatically adjust the number of nodes in your node groups\.
+ [Launch a Guest Book Application](eks-guestbook.md) — Create a sample guest book application to test your cluster and Linux worker nodes\.
+ [Deploy a Windows Sample Application](windows-support.md#windows-sample-application) — Deploy a sample application to test your cluster and Windows worker nodes\.
+ [Tutorial: Deploy the Kubernetes Web UI \(Dashboard\)](dashboard-tutorial.md) — This tutorial guides you through deploying the [Kubernetes dashboard](https://github.com/kubernetes/dashboard) to your cluster\.
+ [Using Helm with Amazon EKS](helm.md) — The `helm` package manager for Kubernetes helps you install and manage applications on your cluster\. 
+ [Installing the Kubernetes Metrics Server](metrics-server.md) — The Kubernetes metrics server is an aggregator of resource usage data in your cluster\.
+ [Control Plane Metrics with Prometheus](prometheus.md) — This topic helps you deploy Prometheus into your cluster with `helm`\.
