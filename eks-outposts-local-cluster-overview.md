# Local clusters for Amazon EKS on AWS Outposts<a name="eks-outposts-local-cluster-overview"></a>

You can use local clusters to run your entire Amazon EKS cluster locally on AWS Outposts\. This helps mitigate the risk of application downtime that might result from temporary network disconnects to the cloud\. These disconnects can be caused by fiber cuts or weather events\. Because the entire Kubernetes cluster runs locally on Outposts, applications remain available\. You can perform cluster operations during network disconnects to the cloud\. For more information, see [Preparing for network disconnects](eks-outposts-network-disconnects.md)\. The following diagram shows a local cluster deployment\.

![\[Outpost local cluster\]](http://docs.aws.amazon.com/eks/latest/userguide/images/outposts-local-cluster.png)

Local clusters are generally available for use with Outposts racks\.<a name="outposts-control-plane-supported-regions"></a>

**Supported AWS Regions**  
You can create local clusters in the following AWS Regions: US East \(Ohio\), US East \(N\. Virginia\), US West \(N\. California\), US West \(Oregon\), Asia Pacific \(Seoul\), Asia Pacific \(Singapore\), Asia Pacific \(Sydney\), Asia Pacific \(Tokyo\), Canada \(Central\), Europe \(Frankfurt\), Europe \(Ireland\), Europe \(London\), Middle East \(Bahrain\), and South America \(São Paulo\)\. For detailed information about supported features, see [Comparing the deployment options](eks-outposts.md#outposts-overview-comparing-deployment-options)\.

**Topics**
+ [Creating a local cluster on an Outpost](eks-outposts-local-cluster-create.md)
+ [Amazon EKS local cluster platform versions](eks-outposts-platform-versions.md)
+ [Amazon EKS local cluster VPC and subnet requirements and considerations](eks-outposts-vpc-subnet-requirements.md)
+ [Preparing for network disconnects](eks-outposts-network-disconnects.md)
+ [Capacity considerations](eks-outposts-capacity-considerations.md)
+ [Troubleshooting local clusters for Amazon EKS on AWS Outposts](eks-outposts-troubleshooting.md)