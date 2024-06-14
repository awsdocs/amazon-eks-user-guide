--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Amazon EKS local cluster platform versions<a name="eks-outposts-platform-versions"></a>

Local cluster platform versions represent the capabilities of the Amazon EKS cluster on AWS Outposts\. The versions include the components that run on the Kubernetes control plane, which Kubernetes API server flags are enabled\. They also include the current Kubernetes patch version\. Each Kubernetes minor version has one or more associated platform versions\. The platform versions for different Kubernetes minor versions are independent\. The platform versions for local clusters and Amazon EKS clusters in the cloud are independent\.

When a new Kubernetes minor version is available for local clusters, such as `1.28`, the initial platform version for that Kubernetes minor version starts at `eks-local-outposts.1`\. However, Amazon EKS releases new platform versions periodically to enable new Kubernetes control plane settings and to provide security fixes\.

When new local cluster platform versions become available for a minor version:
+ The platform version number is incremented \(`eks-local-outposts.n+1`\)\.
+ Amazon EKS automatically updates all existing local clusters to the latest platform version for their corresponding Kubernetes minor version\. Automatic updates of existing platform versions are rolled out incrementally\. The roll\-out process might take some time\. If you need the latest platform version features immediately, we recommend that you create a new local cluster\.
+ Amazon EKS might publish a new node AMI with a corresponding patch version\. All patch versions are compatible between the Kubernetes control plane and node AMIs for a single Kubernetes minor version\.

New platform versions don’t introduce breaking changes or cause service interruptions\.

Local clusters are always created with the latest available platform version \(`eks-local-outposts.n`\) for the specified Kubernetes version\.

The current and recent platform versions are described in the following tables\.

## Kubernetes version `1.28`<a name="platform-versions-1.28"></a>

The following admission controllers are enabled for all `1.28` platform versions: `CertificateApproval`, `CertificateSigning`, `CertificateSubjectRestriction`, `DefaultIngressClass`, `DefaultStorageClass`, `DefaultTolerationSeconds`, `ExtendedResourceToleration`, `LimitRanger`, `MutatingAdmissionWebhook`, `NamespaceLifecycle`, `NodeRestriction`, `PersistentVolumeClaimResize`, `Priority`, `PodSecurity`, `ResourceQuota`, `RuntimeClass`, `ServiceAccount`, `StorageObjectInUseProtection`, `TaintNodesByCondition`, `ValidatingAdmissionPolicy`, and `ValidatingAdmissionWebhook`\.

```
Kubernetes version
```

```
Amazon EKS platform version
```

```
Release notes
```

```
Release date
```

## Kubernetes version `1.27`<a name="platform-versions-1.27"></a>

The following admission controllers are enabled for all `1.27` platform versions: `CertificateApproval`, `CertificateSigning`, `CertificateSubjectRestriction`, `DefaultIngressClass`, `DefaultStorageClass`, `DefaultTolerationSeconds`, `ExtendedResourceToleration`, `LimitRanger`, `MutatingAdmissionWebhook`, `NamespaceLifecycle`, `NodeRestriction`, `PersistentVolumeClaimResize`, `Priority`, `PodSecurity`, `ResourceQuota`, `RuntimeClass`, `ServiceAccount`, `StorageObjectInUseProtection`, `TaintNodesByCondition`, `ValidatingAdmissionPolicy`, and `ValidatingAdmissionWebhook`\.

```
Kubernetes version
```

```
Amazon EKS platform version
```

```
Release notes
```

```
Release date
```

## Kubernetes version `1.26`<a name="platform-versions-1.26"></a>

The following admission controllers are enabled for all `1.26` platform versions: `CertificateApproval`, `CertificateSigning`, `CertificateSubjectRestriction`, `DefaultIngressClass`, `DefaultStorageClass`, `DefaultTolerationSeconds`, `ExtendedResourceToleration`, `LimitRanger`, `MutatingAdmissionWebhook`, `NamespaceLifecycle`, `NodeRestriction`, `PersistentVolumeClaimResize`, `Priority`, `PodSecurity`, `ResourceQuota`, `RuntimeClass`, `ServiceAccount`, `StorageObjectInUseProtection`, `TaintNodesByCondition`, `ValidatingAdmissionPolicy`, and `ValidatingAdmissionWebhook`\.

```
Kubernetes version
```

```
Amazon EKS platform version
```

```
Release notes
```

```
Release date
```

## Kubernetes version `1.25`<a name="platform-versions-1.25"></a>

The following admission controllers are enabled for all `1.25` platform versions: `CertificateApproval`, `CertificateSigning`, `CertificateSubjectRestriction`, `DefaultIngressClass`, `DefaultStorageClass`, `DefaultTolerationSeconds`, `ExtendedResourceToleration`, `LimitRanger`, `MutatingAdmissionWebhook`, `NamespaceLifecycle`, `NodeRestriction`, `PersistentVolumeClaimResize`, `Priority`, `PodSecurity`, `ResourceQuota`, `RuntimeClass`, `ServiceAccount`, `StorageObjectInUseProtection`, `TaintNodesByCondition`, and `ValidatingAdmissionWebhook`\.

```
Kubernetes version
```

```
Amazon EKS platform version
```

```
Release notes
```

```
Release date
```

## Kubernetes version `1.24`<a name="platform-versions-1.24"></a>

The following admission controllers are enabled for all `1.24` platform versions: `DefaultStorageClass`, `DefaultTolerationSeconds`, `LimitRanger`, `MutatingAdmissionWebhook`, `NamespaceLifecycle`, `NodeRestriction`, `ResourceQuota`, `ServiceAccount`, `ValidatingAdmissionWebhook`, `PodSecurityPolicy`, `TaintNodesByCondition`, `StorageObjectInUseProtection`, `PersistentVolumeClaimResize`, `ExtendedResourceToleration`, `CertificateApproval`, `PodPriority`, `CertificateSigning`, `CertificateSubjectRestriction`, `RuntimeClass`, and `DefaultIngressClass`\.

```
Kubernetes version
```

```
Amazon EKS platform version
```

```
Release notes
```

```
Release date
```

## Kubernetes version `1.23`<a name="platform-versions-1.23"></a>

The following admission controllers are enabled for all `1.23` platform versions: `DefaultStorageClass`, `DefaultTolerationSeconds`, `LimitRanger`, `MutatingAdmissionWebhook`, `NamespaceLifecycle`, `NodeRestriction`, `ResourceQuota`, `ServiceAccount`, `ValidatingAdmissionWebhook`, `PodSecurityPolicy`, `TaintNodesByCondition`, `StorageObjectInUseProtection`, `PersistentVolumeClaimResize`, `ExtendedResourceToleration`, `CertificateApproval`, `PodPriority`, `CertificateSigning`, `CertificateSubjectRestriction`, `RuntimeClass`, and `DefaultIngressClass`\.

```
Kubernetes version
```

```
Amazon EKS platform version
```

```
Release notes
```

```
Release date
```