--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Amazon EKS cluster endpoint access control<a name="cluster-endpoint"></a>

This topic helps you to enable private access for your Amazon EKS cluster’s Kubernetes API server endpoint and limit, or completely disable, public access from the internet\.

When you create a new cluster, Amazon EKS creates an endpoint for the managed Kubernetes API server that you use to communicate with your cluster \(using Kubernetes management tools such as `kubectl`\)\. By default, this API server endpoint is public to the internet, and access to the API server is secured using a combination of AWS Identity and Access Management \(IAM\) and native Kubernetes [Role Based Access Control](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) \(RBAC\)\.

You can enable private access to the Kubernetes API server so that all communication between your nodes and the API server stays within your VPC\. You can limit the IP addresses that can access your API server from the internet, or completely disable internet access to the API server\.

**Note**  
Because this endpoint is for the Kubernetes API server and not a traditional AWS PrivateLink endpoint for communicating with an AWS API, it doesn’t appear as an endpoint in the Amazon VPC console\.

When you enable endpoint private access for your cluster, Amazon EKS creates a Route 53 private hosted zone on your behalf and associates it with your cluster’s VPC\. This private hosted zone is managed by Amazon EKS, and it doesn’t appear in your account’s Route 53 resources\. In order for the private hosted zone to properly route traffic to your API server, your VPC must have `enableDnsHostnames` and `enableDnsSupport` set to `true`, and the DHCP options set for your VPC must include `AmazonProvidedDNS` in its domain name servers list\. For more information, see [Updating DNS support for your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns.html#vpc-dns-updating) in the *Amazon VPC User Guide*\.

You can define your API server endpoint access requirements when you create a new cluster, and you can update the API server endpoint access for a cluster at any time\.

## Modifying cluster endpoint access<a name="modify-endpoint-access"></a>

Use the procedures in this section to modify the endpoint access for an existing cluster\. The following table shows the supported API server endpoint access combinations and their associated behavior\.

**API server endpoint access options**
+ This is the default behavior for new Amazon EKS clusters\.
+  Kubernetes API requests that originate from within your cluster’s VPC \(such as node to control plane communication\) leave the VPC but not Amazon’s network\.
+ Your cluster API server is accessible from the internet\. You can, optionally, limit the CIDR blocks that can access the public endpoint\. If you limit access to specific CIDR blocks, then it is recommended that you also enable the private endpoint, or ensure that the CIDR blocks that you specify include the addresses that nodes and Fargate Pods \(if you use them\) access the public endpoint from\.
+  Kubernetes API requests within your cluster’s VPC \(such as node to control plane communication\) use the private VPC endpoint\.
+ Your cluster API server is accessible from the internet\. You can, optionally, limit the CIDR blocks that can access the public endpoint\.
+ All traffic to your cluster API server must come from within your cluster’s VPC or a [connected network](https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/introduction.html)\.
+ The cluster’s API server endpoint is resolved by public DNS servers to a private IP address from the VPC\. In the past, the endpoint could only be resolved from within the VPC\.

  If your endpoint does not resolve to a private IP address within the VPC for an existing cluster, you can:
  + Enable public access and then disable it again\. You only need to do so once for a cluster and the endpoint will resolve to a private IP address from that point forward\.

You can modify your cluster API server endpoint access using the AWS Management Console or AWS CLI\.

 AWS Management Console  

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the name of the cluster to display your cluster information\.

1. Choose the **Networking** tab and choose **Update**\.

1. For **Private access**, choose whether to enable or disable private access for your cluster’s Kubernetes API server endpoint\. If you enable private access, Kubernetes API requests that originate from within your cluster’s VPC use the private VPC endpoint\. You must enable private access to disable public access\.

1. For **Public access**, choose whether to enable or disable public access for your cluster’s Kubernetes API server endpoint\. If you disable public access, your cluster’s Kubernetes API server can only receive requests from within the cluster VPC\.

1. Choose **Update** to finish\.

 AWS CLI  
Complete the following steps using the AWS CLI version `1.27.160` or later\. You can check your current version with `aws --version`\. To install or upgrade the AWS CLI, see [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)\.

\+ NOTE: The following command enables private access and public access from a single IP address for the API server endpoint\. Replace ` 203.0.113.5/32 ` with a single CIDR block, or a comma\-separated list of CIDR blocks that you want to restrict network access to\.

\+

```
aws eks update-cluster-config \
    --region region-code \
    --name my-cluster \
    --resources-vpc-config endpointPublicAccess=true,publicAccessCidrs="203.0.113.5/32",endpointPrivateAccess=true
```

\+

An example output is as follows\.

\+

```
{
    "update": {
        "id": "e6f0905f-a5d4-4a2a-8c49-EXAMPLE00000",
        "status": "InProgress",
        "type": "EndpointAccessUpdate",
        "params": [
            {
                "type": "EndpointPublicAccess",
                "value": "true"
            },
            {
                "type": "EndpointPrivateAccess",
                "value": "true"
            },
            {
                "type": "publicAccessCidrs",
                "value": "[\203.0.113.5/32\"]"
            }
        ],
        "createdAt": 1576874258.137,
        "errors": []
    }
}
```

1. Monitor the status of your endpoint access update with the following command, using the cluster name and update ID that was returned by the previous command\. Your update is complete when the status is shown as `Successful`\.

   ```
   aws eks describe-update \
       --region region-code \
       --name my-cluster \
       --update-id e6f0905f-a5d4-4a2a-8c49-EXAMPLE00000
   ```

   An example output is as follows\.

   ```
   {
       "update": {
           "id": "e6f0905f-a5d4-4a2a-8c49-EXAMPLE00000",
           "status": "Successful",
           "type": "EndpointAccessUpdate",
           "params": [
               {
                   "type": "EndpointPublicAccess",
                   "value": "true"
               },
               {
                   "type": "EndpointPrivateAccess",
                   "value": "true"
               },
               {
                   "type": "publicAccessCidrs",
                   "value": "[\203.0.113.5/32\"]"
               }
           ],
           "createdAt": 1576874258.137,
           "errors": []
       }
   }
   ```

## Accessing a private only API server<a name="private-access"></a>

If you have disabled public access for your cluster’s Kubernetes API server endpoint, you can only access the API server from within your VPC or a [connected network](https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/introduction.html)\. Here are a few possible ways to access the Kubernetes API server endpoint:

Connected network  
+ Connect your network to the VPC with an [AWS transit gateway](https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html) or other [connectivity](https://docs.aws.amazon.com/aws-technical-content/latest/aws-vpc-connectivity-options/introduction.html) option and then use a computer in the connected network\. You must ensure that your Amazon EKS control plane security group contains rules to allow ingress traffic on port 443 from your connected network\.

Amazon EC2 bastion host AWS Cloud9 IDE  