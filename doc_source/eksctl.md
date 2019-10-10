# The `eksctl` Command Line Utility<a name="eksctl"></a>

This chapter covers `eksctl`, a simple command line utility for creating and managing Kubernetes clusters on Amazon EKS\. The `eksctl` command line utility provides the fastest and easiest way to create a new cluster with worker nodes for Amazon EKS\.

For more information and to see the official documentation, visit [https://eksctl\.io/](https://github.com/weaveworks/eksctl)\.

![\[eksctl create cluster\]](http://docs.aws.amazon.com/eks/latest/userguide/images/eksctl-create-cluster.gif)

## Installing or Upgrading `eksctl`<a name="installing-eksctl"></a>

This section helps you to install or upgrade the `eksctl` command line utility\.

Choose the tab below that best represents your client setup\.

------
#### [ macOS ]

**To install or upgrade `eksctl` on macOS using Homebrew**

The easiest way to get started with Amazon EKS and macOS is by installing `eksctl` with [Homebrew](https://brew.sh/)\. The `eksctl` Homebrew recipe installs `eksctl` and any other dependencies that are required for Amazon EKS, such as `kubectl` and the `aws-iam-authenticator`\. 

1. If you do not already have Homebrew installed on macOS, install it with the following command\.

   ```
   /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
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
The `GitTag` version should be at least `0.6.0`\. If not, check your terminal output for any installation or upgrade errors\.

------
#### [ Linux ]

**To install or upgrade `eksctl` on Linux using `curl`**

1. Download and extract the latest release of `eksctl` with the following command\.

   ```
   curl --silent --location "https://github.com/weaveworks/eksctl/releases/download/latest_release/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
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
The `GitTag` version should be at least `0.6.0`\. If not, check your terminal output for any installation or upgrade errors\.

------
#### [ Windows ]

**To install or upgrade `eksctl` on Windows using Chocolatey**

1. If you do not already have Chocolatey installed on your Windows system, see [Installing Chocolatey](https://chocolatey.org/install)\.

1. Install or upgrade `eksctl` and the `aws-iam-authenticator`\.
   + Install the binaries with the following command:

     ```
     chocolatey install -y eksctl aws-iam-authenticator
     ```
   + If they are already installed, run the following command to upgrade:

     ```
     chocolatey upgrade -y eksctl aws-iam-authenticator
     ```

1. Test that your installation was successful with the following command\.

   ```
   eksctl version
   ```
**Note**  
The `GitTag` version should be at least `0.6.0`\. If not, check your terminal output for any installation or upgrade errors\.

------