# Installing `aws-iam-authenticator`<a name="install-aws-iam-authenticator"></a>

Amazon EKS uses IAM to provide authentication to your Kubernetes cluster through the [AWS IAM authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator/blob/master/README.md)\. You can configure the stock `kubectl` client to work with Amazon EKS by installing the AWS IAM authenticator for Kubernetes and [modifying your `kubectl` configuration file](create-kubeconfig.md) to use it for authentication\.

**Note**  
If you're running the AWS CLI version `1.16.156` or later, then you don't need to install the authenticator\. Instead, you can use the `[aws eks get\-token](https://docs.aws.amazon.com/cli/latest/reference/eks/get-token.html)` command\. For more information, see [Create `kubeconfig` file manually](create-kubeconfig.md#create-kubeconfig-manually)\.

If you're unable to use the AWS CLI version `1.16.156` or later to create the `kubeconfig` file, then you can install the AWS IAM authenticator for Kubernetes on macOS, Linux, or Windows\.

------
#### [ macOS ]

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

You can also install the `aws-iam-authenticator` by following these steps\.

1. Download the `aws-iam-authenticator` binary from GitHub for your hardware platform\. The first command downloads the `amd64` release\. The second command downloads the `arm64` release\.

   ```
   curl -Lo aws-iam-authenticator https://github.com/kubernetes-sigs/aws-iam-authenticator/releases/download/v0.6.11/aws-iam-authenticator_0.6.11_darwin_amd64
   ```

   ```
   curl -Lo aws-iam-authenticator https://github.com/kubernetes-sigs/aws-iam-authenticator/releases/download/v0.6.11/aws-iam-authenticator_0.6.11_darwin_arm64
   ```

1. \(Optional\) Verify the downloaded binary with the `SHA-256` checksum for the file\. 

   1. Download the `SHA-256` checksum file\.

      ```
      curl -Lo aws-iam-authenticator.txt https://github.com/kubernetes-sigs/aws-iam-authenticator/releases/download/v0.6.11/authenticator_0.6.11_checksums.txt
      ```

   1. View the checksum for the authenticator binary that you downloaded\. The first command returns the `amd64` checksum\. The second command returns the `arm64` checksum\.

      ```
      awk '/aws-iam-authenticator_0.6.11_darwin_amd64/ {print $1}' aws-iam-authenticator.txt
      ```

      ```
      awk '/aws-iam-authenticator_0.6.11_darwin_arm64/ {print $1}' aws-iam-authenticator.txt
      ```

      An example output is as follows\.

      ```
      7656bd290a7e9cb588df1d9ccec43fab7f2447b88ed4f41d3f5092fd114b0939
      ```

   1. Determine the `SHA-256` checksum for your downloaded binary\.

      ```
      openssl sha1 -sha256 aws-iam-authenticator
      ```

      An example output is as follows\.

      ```
      SHA256(aws-iam-authenticator)= 7656bd290a7e9cb588df1d9ccec43fab7f2447b88ed4f41d3f5092fd114b0939
      ```

      The returned output should match the output returned in the previous step\.

1. Apply execute permissions to the binary\.

   ```
   chmod +x ./aws-iam-authenticator
   ```

1. Copy the binary to a folder in your `$PATH`\. We recommend creating a `$HOME/bin/aws-iam-authenticator` and ensuring that `$HOME/bin` comes first in your `$PATH`\.

   ```
   mkdir -p $HOME/bin && cp ./aws-iam-authenticator $HOME/bin/aws-iam-authenticator && export PATH=$HOME/bin:$PATH
   ```

1. Add `$HOME/bin` to your `PATH` environment variable\.

   ```
   echo 'export PATH=$HOME/bin:$PATH' >> ~/.bash_profile
   ```

1. Test that the `aws-iam-authenticator` binary works\.

   ```
   aws-iam-authenticator help
   ```

------
#### [ Linux ]

**To install `aws-iam-authenticator` on Linux**

1. Download the `aws-iam-authenticator` binary from GitHub for your hardware platform\. The first command downloads the `amd64` release\. The second command downloads the `arm64` release\.

   ```
   curl -Lo aws-iam-authenticator https://github.com/kubernetes-sigs/aws-iam-authenticator/releases/download/v0.6.11/aws-iam-authenticator_0.6.11_linux_amd64
   ```

   ```
   curl -Lo aws-iam-authenticator https://github.com/kubernetes-sigs/aws-iam-authenticator/releases/download/v0.6.11/aws-iam-authenticator_0.6.11_linux_arm64
   ```

1. \(Optional\) Verify the downloaded binary with the `SHA-256` checksum for the file\. 

   1. Download the `SHA-256` checksum file\.

      ```
      curl -Lo aws-iam-authenticator.txt https://github.com/kubernetes-sigs/aws-iam-authenticator/releases/download/v0.6.11/authenticator_0.6.11_checksums.txt
      ```

   1. View the checksum for the authenticator binary that you downloaded\. The first command returns the `amd64` checksum\. The second command returns the `arm64` checksum\.

      ```
      awk '/aws-iam-authenticator_0.6.11_linux_amd64/ {print $1}' aws-iam-authenticator.txt
      ```

      ```
      awk '/aws-iam-authenticator_0.6.11_linux_arm64/ {print $1}' aws-iam-authenticator.txt
      ```

      An example output is as follows\.

      ```
      b192431c22d720c38adbf53b016c33ab17105944ee73b25f485aa52c9e9297a7
      ```

   1. Determine the `SHA-256` checksum for your downloaded binary\.

      ```
      openssl sha1 -sha256 aws-iam-authenticator
      ```

      An example output is as follows\.

      ```
      SHA256(aws-iam-authenticator)= b192431c22d720c38adbf53b016c33ab17105944ee73b25f485aa52c9e9297a7
      ```

      The returned output should match the output returned in the previous step\.

1. Apply execute permissions to the binary\.

   ```
   chmod +x ./aws-iam-authenticator
   ```

1. Copy the binary to a folder in your `$PATH`\. We recommend creating a `$HOME/bin/aws-iam-authenticator` and ensuring that `$HOME/bin` comes first in your `$PATH`\.

   ```
   mkdir -p $HOME/bin && cp ./aws-iam-authenticator $HOME/bin/aws-iam-authenticator && export PATH=$HOME/bin:$PATH
   ```

1. Add `$HOME/bin` to your `PATH` environment variable\.

   ```
   echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc
   ```

1. Test that the `aws-iam-authenticator` binary works\.

   ```
   aws-iam-authenticator help
   ```

------
#### [ Windows ]

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

1. Open a PowerShell terminal window and download the `aws-iam-authenticator` binary from GitHub\.

   ```
   curl -Lo aws-iam-authenticator.exe https://github.com/kubernetes-sigs/aws-iam-authenticator/releases/download/v0.6.11/aws-iam-authenticator_0.6.11_windows_amd64.exe
   ```

1. \(Optional\) Verify the downloaded binary with the `SHA-256` checksum for the file\. 

   1. Download the `SHA-256` checksum file\.

      ```
      curl -Lo aws-iam-authenticator.txt https://github.com/kubernetes-sigs/aws-iam-authenticator/releases/download/v0.6.11/authenticator_0.6.11_checksums.txt
      ```

   1. View the checksum for the authenticator binary that you downloaded\.

      ```
      $checksum = Get-Content aws-iam-authenticator.txt
      $checksum[3]
      ```

      An example output is as follows\.

      ```
      b7345e06c5f1d31b9459a38baffe0744343711cb5042cb31ff1e072d870c42f9  aws-iam-authenticator_0.6.11_windows_amd64.exe
      ```

   1. Determine the `SHA-256` checksum for your downloaded binary\.

      ```
      Get-Filehash aws-iam-authenticator.exe
      ```

      An example output is as follows\.

      ```
      Algorithm       Hash                                                                   Path
      ---------       ----                                                                   ----
      SHA256          B7345E06C5F1D31B9459A38BAFFE0744343711CB5042CB31FF1E072D870C42F9       /home/cloudshell-user/temp/aws-iam-authenticator
      ```

      Though the returned output is uppercase, it should match the lowercase output returned in the previous step\.

1. Copy the binary to a folder in your `PATH`\. If you have an existing directory in your PATH that you use for command line utilities, copy the binary to that directory\. Otherwise, complete the following steps\.

   1. Create a new directory for your command line binaries, such as `C:\bin`\.

   1. Copy the `aws-iam-authenticator.exe` binary to your new directory\.

   1. Edit your user or system `PATH` environment variable to add the new directory to your `PATH`\.

   1. Close your PowerShell terminal and open a new one to pick up the new `PATH` variable\.

1. Test that the `aws-iam-authenticator` binary works\.

   ```
   aws-iam-authenticator help
   ```

------

If you have an existing Amazon EKS cluster, create a `kubeconfig` file for that cluster\. For more information, see [Creating or updating a `kubeconfig` file for an Amazon EKS cluster](create-kubeconfig.md)\. Otherwise, see [Creating an Amazon EKS cluster](create-cluster.md) to create a new Amazon EKS cluster\.
