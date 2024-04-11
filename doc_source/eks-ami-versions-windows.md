# Amazon EKS optimized Windows AMI versions<a name="eks-ami-versions-windows"></a>

**Important**  
Extended Support for Amazon EKS optimized Windows AMIs that are published by AWS isn't available for Kubernetes version `1.23` but is available for Kubernetes version `1.24` and higher\.

This topic lists versions of the Amazon EKS optimized Windows AMIs and their corresponding versions of [https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/), [https://containerd.io/](https://containerd.io/), and [https://github.com/kubernetes-csi/csi-proxy](https://github.com/kubernetes-csi/csi-proxy)\.

The Amazon EKS optimized AMI metadata, including the AMI ID, for each variant can be retrieved programmatically\. For more information, see [Retrieving Amazon EKS optimized Windows AMI IDs](retrieve-windows-ami-id.md)\.

AMIs are versioned by Kubernetes version and the release date of the AMI in the following format:

```
k8s_major_version.k8s_minor_version-release_date
```

**Note**  
Amazon EKS managed node groups support the November 2022 and later releases of the Windows AMIs\.

## Amazon EKS optimized Windows Server 2022 Core AMI<a name="eks-ami-versions-windows-2022-core"></a>

The following tables list the current and previous versions of the Amazon EKS optimized Windows Server 2022 Core AMI\.

------
#### [ Kubernetes version 1\.29 ]


**Kubernetes version `1.29`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.29\-2024\.04\.09 | 1\.29\.0 | 1\.6\.28 | 1\.1\.2 | Upgraded containerd to 1\.6\.28\. Rebuilt CNI and csi\-proxy using golang 1\.22\.1\. | 
| 1\.29\-2024\.03\.12 | 1\.29\.0 | 1\.6\.25 | 1\.1\.2 |  | 
| 1\.29\-2024\.02\.13 | 1\.29\.0 | 1\.6\.25 | 1\.1\.2 |  | 
| 1\.29\-2024\.02\.06  | 1\.29\.0 | 1\.6\.25 | 1\.1\.2 | Fixed a bug where the pause image was incorrectly deleted by kubelet garbage collection process\. | 
| 1\.29\-2024\.01\.11  | 1\.29\.0 | 1\.6\.18 | 1\.1\.2 | Excluded Standalone Windows Update [KB5034439](https://support.microsoft.com/en-au/topic/kb5034439-windows-recovery-environment-update-for-azure-stack-hci-version-22h2-and-windows-server-2022-january-9-2024-6f9d26e6-784c-4503-a3c6-0beedda443ca) on Windows Server 2022 Core AMIs\. The KB applies only to Windows installations with a separate WinRE partition, which aren't included with any of our Amazon EKS Optimized Windows AMIs\. | 

------
#### [ Kubernetes version 1\.28 ]


**Kubernetes version `1.28`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.28\-2024\.04\.09 | 1\.28\.5 | 1\.6\.25 | 1\.1\.2 | Upgraded containerd to 1\.6\.25\. Rebuilt CNI and csi\-proxy using golang 1\.22\.1\. | 
| 1\.28\-2024\.03\.12 | 1\.28\.5 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.28\-2024\.02\.13 | 1\.28\.5 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.28\-2024\.01\.11  | 1\.28\.5 | 1\.6\.18 | 1\.1\.2 | Excluded Standalone Windows Update [KB5034439](https://support.microsoft.com/en-au/topic/kb5034439-windows-recovery-environment-update-for-azure-stack-hci-version-22h2-and-windows-server-2022-january-9-2024-6f9d26e6-784c-4503-a3c6-0beedda443ca) on Windows Server 2022 Core AMIs\. The KB applies only to Windows installations with a separate WinRE partition, which aren't included with any of our Amazon EKS Optimized Windows AMIs\. | 
| 1\.28\-2023\.12\.12 | 1\.28\.3 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.28\-2023\.11\.14 | 1\.28\.3 | 1\.6\.18 | 1\.1\.2 | Includes patches for CVE\-2023\-5528\. | 
| 1\.28\-2023\.10\.19 | 1\.28\.2 | 1\.6\.18 | 1\.1\.2 | Upgraded containerd to 1\.6\.18\. Added new [bootstrap script environment variables](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(SERVICE\_IPV4\_CIDR and EXCLUDED\_SNAT\_CIDRS\)\. | 
| 1\.28\-2023\-09\.27 | 1\.28\.2 | 1\.6\.6 | 1\.1\.2 | Fixed a [security advisory](https://github.com/advisories/GHSA-6xv5-86q9-7xr8) in kubelet\. | 
| 1\.28\-2023\.09\.12 | 1\.28\.1 | 1\.6\.6 | 1\.1\.2 |  | 

------
#### [ Kubernetes version 1\.27 ]


**Kubernetes version `1.27`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.27\-2024\.04\.09 | 1\.27\.9 | 1\.6\.25 | 1\.1\.2 | Upgraded containerd to 1\.6\.25\. Rebuilt CNI and csi\-proxy using golang 1\.22\.1\. | 
| 1\.27\-2024\.03\.12 | 1\.27\.9 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.27\-2024\.02\.13 | 1\.27\.9 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.27\-2024\.01\.11 | 1\.27\.9 | 1\.6\.18 | 1\.1\.2 | Excluded Standalone Windows Update [KB5034439](https://support.microsoft.com/en-au/topic/kb5034439-windows-recovery-environment-update-for-azure-stack-hci-version-22h2-and-windows-server-2022-january-9-2024-6f9d26e6-784c-4503-a3c6-0beedda443ca) on Windows Server 2022 Core AMIs\. The KB applies only to Windows installations with a separate WinRE partition, which aren't included with any of our Amazon EKS Optimized Windows AMIs\. | 
| 1\.27\-2023\.12\.12 | 1\.27\.7 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.27\-2023\.11\.14 | 1\.27\.7 | 1\.6\.18 | 1\.1\.2 | Includes patches for CVE\-2023\-5528\. | 
| 1\.27\-2023\.10\.19 | 1\.27\.6 | 1\.6\.18 | 1\.1\.2 | Upgraded containerd to 1\.6\.18\. Added new [bootstrap script environment variables](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(SERVICE\_IPV4\_CIDR and EXCLUDED\_SNAT\_CIDRS\)\. | 
| 1\.27\-2023\-09\.27 | 1\.27\.6 | 1\.6\.6 | 1\.1\.2 | Fixed a [security advisory](https://github.com/advisories/GHSA-6xv5-86q9-7xr8) in kubelet\. | 
| 1\.27\-2023\.09\.12 | 1\.27\.4 | 1\.6\.6 | 1\.1\.2 | Upgraded the Amazon VPC CNI plugin to use the Kubernetes connector binary, which gets the Pod IP address from the Kubernetes API server\. Merged [pull request \#100](https://github.com/aws/amazon-vpc-cni-plugins/pull/100)\. | 
| 1\.27\-2023\.08\.17 | 1\.27\.4 | 1\.6\.6 | 1\.1\.2 | Includes patches for CVE\-2023\-3676, CVE\-2023\-3893, and CVE\-2023\-3955\. | 
| 1\.27\-2023\.08\.08 | 1\.27\.3 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.27\-2023\.07\.11 | 1\.27\.3 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.27\-2023\.06\.20 | 1\.27\.1 | 1\.6\.6 | 1\.1\.1 | Resolved issue that was causing the DNS suffix search list to be incorrectly populated\. | 
| 1\.27\-2023\.06\.14 | 1\.27\.1 | 1\.6\.6 | 1\.1\.1 | Added support for host port mapping in CNI\. Merged [pull request \#93](https://github.com/aws/amazon-vpc-cni-plugins/pull/93)\. | 
| 1\.27\-2023\.06\.06 | 1\.27\.1 | 1\.6\.6 | 1\.1\.1 | Fixed containers\-roadmap [issue \#2042](https://github.com/aws/containers-roadmap/issues/2042), which caused nodes to fail pulling private Amazon ECR images\. | 
| 1\.27\-2023\.05\.17 | 1\.27\.1 | 1\.6\.6 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.26 ]


**Kubernetes version `1.26`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.26\-2024\.04\.09 | 1\.26\.12 | 1\.6\.25 | 1\.1\.2 | Upgraded containerd to 1\.6\.25\. Rebuilt CNI and csi\-proxy using golang 1\.22\.1\. | 
| 1\.26\-2024\.03\.12 | 1\.26\.12 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.26\-2024\.02\.13 | 1\.26\.12 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.26\-2024\.01\.11 | 1\.26\.12 | 1\.6\.18 | 1\.1\.2 | Excluded Standalone Windows Update [KB5034439](https://support.microsoft.com/en-au/topic/kb5034439-windows-recovery-environment-update-for-azure-stack-hci-version-22h2-and-windows-server-2022-january-9-2024-6f9d26e6-784c-4503-a3c6-0beedda443ca) on Windows Server 2022 Core AMIs\. The KB applies only to Windows installations with a separate WinRE partition, which aren't included with any of our Amazon EKS Optimized Windows AMIs\. | 
| 1\.26\-2023\.12\.12 | 1\.26\.10 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.26\-2023\.11\.14 | 1\.26\.10 | 1\.6\.18 | 1\.1\.2 | Includes patches for CVE\-2023\-5528\. | 
| 1\.26\-2023\.10\.19 | 1\.26\.9 | 1\.6\.18 | 1\.1\.2 | Upgraded containerd to 1\.6\.18\. Upgraded kubelet to 1\.26\.9\. Added new [bootstrap script environment variables](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(SERVICE\_IPV4\_CIDR and EXCLUDED\_SNAT\_CIDRS\)\. | 
| 1\.26\-2023\.09\.12 | 1\.26\.7 | 1\.6\.6 | 1\.1\.2 | Upgraded the Amazon VPC CNI plugin to use the Kubernetes connector binary, which gets the Pod IP address from the Kubernetes API server\. Merged [pull request \#100](https://github.com/aws/amazon-vpc-cni-plugins/pull/100)\. | 
| 1\.26\-2023\.08\.17 | 1\.26\.7 | 1\.6\.6 | 1\.1\.2 | Includes patches for CVE\-2023\-3676, CVE\-2023\-3893, and CVE\-2023\-3955\. | 
| 1\.26\-2023\.08\.08 | 1\.26\.6 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.26\-2023\.07\.11 | 1\.26\.6 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.26\-2023\.06\.20 | 1\.26\.4 | 1\.6\.6 | 1\.1\.1 | Resolved issue that was causing the DNS suffix search list to be incorrectly populated\. | 
| 1\.26\-2023\.06\.14 | 1\.26\.4 | 1\.6\.6 | 1\.1\.1 | Upgraded Kubernetes to 1\.26\.4\. Added support for host port mapping in CNI\. Merged [pull request \#93](https://github.com/aws/amazon-vpc-cni-plugins/pull/93)\. | 
| 1\.26\-2023\.05\.09 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 | Fixed a bug causing network connectivity [issue \#1126](https://github.com/aws/containers-roadmap/issues/1126) on pods after node restart\. Introduced a new [bootstrap script configuration parameter](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(ExcludedSnatCIDRs\)\. | 
| 1\.26\-2023\.04\.26 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.26\-2023\.04\.11 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.26\-2023\.03\.24 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.25 ]


**Kubernetes version `1.25`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.25\-2024\.04\.09 | 1\.25\.16 | 1\.6\.25 | 1\.1\.2 | Upgraded containerd to 1\.6\.25\. Rebuilt CNI and csi\-proxy using golang 1\.22\.1\. | 
| 1\.25\-2024\.03\.12 | 1\.25\.16 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.25\-2024\.02\.13 | 1\.25\.16 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.25\-2024\.01\.11 | 1\.25\.16 | 1\.6\.18 | 1\.1\.2 | Excluded Standalone Windows Update [KB5034439](https://support.microsoft.com/en-au/topic/kb5034439-windows-recovery-environment-update-for-azure-stack-hci-version-22h2-and-windows-server-2022-january-9-2024-6f9d26e6-784c-4503-a3c6-0beedda443ca) on Windows Server 2022 Core AMIs\. The KB applies only to Windows installations with a separate WinRE partition, which aren't included with any of our Amazon EKS Optimized Windows AMIs\. | 
| 1\.25\-2023\.12\.12 | 1\.25\.15 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.25\-2023\.11\.14 | 1\.25\.15 | 1\.6\.18 | 1\.1\.2 | Includes patches for CVE\-2023\-5528\. | 
| 1\.25\-2023\.10\.19 | 1\.25\.14 | 1\.6\.18 | 1\.1\.2 | Upgraded containerd to 1\.6\.18\. Upgraded kubelet to 1\.25\.14\. Added new [bootstrap script environment variables](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(SERVICE\_IPV4\_CIDR and EXCLUDED\_SNAT\_CIDRS\)\. | 
| 1\.25\-2023\.09\.12 | 1\.25\.12 | 1\.6\.6 | 1\.1\.2 | Upgraded the Amazon VPC CNI plugin to use the Kubernetes connector binary, which gets the Pod IP address from the Kubernetes API server\. Merged [pull request \#100](https://github.com/aws/amazon-vpc-cni-plugins/pull/100)\. | 
| 1\.25\-2023\.08\.17 | 1\.25\.12 | 1\.6\.6 | 1\.1\.2 | Includes patches for CVE\-2023\-3676, CVE\-2023\-3893, and CVE\-2023\-3955\. | 
| 1\.25\-2023\.08\.08 | 1\.25\.9 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.25\-2023\.07\.11 | 1\.25\.9 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.25\-2023\.06\.20 | 1\.25\.9 | 1\.6\.6 | 1\.1\.1 | Resolved issue that was causing the DNS suffix search list to be incorrectly populated\. | 
| 1\.25\-2023\.06\.14 | 1\.25\.9 | 1\.6\.6 | 1\.1\.1 | Upgraded Kubernetes to 1\.25\.9\. Added support for host port mapping in CNI\. Merged [pull request \#93](https://github.com/aws/amazon-vpc-cni-plugins/pull/93)\. | 
| 1\.25\-2023\.05\.09 | 1\.25\.7 | 1\.6\.6 | 1\.1\.1 | Fixed a bug causing network connectivity [issue \#1126](https://github.com/aws/containers-roadmap/issues/1126) on pods after node restart\. Introduced a new [bootstrap script configuration parameter](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(ExcludedSnatCIDRs\)\. | 
| 1\.25\-2023\.04\.11 | 1\.25\.7 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.25\-2023\.03\.27 | 1\.25\.6 | 1\.6\.6 | 1\.1\.1 | Installed a [domainless gMSA plugin](https://aws.amazon.com/blogs/containers/domainless-windows-authentication-for-amazon-eks-windows-pods/) to facilitate gMSA authentication for Windows containers on Amazon EKS\. | 
| 1\.25\-2023\.03\.20 | 1\.25\.6 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.25\-2023\.02\.14 | 1\.25\.6 | 1\.6\.6 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.24 ]


**Kubernetes version `1.24`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.24\-2024\.04\.09 | 1\.24\.17 | 1\.6\.25 | 1\.1\.2 | Upgraded containerd to 1\.6\.25\. Rebuilt CNI and csi\-proxy using golang 1\.22\.1\. | 
| 1\.24\-2024\.03\.12 | 1\.24\.17 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.24\-2024\.02\.13 | 1\.24\.17 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.24\-2024\.01\.11 | 1\.24\.17 | 1\.6\.18 | 1\.1\.2 | Excluded Standalone Windows Update [KB5034439](https://support.microsoft.com/en-au/topic/kb5034439-windows-recovery-environment-update-for-azure-stack-hci-version-22h2-and-windows-server-2022-january-9-2024-6f9d26e6-784c-4503-a3c6-0beedda443ca) on Windows Server 2022 Core AMIs\. The KB applies only to Windows installations with a separate WinRE partition, which aren't included with any of our Amazon EKS Optimized Windows AMIs\. | 
| 1\.24\-2023\.12\.12 | 1\.24\.17 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.24\-2023\.11\.14 | 1\.24\.17 | 1\.6\.18 | 1\.1\.2 | Includes patches for CVE\-2023\-5528\. | 
| 1\.24\-2023\.10\.19 | 1\.24\.17 | 1\.6\.18 | 1\.1\.2 | Upgraded containerd to 1\.6\.18\. Upgraded kubelet to 1\.24\.17\. Added new [bootstrap script environment variables](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(SERVICE\_IPV4\_CIDR and EXCLUDED\_SNAT\_CIDRS\)\. | 
| 1\.24\-2023\.09\.12 | 1\.24\.16 | 1\.6\.6 | 1\.1\.2 | Upgraded the Amazon VPC CNI plugin to use the Kubernetes connector binary, which gets the Pod IP address from the Kubernetes API server\. Merged [pull request \#100](https://github.com/aws/amazon-vpc-cni-plugins/pull/100)\. | 
| 1\.24\-2023\.08\.17 | 1\.24\.16 | 1\.6\.6 | 1\.1\.2 | Includes patches for CVE\-2023\-3676, CVE\-2023\-3893, and CVE\-2023\-3955\. | 
| 1\.24\-2023\.08\.08 | 1\.24\.13 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2023\.07\.11 | 1\.24\.13 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2023\.06\.20 | 1\.24\.13 | 1\.6\.6 | 1\.1\.1 | Resolved issue that was causing the DNS suffix search list to be incorrectly populated\. | 
| 1\.24\-2023\.06\.14 | 1\.24\.13 | 1\.6\.6 | 1\.1\.1 | Upgraded Kubernetes to 1\.24\.13\. Added support for host port mapping in CNI\. Merged [pull request \#93](https://github.com/aws/amazon-vpc-cni-plugins/pull/93)\. | 
| 1\.24\-2023\.05\.09 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Fixed a bug causing network connectivity [issue \#1126](https://github.com/aws/containers-roadmap/issues/1126) on pods after node restart\. Introduced a new [bootstrap script configuration parameter](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(ExcludedSnatCIDRs\)\. | 
| 1\.24\-2023\.04\.11 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.24\-2023\.03\.27 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Installed a [domainless gMSA plugin](https://aws.amazon.com/blogs/containers/domainless-windows-authentication-for-amazon-eks-windows-pods/) to facilitate gMSA authentication for Windows containers on Amazon EKS\. | 
| 1\.24\-2023\.03\.20 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Kubernetes version downgraded to 1\.24\.7 because 1\.24\.10 has a reported issue in kube\-proxy\. | 
| 1\.24\-2023\.02\.14 | 1\.24\.10 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2023\.01\.23 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2023\.01\.11 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2022\.12\.13 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2022\.10\.11 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 

------

## Amazon EKS optimized Windows Server 2022 Full AMI<a name="eks-ami-versions-windows-2022-full"></a>

The following tables list the current and previous versions of the Amazon EKS optimized Windows Server 2022 Full AMI\.

------
#### [ Kubernetes version 1\.29 ]


**Kubernetes version `1.29`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.29\-2024\.04\.09 | 1\.29\.0 | 1\.6\.28 | 1\.1\.2 | Upgraded containerd to 1\.6\.28\. Rebuilt CNI and csi\-proxy using golang 1\.22\.1\. | 
| 1\.29\-2024\.03\.12 | 1\.29\.0 | 1\.6\.25 | 1\.1\.2 |  | 
| 1\.29\-2024\.02\.13 | 1\.29\.0 | 1\.6\.25 | 1\.1\.2 |  | 
| 1\.29\-2024\.02\.06  | 1\.29\.0 | 1\.6\.25 | 1\.1\.2 | Fixed a bug where the pause image was incorrectly deleted by kubelet garbage collection process\. | 
| 1\.29\-2024\.01\.09  | 1\.29\.0 | 1\.6\.18 | 1\.1\.2 |  | 

------
#### [ Kubernetes version 1\.28 ]


**Kubernetes version `1.28`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.28\-2024\.04\.09 | 1\.28\.5 | 1\.6\.25 | 1\.1\.2 | Upgraded containerd to 1\.6\.25\. Rebuilt CNI and csi\-proxy using golang 1\.22\.1\. | 
| 1\.28\-2024\.03\.12 | 1\.28\.5 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.28\-2024\.02\.13 | 1\.28\.5 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.28\-2024\.01\.09  | 1\.28\.5 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.28\-2023\.12\.12 | 1\.28\.3 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.28\-2023\.11\.14 | 1\.28\.3 | 1\.6\.18 | 1\.1\.2 | Includes patches for CVE\-2023\-5528\. | 
| 1\.28\-2023\.10\.19 | 1\.28\.2 | 1\.6\.18 | 1\.1\.2 | Upgraded containerd to 1\.6\.18\. Added new [bootstrap script environment variables](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(SERVICE\_IPV4\_CIDR and EXCLUDED\_SNAT\_CIDRS\)\. | 
| 1\.28\-2023\-09\.27 | 1\.28\.2 | 1\.6\.6 | 1\.1\.2 | Fixed a [security advisory](https://github.com/advisories/GHSA-6xv5-86q9-7xr8) in kubelet\. | 
| 1\.28\-2023\.09\.12 | 1\.28\.1 | 1\.6\.6 | 1\.1\.2 |  | 

------
#### [ Kubernetes version 1\.27 ]


**Kubernetes version `1.27`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.27\-2024\.04\.09 | 1\.27\.9 | 1\.6\.25 | 1\.1\.2 | Upgraded containerd to 1\.6\.25\. Rebuilt CNI and csi\-proxy using golang 1\.22\.1\. | 
| 1\.27\-2024\.03\.12 | 1\.27\.9 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.27\-2024\.02\.13 | 1\.27\.9 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.27\-2024\.01\.09  | 1\.27\.9 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.27\-2023\.12\.12 | 1\.27\.7 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.27\-2023\.11\.14 | 1\.27\.7 | 1\.6\.18 | 1\.1\.2 | Includes patches for CVE\-2023\-5528\. | 
| 1\.27\-2023\.10\.19 | 1\.27\.6 | 1\.6\.18 | 1\.1\.2 | Upgraded containerd to 1\.6\.18\. Added new [bootstrap script environment variables](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(SERVICE\_IPV4\_CIDR and EXCLUDED\_SNAT\_CIDRS\)\. | 
| 1\.27\-2023\-09\.27 | 1\.27\.6 | 1\.6\.6 | 1\.1\.2 | Fixed a [security advisory](https://github.com/advisories/GHSA-6xv5-86q9-7xr8) in kubelet\. | 
| 1\.27\-2023\.09\.12 | 1\.27\.4 | 1\.6\.6 | 1\.1\.2 | Upgraded the Amazon VPC CNI plugin to use the Kubernetes connector binary, which gets the Pod IP address from the Kubernetes API server\. Merged [pull request \#100](https://github.com/aws/amazon-vpc-cni-plugins/pull/100)\. | 
| 1\.27\-2023\.08\.17 | 1\.27\.4 | 1\.6\.6 | 1\.1\.2 | Includes patches for CVE\-2023\-3676, CVE\-2023\-3893, and CVE\-2023\-3955\. | 
| 1\.27\-2023\.08\.08 | 1\.27\.3 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.27\-2023\.07\.11 | 1\.27\.3 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.27\-2023\.06\.20 | 1\.27\.1 | 1\.6\.6 | 1\.1\.1 | Resolved issue that was causing the DNS suffix search list to be incorrectly populated\. | 
| 1\.27\-2023\.06\.14 | 1\.27\.1 | 1\.6\.6 | 1\.1\.1 | Added support for host port mapping in CNI\. Merged [pull request \#93](https://github.com/aws/amazon-vpc-cni-plugins/pull/93)\. | 
| 1\.27\-2023\.06\.06 | 1\.27\.1 | 1\.6\.6 | 1\.1\.1 | Fixed containers\-roadmap [issue \#2042](https://github.com/aws/containers-roadmap/issues/2042), which caused nodes to fail pulling private Amazon ECR images\. | 
| 1\.27\-2023\.05\.18 | 1\.27\.1 | 1\.6\.6 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.26 ]


**Kubernetes version `1.26`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.26\-2024\.04\.09 | 1\.26\.12 | 1\.6\.25 | 1\.1\.2 | Upgraded containerd to 1\.6\.25\. Rebuilt CNI and csi\-proxy using golang 1\.22\.1\. | 
| 1\.26\-2024\.03\.12 | 1\.26\.12 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.26\-2024\.02\.13 | 1\.26\.12 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.26\-2024\.01\.09  | 1\.26\.12 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.26\-2023\.12\.12 | 1\.26\.10 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.26\-2023\.11\.14 | 1\.26\.10 | 1\.6\.18 | 1\.1\.2 | Includes patches for CVE\-2023\-5528\. | 
| 1\.26\-2023\.10\.19 | 1\.26\.9 | 1\.6\.18 | 1\.1\.2 | Upgraded containerd to 1\.6\.18\. Upgraded kubelet to 1\.26\.9\. Added new [bootstrap script environment variables](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(SERVICE\_IPV4\_CIDR and EXCLUDED\_SNAT\_CIDRS\)\. | 
| 1\.26\-2023\.09\.12 | 1\.26\.7 | 1\.6\.6 | 1\.1\.2 | Upgraded the Amazon VPC CNI plugin to use the Kubernetes connector binary, which gets the Pod IP address from the Kubernetes API server\. Merged [pull request \#100](https://github.com/aws/amazon-vpc-cni-plugins/pull/100)\. | 
| 1\.26\-2023\.08\.17 | 1\.26\.7 | 1\.6\.6 | 1\.1\.2 | Includes patches for CVE\-2023\-3676, CVE\-2023\-3893, and CVE\-2023\-3955\. | 
| 1\.26\-2023\.08\.08 | 1\.26\.6 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.26\-2023\.07\.11 | 1\.26\.6 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.26\-2023\.06\.20 | 1\.26\.4 | 1\.6\.6 | 1\.1\.1 | Resolved issue that was causing the DNS suffix search list to be incorrectly populated\. | 
| 1\.26\-2023\.06\.14 | 1\.26\.4 | 1\.6\.6 | 1\.1\.1 | Upgraded Kubernetes to 1\.26\.4\. Added support for host port mapping in CNI\. Merged [pull request \#93](https://github.com/aws/amazon-vpc-cni-plugins/pull/93)\. | 
| 1\.26\-2023\.05\.09 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 | Fixed a bug causing network connectivity [issue \#1126](https://github.com/aws/containers-roadmap/issues/1126) on pods after node restart\. Introduced a new [bootstrap script configuration parameter](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(ExcludedSnatCIDRs\)\. | 
| 1\.26\-2023\.04\.26 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.26\-2023\.04\.11 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.26\-2023\.03\.24 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.25 ]


**Kubernetes version `1.25`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.25\-2024\.04\.09 | 1\.25\.16 | 1\.6\.25 | 1\.1\.2 | Upgraded containerd to 1\.6\.25\. Rebuilt CNI and csi\-proxy using golang 1\.22\.1\. | 
| 1\.25\-2024\.03\.12 | 1\.25\.16 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.25\-2024\.02\.13 | 1\.25\.16 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.25\-2024\.01\.09  | 1\.25\.16 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.25\-2023\.12\.12 | 1\.25\.15 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.25\-2023\.11\.14 | 1\.25\.15 | 1\.6\.18 | 1\.1\.2 | Includes patches for CVE\-2023\-5528\. | 
| 1\.25\-2023\.10\.19 | 1\.25\.14 | 1\.6\.18 | 1\.1\.2 | Upgraded containerd to 1\.6\.18\. Upgraded kubelet to 1\.25\.14\. Added new [bootstrap script environment variables](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(SERVICE\_IPV4\_CIDR and EXCLUDED\_SNAT\_CIDRS\)\. | 
| 1\.25\-2023\.09\.12 | 1\.25\.12 | 1\.6\.6 | 1\.1\.2 | Upgraded the Amazon VPC CNI plugin to use the Kubernetes connector binary, which gets the Pod IP address from the Kubernetes API server\. Merged [pull request \#100](https://github.com/aws/amazon-vpc-cni-plugins/pull/100)\. | 
| 1\.25\-2023\.08\.17 | 1\.25\.12 | 1\.6\.6 | 1\.1\.2 | Includes patches for CVE\-2023\-3676, CVE\-2023\-3893, and CVE\-2023\-3955\. | 
| 1\.25\-2023\.08\.08 | 1\.25\.9 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.25\-2023\.07\.11 | 1\.25\.9 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.25\-2023\.06\.20 | 1\.25\.9 | 1\.6\.6 | 1\.1\.1 | Resolved issue that was causing the DNS suffix search list to be incorrectly populated\. | 
| 1\.25\-2023\.06\.14 | 1\.25\.9 | 1\.6\.6 | 1\.1\.1 | Upgraded Kubernetes to 1\.25\.9\. Added support for host port mapping in CNI\. Merged [pull request \#93](https://github.com/aws/amazon-vpc-cni-plugins/pull/93)\. | 
| 1\.25\-2023\.05\.09 | 1\.25\.7 | 1\.6\.6 | 1\.1\.1 | Fixed a bug causing network connectivity [issue \#1126](https://github.com/aws/containers-roadmap/issues/1126) on pods after node restart\. Introduced a new [bootstrap script configuration parameter](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(ExcludedSnatCIDRs\)\. | 
| 1\.25\-2023\.04\.11 | 1\.25\.7 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.25\-2023\.03\.27 | 1\.25\.6 | 1\.6\.6 | 1\.1\.1 | Installed a [domainless gMSA plugin](https://aws.amazon.com/blogs/containers/domainless-windows-authentication-for-amazon-eks-windows-pods/) to facilitate gMSA authentication for Windows containers on Amazon EKS\. | 
| 1\.25\-2023\.03\.20 | 1\.25\.6 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.25\-2023\.02\.14 | 1\.25\.6 | 1\.6\.6 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.24 ]


**Kubernetes version `1.24`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.24\-2024\.04\.09 | 1\.24\.17 | 1\.6\.25 | 1\.1\.2 | Upgraded containerd to 1\.6\.25\. Rebuilt CNI and csi\-proxy using golang 1\.22\.1\. | 
| 1\.24\-2024\.03\.12 | 1\.24\.17 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.24\-2024\.02\.13 | 1\.24\.17 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.24\-2024\.01\.09  | 1\.24\.17 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.24\-2023\.12\.12 | 1\.24\.17 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.24\-2023\.11\.14 | 1\.24\.17 | 1\.6\.18 | 1\.1\.2 | Includes patches for CVE\-2023\-5528\. | 
| 1\.24\-2023\.10\.19 | 1\.24\.17 | 1\.6\.18 | 1\.1\.2 | Upgraded containerd to 1\.6\.18\. Upgraded kubelet to 1\.24\.17\. Added new [bootstrap script environment variables](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(SERVICE\_IPV4\_CIDR and EXCLUDED\_SNAT\_CIDRS\)\. | 
| 1\.24\-2023\.09\.12 | 1\.24\.16 | 1\.6\.6 | 1\.1\.2 | Upgraded the Amazon VPC CNI plugin to use the Kubernetes connector binary, which gets the Pod IP address from the Kubernetes API server\. Merged [pull request \#100](https://github.com/aws/amazon-vpc-cni-plugins/pull/100)\. | 
| 1\.24\-2023\.08\.17 | 1\.24\.16 | 1\.6\.6 | 1\.1\.2 | Includes patches for CVE\-2023\-3676, CVE\-2023\-3893, and CVE\-2023\-3955\. | 
| 1\.24\-2023\.08\.08 | 1\.24\.13 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2023\.07\.11 | 1\.24\.13 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2023\.06\.20 | 1\.24\.13 | 1\.6\.6 | 1\.1\.1 | Resolved issue that was causing the DNS suffix search list to be incorrectly populated\. | 
| 1\.24\-2023\.06\.14 | 1\.24\.13 | 1\.6\.6 | 1\.1\.1 | Upgraded Kubernetes to 1\.24\.13\. Added support for host port mapping in CNI\. Merged [pull request \#93](https://github.com/aws/amazon-vpc-cni-plugins/pull/93)\. | 
| 1\.24\-2023\.05\.09 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Fixed a bug causing network connectivity [issue \#1126](https://github.com/aws/containers-roadmap/issues/1126) on pods after node restart\. Introduced a new [bootstrap script configuration parameter](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(ExcludedSnatCIDRs\)\. | 
| 1\.24\-2023\.04\.11 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.24\-2023\.03\.27 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Installed a [domainless gMSA plugin](https://aws.amazon.com/blogs/containers/domainless-windows-authentication-for-amazon-eks-windows-pods/) to facilitate gMSA authentication for Windows containers on Amazon EKS\. | 
| 1\.24\-2023\.03\.20 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Kubernetes version downgraded to 1\.24\.7 because 1\.24\.10 has a reported issue in kube\-proxy\. | 
| 1\.24\-2023\.02\.14 | 1\.24\.10 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2023\.01\.23 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2023\.01\.11 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2022\.12\.14 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2022\.10\.11 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 

------

## Amazon EKS optimized Windows Server 2019 Core AMI<a name="eks-ami-versions-windows-2019-core"></a>

The following tables list the current and previous versions of the Amazon EKS optimized Windows Server 2019 Core AMI\.

------
#### [ Kubernetes version 1\.29 ]


**Kubernetes version `1.29`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.29\-2024\.04\.09 | 1\.29\.0 | 1\.6\.28 | 1\.1\.2 | Upgraded containerd to 1\.6\.28\. Rebuilt CNI and csi\-proxy using golang 1\.22\.1\. | 
| 1\.29\-2024\.03\.13 | 1\.29\.0 | 1\.6\.25 | 1\.1\.2 |  | 
| 1\.29\-2024\.02\.13 | 1\.29\.0 | 1\.6\.25 | 1\.1\.2 |  | 
| 1\.29\-2024\.02\.06  | 1\.29\.0 | 1\.6\.25 | 1\.1\.2 | Fixed a bug where the pause image was incorrectly deleted by kubelet garbage collection process\. | 
| 1\.29\-2024\.01\.09  | 1\.29\.0 | 1\.6\.18 | 1\.1\.2 |  | 

------
#### [ Kubernetes version 1\.28 ]


**Kubernetes version `1.28`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.28\-2024\.04\.09 | 1\.28\.5 | 1\.6\.25 | 1\.1\.2 | Upgraded containerd to 1\.6\.25\. Rebuilt CNI and csi\-proxy using golang 1\.22\.1\. | 
| 1\.28\-2024\.03\.13 | 1\.28\.5 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.28\-2024\.02\.13 | 1\.28\.5 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.28\-2024\.01\.09  | 1\.28\.5 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.28\-2023\.12\.12 | 1\.28\.3 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.28\-2023\.11\.14 | 1\.28\.3 | 1\.6\.18 | 1\.1\.2 | Includes patches for CVE\-2023\-5528\. | 
| 1\.28\-2023\.10\.19 | 1\.28\.2 | 1\.6\.18 | 1\.1\.2 | Upgraded containerd to 1\.6\.18\. Added new [bootstrap script environment variables](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(SERVICE\_IPV4\_CIDR and EXCLUDED\_SNAT\_CIDRS\)\. | 
| 1\.28\-2023\-09\.27 | 1\.28\.2 | 1\.6\.6 | 1\.1\.2 | Fixed a [security advisory](https://github.com/advisories/GHSA-6xv5-86q9-7xr8) in kubelet\. | 
| 1\.28\-2023\.09\.12 | 1\.28\.1 | 1\.6\.6 | 1\.1\.2 |  | 

------
#### [ Kubernetes version 1\.27 ]


**Kubernetes version `1.27`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.27\-2024\.04\.09 | 1\.27\.9 | 1\.6\.25 | 1\.1\.2 | Upgraded containerd to 1\.6\.25\. Rebuilt CNI and csi\-proxy using golang 1\.22\.1\. | 
| 1\.27\-2024\.03\.13 | 1\.27\.9 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.27\-2024\.02\.13 | 1\.27\.9 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.27\-2024\.01\.09  | 1\.27\.9 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.27\-2023\.12\.12 | 1\.27\.7 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.27\-2023\.11\.14 | 1\.27\.7 | 1\.6\.18 | 1\.1\.2 | Includes patches for CVE\-2023\-5528\. | 
| 1\.27\-2023\.10\.19 | 1\.27\.6 | 1\.6\.18 | 1\.1\.2 | Upgraded containerd to 1\.6\.18\. Added new [bootstrap script environment variables](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(SERVICE\_IPV4\_CIDR and EXCLUDED\_SNAT\_CIDRS\)\. | 
| 1\.27\-2023\-09\.27 | 1\.27\.6 | 1\.6\.6 | 1\.1\.2 | Fixed a [security advisory](https://github.com/advisories/GHSA-6xv5-86q9-7xr8) in kubelet\. | 
| 1\.27\-2023\.09\.12 | 1\.27\.4 | 1\.6\.6 | 1\.1\.2 | Upgraded the Amazon VPC CNI plugin to use the Kubernetes connector binary, which gets the Pod IP address from the Kubernetes API server\. Merged [pull request \#100](https://github.com/aws/amazon-vpc-cni-plugins/pull/100)\. | 
| 1\.27\-2023\.08\.17 | 1\.27\.4 | 1\.6\.6 | 1\.1\.2 | Includes patches for CVE\-2023\-3676, CVE\-2023\-3893, and CVE\-2023\-3955\. | 
| 1\.27\-2023\.08\.08 | 1\.27\.3 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.27\-2023\.07\.11 | 1\.27\.3 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.27\-2023\.06\.20 | 1\.27\.1 | 1\.6\.6 | 1\.1\.1 | Resolved issue that was causing the DNS suffix search list to be incorrectly populated\. | 
| 1\.27\-2023\.06\.14 | 1\.27\.1 | 1\.6\.6 | 1\.1\.1 | Added support for host port mapping in CNI\. Merged [pull request \#93](https://github.com/aws/amazon-vpc-cni-plugins/pull/93)\. | 
| 1\.27\-2023\.06\.06 | 1\.27\.1 | 1\.6\.6 | 1\.1\.1 | Fixed containers\-roadmap [issue \#2042](https://github.com/aws/containers-roadmap/issues/2042), which caused nodes to fail pulling private Amazon ECR images\. | 
| 11\.27\-2023\.05\.18 | 1\.27\.1 | 1\.6\.6 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.26 ]


**Kubernetes version `1.26`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.26\-2024\.04\.09 | 1\.26\.12 | 1\.6\.25 | 1\.1\.2 | Upgraded containerd to 1\.6\.25\. Rebuilt CNI and csi\-proxy using golang 1\.22\.1\. | 
| 1\.26\-2024\.03\.13 | 1\.26\.12 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.26\-2024\.02\.13 | 1\.26\.12 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.26\-2024\.01\.09  | 1\.26\.12 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.26\-2023\.12\.12 | 1\.26\.10 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.26\-2023\.11\.14 | 1\.26\.10 | 1\.6\.18 | 1\.1\.2 | Includes patches for CVE\-2023\-5528\. | 
| 1\.26\-2023\.10\.19 | 1\.26\.9 | 1\.6\.18 | 1\.1\.2 | Upgraded containerd to 1\.6\.18\. Upgraded kubelet to 1\.26\.9\. Added new [bootstrap script environment variables](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(SERVICE\_IPV4\_CIDR and EXCLUDED\_SNAT\_CIDRS\)\. | 
| 1\.26\-2023\.09\.12 | 1\.26\.7 | 1\.6\.6 | 1\.1\.2 | Upgraded the Amazon VPC CNI plugin to use the Kubernetes connector binary, which gets the Pod IP address from the Kubernetes API server\. Merged [pull request \#100](https://github.com/aws/amazon-vpc-cni-plugins/pull/100)\. | 
| 1\.26\-2023\.08\.17 | 1\.26\.7 | 1\.6\.6 | 1\.1\.2 | Includes patches for CVE\-2023\-3676, CVE\-2023\-3893, and CVE\-2023\-3955\. | 
| 1\.26\-2023\.08\.08 | 1\.26\.6 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.26\-2023\.07\.11 | 1\.26\.6 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.26\-2023\.06\.20 | 1\.26\.4 | 1\.6\.6 | 1\.1\.1 | Resolved issue that was causing the DNS suffix search list to be incorrectly populated\. | 
| 1\.26\-2023\.06\.14 | 1\.26\.4 | 1\.6\.6 | 1\.1\.1 | Upgraded Kubernetes to 1\.26\.4\. Added support for host port mapping in CNI\. Merged [pull request \#93](https://github.com/aws/amazon-vpc-cni-plugins/pull/93)\. | 
| 1\.26\-2023\.05\.09 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 | Fixed a bug causing network connectivity [issue \#1126](https://github.com/aws/containers-roadmap/issues/1126) on pods after node restart\. Introduced a new [bootstrap script configuration parameter](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(ExcludedSnatCIDRs\)\. | 
| 1\.26\-2023\.04\.26 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.26\-2023\.04\.11 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.26\-2023\.03\.24 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.25 ]


**Kubernetes version `1.25`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.25\-2024\.04\.09 | 1\.25\.16 | 1\.6\.25 | 1\.1\.2 | Upgraded containerd to 1\.6\.25\. Rebuilt CNI and csi\-proxy using golang 1\.22\.1\. | 
| 1\.25\-2024\.03\.13 | 1\.25\.16 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.25\-2024\.02\.13 | 1\.25\.16 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.25\-2024\.01\.09  | 1\.25\.16 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.25\-2023\.12\.12 | 1\.25\.15 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.25\-2023\.11\.14 | 1\.25\.15 | 1\.6\.18 | 1\.1\.2 | Includes patches for CVE\-2023\-5528\. | 
| 1\.25\-2023\.10\.19 | 1\.25\.14 | 1\.6\.18 | 1\.1\.2 | Upgraded containerd to 1\.6\.18\. Upgraded kubelet to 1\.25\.14\. Added new [bootstrap script environment variables](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(SERVICE\_IPV4\_CIDR and EXCLUDED\_SNAT\_CIDRS\)\. | 
| 1\.25\-2023\.09\.12 | 1\.25\.12 | 1\.6\.6 | 1\.1\.2 | Upgraded the Amazon VPC CNI plugin to use the Kubernetes connector binary, which gets the Pod IP address from the Kubernetes API server\. Merged [pull request \#100](https://github.com/aws/amazon-vpc-cni-plugins/pull/100)\. | 
| 1\.25\-2023\.08\.17 | 1\.25\.12 | 1\.6\.6 | 1\.1\.2 | Includes patches for CVE\-2023\-3676, CVE\-2023\-3893, and CVE\-2023\-3955\. | 
| 1\.25\-2023\.08\.08 | 1\.25\.9 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.25\-2023\.07\.11 | 1\.25\.9 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.25\-2023\.06\.20 | 1\.25\.9 | 1\.6\.6 | 1\.1\.1 | Resolved issue that was causing the DNS suffix search list to be incorrectly populated\. | 
| 1\.25\-2023\.06\.14 | 1\.25\.9 | 1\.6\.6 | 1\.1\.1 | Upgraded Kubernetes to 1\.25\.9\. Added support for host port mapping in CNI\. Merged [pull request \#93](https://github.com/aws/amazon-vpc-cni-plugins/pull/93)\. | 
| 1\.25\-2023\.05\.09 | 1\.25\.7 | 1\.6\.6 | 1\.1\.1 | Fixed a bug causing network connectivity [issue \#1126](https://github.com/aws/containers-roadmap/issues/1126) on pods after node restart\. Introduced a new [bootstrap script configuration parameter](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(ExcludedSnatCIDRs\)\. | 
| 1\.25\-2023\.04\.11 | 1\.25\.7 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.25\-2023\.03\.27 | 1\.25\.6 | 1\.6\.6 | 1\.1\.1 | Installed a [domainless gMSA plugin](https://aws.amazon.com/blogs/containers/domainless-windows-authentication-for-amazon-eks-windows-pods/) to facilitate gMSA authentication for Windows containers on Amazon EKS\. | 
| 1\.25\-2023\.03\.20 | 1\.25\.6 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.25\-2023\.02\.14 | 1\.25\.6 | 1\.6\.6 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.24 ]


**Kubernetes version `1.24`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.24\-2024\.04\.09 | 1\.24\.17 | 1\.6\.25 | 1\.1\.2 | Upgraded containerd to 1\.6\.25\. Rebuilt CNI and csi\-proxy using golang 1\.22\.1\. | 
| 1\.24\-2024\.03\.13 | 1\.24\.17 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.24\-2024\.02\.13 | 1\.24\.17 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.24\-2024\.01\.09  | 1\.24\.17 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.24\-2023\.12\.12 | 1\.24\.17 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.24\-2023\.11\.14 | 1\.24\.17 | 1\.6\.18 | 1\.1\.2 | Includes patches for CVE\-2023\-5528\. | 
| 1\.24\-2023\.10\.19 | 1\.24\.17 | 1\.6\.18 | 1\.1\.2 | Upgraded containerd to 1\.6\.18\. Upgraded kubelet to 1\.24\.17\. Added new [bootstrap script environment variables](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(SERVICE\_IPV4\_CIDR and EXCLUDED\_SNAT\_CIDRS\)\. | 
| 1\.24\-2023\.09\.12 | 1\.24\.16 | 1\.6\.6 | 1\.1\.2 | Upgraded the Amazon VPC CNI plugin to use the Kubernetes connector binary, which gets the Pod IP address from the Kubernetes API server\. Merged [pull request \#100](https://github.com/aws/amazon-vpc-cni-plugins/pull/100)\. | 
| 1\.24\-2023\.08\.17 | 1\.24\.16 | 1\.6\.6 | 1\.1\.2 | Includes patches for CVE\-2023\-3676, CVE\-2023\-3893, and CVE\-2023\-3955\. | 
| 1\.24\-2023\.08\.08 | 1\.24\.13 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2023\.07\.11 | 1\.24\.13 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2023\.06\.20 | 1\.24\.13 | 1\.6\.6 | 1\.1\.1 | Resolved issue that was causing the DNS suffix search list to be incorrectly populated\. | 
| 1\.24\-2023\.06\.14 | 1\.24\.13 | 1\.6\.6 | 1\.1\.1 | Upgraded Kubernetes to 1\.24\.13\. Added support for host port mapping in CNI\. Merged [pull request \#93](https://github.com/aws/amazon-vpc-cni-plugins/pull/93)\. | 
| 1\.24\-2023\.05\.09 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Fixed a bug causing network connectivity [issue \#1126](https://github.com/aws/containers-roadmap/issues/1126) on pods after node restart\. Introduced a new [bootstrap script configuration parameter](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(ExcludedSnatCIDRs\)\. | 
| 1\.24\-2023\.04\.11 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.24\-2023\.03\.27 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Installed a [domainless gMSA plugin](https://aws.amazon.com/blogs/containers/domainless-windows-authentication-for-amazon-eks-windows-pods/) to facilitate gMSA authentication for Windows containers on Amazon EKS\. | 
| 1\.24\-2023\.03\.20 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Kubernetes version downgraded to 1\.24\.7 because 1\.24\.10 has a reported issue in kube\-proxy\. | 
| 1\.24\-2023\.02\.14 | 1\.24\.10 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2023\.01\.23 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2023\.01\.11 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2022\.12\.13 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2022\.11\.08 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 

------

## Amazon EKS optimized Windows Server 2019 Full AMI<a name="eks-ami-versions-windows-2019-full"></a>

The following tables list the current and previous versions of the Amazon EKS optimized Windows Server 2019 Full AMI\.

------
#### [ Kubernetes version 1\.29 ]


**Kubernetes version `1.29`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.29\-2024\.04\.09 | 1\.29\.0 | 1\.6\.28 | 1\.1\.2 | Upgraded containerd to 1\.6\.28\. Rebuilt CNI and csi\-proxy using golang 1\.22\.1\. | 
| 1\.29\-2024\.03\.13 | 1\.29\.0 | 1\.6\.25 | 1\.1\.2 |  | 
| 1\.29\-2024\.02\.13 | 1\.29\.0 | 1\.6\.25 | 1\.1\.2 |  | 
| 1\.29\-2024\.02\.06  | 1\.29\.0 | 1\.6\.25 | 1\.1\.2 | Fixed a bug where the pause image was incorrectly deleted by kubelet garbage collection process\. | 
| 1\.29\-2024\.01\.09  | 1\.29\.0 | 1\.6\.18 | 1\.1\.2 |  | 

------
#### [ Kubernetes version 1\.28 ]


**Kubernetes version `1.28`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.28\-2024\.04\.09 | 1\.28\.5 | 1\.6\.25 | 1\.1\.2 | Upgraded containerd to 1\.6\.25\. Rebuilt CNI and csi\-proxy using golang 1\.22\.1\. | 
| 1\.28\-2024\.03\.13 | 1\.28\.5 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.28\-2024\.02\.13 | 1\.28\.5 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.28\-2024\.01\.09  | 1\.28\.5 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.28\-2023\.12\.12 | 1\.28\.3 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.28\-2023\.11\.14 | 1\.28\.3 | 1\.6\.18 | 1\.1\.2 | Includes patches for CVE\-2023\-5528\. | 
| 1\.28\-2023\.10\.19 | 1\.28\.2 | 1\.6\.18 | 1\.1\.2 | Upgraded containerd to 1\.6\.18\. Added new [bootstrap script environment variables](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(SERVICE\_IPV4\_CIDR and EXCLUDED\_SNAT\_CIDRS\)\. | 
| 1\.28\-2023\-09\.27 | 1\.28\.2 | 1\.6\.6 | 1\.1\.2 | Fixed a [security advisory](https://github.com/advisories/GHSA-6xv5-86q9-7xr8) in kubelet\. | 
| 1\.28\-2023\.09\.12 | 1\.28\.1 | 1\.6\.6 | 1\.1\.2 |  | 

------
#### [ Kubernetes version 1\.27 ]


**Kubernetes version `1.27`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.27\-2024\.04\.09 | 1\.27\.9 | 1\.6\.25 | 1\.1\.2 | Upgraded containerd to 1\.6\.25\. Rebuilt CNI and csi\-proxy using golang 1\.22\.1\. | 
| 1\.27\-2024\.03\.13 | 1\.27\.9 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.27\-2024\.02\.13 | 1\.27\.9 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.27\-2024\.01\.09  | 1\.27\.9 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.27\-2023\.12\.12 | 1\.27\.7 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.27\-2023\.11\.14 | 1\.27\.7 | 1\.6\.18 | 1\.1\.2 | Includes patches for CVE\-2023\-5528\. | 
| 1\.27\-2023\.10\.19 | 1\.27\.6 | 1\.6\.18 | 1\.1\.2 | Upgraded containerd to 1\.6\.18\. Added new [bootstrap script environment variables](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(SERVICE\_IPV4\_CIDR and EXCLUDED\_SNAT\_CIDRS\)\. | 
| 1\.27\-2023\-09\.27 | 1\.27\.6 | 1\.6\.6 | 1\.1\.2 | Fixed a [security advisory](https://github.com/advisories/GHSA-6xv5-86q9-7xr8) in kubelet\. | 
| 1\.27\-2023\.09\.12 | 1\.27\.4 | 1\.6\.6 | 1\.1\.2 | Upgraded the Amazon VPC CNI plugin to use the Kubernetes connector binary, which gets the Pod IP address from the Kubernetes API server\. Merged [pull request \#100](https://github.com/aws/amazon-vpc-cni-plugins/pull/100)\. | 
| 1\.27\-2023\.08\.17 | 1\.27\.4 | 1\.6\.6 | 1\.1\.2 | Includes patches for CVE\-2023\-3676, CVE\-2023\-3893, and CVE\-2023\-3955\. | 
| 1\.27\-2023\.08\.08 | 1\.27\.3 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.27\-2023\.07\.11 | 1\.27\.3 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.27\-2023\.06\.20 | 1\.27\.1 | 1\.6\.6 | 1\.1\.1 | Resolved issue that was causing the DNS suffix search list to be incorrectly populated\. | 
| 1\.27\-2023\.06\.14 | 1\.27\.1 | 1\.6\.6 | 1\.1\.1 | Added support for host port mapping in CNI\. Merged [pull request \#93](https://github.com/aws/amazon-vpc-cni-plugins/pull/93)\. | 
| 1\.27\-2023\.06\.06 | 1\.27\.1 | 1\.6\.6 | 1\.1\.1 | Fixed containers\-roadmap [issue \#2042](https://github.com/aws/containers-roadmap/issues/2042), which caused nodes to fail pulling private Amazon ECR images\. | 
| 1\.27\-2023\.05\.17 | 1\.27\.1 | 1\.6\.6 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.26 ]


**Kubernetes version `1.26`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.26\-2024\.04\.09 | 1\.26\.12 | 1\.6\.25 | 1\.1\.2 | Upgraded containerd to 1\.6\.25\. Rebuilt CNI and csi\-proxy using golang 1\.22\.1\. | 
| 1\.26\-2024\.03\.13 | 1\.26\.12 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.26\-2024\.02\.13 | 1\.26\.12 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.26\-2024\.01\.09  | 1\.26\.12 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.26\-2023\.12\.12 | 1\.26\.10 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.26\-2023\.11\.14 | 1\.26\.10 | 1\.6\.18 | 1\.1\.2 | Includes patches for CVE\-2023\-5528\. | 
| 1\.26\-2023\.10\.19 | 1\.26\.9 | 1\.6\.18 | 1\.1\.2 | Upgraded containerd to 1\.6\.18\. Upgraded kubelet to 1\.26\.9\. Added new [bootstrap script environment variables](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(SERVICE\_IPV4\_CIDR and EXCLUDED\_SNAT\_CIDRS\)\. | 
| 1\.26\-2023\.09\.12 | 1\.26\.7 | 1\.6\.6 | 1\.1\.2 | Upgraded the Amazon VPC CNI plugin to use the Kubernetes connector binary, which gets the Pod IP address from the Kubernetes API server\. Merged [pull request \#100](https://github.com/aws/amazon-vpc-cni-plugins/pull/100)\. | 
| 1\.26\-2023\.08\.17 | 1\.26\.7 | 1\.6\.6 | 1\.1\.2 | Includes patches for CVE\-2023\-3676, CVE\-2023\-3893, and CVE\-2023\-3955\. | 
| 1\.26\-2023\.08\.08 | 1\.26\.6 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.26\-2023\.07\.11 | 1\.26\.6 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.26\-2023\.06\.20 | 1\.26\.4 | 1\.6\.6 | 1\.1\.1 | Resolved issue that was causing the DNS suffix search list to be incorrectly populated\. | 
| 1\.26\-2023\.06\.14 | 1\.26\.4 | 1\.6\.6 | 1\.1\.1 | Upgraded Kubernetes to 1\.26\.4\. Added support for host port mapping in CNI\. Merged [pull request \#93](https://github.com/aws/amazon-vpc-cni-plugins/pull/93)\. | 
| 1\.26\-2023\.05\.09 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 | Fixed a bug causing network connectivity [issue \#1126](https://github.com/aws/containers-roadmap/issues/1126) on pods after node restart\. Introduced a new [bootstrap script configuration parameter](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(ExcludedSnatCIDRs\)\. | 
| 1\.26\-2023\.04\.26 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.26\-2023\.04\.11 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.26\-2023\.03\.24 | 1\.26\.2 | 1\.6\.6 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.25 ]


**Kubernetes version `1.25`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.25\-2024\.04\.09 | 1\.25\.16 | 1\.6\.25 | 1\.1\.2 | Upgraded containerd to 1\.6\.25\. Rebuilt CNI and csi\-proxy using golang 1\.22\.1\. | 
| 1\.25\-2024\.03\.13 | 1\.25\.16 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.25\-2024\.02\.13 | 1\.25\.16 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.25\-2024\.01\.09  | 1\.25\.16 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.25\-2023\.12\.12 | 1\.25\.15 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.25\-2023\.11\.14 | 1\.25\.15 | 1\.6\.18 | 1\.1\.2 | Includes patches for CVE\-2023\-5528\. | 
| 1\.25\-2023\.10\.19 | 1\.25\.14 | 1\.6\.18 | 1\.1\.2 | Upgraded containerd to 1\.6\.18\. Upgraded kubelet to 1\.25\.14\. Added new [bootstrap script environment variables](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(SERVICE\_IPV4\_CIDR and EXCLUDED\_SNAT\_CIDRS\)\. | 
| 1\.25\-2023\.09\.12 | 1\.25\.12 | 1\.6\.6 | 1\.1\.2 | Upgraded the Amazon VPC CNI plugin to use the Kubernetes connector binary, which gets the Pod IP address from the Kubernetes API server\. Merged [pull request \#100](https://github.com/aws/amazon-vpc-cni-plugins/pull/100)\. | 
| 1\.25\-2023\.08\.17 | 1\.25\.12 | 1\.6\.6 | 1\.1\.2 | Includes patches for CVE\-2023\-3676, CVE\-2023\-3893, and CVE\-2023\-3955\. | 
| 1\.25\-2023\.08\.08 | 1\.25\.9 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.25\-2023\.07\.11 | 1\.25\.9 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.25\-2023\.06\.20 | 1\.25\.9 | 1\.6\.6 | 1\.1\.1 | Resolved issue that was causing the DNS suffix search list to be incorrectly populated\. | 
| 1\.25\-2023\.06\.14 | 1\.25\.9 | 1\.6\.6 | 1\.1\.1 | Upgraded Kubernetes to 1\.25\.9\. Added support for host port mapping in CNI\. Merged [pull request \#93](https://github.com/aws/amazon-vpc-cni-plugins/pull/93)\. | 
| 1\.25\-2023\.05\.09 | 1\.25\.7 | 1\.6\.6 | 1\.1\.1 | Fixed a bug causing network connectivity [issue \#1126](https://github.com/aws/containers-roadmap/issues/1126) on pods after node restart\. Introduced a new [bootstrap script configuration parameter](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(ExcludedSnatCIDRs\)\. | 
| 1\.25\-2023\.04\.11 | 1\.25\.7 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.25\-2023\.03\.27 | 1\.25\.6 | 1\.6\.6 | 1\.1\.1 | Installed a [domainless gMSA plugin](https://aws.amazon.com/blogs/containers/domainless-windows-authentication-for-amazon-eks-windows-pods/) to facilitate gMSA authentication for Windows containers on Amazon EKS\. | 
| 1\.25\-2023\.03\.20 | 1\.25\.6 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.25\-2023\.02\.14 | 1\.25\.6 | 1\.6\.6 | 1\.1\.1 |  | 

------
#### [ Kubernetes version 1\.24 ]


**Kubernetes version `1.24`**  

| AMI version | `kubelet` version | `containerd` version | `csi-proxy` version | Release notes | 
| --- | --- | --- | --- | --- | 
| 1\.24\-2024\.04\.09 | 1\.24\.17 | 1\.6\.25 | 1\.1\.2 | Upgraded containerd to 1\.6\.25\. Rebuilt CNI and csi\-proxy using golang 1\.22\.1\. | 
| 1\.24\-2024\.03\.13 | 1\.24\.17 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.24\-2024\.02\.13 | 1\.24\.17 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.24\-2024\.01\.09  | 1\.24\.17 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.24\-2023\.12\.12 | 1\.24\.17 | 1\.6\.18 | 1\.1\.2 |  | 
| 1\.24\-2023\.11\.14 | 1\.24\.17 | 1\.6\.18 | 1\.1\.2 | Includes patches for CVE\-2023\-5528\. | 
| 1\.24\-2023\.10\.19 | 1\.24\.17 | 1\.6\.18 | 1\.1\.2 | Upgraded containerd to 1\.6\.18\. Upgraded kubelet to 1\.24\.17\. Added new [bootstrap script environment variables](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(SERVICE\_IPV4\_CIDR and EXCLUDED\_SNAT\_CIDRS\)\. | 
| 1\.24\-2023\.09\.12 | 1\.24\.16 | 1\.6\.6 | 1\.1\.2 | Upgraded the Amazon VPC CNI plugin to use the Kubernetes connector binary, which gets the Pod IP address from the Kubernetes API server\. Merged [pull request \#100](https://github.com/aws/amazon-vpc-cni-plugins/pull/100)\. | 
| 1\.24\-2023\.08\.17 | 1\.24\.16 | 1\.6\.6 | 1\.1\.2 | Includes patches for CVE\-2023\-3676, CVE\-2023\-3893, and CVE\-2023\-3955\. | 
| 1\.24\-2023\.08\.08 | 1\.24\.13 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2023\.07\.11 | 1\.24\.13 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2023\.06\.21 | 1\.24\.13 | 1\.6\.6 | 1\.1\.1 | Resolved issue that was causing the DNS suffix search list to be incorrectly populated\. | 
| 1\.24\-2023\.06\.14 | 1\.24\.13 | 1\.6\.6 | 1\.1\.1 | Upgraded Kubernetes to 1\.24\.13\. Added support for host port mapping in CNI\. Merged [pull request \#93](https://github.com/aws/amazon-vpc-cni-plugins/pull/93)\. | 
| 1\.24\-2023\.05\.09 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Fixed a bug causing network connectivity [issue \#1126](https://github.com/aws/containers-roadmap/issues/1126) on pods after node restart\. Introduced a new [bootstrap script configuration parameter](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) \(ExcludedSnatCIDRs\)\. | 
| 1\.24\-2023\.04\.11 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Added recovery mechanism for kubelet and kube\-proxy on service crash\. | 
| 1\.24\-2023\.03\.27 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Installed a [domainless gMSA plugin](https://aws.amazon.com/blogs/containers/domainless-windows-authentication-for-amazon-eks-windows-pods/) to facilitate gMSA authentication for Windows containers on Amazon EKS\. | 
| 1\.24\-2023\.03\.20 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 | Kubernetes version downgraded to 1\.24\.7 because 1\.24\.10 has a reported issue in kube\-proxy\. | 
| 1\.24\-2023\.02\.14 | 1\.24\.10 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2023\.01\.23 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2023\.01\.11 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2022\.12\.14 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 
| 1\.24\-2022\.10\.12 | 1\.24\.7 | 1\.6\.6 | 1\.1\.1 |  | 

------