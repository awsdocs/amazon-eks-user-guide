# Amazon EKS optimized Windows AMIs<a name="eks-optimized-windows-ami"></a>

Windows Amazon EKS optimized AMIs are built on top of Windows Server 2019 and Windows Server 2022\. They are configured to serve as the base image for Amazon EKS nodes\. By default, the AMIs include the following components:
+ [https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/)
+ [https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/)
+ [AWS IAM Authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator)
+ [https://github.com/kubernetes-csi/csi-proxy](https://github.com/kubernetes-csi/csi-proxy)
+ [https://containerd.io/](https://containerd.io/)

**Note**  
You can track security or privacy events for Windows Server with the [Microsoft security update guide](https://portal.msrc.microsoft.com/en-us/security-guidance)\.

Amazon EKS offers AMIs that are optimized for Windows containers in the following variants:
+ Amazon EKS\-optimized Windows Server 2019 Core AMI
+ Amazon EKS\-optimized Windows Server 2019 Full AMI
+ Amazon EKS\-optimized Windows Server 2022 Core AMI
+ Amazon EKS\-optimized Windows Server 2022 Full AMI

**Important**  
The Amazon EKS\-optimized Windows Server 20H2 Core AMI is deprecated\. No new versions of this AMI will be released\.
To ensure that you have the latest security updates by default, Amazon EKS maintains optimized Windows AMIs for the last 4 months\. Each new AMI will be available for 4 months from the time of initial release\. After this period, older AMIs are made private and are no longer accessible\. We encourage using the latest AMIs to avoid security vulnerabilities and losing access to older AMIs which have reached the end of their supported lifetime\. While we can't guarantee that we can provide access to AMIs that have been made private, you can request access by filing a ticket with AWS Support\.

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

The script includes the following command\-line parameters:
+ `-EKSClusterName` – Specifies the Amazon EKS cluster name for this worker node to join\.
+ `-KubeletExtraArgs` – Specifies extra arguments for `kubelet` \(optional\)\.
+ `-KubeProxyExtraArgs` – Specifies extra arguments for `kube-proxy` \(optional\)\.
+ `-APIServerEndpoint` – Specifies the Amazon EKS cluster API server endpoint \(optional\)\. Only valid when used with `-Base64ClusterCA`\. Bypasses calling `Get-EKSCluster`\.
+ `-Base64ClusterCA` – Specifies the base64 encoded cluster CA content \(optional\)\. Only valid when used with `-APIServerEndpoint`\. Bypasses calling `Get-EKSCluster`\.
+ `-DNSClusterIP` – Overrides the IP address to use for DNS queries within the cluster \(optional\)\. Defaults to `10.100.0.10` or `172.20.0.10` based on the IP address of the primary interface\.
+ `-ServiceCIDR` – Overrides the Kubernetes service IP address range from which cluster services are addressed\. Defaults to `172.20.0.0/16` or `10.100.0.0/16` based on the IP address of the primary interface\.
+ `-ExcludedSnatCIDRs` – A list of `IPv4` CIDRs to exclude from Source Network Address Translation \(SNAT\)\. This means that the pod private IP which is VPC addressable wouldn't be translated to the IP address of the instance ENI's primary `IPv4` address for outbound traffic\. By default, the `IPv4` CIDR of the VPC for the Amazon EKS Windows node is added\. Specifying CIDRs to this parameter also additionally excludes the specified CIDRs\. For more information, see [SNAT for Pods](external-snat.md)\.

In addition to the command line parameters, you can also specify some environment variable parameters\. When specifying a command line parameter, it takes precedence over the respective environment variable\. The environment variable\(s\) should be defined as machine \(or system\) scoped as the bootstrap script will only read machine\-scoped variables\.

The script takes into account the following environment variables:
+ `SERVICE_IPV4_CIDR` – Refer to the `ServiceCIDR` command line parameter for the definition\. 
+ `EXCLUDED_SNAT_CIDRS` – Should be a comma separated string\. Refer to the `ExcludedSnatCIDRs` command line parameter for the definition\.

## Launch self\-managed Windows Server 2022 nodes with `eksctl`<a name="self-managed-windows-server-2022"></a>

You can use the following `test-windows-2022.yaml` as reference for running Windows Server 2022 as self\-managed nodes\. Replace every `example value` with your own values\.

**Note**  
You must use `eksctl` version [https://github.com/weaveworks/eksctl/releases/tag/v0.116.0](https://github.com/weaveworks/eksctl/releases/tag/v0.116.0) or later to run self\-managed Windows Server 2022 nodes\.

```
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: windows-2022-cluster
  region: region-code
  version: '1.29'

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
+ Amazon EKS supports Active Directory domain identities for authentication\. For more information on domain\-joined gMSA, see [Windows Authentication on Amazon EKS Windowspods](https://aws.amazon.com/blogs/containers/windows-authentication-on-amazon-eks-windows-pods/) on the AWS blog\.
+ Amazon EKS offers a plugin that enables non\-domain\-joined Windows nodes to retrieve gMSA credentials with a portable user identity\. For more information on domainless gMSA, see [Domainless Windows Authentication for Amazon EKS Windowspods](https://aws.amazon.com/blogs/containers/domainless-windows-authentication-for-amazon-eks-windows-pods/) on the AWS blog\.

## Cached container images<a name="windows-cached-container-images"></a>

Amazon EKS Windows optimized AMIs have certain container images cached for the `containerd` runtime\. Container images are cached when building custom AMIs using Amazon\-managed build components\. For more information, see [Using the Amazon\-managed build component](eks-custom-ami-windows.md#custom-windows-ami-build-component)\.

The following cached container images are for the `containerd` runtime:
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
+ For best practices, see [Amazon EKS optimized Windows AMI management](https://aws.github.io/aws-eks-best-practices/windows/docs/ami/) in the *EKS Best Practices Guide*\.