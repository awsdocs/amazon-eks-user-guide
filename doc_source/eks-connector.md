--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Amazon EKS Connector<a name="eks-connector"></a>

The Amazon EKS Connector can connect the following types of Kubernetes clusters to Amazon EKS\.
+ On\-premises Kubernetes clusters
+ Self\-managed clusters that are running on Amazon EC2
+ Managed clusters from other cloud providers

## Amazon EKS Connector considerations<a name="connect-cluster-reqts"></a>

Before you use Amazon EKS Connector, understand the following:
+ You must have administrative privileges to the Kubernetes cluster to connect the cluster to Amazon EKS\.
+ The Kubernetes cluster must have Linux 64\-bit \(x86\) worker nodes present before connecting\. ARM worker nodes aren’t supported\.
+ You must have worker nodes in your Kubernetes cluster that have outbound access to the `ssm.` and `ssmmessages.` Systems Manager endpoints\. For more information, see [Systems Manager endpoints](https://docs.aws.amazon.com/general/latest/gr/ssm.html) in the * AWS General Reference*\.
+ By default, you can connect up to 10 clusters in a Region\. You can request an increase through the [service quota console](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html)\. See [Requesting a quota increase](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html) for more information\.
+ Only the Amazon EKS `RegisterCluster`, `ListClusters`, `DescribeCluster`, and `DeregisterCluster` APIs are supported for external Kubernetes clusters\.
+ You must have the following permissions to register a cluster:
  + eks:RegisterCluster
  + ssm:CreateActivation
  + ssm:DeleteActivation
  + iam:PassRole
+ You must have the following permissions to deregister a cluster:
  + eks:DeregisterCluster
  + ssm:DeleteActivation
  + ssm:DeregisterManagedInstance

## Required IAM roles for Amazon EKS Connector<a name="connector-iam-permissions"></a>

Using the Amazon EKS Connector requires the following two IAM roles: