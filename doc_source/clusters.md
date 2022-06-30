# Amazon EKS clusters<a name="clusters"></a>

An Amazon EKS cluster consists of two primary components:
+ The Amazon EKS control plane
+ Amazon EKS nodes that are registered with the control plane

The Amazon EKS control plane consists of control plane nodes that run the Kubernetes software, such as `etcd` and the Kubernetes API server\. The control plane runs in an account managed by AWS, and the Kubernetes API is exposed via the Amazon EKS endpoint associated with your cluster\. Each Amazon EKS cluster control plane is single\-tenant and unique, and runs on its own set of Amazon EC2 instances\.

All of the data stored by the `etcd` nodes and associated Amazon EBS volumes is encrypted using AWS KMS\. The cluster control plane is provisioned across multiple Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer\. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes \(for example, to support  `kubectl exec` `logs` `proxy` data flows\)\.

**Important**  
In the Amazon EKS environment, `etcd` storage is limited to 8GB as per [upstream](https://etcd.io/docs/v3.5/dev-guide/limit/#storage-size-limit) guidance\. You can monitor the `etcd_db_total_size_in_bytes` metric for the current database size\.

Amazon EKS nodes run in your AWS account and connect to your cluster's control plane via the API server endpoint and a certificate file that is created for your cluster\.

**Note**  
You can find out how the different components of Amazon EKS work in [Amazon EKS networking](eks-networking.md)\. 
For connected clusters, see [Amazon EKS Connector](eks-connector.md)\.