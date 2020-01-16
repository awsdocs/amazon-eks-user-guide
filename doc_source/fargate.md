# AWS Fargate<a name="fargate"></a>

This chapter discusses using Amazon EKS to run Kubernetes pods on AWS Fargate\.

AWS Fargate is a technology that provides on\-demand, right\-sized compute capacity for [containers](https://aws.amazon.com/what-are-containers)\. With AWS Fargate, you no longer have to provision, configure, or scale groups of virtual machines to run containers\. This removes the need to choose server types, decide when to scale your node groups, or optimize cluster packing\.

You can control which pods start on Fargate and how they run with [Fargate profiles](fargate-profile.md), which are defined as part of your Amazon EKS cluster\.

Amazon EKS integrates Kubernetes with AWS Fargate by using controllers that are built by AWS using the upstream, extensible model provided by Kubernetes\. These controllers run as part of the Amazon EKS managed Kubernetes control plane and are responsible for scheduling native Kubernetes pods onto Fargate\. The Fargate controllers include a new scheduler that runs alongside the default Kubernetes scheduler in addition to several mutating and validating admission controllers\. When you start a pod that meets the criteria for running on Fargate, the Fargate controllers running in the cluster recognize, update, and schedule the pod onto Fargate\.

Each pod running on Fargate has its own isolation boundary and does not share the underlying kernel, CPU resources, memory resources, or elastic network interface with another pod\.

This chapter describes the different components of pods running on Fargate, and calls out special considerations for using Fargate with Amazon EKS\.

AWS Fargate with Amazon EKS is currently only available in the following Regions:


| Region Name | Region | 
| --- | --- | 
| US East \(Ohio\) | us\-east\-2 | 
| US East \(N\. Virginia\) | us\-east\-1 | 
| Asia Pacific \(Tokyo\) | ap\-northeast\-1 | 
| EU \(Ireland\) | eu\-west\-1 | 

**Topics**
+ [AWS Fargate Considerations](#fargate-considerations)
+ [Getting Started with AWS Fargate on Amazon EKS](fargate-getting-started.md)
+ [AWS Fargate Profile](fargate-profile.md)
+ [Fargate Pod Configuration](fargate-pod-configuration.md)

## AWS Fargate Considerations<a name="fargate-considerations"></a>

Here's some things to consider about using Fargate on Amazon EKS\.
+ Classic Load Balancers and Network Load Balancers are not supported on pods running on Fargate\. For ingress, we recommend that you use the [ALB Ingress Controller on Amazon EKS](alb-ingress.md) \(minimum version v1\.1\.4\)\.
+ Pods must match a Fargate profile at the time that they are scheduled in order to run on Fargate\. Pods which do not match a Fargate profile may be stuck as `Pending`\. If a matching Fargate profile exists, you can delete pending pods that you have created to reschedule them onto Fargate\.
+ Daemonsets are not supported on Fargate\. If your application requires a daemon, you should reconfigure that daemon to run as a sidecar container in your pods\.
+ Privileged containers are not supported on Fargate\.
+ Pods running on Fargate cannot specify HostPort or HostNetwork in the pod manifest\.
+ GPUs are currently not available on Fargate\.
+ Pods running on Fargate are not assigned public IP addresses, so only private subnets \(with no direct route to an Internet Gateway\) are supported when you create a Fargate profile\.
+ We recommend using the [Vertical Pod Autoscaler](vertical-pod-autoscaler.md) with pods running on Fargate to optimize the CPU and memory used for your applications\. However, because changing the resource allocation for a pod requires the pod to be restarted, you must set the pod update policy to either `Auto` or `Recreate` to ensure correct functionality\.
+ Stateful applications are not recommended for pods running on Fargate\. Instead, we recommend that you use AWS solutions such as Amazon S3 or DynamoDB for pod data storage\.
+ Fargate runs each pod in a VM\-isolated environment without sharing resources with other pods\. However, because Kubernetes is a single\-tenant orchestrator, Fargate cannot guarantee pod\-level security isolation\. You should run sensitive workloads or untrusted workloads that need complete security isolation using separate Amazon EKS clusters\.
+ While adding labels : **Key** cannot contain "kubernetes.io", or "k8s.io", or "eks.amazonaws.com". **Values** must consist of alphanumeric characters or "-", "_", ".", and must start and end with an alphanumeric character
