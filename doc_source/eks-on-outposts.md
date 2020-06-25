# Amazon EKS on AWS Outposts<a name="eks-on-outposts"></a>

Beginning with Kubernetes version 1\.14\.8 with Amazon EKS platform version `eks.5` and Kubernetes version 1\.13\.12 with Amazon EKS platform version `eks.6`, you can create and run Amazon EKS nodes on AWS Outposts\. AWS Outposts enables native AWS services, infrastructure, and operating models in on\-premises facilities\. In AWS Outposts environments, you can use the same AWS APIs, tools, and infrastructure that you use in the AWS Cloud\. Amazon EKS worker nodes on AWS Outposts is ideal for low\-latency workloads that need to be run in close proximity to on\-premises data and applications\. For more information about AWS Outposts, see the [AWS Outposts User Guide](https://docs.aws.amazon.com/outposts/latest/userguide/)\.

## Prerequisites<a name="eks-outposts-prereq"></a>

 The following are the prerequisites for using Amazon EKS worker nodes on AWS Outposts:
+ You must have installed and configured an Outpost in your on\-premises data center\.
+ You must have a reliable network connection between your Outpost and its AWS Region\.
+ The AWS Region for the Outpost must support Amazon EKS\. For a list of supported Regions, see [Amazon EKS service endpoints](https://docs.aws.amazon.com/general/latest/gr/eks.html) in the *AWS General Reference*\.

## Limitations<a name="eks-outposts-limit"></a>

The following are the limitations of using Amazon EKS on Outposts:
+ AWS Identity and Access Management, Application Load Balancer, Network Load Balancer, Classic Load Balancer, and Amazon Route 53 run in the AWS Region, not on Outposts\. This will increase latencies between the services and the containers\.
+ AWS Fargate is not available on AWS Outposts\.

## Network connectivity considerations<a name="eks-outposts-considerations"></a>

The following are network connectivity considerations for Amazon EKS AWS Outposts:
+ If network connectivity between your Outpost and its AWS Region is lost, your nodes will continue to run\. However, you cannot create new nodes or take new actions on existing deployments until connectivity is restored\. In case of instance failures, the instance will not be automatically replaced\. The Kubernetes control plane runs in the Region, and missing heartbeats caused by things like a loss of connectivity to the Availability Zone could lead to failures\. The failed heartbeats will lead to pods on the Outposts being marked as unhealthy, and eventually the node status will time out and pods will be marked for eviction\. For more information, see [Node Controller](https://kubernetes.io/docs/concepts/architecture/nodes/#node-controller) in the Kubernetes documentation\.
+ We recommend that you provide reliable, highly available, and low\-latency connectivity between your Outpost and its AWS Region\.

## Creating Amazon EKS nodes on an Outpost<a name="eks-outposts-create"></a>

Creating Amazon EKS nodes on an Outpost is similar to creating Amazon EKS nodes in the AWS Cloud\. When you create an Amazon EKS node on an Outpost, you must specify a subnet associated with your Outpost\.

An Outpost is an extension of an AWS Region, and you can extend a VPC in an account to span multiple Availability Zones and any associated Outpost locations\. When you configure your Outpost, you associate a subnet with it to extend your Regional VPC environment to your on\-premises facility\. Instances on an Outpost appear as part of your Regional VPC, similar to an Availability Zone with associated subnets\.

![\[Image NOT FOUND\]](http://docs.aws.amazon.com/eks/latest/userguide/images/network-components.png)

 To create Amazon EKS nodes on an Outpost with the AWS CLI, specify a security group and a subnet associated with your Outpost\.

**To create an Amazon EKS node group on an Outpost**

1. Create a VPC\.

   ```
   aws ec2 create-vpc --cidr-block 10.0.0.0/16
   ```

1. Create Outpost subnets\. The `--outpost-arn` parameter must be specified for the subnet to be created for the Outpost\. \(This step is different for AWS Outposts\.\)

   ```
   aws ec2 create-subnet --vpc-id vpc-xxxxxxxx --cidr-block 10.0.3.0/24 \
      –-outpost-arn  arn:aws:outposts:us-west-2:123456789012:outpost/op-xxxxxxxxxxxxxxxx
   ```

1. Create a cluster, specifying the subnets for the Outpost\. \(This step is different for AWS Outposts\.\)

   ```
   aws eks --region region-code create-cluster --name eks-outpost --role-arn \
      arn:aws:iam::123456789012:role/eks-service-role-AWSServiceRoleForAmazonEKS-OUTPOST \
      --resources-vpc-config  subnetIds=subnet-xxxxxxxx,subnet-yyyyyyyy,securityGroupIds=sg-xxxxxxxx
   ```

1. Create the node group\. Specify an instance type that is available on your Outpost\. \(This step is different for AWS Outposts\.\)

   ```
   eksctl create nodegroup --cluster eks-outpost \
          --version    auto \
          --name       outpost-workers \
          --node-type  c5.large \
          --node-ami   auto \
          --nodes      3 \
          --nodes-min  1 \
          --nodes-max  4
   ```

1. Deploy applications and services\.

   ```
   kubectl apply -f kubernetes/deployment.yaml
   ```