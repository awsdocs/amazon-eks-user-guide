# Amazon EKS Kubernetes versions<a name="kubernetes-versions"></a>

The Kubernetes project is continually integrating new features, design updates, and bug fixes\. The community releases new Kubernetes minor versions, such as `1.25`\. New version updates are available on average every three months\. Each minor version is supported for approximately twelve months after it's first released\. 

## Available Amazon EKS Kubernetes versions<a name="available-versions"></a>

The following Kubernetes versions are currently available for new Amazon EKS clusters:
+ `1.25`
+ `1.24`
+ `1.23`
+ `1.22`

If your application doesn't require a specific version of Kubernetes, we recommend that you use the latest available Kubernetes version that's supported by Amazon EKS for your clusters\. As new Kubernetes versions become available in Amazon EKS, we recommend that you proactively update your clusters to use the latest available version\. For instructions on how to update your cluster, see [Updating an Amazon EKS cluster Kubernetes version](update-cluster.md)\. For more information about Kubernetes releases, see [Amazon EKS Kubernetes release calendar](#kubernetes-release-calendar) and [Amazon EKS version support and FAQ](#version-deprecation)\.

**Note**  
For `1.24` and later clusters, officially published Amazon EKS AMIs include `containerd` as the only runtime\. Kubernetes versions earlier than `1.24` use Docker as the default runtime\. These versions have a bootstrap flag option that you can use to test out your workloads on any supported cluster with `containerd`\. For more information, see [Amazon EKS ended support for `Dockershim`](dockershim-deprecation.md)\.

## Kubernetes 1\.25<a name="kubernetes-1.25"></a>

Kubernetes `1.25` is now available in Amazon EKS\. For more information about Kubernetes `1.25`, see the [official release announcement](https://kubernetes.io/blog/2022/08/23/kubernetes-v1-25-release/)\.

**Important**  
`PodSecurityPolicy` \(PSP\) is removed in Kubernetes `1.25`\. PSPs are replaced with [Pod Security Admission \(PSA\)](https://kubernetes.io/docs/concepts/security/pod-security-admission/) and Pod Security Standards \(PSS\)\. PSA is a built\-in admission controller that implements the security controls outlined in the [PSS ](https://kubernetes.io/docs/concepts/security/pod-security-standards/)\. PSA and PSS are graduated to stable in Kubernetes `1.25` and are enabled in Amazon EKS by default\. If you have PSPs in your cluster, make sure to migrate from PSP to the built\-in Kubernetes PSS or to a policy\-as\-code solution before upgrading your cluster to version `1.25`\. If you don't migrate from PSP, you might encounter interruptions to your workloads\. For more information, see the [Pod security policy \(PSP\) removal FAQ](pod-security-policy-removal-faq.md)\.   
Amazon EKS `1.25` includes enhancements to cluster authentication that contain updated YAML libraries\. If a YAML value in the `aws-auth` `ConfigMap` found in the `kube-system` namespace starts with a macro, where the first character is a curly brace, you should add quotation marks \(`“ ”`\) before and after the curly braces \(`{ }`\)\. This is required to ensure that `aws-iam-authenticator` version `v0.6.3` accurately parses the `aws-auth` `ConfigMap` in Amazon EKS `1.25`\.  
The beta API version \(`discovery.k8s.io/v1beta1`\) of `EndpointSlice` was deprecated in Kubernetes `1.21` and is no longer served as of Kubernetes `1.25`\. This API has been updated to `discovery.k8s.io/v1`\. For more information, see [https://kubernetes.io/docs/reference/using-api/deprecation-guide/#endpointslice-v125](https://kubernetes.io/docs/reference/using-api/deprecation-guide/#endpointslice-v125) in the Kubernetes documentation\.  
The AWS Load Balancer Controller `v2.4.6` and earlier used the `v1beta1` endpoint to communicate with `EndpointSlices`\. If you're using the `EndpointSlices` configuration for the AWS Load Balancer Controller, you must upgrade to AWS Load Balancer Controller `v2.4.7` before upgrading your Amazon EKS cluster to `1.25`\. If you upgrade to `1.25` while using the `EndpointSlices` configuration for AWS Load Balancer Controller, the controller will crash and result in interruptions to your workloads\.
+ `SeccompDefault` is promoted to beta in Kubernetes `1.25`\. By setting the `--seccomp-default` flag when you configure `kubelet`, the container runtime uses its `RuntimeDefault``seccomp` profile, rather than the unconfined \(`seccomp disabled`\) mode\. The default profiles provide a strong set of security defaults, while preserving the functionality of the workload\. Although this flag is available, Amazon EKS doesn't enable this flag by default, so Amazon EKS behavior is effectively unchanged\. If you want to, you can start enabling this on your nodes\. For more details, see the tutorial [Restrict a Container's Syscalls with seccomp](https://kubernetes.io/docs/tutorials/security/seccomp/#enable-the-use-of-runtimedefault-as-the-default-seccomp-profile-for-all-workloads/) in the Kubernetes documentation\.
+ Support for the Container Runtime Interface \(CRI\) for Docker \(also known as `Dockershim`\) was removed from Kubernetes `1.24` and later\. The only container runtime in Amazon EKS official AMIs for Kubernetes `1.24` and later clusters is `containerd`\. Before upgrading to Amazon EKS `1.24` or later, remove any reference to bootstrap script flags that aren't supported anymore\. For more information, see [Amazon EKS ended support for `Dockershim`](dockershim-deprecation.md)\.
+ The support for wildcard queries was deprecated in CoreDNS `1.8.7` and removed in CoreDNS `1.9`\. This was done as a security measure\. Wildcard queries no longer work and return `NXDOMAIN` instead of an IP address\.

For the complete Kubernetes `1.25` changelog, see [https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.25.md#changelog-since-v1240](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.25.md#changelog-since-v1240)\.

## Kubernetes 1\.24<a name="kubernetes-1.24"></a>

Kubernetes `1.24` is now available in Amazon EKS\. For more information about Kubernetes `1.24`, see the [official release announcement](https://kubernetes.io/blog/2022/05/03/kubernetes-1-24-release-announcement/)\.

**Important**  
Starting with Kubernetes `1.24`, new beta APIs aren't enabled in clusters by default\. By default, existing beta APIs and new versions of existing beta APIs continue to be enabled\. Amazon EKS follows the same behavior as upstream Kubernetes `1.24`\. The feature gates that control new features for both new and existing API operations are enabled by default\. This is in alignment with upstream Kubernetes\. For more information, see [KEP\-3136: Beta APIs Are Off by Default](https://github.com/kubernetes/enhancements/blob/master/keps/sig-architecture/3136-beta-apis-off-by-default/README.md) on GitHub\.  
Support for Container Runtime Interface \(CRI\) for Docker \(also known as Dockershim\) is removed from Kubernetes `1.24`\. Amazon EKS official AMIs have containerd as the only runtime\. Before moving to Amazon EKS `1.24` or higher, you must remove any reference to bootstrap script flags that aren't supported anymore\. For more information, see [Amazon EKS ended support for `Dockershim`](dockershim-deprecation.md)\.  
With the container runtime change from Docker to `containerd`, the format of container logs in `/var/log/containers/*.log` has changed to the CRI format\. The standard Docker parser no longer works, so the CRI parser needs to be added to your `ConfigMap`\.  

```
[PARSER]
        Name        cri
        Format      regex
        Regex       ^(?<time>[^ ]+) (?<stream>stdout|stderr) (?<logtag>[^ ]*) (?<log>.*)$
        Time_Key    time
        Time_Format %Y-%m-%dT%H:%M:%S.%L%z
```
In Kubernetes `1.23` and earlier, `kubelet` serving certificates with unverifiable IP and DNS Subject Alternative Names \(SANs\) are automatically issued with unverifiable SANs\. These unverifiable SANs are omitted from the provisioned certificate\. In version `1.24` and later clusters, `kubelet` serving certificates aren't issued if any SAN can't be verified\. This prevents `kubectl` exec and `kubectl` logs commands from working\. For more information, see [Certificate signing considerations before upgrading your cluster to Kubernetes 1\.24](cert-signing.md#csr-considerations)\.
+ You can use Topology Aware Hints to indicate your preference for keeping traffic in zone when cluster worker nodes are deployed across multiple availability zones\. Routing traffic within a zone can help reduce costs and improve network performance\. By default, Topology Aware Hints are enabled in Amazon EKS `1.24`\. For more information, see [Topology Aware Hints](https://kubernetes.io/docs/concepts/services-networking/topology-aware-hints/) in the Kubernetes documentation\.
+ The `PodSecurityPolicy` \(PSP\) is scheduled for removal in Kubernetes `1.25`\. PSPs are being replaced with [Pod Security Admission \(PSA\)](https://kubernetes.io/docs/concepts/security/pod-security-admission/)\. PSA is a built\-in admission controller that uses the security controls that are outlined in the [Pod Security Standards \(PSS\) ](https://kubernetes.io/docs/concepts/security/pod-security-standards/)\. PSA and PSS are both beta features and are enabled in Amazon EKS by default\. To address the removal of PSP in version `1.25`, we recommend that you implement PSS in Amazon EKS\. For more information, see [Implementing Pod Security Standards in Amazon EKS](http://aws.amazon.com/blogs/containers/implementing-pod-security-standards-in-amazon-eks/) on the AWS blog\.
+ The `client.authentication.k8s.io/v1alpha1` ExecCredential is removed in Kubernetes `1.24`\. The ExecCredential API was generally available in Kubernetes `1.22`\. If you use a client\-go credential plugin that relies on the `v1alpha1` API, contact the distributor of your plugin on how to migrate to the `v1` API\.
+ For Kubernetes `1.24`, we contributed a feature to the upstream Cluster Autoscaler project that simplifies scaling Amazon EKS managed node groups to and from zero nodes\. Previously, for the Cluster Autoscaler to understand the resources, labels, and taints of a managed node group that was scaled to zero nodes, you needed to tag the underlying Amazon EC2 Auto Scaling group with the details of the nodes that it was responsible for\. Now, when there are no running nodes in the managed node group, the Cluster Autoscaler calls the Amazon EKS `DescribeNodegroup` API operation\. This API operation provides the information that the Cluster Autoscaler requires of the managed node group's resources, labels, and taints\. This feature requires that you add the `eks:DescribeNodegroup` permission to the Cluster Autoscaler service account IAM policy\. When the value of a Cluster Autoscaler tag on the Auto Scaling group powering an Amazon EKS managed node group conflicts with the node group itself, the Cluster Autoscaler prefers the value of the Auto Scaling group tag\. This is so that you can override values as needed\. For more information, see [Autoscaling](autoscaling.md)\.
+ If you intend to use Inferentia or Trainium instance types with Amazon EKS `1.24`, you must upgrade to the AWS Neuron device plugin version 1\.9\.3\.0 or later\. For more information, see [Neuron K8 release \[1\.9\.3\.0\]](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/release-notes/containers/neuron-k8.html#id46) in the AWS Neuron Documentation\.
+ `Containerd` has `IPv6` enabled for pods, by default\. It applies node kernel settings to pod network namespaces\. Because of this, containers in a pod bind to both `IPv4` \(`127.0.0.1`\) and `IPv6` \(`::1`\) loopback addresses\. `IPv6` is the default protocol for communication\. Before updating your cluster to version `1.24`, we recommend that you test your multi\-container pods\. Modify apps so that they can bind to all IP addresses on loopback interfaces\. The majority of libraries enable `IPv6` binding, which is backward compatible with `IPv4`\. When it’s not possible to modify your application code, you have two options:
  + Run an `init` container and set `disable ipv6` to `true` \(`sysctl -w net.ipv6.conf.all.disable ipv6=1`\)\.
  + Configure a [mutating admission webhook](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#mutatingadmissionwebhook) to inject an `init` container alongside your application pods\.

  If you need to block `IPv6` for all pods across all nodes, you might have to disable `IPv6` on your instances\.

For the complete Kubernetes `1.24` changelog, see [https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.24.md#changelog-since-v1230](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.24.md#changelog-since-v1230)\.

## Kubernetes 1\.23<a name="kubernetes-1.23"></a>

Kubernetes `1.23` is now available in Amazon EKS\. For more information about Kubernetes `1.23`, see the [official release announcement](https://kubernetes.io/blog/2021/12/07/kubernetes-1-23-release-announcement/)\.

**Important**  
The Kubernetes in\-tree to container storage interface \(CSI\) volume migration feature is enabled\. This feature enables the replacement of existing Kubernetes in\-tree storage plugins for Amazon EBS with a corresponding Amazon EBS CSI driver\. For more information, see [Kubernetes 1\.17 Feature: Kubernetes In\-Tree to CSI Volume Migration Moves to Beta](https://kubernetes.io/blog/2019/12/09/kubernetes-1-17-feature-csi-migration-beta/) on the Kubernetes blog\.  
The feature translates in\-tree APIs to equivalent CSI APIs and delegates operations to a replacement CSI driver\. With this feature, if you use existing `StorageClass`, `PersistentVolume`, and `PersistentVolumeClaim` objects that belong to these workloads, there likely won't be any noticeable change\. The feature enables Kubernetes to delegate all storage management operations from the in\-tree plugin to the CSI driver\. If you use Amazon EBS volumes in an existing cluster, install the Amazon EBS CSI driver in your cluster before you update your cluster to version `1.23`\. If you don't install the driver before updating an existing cluster, interruptions to your workloads might occur\. If you plan to deploy workloads that use Amazon EBS volumes in a new `1.23` cluster, install the Amazon EBS CSI driver in your cluster before deploying the workloads your cluster\. For instructions on how to install the Amazon EBS CSI driver on your cluster, see [Amazon EBS CSI driver](ebs-csi.md)\. For frequently asked questions about the migration feature, see [Amazon EBS CSI migration frequently asked questions](ebs-csi-migration-faq.md)\.  
Amazon EKS Fargate pod launches might break for pod specs with maximum container resource limits exceeding the sum of requested resources\. For guaranteed scheduling, the maximum of resource limits should always be less than the sum of the requested resources\.
+ Kubernetes stopped supporting `dockershim` in version `1.20` and removed `dockershim` in version `1.24`\. For more information, see [Kubernetes is Moving on From Dockershim: Commitments and Next Steps](https://kubernetes.io/blog/2022/01/07/kubernetes-is-moving-on-from-dockershim/) in the Kubernetes blog\. Amazon EKS will end support for `dockershim` starting in Amazon EKS version `1.24`\. Starting with Amazon EKS version `1.24`, Amazon EKS official AMIs will have `containerd` as the only runtime\.

  Even though Amazon EKS version `1.23` continues to support `dockershim`, we recommend that you start testing your applications now to identify and remove any Docker dependencies\. This way, you are prepared to update your cluster to version `1.24`\. For more information about `dockershim` removal, see [Amazon EKS ended support for `Dockershim`](dockershim-deprecation.md)\.
+ Kubernetes graduated `IPv4`/`IPv6` dual\-stack networking for pods, services, and nodes to general availability\. However, Amazon EKS and the Amazon VPC CNI plugin for Kubernetes don't support dual\-stack networking\. Your clusters can assign `IPv4` or `IPv6` addresses to pods and services, but can't assign both address types\.
+ Kubernetes graduated the Pod Security Admission \(PSA\) feature to beta\. The feature is enabled by default\. For more information, see [Pod Security Admission](https://kubernetes.io/docs/concepts/security/pod-security-admission/) in the Kubernetes documentation\. PSA replaces the [Pod Security Policy](https://aws.github.io/aws-eks-best-practices/security/docs/pods/#pod-security-solutions) \(PSP\) admission controller\. The PSP admission controller isn't supported and is scheduled for removal in Kubernetes version `1.25`\.

  The PSP admission controller enforces pod security standards on pods in a namespace based on specific namespace labels that set the enforcement level\. For more information, see [Pod Security Standards \(PSS\) and Pod Security Admission \(PSA\)](https://aws.github.io/aws-eks-best-practices/security/docs/pods/#pod-security-standards-pss-and-pod-security-admission-psa) in the Amazon EKS best practices guide\.
+ The `kube-proxy` image deployed with clusters is now the [minimal base image](https://gallery.ecr.aws/eks-distro-build-tooling/eks-distro-minimal-base-iptables) maintained by Amazon EKS Distro \(EKS\-D\)\. The image contains minimal packages and doesn't have shells or package managers\.
+ Kubernetes graduated ephemeral containers to beta\. Ephemeral containers are temporary containers that run in the same namespace as an existing pod\. You can use them to observe the state of pods and containers for troubleshooting and debugging purposes\. This is especially useful for interactive troubleshooting when `kubectl exec` is insufficient because either a container has crashed or a container image doesn't include debugging utilities\. An example of a container that includes a debugging utility is [distroless images](https://github.com/GoogleContainerTools/distroless#distroless-container-images)\. For more information, see [Debugging with an ephemeral debug container](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/#ephemeral-container) in the Kubernetes documentation\.
+ Kubernetes graduated the `HorizontalPodAutoscaler` `autoscaling/v2` stable API to general availability\. The `HorizontalPodAutoscaler` `autoscaling/v2beta2` API is deprecated\. It will be unavailable in `1.26`\.

For the complete Kubernetes `1.23` changelog, see [https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.23.md#changelog-since-v1220](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.23.md#changelog-since-v1220)\.

## Kubernetes 1\.22<a name="kubernetes-1.22"></a>

Kubernetes `1.22` is now available in Amazon EKS\. For more information about Kubernetes `1.22`, see the [official release announcement](https://kubernetes.io/blog/2021/08/04/kubernetes-1-22-release-announcement/)\.

**Important**  
[https://github.com/kubernetes/enhancements/issues/542](https://github.com/kubernetes/enhancements/issues/542) graduated to stable and enabled by default in Kubernetes version `1.22`\. This feature improves security of service account tokens\. It allows workloads that are running on Kubernetes to request JSON web tokens that are audience, time, and key bound\. Service account tokens now have an expiration of one hour\. In previous Kubernetes versions, they didn't have an expiration\. This means that clients that rely on these tokens must refresh the tokens within an hour\. The following [Kubernetes client SDKs](https://kubernetes.io/docs/reference/using-api/client-libraries/) refresh tokens automatically within the required timeframe:  
Go version `0.15.7` and later
Python version `12.0.0` and later
Java version `9.0.0` and later
JavaScript version `0.10.3` and later
Ruby `master` branch
Haskell version `0.3.0.0`
C\# version `7.0.5` and later
If your workload is using an older client version, then you must update it\. To enable a smooth migration of clients to the newer time\-bound service account tokens, Kubernetes version `1.22` adds an extended expiry period to the service account token over the default one hour\. For Amazon EKS clusters, the extended expiry period is 90 days\. Your Amazon EKS cluster's Kubernetes API server rejects requests with tokens older than 90 days\. We recommend that you check your applications and their dependencies\. Make sure that the Kubernetes client SDKs are the same or later than the versions listed previously\. For instructions about how to identify pods that are using stale tokens, see [Kubernetes service accounts](service-accounts.md#identify-pods-using-stale-tokens)\.
+ Kubernetes `1.22` removes a number of APIs that are no longer available\. You might need to make changes to your application before you upgrade to Amazon EKS version `1.22`\. Follow the [Kubernetes version `1.22` prerequisites](update-cluster.md#update-1.22) carefully before updating your cluster\.
+ The Ingress API versions `extensions/v1beta1` and `networking.k8s.io/v1beta1` have been removed in Kubernetes `1.22`\. If you're using the [https://github.com/kubernetes-sigs/aws-load-balancer-controller](https://github.com/kubernetes-sigs/aws-load-balancer-controller), you must upgrade to at least [version `2.4.1`](https://github.com/kubernetes-sigs/aws-load-balancer-controller/releases/tag/v2.4.1) before you upgrade your Amazon EKS clusters to version `1.22`\. Additionally, you must modify [Ingress manifests](https://kubernetes.io/docs/reference/kubernetes-api/service-resources/ingress-v1/) to use `apiVersion` `networking.k8s.io/v1`\. This has been available since [Kubernetes version `1.19`](https://kubernetes.io/blog/2020/08/26/kubernetes-release-1.19-accentuate-the-paw-sitive/#ingress-graduates-to-general-availability))\. For more information about changes between Ingress `v1beta1` and `v1`, see the [Kubernetes documentation](https://kubernetes.io/docs/reference/using-api/deprecation-guide/#ingress-v122)\. The AWS Load Balancer Controller [controller sample manifest](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.4/guide/ingress/spec/) uses the `v1` spec\.
+ The Amazon EKS legacy [Windows support controllers](windows-support.md#legacy-windows-support) use the `admissionregistration.k8s.io/v1beta1` API that was removed in Kubernetes `1.22`\. If you're running Windows workloads, you must remove legacy [Windows support](windows-support.md#remove-windows-support-data-plane) and enable [Windows support](windows-support.md#enable-windows-support) before upgrading to Amazon EKS version `1.22`\.
+ The [CertificateSigningRequest \(CSR\)](https://kubernetes.io/docs/reference/kubernetes-api/authentication-resources/certificate-signing-request-v1) API version `certificates.k8s.io/v1beta1` was removed in Kubernetes version `1.22`\. You must migrate manifests and API clients to use the `certificates.k8s.io/v1` CSR API\. This API has been available since version `1.19`\. For instructions on how to use CSR in Amazon EKS, see [Certificate signing](cert-signing.md)\.
+ The `CustomResourceDefinition` API version `apiextensions.k8s.io/v1beta1` was removed in Kubernetes `1.22`\. Make sure that all custom resource definitions in your cluster are updated to `v1`\. API version `v1` custom resource definitions are required to have Open API `v3` schema validation defined\. For more information, see the [Kubernetes documentation](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)\.
+ If you're using App Mesh, you must upgrade to at least App Mesh controller `[v1\.4\.3](https://github.com/aws/aws-app-mesh-controller-for-k8s/releases/tag/v1.4.3)` or later before you upgrade to Amazon EKS version `1.22`\. Older versions of the App Mesh controller use `v1beta1` `CustomResourceDefinition` API version and aren't compatible with Kubernetes version `1.22` and later\.
+  Amazon EKS version `1.22` enables the `EndpointSliceTerminatingCondition` feature by default, which includes pods in terminating state within `EndpointSlices`\. If you set `enableEndpointSlices` to `True` \(disabled by default\) in the AWS Load Balancer Controller, you must upgrade to at least AWS Load Balancer Controller version `2.4.1+` before upgrading to Amazon EKS version `1.22`\. 
+  Starting with Amazon EKS version `1.22`, `kube-proxy` is configured by default to expose Prometheus metrics outside the pod\. This behavior change addresses the request made in containers roadmap issue [ \#657 ](https://github.com/aws/containers-roadmap/issues/657)\. 
+  The initial launch of Amazon EKS version `1.22` uses `etcd` version `3.4` as a backend, and is not affected by the [possibility of data corruption](https://groups.google.com/a/kubernetes.io/g/dev/c/B7gJs88XtQc/m/rSgNOzV2BwAJ?pli=1) present in `etcd` version `3.5`\. 
+ Starting with Amazon EKS `1.22`, Amazon EKS is decoupling AWS cloud specific control logic from core control plane code to the [out\-of\-tree](https://github.com/kubernetes/cloud-provider-aws) AWS Kubernetes [Cloud Controller Manager](https://kubernetes.io/docs/concepts/architecture/cloud-controller/)\. This is in line with the upstream Kubernetes recommendation\. By decoupling the interoperability logic between Kubernetes and the underlying cloud infrastructure, the `cloud-controller-manager` component enables cloud providers to release features at a different pace compared to the main Kubernetes project\. This change is transparent and requires no action\. However, a new log stream named `cloud-controller-manager` now appears under the `ControllerManager` log type when enabled\. For more information, see [Amazon EKS control plane logging](control-plane-logs.md)\.
+ Starting with Amazon EKS `1.22`, Amazon EKS is changing the default AWS Security Token Service endpoint used by IAM roles for service accounts \(IRSA\) to be the regional endpoint instead of the global endpoint to reduce latency and improve reliability\. You can optionally configure IRSA to use the global endpoint in [Configuring the AWS Security Token Service endpoint for a service account](configure-sts-endpoint.md)\.

The following Kubernetes features are now supported in Kubernetes `1.22` Amazon EKS clusters:
+ **[Server\-side Apply graduates to GA](https://kubernetes.io/docs/reference/using-api/server-side-apply/)** \- Server\-side Apply helps users and controllers manage their resources through declarative configurations\. It allows them to create or modify objects declaratively by sending their fully specified intent\. After being in beta for a couple releases, Server\-side Apply is now generally available\.
+ [Warning mechanism for use of unsupported APIs](https://github.com/kubernetes/enhancements/issues/1693) \- Use of unsupported APIs produces warnings visible to API consumers, and metrics visible to cluster administrators\.

 For the complete Kubernetes `1.22` changelog, see [https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.22.md#changelog-since-v1210](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.22.md#changelog-since-v1210)\.

## Kubernetes 1\.21<a name="kubernetes-1.21"></a>

Kubernetes `1.21` is now available in Amazon EKS\. For more information about Kubernetes `1.21`, see the [official release announcement](https://kubernetes.io/blog/2021/04/08/kubernetes-1-21-release-announcement/)\.

**Important**  
[https://github.com/kubernetes/enhancements/issues/542](https://github.com/kubernetes/enhancements/issues/542) graduated to beta and is enabled by default in Kubernetes version `1.21`\. This feature improves security of service account tokens by allowing workloads running on Kubernetes to request JSON web tokens that are audience, time, and key bound\. Service account tokens now have an expiration of one hour\. In previous Kubernetes versions, they didn't have an expiration\. This means that clients that rely on these tokens must refresh the tokens within an hour\. The following [Kubernetes client SDKs](https://kubernetes.io/docs/reference/using-api/client-libraries/) refresh tokens automatically within the required time frame:  
Go version `0.15.7` and later
Python version `12.0.0` and later
Java version `9.0.0` and later
JavaScript version `0.10.3` and later
Ruby `master` branch
Haskell version `0.3.0.0`
C\# version `7.0.5` and later
If your workload is using an older client version, then you must update it\. To enable a smooth migration of clients to the newer time\-bound service account tokens, Kubernetes version `1.21` adds an extended expiry period to the service account token over the default one hour\. For Amazon EKS clusters, the extended expiry period is 90 days\. Your Amazon EKS cluster's Kubernetes API server rejects requests with tokens older than 90 days\. We recommend that you check your applications and their dependencies\. Make sure that the Kubernetes client SDKs are the same or later than the versions listed previously\. For instructions about how to identify pods that are using stale tokens, see [Kubernetes service accounts](service-accounts.md#identify-pods-using-stale-tokens)\.
+ [Dual\-stack networking](https://kubernetes.io/docs/concepts/services-networking/dual-stack/) support \(`IPv4` and `IPv6` addresses\) on pods, services, and nodes reached beta status\. However, Amazon EKS and the Amazon VPC CNI plugin for Kubernetes don't currently support dual stack networking\.
+ The Amazon EKS Optimized Amazon Linux 2 AMI now contains a bootstrap flag to enable the `containerd` runtime as a Docker alternative\. This flag allows preparation for the [removal of Docker as a supported runtime](https://kubernetes.io/blog/2020/12/02/dockershim-faq/) in the next Kubernetes release\. For more information, see [Enable the `containerd` runtime bootstrap flag](eks-optimized-ami.md#containerd-bootstrap)\. This can be tracked through the [ container roadmap on Github](https://github.com/aws/containers-roadmap/issues/313)\.
+ Managed node groups support for Cluster Autoscaler priority expander\. 

  Newly created managed node groups on Amazon EKS version `1.21` clusters use the following format for the underlying Auto Scaling group name: 

  `eks-managed-node-group-name-uuid`

  This enables using the [priority expander](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/expander/priority/readme.md) feature of Cluster Autoscaler to scale node groups based on user defined priorities\. A common use case is to prefer scaling spot node groups over on\-demand groups\. This behavior change solves the [containers roadmap issue \#1304](https://github.com/aws/containers-roadmap/issues/1304)\.

The following Kubernetes features are now supported in Amazon EKS `1.21` clusters:
+ [CronJobs](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/) \(previously ScheduledJobs\) have now graduated to stable status\. With this change, users perform regularly scheduled actions such as backups and report generation\.
+ [Immutable Secrets and ConfigMaps](https://kubernetes.io/docs/concepts/configuration/secret/#secret-immutable) have now graduated to stable status\. A new, immutable field was added to these objects to reject changes\. This rejection protects the cluster from updates that can unintentionally break the applications\. Because these resources are immutable, `kubelet` doesn't watch or poll for changes\. This reduces `kube-apiserver` load and improving scalability and performance\.
+ [Graceful Node Shutdown](https://kubernetes.io/blog/2021/04/21/graceful-node-shutdown-beta/) has now graduated to beta status\. With this update, the `kubelet` is aware of node shutdown and can gracefully terminate that node's pods\. Before this update, when a node shutdown, its pods didn't follow the expected termination lifecycle\. This caused workload problems\. Now, the `kubelet` can detect imminent system shutdown through `systemd`, and inform running pods so they terminate gracefully\.
+ Pods with multiple containers can now use the `kubectl.kubernetes.io/default-container` annotation to have a container preselected for `kubectl` commands\.
+ `PodSecurityPolicy` is being phased out\. `PodSecurityPolicy` will still be functional for several more releases according to Kubernetes deprecation guidelines\. For more information, see [PodSecurityPolicy Deprecation: Past, Present, and Future](https://kubernetes.io/blog/2021/04/06/podsecuritypolicy-deprecation-past-present-and-future) and the [AWS blog](http://aws.amazon.com/blogs/containers/using-gatekeeper-as-a-drop-in-pod-security-policy-replacement-in-amazon-eks/)\.

 

For the complete Kubernetes `1.21` changelog, see [https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.21.md](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.21.md)\.

## Kubernetes 1\.20<a name="kubernetes-1.20"></a>

For more information about Kubernetes `1.20`, see the [official release announcement](https://kubernetes.io/blog/2020/12/08/kubernetes-1-20-release-announcement/)\.
+ `1.20` brings new Amazon EKS created default roles and users\. You can find more information in [Default Amazon EKS created Kubernetes roles and users](default-roles-users.md)\. Ensure that you are using a [supported cert\-manager version](https://cert-manager.io/docs/installation/supported-releases/)\.

The following Kubernetes features are now supported in Kubernetes `1.20` Amazon EKS clusters:
+ [API Priority and Fairness](https://kubernetes.io/docs/concepts/cluster-administration/flow-control/) has reached beta status and is enabled by default\. This allows `kube-apiserver` to categorize incoming requests by priority levels\.
+ [RuntimeClass](https://kubernetes.io/docs/concepts/containers/runtime-class/) has reached stable status\. The `RuntimeClass` resource provides a mechanism for supporting multiple runtimes in a cluster and surfaces information about that container runtime to the control plane\.
+ [Process ID Limits](https://kubernetes.io/docs/concepts/policy/pid-limiting/) has now graduated to general availability\.
+ [kubectl debug](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/) has reached beta status\. `kubectl debug` supports common debugging workflows directly from `kubectl`\.
+ The Docker container runtime has been phased out\. The Kubernetes community has written a [blog post](https://blog.k8s.io/2020/12/02/dont-panic-kubernetes-and-docker/) about this in detail with a dedicated [FAQ page](https://blog.k8s.io/2020/12/02/dockershim-faq/)\. Docker\-produced images can continue to be used and will work as they always have\. You can safely ignore the `dockershim` deprecation warning message printed in `kubelet` startup logs\. Amazon EKS will eventually move to `containerd` as the runtime for the Amazon EKS optimized Amazon Linux 2 AMI\. You can follow the containers roadmap [issue](https://github.com/aws/containers-roadmap/issues/313#issuecomment-831617671) for more details\.
+ Pod Hostname as FQDN has graduated to beta status\. This feature allows setting a pod's hostname to its Fully Qualified Domain Name \(FQDN\)\. This way, you can set the hostname field of the kernel to the FQDN of a pod\.
+ The client\-go credential plugins can now be passed in the current cluster information via the `KUBERNETES_EXEC_INFO` environment variable\. This enhancement allows Go clients to authenticate using external credential providers, such as a key management system \(KMS\)\.

For the complete Kubernetes `1.20` changelog, see [https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.20.md](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.20.md)\.

## Kubernetes 1\.19<a name="kubernetes-1.19"></a>

For more information about Kubernetes `1.19`, see the [official release announcement](https://kubernetes.io/blog/2020/08/26/kubernetes-release-1.19-accentuate-the-paw-sitive/)\.
+ Starting with `1.19`, Amazon EKS no longer adds the `kubernetes.io/cluster/my-cluster` tag to subnets passed in when clusters are created\. This subnet tag is only required if you want to influence where the Kubernetes service controller or AWS Load Balancer Controller places Elastic Load Balancers\. For more information about the requirements of subnets passed to Amazon EKS during cluster creation, see updates to [Amazon EKS VPC and subnet requirements and considerations](network_reqs.md)\.
  + Subnet tags aren't modified on existing clusters updated to `1.19`\.
  + The AWS Load Balancer Controller version `2.1.1` and earlier required the *`my-cluster`* subnet tag\. In version `2.1.2` and later, you can specify the tag to refine subnet discovery, but it's not required\. For more information about the AWS Load Balancer Controller, see [Installing the AWS Load Balancer Controller add\-on](aws-load-balancer-controller.md)\. For more information about subnet tagging when using a load balancer, see [Application load balancing on Amazon EKS](alb-ingress.md) and [Network load balancing on Amazon EKS](network-load-balancing.md)\.
+ You're no longer required to provide a security context for non\-root containers that must access the web identity token file for use with IAM roles for service accounts\. For more information, see [IAM roles for service accounts](iam-roles-for-service-accounts.md) and[proposal for file permission handling in projected service account volume](https://github.com/kubernetes/enhancements/pull/1598) on GitHub\.
+ The pod identity webhook has been updated to address the [missing startup probes](https://github.com/aws/amazon-eks-pod-identity-webhook/issues/84) GitHub issue\. The webhook also now supports an annotation to control token expiration\. For more information, see the [GitHub pull request](https://github.com/aws/amazon-eks-pod-identity-webhook/pull/97)\.
+ CoreDNS version `1.8.0` is the recommended version for Amazon EKS `1.19` clusters\. This version is installed by default in new Amazon EKS `1.19` clusters\. For more information, see [Updating the CoreDNS self\-managed add\-on](managing-coredns.md)\.
+ Amazon EKS optimized Amazon Linux 2 AMIs include the Linux kernel version `5.4` for Kubernetes version `1.19`\. For more information, see [Changelog](https://github.com/awslabs/amazon-eks-ami/blob/master/CHANGELOG.md) on GitHub\.
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
+ Pod Topology Spread has reached stable status\. You can use topology spread constraints to control how pods are spread across your cluster among failure\-domains such as AWS Regions, zones, nodes, and other user\-defined topology domains\. This can help to achieve high availability, as well as efficient resource utilization\. For more information, see [Pod Topology Spread Constraints](https://kubernetes.io/docs/concepts/workloads/pods/pod-topology-spread-constraints/) in the Kubernetes documentation\.
+ The Ingress API has reached general availability\. For more information, see [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) in the Kubernetes documentation\.
+ `EndpointSlices` are enabled by default\. `EndpointSlices` is a new API that provides a more scalable and extensible alternative to the Endpoints API for tracking IP addresses, ports, readiness, and topology information for Pods backing a Service\. For more information, see [Scaling Kubernetes Networking With EndpointSlices](https://kubernetes.io/blog/2020/09/02/scaling-kubernetes-networking-with-endpointslices/) in the Kubernetes blog\.
+ Secret and ConfigMap volumes can now be marked as immutable\. This significantly reduces load on the API server if there are many Secret and ConfigMap volumes in the cluster\. For more information, see [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/) and [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) in the Kubernetes documentation\.

For the complete Kubernetes `1.19` changelog, see [https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.19.md](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.19.md)\.

## Amazon EKS Kubernetes release calendar<a name="kubernetes-release-calendar"></a>

**Note**  
Dates with only a month and a year are approximate and are updated with an exact date when it's known\.


| Kubernetes version | Upstream release | Amazon EKS release | Amazon EKS end of support | 
| --- | --- | --- | --- | 
| 1\.25 | August 23, 2022 | February 22, 2023 | May 2024 | 
| 1\.24 | May 3, 2022 | November 15, 2022 | January 2024 | 
| 1\.23 | December 7, 2021 | August 11, 2022 | October 2023 | 
| 1\.22 | August 4, 2021 | April 4, 2022 | June 4, 2023 | 
| 1\.21 | April 8, 2021 | July 19, 2021 | February 15, 2023 | 
| 1\.20 | December 8, 2020 | May 18, 2021 | November 1, 2022 | 
| 1\.19 | August 26, 2020 | February 16, 2021 | August 1, 2022 | 

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
A: Amazon EKS can't provide specific time frames\. Automatic updates can happen at any time after the end of support date\. You won't receive any notification before the update\. We recommend that you proactively update your control plane without relying on the Amazon EKS automatic update process\. For more information, see [Updating an Amazon EKS cluster Kubernetes version](update-cluster.md)\.

**Q: Can I leave my control plane on a Kubernetes version indefinitely?**  
A: No, cloud security at AWS is the highest priority\. Past a certain point \(usually one year\), the Kubernetes community stops releasing common vulnerabilities and exposures \(CVE\) patches and discourages CVE submission for unsupported versions\. This means that vulnerabilities specific to an older version of Kubernetes might not even be reported\. This leaves clusters exposed with no notice and no remediation options in the event of a vulnerability\. Given this, Amazon EKS doesn't allow control planes to stay on a version that reached end of support\.

**Q: Which Kubernetes features are supported by Amazon EKS?**  
A: Amazon EKS supports all general availability features of the Kubernetes API\. It also supports all beta features, which are enabled by default\. Alpha features aren't supported\.

**Q: Are Amazon EKS managed node groups automatically updated along with the cluster control plane version?**  
A: No, a managed node group creates Amazon EC2 instances in your account\. These instances aren't automatically upgraded when you or Amazon EKS update your control plane\. Assume that Amazon EKS automatically updates your control plane\. The Kubernetes version that's on your managed node group might be more than one version earlier than your control plane\. Then, assume that a managed node group contains instances that are running a version of Kubernetes that's more than one version earlier than the control plane\. The node group has a health issue in the **Node groups** section of the **Compute** tab of your cluster in the console\. Last, if a node group has an available version update, **Update now** appears next to the node group in the console\. For more information, see [Updating a managed node group](update-managed-node-group.md)\. We recommend maintaining the same Kubernetes version on your control plane and nodes\.

**Q: Are self\-managed node groups automatically updated along with the cluster control plane version?**  
A: No, a self\-managed node group includes Amazon EC2 instances in your account\. These instances aren't automatically upgraded when you or Amazon EKS update the control plane version on your behalf\. A self\-managed node group doesn't have any indication in the console that it needs updating\. You can view the `kubelet` version installed on a node by selecting the node in the **Nodes** list on the **Overview** tab of your cluster to determine which nodes need updating\. You must manually update the nodes\. For more information, see [Self\-managed node updates](update-workers.md)\.

The Kubernetes project tests compatibility between the control plane and nodes for up to two minor versions\. For example, `1.23` nodes continue to operate when orchestrated by a `1.25` control plane\. However, running a cluster with nodes that are persistently two minor versions behind the control plane isn't recommended\. For more information, see [Kubernetes version and version skew support policy](https://kubernetes.io/docs/setup/version-skew-policy/) in the Kubernetes documentation\. We recommend maintaining the same Kubernetes version on your control plane and nodes\.

**Q: Are pods running on Fargate automatically upgraded with an automatic cluster control plane version upgrade?**  
Yes, Fargate pods run on infrastructure in AWS owned accounts on the Amazon EKS side of the [shared responsibility model](security.md)\. Amazon EKS uses the Kubernetes eviction API to attempt to gracefully drain pods that are running on Fargate\. For more information, see [The Eviction API](https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/#eviction-api) in the Kubernetes documentation\. If a pod can't be evicted, Amazon EKS issues a Kubernetes `delete pod` command\. We strongly recommend running Fargate pods as part of a replication controller such as a Kubernetes deployment\. This is so that a pod is automatically rescheduled after deletion\. For more information, see [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment) in the Kubernetes documentation\. The new version of the Fargate pod is deployed with a `kubelet` version that's the same version as your updated cluster control plane version\.

**Important**  
If you update the control plane, you must still update the Fargate nodes yourself\. To update Fargate nodes, delete the Fargate pod represented by the node and redeploy the pod\. The new pod is deployed with a `kubelet` version that's the same version as your cluster\.