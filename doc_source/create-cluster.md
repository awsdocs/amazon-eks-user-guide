# Creating an Amazon EKS cluster<a name="create-cluster"></a>

This topic walks you through creating an Amazon EKS cluster\. If this is your first time creating an Amazon EKS cluster, then we recommend that you follow one of our [Getting started with Amazon EKS](getting-started.md) guides instead\. They provide complete end\-to\-end walkthroughs for creating an Amazon EKS cluster with nodes\.

To connect an external Kubernetes cluster to view in Amazon EKS, see [Amazon EKS Connector](eks-connector.md)\.

**Important**  
When an Amazon EKS cluster is created, the IAM entity \(user or role\) that creates the cluster is added to the Kubernetes RBAC authorization table as the administrator \(with `system:masters` permissions\)\. Initially, only that IAM user can make calls to the Kubernetes API server using `kubectl`\. For more information, see [Enabling IAM user and role access to your cluster](add-user-role.md)\. If you use the console to create the cluster, you must ensure that the same IAM user credentials are in the AWS SDK credential chain when you are running `kubectl` commands on your cluster\.

You can create a cluster with `eksctl`, the AWS Management Console, or the AWS CLI\.

------
#### [ eksctl ]

**Prerequisite**  
`eksctl` version 0\.77\.0 or later installed\. To install it or upgrade, see [The `eksctl` command line utility](eksctl.md)\.

Create an Amazon EKS cluster with the Amazon EKS latest Kubernetes version in your default Region\. Replace the `example-values` with your own values\. You can replace `1.21` with any [supported version](kubernetes-versions.md)\.

```
eksctl create cluster \
 --name my-cluster \
 --version 1.21 \
 --without-nodegroup
```

\(Optional\) Add the **\-\-with\-oidc** flag to the previous command to automatically create an [AWS Identity and Access Management \(IAM\) OIDC provider](enable-iam-roles-for-service-accounts.md) for your cluster\. Creating the OIDC provider allows some Amazon EKS add\-ons or your own individual Kubernetes workloads to have specific AWS Identity and Access Management \(IAM\) permissions\. You only need to create an IAM OIDC provider for your cluster once\. To learn more about Amazon EKS add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\. To learn more about assigning specific IAM permissions to your workloads, see [Technical overview](iam-roles-for-service-accounts-technical-overview.md)\. 

**Tip**  
To see most options that can be specified when creating a cluster with `eksctl`, use the **eksctl create cluster \-\-help** command\. To see all options, you can use a config file\. For more information, see [Using config files](https://eksctl.io/usage/creating-and-managing-clusters/#using-config-files) and the [config file schema](https://eksctl.io/usage/schema/) in the `eksctl` documentation\. You can find [config file examples](https://github.com/weaveworks/eksctl/tree/master/examples) on GitHub\.

**Important**  
If you plan to deploy self\-managed nodes in AWS Outposts, AWS Wavelength, or AWS Local Zones after your cluster is deployed, you must have an existing VPC that meets Amazon EKS requirements and use the **\-\-vpc\-private\-subnets** option with the previous command\. The subnet IDs that you specify can't be the AWS Outposts, AWS Wavelength, or AWS Local Zones subnets\. For more information about using an existing VPC, see [Use existing VPC: other custom configuration](https://eksctl.io/usage/vpc-networking/#use-existing-vpc-other-custom-configuration) in the `eksctl` documentation\.

**Warning**  
There is a [https://github.com/weaveworks/eksctl/blob/master/examples/19-kms-cluster.yaml](https://github.com/weaveworks/eksctl/blob/master/examples/19-kms-cluster.yaml) option that requires an existing AWS KMS key in AWS Key Management Service \(AWS KMS\)\. If you create a cluster using a config file with the `secretsEncryption` option and the KMS key that you use is ever deleted, then there is no path to recovery for the cluster\. If you enable [secrets encyption](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/), the Kubernetes secrets are encrypted using the KMS key that you select\. The KMS key must be symmetric, created in the same Region as the cluster, and if the KMS key was created in a different account, the user must have access to the KMS key\. For more information, see [Allowing users in other accounts to use a KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html) in the *[AWS Key Management Service Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/)*\.  
By default, the `create-key` command creates a [symmetric key](https://docs.aws.amazon.com/kms/latest/developerguide/symmetric-asymmetric.html) with a key policy that gives the account root admin access on AWS KMS actions and resources\. For more information, see [Creating keys](https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html)\. If you want to scope down the permissions, make sure that the `kms:DescribeKey` and `kms:CreateGrant` actions are permitted on the policy for the principal that will be calling the `create-cluster` API\. Amazon EKS does not support the policy condition `[kms:GrantIsForAWSResource](https://docs.aws.amazon.com/kms/latest/developerguide/policy-conditions.html#conditions-kms-grant-is-for-aws-resource)`\. Creating a cluster will not work if this action is in the KMS key policy statement\.

Cluster provisioning takes several minutes\. During cluster creation, you'll see several lines of output\. The last line of output is similar to the following example line\.

```
[✓]  EKS cluster "my-cluster" in "region-code" region is ready
```

After your 1\.18 or later cluster is created, you can migrate the Amazon VPC CNI, CoreDNS, and `kube-proxy` add\-ons that were deployed with your cluster to Amazon EKS add\-ons\. For more information, see [Amazon EKS add\-ons](eks-add-ons.md)\.

------
#### [ AWS Management Console ]<a name="create-cluster-prerequisites"></a>

**Prerequisites**
+ An existing VPC and a dedicated security group that meet the requirements for an Amazon EKS cluster\. For more information, see [Cluster VPC considerations](network_reqs.md) and [Amazon EKS security group considerations](sec-group-reqs.md)\. If you don't have a VPC, you can follow [Creating a VPC for your Amazon EKS cluster](creating-a-vpc.md) to create one\.
+ An existing Amazon EKS cluster IAM role\. If you don't have the role, you can follow [Amazon EKS IAM roles](security_iam_service-with-iam.md#security_iam_service-with-iam-roles) to create one\.

**To create your cluster with the console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose **Create cluster**\.

1. On the **Configure cluster** page, fill in the following fields:
   + **Name** – A unique name for your cluster\.
   + **Kubernetes version** – The version of Kubernetes to use for your cluster\. 
   + **Cluster Service Role** – Choose the Amazon EKS cluster role to allow the Kubernetes control plane to manage AWS resources on your behalf\. For more information, see [Amazon EKS cluster IAM role](service_IAM_role.md)\.
   + **Secrets encryption** – \(Optional\) Choose to enable [secrets encyption](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) of Kubernetes secrets using a KMS key\. The KMS key must be symmetric, created in the same region as the cluster, and if the KMS key was created in a different account, the user must have access to the KMS key\. For more information, see [Allowing users in other accounts to use a KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html) in the *[AWS Key Management Service Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/)*\.

     If no keys are listed, you must create one first\. For more information, see [Creating keys](https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html)\.
**Note**  
By default, the `create-key` command creates a [symmetric key](https://docs.aws.amazon.com/kms/latest/developerguide/symmetric-asymmetric.html) with a key policy that gives the account root admin access on AWS KMS actions and resources\. For more information, see [Creating keys](https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html)\. If you want to scope down the permissions, make sure that the `kms:DescribeKey` and `kms:CreateGrant` actions are permitted on the policy for the principal that will be calling the `create-cluster` API\.  
 Amazon EKS does not support the policy condition `[kms:GrantIsForAWSResource](https://docs.aws.amazon.com/kms/latest/developerguide/policy-conditions.html#conditions-kms-grant-is-for-aws-resource)`\. Creating a cluster will not work if this action is in the KMS key policy statement\.
**Warning**  
Deletion of the KMS key will permanently put the cluster in a degraded state\. If any KMS keys used for cluster creation are scheduled for deletion, verify that this is the intended action before deletion\. Once the KMS key is deleted, there is no path to recovery for the cluster\. For more information, see [Deleting AWS KMS keys](https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html)\.
   + **Tags** – \(Optional\) Add any tags to your cluster\. For more information, see [Tagging your Amazon EKS resources](eks-using-tags.md)\.

1. Select **Next**\.

1. On the **Specify networking** page, select values for the following fields:
   + **VPC** – Select an existing VPC to use for your cluster\. If none are listed, then you need to create one first\. For more information, see [Creating a VPC for your Amazon EKS cluster](creating-a-vpc.md)\.
   + **Subnets** – By default, the available subnets in the VPC specified in the previous field are preselected\. Unselect any subnet that you don't want to host cluster resources, such as worker nodes or load balancers\. The subnets must meet the requirements for an Amazon EKS cluster\. For more information, see [Cluster VPC considerations](network_reqs.md)\.
**Important**  
If you select subnets that were created before March 26, 2020 using one of the Amazon EKS AWS CloudFormation VPC templates, be aware of a default setting change that was introduced on March 26, 2020\. For more information, see [Creating a VPC for your Amazon EKS cluster](creating-a-vpc.md)\.
Don't select subnets in AWS Outposts, AWS Wavelength or AWS Local Zones\. If you plan to deploy self\-managed nodes in AWS Outposts, AWS Wavelength or AWS Local Zones subnets after you deploy your cluster, then make sure that you have, or can create, Outposts subnets in the VPC that you select\.

     **Security groups** – The **SecurityGroups** value from the AWS CloudFormation output that you generated when you created your [VPC](creating-a-vpc.md)\. This security group has **ControlPlaneSecurityGroup** in the drop\-down name\.
**Important**  
The node AWS CloudFormation template modifies the security group that you specify here, so **Amazon EKS strongly recommends that you use a dedicated security group for each cluster control plane \(one per cluster\)**\. If this security group is shared with other resources, you might block or disrupt connections to those resources\.
   + \(Optional\) Choose **Configure Kubernetes Service IP address range** and specify a **Service IPv4 range** if you want to specify which CIDR block Kubernetes assigns service IP addresses from\. The CIDR block must meet the following requirements:
     + Within one of the following ranges: 10\.0\.0\.0/8, 172\.16\.0\.0/12, or 192\.168\.0\.0/16\.
     + Between /24 and /12\.
     + Doesn't overlap with any CIDR block specified in your VPC\.

     We recommend specifying a CIDR block that doesn't overlap with any other networks that are peered or connected to your VPC\. If you don't enable this, Kubernetes assigns service IP addresses from either the 10\.100\.0\.0/16 or 172\.20\.0\.0/16 CIDR blocks\.
**Important**  
You can only specify a custom CIDR block when you create a cluster and can't change this value once the cluster is created\.
   + For **Cluster endpoint access** – Choose one of the following options:
     + **Public** – Enables only public access to your cluster's Kubernetes API server endpoint\. Kubernetes API requests that originate from outside of your cluster's VPC use the public endpoint\. By default, access is allowed from any source IP address\. You can optionally restrict access to one or more CIDR ranges such as 192\.168\.0\.0/16, for example, by selecting **Advanced settings** and then selecting **Add source**\.
     + **Private** – Enables only private access to your cluster's Kubernetes API server endpoint\. Kubernetes API requests that originate from within your cluster's VPC use the private VPC endpoint\. 
**Important**  
If you created a VPC without outbound internet access, then you must enable private access\.
     + **Public and private** – Enables public and private access\.

     For more information about the previous options, see [Modifying cluster endpoint access](cluster-endpoint.md#modify-endpoint-access)\.

1. If you selected Kubernetes version 1\.17 or earlier on the previous page, skip to the next step\. If you selected version 1\.18 or later, you can accept the defaults in the **Networking add\-ons** section to install the default version of the [AWS VPC CNI](pod-networking.md), [CoreDNS](managing-coredns.md), and [kube\-proxy](managing-kube-proxy.md) Amazon EKS add\-ons, or you can select a different version\. If you don't require the functionality of any of the add\-ons, you can remove them once your cluster is created\.

   You can only use Amazon EKS add\-ons with 1\.18 or later clusters because Amazon EKS add\-ons require the Server\-side Apply Kubernetes feature, which wasn't available until Kubernetes 1\.18\. If you selected a different Kubernetes version for your cluster, then this option isn't shown\.
**Important**  
The AWS VPC CNI add\-on is configured to use the IAM permissions assigned to the [Amazon EKS node IAM role](create-node-role.md)\. After the cluster is created, but before you deploy any Amazon EC2 nodes to your cluster, you must ensure that the `AmazonEKS_CNI_Policy` IAM policy is attached to either the node IAM role, or to a different role associated to the Kubernetes service account that the add\-on runs as\. We recommend that you assign the policy to a different IAM role than the node IAM role by completing the instructions in [Configuring the Amazon VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\. Once your cluster and IAM role are created, you can [update the add\-on](managing-vpc-cni.md#updating-vpc-cni-eks-add-on) to use the IAM role that you create\.

1. Select **Next**\.

1. On the **Configure logging** page, you can optionally choose which log types that you want to enable\. By default, each log type is **Disabled**\. For more information, see [Amazon EKS control plane logging](control-plane-logs.md)\.

1. Select **Next**\.

1. On the **Review and create** page, review the information that you entered or selected on the previous pages\. Select **Edit** if you need to make changes to any of your selections\. Once you're satisfied with your settings, select **Create**\. The **Status** field shows **CREATING** until the cluster provisioning process completes\.
**Note**  
You might receive an error that one of the Availability Zones in your request doesn't have sufficient capacity to create an Amazon EKS cluster\. If this happens, the error output contains the Availability Zones that can support a new cluster\. Retry creating your cluster with at least two subnets that are located in the supported Availability Zones for your account\. For more information, see [Insufficient capacity](troubleshooting.md#ICE)\.

   Cluster provisioning takes several minutes\.

1. Follow the procedures in [Create a `kubeconfig` for Amazon EKS](create-kubeconfig.md) to enable communication with your new cluster\.

1. \(Optional\) To use some Amazon EKS add\-ons, or to enable individual Kubernetes workloads to have specific AWS Identity and Access Management \(IAM\) permissions, you need to create an IAM OpenID Connect \(OIDC\) provider for your cluster\. To create an IAM OIDC provider for your cluster, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\. You only need to create an IAM OIDC provider for your cluster once\. To learn more about Amazon EKS add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\. To learn more about assigning specific IAM permissions to your workloads, see [Technical overview](iam-roles-for-service-accounts-technical-overview.md)\. 

1. If you're going to deploy Amazon EC2 nodes to your cluster, then you must attach the `AmazonEKS_CNI_Policy` IAM managed policy to either your cluster IAM role, or to an IAM role that you create specifically for the Amazon VPC CNI add\-on\. For more information about creating the role and configuring the add\-on to use it, see [Configuring the Amazon VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.

------
#### [ AWS CLI ]

**Prerequisites**
+ An existing VPC and a dedicated security group that meet the requirements for an Amazon EKS cluster\. For more information, see [Cluster VPC considerations](network_reqs.md) and [Amazon EKS security group considerations](sec-group-reqs.md)\. If you don't have a VPC, you can follow [Creating a VPC for your Amazon EKS cluster](creating-a-vpc.md) to create one\.
+ An existing Amazon EKS cluster IAM role\. If you don't have the role, you can follow [Amazon EKS IAM roles](security_iam_service-with-iam.md#security_iam_service-with-iam-roles) to create one\.
+ The AWS CLI version 2\.3\.7 or later or 1\.22\.8 or later installed\. To install or upgrade, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) in the AWS Command Line Interface User Guide\. We recommend that you also configure the AWS CLI\. For more information, see [Quick configuration with `aws configure`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the AWS Command Line Interface User Guide\.

**To create your cluster with the AWS CLI**

1. Create your cluster with the following command\. Replace the Amazon Resource Name \(ARN\) of your Amazon EKS cluster IAM role that you created in [Amazon EKS cluster IAM role](service_IAM_role.md) and the subnet and security group IDs for the VPC that you created in [Creating a VPC for your Amazon EKS cluster](creating-a-vpc.md)\. Replace `my-cluster` with your cluster name and `region-code` with a [supported Region](https://docs.aws.amazon.com/general/latest/gr/eks.html#eks_region)\. You can replace `1.21` with any [supported version](kubernetes-versions.md)\. 

   For `subnetIds`, don't specify subnets in AWS Outposts, AWS Wavelength or AWS Local Zones\. If you plan to deploy self\-managed nodes in AWS Outposts, AWS Wavelength or AWS Local Zones subnets after you deploy your cluster, then make sure that you have, or can create, Outposts subnets in the VPC that you specify\.

   ```
   aws eks create-cluster \
      --region region-code \
      --name my-cluster \
      --kubernetes-version 1.21 \
      --role-arn arn:aws:iam::111122223333:role/eks-service-role-AWSServiceRoleForAmazonEKS-EXAMPLEBKZRQR \
      --resources-vpc-config subnetIds=subnet-a9189fe2,subnet-50432629,securityGroupIds=sg-f5c54184
   ```
**Note**  
If your IAM user doesn't have administrative privileges, you must explicitly add permissions for that user to call the Amazon EKS API operations\. For more information, see [Amazon EKS identity\-based policy examples](security_iam_id-based-policy-examples.md)\.

   Output:

   ```
   {
       "cluster": {
           "name": "my-cluster",
           "arn": "arn:aws:eks:region-code:111122223333:cluster/my-cluster",
           "createdAt": 1527785885.159,
           "version": "1.21",
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

   To encrypt the Kubernetes secrets, first create a KMS key using the [create\-key](https://docs.aws.amazon.com/goto/aws-cli/kms-2014-11-01/CreateKey) operation\.

   ```
   MY_KEY_ARN=$(aws kms create-key --query KeyMetadata.Arn —-output text)
   ```
**Note**  
By default, the `create-key` command creates a [symmetric key](https://docs.aws.amazon.com/kms/latest/developerguide/symmetric-asymmetric.html) with a key policy that gives the account's root user admin access on AWS KMS actions and resources\. For more information, see [Creating keys](https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html)\. If you want to scope down the permissions, make sure that the `kms:DescribeKey` and `kms:CreateGrant` actions are permitted on the policy for the principal that will be calling the `create-cluster` API\.  
 Amazon EKS does not support the policy condition `[kms:GrantIsForAWSResource](https://docs.aws.amazon.com/kms/latest/developerguide/policy-conditions.html#conditions-kms-grant-is-for-aws-resource)`\. Creating a cluster will not work if this action is in the KMS key policy statement\. 

   Add the **\-\-encryption\-config** parameter to the `aws eks create-cluster` command\. Encryption of Kubernetes secrets can only be enabled when the cluster is created\.

   ```
   --encryption-config '[{"resources":["secrets"],"provider":{"keyArn":"$MY_KEY_ARN"}}]'
   ```

   The `keyArn` member can contain either the alias or ARN of your KMS key\. The KMS key must be symmetric, created in the same Region as the cluster, and if the KMS key was created in a different account, the user must have access to the KMS key\. For more information, see [Allowing users in other accounts to use a KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html) in the *[AWS Key Management Service Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/)*\.
**Warning**  
Deletion of the KMS key will permanently put the cluster in a degraded state\. If any KMS keys used for cluster creation are scheduled for deletion, verify that this is the intended action before deletion\. Once the KMS key is deleted, there is no path to recovery for the cluster\. For more information, see [Deleting AWS KMS keys](https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html)\.

1. Cluster provisioning takes several minutes\. You can query the status of your cluster with the following command\. When your cluster status is `ACTIVE`, you can proceed\.

   ```
   aws eks describe-cluster \
       --region region-code \
       --name my-cluster \
       --query "cluster.status"
   ```

1. Follow the procedures in [Create a `kubeconfig` for Amazon EKS](create-kubeconfig.md) to enable communication with your new cluster\.

1. \(Optional\) To use some Amazon EKS add\-ons, or to enable individual Kubernetes workloads to have specific AWS Identity and Access Management \(IAM\) permissions, you need to create an IAM OpenID Connect \(OIDC\) provider for your cluster\. To create an IAM OIDC provider for your cluster, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\. You only need to create an IAM OIDC provider for your cluster once\. To learn more about Amazon EKS add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\. To learn more about assigning specific IAM permissions to your workloads, see [Technical overview](iam-roles-for-service-accounts-technical-overview.md)\. 

1. If you're going to deploy Amazon EC2 nodes to your cluster, then you must attach the `AmazonEKS_CNI_Policy` IAM managed policy to either your cluster IAM role, or to an IAM role that you create specifically for the Amazon VPC CNI add\-on\. For more information about creating the role and configuring the add\-on to use it, see [Configuring the Amazon VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.

1. \(Optional\) If you created a 1\.18 or later cluster, you can migrate the Amazon VPC CNI, CoreDNS, and `kube-proxy` add\-ons that were deployed with your cluster to Amazon EKS add\-ons\. For more information, see [Amazon EKS add\-ons](eks-add-ons.md)\.

------