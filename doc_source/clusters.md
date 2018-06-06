# Amazon EKS Clusters<a name="clusters"></a>

An Amazon EKS cluster consists of two primary components:
+ The Amazon EKS control plane
+ Amazon EKS worker nodes that are registered with the control plane

The Amazon EKS control plane consists of control plane nodes that run the Kubernetes software, like `etcd` and the Kubernetes API server\. The control plane runs in an account managed by AWS, and the Kubernetes API is exposed via the Amazon EKS endpoint associated with your cluster\.

Amazon EKS worker nodes run in your AWS account and connect to your cluster's control plane via the API server endpoint and a certificate file that is created for your cluster\.

The cluster control plane is provisioned across multiple Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer\. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the worker nodes \(for example, to support kubectl exec, logs, and proxy data flows\)\.

**Topics**
+ [Creating an Amazon EKS Cluster](create-cluster.md)
+ [Deleting a Cluster](delete-cluster.md)