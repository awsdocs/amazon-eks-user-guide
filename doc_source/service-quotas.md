# Amazon EKS service quotas<a name="service-quotas"></a>

The following table provides the default quotas for Amazon EKS for an AWS account that can be changed\.  To request a quota increase, open the [AWS Support Center](https://console.aws.amazon.com/support/home#/) page, sign in if necessary, and choose **Create case**\. Choose **Service limit increase**\. Complete and submit the form\.


| Resource | Default quota | 
| --- | --- | 
| Maximum number of Amazon EKS clusters \(per Region, per account\) | 100 | 
| Maximum number of managed node groups per cluster | 30 | 
| Maximum number of nodes per managed node group | 100 | 
| Maximum number Fargate profiles per cluster | 10 | 
| Maximum number selectors per Fargate profile | 5 | 
| Maximum number of label pairs per Fargate profile selector | 100 | 
| Maximum number of concurrent Fargate pods \(per Region, per account\) | 100 | 
| Maximum number Fargate pod launches per second \(per Region, per account\) | 1, with temporary burst up to 10 | 

The following table provides quotas for Amazon EKS that cannot be changed\.


| Resource | Default quota | 
| --- | --- | 
| Maximum number of control plane security groups per cluster \(these are specified when you create the cluster\) | 4 | 
| Maximum number of public endpoint access CIDR ranges per cluster | 40 | 