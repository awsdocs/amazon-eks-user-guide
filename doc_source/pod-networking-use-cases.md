# Choosing pod networking use cases<a name="pod-networking-use-cases"></a>

The Amazon VPC CNI plugin provides networking for pods\. The following table helps you understand which networking use cases you can use together and the capabilities and Amazon VPC CNI plugin settings that you can use with different Amazon EKS node types\. All information in the table applies to Linux IPv4 nodes only\.

[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/pod-networking-use-cases.html)

**Note**  
Traffic flow to and from Pods with associated security groups are not subjected to Calico network policy enforcement and are limited to Amazon VPC security group enforcement only\. 
IP prefixes and IP addresses are associated with standard Amazon EC2 elastic network interfaces\. Pods requiring specific security groups are assigned the primary IP address of a branch network interface\. You can mix pods getting IP addresses, or IP addresses from IP prefixes with pods getting branch network interfaces on the same node\.

**Windows nodes**  
Each Windows node only supports one network interface and secondary IP addresses for Pods\. The maximum number of Pods for each node is equal to the number of IP addresses that you can assign to each Elastic network interface, minus one\. Calico network policies are supported on Windows\. For more information, see [Open Source Calico for Windows Containers on Amazon EKS](http://aws.amazon.com/blogs/containers/open-source-calico-for-windows-containers-on-amazon-eks/)\. You can't use [security groups for pods](security-groups-for-pods.md) on Windows\.