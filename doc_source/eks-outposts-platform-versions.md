# Amazon EKS local cluster platform versions<a name="eks-outposts-platform-versions"></a>

Local cluster platform versions represent the capabilities of the Amazon EKS cluster on Outposts\. The versions include the components that run on the Kubernetes control plane, which Kubernetes API server flags are enabled\. They also include the current Kubernetes patch version\. Each Kubernetes minor version has one or more associated platform versions\. The platform versions for different Kubernetes minor versions are independent\. The platform versions for local clusters and Amazon EKS clusters in the cloud are independent\.

When a new Kubernetes minor version is available for local clusters, such as `1.24`, the initial platform version for that Kubernetes minor version starts at `eks-local-outposts.1`\. However, Amazon EKS releases new platform versions periodically to enable new Kubernetes control plane settings and to provide security fixes\.

When new local cluster platform versions become available for a minor version:
+ The platform version number is incremented \(`eks-local-outposts.n+1`\)\.
+ Amazon EKS automatically updates all existing local clusters to the latest platform version for their corresponding Kubernetes minor version\. Automatic updates of existing platform versions are rolled out incrementally\. The roll\-out process might take some time\. If you need the latest platform version features immediately, we recommend that you create a new local cluster\. 
+ Amazon EKS might publish a new node AMI with a corresponding patch version\. All patch versions are compatible between the Kubernetes control plane and node AMIs for a single Kubernetes minor version\.

New platform versions don't introduce breaking changes or cause service interruptions\.

Local clusters are always created with the latest available platform version \(`eks-local-outposts.n`\) for the specified Kubernetes version\.

The current and recent platform versions are described in the following tables\.

## Kubernetes version `1.26`<a name="platform-versions-1.26"></a>

The following admission controllers are enabled for all `1.26` platform versions: `CertificateApproval`, `CertificateSigning`, `CertificateSubjectRestriction`, `DefaultIngressClass`, `DefaultStorageClass`, `DefaultTolerationSeconds`, `ExtendedResourceToleration`, `LimitRanger`, `MutatingAdmissionWebhook`, `NamespaceLifecycle`, `NodeRestriction`, `PersistentVolumeClaimResize`, `Priority`, `PodSecurity`, `ResourceQuota`, `RuntimeClass`, `ServiceAccount`, `StorageObjectInUseProtection`, `TaintNodesByCondition`, `ValidatingAdmissionPolicy` and `ValidatingAdmissionWebhook`\.


|  Kubernetes version  |  Amazon EKS platform version  |  Release notes  |  Release date  | 
| --- | --- | --- | --- | 
|  `1.26.2`  |  `eks-local-outposts.2`  |  Updated Bottlerocket version to `1.13.2`  | May 2, 2023 | 
|  `1.26.2`  |  `eks-local-outposts.1`  |  Initial release of Kubernetes version `1.26` for local Amazon EKS clusters on Outposts\.  | April 11, 2023 | 

## Kubernetes version `1.25`<a name="platform-versions-1.25"></a>

The following admission controllers are enabled for all `1.25` platform versions: `CertificateApproval`, `CertificateSigning`, `CertificateSubjectRestriction`, `DefaultIngressClass`, `DefaultStorageClass`, `DefaultTolerationSeconds`, `ExtendedResourceToleration`, `LimitRanger`, `MutatingAdmissionWebhook`, `NamespaceLifecycle`, `NodeRestriction`, `PersistentVolumeClaimResize`, `Priority`, `PodSecurity`, `ResourceQuota`, `RuntimeClass`, `ServiceAccount`, `StorageObjectInUseProtection`, `TaintNodesByCondition`, and `ValidatingAdmissionWebhook`\.


|  Kubernetes version  |  Amazon EKS platform version  |  Release notes  |  Release date  | 
| --- | --- | --- | --- | 
|  `1.25.6`  |  `eks-local-outposts.4`  |  Updated Bottlerocket version to `1.13.2`  | May 2, 2023 | 
|  `1.25.6`  |  `eks-local-outposts.3`  |  Amazon EKS control plane instance operating system updated to Bottlerocket version `v1.13.1` and Amazon VPC CNI plugin for Kubernetes updated to version `v1.12.6`\.  | April 14, 2023 | 
|  `1.25.6`  |  `eks-local-outposts.2`  |  Improved diagnostics collection for Kubernetes control plane instances\.  | March 8, 2023 | 
|  `1.25.6`  |  `eks-local-outposts.1`  | Initial release of Kubernetes version `1.25` for local Amazon EKS clusters on Outposts\. | March 1, 2023 | 

## Kubernetes version `1.24`<a name="platform-versions-1.24"></a>

The following admission controllers are enabled for all `1.24` platform versions: `DefaultStorageClass`, `DefaultTolerationSeconds`, `LimitRanger`, `MutatingAdmissionWebhook`, `NamespaceLifecycle`, `NodeRestriction`, `ResourceQuota`, `ServiceAccount`, `ValidatingAdmissionWebhook`, `PodSecurityPolicy`, `TaintNodesByCondition`, `StorageObjectInUseProtection`, `PersistentVolumeClaimResize`, `ExtendedResourceToleration`, `CertificateApproval`, `PodPriority`, `CertificateSigning`, `CertificateSubjectRestriction`, `RuntimeClass`, and `DefaultIngressClass`\.


|  Kubernetes version  |  Amazon EKS platform version  |  Release notes  |  Release date  | 
| --- | --- | --- | --- | 
|  `1.24.9`  |  `eks-local-outposts.4`  | Updated Bottlerocket version to 1\.13\.2 | May 2, 2023 | 
|  `1.24.9`  |  `eks-local-outposts.3`  | Amazon EKS control plane instance operating system updated to Bottlerocket version v1\.13\.1 and Amazon VPC CNI plugin for Kubernetes updated to version v1\.12\.6\. | April 14, 2023 | 
|  `1.24.9`  |  `eks-local-outposts.2`  |  Improved diagnostics collection for Kubernetes control plane instances\.  | March 8, 2023 | 
|  `1.24.9`  |  `eks-local-outposts.1`  |  Initial release of Kubernetes version `1.24` for local Amazon EKS clusters on Outposts\.  | January 17, 2023 | 

## Kubernetes version `1.23`<a name="platform-versions-1.23"></a>

The following admission controllers are enabled for all `1.23` platform versions: `DefaultStorageClass`, `DefaultTolerationSeconds`, `LimitRanger`, `MutatingAdmissionWebhook`, `NamespaceLifecycle`, `NodeRestriction`, `ResourceQuota`, `ServiceAccount`, `ValidatingAdmissionWebhook`, `PodSecurityPolicy`, `TaintNodesByCondition`, `StorageObjectInUseProtection`, `PersistentVolumeClaimResize`, `ExtendedResourceToleration`, `CertificateApproval`, `PodPriority`, `CertificateSigning`, `CertificateSubjectRestriction`, `RuntimeClass`, and `DefaultIngressClass`\.


|  Kubernetes version  |  Amazon EKS platform version  |  Release notes  |  Release date  | 
| --- | --- | --- | --- | 
|  `1.23.15`  |  `eks-local-outposts.4`  |  Updated Bottlerocket version to `1.13.2`  | May 2, 2023 | 
|  `1.23.15`  |  `eks-local-outposts.3`  |  Amazon EKS control plane instance operating system updated to Bottlerocket version `v1.13.1` and Amazon VPC CNI plugin for Kubernetes updated to version `v1.12.6`\.  | April 14, 2023 | 
|  `1.23.15`  |  `eks-local-outposts.2`  |  Improved diagnostics collection for Kubernetes control plane instances\.  | March 8, 2023 | 
|  `1.23.15`  |  `eks-local-outposts.1`  | Initial release of Kubernetes version `1.23` for local Amazon EKS clusters on Outposts\. | January 17, 2023 | 

## Kubernetes version `1.22`<a name="platform-versions-1.22"></a>

The following admission controllers are enabled for all `1.22` platform versions: `DefaultStorageClass`, `DefaultTolerationSeconds`, `LimitRanger`, `MutatingAdmissionWebhook`, `NamespaceLifecycle`, `NodeRestriction`, `ResourceQuota`, `ServiceAccount`, `ValidatingAdmissionWebhook`, `PodSecurityPolicy`, `TaintNodesByCondition`, `StorageObjectInUseProtection`, `PersistentVolumeClaimResize`, `ExtendedResourceToleration`, `CertificateApproval`, `PodPriority`, `CertificateSigning`, `CertificateSubjectRestriction`, `RuntimeClass`, and `DefaultIngressClass`\.


|  Kubernetes version  |  Amazon EKS platform version  |  Release notes  |  Release date  | 
| --- | --- | --- | --- | 
|  `1.22.17`  |  `eks-local-outposts.4`  |  Updated Bottlerocket version to `1.13.2`  | May 2, 2023 | 
|  `1.22.17`  |  `eks-local-outposts.3`  |  Amazon EKS control plane instance operating system updated to Bottlerocket version `v1.13.1` and Amazon VPC CNI plugin for Kubernetes updated to version `v1.12.6`\.  | April 14, 2023 | 
|  `1.22.17`  |  `eks-local-outposts.2`  |  Improved diagnostics collection for Kubernetes control plane instances\.  | March 8, 2023 | 
|  `1.22.17`  |  `eks-local-outposts.1`  | Initial release of Kubernetes version `1.22` for local Amazon EKS clusters on Outposts\. | January 17, 2023 | 

## Kubernetes version `1.21`<a name="platform-versions-1.21"></a>

The following admission controllers are enabled for all `1.21` platform versions: `DefaultStorageClass`, `DefaultTolerationSeconds`, `LimitRanger`, `MutatingAdmissionWebhook`, `NamespaceLifecycle`, `NodeRestriction`, `ResourceQuota`, `ServiceAccount`, `ValidatingAdmissionWebhook`, `PodSecurityPolicy`, `TaintNodesByCondition`, `StorageObjectInUseProtection`, `PersistentVolumeClaimResize`, `ExtendedResourceToleration`, `CertificateApproval`, `PodPriority`, `CertificateSigning`, `CertificateSubjectRestriction`, `RuntimeClass`, and `DefaultIngressClass`\.


|  Kubernetes version  |  Amazon EKS platform version  |  Release notes  |  Release date  | 
| --- | --- | --- | --- | 
|  `1.21.14`  |  `eks-local-outposts.5`  |  Improved diagnostics collection for Kubernetes control plane instances\.  | March 8, 2023 | 
|  `1.21.14`  |  `eks-local-outposts.4`  | Includes the following updates: [\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/eks-outposts-platform-versions.html) | January 17, 2023 | 
|  `1.21.14`  |  `eks-local-outposts.3`  | Amazon EKS control plane instance operating system updated to Bottlerocket v1\.11\.0, Kubernetes distribution updated to EKS\-D v1\-21\-eks\-21, and Amazon VPC CNI plugin for Kubernetes updated to v1\.11\.4\. | January 3, 2023 | 
|  `1.21.14`  |  `eks-local-outposts.2`  | Support for clusters that don’t have an ingress and egress internet connection \(also known as private clusters\)\. | November 4, 2022 | 
|  `1.21.13`  |  `eks-local-outposts.1`  | Initial release of local Amazon EKS clusters on Outposts\. | September 19, 2022 | 