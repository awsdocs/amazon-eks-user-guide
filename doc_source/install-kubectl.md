# Installing or updating `kubectl`<a name="install-kubectl"></a>

`Kubectl` is a command line tool that you use to communicate with the Kubernetes API server\. The `kubectl` binary is available in many operating system package managers\. Using a package manager for your installation is often easier than a manual download and install process\.

This topic helps you to download and install, or update, the `kubectl` binary on your device\. The binary is identical to the [upstream community versions](https://kubernetes.io/docs/tasks/tools/#kubectl)\. The binary is not unique to Amazon EKS or AWS\.

**Note**  
You must use a `kubectl` version that is within one minor version difference of your Amazon EKS cluster control plane\. For example, a `1.23` `kubectl` client works with Kubernetes `1.22`, `1.23`, and `1.24` clusters\.

**To install or update `kubectl`**

1. Determine whether you already have `kubectl` installed on your device\.

   ```
   kubectl version | grep Client | cut -d : -f 5
   ```

   If you have `kubectl` installed in the path of your device, the example output is as follows\. If you want to update the version that you currently have installed with a later version, complete the next step, making sure to install the new version in the same location that your current version is in\.

   ```
   "version-number-eks-0123456", GitCommit
   ```

   If you receive no output, then you either don't have `kubectl` installed, or it's not installed in a location that's in your device's path\.

1. Install or update `kubectl` on `macOS`, Linux, and Windows operating systems\.

------
#### [ macOS ]<a name="install-kubectl-macos"></a>

**To install or update `kubectl` on `macOS`**

   1. Download the binary for your cluster's Kubernetes version from Amazon S3\.
      + Kubernetes `1.24`

        ```
        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.24.9/2023-01-11/bin/darwin/amd64/kubectl
        ```
      + Kubernetes `1.23`

        ```
        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.23.15/2023-01-11/bin/darwin/amd64/kubectl
        ```
      + Kubernetes `1.22`

        ```
        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.22.17/2023-01-11/bin/darwin/amd64/kubectl
        ```
      + Kubernetes `1.21`

        ```
        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.21.14/2023-01-11/bin/darwin/amd64/kubectl
        ```
      + Kubernetes `1.20`

        ```
        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.20.15/2022-10-31/bin/darwin/amd64/kubectl
        ```
      + Kubernetes `1.19`

        ```
        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.19.6/2021-01-05/bin/darwin/amd64/kubectl
        ```

   1. \(Optional\) Verify the downloaded binary with the `SHA-256` sum for your binary\.

      1. Download the `SHA-256` sum for your cluster's Kubernetes version\.
         + Kubernetes `1.24`

           ```
           curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.24.9/2023-01-11/bin/darwin/amd64/kubectl.sha256
           ```
         + Kubernetes `1.23`

           ```
           curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.23.15/2023-01-11/bin/darwin/amd64/kubectl.sha256
           ```
         + Kubernetes `1.22`

           ```
           curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.22.17/2023-01-11/bin/darwin/amd64/kubectl.sha256
           ```
         + Kubernetes `1.21`

           ```
           curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.21.14/2023-01-11/bin/darwin/amd64/kubectl.sha256
           ```
         + Kubernetes `1.20`

           ```
           curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.20.15/2022-10-31/bin/darwin/amd64/kubectl.sha256
           ```
         + Kubernetes `1.19`

           ```
           curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.19.6/2021-01-05/bin/darwin/amd64/kubectl.sha256
           ```

      1. Check the `SHA-256` sum for your downloaded binary\.

         ```
         openssl sha1 -sha256 kubectl
         ```

      1. Compare the generated `SHA-256` sum in the command output against your downloaded `SHA-256` file\. The two should match\.

   1. Apply execute permissions to the binary\.

      ```
      chmod +x ./kubectl
      ```

   1. Copy the binary to a folder in your `PATH`\. If you have already installed a version of `kubectl`, then we recommend creating a `$HOME/bin/kubectl` and ensuring that `$HOME/bin` comes first in your `$PATH`\.

      ```
      mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$HOME/bin:$PATH
      ```

   1. \(Optional\) Add the `$HOME/bin` path to your shell initialization file so that it is configured when you open a shell\.

      ```
      echo 'export PATH=$PATH:$HOME/bin' >> ~/.bash_profile
      ```

   1. After you install `kubectl`, you can verify its version with the following command:

      ```
      kubectl version --short --client
      ```

------
#### [ Linux ]<a name="install-kubectl-linux"></a>

**To install or update `kubectl` on Linux**

   1. Download the `kubectl` binary for your cluster's Kubernetes version from Amazon S3 using the command for your device's hardware platform\. The first link for each version is for `amd64` and the second link is for `arm64`\.
      + Kubernetes `1.24`

        ```
        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.24.9/2023-01-11/bin/linux/amd64/kubectl
        ```

        ```
        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.24.9/2023-01-11/bin/linux/arm64/kubectl
        ```
      + Kubernetes `1.23`

        ```
        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.23.15/2023-01-11/bin/linux/amd64/kubectl
        ```

        ```
        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.23.15/2023-01-11/bin/linux/arm64/kubectl
        ```
      + Kubernetes `1.22`

        ```
        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.22.17/2023-01-11/bin/linux/amd64/kubectl
        ```

        ```
        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.22.17/2023-01-11/bin/linux/arm64/kubectl
        ```
      + Kubernetes `1.21`

        ```
        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.21.14/2023-01-11/bin/linux/amd64/kubectl
        ```

        ```
        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.21.14/2023-01-11/bin/linux/arm64/kubectl
        ```
      + Kubernetes `1.20`

        ```
        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.20.15/2022-10-31/bin/linux/amd64/kubectl
        ```

        ```
        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.20.15/2022-10-31/bin/linux/arm64/kubectl
        ```
      + Kubernetes `1.19`

        ```
        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.19.6/2021-01-05/bin/linux/amd64/kubectl
        ```

        ```
        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.19.6/2021-01-05/bin/linux/arm64/kubectl
        ```

   1. \(Optional\) Verify the downloaded binary with the `SHA-256` sum for your binary\.

      1. Download the `SHA-256` sum for your cluster's Kubernetes version from Amazon S3 using the command for your device's hardware platform\. The first link for each version is for `amd64` and the second link is for `arm64`\.
         + Kubernetes `1.24`

           ```
           curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.24.9/2023-01-11/bin/linux/amd64/kubectl.sha256
           ```

           ```
           curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.24.9/2023-01-11/bin/linux/arm64/kubectl.sha256
           ```
         + Kubernetes `1.23`

           ```
           curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.23.15/2023-01-11/bin/linux/amd64/kubectl.sha256
           ```

           ```
           curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.23.15/2023-01-11/bin/linux/arm64/kubectl.sha256
           ```
         + Kubernetes `1.22`

           ```
           curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.22.17/2023-01-11/bin/linux/amd64/kubectl.sha256
           ```

           ```
           curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.22.17/2023-01-11/bin/linux/arm64/kubectl.sha256
           ```
         + Kubernetes `1.21`

           ```
           curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.21.14/2023-01-11/bin/linux/amd64/kubectl.sha256
           ```

           ```
           curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.21.14/2023-01-11/bin/linux/arm64/kubectl.sha256
           ```
         + Kubernetes `1.20`

           ```
           curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.20.15/2022-10-31/bin/linux/amd64/kubectl.sha256
           ```

           ```
           curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.20.15/2022-10-31/bin/linux/arm64/kubectl.sha256
           ```
         + Kubernetes `1.19`

           ```
           curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.19.6/2021-01-05/bin/linux/amd64/kubectl.sha256
           ```

           ```
           curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.19.6/2021-01-05/bin/linux/arm64/kubectl.sha256
           ```

      1. Check the `SHA-256` sum for your downloaded binary\.

         ```
         openssl sha1 -sha256 kubectl
         ```

      1. Compare the generated `SHA-256` sum in the command output against your downloaded `SHA-256` file\. The two should match\.

   1. Apply execute permissions to the binary\.

      ```
      chmod +x ./kubectl
      ```

   1. Copy the binary to a folder in your `PATH`\. If you have already installed a version of `kubectl`, then we recommend creating a `$HOME/bin/kubectl` and ensuring that `$HOME/bin` comes first in your `$PATH`\.

      ```
      mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$PATH:$HOME/bin
      ```

   1. \(Optional\) Add the `$HOME/bin` path to your shell initialization file so that it is configured when you open a shell\.
**Note**  
This step assumes you are using the Bash shell; if you are using another shell, change the command to use your specific shell initialization file\.

      ```
      echo 'export PATH=$PATH:$HOME/bin' >> ~/.bashrc
      ```

   1. After you install `kubectl`, you can verify its version with the following command:

      ```
      kubectl version --short --client
      ```

------
#### [ Windows ]<a name="install-kubectl-windows"></a>

**To install or update `kubectl` on Windows**

   1. Open a PowerShell terminal\.

   1. Download the `kubectl` binary for your cluster's Kubernetes version from Amazon S3\.
      + Kubernetes `1.24`

        ```
        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.24.9/2023-01-11/bin/windows/amd64/kubectl.exe
        ```
      + Kubernetes `1.23`

        ```
        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.23.15/2023-01-11/bin/windows/amd64/kubectl.exe
        ```
      + Kubernetes `1.22`

        ```
        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.22.17/2023-01-11/bin/windows/amd64/kubectl.exe
        ```
      + Kubernetes `1.21`

        ```
        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.21.14/2023-01-11/bin/windows/amd64/kubectl.exe
        ```
      + Kubernetes `1.20`

        ```
        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.20.15/2022-10-31/bin/windows/amd64/kubectl.exe
        ```
      + Kubernetes `1.19`

        ```
        curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.19.6/2021-01-05/bin/windows/amd64/kubectl.exe
        ```

   1. \(Optional\) Verify the downloaded binary with the `SHA-256` sum for your binary\.

      1. Download the `SHA-256` sum for your cluster's Kubernetes version for Windows\.
         + Kubernetes `1.24`

           ```
           curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.24.9/2023-01-11/bin/windows/amd64/kubectl.exe.sha256
           ```
         + Kubernetes `1.23`

           ```
           curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.23.15/2023-01-11/bin/windows/amd64/kubectl.exe.sha256
           ```
         + Kubernetes `1.22`

           ```
           curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.22.17/2023-01-11/bin/windows/amd64/kubectl.exe.sha256
           ```
         + Kubernetes `1.21`

           ```
           curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.21.14/2023-01-11/bin/windows/amd64/kubectl.exe.sha256
           ```
         + Kubernetes `1.20`

           ```
           curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.20.15/2022-10-31/bin/windows/amd64/kubectl.exe.sha256
           ```
         + Kubernetes `1.19`

           ```
           curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.19.6/2021-01-05/bin/windows/amd64/kubectl.exe.sha256
           ```

      1. Check the `SHA-256` sum for your downloaded binary\.

         ```
         Get-FileHash kubectl.exe
         ```

      1. Compare the generated `SHA-256` sum in the command output against your downloaded `SHA-256` file\. The two should match, although the PowerShell output will be uppercase\.

   1. Copy the binary to a folder in your `PATH`\. If you have an existing directory in your `PATH` that you use for command line utilities, copy the binary to that directory\. Otherwise, complete the following steps\.

      1. Create a new directory for your command line binaries, such as `C:\bin`\.

      1. Copy the `kubectl.exe` binary to your new directory\.

      1. Edit your user or system `PATH` environment variable to add the new directory to your `PATH`\.

      1. Close your PowerShell terminal and open a new one to pick up the new `PATH` variable\.

   1. After you install `kubectl`, you can verify its version with the following command:

      ```
      kubectl version --short --client
      ```

------