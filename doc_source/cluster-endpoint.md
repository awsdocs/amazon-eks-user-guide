# Amazon EKS Cluster Endpoint Access Control<a name="cluster-endpoint"></a>

This topic helps you to enable private access for your Amazon EKS cluster's Kubernetes API server endpoint and completely disable public access so that it's not accessible from the internet\.

When you create a new cluster, Amazon EKS creates an endpoint for the managed Kubernetes API server that you use to communicate with your cluster \(using Kubernetes management tools such as `kubectl`\)\. By default, this API server endpoint is public to the internet, and access to the API server is secured using a combination of AWS Identity and Access Management \(IAM\) and native Kubernetes [Role Based Access Control](https://kubernetes.io/docs/admin/authorization/rbac/) \(RBAC\)\.

You can enable private access to the Kubernetes API server so that all communication between your worker nodes and the API server stays within your VPC\. You can also completely disable public access to your API server so that it's not accessible from the internet\.

**Note**  
Because this endpoint is for the Kubernetes API server and not a traditional AWS PrivateLink endpoint for communicating with an AWS API, it doesn't appear as an endpoint in the Amazon VPC console\.

When you enable endpoint private access for your cluster, Amazon EKS creates a Route 53 private hosted zone on your behalf and associates it with your cluster's VPC\. This private hosted zone is managed by Amazon EKS, and it doesn't appear in your account's Route 53 resources\. In order for the private hosted zone to properly route traffic to your API server, your VPC must have `enableDnsHostnames` and `enableDnsSupport` set to `true`, and the DHCP options set for your VPC must include `AmazonProvidedDNS` in its domain name servers list\. For more information, see [Updating DNS Support for Your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns.html#vpc-dns-updating) in the *Amazon VPC User Guide*\.

**Note**  
In addition to standard Amazon EKS permissions, your IAM user or role must have `route53:AssociateVPCWithHostedZone` permissions to enable the cluster's endpoint private access\.

You can define your API server endpoint access requirements when you create a new cluster, and you can update the API server endpoint access for a cluster at any time\. 

## Modifying Cluster Endpoint Access<a name="modify-endpoint-access"></a>

Use the procedures in this section to modify the endpoint access for an existing cluster\. The following table shows the supported API server endpoint access combinations and their associated behavior\.


**API server endpoint access options**  

| Endpoint Public Access | Endpoint Private Access | Behavior | 
| --- | --- | --- | 
| Enabled | Disabled |  [\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html)  | 
| Enabled | Enabled |  [\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html)  | 
| Disabled | Enabled |  [\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html)  | 

**To modify your cluster API server endpoint access with the console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the name of the cluster to display your cluster information\.

1. Under **Networking**, choose **Update**\.

1. For **Endpoint private access**, choose whether to enable or disable private access for your cluster's Kubernetes API server endpoint\. If you enable private access, Kubernetes API requests that originate from within your cluster's VPC use the private VPC endpoint\. You must enable private access to disable public access\.

1. For **Endpoint public access**, choose whether to enable or disable public access for your cluster's Kubernetes API server endpoint\. If you disable public access, your cluster's Kubernetes API server can only receive requests from within the cluster VPC\. 

1. Choose **Update** to finish\.

**To modify your cluster API server endpoint access with the AWS CLI**

1. Update your cluster API server endpoint access with the following AWS CLI command\. Substitute your cluster name and desired endpoint access values\.
**Note**  
The following command enables private access for the API server endpoint and completely disables public access\.

   ```
   aws eks --region region update-cluster-config --name dev --resources-vpc-config endpointPublicAccess=false,endpointPrivateAccess=true
   ```

   Output:

   ```
   {
       "update": {
           "id": "70e7ad6d-8de4-4ed3-9040-1ced27f8c332",
           "status": "InProgress",
           "type": "EndpointAccessUpdate",
           "params": [
               {
                   "type": "EndpointPublicAccess",
                   "value": "false"
               },
               {
                   "type": "EndpointPrivateAccess",
                   "value": "true"
               }
           ],
           "createdAt": 1551817408.563,
           "errors": []
       }
   }
   ```

1. Monitor the status of your endpoint access update with the following command, using the cluster name and update ID that was returned by the previous command\. Your update is complete when the status is shown as `Successful`\.

   ```
   aws eks --region region describe-update --name dev --update-id 70e7ad6d-8de4-4ed3-9040-1ced27f8c332
   ```

   Output:

   ```
   {
       "update": {
           "id": "70e7ad6d-8de4-4ed3-9040-1ced27f8c332",
           "status": "Successful",
           "type": "EndpointAccessUpdate",
           "params": [
               {
                   "type": "EndpointPublicAccess",
                   "value": "false"
               },
               {
                   "type": "EndpointPrivateAccess",
                   "value": "true"
               }
           ],
           "createdAt": 1551817408.563,
           "errors": []
       }
   }
   ```

## Accessing a Private Only API Server<a name="private-access"></a>

If you have disabled public access for your cluster's Kubernetes API server endpoint, you can only access the API server from within your VPC or a [connected network](https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/introduction.html)\. Here are a few possible ways to access the Kubernetes API server endpoint:
+ **Connected network** – Connect your network to the VPC with an [AWS Transit Gateway](https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html) or other [connectivity](https://docs.aws.amazon.com/aws-technical-content/latest/aws-vpc-connectivity-options/introduction.html) option and then use a computer in the connected network\.
+ **Amazon EC2 bastion host** – You can launch an Amazon EC2 instance into a public subnet in your cluster's VPC and then log in via SSH into that instance to run `kubectl` commands\. For more information, see [Linux Bastion Hosts on AWS](https://aws.amazon.com/quickstart/architecture/linux-bastion/)\. You must ensure that your Amazon EKS control plane security group contains rules to allow ingress traffic on port 443 from your bastion host\. For more information, see [Amazon EKS Security Group Considerations](sec-group-reqs.md)\.

  When you configure `kubectl` for your bastion host, be sure to use AWS credentials that are already mapped to your cluster's RBAC configuration, or add the IAM user or role that your bastion will use to the RBAC configuration before you remove endpoint public access\. For more information, see [Managing Users or IAM Roles for your Cluster](add-user-role.md) and [Unauthorized or Access Denied \(`kubectl`\)](troubleshooting.md#unauthorized)\.
+ **AWS Cloud9 IDE** – AWS Cloud9 is a cloud\-based integrated development environment \(IDE\) that lets you write, run, and debug your code with just a browser\. You can create an AWS Cloud9 IDE in your cluster's VPC and use the IDE to communicate with your cluster\. For more information, see [Creating an Environment in AWS Cloud9](https://docs.aws.amazon.com/cloud9/latest/user-guide/create-environment.html)\. You must ensure that your Amazon EKS control plane security group contains rules to allow ingress traffic on port 443 from your IDE security group\. For more information, see [Amazon EKS Security Group Considerations](sec-group-reqs.md)\.

  When you configure `kubectl` for your AWS Cloud9 IDE, be sure to use AWS credentials that are already mapped to your cluster's RBAC configuration, or add the IAM user or role that your IDE will use to the RBAC configuration before you remove endpoint public access\. For more information, see [Managing Users or IAM Roles for your Cluster](add-user-role.md) and [Unauthorized or Access Denied \(`kubectl`\)](troubleshooting.md#unauthorized)\.