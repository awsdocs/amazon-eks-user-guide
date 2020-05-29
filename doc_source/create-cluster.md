# Creating an Amazon EKS cluster<a name="create-cluster"></a>

This topic walks you through creating an Amazon EKS cluster\. If this is your first time creating an Amazon EKS cluster, then we recommend that you follow one of our [Getting started with Amazon EKS](getting-started.md) guides instead\. They provide complete end\-to\-end walkthroughs for creating an Amazon EKS cluster with worker nodes\.

**Important**  
When an Amazon EKS cluster is created, the IAM entity \(user or role\) that creates the cluster is added to the Kubernetes RBAC authorization table as the administrator \(with `system:master` permissions\. Initially, only that IAM user can make calls to the Kubernetes API server using kubectl\. For more information, see [Managing users or IAM roles for your cluster](add-user-role.md)\. If you use the console to create the cluster, you must ensure that the same IAM user credentials are in the AWS SDK credential chain when you are running kubectl commands on your cluster\.  
If you install and configure the AWS CLI, you can configure the IAM credentials for your user\. If the AWS CLI version 1\.16\.156 or later is configured properly for your user, then `eksctl` can find those credentials\. For more information, see [Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) in the *AWS Command Line Interface User Guide*\. If you can't install the AWS CLI version 1\.16\.156 or later, then you must install the [https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html](https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html)\.

**Prerequisites**  
You must have the AWS CLI version 1\.16\.156 or later or the `aws-iam-authenticator` installed\. For more information, see [Install the AWS CLI](getting-started-console.md#gs-console-install-awscli) or [Installing `aws-iam-authenticator`](install-aws-iam-authenticator.md)\.

Choose the tab below that corresponds to your desired cluster creation method\.

------
#### [ eksctl ]

This procedure assumes that you have installed `eksctl`, and that your `eksctl` version is at least `0.20.0`\. You can check your version with the following command:

```
eksctl version
```

For more information on installing or upgrading `eksctl`, see [Installing or upgrading `eksctl`](eksctl.md#installing-eksctl)\.

**To create your cluster with `eksctl`**

1. Create a cluster with the Amazon EKS lastest Kubernetes version in your default region\. Replace *my\-cluster* with your own value\.
**Important**  
Kubernetes version 1\.13 is now deprecated on Amazon EKS\. On **June 30th, 2020**, Kubernetes version 1\.13 will no longer be supported on Amazon EKS\. On or after this date, you will no longer be able to create new 1\.13 clusters, and all existing Amazon EKS clusters running Kubernetes version 1\.13 will eventually be automatically updated to version 1\.14\. We recommend that you update any 1\.13 clusters to version 1\.14 or later in order to avoid service interruption\. For more information, see [Amazon EKS version deprecation](kubernetes-versions.md#version-deprecation)\.  
Kubernetes API versions available through Amazon EKS are officially supported by AWS, until we remove the ability to create clusters using that version\. This is true even if upstream Kubernetes is no longer supporting a version available on Amazon EKS\. We backport security fixes that are applicable to the Kubernetes versions supported on Amazon EKS\. Existing clusters are always supported, and Amazon EKS will automatically update your cluster to a supported version if you have not done so manually by the version end of life date\.

   ```
   eksctl create cluster \
    --name my-cluster \
    --version 1.16 \
    --without-nodegroup
   ```

   Cluster provisioning takes several minutes\. During cluster creation, you'll see several lines of output\. The last line of output is similar to the following example line\.

   ```
   [✓]  EKS cluster "my-cluster" in "region-code" region is ready
   ```

1. When your cluster is ready, test that your `kubectl` configuration is correct\.

   ```
   kubectl get svc
   ```
**Note**  
If you receive any authorization or resource type errors, see [Unauthorized or access denied \(`kubectl`\)](troubleshooting.md#unauthorized) in the troubleshooting section\.

   Output:

   ```
   NAME             TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
   svc/kubernetes   ClusterIP   10.100.0.1   <none>        443/TCP   1m
   ```

1. \(Optional\) If you want to run pods on AWS Fargate in your cluster, then you must [Create a Fargate pod execution role](fargate-getting-started.md#fargate-sg-pod-execution-role) and [Create a Fargate profile for your cluster](fargate-getting-started.md#fargate-gs-create-profile)\.

1. Follow the procedures in [Launching Amazon EKS Linux worker nodes](launch-workers.md) to add Linux worker nodes to your cluster to support your workloads\.

1. \(Optional\) After you add Linux worker nodes to your cluster, follow the procedures in [Windows support](windows-support.md) to add Windows support to your cluster and to add Windows worker nodes\. All Amazon EKS clusters must contain at least one Linux worker node, even if you only want to run Windows workloads in your cluster\.

------
#### [ AWS Management Console ]

This procedure has the following prerequisites:
+ You have created a VPC and a dedicated security group that meet the requirements for an Amazon EKS cluster\. For more information, see [Cluster VPC considerations](network_reqs.md) and [Amazon EKS security group considerations](sec-group-reqs.md)\. The [Getting started with the AWS Management Console](getting-started-console.md) guide creates a VPC that meets the requirements, or you can also follow [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md) to create one\.
+ You have created an Amazon EKS cluster IAM role to apply to your cluster\. The [Getting started with Amazon EKS](getting-started.md) guide creates a service role for you, or you can also follow [Amazon EKS IAM roles](security_iam_service-with-iam.md#security_iam_service-with-iam-roles) to create one manually\.

**To create your cluster with the console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose **Create cluster**\.
**Note**  
If your IAM user doesn't have administrative privileges, you must explicitly add permissions for that user to call the Amazon EKS API operations\. For more information, see [Amazon EKS identity\-based policy examples](security_iam_id-based-policy-examples.md)\.

1. On the **Configure cluster** page, fill in the following fields:
   + **Name** – A unique name for your cluster\.
   + **Kubernetes version** – The version of Kubernetes to use for your cluster\.

     Unless you require a specific Kubernetes version for your application, we recommend that you use the latest version available in Amazon EKS\.
**Important**  
Kubernetes version 1\.13 is now deprecated on Amazon EKS\. On **June 30th, 2020**, Kubernetes version 1\.13 will no longer be supported on Amazon EKS\. On or after this date, you will no longer be able to create new 1\.13 clusters, and all existing Amazon EKS clusters running Kubernetes version 1\.13 will eventually be automatically updated to version 1\.14\. We recommend that you update any 1\.13 clusters to version 1\.14 or later in order to avoid service interruption\. For more information, see [Amazon EKS version deprecation](kubernetes-versions.md#version-deprecation)\.  
Kubernetes API versions available through Amazon EKS are officially supported by AWS, until we remove the ability to create clusters using that version\. This is true even if upstream Kubernetes is no longer supporting a version available on Amazon EKS\. We backport security fixes that are applicable to the Kubernetes versions supported on Amazon EKS\. Existing clusters are always supported, and Amazon EKS will automatically update your cluster to a supported version if you have not done so manually by the version end of life date\.
   + **Cluster service role** – Choose the Amazon EKS cluster role to allow the Kubernetes control plane to manage AWS resources on your behalf\. For more information, see [Amazon EKS cluster IAM role](service_IAM_role.md)\.
   + **Secrets encryption** – \(Optional\) Choose to enable envelope encryption of Kubernetes secrets using the AWS Key Management Service \(AWS KMS\)\. If you enable envelope encryption, the Kubernetes secrets are encrypted using the customer master key \(CMK\) that you select\. The CMK must be symmetric, created in the same region as the cluster, and if the CMK was created in a different account, the user must have access to the CMK\. For more information, see [Allowing users in other accounts to use a CMK](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html) in the *AWS Key Management Service Developer Guide*\. Kubernetes secrets encryption with an AWS KMS CMK requires Kubernetes version 1\.13 or later\. If no keys are listed, you must create one first\. For more information, see [Creating keys](https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html)\.
   + **Tags** – \(Optional\) Add any tags to your cluster\. For more information, see [Tagging your Amazon EKS resources](eks-using-tags.md)\.

1. Select **Next**\.

1. On the **Specify networking** page, select values for the following fields:
   + **VPC** – Select an existing VPC to use for your cluster\. If none are listed, then you need to create one first\. For more information, see [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md)\.
   + **Subnets** – By default, the available subnets in the VPC specified in the previous field are preselected\. Select any subnet that you don't want to host cluster resources, such as worker nodes or load balancers\. The subnets must meet the requirements for an Amazon EKS cluster\. For more information, see [Cluster VPC considerations](network_reqs.md)\.
**Important**  
If you select subnets that were created before 03/26/2020 using one of the Amazon EKS AWS CloudFormation VPC templates, be aware of a default setting change that was introduced on 03/26/2020\. For more information, see [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md)\.
   + **Security groups** – The **SecurityGroups** value from the AWS CloudFormation output that you generated with [Create your Amazon EKS cluster VPC](getting-started-console.md#vpc-create)\. This security group has **ControlPlaneSecurityGroup** in the drop\-down name\.
**Important**  
The worker node AWS CloudFormation template modifies the security group that you specify here, so **Amazon EKS strongly recommends that you use a dedicated security group for each cluster control plane \(one per cluster\)**\. If this security group is shared with other resources, you might block or disrupt connections to those resources\.
   + For **Cluster endpoint access** – Choose one of the following options:
     + **Public** – Enables only public access to your cluster's Kubernetes API server endpoint\. Kubernetes API requests that originate from outside of your cluster's VPC use the public endpoint\. By default, access is allowed from any source IP address\. You can optionally restrict access to one or more CIDR ranges such as 192\.168\.0\.0/16, for example, by selecting **Advanced settings** and then selecting **Add source**\.
     + **Private** – Enables only private access to your cluster's Kubernetes API server endpoint\. Kubernetes API requests that originate from within your cluster's VPC use the private VPC endpoint\.
     + **Public and private** – Enables public and private access\.

     For more information about the previous options, see [Modifying cluster endpoint access](cluster-endpoint.md#modify-endpoint-access)\.

1. Select **Next**\.

1. On the **Configure logging** page, you can optionally choose which log types that you want to enable\. By default, each log type is **Disabled**\. For more information, see [Amazon EKS control plane logging](control-plane-logs.md)\.

1. Select **Next**\.

1. On the **Review and create** page, review the information that you entered or selected on the previous pages\. Select **Edit** if you need to make changes to any of your selections\. Once you're satisfied with your settings, select **Create**\. The **Status** field shows **CREATING** until the cluster provisioning process completes\.
**Note**  
You might receive an error that one of the Availability Zones in your request doesn't have sufficient capacity to create an Amazon EKS cluster\. If this happens, the error output contains the Availability Zones that can support a new cluster\. Retry creating your cluster with at least two subnets that are located in the supported Availability Zones for your account\. For more information, see [Insufficient capacity](troubleshooting.md#ICE)\.

   Cluster provisioning usually takes between 10 and 15 minutes\.

1. Now that you have created your cluster, follow the procedures in [Installing `aws-iam-authenticator`](install-aws-iam-authenticator.md) and [Create a `kubeconfig` for Amazon EKS](create-kubeconfig.md) to enable communication with your new cluster\.

1. \(Optional\) If you want to run pods on AWS Fargate in your cluster, see [Getting started with AWS Fargate on Amazon EKS](fargate-getting-started.md)\.

1. After you enable communication, follow the procedures in [Launching Amazon EKS Linux worker nodes](launch-workers.md) to add Linux worker nodes to your cluster to support your workloads\.

1. \(Optional\) After you add Linux worker nodes to your cluster, follow the procedures in [Windows support](windows-support.md) to add Windows support to your cluster and to add Windows worker nodes\. All Amazon EKS clusters must contain at least one Linux worker node, even if you only want to run Windows workloads in your cluster\.

------
#### [ AWS CLI ]

**To create your cluster with the AWS CLI**

This procedure has the following prerequisites:
+ You have created a VPC and a dedicated security group that meets the requirements for an Amazon EKS cluster\. For more information, see [Cluster VPC considerations](network_reqs.md) and [Amazon EKS security group considerations](sec-group-reqs.md)\. The [Getting started with the AWS Management Console](getting-started-console.md) guide creates a VPC that meets the requirements, or you can also follow [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md) to create one\.
+ You have created an Amazon EKS cluster IAM role to apply to your cluster\. The [Getting started with Amazon EKS](getting-started.md) guide creates a service role for you, or you can also follow [Amazon EKS IAM roles](security_iam_service-with-iam.md#security_iam_service-with-iam-roles) to create one manually\.

1. Create your cluster with the following command\. Substitute your cluster name, the Amazon Resource Name \(ARN\) of your Amazon EKS cluster IAM role that you created in [Create your Amazon EKS cluster IAM role](getting-started-console.md#role-create), and the subnet and security group IDs for the VPC that you created in [Create your Amazon EKS cluster VPC](getting-started-console.md#vpc-create)\.
**Important**  
Kubernetes version 1\.13 is now deprecated on Amazon EKS\. On **June 30th, 2020**, Kubernetes version 1\.13 will no longer be supported on Amazon EKS\. On or after this date, you will no longer be able to create new 1\.13 clusters, and all existing Amazon EKS clusters running Kubernetes version 1\.13 will eventually be automatically updated to version 1\.14\. We recommend that you update any 1\.13 clusters to version 1\.14 or later in order to avoid service interruption\. For more information, see [Amazon EKS version deprecation](kubernetes-versions.md#version-deprecation)\.  
Kubernetes API versions available through Amazon EKS are officially supported by AWS, until we remove the ability to create clusters using that version\. This is true even if upstream Kubernetes is no longer supporting a version available on Amazon EKS\. We backport security fixes that are applicable to the Kubernetes versions supported on Amazon EKS\. Existing clusters are always supported, and Amazon EKS will automatically update your cluster to a supported version if you have not done so manually by the version end of life date\.

   ```
   aws eks create-cluster \
      --region region-code \
      --name devel \
      --kubernetes-version 1.16 \
      --role-arn arn:aws:iam::111122223333:role/eks-service-role-AWSServiceRoleForAmazonEKS-EXAMPLEBKZRQR \
      --resources-vpc-config subnetIds=subnet-a9189fe2,subnet-50432629,securityGroupIds=sg-f5c54184
   ```
**Note**  
If your IAM user doesn't have administrative privileges, you must explicitly add permissions for that user to call the Amazon EKS API operations\. For more information, see [Amazon EKS identity\-based policy examples](security_iam_id-based-policy-examples.md)\.

   Output:

   ```
   {
       "cluster": {
           "name": "devel",
           "arn": "arn:aws:eks:region-code:111122223333:cluster/devel",
           "createdAt": 1527785885.159,
           "version": "1.16",
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
You might receive an error that one of the Availability Zones in your request doesn't have sufficient capacity to create an Amazon EKS cluster\. If this happens, the error output contains the Availability Zones that can support a new cluster\. Retry creating your cluster with at least two subnets that are located in the supported Availability Zones for your account\. For more information, see [Insufficient capacity](troubleshooting.md#ICE)\.

   To encrypt the Kubernetes secrets with a customer master key \(CMK\) from AWS Key Management Service \(AWS KMS\), first create a CMK using the [create\-key](https://docs.aws.amazon.com/goto/aws-cli/kms-2014-11-01/CreateKey) operation\.

   ```
   MY_KEY_ARN=$(aws kms create-key --query KeyMetadata.Arn --output text)
   ```
**Note**  
By default, the `create-key` command creates a [symmetric key](https://docs.aws.amazon.com/kms/latest/developerguide/symmetric-asymmetric.html) with a key policy that gives the account's root user admin access on KMS actions and resources. For customers that wish to scope down the permissions, ensure that `kms:DescribeKey` and `kms:CreateGrant` actions are permitted on the key policy for the principal that will be calling the `create-cluster` API.

Additionally, EKS does not support the key policy condition [`kms:GrantIsForAWSResource`](https://docs.aws.amazon.com/kms/latest/developerguide/policy-conditions.html#conditions-kms-grant-is-for-aws-resource). Creating a cluster will not work if this is on the key policy statement. 

   Add the `--encryption-config` parameter to the `aws eks create-cluster` command\. Encryption of Kubernetes secrets can only be enabled when the cluster is created\.

   ```
   --encryption-config '[{"resources":["secrets"],"provider":{"keyArn":"$MY_KEY_ARN"}}]'
   ```

   The `keyArn` member can contain either the alias or ARN of your CMK\. The CMK must be symmetric, created in the same Region as the cluster, and if the CMK was created in a different account, the user must have access to the CMK\. For more information, see [Allowing users in other accounts to use a CMK](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html) in the *AWS Key Management Service Developer Guide*\. For CMKs created in a different account, ensure that `kms:CreateGrant` is an allowed action in the key policy. Kubernetes secrets encryption with an AWS KMS CMK requires Kubernetes version 1\.13 or later\.

**Important**  
Deletion of the customer master key \(CMK\) will permanently put the cluster in a degraded state. If any customer master keys used for cluster creation are scheduled for deletion, please double check and verify that this is the intended action. Once the key is deleted, there is no path to recovery for the cluster. 

1. Cluster provisioning usually takes between 10 and 15 minutes\. You can query the status of your cluster with the following command\. When your cluster status is `ACTIVE`, you can proceed\.

   ```
   aws eks --region region-code describe-cluster --name devel --query "cluster.status"
   ```

2. When your cluster provisioning is complete, retrieve the `endpoint` and `certificateAuthority.data` values with the following commands\. You must add these values to your kubectl configuration so that you can communicate with your cluster\.

   1. Retrieve the `endpoint`\.

      ```
      aws eks --region region-code describe-cluster --name devel  --query "cluster.endpoint" --output text
      ```

   2. Retrieve the `certificateAuthority.data`\.

      ```
      aws eks --region region-code describe-cluster --name devel  --query "cluster.certificateAuthority.data" --output text
      ```

3. Now that you have created your cluster, follow the procedures in [Create a `kubeconfig` for Amazon EKS](create-kubeconfig.md) to enable communication with your new cluster\.

4. \(Optional\) If you want to run pods on AWS Fargate in your cluster, see [Getting started with AWS Fargate on Amazon EKS](fargate-getting-started.md)\.

5. After you enable communication, follow the procedures in [Launching Amazon EKS Linux worker nodes](launch-workers.md) to add worker nodes to your cluster to support your workloads\.

6. \(Optional\) After you add Linux worker nodes to your cluster, follow the procedures in [Windows support](windows-support.md) to add Windows support to your cluster and to add Windows worker nodes\. All Amazon EKS clusters must contain at least one Linux worker node, even if you only want to run Windows workloads in your cluster\.

------
