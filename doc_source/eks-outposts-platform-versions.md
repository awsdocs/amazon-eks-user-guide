# Amazon EKS local cluster platform versions<a name="eks-outposts-platform-versions"></a>

Local cluster platform versions represent the capabilities of the Amazon EKS cluster on Outposts\. The versions include the components that run on the Kubernetes control plane, which Kubernetes API server flags are enabled\. They also include the current Kubernetes patch version\. Each Kubernetes minor version has one or more associated platform versions\. The platform versions for different Kubernetes minor versions are independent\. The platform versions for local clusters and Amazon EKS clusters in the cloud are independent\.

When a new Kubernetes minor version is available for local clusters, such as `1.21`, the initial platform version for that Kubernetes minor version starts at `eks-local-outposts.1`\. However, Amazon EKS releases new platform versions periodically to enable new Kubernetes control plane settings and to provide security fixes\.

When new local cluster platform versions become available for a minor version:
+ The platform version number is incremented \(`eks-local-outposts.n+1`\)\.
+ Amazon EKS automatically updates all existing local clusters to the latest platform version for their corresponding Kubernetes minor version\. Automatic updates of existing platform versions are rolled out incrementally\. The roll\-out process might take some time\. If you need the latest platform version features immediately, we recommend that you create a new local cluster\. 
+ Amazon EKS might publish a new node AMI with a corresponding patch version\. All patch versions are compatible between the Kubernetes control plane and node AMIs for a single Kubernetes minor version\.

New platform versions don't introduce breaking changes or cause service interruptions\.

Local clusters are always created with the latest available platform version \(`eks-local-outposts.n`\) for the specified Kubernetes version\.

The current and recent platform versions are described in the following table\.

## Kubernetes version `1.21`<a name="platform-versions-1.21"></a>

The following admission controllers are enabled for all `1.21` platform versions: `DefaultStorageClass`, `DefaultTolerationSeconds`, `LimitRanger`, `MutatingAdmissionWebhook`, `NamespaceLifecycle`, `NodeRestriction`, `ResourceQuota`, `ServiceAccount`, `ValidatingAdmissionWebhook`, `PodSecurityPolicy`, `TaintNodesByCondition`, `StorageObjectInUseProtection`, `PersistentVolumeClaimResize`, `ExtendedResourceToleration`, `CertificateApproval`, `PodPriority`, `CertificateSigning`, `CertificateSubjectRestriction`, `RuntimeClass`, and `DefaultIngressClass`\.


|  Kubernetes version  |  Amazon EKS platform version  |  Release notes  |  Release date  | 
| --- | --- | --- | --- | 
|  `1.21.14`  |  `eks-local-outposts.3`  | Support for clusters that doen’t have an ingress and egress internet connection \(also known as private clusters\)\. | November 26, 2022 | 
|  `1.21.13`  |  `eks-local-outposts.1`  | Initial release of local Amazon EKS clusters on Outposts\. | September 19, 2022 | 