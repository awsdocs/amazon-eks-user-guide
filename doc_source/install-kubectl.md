# Installing `kubectl`<a name="install-kubectl"></a>

Kubernetes uses a command line utility called `kubectl` for communicating with the cluster API server\. The `kubectl` binary is available in many operating system package managers, and this option is often much easier than a manual download and install process\. You can follow the instructions for your specific operating system or package manager in the [Kubernetes documentation](https://kubernetes.io/docs/tasks/tools/install-kubectl/) to install\.

This topic helps you to download and install the Amazon EKS\-vended kubectl binaries for macOS, Linux, and Windows operating systems\.

**Note**  
You must use a `kubectl` version that is within one minor version difference of your Amazon EKS cluster control plane \. For example, a 1\.11 `kubectl` client should work with Kubernetes 1\.10, 1\.11, and 1\.12 clusters\.

------
#### [ macOS ]

**To install `kubectl` on macOS**

1. Download the Amazon EKS\-vended kubectl binary for your cluster's Kubernetes version from Amazon S3:
   + **Kubernetes 1\.13:**

     ```
     curl -o kubectl https://amazon-eks.s3-us-west-2.amazonaws.com/1.13.7/2019-06-11/bin/darwin/amd64/kubectl
     ```
   + **Kubernetes 1\.12:**

     ```
     curl -o kubectl https://amazon-eks.s3-us-west-2.amazonaws.com/1.12.7/2019-03-27/bin/darwin/amd64/kubectl
     ```
   + **Kubernetes 1\.11:**

     ```
     curl -o kubectl https://amazon-eks.s3-us-west-2.amazonaws.com/1.11.9/2019-03-27/bin/darwin/amd64/kubectl
     ```
   + **Kubernetes 1\.10:**

     ```
     curl -o kubectl https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.13/2019-03-27/bin/darwin/amd64/kubectl
     ```

1. \(Optional\) Verify the downloaded binary with the SHA\-256 sum for your binary\.

   1. Download the SHA\-256 sum for your cluster's Kubernetes version for macOS:
      + **Kubernetes 1\.13:**

        ```
        curl -o kubectl.sha256 https://amazon-eks.s3-us-west-2.amazonaws.com/1.13.7/2019-06-11/bin/darwin/amd64/kubectl.sha256
        ```
      + **Kubernetes 1\.12:**

        ```
        curl -o kubectl.sha256 https://amazon-eks.s3-us-west-2.amazonaws.com/1.12.7/2019-03-27/bin/darwin/amd64/kubectl.sha256
        ```
      + **Kubernetes 1\.11:**

        ```
        curl -o kubectl.sha256 https://amazon-eks.s3-us-west-2.amazonaws.com/1.11.9/2019-03-27/bin/darwin/amd64/kubectl.sha256
        ```
      + **Kubernetes 1\.10:**

        ```
        curl -o kubectl.sha256 https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.13/2019-03-27/bin/darwin/amd64/kubectl.sha256
        ```

   1. Check the SHA\-256 sum for your downloaded binary\.

      ```
      openssl sha1 -sha256 kubectl
      ```

   1. Compare the generated SHA\-256 sum in the command output against your downloaded SHA\-256 file\. The two should match\.

1. Apply execute permissions to the binary\.

   ```
   chmod +x ./kubectl
   ```

1. Copy the binary to a folder in your `PATH`\. If you have already installed a version of kubectl, then we recommend creating a `$HOME/bin/kubectl` and ensuring that `$HOME/bin` comes first in your `$PATH`\.

   ```
   mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$HOME/bin:$PATH
   ```

1. \(Optional\) Add the `$HOME/bin` path to your shell initialization file so that it is configured when you open a shell\.

   ```
   echo 'export PATH=$HOME/bin:$PATH' >> ~/.bash_profile
   ```

1. After you install kubectl, you can verify its version with the following command:

   ```
   kubectl version --short --client
   ```

------
#### [ Linux ]

**To install `kubectl` on Linux**

1. Download the Amazon EKS\-vended kubectl binary for your cluster's Kubernetes version from Amazon S3:
   + **Kubernetes 1\.13:**

     ```
     curl -o kubectl https://amazon-eks.s3-us-west-2.amazonaws.com/1.13.7/2019-06-11/bin/linux/amd64/kubectl
     ```
   + **Kubernetes 1\.12:**

     ```
     curl -o kubectl https://amazon-eks.s3-us-west-2.amazonaws.com/1.12.7/2019-03-27/bin/linux/amd64/kubectl
     ```
   + **Kubernetes 1\.11:**

     ```
     curl -o kubectl https://amazon-eks.s3-us-west-2.amazonaws.com/1.11.9/2019-03-27/bin/linux/amd64/kubectl
     ```
   + **Kubernetes 1\.10:**

     ```
     curl -o kubectl https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.13/2019-03-27/bin/linux/amd64/kubectl
     ```

1. \(Optional\) Verify the downloaded binary with the SHA\-256 sum for your binary\.

   1. Download the SHA\-256 sum for your cluster's Kubernetes version for Linux:
      + **Kubernetes 1\.13:**

        ```
        curl -o kubectl.sha256 https://amazon-eks.s3-us-west-2.amazonaws.com/1.13.7/2019-06-11/bin/linux/amd64/kubectl.sha256
        ```
      + **Kubernetes 1\.12:**

        ```
        curl -o kubectl.sha256 https://amazon-eks.s3-us-west-2.amazonaws.com/1.12.7/2019-03-27/bin/linux/amd64/kubectl.sha256
        ```
      + **Kubernetes 1\.11:**

        ```
        curl -o kubectl.sha256 https://amazon-eks.s3-us-west-2.amazonaws.com/1.11.9/2019-03-27/bin/linux/amd64/kubectl.sha256
        ```
      + **Kubernetes 1\.10:**

        ```
        curl -o kubectl.sha256 https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.13/2019-03-27/bin/linux/amd64/kubectl.sha256
        ```

   1. Check the SHA\-256 sum for your downloaded binary\.

      ```
      openssl sha1 -sha256 kubectl
      ```

   1. Compare the generated SHA\-256 sum in the command output against your downloaded SHA\-256 file\. The two should match\.

1. Apply execute permissions to the binary\.

   ```
   chmod +x ./kubectl
   ```

1. Copy the binary to a folder in your `PATH`\. If you have already installed a version of kubectl, then we recommend creating a `$HOME/bin/kubectl` and ensuring that `$HOME/bin` comes first in your `$PATH`\.

   ```
   mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$HOME/bin:$PATH
   ```

1. \(Optional\) Add the `$HOME/bin` path to your shell initialization file so that it is configured when you open a shell\.
**Note**  
This step assumes you are using the Bash shell; if you are using another shell, change the command to use your specific shell initialization file\.

   ```
   echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc
   ```

1. After you install kubectl, you can verify its version with the following command:

   ```
   kubectl version --short --client
   ```

------
#### [ Windows ]

**To install `kubectl` on Windows**

1. Open a PowerShell terminal\.

1. Download the Amazon EKS\-vended kubectl binary for your cluster's Kubernetes version from Amazon S3:
   + **Kubernetes 1\.13:**

     ```
     curl -o kubectl.exe https://amazon-eks.s3-us-west-2.amazonaws.com/1.13.7/2019-06-11/bin/windows/amd64/kubectl.exe
     ```
   + **Kubernetes 1\.12:**

     ```
     curl -o kubectl.exe https://amazon-eks.s3-us-west-2.amazonaws.com/1.12.7/2019-03-27/bin/windows/amd64/kubectl.exe
     ```
   + **Kubernetes 1\.11:**

     ```
     curl -o kubectl.exe https://amazon-eks.s3-us-west-2.amazonaws.com/1.11.9/2019-03-27/bin/windows/amd64/kubectl.exe
     ```
   + **Kubernetes 1\.10:**

     ```
     curl -o kubectl.exe https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.13/2019-03-27/bin/windows/amd64/kubectl.exe
     ```

1. \(Optional\) Verify the downloaded binary with the SHA\-256 sum for your binary\.

   1. Download the SHA\-256 sum for your cluster's Kubernetes version for Windows:
      + **Kubernetes 1\.13:**

        ```
        curl -o kubectl.exe.sha256 https://amazon-eks.s3-us-west-2.amazonaws.com/1.13.7/2019-06-11/bin/windows/amd64/kubectl.exe.sha256
        ```
      + **Kubernetes 1\.12:**

        ```
        curl -o kubectl.exe.sha256 https://amazon-eks.s3-us-west-2.amazonaws.com/1.12.7/2019-03-27/bin/windows/amd64/kubectl.exe.sha256
        ```
      + **Kubernetes 1\.11:**

        ```
        curl -o kubectl.exe.sha256 https://amazon-eks.s3-us-west-2.amazonaws.com/1.11.9/2019-03-27/bin/windows/amd64/kubectl.exe.sha256
        ```
      + **Kubernetes 1\.10:**

        ```
        curl -o kubectl.exe.sha256 https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.13/2019-03-27/bin/windows/amd64/kubectl.exe.sha256
        ```

   1. Check the SHA\-256 sum for your downloaded binary\.

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