# Manage `kube-proxy` in Amazon EKS clusters<a name="managing-kube-proxy"></a>

**Important**  
We recommend adding the Amazon EKS type of the add\-on to your cluster instead of using the self\-managed type of the add\-on\. If you're not familiar with the difference between the types, see [Amazon EKS add\-ons](eks-add-ons.md)\. For more information about adding an Amazon EKS add\-on to your cluster, see [Creating an Amazon EKS add\-on](creating-an-add-on.md)\. If you're unable to use the Amazon EKS add\-on, we encourage you to submit an issue about why you can't to the [Containers roadmap GitHub repository](https://github.com/aws/containers-roadmap/issues)\.

The `kube-proxy` add\-on is deployed on each Amazon EC2 node in your Amazon EKS cluster\. It maintains network rules on your nodes and enables network communication to your Pods\. The add\-on isn't deployed to Fargate nodes in your cluster\. For more information, see [https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/) in the Kubernetes documentation\.

## `kube-proxy` versions<a name="kube-proxy-versions"></a>

The following table lists the latest version of the Amazon EKS add\-on type for each Kubernetes version\.


| Kubernetes version | `1.30` | `1.29` | `1.28` | `1.27` | `1.26` | `1.25` | `1.24` | `1.23` | 
| --- | --- | --- | --- | --- | --- | --- | --- | --- | 
|  | v1\.30\.3\-eksbuild\.5 | v1\.29\.7\-eksbuild\.5 | v1\.28\.12\-eksbuild\.5 | v1\.27\.16\-eksbuild\.3 | v1\.26\.15\-eksbuild\.10 | v1\.25\.16\-eksbuild\.13 | v1\.24\.17\-eksbuild\.19 | v1\.23\.17\-eksbuild\.16 | 

**Important**  
An earlier version of the documentation was incorrect\. `kube-proxy` versions `v1.28.5`, `v1.27.9`, and `v1.26.12` aren't available\.  
If you're self\-managing this add\-on, the versions in the table might not be the same as the available self\-managed versions\.

## `kube-proxy` container image migration<a name="managing-kube-proxy-images"></a>

There are two types of the `kube-proxy` container image available for each Amazon EKS cluster version:
+ **Default** – This image type is based on a Debian\-based Docker image that is maintained by the Kubernetes upstream community\.
+ **Minimal** – This image type is based on a [minimal base image](https://gallery.ecr.aws/eks-distro-build-tooling/eks-distro-minimal-base-iptables) maintained by Amazon EKS Distro, which contains minimal packages and doesn't have shells\. For more information, see [Amazon EKS Distro](https://distro.eks.amazonaws.com/)\.

The following table lists the latest available self\-managed `kube-proxy` container image version for each Amazon EKS cluster version\.


| Image type | `1.30` | `1.29` | `1.28` | `1.27` | `1.26` | `1.25` | `1.24` | `1.23` | 
| --- | --- | --- | --- | --- | --- | --- | --- | --- | 
| kube\-proxy \(default type\) | Only minimal type is available | Only minimal type is available | Only minimal type is available | Only minimal type is available | Only minimal type is available | Only minimal type is available | v1\.24\.10\-eksbuild\.2 | v1\.23\.16\-eksbuild\.2 | 
| kube\-proxy \(minimal type\) | v1\.30\.3\-minimal\-eksbuild\.5 | v1\.29\.7\-minimal\-eksbuild\.5 | v1\.28\.12\-minimal\-eksbuild\.5 | v1\.27\.16\-minimal\-eksbuild\.3 | v1\.26\.15\-minimal\-eksbuild\.10 | v1\.25\.16\-minimal\-eksbuild\.8 | v1\.24\.17\-minimal\-eksbuild\.4 | v1\.23\.17\-minimal\-eksbuild\.5 | 

**Important**  
The default image type isn't available for Kubernetes version `1.25` and later\. You must use the minimal image type\.
When you [update an Amazon EKS add\-on type](updating-an-add-on.md), you specify a valid Amazon EKS add\-on version, which might not be a version listed in this table\. This is because [Amazon EKS add\-on](workloads-add-ons-available-eks.md#add-ons-kube-proxy) versions don't always match container image versions specified when updating the self\-managed type of this add\-on\. When you update the self\-managed type of this add\-on, you specify a valid container image version listed in this table\. 