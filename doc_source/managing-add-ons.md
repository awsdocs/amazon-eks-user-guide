# Managing Amazon EKS add\-ons<a name="managing-add-ons"></a>

Amazon EKS add\-ons are a curated set of add\-on software for Amazon EKS clusters\. All Amazon EKS add\-ons:
+ include the latest security patches and bug fixes\.
+ are validated by AWS to work with Amazon EKS\.
+ reduce the amount of work required to manage the add\-on software\.

The AWS Management Console notifies you when a new version is available for an Amazon EKS add\-on\. You can simply initiate the update, and Amazon EKS updates the add\-on software for you\. 

For a list of available add\-ons, see [Available Amazon EKS add\-ons from Amazon EKS](eks-add-ons.md#workloads-add-ons-available-eks)\. For more information about Kubernetes field management, see [ Kubernetes field management](kubernetes-field-management.md)<a name="managing-add-ons-prerequisites"></a>

**Prerequisites**
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\.
+ If you're creating an add\-on that uses a Kubernetes service account and IAM role, then you need to have an AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one for your cluster, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.

## Creating an add\-on<a name="creating-an-add-on"></a>

You can create an Amazon EKS add\-on using `eksctl`, the AWS Management Console, or the AWS CLI\. If the add\-on requires an IAM role, see the details for the specific add\-on in [Available Amazon EKS add\-ons from Amazon EKS](eks-add-ons.md#workloads-add-ons-available-eks) for details about creating the role\.

------
#### [ eksctl ]

**Prerequisite**  
Version `0.175.0` or later of the `eksctl` command line tool installed on your device or AWS CloudShell\. To install or update `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.

**To create an Amazon EKS add\-on using `eksctl`**

1. View the names of add\-ons available for a cluster version\. Replace `1.29` with the version of your cluster\.

   ```
   eksctl utils describe-addon-versions --kubernetes-version 1.29 | grep AddonName
   ```

    An example output is as follows\. 

   ```
   "AddonName": "aws-ebs-csi-driver",
                           "AddonName": "coredns",
                           "AddonName": "kube-proxy",
                           "AddonName": "vpc-cni",
                           "AddonName": "adot",
                           "AddonName": "dynatrace_dynatrace-operator",
                           "AddonName": "upbound_universal-crossplane",
                           "AddonName": "teleport_teleport",
                           "AddonName": "factorhouse_kpow",
                           [...]
   ```

1. View the versions available for the add\-on that you would like to create\. Replace `1.29` with the version of your cluster\. Replace `name-of-addon` with the name of the add\-on you want to view the versions for\. The name must be one of the names returned in the previous steps\.

   ```
   eksctl utils describe-addon-versions --kubernetes-version 1.29 --name name-of-addon | grep AddonVersion
   ```

   The following output is an example of what is returned for the add\-on named `vpc-cni`\. You can see that the add\-on has several available versions\.

   ```
   "AddonVersions": [
       "AddonVersion": "v1.12.0-eksbuild.1",
       "AddonVersion": "v1.11.4-eksbuild.1",
       "AddonVersion": "v1.10.4-eksbuild.1",
       "AddonVersion": "v1.9.3-eksbuild.1",
   ```

1. Determine whether the add\-on you want to create is an Amazon EKS or AWS Marketplace add\-on\. The AWS Marketplace has third party add\-ons that require you to complete additional steps to create the add\-on\.

   ```
   eksctl utils describe-addon-versions --kubernetes-version 1.29 --name name-of-addon | grep ProductUrl
   ```

   If no output is returned, then the add\-on is an Amazon EKS\. If output is returned, then the add\-on is an AWS Marketplace add\-on\. The following output is for an add\-on named `teleport_teleport`\. 

   ```
   "ProductUrl": "https://aws.amazon.com/marketplace/pp?sku=3bda70bb-566f-4976-806c-f96faef18b26"
   ```

   You can learn more about the add\-on in the AWS Marketplace with the returned URL\. If the add\-on requires a subscription, you can subscribe to the add\-on through the AWS Marketplace\. If you're going to create an add\-on from the AWS Marketplace, then the [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) that you're using to create the add\-on must have permission to create the [AWSServiceRoleForAWSLicenseManagerRole](https://docs.aws.amazon.com/license-manager/latest/userguide/license-manager-role-core.html) service\-linked role\. For more information about assigning permissions to an IAM entity, see [Adding and removing IAM identity permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html) in the IAM User Guide\.

1. Create an Amazon EKS add\-on\. Copy the command that follows to your device\. Make the following modifications to the command as needed and then run the modified command:
   + Replace `my-cluster` with the name of your cluster\.
   + Replace `name-of-addon` with the name of the add\-on that you want to create\.
   + If you want a version of the add\-on that's earlier than the latest version, then replace `latest` with the version number returned in the output of a previous step that you want to use\.
   + If the add\-on uses a service account role, replace `111122223333` with your account ID and replace `role-name` with the name of the role\. For instructions on creating a role for your service account, see the [documentation](eks-add-ons.md#workloads-add-ons-available-eks) for the add\-on that you're creating\. Specifying a service account role requires that you have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one for your cluster, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.

     If the add\-on doesn't use a service account role, delete `--service-account-role-arn arn:aws:iam::111122223333:role/role-name`\.
   + This example command overwrites the configuration of any existing self\-managed version of the add\-on, if there is one\. If you don't want to overwrite the configuration of an existing self\-managed add\-on, remove the `--force` option\. If you remove the option, and the Amazon EKS add\-on needs to overwrite the configuration of an existing self\-managed add\-on, then creation of the Amazon EKS add\-on fails with an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\.

     ```
     eksctl create addon --cluster my-cluster --name name-of-addon --version latest \
         --service-account-role-arn arn:aws:iam::111122223333:role/role-name --force
     ```

You can see a list of all available options for the command\.

```
eksctl create addon --help
```

For more information about available options see [Addons](https://eksctl.io/usage/addons/) in the `eksctl` documentation\.

------
#### [ AWS Management Console ]

**To create an Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to create the add\-on for\.

1. Choose the **Add\-ons** tab\.

1. Choose **Get more add\-ons**\.

1. Choose the add\-ons that you want to add to your cluster\. You can add as many **Amazon EKS add\-ons** and **AWS Marketplace add\-ons** as you require\.

   For **AWS Marketplace** add\-ons the [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) that you're using to create the add\-on must have permissions to read entitlements for the add\-on from the AWS LicenseManager\. AWS LicenseManager requires [AWSServiceRoleForAWSLicenseManagerRole](https://docs.aws.amazon.com/license-manager/latest/userguide/license-manager-role-core.html) service\-linked role \(SLR\) that allows AWS resources to manage licenses on your behalf\. The SLR is a one time requirement, per account, and you will not have to create separate SLR's for each add\-on nor each cluster\. For more information about assigning permissions to an [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) see [Adding and removing IAM identity permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html) in the IAM User Guide\.

   If the **AWS Marketplace add\-ons** that you want to install aren't listed, you can search for available add\-ons by entering text in the search box\. In the **Filtering options**, you can also filter by **category**, **vendor**, or **pricing model** and then choose the add\-ons from the search results\. Once you've selected the add\-ons that you want to install, choose **Next**\.

1. On the **Configure selected add\-ons settings** page:
   + Choose **View subscription options** to open the **Subscription options** form\. Review the **Pricing details** and **Legal** sections, then choose the **Subscribe** button to continue\.
   + For **Version**, select the version that you want to install\. We recommend the version marked **latest**, unless the individual add\-on that you're creating recommends a different version\. To determine whether an add\-on has a recommended version, see the [documentation](eks-add-ons.md#workloads-add-ons-available-eks) for the add\-on that you're creating\.
   + If all of the add\-ons that you selected have **Requires subscription** under **Status**, select **Next**\. You can't [configure those add\-ons](#updating-an-add-on) further until you've subscribed to them after your cluster is created\. For the add\-ons that don't have **Requires subscription** under **Status**:
     + For **Select IAM role**, accept the default option, unless the add\-on requires IAM permissions\. If the add\-on requires AWS permissions, you can use the IAM role of the node \(**Not set**\) or an existing role that you created for use with the add\-on\. If there's no role to select, then you don't have an existing role\. Regardless of which option your choose, see the [documentation](eks-add-ons.md#workloads-add-ons-available-eks) for the add\-on that you're creating to create an IAM policy and attach it to a role\. Selecting an IAM role requires that you have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one for your cluster, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
     + Choose **Optional configuration settings**\.
       + If the add\-on requires configuration, enter it in the **Configuration values** box\. To determine whether the add\-on requires configuration information, see the [documentation](eks-add-ons.md#workloads-add-ons-available-eks) for the add\-on that you're creating\.
       + Select one of the available options for **Conflict resolution method**\.
     + Choose **Next**\.

1. On the **Review and add** page, choose **Create**\. After the add\-on installation is complete, you see your installed add\-ons\.

1. If any of the add\-ons that you installed require a subscription, complete the following steps:

   1. Choose the **Subscribe** button in the lower right corner for the add\-on\. You're taken to the page for the add\-on in the AWS Marketplace\. Read the information about the add\-on such as its **Product Overview** and **Pricing Information**\.

   1. Select the **Continue to Subscribe** button on the top right of the add\-on page\.

   1. Read through the **Terms and Conditions**\. If you agree to them, choose **Accept Terms**\. It may take several minutes to process the subscription\. While the subscription is processing, the **Return to Amazon EKS Console** button is grayed out\. 

   1. Once the subscription has finished processing, the **Return to Amazon EKS Console** button is no longer grayed out\. Choose the button to go back to the Amazon EKS console **Add\-ons** tab for your cluster\.

   1. For the add\-on that you subscribed to, choose **Remove and reinstall** and then choose **Reinstall add\-on**\. Installation of the add\-on can take several minutes\. When Installation is complete, you can configure the add\-on\.

------
#### [ AWS CLI ]

**Prerequisite**  
Version `2.12.3` or later or version `1.27.160` or later of the AWS Command Line Interface \(AWS CLI\) installed and configured on your device or AWS CloudShell\. To check your current version, use `aws --version | cut -d / -f2 | cut -d ' ' -f1`\. Package managers such `yum`, `apt-get`, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI\. To install the latest version, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with aws configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the *AWS Command Line Interface User Guide*\. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version\. To update it, see [Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the *AWS CloudShell User Guide*\.

**To create an Amazon EKS add\-on using the AWS CLI**

1. Determine which add\-ons are available\. You can see all available add\-ons, their type, and their publisher\. You can also see the URL for add\-ons that are available through the AWS Marketplace\. Replace `1.29` with the version of your cluster\.

   ```
   aws eks describe-addon-versions --kubernetes-version 1.29 \
       --query 'addons[].{MarketplaceProductUrl: marketplaceInformation.productUrl, Name: addonName, Owner: owner Publisher: publisher, Type: type}' --output table
   ```

   An example output is as follows\.

   ```
   ---------------------------------------------------------------------------------------------------------------------------------------------------------
   |                                                                 DescribeAddonVersions                                                                 |
   +---------------------------------------------------------------+-------------------------------+------------------+--------------+---------------------+
   |                     MarketplaceProductUrl                     |             Name              |      Owner       |  Publisher   |        Type         |
   +---------------------------------------------------------------+-------------------------------+------------------+--------------+---------------------+
   |  None                                                         |  aws-ebs-csi-driver           |  aws             |  eks         |  storage            |
   |  None                                                         |  coredns                      |  aws             |  eks         |  networking         |
   |  None                                                         |  kube-proxy                   |  aws             |  eks         |  networking         |
   |  None                                                         |  vpc-cni                      |  aws             |  eks         |  networking         |
   |  None                                                         |  adot                         |  aws             |  eks         |  observability      |
   |  https://aws.amazon.com/marketplace/pp/prodview-brb73nceicv7u |  dynatrace_dynatrace-operator |  aws-marketplace |  dynatrace   |  monitoring         |
   |  https://aws.amazon.com/marketplace/pp/prodview-uhc2iwi5xysoc |  upbound_universal-crossplane |  aws-marketplace |  upbound     |  infra-management   |
   |  https://aws.amazon.com/marketplace/pp/prodview-hd2ydsrgqy4li |  teleport_teleport            |  aws-marketplace |  teleport    |  policy-management  |
   |  https://aws.amazon.com/marketplace/pp/prodview-vgghgqdsplhvc |  factorhouse_kpow             |  aws-marketplace |  factorhouse |  monitoring         |
   |  [...]                                                        |  [...]                        |  [...]           |  [...]       |  [...]              |
   +---------------------------------------------------------------+-------------------------------+------------------+--------------+---------------------+
   ```

   Your output might be different\. In this example output, there are three different add\-ons available of type `networking` and five add\-ons with a publisher of type `eks`\. The add\-ons with `aws-marketplace` in the `Owner` column may require a subscription before you can install them\. You can visit the URL to learn more about the add\-on and to subscribe to it\.

1. You can see which versions are available for each add\-on\. Replace `1.29` with the version of your cluster and replace `vpc-cni` with the name of an add\-on returned in the previous step\.

   ```
   aws eks describe-addon-versions --kubernetes-version 1.29 --addon-name vpc-cni \
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

1. \(Optional\) Find the configuration options for your chosen add\-on by running the following command: 

   ```
   aws eks describe-addon-configuration --addon-name vpc-cni --addon-version v1.12.0-eksbuild.1
   ```

   ```
   {
       "addonName": "vpc-cni",
       "addonVersion": "v1.12.0-eksbuild.1",
       "configurationSchema": "{\"$ref\":\"#/definitions/VpcCni\",\"$schema\":\"http://json-schema.org/draft-06/schema#\",\"definitions\":{\"Cri\":{\"additionalProperties\":false,\"properties\":{\"hostPath\":{\"$ref\":\"#/definitions/HostPath\"}},\"title\":\"Cri\",\"type\":\"object\"},\"Env\":{\"additionalProperties\":false,\"properties\":{\"ADDITIONAL_ENI_TAGS\":{\"type\":\"string\"},\"AWS_VPC_CNI_NODE_PORT_SUPPORT\":{\"format\":\"boolean\",\"type\":\"string\"},\"AWS_VPC_ENI_MTU\":{\"format\":\"integer\",\"type\":\"string\"},\"AWS_VPC_K8S_CNI_CONFIGURE_RPFILTER\":{\"format\":\"boolean\",\"type\":\"string\"},\"AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG\":{\"format\":\"boolean\",\"type\":\"string\"},\"AWS_VPC_K8S_CNI_EXTERNALSNAT\":{\"format\":\"boolean\",\"type\":\"string\"},\"AWS_VPC_K8S_CNI_LOGLEVEL\":{\"type\":\"string\"},\"AWS_VPC_K8S_CNI_LOG_FILE\":{\"type\":\"string\"},\"AWS_VPC_K8S_CNI_RANDOMIZESNAT\":{\"type\":\"string\"},\"AWS_VPC_K8S_CNI_VETHPREFIX\":{\"type\":\"string\"},\"AWS_VPC_K8S_PLUGIN_LOG_FILE\":{\"type\":\"string\"},\"AWS_VPC_K8S_PLUGIN_LOG_LEVEL\":{\"type\":\"string\"},\"DISABLE_INTROSPECTION\":{\"format\":\"boolean\",\"type\":\"string\"},\"DISABLE_METRICS\":{\"format\":\"boolean\",\"type\":\"string\"},\"DISABLE_NETWORK_RESOURCE_PROVISIONING\":{\"format\":\"boolean\",\"type\":\"string\"},\"ENABLE_POD_ENI\":{\"format\":\"boolean\",\"type\":\"string\"},\"ENABLE_PREFIX_DELEGATION\":{\"format\":\"boolean\",\"type\":\"string\"},\"WARM_ENI_TARGET\":{\"format\":\"integer\",\"type\":\"string\"},\"WARM_PREFIX_TARGET\":{\"format\":\"integer\",\"type\":\"string\"}},\"title\":\"Env\",\"type\":\"object\"},\"HostPath\":{\"additionalProperties\":false,\"properties\":{\"path\":{\"type\":\"string\"}},\"title\":\"HostPath\",\"type\":\"object\"},\"Limits\":{\"additionalProperties\":false,\"properties\":{\"cpu\":{\"type\":\"string\"},\"memory\":{\"type\":\"string\"}},\"title\":\"Limits\",\"type\":\"object\"},\"Resources\":{\"additionalProperties\":false,\"properties\":{\"limits\":{\"$ref\":\"#/definitions/Limits\"},\"requests\":{\"$ref\":\"#/definitions/Limits\"}},\"title\":\"Resources\",\"type\":\"object\"},\"VpcCni\":{\"additionalProperties\":false,\"properties\":{\"cri\":{\"$ref\":\"#/definitions/Cri\"},\"env\":{\"$ref\":\"#/definitions/Env\"},\"resources\":{\"$ref\":\"#/definitions/Resources\"}},\"title\":\"VpcCni\",\"type\":\"object\"}}}"
   }
   ```

   The output is a standard JSON schema\.

   Here is an example of valid configuration values, in JSON format, that works with the schema above\.

   ```
   {
     "resources": {
       "limits": {
         "cpu": "100m"
       }
     }
   }
   ```

   Here is an example of valid configuration values, in YAML format, that works with the schema above\.

   ```
     resources: 
       limits: 
         cpu: 100m
   ```

1. Create an Amazon EKS add\-on\. Copy the command that follows to your device\. Make the following modifications to the command as needed and then run the modified command:
   + Replace `my-cluster` with the name of your cluster\.
   + Replace `vpc-cni` with an add\-on name returned in the output of the previous step that you want to create\.
   + Replace `version-number` with the version returned in the output of the previous step that you want to use\.
   + If the add\-on uses a Kubernetes service account and IAM role, replace `111122223333` with your account ID and `role-name` with the name of an existing IAM role that you've created\. For instructions on creating the role, see the [documentation](eks-add-ons.md#workloads-add-ons-available-eks) for the add\-on that you're creating\. Specifying a service account role requires that you have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one for your cluster, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.

     If the add\-on doesn't use a Kubernetes service account and IAM role, delete `--service-account-role-arn arn:aws:iam::111122223333:role/role-name`\.
   + These example commands overwrites the `--configuration-values` option of any existing self\-managed version of the add\-on, if there is one\. Replace this with the desired configuration values, such as a string or a file input\. If you don't want to provide configuration values, then delete the `--configuration-values` option\. If you don't want the AWS CLI to overwrite the configuration of an existing self\-managed add\-on, remove the `--resolve-conflicts OVERWRITE` option\. If you remove the option, and the Amazon EKS add\-on needs to overwrite the configuration of an existing self\-managed add\-on, then creation of the Amazon EKS add\-on fails with an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\.

   ```
   aws eks create-addon --cluster-name my-cluster --addon-name vpc-cni --addon-version version-number \
       --service-account-role-arn arn:aws:iam::111122223333:role/role-name --configuration-values '{"resources":{"limits":{"cpu":"100m"}}}' --resolve-conflicts OVERWRITE
   ```

   ```
   aws eks create-addon --cluster-name my-cluster --addon-name vpc-cni --addon-version version-number \
       --service-account-role-arn arn:aws:iam::111122223333:role/role-name --configuration-values 'file://example.yaml' --resolve-conflicts OVERWRITE
   ```

   For a full list of available options, see `[create\-addon](https://docs.aws.amazon.com/cli/latest/reference/eks/create-addon.html)` in the Amazon EKS Command Line Reference\. If the add\-on that you created has `aws-marketplace` listed in the `Owner` column of a previous step, then creation may fail, and you may receive an error message similar to the following error\.

   ```
   {
       "addon": {
           "addonName": "addon-name",
           "clusterName": "my-cluster",
           "status": "CREATE_FAILED",
           "addonVersion": "version",
           "health": {
               "issues": [
                   {
                       "code": "AddonSubscriptionNeeded",
                       "message": "You are currently not subscribed to this add-on. To subscribe, visit the AWS Marketplace console, agree to the seller EULA, select the pricing type if required, then re-install the add-on"
   [...]
   ```

   If you receive an error similar to the error in the previous output, visit the URL in the output of a previous step to subscribe to the add\-on\. Once subscribed, run the `create-addon` command again\.

------

## Updating an add\-on<a name="updating-an-add-on"></a>

Amazon EKS doesn't automatically update an add\-on when new versions are released or after you update your cluster to a new Kubernetes minor version\. To update an add\-on for an existing cluster, you must initiate the update\. After you initiate the update, Amazon EKS updates the add\-on for you\. Before updating an add\-on, review the current documentation for the add\-on\. For a list of available add\-ons, see [Available Amazon EKS add\-ons from Amazon EKS](eks-add-ons.md#workloads-add-ons-available-eks)\. If the add\-on requires an IAM role, see the details for the specific add\-on in [Available Amazon EKS add\-ons from Amazon EKS](eks-add-ons.md#workloads-add-ons-available-eks) for details about creating the role\.

You can update an Amazon EKS add\-on using `eksctl`, the AWS Management Console, or the AWS CLI\.

------
#### [ eksctl ]

**Prerequisite**  
Version `0.175.0` or later of the `eksctl` command line tool installed on your device or AWS CloudShell\. To install or update `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.

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
      + If you want to update to a version earlier than the latest available version, then replace `latest` with the version number returned in the output of the previous step that you want to use\. Some add\-ons have recommended versions\. For more information, see the [documentation](eks-add-ons.md#workloads-add-ons-available-eks) for the add\-on that you're updating\.
      + If the add\-on uses a Kubernetes service account and IAM role, replace `111122223333` with your account ID and `role-name` with the name of an existing IAM role that you've created\. For instructions on creating the role, see the [documentation](eks-add-ons.md#workloads-add-ons-available-eks) for the add\-on that you're creating\. Specifying a service account role requires that you have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one for your cluster, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.

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

   For more information about updating add\-ons, see [Addons](https://eksctl.io/usage/addons/) in the `eksctl` documentation\.

------
#### [ AWS Management Console ]

**To update an Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to configure the add\-on for\.

1. Choose the **Add\-ons** tab\.

1. Select the box in the top right of the add\-on box and then choose **Edit**\.

1. On the **Configure *name of addon*** page:
   + Select the **Version** that you'd like to use\. The add\-on might have a recommended version\. For more information, see the [documentation](eks-add-ons.md#workloads-add-ons-available-eks) for the add\-on that you're updating\.
   + For **Select IAM role**, you can use the IAM role of the node \(**Not set**\) or an existing role that you created for use with the add\-on\. If there's no role to select, then you don't have an existing role\. Regardless of which option your choose, see the [documentation](eks-add-ons.md#workloads-add-ons-available-eks) for the add\-on that you're creating to create an IAM policy and attach it to a role\. Selecting an IAM role requires that you have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one for your cluster, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
   + For `Code editor`, enter any add\-on specific configuration information\. For more information, see the [documentation](eks-add-ons.md#workloads-add-ons-available-eks) for the add\-on that you're updating\. 
   + For **Conflict resolution method**, select one of the options\. If you have set custom values for add\-on settings, we recommend the **Preserve** option\. If you don't choose this option, Amazon EKS overwrites your values with its default values\. If you use this option, then we recommend that you test any field and value changes on a non\-production cluster before updating the add\-on on your production cluster\.

1. Choose **Update**\.

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

1. You can see which versions of the add\-on are available for your cluster's version\. Replace `1.29` with your cluster's version and `vpc-cni` with the name of the add\-on that you want to update\.

   ```
   aws eks describe-addon-versions --kubernetes-version 1.29 --addon-name vpc-cni \
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

1. Update your add\-on\. Copy the command that follows to your device\. Make the following modifications to the command, as needed, and then run the modified command\.
   + Replace `my-cluster` with the name of your cluster\.
   + Replace `vpc-cni` with the name of the add\-on that you want to update that was returned in the output of a previous step\.
   + Replace `version-number` with the version returned in the output of the previous step that you want to update to\. Some add\-ons have recommended versions\. For more information, see the [documentation](eks-add-ons.md#workloads-add-ons-available-eks) for the add\-on that you're updating\.
   + If the add\-on uses a Kubernetes service account and IAM role, replace `111122223333` with your account ID and `role-name` with the name of an existing IAM role that you've created\. For instructions on creating the role, see the [documentation](eks-add-ons.md#workloads-add-ons-available-eks) for the add\-on that you're creating\. Specifying a service account role requires that you have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one for your cluster, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.

     If the add\-on doesn't use a Kubernetes service account and IAM role, delete the **serviceAccountRoleARN: arn:aws:iam::*111122223333*:role/*role\-name*** line\.
   + The **\-\-resolve\-conflicts** *PRESERVE* option preserves existing values for the add\-on\. If you have set custom values for add\-on settings, and you don't use this option, Amazon EKS overwrites your values with its default values\. If you use this option, then we recommend that you test any field and value changes on a non\-production cluster before updating the add\-on on your production cluster\. If you change this value to `overwrite`, all settings are changed to Amazon EKS default values\. If you've set custom values for any settings, they might be overwritten with Amazon EKS default values\. If you change this value to `none`, Amazon EKS doesn't change the value of any settings, but the update might fail\. If the update fails, you receive an error message to help you resolve the conflict\.
   + If you want to remove all custom configuration then perform the update using the *`--configuration-values '{}'`* option\. This sets all custom configuration back to the default values\. If you don't want to change your custom configuration, don't provide the *`--configuration-values`* flag\. If you want to adjust a custom configuration then replace `{}` with the new parameters\. To see a list of parameters, see [viewing configuration schema](#get-configuration-schema) step in the create an add\-on section\.

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

## Deleting an add\-on<a name="removing-an-add-on"></a>

When you delete an Amazon EKS add\-on:
+ There is no downtime for the functionality that the add\-on provides\.
+ If the add\-on has an IAM role associated with it, the IAM role isn't removed\.
+ Amazon EKS stops managing settings for the add\-on\.
+ The console stops notifying you when new versions are available\.
+ You can't update the add\-on using any AWS tools or APIs\.
+ You can choose to leave the add\-on software on your cluster so that you can self\-manage it, or you can remove the add\-on software from your cluster\. You should only remove the add\-on software from your cluster if there are no resources on your cluster are dependent on the functionality that the add\-on provides\.

You can delete an Amazon EKS add\-on from your cluster using `eksctl`, the AWS Management Console, or the AWS CLI\.

------
#### [ eksctl ]

**Prerequisite**  
Version `0.175.0` or later of the `eksctl` command line tool installed on your device or AWS CloudShell\. To install or update `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.

**To delete an Amazon EKS add\-on using `eksctl`**

1. Determine the current add\-ons installed on your cluster\. Replace `my-cluster` with the name of your cluster\.

   ```
   eksctl get addon --cluster my-cluster
   ```

   An example output is as follows\.

   ```
   NAME        VERSION              STATUS  ISSUES  IAMROLE  UPDATE AVAILABLE
   coredns     v1.8.7-eksbuild.2    ACTIVE  0
   kube-proxy  v1.23.7-eksbuild.1   ACTIVE  0                
   vpc-cni     v1.10.4-eksbuild.1   ACTIVE  0
   [...]
   ```

   Your output might look different, depending on which add\-ons and versions that you have on your cluster\.

1. Delete the add\-on\. Replace *`my-cluster`* with the name of your cluster and `name-of-add-on` with the name of the add\-on returned in the output of the previous step that you want to remove\. If you remove the ***\-\-preserve*** option, in addition to Amazon EKS no longer managing the add\-on, the add\-on software is removed from your cluster\.

   ```
   eksctl delete addon --cluster my-cluster --name name-of-addon --preserve
   ```

------
#### [ AWS Management Console ]

**To delete an Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to remove the Amazon EKS add\-on for\.

1. Choose the **Add\-ons** tab\.

1. Select the check box in the upper right of the add\-on box and then choose **Remove**\. Select **Preserve on the cluster** if you want Amazon EKS to stop managing settings for the add\-on, but want to retain the add\-on software on your cluster so that you can self\-manage all of the settings for the add\-on\. Type the add\-on name and then select **Remove**\.

------
#### [ AWS CLI ]

**Prerequisite**  
Version `0.175.0` or later of the `eksctl` command line tool installed on your device or AWS CloudShell\. To install or update `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.

**To delete an Amazon EKS add\-on using the AWS CLI**

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
           "vpc-cni",
           "name-of-addon"
       ]
   }
   ```

1. Delete the installed add\-on\. Replace `my-cluster` with the name of your cluster and `name-of-add-on` with the name of the add\-on that you want to remove\. Removing ***\-\-preserve*** removes the add\-on software from your cluster\.

   ```
   aws eks delete-addon --cluster-name my-cluster --addon-name name-of-addon --preserve
   ```

   The abbreviated example output is as follows\.

   ```
   {
       "addon": {
           "addonName": "name-of-add-on",
           "clusterName": "my-cluster",
           "status": "DELETING",
   [...]
   ```

1. Check the status of the deletion\. Replace `my-cluster` with the name of your cluster and `name-of-addon` with the name of the add\-on that you're removing\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name name-of-addon
   ```

   After the add\-on is deleted, the example output is as follows\.

   ```
   An error occurred (ResourceNotFoundException) when calling the DescribeAddon operation: No addon: name-of-addon found in cluster: my-cluster
   ```

------

## Retrieve addon version compatibility<a name="addon-compat"></a>

Use the [`describe-addon-verisions` API ](https://docs.aws.amazon.com/eks/latest/APIReference/API_DescribeAddonVersions.html)to list the available versions of EKS addons, and which Kubernetes versions each addon version supports\. 

**Retrieve addon version compatibility \(AWS CLI\)**

1. Verify the AWS CLI is installed and working with `aws sts get-caller-identity`\. If this command doesn't work, learn how to [Get started with the AWS CLI\.](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) 

1. Determine the name of the addon you want to retrieve version compatibility information for, such as `amazon-cloudwatch-observability`\.

1. Determine the Kubernetes version of your cluster, such as `1.28`\.

1. Use the AWS CLI to retrieve the addon versions that are compatible with the Kubernetes version of your cluster\. 

   ```
   aws eks describe-addon-versions --addon-name amazon-cloudwatch-observability --kubernetes-version 1.29
   ```

   An example output is as follows\. 

   ```
   {
       "addons": [
           {
               "addonName": "amazon-cloudwatch-observability",
               "type": "observability",
               "addonVersions": [
                   {
                       "addonVersion": "v1.5.0-eksbuild.1",
                       "architecture": [
                           "amd64",
                           "arm64"
                       ],
                       "compatibilities": [
                           {
                               "clusterVersion": "1.28",
                               "platformVersions": [
                                   "*"
                               ],
                               "defaultVersion": true
                           }
                       ],
   [...]
   ```

   This output shows that addon version `v1.5.0-eksbuild.1` is compatible with Kubernetes cluster version `1.28`\.