# IAM roles for service accounts<a name="iam-roles-for-service-accounts"></a>

Applications in a pod's containers can use an AWS SDK or the AWS CLI to make API requests to AWS services using AWS Identity and Access Management \(IAM\) permissions\. Applications must sign their AWS API requests with AWS credentials\. IAM roles for service accounts provide the ability to manage credentials for your applications, similar to the way that Amazon EC2 instance profiles provide credentials to Amazon EC2 instances\. Instead of creating and distributing your AWS credentials to the containers or using the Amazon EC2 instance's role, you associate an IAM role with a Kubernetes service account and configure your pods to use the service account\. You can't use IAM roles for service accounts with [local clusters for Amazon EKS on AWS Outposts](eks-outposts-local-cluster-overview.md)\.

IAM roles for service accounts provide the following benefits:
+ **Least privilege** – You can scope IAM permissions to a service account, and only pods that use that service account have access to those permissions\. This feature also eliminates the need for third\-party solutions such as `kiam` or `kube2iam`\.
+ **Credential isolation** – A pod's containers can only retrieve credentials for the IAM role that's associated with the service account that the container uses\. A container never has access to credentials that are used by other containers in other pods\. When using IAM roles for service accounts, the pod's containers also have the permissions assigned to the [Amazon EKS node IAM role](create-node-role.md), unless you block pod access to the [Amazon EC2 Instance Metadata Service \(IMDS\)](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html)\. For more information, see [Restrict access to the instance profile assigned to the worker node](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node)\.
+ **Auditability** – Access and event logging is available through AWS CloudTrail to help ensure retrospective auditing\.

Enable IAM roles for service accounts by completing the following procedures:

1. [Creating an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md) – You only complete this procedure once for each cluster\.

1. [Configuring the AWS Security Token Service endpoint for a service account](configure-sts-endpoint.md) – Complete this procedure for each unique set of permissions that you want an application to have\.

1. [Configuring pods to use a Kubernetes service account](pod-configuration.md) – Complete this procedure for each pod that needs access to AWS services\.

**IAM, Kubernetes, and OpenID Connect \(OIDC\) background information**  
In 2014, AWS Identity and Access Management added support for federated identities using OpenID Connect \(OIDC\)\. This feature allows you to authenticate AWS API calls with supported identity providers and receive a valid OIDC JSON web token \(JWT\)\. You can pass this token to the AWS STS `AssumeRoleWithWebIdentity` API operation and receive IAM temporary role credentials\. You can use these credentials to interact with any AWS service, including Amazon S3 and DynamoDB\. 

Kubernetes has long used service accounts as its own internal identity system\. Pods can authenticate with the Kubernetes API server using an auto\-mounted token \(which was a non\-OIDC JWT\) that only the Kubernetes API server could validate\. These legacy service account tokens don't expire, and rotating the signing key is a difficult process\. In Kubernetes version `1.12`, support was added for a new `ProjectedServiceAccountToken` feature\. This feature is an OIDC JSON web token that also contains the service account identity and supports a configurable audience\.

Amazon EKS hosts a public OIDC discovery endpoint for each cluster that contains the signing keys for the `ProjectedServiceAccountToken` JSON web tokens so external systems, such as IAM, can validate and accept the OIDC tokens that are issued by Kubernetes\.