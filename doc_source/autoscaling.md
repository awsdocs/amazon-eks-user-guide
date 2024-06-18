# Autoscaling<a name="autoscaling"></a>

Autoscaling is a function that automatically scales your resources out and in to meet changing demands\. This is a major Kubernetes function that would otherwise require extensive human resources to perform manually\.

Amazon EKS supports two autoscaling products:

**Karpenter**  
Karpenter is a flexible, high\-performance Kubernetes cluster autoscaler that helps improve application availability and cluster efficiency\. Karpenter launches right\-sized compute resources \(for example, Amazon EC2 instances\) in response to changing application load in under a minute\. Through integrating Kubernetes with AWS, Karpenter can provision just\-in\-time compute resources that precisely meet the requirements of your workload\. Karpenter automatically provisions new compute resources based on the specific requirements of cluster workloads\. These include compute, storage, acceleration, and scheduling requirements\. Amazon EKS supports clusters using Karpenter, although Karpenter works with any conformant Kubernetes cluster\. For more information, see the [https://karpenter.sh/docs/](https://karpenter.sh/docs/) documentation\.

**Cluster Autoscaler**  
The Kubernetes Cluster Autoscaler automatically adjusts the number of nodes in your cluster when pods fail or are rescheduled onto other nodes\. The Cluster Autoscaler uses Auto Scaling groups\. For more information, see [Cluster Autoscaler on AWS](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/cloudprovider/aws/README.md)\.