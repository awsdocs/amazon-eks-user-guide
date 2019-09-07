# Amazon EKS Kubernetes Versions<a name="kubernetes-versions"></a>

The Kubernetes project is rapidly evolving with new features, design updates, and bug fixes\. The community releases new Kubernetes minor versions, such as 1\.14, as generally available approximately every three months, and each minor version is supported for approximately one year after it is first released\. 

## Available Amazon EKS Kubernetes Versions<a name="available-versions"></a>

The following Kubernetes versions are currently available for new clusters in Amazon EKS:
+ 1\.14\.6
+ 1\.13\.10
+ 1\.12\.10
+ 1\.11\.10

**Important**  
Amazon EKS will deprecate Kubernetes version 1\.11 on November 4th, 2019\. On this day, you will no longer be able to create new 1\.11 clusters, and all Amazon EKS clusters running Kubernetes version 1\.11 will be updated to the latest available platform version of Kubernetes version 1\.12\. For more information, see [Amazon EKS Version Deprecation](#version-deprecation)\.  
Kubernetes version 1\.10 is no longer supported on Amazon EKS\. You can no longer create new 1\.10 clusters, and all existing Amazon EKS clusters running Kubernetes version 1\.10 will eventually be automatically updated to the latest available platform version of Kubernetes version 1\.11\. For more information, see [Amazon EKS Version Deprecation](#version-deprecation)\.  
Please update any 1\.10 clusters to version 1\.11 or higher in order to avoid service interruption\. For more information, see [Updating an Amazon EKS Cluster Kubernetes Version](update-cluster.md)\.

Unless your application requires a specific version of Kubernetes, we recommend that you choose the latest available Kubernetes version supported by Amazon EKS for your clusters\. As new Kubernetes versions become available in Amazon EKS, we recommend that you proactively update your clusters to use the latest available version\. For more information, see [Updating an Amazon EKS Cluster Kubernetes Version](update-cluster.md)\.

## Kubernetes 1\.14<a name="kubernetes-1.14"></a>

Kubernetes 1\.14 is now available in Amazon EKS\. For more information about Kubernetes 1\.14, see the [official release announcement](https://kubernetes.io/blog/2019/03/25/kubernetes-1-14-release-announcement/)\.

**Important**  
The `--allow-privileged` flag has been removed from `kubelet` on Amazon EKS 1\.14 worker nodes\. If you have modified or restricted the [Amazon EKS Default Pod Security Policy](pod-security-policy.md#default-psp) on your cluster, you should verify that your applications have the permissions they need on 1\.14 worker nodes\.

The following features are now supported in Kubernetes 1\.14 Amazon EKS clusters:
+ Container Storage Interface Topology is in beta for Kubernetes version 1\.14 clusters\. For more information, see [CSI Topology Feature](https://kubernetes-csi.github.io/docs/topology.html#csi-topology-feature) in the Kubernetes CSI Developer Documentation\. The following CSI drivers provide a CSI interface for container orchestrators like Kubernetes to manage the lifecycle of Amazon EBS volumes, Amazon EFS file systems, and Amazon FSx for Lustre file systems:
  + [Amazon Elastic Block Store \(EBS\) CSI driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver)
  + [Amazon EFS CSI Driver](https://github.com/kubernetes-sigs/aws-efs-csi-driver)
  + [Amazon FSx for Lustre CSI Driver](https://github.com/kubernetes-sigs/aws-fsx-csi-driver)
+ Process ID \(PID\) limiting is in beta for Kubernetes version 1\.14 clusters\. This feature allows you to set quotas for how many processes a pods can create, which can prevent resource starvation for other applications on a cluster\. For more information, see [Process ID Limiting for Stability Improvements in Kubernetes 1\.14](https://kubernetes.io/blog/2019/04/15/process-id-limiting-for-stability-improvements-in-kubernetes-1.14/)\.
+ Persistent Local Volumes are now GA and make locally attached storage available as a persistent volume source\. For more information, see [Kubernetes 1\.14: Local Persistent Volumes GA](https://kubernetes.io/blog/2019/04/04/kubernetes-1.14-local-persistent-volumes-ga/)\.
+ Pod Priority and Preemption is now GA and allows pods to be assigned a scheduling priority level\. For more information, see [Pod Priority and Preemption](https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/) in the Kubernetes documentation\.
+ Windows worker node support is GA with Kubernetes 1\.14\. Amazon EKS currently supports running Windows nodes and containers as part of a [public preview](https://github.com/aws/containers-roadmap/tree/master/preview-programs/eks-windows-preview)\. Official support is coming soon\.

For the complete Kubernetes 1\.14 changelog, see [https://github\.com/kubernetes/kubernetes/blob/master/CHANGELOG\-1\.14\.md](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG-1.14.md)

## Kubernetes 1\.13<a name="kubernetes-1.13"></a>

The following features are now supported in Kubernetes 1\.13 Amazon EKS clusters:
+ The `PodSecurityPolicy` admission controller is now enabled\. This admission controller allows fine\-grained control over pod creation and updates\. For more information, see [Pod Security Policy](pod-security-policy.md)\.
+ Amazon ECR interface VPC endpoints \(AWS PrivateLink\) are supported\. When you enable these endpoints in your VPC, all network traffic between your VPC and Amazon ECR is restricted to the Amazon network\. For more information, see [Amazon ECR Interface VPC Endpoints \(AWS PrivateLink\)](https://docs.aws.amazon.com/AmazonECR/latest/userguide/vpc-endpoints.html) in the *Amazon Elastic Container Registry User Guide*\.
+ The `DryRun` feature is in beta in Kubernetes 1\.13 and is enabled by default for Amazon EKS clusters\. For more information, see [Dry run](https://kubernetes.io/docs/reference/using-api/api-concepts/#dry-run) in the Kubernetes documentation\.
+ The `TaintBasedEvictions` feature is in beta in Kubernetes 1\.13 and is enabled by default for Amazon EKS clusters\. For more information, see [Taint based Evictions](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/#taint-based-evictions) in the Kubernetes documentation\. 
+ Raw block volume support is in beta in Kubernetes 1\.13 and is enabled by default for Amazon EKS clusters\. This is accessible via the `volumeDevices` container field in pod specs, and the `volumeMode` field in persistent volume and persistent volume claim definitions\. For more information, see [Raw Block Volume Support](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#raw-block-volume-support) in the Kubernetes documentation\. 
+ Node lease renewal is treated as the heartbeat signal from the node, in addition to its `NodeStatus` update\. This reduces load on the control plane for large clusters\. For more information, see [https://github\.com/kubernetes/kubernetes/pull/69241](https://github.com/kubernetes/kubernetes/pull/69241)\.

For the complete Kubernetes 1\.13 changelog, see [https://github\.com/kubernetes/kubernetes/blob/master/CHANGELOG\-1\.13\.md](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG-1.13.md)

## Amazon EKS Version Deprecation<a name="version-deprecation"></a>

In line with the Kubernetes community support for Kubernetes versions, Amazon EKS is committed to running at least three production\-ready versions of Kubernetes at any given time, with a fourth version in deprecation\. 

We will announce the deprecation of a given Kubernetes minor version at least 60 days before the deprecation date\. Because of the Amazon EKS qualification and release process for new Kubernetes versions, the deprecation of a Kubernetes version on Amazon EKS will be on or after the date the Kubernetes project stops supporting the version upstream\.

On the deprecation date, Amazon EKS clusters running the version targeted for deprecation will begin to be updated to the next Amazon EKS\-supported version of Kubernetes\. This means that if the deprecated version is 1\.11, clusters will eventually be automatically updated to version 1\.12\. If a cluster is automatically updated by Amazon EKS, you must also update the version of your worker nodes after the update is complete\. For more information, see [Worker Node Updates](update-workers.md)\.

Kubernetes supports compatibility between masters and workers for at least 2 minor versions, so 1\.11 workers will continue to operate when orchestrated by a 1\.12 control plane\. For more information, see [Kubernetes Version and Version Skew Support Policy](https://kubernetes.io/docs/setup/version-skew-policy/) in the Kubernetes documentation\.