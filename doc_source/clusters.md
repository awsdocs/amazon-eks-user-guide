# Amazon EKS clusters<a name="clusters"></a>

An Amazon EKS cluster consists of two primary components:
+ The Amazon EKS control plane
+ Amazon EKS nodes that are registered with the control plane

The Amazon EKS control plane consists of control plane nodes that run the Kubernetes software, such as `etcd` and the Kubernetes API server\. The control plane runs in an account managed by AWS, and the Kubernetes API is exposed via the Amazon EKS endpoint associated with your cluster\. Each Amazon EKS cluster control plane is single\-tenant and unique, and runs on its own set of Amazon EC2 instances\.

All of the data stored by the `etcd` nodes and associated Amazon EBS volumes is encrypted using AWS KMS\. The cluster control plane is provisioned across multiple Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer\. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes \(for example, to support  `kubectl exec` `logs` `proxy` data flows\)\.

**Important**  
In the Amazon EKS environment, `etcd` storage is limited to 8 GiB as per [upstream](https://etcd.io/docs/v3.5/dev-guide/limit/#storage-size-limit) guidance\. You can monitor a metric for the current database size by running the following command\. If your cluster has a Kubernetes version below `1.28`, replace `apiserver_storage_size_bytes` with the following:  
Kubernetes version `1.27` and `1.26` – **`apiserver_storage_db_total_size_in_bytes`**
Kubernetes version `1.25` and below – **`etcd_db_total_size_in_bytes`**

```
kubectl get --raw=/metrics | grep "apiserver_storage_size_bytes"
```

Amazon EKS nodes run in your AWS account and connect to your cluster's control plane via the API server endpoint and a certificate file that is created for your cluster\.

**Note**  
You can find out how the different components of Amazon EKS work in [Amazon EKS networking](eks-networking.md)\. 
For connected clusters, see [Amazon EKS Connector](eks-connector.md)\.

**Topics**
+ [Creating an Amazon EKS cluster](create-cluster.md)
+ [Cluster insights](cluster-insights.md)
+ [Updating an Amazon EKS cluster Kubernetes version](update-cluster.md)
+ [Deleting an Amazon EKS cluster](delete-cluster.md)
+ [Amazon EKS cluster endpoint access control](cluster-endpoint.md)
+ [Enabling secret encryption on an existing cluster](enable-kms.md)
+ [Enabling Windows support for your Amazon EKS cluster](windows-support.md)
+ [Private cluster requirements](private-clusters.md)
+ [Amazon EKS Kubernetes versions](kubernetes-versions.md)
+ [Amazon EKS platform versions](platform-versions.md)
+ [Autoscaling](autoscaling.md)