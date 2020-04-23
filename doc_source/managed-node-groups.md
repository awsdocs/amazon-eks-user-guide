# Managed node groups<a name="managed-node-groups"></a>

Amazon EKS managed node groups automate the provisioning and lifecycle management of nodes \(Amazon EC2 instances\) for Amazon EKS Kubernetes clusters\.

**Note**  
[Managed node groups](#managed-node-groups) are supported on Amazon EKS clusters beginning with Kubernetes version 1\.14 and [platform version](platform-versions.md) `eks.3`\. Existing clusters can update to version 1\.14 or later to take advantage of this feature\. For more information, see [Updating an Amazon EKS cluster Kubernetes version](update-cluster.md)\.

With Amazon EKS managed node groups, you don’t need to separately provision or register the Amazon EC2 instances that provide compute capacity to run your Kubernetes applications\. You can create, update, or terminate nodes for your cluster with a single operation\. Nodes run using the latest Amazon EKS\-optimized AMIs in your AWS account while node updates and terminations gracefully drain nodes to ensure that your applications stay available\.

All managed nodes are provisioned as part of an Amazon EC2 Auto Scaling group that is managed for you by Amazon EKS\. All resources including the instances and Auto Scaling groups run within your AWS account\. Each node group uses the Amazon EKS\-optimized Amazon Linux 2 AMI and can run across multiple Availability Zones that you define\.

You can add a managed node group to new or existing clusters using the Amazon EKS console, `eksctl`, AWS CLI, AWS API, or infrastructure as code tools including AWS CloudFormation\. Nodes launched as part of a managed node group are automatically tagged for auto\-discovery by the Kubernetes cluster autoscaler and you can use the node group to apply Kubernetes labels to nodes and update them at any time\.

There are no additional costs to use Amazon EKS managed node groups, you only pay for the AWS resources you provision\. These include Amazon EC2 instances, Amazon EBS volumes, Amazon EKS cluster hours, and any other AWS infrastructure\. There are no minimum fees and no upfront commitments\.

To get started with a new Amazon EKS cluster and managed node group, see [Getting started with the AWS Management Console](getting-started-console.md)\.

To add a managed node group to an existing cluster, see [Creating a managed node group](create-managed-node-group.md)\.

## Managed node groups concepts<a name="managed-node-group-concepts"></a>
+ Amazon EKS managed node groups create and manage Amazon EC2 instances for you\.
+ All managed nodes are provisioned as part of an Amazon EC2 Auto Scaling group that is managed for you by Amazon EKS and all resources including Amazon EC2 instances and Auto Scaling groups run within your AWS account\.
+ A managed node group's Auto Scaling group spans all of the subnets that you specify when you create the group\.
+ Amazon EKS tags managed node group resources so that they are configured to use the Kubernetes [Cluster Autoscaler](cluster-autoscaler.md)\.
**Important**  
If you are running a stateful application across multiple Availability Zones that is backed by Amazon EBS volumes and using the Kubernetes [Cluster Autoscaler](cluster-autoscaler.md), you should configure multiple node groups, each scoped to a single Availability Zone\. In addition, you should enable the `--balance-similar-node-groups` feature\.
+ Instances in a managed node group use the latest version of the Amazon EKS\-optimized Amazon Linux 2 AMI for its cluster's Kubernetes version\. You can choose between standard and GPU variants of the Amazon EKS\-optimized Amazon Linux 2 AMI\.
+ Amazon EKS follows the shared responsibility model for CVEs and security patches on managed node groups\. Because managed nodes run the Amazon EKS\-optimized AMIs, Amazon EKS is responsible for building patched versions of these AMIs when bugs or issues are reported and we are able to publish a fix\. However, you are responsible for deploying these patched AMI versions to your managed node groups\. When updates become available, see [Updating a managed node group](update-managed-node-group.md)\.
+ Amazon EKS managed node groups can be launched in both public and private subnets\. If you launch a managed node group in a public subnet on or after 04/22/2020, the subnet must have `MapPublicIpOnLaunch` set to true for the instances to be able to successfully join a cluster\. If the public subnet was created using `eksctl` or the [Amazon EKS\-vended AWS CloudFormation templates](create-public-private-vpc.md) on or after 03/26/2020, then this setting is already set to true\. If the public subnets were created before 03/26/2020, then you need to change the setting manually\. For more information, see [Modifying the public IPv4 addressing attribute for your subnet](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#subnet-public-ip)\.
+ You can create multiple managed node groups within a single cluster\. For example, you could create one node group with the standard Amazon EKS\-optimized Amazon Linux 2 AMI for some workloads and another with the GPU variant for workloads that require GPU support\. 
+ If your managed node group encounters a health issue, Amazon EKS returns an error message to help you to diagnose the issue\. For more information, see [Managed node group errors](troubleshooting.md#troubleshoot-managed-node-groups)\.
+ Amazon EKS adds Kubernetes labels to managed node group instances\. These Amazon EKS\-provided labels are prefixed with `eks.amazon.com`\.
+ Amazon EKS automatically drains nodes using the Kubernetes API during terminations or updates\. Updates respect the pod disruption budgets that you set for your pods\.
+ There are no additional costs to use Amazon EKS managed node groups, you only pay for the AWS resources you provision\.