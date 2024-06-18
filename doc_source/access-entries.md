# Manage access entries<a name="access-entries"></a>

**Prerequisites**
+ Familiarity with cluster access options for your Amazon EKS cluster\. For more information, see [Grant access to Kubernetes APIs ](grant-k8s-access.md)\.
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\. To use *access entries* and change the authentication mode of a cluster, the cluster must have a platform version that is the same or later than the version listed in the following table, or a Kubernetes version that is later than the versions listed in the table\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/access-entries.html)

  You can check your current Kubernetes and platform version by replacing *my\-cluster* in the following command with the name of your cluster and then running the modified command: **aws eks describe\-cluster \-\-name *my\-cluster* \-\-query 'cluster\.\{"Kubernetes Version": version, "Platform Version": platformVersion\}'**\.
**Important**  
After Amazon EKS updates your cluster to the platform version listed in the table, Amazon EKS creates an access entry with administrator permissions to the cluster for the IAM principal that originally created the cluster\. If you don't want that IAM principal to have administrator permissions to the cluster, remove the access entry that Amazon EKS created\.  
For clusters with platform versions that are earlier than those listed in the previous table, the cluster creator is always a cluster administrator\. It's not possible to remove cluster administrator permissions from the IAM user or role that created the cluster\.
+ An IAM principal with the following permissions for your cluster: `CreateAccessEntry`, `ListAccessEntries`, `DescribeAccessEntry`, `DeleteAccessEntry`, and `UpdateAccessEntry`\. For more information about Amazon EKS permissions, see [Actions defined by Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html#amazonelastickubernetesservice-actions-as-permissions) in the Service Authorization Reference\.
+ An existing IAM principal to create an access entry for, or an existing access entry to update or delete\.

## Setting up access entries<a name="setting-up-access-entries"></a>

To begin using access entries, you must change the authentication mode of the cluster to either the `API_AND_CONFIG_MAP` or `API` modes\. This adds the API for access entries\.

------
#### [ AWS Management Console ]

**To create an access entry**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the name of the cluster that you want to create an access entry in\.

1. Choose the **Access** tab\.

1. The **Authentication mode** show the current authentication mode of the cluster\. If the mode says EKS API, you can already add access entries and you can skip the remaining steps\.

1. Choose **Manage access**\.

1. For **Cluster authentication mode**, select a mode with the EKS API\. Note that you can't change the authentication mode back to a mode that removes the EKS API and access entries\.

1. Choose **Save changes**\. Amazon EKS begins to update the cluster, the status of the cluster changes to Updating, and the change is recorded in the **Update history** tab\.

1. Wait for the status of the cluster to return to Active\. When the cluster is Active, you can follow the steps in [Creating access entries](#creating-access-entries) to add access to the cluster for IAM principals\.

------
#### [ AWS CLI ]

**Prerequisite**  
The latest version of the AWS CLI v1 installed and configured on your device or AWS CloudShell\. AWS CLI v2 doesn't support new features for a few days\. You can check your current version with `aws --version | cut -d / -f2 | cut -d ' ' -f1`\. Package managers such `yum`, `apt-get`, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI\. To install the latest version, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with `aws configure`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the AWS Command Line Interface User Guide\. The AWS CLI version installed in the AWS CloudShell may also be several versions behind the latest version\. To update it, see [Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the AWS CloudShell User Guide\.

1. Run the following command\. Replace *my\-cluster* with the name of your cluster\. If you want to disable the `ConfigMap` method permanently, replace `API_AND_CONFIG_MAP` with `API`\.

   Amazon EKS begins to update the cluster, the status of the cluster changes to UPDATING, and the change is recorded in the aws eks list\-updates\.

   ```
   aws eks update-cluster-config --name my-cluster --access-config authenticationMode=API_AND_CONFIG_MAP
   ```

1. Wait for the status of the cluster to return to Active\. When the cluster is Active, you can follow the steps in [Creating access entries](#creating-access-entries) to add access to the cluster for IAM principals\.

------

## Creating access entries<a name="creating-access-entries"></a>

**Considerations**

Before creating access entries, consider the following:
+ An *access entry* includes the Amazon Resource Name \(ARN\) of one, and only one, existing IAM principal\. An IAM principal can't be included in more than one access entry\. Additional considerations for the ARN that you specify:
  +  IAM best practices recommend accessing your cluster using IAM *roles* that have short\-term credentials, rather than IAM *users* that have long\-term credentials\. For more information, see [Require human users to use federation with an identity provider to access AWS using temporary credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#bp-users-federation-idp) in the IAM User Guide\.
  + If the ARN is for an IAM role, it *can* include a path\. ARNs in `aws-auth` `ConfigMap` entries, *can't* include a path\. For example, your ARN can be `arn:aws:iam::111122223333:role/development/apps/my-role` or `arn:aws:iam::111122223333:role/my-role`\.
  + If the type of the access entry is anything other than `STANDARD` \(see next consideration about types\), the ARN must be in the same AWS account that your cluster is in\. If the type is `STANDARD`, the ARN can be in the same, or different, AWS account than the account that your cluster is in\.
  + You can't change the IAM principal after the access entry is created\.
  + If you ever delete the IAM principal with this ARN, the access entry isn't automatically deleted\. We recommend that you delete the access entry with an ARN for an IAM principal that you delete\. If you don't delete the access entry and ever recreate the IAM principal, even if it has the same ARN, the access entry won't work\. This is because even though the ARN is the same for the recreated IAM principal, the `roleID` or `userID` \(you can see this with the `aws sts get-caller-identity` AWS CLI command\) is different for the recreated IAM principal than it was for the original IAM principal\. Even though you don't see the IAM principal's `roleID` or `userID` for an access entry, Amazon EKS stores it with the access entry\.
+ Each access entry has a *type*\. You can specify `EC2 Linux` \(for an IAM role used with Linux or Bottlerocket self\-managed nodes\), `EC2 Windows` \(for an IAM roles used with Windows self\-managed nodes\), `FARGATE_LINUX` \(for an IAM roles used with AWS Fargate \(Fargate\)\), or `STANDARD` as a type\. If you don't specify a type, Amazon EKS automatically sets the type to `STANDARD`\. It's unnecessary to create an access entry for an IAM role that's used for a managed node group or a Fargate profile, because Amazon EKS adds entries for these roles to the `aws-auth` `ConfigMap`, regardless of which platform version your cluster is at\. 

  You can't change the type after the access entry is created\.
+ If the type of the access entry is `STANDARD`, you can specify a *username* for the access entry\. If you don't specify a value for username, Amazon EKS sets one of the following values for you, depending on the type of the access entry and whether the IAM principal that you specified is an IAM role or IAM user\. Unless you have a specific reason for specifying your own username, we recommend that don't specify one and let Amazon EKS auto\-generate it for you\. If you specify your own username:
  + It can't start with `system:`, `eks:`, `aws:`, `amazon:`, or `iam:`\.
  + If the username is for an IAM role, we recommend that you add `{{SessionName}}` to the end of your username\. If you add `{{SessionName}}` to your username, the username must include a colon *before* \{\{SessionName\}\}\. When this role is assumed, the name of the session specified when assuming the role is automatically passed to the cluster and will appear in CloudTrail logs\. For example, you can't have a username of `john{{SessionName}}`\. The username would have to be `:john{{SessionName}}` or `jo:hn{{SessionName}}`\. The colon only has to be before `{{SessionName}}`\. The username generated by Amazon EKS in the following table includes an ARN\. Since an ARN includes colons, it meets this requirement\. The colon isn't required if you don't include `{{SessionName}}` in your username\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/access-entries.html)

  You can change the username after the access entry is created\.
+ If an access entry's type is `STANDARD`, and you want to use Kubernetes RBAC authorization, you can add one or more *group names* to the access entry\. After you create an access entry you can add and remove group names\. For the IAM principal to have access to Kubernetes objects on your cluster, you must create and manage Kubernetes role\-based authorization \(RBAC\) objects\. Create Kubernetes `RoleBinding` or `ClusterRoleBinding` objects on your cluster that specify the group name as a `subject` for `kind: Group`\. Kubernetes authorizes the IAM principal access to any cluster objects that you've specified in a Kubernetes `Role` or `ClusterRole` object that you've also specified in your binding's `roleRef`\. If you specify group names, we recommend that you're familiar with the Kubernetes role\-based authorization \(RBAC\) objects\. For more information, see [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) in the Kubernetes documentation\. 
**Important**  
Amazon EKS doesn't confirm that any Kubernetes RBAC objects that exist on your cluster include any of the group names that you specify\.

  Instead of, or in addition to, Kubernetes authorizing the IAM principal access to Kubernetes objects on your cluster, you can associate Amazon EKS *access policies* to an access entry\. Amazon EKS authorizes IAM principals to access Kubernetes objects on your cluster with the permissions in the access policy\. You can scope an access policy's permissions to Kubernetes namespaces that you specify\. Use of access policies don't require you to manage Kubernetes RBAC objects\. For more information, see [Associating and disassociating access policies to and from access entries](access-policies.md)\.
+ If you create an access entry with type `EC2 Linux` or `EC2 Windows`, the IAM principal creating the access entry must have the `iam:PassRole` permission\. For more information, see [Granting a user permissions to pass a role to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_passrole.html) in the IAM User Guide\.
+ Similar to standard [IAM behavior](https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_general.html#troubleshoot_general_eventual-consistency), access entry creation and updates are eventually consistent, and may take several seconds to be effective after the initial API call returns successfully\. You must design your applications to account for these potential delays\. We recommend that you don't include access entry creates or updates in the critical, high\- availability code paths of your application\. Instead, make changes in a separate initialization or setup routine that you run less frequently\. Also, be sure to verify that the changes have been propagated before production workflows depend on them\. 
+ Access entries do not support [service linked roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html)\. You cannot create access entries where the principal ARN is a service linked role\. You can identify service linked roles by their ARN, which is in the format `arn:aws:iam::*:role/aws-service-role/*`\. 

You can create an access entry using the AWS Management Console or the AWS CLI\.

------
#### [ AWS Management Console ]

**To create an access entry**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the name of the cluster that you want to create an access entry in\.

1. Choose the **Access** tab\.

1. Choose **Create access entry**\.

1. For **IAM principal**, select an existing IAM role or user\. IAM best practices recommend accessing your cluster using IAM *roles* that have short\-term credentials, rather than IAM *users* that have long\-term credentials\. For more information, see [Require human users to use federation with an identity provider to access AWS using temporary credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#bp-users-federation-idp) in the IAM User Guide\.

1. For **Type**, if the access entry is for the node role used for self\-managed Amazon EC2 nodes, select **EC2 Linux** or **EC2 Windows**\. Otherwise, accept the default \(**Standard**\)\.

1. If the **Type** you chose is **Standard** and you want to specify a **Username**, enter the username\.

1. If the **Type** you chose is **Standard** and you want to use Kubernetes RBAC authorization for the IAM principal, specify one or more names for **Groups**\. If you don't specify any group names and want to use Amazon EKS authorization, you can associate an access policy in a later step, or after the access entry is created\.

1. \(Optional\) For **Tags**, assign labels to the access entry\. For example, to make it easier to find all resources with the same tag\.

1. Choose **Next**\.

1. On the **Add access policy** page, if the type you chose was **Standard** and you want Amazon EKS to authorize the IAM principal to have permissions to the Kubernetes objects on your cluster, complete the following steps\. Otherwise, choose **Next**\.

   1. For **Policy name**, choose an access policy\. You can't view the permissions of the access policies, but they include similar permissions to those in the Kubernetes user\-facing `ClusterRole` objects\. For more information, see [User\-facing roles](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#user-facing-roles) in the Kubernetes documentation\.

   1. Choose one of the following options:
      + **Cluster** – Choose this option if you want Amazon EKS to authorize the IAM principal to have the permissions in the access policy for all Kubernetes objects on your cluster\.
      + **Kubernetes namespace** – Choose this option if you want Amazon EKS to authorize the IAM principal to have the permissions in the access policy for all Kubernetes objects in a specific Kubernetes namespace on your cluster\. For **Namespace**, enter the name of the Kubernetes namespace on your cluster\. If you want to add additional namespaces, choose **Add new namespace** and enter the namespace name\.

   1. If you want to add additional policies, choose **Add policy**\. You can scope each policy differently, but you can add each policy only once\.

   1. Choose **Next**\.

1. Review the configuration for your access entry\. If anything looks incorrect, choose **Previous** to go back through the steps and correct the error\. If the configuration is correct, choose **Create**\.

------
#### [ AWS CLI ]

**Prerequisite**  
The latest version of the AWS CLI v1 installed and configured on your device or AWS CloudShell\. AWS CLI v2 doesn't support new features for a few days\. You can check your current version with `aws --version | cut -d / -f2 | cut -d ' ' -f1`\. Package managers such `yum`, `apt-get`, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI\. To install the latest version, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with `aws configure`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the AWS Command Line Interface User Guide\. The AWS CLI version installed in the AWS CloudShell may also be several versions behind the latest version\. To update it, see [Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the AWS CloudShell User Guide\.

**To create an access entry**  
You can use any of the following examples to create access entries:
+ Create an access entry for a self\-managed Amazon EC2 Linux node group\. Replace *my\-cluster* with the name of your cluster, *111122223333* with your AWS account ID, and *EKS\-my\-cluster\-self\-managed\-ng\-1* with the name of your [node IAM role](create-node-role.md)\. If your node group is a Windows node group, then replace *EC2\_Linux* with **EC2\_Windows**\.

  ```
  aws eks create-access-entry --cluster-name my-cluster --principal-arn arn:aws:iam::111122223333:role/EKS-my-cluster-self-managed-ng-1 --type EC2_Linux
  ```

  You can't use the `--kubernetes-groups` option when you specify a type other than `STANDARD`\. You can't associate an access policy to this access entry, because its type is a value other than `STANDARD`\.
+ Create an access entry that allows an IAM role that's not used for an Amazon EC2 self\-managed node group, that you want Kubernetes to authorize access to your cluster with\. Replace *my\-cluster* with the name of your cluster, *111122223333* with your AWS account ID, and *my\-role* with the name of your IAM role\. Replace *Viewers* with the name of a group that you've specified in a Kubernetes `RoleBinding` or `ClusterRoleBinding` object on your cluster\.

  ```
  aws eks create-access-entry --cluster-name my-cluster --principal-arn arn:aws:iam::111122223333:role/my-role --type STANDARD --user Viewers --kubernetes-groups Viewers
  ```
+ Create an access entry that allows an IAM user to authenticate to your cluster\. This example is provided because this is possible, though IAM best practices recommend accessing your cluster using IAM *roles* that have short\-term credentials, rather than IAM *users* that have long\-term credentials\. For more information, see [Require human users to use federation with an identity provider to access AWS using temporary credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#bp-users-federation-idp) in the IAM User Guide\.

  ```
  aws eks create-access-entry --cluster-name my-cluster --principal-arn arn:aws:iam::111122223333:user/my-user --type STANDARD --username my-user
  ```

  If you want this user to have more access to your cluster than the permissions in the Kubernetes API discovery roles, then you need to associate an access policy to the access entry, since the `--kubernetes-groups` option isn't used\. For more information, see [Associating and disassociating access policies to and from access entries](access-policies.md) and [API discovery roles ](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#discovery-roles) in the Kubernetes documentation\.

------

## Updating access entries<a name="updating-access-entries"></a>

You can update an access entry using the AWS Management Console or the AWS CLI\.

------
#### [ AWS Management Console ]

**To update an access entry**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the name of the cluster that you want to create an access entry in\.

1. Choose the **Access** tab\.

1. Choose the access entry that you want to update\.

1. Choose **Edit**\.

1. For **Username**, you can change the existing value\.

1. For **Groups**, you can remove existing group names or add new group names\. If the following groups names exist, don't remove them: **system:nodes** or **system:bootstrappers**\. Removing these groups can cause your cluster to function improperly\. If you don't specify any group names and want to use Amazon EKS authorization, associate an [access policy](access-policies.md) in a later step\.

1. For **Tags**, you can assign labels to the access entry\. For example, to make it easier to find all resources with the same tag\. You can also remove existing tags\.

1. Choose **Save changes**\.

1. If you want to associate an access policy to the entry, see [Associating and disassociating access policies to and from access entries](access-policies.md)\.

------
#### [ AWS CLI ]

**Prerequisite**  
Version `2.12.3` or later or version `1.27.160` or later of the AWS Command Line Interface \(AWS CLI\) installed and configured on your device or AWS CloudShell\. To check your current version, use `aws --version | cut -d / -f2 | cut -d ' ' -f1`\. Package managers such `yum`, `apt-get`, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI\. To install the latest version, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with aws configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the *AWS Command Line Interface User Guide*\. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version\. To update it, see [Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the *AWS CloudShell User Guide*\.

**To update an access entry**  
Replace *my\-cluster* with the name of your cluster, *111122223333* with your AWS account ID, and *EKS\-my\-cluster\-my\-namespace\-Viewers* with the name of an IAM role\.

```
aws eks update-access-entry --cluster-name my-cluster --principal-arn arn:aws:iam::111122223333:role/EKS-my-cluster-my-namespace-Viewers --kubernetes-groups Viewers 
```

You can't use the `--kubernetes-groups` option if the type of the access entry is a value other than `STANDARD`\. You also can't associate an access policy to an access entry with a type other than `STANDARD`\. 

------

## Deleting access entries<a name="deleting-access-entries"></a>

If you discover that you deleted an access entry in error, you can always recreate it\. If the access entry that you're deleting is associated to any access policies, the associations are automatically deleted\. You don't have to disassociate access policies from an access entry before deleting the access entry\.

You can delete an access entry using the AWS Management Console or the AWS CLI\.

------
#### [ AWS Management Console ]

**To delete an access entry**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the name of the cluster that you want to delete an access entry from\.

1. Choose the **Access** tab\.

1. In the **Access entries** list, choose the access entry that you want to delete\.

1. Choose Delete\.

1. In the confirmation dialog box, choose **Delete**\.

------
#### [ AWS CLI ]

**Prerequisite**  
Version `2.12.3` or later or version `1.27.160` or later of the AWS Command Line Interface \(AWS CLI\) installed and configured on your device or AWS CloudShell\. To check your current version, use `aws --version | cut -d / -f2 | cut -d ' ' -f1`\. Package managers such `yum`, `apt-get`, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI\. To install the latest version, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with aws configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the *AWS Command Line Interface User Guide*\. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version\. To update it, see [Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the *AWS CloudShell User Guide*\.

**To delete an access entry**  
Replace *my\-cluster* with the name of your cluster, *111122223333* with your AWS account ID, and *my\-role* with the name of the IAM role that you no longer want to have access to your cluster\.

```
aws eks delete-access-entry --cluster-name my-cluster --principal-arn arn:aws:iam::111122223333:role/my-role
```

------