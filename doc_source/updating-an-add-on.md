# Updating an Amazon EKS add\-on<a name="updating-an-add-on"></a>

Amazon EKS doesn't automatically update an add\-on when new versions are released or after you update your cluster to a new Kubernetes minor version\. To update an add\-on for an existing cluster, you must initiate the update\. After you initiate the update, Amazon EKS updates the add\-on for you\. Before updating an add\-on, review the current documentation for the add\-on\. For a list of available add\-ons, see [Available Amazon EKS add\-ons from AWS](workloads-add-ons-available-eks.md)\. If the add\-on requires an IAM role, see the details for the specific add\-on in [Available Amazon EKS add\-ons from AWS](workloads-add-ons-available-eks.md) for details about creating the role\.

## Prerequisites<a name="updating-an-add-on-prereq"></a>

Complete the following before you create an add\-on:
+ Check if your add\-on requires an IAM role\. For more information, see [Amazon EKS add\-ons](eks-add-ons.md)\. 
+ Verify that the Amazon EKS add\-on version is compatible with your cluster\. For more information, see [Verifying Amazon EKS add\-on version compatibility with a cluster](addon-compat.md)\.

## Procedure<a name="updating-an-add-on-procedure"></a>

You can update an Amazon EKS add\-on using `eksctl`, the AWS Management Console, or the AWS CLI\.

------
#### [ eksctl ]

**To update an Amazon EKS add\-on using `eksctl`**

1. Determine the current add\-ons and add\-on versions installed on your cluster\. Replace `my-cluster` with the name of your cluster\.

   ```
   eksctl get addon --cluster my-cluster
   ```

   An example output is as follows\.

   ```
   NAME        VERSION              STATUS  ISSUES  IAMROLE  UPDATE AVAILABLE
   coredns     v1.8.7-eksbuild.2    ACTIVE  0
   kube-proxy  v1.23.7-eksbuild.1   ACTIVE  0                v1.23.8-eksbuild.2
   vpc-cni     v1.10.4-eksbuild.1   ACTIVE  0                v1.12.0-eksbuild.1,v1.11.4-eksbuild.1,v1.11.3-eksbuild.1,v1.11.2-eksbuild.1,v1.11.0-eksbuild.1
   ```

   Your output might look different, depending on which add\-ons and versions that you have on your cluster\. You can see that in the previous example output, two existing add\-ons on the cluster have newer versions available in the `UPDATE AVAILABLE` column\.

1. Update the add\-on\.

   1. Copy the command that follows to your device\. Make the following modifications to the command as needed:
      + Replace `my-cluster` with the name of your cluster\.
      + Replace `region-code` with the AWS Region that your cluster is in\.
      + Replace `vpc-cni` with the name of an add\-on returned in the output of the previous step that you want to update\.
      + If you want to update to a version earlier than the latest available version, then replace `latest` with the version number returned in the output of the previous step that you want to use\. Some add\-ons have recommended versions\. For more information, see the [documentation](workloads-add-ons-available-eks.md) for the add\-on that you're updating\.
      + If the add\-on uses a Kubernetes service account and IAM role, replace `111122223333` with your account ID and `role-name` with the name of an existing IAM role that you've created\. For instructions on creating the role, see the [documentation](workloads-add-ons-available-eks.md) for the add\-on that you're creating\. Specifying a service account role requires that you have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one for your cluster, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.

        If the add\-on doesn't use a Kubernetes service account and IAM role, delete the **serviceAccountRoleARN: arn:aws:iam::*111122223333*:role/*role\-name*** line\.
      + The `preserve` option preserves existing values for the add\-on\. If you have set custom values for add\-on settings, and you don't use this option, Amazon EKS overwrites your values with its default values\. If you use this option, then we recommend that you test any field and value changes on a non\-production cluster before updating the add\-on on your production cluster\. If you change this value to `overwrite`, all settings are changed to Amazon EKS default values\. If you've set custom values for any settings, they might be overwritten with Amazon EKS default values\. If you change this value to `none`, Amazon EKS doesn't change the value of any settings, but the update might fail\. If the update fails, you receive an error message to help you resolve the conflict\.

        ```
        cat >update-addon.yaml <<EOF
        apiVersion: eksctl.io/v1alpha5
        kind: ClusterConfig
        metadata:
          name: my-cluster
          region: region-code
        
        addons:
        - name: vpc-cni
          version: latest
          serviceAccountRoleARN: arn:aws:iam::111122223333:role/role-name
          resolveConflicts: preserve
        EOF
        ```

   1. Run the modified command to create the `update-addon.yaml` file\.

   1. Apply the config file to your cluster\.

      ```
      eksctl update addon -f update-addon.yaml
      ```

   For more information about updating add\-ons, see [Updating addons](https://eksctl.io/usage/addons/#updating-addons) in the `eksctl` documentation\.

------
#### [ AWS Management Console ]

**To update an Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, choose **Clusters**\.

1. Choose the name of the cluster that you want to update the add\-on for\.

1. Choose the **Add\-ons** tab\.

1. Choose the add\-on that you want to update\.

1. Choose **Edit**\.

1. On the **Configure *name of addon*** page, do the following:

   1. Choose the **Version** that you'd like to use\. The add\-on might have a recommended version\. For more information, see the [documentation](workloads-add-ons-available-eks.md) for the add\-on that you're updating\.

   1. For **Select IAM role**, you can use the IAM role of the node \(**Not set**\) or an existing role that you created for use with the add\-on\. If there's no role to select, then you don't have an existing role\. Regardless of which option your choose, see the [documentation](workloads-add-ons-available-eks.md) for the add\-on that you're creating to create an IAM policy and attach it to a role\. Selecting an IAM role requires that you have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one for your cluster, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.

   1. Expand the **Optional configuration settings**\.

   1. In **Configuration values**, enter any add\-on specific configuration information\. For more information, see the [documentation](workloads-add-ons-available-eks.md) for the add\-on that you're updating\.

   1. For **Conflict resolution method**, select one of the options\. If you have set custom values for add\-on settings, we recommend the **Preserve** option\. If you don't choose this option, Amazon EKS overwrites your values with its default values\. If you use this option, then we recommend that you test any field and value changes on a non\-production cluster before updating the add\-on on your production cluster\.

1. Choose **Save changes**\.

------
#### [ AWS CLI ]

**Prerequisite**  
Version `2.12.3` or later or version `1.27.160` or later of the AWS Command Line Interface \(AWS CLI\) installed and configured on your device or AWS CloudShell\. To check your current version, use `aws --version | cut -d / -f2 | cut -d ' ' -f1`\. Package managers such `yum`, `apt-get`, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI\. To install the latest version, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with aws configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the *AWS Command Line Interface User Guide*\. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version\. To update it, see [Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the *AWS CloudShell User Guide*\.

**To update an Amazon EKS add\-on using the AWS CLI**

1. See a list of installed add\-ons\. Replace `my-cluster` with the name of your cluster\.

   ```
   aws eks list-addons --cluster-name my-cluster
   ```

   An example output is as follows\.

   ```
   {
       "addons": [
           "coredns",
           "kube-proxy",
           "vpc-cni"
       ]
   }
   ```

1. View the current version of the add\-on that you want to update\. Replace `my-cluster` with your cluster name and `vpc-cni` with the name of the add\-on that you want to update\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name vpc-cni --query "addon.addonVersion" --output text
   ```

   An example output is as follows\.

   ```
   v1.10.4-eksbuild.1
   ```

1. Determine which versions of the add\-on are available for your cluster's version\. Replace `1.30` with your cluster's version and `vpc-cni` with the name of the add\-on that you want to update\.

   ```
   aws eks describe-addon-versions --kubernetes-version 1.30 --addon-name vpc-cni \
       --query 'addons[].addonVersions[].{Version: addonVersion, Defaultversion: compatibilities[0].defaultVersion}' --output table
   ```

   An example output is as follows\.

   ```
   ------------------------------------------
   |          DescribeAddonVersions         |
   +-----------------+----------------------+
   | Defaultversion  |       Version        |
   +-----------------+----------------------+
   |  False          |  v1.12.0-eksbuild.1  |
   |  True           |  v1.11.4-eksbuild.1  |
   |  False          |  v1.10.4-eksbuild.1  |
   |  False          |  v1.9.3-eksbuild.1   |
   +-----------------+----------------------+
   ```

   The version with `True` in the `Defaultversion` column is the version that the add\-on is created with, by default\.

1. Update your add\-on\. Copy the command that follows to your device\. Make the following modifications to the command, as needed, and then run the modified command\. For more information about this command, see [https://docs.aws.amazon.com/cli/latest/reference/eks/update-addon.html](https://docs.aws.amazon.com/cli/latest/reference/eks/update-addon.html) in the Amazon EKS Command Line Reference\.
   + Replace `my-cluster` with the name of your cluster\.
   + Replace `vpc-cni` with the name of the add\-on that you want to update that was returned in the output of a previous step\.
   + Replace `version-number` with the version returned in the output of the previous step that you want to update to\. Some add\-ons have recommended versions\. For more information, see the [documentation](workloads-add-ons-available-eks.md) for the add\-on that you're updating\.
   + If the add\-on uses a Kubernetes service account and IAM role, replace `111122223333` with your account ID and `role-name` with the name of an existing IAM role that you've created\. For instructions on creating the role, see the [documentation](workloads-add-ons-available-eks.md) for the add\-on that you're creating\. Specifying a service account role requires that you have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one for your cluster, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.

     If the add\-on doesn't use a Kubernetes service account and IAM role, delete the **serviceAccountRoleARN: arn:aws:iam::*111122223333*:role/*role\-name*** line\.
   + The **\-\-resolve\-conflicts** *PRESERVE* option preserves existing values for the add\-on\. If you have set custom values for add\-on settings, and you don't use this option, Amazon EKS overwrites your values with its default values\. If you use this option, then we recommend that you test any field and value changes on a non\-production cluster before updating the add\-on on your production cluster\. If you change this value to `OVERWRITE`, all settings are changed to Amazon EKS default values\. If you've set custom values for any settings, they might be overwritten with Amazon EKS default values\. If you change this value to `NONE`, Amazon EKS doesn't change the value of any settings, but the update might fail\. If the update fails, you receive an error message to help you resolve the conflict\.
   + If you want to remove all custom configuration then perform the update using the *`--configuration-values '{}'`* option\. This sets all custom configuration back to the default values\. If you don't want to change your custom configuration, don't provide the *`--configuration-values`* flag\. If you want to adjust a custom configuration then replace `{}` with the new parameters\. To see a list of parameters, see [viewing configuration schema](creating-an-add-on.md#get-configuration-schema) step in the create an add\-on section\.

   ```
   aws eks update-addon --cluster-name my-cluster --addon-name vpc-cni --addon-version version-number \
       --service-account-role-arn arn:aws:iam::111122223333:role/role-name --configuration-values '{}' --resolve-conflicts PRESERVE
   ```

1. Check the status of the update\. Replace `my-cluster` with the name of your cluster and `vpc-cni` with the name of the add\-on you're updating\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name vpc-cni
   ```

   An example output is as follows\.

   ```
   {
       "addon": {
           "addonName": "vpc-cni",
           "clusterName": "my-cluster",
           "status": "UPDATING",
   [...]
   ```

   The update is complete when the status is `ACTIVE`\.

------