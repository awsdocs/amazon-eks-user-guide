# External source network address translation \(SNAT\)<a name="external-snat"></a>

Communication within a VPC \(such as pod to pod\) is direct between private IP addresses and requires no source network address translation \(SNAT\)\. When traffic is destined for an address outside of the VPC, the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) translates the private IP address of each pod to the primary private IP address assigned to the primary [network interface](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html) \(network interface\) of the Amazon EC2 node that the pod is running on, by default\. SNAT:
+ Enables pods to communicate bi\-directionally with the internet\. The node must be in a [public subnet](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html#vpc-subnet-basics) and have a [public](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html) or [elastic](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-eips.html) IP address assigned to the primary private IP address of its primary network interface\. The traffic is translated to and from the public or Elastic IP address and routed to and from the internet by an [internet gateway](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html), as shown in the following picture\.   
![\[Image NOT FOUND\]](http://docs.aws.amazon.com/eks/latest/userguide/images/SNAT-enabled.jpg)

  SNAT is necessary because the internet gateway can only translate between the primary private and public or Elastic IP address assigned to the primary network interface of the Amazon EC2 instance node that pods are running on\.
+ Prevents a device in other private IP address spaces \(for example, [VPC peering](https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html), [Transit VPC](https://docs.aws.amazon.com/aws-technical-content/latest/aws-vpc-connectivity-options/transit-vpc.html), or [Direct Connect](https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html)\) from communicating directly to a pod that is not assigned the primary private IP address of the primary network interface of the Amazon EC2 instance node\. 

If the internet or devices in other private IP address spaces need to communicate with a pod that isn't assigned the primary private IP address assigned to the primary network interface of the Amazon EC2 instance node that the pod is running on, then:
+ The node must be deployed in a private subnet that has a route to a [NAT device](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-comparison.html) in a public subnet\.
+ You need to enable external SNAT in the CNI plugin `aws-node` DaemonSet with the following command:

  ```
  kubectl set env daemonset -n kube-system aws-node AWS_VPC_K8S_CNI_EXTERNALSNAT=true
  ```

After external SNAT is enabled, the CNI plugin doesn't translate a pod's private IP address to the primary private IP address assigned to the primary network interface of the Amazon EC2 instance node that the pod is running on when traffic is destined for an address outside of the VPC\. Traffic from the pod to the internet is externally translated to and from the public IP address of the NAT device and routed to and from the internet by an internet gateway, as shown in the following picture\.

![\[Image NOT FOUND\]](http://docs.aws.amazon.com/eks/latest/userguide/images/SNAT-disabled.jpg)