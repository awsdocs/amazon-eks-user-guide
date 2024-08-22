# Review release notes for Kubernetes version 1\.22<a name="kubernetes-versions-1-21-1-22"></a>

**Important**  
You cannot create new clusters with these versions\.

This topic gives important changes to be aware of for version `1.22`\. When upgrading, carefully review the changes that have occurred between the old and new versions for your cluster\.

## Kubernetes version `1.22`<a name="platform-versions-1.22"></a>

The following admission controllers are enabled for all `1.22` platform versions: `DefaultStorageClass`, `DefaultTolerationSeconds`, `LimitRanger`, `MutatingAdmissionWebhook`, `NamespaceLifecycle`, `NodeRestriction`, `ResourceQuota`, `ServiceAccount`, `ValidatingAdmissionWebhook`, `PodSecurityPolicy`, `TaintNodesByCondition`, `StorageObjectInUseProtection`, `PersistentVolumeClaimResize`, `ExtendedResourceToleration`, `CertificateApproval`, `PodPriority`, `CertificateSigning`, `CertificateSubjectRestriction`, `RuntimeClass`, and `DefaultIngressClass`\.


| Kubernetes version | Amazon EKS platform version | Release notes | Release date | 
| --- | --- | --- | --- | 
|  `1.22.17`  |  `eks.28`  |  New platform version with security fixes and enhancements\.  | May 16, 2024 | 
|  `1.22.17`  |  `eks.26`  |  New platform version with security fixes and enhancements\.  | April 1, 2024 | 
|  `1.22.17`  |  `eks.14`  |  New platform version with security fixes and enhancements\.  | June 30, 2023 | 
|  `1.22.17`  |  `eks.13`  |  New platform version with security fixes and enhancements\.  | June 9, 2023 | 
|  `1.22.17`  |  `eks.12`  |  New platform version with security fixes and enhancements\.  | May 5, 2023 | 
|  `1.22.17`  |  `eks.11`  |  New platform version with security fixes and enhancements\.  | March 24, 2023 | 
|  `1.22.16`  |  `eks.10`  |  New platform version with security fixes and enhancements\.  | January 27, 2023 | 
|  `1.22.15`  |  `eks.9`  |  New platform version with security fixes and enhancements\.  | December 5, 2022 | 
|  `1.22.15`  |  `eks.8`  |  New platform version with security fixes and enhancements\.  | November 18, 2022 | 
|  `1.22.15`  |  `eks.7`  |  New platform version with security fixes and enhancements\.  | November 7, 2022 | 
|  `1.22.13`  |  `eks.6`  |  New platform version with security fixes and enhancements\.  | September 21, 2022 | 
|  `1.22.10`  |  `eks.5`  |  New platform version with improved `etcd` resiliency\.  | August 15, 2022 | 
|  `1.22.10`  |  `eks.4`  |  New platform version with security fixes and enhancements\. This platform version also introduces a new tagging controller which tags all worker nodes with `aws:eks:cluster-name` to make it easy to allocate cost for these worker nodes\. For more information, see [Tagging your resources for billing](eks-using-tags.md#tag-resources-for-billing)\.  | July 21, 2022 | 
|  `1.22.10`  |  `eks.3`  |  New platform version with security fixes and enhancements\.  | July 7, 2022 | 
|  `1.22.9`  |  `eks.2`  |  New platform version with security fixes and enhancements\.  | May 31, 2022 | 
|  `1.22.6`  |  `eks.1`  | Initial release of Kubernetes version 1\.22 for Amazon EKS\. | April 4, 2022 | 