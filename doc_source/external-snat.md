# External Source Network Address Translation \(SNAT\)<a name="external-snat"></a>

By default, the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) configures pods with source network address translation \(SNAT\) enabled for traffic that leaves the VPC\. Communication within the VPC \(such as pod to pod\) is direct and SNAT does not occur; in this case, all routing is based on private IPs\.

For traffic that leaves the VPC, the CNI sets the source address for a packet to the primary private IP of the worker node's `eth0` interface\. When this traffic reaches the Internet Gateway, SNAT works differently in private and public subnets:
+ For pods running on worker nodes in a private subnet, the Internet Gateway translates the node's primary private IP address to the public IP address of the Internet Gateway\.
+ For pods running on worker nodes in a public subnet, the Internet Gateway translates the node's primary private IP address to the node's public IP address\.

However, SNAT can cause issues if traffic from another private IP space \(for example, [VPC peering](https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html), [Transit VPC](https://docs.aws.amazon.com/aws-technical-content/latest/aws-vpc-connectivity-options/transit-vpc.html), or [Direct Connect](https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html)\) attempts to communicate directly to a pod that is not attached to the primary elastic network interface of the Amazon EC2 instance\. To specify that NAT be handled by an external device \(such as a NAT gateway, and not on the instance itself\), you can disable SNAT on the instance by setting the `AWS_VPC_K8S_CNI_EXTERNALSNAT` environment variable to `true`\. Disable SNAT to allow inbound communication to your pods from external VPNs, direct connections, and external VPCs, and your pods do not need to access the internet directly via an internet gateway\.

**Note**  
SNAT is required for nodes that reside in a public subnet\. To use external SNAT, your nodes must reside in a private subnet and connect to the internet through a NAT gateway or another external NAT device\.

![\[SNAT disabled\]](http://docs.aws.amazon.com/eks/latest/userguide/images/SNAT-disabled.jpg)

**To disable SNAT on your worker nodes**
+ Set the `AWS_VPC_K8S_CNI_EXTERNALSNAT` environment variable to `true` in the `aws-node` DaemonSet:

  ```
  kubectl set env daemonset -n kube-system aws-node AWS_VPC_K8S_CNI_EXTERNALSNAT=true
  ```