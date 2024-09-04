# Assign IPv6 addresses to clusters, pods, and services<a name="cni-ipv6"></a>

**Applies to**: Pods with Amazon EC2 instances and Fargate Pods 

By default, Kubernetes assigns `IPv4` addresses to your Pods and services\. Instead of assigning `IPv4` addresses to your Pods and services, you can configure your cluster to assign `IPv6` addresses to them\. Amazon EKS doesn't support dual\-stacked Pods or services, even though Kubernetes does in version `1.23` and later\. As a result, you can't assign both `IPv4` and `IPv6` addresses to your Pods and services\. 

You select which IP family you want to use for your cluster when you create it\. You can't change the family after you create the cluster\.

## Considerations<a name="ipv6-considerations"></a>

The following are considerations for using the feature:
+ You must create a new cluster and specify that you want to use the `IPv6` family for that cluster\. You can't enable the `IPv6` family for a cluster that you updated from a previous version\. For instructions on how to create a new cluster, see [Considerations ](#ipv6-considerations)\.
+ The version of the Amazon VPC CNI add\-on that you deploy to your cluster must be version `1.10.1` or later\. This version or later is deployed by default\. After you deploy the add\-on, you can't downgrade your Amazon VPC CNI add\-on to a version lower than `1.10.1` without first removing all nodes in all node groups in your cluster\.
+ Windows Pods and services aren't supported\.
+ If you use Amazon EC2 nodes, you must configure the Amazon VPC CNI add\-on with IP prefix delegation and `IPv6`\. If you choose the `IPv6` family when creating your cluster, the `1.10.1` version of the add\-on defaults to this configuration\. This is the case for both a self\-managed or Amazon EKS add\-on\. For more information about IP prefix delegation, see [Assign more IP addresses to Amazon EKS nodes with prefixes](cni-increase-ip-addresses.md)\.
+ When you create a cluster, the VPC and subnets that you specify must have an `IPv6` CIDR block that's assigned to the VPC and subnets that you specify\. They must also have an `IPv4` CIDR block assigned to them\. This is because, even if you only want to use `IPv6`, a VPC still requires an `IPv4` CIDR block to function\. For more information, see [Associate an `IPv6` CIDR block with your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html#vpc-associate-ipv6-cidr) in the Amazon VPC User Guide\.
+ When you create your nodes, you must specify subnets that are configured to auto\-assign `IPv6` addresses\. Otherwise, you can't deploy your nodes\. By default, this configuration is disabled\. For more information, see [Modify the `IPv6` addressing attribute for your subnet](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#subnet-ipv6) in the Amazon VPC User Guide\.
+ The route tables that are assigned to your subnets must have routes for `IPv6` addresses\. For more information, see [Migrate to `IPv6`](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-migrate-ipv6.html) in the Amazon VPC User Guide\.
+ Your security groups must allow `IPv6` addresses\. For more information, see [Migrate to `IPv6`](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-migrate-ipv6.html) in the Amazon VPC User Guide\.
+ You can only use `IPv6` with AWS Nitro\-based Amazon EC2 or Fargate nodes\.
+ You can use `IPv6` with [Assign security groups to individual pods](security-groups-for-pods.md) with Amazon EC2 nodes and Fargate nodes\.
+ If you previously used [custom networking](cni-custom-network.md) to help alleviate IP address exhaustion, you can use `IPv6` instead\. You can't use custom networking with `IPv6`\. If you use custom networking for network isolation, then you might need to continue to use custom networking and the `IPv4` family for your clusters\.
+ You can't use `IPv6` with [AWS Outposts](eks-outposts.md)\.
+ Kubernetes Services are only assigned an IPv6 address\. They aren't assigned an IPv4 address\. 
+ Pods are assigned an IPv6 address and a host\-local IPv4 address\. The host\-local IPv4 address is assigned by using a host\-local CNI plugin chained with VPC CNI and the address is not reported to the Kubernetes control plane\. It is only used when a pod needs to communicate with an external IPv4 resources in another Amazon VPC or the internet\. The host\-local IPv4 address gets SNATed \(by VPC CNI\) to the primary IPv4 address of the primary ENI of the worker node\. 
+ Pods and services are only assigned an `IPv6` address\. They aren't assigned an `IPv4` address\. Because Pods are able to communicate to `IPv4` endpoints through NAT on the instance itself, [DNS64 and NAT64](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html#nat-gateway-nat64-dns64) aren't needed\. If the traffic needs a public IP address, the traffic is then source network address translated to a public IP\.
+ The source `IPv6` address of a Pod isn't source network address translated to the `IPv6` address of the node when communicating outside of the VPC\. It is routed using an internet gateway or egress\-only internet gateway\.
+ All nodes are assigned an `IPv4` and `IPv6` address\.
+ The [Store high\-performance apps with FSx for Lustre](fsx-csi.md) is not supported\.
+ You can use version `2.3.1` or later of the AWS Load Balancer Controller to load balance [application](alb-ingress.md) or [network](network-load-balancing.md) traffic to `IPv6` Pods in IP mode, but not instance mode\. For more information, see [Route internet traffic with AWS Load Balancer Controller](aws-load-balancer-controller.md)\.
+ You must attach an `IPv6` IAM policy to your node IAM or CNI IAM role\. Between the two, we recommend that you attach it to a CNI IAM role\. For more information, see [Create IAM policy for clusters that use the `IPv6` family](cni-iam-role.md#cni-iam-role-create-ipv6-policy) and [Step 1: Create the Amazon VPC CNI plugin for Kubernetes IAM role](cni-iam-role.md#cni-iam-role-create-role)\.
+ Each Fargate Pod receives an `IPv6` address from the CIDR that's specified for the subnet that it's deployed in\. The underlying hardware unit that runs Fargate Pods gets a unique `IPv4` and `IPv6` address from the CIDRs that are assigned to the subnet that the hardware unit is deployed in\.
+ We recommend that you perform a thorough evaluation of your applications, Amazon EKS add\-ons, and AWS services that you integrate with before deploying `IPv6` clusters\. This is to ensure that everything works as expected with `IPv6`\.
+ Use of the Amazon EC2 [Instance Metadata Service](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html) `IPv6` endpoint is not supported with Amazon EKS\.
+ When creating a self\-managed node group in a cluster that uses the `IPv6` family, user\-data must include the following `BootstrapArguments` for the [https://github.com/awslabs/amazon-eks-ami/blob/main/templates/al2/runtime/bootstrap.sh](https://github.com/awslabs/amazon-eks-ami/blob/main/templates/al2/runtime/bootstrap.sh) file that runs at node start up\. Replace *your\-cidr* with the `IPv6` CIDR range of your cluster's VPC\.

  ```
  --ip-family ipv6 --service-ipv6-cidr your-cidr
  ```

  If you don't know the `IPv6` `CIDR` range for your cluster, you can see it with the following command \(requires the AWS CLI version `2.4.9` or later\)\.

  ```
  aws eks describe-cluster --name my-cluster --query cluster.kubernetesNetworkConfig.serviceIpv6Cidr --output text
  ```