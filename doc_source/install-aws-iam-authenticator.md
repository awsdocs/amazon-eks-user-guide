# Installing `aws-iam-authenticator`<a name="install-aws-iam-authenticator"></a>

Amazon EKS uses IAM to provide authentication to your Kubernetes cluster through the [AWS IAM authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator)\. You can configure the stock kubectl client to work with Amazon EKS by installing the AWS IAM authenticator for Kubernetes and modifying your kubectl configuration file to use it for authentication\.

**Note**  
If you're running the AWS CLI version 1\.16\.156 or later, then you don't need to install the authenticator\. Instead, you can use the `[aws eks get\-token](https://docs.aws.amazon.com/cli/latest/reference/eks/get-token.html)` command\. For more information, see [Create `kubeconfig` manually](create-kubeconfig.md#create-kubeconfig-manually)\.

If you're unable to use the AWS CLI version 1\.16\.156 or later to create the `kubeconfig` file, then select the operating system that you want to install the `aws-iam-authenticator` on\.

## macOS<a name="macOS"></a>

**To install `aws-iam-authenticator` with Homebrew**

The easiest way to install the `aws-iam-authenticator` is with [Homebrew](https://brew.sh/)\.

1. If you do not already have [Homebrew](https://brew.sh/) installed on your Mac, install it with the following command\.

   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
   ```

1. Install the `aws-iam-authenticator` with the following command\.

   ```
   brew install aws-iam-authenticator
   ```

1. Test that the `aws-iam-authenticator` binary works\.

   ```
   aws-iam-authenticator help
   ```

**To install `aws-iam-authenticator` on macOS**

You can also install the AWS\-vended version of the `aws-iam-authenticator` by following these steps\.

1. Download the Amazon EKS\-vended `aws-iam-authenticator` binary from Amazon S3:

   ```
   curl -o aws-iam-authenticator https://amazon-eks.s3.us-west-2.amazonaws.com/1.16.8/2020-04-16/bin/darwin/amd64/aws-iam-authenticator
   ```

1. \(Optional\) Verify the downloaded binary with the SHA\-256 sum provided in the same bucket prefix\. 

   1. Download the SHA\-256 sum for your system\.

      ```
      curl -o aws-iam-authenticator.sha256 https://amazon-eks.s3.us-west-2.amazonaws.com/1.16.8/2020-04-16/bin/darwin/amd64/aws-iam-authenticator.sha256
      ```

   1. Check the SHA\-256 sum for your downloaded binary\.

      ```
      openssl sha1 -sha256 aws-iam-authenticator
      ```

   1. Compare the generated SHA\-256 sum in the command output against your downloaded `aws-iam-authenticator.sha256` file\. The two should match\.

1. Apply execute permissions to the binary\.

   ```
   chmod +x ./aws-iam-authenticator
   ```

1. Copy the binary to a folder in your `$PATH`\. We recommend creating a `$HOME/bin/aws-iam-authenticator` and ensuring that `$HOME/bin` comes first in your `$PATH`\.

   ```
   mkdir -p $HOME/bin && cp ./aws-iam-authenticator $HOME/bin/aws-iam-authenticator && export PATH=$PATH:$HOME/bin
   ```

1. Add `$HOME/bin` to your `PATH` environment variable\.

   ```
   echo 'export PATH=$PATH:$HOME/bin' >> ~/.bash_profile
   ```

1. Test that the `aws-iam-authenticator` binary works\.

   ```
   aws-iam-authenticator help
   ```

## Linux<a name="Linux"></a>

**To install `aws-iam-authenticator` on Linux**

1. Download the Amazon EKS\-vended `aws-iam-authenticator` binary from Amazon S3\. To download the ARM version, change `amd64` to `arm64` before running the command\.

   ```
   curl -o aws-iam-authenticator https://amazon-eks.s3.us-west-2.amazonaws.com/1.16.8/2020-04-16/bin/linux/amd64/aws-iam-authenticator
   ```

1. \(Optional\) Verify the downloaded binary with the SHA\-256 sum provided in the same bucket prefix\. 

   1. Download the SHA\-256 sum for your system\. To download the ARM version, change `amd64` to `arm64` before running the command\.

      ```
      curl -o aws-iam-authenticator.sha256 https://amazon-eks.s3.us-west-2.amazonaws.com/1.16.8/2020-04-16/bin/linux/amd64/aws-iam-authenticator.sha256
      ```

   1. Check the SHA\-256 sum for your downloaded binary\.

      ```
      openssl sha1 -sha256 aws-iam-authenticator
      ```

   1. Compare the generated SHA\-256 sum in the command output against your downloaded `aws-iam-authenticator.sha256` file\. The two should match\.

1. Apply execute permissions to the binary\.

   ```
   chmod +x ./aws-iam-authenticator
   ```

1. Copy the binary to a folder in your `$PATH`\. We recommend creating a `$HOME/bin/aws-iam-authenticator` and ensuring that `$HOME/bin` comes first in your `$PATH`\.

   ```
   mkdir -p $HOME/bin && cp ./aws-iam-authenticator $HOME/bin/aws-iam-authenticator && export PATH=$PATH:$HOME/bin
   ```

1. Add `$HOME/bin` to your `PATH` environment variable\.

   ```
   echo 'export PATH=$PATH:$HOME/bin' >> ~/.bashrc
   ```

1. Test that the `aws-iam-authenticator` binary works\.

   ```
   aws-iam-authenticator help
   ```

## Windows<a name="Windows"></a>

**To install `aws-iam-authenticator` on Windows with Chocolatey**

1. If you do not already have Chocolatey installed on your Windows system, see [Installing chocolatey](https://chocolatey.org/install)\.

1. Open a PowerShell terminal window and install the `aws-iam-authenticator` package with the following command:

   ```
   choco install -y aws-iam-authenticator
   ```

1. Test that the `aws-iam-authenticator` binary works\.

   ```
   aws-iam-authenticator help
   ```

**To install `aws-iam-authenticator` on Windows**

1. Open a PowerShell terminal window and download the Amazon EKS\-vended `aws-iam-authenticator` binary from Amazon S3:

   ```
   curl -o aws-iam-authenticator.exe https://amazon-eks.s3.us-west-2.amazonaws.com/1.16.8/2020-04-16/bin/windows/amd64/aws-iam-authenticator.exe
   ```

1. \(Optional\) Verify the downloaded binary with the SHA\-256 sum provided in the same bucket prefix\. 

   1. Download the SHA\-256 sum for your system\.

      ```
      curl -o aws-iam-authenticator.sha256 https://amazon-eks.s3.us-west-2.amazonaws.com/1.16.8/2020-04-16/bin/windows/amd64/aws-iam-authenticator.exe.sha256
      ```

   1. Check the SHA\-256 sum for your downloaded binary\.

      ```
      Get-FileHash aws-iam-authenticator.exe
      ```

   1. Compare the generated SHA\-256 sum in the command output against your downloaded SHA\-256 file\. The two should match, although the PowerShell output will be uppercase\.

1. Copy the binary to a folder in your `PATH`\. If you have an existing directory in your PATH that you use for command line utilities, copy the binary to that directory\. Otherwise, complete the following steps\.

   1. Create a new directory for your command line binaries, such as `C:\bin`\.

   1. Copy the `aws-iam-authenticator.exe` binary to your new directory\.

   1. Edit your user or system PATH environment variable to add the new directory to your PATH\.

   1. Close your PowerShell terminal and open a new one to pick up the new PATH variable\.

1. Test that the `aws-iam-authenticator` binary works\.

   ```
   aws-iam-authenticator help
   ```

If you have an existing Amazon EKS cluster, create a `kubeconfig` file for that cluster\. For more information, see [Create a `kubeconfig` for Amazon EKS](create-kubeconfig.md)\. Otherwise, see [Creating an Amazon EKS cluster](create-cluster.md) to create a new Amazon EKS cluster\.