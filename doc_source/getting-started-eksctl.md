# Getting Started with `eksctl`<a name="getting-started-eksctl"></a>

This getting started guide helps you to install all of the required resources to get started with Amazon EKS using `eksctl`, a simple command line utility for creating and managing Kubernetes clusters on Amazon EKS\. At the end of this tutorial, you will have a running Amazon EKS cluster with worker nodes, and the `kubectl` command line utility will be configured to use your new cluster\.

## Prerequisites<a name="eksctl-prereqs"></a>

This section helps you to install and configure the binaries you need to create and manage an Amazon EKS cluster\.

### Install the Latest AWS CLI<a name="install-awscli"></a>

To use `kubectl` with your Amazon EKS clusters, you must install a binary that can create the required client security token for cluster API server communication\. The aws eks get\-token command, available in version 1\.16\.156 or greater of the AWS CLI, supports client security token creation\. To install or upgrade the AWS CLI, see [Installing the AWS Command Line Interface](https://docs.aws.amazon.com/cli/latest/userguide/installing.html) in the *AWS Command Line Interface User Guide*\.

If you already have pip and a supported version of Python, you can install or upgrade the AWS CLI with the following command:

```
pip install awscli --upgrade --user
```

**Note**  
Your system's Python version must be 2\.7\.9 or greater\. Otherwise, you receive `hostname doesn't match` errors with AWS CLI calls to Amazon EKS\. For more information, see [What are "hostname doesn't match" errors?](http://docs.python-requests.org/en/master/community/faq/#what-are-hostname-doesn-t-match-errors) in the Python Requests FAQ\.

For more information about other methods of installing or upgrading the AWS CLI for your platform, see the following topics in the *AWS Command Line Interface User Guide*\.
+  [Install the AWS Command Line Interface on macOS](https://docs.aws.amazon.com/cli/latest/userguide/install-macos.html) 
+  [Install the AWS Command Line Interface on Linux](https://docs.aws.amazon.com/cli/latest/userguide/install-linux.html) 
+  [Install the AWS Command Line Interface on Microsoft Windows](https://docs.aws.amazon.com/cli/latest/userguide/install-windows.html) 

If you are unable to install version 1\.16\.156 or greater of the AWS CLI on your system, you must ensure that the AWS IAM Authenticator for Kubernetes is installed on your system\. For more information, see [Installing `aws-iam-authenticator`](install-aws-iam-authenticator.md)\.

### Configure Your AWS CLI Credentials<a name="configure-awscli"></a>

Both `eksctl` and the AWS CLI require that you have AWS credentials configured in your environment\. The aws configure command is the fastest way to set up your AWS CLI installation for general use\.

```
$ aws configure
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-west-2
Default output format [None]: json
```

When you type this command, the AWS CLI prompts you for four pieces of information: access key, secret access key, AWS Region, and output format\. This information is stored in a profile \(a collection of settings\) named `default`\. This profile is used unless you specify another one\.

For more information, see [Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) in the *AWS Command Line Interface User Guide*\.

### Install `eksctl`<a name="install-eksctl"></a>

This section helps you to install the `eksctl` command line utility\. For more information, see the [https://eksctl\.io/](https://github.com/weaveworks/eksctl)\.

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
The `GitTag` version should be at least `0.1.37`\. If not, check your terminal output for any installation or upgrade errors\.

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
The `GitTag` version should be at least `0.1.37`\. If not, check your terminal output for any installation or upgrade errors\.

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
The `GitTag` version should be at least `0.1.37`\. If not, check your terminal output for any installation or upgrade errors\.

------

### Install and Configure kubectl for Amazon EKS<a name="eksctl-kubectl"></a>

Kubernetes uses the `kubectl` command\-line utility for communicating with the cluster API server\.

**Note**  
If you used the preceding Homebrew instructions to install `eksctl` on macOS, then `kubectl` and the `aws-iam-authenticator` have already been installed on your system\. You can skip to [Create Your Amazon EKS Cluster and Worker Nodes](#eksctl-create-cluster)\.

**To install kubectl for Amazon EKS**
+ You have multiple options to download and install kubectl for your operating system\.
  + The `kubectl` binary is available in many operating system package managers, and this option is often much easier than a manual download and install process\. You can follow the instructions for your specific operating system or package manager in the [Kubernetes documentation](https://kubernetes.io/docs/tasks/tools/install-kubectl/) to install\.
  + Amazon EKS also vends kubectl binaries that you can use that are identical to the upstream kubectl binaries with the same version\. To install the Amazon EKS\-vended binary for your operating system, see [Installing `kubectl`](install-kubectl.md)\.

## Create Your Amazon EKS Cluster and Worker Nodes<a name="eksctl-create-cluster"></a>

Now you can create your Amazon EKS cluster and a worker node group with the `eksctl` command line utility\.

**To create your cluster and worker nodes with `eksctl`**

This procedure assumes that you have installed `eksctl`, and that your `eksctl` version is at least `0.1.37`\. You can check your version with the following command:

```
eksctl version
```

 For more information on installing or upgrading `eksctl`, see [Installing or Upgrading `eksctl`](eksctl.md#installing-eksctl)\.

1. Create your Amazon EKS cluster and worker nodes with the following command\. Substitute the red text with your own values\.
**Important**  
Kubernetes version 1\.10 is no longer supported on Amazon EKS\. You can no longer create new 1\.10 clusters, and all existing Amazon EKS clusters running Kubernetes version 1\.10 will eventually be automatically updated to the latest available platform version of Kubernetes version 1\.11\. For more information, see [Amazon EKS Version Deprecation](kubernetes-versions.md#version-deprecation)\.  
Please update any 1\.10 clusters to version 1\.11 or higher in order to avoid service interruption\. For more information, see [Updating an Amazon EKS Cluster Kubernetes Version](update-cluster.md)\.

   ```
   eksctl create cluster \
   --name prod \
   --version 1.13 \
   --nodegroup-name standard-workers \
   --node-type t3.medium \
   --nodes 3 \
   --nodes-min 1 \
   --nodes-max 4 \
   --node-ami auto
   ```
**Note**  
For more information on the available options for eksctl create cluster, see the project [README on GitHub](https://github.com/weaveworks/eksctl/blob/master/README.md) or view the help page with the following command\.  

   ```
   eksctl create cluster --help
   ```

   Output:

   ```
   [ℹ]  using region us-west-2
   [ℹ]  setting availability zones to [us-west-2b us-west-2c us-west-2d]
   [ℹ]  subnets for us-west-2b - public:192.168.0.0/19 private:192.168.96.0/19
   [ℹ]  subnets for us-west-2c - public:192.168.32.0/19 private:192.168.128.0/19
   [ℹ]  subnets for us-west-2d - public:192.168.64.0/19 private:192.168.160.0/19
   [ℹ]  nodegroup "standard-workers" will use "ami-0923e4b35a30a5f53" [AmazonLinux2/1.12]
   [ℹ]  creating EKS cluster "prod" in "us-west-2" region
   [ℹ]  will create 2 separate CloudFormation stacks for cluster itself and the initial nodegroup
   [ℹ]  if you encounter any issues, check CloudFormation console or try 'eksctl utils describe-stacks --region=us-west-2 --name=prod'
   [ℹ]  building cluster stack "eksctl-prod-cluster"
   [ℹ]  creating nodegroup stack "eksctl-prod-nodegroup-standard-workers"
   [✔]  all EKS cluster resource for "prod" had been created
   [✔]  saved kubeconfig as "/Users/ericn/.kube/config"
   [ℹ]  adding role "arn:aws:iam::111122223333:role/eksctl-prod-nodegroup-standard-wo-NodeInstanceRole-IJP4S12W3020" to auth ConfigMap
   [ℹ]  nodegroup "standard-workers" has 0 node(s)
   [ℹ]  waiting for at least 1 node(s) to become ready in "standard-workers"
   [ℹ]  nodegroup "standard-workers" has 2 node(s)
   [ℹ]  node "ip-192-168-22-17.us-west-2.compute.internal" is not ready
   [ℹ]  node "ip-192-168-32-184.us-west-2.compute.internal" is ready
   [ℹ]  kubectl command should work with "/Users/ericn/.kube/config", try 'kubectl get nodes'
   [✔]  EKS cluster "prod" in "us-west-2" region is ready
   ```

1. Cluster provisioning usually takes between 10 and 15 minutes\. When your cluster is ready, test that your `kubectl` configuration is correct\.

   ```
   kubectl get svc
   ```
**Note**  
If you receive the error `"aws-iam-authenticator": executable file not found in $PATH`, your kubectl isn't configured for Amazon EKS\. For more information, see [Installing `aws-iam-authenticator`](install-aws-iam-authenticator.md)\.  
If you receive any other authorization or resource type errors, see [Unauthorized or Access Denied \(`kubectl`\)](troubleshooting.md#unauthorized) in the troubleshooting section\.

   Output:

   ```
   NAME             TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
   svc/kubernetes   ClusterIP   10.100.0.1   <none>        443/TCP   1m
   ```

1. \(GPU workers only\) If you chose a P2 or P3 instance type and the Amazon EKS\-optimized AMI with GPU support, you must apply the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) as a DaemonSet on your cluster with the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/1.0.0-beta/nvidia-device-plugin.yml
   ```

## Next Steps<a name="eksctl-gs-next-steps"></a>

Now that you have a working Amazon EKS cluster with worker nodes, you are ready to start installing Kubernetes add\-ons and deploying applications to your cluster\. The following documentation topics help you to extend the functionality of your cluster\.
+ [Launch a Guest Book Application](eks-guestbook.md) — Create a sample guest book application to test your cluster\.
+ [Tutorial: Deploy the Kubernetes Web UI \(Dashboard\)](dashboard-tutorial.md) — This tutorial guides you through deploying the [Kubernetes dashboard](https://github.com/kubernetes/dashboard) to your cluster\.
+ [Using Helm with Amazon EKS](helm.md) — The `helm` package manager for Kubernetes helps you install and manage applications on your cluster\. 
+ [Installing the Kubernetes Metrics Server](metrics-server.md) — The Kubernetes metrics server is an aggregator of resource usage data in your cluster\.
+ [Control Plane Metrics with Prometheus](prometheus.md) — This topic helps you deploy Prometheus into your cluster with `helm`\.