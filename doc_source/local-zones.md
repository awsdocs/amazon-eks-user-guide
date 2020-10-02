# Amazon EKS on AWS Local Zones<a name="local-zones"></a>

An AWS Local Zone is an extension of an AWS Region in geographic proximity to your users\. Local Zones have their own connections to the internet and support AWS Direct Connect\. Resources created in a Local Zone can serve local users with low\-latency communications\. For more information, see [Local Zones](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-local-zones)\. 

Amazon EKS supports running certain infrastructure, including Amazon EC2 instances, Amazon EBS volumes, and Application Load Balancers from a Local Zone as part of your cluster\. There are several considerations when using Local Zone infrastructure as part of your Amazon EKS cluster\. 

**Kubernetes versions**  
Only Amazon EKS clusters running Kubernetes versions 1\.17 and later can use Local Zone compute resources\.

**Nodes**  
Amazon EKS does not support creating managed node groups in AWS Local Zones\. You must create self\-managed nodes using the Amazon EC2 API or AWS CloudFormation\. **Do not use eksctl to create your cluster or nodes in Local Zones**\. For details and options, follow the instructions in [Self\-managed nodes](worker.md)\.

**Network architecture**  
The Amazon EKS managed Kubernetes control plane always runs in the AWS Region\. The Amazon EKS managed Kubernetes control plane cannot run in the Local Zone\. Since Local Zones appear as a subnet within your VPC, Kubernetes sees your Local Zone resources as part of that subnet\. 

The Amazon EKS Kubernetes cluster communicates with the Amazon EC2 instances you run in the AWS Region or Local Zone using Amazon EKS managed [elastic network interfaces](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html)\. To learn more about Amazon EKS networking architecture, see [Amazon EKS networking](eks-networking.md)\.

Unlike regional subnets, Amazon EKS cannot place network interfaces into your Local Zone subnets\. This means that you must not specify Local Zone subnets when you create your cluster\. 

After the cluster is created, tag your Local Zone subnets with the Amazon EKS cluster name\. For more information, see [Subnet tagging requirement](network_reqs.md#vpc-subnet-tagging)\. You can then deploy self\-managed nodes to the Local Zone subnets and the nodes will be able to join your Amazon EKS cluster\.