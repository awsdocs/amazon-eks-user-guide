# Platform versions<a name="platform-versions"></a>

Amazon EKS platform versions represent the capabilities of the cluster control plane, such as which Kubernetes API server flags are enabled, as well as the current Kubernetes patch version\. Each Kubernetes minor version has one or more associated Amazon EKS platform versions\. The platform versions for different Kubernetes minor versions are independent\.

When a new Kubernetes minor version is available in Amazon EKS, such as 1\.18, the initial Amazon EKS platform version for that Kubernetes minor version starts at `eks.1`\. However, Amazon EKS releases new platform versions periodically to enable new Kubernetes control plane settings and to provide security fixes\.

When new Amazon EKS platform versions become available for a minor version:
+ The Amazon EKS platform version number is incremented \(`eks.<n+1>`\)\.
+ Amazon EKS automatically upgrades all existing clusters to the latest Amazon EKS platform version for their corresponding Kubernetes minor version\.
+ Amazon EKS might publish a new node AMI with a corresponding patch version\. However, all patch versions are compatible between the EKS control plane and node AMIs for a given Kubernetes minor version\.

 New Amazon EKS platform versions don't introduce breaking changes or cause service interruptions\. 

**Note**  
Automatic upgrades of existing Amazon EKS platform versions are rolled out incrementally\. The roll\-out process might take some time\. If you need the latest Amazon EKS platform version features immediately, you should create a new Amazon EKS cluster\.

Clusters are always created with the latest available Amazon EKS platform version \(`eks.<n>`\) for the specified Kubernetes version\. If you update your cluster to a new Kubernetes minor version, your cluster receives the current Amazon EKS platform version for the Kubernetes minor version that you updated to\.

The current and recent Amazon EKS platform versions are described in the following tables\.

## Kubernetes version 1\.18<a name="platform-versions-1.18"></a>


| Kubernetes version | Amazon EKS platform version | Enabled admission controllers | Release notes | 
| --- | --- | --- | --- | 
| 1\.18\.8 | eks\.1 | NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction, MutatingAdmissionWebhook, ValidatingAdmissionWebhook, PodSecurityPolicy, TaintNodesByCondition, Priority, StorageObjectInUseProtection, PersistentVolumeClaimResize | Initial release of Kubernetes 1\.18 for Amazon EKS\. For more information, see [Kubernetes 1\.18](kubernetes-versions.md#kubernetes-1.18)\. | 

## Kubernetes version 1\.17<a name="platform-versions-1.17"></a>


| Kubernetes version | Amazon EKS platform version | Enabled admission controllers | Release notes | 
| --- | --- | --- | --- | 
| 1\.17\.9 | eks\.3 | NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction, MutatingAdmissionWebhook, ValidatingAdmissionWebhook, PodSecurityPolicy, TaintNodesByCondition, Priority, StorageObjectInUseProtection, PersistentVolumeClaimResize | New platform version with support for [Security groups for pods](security-groups-for-pods.md)\. This release creates a vpc\-resource\-controller service account that is required for the VPC resource controller\. | 
| 1\.17\.9 | eks\.2 | NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction, MutatingAdmissionWebhook, ValidatingAdmissionWebhook, PodSecurityPolicy, TaintNodesByCondition, Priority, StorageObjectInUseProtection, PersistentVolumeClaimResize | New platform version with security fixes and enhancements, including UDP support for services of type LoadBalancer when using NLB and support for using Amazon EFS volumes with Fargate pods\. For more information, see the [Allow UDP for AWS NLB](https://github.com/kubernetes/kubernetes/pull/92109) issue on GitHub\. | 
| 1\.17\.6 | eks\.1 | NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction, MutatingAdmissionWebhook, ValidatingAdmissionWebhook, PodSecurityPolicy, TaintNodesByCondition, Priority, StorageObjectInUseProtection, PersistentVolumeClaimResize | Initial release of Kubernetes 1\.17 for Amazon EKS\. For more information, see [Kubernetes 1\.17](kubernetes-versions.md#kubernetes-1.17)\. | 

## Kubernetes version 1\.16<a name="platform-versions-1.16"></a>


| Kubernetes version | Amazon EKS platform version | Enabled admission controllers | Release notes | 
| --- | --- | --- | --- | 
| 1\.16\.13 | eks\.3 | NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction, MutatingAdmissionWebhook, ValidatingAdmissionWebhook, PodSecurityPolicy, TaintNodesByCondition, Priority, StorageObjectInUseProtection, PersistentVolumeClaimResize | New platform version with security fixes and enhancements, including UDP support for services of type LoadBalancer when using NLB\. For more information, see the [Allow UDP for AWS NLB](https://github.com/kubernetes/kubernetes/pull/92109) issue on GitHub\. | 
| 1\.16\.8 | eks\.2 | NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction, MutatingAdmissionWebhook, ValidatingAdmissionWebhook, PodSecurityPolicy, TaintNodesByCondition, Priority, StorageObjectInUseProtection, PersistentVolumeClaimResize | New platform version with security fixes\. | 
| 1\.16\.8 | eks\.1 | NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction, MutatingAdmissionWebhook, ValidatingAdmissionWebhook, PodSecurityPolicy, TaintNodesByCondition, Priority, StorageObjectInUseProtection, PersistentVolumeClaimResize | Initial release of Kubernetes 1\.16 for Amazon EKS\. For more information, see [Kubernetes 1\.16](kubernetes-versions.md#kubernetes-1.16)\. | 

## Kubernetes version 1\.15<a name="platform-versions-1.15"></a>


| Kubernetes version | Amazon EKS platform version | Enabled admission controllers | Release notes | 
| --- | --- | --- | --- | 
| 1\.15\.11 | eks\.4 | NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction, MutatingAdmissionWebhook, ValidatingAdmissionWebhook, PodSecurityPolicy, TaintNodesByCondition, Priority, StorageObjectInUseProtection, PersistentVolumeClaimResize | New platform version with security fixes and enhancements, including UDP support for services of type LoadBalancer when using NLB\. For more information, see the [Allow UDP for AWS NLB](https://github.com/kubernetes/kubernetes/pull/92109) issue on GitHub\. | 
| 1\.15\.11 | eks\.3 | NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction, MutatingAdmissionWebhook, ValidatingAdmissionWebhook, PodSecurityPolicy, TaintNodesByCondition, Priority, StorageObjectInUseProtection, PersistentVolumeClaimResize | New platform version with security fixes\. | 
| 1\.15\.11 | eks\.2 | NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction, MutatingAdmissionWebhook, ValidatingAdmissionWebhook, PodSecurityPolicy, TaintNodesByCondition, Priority, StorageObjectInUseProtection, PersistentVolumeClaimResize | New platform version with bug fixes and enhancements, including an update to the server side AWS IAM Authenticator, with [IAM role traceability](https://github.com/aws/containers-roadmap/issues/726) improvements\. | 
| 1\.15\.10 | eks\.1 | NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction, MutatingAdmissionWebhook, ValidatingAdmissionWebhook, PodSecurityPolicy, TaintNodesByCondition, Priority, StorageObjectInUseProtection, PersistentVolumeClaimResize | Initial release of Kubernetes 1\.15 for Amazon EKS\. For more information, see [Kubernetes 1\.15](kubernetes-versions.md#kubernetes-1.15)\. | 

## Kubernetes version 1\.14<a name="platform-versions-1.14"></a>


| Kubernetes version | Amazon EKS platform version | Enabled admission controllers | Release notes | 
| --- | --- | --- | --- | 
| 1\.15\.9 | eks\.11 | ​NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction, MutatingAdmissionWebhook, ValidatingAdmissionWebhook, PodSecurityPolicy | New platform version with security fixes and enhancements\. | 
| 1\.15\.9 | eks\.10 | ​NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction, MutatingAdmissionWebhook, ValidatingAdmissionWebhook, PodSecurityPolicy | New platform version with security fixes\. | 
| 1\.15\.9 | eks\.9 | ​NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction, MutatingAdmissionWebhook, ValidatingAdmissionWebhook, PodSecurityPolicy | New platform version with enhancements and additional feature support\. | 
| 1\.15\.9 | eks\.8 | ​NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction, MutatingAdmissionWebhook, ValidatingAdmissionWebhook, PodSecurityPolicy | New platform version with security and bug fixes\. | 
| 1\.15\.9 | eks\.7 | ​NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction, MutatingAdmissionWebhook, ValidatingAdmissionWebhook, PodSecurityPolicy | New platform version with security fixes\. | 
| 1\.15\.9 | eks\.6 | ​NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction, MutatingAdmissionWebhook, ValidatingAdmissionWebhook, PodSecurityPolicy | New platform version updating Amazon EKS Kubernetes 1\.14 clusters to 1\.14\.9, various bug fixes, and performance improvements\. | 
| 1\.15\.8 | eks\.5 | ​NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction, MutatingAdmissionWebhook, ValidatingAdmissionWebhook, PodSecurityPolicy | New platform version adding support for [AWS Fargate](fargate.md)\. | 
| 1\.15\.8 | eks\.4 | ​NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction, MutatingAdmissionWebhook, ValidatingAdmissionWebhook, PodSecurityPolicy | New platform version for various bug fixes and performance improvements\. | 
| 1\.15\.8 | eks\.3 | ​NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction, MutatingAdmissionWebhook, ValidatingAdmissionWebhook, PodSecurityPolicy | New platform version adding support for [Managed node groups](managed-node-groups.md)\. | 
| 1\.15\.8 | eks\.2 | ​NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction, MutatingAdmissionWebhook, ValidatingAdmissionWebhook, PodSecurityPolicy | New platform version updating Amazon EKS Kubernetes 1\.14 clusters to 1\.14\.8 to address [CVE\-2019\-11253](https://groups.google.com/forum/#!msg/kubernetes-security-announce/jk8polzSUxs/dfq6a-MnCQAJ)\. | 
| 1\.15\.6 | eks\.1 | ​NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction, MutatingAdmissionWebhook, ValidatingAdmissionWebhook, PodSecurityPolicy | Initial release of Kubernetes 1\.14 for Amazon EKS\. For more information, see [Kubernetes 1\.14](kubernetes-versions.md#kubernetes-1.14)\. | 