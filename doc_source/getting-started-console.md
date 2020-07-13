# Getting started with the AWS Management Console<a name="getting-started-console"></a>

This getting started guide helps you to create all of the required resources to get started with Amazon EKS using the AWS Management Console\. In this guide, you manually create each resource in the Amazon EKS or AWS CloudFormation consoles\. At the end of this tutorial, you will have a running Amazon EKS cluster with a managed node group, and the `kubectl` command line utility will be configured to use your new cluster\. The procedures in this guide give you complete visibility into how each resource is created and how the resources interact with each other\.

If you'd rather have most of the resources created for you automatically, use the `eksctl` CLI to create your cluster and worker nodes\. For more information, see [Getting started with `eksctl`](getting-started-eksctl.md)\.

## Prerequisites<a name="eks-prereqs"></a>

This section helps you to install and configure the tools and resources that you need to create and manage an Amazon EKS cluster\.

### Install the AWS CLI<a name="gs-console-install-awscli"></a>

To install the latest version of the AWS CLI, choose the tab with the name of the operating system that you'd like to install the AWS CLI on\.

------
#### [ macOS ]

If you currently have the AWS CLI installed, determine which version that you have installed\.

```
aws --version
```

If you don't have version 1\.18\.97 or later, or version 2\.0\.30 or later installed, then install the AWS CLI version 2\. For other installation options, or to upgrade your currently installed version 2, see [Upgrading the AWS CLI version 2 on macOS](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-mac.html#cliv2-mac-upgrade)\.

```
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```

 If you're unable to use the AWS CLI version 2, then ensure that you have the latest version of the [AWS CLI version 1](https://docs.aws.amazon.com/cli/latest/userguide/install-macos.html) installed using the following command\.

```
pip3 install awscli --upgrade --user
```

------
#### [ Linux ]

If you currently have the AWS CLI installed, determine which version that you have installed\.

```
aws --version
```

If you don't have version 1\.18\.97 or later, or version 2\.0\.30 or later installed, then install the AWS CLI version 2\. For other installation options, or to upgrade your currently installed version 2, see [Upgrading the AWS CLI version 2 on Linux](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html#cliv2-linux-upgrade)\.

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

If you're unable to use the AWS CLI version 2, then ensure that you have the latest version of the [AWS CLI version 1](https://docs.aws.amazon.com/cli/latest/userguide/install-linux.html) installed using the following command\.

```
pip3 install --upgrade --user awscli
```

------
#### [ Windows ]

If you currently have the AWS CLI installed, determine which version that you have installed\.

```
aws --version
```

**To install the AWS CLI version 2**

If you don't have either version 1\.18\.97 or later, or version 2\.0\.30 or later installed, then install the AWS CLI version 2 using the following steps\. For other installation options, or to upgrade your currently installed version 2, see [Upgrading the AWS CLI version 2 on Windows](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-windows.html#cliv2-windows-upgrade)\.

1. Download the AWS CLI MSI installer for Windows \(64\-bit\) at [https://awscli\.amazonaws\.com/AWSCLIV2\.msi](https://awscli.amazonaws.com/AWSCLIV2.msi)

1. Run the downloaded MSI installer and follow the onscreen instructions\. By default, the AWS CLI installs to `C:\Program Files\Amazon\AWSCLIV2`\.

If you're unable to use the AWS CLI version 2, then ensure that you have the latest version of the [AWS CLI version 1](https://docs.aws.amazon.com/cli/latest/userguide/install-windows.html) installed using the following command\.

```
pip3 install --user --upgrade awscli
```

------

### Configure your AWS CLI credentials<a name="configure-awscli"></a>

The AWS CLI requires that you have AWS credentials configured in your environment\. The aws configure command is the fastest way to set up your AWS CLI installation for general use\.

```
$ aws configure
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: region-code
Default output format [None]: json
```

When you type this command, the AWS CLI prompts you for four pieces of information: `access key`, `secret access key`, `AWS Region`, and `output format`\. This information is stored in a profile \(a collection of settings\) named `default`\. This profile is used when you run commands, unless you specify another one\.

For more information, see [Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) in the *AWS Command Line Interface User Guide*\.

### Install and configure kubectl<a name="eksctl-kubectl"></a>

Kubernetes uses the `kubectl` command\-line utility for communicating with the cluster API server\.

To install version 1\.17 of the `kubectl` command line utility, choose the tab with the name of the operating system that you'd like to install `kubectl` on\. If you need to install a different version to use with a different cluster version, then see [Installing `kubectl`](install-kubectl.md)\.

------
#### [ macOS ]

**To install `kubectl` on macOS**

1. Download the Amazon EKS\-vended kubectl binary\.

   ```
   curl -o kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.17.7/2020-07-08/bin/darwin/amd64/kubectl
   ```

1. \(Optional\) Verify the downloaded binary with the SHA\-256 sum\.

   1. Download the SHA\-256 sum\.

      ```
      curl -o kubectl.sha256 https://amazon-eks.s3.us-west-2.amazonaws.com/1.17.7/2020-07-08/bin/darwin/amd64/kubectl.sha256
      ```

   1. Check the SHA\-256 sum\.

      ```
      openssl sha1 -sha256 kubectl
      ```

   1. Compare the generated SHA\-256 sum in the command output against your downloaded SHA\-256 file\. The two should match\.

1. Apply execute permissions to the binary\.

   ```
   chmod +x ./kubectl
   ```

1. Move kubectl to a folder that is in your path\.
   + If you don't already have a version of kubectl installed, then move the binary to a folder that's already in your `PATH`\.

     ```
     sudo mv ./kubectl /usr/local/bin
     ```
   + If you already have a version of kubectl installed, then we recommend creating a `$HOME/bin/kubectl` folder, moving the binary to that folder, and ensuring that `$HOME/bin` comes first in your `$PATH`\.

     ```
     mkdir -p $HOME/bin && mv ./kubectl $HOME/bin/kubectl && export PATH=$PATH:$HOME/bin
     ```

     \(Optional\) Add the `$HOME/bin` path to your shell initialization file so that it is configured when you open a shell\.

     ```
     echo 'export PATH=$PATH:$HOME/bin' >> ~/.bash_profile
     ```

1. After you install kubectl, you can verify its version with the following command:

   ```
   kubectl version --short --client
   ```

------
#### [ Linux ]

**To install `kubectl` on Linux**

1. Download the Amazon EKS\-vended kubectl binary\.

   ```
   curl -o kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.17.7/2020-07-08/bin/linux/amd64/kubectl
   ```

1. \(Optional\) Verify the downloaded binary with the SHA\-256 sum\.

   1. Download the SHA\-256 sum\.

      ```
      curl -o kubectl.sha256 https://amazon-eks.s3.us-west-2.amazonaws.com/1.17.7/2020-07-08/bin/linux/amd64/kubectl.sha256
      ```

   1. Check the SHA\-256 sum\.

      ```
      openssl sha1 -sha256 kubectl
      ```

   1. Compare the generated SHA\-256 sum in the command output against your downloaded SHA\-256 file\. The two should match\.

1. Apply execute permissions to the binary\.

   ```
   chmod +x ./kubectl
   ```

1. Move kubectl to a folder that is in your path\.
   + If you don't already have a version of kubectl installed, then move the binary to a folder in your `PATH`\.

     ```
     sudo mv ./kubectl /usr/local/bin
     ```
   + If you already have a version of kubectl installed, then we recommend creating a `$HOME/bin/kubectl` folder, moving the binary to that folder, and ensuring that `$HOME/bin` comes first in your `$PATH`\.

     ```
     mkdir -p $HOME/bin && mv ./kubectl $HOME/bin/kubectl && export PATH=$PATH:$HOME/bin
     ```

     \(Optional\) Add the `$HOME/bin` path to your shell initialization file so that it is configured when you open a shell\.

     ```
     echo 'export PATH=$PATH:$HOME/bin' >> ~/.bash_profile
     ```
**Note**  
This step assumes you are using the Bash shell; if you are using another shell, change the command to use your specific shell initialization file\.

1. After you install kubectl, you can verify its version with the following command:

   ```
   kubectl version --short --client
   ```

------
#### [ Windows ]

**To install `kubectl` on Windows**

1. Open a PowerShell terminal\.

1. Download the Amazon EKS\-vended kubectl binary\.

   ```
   curl -o kubectl.exe https://amazon-eks.s3.us-west-2.amazonaws.com/1.17.7/2020-07-08/bin/windows/amd64/kubectl.exe
   ```

1. \(Optional\) Verify the downloaded binary with the SHA\-256 sum\.

   1. Download the SHA\-256 sum\.

      ```
      curl -o kubectl.exe.sha256 https://amazon-eks.s3.us-west-2.amazonaws.com/1.17.7/2020-07-08/bin/windows/amd64/kubectl.exe.sha256
      ```

   1. Check the SHA\-256 sum\.

      ```
      Get-FileHash kubectl.exe
      ```

   1. Compare the generated SHA\-256 sum in the command output against your downloaded SHA\-256 file\. The two should match, although the PowerShell output will be uppercase\.

1. Copy the binary to a folder in your `PATH`\. If you have an existing directory in your PATH that you use for command line utilities, copy the binary to that directory\. Otherwise, complete the following steps\.

   1. Create a new directory for your command line binaries, such as `C:\bin`\.

   1. Copy the `kubectl.exe` binary to your new directory\.

   1. Edit your user or system PATH environment variable to add the new directory to your PATH\.

   1. Close your PowerShell terminal and open a new one to pick up the new PATH variable\.

1. After you install kubectl, you can verify its version with the following command:

   ```
   kubectl version --short --client
   ```

------

### Create your Amazon EKS cluster IAM role<a name="role-create"></a>

You can create the role using the AWS Management Console or AWS CloudFormation\. Select the tab with the name of the tool that you'd like to use to create the role\.

------
#### [ AWS Management Console ]

**To create your Amazon EKS cluster role in the IAM console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. Choose **Roles**, then **Create role**\.

1. Choose **EKS** from the list of services, then **EKS \- Cluster** for your use case, and then **Next: Permissions**\.

1. Choose **Next: Tags**\.

1. \(Optional\) Add metadata to the role by attaching tags as key–value pairs\. For more information about using tags in IAM, see [Tagging IAM Entities](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html) in the *IAM User Guide*\. 

1. Choose **Next: Review**\.

1. For **Role name**, enter a unique name for your role, such as `eksClusterRole`, then choose **Create role**\.

------
#### [ AWS CloudFormation ]

**To create your Amazon EKS cluster role with AWS CloudFormation**

1. Save the following AWS CloudFormation template to a text file on your local system\.

   ```
   ---
   AWSTemplateFormatVersion: '2010-09-09'
   Description: 'Amazon EKS Cluster Role'
   
   
   Resources:
   
     eksClusterRole:
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
           - arn:aws:iam::aws:policy/AmazonEKSClusterPolicy
   
   Outputs:
   
     RoleArn:
       Description: The role that Amazon EKS will use to create AWS resources for Kubernetes clusters
       Value: !GetAtt eksClusterRole.Arn
       Export:
         Name: !Sub "${AWS::StackName}-RoleArn"
   ```
**Note**  
Prior to April 16, 2020, `ManagedPolicyArns` had an entry for `arn:aws:iam::aws:policy/AmazonEKSServicePolicy`\. With the `AWSServiceRoleForAmazonEKS` service\-linked role, that policy is no longer required\.

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. Choose **Create stack**\.

1. For **Specify template**, select **Upload a template file**, and then choose **Choose file**\.

1. Choose the file you created earlier, and then choose **Next**\.

1. For **Stack name**, enter a name for your role, such as `eksClusterRole`, and then choose **Next**\.

1. On the **Configure stack options** page, choose **Next**\.

1. On the **Review** page, review your information, acknowledge that the stack might create IAM resources, and then choose **Create stack**\.

------

### Create your Amazon EKS cluster VPC<a name="vpc-create"></a>

This section guides you through creating a VPC with either two public subnets and two private subnets or a VPC with three public subnets\. 

When you create an Amazon EKS cluster, you specify the VPC subnets for your cluster to use\. Amazon EKS requires subnets in at least two Availability Zones\. We recommend a VPC with public and private subnets so that Kubernetes can create public load balancers in the public subnets that load balance traffic to pods running on worker nodes that are in private subnets\.

For more information about both VPC types, see [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md)\.

Choose the tab below that represents your desired VPC configuration\.

------
#### [ Public and private subnets ]

**To create your cluster VPC with public and private subnets**

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. From the navigation bar, select a Region that supports Amazon EKS\.

1. Choose **Create stack**\.

1. For **Choose a template**, select **Specify an Amazon S3 template URL**\.

1. Paste the following URL into the text area and choose **Next**:

   ```
   https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-06-10/amazon-eks-vpc-private-subnets.yaml
   ```

1. On the **Specify Details** page, fill out the parameters accordingly, and then choose **Next**\.
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it **eks\-vpc**\.
   + **VpcBlock**: Choose a CIDR range for your VPC\. You can keep the default value\.
   + **PublicSubnet01Block**: Specify a CIDR range for public subnet 1\. We recommend that you keep the default value so that you have plenty of IP addresses for load balancers to use\.
   + **PublicSubnet02Block**: Specify a CIDR range for public subnet 2\. We recommend that you keep the default value so that you have plenty of IP addresses for load balancers to use\.
   + **PrivateSubnet01Block**: Specify a CIDR range for private subnet 1\. We recommend that you keep the default value so that you have plenty of IP addresses for pods and load balancers to use\.
   + **PrivateSubnet02Block**: Specify a CIDR range for private subnet 2\. We recommend that you keep the default value so that you have plenty of IP addresses for pods and load balancers to use\.

1. \(Optional\) On the **Options** page, tag your stack resources\. Choose **Next**\.

1. On the **Review** page, choose **Create**\.

1. When your stack is created, select it in the console and choose **Outputs**\.

1. Record the **SecurityGroups** value for the security group that was created\. When you add worker nodes to your cluster, you must specify the ID of the security group\. The security group is applied to the cross\-account elastic network interfaces that are created in your subnets that allow the Amazon EKS control plane to communicate with your worker nodes\.

1. Record the **VpcId** for the VPC that was created\. You need this when you launch your worker node group template\.

1. Record the **SubnetIds** for the subnets that were created and whether you created them as public or private subnets\. When you add worker nodes to your cluster, you must specify the IDs of the subnets that you want to launch the worker nodes into\.

------
#### [ Only public subnets ]

**To create your cluster VPC with only public subnets**

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. From the navigation bar, select a Region that supports Amazon EKS\.

1. Choose **Create stack**\.

1. For **Choose a template**, select **Specify an Amazon S3 template URL**\.

1. Paste the following URL into the text area and choose **Next**:

   ```
   https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-06-10/amazon-eks-vpc-sample.yaml
   ```

1. On the **Specify Details** page, fill out the parameters accordingly, and then choose **Next**\.
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it **eks\-vpc**\.
   + **VpcBlock**: Choose a CIDR range for your VPC\. You can keep the default value\.
   + **Subnet01Block**: Specify a CIDR range for subnet 1\. We recommend that you keep the default value so that you have plenty of IP addresses for pods and load balancers to use\.
   + **Subnet02Block**: Specify a CIDR range for subnet 2\. We recommend that you keep the default value so that you have plenty of IP addresses for pods and load balancers to use\.
   + **Subnet03Block**: Specify a CIDR range for subnet 3\. We recommend that you keep the default value so that you have plenty of IP addresses for pods and load balancers to use\.

1. \(Optional\) On the **Options** page, tag your stack resources\. Choose **Next**\.

1. On the **Review** page, choose **Create**\.

1. When your stack is created, select it in the console and choose **Outputs**\.

1. Record the **SecurityGroups** value for the security group that was created\. When you add worker nodes to your cluster, you must specify the ID of the security group\. The security group is applied to the cross\-account elastic network interfaces that are created in your subnets that allow the Amazon EKS control plane to communicate with your worker nodes\.

1. Record the **VpcId** for the VPC that was created\. You need this when you launch your worker node group template\.

1. Record the **SubnetIds** for the subnets that were created\. When you add worker nodes to your cluster, you must specify the IDs of the subnets that you want to launch the worker nodes into\.

------
#### [ Only private subnets ]

**To create your cluster VPC with only private subnets**

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. From the navigation bar, select a Region that supports Amazon EKS\.

1. Choose **Create stack**\.

1. For **Choose a template**, select **Specify an Amazon S3 template URL**\.

1. Paste the following URL into the text area and choose **Next**:

   ```
   https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-06-10/amazon-eks-fully-private-vpc.yaml 
   ```

1. On the **Specify Details** page, fill out the parameters accordingly, and then choose **Next**\.
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it **eks\-vpc**\.
   + **VpcBlock**: Choose a CIDR range for your VPC\. You can keep the default value\.
   + **PrivateSubnet01Block**: Specify a CIDR range for subnet 1\. We recommend that you keep the default value so that you have plenty of IP addresses for pods and load balancers to use\.
   + **PrivateSubnet02Block**: Specify a CIDR range for subnet 2\. We recommend that you keep the default value so that you have plenty of IP addresses for pods and load balancers to use\.
   + **PrivateSubnet03Block**: Specify a CIDR range for subnet 3\. We recommend that you keep the default value so that you have plenty of IP addresses for pods and load balancers to use\.

1. \(Optional\) On the **Options** page, tag your stack resources\. Choose **Next**\.

1. On the **Review** page, choose **Create**\.

1. When your stack is created, select it in the console and choose **Outputs**\.

1. Record the **SecurityGroups** value for the security group that was created\. When you add worker nodes to your cluster, you must specify the ID of the security group\. The security group is applied to the cross\-account elastic network interfaces that are created in your subnets that allow the Amazon EKS control plane to communicate with your worker nodes\.

1. Record the **VpcId** for the VPC that was created\. You need this when you launch your worker node group template\.

1. Record the **SubnetIds** for the subnets that were created\. When you add worker nodes to your cluster, you must specify the IDs of the subnets that you want to launch the worker nodes into\.

------

## Step 1: Create your Amazon EKS cluster<a name="eks-create-cluster"></a>

This section helps you to create an Amazon EKS cluster\. The latest Kubernetes version available in Amazon EKS is installed so that you can take advantage of the latest Kubernetes and Amazon EKS features\. Some features are not available on older versions of Kubernetes\.

**Important**  
When an Amazon EKS cluster is created, the IAM entity \(user or role\) that creates the cluster is added to the Kubernetes RBAC authorization table as the administrator \(with `system:masters` permissions\. Initially, only that IAM user can make calls to the Kubernetes API server using kubectl\. For more information, see [Managing users or IAM roles for your cluster](add-user-role.md)\. If you use the console to create the cluster, you must ensure that the same IAM user credentials are in the AWS SDK credential chain when you are running kubectl commands on your cluster\.  
If you install and configure the AWS CLI, you can configure the IAM credentials for your user\. If the AWS CLI version 1\.16\.156 or later is configured properly for your user, then `eksctl` can find those credentials\. For more information, see [Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) in the *AWS Command Line Interface User Guide*\. If you can't install the AWS CLI version 1\.16\.156 or later, then you must install the [https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html](https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html)\.

**To create your cluster with the console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose **Create cluster**\.
**Note**  
If your IAM user doesn't have administrative privileges, you must explicitly add permissions for that user to call the Amazon EKS API operations\. For more information, see [Amazon EKS identity\-based policy examples](security_iam_id-based-policy-examples.md)\.

1. On the **Configure cluster** page, fill in the following fields:
   + **Name** – A unique name for your cluster\.
   + **Kubernetes version** – The version of Kubernetes to use for your cluster\.
**Note**  
You cannot deploy Kubernetes 1\.17 in the `us-gov-east-1` or `us-gov-east-2 Regions`\. 
   + **Cluster service role** – Select the IAM role that you created with [Create your Amazon EKS cluster IAM role](#role-create)\.
   + **Secrets encryption** – \(Optional\) Choose to enable envelope encryption of Kubernetes secrets using the AWS Key Management Service \(AWS KMS\)\. If you enable envelope encryption, the Kubernetes secrets are encrypted using the customer master key \(CMK\) that you select\. The CMK must be symmetric, created in the same region as the cluster, and if the CMK was created in a different account, the user must have access to the CMK\. For more information, see [Allowing users in other accounts to use a CMK](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html) in the *AWS Key Management Service Developer Guide*\.

      Kubernetes secrets encryption with an AWS KMS CMK requires Kubernetes version 1\.13 or later\. If no keys are listed, you must create one first\. For more information, see [Creating keys](https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html)\.
   + **Tags** – \(Optional\) Add any tags to your cluster\. For more information, see [Tagging your Amazon EKS resources](eks-using-tags.md)\.

1. Select **Next**\.

1. On the **Specify networking** page, select values for the following fields:
   + **VPC** – The VPC that you created previously in [Create your Amazon EKS cluster VPC](#vpc-create)\. You can find the name of your VPC in the drop\-down list\.
   + **Subnets** – By default, the available subnets in the VPC specified in the previous field are preselected\. Select any subnet that you don't want to host cluster resources, such as worker nodes or load balancers\.
   + **Security groups** – The **SecurityGroups** value from the AWS CloudFormation output that you generated with [Create your Amazon EKS cluster VPC](#vpc-create)\. This security group has **ControlPlaneSecurityGroup** in the drop\-down name\.
**Important**  
The worker node AWS CloudFormation template modifies the security group that you specify here, so **Amazon EKS strongly recommends that you use a dedicated security group for each cluster control plane \(one per cluster\)**\. If this security group is shared with other resources, you might block or disrupt connections to those resources\.
   + For **Cluster endpoint access** – Choose one of the following options:
     + **Public** – Enables only public access to your cluster's Kubernetes API server endpoint\. Kubernetes API requests that originate from outside of your cluster's VPC use the public endpoint\. By default, access is allowed from any source IP address\. You can optionally restrict access to one or more CIDR ranges such as 192\.168\.0\.0/16, for example, by selecting **Advanced settings** and then selecting **Add source**\.
     + **Private** – Enables only private access to your cluster's Kubernetes API server endpoint\. Kubernetes API requests that originate from within your cluster's VPC use the private VPC endpoint\. 
**Important**  
If you created a VPC without outbound internet access, then you must enable private access\.
     + **Public and private** – Enables public and private access\.

     For more information about the previous options, see [Modifying cluster endpoint access](cluster-endpoint.md#modify-endpoint-access)\.

1. Select **Next**\.

1. On the **Configure logging** page, you can optionally choose which log types that you want to enable\. By default, each log type is **Disabled**\. For more information, see [Amazon EKS control plane logging](control-plane-logs.md)\.

1. Select **Next**\.

1. On the **Review and create** page, review the information that you entered or selected on the previous pages\. Select **Edit** if you need to make changes to any of your selections\. Once you're satisfied with your settings, select **Create**\. The **Status** field shows **CREATING** until the cluster provisioning process completes\.
**Note**  
You might receive an error that one of the Availability Zones in your request doesn't have sufficient capacity to create an Amazon EKS cluster\. If this happens, the error output contains the Availability Zones that can support a new cluster\. Retry creating your cluster with at least two subnets that are located in the supported Availability Zones for your account\. For more information, see [Insufficient capacity](troubleshooting.md#ICE)\.

   When your cluster provisioning is complete \(usually between 10 and 15 minutes\), note the **API server endpoint** and **Certificate authority** values\. These are used in your kubectl configuration\.

## Step 2: Create a `kubeconfig` file<a name="eks-configure-kubectl"></a>

In this section, you create a `kubeconfig` file for your cluster with the AWS CLI update\-kubeconfig command\.

**To create your `kubeconfig` file with the AWS CLI**

1. Use the AWS CLI update\-kubeconfig command to create or update a `kubeconfig` for your cluster\.
   + By default, the resulting configuration file is created at the default kubeconfig path \(`.kube/config`\) in your home directory or merged with an existing kubeconfig at that location\. You can specify another path with the `--kubeconfig` option\.
   + You can specify an IAM role ARN with the `--role-arn` option to use for authentication when you issue kubectl commands\. Otherwise, the IAM entity in your default AWS CLI or SDK credential chain is used\. You can view your default AWS CLI or SDK identity by running the aws sts get\-caller\-identity command\.
   + For more information, see the help page with the aws eks update\-kubeconfig help command or see [update\-kubeconfig](https://docs.aws.amazon.com/cli/latest/reference/eks/update-kubeconfig.html) in the *AWS CLI Command Reference*\.
**Note**  
To run the following command, you must have permission to the use the `eks:DescribeCluster` API action with the cluster that you specify\. For more information, see [Amazon EKS identity\-based policy examples](security_iam_id-based-policy-examples.md)\.

   ```
   aws eks --region us-west-2 update-kubeconfig --name cluster_name
   ```

1. Test your configuration\.

   ```
   kubectl get svc
   ```
**Note**  
If you receive any authorization or resource type errors, see [Unauthorized or access denied \(`kubectl`\)](troubleshooting.md#unauthorized) in the troubleshooting section\.

   Output:

   ```
   NAME             TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
   svc/kubernetes   ClusterIP   10.100.0.1   <none>        443/TCP   1m
   ```

## Step 3: Launch a managed node group<a name="eks-launch-workers"></a>

Now that your VPC and Kubernetes control plane are created, you can launch and configure a managed node group\.

**Important**  
Amazon EKS worker nodes are standard Amazon EC2 instances, and you are billed for them based on normal Amazon EC2 instance prices\. For more information, see [Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/)\.

The Amazon EKS worker node `kubelet` daemon makes calls to AWS APIs on your behalf\. Worker nodes receive permissions for these API calls through an IAM instance profile and associated policies\. 

Before you can launch worker nodes and register them into a cluster, you must create an IAM role for those worker nodes to use when they are launched\. For more information, see [Amazon EKS worker node IAM role](worker_node_IAM_role.md)\. You can create the role using the AWS Management Console or AWS CloudFormation\. Select the tab with the name of the tool that you'd like to use to create the role\.

**Note**  
We recommend that you create a new worker node IAM role for each cluster\. Otherwise, a node from one cluster could authenticate with another cluster that it does not belong to\.

------
#### [ AWS Management Console ]

**To create your Amazon EKS worker node role in the IAM console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. Choose **Roles**, then **Create role**\.

1. Choose **EC2** from the list of **Common use cases** under** Choose a use case,** then choose **Next: Permissions**\.

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
   https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-06-10/amazon-eks-nodegroup-role.yaml
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

1. On the cluster page, select the **Compute** tab, and then choose **Add Node Group**\.

1. On the **Configure node group** page, fill out the parameters accordingly, and then choose **Next**\.
   + **Name** – Enter a unique name for your managed node group\.
   + **Node IAM role name** – Choose the node instance role to use with your node group\. For more information, see [Amazon EKS worker node IAM role](worker_node_IAM_role.md)\.
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
   + **Instance type** – Choose the instance type to use in your managed node group\. Larger instance types can accommodate more pods\.
   + **Disk size** – Enter the disk size \(in GiB\) to use for your worker node root volume\.

1. On the **Setup scaling policies** page, fill out the parameters accordingly, and then choose **Next**\.
**Note**  
Amazon EKS does not automatically scale your node group in or out\. However, you can configure the Kubernetes [Cluster Autoscaler](cluster-autoscaler.md) to do this for you\.
   + **Minimum size** – Specify the minimum number of worker nodes that the managed node group can scale in to\.
   + **Maximum size** – Specify the maximum number of worker nodes that the managed node group can scale out to\.
   + **Desired size** – Specify the current number of worker nodes that the managed node group should maintain at launch\.

1. On the **Review and create** page, review your managed node group configuration and choose **Create**\.
**Note**  
If worker nodes fail to join the cluster, see [Worker nodes fail to join cluster](troubleshooting.md#worker-node-fail) in the Troubleshooting guide\.

1. Watch the status of your nodes and wait for them to reach the `Ready` status\.

   ```
   kubectl get nodes --watch
   ```

1. \(GPU workers only\) If you chose a GPU instance type and the Amazon EKS\-optimized accelerated AMI, then you must apply the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) as a DaemonSet on your cluster with the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/1.0.0-beta/nvidia-device-plugin.yml
   ```

1. \(Optional\) [Deploy a sample Linux application](sample-deployment.md) — Deploy a sample application to test your cluster and Linux worker nodes\.

**\(Optional\) To launch Windows worker nodes**  
Add Windows support to your cluster and launch Windows worker nodes\. For more information, see [Windows support](windows-support.md)\. All Amazon EKS clusters must contain at least one Linux worker node, even if you only want to run Windows workloads in your cluster\.

## Next steps<a name="gs-next-steps"></a>

Now that you have a working Amazon EKS cluster with worker nodes, you are ready to start installing Kubernetes add\-ons and deploying applications to your cluster\. The following documentation topics help you to extend the functionality of your cluster\.
+ [Cluster Autoscaler](cluster-autoscaler.md) – Configure the Kubernetes [Cluster autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler) to automatically adjust the number of nodes in your node groups\.
+ [Deploy a sample Linux application](sample-deployment.md) – Deploy a sample Linux application to test your cluster and Linux worker nodes\.
+ [Deploy a Windows sample application](windows-support.md#windows-sample-application) – Deploy a sample application to test your cluster and Windows worker nodes\.
+ [Tutorial: Deploy the Kubernetes Dashboard \(web UI\)](dashboard-tutorial.md) – This tutorial guides you through deploying the [Kubernetes dashboard](https://github.com/kubernetes/dashboard) to your cluster\.
+ [Using Helm with Amazon EKS](helm.md) – The `helm` package manager for Kubernetes helps you install and manage applications on your cluster\. 
+ [Installing the Kubernetes Metrics Server](metrics-server.md) – The Kubernetes metrics server is an aggregator of resource usage data in your cluster\.
+ [Control plane metrics with Prometheus](prometheus.md) – This topic helps you deploy Prometheus into your cluster with `helm`\.