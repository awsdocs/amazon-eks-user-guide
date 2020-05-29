# Cluster VPC considerations<a name="network_reqs"></a>

When you create an Amazon EKS cluster, you specify the VPC subnets for your cluster to use\. Amazon EKS requires subnets in at least two Availability Zones\. We recommend a VPC with public and private subnets so that Kubernetes can create public load balancers in the public subnets that load balance traffic to pods running on worker nodes that are in private subnets\.

When you create your cluster, specify all of the subnets that will host resources for your cluster \(such as worker nodes and load balancers\)\. 

**Note**  
Internet\-facing load balancers require a public subnet in your cluster\. Worker nodes also require outbound internet access to the Amazon EKS APIs for cluster introspection and node registration at launch time\. To pull container images, they require access to the Amazon S3 and Amazon ECR APIs \(and any other container registries, such as DockerHub\)\. For more information, see [Amazon EKS security group considerations](sec-group-reqs.md) and [AWS IP Address Ranges](https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html) in the *AWS General Reference*\.

The subnets that you pass when you create the cluster influence where Amazon EKS places elastic network interfaces that are used for the control plane to worker node communication\.

It is possible to specify only public or private subnets when you create your cluster, but there are some limitations associated with these configurations:
+ **Private\-only**: Everything runs in a private subnet and Kubernetes cannot create internet\-facing load balancers for your pods\.
+ **Public\-only**: Everything runs in a public subnet, including your worker nodes\.

Amazon EKS creates an elastic network interface in your private subnets to facilitate communication to your worker nodes\. This communication channel supports Kubernetes functionality such as kubectl exec and kubectl logs\. The security group that you specify when you create your cluster is applied to the elastic network interfaces that are created for your cluster control plane\.

Your VPC must have DNS hostname and DNS resolution support\. Otherwise, your worker nodes cannot register with your cluster\. For more information, see [Using DNS with Your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns.html) in the *Amazon VPC User Guide*\.

## VPC IP addressing<a name="vpc-cidr"></a>

Your worker nodes must be able to access the internet using a public IP address to function properly\. If your worker nodes are deployed in a private subnet, then the subnet must have a default route to a [NAT gateway](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)\. The NAT gateway must be assigned a public IP address to provide internet access for the worker nodes\. If self\-managed worker nodes are deployed to a public subnet, then the subnet must be configured to auto\-assign public IP addresses or your worker node instances must be assigned a public IP address when they're [launched](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#vpc-public-ip)\. If managed worker nodes are deployed to a public subnet, then the subnet must be configured to auto\-assign public IP addresses or the worker nodes will not be assigned a public IP address\. Determine whether your public subnets are configured to auto\-assign public IP addresses with the following command\.

```
aws ec2 describe-subnets \
    --filters "Name=vpc-id,Values=VPC-ID" | grep 'SubnetId\|MapPublicIpOnLaunch'
```

Output

```
"MapPublicIpOnLaunch": false,
"SubnetId": "subnet-aaaaaaaaaaaaaaaaa",
"MapPublicIpOnLaunch": false,
"SubnetId": "subnet-bbbbbbbbbbbbbbbbb",
```

For any subnets that have `MapPublicIpOnLaunch` set to `false`, change the setting to `true`\.

```
aws ec2 modify-subnet-attribute --map-public-ip-on-launch --subnet-id subnet-aaaaaaaaaaaaaaaaa
```

**Important**  
If you used an [Amazon EKS AWS CloudFormation template](create-public-private-vpc.md) to deploy your VPC prior to 03/26/2020, then you need to change the setting for your public subnets\.

You can define both private \(RFC 1918\) and public \(non\-RFC 1918\) CIDR ranges within the VPC used for your Amazon EKS cluster\. For more information, see [VPCs and Subnets](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html) and [IP Addressing in Your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html) in the *Amazon VPC User Guide*\.

The Amazon EKS control plane creates up to 4 cross\-account elastic network interfaces in your VPC for each cluster\. Be sure that the subnets you specify have enough available IP addresses for the cross\-account elastic network interfaces and your pods\.

## VPC tagging requirement<a name="vpc-tagging"></a>

When you create an Amazon EKS cluster earlier than version 1\.15, Amazon EKS tags the VPC containing the subnets you specify in the following way so that Kubernetes can discover it:


| Key | Value | 
| --- | --- | 
|  `kubernetes.io/cluster/<cluster-name>`  |  `shared`  | 
+ **Key**: The *<cluster\-name>* value matches your Amazon EKS cluster's name\. 
+ **Value**: The `shared` value allows more than one cluster to use this VPC\.

This tag is not required or created by Amazon EKS for 1\.15 clusters\. If you deploy a 1\.15 cluster to a VPC that already has this tag, the tag is not removed\.

## Subnet tagging requirement<a name="vpc-subnet-tagging"></a>

When you create your Amazon EKS cluster, Amazon EKS tags the subnets you specify in the following way so that Kubernetes can discover them:

**Note**  
All subnets \(public and private\) that your cluster uses for resources should have this tag\.


| Key | Value | 
| --- | --- | 
| `kubernetes.io/cluster/<cluster-name>` | `shared` | 
+ **Key**: The *<cluster\-name>* value matches your Amazon EKS cluster\. 
+ **Value**: The `shared` value allows more than one cluster to use this subnet\.

### Private subnet tagging requirement for internal load balancers<a name="vpc-private-subnet-tagging"></a>

Private subnets must be tagged in the following way so that Kubernetes knows it can use the subnets for internal load balancers\. If you use an Amazon EKS AWS CloudFormation template to create your VPC after 03/26/2020, then the subnets created by the template are tagged when they're created\. For more information about the Amazon EKS AWS CloudFormation VPC templates, see [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md)\.


| Key | Value | 
| --- | --- | 
|  `kubernetes.io/role/internal-elb`  |  `1`  | 

### Public subnet tagging option for external load balancers<a name="vpc-public-subnet-tagging"></a>

You must tag the public subnets in your VPC so that Kubernetes knows to use only those subnets for external load balancers instead of choosing a public subnet in each Availability Zone \(in lexicographical order by subnet ID\)\. If you use an Amazon EKS AWS CloudFormation template to create your VPC after 03/26/2020, then the subnets created by the template are tagged when they're created\. For more information about the Amazon EKS AWS CloudFormation VPC templates, see [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md)\.


| Key | Value | 
| --- | --- | 
| `kubernetes.io/role/elb` | `1` | 