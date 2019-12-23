# Load Balancing<a name="load-balancing"></a>

Amazon EKS supports the Network Load Balancer and the Classic Load Balancer for pods running on Amazon EC2 instance worker nodes through the Kubernetes service of type `LoadBalancer`\. Classic Load Balancers and Network Load Balancers are not supported for pods running on AWS Fargate \(Fargate\)\. For Fargate ingress, we recommend that you use the [ALB Ingress Controller](alb-ingress.md) on Amazon EKS \(minimum version v1\.1\.4\)\. 

The configuration of your load balancer is controlled by annotations that are added to the manifest for your service\. By default, Classic Load Balancers are used for `LoadBalancer` type services\. To use the Network Load Balancer instead, apply the following annotation to your service: 

```
service.beta.kubernetes.io/aws-load-balancer-type: nlb
```

For more information about using Network Load Balancer with Kubernetes, see [Network Load Balancer support on AWS](https://kubernetes.io/docs/concepts/services-networking/service/#aws-nlb-support) in the Kubernetes documentation\.

By default, services of type `LoadBalancer` create public\-facing load balancers\. To use an internal load balancer, apply the following annotation to your service: 

```
service.beta.kubernetes.io/aws-load-balancer-internal: 0.0.0.0/0
```

For internal load balancers, your Amazon EKS cluster must be configured to use at least one private subnet in your VPC\. Kubernetes examines the route table for your subnets to identify whether they are public or private\. Public subnets have a route directly to the internet using an internet gateway, but private subnets do not\. 

## Subnet Tagging for Load Balancers<a name="subnet-tagging-for-load-balancers"></a>

Public subnets in your VPC may be tagged accordingly so that Kubernetes knows to use only those subnets for external load balancers, instead of choosing a public subnet in each Availability Zone \(in lexicographical order by subnet ID\):


| Key | Value | 
| --- | --- | 
|  `kubernetes.io/role/elb`  |  `1`  | 

Private subnets in your VPC should be tagged accordingly so that Kubernetes knows that it can use them for internal load balancers:


| Key | Value | 
| --- | --- | 
|  `kubernetes.io/role/internal-elb`  |  `1`  | 