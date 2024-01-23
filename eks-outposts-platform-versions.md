# Amazon EKS local cluster platform versions<a name="eks-outposts-platform-versions"></a>

Local cluster platform versions represent the capabilities of the Amazon EKS cluster on AWS Outposts\. The versions include the components that run on the Kubernetes control plane, which Kubernetes API server flags are enabled\. They also include the current Kubernetes patch version\. Each Kubernetes minor version has one or more associated platform versions\. The platform versions for different Kubernetes minor versions are independent\. The platform versions for local clusters and Amazon EKS clusters in the cloud are independent\.

When a new Kubernetes minor version is available for local clusters, such as `1.28`, the initial platform version for that Kubernetes minor version starts at `eks-local-outposts.1`\. However, Amazon EKS releases new platform versions periodically to enable new Kubernetes control plane settings and to provide security fixes\.

When new local cluster platform versions become available for a minor version:
+ The platform version number is incremented \(`eks-local-outposts.n+1`\)\.
+ Amazon EKS automatically updates all existing local clusters to the latest platform version for their corresponding Kubernetes minor version\. Automatic updates of existing platform versions are rolled out incrementally\. The roll\-out process might take some time\. If you need the latest platform version features immediately, we recommend that you create a new local cluster\. 
+ Amazon EKS might publish a new node AMI with a corresponding patch version\. All patch versions are compatible between the Kubernetes control plane and node AMIs for a single Kubernetes minor version\.

New platform versions don't introduce breaking changes or cause service interruptions\.

Local clusters are always created with the latest available platform version \(`eks-local-outposts.n`\) for the specified Kubernetes version\.

The current and recent platform versions are described in the following tables\.

## Kubernetes version `1.28`<a name="platform-versions-1.28"></a>

The following admission controllers are enabled for all `1.28` platform versions: `CertificateApproval`, `CertificateSigning`, `CertificateSubjectRestriction`, `DefaultIngressClass`, `DefaultStorageClass`, `DefaultTolerationSeconds`, `ExtendedResourceToleration`, `LimitRanger`, `MutatingAdmissionWebhook`, `NamespaceLifecycle`, `NodeRestriction`, `PersistentVolumeClaimResize`, `Priority`, `PodSecurity`, `ResourceQuota`, `RuntimeClass`, `ServiceAccount`, `StorageObjectInUseProtection`, `TaintNodesByCondition`, `ValidatingAdmissionPolicy`, and `ValidatingAdmissionWebhook`\.


|  Kubernetes version  |  Amazon EKS platform version  |  Release notes  |  Release date  | 
| --- | --- | --- | --- | 
|  `1.28.1`  |  `eks-local-outposts.1`  |  Initial release of Kubernetes version `1.28` for local Amazon EKS clusters on Outposts\.  | October 4, 2023 | 

## Kubernetes version `1.27`<a name="platform-versions-1.27"></a>

The following admission controllers are enabled for all `1.27` platform versions: `CertificateApproval`, `CertificateSigning`, `CertificateSubjectRestriction`, `DefaultIngressClass`, `DefaultStorageClass`, `DefaultTolerationSeconds`, `ExtendedResourceToleration`, `LimitRanger`, `MutatingAdmissionWebhook`, `NamespaceLifecycle`, `NodeRestriction`, `PersistentVolumeClaimResize`, `Priority`, `PodSecurity`, `ResourceQuota`, `RuntimeClass`, `ServiceAccount`, `StorageObjectInUseProtection`, `TaintNodesByCondition`, `ValidatingAdmissionPolicy`, and `ValidatingAdmissionWebhook`\.


|  Kubernetes version  |  Amazon EKS platform version  |  Release notes  |  Release date  | 
| --- | --- | --- | --- | 
|  `1.27.3`  |  `eks-local-outposts.3`  |  New platform version with security fixes and enhancements\. `kube-proxy` updated to `v1.27.3`\. Amazon VPC CNI plugin for Kubernetes updated to `v1.13.2`\.   | July 14, 2023 | 
|  `1.27.1`  |  `eks-local-outposts.2`  |  Updated CoreDNS image to `v1.10.1`  | June 22, 2023 | 
|  `1.27.1`  |  `eks-local-outposts.1`  |  Initial release of Kubernetes version `1.27` for local Amazon EKS clusters on Outposts\.  | May 30, 2023 | 

## Kubernetes version `1.26`<a name="platform-versions-1.26"></a>

The following admission controllers are enabled for all `1.26` platform versions: `CertificateApproval`, `CertificateSigning`, `CertificateSubjectRestriction`, `DefaultIngressClass`, `DefaultStorageClass`, `DefaultTolerationSeconds`, `ExtendedResourceToleration`, `LimitRanger`, `MutatingAdmissionWebhook`, `NamespaceLifecycle`, `NodeRestriction`, `PersistentVolumeClaimResize`, `Priority`, `PodSecurity`, `ResourceQuota`, `RuntimeClass`, `ServiceAccount`, `StorageObjectInUseProtection`, `TaintNodesByCondition`, `ValidatingAdmissionPolicy`, and `ValidatingAdmissionWebhook`\.


|  Kubernetes version  |  Amazon EKS platform version  |  Release notes  |  Release date  | 
| --- | --- | --- | --- | 
|  `1.26.6`  |  `eks-local-outposts.4`  |  New platform version with security fixes and enhancements\. `kube-proxy` updated to `v1.26.6`\. Amazon VPC CNI plugin for Kubernetes updated to `v1.13.2`\.   | July 14, 2023 | 
|  `1.26.4`  |  `eks-local-outposts.3`  |  New platform version with security fixes and enhancements\.  | July 13, 2023 | 
|  `1.26.2`  |  `eks-local-outposts.2`  |  Updated Bottlerocket version to `1.13.2`  | May 2, 2023 | 
|  `1.26.2`  |  `eks-local-outposts.1`  |  Initial release of Kubernetes version `1.26` for local Amazon EKS clusters on Outposts\.  | April 11, 2023 | 

## Kubernetes version `1.25`<a name="platform-versions-1.25"></a>

The following admission controllers are enabled for all `1.25` platform versions: `CertificateApproval`, `CertificateSigning`, `CertificateSubjectRestriction`, `DefaultIngressClass`, `DefaultStorageClass`, `DefaultTolerationSeconds`, `ExtendedResourceToleration`, `LimitRanger`, `MutatingAdmissionWebhook`, `NamespaceLifecycle`, `NodeRestriction`, `PersistentVolumeClaimResize`, `Priority`, `PodSecurity`, `ResourceQuota`, `RuntimeClass`, `ServiceAccount`, `StorageObjectInUseProtection`, `TaintNodesByCondition`, and `ValidatingAdmissionWebhook`\.


|  Kubernetes version  |  Amazon EKS platform version  |  Release notes  |  Release date  | 
| --- | --- | --- | --- | 
|  `1.25.11`  |  `eks-local-outposts.6`  |  New platform version with security fixes and enhancements\. `kube-proxy` updated to `v1.25.11`\. Amazon VPC CNI plugin for Kubernetes updated to `v1.13.2`\.   | July 14, 2023 | 
|  `1.25.9`  |  `eks-local-outposts.5`  |  New platform version with security fixes and enhancements\.  | July 13, 2023 | 
|  `1.25.6`  |  `eks-local-outposts.4`  |  Updated Bottlerocket version to `1.13.2`  | May 2, 2023 | 
|  `1.25.6`  |  `eks-local-outposts.3`  |  Amazon EKS control plane instance operating system updated to Bottlerocket version `v1.13.1` and Amazon VPC CNI plugin for Kubernetes updated to version `v1.12.6`\.  | April 14, 2023 | 
|  `1.25.6`  |  `eks-local-outposts.2`  |  Improved diagnostics collection for Kubernetes control plane instances\.  | March 8, 2023 | 
|  `1.25.6`  |  `eks-local-outposts.1`  | Initial release of Kubernetes version `1.25` for local Amazon EKS clusters on Outposts\. | March 1, 2023 | 

## Kubernetes version `1.24`<a name="platform-versions-1.24"></a>

The following admission controllers are enabled for all `1.24` platform versions: `DefaultStorageClass`, `DefaultTolerationSeconds`, `LimitRanger`, `MutatingAdmissionWebhook`, `NamespaceLifecycle`, `NodeRestriction`, `ResourceQuota`, `ServiceAccount`, `ValidatingAdmissionWebhook`, `PodSecurityPolicy`, `TaintNodesByCondition`, `StorageObjectInUseProtection`, `PersistentVolumeClaimResize`, `ExtendedResourceToleration`, `CertificateApproval`, `PodPriority`, `CertificateSigning`, `CertificateSubjectRestriction`, `RuntimeClass`, and `DefaultIngressClass`\.


|  Kubernetes version  |  Amazon EKS platform version  |  Release notes  |  Release date  | 
| --- | --- | --- | --- | 
|  `1.24.15`  |  `eks-local-outposts.6`  |  New platform version with security fixes and enhancements\. `kube-proxy` updated to `v1.24.15`\. Amazon VPC CNI plugin for Kubernetes updated to `v1.13.2`\.   | July 14, 2023 | 
|  `1.24.13`  |  `eks-local-outposts.5`  | New platform version with security fixes and enhancements\. | July 13, 2023 | 
|  `1.24.9`  |  `eks-local-outposts.4`  | Updated Bottlerocket version to 1\.13\.2 | May 2, 2023 | 
|  `1.24.9`  |  `eks-local-outposts.3`  | Amazon EKS control plane instance operating system updated to Bottlerocket version v1\.13\.1 and Amazon VPC CNI plugin for Kubernetes updated to version v1\.12\.6\. | April 14, 2023 | 
|  `1.24.9`  |  `eks-local-outposts.2`  |  Improved diagnostics collection for Kubernetes control plane instances\.  | March 8, 2023 | 
|  `1.24.9`  |  `eks-local-outposts.1`  |  Initial release of Kubernetes version `1.24` for local Amazon EKS clusters on Outposts\.  | January 17, 2023 | 

## Kubernetes version `1.23`<a name="platform-versions-1.23"></a>

The following admission controllers are enabled for all `1.23` platform versions: `DefaultStorageClass`, `DefaultTolerationSeconds`, `LimitRanger`, `MutatingAdmissionWebhook`, `NamespaceLifecycle`, `NodeRestriction`, `ResourceQuota`, `ServiceAccount`, `ValidatingAdmissionWebhook`, `PodSecurityPolicy`, `TaintNodesByCondition`, `StorageObjectInUseProtection`, `PersistentVolumeClaimResize`, `ExtendedResourceToleration`, `CertificateApproval`, `PodPriority`, `CertificateSigning`, `CertificateSubjectRestriction`, `RuntimeClass`, and `DefaultIngressClass`\.


|  Kubernetes version  |  Amazon EKS platform version  |  Release notes  |  Release date  | 
| --- | --- | --- | --- | 
|  `1.23.17`  |  `eks-local-outposts.5`  |  New platform version with security fixes and enhancements\.  | July 13, 2023 | 
|  `1.23.15`  |  `eks-local-outposts.4`  |  Updated Bottlerocket version to `1.13.2`  | May 2, 2023 | 
|  `1.23.15`  |  `eks-local-outposts.3`  |  Amazon EKS control plane instance operating system updated to Bottlerocket version `v1.13.1` and Amazon VPC CNI plugin for Kubernetes updated to version `v1.12.6`\.  | April 14, 2023 | 
|  `1.23.15`  |  `eks-local-outposts.2`  |  Improved diagnostics collection for Kubernetes control plane instances\.  | March 8, 2023 | 
|  `1.23.15`  |  `eks-local-outposts.1`  | Initial release of Kubernetes version `1.23` for local Amazon EKS clusters on Outposts\. | January 17, 2023 | 