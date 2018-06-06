# Configure kubectl for Amazon EKS<a name="configure-kubectl"></a>

Amazon EKS uses IAM to provide authentication to your Kubernetes cluster through the [Heptio Authenticator](https://github.com/heptio/authenticator)\. Beginning with Kubernetes version 1\.10, you can configure the stock kubectl client to work with Amazon EKS by installing the Heptio Authenticator and modifying your kubectl configuration file to use it for authentication\.

**To install kubectl for Amazon EKS**

1. Download and install kubectl for your operating system\. Amazon EKS vends kubectl binaries that you can use, or you can follow the instructions in the Kubernetes documentation to install\.
   + To install the Amazon EKS\-vended version of kubectl:

     1. Download the Amazon EKS\-vended kubectl binary from Amazon S3:
        + **Linux**: [https://amazon\-eks\.s3\-us\-west\-2\.amazonaws\.com/1\.10\.3/2018\-06\-05/bin/linux/amd64/kubectl](https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/bin/linux/amd64/kubectl)
        + **MacOS**: [https://amazon\-eks\.s3\-us\-west\-2\.amazonaws\.com/1\.10\.3/2018\-06\-05/bin/darwin/amd64/kubectl](https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/bin/darwin/amd64/kubectl)
        + **Windows**: [https://amazon\-eks\.s3\-us\-west\-2\.amazonaws\.com/1\.10\.3/2018\-06\-05/bin/windows/amd64/kubectl\.exe](https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/bin/windows/amd64/kubectl.exe)

        Use the command below to download the binary, substituting the correct URL for your platform\. The example below is for macOS clients\.

        ```
        curl -o kubectl https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/bin/darwin/amd64/kubectl
        ```

     1. \(Optional\) Verify the downloaded binary with the MD5 sum provided in the same bucket prefix, substituting the correct URL for your platform\. The example below is to download the MD5 sum for macOS clients\.

        ```
        curl -o kubectl.md5 https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/bin/darwin/amd64/kubectl.md5
        ```

     1. Apply execute permissions to the binary\.

        ```
        chmod +x ./kubectl
        ```

     1. Copy the binary to a folder in your `$PATH`\. If you have already installed a version of kubectl \(from Homebrew or Apt\), then we recommend creating a `$HOME/bin/kubectl` and ensuring that `$HOME/bin` comes first in your `$PATH`\.

        ```
        cp ./kubectl $HOME/bin/kubectl && export PATH=$HOME/bin:$PATH
        ```

     1. \(Optional\) Add the `$HOME/bin` path to your shell initialization file so that it is configured when you open a shell\.
        + For Bash shells on macOS:

          ```
          echo 'export PATH=$HOME/bin:$PATH' >> ~/.bash_profile
          ```
        + For Bash shells on Linux:

          ```
          echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc
          ```
   + Or, to install kubectl using the Kubernetes documentation, see [Install and Set Up kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) in the Kubernetes documentation\.

1. After you install kubectl, you can verify its version with the following command:

   ```
   kubectl version --short --client
   ```

   Example output:

   ```
   Client Version: v1.10.3
   ```

**To install `heptio-authenticator-aws` for Amazon EKS**

1. Download and install the `heptio-authenticator-aws` binary\. Amazon EKS vends `heptio-authenticator-aws` binaries that you can use, or you can use go get to fetch the binary from the [Heptio Authenticator](https://github.com/heptio/authenticator) project on GitHub for other operating systems\.
   + To download and install the Amazon EKS\-vended `heptio-authenticator-aws` binary for Linux:

     1. Download the Amazon EKS\-vended `heptio-authenticator-aws` binary from Amazon S3:
        + **Linux**: [https://amazon\-eks\.s3\-us\-west\-2\.amazonaws\.com/1\.10\.3/2018\-06\-05/bin/linux/amd64/heptio\-authenticator\-aws](https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/bin/linux/amd64/heptio-authenticator-aws)
        + **MacOS**: [https://amazon\-eks\.s3\-us\-west\-2\.amazonaws\.com/1\.10\.3/2018\-06\-05/bin/darwin/amd64/heptio\-authenticator\-aws](https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/bin/darwin/amd64/heptio-authenticator-aws)
        + **Windows**: [https://amazon\-eks\.s3\-us\-west\-2\.amazonaws\.com/1\.10\.3/2018\-06\-05/bin/windows/amd64/heptio\-authenticator\-aws\.exe](https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/bin/windows/amd64/heptio-authenticator-aws.exe)

        Use the command below to download the binary, substituting the correct URL for your platform\. The example below is for macOS clients\.

        ```
        curl -o heptio-authenticator-aws https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/bin/darwin/amd64/heptio-authenticator-aws
        ```

     1. \(Optional\) Verify the downloaded binary with the MD5 sum provided in the same bucket prefix, substituting the correct URL for your platform\. The example below is to download the MD5 sum for macOS clients\.

        ```
        curl -o heptio-authenticator-aws.md5 https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/bin/darwin/amd64/heptio-authenticator-aws.md5
        ```

     1. Apply execute permissions to the binary\.

        ```
        chmod +x ./heptio-authenticator-aws
        ```

     1. Copy the binary to a folder in your `$PATH`\. We recommend creating a `$HOME/bin/heptio-authenticator-aws` and ensuring that `$HOME/bin` comes first in your `$PATH`\.

        ```
        cp ./heptio-authenticator-aws $HOME/bin/heptio-authenticator-aws && export PATH=$HOME/bin:$PATH
        ```

     1. Add `$HOME/bin` to your `PATH` environment variable\.
        + For Bash shells on macOS:

          ```
          echo 'export PATH=$HOME/bin:$PATH' >> ~/.bash_profile
          ```
        + For Bash shells on Linux:

          ```
          echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc
          ```
   + Or, to install the `heptio-authenticator-aws` binary from GitHub using go get:

     1. Install the Go programming language for your operating system if you do not already have go installed\. For more information, see [Install the Go tools](https://golang.org/doc/install#install) in the Go documentation\.

     1. Use go get to install the `heptio-authenticator-aws` binary\.

        ```
        go get -u -v github.com/heptio/authenticator/cmd/heptio-authenticator-aws
        ```

     1. Add `$HOME/go/bin` to your `PATH` environment variable\.
        + For Bash shells on macOS:

          ```
          echo 'export PATH=$HOME/go/bin:$PATH' >> ~/.bash_profile
          ```
        + For Bash shells on Linux:

          ```
          echo 'export PATH=$HOME/go/bin:$PATH' >> ~/.bashrc
          ```

1. Test that the `heptio-authenticator-aws` binary works\.

   ```
   heptio-authenticator-aws help
   ```