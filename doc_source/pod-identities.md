# EKS Pod Identities<a name="pod-identities"></a>

Applications in a Pod's containers can use an AWS SDK or the AWS CLI to make API requests to AWS services using AWS Identity and Access Management \(IAM\) permissions\. Applications must sign their AWS API requests with AWS credentials\.

*EKS Pod Identities* provide the ability to manage credentials for your applications, similar to the way that Amazon EC2 instance profiles provide credentials to Amazon EC2 instances\. Instead of creating and distributing your AWS credentials to the containers or using the Amazon EC2 instance's role, you associate an IAM role with a Kubernetes service account and configure your Pods to use the service account\.

Each EKS Pod Identity association maps a role to a service account in a namespace in the specified cluster\. If you have the same application in multiple clusters, you can make identical associations in each cluster without modifying the trust policy of the role\.

If a pod uses a service account that has an association, Amazon EKS sets environment variables in the containers of the pod\. The environment variables configure the AWS SDKs, including the AWS CLI, to use the EKS Pod Identity credentials\.

## Benefits of EKS Pod Identities<a name="pod-id-benefits"></a>

EKS Pod Identities provide the following benefits:
+ **Least privilege** – You can scope IAM permissions to a service account, and only Pods that use that service account have access to those permissions\. This feature also eliminates the need for third\-party solutions such as `kiam` or `kube2iam`\.
+ **Credential isolation** – A Pod's containers can only retrieve credentials for the IAM role that's associated with the service account that the container uses\. A container never has access to credentials that are used by other containers in other Pods\. When using Pod Identities, the Pod's containers also have the permissions assigned to the [Amazon EKS node IAM role](create-node-role.md), unless you block Pod access to the [Amazon EC2 Instance Metadata Service \(IMDS\)](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html)\. For more information, see [Restrict access to the instance profile assigned to the worker node](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node)\.
+ **Auditability** – Access and event logging is available through AWS CloudTrail to help facilitate retrospective auditing\.

EKS Pod Identity is a simpler method than [IAM roles for service accounts](iam-roles-for-service-accounts.md), as this method doesn't use OIDC identity providers\. EKS Pod Identity has the following enhancements:
+ **Independent operations** – In many organizations, creating OIDC identity providers is a responsibility of different teams than administering the Kubernetes clusters\. EKS Pod Identity has clean separation of duties, where all configuration of EKS Pod Identity associations is done in Amazon EKS and all configuration of the IAM permissions is done in IAM\.
+ **Reusability** – EKS Pod Identity uses a single IAM principal instead of the separate principals for each cluster that IAM roles for service accounts use\. Your IAM administrator adds the following principal to the trust policy of any role to make it usable by EKS Pod Identities\.

  ```
              "Principal": {
                  "Service": "pods.eks.amazonaws.com"
              }
  ```
+ **Scalability** – Each set of temporary credentials are assumed by the EKS Auth service in EKS Pod Identity, instead of each AWS SDK that you run in each pod\. Then, the Amazon EKS Pod Identity Agent that runs on each node issues the credentials to the SDKs\. Thus the load is reduced to once for each node and isn't duplicated in each pod\. For more details of the process, see [How EKS Pod Identity works](pod-id-how-it-works.md)\.

For more information to compare the two alternatives, see [Grant Kubernetes workloads access to AWS using Kubernetes Service Accounts](service-accounts.md)\.

## Overview of setting up EKS Pod Identities<a name="pod-id-setup-overview"></a>

Turn on EKS Pod Identities by completing the following procedures:

1. [Set up the Amazon EKS Pod Identity Agent](pod-id-agent-setup.md) – You only complete this procedure once for each cluster\.

1. [Configure a Kubernetes service account to assume an IAM role with EKS Pod Identity](pod-id-association.md) – Complete this procedure for each unique set of permissions that you want an application to have\.

   

1. [Configure Pods to use a Kubernetes service account](pod-id-configure-pods.md) – Complete this procedure for each Pod that needs access to AWS services\.

1. [Using a supported AWS SDK](pod-id-minimum-sdk.md) – Confirm that the workload uses an AWS SDK of a supported version and that the workload uses the default credential chain\.

## EKS Pod Identity considerations<a name="pod-id-considerations"></a>
+ You can associate one IAM role to each Kubernetes service account in each cluster\. You can change which role is mapped to the service account by editing the EKS Pod Identity association\.
+ You can only associate roles that are in the same AWS account as the cluster\. You can delegate access from another account to the role in this account that you configure for EKS Pod Identities to use\. For a tutorial about delegating access and `AssumeRole`, see [Delegate access across AWS accounts using IAM roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_cross-account-with-roles.html) in the *IAM User Guide*\.
+ The EKS Pod Identity Agent is required\. It runs as a Kubernetes `DaemonSet` on your nodes and only provides credentials to pods on the node that it runs on\. For more information about EKS Pod Identity Agent compatibility, see the following section [EKS Pod Identity restrictions](#pod-id-restrictions)\.
+ The EKS Pod Identity Agent uses the `hostNetwork` of the node and it uses port `80` and port `2703` on a link\-local address on the node\. This address is `169.254.170.23` for IPv4 and `[fd00:ec2::23]` for IPv6 clusters\.

### EKS Pod Identity cluster versions<a name="pod-id-cluster-versions"></a>

 To use EKS Pod Identities, the cluster must have a platform version that is the same or later than the version listed in the following table, or a Kubernetes version that is later than the versions listed in the table\.


| Kubernetes version | Platform version | 
| --- | --- | 
| 1\.28 | eks\.4 | 
| 1\.27 | eks\.8 | 
| 1\.26 | eks\.9 | 
| 1\.25 | eks\.10 | 
| 1\.24 | eks\.13 | 

### EKS Pod Identity restrictions<a name="pod-id-restrictions"></a>

EKS Pod Identities are available on the following:
+ Amazon EKS cluster versions listed in the previous topic [EKS Pod Identity cluster versions](#pod-id-cluster-versions)\.
+ Worker nodes in the cluster that are Linux Amazon EC2 instances\.

EKS Pod Identities aren't available on the following:
+ China Regions\.
+ AWS GovCloud \(US\)\.
+ AWS Outposts\.
+ Amazon EKS Anywhere\.
+ Kubernetes clusters that you create and run on Amazon EC2\. The EKS Pod Identity components are only available on Amazon EKS\.

You can't use EKS Pod Identities with:
+ Pods that run anywhere except Linux Amazon EC2 instances\. Linux and Windows pods that run on AWS Fargate \(Fargate\) aren't supported\. Pods that run on Windows Amazon EC2 instances aren't supported\.
+ *Amazon EKS add\-ons* that need IAM credentials\. The EKS add\-ons can only use *IAM roles for service accounts* instead\. The list of EKS add\-ons that use IAM credentials include:
  + Amazon VPC CNI plugin for Kubernetes
  + AWS Load Balancer Controller
  + The CSI storage drivers: EBS CSI, EFS CSI, Amazon FSx for Lustre CSI driver, Amazon FSx for NetApp ONTAP CSI driver, Amazon FSx for OpenZFS CSI driver, Amazon File Cache CSI driver
**Note**  
If these controllers, drivers, and plugins are installed as self\-managed add\-ons instead of EKS add\-ons, they support EKS Pod Identities as long as they are updated to use the latest AWS SDKs\.