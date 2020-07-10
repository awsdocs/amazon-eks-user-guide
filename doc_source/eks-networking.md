# Amazon EKS networking<a name="eks-networking"></a>

This chapter covers the following networking topics for running Kubernetes on Amazon EKS\.
+ [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md#create-vpc) – An Amazon Virtual Private Cloud \(Amazon VPC\) enables you to launch AWS resources into a virtual network that you've defined\.
+ [Cluster VPC considerations](network_reqs.md) – Learn about requirements for your VPC and subnets\.
+ [Amazon EKS security group considerations](sec-group-reqs.md) – Learn about requirements for security groups\.
+ [Pod networking \(CNI\)](pod-networking.md) – Using the CNI plugin allows Kubernetes pods to have the same IP address inside the pod as they do on the VPC network\.
+ [Installing or upgrading CoreDNS](coredns.md) – CoreDNS is supported on Amazon EKS clusters with Kubernetes version 1\.14 or later\.
+ [Installing Calico on Amazon EKS](calico.md) – Project Calico is a network policy engine for Kubernetes\. With Calico network policy enforcement, you can implement network segmentation and tenant isolation\.