# AWS managed policies for Amazon Elastic Kubernetes Service<a name="security-iam-awsmanpol"></a>





To add permissions to users, groups, and roles, it is easier to use AWS managed policies than to write policies yourself\. It takes time and expertise to [create IAM customer managed policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create-console.html) that provide your team with only the permissions they need\. To get started quickly, you can use our AWS managed policies\. These policies cover common use cases and are available in your AWS account\. For more information about AWS managed policies, see [AWS managed policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html#aws-managed-policies) in the *IAM User Guide*\.

AWS services maintain and update AWS managed policies\. You can't change the permissions in AWS managed policies\. Services occasionally add additional permissions to an AWS managed policy to support new features\. This type of update affects all identities \(users, groups, and roles\) where the policy is attached\. Services are most likely to update an AWS managed policy when a new feature is launched or when new operations become available\. Services do not remove permissions from an AWS managed policy, so policy updates won't break your existing permissions\.

Additionally, AWS supports managed policies for job functions that span multiple services\. For example, the **ReadOnlyAccess** AWS managed policy provides read\-only access to all AWS services and resources\. When a service launches a new feature, AWS adds read\-only permissions for new operations and resources\. For a list and descriptions of job function policies, see [AWS managed policies for job functions](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_job-functions.html) in the *IAM User Guide*\.

## AWS managed policy: AmazonEKS\_CNI\_Policy<a name="security-iam-awsmanpol-AmazonEKS_CNI_Policy"></a>

You can attach the `AmazonEKS_CNI_Policy` to your IAM entities\. Before you create an Amazon EC2 node group, this policy must be attached to either the [node IAM role](create-node-role.md), or to an IAM role that's used specifically by the AWS VPC CNI plugin\. This is so that it can perform actions on your behalf\. We recommend that you attach the policy to a role that's used only by the CNI plugin\. For more information, see [Pod networking \(CNI\)](pod-networking.md) and [Configuring the Amazon VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.

**Permissions details**

This policy includes the following permissions that allow Amazon EKS to complete the following tasks:
+ `ec2` – Allows the Amazon VPC CNI plugin to perform actions such as provisioning Elastic Network Interfaces and IP addresses for pods to provide networking for applications that run in Amazon EKS\.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:AssignPrivateIpAddresses",
                "ec2:AttachNetworkInterface",
                "ec2:CreateNetworkInterface",
                "ec2:DeleteNetworkInterface",
                "ec2:DescribeInstances",
                "ec2:DescribeTags",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DescribeInstanceTypes",
                "ec2:DetachNetworkInterface",
                "ec2:ModifyNetworkInterfaceAttribute",
                "ec2:UnassignPrivateIpAddresses"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateTags"
            ],
            "Resource": [
                "arn:aws:ec2:*:*:network-interface/*"
            ]
        }
    ]
}
```

## AWS managed policy: AmazonEKSClusterPolicy<a name="security-iam-awsmanpol-AmazonEKSClusterPolicy"></a>

You can attach `AmazonEKSClusterPolicy` to your IAM entities\. Before creating a cluster, you must have a [cluster IAM role](service_IAM_role.md) with this policy attached\. Kubernetes clusters managed by Amazon EKS make calls to other AWS services on your behalf\. They do this to manage the resources that you use with the service\.

This policy includes the following permissions that allow Amazon EKS to complete the following tasks:
+ `autoscaling` – Read and update the configuration of an Auto Scaling group\. These permissions aren't used by Amazon EKS but remain in the policy for backwards compatibility\.
+ `ec2` – Work with volumes and network resources that are associated to Amazon EC2 nodes\. This is required so that the Kubernetes control plane can join instances to a cluster and dynamically provision and manage Amazon EBS volumes requested by Kubernetes Persistent Volumes\. 
+ `elasticloadbalancing` – Work with Elastic Load Balancers and add nodes to them as targets\. This is required so that the Kubernetes control plane can dynamically provision Elastic Load Balancers requested by Kubernetes services\.
+ `iam` – Create a service\-linked role\. This is required so that the Kubernetes control plane can dynamically provision Elastic Load Balancers requested by Kubernetes services\.
+ `kms` – Read a key from AWS KMS\. This is required for the Kubernetes control plane to support [secrets encyption](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) of Kubernetes secrets stored in `etcd`\.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "autoscaling:DescribeAutoScalingGroups",
                "autoscaling:UpdateAutoScalingGroup",
                "ec2:AttachVolume",
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:CreateRoute",
                "ec2:CreateSecurityGroup",
                "ec2:CreateTags",
                "ec2:CreateVolume",
                "ec2:DeleteRoute",
                "ec2:DeleteSecurityGroup",
                "ec2:DeleteVolume",
                "ec2:DescribeInstances",
                "ec2:DescribeRouteTables",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeSubnets",
                "ec2:DescribeVolumes",
                "ec2:DescribeVolumesModifications",
                "ec2:DescribeVpcs",
                "ec2:DescribeDhcpOptions",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DetachVolume",
                "ec2:ModifyInstanceAttribute",
                "ec2:ModifyVolume",
                "ec2:RevokeSecurityGroupIngress",
                "ec2:DescribeAccountAttributes",
                "ec2:DescribeAddresses",
                "ec2:DescribeInternetGateways",
                "elasticloadbalancing:AddTags",
                "elasticloadbalancing:ApplySecurityGroupsToLoadBalancer",
                "elasticloadbalancing:AttachLoadBalancerToSubnets",
                "elasticloadbalancing:ConfigureHealthCheck",
                "elasticloadbalancing:CreateListener",
                "elasticloadbalancing:CreateLoadBalancer",
                "elasticloadbalancing:CreateLoadBalancerListeners",
                "elasticloadbalancing:CreateLoadBalancerPolicy",
                "elasticloadbalancing:CreateTargetGroup",
                "elasticloadbalancing:DeleteListener",
                "elasticloadbalancing:DeleteLoadBalancer",
                "elasticloadbalancing:DeleteLoadBalancerListeners",
                "elasticloadbalancing:DeleteTargetGroup",
                "elasticloadbalancing:DeregisterInstancesFromLoadBalancer",
                "elasticloadbalancing:DeregisterTargets",
                "elasticloadbalancing:DescribeListeners",
                "elasticloadbalancing:DescribeLoadBalancerAttributes",
                "elasticloadbalancing:DescribeLoadBalancerPolicies",
                "elasticloadbalancing:DescribeLoadBalancers",
                "elasticloadbalancing:DescribeTargetGroupAttributes",
                "elasticloadbalancing:DescribeTargetGroups",
                "elasticloadbalancing:DescribeTargetHealth",
                "elasticloadbalancing:DetachLoadBalancerFromSubnets",
                "elasticloadbalancing:ModifyListener",
                "elasticloadbalancing:ModifyLoadBalancerAttributes",
                "elasticloadbalancing:ModifyTargetGroup",
                "elasticloadbalancing:ModifyTargetGroupAttributes",
                "elasticloadbalancing:RegisterInstancesWithLoadBalancer",
                "elasticloadbalancing:RegisterTargets",
                "elasticloadbalancing:SetLoadBalancerPoliciesForBackendServer",
                "elasticloadbalancing:SetLoadBalancerPoliciesOfListener",
                "kms:DescribeKey"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "iam:CreateServiceLinkedRole",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "iam:AWSServiceName": "elasticloadbalancing.amazonaws.com"
                }
            }
        }
    ]
}
```

## AWS managed policy: AmazonEKSFargatePodExecutionRolePolicy<a name="security-iam-awsmanpol-AmazonEKSFargatePodExecutionRolePolicy"></a>

You can attach `AmazonEKSFargatePodExecutionRolePolicy` to your IAM entities\. Before you can create a Fargate profile, you must create a Fargate pod execution role and attach this policy to it\. For more information, see [Create a Fargate pod execution role](fargate-getting-started.md#fargate-sg-pod-execution-role) and [AWS Fargate profile](fargate-profile.md)\.

This policy grants the role the permissions that provide access to other AWS service resources that are required to run Amazon EKS pods on Fargate\.

**Permissions details**

This policy includes the following permissions that allow Amazon EKS to complete the following tasks:
+ `ecr` – Allows Pods running on Fargate to pull container images that are stored in Amazon ECR\.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage"
            ],
            "Resource": "*"
        }
    ]
}
```

## AWS managed policy: AmazonEKSForFargateServiceRolePolicy<a name="security-iam-awsmanpol-AmazonEKSForFargateServiceRolePolicy"></a>

You can't attach `AmazonEKSForFargateServiceRolePolicy` to your IAM entities\. This policy is attached to a service\-linked role that allows Amazon EKS to perform actions on your behalf\. For more information, see AWSServiceRoleforAmazonEKSForFargate\.

This policy grants necessary permissions to Amazon EKS to run Fargate tasks\. The policy is only used if you have Fargate nodes\.

**Permissions details**

This policy includes the following permissions that allow Amazon EKS to complete the following tasks\.
+ `ec2` – Create and delete Elastic Network Interfaces and describe Elastic Network Interfaces and resources\. This is required so that the Amazon EKS Fargate service can configure VPC networking required for Fargate Pods\.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateNetworkInterface",
                "ec2:CreateNetworkInterfacePermission",
                "ec2:DeleteNetworkInterface",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeSubnets",
                "ec2:DescribeVpcs",
                "ec2:DescribeDhcpOptions",
                "ec2:DescribeRouteTables"
            ],
            "Resource": "*"
        }
    ]
}
```

## AWS managed policy: AmazonEKSServicePolicy<a name="security-iam-awsmanpol-AmazonEKSServicePolicy"></a>

You can attach `AmazonEKSServicePolicy` to your IAM entities\. Clusters created before April 16, 2020, required you to create an IAM role and attach this policy to it\. Clusters created on or after April 16, 2020, don't require you to create a role and don't require you to assign this policy\. When you create a cluster using an IAM principal that has the `iam:CreateServiceLinkedRole` permission, the [AWSServiceRoleforAmazonEKS](using-service-linked-roles-eks.md#service-linked-role-permissions-eks) service\-linked role is automatically created for you\. The service\-linked role has the [AWS managed policy: AmazonEKSServiceRolePolicy](#security-iam-awsmanpol-AmazonEKSServiceRolePolicy) attached to it\.

This policy allows Amazon EKS to create and manage the necessary resources to operate Amazon EKS clusters\. 

**Permissions details**

This policy includes the following permissions that allow Amazon EKS to complete the following tasks\.
+ `eks` – Update the Kubernetes version of your cluster after you initiate an update\. This permission isn't used by Amazon EKS but remains in the policy for backwards compatibility\.
+ `ec2` – Work with Elastic Network Interfaces and other network resources and tags\. This is required by Amazon EKS to configure networking that facilitates communication between nodes and the Kubernetes control plane\.
+ `route53` – Associate a VPC with a hosted zone\. This is required by Amazon EKS to enable private endpoint networking for your Kubernetes cluster API server\.
+ `logs` – Log events\. This is required so that Amazon EKS can ship Kubernetes control plane logs to CloudWatch\.
+ `iam` – Create a service\-linked role\. This is required so that Amazon EKScan create the [`AWSServiceRoleForAmazonEKS`](using-service-linked-roles-eks.md#service-linked-role-permissions-eks) service\-linked role on your behalf\.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateNetworkInterface",
                "ec2:CreateNetworkInterfacePermission",
                "ec2:DeleteNetworkInterface",
                "ec2:DescribeInstances",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DetachNetworkInterface",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeSubnets",
                "ec2:DescribeVpcs",
                "ec2:ModifyNetworkInterfaceAttribute",
                "iam:ListAttachedRolePolicies",
                "eks:UpdateClusterVersion"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateTags",
                "ec2:DeleteTags"
            ],
            "Resource": [
                "arn:aws:ec2:*:*:vpc/*",
                "arn:aws:ec2:*:*:subnet/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": "route53:AssociateVPCWithHostedZone",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:DescribeLogStreams"
            ],
            "Resource": "arn:aws:logs:*:*:log-group:/aws/eks/*:*"
        },
        {
            "Effect": "Allow",
            "Action": "logs:PutLogEvents",
            "Resource": "arn:aws:logs:*:*:log-group:/aws/eks/*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": "iam:CreateServiceLinkedRole",
            "Resource": "*",
            "Condition": {
                "StringLike": {
                    "iam:AWSServiceName": "eks.amazonaws.com"
                }
            }
        }
    ]
}
```

## AWS managed policy: AmazonEKSServiceRolePolicy<a name="security-iam-awsmanpol-AmazonEKSServiceRolePolicy"></a>

You can't attach `AmazonEKSServiceRolePolicy` to your IAM entities\. This policy is attached to a service\-linked role that allows Amazon EKS to perform actions on your behalf\. For more information, see [Service\-Linked Role Permissions for Amazon EKS](using-service-linked-roles-eks.md#service-linked-role-permissions-eks)\. When you create a cluster using an IAM principal that has the `iam:CreateServiceLinkedRole` permission, the [AWSServiceRoleforAmazonEKS](using-service-linked-roles-eks.md#service-linked-role-permissions-eks) service\-linked role is automatically created for you and this policy is attached to it\.

This policy allows the service\-linked role to call AWS services on your behalf\. 

**Permissions details**

This policy includes the following permissions that allow Amazon EKS to complete the following tasks\.
+ `ec2` – Create and describe Elastic Network Interfaces and Amazon EC2 instances, the [cluster security group](sec-group-reqs.md#cluster-sg), and VPC that are required for cluster creation\.
+ `iam` – List all of the managed policies that attached to an IAM role\. This is required so that Amazon EKS can list and validate all managed policies and permissions required for creating clusters\.
+  Associate a VPC with a hosted zone\. This is required by Amazon EKS to enable private endpoint networking for your Kubernetes cluster API server\.
+ Log event\. This is required so that Amazon EKS can ship Kubernetes control plane logs to CloudWatch\.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateNetworkInterface",
                "ec2:DeleteNetworkInterface",
                "ec2:DetachNetworkInterface",
                "ec2:ModifyNetworkInterfaceAttribute",
                "ec2:DescribeInstances",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeSubnets",
                "ec2:DescribeVpcs",
                "ec2:CreateNetworkInterfacePermission",
                "iam:ListAttachedRolePolicies",
                "ec2:CreateSecurityGroup"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DeleteSecurityGroup",
                "ec2:RevokeSecurityGroupIngress",
                "ec2:AuthorizeSecurityGroupIngress"
            ],
            "Resource": "arn:aws:ec2:*:*:security-group/*",
            "Condition": {
                "ForAnyValue:StringLike": {
                    "ec2:ResourceTag/Name": "eks-cluster-sg*"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateTags",
                "ec2:DeleteTags"
            ],
            "Resource": [
                "arn:aws:ec2:*:*:vpc/*",
                "arn:aws:ec2:*:*:subnet/*"
            ],
            "Condition": {
                "ForAnyValue:StringLike": {
                    "aws:TagKeys": [
                        "kubernetes.io/cluster/*"
                    ]
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateTags",
                "ec2:DeleteTags"
            ],
            "Resource": [
                "arn:aws:ec2:*:*:security-group/*"
            ],
            "Condition": {
                "ForAnyValue:StringLike": {
                    "aws:TagKeys": [
                        "kubernetes.io/cluster/*"
                    ],
                    "aws:RequestTag/Name": "eks-cluster-sg*"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": "route53:AssociateVPCWithHostedZone",
            "Resource": "arn:aws:route53:::hostedzone/*"
        },
        {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:*:*:log-group:/aws/eks/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:DescribeLogStreams"
            ],
            "Resource": "arn:aws:logs:*:*:log-group:/aws/eks/*:*"
        },
        {
            "Effect": "Allow",
            "Action": "logs:PutLogEvents",
            "Resource": "arn:aws:logs:*:*:log-group:/aws/eks/*:*:*"
        }
    ]
}
```

## AWS managed policy: AmazonEKSVPCResourceController<a name="security-iam-awsmanpol-AmazonEKSVPCResourceController"></a>

You can attach the `AmazonEKSVPCResourceController` policy to your IAM identities\. If you're using [security groups for pods](security-groups-for-pods.md), you must attach this policy to your [Amazon EKS cluster IAM role](service_IAM_role.md) to perform actions on your behalf\. 

This policy grants the cluster role permissions to manage Elastic Network Interfaces and IP addresses for nodes\. 

**Permissions details**

This policy includes the following permissions that allow Amazon EKS to complete the following tasks:
+ `ec2` – Manage Elastic Network Interfaces and IP addresses to support pod security groups and Windows nodes\.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "ec2:CreateNetworkInterfacePermission",
            "Resource": "*",
            "Condition": {
                "ForAnyValue:StringEquals": {
                    "ec2:ResourceTag/eks:eni:owner": "eks-vpc-resource-controller"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateNetworkInterface",
                "ec2:DetachNetworkInterface",
                "ec2:ModifyNetworkInterfaceAttribute",
                "ec2:DeleteNetworkInterface",
                "ec2:AttachNetworkInterface",
                "ec2:UnassignPrivateIpAddresses",
                "ec2:AssignPrivateIpAddresses"
            ],
            "Resource": "*"
        }
    ]
}
```

## AWS managed policy: AmazonEKSWorkerNodePolicy<a name="security-iam-awsmanpol-AmazonEKSWorkerNodePolicy"></a>

You can attach the `AmazonEKSWorkerNodePolicy` to your IAM entities\. You must attach this policy to a [node IAM role](create-node-role.md) that you specify when you create Amazon EC2 nodes that allow Amazon EKS to perform actions on your behalf\. If you create a node group using `eksctl`, it creates the node IAM role and attaches this policy to the role automatically\.

This policy grants Amazon EKS Amazon EC2 nodes permissions to connect to Amazon EKS clusters\. 

**Permissions details**

This policy includes the following permissions that allow Amazon EKS to complete the following tasks:
+ `ec2` – Read instance volume and network information\. This is required so that Kubernetes nodes can describe information about Amazon EC2 resources required for the node to join the Amazon EKS cluster\.
+ `eks` – Optionally describe the cluster as part of node bootstrapping\.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "ec2:DescribeInstances",
                "ec2:DescribeRouteTables",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeSubnets",
                "ec2:DescribeVolumes",
                "ec2:DescribeVolumesModifications",
                "ec2:DescribeVpcs",
                "eks:DescribeCluster"
            ],
            "Resource": "*",
            "Effect": "Allow"
        }
    ]
}
```

## AWS managed policy: AWSServiceRoleForAmazonEKSNodegroup<a name="security-iam-awsmanpol-AWSServiceRoleForAmazonEKSNodegroup"></a>

You can't attach `AWSServiceRoleForAmazonEKSNodegroup` to your IAM entities\. This policy is attached to a service\-linked role that allows Amazon EKS to perform actions on your behalf\. For more information, see [Service\-linked role permissions for Amazon EKS](using-service-linked-roles-eks-nodegroups.md#service-linked-role-permissions-eks-nodegroups)\.

This policy grants the `AWSServiceRoleForAmazonEKSNodegroup` role permissions that allow it to create and manage Amazon EC2 node groups in your account\. 

**Permissions details**

This policy includes the following permissions that allow Amazon EKS to complete the following tasks:
+ `ec2` – Work with security groups, tags, and launch templates\. This is required for Amazon EKS managed node groups to enable remote access configuration\. Additionally, Amazon EKS managed node groups create a launch template on your behalf\. This is to configure the Amazon EC2 Auto Scaling group that backs each managed node group\. 
+ `iam` – Create a service\-linked role and pass a role\. This is required by Amazon EKS managed node groups to manage instance profiles for the role being passed when creating a managed node group\. This instance profile is used by Amazon EC2 instances launched as part of a managed node group\. Amazon EKS needs to create service\-linked roles for other services such as Amazon EC2 Auto Scaling groups\. These are used in the creation of a managed node group
+ `autoscaling` – Work with security Auto Scaling groups\. This is required by Amazon EKS managed node groups to manage the Amazon EC2 Auto Scaling group that backs each managed node group\. It's also used to support functionality such as evicting pods when nodes are terminated or recycled during node group updates\.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "SharedSecurityGroupRelatedPermissions",
            "Effect": "Allow",
            "Action": [
                "ec2:RevokeSecurityGroupIngress",
                "ec2:AuthorizeSecurityGroupEgress",
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:DescribeInstances",
                "ec2:RevokeSecurityGroupEgress",
                "ec2:DeleteSecurityGroup"
            ],
            "Resource": "*",
            "Condition": {
                "StringLike": {
                    "ec2:ResourceTag/eks": "*"
                }
            }
        },
        {
            "Sid": "EKSCreatedSecurityGroupRelatedPermissions",
            "Effect": "Allow",
            "Action": [
                "ec2:RevokeSecurityGroupIngress",
                "ec2:AuthorizeSecurityGroupEgress",
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:DescribeInstances",
                "ec2:RevokeSecurityGroupEgress",
                "ec2:DeleteSecurityGroup"
            ],
            "Resource": "*",
            "Condition": {
                "StringLike": {
                    "ec2:ResourceTag/eks:nodegroup-name": "*"
                }
            }
        },
        {
            "Sid": "LaunchTemplateRelatedPermissions",
            "Effect": "Allow",
            "Action": [
                "ec2:DeleteLaunchTemplate",
                "ec2:CreateLaunchTemplateVersion"
            ],
            "Resource": "*",
            "Condition": {
                "StringLike": {
                    "ec2:ResourceTag/eks:nodegroup-name": "*"
                }
            }
        },
        {
            "Sid": "AutoscalingRelatedPermissions",
            "Effect": "Allow",
            "Action": [
                "autoscaling:UpdateAutoScalingGroup",
                "autoscaling:DeleteAutoScalingGroup",
                "autoscaling:TerminateInstanceInAutoScalingGroup",
                "autoscaling:CompleteLifecycleAction",
                "autoscaling:PutLifecycleHook",
                "autoscaling:PutNotificationConfiguration",
                "autoscaling:EnableMetricsCollection"
            ],
            "Resource": "arn:aws:autoscaling:*:*:*:autoScalingGroupName/eks-*"
        },
        {
            "Sid": "AllowAutoscalingToCreateSLR",
            "Effect": "Allow",
            "Condition": {
                "StringEquals": {
                    "iam:AWSServiceName": "autoscaling.amazonaws.com"
                }
            },
            "Action": "iam:CreateServiceLinkedRole",
            "Resource": "*"
        },
        {
            "Sid": "AllowASGCreationByEKS",
            "Effect": "Allow",
            "Action": [
                "autoscaling:CreateOrUpdateTags",
                "autoscaling:CreateAutoScalingGroup"
            ],
            "Resource": "*",
            "Condition": {
                "ForAnyValue:StringEquals": {
                    "aws:TagKeys": [
                        "eks",
                        "eks:cluster-name",
                        "eks:nodegroup-name"
                    ]
                }
            }
        },
        {
            "Sid": "AllowPassRoleToAutoscaling",
            "Effect": "Allow",
            "Action": "iam:PassRole",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "iam:PassedToService": "autoscaling.amazonaws.com"
                }
            }
        },
        {
            "Sid": "AllowPassRoleToEC2",
            "Effect": "Allow",
            "Action": "iam:PassRole",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "iam:PassedToService": [
                        "ec2.amazonaws.com"
                    ]
                }
            }
        },
        {
            "Sid": "PermissionsToManageResourcesForNodegroups",
            "Effect": "Allow",
            "Action": [
                "iam:GetRole",
                "ec2:CreateLaunchTemplate",
                "ec2:DescribeInstances",
                "iam:GetInstanceProfile",
                "ec2:DescribeLaunchTemplates",
                "autoscaling:DescribeAutoScalingGroups",
                "ec2:CreateSecurityGroup",
                "ec2:DescribeLaunchTemplateVersions",
                "ec2:RunInstances",
                "ec2:DescribeSecurityGroups",
                "ec2:GetConsoleOutput",
                "ec2:DescribeRouteTables",
                "ec2:DescribeSubnets"
            ],
            "Resource": "*"
        },
        {
            "Sid": "PermissionsToCreateAndManageInstanceProfiles",
            "Effect": "Allow",
            "Action": [
                "iam:CreateInstanceProfile",
                "iam:DeleteInstanceProfile",
                "iam:RemoveRoleFromInstanceProfile",
                "iam:AddRoleToInstanceProfile"
            ],
            "Resource": "arn:aws:iam::*:instance-profile/eks-*"
        },
        {
            "Sid": "PermissionsToManageEKSAndKubernetesTags",
            "Effect": "Allow",
            "Action": [
                "ec2:CreateTags",
                "ec2:DeleteTags"
            ],
            "Resource": "*",
            "Condition": {
                "ForAnyValue:StringLike": {
                    "aws:TagKeys": [
                        "eks",
                        "eks:cluster-name",
                        "eks:nodegroup-name",
                        "kubernetes.io/cluster/*"
                    ]
                }
            }
        }
    ]
}
```





## Amazon EKS updates to AWS managed policies<a name="security-iam-awsmanpol-updates"></a>



View details about updates to AWS managed policies for Amazon EKS since this service began tracking these changes\. For automatic alerts about changes to this page, subscribe to the RSS feed on the Amazon EKS Document history page\.




| Change | Description | Date | 
| --- | --- | --- | 
|  Updated [AWSServiceRoleForAmazonEKSNodegroup](#security-iam-awsmanpol-AWSServiceRoleForAmazonEKSNodegroup)  |  Removed `ec2.amazonaws.com.cn` and replaced `StringEqualsIfExists` with `StringEquals` from `AllowPassRoleToEC2` to address security concerns\.  | Feb 03, 2022 |
|  Added permissions to [AWSServiceRoleForAmazonEKSNodegroup](#security-iam-awsmanpol-AWSServiceRoleForAmazonEKSNodegroup)  |  Added `autoscaling:EnableMetricsCollection` permission to allow Amazon EKS to enable metrics collection\.  | Dec 13, 2021 | 
|  Added permissions to [AmazonEKSClusterPolicy](#security-iam-awsmanpol-AmazonEKSClusterPolicy)  | Added ec2:DescribeAccountAttributes, ec2:DescribeAddresses, and ec2:DescribeInternetGateways permissions to allow Amazon EKS to create a service\-linked role for a Network Load Balancer\. | June 17, 2021 | 
|  Amazon EKS started tracking changes\.  |  Amazon EKS started tracking changes for its AWS managed policies\.  | June 17, 2021 | 
