# The `eksctl` command line utility<a name="eksctl"></a>

This topic covers `eksctl`, a simple command line utility for creating and managing Kubernetes clusters on Amazon EKS\. The `eksctl` command line utility provides the fastest and easiest way to create a new cluster with nodes for Amazon EKS\.

For more information and to see the official documentation, visit [https://eksctl\.io/](https://github.com/weaveworks/eksctl)\.

![\[eksctl create cluster\]](http://docs.aws.amazon.com/eks/latest/userguide/images/eksctl-create-cluster.gif)

## Installing or upgrading `eksctl`<a name="installing-eksctl"></a>

This section helps you to install or upgrade the latest version of the `eksctl` command line utility\.

You can install `eksctl` on [macOS](#install-eksctl-macos2), [Linux](#install-eksctl-linux2), or [Windows](#install-eksctl-windows2)\.<a name="install-eksctl-macos2"></a>

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
 The `GitTag` version should be at least `0.29.0-rc.1`\. If not, check your terminal output for any installation or upgrade errors, or manually download an archive of the release from [https://github\.com/weaveworks/eksctl/releases/download/0\.29\.0\-rc\.1/eksctl\_Darwin\_amd64\.tar\.gz](https://github.com/weaveworks/eksctl/releases/download/0.29.0-rc.1/eksctl_Darwin_amd64.tar.gz), extract `eksctl`, and then execute it\.<a name="install-eksctl-linux2"></a>

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
The `GitTag` version should be at least `0.29.0-rc.1`\. If not, check your terminal output for any installation or upgrade errors, or replace the address in step 1 with `https://github.com/weaveworks/eksctl/releases/download/0.29.0-rc.1/eksctl_Linux_amd64.tar.gz` and complete steps 1\-3 again\.<a name="install-eksctl-windows2"></a>

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
 The `GitTag` version should be at least `0.29.0-rc.1`\. If not, check your terminal output for any installation or upgrade errors, or manually download an archive of the release from [https://github\.com/weaveworks/eksctl/releases/download/0\.29\.0\-rc\.1/eksctl\_Windows\_amd64\.zip](https://github.com/weaveworks/eksctl/releases/download/0.29.0-rc.1/eksctl_Windows_amd64.zip), extract `eksctl`, and then execute it\.