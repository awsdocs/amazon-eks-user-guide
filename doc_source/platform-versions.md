# Amazon EKS platform versions<a name="platform-versions"></a>

Amazon EKS platform versions represent the capabilities of the Amazon EKS cluster control plane, such as which Kubernetes API server flags are enabled, as well as the current Kubernetes patch version\. Each Kubernetes minor version has one or more associated Amazon EKS platform versions\. The platform versions for different Kubernetes minor versions are independent\. If you have a local cluster on AWS Outposts, see [Amazon EKS local cluster platform versions](eks-outposts-platform-versions.md) instead of this topic\.

When a new Kubernetes minor version is available in Amazon EKS, such as 1\.28, the initial Amazon EKS platform version for that Kubernetes minor version starts at `eks.1`\. However, Amazon EKS releases new platform versions periodically to enable new Kubernetes control plane settings and to provide security fixes\.

When new Amazon EKS platform versions become available for a minor version:
+ The Amazon EKS platform version number is incremented \(`eks.n+1`\)\.
+ Amazon EKS automatically upgrades all existing clusters to the latest Amazon EKS platform version for their corresponding Kubernetes minor version\. Automatic upgrades of existing Amazon EKS platform versions are rolled out incrementally\. The roll\-out process might take some time\. If you need the latest Amazon EKS platform version features immediately, you should create a new Amazon EKS cluster\.

  If your cluster is more than two platform versions behind the current platform version, then it's possible that Amazon EKS wasn't able to automatically update your cluster\. For details of what may cause this, see [Amazon EKS platform version is more than two versions behind the current platform version](troubleshooting.md#troubleshooting-platform-version)\.
+ Amazon EKS might publish a new node AMI with a corresponding patch version\. However, all patch versions are compatible between the EKS control plane and node AMIs for a given Kubernetes minor version\.

 New Amazon EKS platform versions don't introduce breaking changes or cause service interruptions\.

Clusters are always created with the latest available Amazon EKS platform version \(`eks.n`\) for the specified Kubernetes version\. If you update your cluster to a new Kubernetes minor version, your cluster receives the current Amazon EKS platform version for the Kubernetes minor version that you updated to\.

The current and recent Amazon EKS platform versions are described in the following tables\.

## Kubernetes version `1.28`<a name="platform-versions-1.28"></a>

The following admission controllers are enabled for all `1.28` platform versions: `NodeRestriction`, `ExtendedResourceToleration`, `NamespaceLifecycle`, `LimitRanger`, `ServiceAccount`, `TaintNodesByCondition`, `PodSecurity`, `Priority`, `DefaultTolerationSeconds`, `DefaultStorageClass`, `StorageObjectInUseProtection`, `PersistentVolumeClaimResize`, `RuntimeClass`, `CertificateApproval`, `CertificateSigning`, `CertificateSubjectRestriction`, `DefaultIngressClass`, `MutatingAdmissionWebhook`, `ValidatingAdmissionPolicy`, `ValidatingAdmissionWebhook`, `ResourceQuota`\.


|  Kubernetes version  |  Amazon EKS platform version  |  Release notes  |  Release date  | 
| --- | --- | --- | --- | 
|  `1.28.3`  |  `eks.3`  |  New platform version with security fixes and enhancements\.  | November 3, 2023 | 
|  `1.28.2`  |  `eks.2`  |  New platform version with security fixes and enhancements\.  | October 16, 2023 | 
|  `1.28.1`  |  `eks.1`  |  Initial release of Kubernetes version `1.28` for Amazon EKS\. For more information, see [Kubernetes 1\.28](kubernetes-versions-standard.md#kubernetes-1.28)\.  | September 26, 2023 | 

## Kubernetes version `1.27`<a name="platform-versions-1.27"></a>

The following admission controllers are enabled for all `1.27` platform versions: `NodeRestriction`, `ExtendedResourceToleration`, `NamespaceLifecycle`, `LimitRanger`, `ServiceAccount`, `TaintNodesByCondition`, `PodSecurity`, `Priority`, `DefaultTolerationSeconds`, `DefaultStorageClass`, `StorageObjectInUseProtection`, `PersistentVolumeClaimResize`, `RuntimeClass`, `CertificateApproval`, `CertificateSigning`, `CertificateSubjectRestriction`, `DefaultIngressClass`, `MutatingAdmissionWebhook`, `ValidatingAdmissionPolicy`, `ValidatingAdmissionWebhook`, `ResourceQuota`\.


|  Kubernetes version  |  Amazon EKS platform version  |  Release notes  |  Release date  | 
| --- | --- | --- | --- | 
|  `1.27.7`  |  `eks.7`  |  New platform version with security fixes and enhancements\.  | November 3, 2023 | 
|  `1.27.6`  |  `eks.6`  |  New platform version with security fixes and enhancements\.  | October 16, 2023 | 
|  `1.27.4`  |  `eks.5`  |  New platform version with security fixes and enhancements\.  | August 30, 2023 | 
|  `1.27.4`  |  `eks.4`  |  New platform version with security fixes and enhancements\.  | July 30, 2023 | 
|  `1.27.3`  |  `eks.3`  |  New platform version with security fixes and enhancements\.  | June 30, 2023 | 
|  `1.27.2`  |  `eks.2`  |  New platform version with security fixes and enhancements\.  | June 9, 2023 | 
|  `1.27.1`  |  `eks.1`  |  Initial release of Kubernetes version `1.27` for Amazon EKS\. For more information, see [Kubernetes 1\.27](kubernetes-versions-standard.md#kubernetes-1.27)\.  | May 24, 2023 | 

## Kubernetes version `1.26`<a name="platform-versions-1.26"></a>

The following admission controllers are enabled for all `1.26` platform versions: `NodeRestriction`, `ExtendedResourceToleration`, `NamespaceLifecycle`, `LimitRanger`, `ServiceAccount`, `TaintNodesByCondition`, `PodSecurity`, `Priority`, `DefaultTolerationSeconds`, `DefaultStorageClass`, `StorageObjectInUseProtection`, `PersistentVolumeClaimResize`, `RuntimeClass`, `CertificateApproval`, `CertificateSigning`, `CertificateSubjectRestriction`, `DefaultIngressClass`, `MutatingAdmissionWebhook`, `ValidatingAdmissionPolicy`, `ValidatingAdmissionWebhook`, `ResourceQuota`\.


|  Kubernetes version  |  Amazon EKS platform version  |  Release notes  |  Release date  | 
| --- | --- | --- | --- | 
|  `1.26.10`  |  `eks.8`  |  New platform version with security fixes and enhancements\.  | November 3, 2023 | 
|  `1.26.9`  |  `eks.7`  |  New platform version with security fixes and enhancements\.  | October 16, 2023 | 
|  `1.26.7`  |  `eks.6`  |  New platform version with security fixes and enhancements\.  | August 30, 2023 | 
|  `1.26.7`  |  `eks.5`  |  New platform version with security fixes and enhancements\.  | July 30, 2023 | 
|  `1.26.6`  |  `eks.4`  |  New platform version with security fixes and enhancements\.  | June 30, 2023 | 
|  `1.26.5`  |  `eks.3`  |  New platform version with security fixes and enhancements\.  | June 9, 2023 | 
|  `1.26.4`  |  `eks.2`  |  New platform version with security fixes and enhancements\.  | May 5, 2023 | 
|  `1.26.2`  |  `eks.1`  |  Initial release of Kubernetes version `1.26` for Amazon EKS\. For more information, see [Kubernetes 1\.26](kubernetes-versions-standard.md#kubernetes-1.26)\.  | April 11, 2023 | 

## Kubernetes version `1.25`<a name="platform-versions-1.25"></a>

The following admission controllers are enabled for all `1.25` platform versions: `NodeRestriction`, `ExtendedResourceToleration`, `NamespaceLifecycle`, `LimitRanger`, `ServiceAccount`, `TaintNodesByCondition`, `PodSecurity`, `Priority`, `DefaultTolerationSeconds`, `DefaultStorageClass`, `StorageObjectInUseProtection`, `PersistentVolumeClaimResize`, `RuntimeClass`, `CertificateApproval`, `CertificateSigning`, `CertificateSubjectRestriction`, `DefaultIngressClass`, `MutatingAdmissionWebhook`, `ValidatingAdmissionPolicy`, `ValidatingAdmissionWebhook`, `ResourceQuota`\.


|  Kubernetes version  |  Amazon EKS platform version  |  Release notes  |  Release date  | 
| --- | --- | --- | --- | 
|  `1.25.15`  |  `eks.9`  |  New platform version with security fixes and enhancements\.  | November 3, 2023 | 
|  `1.25.14`  |  `eks.8`  |  New platform version with security fixes and enhancements\.  | October 16, 2023 | 
|  `1.25.12`  |  `eks.7`  |  New platform version with security fixes and enhancements\.  | August 30, 2023 | 
|  `1.25.12`  |  `eks.6`  |  New platform version with security fixes and enhancements\.  | July 30, 2023 | 
|  `1.25.11`  |  `eks.5`  | New platform version with security fixes and enhancements\. | June 30, 2023 | 
|  `1.25.10`  |  `eks.4`  | New platform version with security fixes and enhancements\. | June 9, 2023 | 
|  `1.25.9`  |  `eks.3`  | New platform version with security fixes and enhancements\. | May 5, 2023 | 
|  `1.25.8`  |  `eks.2`  |  New platform version with security fixes and enhancements\.  | March 24, 2023 | 
|  `1.25.6`  |  `eks.1`  |  Initial release of Kubernetes version `1.25` for Amazon EKS\. For more information, see [Kubernetes 1\.25](kubernetes-versions-standard.md#kubernetes-1.25)\.  | February 21, 2023 | 

## Kubernetes version `1.24`<a name="platform-versions-1.24"></a>

The following admission controllers are enabled for all `1.24` platform versions: `CertificateApproval`, `CertificateSigning`, `CertificateSubjectRestriction`, `DefaultIngressClass`, `DefaultStorageClass`, `DefaultTolerationSeconds`, `ExtendedResourceToleration`, `LimitRanger`, `MutatingAdmissionWebhook`, `NamespaceLifecycle`, `NodeRestriction`, `PersistentVolumeClaimResize`, `Priority`, `PodSecurityPolicy`, `ResourceQuota`, `RuntimeClass`, `ServiceAccount`, `StorageObjectInUseProtection`, `TaintNodesByCondition`, and `ValidatingAdmissionWebhook`\.


|  Kubernetes version  |  Amazon EKS platform version  |  Release notes  |  Release date  | 
| --- | --- | --- | --- | 
|  `1.24.17`  |  `eks.12`  |  New platform version with security fixes and enhancements\.  | November 3, 2023 | 
|  `1.24.17`  |  `eks.11`  |  New platform version with security fixes and enhancements\.  | October 16, 2023 | 
|  `1.24.16`  |  `eks.10`  |  New platform version with security fixes and enhancements\.  | August 30, 2023 | 
|  `1.24.16`  |  `eks.9`  |  New platform version with security fixes and enhancements\.  | July 30, 2023 | 
|  `1.24.15`  |  `eks.8`  |  New platform version with security fixes and enhancements\.   | June 30, 2023 | 
|  `1.24.14`  |  `eks.7`  |  New platform version with security fixes and enhancements\.   | June 9, 2023 | 
|  `1.24.13`  |  `eks.6`  |  New platform version with security fixes and enhancements\.   | May 5, 2023 | 
|  `1.24.12`  |  `eks.5`  |  New platform version with security fixes and enhancements\.   | March 24, 2023 | 
|  `1.24.8`  |  `eks.4`  |  New platform version with security fixes and enhancements\.   | January 27, 2023 | 
|  `1.24.7`  |  `eks.3`  |  New platform version with security fixes and enhancements\.   | December 5, 2022 | 
|  `1.24.7`  |  `eks.2`  |  New platform version with security fixes and enhancements\.   | November 18, 2022 | 
|  `1.24.7`  |  `eks.1`  |  Initial release of Kubernetes version `1.24` for Amazon EKS\. For more information, see [Kubernetes 1\.24](kubernetes-versions-standard.md#kubernetes-1.24)\.  | November 15, 2022 | 

## Kubernetes version `1.23`<a name="platform-versions-1.23"></a>

The following admission controllers are enabled for all `1.23` platform versions: `CertificateApproval`, `CertificateSigning`, `CertificateSubjectRestriction`, `DefaultIngressClass`, `DefaultStorageClass`, `DefaultTolerationSeconds`, `ExtendedResourceToleration`, `LimitRanger`, `MutatingAdmissionWebhook`, `NamespaceLifecycle`, `NodeRestriction`, `PersistentVolumeClaimResize`, `Priority`, `PodSecurityPolicy`, `ResourceQuota`, `RuntimeClass`, `ServiceAccount`, `StorageObjectInUseProtection`, `TaintNodesByCondition`, and `ValidatingAdmissionWebhook`\.


|  Kubernetes version  |  Amazon EKS platform version  |  Release notes  |  Release date  | 
| --- | --- | --- | --- | 
|  `1.23.17`  |  `eks.14`  |  New platform version with security fixes and enhancements\.  | November 3, 2023 | 
|  `1.23.17`  |  `eks.13`  |  New platform version with security fixes and enhancements\.  | October 16, 2023 | 
|  `1.23.17`  |  `eks.12`  |  New platform version with security fixes and enhancements\.  | August 30, 2023 | 
|  `1.23.17`  |  `eks.11`  |  New platform version with security fixes and enhancements\.  | July 30, 2023 | 
|  `1.23.17`  |  `eks.10`  |  New platform version with security fixes and enhancements\.  | June 30, 2023 | 
|  `1.23.17`  |  `eks.9`  |  New platform version with security fixes and enhancements\.  | June 9, 2023 | 
|  `1.23.17`  |  `eks.8`  |  New platform version with security fixes and enhancements\.  | May 5, 2023 | 
|  `1.23.17`  |  `eks.7`  |  New platform version with security fixes and enhancements\.  | March 24, 2023 | 
|  `1.23.14`  |  `eks.6`  |  New platform version with security fixes and enhancements\.  | January 27, 2023 | 
|  `1.23.13`  |  `eks.5`  |  New platform version with security fixes and enhancements\.   | December 5, 2022 | 
|  `1.23.13`  |  `eks.4`  |  New platform version with security fixes and enhancements\.   | November 18, 2022 | 
|  `1.23.12`  |  `eks.3`  |  New platform version with security fixes and enhancements\.   | November 7, 2022 | 
|  `1.23.10`  |  `eks.2`  |  New platform version with security fixes and enhancements\.   | September 21, 2022 | 
|  `1.23.7`  |  `eks.1`  |  Initial release of Kubernetes version `1.23` for Amazon EKS\. For more information, see [Kubernetes 1\.23](kubernetes-versions-extended.md#kubernetes-1.23)\.  | August 11, 2022 | 