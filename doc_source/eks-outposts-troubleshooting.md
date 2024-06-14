--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Troubleshooting local clusters for Amazon EKS on AWS Outposts<a name="eks-outposts-troubleshooting"></a>

This topic covers some common errors that you might see while using local clusters and how to troubleshoot them\. Local clusters are similar to Amazon EKS clusters in the cloud, but there are some differences in how they’re managed by Amazon EKS\.

## API behavior<a name="outposts-troubleshooting-api-behavior"></a>

Local clusters are created through the Amazon EKS API, but are run in an asynchronous manner\. This means that requests to the Amazon EKS API return immediately for local clusters\. However, these requests might succeed, fail fast because of input validation errors, or fail and have descriptive validation errors\. This behavior is similar to the Kubernetes API\.

Local clusters don’t transition to a `FAILED` status\. Amazon EKS attempts to reconcile the cluster state with the user\-requested desired state in a continuous manner\. As a result, a local cluster might remain in the `CREATING` state for an extended period of time until the underlying issue is resolved\.

## Describe cluster health field<a name="outposts-troubleshooting-describe-cluster-health-field"></a>

Local cluster issues can be discovered using the [describe\-cluster](https://docs.aws.amazon.com/cli/latest/reference/eks/describe-cluster.html) Amazon EKS AWS CLI command\. Local cluster issues are surfaced by the `cluster.health` field of the `describe-cluster` command’s response\. The message contained in this field includes an error code, descriptive message, and related resource IDs\. This information is available through the Amazon EKS API and AWS CLI only\. In the following example, replace *my\-cluster* with the name of your local cluster\.

```
aws eks describe-cluster --name my-cluster --query 'cluster.health'
```

An example output is as follows\.

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

If the problem is beyond repair, you might need to delete the local cluster and create a new one\. For example, trying to provision a cluster with an instance type that’s not available on your Outpost\. The following table includes common health related errors\.

Provided subnets couldn’t be found\.

 `ResourceNotFound` 

 `The subnet ID subnet-id does not exist` 

Provided subnets don’t belong to the same VPC\.

 `ConfigurationConflict` 

 `Subnets specified must belong to the same VPC` 

Some provided subnets don’t belong to the specified Outpost\.

 `ConfigurationConflict` 

 `Subnet subnet-id expected to be in outpost-arn, but is in other-outpost-arn ` 

Some provided subnets don’t belong to any Outpost\.

 `ConfigurationConflict` 

 `Subnet subnet-id is not part of any Outpost` 

Some provided subnets don’t have enough free addresses to create elastic network interfaces for control plane instances\.

 `ResourceLimitExceeded` 

 `The specified subnet does not have enough free addresses to satisfy the request.` 

The specified control plane instance type isn’t supported on your Outpost\.

 `ConfigurationConflict` 

 `The instance type type is not supported in Outpost outpost-arn ` 

 `InternalFailure` 

 `EC2 instance state "Terminated" is unexpected` 

You have insufficient capacity on your Outpost\. This can also happen when a cluster is being created if an Outpost is disconnected from the AWS Region\.

 `ResourceLimitExceeded` 

 `There is not enough capacity on the Outpost to launch or start the instance.` 

 `ResourceLimitExceeded` 

 `ResourceLimitExceeded` 

 `ClusterUnreachable` 

Amazon EKS control plane instances are not reachable through SSM\. Please verify your SSM and network configuration, and reference the EKS on Outposts troubleshooting documentation\.

Based on Amazon EC2 client error code\.

The following table lists errors from other AWS services that are presented in the health field of the `describe-cluster` response\.

 `AuthFailure` 

 `AccessDenied` 

 `UnauthorizedOperation` 

 `AccessDenied` 

 `InvalidSubnetID.NotFound` 

 `ResourceNotFound` 

This error occurs when subnet ID for the ingress rules of a security group can’t be found\.

 `InvalidPermission.NotFound` 

 `ResourceNotFound` 

 `InvalidGroup.NotFound` 

 `ResourceNotFound` 

 `InvalidNetworkInterfaceID.NotFound` 

 `ResourceNotFound` 

 `InsufficientFreeAddressesInSubnet` 

 `ResourceLimitExceeded` 

 `InsufficientCapacityOnOutpost` 

 `ResourceLimitExceeded` 

 `NetworkInterfaceLimitExceeded` 

 `ResourceLimitExceeded` 

This error occurs when the elastic network interface quota is exceeded\.

 `SecurityGroupLimitExceeded` 

 `ResourceLimitExceeded` 

 `VcpuLimitExceeded` 

 `ResourceLimitExceeded` 

 `InvalidParameterValue` 

 `ConfigurationConflict` 

Amazon EC2 returns this error code if the specified instance type isn’t supported on the Outpost\.

 `InternalFailure` 

## Unable to create or modify clusters<a name="outposts-troubleshooting-unable-to-create-or-modify-clusters"></a>

## Cluster is stuck in `CREATING` state<a name="outposts-troubleshooting-cluster-stuck-in-creating-state"></a>

The amount of time it takes to create a local cluster varies depending on several factors\. These factors include your network configuration, Outpost configuration, and the cluster’s configuration\. In general, a local cluster is created and changes to the `ACTIVE` status within 15–20 minutes\. If a local cluster remains in the `CREATING` state, you can call `describe-cluster` for information about the cause in the `cluster.health` output field\.

The most common issues are the following:
+ Your cluster can’t connect to the control plane instance from the AWS Region that Systems Manager is in\. You can verify this by calling `aws ssm start-session --target instance-id ` from an in\-Region bastion host\. If that command doesn’t work, check if Systems Manager is running on the control plane instance\. Or, another work around is to delete the cluster and then recreate it\.
+ Systems Manager control plane instances might not have internet access\. Check if the subnet that you provided when you created the cluster has a NAT gateway and a VPC with an internet gateway\. Use VPC reachability analyzer to verify that the control plane instance can reach the internet gateway\. For more information, see [Getting started with VPC Reachability Analyzer](https://docs.aws.amazon.com/vpc/latest/reachability/getting-started.html)\.
+ All the provided subnets must be associated with the same Outpost and must reach each other\. When multiple subnets are specified when a cluster is created, Amazon EKS attempts to spread the control plane instances across multiple subnets\.
+ The Amazon EKS managed security groups are applied at the elastic network interface\. However, other configuration elements such as NACL firewall rules might conflict with the rules for the elastic network interface\.

## Can’t join nodes to a cluster<a name="outposts-troubleshooting-unable-to-join-nodes-to-a-cluster"></a>
+ AMI issues:
  + If you used an AWS CloudFormation template to create your nodes, make sure it wasn’t using an unsupported AMI\.
+ The wrong security group is used – Make sure to use `eks-cluster-sg-cluster-name-uniqueid ` for your worker nodes' security group\. The selected security group is changed by AWS CloudFormation to allow a new security group each time the stack is used\.
+ Following unexpected private link VPC steps – Wrong CA data \(`--b64-cluster-ca`\) or API Endpoint \(`--apiserver-endpoint`\) are passed\.
+ Misconfigured Pod security policy:
  + The CoreDNS and Amazon VPC CNI plugin for  Kubernetes Daemonsets must run on nodes for nodes to join and communicate with the cluster\.
  + The Amazon VPC CNI plugin for  Kubernetes requires some privileged networking features to work properly\. You can view the privileged networking features with the following command: `kubectl describe psp eks.privileged`\.

## Collecting logs<a name="outposts-troubleshooting-collecting-logs"></a>

## Control plane instances aren’t reachable through AWS Systems Manager<a name="outposts-troubleshooting-control-plane-instances-ssm"></a>

When the Amazon EKS control plane instances aren’t reachable through AWS Systems Manager \(Systems Manager\), Amazon EKS displays the following error for your cluster\.

```
Amazon EKS control plane instances are not reachable through SSM. Please verify your SSM and network configuration, and reference the EKS on Outposts troubleshooting documentation.
```