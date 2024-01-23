# Self\-managed nodes<a name="worker"></a>

A cluster contains one or more Amazon EC2 nodes that Pods are scheduled on\. Amazon EKS nodes run in your AWS account and connect to the control plane of your cluster through the cluster API server endpoint\. You're billed for them based on Amazon EC2 prices\. For more information, see [Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/)\.

A cluster can contain several node groups\. Each node group contains one or more nodes that are deployed in an [Amazon EC2 Auto Scaling group](https://docs.aws.amazon.com/autoscaling/ec2/userguide/AutoScalingGroup.html)\. The instance type of the nodes within the group can vary, such as when using [attribute\-based instance type selection](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-fleet-attribute-based-instance-type-selection.html) with [https://karpenter.sh/](https://karpenter.sh/)\. All instances in a node group must use the [Amazon EKS node IAM role](create-node-role.md)\.

Amazon EKS provides specialized Amazon Machine Images \(AMIs\) that are called Amazon EKS optimized AMIs\. The AMIs are configured to work with Amazon EKS\. Their components include `containerd`, `kubelet`, and the AWS IAM Authenticator\. The AMIs also contain a specialized [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) that allows it to discover and connect to your cluster's control plane automatically\.

If you restrict access to the public endpoint of your cluster using CIDR blocks, we recommend that you also enable private endpoint access\. This is so that nodes can communicate with the cluster\. Without the private endpoint enabled, the CIDR blocks that you specify for public access must include the egress sources from your VPC\. For more information, see [Amazon EKS cluster endpoint access control](cluster-endpoint.md)\. 

To add self\-managed nodes to your Amazon EKS cluster, see the topics that follow\. If you launch self\-managed nodes manually, add the following tag to each node\. For more information, see [Adding and deleting tags on an individual resource](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Using_Tags.html#adding-or-deleting-tags)\. If you follow the steps in the guides that follow, the required tag is automatically added to nodes for you\. 


| Key | Value | 
| --- | --- | 
|  `kubernetes.io/cluster/my-cluster`  |  `owned`  | 

For more information about nodes from a general Kubernetes perspective, see [Nodes](https://kubernetes.io/docs/concepts/architecture/nodes/) in the Kubernetes documentation\.

**Topics**
+ [Launching self\-managed Amazon Linux nodes](launch-workers.md)
+ [Launching self\-managed Bottlerocket nodes](launch-node-bottlerocket.md)
+ [Launching self\-managed Windows nodes](launch-windows-workers.md)
+ [Self\-managed node updates](update-workers.md)