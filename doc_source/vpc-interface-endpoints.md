# Access the Amazon Elastic Kubernetes Service using an interface endpoint \(AWS PrivateLink\)<a name="vpc-interface-endpoints"></a>

You can use AWS PrivateLink to create a private connection between your VPC and Amazon Elastic Kubernetes Service\. You can access Amazon EKS as if it were in your VPC, without the use of an internet gateway, NAT device, VPN connection, or AWS Direct Connect connection\. Instances in your VPC don't need public IP addresses to access Amazon EKS\.

You establish this private connection by creating an interface endpoint powered by AWS PrivateLink\. We create an endpoint network interface in each subnet that you enable for the interface endpoint\. These are requester\-managed network interfaces that serve as the entry point for traffic destined for Amazon EKS\.

For more information, see [Access AWS services through AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/privatelink-access-aws-services.html) in the *AWS PrivateLink Guide*\.

## Considerations for Amazon EKS<a name="vpc-endpoint-considerations"></a>
+ Before you set up an interface endpoint for Amazon EKS, review [Considerations](https://docs.aws.amazon.com/vpc/latest/privatelink/create-interface-endpoint.html#considerations-interface-endpoints) in the *AWS PrivateLink Guide*\.
+ Amazon EKS supports making calls to all of its API actions through the interface endpoint, but not to the Kubernetes APIs\. The Kubernetes API server already supports a [private endpoint](cluster-endpoint.md)\. The Kubernetes API server private endpoint creates a private endpoint for the Kubernetes API server that you use to communicate with your cluster \(using Kubernetes management tools such as `kubectl`\)\. You can enable [private access](private-clusters.md) to the Kubernetes API server so that all communication between your nodes and the API server stays within your VPC\. AWS PrivateLink for the Amazon EKS API helps you call the Amazon EKS APIs from your VPC without exposing traffic to the public internet\.
+ You can't configure Amazon EKS to only be accessed through an interface endpoint\.
+ Standard pricing for AWS PrivateLink applies for interface endpoints for Amazon EKS\. You are billed for every hour that an interface endpoint is provisioned in each Availability Zone and for data processed through the interface endpoint\. For more information, see [AWS PrivateLink pricing](https://aws.amazon.com/privatelink/pricing/)\.
+ VPC endpoint policies are not supported for Amazon EKS\. By default, full access to Amazon EKS is allowed through the interface endpoint\. Alternatively, you can associate a security group with the endpoint network interfaces to control traffic to Amazon EKS through the interface endpoint\.
+ You can use VPC flow logs to capture information about IP traffic going to and from network interfaces, including interface endpoints\. You can publish flow log data to Amazon CloudWatch or Amazon S3\. For more information, see [Logging IP traffic using VPC Flow Logs](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html) in the Amazon VPC User Guide\.
+ You can access the Amazon EKS APIs from an on\-premises data center by connecting it to a VPC that has an interface endpoint\. You can use AWS Direct Connect or AWS Site\-to\-Site VPN to connect your on\-premises sites to a VPC\.
+ You can connect other VPCs to the VPC with an interface endpoint using an AWS Transit Gateway or VPC peering\. VPC peering is a networking connection between two VPCs\. You can establish a VPC peering connection between your VPCs, or with a VPC in another account\. The VPCs can be in different AWS Regions\. Traffic between peered VPCs stays on the AWS network\. The traffic doesn't traverse the public internet\. A Transit Gateway is a network transit hub that you can use to interconnect VPCs\. Traffic between a VPC and a Transit Gateway remains on the AWS global private network\. The traffic isn't exposed to the public internet\.
+ VPC interface endpoints for Amazon EKS are only accessible over `IPv4`\. `IPv6` isn't supported\.
+ AWS PrivateLink support isn't available in the Asia Pacific \(Hyderabad\), Asia Pacific \(Jakarta\), Asia Pacific \(Melbourne\), Asia Pacific \(Osaka\), Canada West \(Calgary\), Europe \(Spain\), Europe \(Zurich\), Israel \(Tel Aviv\), or Middle East \(UAE\) AWS Regions\.

## Create an interface endpoint for Amazon EKS<a name="vpc-endpoint-create"></a>

You can create an interface endpoint for Amazon EKS using either the Amazon VPC console or the AWS Command Line Interface \(AWS CLI\)\. For more information, see [Create a VPC endpoint](https://docs.aws.amazon.com/vpc/latest/privatelink/create-interface-endpoint.html#create-interface-endpoint-aws) in the *AWS PrivateLink Guide*\.

Create an interface endpoint for Amazon EKS using the following service name:

```
com.amazonaws.region-code.eks
```

The private DNS feature is enabled by default when creating an interface endpoint for Amazon EKS and other AWS services\. However, you must ensure that the following VPC attributes are set to `true`: `enableDnsHostnames` and `enableDnsSupport`\. For more information, see [View and update DNS attributes for your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns.html#vpc-dns-updating) in the Amazon VPC User Guide\. With the private DNS feature enabled for the interface endpoint:
+ You can make any API request to Amazon EKS using its default Regional DNS name\. For example, `eks.region.amazonaws.com`\. For a list of APIs, see [Actions](https://docs.aws.amazon.com/eks/latest/APIReference/API_Operations.html) in the Amazon EKS API Reference\.
+ You don't need to make any changes to your applications that call the EKS APIs\.
+ Any call made to the Amazon EKS default service endpoint is automatically routed through the interface endpoint over the private AWS network\.