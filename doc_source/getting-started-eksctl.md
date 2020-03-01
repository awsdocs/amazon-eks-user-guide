# Getting Started with `eksctl`<a name="getting-started-eksctl"></a>

This getting started guide helps you to install all of the required resources to get started with Amazon EKS using `eksctl`, a simple command line utility for creating and managing Kubernetes clusters on Amazon EKS\. At the end of this tutorial, you will have a running Amazon EKS cluster with a managed node group, and the `kubectl` command line utility will be configured to use your new cluster\.

## Prerequisites<a name="eksctl-prereqs"></a>

This section helps you to install and configure the binaries you need to create and manage an Amazon EKS cluster\.

### Install the Latest AWS CLI<a name="install-awscli"></a>

To use `kubectl` with your Amazon EKS clusters, you must install a binary that can create the required client security token for cluster API server communication\. The aws eks get\-token command, available in version 1\.18\.10 or greater of the AWS CLI, supports client security token creation\. To install or upgrade the AWS CLI, see [Installing the AWS Command Line Interface](https://docs.aws.amazon.com/cli/latest/userguide/installing.html) in the *AWS Command Line Interface User Guide*\.

If you already have pip and a supported version of Python, you can install or upgrade the AWS CLI with the following command:

```
pip install awscli --upgrade --user
```

**Note**  
Your system's Python version must be 2\.7\.9 or greater\. Otherwise, you receive `hostname doesn't match` errors with AWS CLI calls to Amazon EKS\. For more information, see [What are "hostname doesn't match" errors?](https://2.python-requests.org/projects/3/community/faq/#what-are-hostname-doesn-t-match-errors) in the Python Requests FAQ\.

For more information about other methods of installing or upgrading the AWS CLI for your platform, see the following topics in the *AWS Command Line Interface User Guide*\.
+  [Install the AWS Command Line Interface on macOS](https://docs.aws.amazon.com/cli/latest/userguide/install-macos.html) 
+  [Install the AWS Command Line Interface on Linux](https://docs.aws.amazon.com/cli/latest/userguide/install-linux.html) 
+  [Install the AWS Command Line Interface on Microsoft Windows](https://docs.aws.amazon.com/cli/latest/userguide/install-windows.html) 

If you are unable to install version 1\.18\.10 or greater of the AWS CLI on your system, you must ensure that the AWS IAM Authenticator for Kubernetes is installed on your system\. For more information, see [Installing `aws-iam-authenticator`](install-aws-iam-authenticator.md)\.

### Configure Your AWS CLI Credentials<a name="configure-awscli"></a>

Both `eksctl` and the AWS CLI require that you have AWS credentials configured in your environment\. The aws configure command is the fastest way to set up your AWS CLI installation for general use\.

```
$ aws configure
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: region-code
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
The `GitTag` version should be at least `0.14.0`\. If not, check your terminal output for any installation or upgrade errors\.

------
#### [ Linux ]

**To install or upgrade `eksctl` on Linux using `curl`**

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
The `GitTag` version should be at least `0.14.0`\. If not, check your terminal output for any installation or upgrade errors\.

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
The `GitTag` version should be at least `0.14.0`\. If not, check your terminal output for any installation or upgrade errors\.

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

**To create your cluster with `eksctl`**

1. Choose a tab below that matches your workload requirements\. If you want to create a cluster that only runs pods on AWS Fargate, choose **AWS Fargate\-only cluster**\. If you only intend to run Linux workloads on your cluster, choose **Cluster with Linux\-only workloads**\. If you want to run Linux and Windows workloads on your cluster, choose **Cluster with Linux and Windows workloads**\.

------
#### [ AWS Fargate\-only cluster ]

   This procedure assumes that you have installed `eksctl`, and that your `eksctl` version is at least `0.14.0`\. You can check your version with the following command:

   ```
   eksctl version
   ```

    For more information on installing or upgrading `eksctl`, see [Installing or Upgrading `eksctl`](eksctl.md#installing-eksctl)\.

   Create your Amazon EKS cluster with Fargate support with the following command\. Replace the example *values* with your own values\. For `--region`, specify a [supported region](fargate.md)\.

   ```
   eksctl create cluster \
   --name prod \
   --version 1.14 \
   --region region-code \
   --fargate
   ```

   Your new Amazon EKS cluster is created without a worker node group\. However, `eksctl` creates a pod execution role, a Fargate profile for the `default` and `kube-system` namespaces, and it patches the `coredns` deployment so that it can run on Fargate\. For more information see [AWS Fargate](fargate.md)\.

------
#### [ Cluster with Linux\-only workloads ]

   This procedure assumes that you have installed `eksctl`, and that your `eksctl` version is at least `0.14.0`\. You can check your version with the following command:

   ```
   eksctl version
   ```

    For more information on installing or upgrading `eksctl`, see [Installing or Upgrading `eksctl`](eksctl.md#installing-eksctl)\.

   Create your Amazon EKS cluster and Linux worker nodes with the following command\. Replace the example *values* with your own values\.

**Important**  
Kubernetes version 1\.11 and earlier are no longer supported on Amazon EKS\. You can no longer create new 1\.11 clusters, and all existing Amazon EKS clusters running Kubernetes version 1\.11 will eventually be automatically updated to the latest available platform version of Kubernetes version 1\.12\. For more information, see [Amazon EKS Version Deprecation](kubernetes-versions.md#version-deprecation)\.  
Please update any 1\.11 clusters to version 1\.12 or later in order to avoid service interruption\. For more information, see [Updating an Amazon EKS Cluster Kubernetes Version](update-cluster.md)\.  
Kubernetes API versions available through Amazon EKS are officially supported by AWS, until we remove the ability to create clusters using that version\. This is true even if upstream Kubernetes is no longer supporting a version available on Amazon EKS\. We backport security fixes that are applicable to the Kubernetes versions supported on Amazon EKS\. Existing clusters are always supported, and Amazon EKS will automatically update your cluster to a supported version if you have not done so manually by the version end of life date\.

   ```
   eksctl create cluster \
   --name prod \
   --version 1.14 \
   --region region-code \
   --nodegroup-name standard-workers \
   --node-type t3.medium \
   --nodes 3 \
   --nodes-min 1 \
   --nodes-max 4 \
   --ssh-access \
   --ssh-public-key my-public-key.pub \
   --managed
   ```

**Note**  
The `--managed` option for Amazon EKS [Managed Node Groups](managed-node-groups.md) is currently only supported on Kubernetes 1\.14 clusters\. We recommend that you use the latest version of Kubernetes that is available in Amazon EKS to take advantage of the latest features\. If you choose to use an earlier Kubernetes version, you must remove the `--managed` option\.  
For more information on the available options for eksctl create cluster, see the project [README on GitHub](https://github.com/weaveworks/eksctl/blob/master/README.md) or view the help page with the following command\.  

     ```
     eksctl create cluster --help
     ```
Though `--ssh-public-key` is optional, we highly recommend that you specify it when you create your node group with a cluster\. This option enables SSH access to the nodes in your managed node group\. Enabling SSH access allows you to connect to your instances and gather diagnostic information if there are issues\. You cannot enable remote access after the node group is created\. For more information, about keys, see [Amazon EC2 Key Pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) in the Amazon EC2 User Guide for Linux Instances\.

   Output:

   ```
   [ℹ]  eksctl version 0.11.1
   [ℹ]  using region region-code
   [ℹ]  setting availability zones to [region-codec region-codea region-coded]
   [ℹ]  subnets for region-codec - public:192.168.0.0/19 private:192.168.96.0/19
   [ℹ]  subnets for region-codea - public:192.168.32.0/19 private:192.168.128.0/19
   [ℹ]  subnets for region-coded - public:192.168.64.0/19 private:192.168.160.0/19
   [ℹ]  using SSH public key "my-public-key.pub" as "eksctl-prod-nodegroup-standard-workers-00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00"
   [ℹ]  using Kubernetes version 1.14
   [ℹ]  creating EKS cluster "prod" in "region-code" region with managed nodes
   [ℹ]  will create 2 separate CloudFormation stacks for cluster itself and the initial managed nodegroup
   [ℹ]  if you encounter any issues, check CloudFormation console or try 'eksctl utils describe-stacks --region=region-code --cluster=prod'
   [ℹ]  CloudWatch logging will not be enabled for cluster "prod" in "region-code"
   [ℹ]  you can enable it with 'eksctl utils update-cluster-logging --region=region-code --cluster=prod'
   [ℹ]  Kubernetes API endpoint access will use default of {publicAccess=true, privateAccess=false} for cluster "prod" in "region-code"
   [ℹ]  2 sequential tasks: { create cluster control plane "prod", create managed nodegroup "standard-workers" }
   [ℹ]  building cluster stack "eksctl-prod-cluster"
   [ℹ]  deploying stack "eksctl-prod-cluster"
   [ℹ]  building managed nodegroup stack "eksctl-prod-nodegroup-standard-workers"
   [ℹ]  deploying stack "eksctl-prod-nodegroup-standard-workers"
   [✔]  all EKS cluster resources for "prod" have been created
   [✔]  saved kubeconfig as "/home/user/.kube/config"
   [ℹ]  nodegroup "standard-workers" has 3 node(s)
   [ℹ]  node "ip-192-168-26-79.region-code.compute.internal" is ready
   [ℹ]  node "ip-192-168-51-105.region-code.compute.internal" is ready
   [ℹ]  node "ip-192-168-80-87.region-code.compute.internal" is ready
   [ℹ]  waiting for at least 1 node(s) to become ready in "standard-workers"
   [ℹ]  nodegroup "standard-workers" has 3 node(s)
   [ℹ]  node "ip-192-168-26-79.region-code.compute.internal" is ready
   [ℹ]  node "ip-192-168-51-105.region-code.compute.internal" is ready
   [ℹ]  node "ip-192-168-80-87.region-code.compute.internal" is ready
   [ℹ]  kubectl command should work with "/home/user/.kube/config", try 'kubectl get nodes'
   [✔]  EKS cluster "prod" in "region-code" region is ready
   ```

------
#### [ Cluster with Linux and Windows workloads ]

   This procedure assumes that you have installed `eksctl`, and that your `eksctl` version is at least `0.14.0`\. You can check your version with the following command:

   ```
   eksctl version
   ```

   For more information on installing or upgrading `eksctl`, see [Installing or Upgrading `eksctl`](eksctl.md#installing-eksctl)\.

   Familiarize yourself with the Windows support [considerations](windows-support.md#considerations), which include supported values for `instanceType` in the example text below\. Replace the example *values* with your own values\. Save the text below to a file named `cluster-spec.yaml`\. The configuration file is used to create a cluster and both Linux and Windows worker node groups\. Even if you only want to run Windows workloads in your cluster, all Amazon EKS clusters must contain at least one Linux worker node\. We recommend that you create at least two worker nodes in each node group for availability purposes\. The minimum required Kubernetes version for Windows workloads is 1\.14\.

   ```
   ---
   apiVersion: eksctl.io/v1alpha5
   kind: ClusterConfig
   
   metadata:
     name: windows-prod
     region: region-code
     version: '1.14'
   
   managedNodeGroups:
     - name: linux-ng
       instanceType: t2.large
       minSize: 2
   
   nodeGroups:
     - name: windows-ng
       instanceType: m5.large
       minSize: 2
       volumeSize: 100
       amiFamily: WindowsServer2019FullContainer
   ```

   Create your Amazon EKS cluster and Windows and Linux worker nodes with the following command\.

   ```
   eksctl create cluster -f cluster-spec.yaml --install-vpc-controllers
   ```

**Note**  
The `managedNodeGroups` option for Amazon EKS [Managed Node Groups](managed-node-groups.md) is currently only supported on Kubernetes 1\.14 clusters\. We recommend that you use the latest version of Kubernetes that is available in Amazon EKS to take advantage of the latest features\. If you choose to use an earlier Kubernetes version, you must remove the `--managed` option\.  
For more information on the available options for eksctl create cluster, see the project [README on GitHub](https://github.com/weaveworks/eksctl/blob/master/README.md) or view the help page with the following command\.  

   ```
   eksctl create cluster --help
   ```

   Output:

   ```
   [ℹ]  using region region-code
   [ℹ]  setting availability zones to [region-codea region-coded region-codec]
   [ℹ]  subnets for region-codea - public:192.168.0.0/19 private:192.168.96.0/19
   [ℹ]  subnets for region-coded - public:192.168.32.0/19 private:192.168.128.0/19
   [ℹ]  subnets for region-codec - public:192.168.64.0/19 private:192.168.160.0/19
   [ℹ]  nodegroup "linux-ng" will use "ami-076c743acc3ec4159" [AmazonLinux2/1.14]
   [ℹ]  nodegroup "windows-ng" will use "ami-0c7f1b5f1bebccac2" [WindowsServer2019FullContainer/1.14]
   [ℹ]  using Kubernetes version 1.14
   [ℹ]  creating EKS cluster "windows-cluster" in "region-code" region
   [ℹ]  2 nodegroups (linux-ng, windows-ng) were included (based on the include/exclude rules)
   [ℹ]  will create a CloudFormation stack for cluster itself and 2 nodegroup stack(s)
   [ℹ]  if you encounter any issues, check CloudFormation console or try 'eksctl utils describe-stacks --region=region-code --name=windows-cluster'
   [ℹ]  CloudWatch logging will not be enabled for cluster "windows-cluster" in "region-code"
   [ℹ]  you can enable it with 'eksctl utils update-cluster-logging --region=region-code --name=windows-cluster'
   [ℹ]  3 sequential tasks: { create cluster control plane "windows-cluster", 2 parallel sub-tasks: { create nodegroup "linux-ng", create nodegroup "windows-ng" }, install Windows VPC controller }
   [ℹ]  building cluster stack "eksctl-windows-cluster-cluster"
   [ℹ]  deploying stack "eksctl-windows-cluster-cluster"
   [ℹ]  building nodegroup stack "eksctl-windows-cluster-nodegroup-linux-ng"
   [ℹ]  building nodegroup stack "eksctl-windows-cluster-nodegroup-linux-ng"
   0m[ℹ]  --nodes-max=2 was set automatically for nodegroup windows-ng
   [ℹ]  --nodes-max=2 was set automatically for nodegroup linux-ng
   [ℹ]  deploying stack "eksctl-windows-cluster-nodegroup-windows-ng"
   [ℹ]  deploying stack "eksctl-windows-cluster-nodegroup-linux-ng"
   [ℹ]  created "ClusterRole.rbac.authorization.k8s.io/vpc-resource-controller"
   [ℹ]  created "ClusterRoleBinding.rbac.authorization.k8s.io/vpc-resource-controller"
   [ℹ]  created "kube-system:ServiceAccount/vpc-resource-controller"
   [ℹ]  created "kube-system:Deployment.apps/vpc-resource-controller"
   [ℹ]  created "CertificateSigningRequest.certificates.k8s.io/vpc-admission-webhook.kube-system"
   [ℹ]  created "kube-system:secret/vpc-admission-webhook-certs"
   [ℹ]  created "kube-system:Service/vpc-admission-webhook"
   [ℹ]  created "kube-system:Deployment.apps/vpc-admission-webhook"
   [ℹ]  created "kube-system:MutatingWebhookConfiguration.admissionregistration.k8s.io/vpc-admission-webhook-cfg"
   [✔]  all EKS cluster resources for "windows-cluster" have been created
   [✔]  saved kubeconfig as "C:\\Users\\username/.kube/config"
   [ℹ]  adding role "arn:aws:iam::123456789012:role/eksctl-windows-cluster-nodegroup-NodeInstanceRole-ZR93IIUZSYPR" to auth ConfigMap
   [ℹ]  nodegroup "linux-ng" has 0 node(s)
   [ℹ]  waiting for at least 2 node(s) to become ready in "linux-ng"
   [ℹ]  nodegroup "linux-ng" has 2 node(s)
   [ℹ]  node "ip-192-168-8-247.region-code.compute.internal" is ready
   [ℹ]  node "ip-192-168-80-253.region-code.compute.internal" is ready
   [ℹ]  adding role "arn:aws:iam::123456789012:role/eksctl-windows-cluster-nodegroup-NodeInstanceRole-XM9UZN3NXBOB" to auth ConfigMap
   [ℹ]  nodegroup "windows-ng" has 0 node(s)
   [ℹ]  waiting for at least 2 node(s) to become ready in "windows-ng"
   [ℹ]  nodegroup "windows-ng" has 2 node(s)
   [ℹ]  node "ip-192-168-4-192.region-code.compute.internal" is ready
   [ℹ]  node "ip-192-168-63-224.region-code.compute.internal" is ready
   [ℹ]  kubectl command should work with "C:\\Users\\username/.kube/config", try 'kubectl get nodes'
   [✔]  EKS cluster "windows-cluster" in "region-code" region is ready
   ```

------

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

1. \(Linux GPU workers only\) If you chose a GPU instance type and the Amazon EKS\-optimized AMI with GPU support, you must apply the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) as a DaemonSet on your cluster with the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/1.0.0-beta/nvidia-device-plugin.yml
   ```

## Next Steps<a name="eksctl-gs-next-steps"></a>

Now that you have a working Amazon EKS cluster with worker nodes, you are ready to start installing Kubernetes add\-ons and deploying applications to your cluster\. The following documentation topics help you to extend the functionality of your cluster\.
+ [Cluster Autoscaler](cluster-autoscaler.md) — Configure the Kubernetes [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler) to automatically adjust the number of nodes in your node groups\.
+ [Launch a Guest Book Application](eks-guestbook.md) — Create a sample guest book application to test your cluster and Linux worker nodes\.
+ [Deploy a Windows Sample Application](windows-support.md#windows-sample-application) — Deploy a sample application to test your cluster and Windows worker nodes\.
+ [Tutorial: Deploy the Kubernetes Web UI \(Dashboard\)](dashboard-tutorial.md) — This tutorial guides you through deploying the [Kubernetes dashboard](https://github.com/kubernetes/dashboard) to your cluster\.
+ [Using Helm with Amazon EKS](helm.md) — The `helm` package manager for Kubernetes helps you install and manage applications on your cluster\. 
+ [Installing the Kubernetes Metrics Server](metrics-server.md) — The Kubernetes metrics server is an aggregator of resource usage data in your cluster\.
+ [Control Plane Metrics with Prometheus](prometheus.md) — This topic helps you deploy Prometheus into your cluster with `helm`\.
