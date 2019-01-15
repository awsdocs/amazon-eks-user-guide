# Cluster VPC Considerations<a name="network_reqs"></a>

When you create an Amazon EKS cluster, you specify the Amazon VPC subnets for your cluster to use\. Amazon EKS requires subnets in at least two Availability Zones\. We recommend a network architecture that uses private subnets for your worker nodes and public subnets for Kubernetes to create internet\-facing load balancers within\. When you create your cluster, specify all of the subnets that will host resources for your cluster \(such as worker nodes and load balancers\)\.

**Note**  
Internet\-facing load balancers require a public subnet in your cluster\.

The subnets that you pass when you create the cluster influence where Amazon EKS places elastic network interfaces that are used for the control plane to worker node communication\.

It is possible to specify only public or private subnets when you create your cluster, but there are some limitations associated with these configurations:
+ **Private\-only**: Everything runs in a private subnet and Kubernetes cannot create internet\-facing load balancers for your pods without manually tagging resources\.
+ **Public\-only**: Everything runs in a public subnet, including your worker nodes\.

Amazon EKS creates an elastic network interface in your private subnets to facilitate communication to your worker nodes\. This communication channel supports Kubernetes functionality such as kubectl exec and kubectl logs\. The security group that you specify when you create your cluster is applied to the elastic network interfaces that are created for your cluster control plane\.

Your VPC must have DNS hostname and DNS resolution support\. Otherwise, your worker nodes cannot register with your cluster\. For more information, see [Using DNS with Your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns.html) in the *Amazon VPC User Guide*\.

## VPC Tagging Requirement<a name="vpc-tagging"></a>

When you create your Amazon EKS cluster, Amazon EKS tags the VPC containing the subnets you specify in the following way so that Kubernetes can discover it:


| Key | Value | 
| --- | --- | 
|  `kubernetes.io/cluster/<cluster-name>`  |  `shared`  | 
+ **Key**: The *<cluster\-name>* value matches your Amazon EKS cluster's name\. 
+ **Value**: The `shared` value allows more than one cluster to use this VPC\.

## Subnet Tagging Requirement<a name="vpc-subnet-tagging"></a>

When you create your Amazon EKS cluster, Amazon EKS tags the subnets you specify in the following way so that Kubernetes can discover them:


| Key | Value | 
| --- | --- | 
| `kubernetes.io/cluster/<cluster-name>` | `shared` | 
+ **Key**: The *<cluster\-name>* value matches your Amazon EKS cluster\. 
+ **Value**: The `shared` value allows more than one cluster to use this subnet\.

## Private Subnet Tagging Requirement for Internal Load Balancers<a name="vpc-private-subnet-tagging"></a>

Private subnets in your VPC should be tagged accordingly so that Kubernetes knows that it can use them for internal load balancers:


| Key | Value | 
| --- | --- | 
|  `kubernetes.io/role/internal-elb`  |  `1`  | 

## Public Facing Subnet Tagging for Load Balancers for nodes in Private Subnets <a name="vpc-private-node-public-load-balancers-tagging"></a>

When you create your Amazon EKS cluster, Amazon EKS tags the subnets you specify for your nodes. If you need to deploy your nodes in private subnets, but require public-facing Load Balancers for some of your services, you will need to manually tag your public subnets and verify that Elastic IP's, NAT Gateways, and Route Tables are set up correctly.

### Subnet Tagging

| Key | Value | 
| --- | --- | 
|  `kubernetes.io/cluster/<cluster-name>`  |  `shared`  | 
+ **Key**: The *<cluster\-name>* value matches your Amazon EKS cluster's name\. 
+ **Value**: The `shared` value allows more than one cluster to use this VPC\.


### Subnet Requirements Example

| Name | Availability Zone | Public/Private | Route Table |
| --- | --- | --- | --- |
| `Subnet-1` | `us-east-1a` | `Public`  | `RouteTable-Public` |
| `Subnet-2` | `us-east-1b` | `Public`  | `RouteTable-Public` |
| `Subnet-3` | `us-east-1a` | `Private` | `RouteTable-Private-1` |
| `Subnet-4` | `us-east-1b` | `Private` | `RouteTable-Private-2` |


The Public Subnets should have the (minimum) following resources created:
1. One Route Table.
2. One <a href="https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html">EIP</a> per Public Subnet.
3. One <a href="https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html">Internet Gateway (IGW)</a>.


The Private Subnets should have the (minimum) following resources created:
1. One Route Table per Private Subnet.
2. One <a href="https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html">NAT Gateway</a> per Private Subnet, associated with the EIP in the Public Subnet in the same Availability Zone as your private subnet.
3. One Subnet in each Availability Zone with a Public Subnet
