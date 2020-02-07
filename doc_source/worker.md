# Worker Nodes<a name="worker"></a>

Worker machines in Kubernetes are called nodes\. Amazon EKS worker nodes run in your AWS account and connect to your cluster's control plane via the cluster API server endpoint\. You deploy one or more worker nodes into a node group\. A node group is one or more Amazon EC2 instances that are deployed in an [Amazon EC2 Auto Scaling group](https://docs.aws.amazon.com/autoscaling/ec2/userguide/AutoScalingGroup.html)\. All instances in a node group must:
+ Be the same instance type
+ Be running the same Amazon Machine Image \(AMI\)
+ Use the same [Amazon EKS Worker Node IAM Role](worker_node_IAM_role.md)

A cluster can contain several node groups, and each node group can contain several worker nodes\. If you deploy [managed node groups](managed-node-groups.md), then there is a maximum number of nodes that can be in a node group and a maximum number of node groups that you can have within a cluster\. See [service quotas](service-quotas.md) for details\. With this information, you can determine how many node groups you may need in a cluster to meet your requirements\.

Amazon EKS worker nodes are standard Amazon EC2 instances, and you are billed for them based on normal EC2 prices\. For more information, see [Amazon EC2 Pricing](https://aws.amazon.com/ec2/pricing/)\.

Amazon EKS provides a specialized Amazon Machine Image \(AMI\) called the Amazon EKS\-optimized AMI\. This AMI is built on top of Amazon Linux 2, and is configured to serve as the base image for Amazon EKS worker nodes\. The AMI is configured to work with Amazon EKS out of the box, and it includes Docker, kubelet, and the AWS IAM Authenticator\. The AMI also contains a specialized [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) that allows it to discover and connect to your cluster's control plane automatically\.

**Note**  
You can track security or privacy events for Amazon Linux 2 at the [Amazon Linux Security Center](https://alas.aws.amazon.com/alas2.html) or subscribe to the associated [RSS feed](https://alas.aws.amazon.com/AL2/alas.rss)\. Security and privacy events include an overview of the issue, what packages are affected, and how to update your instances to correct the issue\.

Beginning with Kubernetes version 1\.14 and [platform version](platform-versions.md) `eks.3`, Amazon EKS clusters support [Managed Node Groups](managed-node-groups.md), which automate the provisioning and lifecycle management of nodes\. Earlier versions of Amazon EKS clusters can launch worker nodes with an Amazon EKS\-provided AWS CloudFormation template\.

If you restrict access to your cluster's public endpoint using CIDR blocks, it is recommended that you also enable private endpoint access so that worker nodes can communicate with the cluster\. Without the private endpoint enabled, the CIDR blocks that you specify for public access must include the egress sources from your VPC\. For more information, see [Amazon EKS Cluster Endpoint Access Control](cluster-endpoint.md)\. 

To add worker nodes to your Amazon EKS cluster, see [Launching Amazon EKS Linux Worker Nodes](launch-workers.md)\. If you follow the steps in the guide, the required tag is added to the worker node for you\. If you launch workers manually, you must add the following tag to each worker node\. For more information, see [Adding and Deleting Tags on an Individual Resource](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Using_Tags.html#adding-or-deleting-tags)\.


| Key | Value | 
| --- | --- | 
|  `kubernetes.io/cluster/<cluster-name>`  |  `owned`  | 

For more information about worker nodes from a general Kubernetes perspective, see [Nodes](https://kubernetes.io/docs/concepts/architecture/nodes/) in the Kubernetes documentation\.

**Topics**
+ [Amazon EKS\-Optimized Linux AMI](eks-optimized-ami.md)
+ [Amazon EKS\-Optimized Windows AMI](eks-optimized-windows-ami.md)
+ [Managed Node Groups](managed-node-groups.md)
+ [Launching Amazon EKS Linux Worker Nodes](launch-workers.md)
+ [Launching Amazon EKS Windows Worker Nodes](launch-windows-workers.md)
+ [Worker Node Updates](update-workers.md)
+ [Ubuntu Amazon EKS\-Optimized AMIs](eks-partner-amis.md)