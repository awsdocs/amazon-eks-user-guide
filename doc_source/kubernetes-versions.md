# Amazon EKS Kubernetes Versions<a name="kubernetes-versions"></a>

The Kubernetes project is rapidly evolving with new features, design updates, and bug fixes\. The community releases new Kubernetes minor versions, such as 1\.13, as generally available approximately every three months, and each minor version is supported for approximately one year after it is first released\. 

## Available Amazon EKS Kubernetes Versions<a name="available-versions"></a>

The following Kubernetes versions are currently available for new clusters in Amazon EKS:
+ 1\.13\.7
+ 1\.12\.6
+ 1\.11\.8
+ 1\.10\.13

**Important**  
Amazon EKS will deprecate Kubernetes version 1\.10 on July 22, 2019\. On this day, you will no longer be able to create new 1\.10 clusters, and all Amazon EKS clusters running Kubernetes version 1\.10 will be updated to the latest available platform version of Kubernetes version 1\.11\. For more information, see [Amazon EKS Version Deprecation](#version-deprecation)\.

Unless your application requires a specific version of Kubernetes, we recommend that you choose the latest available Kubernetes version supported by Amazon EKS for your clusters\. As new Kubernetes versions become available in Amazon EKS, we recommend that you proactively update your clusters to use the latest available version\. For more information, see [Updating an Amazon EKS Cluster Kubernetes Version](update-cluster.md)\.

## Kubernetes 1\.13<a name="kubernetes-1.13"></a>

The following features are now supported in Kubernetes 1\.13 Amazon EKS clusters:
+ The `PodSecurityPolicy` admission controller is now enabled\. This admission controller allows fine\-grained control over pod creation and updates\. For more information, see [Pod Security Policy](pod-security-policy.md)\.
+ Amazon ECR interface VPC endpoints \(AWS PrivateLink\) are supported\. When you enable these endpoints in your VPC, all network traffic between your VPC and Amazon ECR is restricted to the Amazon network\. For more information, see [Amazon ECR Interface VPC Endpoints \(AWS PrivateLink\)]() in the *Amazon Elastic Container Registry User Guide*\.
+ The `DryRun` feature is in beta in Kubernetes 1\.13 and is enabled by default for Amazon EKS clusters\. For more information, see [Dry run](https://kubernetes.io/docs/reference/using-api/api-concepts/#dry-run) in the Kubernetes documentation\.
+ The `TaintBasedEvictions` feature is in beta in Kubernetes 1\.13 and is enabled by default for Amazon EKS clusters\. For more information, see [Taint based Evictions](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#taint-based-evictions) in the Kubernetes documentation\. 
+ Raw block volume support is in beta in Kubernetes 1\.13 and is enabled by default for Amazon EKS clusters\. This is accessible via the `volumeDevices` container field in pod specs, and the `volumeMode` field in persistent volume and persistent volume claim definitions\. For more information, see [Raw Block Volume Support](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#raw-block-volume-support) in the Kubernetes documentation\. 
+ Node lease renewal is treated as the heartbeat signal from the node, in addition to its `NodeStatus` update\. This reduces load on the control plane for large clusters\. For more information, see [https://github\.com/kubernetes/kubernetes/pull/69241](https://github.com/kubernetes/kubernetes/pull/69241)\.

For the complete Kubernetes 1\.13 changelog, see [https://github\.com/kubernetes/kubernetes/blob/master/CHANGELOG\-1\.13\.md](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG-1.13.md)

## Amazon EKS Version Deprecation<a name="version-deprecation"></a>

In line with the Kubernetes community support for Kubernetes versions, Amazon EKS is committed to running at least three production\-ready versions of Kubernetes at any given time, with a fourth version in deprecation\. 

We will announce the deprecation of a given Kubernetes minor version at least 60 days before the deprecation date\. Because of the Amazon EKS qualification and release process for new Kubernetes versions, the deprecation of a Kubernetes version on Amazon EKS will be on or after the date the Kubernetes project stops supporting the version upstream\.

On the deprecation date, Amazon EKS clusters running the version targeted for deprecation will begin to be updated to the next Amazon EKS\-supported version of Kubernetes\. This means that if the deprecated version is 1\.10, clusters will be automatically updated to version 1\.11\. If a cluster is automatically updated by Amazon EKS, you must also update the version of your worker nodes after the update is complete\. For more information, see [Worker Node Updates](update-workers.md)\.

Kubernetes supports compatibility between masters and workers for at least 2 minor versions, so 1\.10 workers will continue to operate when orchestrated by a 1\.11 control plane\. For more information, see [Kubernetes Version and Version Skew Support Policy](https://kubernetes.io/docs/setup/version-skew-policy/) in the Kubernetes documentation\.