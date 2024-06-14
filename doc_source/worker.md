--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Self\-managed nodes<a name="worker"></a>

A cluster contains one or more Amazon EC2 nodes that Pods are scheduled on\. Amazon EKS nodes run in your AWS account and connect to the control plane of your cluster through the cluster API server endpoint\. You’re billed for them based on Amazon EC2 prices\. For more information, see [Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/)\.

Amazon EKS provides specialized Amazon Machine Images \(AMIs\) that are called Amazon EKS optimized AMIs\. The AMIs are configured to work with Amazon EKS\. Their components include `containerd`, `kubelet`, and the AWS IAM Authenticator\. The AMIs also contain a specialized [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) that allows it to discover and connect to your cluster’s control plane automatically\.

To add self\-managed nodes to your Amazon EKS cluster, see the topics that follow\. If you launch self\-managed nodes manually, add the following tag to each node\. For more information, see \{https\-\-\-docs\-aws\-amazon\-com\-AWSEC2\-latest\-UserGuide\-Using\-Tags\-html\-adding\-or\-deleting\-tags\}\[Adding and deleting tags on an individual resource\]\. If you follow the steps in the guides that follow, the required tag is automatically added to nodes for you\.

 `kubernetes.io/cluster/my-cluster ` 

 `owned` 

For more information about nodes from a general Kubernetes perspective, see [Nodes](https://kubernetes.io/docs/concepts/architecture/nodes/) in the Kubernetes documentation\.

**Topics**
+ [Launching self\-managed Amazon Linux nodes](launch-workers.md)
+ [Launching self\-managed Bottlerocket nodes](launch-node-bottlerocket.md)
+ [Launching self\-managed Windows nodes](launch-windows-workers.md)
+ [Launching self\-managed Ubuntu nodes](launch-node-ubuntu.md)
+ [Self\-managed node updates](update-workers.md)