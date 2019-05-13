# Getting Started with the AWS Management Console<a name="getting-started-console"></a>

This getting started guide helps you to create all of the required resources to get started with Amazon EKS in the AWS Management Console\. In this guide, you manually create each resource in the Amazon EKS or AWS CloudFormation consoles, and the workflow described here gives you complete visibility into how each resource is created and how they interact with each other\.

For a simpler and more automated getting started experience, see [Getting Started with `eksctl`](getting-started-eksctl.md)\.

## Amazon EKS Prerequisites<a name="eks-prereqs"></a>

Before you can create an Amazon EKS cluster, you must create an IAM role that Kubernetes can assume to create AWS resources\. For example, when a load balancer is created, Kubernetes assumes the role to create an Elastic Load Balancing load balancer in your account\. This only needs to be done one time and can be used for multiple EKS clusters\.

You must also create a VPC and a security group for your cluster to use\. Although the VPC and security groups can be used for multiple EKS clusters, we recommend that you use a separate VPC for each EKS cluster to provide better network isolation\.

This section also helps you to install the kubectl binary and configure it to work with Amazon EKS\.

### Create your Amazon EKS Service Role<a name="role-create"></a>

**To create your Amazon EKS service role in the IAM console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. Choose **Roles**, then **Create role**\.

1. Choose **EKS** from the list of services, then **Allows Amazon EKS to manage your clusters on your behalf** for your use case, then **Next: Permissions**\.

1. Choose **Next: Tags**\.

1. \(Optional\) Add metadata to the role by attaching tags as key–value pairs\. For more information about using tags in IAM, see [Tagging IAM Entities](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html) in the *IAM User Guide*\. 

1. Choose **Next: Review**\.

1. For **Role name**, enter a unique name for your role, such as `eksServiceRole`, then choose **Create role**\.

### Create your Amazon EKS Cluster VPC<a name="vpc-create"></a>

**To create your cluster VPC**

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. From the navigation bar, select a Region that supports Amazon EKS\.

1. Choose **Create stack**\.

1. For **Choose a template**, select **Specify an Amazon S3 template URL**\.

1. Paste the following URL into the text area and choose **Next**:

   ```
   https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-02-11/amazon-eks-vpc-sample.yaml
   ```

1. On the **Specify Details** page, fill out the parameters accordingly, and then choose **Next**\.
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it **eks\-vpc**\.
   + **VpcBlock**: Choose a CIDR range for your VPC\. You can keep the default value\.
   + **Subnet01Block**: Choose a CIDR range for subnet 1\. You can keep the default value\.
   + **Subnet02Block**: Choose a CIDR range for subnet 2\. You can keep the default value\.
   + **Subnet03Block**: Choose a CIDR range for subnet 3\. You can keep the default value\.

1. \(Optional\) On the **Options** page, tag your stack resources\. Choose **Next**\.

1. On the **Review** page, choose **Create**\.

1. When your stack is created, select it in the console and choose **Outputs**\.

1. Record the **SecurityGroups** value for the security group that was created\. You need this when you create your EKS cluster; this security group is applied to the cross\-account elastic network interfaces that are created in your subnets that allow the Amazon EKS control plane to communicate with your worker nodes\.

1. Record the **VpcId** for the VPC that was created\. You need this when you launch your worker node group template\.

1. Record the **SubnetIds** for the subnets that were created\. You need this when you create your EKS cluster; these are the subnets that your worker nodes are launched into\.

### Install and Configure kubectl for Amazon EKS<a name="get-started-kubectl"></a>

Kubernetes uses a command\-line utility called `kubectl` for communicating with the cluster API server\.

**To install kubectl for Amazon EKS**
+ You have multiple options to download and install kubectl for your operating system\.
  + The `kubectl` binary is available in many operating system package managers, and this option is often much easier than a manual download and install process\. You can follow the instructions for your specific operating system or package manager in the [Kubernetes documentation](https://kubernetes.io/docs/tasks/tools/install-kubectl/) to install\.
  + Amazon EKS also vends kubectl binaries that you can use that are identical to the upstream kubectl binaries with the same version\. To install the Amazon EKS\-vended binary for your operating system, see [Installing `kubectl`](install-kubectl.md)\.

### Install the Latest AWS CLI<a name="custom-aws-cli"></a>

To use `kubectl` with your Amazon EKS clusters, you must install a binary that can create the required client security token for cluster API server communication\. The aws eks get\-token command, available in version 1\.16\.156 or greater of the AWS CLI, supports client security token creation\. To install or upgrade the AWS CLI, see [Installing the AWS Command Line Interface](https://docs.aws.amazon.com/cli/latest/userguide/installing.html) in the *AWS Command Line Interface User Guide*\.

**Important**  
Package managers such yum, apt\-get, or Homebrew for macOS are often behind several versions of the AWS CLI\. To ensure that you have the latest version, see [Installing the AWS Command Line Interface](https://docs.aws.amazon.com/cli/latest/userguide/installing.html) in the *AWS Command Line Interface User Guide*\.

You can check your AWS CLI version with the following command:

```
aws --version
```

**Note**  
Your system's Python version must be 2\.7\.9 or greater\. Otherwise, you receive `hostname doesn't match` errors with AWS CLI calls to Amazon EKS\. For more information, see [What are "hostname doesn't match" errors?](http://docs.python-requests.org/en/master/community/faq/#what-are-hostname-doesn-t-match-errors) in the Python Requests FAQ\.

If you are unable to install version 1\.16\.156 or greater of the AWS CLI on your system, you must ensure that the AWS IAM Authenticator for Kubernetes is installed on your system\. For more information, see [Installing `aws-iam-authenticator`](install-aws-iam-authenticator.md)\.

## Step 1: Create Your Amazon EKS Cluster<a name="eks-create-cluster"></a>

Now you can create your Amazon EKS cluster\.

**Important**  
When an Amazon EKS cluster is created, the IAM entity \(user or role\) that creates the cluster is added to the Kubernetes RBAC authorization table as the administrator \(with `system:master` permissions\. Initially, only that IAM user can make calls to the Kubernetes API server using kubectl\. For more information, see [Managing Users or IAM Roles for your Cluster](add-user-role.md)\. If you use the console to create the cluster, you must ensure that the same IAM user credentials are in the AWS SDK credential chain when you are running kubectl commands on your cluster\.  
If you install and configure the AWS CLI, you can configure the IAM credentials for your user\. If the AWS CLI is configured properly for your user, then `eksctl` and the [AWS IAM Authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator) can find those credentials as well\. For more information, see [Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) in the *AWS Command Line Interface User Guide*\.

**To create your cluster with the console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose **Create cluster**\.
**Note**  
If your IAM user does not have administrative privileges, you must explicitly add permissions for that user to call the Amazon EKS API operations\. For more information, see [Creating Amazon EKS IAM Policies](EKS_IAM_user_policies.md)\.

1. On the **Create cluster** page, fill in the following fields and then choose **Create**:
   + **Cluster name**: A unique name for your cluster\.
   + **Kubernetes version**: The version of Kubernetes to use for your cluster\. By default, the latest available version is selected\.
   + **Role ARN**: Select the IAM role that you created with [Create your Amazon EKS Service Role](#role-create)\.
   + **VPC**: The VPC you created with [Create your Amazon EKS Cluster VPC](#vpc-create)\. You can find the name of your VPC in the drop\-down list\.
   + **Subnets**: The **SubnetIds** values \(comma\-separated\) from the AWS CloudFormation output that you generated with [Create your Amazon EKS Cluster VPC](#vpc-create)\. By default, the available subnets in the above VPC are preselected\.
   + **Security Groups**: The **SecurityGroups** value from the AWS CloudFormation output that you generated with [Create your Amazon EKS Cluster VPC](#vpc-create)\. This security group has **ControlPlaneSecurityGroup** in the drop\-down name\.
**Important**  
The worker node AWS CloudFormation template modifies the security group that you specify here, so **Amazon EKS strongly recommends that you use a dedicated security group for each cluster control plane \(one per cluster\)**\. If this security group is shared with other resources, you might block or disrupt connections to those resources\.
   + **Endpoint private access**: Choose whether to enable or disable private access for your cluster's Kubernetes API server endpoint\. If you enable private access, Kubernetes API requests that originate from within your cluster's VPC will use the private VPC endpoint\. For more information, see [Amazon EKS Cluster Endpoint Access Control](cluster-endpoint.md)\.
   + **Endpoint public access**: Choose whether to enable or disable public access for your cluster's Kubernetes API server endpoint\. If you disable public access, your cluster's Kubernetes API server can only receive requests from within the cluster VPC\. For more information, see [Amazon EKS Cluster Endpoint Access Control](cluster-endpoint.md)\.
   + **Logging** – For each individual log type, choose whether the log type should be **Enabled** or **Disabled**\. By default, each log type is **Disabled**\. For more information, see [Amazon EKS Control Plane Logging](control-plane-logs.md)
**Note**  
You might receive an error that one of the Availability Zones in your request doesn't have sufficient capacity to create an Amazon EKS cluster\. If this happens, the error output contains the Availability Zones that can support a new cluster\. Retry creating your cluster with at least two subnets that are located in the supported Availability Zones for your account\. For more information, see [Insufficient Capacity](troubleshooting.md#ICE)\.

1. On the **Clusters** page, choose the name of your newly created cluster to view the cluster information\.

1. The **Status** field shows **CREATING** until the cluster provisioning process completes\. Cluster provisioning usually takes between 10 and 15 minutes\.

## Step 2: Create a `kubeconfig` File<a name="eks-configure-kubectl"></a>

In this section, you create a `kubeconfig` file for your cluster with the AWS CLI update\-kubeconfig command\. If you do not want to install the AWS CLI, or if you would prefer to create or update your kubeconfig manually, see [Create a `kubeconfig` for Amazon EKS](create-kubeconfig.md)\.

**To create your `kubeconfig` file with the AWS CLI**

1. Ensure that you have at least version 1\.16\.156 of the AWS CLI installed\. To install or upgrade the AWS CLI, see [Installing the AWS Command Line Interface](https://docs.aws.amazon.com/cli/latest/userguide/installing.html) in the *AWS Command Line Interface User Guide*\.
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

## Step 3: Launch and Configure Amazon EKS Worker Nodes<a name="eks-launch-workers"></a>

Now that your VPC and Kubernetes control plane are created, you can launch and configure your worker nodes\.

**Important**  
Amazon EKS worker nodes are standard Amazon EC2 instances, and you are billed for them based on normal Amazon EC2 On\-Demand Instance prices\. For more information, see [Amazon EC2 Pricing](https://aws.amazon.com/ec2/pricing/on-demand/)\.

**To launch your worker nodes**

1. Wait for your cluster status to show as `ACTIVE`\. If you launch your worker nodes before the cluster is active, the worker nodes will fail to register with the cluster and you will have to relaunch them\.

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. From the navigation bar, select a Region that supports Amazon EKS\.

1. Choose **Create stack**\.

1. For **Choose a template**, select **Specify an Amazon S3 template URL**\.

1. Paste the following URL into the text area and choose **Next**:

   ```
   https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-02-11/amazon-eks-nodegroup.yaml
   ```

1. On the **Specify Details** page, fill out the following parameters accordingly, and choose **Next**\.
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it ***<cluster\-name>*\-worker\-nodes**\.
   + **ClusterName**: Enter the name that you used when you created your Amazon EKS cluster\.
**Important**  
This name must exactly match the name you used in [Step 1: Create Your Amazon EKS Cluster](#eks-create-cluster); otherwise, your worker nodes cannot join the cluster\.
   + **ClusterControlPlaneSecurityGroup**: Choose the **SecurityGroups** value from the AWS CloudFormation output that you generated with [Create your Amazon EKS Cluster VPC](#vpc-create)\.
   + **NodeGroupName**: Enter a name for your node group\. This name can be used later to identify the Auto Scaling node group that is created for your worker nodes\.
   + **NodeAutoScalingGroupMinSize**: Enter the minimum number of nodes that your worker node Auto Scaling group can scale in to\.
   + **NodeAutoScalingGroupDesiredCapacity**: Enter the desired number of nodes to scale to when your stack is created\.
   + **NodeAutoScalingGroupMaxSize**: Enter the maximum number of nodes that your worker node Auto Scaling group can scale out to\.
   + **NodeInstanceType**: Choose an instance type for your worker nodes\.
**Important**  
Some instance types might not be available in all regions\.
   + **NodeImageId**: Enter the current Amazon EKS worker node AMI ID for your Region\. The AMI IDs for the latest Amazon EKS\-optimized AMI \(with and without [GPU support](gpu-ami.md)\) are shown in the following table\.
**Note**  
The Amazon EKS\-optimized AMI with GPU support only supports P2 and P3 instance types\. Be sure to specify these instance types in your worker node AWS CloudFormation template\. By using the Amazon EKS\-optimized AMI with GPU support, you agree to [NVIDIA's end user license agreement \(EULA\)](https://www.nvidia.com/en-us/about-nvidia/eula-agreement/)\.

------
#### [ Kubernetes version 1\.12\.7 ]    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/getting-started-console.html)

------
#### [ Kubernetes version 1\.11\.9 ]    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/getting-started-console.html)

------
#### [ Kubernetes version 1\.10\.13 ]    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/getting-started-console.html)

------
**Note**  
The Amazon EKS worker node AMI is based on Amazon Linux 2\. You can track security or privacy events for Amazon Linux 2 at the [Amazon Linux Security Center](https://alas.aws.amazon.com/alas2.html) or subscribe to the associated [RSS feed](https://alas.aws.amazon.com/AL2/alas.rss)\. Security and privacy events include an overview of the issue, what packages are affected, and how to update your instances to correct the issue\.
   + **KeyName**: Enter the name of an Amazon EC2 SSH key pair that you can use to connect using SSH into your worker nodes with after they launch\. If you don't already have an Amazon EC2 keypair, you can create one in the AWS Management Console\. For more information, see [Amazon EC2 Key Pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) in the *Amazon EC2 User Guide for Linux Instances*\.
**Note**  
If you do not provide a keypair here, the AWS CloudFormation stack creation fails\.
   + **BootstrapArguments**: Specify any optional arguments to pass to the worker node bootstrap script, such as extra kubelet arguments\. For more information, view the bootstrap script usage information at [https://github\.com/awslabs/amazon\-eks\-ami/blob/master/files/bootstrap\.sh](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) 
   + **VpcId**: Enter the ID for the VPC that you created in [Create your Amazon EKS Cluster VPC](#vpc-create)\.
   + **Subnets**: Choose the subnets that you created in [Create your Amazon EKS Cluster VPC](#vpc-create)\.

1. On the **Options** page, you can choose to tag your stack resources\. Choose **Next**\.

1. On the **Review** page, review your information, acknowledge that the stack might create IAM resources, and then choose **Create**\.

1. When your stack has finished creating, select it in the console and choose the **Outputs** tab\.

1. Record the **NodeInstanceRole** for the node group that was created\. You need this when you configure your Amazon EKS worker nodes\.

**To enable worker nodes to join your cluster**

1. Download, edit, and apply the AWS authenticator configuration map:

   1. Download the configuration map with the following command:

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

   1. Apply the configuration\. This command might take a few minutes to finish\.

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

1. \(GPU workers only\) If you chose a P2 or P3 instance type and the Amazon EKS\-optimized AMI with GPU support, you must apply the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) as a daemon set on your cluster with the following command\.
**Note**  
If your cluster is running a different Kubernetes version than 1\.12, be sure to substitute your cluster's version in the following URL\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v1.12/nvidia-device-plugin.yml
   ```

## Next Steps<a name="gs-next-steps"></a>

Now that you have a working Amazon EKS cluster with worker nodes, you are ready to start installing Kubernetes add\-ons and deploying applications to your cluster\. The following documentation topics help you to extend the functionality of your cluster\.
+ [Launch a Guest Book Application](eks-guestbook.md) — Create a sample guest book application to test your cluster\.
+ [Tutorial: Deploy the Kubernetes Web UI \(Dashboard\)](dashboard-tutorial.md) — This tutorial guides you through deploying the [Kubernetes dashboard](https://github.com/kubernetes/dashboard) to your cluster\.
+ [Using Helm with Amazon EKS](helm.md) — The `helm` package manager for Kubernetes helps you install and manage applications on your cluster\. 
+ [Installing the Kubernetes Metrics Server](metrics-server.md) — The Kubernetes metrics server is an aggregator of resource usage data in your cluster\.
+ [Control Plane Metrics with Prometheus](prometheus.md) — This topic helps you deploy Prometheus into your cluster with `helm`\.