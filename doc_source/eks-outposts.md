# Amazon EKS on AWS Outposts<a name="eks-outposts"></a>

You can use Amazon EKS to run on\-premises Kubernetes applications on AWS Outposts\. You can deploy Amazon EKS on Outposts in the following ways:
+ **Extended clusters** – Run the Kubernetes control plane in an AWS Region and nodes on your Outpost\.
+ **Local clusters** – Run the Kubernetes control plane and nodes on your Outpost\.

For both deployment options, the Kubernetes control plane is fully managed by AWS\. You can use the same Amazon EKS APIs, tools, and console that you use in the cloud to create and run Amazon EKS on Outposts\.

The following diagram shows these deployment options\.

![\[Outpost deployment options\]](http://docs.aws.amazon.com/eks/latest/userguide/images/outposts-deployment-options.png)

## When to use each deployment option<a name="outposts-overview-when-deployment-options"></a>

Both local and extended clusters are general\-purpose deployment options and can be used for a range of applications\. 

With local clusters, you can run the entire Amazon EKS cluster locally on Outposts\. This option can mitigate the risk of application downtime that might result from temporary network disconnects to the cloud\. These network disconnects can be caused by fiber cuts or weather events\. Because the entire Amazon EKS cluster runs locally on Outposts, applications remain available\. You can perform cluster operations during network disconnects to the cloud\. For more information, see [Preparing for network disconnects](eks-outposts-network-disconnects.md)\. If you're concerned about the quality of the network connection from your Outposts to the parent AWS Region and require high availability through network disconnects, use the local cluster deployment option\.

With extended clusters, you can conserve capacity on your Outpost because the Kubernetes control plane runs in the parent AWS Region\. This option is suitable if you can invest in reliable, redundant network connectivity from your Outpost to the AWS Region\. The quality of the network connection is critical for this option\. The way that Kubernetes handles network disconnects between the Kubernetes control plane and nodes might lead to application downtime\. For more information on the behavior of Kubernetes, see [Scheduling, Preemption, and Eviction](https://kubernetes.io/docs/concepts/scheduling-eviction/) in the Kubernetes documentation\.

## Comparing the deployment options<a name="outposts-overview-comparing-deployment-options"></a>

The following table compares the differences between the two options\.


| Feature | Extended cluster | Local cluster | 
| --- | --- | --- | 
|  Kubernetes control plane location  | AWS Region | Outpost | 
|  Kubernetes control plane account  | AWS account | Your account | 
| Regional availability | See [Service endpoints](https://docs.aws.amazon.com/general/latest/gr/eks.html#eks_region) | US East \(Ohio\), US East \(N\. Virginia\), US West \(N\. California\), US West \(Oregon\), Asia Pacific \(Seoul\), Asia Pacific \(Singapore\), Asia Pacific \(Sydney\), Asia Pacific \(Tokyo\), Canada \(Central\), Europe \(Frankfurt\), Europe \(Ireland\), Europe \(London\), Middle East \(Bahrain\), and South America \(São Paulo\) | 
| Kubernetes minor versions |  [Supported Amazon EKS versions](kubernetes-versions.md)\. | [Supported Amazon EKS versions](kubernetes-versions.md)\. | 
| Platform versions | See [Amazon EKS platform versions](platform-versions.md) | See [Amazon EKS local cluster platform versions](eks-outposts-platform-versions.md) | 
| Outpost form factors | Outpost racks | Outpost racks | 
| User interfaces | AWS Management Console, AWS CLI, Amazon EKS API, `eksctl`, AWS CloudFormation, and Terraform | AWS Management Console, AWS CLI, Amazon EKS API, eksctl, AWS CloudFormation, and Terraform | 
| Managed policies | [AmazonEKSClusterPolicy](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonEKSClusterPolicy) and [AmazonEKSServiceRolePolicy](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonEKSServiceRolePolicy) | [AmazonEKSLocalOutpostClusterPolicy](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonEKSLocalOutpostClusterPolicy) and [AmazonEKSLocalOutpostServiceRolePolicy](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonEKSLocalOutpostServiceRolePolicy) | 
| Cluster VPC and subnets | See [Amazon EKS VPC and subnet requirements and considerations](network_reqs.md) | See [Amazon EKS local cluster VPC and subnet requirements and considerations](eks-outposts-vpc-subnet-requirements.md) | 
| Cluster endpoint access | Public or private or both | Private only | 
| Kubernetes API server authentication | AWS Identity and Access Management \(IAM\) and OIDC | IAM and `x.509` certificates | 
| Node types | Self\-managed only | Self\-managed only | 
| Node compute types | Amazon EC2 on\-demand | Amazon EC2 on\-demand | 
| Node storage types | Amazon EBS `gp2` and local NVMe SSD | Amazon EBS `gp2` and local NVMe SSD | 
| Amazon EKS optimized AMIs | Amazon Linux, Windows, and Bottlerocket | Amazon Linux only | 
| IP versions | `IPv4` only | `IPv4` only | 
| Add\-ons | Amazon EKS add\-ons or self\-managed add\-ons | Self\-managed add\-ons only | 
| Default Container Network Interface | Amazon VPC CNI plugin for Kubernetes | Amazon VPC CNI plugin for Kubernetes | 
| Kubernetes control plane logs | Amazon CloudWatch Logs |  Amazon CloudWatch Logs  | 
| Load balancing | Use the [AWS Load Balancer Controller](aws-load-balancer-controller.md) to provision Application Load Balancers only \(no Network Load Balancers\) | Use the [AWS Load Balancer Controller](aws-load-balancer-controller.md) to provision Application Load Balancers only \(no Network Load Balancers\) | 
| Secrets envelope encryption | See [Enabling secret encryption on an existing cluster](enable-kms.md) | Not supported | 
| IAM roles for service accounts | See [IAM roles for service accounts](iam-roles-for-service-accounts.md) | Not supported | 
| Troubleshooting | See [Amazon EKS troubleshooting](troubleshooting.md) | See [Troubleshooting local clusters for Amazon EKS on AWS Outposts](eks-outposts-troubleshooting.md) | 

**Topics**