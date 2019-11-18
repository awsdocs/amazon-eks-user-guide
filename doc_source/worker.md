# Worker Nodes<a name="worker"></a>

Worker machines in Kubernetes are called nodes\. Amazon EKS worker nodes run in your AWS account and connect to your cluster's control plane via the cluster API server endpoint\.

Amazon EKS worker nodes are standard Amazon EC2 instances, and you are billed for them based on normal EC2 prices\. For more information, see [Amazon EC2 Pricing](https://aws.amazon.com/ec2/pricing/)\.

Amazon EKS provides a specialized Amazon Machine Image \(AMI\) called the Amazon EKS\-optimized AMI\. This AMI is built on top of Amazon Linux 2, and is configured to serve as the base image for Amazon EKS worker nodes\. The AMI is configured to work with Amazon EKS out of the box, and it includes Docker, kubelet, and the AWS IAM Authenticator\. The AMI also contains a specialized [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) that allows it to discover and connect to your cluster's control plane automatically\.

**Note**  
You can track security or privacy events for Amazon Linux 2 at the [Amazon Linux Security Center](https://alas.aws.amazon.com/alas2.html) or subscribe to the associated [RSS feed](https://alas.aws.amazon.com/AL2/alas.rss)\. Security and privacy events include an overview of the issue, what packages are affected, and how to update your instances to correct the issue\.

Beginning with Kubernetes version 1\.14 and [platform version](platform-versions.md) `eks.3`, Amazon EKS clusters support [Managed Node Groups](managed-node-groups.md), which automate the provisioning and lifecycle management of nodes\. Earlier versions of Amazon EKS clusters can launch worker nodes with an Amazon EKS\-provided AWS CloudFormation template\.

To add worker nodes to your Amazon EKS cluster, see [Launching Amazon EKS Linux Worker Nodes](launch-workers.md)\.

For more information about worker nodes from a general Kubernetes perspective, see [Nodes](https://kubernetes.io/docs/concepts/architecture/nodes/) in the Kubernetes documentation\.

**Topics**
+ [Amazon EKS\-Optimized Linux AMI](eks-optimized-ami.md)
+ [Amazon EKS\-Optimized Windows AMI](eks-optimized-windows-ami.md)
+ [Managed Node Groups](managed-node-groups.md)
+ [Launching Amazon EKS Linux Worker Nodes](launch-workers.md)
+ [Launching Amazon EKS Windows Worker Nodes](launch-windows-workers.md)
+ [Worker Node Updates](update-workers.md)
+ [Amazon EKS Partner AMIs](eks-partner-amis.md)