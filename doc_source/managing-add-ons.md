# Managing add\-ons<a name="managing-add-ons"></a>

Amazon EKS add\-ons provides management of a curated set of add\-ons for Amazon EKS clusters\. All Amazon EKS add\-ons include the latest security patches, bug fixes, and are validated by AWS to work with Amazon EKS\. Amazon EKS add\-ons allow you to consistently ensure that your Amazon EKS clusters are secure and stable and reduce the amount of work that you need to do in order manage your add\-ons\. For a list of available add\-ons, see [Managing add\-ons](#managing-add-ons)\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

**Prerequisite**  
An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\.

## Creating an add\-on<a name="creating-an-add-on"></a>

You can create an Amazon EKS add\-on on your cluster with `eksctl`, the AWS Management Console, or the AWS CLI\.

------
#### [ eksctl ]

**To create an Amazon EKS add\-on using `eksctl`**

1. See a list of available add\-ons and the available versions for each add\-on with the following command\. Replace `1.24` with the version of your cluster\.

   ```
   eksctl utils describe-addon-versions --kubernetes-version 1.24 | grep AddonName
   ```

   The output returned is for all available add\-ons, with the `AddonName` property highlighted\. The output also includes the `AddonVersion` property followed by the available versions of each add\-on\.

1. Create an Amazon EKS add\-on with the following command\. Make the following modifications to the command as needed\.
   + Replace `my-cluster` with the name of your cluster\.
   + Replace `my-addon` with the name of the add\-on that you want to create\.
   + This example command creates the add\-on with the latest available version\. If you want an earlier version of the add\-on, then you need to replace `latest` with the version number that you want to use\.
   + If the add\-on uses a service account role, specify the name of an existing IAM role that you've created with the `--service-account-role-arn` option\. For instructions on creating the role, see the documentation for the add\-on that you're creating\. If the add\-on doesn't use a service account role, delete the `--service-account-role-arn` option and its value\.
   + This example command overwrites the configuration of any existing self\-managed version of the add\-on, if there is one\. If you don't want `eksctl` to overwrite the configuration of an existing self\-managed add\-on, remove the `--force` option\. If you remove the option, and the Amazon EKS add\-on needs to overwrite the configuration of an existing self\-managed add\-on, then creation of the Amazon EKS add\-on fails with an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\.

```
eksctl create addon --cluster my-cluster --name my-addon --version latest \
    --service-account-role-arn arn:aws:iam::111122223333:role/role-name --force
```

For a full list of available options, enter the following command\. For more information about other options when using `eksctl`, see [Addons](https://eksctl.io/usage/addons/) in the `eksctl` documentation\. 

```
eksctl create addon --help
```

------
#### [ AWS Management Console ]

**To create an Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to have the add\-on\.

1. Choose the **Add\-ons** tab\.

1. Select **Add new**\.

1. Select the name of the add\-on you’ve chosen for **Name**\.

1. Select the **Version** you'd like to use\. We recommend the **latest** version, unless the individual add\-on that you're creating recommends a different version\. For recommended versions, see the documentation for the add\-on that you're creating\.

1. If the add\-on uses a **service account role**, select the name of an existing IAM role that you've created\. For instructions on creating the role, see the documentation for the add\-on that you're creating\.

1. Select one of the **available options for this add\-on on the cluster**\. If there's already a self\-managed version of the add\-on installed on your cluster, then choose **override existing configuration**\. If you don't choose this option, and any of the Amazon EKS settings conflict with the settings for the existing self\-managed add\-on, then adding the Amazon EKS add\-on fails, and you receive an error message to help you resolve the conflict\.

1. Choose **Add**\.

------
#### [ AWS CLI ]

**To create an Amazon EKS add\-on using the AWS CLI**

1. If you don't know the specific names of the available add\-ons, you can list them with the following command\. Replace `1.24` with the version of your cluster\.

   ```
   aws eks describe-addon-versions --kubernetes-version 1.24
   ```

   A list of the names of the available add\-ons is returned\.

1. \(Optional\) You can see which versions are available for each add\-on with the following command\. Replace `1.24` with the version of your cluster\.

   ```
   aws eks describe-addon-versions --kubernetes-version 1.24 --addon-name my-addon --query addons[].addonVersions[].addonVersion
   ```

   A list of the available versions for the add\-on is returned\.

1. Create an Amazon EKS add\-on with the following command\. Make the following modifications to the command as needed\. For a full list of available options, see `[create\-addon](https://docs.aws.amazon.com/cli/latest/reference/eks/create-addon.html)` in the Amazon EKS Command Line Reference\.
   + Replace `my-cluster` with the name of your cluster\.
   + Replace `my-addon` with the name of the add\-on that you want to create\.
   + Replace `version-number` with the version returned in the output of the previous step that you want to use\. Alternatively, you can delete the option and value to use the latest add\-on version\.
   + If the add\-on uses a service account role, specify the name of an existing IAM role that you've created with the `--service-account-role-arn` option\. For instructions on creating the role, see the documentation for the add\-on that you're creating\. If the add\-on doesn't use a service account role, delete the `--service-account-role-arn` option and its value\.
   + This example command overwrites the configuration of any existing self\-managed version of the add\-on, if there is one\. If you don't want the AWS CLI to overwrite the configuration of an existing self\-managed add\-on, remove the `--resolve-conflicts OVERWRITE` option\. If you remove the option, and the Amazon EKS add\-on needs to overwrite the configuration of an existing self\-managed add\-on, then creation of the Amazon EKS add\-on fails with an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\.

     Alternatively, `--resolve-conflicts PRESERVE` preserves any custom settings that you've set for the add\-on\. For more information about `--resolve-conflicts` options, see `[update\-addon](https://docs.aws.amazon.com/cli/latest/reference/eks/update-addon.html)` in the Amazon EKS Command Line Reference\.

   ```
   aws eks create-addon --cluster-name my-cluster --addon-name my-addon --addon-version version-number \
       --service-account-role-arn arn:aws:iam::111122223333:role/role-name --resolve-conflicts OVERWRITE
   ```

------

## Updating an add\-on<a name="updating-an-add-on"></a>

Amazon EKS doesn't automatically update an add\-on when new versions are released or after you update your cluster to a new Kubernetes minor version\. To update an add\-on for an existing cluster, you must initiate the update\. After you initiate the update, Amazon EKS updates the add\-on for you\.

Before updating an add\-on, review the current documentation for the add\-on\. For a list of available add\-ons, see [Available Amazon EKS add\-ons](eks-add-ons.md#workloads-add-ons-available-add-ons)\.

------
#### [ eksctl ]

**To update an Amazon EKS add\-on using `eksctl`**

1. Check the current add\-ons and add\-on versions installed on your cluster with the following command\. Replace `my-cluster` with your cluster name and `my-addon` with the name of the add\-on that you want to update\.

   ```
   eksctl get addon --cluster my-cluster --name my-addon
   ```

   The returned output includes the names of the add\-ons and the versions of the add\-ons that are currently on your cluster\.

1. If you want to update to a version other than the latest version, you can view all versions available for the add\-on and your cluster's version with the following command\. Replace `1.24` with your cluster's version\.

   ```
   eksctl utils describe-addon-versions --name my-addon --kubernetes-version 1.24 | grep AddonVersion:
   ```

1. Update your add\-on with the following command\. Make the following modifications to the command as needed\.
   + Replace `my-cluster` with the name of your cluster\.
   + Replace `my-addon` with the name of the add\-on that you want to update\.
   + This example command updates the add\-on to the latest available version\. If you want an earlier version of the add\-on, then you need to replace `latest` with the version number that you want to use\.
   + This example command overwrites the configuration of any existing self\-managed version of the add\-on, if there is one\. If you don't want `eksctl` to overwrite the configuration of an existing self\-managed add\-on, remove the `--force` option\. If you remove the option, and the Amazon EKS add\-on needs to overwrite the configuration of an existing self\-managed add\-on, then updating the Amazon EKS add\-on fails with an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\. To fully preserve settings, you must update the add\-on using an `eksctl` config file, because there isn't an option to fully preserve your existing configuration when using the command line alone\.

   ```
   eksctl update addon --cluster my-cluster --name my-addon --version latest --force
   ```

   For more information about other options when using `eksctl`, see [Addons](https://eksctl.io/usage/addons/) in the `eksctl` documentation\.

------
#### [ eksctl config file ]

**To update an Amazon EKS add\-on using an `eksctl` config file**

Rather than Amazon EKS overwriting existing settings for an add\-on, it can preserve your existing settings, and only update settings that you don't manage\. To fully preserve settings, you must update the add\-on using an `eksctl` config file, because there isn't an option to fully preserve your existing configuration when using the command line alone\. If you want to preserve your existing settings, complete the following steps to update the add\-on\.

1. Copy the following contents to your device\. Replace `my-addon` with the name of the add\-on that you want to update and then run the modified command to create an `eksctl` config file\. For the config file schema with additional options that you can specify, see `[addons](https://eksctl.io/usage/schema/#addons)` in the `eksctl` documentation\.

   ```
   cat >update-addon.yaml <<EOF
   addons:
   - name: my-addon
     resolveConflicts: preserve
   EOF
   ```

1. Apply the config file to your cluster\.

   ```
   eksctl update addon -f update-addon.yaml
   ```

------
#### [ AWS Management Console ]

**To update an Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to configure the add\-on for\.

1. Choose the **Add\-ons** tab\.

1. Select the box in the top right of the add\-on box and then choose **Edit**\.

1. Select the **Version** you'd like to use\. For recommended versions see the documentation for that add\-on\.

1. For **Conflict resolution method**, select one of the options\.

1. Choose **Update**\.

------
#### [ AWS CLI ]

**To update an Amazon EKS add\-on using the AWS CLI**

1. \(Optional\) See a list of installed add\-ons with the following command\. Replace `my-cluster` with the name of your cluster\.

   ```
   aws eks list-addons --cluster-name my-cluster
   ```

   The add\-on should appear in the output\. The `addon-name` of the add\-on to be updated can be validated from the `addons` list within the response JSON\.

1. \(Optional\) Check the current version of your add\-on with the following command\. Replace `my-cluster` with your cluster name and `my-addon` with the name of the add\-on that you want to update\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name my-addon --query "addon.addonVersion" --output text
   ```

   The version number of the add\-on that you specified is returned\.

1. \(Optional\) Determine which versions of the add\-on are available for your cluster's version with the following command\. Replace `my-addon` with the name of the add\-on that you want to update and `1.24` with your cluster's version\.

   ```
   aws eks describe-addon-versions --addon-name my-addon --kubernetes-version 1.24 --output text
   ```

   The returned output lists all of the available versions\. Depending on the add\-on, the latest version might not be the recommended version\. To determine whether an add\-on has a recommended version, see the topic for the [individual add\-on](eks-add-ons.md#workloads-add-ons-available-add-ons)\.

1. Update your add\-on with the following command\. Make the following modifications to the command as needed\.
   + Replace `my-cluster` with the name of your cluster\.
   + Replace `my-addon` with the name of the add\-on that you want to update\.
   + Replace `version-number` with the version returned in the output of the previous step that you want to update to\. Alternatively, you can delete the option and value to update to the latest add\-on version\.
   + This example command overwrites the configuration of any existing self\-managed version of the add\-on, if there is one\. If you don't want the AWS CLI to overwrite the configuration of an existing self\-managed add\-on, remove the `--resolve-conflicts OVERWRITE` option\. If you remove the option, and the Amazon EKS add\-on needs to overwrite the configuration of an existing self\-managed add\-on, then creation of the Amazon EKS add\-on fails with an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\.

     Alternatively, `--resolve-conflicts PRESERVE` preserves any custom settings that you've set for the add\-on\. For more information about `--resolve-conflicts` options, see `[update\-addon](https://docs.aws.amazon.com/cli/latest/reference/eks/update-addon.html)` in the Amazon EKS Command Line Reference\.

   ```
   aws eks update-addon --cluster-name my-cluster --addon-name my-addon --addon-version version-number --resolve-conflicts OVERWRITE
   ```

   The update begins to apply any necessary changes to your Kubernetes cluster, which you can monitor using `kubectl` commands\. Each add\-on can deploy different kinds of resources, and you should consult the applicable add\-on documentation to determine which resources you may want to monitor during the update\.

1. The status of the update can be checked by running the following command\. Replace `my-cluster` with the name of your cluster and `my-addon` with the name of the add\-on you are updating\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name my-addon
   ```

------

## Removing an add\-on<a name="removing-an-add-on"></a>

You have two options when removing an Amazon EKS add\-on:
+ **Preserve the add\-on software on your cluster** – This option removes Amazon EKS management of any settings and the ability for Amazon EKS to notify you of updates and automatically update the Amazon EKS add\-on after you initiate an update, but preserves the add\-on's software on your cluster\. This option makes the add\-on a self\-managed add\-on, rather than an Amazon EKS add\-on\. There is no downtime for the add\-on\.
+ **Removing the add\-on software entirely from your cluster** – You should only remove the Amazon EKS add\-on from your cluster if there are no resources on your cluster are dependent on the functionality that the add\-on provides\. After removing the Amazon EKS add\-on, you can add it again if you want to\.

If the add\-on has an IAM account associated with it, the IAM account isn't removed\.

You can remove the Amazon EKS add\-on from your cluster with `eksctl`, the AWS Management Console, or the AWS CLI\.

------
#### [ eksctl ]

**To remove an Amazon EKS add\-on using `eksctl`**  
Replace *`my-cluster`* with the name of your cluster and `my-addon` with the name of the add\-on you want to remove, then run the following command\. Removing `--preserve` removes the add\-on software from your cluster\.

```
eksctl delete addon --cluster my-cluster --name my-addon --preserve
```

------
#### [ AWS Management Console ]

**To remove an Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to remove the Amazon EKS add\-on for\.

1. Choose the **Add\-ons** tab\.

1. Select the check box in the upper right of the add\-on box and then choose **Remove**\. Select **Preserve on the cluster** if you want Amazon EKS to stop managing settings for the add\-on, but want to retain the add\-on software on your cluster so that you can self\-manage all of the add\-on's settings\. Type the add\-on name and then select **Remove**\.

------
#### [ AWS CLI ]

**To remove an Amazon EKS add\-on using the AWS CLI**

1. \(Optional\) See a list of installed add\-ons with the following command\. Replace `my-cluster` with the name of your cluster\.

   ```
   aws eks list-addons --cluster-name my-cluster
   ```

   The add\-on should appear in the output\. The `addon-name` of the add\-on to be deleted can be validated from the `addons` list within the response JSON\.

1. Delete the installed add\-on with the following command\. Replace `my-cluster` with the name of your cluster and `my-addon` with the name of the add\-on that you want to remove\. Removing `--preserve` removes the add\-on software from your cluster\.

   ```
   aws eks delete-addon --cluster-name my-cluster --addon-name my-addon --preserve
   ```

   The response JSON will indicate the state of the request\. If there are issues which require manual action, they will be called out within the JSON response under the health key in the response in the issues list\.

1. The status of the deletion can be checked by running the following command\. Replace `my-cluster` with the name of your cluster and `my-addon` with the name of the add\-on that you are removing\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name my-addon
   ```

------