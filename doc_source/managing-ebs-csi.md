# Managing the Amazon EBS CSI driver as an Amazon EKS add\-on<a name="managing-ebs-csi"></a>


|  | 
| --- |
| You can manage the Amazon EBS CSI driver as an Amazon EKS add\-on\. However, this feature is only available in preview release for Amazon EKS and is subject to change\. Here are some considerations for the preview release:[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/managing-ebs-csi.html) | 

For information about Amazon EKS add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\. You can add the Amazon EBS CSI add\-on by following the steps in [Adding the Amazon EBS CSI add\-on](#adding-ebs-csi-eks-add-on)\.

If you added the Amazon EBS CSI add\-on, you can manage it by following the steps in the [Updating the Amazon EBS CSI driver as an Amazon EKS add\-on](#updating-ebs-csi-eks-add-on) and [Removing the Amazon EBS CSI add\-on](#removing-ebs-csi-eks-add-on) sections\.

**Prerequisites**
+ An existing cluster that's version 1\.18 or later\.
  + 1\.18 requires eks\.9 or later\.
  + 1\.19 requires eks\.7 or later\.
  + 1\.20 requires eks\.3 or later\.
  + 1\.21 requires eks\.3 or later\.
+ An existing AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.

## Configuring the Amazon EBS CSI plugin to use IAM roles for service accounts<a name="csi-iam-role"></a>

The Amazon EBS CSI plugin requires IAM permissions to make calls to AWS APIs on your behalf\. For more information, see [Set up driver permission](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/tree/master/docs#set-up-driver-permission) on GitHub\.

When the plugin is deployed, it creates and is configured to use a service account that's named `ebs-csi-controller-sa`\. The service account is bound to a Kubernetes `clusterrole` that's named `ebs-csi-controller-sa` and is assigned the required Kubernetes permissions\.

**Note**  
No matter if you configure the Amazon EBS CSI plugin to use IAM roles for service accounts, the pods have access to the permissions that are assigned to the IAM role\. This is the case except when you block access to IMDS\. For more information, see [Security best practices for Amazon EKS](security-best-practices.md)\.

1. Create an IAM policy that allows the CSI driver's service account to make calls to AWS APIs on your behalf\. You can view the policy document [on GitHub](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/docs/example-iam-policy.json)\.

   1. Download the IAM policy document from GitHub\.

      ```
      curl -o example-iam-policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-ebs-csi-driver/master/docs/example-iam-policy.json
      ```

   1. If you use a custom KMS key for encryption on your EBS volumes, customize the IAM policy as needed\. For example, add the following to the IAM policy and replace `custom-key-id` with the custom KMS key ID\.

      ```
      {
        "Effect": "Allow",
        "Action": [
          "kms:CreateGrant",
          "kms:ListGrants",
          "kms:RevokeGrant"
        ],
        "Resource": ["custom-key-id"],
        "Condition": {
          "Bool": {
            "kms:GrantIsForAWSResource": "true"
          }
        }
      },
      {
        "Effect": "Allow",
        "Action": [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:ReEncrypt*",
          "kms:GenerateDataKey*",
          "kms:DescribeKey"
        ],
        "Resource": ["custom-key-id"]
      }
      ```

      For instructions on how to use a visual editor, see [Create an IAM policy](create-service-account-iam-policy-and-role.md#create-service-account-iam-policy)\.

   1. Create the policy\. You can change `AmazonEKS_EBS_CSI_Driver_Policy` to a different name, but if you do, make sure to change it in later steps too\.

      ```
      aws iam create-policy \
          --policy-name AmazonEKS_EBS_CSI_Driver_Policy \
          --policy-document file://example-iam-policy.json
      ```

1. Create an IAM role and attach the IAM policy to it\. You can use either `eksctl` or the AWS Management Console\.

------
#### [ eksctl ]

1. Create an IAM role and attach the IAM policy with the following command\. Replace *`my-cluster`* with your own value and *111122223333* with your account ID\. The command deploys an AWS CloudFormation stack that creates an IAM role, attaches the IAM policy to it, and annotates the existing `ebs-csi-controller-sa` service account with the Amazon Resource Name \(ARN\) of the IAM role\. 

   ```
   eksctl create iamserviceaccount \
       --name ebs-csi-controller-sa \
       --namespace kube-system \
       --cluster my-cluster \
       --attach-policy-arn arn:aws:iam::111122223333:policy/AmazonEKS_EBS_CSI_Driver_Policy \
       --approve \
       --role-only
   ```

1. Find the role name that was created by running the following command\. Replace `stack-name` with the stack name from the logs of the previous `eksctl` command\. This role name will be used later\.

   ```
   aws cloudformation describe-stack-resources --query 'StackResources[0].PhysicalResourceId' --output text --stack-name stack-name
   ```

------
#### [ AWS Management Console ]

**To create your Amazon EBS CSI plugin IAM role with the AWS Management Console**

1. In the navigation pane, choose **Roles**, **Create role**\.

1. In the **Select trusted entity** section, choose **Web identity**\.

1. In the **Choose a web identity provider** section:

   1. For **Identity provider**, choose the URL for your cluster\.

   1. For **Audience**, choose `sts.amazonaws.com`\.

1. Choose **Next**\.

1. In the **Filter policies** box, enter `AmazonEKS_EBS_CSI_Driver_Policy`\.

1. Choose **Next: Tags**\.

1. On the **Add tags \(optional\)** screen, you can add tags for the account\. Choose **Next: Review**\.

1. For **Role Name**, enter a name for your role \(for example, *`AmazonEKSEBSCSIRole`*\), and then choose **Create Role**\.

1. After the role is created, choose the role in the console to open it for editing\.

1. Choose the **Trust relationships** tab, and then choose **Edit trust policy**\.

1. Find the line that looks similar to the following\.

   ```
   "oidc.eks.us-west-2.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E:aud": "sts.amazonaws.com"
   ```

   Change the line to look like the following line\. Replace *`EXAMPLED539D4633E53DE1B716D3041E`* with your cluster's OIDC provider ID, `region-code` with the AWS Region code that your cluster is in, and `aud` \(in the previous output\) to `sub`\.

   ```
   "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E:sub": "system:serviceaccount:kube-system:ebs-csi-controller-sa"
   ```

1. Choose **Update policy** to finish\.

------

## Adding the Amazon EBS CSI add\-on<a name="adding-ebs-csi-eks-add-on"></a>

Select the tab with the name of the tool that you want to use to add the Amazon EBS CSI add\-on to your cluster with\.

**Important**  
Before adding the Amazon EBS CSI add\-on, confirm that you don't self\-manage any settings that Amazon EKS will start managing\. To determine which settings Amazon EKS manages, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------
#### [ eksctl ]

**To add the Amazon EBS CSI add\-on using `eksctl`**  
Replace `my-cluster` with the name of your cluster, *111122223333* with your account ID, and `role-name` with the name of the role created earlier\. Then, run the following command\.

```
eksctl create addon --name aws-ebs-csi-driver --cluster my-cluster --service-account-role-arn arn:aws:iam::111122223333:role/role-name --force
```

If you remove the `--force` option and there's a conflict with your existing settings, then the command fails with an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to self\-manage\. This is because those settings are overwritten with this option\. For more information about managing Amazon EKS add\-ons, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------
#### [ AWS Management Console ]

**To add the Amazon EBS CSI add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select Amazon EKS **Clusters**\.

1. Select the name of the cluster that you want to configure the Amazon EBS CSI add\-on for\.

1. Choose the **Configuration** tab\.

1. Choose the **Add\-ons** tab\.

1. Select **Add new**\.

   1. Select **Amazon EBS CSI Driver** for **Name**\.

   1. Select the **Version** you'd like to use\.

   1. For **Service account role**, select the name of an IAM role that you attached the IAM policy to\.

   1. If you select **Override existing configuration for this add\-on on the cluster\.**, then one or more of the settings for the existing add\-on can be overwritten with the Amazon EKS add\-on settings\. If you don't enable this option and there's a conflict with your existing settings, the operation fails with an error message to help you resolve the conflict\. Before selecting this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to self\-manage\. For more information about managing Amazon EKS add\-ons, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

   1. Select **Add**\.

------
#### [ AWS CLI ]

**To add the Amazon EBS CSI add\-on using the AWS CLI**  
Replace `my-cluster` with the name of your cluster, `111122223333` with your account ID, and `role-name` with the name of the role that was created earlier\. Then, run the following command\.

```
aws eks create-addon \
--cluster-name my-cluster \
--addon-name aws-ebs-csi-driver \
--service-account-role-arn arn:aws:iam::111122223333:role/role-name
```

------

## Updating the Amazon EBS CSI driver as an Amazon EKS add\-on<a name="updating-ebs-csi-eks-add-on"></a>

Amazon EKS doesn't automatically update Amazon EBS CSI for your cluster when new versions are released or after you [update your cluster](update-cluster.md) to a new Kubernetes minor version\. To update Amazon EBS CSI on an existing cluster, you must initiate the update and then Amazon EKS updates the add\-on for you\.

**Important**  
Update your cluster and nodes to a new Kubernetes minor version before you update Amazon EBS CSI to the same minor version\.

------
#### [ eksctl ]

**To update the Amazon EBS CSI add\-on using `eksctl`**

1. Check the current version of your Amazon EBS CSI add\-on\. Replace `my-cluster` with your cluster name\.

   ```
   eksctl get addon --name aws-ebs-csi-driver --cluster my-cluster
   ```

   The output is as follows\.

   ```
   NAME            VERSION                 STATUS  ISSUES  IAMROLE UPDATE AVAILABLE
   aws-ebs-csi-driver      v1.4.0-eksbuild.preview      ACTIVE  0               v1.4.0-eksbuild.1
   ```

1. Update the add\-on to the version returned under `UPDATE AVAILABLE` in the output of the previous step\.

   ```
   eksctl update addon \
   --name aws-ebs-csi-driver \
   --version v1.4.0-eksbuild.1 \
   --cluster my-cluster \
   --force
   ```

   If you remove the `--force` option and there's a conflict with your existing settings, then the command fails with an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to self\-manage\. This is because those settings are overwritten with this option\. For more information about managing Amazon EKS add\-ons, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------
#### [ AWS Management Console ]

**To update the Amazon EBS CSI add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select Amazon EKS **Clusters**\.

1. Select the name of the cluster that you want to update the Amazon EBS CSI add\-on for\. 

1. Choose the **Configuration** tab\.

1. Choose the **Add\-ons** tab\.

1. Select the check box in the top right of the **aws\-ebs\-csi\-driver** box\.

1. Choose **Edit**\.

   1. Select the **Version** of the Amazon EKS add\-on that you want to use\.

   1. For **Service account role**, select the name of an IAM role that you've attached the IAM policy to, if one isn't already selected\.

   1. If you select **Override existing configuration for this add\-on on the cluster\.**, then one or more of the settings for the existing add\-on can be overwritten with the Amazon EKS add\-on settings\. If you don't enable this option and there's a conflict with your existing settings, the operation fails with an error message to help you resolve the conflict\. Before selecting this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to self\-manage\. For more information about managing Amazon EKS add\-ons, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

   1. Select **Update**\.

------
#### [ AWS CLI ]

**To update the Amazon EBS CSI add\-on using the AWS CLI**

1. Check the current version of your Amazon EBS CSI add\-on\. Replace `my-cluster` with your cluster name\.

   ```
   aws eks describe-addon \
   --cluster-name my-cluster \
   --addon-name aws-ebs-csi-driver \
   --query "addon.addonVersion" \
   --output text
   ```

   The output is as follows\.

   ```
   v1.4.0-eksbuild.preview
   ```

1. Determine which versions of the Amazon EBS CSI add\-on are available for your cluster version\.

   ```
   aws eks describe-addon-versions \
   --addon-name aws-ebs-csi-driver \
   --kubernetes-version 1.20 \
   --query "addons[].addonVersions[].[addonVersion, compatibilities[].defaultVersion]" \
   --output text
   ```

   The output is as follows\.

   ```
   v1.4.0-eksbuild.preview
   True
   ```

   The version with `True` underneath is the default version deployed with new clusters with the version that you specified\.

1. Update the add\-on to the version with `True` that was returned in the output of the previous step\. You can also update to a later version if it was returned in the output\.

   ```
   aws eks update-addon \
   --cluster-name my-cluster \
   --addon-name aws-ebs-csi-driver \
   --addon-version v1.4.0-eksbuild.preview \
   --resolve-conflicts OVERWRITE
   ```

   If you remove the `--resolve-conflicts OVERWRITE` option and there's a conflict with your existing settings, then the command fails with an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to self\-manage\. This is because those settings are overwritten with this option\. For more information about managing Amazon EKS add\-ons, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------

## Removing the Amazon EBS CSI add\-on<a name="removing-ebs-csi-eks-add-on"></a>

You have two options for removing an Amazon EKS add\-on\.
+ **Preserve add\-on software on your cluster** – This option removes Amazon EKS management of any settings\. It also removes the ability for Amazon EKS to notify you of updates and automatically update the Amazon EKS add\-on after you initiate an update\. However, it preserves the add\-on software on your cluster\. This option makes the add\-on a self\-managed add\-on, rather than an Amazon EKS add\-on\. With this option, there's no downtime for the add\-on\.
+ **Remove add\-on software entirely from your cluster** – We recommend that you remove the Amazon EKS add\-on from your cluster only if there are no resources on your cluster that are dependent on it\. After you remove the Amazon EKS add\-on, you can add it back\.

If the add\-on has an IAM account associated with it, the IAM account isn't removed\.

Select the tab with the name of the tool that you want to use to remove the Amazon EBS CSI add\-on\.

------
#### [ eksctl ]

**To remove the Amazon EBS CSI add\-on using `eksctl`**  
Replace `my-cluster` with the name of your cluster, and then run the following command\. If you remove the add\-on, this removes the add\-on software from your cluster\. If you don't want Amazon EKS to manage any settings for the add\-on, use the AWS Management Console or AWS CLI to remove the add\-on\. Doing this, you can preserve the add\-on software on your cluster\. If you remove `--preserve`, this removes the add\-on software from your cluster\.

```
eksctl delete addon --cluster my-cluster --name aws-ebs-csi-driver --preserve
```

------
#### [ AWS Management Console ]

**To remove the Amazon EBS CSI add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select Amazon EKS **Clusters**\.

1. Select the name of the cluster that you want to remove the Amazon EBS CSI add\-on for\.

1. Choose the **Configuration** tab\.

1. Choose the **Add\-ons** tab\.

1. Select the check box in the top right of the **aws\-ebs\-csi\-driver** box\.

1. Choose **Remove**\.

1. Select **Preserve on cluster** if you want Amazon EKS to stop managing settings for the add\-on\. Do this if you want to retain the add\-on software on your cluster\. This is so that you can manage all of the settings of the add\-on on your own\.

1. Type **`aws-ebs-csi-driver`**\.

1. Select **Remove**\.

------
#### [ AWS CLI ]

**To remove the Amazon EBS CSI add\-on using the AWS CLI**  
Replace `my-cluster` with the name of your cluster, and then run the following command\. If you remove `--preserve`, this removes the add\-on software from your cluster\.

```
aws eks delete-addon --cluster-name my-cluster --addon-name aws-ebs-csi-driver --preserve
```

------