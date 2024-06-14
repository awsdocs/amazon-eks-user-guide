# Infrastructure security in Amazon EKS<a name="infrastructure-security"></a>

As a managed service, Amazon Elastic Kubernetes Service is protected by AWS global network security\. For information about AWS security services and how AWS protects infrastructure, see [AWS Cloud Security](https://aws.amazon.com/security/)\. To design your AWS environment using the best practices for infrastructure security, see [Infrastructure Protection](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/infrastructure-protection.html) in *Security Pillar AWS Well‐Architected Framework*\.

You use AWS published API calls to access Amazon EKS through the network\. Clients must support the following:
+ Transport Layer Security \(TLS\)\. We require TLS 1\.2 and recommend TLS 1\.3\.
+ Cipher suites with perfect forward secrecy \(PFS\) such as DHE \(Ephemeral Diffie\-Hellman\) or ECDHE \(Elliptic Curve Ephemeral Diffie\-Hellman\)\. Most modern systems such as Java 7 and later support these modes\.

Additionally, requests must be signed by using an access key ID and a secret access key that is associated with an IAM principal\. Or you can use the [AWS Security Token Service](https://docs.aws.amazon.com/STS/latest/APIReference/Welcome.html) \(AWS STS\) to generate temporary security credentials to sign requests\.

When you create an Amazon EKS cluster, you specify the VPC subnets for your cluster to use\. Amazon EKS requires subnets in at least two Availability Zones\. We recommend a VPC with public and private subnets so that Kubernetes can create public load balancers in the public subnets that load balance traffic to Pods running on nodes that are in private subnets\.

For more information about VPC considerations, see [Amazon EKS VPC and subnet requirements and considerations](network_reqs.md)\.

If you create your VPC and node groups with the AWS CloudFormation templates provided in the [Getting started with Amazon EKS](getting-started.md) walkthrough, then your control plane and node security groups are configured with our recommended settings\.

For more information about security group considerations, see [Amazon EKS security group requirements and considerations](sec-group-reqs.md)\. 

When you create a new cluster, Amazon EKS creates an endpoint for the managed Kubernetes API server that you use to communicate with your cluster \(using Kubernetes management tools such as `kubectl`\)\. By default, this API server endpoint is public to the internet, and access to the API server is secured using a combination of AWS Identity and Access Management \(IAM\) and native Kubernetes [Role Based Access Control](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) \(RBAC\)\.

You can enable private access to the Kubernetes API server so that all communication between your nodes and the API server stays within your VPC\. You can limit the IP addresses that can access your API server from the internet, or completely disable internet access to the API server\.

For more information about modifying cluster endpoint access, see [Modifying cluster endpoint access](cluster-endpoint.md#modify-endpoint-access)\.

You can implement Kubernetes *network policies* with the Amazon VPC CNI or third\-party tools such as [Project Calico](https://docs.tigera.io/calico/latest/about/)\. For more information about using the Amazon VPC CNI for network policies, see [Configure your cluster for Kubernetes network policies](cni-network-policy.md)\. Project Calico is a third party open source project\. For more information, see the [Project Calico documentation](https://docs.tigera.io/calico/latest/getting-started/kubernetes/managed-public-cloud/eks/)\.