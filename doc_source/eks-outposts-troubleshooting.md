# Troubleshooting local clusters for Amazon EKS on AWS Outposts<a name="eks-outposts-troubleshooting"></a>

This topic covers some common errors that you may see while using local clusters and how to work around them\. While local clusters are similar to Amazon EKS clusters in the cloud, there are some differences in how a local cluster is managed by the Amazon EKS service\.

## API behavior<a name="outposts-troubleshooting-api-behavior"></a>

Local clusters are created through the Amazon EKS API, but are executed in an asynchronous manner\. This means that requests to the Amazon EKS API return immediately for local clusters, and may succeed, fail fast \(input validation errors\), or fail with descriptive validation errors at a later point during the execution of the request\. This behavior is similar to that of the Kubernetes API\.

Local clusters do not transition to a `FAILED` status\. The Amazon EKS service attempts to reconcile the cluster state with the user\-requested desired state in a continuous manner\. As a result, a local cluster may remain in the `CREATING` state for an extended period of time until the underlying issue is resolved\.

## Describe cluster health field<a name="outposts-troubleshooting-describe-cluster-health-field"></a>

Local cluster issues can be discovered with the [https://docs.aws.amazon.com/cli/latest/reference/eks/describe-cluster.html](https://docs.aws.amazon.com/cli/latest/reference/eks/describe-cluster.html) Amazon EKS AWS CLI command\. Local cluster issues are surfaced by the `cluster.health` field of the `describe-cluster` command's response\. The message contained in this field includes an error code, descriptive message, and related resource IDs\. This information is available through the Amazon EKS API and AWS CLI only\. In the following example, replace *my\-cluster* with the name of your local cluster\.

```
aws eks describe-cluster --name my-cluster --query 'cluster.health'
```

An example of the output that might be returned follows\.

```
{
    "issues": [
        {
            "code": "ConfigurationConflict",
            "message": "The instance type 'm5.large' is not supported in Outpost 'my-outpost-arn'.",
            "resourceIds": [
                "my-cluster-arn"
            ]
        }
    ]
}
```

If the problem is beyond repair, you might need to delete the local cluster and create a new one\. For example, trying to provision a cluster with an instance type that is not available on your Outpost\. The following table includes common health related errors: 


| Error scenario | Code | Message | ResourceIds | 
| --- | --- | --- | --- | 
|  Provided subnets don't exist  |  `ResourceNotFound`  |  `The subnet ID subnet-id does not exist`  | All provided subnet IDs | 
|  Provided subnets don't belong to the same VPC  | `ConfigurationConflict` |  `Subnets specified must belong to the same VPC`  | All provided subnet IDs | 
|  Some provided subnets don't belong to the specified Outpost  | `ConfigurationConflict` | `Subnet subnet-id expected to be in outpost-arn, but is in other-outpost-arn` | Problematic subnet ID | 
|  Some provided subnets don't belong to any Outpost  | `ConfigurationConflict` |  `Subnet subnet-id is not part of any Outpost`  | Problematic subnet ID | 
|  Some provided subnets don't have enough free addresses to support creation of elastic network interfaces for control plane instances  |  `ResourceLimitExceeded`  |  `The specified subnet does not have enough free addresses to satisfy the request.`  | Problematic subnet ID | 
|  The specified control plane instance type isn't supported on your Outpost  | `ConfigurationConflict` |  `The instance type type is not supported in Outpost outpost-arn`  | Cluster ARN | 
| You terminated a control plane Amazon EC2 instance or run\-instance succeeded but the state observed changes to Terminated\. This can happen for a period of time after your Outpost reconnects and Amazon EBS internal errors cause an Amazon EC2 internal work flow to fail\. | `InternalFailure` |  `EC2 instance state "Terminated" is unexpected`  | Cluster ARN | 
|  Insufficient capacity on your Outpost\. This can also happen during cluster creation when an Outpost is disconnected from the AWS Region\.  | `ResourceLimitExceeded` |  `There is not enough capacity on the Outpost to launch or start the instance.`  | Cluster ARN | 
| Your account exceeds your security group limit | `ResourceLimitExceeded` | Error message returned by Amazon EC2 API | Target VPC ID | 
| Your account exceeds your elastic network interface limit | `ResourceLimitExceeded` | Error message returned by Amazon EC2 API | Target subnet ID | 
| Control plane instances aren't reachable through AWS Systems Manager\. For resolution, see [Control plane instances aren't reachable through AWS Systems Manager](#outposts-troubleshooting-control-plane-instances-ssm)\. | `ClusterUnreachable` | Amazon EKS control plane instances are not reachable through SSM\. Please verify your SSM and network configuration, and reference the EKS on Outposts troubleshooting documentation\. | Amazon EC2 instance IDs | 
| There's an error describing a managed security group or elastic network interface |  Based on Amazon EC2 client error code\.  | Error message returned by Amazon EC2 API | All managed security group IDs | 
| There's an error in authorizing or revoking security group ingress rules\. This applies to both the cluster and control plane security groups\. | Based on Amazon EC2 client error code\. | Error message returned by Amazon EC2 API | Problematic security group ID | 
| There's an error deleting an elastic network interface for a control plane instance | Based on Amazon EC2 client error code\. | Error message returned by Amazon EC2 API | Problematic elastic network interface ID | 

The following table lists errors from other AWS services that are presented in the health field of the `describe-cluster` response:


| Amazon EC2 error code | Cluster health issue code | Additional information | 
| --- | --- | --- | 
| `AuthFailure` | `AccessDenied` | These can happen for various reasons\. Most commonly they happen if a tag the service uses to scope down the service linked role policy is accidentally removed from the control plane instance\. If this happens, Amazon EKS loses permission to continue to manage and monitor these AWS resources | 
| `UnauthorizedOperation` | `AccessDenied` | These can happen for various reasons\. Most commonly they happen if a tag the service uses to scope down the service linked role policy is accidentally removed from the control plane instance\. If this happens, Amazon EKS loses permission to continue to manage and monitor these AWS resources | 
| `InvalidSubnetID.NotFound` | `ResourceNotFound` |  Refers to the ingress rules of a security group  | 
| `InvalidPermission.NotFound` | `ResourceNotFound` | Refers to the ingress rules of a security group | 
| `InvalidGroup.NotFound` | `ResourceNotFound` | Refers to the ingress rules of a security group | 
| `InvalidNetworkInterfaceID.NotFound` | `ResourceNotFound` | Refers to the ingress rules of a security group | 
| `InsufficientFreeAddressesInSubnet` | `ResourceLimitExceeded` | Subnet resource limit | 
| `InsufficientCapacityOnOutpost` | `ResourceLimitExceeded` | Outpost capacity limit | 
| `NetworkInterfaceLimitExceeded` | `ResourceLimitExceeded` |  Elastic network interface limit  | 
| `SecurityGroupLimitExceeded` | `ResourceLimitExceeded` | Security group limit | 
| `VcpuLimitExceeded` | `ResourceLimitExceeded` | This is observed when creating an Amazon EC2 instance in a new account\. The error might be similar to "You have requested more vCPU capacity than your current vCPU limit of 32 allows for the instance bucket that the specified instance type belongs to\. Please visit http://aws\.amazon\.com/contact\-us/ec2\-request to request an adjustment to this limit\." | 
| `InvalidParameterValue` | `ConfigurationConflict` |  Amazon EC2 returns this error code if the specified instance type isn't supported on the Outpost\.  | 
| All other failures | `InternalFailure` | None | 

## Unable to create or modify clusters<a name="outposts-troubleshooting-unable-to-create-or-modify-clusters"></a>

Local clusters require different permissions and policies than Amazon EKS clusters in the cloud\. When cluster creation fails with an `InvalidPermissions` result, check to see that the cluster role you are using has the [AmazonEKSLocalOutpostClusterPolicy](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonEKSLocalOutpostClusterPolicy) managed policy attached to it\. All other API calls require the same set of permissions as Amazon EKS clusters in the cloud\.

## Cluster is stuck in `CREATING` state<a name="outposts-troubleshooting-cluster-stuck-in-creating-state"></a>

Local cluster creation time might vary depending on the characteristics of your network configuration, Outpost configuration, and the cluster you are trying to create\. A local cluster should be created and be `ACTIVE` within 15–20 minutes\. If a local cluster remains in the `CREATING` state, a call to `describe-cluster` might provide hints of the cause in the `cluster.health` field\. 

The most common issues follow\.

**AWS Systems Manager \(Systems Manager\)**
+ Unable to connect to the control plane instance from the AWS Region using Systems Manager\. You can verify this by calling `aws ssm start-session --target instance-id` from an in\-region bastion host\. If that fails, determine whether Systems Manager is running on the control plane instance and refer to the AWS Systems Manager User Guide for further help\. Alternatively, you can simply delete this cluster and try to recreate the cluster\.
+ Control plane instances might not have internet access\. Check to see whether the subnet you provided when creating the cluster has a NAT gateway configured and that its VPC has an internet gateway configured\. Use VPC reachability analyzer to verify that the control plane instance can reach the internet gateway\. For more information, see [Getting started with VPC Reachability Analyzer](https://docs.aws.amazon.com/vpc/latest/reachability/getting-started.html)\.
+ The provided role ARN is missing policies\. Check to see if the [AWS managed policy: AmazonEKSLocalOutpostClusterPolicy](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonEKSLocalOutpostClusterPolicy) was removed from the role\. This can also happen due to a misconfigured AWS CloudFormation stack\.

**Multiple subnets misconfigured and specified when creating a cluster**
+ All provided subnets must be associated with the same Outpost and be able to reach each another\. When multiple subnets are specified during cluster creation, Amazon EKS tries to spread the control plane instances across multiple subnets\. 
+ The Amazon EKS managed security groups are applied at the elastic network interface\. There could be other configuration elements that are conflicting with it, such as NACL firewall rules\.

**VPC and subnet DNS configuration is misconfigured or missing**  
Review [Amazon EKS local cluster VPC and subnet requirements and considerations](eks-outposts-vpc-subnet-requirements.md)\.

## Unable to join worker nodes to a cluster<a name="outposts-troubleshooting-unable-to-join-nodes-to-a-cluster"></a>

**Common causes:**
+ AMI issues
  + You're using an unsupported AMI\. You must be using [v20220620](https://github.com/awslabs/amazon-eks-ami/releases/tag/v20220620) or later of an [Amazon EKS optimized Amazon Linux AMIs](eks-optimized-ami.md) Amazon EKS optimized Amazon Linux\.
  + If you used an AWS CloudFormation template to create your nodes, make sure it wasn't using an unsupported AMI\.
+ Missing AWS IAM Authenticator `ConfigMap` – If it's missing, you need to create it\. For more information, see [Apply the `aws-auth``ConfigMap` to your cluster](add-user-role.md#aws-auth-configmap) \.
+ Wrong security group is used – Make sure to use `eks-cluster-sg-cluster-name-uniqueid` for your worker nodes' security group\. The selected security group is changed by AWS CloudFormation to allow a new security group each time the stack is used\.
+ Following unexpected private link VPC steps – Wrong CA data \(`--b64-cluster-ca`\) or API Endpoint \(`--apiserver-endpoint`\) are passed\.
+ Misconfigured pod security policy
  + The CoreDNS and Amazon VPC CNI plugin for Kubernetes Daemonsets must run on nodes for nodes to be able to properly join and communicate with the cluster\.
  + The Amazon VPC CNI plugin for Kubernetes requires some privileged networking features in order to work properly\. You can view the privileged networking features with the following command: `kubectl describe psp eks.privileged`\.

  We recommend that you don't modify the default pod security policy\. For more information, see [Pod security policy](pod-security-policy.md)\.

## Collecting logs<a name="outposts-troubleshooting-collecting-logs"></a>

When an Outpost gets disconnected from its AWS Region, the Kubernetes cluster should continue working normally, but you should be familiar with [Preparing for network disconnects](eks-outposts-network-disconnects.md)\. If you encounter other issues, you should contact AWS support\. It can guide you on how to download and run a log collection tool so that you can collect logs from your Kubernetes cluster control plane instances and send them to AWS support for further investigation\.

## Control plane instances aren't reachable through AWS Systems Manager<a name="outposts-troubleshooting-control-plane-instances-ssm"></a>

When the Amazon EKS control plane instances aren't reachable through AWS Systems Manager \(Systems Manager\), Amazon EKS displays the following error for your cluster\.

```
Amazon EKS control plane instances are not reachable through SSM. Please verify your SSM and network configuration, and reference the EKS on Outposts troubleshooting documentation.
```

To resolve this issue, make sure that your VPC and subnets meet the requirements in [Amazon EKS local cluster VPC and subnet requirements and considerations](eks-outposts-vpc-subnet-requirements.md) and that you have completed the steps in [Setting up Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-getting-started.html) in the AWS Systems Manager User Guide\. 