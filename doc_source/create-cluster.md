# Creating an Amazon EKS cluster<a name="create-cluster"></a>

This topic walks you through creating an Amazon EKS cluster\. If this is your first time creating an Amazon EKS cluster, then we recommend that you follow one of our [Getting started with Amazon EKS](getting-started.md) guides instead\. They provide complete end\-to\-end walkthroughs for creating an Amazon EKS cluster with nodes\.

To connect an external Kubernetes cluster to view in Amazon EKS, see [Amazon EKS Connector](eks-connector.md)\.

**Important**  
When an Amazon EKS cluster is created, the IAM entity \(user or role\) that creates the cluster is permanently added to the Kubernetes RBAC authorization table as the administrator \(with `system:masters` permissions\)\. Initially, only that IAM user can make calls to the Kubernetes API server using `kubectl`\. For more information, see [Enabling IAM user and role access to your cluster](add-user-role.md)\. If you use the console to create the cluster, you must ensure that the same IAM user credentials are in the AWS SDK credential chain when you are running `kubectl` commands on your cluster\.
As a best practice, ensure that an IAM role is added to the `aws-auth` ConfigMap\. This ensures that a cluster can be deleted after the creating user has been deleted\. If you are in this situation and cannot delete a cluster, see [this article](https://aws.amazon.com/premiumsupport/knowledge-center/eks-api-server-unauthorized-error/) to resolvebrazi\.

You can create a cluster with `eksctl`, the AWS Management Console, or the AWS CLI\.

To deploy a new cluster on AWS Outposts, see [Deploy an Amazon EKS cluster with worker nodes on AWS Outposts](eks-on-outposts.md#eks-outposts-deploy)


## (Optional) Step 1: Create an IAM Role to own your EKS Cluster
The IAM security principal that you use to create your EKS Cluster permanently has full access to the Kubernetes API. We recommend creating a dedicated IAM role associated with the cluster, to contain these special permissions. This role may also be used to recover the cluster if other authentication mechanisms fail.

1. Create IAM Role 

This guide uses the `AdministratorAccess` managed policy. Creating a cluster requires wide ranging permissions. For more information, see [Minimum IAM Policies](https://eksctl.io/usage/minimum-iam-policies/).

------
#### [ CloudFormation ]

1. Create a role with sufficient permissions, and define a trust relationship for assuming the role. 

   1. Copy the following contents to a file named `ClusterCreateRoleStack.yaml`.

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Resources:
  ClusterCreateRole:
    Type: 'AWS::IAM::Role'
    Properties:
      RoleName: "ClusterCreate"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              AWS:
                - arn:aws:iam::<your-account-id>:root
            Action:
              - 'sts:AssumeRole'
      Path: /
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AdministratorAccess
```

   1. Create the CloudFormation stack for the role\.

```
aws cloudformation create-stack \
  --stack-name ClusterCreateRoleStack \
  --template-body file://$(pwd)/ClusterCreateRoleStack.yaml \
  --capabilities CAPABILITY_NAMED_IAM
```

------
#### [ Terraform ]
[[Note: This is merely an example of using TF in the docs.]]

This example uses the [official AWS Terraform provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs).

1. Create a role with sufficient permissions, and define a trust relationship for assuming the role. 

   1. Copy the following contents to a file named `ClusterCreateRoleStack.tf` in an empty directory.

```terraform
resource "aws_iam_role" "ClusterCreate" {
  name = "ClusterCreate"

  path = "/"
  managed_policy_arns = [ "arn:aws:iam::aws:policy/AdministratorAccess" ]


  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          AWS = "arn:aws:iam::<your-account-id>:root"
          [[TODO: replace the account ID with a TF variable]]
        }
      },
    ]
  })

}
```

   1. In the new directory, apply the terraform document.

```
terraform apply
```

------
#### [ AWS Console ]

1. Open the Amazon IAM console at [https://console.aws.amazon.com/iamv2/](https://console.aws.amazon.com/iamv2/)\.

1. Choose **Roles** under *Access Management* in the left sidebar, and then choose **Create Role**\. 

1. On the **Select trusted entity** page, do the following:

   1. Select **AWS account** as the *Trusted Entity*.

   1. For the AWS account, choose **This account**)\.

   1. Leave the remaining settings at their default values and choose **Next**\.

1. On the **Add permissions** page, do the following:

   1. Select the **AdministratorAccess** policy.

   1. Leave the remaining settings at their default values and choose **Next**\.

1. On the **Name, review, and create** page, add a name such as "ClusterCreate",  choose **Create Role**\.

------

## (Optional) Step 2: Create your EKS Cluster

------
#### [ eksctl ]

**Prerequisite**  
Version 0\.89\.0 or later of the `eksctl` command line tool installed on your computer or AWS CloudShell\. To install or update `eksctl`, see [Installing `eksctl`](eksctl.md)\.

1. Optional: Assume an IAM Role to own the cluster

As discussed previously, the IAM entity \(user or role\) that creates a cluster is permanently added to the Kubernetes RBAC authorization table as the administrator \(with `system:masters` permissions\)\.

Assume an appropriate role for creating the cluster. This may be the dedicated IAM Role created in Step 1. 

This guide creates an awscli profile to automate assuming the role. For more information, review how to [use IAM roles with the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-role.html).

Insert a new profile for the role to ` ~/.aws/config`:

```
[profile ClusterCreate]
role_arn = arn:aws:iam::<your-account-id>:role/ClusterCreate
source_profile = <default-profile>
```

Configure the awscli to use the new profile:

```
export AWS_PROFILE=ClusterCreate
```

Now, `eksctl` will use this dedicated IAM role to create the cluster.

1. Create the Cluster

Create an Amazon EKS IPv4 cluster with the Amazon EKS latest Kubernetes version in your default Region\. If you want to create an IPv6 cluster, you must deploy your cluster using a config file\. For an example, see [Deploy an IPv6 cluster and nodes](cni-ipv6.md#deploy-ipv6-cluster)\. Replace the `example-values` with your own values\. You can replace `1.21` with any [supported version](kubernetes-versions.md)\. The cluster name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can't be longer than 128 characters\.

```
eksctl create cluster \
    --name my-cluster \
    --version 1.21 \
    --without-nodegroup
```

[[question -- can we promote this to default or recommended?]]
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

After your cluster is created, you can migrate the Amazon VPC CNI, CoreDNS, and `kube-proxy` self\-managed add\-ons that were deployed with your cluster to Amazon EKS add\-ons\. For more information, see [Amazon EKS add\-ons](eks-add-ons.md)\.

------
#### [ AWS Management Console ]<a name="create-cluster-prerequisites-console"></a>

**Prerequisites**
+ An existing VPC and a dedicated security group that meet the requirements for an Amazon EKS cluster\. For more information, see [Cluster VPC and subnet considerations](network_reqs.md) and [Amazon EKS security group considerations](sec-group-reqs.md)\. If you don't have a VPC, you can follow [Creating a VPC for your Amazon EKS cluster](creating-a-vpc.md) to create one\. If you want to assign IPv6 IP addresses to Pods and Services, then ensure that your VPC, subnets, and security groups meet the requirements and considerations listed in [Assigning IPv6 addresses to pods and services](cni-ipv6.md) or use the Amazon EKS public and private subnet AWS CloudFormation IPv6 VPC template to deploy an IPv6 VPC\.
+ An existing Amazon EKS cluster service IAM role\. If you don't have the role, you can follow [Amazon EKS IAM roles](security_iam_service-with-iam.md#security_iam_service-with-iam-roles) to create one\.

**Optional: Assume an IAM Role to own the cluster**

As discussed previously, the IAM entity \(user or role\) that creates a cluster is permanently added to the Kubernetes RBAC authorization table as the administrator \(with `system:masters` permissions\)\.

[Assume an appropriate role for creating the cluster.](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-console.html) This may be the dedicated IAM Role created in Step 1. 

**To create your cluster with the console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose **Create cluster**\.

1. On the **Configure cluster** page, fill in the following fields:
   + **Name** – A unique name for your cluster\.
   + **Kubernetes version** – The version of Kubernetes to use for your cluster\. 
   + **Cluster Service Role** – Choose the Amazon EKS cluster role to allow the Kubernetes control plane to manage AWS resources on your behalf\. For more information, see the [Prerequisites](#create-cluster-prerequisites-console)\.
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
   + **VPC** – Select an existing VPC to use for your cluster\. If none are listed, then you need to create one first\. For more information, see the [Prerequisites](#create-cluster-prerequisites-console)\.
   + **Subnets** – By default, the available subnets in the VPC specified in the previous field are preselected\. Unselect any subnet that you don't want to host cluster resources, such as worker nodes or load balancers\. The subnets must meet the requirements for an Amazon EKS cluster\. For more information, see [Cluster VPC and subnet considerations](network_reqs.md)\.
**Important**  
If you select subnets that were created before March 26, 2020 using one of the Amazon EKS AWS CloudFormation VPC templates, be aware of a default setting change that was introduced on March 26, 2020\. For more information, see [Creating a VPC for your Amazon EKS cluster](creating-a-vpc.md)\.
Don't select subnets in AWS Outposts, AWS Wavelength or AWS Local Zones\. If you plan to deploy self\-managed nodes in AWS Outposts, AWS Wavelength or AWS Local Zones subnets after you deploy your cluster, then make sure that you have, or can create, Outposts subnets in the VPC that you select\.

     **Security groups** – The **SecurityGroups** value from the AWS CloudFormation output that you generated when you created your [VPC](creating-a-vpc.md)\. This security group has **ControlPlaneSecurityGroup** in the dropdown name\.
**Important**  
The node AWS CloudFormation template modifies the security group that you specify here, so **Amazon EKS strongly recommends that you use a dedicated security group for each cluster control plane \(one per cluster\)**\. If this security group is shared with other resources, you might block or disrupt connections to those resources\.
   + **Choose cluster IP address family** – If the version you chose for your cluster is 1\.20 or earlier, only the **IPv4** option is available\. If you chose version 1\.21 or later for your cluster version, then you can choose whether Kubernetes will assign **IPv4** or **IPv6** addresses to Pods and Services\. You can't change this option after cluster creation\. If you choose IPv6, you can't choose the **Configure Kubernetes Service IP address range** option\. Kubernetes assigns Service addresses from the unique local address range \(`fc00::/7`\)\. You can't specify a custom address range\.
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

1. You can accept the defaults in the **Networking add\-ons** section to install the default version of the [AWS VPC CNI](pod-networking.md), [CoreDNS](managing-coredns.md), and [kube\-proxy](managing-kube-proxy.md) Amazon EKS add\-ons, or you can select a different version\. If you don't require the functionality of any of the add\-ons, you can remove them once your cluster is created\. If you need to manage Amazon EKS managed settings for any of these add\-ons yourself, then you can remove Amazon EKS management of the add\-on once your cluster is created\. For more information, see [Amazon EKS add\-ons](eks-add-ons.md)\.
**Important**  
The AWS VPC CNI add\-on is configured to use the IAM permissions assigned to the [Amazon EKS node IAM role](create-node-role.md)\. After the cluster is created, but before you deploy any Amazon EC2 nodes to your cluster, you must ensure that the `AmazonEKS_CNI_Policy` managed IAM policy \(if using IPv4 for your cluster\) or the *AmazonEKS\_CNI\_IPv6\_Policy* IAM policy \(that you [create yourself](cni-iam-role.md#cni-iam-role-create-ipv6-policy) if you're using IPv6 for your cluster\) is attached to either the node IAM role, or to a different role associated to the Kubernetes service account that the add\-on runs as\. We recommend that you assign the policy to a different IAM role than the node IAM role by completing the instructions in [Configuring the Amazon VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\. Once your cluster and IAM role are created, you can [update the add\-on](managing-vpc-cni.md#updating-vpc-cni-eks-add-on) to use the IAM role that you create\.

1. Select **Next**\.

1. On the **Configure logging** page, you can optionally choose which log types that you want to enable\. By default, each log type is **Disabled**\. For more information, see [Amazon EKS control plane logging](control-plane-logs.md)\.

1. Select **Next**\.

1. On the **Review and create** page, review the information that you entered or selected on the previous pages\. Select **Edit** if you need to make changes to any of your selections\. Once you're satisfied with your settings, select **Create**\. The **Status** field shows **CREATING** until the cluster provisioning process completes\.
**Note**  
You might receive an error that one of the Availability Zones in your request doesn't have sufficient capacity to create an Amazon EKS cluster\. If this happens, the error output contains the Availability Zones that can support a new cluster\. Retry creating your cluster with at least two subnets that are located in the supported Availability Zones for your account\. For more information, see [Insufficient capacity](troubleshooting.md#ICE)\.

   Cluster provisioning takes several minutes\.

1. Follow the procedures in [Create a `kubeconfig` for Amazon EKS](create-kubeconfig.md) to enable communication with your new cluster\.

1. \(Optional\) To use some Amazon EKS add\-ons, or to enable individual Kubernetes workloads to have specific AWS Identity and Access Management \(IAM\) permissions, you need to create an IAM OpenID Connect \(OIDC\) provider for your cluster\. To create an IAM OIDC provider for your cluster, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\. You only need to create an IAM OIDC provider for your cluster once\. To learn more about Amazon EKS add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\. To learn more about assigning specific IAM permissions to your workloads, see [Technical overview](iam-roles-for-service-accounts-technical-overview.md)\. 

1. If you're going to deploy Amazon EC2 nodes to your cluster, then you must attach one of the following policies to either your cluster IAM role, or to an IAM role that you create specifically for the Amazon VPC CNI add\-on \(this option requires the previous step\)\. For more information about creating the role and configuring the add\-on to use it, see [Configuring the Amazon VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.
   + The `AmazonEKS_CNI_Policy` IAM managed policy, if you created a 1\.20 or earlier cluster or a 1\.21 or later cluster with the IPv4 family\.
   + [An IAM policy that you create](cni-iam-role.md#cni-iam-role-create-ipv6-policy), if you created a 1\.21 or later cluster with the IPv6 family\.

1. \(Optional\) Configure the VPC CNI add\-on to use its own IAM role\. This option requires the IAM OIDC provider created in a previous step and that you created an IAM role specifically for the add\-on in the previous step\. For more information, see [Updating the Amazon VPC CNI Amazon EKS add\-on](managing-vpc-cni.md#updating-vpc-cni-eks-add-on)\.

------
#### [ AWS CLI ]

**Prerequisites**
+ Version 2\.4\.9 or later or 1\.22\.30 or later of the AWS CLI installed and configured on your computer or AWS CloudShell\. For more information, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with `aws configure`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the AWS Command Line Interface User Guide\.
+ An existing VPC and a dedicated security group that meet the requirements for an Amazon EKS cluster\. For more information, see [Cluster VPC and subnet considerations](network_reqs.md) and [Amazon EKS security group considerations](sec-group-reqs.md)\. If you don't have a VPC, you can follow [Creating a VPC for your Amazon EKS cluster](creating-a-vpc.md) to create one\. If you want to assign IPv6 IP addresses to Pods and Services, then then ensure that your VPC, subnets, and security group meets the requirements listed in the considerations in [Assigning IPv6 addresses to pods and services](cni-ipv6.md)\.
+ An existing Amazon EKS cluster IAM role\. If you don't have the role, you can follow [Amazon EKS IAM roles](security_iam_service-with-iam.md#security_iam_service-with-iam-roles) to create one\.

**Optional: Assume an IAM Role to own the cluster**

As discussed previously, the IAM entity \(user or role\) that creates a cluster is permanently added to the Kubernetes RBAC authorization table as the administrator \(with `system:masters` permissions\)\.

Assume an appropriate role for creating the cluster. This may be the dedicated IAM Role created in Step 1. 

This guide creates an awscli profile to automate assuming the role. For more information, review how to [use IAM roles with the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-role.html).

Insert a new profile for the role to ` ~/.aws/config`:

```
[profile ClusterCreate]
role_arn = arn:aws:iam::<your-account-id>:role/ClusterCreate
source_profile = <default-profile>
```

Configure the awscli to use the new profile:

```
export AWS_PROFILE=ClusterCreate
```

**To create your cluster with the AWS CLI**

1. Create your cluster with the following command\. Replace the Amazon Resource Name \(ARN\) of your Amazon EKS cluster IAM role that you created in [Amazon EKS cluster IAM role](service_IAM_role.md) and the subnet and security group IDs for the VPC that you created in [Creating a VPC for your Amazon EKS cluster](creating-a-vpc.md)\. Replace `my-cluster` with your cluster name and `region-code` with a [supported Region](https://docs.aws.amazon.com/general/latest/gr/eks.html#eks_region)\. You can replace `1.21` with any [supported version](kubernetes-versions.md)\. 

   For `subnetIds`, don't specify subnets in AWS Outposts, AWS Wavelength or AWS Local Zones\. If you plan to deploy self\-managed nodes in AWS Outposts, AWS Wavelength or AWS Local Zones subnets after you deploy your cluster, then make sure that you have, or can create, Outposts subnets in the VPC that you specify\.

   If you want the cluster to assign IPv6 addresses to Pods and Services instead of IPv4 addresses, add **`--kubernetes-network-config ipFamily=ipv6`** to the following command and specify `1.21` or later for `--kubernetes-version`\.

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
By default, the `create-key` command creates a [symmetric key](https://docs.aws.amazon.com/kms/latest/developerguide/symmetric-asymmetric.html) that encrypts and decrypts data\. This key has a key policy that gives the account's root user admin access on AWS KMS actions and resources\. For more information, see [Creating keys](https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html)\. If you want to scope down the permissions, make sure that the `kms:DescribeKey` and `kms:CreateGrant` actions are permitted on the policy for the principal that will be calling the `create-cluster` API\.  
 Amazon EKS does not support the policy condition `[kms:GrantIsForAWSResource](https://docs.aws.amazon.com/kms/latest/developerguide/policy-conditions.html#conditions-kms-grant-is-for-aws-resource)`\. Creating a cluster will not work if this action is in the KMS key policy statement\. 

   Add the **\-\-encryption\-config** parameter to the `aws eks create-cluster` command\. Encryption of Kubernetes secrets can only be enabled when the cluster is created\.

   ```
   --encryption-config '[{"resources":["secrets"],"provider":{"keyArn":"$MY_KEY_ARN"}}]'
   ```

   The `keyArn` member can contain either the alias or ARN of your KMS key\. The KMS key must be
   + Symmetric
   + Able to encrypt and decrypt data
   + Created in the same region as the cluster
   + If the KMS key was created in a different account, the user must have access to the KMS key\.

   For more information, see [Allowing users in other accounts to use a KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html) in the *[AWS Key Management Service Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/)*\.
**Warning**  
Deletion of the KMS key permanently puts the cluster in a degraded state\. If any KMS keys used for cluster creation are scheduled for deletion, verify that this is the intended action before deletion\. Once the KMS key is deleted, there is no path to recovery for the cluster\. For more information, see [Deleting AWS KMS keys](https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html)\.

1. Cluster provisioning takes several minutes\. You can query the status of your cluster with the following command\. When your cluster status is `ACTIVE`, you can proceed\.

   ```
   aws eks describe-cluster \
       --region region-code \
       --name my-cluster \
       --query "cluster.status"
   ```

1. Follow the procedures in [Create a `kubeconfig` for Amazon EKS](create-kubeconfig.md) to enable communication with your new cluster\.

1. \(Optional\) To use some Amazon EKS add\-ons, or to enable individual Kubernetes workloads to have specific AWS Identity and Access Management \(IAM\) permissions, you need to create an IAM OpenID Connect \(OIDC\) provider for your cluster\. To create an IAM OIDC provider for your cluster, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\. You only need to create an IAM OIDC provider for your cluster once\. To learn more about Amazon EKS add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\. To learn more about assigning specific IAM permissions to your workloads, see [Technical overview](iam-roles-for-service-accounts-technical-overview.md)\. 

1. If you're going to deploy Amazon EC2 nodes to your cluster, then you must attach one of the following policies to either your cluster IAM role, or to an IAM role that you create specifically for the Amazon VPC CNI add\-on \(this option requires the previous step\)\. For more information about creating the role and configuring the add\-on to use it, see [Configuring the Amazon VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.:
   + The `AmazonEKS_CNI_Policy` IAM managed policy, if you created a 1\.20 or earlier cluster or a 1\.21 or later cluster with the IPv4 family\.
   + [An IAM policy that you create](cni-iam-role.md#cni-iam-role-create-ipv6-policy), if you created a 1\.21 or later cluster with the IPv6 family\.

1. \(Optional\) Migrate the Amazon VPC CNI, CoreDNS, and `kube-proxy` self\-managed add\-ons that were deployed with your cluster to Amazon EKS add\-ons\. For more information, see [Amazon EKS add\-ons](eks-add-ons.md)\. Configure the Amazon EKS VPC CNI add\-on to use its own IAM role\. This option requires the IAM OIDC provider created in a previous step and that you created an IAM role specifically for the add\-on in the previous step\. For more information, see [Updating the Amazon VPC CNI Amazon EKS add\-on](managing-vpc-cni.md#updating-vpc-cni-eks-add-on)\.

------

## Reccomended Next Steps

- [Create a kubeconfig to access the API server.](create-kubeconfig.md)
- [Add IAM users or roles to your Amazon EKS cluster.](add-user-role.md)