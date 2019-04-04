# Creating an Amazon EKS Cluster<a name="create-cluster"></a>

This topic walks you through creating an Amazon EKS cluster\.

If this is your first time creating an Amazon EKS cluster, we recommend that you follow our [Getting Started with Amazon EKS](getting-started.md) guide instead\. It provides a complete end\-to\-end walkthrough from creating an Amazon EKS cluster to deploying a sample Kubernetes application\.

This topic has the following prerequisites:
+ You have created a VPC and a dedicated security group that meets the requirements for an Amazon EKS cluster\. For more information, see [Cluster VPC Considerations](network_reqs.md) and [Cluster Security Group Considerations](sec-group-reqs.md)\. The [Getting Started with Amazon EKS](getting-started.md) guide creates a VPC that meets the requirements, or you can also follow [Tutorial: Creating a VPC with Public and Private Subnets for Your Amazon EKS Cluster](create-public-private-vpc.md) to create one manually\.
+ You have created an Amazon EKS service role to apply to your cluster\. The [Getting Started with Amazon EKS](getting-started.md) guide creates a service role for you, or you can also follow [Amazon EKS Service IAM Role](service_IAM_role.md) to create one manually\.

**Important**  
When an Amazon EKS cluster is created, the IAM entity \(user or role\) that creates the cluster is added to the Kubernetes RBAC authorization table as the administrator \(with `system:master` permissions\. Initially, only that IAM user can make calls to the Kubernetes API server using kubectl\. For more information, see [Managing Users or IAM Roles for your Cluster](add-user-role.md)\. Also, the [AWS IAM Authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator) uses the AWS SDK for Go to authenticate against your Amazon EKS cluster\. If you use the console to create the cluster, you must ensure that the same IAM user credentials are in the AWS SDK credential chain when you are running kubectl commands on your cluster\.  
If you install and configure the AWS CLI, you can configure the IAM credentials for your user\. These also work for the [AWS IAM Authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator)\. If the AWS CLI is configured properly for your user, the [AWS IAM Authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator) can find those credentials as well\. For more information, see [Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) in the *AWS Command Line Interface User Guide*\.

**To create your cluster with the console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose **Create cluster**\.
**Note**  
If your IAM user doesn't have administrative privileges, you must explicitly add permissions for that user to call the Amazon EKS API operations\. For more information, see [Creating Amazon EKS IAM Policies](EKS_IAM_user_policies.md)\.

1. On the **Create cluster** page, fill in the following fields and then choose **Create**:
   + **Cluster name** – A unique name for your cluster\.
   + **Kubernetes version** – The version of Kubernetes to use for your cluster\. By default, the latest available version is selected\.
   + **Role name** – Choose the Amazon EKS service role to allow Amazon EKS and the Kubernetes control plane to manage AWS resources on your behalf\. For more information, see [Amazon EKS Service IAM Role](service_IAM_role.md)\.
   + **VPC** – The VPC to use for your cluster\.
   + **Subnets** – The subnets within the preceding VPC to use for your cluster\. By default, the available subnets in the VPC are preselected\. Your subnets must meet the requirements for an Amazon EKS cluster\. For more information, see [Cluster VPC Considerations](network_reqs.md)\.
   + **Security Groups** – Specify one or more \(up to a limit of 5\) security groups within the preceding VPC to apply to the cross\-account elastic network interfaces for your cluster\. Your cluster and worker node security groups must meet the requirements for an Amazon EKS cluster\. For more information, see [Cluster Security Group Considerations](sec-group-reqs.md)\.
**Important**  
The worker node AWS CloudFormation template modifies the security group that you specify here, so **Amazon EKS strongly recommends that you use a dedicated security group for each cluster control plane \(one per cluster\)**\. If this security group is shared with other resources, you might block or disrupt connections to those resources\.
   + **Endpoint private access** – Choose whether to enable or disable private access for your cluster's Kubernetes API server endpoint\. If you enable private access, Kubernetes API requests that originate from within your cluster's VPC use the private VPC endpoint\. For more information, see [Amazon EKS Cluster Endpoint Access Control](cluster-endpoint.md)\.
   + **Endpoint public access** – Choose whether to enable or disable public access for your cluster's Kubernetes API server endpoint\. If you disable public access, your cluster's Kubernetes API server can receive only requests from within the cluster VPC\. For more information, see [Amazon EKS Cluster Endpoint Access Control](cluster-endpoint.md)\.
   + **Logging** – For each individual log type, choose whether the log type should be **Enabled** or **Disabled**\. By default, each log type is **Disabled**\. For more information, see [Amazon EKS Control Plane Logging](control-plane-logs.md)\.
**Note**  
You might receive an error that one of the Availability Zones in your request doesn't have sufficient capacity to create an Amazon EKS cluster\. If this happens, the error output contains the Availability Zones that can support a new cluster\. Retry creating your cluster with at least two subnets that are located in the supported Availability Zones for your account\. For more information, see [Insufficient Capacity](troubleshooting.md#ICE)\.

1. On the **Clusters** page, choose the name of your new cluster to view the cluster information\.

1. The **Status** field shows **CREATING** until the cluster provisioning process completes\. When your cluster provisioning is complete \(usually between 10 and 15 minutes\), note the **API server endpoint** and **Certificate authority** values\. These are used in your kubectl configuration\.

1. Now that you have created your cluster, follow the procedures in [Installing `aws-iam-authenticator`](install-aws-iam-authenticator.md) and [Create a `kubeconfig` for Amazon EKS](create-kubeconfig.md) to enable communication with your new cluster\.

**To create your cluster with the AWS CLI**

1. Create your cluster with the following command\. Substitute your cluster name, the Amazon Resource Name \(ARN\) of your Amazon EKS service role that you created in [Create your Amazon EKS Service Role](getting-started.md#role-create), and the subnet and security group IDs for the VPC that you created in [Create your Amazon EKS Cluster VPC](getting-started.md#vpc-create)\.

   ```
   aws eks --region region create-cluster --name devel \
   --role-arn arn:aws:iam::111122223333:role/eks-service-role-AWSServiceRoleForAmazonEKS-EXAMPLEBKZRQR \
   --resources-vpc-config subnetIds=subnet-a9189fe2,subnet-50432629,securityGroupIds=sg-f5c54184
   ```
**Important**  
If you receive a syntax error similar to the following, you might be using a preview version of the AWS CLI for Amazon EKS\. The syntax for many Amazon EKS commands has changed since the public service launch\. Update your AWS CLI version to the latest available and delete the custom service model directory at `~/.aws/models/eks`\.  

   ```
   aws: error: argument --cluster-name is required
   ```
**Note**  
If your IAM user doesn't have administrative privileges, you must explicitly add permissions for that user to call the Amazon EKS API operations\. For more information, see [Creating Amazon EKS IAM Policies](EKS_IAM_user_policies.md)\.

   Output:

   ```
   {
       "cluster": {
           "name": "devel",
           "arn": "arn:aws:eks:us-west-2:111122223333:cluster/devel",
           "createdAt": 1527785885.159,
           "version": "1.10",
           "roleArn": "arn:aws:iam::111122223333:role/eks-service-role-AWSServiceRoleForAmazonEKS-AFNL4H8HB71F",
           "resourcesVpcConfig": {
               "subnetIds": [
                   "subnet-a9189fe2",
                   "subnet-50432629"
               ],
               "securityGroupIds": [
                   "sg-f5c54184"
               ],
               "vpcId": "vpc-a54041dc",
               "endpointPublicAccess": true,
               "endpointPrivateAccess": false
           },
           "status": "CREATING",
           "certificateAuthority": {}
       }
   }
   ```
**Note**  
You might receive an error that one of the Availability Zones in your request doesn't have sufficient capacity to create an Amazon EKS cluster\. If this happens, the error output contains the Availability Zones that can support a new cluster\. Retry creating your cluster with at least two subnets that are located in the supported Availability Zones for your account\. For more information, see [Insufficient Capacity](troubleshooting.md#ICE)\.

1. Cluster provisioning usually takes between 10 and 15 minutes\. You can query the status of your cluster with the following command\. When your cluster status is `ACTIVE`, you can proceed\.

   ```
   aws eks --region region describe-cluster --name devel --query cluster.status
   ```

1. When your cluster provisioning is complete, retrieve the `endpoint` and `certificateAuthority.data` values with the following commands\. You must add these values to your kubectl configuration so that you can communicate with your cluster\.

   1. Retrieve the `endpoint`\.

      ```
      aws eks --region region describe-cluster --name devel  --query cluster.endpoint --output text
      ```

   1. Retrieve the `certificateAuthority.data`\.

      ```
      aws eks --region region describe-cluster --name devel  --query cluster.certificateAuthority.data --output text
      ```

1. Now that you have created your cluster, follow the procedures in [Installing `aws-iam-authenticator`](install-aws-iam-authenticator.md) and [Create a `kubeconfig` for Amazon EKS](create-kubeconfig.md) to enable communication with your new cluster\.