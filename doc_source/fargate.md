# AWS Fargate<a name="fargate"></a>

**Important**  
AWS Fargate with Amazon EKS isn't available in AWS GovCloud \(US\-East\) and AWS GovCloud \(US\-West\)\.

This topic discusses using Amazon EKS to run Kubernetes Pods on AWS Fargate\. Fargate is a technology that provides on\-demand, right\-sized compute capacity for [containers](https://aws.amazon.com/what-are-containers)\. With Fargate, you don't have to provision, configure, or scale groups of virtual machines on your own to run containers\. You also don't need to choose server types, decide when to scale your node groups, or optimize cluster packing\.

You can control which Pods start on Fargate and how they run with [Fargate profiles](fargate-profile.md)\. Fargate profiles are defined as part of your Amazon EKS cluster\. Amazon EKS integrates Kubernetes with Fargate by using controllers that are built by AWS using the upstream, extensible model provided by Kubernetes\. These controllers run as part of the Amazon EKS managed Kubernetes control plane and are responsible for scheduling native Kubernetes Pods onto Fargate\. The Fargate controllers include a new scheduler that runs alongside the default Kubernetes scheduler in addition to several mutating and validating admission controllers\. When you start a Pod that meets the criteria for running on Fargate, the Fargate controllers that are running in the cluster recognize, update, and schedule the Pod onto Fargate\.

This topic describes the different components of Pods that run on Fargate, and calls out special considerations for using Fargate with Amazon EKS\.

## AWS Fargate considerations<a name="fargate-considerations"></a>

Here are some things to consider about using Fargate on Amazon EKS\.
+ Each Pod that runs on Fargate has its own isolation boundary\. They don't share the underlying kernel, CPU resources, memory resources, or elastic network interface with another Pod\.
+ Network Load Balancers and Application Load Balancers \(ALBs\) can be used with Fargate with IP targets only\. For more information, see [Create a network load balancer](network-load-balancing.md#network-load-balancer) and [Application load balancing on Amazon EKS](alb-ingress.md)\. 
+ Fargate exposed services only run on target type IP mode, and not on node IP mode\. The recommended way to check the connectivity from a service running on a managed node and a service running on Fargate is to connect via service name\.
+ Pods must match a Fargate profile at the time that they're scheduled to run on Fargate\. Pods that don't match a Fargate profile might be stuck as `Pending`\. If a matching Fargate profile exists, you can delete pending Pods that you have created to reschedule them onto Fargate\.
+ Daemonsets aren't supported on Fargate\. If your application requires a daemon, reconfigure that daemon to run as a sidecar container in your Pods\.
+ Privileged containers aren't supported on Fargate\.
+ Pods running on Fargate can't specify `HostPort` or `HostNetwork` in the Pod manifest\.
+ The default `nofile` and `nproc` soft limit is 1024 and the hard limit is 65535 for Fargate Pods\.
+ GPUs aren't currently available on Fargate\.
+ Pods that run on Fargate are only supported on private subnets \(with NAT gateway access to AWS services, but not a direct route to an Internet Gateway\), so your cluster's VPC must have private subnets available\. For clusters without outbound internet access, see [Private cluster requirements](private-clusters.md)\.
+ You can use the [Vertical Pod Autoscaler](vertical-pod-autoscaler.md) to set the initial correct size of CPU and memory for your Fargate Pods, and then use the [Horizontal Pod Autoscaler](horizontal-pod-autoscaler.md) to scale those Pods\. If you want the Vertical Pod Autoscaler to automatically re\-deploy Pods to Fargate with larger CPU and memory combinations, set the mode for the Vertical Pod Autoscaler to either `Auto` or `Recreate` to ensure correct functionality\. For more information, see the [Vertical Pod Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler#quick-start) documentation on GitHub\.
+ DNS resolution and DNS hostnames must be enabled for your VPC\. For more information, see [Viewing and updating DNS support for your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns.html#vpc-dns-updating)\.
+ Amazon EKS Fargate adds defense\-in\-depth for Kubernetes applications by isolating each Pod within a Virtual Machine \(VM\)\. This VM boundary prevents access to host\-based resources used by other Pods in the event of a container escape, which is a common method of attacking containerized applications and gain access to resources outside of the container\.

  Using Amazon EKS doesn't change your responsibilities under the [shared responsibility model](security.md)\. You should carefully consider the configuration of cluster security and governance controls\. The safest way to isolate an application is always to run it in a separate cluster\.
+ Fargate profiles support specifying subnets from VPC secondary CIDR blocks\. You might want to specify a secondary CIDR block\. This is because there's a limited number of IP addresses available in a subnet\. As a result, there's also a limited number of Pods that can be created in the cluster\. By using different subnets for Pods, you can increase the number of available IP addresses\. For more information, see [Adding `IPv4` CIDR blocks to a VPC\.](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html#vpc-resize)
+ The Amazon EC2 instance metadata service \(IMDS\) isn't available to Pods that are deployed to Fargate nodes\. If you have Pods that are deployed to Fargate that need IAM credentials, assign them to your Pods using [IAM roles for service accounts](iam-roles-for-service-accounts.md)\. If your Pods need access to other information available through IMDS, then you must hard code this information into your Pod spec\. This includes the AWS Region or Availability Zone that a Pod is deployed to\.
+ You can't deploy Fargate Pods to AWS Outposts, AWS Wavelength, or AWS Local Zones\.
+ Amazon EKS must periodically patch Fargate Pods to keep them secure\. We attempt the updates in a way that reduces impact, but there are times when Pods must be deleted if they aren't successfully evicted\. There are some actions you can take to minimize disruption\. For more information, see [Fargate OS patching](fargate-pod-patching.md)\.
+ The [Amazon VPC CNI plugin for Amazon EKS](https://github.com/aws/amazon-vpc-cni-plugins) is installed on Fargate nodes\. You can't use [Alternate compatible CNI plugins](alternate-cni-plugins.md) with Fargate nodes\.
+ A Pod running on Fargate automatically mounts an Amazon EFS file system\. You can't use dynamic persistent volume provisioning with Fargate nodes, but you can use static provisioning\.
+ You can't mount Amazon EBS volumes to Fargate Pods\.
+ You can run the Amazon EBS CSI controller on Fargate nodes, but the Amazon EBS CSI node DaemonSet can only run on Amazon EC2 instances\.
+ After a [Kubernetes Job](https://kubernetes.io/docs/concepts/workloads/controllers/job/) is marked `Completed` or `Failed`, the Pods that the Job creates normally continue to exist\. This behavior allows you to view your logs and results, but with Fargate you will incur costs if you don't clean up the Job afterwards\.

  To automatically delete the related Pods after a Job completes or fails, you can specify a time period using the time\-to\-live \(TTL\) controller\. The following example shows specifying `.spec.ttlSecondsAfterFinished` in your Job manifest\.

  ```
  apiVersion: batch/v1
  kind: Job
  metadata:
    name: busybox
  spec:
    template:
      spec:
        containers:
        - name: busybox
          image: busybox
          command: ["/bin/sh", "-c", "sleep 10"]
        restartPolicy: Never
    ttlSecondsAfterFinished: 60 # <-- TTL controller
  ```