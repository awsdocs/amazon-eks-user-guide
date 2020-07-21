# Self\-managed nodes<a name="worker"></a>

Worker machines in Kubernetes are called nodes\. Amazon EKS nodes run in your AWS account and connect to your cluster's control plane via the cluster API server endpoint\. You deploy one or more nodes into a node group\. A node group is one or more Amazon EC2 instances that are deployed in an [Amazon EC2 Auto Scaling group](https://docs.aws.amazon.com/autoscaling/ec2/userguide/AutoScalingGroup.html)\. All instances in a node group must:
+ Be the same instance type
+ Be running the same Amazon Machine Image \(AMI\)
+ Use the same [Amazon EKS node IAM role](worker_node_IAM_role.md)

A cluster can contain several node groups, and each node group can contain several nodes\. 

Amazon EKS nodes are standard Amazon EC2 instances, and you are billed for them based on normal EC2 prices\. For more information, see [Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/)\.

Amazon EKS provides a specialized Amazon Machine Image \(AMI\) called the Amazon EKS\-optimized AMI\. This AMI is built on top of Amazon Linux 2, and is configured to serve as the base image for Amazon EKS nodes\. The AMI is configured to work with Amazon EKS out of the box, and it includes Docker, kubelet, and the AWS IAM Authenticator\. The AMI also contains a specialized [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) that allows it to discover and connect to your cluster's control plane automatically\.

**Note**  
You can track security or privacy events for Amazon Linux 2 at the [Amazon Linux security center](https://alas.aws.amazon.com/alas2.html) or subscribe to the associated [RSS feed](https://alas.aws.amazon.com/AL2/alas.rss)\. Security and privacy events include an overview of the issue, what packages are affected, and how to update your instances to correct the issue\.

If you restrict access to your cluster's public endpoint using CIDR blocks, it is recommended that you also enable private endpoint access so that nodes can communicate with the cluster\. Without the private endpoint enabled, the CIDR blocks that you specify for public access must include the egress sources from your VPC\. For more information, see [Amazon EKS cluster endpoint access control](cluster-endpoint.md)\. 

To add self\-managed nodes to your Amazon EKS cluster, see [Launching self\-managed Amazon Linux 2 Linux nodes](launch-workers.md)\. If you follow the steps in the guide, the required tag is added to the node for you\. If you launch self\-managed nodes manually, then you must add the following tag to each node\. For more information, see [Adding and deleting tags on an individual resource](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Using_Tags.html#adding-or-deleting-tags)\.


| Key | Value | 
| --- | --- | 
|  `kubernetes.io/cluster/<cluster-name>`  |  `owned`  | 

For more information about nodes from a general Kubernetes perspective, see [Nodes](https://kubernetes.io/docs/concepts/architecture/nodes/) in the Kubernetes documentation\.

**Topics**
+ [Launching self\-managed Amazon Linux 2 Linux nodes](launch-workers.md)
+ [Launching self\-managed Windows nodes](launch-windows-workers.md)
+ [Self\-managed node updates](update-workers.md)