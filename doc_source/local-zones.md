# Amazon EKS and AWS Local Zones<a name="local-zones"></a>

An AWS Local Zone is an extension of an AWS Region in geographic proximity to your users\. Local Zones have their own connections to the internet and support AWS Direct Connect\. Resources created in a Local Zone can serve local users with low\-latency communications\. For more information, see [Local Zones](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-local-zones)\. 

Amazon EKS supports certain resources in Local Zones\. This includes [self\-managed Amazon EC2 nodes](worker.md), Amazon EBS volumes, and Application Load Balancers \(ALBs\)\. We recommend that you consider the following when using Local Zones as part of your Amazon EKS cluster\. 

**Nodes**  
You can't create managed node groups or Fargate nodes in Local Zones with Amazon EKS\. However, you can create self\-managed Amazon EC2 nodes in Local Zones using the Amazon EC2 API, AWS CloudFormation, or `eksctl`\. For more information, see [Self\-managed nodes](worker.md)\.

**Network architecture**
+ The Amazon EKS managed Kubernetes control plane always runs in the AWS Region\. The Amazon EKS managed Kubernetes control plane can't run in the Local Zone\. Because Local Zones appear as a subnet within your VPC, Kubernetes sees your Local Zone resources as part of that subnet\. 
+ The Amazon EKS Kubernetes cluster communicates with the Amazon EC2 instances you run in the AWS Region or Local Zone using Amazon EKS managed [elastic network interfaces](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html)\. To learn more about Amazon EKS networking architecture, see [Amazon EKS networking](eks-networking.md)\.
+ Unlike regional subnets, Amazon EKS can't place network interfaces into your Local Zone subnets\. This means that you must not specify Local Zone subnets when you create your cluster\.