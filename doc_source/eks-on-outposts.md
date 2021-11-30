# Amazon EKS on AWS Outposts<a name="eks-on-outposts"></a>

You can create and run Amazon EKS nodes on AWS Outposts\. AWS Outposts enables native AWS services, infrastructure, and operating models in on\-premises facilities\. In AWS Outposts environments, you can use the same AWS APIs, tools, and infrastructure that you use in the AWS Cloud\. Amazon EKS nodes on AWS Outposts is ideal for low\-latency workloads that need to be run in close proximity to on\-premises data and applications\. For more information about AWS Outposts, see the [AWS Outposts User Guide](https://docs.aws.amazon.com/outposts/latest/userguide/)\.

## Prerequisites<a name="eks-outposts-prereq"></a>

 The following are the prerequisites for using Amazon EKS nodes on AWS Outposts:
+ You must have installed and configured an Outpost in your on\-premises data center\. For more information, see [Create an Outpost and order Outpost capacity](https://docs.aws.amazon.com/outposts/latest/userguide/order-outpost-capacity.html) in the AWS Outposts User Guide\.
+ You must have a reliable network connection between your Outpost and its AWS Region\. We recommend that you provide highly available and low\-latency connectivity between your Outpost and its AWS Region\. For more information, see [Outpost connectivity to the local network](https://docs.aws.amazon.com/outposts/latest/userguide/local-network-connectivity.html) in the AWS Outposts User Guide\. 
+ The AWS Region for the Outpost must support Amazon EKS\. For a list of supported Regions, see [Amazon EKS service endpoints](https://docs.aws.amazon.com/general/latest/gr/eks.html) in the *AWS General Reference*\.

## Outpost limits<a name="eks-outposts-limit"></a>
+ AWS Identity and Access Management, Network Load Balancer, Classic Load Balancer, and Amazon Route 53 run in the AWS Region, not on Outposts\. This increases latencies between the services and the containers\.
+ You can deploy self\-managed nodes to AWS Outposts, but not managed or Fargate nodes\. For more information, see [Launching self\-managed Amazon Linux nodes](launch-workers.md), [Launching self\-managed Bottlerocket nodes](launch-node-bottlerocket.md), or [Launching self\-managed Windows nodes](launch-windows-workers.md)\.
+ You can't pass Outposts subnets in when creating a cluster\. For more information, see [Creating an Amazon EKS cluster](create-cluster.md)\. 
+ You can't use AWS Outposts in China Regions\.

## Considerations<a name="eks-outposts-considerations"></a>
+ If network connectivity between your Outpost and its AWS Region is lost, your nodes will continue to run\. However, you cannot create new nodes or take new actions on existing deployments until connectivity is restored\. In case of instance failures, the instance will not be automatically replaced\. The Kubernetes control plane runs in the Region, and missing heartbeats caused by things like a loss of connectivity to the Availability Zone could lead to failures\. The failed heartbeats will lead to pods on the Outposts being marked as unhealthy, and eventually the node status will time out and pods will be marked for eviction\. For more information, see [Node Controller](https://kubernetes.io/docs/concepts/architecture/nodes/#node-controller) in the Kubernetes documentation\.