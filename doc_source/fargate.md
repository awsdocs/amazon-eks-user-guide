--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# AWS Fargate<a name="fargate"></a>

**Important**  
 AWS Fargate with Amazon EKS isn’t available in AWS GovCloud \(US\-East\) and AWS GovCloud \(US\-West\)\.

This topic discusses using Amazon EKS to run Kubernetes Pods on AWS Fargate\. Fargate is a technology that provides on\-demand, right\-sized compute capacity for [containers](https://aws.amazon.com/what-are-containers)\. With Fargate, you don’t have to provision, configure, or scale groups of virtual machines on your own to run containers\. You also don’t need to choose server types, decide when to scale your node groups, or optimize cluster packing\.

This topic describes the different components of Pods that run on Fargate, and calls out special considerations for using Fargate with Amazon EKS\.

## AWS Fargate considerations<a name="fargate-considerations"></a>

Here are some things to consider about using Fargate on Amazon EKS\.
+ Each Pod that runs on Fargate has its own isolation boundary\. They don’t share the underlying kernel, CPU resources, memory resources, or elastic network interface with another Pod\.
+ Fargate exposed services only run on target type IP mode, and not on node IP mode\. The recommended way to check the connectivity from a service running on a managed node and a service running on Fargate is to connect via service name\.
+ Pods must match a Fargate profile at the time that they’re scheduled to run on Fargate\. Pods that don’t match a Fargate profile might be stuck as `Pending`\. If a matching Fargate profile exists, you can delete pending Pods that you have created to reschedule them onto Fargate\.
+ Daemonsets aren’t supported on Fargate\. If your application requires a daemon, reconfigure that daemon to run as a sidecar container in your Pods\.
+ Privileged containers aren’t supported on Fargate\.
+ Pods running on Fargate can’t specify `HostPort` or `HostNetwork` in the Pod manifest\.
+ The default `nofile` and `nproc` soft limit is 1024 and the hard limit is 65535 for Fargate Pods\.
+ GPUs aren’t currently available on Fargate\.
+ DNS resolution and DNS hostnames must be enabled for your VPC\. For more information, see [Viewing and updating DNS support for your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns.html#vpc-dns-updating)\.
+ Amazon EKS Fargate adds defense\-in\-depth for Kubernetes applications by isolating each Pod within a Virtual Machine \(VM\)\. This VM boundary prevents access to host\-based resources used by other Pods in the event of a container escape, which is a common method of attacking containerized applications and gain access to resources outside of the container\.
+ Fargate profiles support specifying subnets from VPC secondary CIDR blocks\. You might want to specify a secondary CIDR block\. This is because there’s a limited number of IP addresses available in a subnet\. As a result, there’s also a limited number of Pods that can be created in the cluster\. By using different subnets for Pods, you can increase the number of available IP addresses\. For more information, see [Adding IPv4 CIDR blocks to a VPC\.](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html#vpc-resize) 
+ You can’t deploy Fargate Pods to AWS Outposts, AWS Wavelength, or AWS Local Zones\.
+ A Pod running on Fargate automatically mounts an Amazon EFS file system\. You can’t use dynamic persistent volume provisioning with Fargate nodes, but you can use static provisioning\.
+ You can’t mount Amazon EBS volumes to Fargate Pods\.
+ You can run the Amazon EBS CSI controller on Fargate nodes, but the Amazon EBS CSI node DaemonSet can only run on Amazon EC2 instances\.
+ After a [Kubernetes Job](https://kubernetes.io/docs/concepts/workloads/controllers/job/) is marked `Completed` or `Failed`, the Pods that the Job creates normally continue to exist\. This behavior allows you to view your logs and results, but with Fargate you will incur costs if you don’t clean up the Job afterwards\.

  To automatically delete the related Pods after a Job completes or fails, you can specify a time period using the time\-to\-live \(TTL\) controller\. The following example shows specifying `0spec.ttlSecondsAfterFinished` in your Job manifest\.

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