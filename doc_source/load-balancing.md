# Load Balancing<a name="load-balancing"></a>

Amazon EKS supports the Network Load Balancer and the Classic Load Balancer through the Kubernetes service of type `LoadBalancer`\. The configuration of your load balancer is controlled by annotations that are added to the manifest for your service\. 

By default, Classic Load Balancers are used for `LoadBalancer` type services\. To use the Network Load Balancer instead, apply the following annotation to your service: 

```
service.beta.kubernetes.io/aws-load-balancer-type: nlb
```

For internal load balancers, your Amazon EKS cluster must be configured to use at least one private subnet in your VPC\. Kubernetes examines the route table for your subnets to identify whether they are public or private\. Public subnets have a route directly to the internet using an internet gateway, but private subnets do not\. 

To use an internal load balancer, apply the following annotation to your service: 

```
service.beta.kubernetes.io/aws-load-balancer-internal: 0.0.0.0/0
```