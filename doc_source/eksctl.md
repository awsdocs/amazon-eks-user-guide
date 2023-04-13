# Installing or updating `eksctl`<a name="eksctl"></a>

This topic helps you install or update `eksctl`, a simple command line tool for creating and managing Kubernetes clusters on Amazon EKS\. `eksctl` provides the fastest and easiest way to create a new cluster with nodes for Amazon EKS\. For more information and to see the official documentation, see [https://eksctl\.io/](https://eksctl.io/)\.

`eksctl` is available from official releases as described in this section. We recommend that you install `eksctl` from only the official GitHub releases\. You may opt to use a third-party installer, but please be advised that AWS does not maintain nor support these methods of installation\. Use them at your own discretion\.

**Prerequisite**  
The `kubectl` command line tool is installed on your device or AWS CloudShell\. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster\. For example, if your cluster version is `1.24`, you can use `kubectl` version `1.23`, `1.24`, or `1.25` with it\. To install or upgrade `kubectl`, see [Installing or updating `kubectl`](install-kubectl.md)\.

**To install or update `eksctl`**

1. Determine whether you already have `eksctl` installed on your device\.

   ```
   eksctl version
   ```

   If you have `eksctl` installed in the path of your device, the example output is as follows\. If you want to update the version that you currently have installed with a later version, complete the next step, making sure to install the new version in the same location that your current version is in\.

   ```
   0.137.0
   ```

   If you receive no output, then you either don't have `eksctl` installed, or it's not installed in a location that's in your device's path\.

1. You can install `eksctl` on Unix (`macOS`, Linux), or Windows

------

### Unix<a name="install-unix"></a>

   1. Set `PLATFORM` according to the `ARCH` you are using\. 

------
#### [ Unix x86 \(64\-bit\) ]
```
PLATFORM=$(uname -s)_amd64
```
------
#### [ Unix ARM \(64\-bit\) ]
```
PLATFORM=$(uname -s)_arm64
```
------
#### [ Unix ARM \(v6\) ]
```
PLATFORM=$(uname -s)_armv6
```
------
#### [ Unix ARM \(v7\) ]
```
PLATFORM=$(uname -s)_armv7
```
------

   1. Download the latest release of `eksctl` with the following command\. 
      ```
      curl --silent --location --remote-name "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$PLATFORM.tar.gz"
      ```

      (Optional) Verifying the integrity of your downloaded archive file
      ```
      curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_checksums.txt" | grep $PLATFORM | sha256sum --check
      ```

      The output should look like `eksctl_$PLATFORM.tar.gz: OK`. 

   2. Extract and move the extracted binary to `/usr/local/bin`\.
      ```
      tar -xzf eksctl_$PLATFORM.tar.gz -C /tmp

      rm eksctl_$PLATFORM.tar.gz

      sudo mv /tmp/eksctl /usr/local/bin
      ```

   3. Test that your installation was successful with the following command\.

      ```
      eksctl version
      ```

**Note**  
The `GitTag` version should be at least `0.137.0`\. If not, check your terminal output for any installation or upgrade errors, or replace the address in step 1 with the correct one from `https://github.com/weaveworks/eksctl/releases/` and complete steps 2\-3 again\.

------

### Windows<a name="install-windows"></a>

------
#### [ Direct download (latest release) ]

[AMD64/x86_64](https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_windows_amd64.zip) - [ARMv6](https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_windows_armv6.zip) - [ARMv7](https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_windows_armv7.zip) - [ARM64](https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_windows_arm64.zip)

Make sure to unzip the archive to a folder in the `PATH` variable\. 

Optionally, verify the checksum: 

   1. Download the checksum file: [latest](https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_checksums.txt)

------
##### [ Command Prompt ]
   Use Command Prompt to manually compare `CertUtil`'s output to the checksum file downloaded\. 
   ```
   REM Replace amd64 with armv6, armv7 or arm64
   CertUtil -hashfile eksctl_Windows_amd64.zip SHA256
   ```

------
##### [ PowerShell ]
   Using PowerShell to automate the verification using the `-eq` operator to get a `True` or `False` result:
   ```
   # Replace amd64 with armv6, armv7 or arm64
   (Get-FileHash -Algorithm SHA256 .\eksctl_Windows_amd64.zip).Hash -eq ((Get-Content .\eksctl_checksums.txt) -match 'eksctl_Windows_amd64.zip' -split ' ')[0]
   ```
------

------
####  [ Using Git Bash ]
   1. Download the latest release of `eksctl` with the following command\. 
      ```
      # for ARM systems, set ARCH to: `arm64`, `armv6` or `armv7`
      ARCH=amd64
      PLATFORM=windows_$ARCH

      curl --silent --location --remote-name "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$PLATFORM.zip"

      # (Optional) Verify checksum
      curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_checksums.txt" | grep $PLATFORM | sha256sum --check
      ```

   3. Extract the binary to `$HOME/bin`, which is in `$PATH` from Git Bash\.
      ```
      unzip eksctl_$PLATFORM.zip -d $HOME/bin

      rm eksctl_$PLATFORM.zip
      ```

   4. Test that your installation was successful with the following command\.
      ```
      eksctl version
      ```
------
**Note**  
 The `GitTag` version should be at least `0.137.0`\. If not, check your terminal output for any installation or upgrade errors\. If needed, you can manually download an archive of the release from `https://github.com/weaveworks/eksctl/releases/`, extract `eksctl`, and then run it\.
