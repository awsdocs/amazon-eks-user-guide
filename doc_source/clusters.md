# Amazon EKS Clusters<a name="clusters"></a>

An Amazon EKS cluster consists of two primary components:
+ The Amazon EKS control plane
+ Amazon EKS worker nodes that are registered with the control plane

The Amazon EKS control plane consists of control plane nodes that run the Kubernetes software, such as `etcd` and the Kubernetes API server\. The control plane runs in an account managed by AWS, and the Kubernetes API is exposed via the Amazon EKS endpoint associated with your cluster\. Each Amazon EKS cluster control plane is single\-tenant and unique, and runs on its own set of Amazon EC2 instances\.

All of the data stored by the `etcd` nodes and associated Amazon EBS volumes is encrypted\. Amazon EKS uses master encryption keys that generate volume encryption keys which are managed by the Amazon EKS service\.

The cluster control plane is provisioned across multiple Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer\. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the worker nodes \(for example, to support kubectl exec, logs, and proxy data flows\)\.

Amazon EKS worker nodes run in your AWS account and connect to your cluster's control plane via the API server endpoint and a certificate file that is created for your cluster\.