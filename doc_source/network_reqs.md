# Cluster VPC Considerations<a name="network_reqs"></a>

When you create an Amazon EKS cluster, you specify the Amazon VPC subnets for your cluster to use\. Amazon EKS requires subnets in at least two Availability Zones\. We recommend a network architecture that uses private subnets for your worker nodes and public subnets for Kubernetes to create internet\-facing load balancers within\.

When you create your cluster, specify all of the subnets that will host resources for your cluster \(such as worker nodes and load balancers\)\. 

**Note**  
Internet\-facing load balancers require a public subnet in your cluster\. Worker nodes also require outbound internet access to the Amazon EKS APIs for cluster introspection and node registration at launch time\. To pull container images, they require access to the Amazon S3 and Amazon ECR APIs \(and any other container registries, such as DockerHub\)\. For more information, see [Amazon EKS Security Group Considerations](sec-group-reqs.md) and [AWS IP Address Ranges](https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html) in the *AWS General Reference*\.

The subnets that you pass when you create the cluster influence where Amazon EKS places elastic network interfaces that are used for the control plane to worker node communication\.

It is possible to specify only public or private subnets when you create your cluster, but there are some limitations associated with these configurations:
+ **Private\-only**: Everything runs in a private subnet and Kubernetes cannot create internet\-facing load balancers for your pods\.
+ **Public\-only**: Everything runs in a public subnet, including your worker nodes\.

Amazon EKS creates an elastic network interface in your private subnets to facilitate communication to your worker nodes\. This communication channel supports Kubernetes functionality such as kubectl exec and kubectl logs\. The security group that you specify when you create your cluster is applied to the elastic network interfaces that are created for your cluster control plane\.

Your VPC must have DNS hostname and DNS resolution support\. Otherwise, your worker nodes cannot register with your cluster\. For more information, see [Using DNS with Your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns.html) in the *Amazon VPC User Guide*\.

## VPC IP Addressing<a name="vpc-cidr"></a>

You can define both private \(RFC 1918\) and public \(non\-RFC 1918\) CIDR ranges within the VPC used for your Amazon EKS cluster\. For more information, see [VPCs and Subnets](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html) and [IP Addressing in Your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html) in the *Amazon VPC User Guide*\.

The Amazon EKS control plane creates up to 4 cross\-account elastic network interfaces in your VPC for each cluster\. Be sure that the subnets you specify have enough available IP addresses for the cross\-account elastic network interfaces and your pods\.

**Important**  
Docker runs in the `172.17.0.0/16` CIDR range in Amazon EKS clusters\. We recommend that your cluster's VPC subnets do not overlap this range\. Otherwise, you will receive the following error:  

```
Error: : error upgrading connection: error dialing backend: dial tcp 172.17.nn.nn:10250: getsockopt: no route to host
```

## VPC Tagging Requirement<a name="vpc-tagging"></a>

When you create your Amazon EKS cluster, Amazon EKS tags the VPC containing the subnets you specify in the following way so that Kubernetes can discover it:


| Key | Value | 
| --- | --- | 
|  `kubernetes.io/cluster/<cluster-name>`  |  `shared`  | 
+ **Key**: The *<cluster\-name>* value matches your Amazon EKS cluster's name\. 
+ **Value**: The `shared` value allows more than one cluster to use this VPC\.

## Subnet Tagging Requirement<a name="vpc-subnet-tagging"></a>

When you create your Amazon EKS cluster, Amazon EKS tags the subnets you specify in the following way so that Kubernetes can discover them:

**Note**  
All subnets \(public and private\) that your cluster uses for resources should have this tag\.


| Key | Value | 
| --- | --- | 
| `kubernetes.io/cluster/<cluster-name>` | `shared` | 
+ **Key**: The *<cluster\-name>* value matches your Amazon EKS cluster\. 
+ **Value**: The `shared` value allows more than one cluster to use this subnet\.

### Private Subnet Tagging Requirement for Internal Load Balancers<a name="vpc-private-subnet-tagging"></a>

Private subnets in your VPC should be tagged accordingly so that Kubernetes knows that it can use them for internal load balancers:


| Key | Value | 
| --- | --- | 
|  `kubernetes.io/role/internal-elb`  |  `1`  | 

### Public Subnet Tagging Option for External Load Balancers<a name="vpc-public-subnet-tagging"></a>

Public subnets in your VPC may be tagged accordingly so that Kubernetes knows to use only those subnets for external load balancers, instead of choosing a public subnet in each Availability Zone \(in lexicographical order by subnet ID\):


| Key | Value | 
| --- | --- | 
|  `kubernetes.io/role/elb`  |  `1`  | 