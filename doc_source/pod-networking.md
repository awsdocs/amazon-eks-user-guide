# Pod networking \(CNI\)<a name="pod-networking"></a>

Amazon EKS supports native VPC networking via the Amazon VPC CNI plugin for Kubernetes\. Using this CNI plugin allows Kubernetes pods to have the same IP address inside the pod as they do on the VPC network\. This CNI plugin is an open\-source project that is maintained on [GitHub](https://github.com/aws/amazon-vpc-cni-k8s)\.

![\[EKS networking\]](http://docs.aws.amazon.com/eks/latest/userguide/images/networking.png)

The CNI plugin is responsible for allocating VPC IP addresses to Kubernetes nodes and configuring the necessary networking for pods on each node\. ​The plugin consists of two primary components:
+ The L\-IPAM daemon is responsible for attaching elastic network interfaces to instances, assigning secondary IP addresses to elastic network interfaces, and maintaining a "warm pool" of IP addresses on each node for assignment to Kubernetes pods when they are scheduled\.
+ The CNI plugin itself is responsible for wiring the host network \(for example, configuring the interfaces and virtual Ethernet pairs\) and adding the correct interface to the pod namespace\. 

For more information about the design and networking configuration, see [CNI plugin for Kubernetes networking over AWS VPC](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/README.md)\.

Elastic network interface and secondary IP address limitations by Amazon EC2 instance types are applicable\. In general, larger instances can support more IP addresses\. For more information, see [IP Addresses Per Network Interface Per Instance Type](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#AvailableIpPerENI) in the *Amazon EC2 User Guide for Linux Instances*\.

**Topics**
+ [CNI configuration variables](cni-env-vars.md)
+ [External source network address translation \(SNAT\)](external-snat.md)
+ [CNI custom networking](cni-custom-network.md)
+ [CNI metrics helper](cni-metrics-helper.md)
+ [Amazon VPC CNI plugin for Kubernetes upgrades](cni-upgrades.md)