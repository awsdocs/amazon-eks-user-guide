# Self\-managed nodes<a name="worker"></a>

A cluster contains one or more Amazon EC2 nodes that pods are scheduled on\. Amazon EKS nodes run in your AWS account and connect to the control plane of your cluster through the cluster API server endpoint\. You deploy one or more nodes into a node group\. A node group is one or more Amazon EC2 instances that are deployed in an [Amazon EC2 Auto Scaling group](https://docs.aws.amazon.com/autoscaling/ec2/userguide/AutoScalingGroup.html)\. All instances in a node group must have the following characteristics:
+ Be the same instance type
+ Be running the same Amazon Machine Image \(AMI\)
+ Use the same [Amazon EKS node IAM role](create-node-role.md)

A cluster can contain several node groups\. If each node group meets the previous requirements, the cluster can contain node groups that contain different instance types and host operating systems\. Each node group can contain several nodes\.

Amazon EKS nodes are standard Amazon EC2 instances\. You're billed for them based on EC2 prices\. For more information, see [Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/)\.

Amazon EKS provides specialized Amazon Machine Images \(AMI\) that are called Amazon EKS optimized AMIs\. The AMIs are configured to work with Amazon EKS and include Docker,  `kubelet`  , and the AWS IAM Authenticator\. The AMIs also contain a specialized [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) that allows it to discover and connect to your cluster's control plane automatically\.

If you restrict access to the public endpoint of your cluster using CIDR blocks, we recommend that you also enable private endpoint access\. This is so that nodes can communicate with the cluster\. Without the private endpoint enabled, the CIDR blocks that you specify for public access must include the egress sources from your VPC\. For more information, see [Amazon EKS cluster endpoint access control](cluster-endpoint.md)\. 

To add self\-managed nodes to your Amazon EKS cluster, see the topics that follow\. If you launch self\-managed nodes manually, add the following tag to each node\. For more information, see [Adding and deleting tags on an individual resource](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Using_Tags.html#adding-or-deleting-tags)\. If you follow the steps in the guides that follow, the required tag is automatically added to nodes for you\. 


| Key | Value | 
| --- | --- | 
|  `kubernetes.io/cluster/<cluster-name>`  |  `owned`  | 

For more information about nodes from a general Kubernetes perspective, see [Nodes](https://kubernetes.io/docs/concepts/architecture/nodes/) in the Kubernetes documentation\.

**Topics**
+ [Launching self\-managed Amazon Linux nodes](launch-workers.md)
+ [Launching self\-managed Bottlerocket nodes](launch-node-bottlerocket.md)
+ [Launching self\-managed Windows nodes](launch-windows-workers.md)
+ [Self\-managed node updates](update-workers.md)