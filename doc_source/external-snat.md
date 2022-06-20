# SNAT for pods<a name="external-snat"></a>

If you deployed your cluster using the `IPv6` family, then the information in this topic isn't applicable to your cluster, because `IPv6` addresses are not network translated\. For more information about using `IPv6` with your cluster, see [Assigning `IPv6` addresses to pods and services](cni-ipv6.md)\.

By default, each pod in your cluster is assigned a [private](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-instance-addressing.html#concepts-private-addresses) `IPv4` address from a classless inter\-domain routing \(CIDR\) block that is associated with the VPC that the pod is deployed in\. Pods in the same VPC communicate with each other using these private IP addresses as end points\. When a pod communicates to any `IPv4` address that isn't within a CIDR block that's associated to your VPC, the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s#amazon-vpc-cni-k8s) translates the pod's `IPv4` address to the primary private `IPv4` address of the primary [elastic network interface](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#eni-basics) of the node that the pod is running on, by default [\*](#snat-exception)\.

 Due to this behavior:
+ Resources that are in networks or VPCs that are connected to your cluster VPC using [VPC peering](https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html), a [transit VPC](https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/transit-vpc-option.html), or [Direct Connect](https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html) can't initiate communication to your pods\. Your pods can initiate communication to those resources and receive responses from them though\.
+ Your pods can communicate with internet resources only if the node that they're running on has a [public](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-instance-addressing.html#concepts-public-addresses) or [elastic](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-eips.html) IP address assigned to it and is in a public subnet\. A public subnet's associated [route table](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html) has a route to an internet gateway\. A private subnet's associated route table doesn't have a route to an internet gateway\. We recommend deploying nodes to private subnets, whenever possible\.

If you have either of the following requirements, then you need to change the default configuration of the Amazon VPC CNI plugin for Kubernetes:
+ You have resources in networks or VPCs that are connected to your cluster VPC using [VPC peering](https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html), a [transit VPC](https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/transit-vpc-option.html), or [Direct Connect](https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html) that need to initiate communication with your pods using an `IPv4` address\.
+ Your nodes are in private subnets\.

Change the default configuration with the following command\.

```
kubectl set env daemonset -n kube-system aws-node AWS_VPC_K8S_CNI_EXTERNALSNAT=true
```

If you want pods to communicate to the internet after you've changed the setting, then the route table that's associated with the private subnet must contain a route to a public [NAT gateway](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)\. Resources on the internet can't initiate communication to pods in private subnets, unless you've deployed a load balancer or ingress to a public subnet in your VPC\. The load balancer or ingress can route traffic to the private IP address of the pods\. For more information about creating network load balancers and ingresses \(application load balancers\), see [Network load balancing on Amazon EKS](network-load-balancing.md) and [Application load balancing on Amazon EKS](alb-ingress.md)\.

\*If a pod's spec contains `hostNetwork=true` \(default is `false`\), then its IP address isn't translated to a different address\. This is the case for the `kube-proxy` and Amazon VPC CNI plugin for Kubernetes pods that run on your cluster, by default\. For these pods, the IP address is the same as the node's primary IP address, so the pod's IP address isn't translated\. For more information about a pod's `hostNetwork` setting, see [PodSpec v1 core](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/#podspec-v1-core) in the Kubernetes API reference\. 
