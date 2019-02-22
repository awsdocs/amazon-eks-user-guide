# Platform Versions<a name="platform-versions"></a>

Amazon EKS cluster platform versions represent the capabilities of the cluster control plane, such as which Kubernetes API server flags are enabled, as well as the current Kubernetes patch version\. Each Amazon EKS platform version is associated with, but independent of, a Kubernetes version\. 

When a new Kubernetes minor version is available in Amazon EKS \(for example, 1\.11\), the initial platform version for that Kubernetes minor version starts at `eks.1`\. However, Amazon EKS releases new platform versions periodically to enable new Kubernetes control plane settings and to provide security fixes\.

When new platform versions become available for a Kubernetes minor version:
+ The Amazon EKS platform version number is incremented \(`eks.n+1`\)\.
+ Amazon EKS automatically upgrades all existing clusters to the latest platform version for their corresponding Kubernetes minor version\.

 New platform versions do not introduce breaking changes or cause service interruptions\. 

**Note**  
Automatic upgrades of existing cluster platform versions are rolled out incrementally, and this process may take some time\. If you need the latest platform version features immediately, you should create a new Amazon EKS cluster\.

New clusters are always created with the latest available Amazon EKS platform version \(`eks.n`\) for the specified Kubernetes version\. If you update your cluster to a new Kubernetes minor version, your cluster receives the current platform version for the Kubernetes minor version that you updated to\.

The current and recent Amazon EKS platform versions are described in the following tables\. 

## Kubernetes 1\.11 Platform Versions<a name="1.11-platform-versions"></a>


| Kubernetes Version | Kubernetes Patch Version | Amazon EKS Platform Version | Enabled Admission Controllers | Release Notes | 
| --- | --- | --- | --- | --- | 
| 1\.11 | 1\.11\.5 | eks\.1 | ​Initializers, NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction, MutatingAdmissionWebhook, ValidatingAdmissionWebhook | Initial release of Kubernetes 1\.11 for Amazon EKS\. | 

## Kubernetes 1\.10 Platform Versions<a name="1.10-platform-versions"></a>


| Kubernetes Version | Kubernetes Patch Version | Amazon EKS Platform Version | Enabled Admission Controllers | Release Notes | 
| --- | --- | --- | --- | --- | 
| 1\.10 | 1\.10\.11 | eks\.3 | ​Initializers, NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction, MutatingAdmissionWebhook, ValidatingAdmissionWebhook |  New platform version updating Kubernetes to patch level 1\.10\.11 to address [CVE\-2018\-1002105](https://aws.amazon.com/security/security-bulletins/AWS-2018-020/)\.  | 
| 1\.10 | 1\.10\.3 | eks\.2 | ​Initializers, NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction, MutatingAdmissionWebhook, ValidatingAdmissionWebhook |  [\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html)  | 
| 1\.10 | 1\.10\.3 | eks\.1 | ​Initializers, NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction | Initial launch of Amazon EKS\. | 