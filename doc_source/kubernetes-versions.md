# Amazon EKS Kubernetes versions<a name="kubernetes-versions"></a>

The Kubernetes project is continually integrating new features, design updates, and bug fixes\. The community releases new Kubernetes minor versions, such as `1.22`\. New version updates are available on average every three months\. Each minor version is supported for approximately twelve months after it's first released\. 

## Available Amazon EKS Kubernetes versions<a name="available-versions"></a>

The following Kubernetes versions are currently available for new Amazon EKS clusters:
+ `1.22.9`
+ `1.21.12`
+ `1.20.15`
+ `1.19.16`

If your application doesn't require a specific version of Kubernetes, we recommend that you use the latest available Kubernetes version that's supported by Amazon EKS for your clusters\. As new Kubernetes versions become available in Amazon EKS, we recommend that you proactively update your clusters to use the latest available version\. For instructions on how to update your cluster, see [Updating an Amazon EKS cluster Kubernetes version](update-cluster.md)\. For more information about Kubernetes releases, see [Amazon EKS Kubernetes release calendar](#kubernetes-release-calendar) and [Amazon EKS version support and FAQ](#version-deprecation)\.

**Note**  
Starting with the Kubernetes version `1.23` launch, officially published Amazon EKS AMIs will include `containerd` as the only runtime\. Kubernetes version `1.18`–`1.21` use Docker as the default runtime\. However, these versions have a bootstrap flag option that you can use test out your workloads on any supported cluster with `containerd`\. For more information, see [Amazon EKS is ending support for `Dockershim`](dockershim-deprecation.md)\.

## Kubernetes`1.22`<a name="kubernetes-1.22"></a>

Kubernetes `1.22` is now available in Amazon EKS\. For more information about Kubernetes `1.22`, see the [official release announcement](https://kubernetes.io/blog/2021/08/04/kubernetes-1-22-release-announcement/)\.
+ Kubernetes `1.22` removes a number of APIs that are no longer available\. You might need to make changes to your application before you upgrade to Amazon EKS version `1.22`\. Follow the [Kubernetes version `1.22` prerequisites](update-cluster.md#update-1.22) carefully before updating your cluster\.
+ 
**Important**  
[https://github.com/kubernetes/enhancements/issues/542](https://github.com/kubernetes/enhancements/issues/542) graduated to stable and enabled by default in Kubernetes version `1.22`\. This feature improves security of service account tokens\. It allows workloads that are running on Kubernetes to request JSON web tokens that are audience, time, and key bound\. Service account tokens now have an expiration of one hour\. In previous Kubernetes versions, they didn't have an expiration\. This means that clients that rely on these tokens must refresh the tokens within an hour\. The following [Kubernetes client SDKs](https://kubernetes.io/docs/reference/using-api/client-libraries/) refresh tokens automatically within the required time frame:  
Go version `0.15.7` and later
Python version `12.0.0` and later
Java version `9.0.0` and later
JavaScript version `0.10.3` and later
Ruby `master` branch
Haskell version `0.3.0.0`
C\# version `7.0.5` and later
If your workload is using an older client version, then you must update it\. To enable a smooth migration of clients to the newer time\-bound service account tokens, Kubernetes version `1.22` adds an extended expiry period to the service account token over the default one hour\. For Amazon EKS clusters, the extended expiry period is 90 days\. Your Amazon EKS cluster's Kubernetes API server rejects requests with tokens older than 90 days\. We recommend that you check your applications and their dependencies to make sure that the Kubernetes client SDKs are the same or later than the versions listed above\. For instructions about how to identify pods that are using stale tokens, see [Kubernetes service accounts](service-accounts.md#identify-pods-using-stale-tokens)\.
+ The Ingress API versions `extensions/v1beta1` and `networking.k8s.io/v1beta1` have been removed in Kubernetes `1.22`\. If you're using the [https://github.com/kubernetes-sigs/aws-load-balancer-controller](https://github.com/kubernetes-sigs/aws-load-balancer-controller), you must upgrade to at least [version `2.4.1`](https://github.com/kubernetes-sigs/aws-load-balancer-controller/releases/tag/v2.4.1) before you upgrade your Amazon EKS clusters to version `1.22`\. Additionally, you must modify [Ingress manifests](https://kubernetes.io/docs/reference/kubernetes-api/service-resources/ingress-v1/) to use apiVersion `networking.k8s.io/v1`\. This has been available since [Kubernetes version `1.19`](https://kubernetes.io/blog/2020/08/26/kubernetes-release-1.19-accentuate-the-paw-sitive/#ingress-graduates-to-general-availability))\. For more information about changes between Ingress `v1beta1` and `v1`, see the [Kubernetes documentation](https://kubernetes.io/docs/reference/using-api/deprecation-guide/#ingress-v122)\. The AWS Load Balancer Controller [controller sample manifest](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.4/guide/ingress/spec/) uses the `v1` spec\.
+ The Amazon EKS legacy [Windows support controllers](https://docs.aws.amazon.com/eks/latest/userguide/windows-support.html#legacy-windows-support) use the `admissionregistration.k8s.io/v1beta1` API that was removed in Kubernetes `1.22`\. If you're running Windows workloads, you must remove legacy [Windows support](https://docs.aws.amazon.com/eks/latest/userguide/windows-support.html#remove-windows-support-data-plane) and enable [Windows support](https://docs.aws.amazon.com/eks/latest/userguide/windows-support.html#enable-windows-support) before upgrading to Amazon EKS version `1.22`\.
+ The [CertificateSigningRequest \(CSR\)](https://kubernetes.io/docs/reference/kubernetes-api/authentication-resources/certificate-signing-request-v1) API version `certificates.k8s.io/v1beta1` was removed in Kubernetes version `1.22`\. You must migrate manifests and API clients to use the `certificates.k8s.io/v1` CSR API\. This API has been available since version `1.19`\. For instructions on how to use CSR in Amazon EKS, see [Certificate signing](cert-signing.md)\.
+ The `CustomResourceDefinition` API version `apiextensions.k8s.io/v1beta1` was removed in Kubernetes `1.22`\. Make sure that all custom resource definitions in your cluster are updated to `v1`\. API version `v1` custom resource definitions are required to have Open API `v3` schema validation defined\. For more information, see the [Kubernetes documentation](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)\.
+ If you're using App Mesh, you must upgrade to at least App Mesh controller `[v1\.4\.3](https://github.com/aws/aws-app-mesh-controller-for-k8s/releases/tag/v1.4.3)` or later before you upgrade to Amazon EKS version `1.22`\. Older versions of the App Mesh controller use `v1beta1` `CustomResourceDefinition` API version and aren't compatible with Kubernetes version `1.22` and later\.
+  Amazon EKS version `1.22` enables the `EndpointSliceTerminatingCondition` feature by default, which will include pods in terminating state within EndpointSlices\. If you set `enableEndpointSlices` to `True` \(the default is disabled\) in the AWS Load Balancer Controller, you must upgraded to at least AWS Load Balancer Controller version `2.4.1+` before upgrading to Amazon EKS versionn `1.22`\. 
+  Starting with Amazon EKS version `1.22`, `kube-proxy` is configured by default to expose Prometheus metrics outside the pod\. This behavior change addresses the request made in containers roadmap issue [ \#657 ](https://github.com/aws/containers-roadmap/issues/657)\. 
+  The initial launch of Amazon EKS version `1.22` uses `etcd` version `3.4` as a backend, and is not affected by the [possibility of data corruption](https://groups.google.com/a/kubernetes.io/g/dev/c/B7gJs88XtQc/m/rSgNOzV2BwAJ?pli=1) present in `etcd` version `3.5`\. 
+ Starting with Amazon EKS `1.22`, Amazon EKS is decoupling AWS cloud\-specific control logic from core control plane code to the [out\-of\-tree](https://github.com/kubernetes/cloud-provider-aws) AWS Kubernetes [Cloud Controller Manager](https://kubernetes.io/docs/concepts/architecture/cloud-controller/)\. This is in line with the upstream Kubernetes recommendation\. By decoupling the interoperability logic between Kubernetes and the underlying cloud infrastructure, the `cloud-controller-manager` component enables cloud providers to release features at a different pace compared to the main Kubernetes project\. This change is transparent and requires no action\. However, a new log stream named `cloud-controller-manager` now appears under the `ControllerManager` log type when enabled\. For more information, see [Amazon EKS control plane logging](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html)\.
+ Starting with Amazon EKS `1.22`, Amazon EKS is changing the default AWS Security Token Service endpoint used by IAM roles for service accounts \(IRSA\) to be the regional endpoint instead of the global endpoint to reduce latency and improve reliability\. You can optionally configure IRSA to use the global endpoint in [Associate an IAM role to a service account](specify-service-account-role.md)\.

The following Kubernetes features are now supported in Kubernetes `1.22` Amazon EKS clusters:
+ **[Server\-side Apply graduates to GA](https://kubernetes.io/docs/reference/using-api/server-side-apply/)** \- Server\-side Apply helps users and controllers manage their resources through declarative configurations\. It allows them to create or modify objects declaratively by sending their fully specified intent\. After being in beta for a couple releases, Server\-side Apply is now generally available\.
+ [Warning mechanism for deprecated API user](https://github.com/kubernetes/enhancements/issues/1693) \- Use of deprecated APIs produces warnings visible to API consumers, and metrics visible to cluster administrators\.

 For the complete Kubernetes `1.22` changelog, see [https://github\.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG\-1\.22\.md\#changelog\-since\-v1210](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.22.md#changelog-since-v1210)\.

## Kubernetes`1.21`<a name="kubernetes-1.21"></a>

Kubernetes `1.21` is now available in Amazon EKS\. For more information about Kubernetes `1.21`, see the [official release announcement](https://kubernetes.io/blog/2021/04/08/kubernetes-1-21-release-announcement/)\.
+ 
**Important**  
[https://github.com/kubernetes/enhancements/issues/542](https://github.com/kubernetes/enhancements/issues/542) graduated to beta and is enabled by default in Kubernetes version `1.21`\. This feature improves security of service account tokens by allowing workloads running on Kubernetes to request JSON web tokens that are audience, time, and key bound\. Service account tokens now have an expiration of one hour\. In previous Kubernetes versions, they didn't have an expiration\. This means that clients that rely on these tokens must refresh the tokens within an hour\. The following [Kubernetes client SDKs](https://kubernetes.io/docs/reference/using-api/client-libraries/) refresh tokens automatically within the required time frame:  
Go version `0.15.7` and later
Python version `12.0.0` and later
Java version `9.0.0` and later
JavaScript version `0.10.3` and later
Ruby `master` branch
Haskell version `0.3.0.0`
C\# version `7.0.5` and later
If your workload is using an older client version, then you must update it\. To enable a smooth migration of clients to the newer time\-bound service account tokens, Kubernetes version `1.21` adds an extended expiry period to the service account token over the default one hour\. For Amazon EKS clusters, the extended expiry period is 90 days\. Your Amazon EKS cluster's Kubernetes API server rejects requests with tokens older than 90 days\. We recommend that you check your applications and their dependencies to make sure that the Kubernetes client SDKs are the same or later than the versions listed above\. For instructions about how to identify pods that are using stale tokens, see [Kubernetes service accounts](service-accounts.md#identify-pods-using-stale-tokens)\.
+ [Dual\-stack networking](https://kubernetes.io/docs/concepts/services-networking/dual-stack/) support \(`IPv4` and `IPv6` addresses\) on pods, services, and nodes reached beta status\. However, Amazon EKS and the Amazon VPC CNI plugin for Kubernetes don't currently support dual stack networking\. 
+ The Amazon EKS Optimized Amazon Linux 2 AMI now contains a bootstrap flag to enable the `containerd` runtime as a Docker alternative\. This flag allows preparation for the [removal of Docker as a supported runtime](https://kubernetes.io/blog/2020/12/02/dockershim-faq/) in the next Kubernetes release\. For more information, see [Enable the `containerd` runtime bootstrap flag](eks-optimized-ami.md#containerd-bootstrap)\. This can be tracked through the [ container roadmap on Github](https://github.com/aws/containers-roadmap/issues/313)\.
+ Managed node groups support for Cluster Autoscaler priority expander\. 

  Newly created managed node groups on Amazon EKS version `1.21` clusters use the following format for the underlying Auto Scaling group name: 

  `eks-<managed-node-group-name>-<uuid>`

  This enables using the [priority expander](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/expander/priority/readme.md) feature of Cluster Autoscaler to scale node groups based on user defined priorities\. A common use case is to prefer scaling spot node groups over on\-demand groups\. This behavior change solves the [containers roadmap issue \#1304](https://github.com/aws/containers-roadmap/issues/1304)\.

The following Kubernetes features are now supported in Amazon EKS `1.21` clusters:
+ [CronJobs](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/) \(previously ScheduledJobs\) have now graduated to stable status\. With this change, users perform regularly scheduled actions such as backups and report generation\.
+ [Immutable Secrets and ConfigMaps](https://kubernetes.io/docs/concepts/configuration/secret/#secret-immutable) have now graduated to stable status\. A new, immutable field was added to these objects to reject changes\. This rejection protects the cluster from updates that can unintentionally break the applications\. Because these resources are immutable, `kubelet` doesn't watch or poll for changes\. This reduces `kube-apiserver` load and improving scalability and performance\.
+ [Graceful Node Shutdown](https://kubernetes.io/blog/2021/04/21/graceful-node-shutdown-beta/) has now graduated to beta status\. With this update, the `kubelet` is aware of node shutdown and can gracefully terminate that node's pods\. Before this update, when a node shutdown, its pods didn't follow the expected termination lifecycle\. This caused workload problems\. Now, the `kubelet` can detect imminent system shutdown through `systemd`, and inform running pods so they terminate gracefully\.
+ Pods with multiple containers can now use the `kubectl.kubernetes.io/default-container` annotation to have a container preselected for `kubectl` commands\.
+ PodSecurityPolicy is being phased out\. PodSecurityPolicy will still be functional for several more releases according to Kubernetes deprecation guidelines\. For more information, see [PodSecurityPolicy Deprecation: Past, Present, and Future](https://kubernetes.io/blog/2021/04/06/podsecuritypolicy-deprecation-past-present-and-future) and the [AWS blog](http://aws.amazon.com/blogs/containers/using-gatekeeper-as-a-drop-in-pod-security-policy-replacement-in-amazon-eks/)\.

 

For the complete Kubernetes `1.21` changelog, see [https://github\.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG\-1\.21\.md](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.21.md)\.

## Kubernetes`1.20`<a name="kubernetes-1.20"></a>

For more information about Kubernetes `1.20`, see the [official release announcement](https://kubernetes.io/blog/2020/12/08/kubernetes-1-20-release-announcement/)\.
+ `1.20` brings new default roles and users\. You can find more information in [Default EKS Kubernetes roles and users](https://docs.aws.amazon.com/eks/latest/userguide/default-roles-users.html)\. Ensure that you are using a [supported cert\-manager version](https://cert-manager.io/docs/installation/supported-releases/)\.

The following Kubernetes features are now supported in Kubernetes `1.20` Amazon EKS clusters:
+ [API Priority and Fairness](https://kubernetes.io/docs/concepts/cluster-administration/flow-control/) has reached beta status and is enabled by default\. This allows `kube-apiserver` to categorize incoming requests by priority levels\.
+ [RuntimeClass](https://kubernetes.io/docs/concepts/containers/runtime-class/) has reached stable status\. The `RuntimeClass` resource provides a mechanism for supporting multiple runtimes in a cluster and surfaces information about that container runtime to the control plane\.
+ [Process ID Limits](https://kubernetes.io/docs/concepts/policy/pid-limiting/) has now graduated to general availability\.
+ [kubectl debug](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/) has reached beta status\. `kubectl debug` provides support for common debugging workflows directly from `kubectl`\.
+ The Docker container runtime has been phased out\. The Kubernetes community has written a [blog post](https://blog.k8s.io/2020/12/02/dont-panic-kubernetes-and-docker/) about this in detail with a dedicated [FAQ page](https://blog.k8s.io/2020/12/02/dockershim-faq/)\. Docker\-produced images can continue to be used and will work as they always have\. You can safely ignore the `Dockershim` deprecation warning message printed in `kubelet` startup logs\. Amazon EKS will eventually move to `containerd` as the runtime for the Amazon EKS optimized Amazon Linux 2 AMI\. You can follow the containers roadmap [issue](https://github.com/aws/containers-roadmap/issues/313#issuecomment-831617671) for more details\.
+ Pod Hostname as FQDN has graduated to beta status\. This feature allows setting a pod’s hostname to its Fully Qualified Domain Name \(FQDN\), giving the ability to set the hostname field of the kernel to the FQDN of a pod\.
+ The client\-go credential plugins can now be passed in the current cluster information via the `KUBERNETES_EXEC_INFO` environment variable\. This enhancement allows Go clients to authenticate using external credential providers, such as a key management system \(KMS\)\.

For the complete Kubernetes `1.20` changelog, see [https://github\.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG\-1\.20\.md](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.20.md)\.

## Kubernetes`1.19`<a name="kubernetes-1.19"></a>

For more information about Kubernetes `1.19`, see the [official release announcement](https://kubernetes.io/blog/2020/08/26/kubernetes-release-1.19-accentuate-the-paw-sitive/)\.
+ Starting with `1.19`, Amazon EKS no longer adds the `kubernetes.io/cluster/cluster-name` tag to subnets passed in when clusters are created\. This subnet tag is only required if you want to influence where the Kubernetes service controller or AWS Load Balancer Controller places Elastic Load Balancers\. For more information about the requirements of subnets passed to Amazon EKS during cluster creation, see updates to [Amazon EKS VPC and subnet requirements and considerations](network_reqs.md)\.
  + Subnet tags aren't modified on existing clusters updated to `1.19`\.
  + The AWS Load Balancer Controller version `2.1.1` and earlier required the *`cluster-name`* subnet tag\. In version `2.1.2` and later, you can specify the tag to refine subnet discovery, but it's not required\. For more information about the AWS Load Balancer Controller, see [Installing the AWS Load Balancer Controller add\-on](aws-load-balancer-controller.md)\. For more information about subnet tagging when using a load balancer, see [Application load balancing on Amazon EKS](alb-ingress.md) and [Network load balancing on Amazon EKS](network-load-balancing.md)\.
+ You're no longer required to provide a security context for non\-root containers that must access the web identity token file for use with IAM roles for service accounts\. For more information, see [IAM roles for service accounts](iam-roles-for-service-accounts.md) and[proposal for file permission handling in projected service account volume](https://github.com/kubernetes/enhancements/pull/1598) on GitHub\.
+ The pod identity webhook has been updated to address the [missing startup probes](https://github.com/aws/amazon-eks-pod-identity-webhook/issues/84) GitHub issue\. The webhook also now supports an annotation to control token expiration\. For more information, see the [GitHub pull request](https://github.com/aws/amazon-eks-pod-identity-webhook/pull/97)\.
+ CoreDNS version `1.8.0` is the recommended version for Amazon EKS `1.19` clusters\. This version is installed by default in new Amazon EKS `1.19` clusters\. For more information, see [Managing the CoreDNS add\-on](managing-coredns.md)\.
+ Amazon EKS optimized Amazon Linux 2 AMIs include the Linux kernel version `5.4` for Kubernetes version `1.19`\. For more information, see [Amazon EKS optimized Amazon Linux AMI](eks-linux-ami-versions.md#eks-al2-ami-versions)\.
+ The `CertificateSigningRequest API` has been promoted to stable `certificates.k8s.io/v1` with the following changes:
  + `spec.signerName` is now required\. You can't create requests for `kubernetes.io/legacy-unknown` with the `certificates.k8s.io/v1` API\.
  + You can continue to create CSRs with the `kubernetes.io/legacy-unknown` signer name with the `certificates.k8s.io/v1beta1` API\.
  + You can continue to request that a CSR to is signed for a non\-node server cert, webhooks \(for example, with the `certificates.k8s.io/v1beta1` API\)\. These CSRs aren't auto\-approved\.
  + To approve certificates, a privileged user requires `kubectl` `1.18.8` or later\. 

  For more information about the certificate `v1` API, see [Certificate Signing Requests](https://kubernetes.io/docs/reference/access-authn-authz/certificate-signing-requests/) in the Kubernetes documentation\.

The following Amazon EKS Kubernetes resources are critical for the Kubernetes control plane to work\. We recommend that you don't delete or edit them\.


| Permission | Kind | Namespace | Reason | 
| --- | --- | --- | --- | 
| eks:certificate\-controller | Rolebinding | kube\-system | Impacts signer and approver functionality in the control plane\. | 
| eks:certificate\-controller | Role | kube\-system | Impacts signer and approver functionality in the control plane\. | 
| eks:certificate\-controller | ClusterRolebinding | All | Impacts kubelet's ability to request server certificates, which affects certain cluster functionality like kubectl exec and kubectl logs\. | 

The following Kubernetes features are now supported in Kubernetes `1.19` Amazon EKS clusters:
+ The `ExtendedResourceToleration` admission controller is enabled\. This admission controller automatically adds tolerations for taints to pods requesting extended resources, such as GPUs\. This way, you don't have to manually add the tolerations\. For more information, see [ExtendedResourceToleration](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#extendedresourcetoleration) in the Kubernetes documentation\.
+ Elastic Load Balancers \(CLB and NLB\) provisioned by the in\-tree Kubernetes service controller support filtering the nodes included as instance targets\. This can help prevent reaching target group limits in large clusters\. For more information, see the related [GitHub issue](https://github.com/kubernetes/kubernetes/pull/90943) and the `service.beta.kubernetes.io/aws-load-balancer-target-node-labels` annotation under [Other ELB annotations](https://kubernetes.io/docs/concepts/services-networking/service/#other-elb-annotations) in the Kubernetes documentation\.
+ Pod Topology Spread has reached stable status\. You can use topology spread constraints to control how pods are spread across your cluster among failure\-domains such as regions, zones, nodes, and other user\-defined topology domains\. This can help to achieve high availability, as well as efficient resource utilization\. For more information, see [Pod Topology Spread Constraints](https://kubernetes.io/docs/concepts/workloads/pods/pod-topology-spread-constraints/) in the Kubernetes documentation\.
+ The Ingress API has reached general availability\. For more information, see [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) in the Kubernetes documentation\.
+ EndpointSlices are enabled by default\. EndpointSlices are a new API that provides a more scalable and extensible alternative to the Endpoints API for tracking IP addresses, ports, readiness, and topology information for Pods backing a Service\. For more information, see [Scaling Kubernetes Networking With EndpointSlices](https://kubernetes.io/blog/2020/09/02/scaling-kubernetes-networking-with-endpointslices/) in the Kubernetes blog\.
+ Secret and ConfigMap volumes can now be marked as immutable\. This significantly reduces load on the API server if there are many Secret and ConfigMap volumes in the cluster\. For more information, see [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/) and [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) in the Kubernetes documentation\.

For the complete Kubernetes `1.19` changelog, see [https://github\.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG\-1\.19\.md](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.19.md)\.

## Kubernetes`1.18`<a name="kubernetes-1.18"></a>

For more information about Kubernetes `1.18`, see the [official release announcement](https://kubernetes.io/blog/2020/03/25/kubernetes-1-18-release-announcement/)\.

The following Kubernetes features are now supported in Kubernetes `1.18` Amazon EKS clusters:
+ Topology Manager has reached beta status\. This feature allows the CPU and Device Manager to coordinate resource allocation decisions, optimizing for low latency with machine learning and analytics workloads\. For more information, see [Control Topology Management Policies on a node](https://kubernetes.io/docs/tasks/administer-cluster/topology-manager/) in the Kubernetes documentation\.
+ Server\-side Apply is updated with a new beta version\. This feature tracks and manages changes to fields of all new Kubernetes objects\. This helps you to know what changed your resources and when\. For more information, see [What is Server\-side Apply?](https://kubernetes.io/blog/2020/04/01/kubernetes-1.18-feature-server-side-apply-beta-2/#what-is-server-side-apply) in the Kubernetes documentation\.
+  A new `pathType` field and a new `IngressClass` resource has been added to the Ingress specification\. These features make it simpler to customize Ingress configuration, and are supported by the [AWS Load Balancer Controller](alb-ingress.md) \(formerly called the ALB Ingress Controller\)\. For more information, see [Improvements to the Ingress API in Kubernetes`1.18` in the Kubernetes documentation\.](https://kubernetes.io/blog/2020/04/02/improvements-to-the-ingress-api-in-kubernetes-1.18/)
+ Configurable horizontal pod autoscaling behavior\. For more information, see [Support for configurable scaling behavior](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#support-for-configurable-scaling-behavior) in the Kubernetes documentation\.
+ In `1.18` clusters, you no longer need to include the `AWS_DEFAULT_REGION=region-code` environment variable to pods when using IAM roles for service accounts in China Regions, whether you use the mutating web hook or configure the environment variables manually\. You still need to include the variable for all pods in earlier versions\.
+ New clusters contain updated default values in `externalTrafficPolicy`\. `HealthyThresholdCount` and `UnhealthyThresholdCount` are 2 each, and `HealthCheckIntervalSeconds` is reduced to 10 seconds\. Clusters created in older versions and upgraded retain the old values\.

For the complete Kubernetes `1.18` changelog, see [https://github\.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG\-1\.18\.md](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.18.md)\.

## Kubernetes`1.17`<a name="kubernetes-1.17"></a>

For more information about Kubernetes `1.17`, see the [official release announcement](https://kubernetes.io/blog/2019/12/09/kubernetes-1-17-release-announcement/)\.

**Important**  
The `CSIMigrationAWS` feature flag isn't enabled on EKS\. It will be enabled in a future release\. Detailed migration instructions will also be provided at that time\. For more information about CSI migration, see the [Kubernetes blog](https://kubernetes.io/blog/2019/12/09/kubernetes-1-17-feature-csi-migration-beta/)\.

The following Kubernetes features are now supported in Kubernetes `1.17` Amazon EKS clusters:
+ [Cloud Provider Labels](https://kubernetes.io/docs/reference/kubernetes-api/labels-annotations-taints) have reached general availability\. If you're using the beta labels in your pod specs for features such as node affinity, or in any custom controllers, then we recommend that you start migrating them to the new GA labels\. For information about the new labels, see the following Kubernetes documentation:
  + [ node\.kubernetes\.io/instance\-type](https://kubernetes.io/docs/reference/labels-annotations-taints/#nodekubernetesioinstance-type)
  + [topology\.kubernetes\.io/region](https://kubernetes.io/docs/reference/labels-annotations-taints/#topologykubernetesioregion)
  + [topology\.kubernetes\.io/zone](https://kubernetes.io/docs/reference/labels-annotations-taints/#topologykubernetesiozone)
+  The [ResourceQuotaScopeSelectors](https://kubernetes.io/docs/concepts/policy/resource-quotas/#quota-scopes) feature has graduated to generally available\. You can use this feature to limit the number of resources a quota supports to only those that pertain to the scope\. 
+ The [TaintNodesByCondition](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/#taint-nodes-by-condition) feature has graduated to generally available\. This feature allows you to taint nodes that have conditions such as high disk or memory pressure\.
+ The [CSI Topology](https://kubernetes-csi.github.io/docs/topology.html) feature has graduated to generally available, and is fully supported by the [EBS CSI driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver#features-1)\. You can use topology to restrict the Availability Zone where a volume is provisioned\.
+ [Finalizer protection](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/#garbage-collecting-load-balancers) for services of type `LoadBalancer` has graduated to generally available\. This feature ensures that a service resource isn't fully deleted until the correlating load balancer is also deleted\.
+ Custom resources now support [default values\.](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#defaulting) You specify values in an [OpenAPI `v3` validation schema](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#validation)\.
+  The [Windows containers RunAsUsername](https://kubernetes.io/docs/tasks/configure-pod-container/configure-runasusername/) feature is now in beta\. You can use it to run Windows applications in a container as a different user name than the default\. 

For the complete Kubernetes `1.17` changelog, see [https://github\.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG\-1\.17\.md](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.17.md)\. 

## Amazon EKS Kubernetes release calendar<a name="kubernetes-release-calendar"></a>

**Note**  
Dates with only a month and a year are approximate and are updated with an exact date when it's known\.


| Kubernetes version | Upstream release | Amazon EKS release | Amazon EKS end of support | 
| --- | --- | --- | --- | 
| 1\.17 | December 9, 2019 | July 10, 2020 | November 2, 2021 | 
| 1\.18 | March 23, 2020 | October 13, 2020 | March 31, 2022 | 
| 1\.19 | August 26, 2020 | February 16, 2021 | August 1, 2022 | 
| 1\.20 | December 8, 2020 | May 18, 2021 | October 3, 2022 | 
| 1\.21 | April 8, 2021 | July 19, 2021 | February 2023 | 
| 1\.22 | August 4, 2021 | April 4, 2022 | May 2023 | 
| 1\.23 | December 7, 2021 | August 2022 | October 2023 | 

## Amazon EKS version support and FAQ<a name="version-deprecation"></a>

In line with the Kubernetes community support for Kubernetes versions, Amazon EKS is committed to supporting at least four production\-ready versions of Kubernetes at any given time\. We will announce the end of support date of a given Kubernetes minor version at least 60 days before the end of support date\. Because of the Amazon EKS qualification and release process for new Kubernetes versions, the end of support date of a Kubernetes version on Amazon EKS will be on or after the date that the Kubernetes project stops supporting the version upstream\.

### Frequently asked questions<a name="deprecation-faq"></a>

**Q: How long is a Kubernetes version supported by Amazon EKS?**  
A: A Kubernetes version is supported for 14 months after first being available on Amazon EKS\. This is true even if upstream Kubernetes no longer support a version that's available on Amazon EKS\. We backport security patches that are applicable to the Kubernetes versions that are supported on Amazon EKS\.

**Q: Am I notified when support is ending for a Kubernetes version on Amazon EKS?**  
A: Yes, if any clusters in your account are running the version nearing the end of support, Amazon EKS sends out a notice through the AWS Health Dashboard approximately 12 months after the Kubernetes version was released on Amazon EKS\. The notice includes the end of support date\. This is at least 60 days from the date of the notice\.

**Q: What happens on the end of support date?**  
A: On the end of support date, you can no longer create new Amazon EKS clusters with the unsupported version\. Existing control planes are automatically updated by Amazon EKS to the earliest supported version through a gradual deployment process after the end of support date\. After the automatic control plane update, make sure to manually update cluster add\-ons and Amazon EC2 nodes\. For more information, see [Update the Kubernetes version for your Amazon EKS cluster ](update-cluster.md#update-existing-cluster)\.

**Q: When exactly is my control plane automatically updated after the end of support date?**  
A: Amazon EKS can't provide specific timeframes\. Automatic updates can happen at any time after the end of support date\. We recommend that you proactively update your control plane without relying on the Amazon EKS automatic update process\. For more information, see [Updating an Amazon EKS cluster Kubernetes version](update-cluster.md)\.

**Q: Can I leave my control plane on a Kubernetes version indefinitely?**  
A: No, cloud security at AWS is the highest priority\. Past a certain point \(usually one year\), the Kubernetes community stops releasing CVE patches and discourages CVE submission for deprecated versions\. This means that vulnerabilities specific to an older version of Kubernetes might not even be reported\. This leaves clusters exposed with no notice and no remediation options in the event of a vulnerability\. Given this, Amazon EKS doesn't allow control planes to stay on a version that reached end of support\.

**Q: Which Kubernetes features are supported by Amazon EKS?**  
A: Amazon EKS supports all general availability features of the Kubernetes API\. It also supports all beta features, which are enabled by default\. Alpha features aren't supported\.

**Q: Are Amazon EKS managed node groups automatically updated along with the cluster control plane version?**  
A: No, a managed node group creates Amazon EC2 instances in your account\. These instances aren't automatically upgraded when you or Amazon EKS update your control plane\. Assume that Amazon EKS automatically updates your control plane\. The Kubernetes version that's on your managed node group might be more than one version earlier than your control plane\. Then, assume that a managed node group contains instances that are running a version of Kubernetes that's more than one version earlier than the control plane\. The node group has a health issue in the **Node Groups** section of the **Compute** tab of your cluster in the console\. Last, if a node group has an available version update, **Update now** appears next to the node group in the console\. For more information, see [Updating a managed node group](update-managed-node-group.md)\. We recommend maintaining the same Kubernetes version on your control plane and nodes\.

**Q: Are self\-managed node groups automatically updated along with the cluster control plane version?**  
A: No, a self\-managed node group includes Amazon EC2 instances in your account\. These instances aren't automatically upgraded when you or Amazon EKS update the control plane version on your behalf\. A self\-managed node group doesn't have any indication in the console that it needs updating\. You can view the `kubelet` version installed on a node by selecting the node in the **Nodes** list on the **Overview** tab of your cluster to determine which nodes need updating\. You must manually update the nodes\. For more information, see [Self\-managed node updates](update-workers.md)\.

The Kubernetes project tests compatibility between the control plane and nodes for up to two minor versions\. For example, `1.20` nodes continue to operate when orchestrated by a `1.22` control plane\. However, running a cluster with nodes that are persistently two minor versions behind the control plane isn't recommended\. For more information, see [Kubernetes version and version skew support policy](https://kubernetes.io/docs/setup/version-skew-policy/) in the Kubernetes documentation\. We recommend maintaining the same Kubernetes version on your control plane and nodes\.

**Q: Are pods running on Fargate automatically upgraded with an automatic cluster control plane version upgrade?**  
Yes, Fargate pods run on infrastructure in AWS owned accounts on the Amazon EKS side of the [shared responsibility model](security.md)\. Amazon EKS uses the Kubernetes eviction API to attempt to gracefully drain pods that are running on Fargate\. For more information, see [The Eviction API](https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/#eviction-api) in the Kubernetes documentation\. If a pod can’t be evicted, Amazon EKS issues a Kubernetes `delete pod` command\. We strongly recommend running Fargate pods as part of a replication controller such as a Kubernetes deployment\. This is so a pod is automatically rescheduled after deletion\. For more information, see [Deployments]((https://kubernetes.io/docs/concepts/workloads/controllers/deployment) in the Kubernetes documentation\. The new version of the Fargate pod is deployed with a `kubelet` version that's the same version as your updated cluster control plane version\.

**Important**  
If you update the control plane, you still need to update the Fargate nodes yourself\. To update Fargate nodes, delete the Fargate pod represented by the node and redeploy the pod\. The new pod is deployed with a `kubelet` version that's the same version as your cluster\.