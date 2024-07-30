# Change authentication mode to use access entries<a name="setting-up-access-entries"></a>

To begin using access entries, you must change the authentication mode of the cluster to either the `API_AND_CONFIG_MAP` or `API` modes\. This adds the API for access entries\.

------
#### [ AWS Management Console ]

**To create an access entry**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the name of the cluster that you want to create an access entry in\.

1. Choose the **Access** tab\.

1. The **Authentication mode** shows the current authentication mode of the cluster\. If the mode says EKS API, you can already add access entries and you can skip the remaining steps\.

1. Choose **Manage access**\.

1. For **Cluster authentication mode**, select a mode with the EKS API\. Note that you can't change the authentication mode back to a mode that removes the EKS API and access entries\.

1. Choose **Save changes**\. Amazon EKS begins to update the cluster, the status of the cluster changes to Updating, and the change is recorded in the **Update history** tab\.

1. Wait for the status of the cluster to return to Active\. When the cluster is Active, you can follow the steps in [Create access entries](creating-access-entries.md) to add access to the cluster for IAM principals\.

------
#### [ AWS CLI ]

**Prerequisite**  
Install the AWS CLI, as described in [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) in the AWS Command Line Interface User Guide\.

1. Run the following command\. Replace *my\-cluster* with the name of your cluster\. If you want to disable the `ConfigMap` method permanently, replace `API_AND_CONFIG_MAP` with `API`\.

   Amazon EKS begins to update the cluster, the status of the cluster changes to UPDATING, and the change is recorded in the aws eks list\-updates\.

   ```
   aws eks update-cluster-config --name my-cluster --access-config authenticationMode=API_AND_CONFIG_MAP
   ```

1. Wait for the status of the cluster to return to Active\. When the cluster is Active, you can follow the steps in [Create access entries](creating-access-entries.md) to add access to the cluster for IAM principals\.

------