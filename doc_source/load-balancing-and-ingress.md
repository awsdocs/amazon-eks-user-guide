# Load balancing and ingress<a name="load-balancing-and-ingress"></a>

This chapter covers the following load balancing and ingress configuration options for Amazon EKS clusters:
+ [Load balancing](load-balancing.md) – Amazon EKS supports the AWS Network Load Balancer and the Classic Load Balancer for pods running on Amazon EC2 instance worker nodes through the Kubernetes `LoadBalancer` service type\.
+ [ALB Ingress Controller on Amazon EKS](alb-ingress.md) – The AWS ALB Ingress Controller for Kubernetes is a controller that triggers the creation of an AWS Application Load Balancer and the necessary supporting AWS resources whenever an ingress resource is created on a cluster with the `kubernetes.io/ingress.class: alb` annotation\. 