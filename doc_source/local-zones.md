--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Amazon EKS and AWS Local Zones<a name="local-zones"></a>

An AWS Local Zone is an extension of an AWS Region in geographic proximity to your users\. Local Zones have their own connections to the internet and support AWS Direct Connect\. Resources created in a Local Zone can serve local users with low\-latency communications\. For more information, see \{https\-\-\-docs\-aws\-amazon\-com\-AWSEC2\-latest\-UserGuide\-using\-regions\-availability\-zones\-html\-concepts\-local\-zones\}\[Local Zones\]\.

**Nodes**
+ The Amazon EKS managed Kubernetes control plane always runs in the AWS Region\. The Amazon EKS managed Kubernetes control plane can’t run in the Local Zone\. Because Local Zones appear as a subnet within your VPC, Kubernetes sees your Local Zone resources as part of that subnet\.
+ Unlike regional subnets, Amazon EKS can’t place network interfaces into your Local Zone subnets\. This means that you must not specify Local Zone subnets when you create your cluster\.