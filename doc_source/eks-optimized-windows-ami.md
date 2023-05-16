# Amazon EKS optimized Windows AMIs<a name="eks-optimized-windows-ami"></a>

Windows Amazon EKS optimized AMIs are built on top of Windows Server 2019 and Windows Server 2022\. They are configured to serve as the base image for Amazon EKS nodes\. By default, the AMIs include the following components:
+ `kubelet`
+ `kube-proxy`
+ AWS IAM Authenticator
+ CSI proxy
+ Docker \(Amazon EKS version `1.23` and earlier\)
**Important**  
For Windows Amazon EKS optimized AMIs versions that include the Docker component, those that are published in September 2022 or later include the Docker CE \(Moby project\) runtime instead of the Docker EE \(Mirantis\) runtime\. For more information, see [Amazon ECS and Amazon EKS optimized Amazon Machine Images for MicrosoftWindows Server now use Docker CE runtime](http://aws.amazon.com/about-aws/whats-new/2022/10/amazon-ecs-eks-optimized-machine-images-microsoft-windows-server-docker-ce-runtime/)\.
+ `containerd` \(Amazon EKS version `1.21` and later\)

**Note**  
You can track security or privacy events for Windows Server with the [Microsoft security update guide](https://portal.msrc.microsoft.com/en-us/security-guidance)\.

Amazon EKS offers AMIs that are optimized for Windows containers in the following variants:
+ Amazon EKS\-optimized Windows Server 2019 Core AMI
+ Amazon EKS\-optimized Windows Server 2019 Full AMI
+ Amazon EKS\-optimized Windows Server 2022 Core AMI
+ Amazon EKS\-optimized Windows Server 2022 Full AMI

**Important**  
The Amazon EKS\-optimized Windows Server 20H2 Core AMI is deprecated\. No new versions of this AMI will be released\.

## Release calendar<a name="windows-ami--release-calendar"></a>

The following table lists the release and end of support dates for Windows versions on Amazon EKS\. If an end date is blank, it's because the version is still supported\.


| Windows version | Amazon EKS release | Amazon EKS end of support | 
| --- | --- | --- | 
| Windows Server 2022 Core | 10/17/2022 |  | 
| Windows Server 2022 Full | 10/17/2022 |  | 
| Windows Server 20H2 Core | 8/12/2021 | 8/9/2022 | 
| Windows Server 2004 Core | 8/19/2020 | 12/14/2021 | 
| Windows Server 2019 Core | 10/7/2019 |  | 
| Windows Server 2019 Full | 10/7/2019 |  | 
| Windows Server 1909 Core | 10/7/2019 | 12/8/2020 | 

## Bootstrap script configuration parameters<a name="bootstrap-script-configuration-parameters"></a>

When you create a Windows node, there's a script on the node that allows for configuring different parameters\. Depending on your setup, this script can be found on the node at a location similar to: `C:\Program Files\Amazon\EKS\Start-EKSBootstrap.ps1`\. You can specify custom parameter values by specifying them as arguments to the bootstrap script\. For example, you can update the user data in the launch template\. For more information, see [Amazon EC2 user data](launch-templates.md#launch-template-user-data)\.

The script includes the following parameters:
+ `-EKSClusterName` – Specifies the Amazon EKS cluster name for this worker node to join\.
+ `-KubeletExtraArgs` – Specifies extra arguments for `kubelet` \(optional\)\.
+ `-KubeProxyExtraArgs` – Specifies extra arguments for `kube-proxy` \(optional\)\.
+ `-APIServerEndpoint` – Specifies the Amazon EKS cluster API server endpoint \(optional\)\. Only valid when used with `-Base64ClusterCA`\. Bypasses calling `Get-EKSCluster`\.
+ `-Base64ClusterCA` – Specifies the base64 encoded cluster CA content \(optional\)\. Only valid when used with `-APIServerEndpoint`\. Bypasses calling `Get-EKSCluster`\.
+ `-DNSClusterIP` – Overrides the IP address to use for DNS queries within the cluster \(optional\)\. Defaults to `10.100.0.10` or `172.20.0.10` based on the IP address of the primary interface\.
+ `-ContainerRuntime` – Specifies the container runtime to be used on the node\.
+ `-ServiceCIDR` – Overrides the Kubernetes service IP address range from which cluster services are addressed\. Defaults to `172.20.0.0/16` or `10.100.0.0/16` based on the IP address of the primary interface\.
+ `-ExcludedSnatCIDRs` – A list of `IPv4` CIDRs to exclude from Source Network Address Translation \(SNAT\)\. This means that the pod private IP which is VPC addressable wouldn't be translated to the IP address of the instance ENI's primary `IPv4` address for outbound traffic\. By default, the `IPv4` CIDR of the VPC for the Amazon EKS Windows node is added\. Specifying CIDRs to this parameter also additionally excludes the specified CIDRs\. For more information, see [SNAT for Pods](external-snat.md)

## Enable the `containerd` runtime bootstrap flag<a name="containerd-bootstrap-windows"></a>

For Kubernetes version 1\.23 or earlier, you can use an optional bootstrap flag to enable the `containerd` runtime for Amazon EKS optimized Windows AMIs\. This feature gives you a clear path to migrate to `containerd` when updating to version `1.24` or later\. Amazon EKS ended support for Docker starting with the Kubernetes version `1.24` launch\. For more information, see [Amazon EKS ended support for `Dockershim`](dockershim-deprecation.md)\.

For Amazon EKS version `1.23` or earlier, the supported values for the container runtime are `docker` and `containerd`\. The container runtime is specified when launching the Windows nodes using either `eksctl` or the AWS Management Console\.
+ If the specified value is `docker` and the Amazon EKS version is `1.23` or earlier, then Docker is used as the runtime on the node\.
+ If the specified value is `containerd` and the Amazon EKS version is later than `1.20`, then `containerd` is selected as the runtime\. If the Amazon EKS version is earlier than `1.21`, then the bootstrap fails and nodes are unable to join the cluster\.
+ If any other value is specified, then the bootstrap fails and the node isn't able to join the cluster\.
+ If this flag isn't specified, then the default value of the container runtime is selected\. For Amazon EKS version `1.23` and earlier, the default is Docker\. For `1.24` and later clusters, it is `containerd`\.

When launching Windows nodes in your Amazon EKS cluster, follow the steps in [Launching self\-managed Windows nodes](launch-windows-workers.md)\. Windows self\-managed nodes with the `containerd` runtime can be launched using `eksctl` or the AWS Management Console\.

------
#### [ eksctl ]

**To enable the `containerd` runtime with `eksctl`**

For Windows self\-managed nodes, the container runtime can be specified in the configuration while creating new node groups\. You can use the following `test-windows-with-containerd.yaml` as reference\.

**Note**  
You must use `eksctl` version [https://github.com/weaveworks/eksctl/releases/tag/v0.95.0](https://github.com/weaveworks/eksctl/releases/tag/v0.95.0) or later to use the `containerRuntime` setting in the configuration file\.

```
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: windows-containerd-cluster
  region: us-west-2
  version: '1.21'

nodeGroups:
  - name: windows-ng
    instanceType: m5.2xlarge
    amiFamily: WindowsServer2019FullContainer
    volumeSize: 100
    minSize: 2
    maxSize: 3
    containerRuntime: containerd
  - name: linux-ng
    amiFamily: AmazonLinux2
    minSize: 2
    maxSize: 3
```

The node groups can then be created using the following command\.

```
eksctl create cluster -f test-windows-with-containerd.yaml
```

**Note**  
Starting with `eksctl` version `0.95`, you can no longer use `preBootstrapCommands` to configure `ContainerRuntime` for Windows nodes\.

For more information, see [Creating a nodegroup from a config file](https://eksctl.io/usage/managing-nodegroups/#creating-a-nodegroup-from-a-config-file), [defining containerd runtime](https://eksctl.io/usage/container-runtime/), and [Config file schema](https://eksctl.io/usage/schema/) in the `eksctl` documentation\.

------
#### [ AWS Management Console ]

**To enable the `containerd` runtime with the AWS Management Console**

In the AWS CloudFormation template, there's a parameter named `BootstrapArguments` which can be used to pass in additional arguments to the bootstrap script\. A parameter named `ContainerRuntime` can be used to select a particular runtime on the node\.

Specify the following in `BootstrapArguments` to enable the `containerd` runtime:

```
-ContainerRuntime containerd
```

------

## Launch self\-managed Windows Server 2022 nodes with `eksctl`<a name="self-managed-windows-server-2022"></a>

Amazon EKS optimized Windows Server 2022 AMIs are available for Kubernetes version 1\.23 or higher\. You can use the following `test-windows-2022.yaml` as reference for running Windows Server 2022 as self\-managed nodes\.

**Note**  
You must use `eksctl` version [https://github.com/weaveworks/eksctl/releases/tag/v0.116.0](https://github.com/weaveworks/eksctl/releases/tag/v0.116.0) or later to run self\-managed Windows Server 2022 nodes\.

```
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: windows-2022-cluster
  region: us-west-2
  version: '1.23'

nodeGroups:
  - name: windows-ng
    instanceType: m5.2xlarge
    amiFamily: WindowsServer2022FullContainer
    volumeSize: 100
    minSize: 2
    maxSize: 3
  - name: linux-ng
    amiFamily: AmazonLinux2
    minSize: 2
    maxSize: 3
```

The node groups can then be created using the following command\.

```
eksctl create cluster -f test-windows-2022.yaml
```

## gMSA authentication support<a name="ad-and-gmsa-support"></a>

Amazon EKS Windows Pods allow different types of group Managed Service Account \(gMSA\) authentication\.
+ Amazon EKS supports Active Directory domain identities for authentication\. For more information on domain\-joined gMSA, see [Windows Authentication on Amazon EKS Windowspods](http://aws.amazon.com/blogs/containers/windows-authentication-on-amazon-eks-windows-pods/) on the AWS blog\.
+ Amazon EKS offers a plugin that enables non\-domain\-joined Windows nodes to retrieve gMSA credentials with a portable user identity\. For more information on domainless gMSA, see [Domainless Windows Authentication for Amazon EKS Windowspods](http://aws.amazon.com/blogs/containers/domainless-windows-authentication-for-amazon-eks-windows-pods/) on the AWS blog\.

## Cached container images<a name="windows-cached-container-images"></a>

Amazon EKS Windows optimized AMIs have certain container images cached for both the `docker` and `containerd` runtimes\. Container images are cached when building custom AMIs using Amazon\-managed build components\. For more information, see [Using the Amazon\-managed build component](eks-custom-ami-windows.md#custom-windows-ami-build-component)\.

### For Amazon EKS `1.23` and lower<a name="windows-cached-1.23-and-lower"></a>

The `docker` runtime is the default and has the following container images cached on Amazon EKS Windows AMIs\. Retrieve this image list by running `docker` images on the Amazon EKS Windows node:
+ `amazonaws.com/eks/pause-windows`
+ `mcr.microsoft.com/windows/nanoserver`
+ `mcr.microsoft.com/windows/servercore`

 The `containerd` runtime only has one container image\. Retrieve this image list by running `ctr -n k8s.io images list`:
+ `amazonaws.com/eks/pause-windows`

### For Amazon EKS `1.24` and higher<a name="windows-cached-1.24-and-higher"></a>

There is no `docker` runtime\. The following cached container images are for the `containerd` runtime:
+ `amazonaws.com/eks/pause-windows`
+ `mcr.microsoft.com/windows/nanoserver`
+ `mcr.microsoft.com/windows/servercore`

## More information<a name="windows-more-information"></a>

For more information about using Amazon EKS optimized Windows AMIs, see the following sections:
+ To use Windows with managed node groups, see [Managed node groups](managed-node-groups.md)\.
+ To launch self\-managed Windows nodes, see [Launching self\-managed Windows nodes](launch-windows-workers.md)\.
+ For version information, see [Amazon EKS optimized Windows AMI versions](eks-ami-versions-windows.md)\.
+ To retrieve the latest IDs of the Amazon EKS optimized Windows AMIs, see [Retrieving Amazon EKS optimized Windows AMI IDs](retrieve-windows-ami-id.md)\.
+ To use Amazon EC2 Image Builder to create custom Amazon EKS optimized Windows AMIs, see [Creating custom Amazon EKS optimized Windows AMIs](eks-custom-ami-windows.md)\.