# Amazon EKS Kubernetes versions<a name="kubernetes-versions"></a>

The Kubernetes project is rapidly evolving with new features, design updates, and bug fixes\. The community releases new Kubernetes minor versions, such as 1\.18, as generally available approximately every three months, and each minor version is supported for approximately twelve months after it is first released\. 

## Available Amazon EKS Kubernetes versions<a name="available-versions"></a>

The following Kubernetes versions are currently available for new clusters in Amazon EKS:
+ 1\.18\.9
+ 1\.17\.12
+ 1\.16\.15
+ 1\.15\.12

Unless your application requires a specific version of Kubernetes, we recommend that you choose the latest available Kubernetes version supported by Amazon EKS for your clusters\. As new Kubernetes versions become available in Amazon EKS, we recommend that you proactively update your clusters to use the latest available version\. For more information, see [Updating a Cluster](update-cluster.md)\. For more information, see [Amazon EKS Kubernetes release calendar](#kubernetes-release-calendar) and [Amazon EKS version support and FAQ](#version-deprecation)\.

## Kubernetes 1\.18<a name="kubernetes-1.18"></a>

Kubernetes 1\.18 is now available in Amazon EKS\. For more information about Kubernetes 1\.18, see the [official release announcement](https://kubernetes.io/blog/2020/03/25/kubernetes-1-18-release-announcement/)\.

The following Kubernetes features are now supported in Kubernetes 1\.18 Amazon EKS clusters:
+ Topology Manager has reached beta status\. This feature allows the CPU and Device Manager to coordinate resource allocation decisions, optimizing for low latency with machine learning and analytics workloads\. For more information, see [Control Topology Management Policies on a node](https://kubernetes.io/docs/tasks/administer-cluster/topology-manager/) in the Kubernetes documentation\.
+ Server\-side Apply is updated with a new beta version\. This feature tracks and manages changes to fields of all new Kubernetes objects, allowing you to know what changed your resources and when\. For more information, see [What is Server\-side Apply?](https://kubernetes.io/blog/2020/04/01/kubernetes-1.18-feature-server-side-apply-beta-2/#what-is-server-side-apply) in the Kubernetes documentation\.
+  A new `pathType` field and a new `IngressClass` resource has been added to the Ingress specification\. These features make it simpler to customize Ingress configuration, and are supported by the [AWS Load Balancer Controller](alb-ingress.md) \(formerly called the ALB Ingress Controller\)\. For more information, see [Improvements to the Ingress API in Kubernetes 1\.18 in the Kubernetes documentation\.](https://kubernetes.io/blog/2020/04/02/improvements-to-the-ingress-api-in-kubernetes-1.18/)
+ Configurable horizontal pod autoscaling behavior\. For more information, see [Support for configurable scaling behavior](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#support-for-configurable-scaling-behavior) in the Kubernetes documentation\.
+ In 1\.18 clusters, you no longer need to include the `AWS_DEFAULT_REGION=<region-code>` environment variable to pods when using IAM roles for service accounts in China regions, whether you use the mutating web hook or configure the environment variables manually\. You still need to include the variable for all pods in earlier versions\.

For the complete Kubernetes 1\.18 changelog, see [https://github\.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG\-1\.18\.md](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.18.md)\.

## Kubernetes 1\.17<a name="kubernetes-1.17"></a>

Kubernetes 1\.17 is now available in Amazon EKS\. For more information about Kubernetes 1\.17, see the [official release announcement](https://kubernetes.io/blog/2019/12/09/kubernetes-1-17-release-announcement/)\.

**Important**  
EKS has not enabled the `CSIMigrationAWS` feature flag\. This will be enabled in a future release, along with detailed migration instructions\. For more info on CSI migration, see the [Kubernetes blog](https://kubernetes.io/blog/2019/12/09/kubernetes-1-17-feature-csi-migration-beta/)\.
Updating a cluster from 1\.16 to 1\.17 will fail if any of your AWS Fargate pods have a `kubelet` minor version earlier than 1\.16\. Before updating your cluster from 1\.16 to 1\.17, you need to recycle your Fargate pods so that their `kubelet` is 1\.16 before attempting to update the cluster to 1\.17\. To recycle a Kubernetes deployment on a 1\.15 or later cluster, use the following command\.  

  ```
  kubectl rollout restart deployment <deployment-name>
  ```

The following Kubernetes features are now supported in Kubernetes 1\.17 Amazon EKS clusters:
+ [Cloud Provider Labels](https://kubernetes.io/docs/reference/kubernetes-api/labels-annotations-taints) have reached general availability\. If you are using the beta labels in your pod specs for features such as node affinity, or in any custom controllers, then we recommend that you start migrating them to the new GA labels\. For information about the new labels, see the following Kubernetes documentation:
  + [ node\.kubernetes\.io/instance\-type](https://kubernetes.io/docs/reference/kubernetes-api/labels-annotations-taints/#nodekubernetesioinstance-type)
  + [topology\.kubernetes\.io/region](https://kubernetes.io/docs/reference/kubernetes-api/labels-annotations-taints/#topologykubernetesioregion)
  + [topology\.kubernetes\.io/zone](https://kubernetes.io/docs/reference/kubernetes-api/labels-annotations-taints/#topologykubernetesiozone)
+  The [ResourceQuotaScopeSelectors](https://kubernetes.io/docs/concepts/policy/resource-quotas/#quota-scopes) feature has graduated to generally available\. This feature allows you to limit the number of resources a quota supports to only those that pertain to the scope\. 
+ The [TaintNodesByCondition](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/#taint-nodes-by-condition) feature has graduated to generally available\. This feature allows you to taint nodes that have conditions such as high disk or memory pressure\.
+ The [CSI Topology](https://kubernetes-csi.github.io/docs/topology.html) feature has graduated to generally available, and is fully supported by the [EBS CSI driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver#features-1)\. You can use topology to restrict the Availability Zone where a volume is provisioned\.
+ [Finalizer protection](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/#garbage-collecting-load-balancers) for services of type `LoadBalancer` has graduated to generally available\. This feature ensures that a service resource is not fully deleted until the correlating load balancer is also deleted\.
+ Custom resources now support [default values\.](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#defaulting) You specify values in an [OpenAPI v3 validation schema](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#validation)\.
+  The [Windows containers RunAsUsername](https://kubernetes.io/docs/tasks/configure-pod-container/configure-runasusername/) feature is now in beta, allowing you to run Windows applications in a container as a different username than the default\. 

For the complete Kubernetes 1\.17 changelog, see [https://github\.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG\-1\.17\.md](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.17.md)\. 

## Kubernetes 1\.16<a name="kubernetes-1.16"></a>

Kubernetes 1\.16 is now available in Amazon EKS\. For more information about Kubernetes 1\.16, see the [official release announcement](https://kubernetes.io/blog/2019/09/18/kubernetes-1-16-release-announcement/)\.

**Important**  
Kubernetes 1\.16 removes a number of deprecated APIs\. Changes to your applications may be required before updating your cluster to 1\.16\. Carefully follow the 1\.16 [update prerequisites](update-cluster.md#1-16-prerequisites) before updating\.
Starting with 1\.16, the Amazon EKS certificate authority will honor certificate signing requests with SAN X\.509 extensions, which resolves the [EKS CA should honor SAN x509 extension](https://github.com/aws/containers-roadmap/issues/750) feature request from GitHub\.

The following Kubernetes features are now supported in Kubernetes 1\.16 Amazon EKS clusters:
+ Volume expansion in the CSI specification has moved to beta, which allows for any CSI spec volume plugin to be resizeable\. For more information, see [Volume Expansion](https://kubernetes-csi.github.io/docs/volume-expansion.html) in the Kubernetes CSI documentation\. The latest version of the [EBS CSI driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/tree/master/examples/kubernetes/resizing) supports volume expansion when running on an Amazon EKS 1\.16 cluster\.
+ Windows GMSA support has graduated from alpha to beta, and is now supported by Amazon EKS\. For more information, see [Configure GMSA for Windows Pods and containers](https://kubernetes.io/docs/tasks/configure-pod-container/configure-gmsa/) in the Kubernetes documentation\.
+  A new annotation: `service.beta.kubernetes.io/aws-load-balancer-eip-allocations` is available on service type `LoadBalancer` to assign an elastic IP address to Network Load Balancers\. For more information, see the [Support EIP Allocations with AWS NLB](https://github.com/kubernetes/kubernetes/issues/63959) GitHub issue\. 
+ Finalizer protection for service load balancers is now in beta and enabled by default\. Service load balancer finalizer protection ensures that any load balancer resources allocated for a Kubernetes Service object, such as the [AWS Network Load Balancer](https://docs.aws.amazon.com/eks/latest/userguide/load-balancing.html), will be destroyed or released when the service is deleted\. For more information, see [Garbage Collecting Load Balancers](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/#garbage-collecting-load-balancers) in the Kubernetes documentation\.
+ The Kubernetes custom resource definitions and admission webhooks extensibility mechanisms have both reached general availability\. For more information, see [Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) and [Dynamic Admission Control](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/) in the Kubernetes documentation\.
+ The server\-side apply feature has reached beta status and is enabled by default\. For more information, see [Server Side Apply](https://kubernetes.io/docs/reference/using-api/api-concepts/#server-side-apply) in the Kubernetes documentation\.
+ The `CustomResourceDefaulting` feature is promoted to beta and enabled by default\. Defaults may be specified in structural schemas through the `apiextensions.k8s.io/v1` API\. For more information, see [Specifying a structural schema](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#specifying-a-structural-schema) in the Kubernetes documentation\.

For the complete Kubernetes 1\.16 changelog, see [https://github\.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG\-1\.16\.md](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.16.md)\. 

## Kubernetes 1\.15<a name="kubernetes-1.15"></a>

Kubernetes 1\.15 is now available in Amazon EKS\. For more information about Kubernetes 1\.15, see the [official release announcement](https://kubernetes.io/blog/2019/06/19/kubernetes-1-15-release-announcement/)\.

**Important**  
Starting with 1\.15, Amazon EKS no longer tags the VPC containing your cluster\.   
Subnets within the VPC of your cluster are still tagged\. 
VPC tags are not modified on existing cluster updates to 1\.15\.
For more information about VPC tagging, see [VPC tagging requirement](network_reqs.md#vpc-tagging)\. 

**Important**  
Amazon EKS has set the re\-invocation policy for the Pod Identity Webhook to `IfNeeded`\. This allows the webhook to be re\-invoked if objects are changed by other mutating admission webhooks like the App Mesh sidecar injector\. For more information about the App Mesh sidecar injector, see [Install the sidecar injector](https://docs.aws.amazon.com/eks/latest/userguide/mesh-k8s-integration.html#install-injector)\.

The following features are now supported in Kubernetes 1\.15 Amazon EKS clusters:
+ EKS now supports configuring transport layer security \(TLS\) termination, access logs, and source ranges for network load balancers\. For more information, see [Network Load Balancer support on AWS](https://kubernetes.io/docs/concepts/services-networking/service/#aws-nlb-support) on GitHub\.
+ Improved flexibility of Custom Resource Definitions \(CRD\), including the ability to convert between versions on the fly\. For more information, see [Extend the Kubernetes API with CustomResourceDefinitions](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/) on GitHub\. 
+ NodeLocal DNSCache is in beta for Kubernetes version 1\.15 clusters\. This feature can help improve cluster DNS performance by running a DNS caching agent on cluster nodes as a DaemonSet\. For more information, see [ Using NodeLocal DNSCache in Kubernetes clusters](https://kubernetes.io/docs/tasks/administer-cluster/nodelocaldns/) on GitHub\.
**Note**  
When running CoreDNS on Amazon EC2, we recommend not using `force_tcp` in the configuration and ensuring that `options use-vc` is not set in `/etc/resolv.conf`\.

For the complete Kubernetes 1\.15 changelog, see [https://github\.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG\-1\.15\.md](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.15.md)\. 

## Amazon EKS Kubernetes release calendar<a name="kubernetes-release-calendar"></a>

**Note**  
Dates with only a month and a year are approximate and are updated with an exact date when it is known\.


| Kubernetes version | Upstream release | Amazon EKS release | Amazon EKS end of support | 
| --- | --- | --- | --- | 
| 1\.15 | June 19, 2019 | March 10, 2020 | May, 2021 | 
| 1\.16 | September 8, 2019 | April 30, 2020 | July, 2021 | 
| 1\.17 | December 9, 2019 | July 10, 2020 | September, 2021 | 
| 1\.18 | March 23, 2020 | October 13, 2020 | November, 2021 | 
| 1\.19 | August 26, 2020 | January, 2021 | February, 2022 | 

## Amazon EKS version support and FAQ<a name="version-deprecation"></a>

In line with the Kubernetes community support for Kubernetes versions, Amazon EKS is committed to supporting at least four production\-ready versions of Kubernetes at any given time\. We will announce the end of support date of a given Kubernetes minor version at least 60 days before the end of support date\. Because of the Amazon EKS qualification and release process for new Kubernetes versions, the end of support date of a Kubernetes version on Amazon EKS will be on or after the date that the Kubernetes project stops supporting the version upstream\.

### Frequently asked questions<a name="deprecation-faq"></a>

**Q: How long is a Kubernetes version supported by Amazon EKS?**  
A: A Kubernetes version is fully supported for 14 months after first being available on Amazon EKS\. This is true even if upstream Kubernetes is no longer supporting a version available on Amazon EKS\. We backport security patches that are applicable to the Kubernetes versions supported on Amazon EKS\.

**Q: When does support end for a Kubernetes version on Amazon EKS?**  
A: Approximately 12 months after a version is released on Amazon EKS \(usually with the release of a new version\) Amazon EKS will send out a notice through the AWS Personal Health Dashboard if any clusters in your account are running the version nearing end of support\. The notice will include the end of support date, which will be at least 60 days from the date of the notice\.

**Q: What happens on the end of support date?**  
A: On the end of support date, you will no longer be able to create new Amazon EKS clusters with the unsupported version\. Existing clusters are automatically updated to the oldest supported version through a gradual deployment process after the end of support date\. After the automatic control plane update, you'll still need to manually update cluster add\-ons\. For more information, see [Update an existing cluster](update-cluster.md#update-existing-cluster)\.

**Q: When exactly will my cluster be automatically updated after the end of support date?**  
A: Amazon EKS is unable to provide specific timeframes\. Automatic updates can happen at any time after the end of support date\. We recommend that you take proactive action and update your clusters without relying on the Amazon EKS automatic update process\. For more information, see [Updating a Cluster](update-cluster.md)\.

**Q: Can I leave my cluster on a Kubernetes version indefinitely?**  
A: No\. Cloud security at AWS is the highest priority\. Amazon EKS does not allow clusters to stay on a version that has reached end of support\.

**Q: Are Amazon EKS managed node groups automatically updated along with the cluster control plane version?**  
A: No\. **Update now** appears next to a node group in the console if it can be updated to a later version\. You can update the node group to the same version as the control plane's Kubernetes version\. For more information, see [Updating a managed node group](update-managed-node-group.md)\.

**Q: Are self\-managed node groups automatically updated along with the cluster control plane version?**  
A: No\. A self\-managed node group won't have any indication in the console that it needs to be updated\. You can however, view the `kubelet` version installed on a node by viewing the node in the **Nodes** list on the **Overview** tab of your cluster\. For more information, see [Self\-managed node updates](update-workers.md)\. The Kubernetes project tests compatibility between the control plane and nodes for up to two minor versions\. For example, 1\.16 nodes will continue to operate when orchestrated by a 1\.18 control plane\. However, running a cluster with nodes that are persistently two minor versions behind the control plane is not recommended\. For more information, see [Kubernetes version and version skew support policy](https://kubernetes.io/docs/setup/version-skew-policy/) in the Kubernetes documentation\. You can update a node group one version at a time up to the same version as the control plane\. We recommend maintaining the same Kubernetes version on your control plane and nodes\. 

**Q: Are Fargate nodes automatically updated along with the cluster control plane version?**  
A: No\. To update a Fargate node after updating your control plane, delete the Fargate pod represented by the node and redeploy the pod\. The new version of the pod is deployed with a `kubelet` version that is the same version as your cluster\.