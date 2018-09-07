# Platform Versions<a name="platform-versions"></a>

Starting with the release of Kubernetes [aggregation layer](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/) support in new clusters, Amazon EKS introduced the concept of platform versions, which allows you to identify the features that are currently enabled for your clusters\. The Amazon EKS platform version represents capabilities of the cluster control plane, such as which Kubernetes API server flags are enabled, as well as the current Kubernetes patch version\.

New clusters are created with the latest available platform version\. Existing clusters are automatically upgraded to the latest platform version in incremental roll outs\. To take advantage of the latest platform version features immediately, you can create a new Amazon EKS cluster\.

Current and recent Amazon EKS platform versions are described in the table below\. 


| Kubernetes Version | Kubernetes Patch Version | Amazon EKS Platform Version | Enabled Admission Controllers | Release Notes | 
| --- | --- | --- | --- | --- | 
| 1\.10 | 1\.10\.3 | eks\.2 | ​Initializers, NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction |  [\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html)  | 
| 1\.10 | 1\.10\.3 | eks\.1 | ​Initializers, NamespaceLifecycle, LimitRanger, ServiceAccount, DefaultStorageClass, ResourceQuota, DefaultTolerationSeconds, NodeRestriction | Initial launch of Amazon EKS\. | 