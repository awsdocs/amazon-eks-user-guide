# Amazon EKS Service Quotas<a name="service-quotas"></a>

The following table provides the default quotas for Amazon EKS for an AWS account that can be changed\. For more information, see [AWS Service Quotas](https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html) in the *Amazon Web Services General Reference*\.


| Resource | Default Quota | 
| --- | --- | 
| Maximum number of Amazon EKS clusters \(per region, per account\) | 100 | 
| Maximum number of managed node groups per cluster | 10 | 
| Maximum number of nodes per managed node group | 100 | 
| Maximum number Fargate profiles per cluster | 10 | 
| Maximum number selectors per Fargate profile | 5 | 
| Maximum number of label pairs per Fargate profile selector | 100 | 
| Maximum number of concurrent Fargate pods \(per region, per account\) | 100 | 
| Maximum number Fargate pod launches per second \(per region, per account\) | 1, with temporary burst up to 10 | 

The following table provides quotas for Amazon EKS that cannot be changed\.


| Resource | Default Quota | 
| --- | --- | 
| Maximum number of control plane security groups per cluster \(these are specified when you create the cluster\) | 4 | 