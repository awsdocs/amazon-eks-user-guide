# Infrastructure security in Amazon EKS<a name="infrastructure-security"></a>

As a managed service, Amazon EKS is protected by the AWS global network security procedures that are described in the [Amazon Web Services: Overview of security processes](https://d0.awsstatic.com/whitepapers/Security/AWS_Security_Whitepaper.pdf) whitepaper\.

You use AWS published API calls to access Amazon EKS through the network\. Clients must support Transport Layer Security \(TLS\) 1\.2 or later\. Clients must also support cipher suites with perfect forward secrecy \(PFS\) such as Ephemeral Diffie\-Hellman \(DHE\) or Elliptic Curve Ephemeral Diffie\-Hellman \(ECDHE\)\. Most modern systems such as Java 7 and later support these modes\.

Additionally, requests must be signed by using an access key ID and a secret access key that is associated with an IAM principal\. Or you can use the [AWS Security Token Service](https://docs.aws.amazon.com/STS/latest/APIReference/Welcome.html) \(AWS STS\) to generate temporary security credentials to sign requests\.

When you create an Amazon EKS cluster, you specify the VPC subnets for your cluster to use\. Amazon EKS requires subnets in at least two Availability Zones\. We recommend a VPC with public and private subnets so that Kubernetes can create public load balancers in the public subnets that load balance traffic to pods running on worker nodes that are in private subnets\.

For more information about VPC considerations, see [Cluster VPC considerations](network_reqs.md)\.

If you create your VPC and worker node groups with the AWS CloudFormation templates provided in the [Getting started with Amazon EKS](getting-started.md) walkthrough, then your control plane and worker node security groups are configured with our recommended settings\.

For more information about security group considerations, see [Amazon EKS security group considerations](sec-group-reqs.md)\. 

When you create a new cluster, Amazon EKS creates an endpoint for the managed Kubernetes API server that you use to communicate with your cluster \(using Kubernetes management tools such as `kubectl`\)\. By default, this API server endpoint is public to the internet, and access to the API server is secured using a combination of AWS Identity and Access Management \(IAM\) and native Kubernetes [Role Based Access Control](https://kubernetes.io/docs/admin/authorization/rbac/) \(RBAC\)\.

You can enable private access to the Kubernetes API server so that all communication between your worker nodes and the API server stays within your VPC\. You can limit the IP addresses that can access your API server from the internet, or completely disable internet access to the API server\.

For more information about modifying cluster endpoint access, see [Modifying cluster endpoint access](cluster-endpoint.md#modify-endpoint-access)\.

You can implement network policies with tools such as [Project Calico](calico.md)\. Project Calico is a third party open source project\. For more information, see the [Project Calico documentation](https://docs.projectcalico.org/v3.7/introduction/)\.
