# Getting started with `eksctl`<a name="getting-started-eksctl"></a>

This getting started guide helps you to create all of the required resources to get started with Amazon EKS using `eksctl`, a simple command line utility for creating and managing Kubernetes clusters on Amazon EKS\. At the end of this tutorial, you will have a running Amazon EKS cluster that you can deploy applications to\. 

The procedures in this guide create several resources for you automatically, that you have to create manually when you create your cluster using the AWS Management Console\. If you'd rather manually create most of the resources to better understand how they interact with each other, then use the AWS Management Console to create your cluster and compute\. For more information, see [Getting started with the AWS Management Console](getting-started-console.md)\.

## Prerequisites<a name="eksctl-prereqs"></a>

This section helps you to install and configure the following tools that you need to create and manage an Amazon EKS cluster\.
+ **[AWS CLI](#install-awscli)** – Command line tools for working with AWS services, including Amazon EKS\.
+ **`eksctl`** – A command line tool for working with EKS clusters that automates many individual tasks\.
+ **[`kubectl`](#eksctl-gs-install-kubectl)** – A command line tool for working with Kubernetes clusters\.

### Install the AWS CLI<a name="install-awscli"></a>

You can install the latest version of the AWS CLI for [macOS](#install-aws-cli-macos), [Linux](#install-aws-cli-linux), or [Windows](#install-aws-cli-windows)\.<a name="install-aws-cli-macos"></a>

**\[ To install the AWS CLI for macOS \]**

1. If you currently have the AWS CLI installed, determine which version that you have installed\.

   ```
   aws --version
   ```

1. If you don't have version 1\.18\.188 or later, or version 2\.1\.6 or later installed, then install the AWS CLI version 2\. For other installation options, or to upgrade your currently installed version 2, see [Upgrading the AWS CLI version 2 on macOS](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-mac.html#cliv2-mac-upgrade)\.

   ```
   curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
   sudo installer -pkg AWSCLIV2.pkg -target /
   ```

    If you're unable to use the AWS CLI version 2, then ensure that you have the latest version of the [AWS CLI version 1](https://docs.aws.amazon.com/cli/latest/userguide/install-macos.html) installed using the following command\.

   ```
   pip3 install awscli --upgrade --user
   ```<a name="install-aws-cli-linux"></a>

**\[ To install the AWS CLI for Linux \]**

1. If you currently have the AWS CLI installed, determine which version that you have installed\.

   ```
   aws --version
   ```

1. If you don't have version 1\.18\.188 or later, or version 2\.1\.6 or later installed, then install the AWS CLI version 2\. For other installation options, or to upgrade your currently installed version 2, see [Upgrading the AWS CLI version 2 on Linux](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html#cliv2-linux-upgrade)\.

   ```
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   unzip awscliv2.zip
   sudo ./aws/install
   ```

   If you're unable to use the AWS CLI version 2, then ensure that you have the latest version of the [AWS CLI version 1](https://docs.aws.amazon.com/cli/latest/userguide/install-linux.html) installed using the following command\.

   ```
   pip3 install --upgrade --user awscli
   ```<a name="install-aws-cli-windows"></a>

**\[To install the AWS CLI for Windows\]**

1. If you currently have the AWS CLI installed, determine which version that you have installed\.

   ```
   aws --version
   ```

1. If you don't have either version 1\.18\.188 or later, or version 2\.1\.6 or later installed, then install the AWS CLI version 2 using the following steps\. For other installation options, or to upgrade your currently installed version 2, see [Upgrading the AWS CLI version 2 on Windows](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-windows.html#cliv2-windows-upgrade)\.

   1. Download the AWS CLI MSI installer for Windows \(64\-bit\) at [https://awscli\.amazonaws\.com/AWSCLIV2\.msi](https://awscli.amazonaws.com/AWSCLIV2.msi)

   1. Run the downloaded MSI installer and follow the onscreen instructions\. By default, the AWS CLI installs to `C:\Program Files\Amazon\AWSCLIV2`\.

1. \(Optional\) If you're unable to use the AWS CLI version 2, then ensure that you have the latest version of the [AWS CLI version 1](https://docs.aws.amazon.com/cli/latest/userguide/install-windows.html) installed using the following command\.

   ```
   pip3 install --user --upgrade awscli
   ```

### Configure your AWS CLI credentials<a name="configure-awscli"></a>

Both `eksctl` and the AWS CLI require that you have AWS credentials configured in your environment\. The  `aws configure`  command is the fastest way to set up your AWS CLI installation for general use\.

```
$ aws configure
AWS Access Key ID [None]: <AKIAIOSFODNN7EXAMPLE>
AWS Secret Access Key [None]: <wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY>
Default region name [None]: <region-code>
Default output format [None]: <json>
```

When you type this command, the AWS CLI prompts you for four pieces of information: `access key`, `secret access key`, `AWS Region`, and `output format`\. This information is stored in a profile \(a collection of settings\) named `default`\. This profile is used when you run commands, unless you specify another one\.

For more information, see [Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) in the *AWS Command Line Interface User Guide*\.

### Install `eksctl`<a name="install-eksctl"></a>

You can install 0\.33\.0\-rc\.0 version or later of the  `eksctl`  command line utility on [macOS](#install-eksctl-macos), [Linux](#install-eksctl-linux), or [Windows](#install-eksctl-windows)\. For more information, see [https://eksctl\.io/](https://github.com/weaveworks/eksctl)\.<a name="install-eksctl-macos"></a>

**\[ To install or upgrade `eksctl` on macOS using Homebrew \]**

The easiest way to get started with Amazon EKS and macOS is by installing `eksctl` with [Homebrew](https://brew.sh/)\. The `eksctl` Homebrew recipe installs `eksctl` and any other dependencies that are required for Amazon EKS, such as `kubectl`\. The recipe also installs the [`aws-iam-authenticator`](install-aws-iam-authenticator.md), which is required if you don't have the AWS CLI version 1\.16\.156 or higher installed\.

1. If you do not already have Homebrew installed on macOS, install it with the following command\.

   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
   ```

1. Install the Weaveworks Homebrew tap\.

   ```
   brew tap weaveworks/tap
   ```

1. Install or upgrade `eksctl`\.
   + Install `eksctl` with the following command:

     ```
     brew install weaveworks/tap/eksctl
     ```
   + If `eksctl` is already installed, run the following command to upgrade:

     ```
     brew upgrade eksctl && brew link --overwrite eksctl
     ```

1. Test that your installation was successful with the following command\.

   ```
   eksctl version
   ```
**Note**  
 The `GitTag` version should be at least `0.33.0-rc.0`\. If not, check your terminal output for any installation or upgrade errors, or manually download an archive of the release from [https://github\.com/weaveworks/eksctl/releases/download/0\.33\.0\-rc\.0/eksctl\_Darwin\_amd64\.tar\.gz](https://github.com/weaveworks/eksctl/releases/download/0.33.0-rc.0/eksctl_Darwin_amd64.tar.gz), extract `eksctl`, and then execute it\.<a name="install-eksctl-linux"></a>

**\[ To install or upgrade `eksctl` on Linux using `curl` \]**

1. Download and extract the latest release of `eksctl` with the following command\.

   ```
   curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
   ```

1. Move the extracted binary to `/usr/local/bin`\.

   ```
   sudo mv /tmp/eksctl /usr/local/bin
   ```

1. Test that your installation was successful with the following command\.

   ```
   eksctl version
   ```
**Note**  
The `GitTag` version should be at least `0.33.0-rc.0`\. If not, check your terminal output for any installation or upgrade errors, or replace the address in step 1 with `https://github.com/weaveworks/eksctl/releases/download/0.33.0-rc.0/eksctl_Linux_amd64.tar.gz` and complete steps 1\-3 again\.<a name="install-eksctl-windows"></a>

**\[ To install or upgrade `eksctl` on Windows using Chocolatey \]**

1. If you do not already have Chocolatey installed on your Windows system, see [Installing Chocolatey](https://chocolatey.org/install)\.

1. Install or upgrade `eksctl` \.
   + Install the binaries with the following command:

     ```
     chocolatey install -y eksctl 
     ```
   + If they are already installed, run the following command to upgrade:

     ```
     chocolatey upgrade -y eksctl 
     ```

1. Test that your installation was successful with the following command\.

   ```
   eksctl version
   ```
**Note**  
 The `GitTag` version should be at least `0.33.0-rc.0`\. If not, check your terminal output for any installation or upgrade errors, or manually download an archive of the release from [https://github\.com/weaveworks/eksctl/releases/download/0\.33\.0\-rc\.0/eksctl\_Windows\_amd64\.zip](https://github.com/weaveworks/eksctl/releases/download/0.33.0-rc.0/eksctl_Windows_amd64.zip), extract `eksctl`, and then execute it\.

### Install and configure `kubectl`<a name="eksctl-gs-install-kubectl"></a>

Kubernetes uses the  `kubectl`  command\-line utility for communicating with the cluster API server\.

**Note**  
If you used the preceding Homebrew instructions to install `eksctl` on macOS, then `kubectl`  has already been installed on your system\. You can skip to [Create your Amazon EKS cluster and compute](#create-cluster-gs-eksctl)\.

You can install version 1\.18 of the `kubectl` command line utility for [macOS](#gs-install-kubectl-macos), [Linux](#gs-install-kubectl-linux), or [Windows](#gs-install-kubectl-windows)\. If you need to install a different version to use with a different cluster version, then see [Installing `kubectl`](install-kubectl.md)\.<a name="gs-install-kubectl-macos"></a>

**\[ To install `kubectl` on macOS \]**

1. Download the Amazon EKS vended `kubectl` binary that corresponds to the Region that your cluster is in\.
   + All Regions other than China Regions\.

     ```
     curl -o kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.18.9/2020-11-02/bin/darwin/amd64/kubectl
     ```
   + Beijing and Ningxia China Regions\.

     ```
     curl -o kubectl https://amazon-eks.s3.cn-north-1.amazonaws.com.cn/1.18.9/2020-11-02/bin/darwin/amd64/kubectl
     ```

1. \(Optional\) Verify the downloaded binary with the SHA\-256 sum\.

   1. Download the SHA\-256 sum that corresponds to the Region that your cluster is in\.
      + All Regions other than China Regions\.

        ```
        curl -o kubectl.sha256 https://amazon-eks.s3.us-west-2.amazonaws.com/1.18.9/2020-11-02/bin/darwin/amd64/kubectl.sha256
        ```
      + Beijing and Ningxia China Regions\.

        ```
        curl -o kubectl.sha256 https://amazon-eks.s3.cn-north-1.amazonaws.com.cn/1.18.9/2020-11-02/bin/darwin/amd64/kubectl.sha256
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

1. Move `kubectl` to a folder that is in your path\.
   + If you don't already have a version of  `kubectl`  installed, then move the binary to a folder that's already in your `PATH`\.

     ```
     sudo mv ./kubectl /usr/local/bin
     ```
   + If you already have a version of `kubectl` installed, then we recommend creating a `$HOME/bin/kubectl` folder, moving the binary to that folder, and ensuring that `$HOME/bin` comes first in your `$PATH`\.

     ```
     mkdir -p $HOME/bin && mv ./kubectl $HOME/bin/kubectl && export PATH=$PATH:$HOME/bin
     ```

     \(Optional\) Add the `$HOME/bin` path to your shell initialization file so that it is configured when you open a shell\.

     ```
     echo 'export PATH=$PATH:$HOME/bin' >> ~/.bash_profile
     ```

1. After you install `kubectl`, you can verify its version with the following command:

   ```
   kubectl version --short --client
   ```<a name="gs-install-kubectl-linux"></a>

**\[ To install `kubectl` on Linux \]**

1. Download the Amazon EKS vended `kubectl` binary that corresponds to the Region that your cluster is in\.
   + All Regions other than China Regions\.

     ```
     curl -o kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.18.9/2020-11-02/bin/linux/amd64/kubectl
     ```
   + Beijing and Ningxia China Regions\.

     ```
     curl -o kubectl https://amazon-eks.s3.cn-north-1.amazonaws.com.cn/1.18.9/2020-11-02/bin/linux/amd64/kubectl
     ```

1. \(Optional\) Verify the downloaded binary with the SHA\-256 sum\.

   1. Download the SHA\-256 sum that corresponds to the Region that your cluster is in\.
      + All Regions other than China Regions\.

        ```
        curl -o kubectl.sha256 https://amazon-eks.s3.us-west-2.amazonaws.com/1.18.9/2020-11-02/bin/linux/amd64/kubectl.sha256
        ```
      + Beijing and Ningxia China Regions\.

        ```
        curl -o kubectl.sha256 https://amazon-eks.s3.cn-north-1.amazonaws.com.cn/1.18.9/2020-11-02/bin/linux/amd64/kubectl.sha256
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

1. Move `kubectl` to a folder that is in your path\.
   + If you don't already have a version of `kubectl` installed, then move the binary to a folder in your `PATH`\.

     ```
     sudo mv ./kubectl /usr/local/bin
     ```
   + If you already have a version of `kubectl` installed, then we recommend creating a `$HOME/bin/kubectl` folder, moving the binary to that folder, and ensuring that `$HOME/bin` comes first in your `$PATH`\.

     ```
     mkdir -p $HOME/bin && mv ./kubectl $HOME/bin/kubectl && export PATH=$PATH:$HOME/bin
     ```

     \(Optional\) Add the `$HOME/bin` path to your shell initialization file so that it is configured when you open a shell\.

     ```
     echo 'export PATH=$PATH:$HOME/bin' >> ~/.bash_profile
     ```
**Note**  
This step assumes you are using the Bash shell; if you are using another shell, change the command to use your specific shell initialization file\.

1. After you install `kubectl`, you can verify its version with the following command:

   ```
   kubectl version --short --client
   ```<a name="gs-install-kubectl-windows"></a>

**\[ To install `kubectl` on Windows \]**

1. Open a PowerShell terminal\.

1. Download the Amazon EKS vended `kubectl` binary that corresponds to the region that your cluster is in\.
   + All Regions other than China Regions\.

     ```
     curl -o kubectl.exe https://amazon-eks.s3.us-west-2.amazonaws.com/1.18.9/2020-11-02/bin/windows/amd64/kubectl.exe
     ```
   + Beijing and Ningxia China Regions\.

     ```
     curl -o kubectl.exe https://amazon-eks.s3.cn-north-1.amazonaws.com.cn/1.18.9/2020-11-02/bin/windows/amd64/kubectl.exe
     ```

1. \(Optional\) Verify the downloaded binary with the SHA\-256 sum\.

   1. Download the SHA\-256 sum that corresponds to the region that your cluster is in\.
      + All Regions other than China Regions\.

        ```
        curl -o kubectl.exe.sha256 https://amazon-eks.s3.us-west-2.amazonaws.com/1.18.9/2020-11-02/bin/windows/amd64/kubectl.exe.sha256
        ```
      + Beijing and Ningxia China Regions\.

        ```
        curl -o kubectl.exe.sha256 https://amazon-eks.s3.cn-north-1.amazonaws.com.cn/1.18.9/2020-11-02/bin/windows/amd64/kubectl.exe.sha256
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

1. After you install `kubectl`, you can verify its version with the following command:

   ```
   kubectl version --short --client
   ```

## Create your Amazon EKS cluster and compute<a name="create-cluster-gs-eksctl"></a>

This section helps you to create an Amazon EKS cluster with a compute option to run your applications\. The latest Kubernetes version available in Amazon EKS is installed so that you can take advantage of the latest Kubernetes and Amazon EKS features\. Some features are not available on older versions of Kubernetes\.

**Important**  
Make sure that the AWS Security Token Service \(STS\) endpoint for the Region that your cluster is in is enabled for your account\. If the endpoint is not enabled, then nodes will fail to join the cluster during cluster creation\. For more information, see [Activating and deactivating AWS STS in an AWS Region](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_enable-regions.html#sts-regions-activate-deactivate)\.

Select one of the following compute options\. To learn more about each option, see [Amazon EKS nodes](eks-compute.md)\. After your cluster is deployed, you can add other options, if you choose\.
+ [Fargate – Linux](#gs-eksctl-fargate) – Select this option if you want to run Linux applications on AWS Fargate\.
+ [Managed nodes – Linux](#gs-eksctl-linux) – Select this option if you want to run Amazon Linux applications on Amazon EC2 instances
+ [Self\-managed nodes – Windows](#gs-eksctl-windows) – Select this option if you want to run Windows applications on Amazon EC2 instances\. You can also run Linux applications using this option because even if you only need to run Windows applications, your cluster must still have at least one Linux node\.

Though not covered in this guide, you can also add [Bottlerocket](http://aws.amazon.com/bottlerocket/) nodes to your cluster\. For more information, see [Launching self\-managed Bottlerocket nodes](launch-node-bottlerocket.md)\.

### \[ Fargate – Linux \]<a name="gs-eksctl-fargate"></a>

**Note**  
You can only use AWS Fargate with Amazon EKS in some Regions\. Before using Fargate with Amazon EKS, ensure that the Region that you want to use is supported\. For more information, see [Getting started with AWS Fargate using Amazon EKS](fargate-getting-started.md)\.
Do not use `eksctl` to create a cluster or nodes in an AWS Region where you have AWS Outposts, AWS Wavelength, or AWS Local Zones enabled\. Create a cluster and self\-managed nodes using the Amazon EC2 API or AWS CloudFormation instead\. For more information, see [To launch self\-managed Linux nodes using the AWS Management Console](launch-workers.md#launch-al-nodes-console) and [To launch self\-managed Windows nodes using the AWS Management Console](launch-windows-workers.md#launch-windows-nodes-console)\.

Create your Amazon EKS cluster with Fargate support with the following command\. Replace the `<example values>` \(including `<>`\) with your own values\. You can replace `<us-west-2>` with any Amazon EKS [supported Region](https://docs.aws.amazon.com/general/latest/gr/eks.html#eks_region)\. You can replace `<us-west-2>` with any [Amazon EKS Fargate supported Region](fargate.md)\. We recommend that you deploy version `1.18`, but if you replace it with an earlier version, then read the important [Amazon EKS release notes](kubernetes-versions.md) for the version and install the corresponding version of [`kubectl`](install-kubectl.md)\.

```
eksctl create cluster \
--name <my-cluster> \
--version <1.18> \
--region <us-west-2> \
--fargate
```

Your new Amazon EKS cluster is created without a node group\. `Eksctl` creates a pod execution role, a [Fargate profile](fargate-profile.md) for the `default` and `kube-system` namespaces, and it patches the `coredns` deployment so that it can run on Fargate\. For more information see [AWS Fargate](fargate.md)\.

### \[ Managed nodes – Linux \]<a name="gs-eksctl-linux"></a>

1. You can create the nodes with or without a launch template\. A launch template allows for greater customization, to include the ability to deploy a custom AMI\. For either option, replace the `<example values>` \(including `<>`\) with your own values\.

   You can replace `<us-west-2>` with any Amazon EKS [supported Region](https://docs.aws.amazon.com/general/latest/gr/eks.html#eks_region)\. We recommend that you deploy version `1.18`, but if you replace it with an earlier version, then read the important [Amazon EKS release notes](kubernetes-versions.md) for the version and install the corresponding version of [`kubectl`](install-kubectl.md)\. 

   Though `--ssh-public-key` is optional, we highly recommend that you specify it when you create your node group with a cluster\. This option enables SSH access to the nodes in your managed node group\. Enabling SSH access allows you to connect to your instances and gather diagnostic information if there are issues\. You cannot enable remote access after the node group is created\. If you don't have a public key, then you can [create a key pair](https://docs.aws.amazon.com/cli/latest/userguide/cli-services-ec2-keypairs.html#creating-a-key-pair) for Amazon EC2 to specify for `--ssh-public-key`\. Ensure that you create the key in the same Region that you create the cluster in\.
**Important**  
Do not use `eksctl` to create a cluster or nodes in an AWS Region where you have AWS Outposts, AWS Wavelength, or AWS Local Zones enabled\. Create a cluster and self\-managed nodes using the Amazon EC2 API or AWS CloudFormation instead\. For more information, see [To launch self\-managed Linux nodes using the AWS Management Console](launch-workers.md#launch-al-nodes-console) and [To launch self\-managed Windows nodes using the AWS Management Console](launch-windows-workers.md#launch-windows-nodes-console)\.
**Important**  
Amazon EKS nodes are standard Amazon EC2 instances, and you are billed for them based on normal Amazon EC2 instance prices\. For more information, see [Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/)\.
   + **Without** a launch template\.
**Note**  
Even when you don't specify your own launch template, the Amazon EKS API creates a default launch template and deploys the nodes using the launch template\.

     ```
     eksctl create cluster \
     --name <my-cluster> \
     --version <1.18> \
     --region <us-west-2> \
     --nodegroup-name <linux-nodes> \
     --nodes <3> \
     --nodes-min <1> \
     --nodes-max <4> \
     --with-oidc \
     --ssh-access \
     --ssh-public-key <name-of-ec2-keypair> \
     --managed
     ```
   + **With** a launch template – Create your Amazon EKS cluster and Amazon Linux nodes with a launch template\. The launch template must already exist and must meet the requirements specified in [Launch template configuration basics](launch-templates.md#launch-template-basics)\. Create a file with the following contents, replacing the `<example values>` \(including `<>`\) with your own values\. Several settings that you specify when deploying without a launch template are moved into the launch template\. If you don't specify a version, the template's default version is used\.

     ```
     ---
     apiVersion: eksctl.io/v1alpha5
     kind: ClusterConfig
     
     metadata:
       name: <my-cluster>
       region: <us-west-2>
       version: '<1.18>'
     iam:
       withOIDC: true 
     managedNodeGroups:
     - name: <ng-linux>
       launchTemplate:
         id: lt-<id>
         version: "<1>"
     ```

1. Create the cluster and node group with the following command\.

   ```
   eksctl create cluster --config-file <filename-you-used-in-previous-step.yaml>
   ```

   Output:

   You'll see several lines of output as the cluster and nodes are created\. The last line of output is similar to the following example line\.

   ```
   [✓]  EKS cluster "<my-cluster>" in "<us-west-2>" region is ready
   ```

   If nodes fail to join the cluster, then see [Nodes fail to join cluster](troubleshooting.md#worker-node-fail) in the Troubleshooting guide\.

### \[ Self\-managed nodes – Windows \]<a name="gs-eksctl-windows"></a>

Familiarize yourself with the Windows support [considerations](windows-support.md#considerations), which include supported values for `instanceType` in the example text below\. Replace the example <values> with your own values\.

We recommend that you deploy version `1.18`\. If you must deploy an earlier version, then you can only replace it with version `1.16` or later\. If you change `1.18`, then read the important [Amazon EKS release notes](kubernetes-versions.md) for the version and install the corresponding version of [`kubectl`](install-kubectl.md)\.

**Important**  
Do not use `eksctl` to create a cluster or nodes in an AWS Region where you have AWS Outposts, AWS Wavelength, or AWS Local Zones enabled\. Create a cluster and self\-managed nodes using the Amazon EC2 API or AWS CloudFormation instead\. For more information, see [To launch self\-managed Linux nodes using the AWS Management Console](launch-workers.md#launch-al-nodes-console) and [To launch self\-managed Windows nodes using the AWS Management Console](launch-windows-workers.md#launch-windows-nodes-console)\.

**Important**  
Amazon EKS nodes are standard Amazon EC2 instances, and you are billed for them based on normal Amazon EC2 instance prices\. For more information, see [Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/)\.

1. Create a file with the following contents, replacing the `<example values>` \(including `<>`\) with your own values\. The file will be used to create a cluster with a self\-managed Windows node group and a managed Linux node group\. Even if you only want to run Windows applications in your cluster, all Amazon EKS clusters must contain at least one Linux node, though we recommend that you create at least two Linux nodes for availability purposes\. For more information about using a [config file](https://eksctl.io/usage/creating-and-managing-clusters/#using-config-files) with `eksctl`, the [config file schema](https://eksctl.io/usage/schema/), and [config file samples](https://github.com/weaveworks/eksctl/tree/master/examples), see the `eksctl` documentation\. We recommend that you deploy version `1.18` \(but first remove the `<>`\)\. If you replace `1.18`, then read the important [Amazon EKS release notes](kubernetes-versions.md) for the version and install the corresponding version of [`kubectl`](install-kubectl.md)\.

   ```
   ---
   apiVersion: eksctl.io/v1alpha5
   kind: ClusterConfig
   
   metadata:
     name: <my-cluster>
     region: <us-west-2>
     version: '<1.18>'
   
   iam:
     withOIDC: true   
   
   managedNodeGroups:
     - name: <linux-ng>
       instanceType: <m5.large>
       minSize: <2>
   
   nodeGroups:
     - name: <windows-ng>
       instanceType: <m5.large>
       minSize: <2>
       volumeSize: <100>
       amiFamily: <WindowsServer2019FullContainer>
   ```

1. Create your Amazon EKS cluster and Windows and Linux nodes with the following command\.

   ```
   eksctl create cluster -f <filename-you-used-in-previous-step.yaml> --install-vpc-controllers
   ```
**Note**  
For more information about the available options for `eksctl create cluster`, see the project [README on GitHub](https://github.com/weaveworks/eksctl/blob/master/README.md) or view the help page with the following command\.  

   ```
   eksctl create cluster --help
   ```

   Output:

   You'll see several lines of output as the cluster and nodes are created\. The last line of output is similar to the following example line\.

   ```
   [✓]  EKS cluster "<my-cluster>" in "<us-west-2>" region is ready
   ```

   If nodes fail to join the cluster, then see [Nodes fail to join cluster](troubleshooting.md#worker-node-fail) in the Troubleshooting guide\.

   Cluster provisioning usually takes between 10 and 15 minutes\.

1. When your cluster is ready, test that your `kubectl` configuration is correct\. 

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

1. \(Linux accelerated AMI nodes only\) If you chose an accelerated AMI instance type and the Amazon EKS optimized accelerated AMI , then you must apply the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) as a DaemonSet on your cluster with the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.6.0/nvidia-device-plugin.yml
   ```

## Next steps<a name="gs-next-steps"></a>

Now that you have a working Amazon EKS cluster with nodes, you are ready to start installing Kubernetes add\-ons and deploying applications to your cluster\. The following documentation topics help you to extend the functionality of your cluster\.
+ [Restrict access to IMDS](best-practices-security.md#restrict-ec2-credential-access) – If you plan to assign IAM roles to all of your Kubernetes service accounts so that pods only have the minimum permissions that they neeed, and no pods in the cluster require access to the Amazon EC2 instance metadata service \(IMDS\) for other reasons, such as retrieving the current Region, then we recommend blocking pod access to IMDS\. For more information, see [IAM roles for service accounts](iam-roles-for-service-accounts.md) and [Restricting access to the IMDS and Amazon EC2 instance profile credentials](best-practices-security.md#restrict-ec2-credential-access)\.
+ [Cluster Autoscaler](cluster-autoscaler.md) – Configure the Kubernetes Cluster Autoscaler to automatically adjust the number of nodes in your node groups\.
+ [Deploy a sample Linux workload](sample-deployment.md) – Deploy a sample application to test your cluster and Linux nodes\.
+ [Deploy a Windows sample application](windows-support.md#windows-sample-application) – Deploy a sample application to test your cluster and Windows nodes\.
+ [Cluster management](eks-managing.md) – Learn how to use important tools for managing your cluster\.