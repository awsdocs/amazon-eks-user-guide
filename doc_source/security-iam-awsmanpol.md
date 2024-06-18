# AWS managed policies for Amazon Elastic Kubernetes Service<a name="security-iam-awsmanpol"></a>





An AWS managed policy is a standalone policy that is created and administered by AWS\. AWS managed policies are designed to provide permissions for many common use cases so that you can start assigning permissions to users, groups, and roles\.

Keep in mind that AWS managed policies might not grant least\-privilege permissions for your specific use cases because they're available for all AWS customers to use\. We recommend that you reduce permissions further by defining [ customer managed policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html#customer-managed-policies) that are specific to your use cases\.

You cannot change the permissions defined in AWS managed policies\. If AWS updates the permissions defined in an AWS managed policy, the update affects all principal identities \(users, groups, and roles\) that the policy is attached to\. AWS is most likely to update an AWS managed policy when a new AWS service is launched or new API operations become available for existing services\.

For more information, see [AWS managed policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html#aws-managed-policies) in the *IAM User Guide*\.









## AWS managed policy: AmazonEKS\_CNI\_Policy<a name="security-iam-awsmanpol-AmazonEKS_CNI_Policy"></a>

You can attach the `AmazonEKS_CNI_Policy` to your IAM entities\. Before you create an Amazon EC2 node group, this policy must be attached to either the [node IAM role](create-node-role.md), or to an IAM role that's used specifically by the Amazon VPC CNI plugin for Kubernetes\. This is so that it can perform actions on your behalf\. We recommend that you attach the policy to a role that's used only by the plugin\. For more information, see [Working with the Amazon VPC CNI plugin for Kubernetes Amazon EKS add\-on](managing-vpc-cni.md) and [Configuring the Amazon VPC CNI plugin for Kubernetes to use IAM roles for service accounts \(IRSA\)](cni-iam-role.md)\.

**Permissions details**

This policy includes the following permissions that allow Amazon EKS to complete the following tasks:
+ **`ec2:*NetworkInterface` and `ec2:*PrivateIpAddresses` ** – Allows the Amazon VPC CNI plugin to perform actions such as provisioning Elastic Network Interfaces and IP addresses for Pods to provide networking for applications that run in Amazon EKS\.
+ **`ec2` read actions** – Allows the Amazon VPC CNI plugin to perform actions such as describe instances and subnets to see the amount of free IP addresses in your Amazon VPC subnets\. The VPC CNI can use the free IP addresses in each subnet to pick the subnets with the most free IP addresses to use when creating an elastic network interface\.

To view the latest version of the JSON policy document, see [AmazonEKS\_CNI\_Policy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKS_CNI_Policy.html#AmazonEKS_CNI_Policy-json) in the AWS Managed Policy Reference Guide\.

## AWS managed policy: AmazonEKSClusterPolicy<a name="security-iam-awsmanpol-AmazonEKSClusterPolicy"></a>

You can attach `AmazonEKSClusterPolicy` to your IAM entities\. Before creating a cluster, you must have a [cluster IAM role](service_IAM_role.md) with this policy attached\. Kubernetes clusters that are managed by Amazon EKS make calls to other AWS services on your behalf\. They do this to manage the resources that you use with the service\.

This policy includes the following permissions that allow Amazon EKS to complete the following tasks:
+ **`autoscaling`** – Read and update the configuration of an Auto Scaling group\. These permissions aren't used by Amazon EKS but remain in the policy for backwards compatibility\.
+ **`ec2`** – Work with volumes and network resources that are associated to Amazon EC2 nodes\. This is required so that the Kubernetes control plane can join instances to a cluster and dynamically provision and manage Amazon EBS volumes that are requested by Kubernetes persistent volumes\. 
+ **`elasticloadbalancing`** – Work with Elastic Load Balancers and add nodes to them as targets\. This is required so that the Kubernetes control plane can dynamically provision Elastic Load Balancers requested by Kubernetes services\.
+ **`iam`** – Create a service\-linked role\. This is required so that the Kubernetes control plane can dynamically provision Elastic Load Balancers that are requested by Kubernetes services\.
+ **`kms`** – Read a key from AWS KMS\. This is required for the Kubernetes control plane to support [secrets encryption](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) of Kubernetes secrets stored in `etcd`\.

To view the latest version of the JSON policy document, see [AmazonEKSClusterPolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSClusterPolicy.html#AmazonEKSClusterPolicy-json) in the AWS Managed Policy Reference Guide\.

## AWS managed policy: AmazonEKSFargatePodExecutionRolePolicy<a name="security-iam-awsmanpol-AmazonEKSFargatePodExecutionRolePolicy"></a>

You can attach `AmazonEKSFargatePodExecutionRolePolicy` to your IAM entities\. Before you can create a Fargate profile, you must create a Fargate Pod execution role and attach this policy to it\. For more information, see [Create a Fargate Pod execution role](fargate-getting-started.md#fargate-sg-pod-execution-role) and [AWS Fargate profile](fargate-profile.md)\.

This policy grants the role the permissions that provide access to other AWS service resources that are required to run Amazon EKS Pods on Fargate\.

**Permissions details**

This policy includes the following permissions that allow Amazon EKS to complete the following tasks:
+ **`ecr`** – Allows Pods that are running on Fargate to pull container images that are stored in Amazon ECR\.

To view the latest version of the JSON policy document, see [AmazonEKSFargatePodExecutionRolePolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSFargatePodExecutionRolePolicy.html#AmazonEKSFargatePodExecutionRolePolicy-json) in the AWS Managed Policy Reference Guide\.

## AWS managed policy: AmazonEKSForFargateServiceRolePolicy<a name="security-iam-awsmanpol-AmazonEKSForFargateServiceRolePolicy"></a>

You can't attach `AmazonEKSForFargateServiceRolePolicy` to your IAM entities\. This policy is attached to a service\-linked role that allows Amazon EKS to perform actions on your behalf\. For more information, see AWSServiceRoleforAmazonEKSForFargate\.

This policy grants necessary permissions to Amazon EKS to run Fargate tasks\. The policy is only used if you have Fargate nodes\.

**Permissions details**

This policy includes the following permissions that allow Amazon EKS to complete the following tasks\.
+ **`ec2`** – Create and delete Elastic Network Interfaces and describe Elastic Network Interfaces and resources\. This is required so that the Amazon EKS Fargate service can configure the VPC networking that's required for Fargate Pods\.

To view the latest version of the JSON policy document, see [AmazonEKSForFargateServiceRolePolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSForFargateServiceRolePolicy.html#AmazonEKSForFargateServiceRolePolicy-json) in the AWS Managed Policy Reference Guide\.

## AWS managed policy: AmazonEKSServicePolicy<a name="security-iam-awsmanpol-AmazonEKSServicePolicy"></a>

You can attach `AmazonEKSServicePolicy` to your IAM entities\. Clusters that were created before April 16, 2020, required you to create an IAM role and attach this policy to it\. Clusters that were created on or after April 16, 2020, don't require you to create a role and don't require you to assign this policy\. When you create a cluster using an IAM principal that has the `iam:CreateServiceLinkedRole` permission, the [AWSServiceRoleforAmazonEKS](using-service-linked-roles-eks.md#service-linked-role-permissions-eks) service\-linked role is automatically created for you\. The service\-linked role has the [AWS managed policy: AmazonEKSServiceRolePolicy](#security-iam-awsmanpol-AmazonEKSServiceRolePolicy) attached to it\.

This policy allows Amazon EKS to create and manage the necessary resources to operate Amazon EKS clusters\. 

**Permissions details**

This policy includes the following permissions that allow Amazon EKS to complete the following tasks\.
+ **`eks`** – Update the Kubernetes version of your cluster after you initiate an update\. This permission isn't used by Amazon EKS but remains in the policy for backwards compatibility\.
+ **`ec2`** – Work with Elastic Network Interfaces and other network resources and tags\. This is required by Amazon EKS to configure networking that facilitates communication between nodes and the Kubernetes control plane\.
+ **`route53`** – Associate a VPC with a hosted zone\. This is required by Amazon EKS to enable private endpoint networking for your Kubernetes cluster API server\.
+ **`logs`** – Log events\. This is required so that Amazon EKS can ship Kubernetes control plane logs to CloudWatch\.
+ **`iam`** – Create a service\-linked role\. This is required so that Amazon EKS can create the [`AWSServiceRoleForAmazonEKS`](using-service-linked-roles-eks.md#service-linked-role-permissions-eks) service\-linked role on your behalf\.

To view the latest version of the JSON policy document, see [AmazonEKSServicePolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSServicePolicy.html#AmazonEKSServicePolicy-json) in the AWS Managed Policy Reference Guide\.

## AWS managed policy: AmazonEKSServiceRolePolicy<a name="security-iam-awsmanpol-AmazonEKSServiceRolePolicy"></a>

You can't attach `AmazonEKSServiceRolePolicy` to your IAM entities\. This policy is attached to a service\-linked role that allows Amazon EKS to perform actions on your behalf\. For more information, see [Service\-linked role permissions for Amazon EKS](using-service-linked-roles-eks.md#service-linked-role-permissions-eks)\. When you create a cluster using an IAM principal that has the `iam:CreateServiceLinkedRole` permission, the [AWSServiceRoleforAmazonEKS](using-service-linked-roles-eks.md#service-linked-role-permissions-eks) service\-linked role is automatically created for you and this policy is attached to it\.

This policy allows the service\-linked role to call AWS services on your behalf\. 

**Permissions details**

This policy includes the following permissions that allow Amazon EKS to complete the following tasks\.
+ **`ec2`** – Create and describe Elastic Network Interfaces and Amazon EC2 instances, the [cluster security group](sec-group-reqs.md), and VPC that are required to create a cluster\.
+ **`iam`** – List all of the managed policies that attached to an IAM role\. This is required so that Amazon EKS can list and validate all managed policies and permissions required to create a cluster\.
+ **Associate a VPC with a hosted zone** – This is required by Amazon EKS to enable private endpoint networking for your Kubernetes cluster API server\.
+ **Log event** – This is required so that Amazon EKS can ship Kubernetes control plane logs to CloudWatch\.

To view the latest version of the JSON policy document, see [AmazonEKSServiceRolePolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSServiceRolePolicy.html#AmazonEKSServiceRolePolicy-json) in the AWS Managed Policy Reference Guide\.

## AWS managed policy: AmazonEKSVPCResourceController<a name="security-iam-awsmanpol-AmazonEKSVPCResourceController"></a>

You can attach the `AmazonEKSVPCResourceController` policy to your IAM identities\. If you're using [security groups for Pods](security-groups-for-pods.md), you must attach this policy to your [Amazon EKS cluster IAM role](service_IAM_role.md) to perform actions on your behalf\. 

This policy grants the cluster role permissions to manage Elastic Network Interfaces and IP addresses for nodes\. 

**Permissions details**

This policy includes the following permissions that allow Amazon EKS to complete the following tasks:
+ **`ec2`** – Manage Elastic Network Interfaces and IP addresses to support Pod security groups and Windows nodes\.

To view the latest version of the JSON policy document, see [AmazonEKSVPCResourceController](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSVPCResourceController.html#AmazonEKSVPCResourceController-json) in the AWS Managed Policy Reference Guide\.

## AWS managed policy: AmazonEKSWorkerNodePolicy<a name="security-iam-awsmanpol-AmazonEKSWorkerNodePolicy"></a>

You can attach the `AmazonEKSWorkerNodePolicy` to your IAM entities\. You must attach this policy to a [node IAM role](create-node-role.md) that you specify when you create Amazon EC2 nodes that allow Amazon EKS to perform actions on your behalf\. If you create a node group using `eksctl`, it creates the node IAM role and attaches this policy to the role automatically\.

This policy grants Amazon EKS Amazon EC2 nodes permissions to connect to Amazon EKS clusters\. 

**Permissions details**

This policy includes the following permissions that allow Amazon EKS to complete the following tasks:
+ **`ec2`** – Read instance volume and network information\. This is required so that Kubernetes nodes can describe information about Amazon EC2 resources that are required for the node to join the Amazon EKS cluster\.
+ **`eks`** – Optionally describe the cluster as part of node bootstrapping\.
+ **`eks-auth:AssumeRoleForPodIdentity`** – Allow retrieving credentials for EKS workloads on the node\. This is required for EKS Pod Identity to function properly\.

To view the latest version of the JSON policy document, see [AmazonEKSWorkerNodePolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSWorkerNodePolicy.html#AmazonEKSWorkerNodePolicy-json) in the AWS Managed Policy Reference Guide\.

## AWS managed policy: AWSServiceRoleForAmazonEKSNodegroup<a name="security-iam-awsmanpol-AWSServiceRoleForAmazonEKSNodegroup"></a>

You can't attach `AWSServiceRoleForAmazonEKSNodegroup` to your IAM entities\. This policy is attached to a service\-linked role that allows Amazon EKS to perform actions on your behalf\. For more information, see [Service\-linked role permissions for Amazon EKS](using-service-linked-roles-eks-nodegroups.md#service-linked-role-permissions-eks-nodegroups)\.

This policy grants the `AWSServiceRoleForAmazonEKSNodegroup` role permissions that allow it to create and manage Amazon EC2 node groups in your account\. 

**Permissions details**

This policy includes the following permissions that allow Amazon EKS to complete the following tasks:
+ **`ec2`** – Work with security groups, tags, and launch templates\. This is required for Amazon EKS managed node groups to enable remote access configuration\. Additionally, Amazon EKS managed node groups create a launch template on your behalf\. This is to configure the Amazon EC2 Auto Scaling group that backs each managed node group\. 
+ **`iam`** – Create a service\-linked role and pass a role\. This is required by Amazon EKS managed node groups to manage instance profiles for the role being passed when creating a managed node group\. This instance profile is used by Amazon EC2 instances launched as part of a managed node group\. Amazon EKS needs to create service\-linked roles for other services such as Amazon EC2 Auto Scaling groups\. These permissions are used in the creation of a managed node group\.
+ **`autoscaling`** – Work with security Auto Scaling groups\. This is required by Amazon EKS managed node groups to manage the Amazon EC2 Auto Scaling group that backs each managed node group\. It's also used to support functionality such as evicting Pods when nodes are terminated or recycled during node group updates\.

To view the latest version of the JSON policy document, see [AWSServiceRoleForAmazonEKSNodegroup](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AWSServiceRoleForAmazonEKSNodegroup.html#AWSServiceRoleForAmazonEKSNodegroup-json) in the AWS Managed Policy Reference Guide\.

## AWS managed policy: AmazonEBSCSIDriverPolicy<a name="security-iam-awsmanpol-AmazonEBSCSIDriverServiceRolePolicy"></a>

The `AmazonEBSCSIDriverPolicy` policy allows the Amazon EBS Container Storage Interface \(CSI\) driver to create, modify, attach, detach, and delete volumes on your behalf\. It also grants the EBS CSI driver permissions to create and delete snapshots, and to list your instances, volumes, and snapshots\.

To view the latest version of the JSON policy document, see [AmazonEBSCSIDriverServiceRolePolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEBSCSIDriverPolicy.html#AmazonEBSCSIDriverPolicy-json) in the AWS Managed Policy Reference Guide\.

## AWS managed policy: AmazonEFSCSIDriverPolicy<a name="security-iam-awsmanpol-AmazonEFSCSIDriverServiceRolePolicy"></a>

The `AmazonEFSCSIDriverPolicy` policy allows the Amazon EFS Container Storage Interface \(CSI\) to create and delete access points on your behalf\. It also grants the Amazon EFS CSI driver permissions to list your access points file systems, mount targets, and Amazon EC2 availability zones\.

To view the latest version of the JSON policy document, see [AmazonEFSCSIDriverServiceRolePolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEFSCSIDriverPolicy.html#AmazonEFSCSIDriverPolicy-json) in the AWS Managed Policy Reference Guide\.

## AWS managed policy: AmazonEKSLocalOutpostClusterPolicy<a name="security-iam-awsmanpol-AmazonEKSLocalOutpostClusterPolicy"></a>

You can attach this policy to IAM entities\. Before creating a local cluster, you must attach this policy to your [cluster role](service_IAM_role.md)\. Kubernetes clusters that are managed by Amazon EKS make calls to other AWS services on your behalf\. They do this to manage the resources that you use with the service\.

The `AmazonEKSLocalOutpostClusterPolicy` includes the following permissions:
+ **`ec2`** – Required permissions for Amazon EC2 instances to successfully join the cluster as control plane instances\.
+ **`ssm`** – Allows Amazon EC2 Systems Manager connection to the control plane instance, which is used by Amazon EKS to communicate and manage the local cluster in your account\.
+ **`logs`** – Allows instances to push logs to Amazon CloudWatch\.
+ **`secretsmanager`** – Allows instances to get and delete bootstrap data for the control plane instances securely from AWS Secrets Manager\.
+ **`ecr`** – Allows Pods and containers that are running on the control plane instances to pull container images that are stored in Amazon Elastic Container Registry\.

To view the latest version of the JSON policy document, see [AmazonEKSLocalOutpostClusterPolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSLocalOutpostClusterPolicy.html#AmazonEKSLocalOutpostClusterPolicy-json) in the AWS Managed Policy Reference Guide\.

## AWS managed policy: AmazonEKSLocalOutpostServiceRolePolicy<a name="security-iam-awsmanpol-AmazonEKSLocalOutpostServiceRolePolicy"></a>

You can't attach this policy to your IAM entities\. When you create a cluster using an IAM principal that has the `iam:CreateServiceLinkedRole` permission, Amazon EKS automatically creates the [`AWSServiceRoleforAmazonEKSLocalOutpost`](using-service-linked-roles-eks-outpost.md) service\-linked role for you and attaches this policy to it\. This policy allows the service\-linked role to call AWS services on your behalf for local clusters\. 

The `AmazonEKSLocalOutpostServiceRolePolicy` includes the following permissions:
+ **`ec2`** – Allows Amazon EKS to work with security, network, and other resources to successfully launch and manage control plane instances in your account\.
+ **`ssm`** – Allows Amazon EC2 Systems Manager connection to the control plane instances, which is used by Amazon EKS to communicate and manage the local cluster in your account\.
+ **`iam`** – Allows Amazon EKS to manage the instance profile associated with the control plane instances\.
+ **`secretsmanager`** – Allows Amazon EKS to put bootstrap data for the control plane instances into AWS Secrets Manager so it can be securely referenced during instance bootstrapping\.
+ **`outposts`** – Allows Amazon EKS to get Outpost information from your account to successfully launch a local cluster in an Outpost\.

To view the latest version of the JSON policy document, see [AmazonEKSLocalOutpostServiceRolePolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSLocalOutpostServiceRolePolicy.html#AmazonEKSLocalOutpostServiceRolePolicy-json) in the AWS Managed Policy Reference Guide\.





## Amazon EKS updates to AWS managed policies<a name="security-iam-awsmanpol-updates"></a>



View details about updates to AWS managed policies for Amazon EKS since this service began tracking these changes\. For automatic alerts about changes to this page, subscribe to the RSS feed on the Amazon EKS Document history page\.




| Change | Description | Date | 
| --- | --- | --- | 
|  [AmazonEKS\_CNI\_Policy](#security-iam-awsmanpol-AmazonEKS_CNI_Policy) – Update to an existing policy  |  Amazon EKS added new `ec2:DescribeSubnets` permissions to allow the Amazon VPC CNI plugin for Kubernetes to see the amount of free IP addresses in your Amazon VPC subnets\.  The VPC CNI can use the free IP addresses in each subnet to pick the subnets with the most free IP addresses to use when creating an elastic network interface\.  | March 4, 2024 | 
|  [AmazonEKSWorkerNodePolicy](#security-iam-awsmanpol-AmazonEKSWorkerNodePolicy) – Update to an existing policy  |  Amazon EKS added new permissions to allow EKS Pod Identities\. The Amazon EKS Pod Identity Agent uses the node role\.  | November 26, 2023 | 
|  Introduced [AmazonEFSCSIDriverPolicy](#security-iam-awsmanpol-AmazonEFSCSIDriverServiceRolePolicy)\.  |  AWS introduced the `AmazonEFSCSIDriverPolicy`\.  | July 26, 2023 | 
|  Added permissions to [AmazonEKSClusterPolicy](#security-iam-awsmanpol-AmazonEKSClusterPolicy)\.  |   Added `ec2:DescribeAvailabilityZones` permission to allow Amazon EKS to get the AZ details during subnet auto\-discovery while creating load balancers\.  | February 7, 2023 | 
|  Updated policy conditions in [AmazonEBSCSIDriverPolicy](#security-iam-awsmanpol-AmazonEBSCSIDriverServiceRolePolicy)\.  |  Removed invalid policy conditions with wildcard characters in the `StringLike` key field\. Also added a new condition `ec2:ResourceTag/kubernetes.io/created-for/pvc/name: "*"` to `ec2:DeleteVolume`, which allows the EBS CSI driver to delete volumes created by the in\-tree plugin\.  | November 17, 2022 | 
|  Added permissions to [AmazonEKSLocalOutpostServiceRolePolicy](#security-iam-awsmanpol-AmazonEKSLocalOutpostServiceRolePolicy)\.  | Added `ec2:DescribeVPCAttribute`, `ec2:GetConsoleOutput` and `ec2:DescribeSecret` to allow better prerequisite validation and managed lifecycle control\. Also added `ec2:DescribePlacementGroups` and `"arn:aws:ec2:*:*:placement-group/*"` to `ec2:RunInstances` to support placement control of the control plane Amazon EC2 instances on Outposts\. | October 24, 2022 | 
|  Update Amazon Elastic Container Registry permissions in [AmazonEKSLocalOutpostClusterPolicy](#security-iam-awsmanpol-AmazonEKSLocalOutpostClusterPolicy)\.  |  Moved action `ecr:GetDownloadUrlForLayer` from all resource sections to a scoped section\. Added resource `arn:aws:ecr:*:*:repository/eks/*`\. Removed resource `arn:aws:ecr:*:*:repository/eks/eks-certificates-controller-public`\. This resource is covered by the added `arn:aws:ecr:*:*:repository/eks/*` resource\.  | October 20, 2022 | 
|  Added permissions to [AmazonEKSLocalOutpostClusterPolicy](#security-iam-awsmanpol-AmazonEKSLocalOutpostClusterPolicy)\.  |  Added the `arn:aws:ecr:*:*:repository/kubelet-config-updater` Amazon Elastic Container Registry repository so the cluster control plane instances can update some `kubelet` arguments\.  | August 31, 2022 | 
|  Introduced [AmazonEKSLocalOutpostClusterPolicy](#security-iam-awsmanpol-AmazonEKSLocalOutpostClusterPolicy)\.  |  AWS introduced the `AmazonEKSLocalOutpostClusterPolicy`\.  | August 24, 2022 | 
|  Introduced [AmazonEKSLocalOutpostServiceRolePolicy](#security-iam-awsmanpol-AmazonEKSLocalOutpostServiceRolePolicy)\.  |  AWS introduced the `AmazonEKSLocalOutpostServiceRolePolicy`\.  | August 23, 2022 | 
|  Introduced [AmazonEBSCSIDriverPolicy](#security-iam-awsmanpol-AmazonEBSCSIDriverServiceRolePolicy)\.  |  AWS introduced the `AmazonEBSCSIDriverPolicy`\.  | April 4, 2022 | 
|  Added permissions to [AmazonEKSWorkerNodePolicy](#security-iam-awsmanpol-AmazonEKSWorkerNodePolicy)\.  |  Added `ec2:DescribeInstanceTypes` to enable Amazon EKS\-optimized AMIs that can auto discover instance level properties\.  | March 21, 2022 | 
|  Added permissions to [AWSServiceRoleForAmazonEKSNodegroup](#security-iam-awsmanpol-AWSServiceRoleForAmazonEKSNodegroup)\.  |  Added `autoscaling:EnableMetricsCollection` permission to allow Amazon EKS to enable metrics collection\.  | December 13, 2021 | 
|  Added permissions to [AmazonEKSClusterPolicy](#security-iam-awsmanpol-AmazonEKSClusterPolicy)\.  |  Added `ec2:DescribeAccountAttributes`, `ec2:DescribeAddresses`, and `ec2:DescribeInternetGateways` permissions to allow Amazon EKS to create a service\-linked role for a Network Load Balancer\.  | June 17, 2021 | 
|  Amazon EKS started tracking changes\.  |  Amazon EKS started tracking changes for its AWS managed policies\.  | June 17, 2021 | 