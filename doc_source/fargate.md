# AWS Fargate<a name="fargate"></a>

This topic discusses using Amazon EKS to run Kubernetes pods on AWS Fargate\.

AWS Fargate is a technology that provides on\-demand, right\-sized compute capacity for [containers](https://aws.amazon.com/what-are-containers)\. With AWS Fargate, you no longer have to provision, configure, or scale groups of virtual machines to run containers\. This removes the need to choose server types, decide when to scale your node groups, or optimize cluster packing\. You can control which pods start on Fargate and how they run with [Fargate profiles](fargate-profile.md), which are defined as part of your Amazon EKS cluster\.

Amazon EKS integrates Kubernetes with AWS Fargate by using controllers that are built by AWS using the upstream, extensible model provided by Kubernetes\. These controllers run as part of the Amazon EKS managed Kubernetes control plane and are responsible for scheduling native Kubernetes pods onto Fargate\. The Fargate controllers include a new scheduler that runs alongside the default Kubernetes scheduler in addition to several mutating and validating admission controllers\. When you start a pod that meets the criteria for running on Fargate, the Fargate controllers running in the cluster recognize, update, and schedule the pod onto Fargate\.

This topic describes the different components of pods running on Fargate, and calls out special considerations for using Fargate with Amazon EKS\.

## AWS Fargate considerations<a name="fargate-considerations"></a>

Here's some things to consider about using Fargate on Amazon EKS\.
+ AWS Fargate with Amazon EKS is available in all Amazon EKS Regions except China \(Beijing\), China \(Ningxia\), AWS GovCloud \(US\-East\), and AWS GovCloud \(US\-West\)\.
+ Each pod running on Fargate has its own isolation boundary and does not share the underlying kernel, CPU resources, memory resources, or elastic network interface with another pod\.
+ Network Load Balancers and Application Load Balancers can be used with Fargate with IP targets only\. For more information, see [Load balancer – IP targets](load-balancing.md#load-balancer-ip) and [Application load balancing on Amazon EKS](alb-ingress.md)\. 
+ Pods must match a Fargate profile at the time that they are scheduled in order to run on Fargate\. Pods which do not match a Fargate profile may be stuck as `Pending`\. If a matching Fargate profile exists, you can delete pending pods that you have created to reschedule them onto Fargate\.
+ Daemonsets are not supported on Fargate\. If your application requires a daemon, you should reconfigure that daemon to run as a sidecar container in your pods\.
+ Privileged containers are not supported on Fargate\.
+ Pods running on Fargate cannot specify `HostPort` or `HostNetwork` in the pod manifest\.
+ The default `nofile` and `nproc` soft limit is 1024 and the hard limit is 65535 for Fargate pods\.
+ GPUs are currently not available on Fargate\.
+ You cannot use [Security groups for pods](security-groups-for-pods.md) with pods running on Fargate\.
+ Pods running on Fargate are only supported on private subnets \(with NAT gateway access to AWS services, but not a direct route to an Internet Gateway\), so your cluster's VPC must have private subnets available\. For clusters without outbound internet access, see [Private clusters](private-clusters.md)\.
+ You can use the [Vertical Pod Autoscaler](vertical-pod-autoscaler.md) to initially right size the CPU and memory for your Fargate pods, and then use the [Horizontal Pod Autoscaler](horizontal-pod-autoscaler.md) to scale those pods\. If you want the Vertical Pod Autoscaler to automatically re\-deploy pods to Fargate with larger CPU and memory combinations, then set the Vertical Pod Autoscaler's mode to either `Auto` or `Recreate` to ensure correct functionality\. For more information, see the [Vertical Pod Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler#quick-start) documentation on GitHub\.
+ DNS resolution and DNS hostnames must be enabled for your VPC\. For more information, see [Viewing and updating DNS support for your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns.html#vpc-dns-updating)\.
+ Fargate runs each pod in a VM\-isolated environment without sharing resources with other pods\. However, because Kubernetes is a single\-tenant orchestrator, Fargate cannot guarantee pod\-level security isolation\. You should run sensitive workloads or untrusted workloads that need complete security isolation using separate Amazon EKS clusters\.
+ Fargate profiles support specifying subnets from VPC secondary CIDR blocks\. You may want to specify a secondary CIDR block because there are a limited number of IP addresses available in a subnet\. As a result, there are a limited number of pods that can be created in the cluster\. Using different subnets for pods allows you to increase the number of available IP addresses\. For more information, see [Adding IPv4 CIDR blocks to a VPC\.](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html#vpc-resize)
+ The Amazon EC2 instance metadata service \(IMDS\) is not available to pods deployed to Fargate nodes\. If you have pods deployed to Fargate that need IAM credentials, assign them to your pods using [IAM roles for service accounts](iam-roles-for-service-accounts.md)\. If your pods need access to other information available through IMDS, such as the Region or Availability Zone that a pod is deployed to, then you must hard code this information into your pod spec\.
+ You can't deploy Fargate pods to AWS Outposts, AWS Wavelength or AWS Local Zones\.