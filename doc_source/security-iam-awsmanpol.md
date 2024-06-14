--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# AWS managed policies for Amazon Elastic Kubernetes Service<a name="security-iam-awsmanpol"></a>

An AWS managed policy is a standalone policy that is created and administered by AWS\. AWS managed policies are designed to provide permissions for many common use cases so that you can start assigning permissions to users, groups, and roles\.

Keep in mind that AWS managed policies might not grant least\-privilege permissions for your specific use cases because they’re available for all AWS customers to use\. We recommend that you reduce permissions further by defining [customer managed policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html#customer-managed-policies) that are specific to your use cases\.

You cannot change the permissions defined in AWS managed policies\. If AWS updates the permissions defined in an AWS managed policy, the update affects all principal identities \(users, groups, and roles\) that the policy is attached to\. AWS is most likely to update an AWS managed policy when a new AWS service is launched or new API operations become available for existing services\.

For more information, see [AWS managed policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html#aws-managed-policies) in the *IAM User Guide*\.

## AWS managed policy: AmazonEKS\_CNI\_Policy<a name="security-iam-awsmanpol-amazoneks-cni-policy"></a>

 **Permissions details** 

This policy includes the following permissions that allow Amazon EKS to complete the following tasks:
+  ** `ec2:*NetworkInterface` and `ec2:*PrivateIpAddresses` ** – Allows the Amazon VPC CNI plugin to perform actions such as provisioning Elastic Network Interfaces and IP addresses for Pods to provide networking for applications that run in Amazon EKS\.
+  ** `ec2` read actions** – Allows the Amazon VPC CNI plugin to perform actions such as describe instances and subnets to see the amount of free IP addresses in your Amazon VPC subnets\. The VPC CNI can use the free IP addresses in each subnet to pick the subnets with the most free IP addresses to use when creating an elastic network interface\.

To view the latest version of the JSON policy document, see [AmazonEKS\_CNI\_Policy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKS_CNI_Policy.html#AmazonEKS_CNI_Policy-json) in the AWS Managed Policy Reference Guide\.

## AWS managed policy: AmazonEKSClusterPolicy<a name="security-iam-awsmanpol-amazoneksclusterpolicy"></a>

This policy includes the following permissions that allow Amazon EKS to complete the following tasks:
+  ** `autoscaling` ** – Read and update the configuration of an Auto Scaling group\. These permissions aren’t used by Amazon EKS but remain in the policy for backwards compatibility\.
+  ** `ec2` ** – Work with volumes and network resources that are associated to Amazon EC2 nodes\. This is required so that the Kubernetes control plane can join instances to a cluster and dynamically provision and manage Amazon EBS volumes that are requested by Kubernetes persistent volumes\.
+  ** `elasticloadbalancing` ** – Work with Elastic Load Balancers and add nodes to them as targets\. This is required so that the Kubernetes control plane can dynamically provision Elastic Load Balancers requested by Kubernetes services\.
+  ** `iam` ** – Create a service\-linked role\. This is required so that the Kubernetes control plane can dynamically provision Elastic Load Balancers that are requested by Kubernetes services\.
+  ** `kms` ** – Read a key from AWS KMS\. This is required for the Kubernetes control plane to support [secrets encryption](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) of Kubernetes secrets stored in `etcd`\.

To view the latest version of the JSON policy document, see [AmazonEKSClusterPolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSClusterPolicy.html#AmazonEKSClusterPolicy-json) in the AWS Managed Policy Reference Guide\.

## AWS managed policy: AmazonEKSFargatePodExecutionRolePolicy<a name="security-iam-awsmanpol-amazoneksfargatepodexecutionrolepolicy"></a>

This policy grants the role the permissions that provide access to other AWS service resources that are required to run Amazon EKS Pods on Fargate\.

 **Permissions details** 

This policy includes the following permissions that allow Amazon EKS to complete the following tasks:
+  ** `ecr` ** – Allows Pods that are running on Fargate to pull container images that are stored in Amazon ECR\.

To view the latest version of the JSON policy document, see [AmazonEKSFargatePodExecutionRolePolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSFargatePodExecutionRolePolicy.html#AmazonEKSFargatePodExecutionRolePolicy-json) in the AWS Managed Policy Reference Guide\.

## AWS managed policy: AmazonEKSForFargateServiceRolePolicy<a name="security-iam-awsmanpol-amazoneksforfargateservicerolepolicy"></a>

You can’t attach `AmazonEKSForFargateServiceRolePolicy` to your IAM entities\. This policy is attached to a service\-linked role that allows Amazon EKS to perform actions on your behalf\. For more information, see AWSServiceRoleforAmazonEKSForFargate\.

This policy grants necessary permissions to Amazon EKS to run Fargate tasks\. The policy is only used if you have Fargate nodes\.

 **Permissions details** 

This policy includes the following permissions that allow Amazon EKS to complete the following tasks\.
+  ** `ec2` ** – Create and delete Elastic Network Interfaces and describe Elastic Network Interfaces and resources\. This is required so that the Amazon EKS Fargate service can configure the VPC networking that’s required for Fargate Pods\.

To view the latest version of the JSON policy document, see [AmazonEKSForFargateServiceRolePolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSForFargateServiceRolePolicy.html#AmazonEKSForFargateServiceRolePolicy-json) in the AWS Managed Policy Reference Guide\.

## AWS managed policy: AmazonEKSServicePolicy<a name="security-iam-awsmanpol-amazoneksservicepolicy"></a>

This policy allows Amazon EKS to create and manage the necessary resources to operate Amazon EKS clusters\.

 **Permissions details** 

This policy includes the following permissions that allow Amazon EKS to complete the following tasks\.
+  ** `eks` ** – Update the Kubernetes version of your cluster after you initiate an update\. This permission isn’t used by Amazon EKS but remains in the policy for backwards compatibility\.
+  ** `ec2` ** – Work with Elastic Network Interfaces and other network resources and tags\. This is required by Amazon EKS to configure networking that facilitates communication between nodes and the Kubernetes control plane\.
+  ** `route53` ** – Associate a VPC with a hosted zone\. This is required by Amazon EKS to enable private endpoint networking for your Kubernetes cluster API server\.
+  ** `logs` ** – Log events\. This is required so that Amazon EKS can ship Kubernetes control plane logs to CloudWatch\.

To view the latest version of the JSON policy document, see [AmazonEKSServicePolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSServicePolicy.html#AmazonEKSServicePolicy-json) in the AWS Managed Policy Reference Guide\.

## AWS managed policy: AmazonEKSServiceRolePolicy<a name="security-iam-awsmanpol-amazoneksservicerolepolicy"></a>

This policy allows the service\-linked role to call AWS services on your behalf\.

 **Permissions details** 

This policy includes the following permissions that allow Amazon EKS to complete the following tasks\.
+  ** `iam` ** – List all of the managed policies that attached to an IAM role\. This is required so that Amazon EKS can list and validate all managed policies and permissions required to create a cluster\.
+  **Associate a VPC with a hosted zone** – This is required by Amazon EKS to enable private endpoint networking for your Kubernetes cluster API server\.
+  **Log event** – This is required so that Amazon EKS can ship Kubernetes control plane logs to CloudWatch\.

To view the latest version of the JSON policy document, see [AmazonEKSServiceRolePolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSServiceRolePolicy.html#AmazonEKSServiceRolePolicy-json) in the AWS Managed Policy Reference Guide\.

## AWS managed policy: AmazonEKSVPCResourceController<a name="security-iam-awsmanpol-amazoneksvpcresourcecontroller"></a>

This policy grants the cluster role permissions to manage Elastic Network Interfaces and IP addresses for nodes\.

 **Permissions details** 

This policy includes the following permissions that allow Amazon EKS to complete the following tasks:
+  ** `ec2` ** – Manage Elastic Network Interfaces and IP addresses to support Pod security groups and Windows nodes\.

To view the latest version of the JSON policy document, see [AmazonEKSVPCResourceController](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSVPCResourceController.html#AmazonEKSVPCResourceController-json) in the AWS Managed Policy Reference Guide\.

## AWS managed policy: AmazonEKSWorkerNodePolicy<a name="security-iam-awsmanpol-amazoneksworkernodepolicy"></a>

This policy grants Amazon EKS Amazon EC2 nodes permissions to connect to Amazon EKS clusters\.

 **Permissions details** 

This policy includes the following permissions that allow Amazon EKS to complete the following tasks:
+  ** `ec2` ** – Read instance volume and network information\. This is required so that Kubernetes nodes can describe information about Amazon EC2 resources that are required for the node to join the Amazon EKS cluster\.
+  ** `eks` ** – Optionally describe the cluster as part of node bootstrapping\.
+  ** `eks-auth:AssumeRoleForPodIdentity` ** – Allow retrieving credentials for EKS workloads on the node\. This is required for EKS Pod Identity to function properly\.

To view the latest version of the JSON policy document, see [AmazonEKSWorkerNodePolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSWorkerNodePolicy.html#AmazonEKSWorkerNodePolicy-json) in the AWS Managed Policy Reference Guide\.

## AWS managed policy: AWSServiceRoleForAmazonEKSNodegroup<a name="security-iam-awsmanpol-awsserviceroleforamazoneksnodegroup"></a>

This policy grants the ` AWSServiceRoleForAmazonEKSNodegroup` role permissions that allow it to create and manage Amazon EC2 node groups in your account\.

 **Permissions details** 

This policy includes the following permissions that allow Amazon EKS to complete the following tasks:
+  ** `ec2` ** – Work with security groups, tags, and launch templates\. This is required for Amazon EKS managed node groups to enable remote access configuration\. Additionally, Amazon EKS managed node groups create a launch template on your behalf\. This is to configure the Amazon EC2 Auto Scaling group that backs each managed node group\.
+  ** `iam` ** – Create a service\-linked role and pass a role\. This is required by Amazon EKS managed node groups to manage instance profiles for the role being passed when creating a managed node group\. This instance profile is used by Amazon EC2 instances launched as part of a managed node group\. Amazon EKS needs to create service\-linked roles for other services such as Amazon EC2 Auto Scaling groups\. These permissions are used in the creation of a managed node group\.
+  ** `autoscaling` ** – Work with security Auto Scaling groups\. This is required by Amazon EKS managed node groups to manage the Amazon EC2 Auto Scaling group that backs each managed node group\. It’s also used to support functionality such as evicting Pods when nodes are terminated or recycled during node group updates\.

To view the latest version of the JSON policy document, see \{https\-\-\-docs\-aws\-amazon\-com\-aws\-managed\-policy\-latest\-reference\-AWSServiceRoleForAmazonEKSNodegroup\-html\-AWSServiceRoleForAmazonEKSNodegroup\-json\}\[AWSServiceRoleForAmazonEKSNodegroup\] in the AWS Managed Policy Reference Guide\.

## AWS managed policy: AmazonEBSCSIDriverPolicy<a name="security-iam-awsmanpol-amazonebscsidriverservicerolepolicy"></a>

The `AmazonEBSCSIDriverPolicy` policy allows the Amazon EBS Container Storage Interface \(CSI\) driver to create, modify, attach, detach, and delete volumes on your behalf\. It also grants the EBS CSI driver permissions to create and delete snapshots, and to list your instances, volumes, and snapshots\.

To view the latest version of the JSON policy document, see [AmazonEBSCSIDriverServiceRolePolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEBSCSIDriverPolicy.html#AmazonEBSCSIDriverPolicy-json) in the AWS Managed Policy Reference Guide\.

## AWS managed policy: AmazonEFSCSIDriverPolicy<a name="security-iam-awsmanpol-amazonefscsidriverservicerolepolicy"></a>

The `AmazonEFSCSIDriverPolicy` policy allows the Amazon EFS Container Storage Interface \(CSI\) to create and delete access points on your behalf\. It also grants the Amazon EFS CSI driver permissions to list your access points file systems, mount targets, and Amazon EC2 availability zones\.

To view the latest version of the JSON policy document, see [AmazonEFSCSIDriverServiceRolePolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEFSCSIDriverPolicy.html#AmazonEFSCSIDriverPolicy-json) in the AWS Managed Policy Reference Guide\.

## AWS managed policy: AmazonEKSLocalOutpostClusterPolicy<a name="security-iam-awsmanpol-amazonekslocaloutpostclusterpolicy"></a>

The `AmazonEKSLocalOutpostClusterPolicy` includes the following permissions:
+  ** `ec2` ** – Required permissions for Amazon EC2 instances to successfully join the cluster as control plane instances\.
+  ** `ssm` ** – Allows Amazon EC2 Systems Manager connection to the control plane instance, which is used by Amazon EKS to communicate and manage the local cluster in your account\.
+  ** `logs` ** – Allows instances to push logs to Amazon CloudWatch\.
+  ** `secretsmanager` ** – Allows instances to get and delete bootstrap data for the control plane instances securely from AWS Secrets Manager\.
+  ** `ecr` ** – Allows Pods and containers that are running on the control plane instances to pull container images that are stored in Amazon Elastic Container Registry\.

To view the latest version of the JSON policy document, see [AmazonEKSLocalOutpostClusterPolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSLocalOutpostClusterPolicy.html#AmazonEKSLocalOutpostClusterPolicy-json) in the AWS Managed Policy Reference Guide\.

## AWS managed policy: AmazonEKSLocalOutpostServiceRolePolicy<a name="security-iam-awsmanpol-amazonekslocaloutpostservicerolepolicy"></a>

The `AmazonEKSLocalOutpostServiceRolePolicy` includes the following permissions:
+  ** `ec2` ** – Allows Amazon EKS to work with security, network, and other resources to successfully launch and manage control plane instances in your account\.
+  ** `ssm` ** – Allows Amazon EC2 Systems Manager connection to the control plane instances, which is used by Amazon EKS to communicate and manage the local cluster in your account\.
+  ** `iam` ** – Allows Amazon EKS to manage the instance profile associated with the control plane instances\.
+  ** `secretsmanager` ** – Allows Amazon EKS to put bootstrap data for the control plane instances into AWS Secrets Manager so it can be securely referenced during instance bootstrapping\.
+  ** `outposts` ** – Allows Amazon EKS to get Outpost information from your account to successfully launch a local cluster in an Outpost\.

To view the latest version of the JSON policy document, see [AmazonEKSLocalOutpostServiceRolePolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSLocalOutpostServiceRolePolicy.html#AmazonEKSLocalOutpostServiceRolePolicy-json) in the AWS Managed Policy Reference Guide\.

## Amazon EKS updates to AWS managed policies<a name="security-iam-awsmanpol-updates"></a>

View details about updates to AWS managed policies for Amazon EKS since this service began tracking these changes\. For automatic alerts about changes to this page, subscribe to the RSS feed on the Amazon EKS Document history page\.

Amazon EKS added new `ec2:DescribeSubnets` permissions to allow the Amazon VPC CNI plugin for  Kubernetes to see the amount of free IP addresses in your Amazon VPC subnets\.

The VPC CNI can use the free IP addresses in each subnet to pick the subnets with the most free IP addresses to use when creating an elastic network interface\.

Amazon EKS added new permissions to allow EKS Pod Identities\.

The Amazon EKS Pod Identity Agent uses the node role\.

 AWS introduced the `AmazonEFSCSIDriverPolicy`\.

Added `ec2:DescribeAvailabilityZones` permission to allow Amazon EKS to get the AZ details during subnet auto\-discovery while creating load balancers\.

Removed invalid policy conditions with wildcard characters in the `StringLike` key field\. Also added a new condition `ec2:ResourceTag/kubernetes.io/created-for/pvc/name: "*"` to `ec2:DeleteVolume`, which allows the EBS CSI driver to delete volumes created by the in\-tree plugin\.

Added `ec2:DescribeVPCAttribute`, `ec2:GetConsoleOutput` and `ec2:DescribeSecret` to allow better prerequisite validation and managed lifecycle control\. Also added `ec2:DescribePlacementGroups` and `"arn:aws:ec2:*:*:placement-group/*"` to `ec2:RunInstances` to support placement control of the control plane Amazon EC2 instances on Outposts\.

Moved action `ecr:GetDownloadUrlForLayer` from all resource sections to a scoped section\. Added resource `arn:aws:ecr:*:*:repository/eks/ `\. Removed resource `arn:aws:ecr:`\. This resource is covered by the added `arn:aws:ecr:*:*:repository/eks/*` resource\.

Added the `arn:aws:ecr:*:*:repository/kubelet-config-updater` Amazon Elastic Container Registry repository so the cluster control plane instances can update some `kubelet` arguments\.

 AWS introduced the `AmazonEKSLocalOutpostClusterPolicy`\.

 AWS introduced the `AmazonEKSLocalOutpostServiceRolePolicy`\.

 AWS introduced the `AmazonEBSCSIDriverPolicy`\.

Added `ec2:DescribeInstanceTypes` to enable Amazon EKS\-optimized AMIs that can auto discover instance level properties\.

Added `autoscaling:EnableMetricsCollection` permission to allow Amazon EKS to enable metrics collection\.

December 13, 2021

Added `ec2:DescribeAccountAttributes`, `ec2:DescribeAddresses`, and `ec2:DescribeInternetGateways` permissions to allow Amazon EKS to create a service\-linked role for a Network Load Balancer\.

Amazon EKS started tracking changes\.

Amazon EKS started tracking changes for its AWS managed policies\.