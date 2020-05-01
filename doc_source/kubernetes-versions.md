# Amazon EKS Kubernetes versions<a name="kubernetes-versions"></a>

The Kubernetes project is rapidly evolving with new features, design updates, and bug fixes\. The community releases new Kubernetes minor versions, such as 1\.16, as generally available approximately every three months, and each minor version is supported for approximately nine months after it is first released\. 

## Available Amazon EKS Kubernetes versions<a name="available-versions"></a>

The following Kubernetes versions are currently available for new clusters in Amazon EKS:
+ 1\.16\.8
+ 1\.15\.11
+ 1\.14\.9
+ 1\.13\.12
+ 1\.12\.10

**Important**  
Kubernetes version 1\.13 is now deprecated on Amazon EKS\. On **June 30th, 2020**, Kubernetes version 1\.13 will no longer be supported on Amazon EKS\. On or after this date, you will no longer be able to create new 1\.13 clusters, and all existing Amazon EKS clusters running Kubernetes version 1\.13 will eventually be automatically updated to version 1\.14\. We recommend that you update any 1\.13 clusters to version 1\.14 or later in order to avoid service interruption\. For more information, see [Amazon EKS version deprecation](#version-deprecation)\.  
Kubernetes version 1\.12 is now deprecated on Amazon EKS\. On **May 11th, 2020**, Kubernetes version 1\.12 will no longer be supported on Amazon EKS\. On or after this date, you will no longer be able to create new 1\.12 clusters, and all existing Amazon EKS clusters running Kubernetes version 1\.12 will eventually be automatically updated to version 1\.13\. We recommend that you update any 1\.12 clusters to version 1\.13 or later in order to avoid service interruption\. For more information, see [Amazon EKS version deprecation](#version-deprecation)\.  
Kubernetes API versions available through Amazon EKS are officially supported by AWS, until we remove the ability to create clusters using that version\. This is true even if upstream Kubernetes is no longer supporting a version available on Amazon EKS\. We backport security fixes that are applicable to the Kubernetes versions supported on Amazon EKS\. Existing clusters are always supported, and Amazon EKS will automatically update your cluster to a supported version if you have not done so manually by the version end of life date\.

Unless your application requires a specific version of Kubernetes, we recommend that you choose the latest available Kubernetes version supported by Amazon EKS for your clusters\. As new Kubernetes versions become available in Amazon EKS, we recommend that you proactively update your clusters to use the latest available version\. For more information, see [Updating an Amazon EKS cluster Kubernetes version](update-cluster.md)\.

## Kubernetes 1\.16<a name="kubernetes-1.16"></a>

Kubernetes 1\.16 is now available in Amazon EKS\. For more information about Kubernetes 1\.16, see the [official release announcement](https://kubernetes.io/blog/2019/09/18/kubernetes-1-16-release-announcement/)\.

**Important**  
Kubernetes 1\.16 removes a number of deprecated APIs\. Changes to your applications may be required before upgrading your cluster to 1\.16\. Carefully follow the 1\.16 [upgrade prerequisites](update-cluster.md#1-16-prequisites) before upgrading\.
Starting with 1\.16, the Amazon EKS certificate authority will honor certificate signing requests with SAN X\.509 extensions, which resolves the [EKS CA should honor SAN x509 extension](https://github.com/aws/containers-roadmap/issues/750) feature request from GitHub\.

The following Kubernetes features are now supported in Kubernetes 1\.16 Amazon EKS clusters:
+ Volume expansion in the CSI specification has moved to beta, which allows for any CSI spec volume plugin to be resizeable\. For more information, see [Volume Expansion](https://kubernetes-csi.github.io/docs/volume-expansion.html) in the Kubernetes CSI documentation\. The latest version of the [EBS CSI driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/tree/master/examples/kubernetes/resizing) supports volume expansion when running on an Amazon EKS 1\.16 cluster\.
+ Windows GMSA support has graduated from alpha to beta, and is now supported by Amazon EKS\. For more information, see [Configure GMSA for Windows Pods and containers](https://kubernetes.io/docs/tasks/configure-pod-container/configure-gmsa/) in the Kubernetes documentation\.
+  A new annotation: `service.beta.kubernetes.io/aws-load-balancer-eip-allocations` is available on service type `LoadBalancer` to assign an elastic IP address to Network Load Balancers\. For more information, see the [Support EIP Allocations with AWS NLB](https://github.com/kubernetes/kubernetes/issues/63959) GitHub issue\. 
+ Finalizer protection for service load balancers is now in beta and enabled by default\. Service load balancer finalizer protection ensures that any load balancer resources allocated for a Kubernetes Service object, such as the [AWS Network Load Balancer](https://docs.aws.amazon.com/eks/latest/userguide/load-balancing.html), will be destroyed or released when the service is deleted\. For more information, see [Garbage Collecting Load Balancers](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/#garbage-collecting-load-balancers) in the Kubernetes documentation\.
+ The Kubernetes custom resource definitions and admission webhooks extensibility mechanisms have both reached general availability\. For more information, see [Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) and [Dynamic Admission Control](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/) in the Kubernetes documentation\.
+ The server\-side apply feature has reached beta status and is enabled by default\. For more information, see [Server Side Apply](https://kubernetes.io/docs/reference/using-api/api-concepts/#server-side-apply) in the Kubernetes documentation\.
+ The `CustomResourceDefaulting` feature is promoted to beta and enabled by default\. Defaults may be specified in structural schemas through the `apiextensions.k8s.io/v1` API\. For more information, see [Specifying a structural schema](https://kubernetes.io/docs/tasks/access-kubernetes-api/custom-resources/custom-resource-definitions/#specifying-a-structural-schema) in the Kubernetes documentation\.

For the complete Kubernetes 1\.16 changelog, see [https://github\.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG\-1\.16\.md](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.16.md)\. 

## Kubernetes 1\.15<a name="kubernetes-1.15"></a>

Kubernetes 1\.15 is now available in Amazon EKS\. For more information about Kubernetes 1\.15, see the [official release announcement](https://kubernetes.io/blog/2019/06/19/kubernetes-1-15-release-announcement/)\.

**Important**  
Starting with 1\.15, Amazon EKS no longer tags the VPC containing your cluster\.   
Subnets within the VPC of your cluster are still tagged\. 
VPC tags will not be modified on existing cluster upgrades to 1\.15\.
For more information about VPC tagging, see [VPC tagging requirement](network_reqs.md#vpc-tagging)\. 

**Important**  
Amazon EKS has set the re\-invocation policy for the Pod Identity Webhook to `IfNeeded`\. This allows the webhook to be re\-invoked if objects are changed by other mutating admission webhooks like the App Mesh sidecar injector\. For more information about the App Mesh sidecar injector, see [Install the sidecar injector](https://docs.aws.amazon.com/eks/latest/userguide/mesh-k8s-integration.html#install-injector)\.

The following features are now supported in Kubernetes 1\.15 Amazon EKS clusters:
+ EKS now supports configuring transport layer security \(TLS\) termination, access logs, and source ranges for network load balancers\. For more information, see [Network Load Balancer support on AWS](https://kubernetes.io/docs/concepts/services-networking/service/#aws-nlb-support) on GitHub\.
+ Improved flexibility of Custom Resource Definitions \(CRD\), including the ability to convert between versions on the fly\. For more information, see [Extend the Kubernetes API with CustomResourceDefinitions](https://kubernetes.io/docs/tasks/access-kubernetes-api/custom-resources/custom-resource-definitions) on GitHub\. 
+ NodeLocal DNSCache is in beta for Kubernetes version 1\.15 clusters\. This feature can help improve cluster DNS performance by running a DNS caching agent on cluster nodes as a DaemonSet\. For more information, see [ Using NodeLocal DNSCache in Kubernetes clusters](https://kubernetes.io/docs/tasks/administer-cluster/nodelocaldns/) on GitHub\.

For the complete Kubernetes 1\.15 changelog, see [https://github\.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG\-1\.15\.md](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.15.md)\. 

## Kubernetes 1\.14<a name="kubernetes-1.14"></a>

Kubernetes 1\.14 is now available in Amazon EKS\. For more information about Kubernetes 1\.14, see the [official release announcement](https://kubernetes.io/blog/2019/03/25/kubernetes-1-14-release-announcement/)\.

**Important**  
The `--allow-privileged` flag has been removed from `kubelet` on Amazon EKS 1\.14 worker nodes\. If you have modified or restricted the [Amazon EKS default pod security policy](pod-security-policy.md#default-psp) on your cluster, you should verify that your applications have the permissions they need on 1\.14 worker nodes\.

The following features are now supported in Kubernetes 1\.14 Amazon EKS clusters:
+ Container Storage Interface Topology is in beta for Kubernetes version 1\.14 clusters\. For more information, see [CSI Topology Feature](https://kubernetes-csi.github.io/docs/topology.html#csi-topology-feature) in the Kubernetes CSI Developer Documentation\. The following CSI drivers provide a CSI interface for container orchestrators like Kubernetes to manage the life cycle of Amazon EBS volumes, Amazon EFS file systems, and Amazon FSx for Lustre file systems:
  + [Amazon Elastic Block Store \(EBS\) CSI driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver)
  + [Amazon EFS CSI driver](https://github.com/kubernetes-sigs/aws-efs-csi-driver)
  + [Amazon FSx for Lustre CSI driver](https://github.com/kubernetes-sigs/aws-fsx-csi-driver)
+ Process ID \(PID\) limiting is in beta for Kubernetes version 1\.14 clusters\. This feature allows you to set quotas for how many processes a pods can create, which can prevent resource starvation for other applications on a cluster\. For more information, see [Process ID limiting for stability improvements in Kubernetes 1\.14](https://kubernetes.io/blog/2019/04/15/process-id-limiting-for-stability-improvements-in-kubernetes-1.14/)\.
+ Persistent Local Volumes are now GA and make locally attached storage available as a persistent volume source\. For more information, see [Kubernetes 1\.14: Local persistent volumes GA](https://kubernetes.io/blog/2019/04/04/kubernetes-1.14-local-persistent-volumes-ga/)\.
+ Pod Priority and Preemption is now GA and allows pods to be assigned a scheduling priority level\. For more information, see [Pod Priority and Preemption](https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/) in the Kubernetes documentation\.
+ Windows worker node support is GA with Kubernetes 1\.14\.

For the complete Kubernetes 1\.14 changelog, see [https://github\.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG\-1\.14\.md](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.14.md)\. 

## Kubernetes 1\.13<a name="kubernetes-1.13"></a>

The following features are now supported in Kubernetes 1\.13 Amazon EKS clusters:
+ The `PodSecurityPolicy` admission controller is now enabled\. This admission controller allows fine\-grained control over pod creation and updates\. For more information, see [Pod security policy](pod-security-policy.md)\. If you do not have any pod security policies defined in your cluster when you upgrade to 1\.13, then Amazon EKS creates a default policy for you\.
**Important**  
If you have **any** pod security policies defined in your cluster, the default policy is not created when you upgrade to Kubernetes 1\.13\. If your cluster does not have the default Amazon EKS pod security policy, your pods may not be able to launch if your existing pod security policies are too restrictive\. You can check for any existing pod security policies with the following command:  

  ```
  kubectl get psp
  ```
If you cluster has any pod security policies defined, you should also make sure that you have the default Amazon EKS pod security policy \(`eks.privileged`\) defined\. If not, you can apply it by following the steps in [To install or restore the default pod security policy](pod-security-policy.md#install-default-psp)\.
+ Amazon ECR interface VPC endpoints \(AWS PrivateLink\) are supported\. When you enable these endpoints in your VPC, all network traffic between your VPC and Amazon ECR is restricted to the Amazon network\. For more information, see [Amazon ECR interface VPC endpoints \(AWS PrivateLink\)](https://docs.aws.amazon.com/AmazonECR/latest/userguide/vpc-endpoints.html) in the *Amazon Elastic Container Registry User Guide*\.
+ The `DryRun` feature is in beta in Kubernetes 1\.13 and is enabled by default for Amazon EKS clusters\. For more information, see [Dry run](https://kubernetes.io/docs/reference/using-api/api-concepts/#dry-run) in the Kubernetes documentation\.
+ The `TaintBasedEvictions` feature is in beta in Kubernetes 1\.13 and is enabled by default for Amazon EKS clusters\. For more information, see [Taint based evictions](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#taint-based-evictions) in the Kubernetes documentation\. 
+ Raw Block Volume Support is in beta in Kubernetes 1\.13 and is enabled by default for Amazon EKS clusters\. This is accessible via the `volumeDevices` container field in pod specs, and the `volumeMode` field in persistent volume and persistent volume claim definitions\. For more information, see [Raw Block Volume Support](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#raw-block-volume-support) in the Kubernetes documentation\. 
+ Node lease renewal is treated as the heartbeat signal from the node, in addition to its `NodeStatus` update\. This reduces load on the control plane for large clusters\. For more information, see [https://github\.com/kubernetes/kubernetes/pull/69241](https://github.com/kubernetes/kubernetes/pull/69241)\.

For the complete Kubernetes 1\.13 changelog, see [https://github\.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG\-1\.13\.md](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.13.md)\.

## Amazon EKS version deprecation<a name="version-deprecation"></a>

In line with the Kubernetes community support for Kubernetes versions, Amazon EKS is committed to running at least three production\-ready versions of Kubernetes at any given time, with a fourth version in deprecation\. 

We will announce the deprecation of a given Kubernetes minor version at least 60 days before the end of support date\. Because of the Amazon EKS qualification and release process for new Kubernetes versions, the deprecation of a Kubernetes version on Amazon EKS will be on or after the date the Kubernetes project stops supporting the version upstream\.

On the end of support date, Amazon EKS clusters running the deprecated version will begin to be automatically updated to the next Amazon EKS\-supported version of Kubernetes\. For example, if the deprecated version is 1\.13, clusters will eventually be automatically updated to version 1\.14\. If a cluster is automatically updated by Amazon EKS, you must update the version of your worker nodes after the update is complete\. For more information, see [Worker node updates](update-workers.md)\.

Kubernetes supports compatibility between masters and workers for at least two minor versions, so 1\.13 workers will continue to operate when orchestrated by a 1\.14 control plane\. For more information, see [Kubernetes version and version skew support policy](https://kubernetes.io/docs/setup/version-skew-policy/) in the Kubernetes documentation\.