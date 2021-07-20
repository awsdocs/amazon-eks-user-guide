# Managing the Amazon VPC CNI add\-on<a name="managing-vpc-cni"></a>

Amazon EKS supports native VPC networking with the Amazon VPC Container Network Interface \(CNI\) plugin for Kubernetes\. Using this plugin allows Kubernetes pods to have the same IP address inside the pod as they do on the VPC network\. For more information, see [Pod networking \(CNI\)](pod-networking.md)\. <a name="vpc-cni-versions"></a>

The following table lists the recommend Amazon VPC CNI version for each supported Kubernetes cluster version\.


**Recommended Amazon VPC CNI plugin version for each Amazon EKS supported cluster version**  

| Kubernetes version | 1\.21 | 1\.20 | 1\.19 | 1\.18 | 1\.17 | 1\.16 | 
| --- | --- | --- | --- | --- | --- | --- | 
| VPC CNI | 1\.8\.x \(latest patch version\) | 1\.8\.x \(latest patch version\) | 1\.8\.x \(latest patch version\) | 1\.8\.x \(latest patch version\) | 1\.8\.x \(latest patch version\) | 1\.8\.x \(latest patch version\) | 

If you have a 1\.18 or later cluster that you have not added the VPC CNI Amazon EKS add\-on to, you can add it using the procedure in [Adding the Amazon VPC CNI Amazon EKS add\-on](#adding-vpc-cni-eks-add-on)\. If you've added the Amazon VPC CNI Amazon EKS add\-on to your 1\.16 or later cluster, you can manage it using the procedures in the [Updating the Amazon VPC CNI Amazon EKS add\-on](#updating-vpc-cni-eks-add-on) and [Removing the Amazon VPC CNI Amazon EKS add\-on](#removing-vpc-cni-eks-add-on) sections\. For more information about Amazon EKS add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\.

If you have not added the Amazon VPC CNI Amazon EKS add\-on, the Amazon VPC CNI add\-on is still running on your cluster\. You can manually update the `vpc-cni` add\-on using the procedure in the [Updating the Amazon VPC CNI add\-on manually](#updating-vpc-cni-add-on) section\.

## Adding the Amazon VPC CNI Amazon EKS add\-on<a name="adding-vpc-cni-eks-add-on"></a>

Before adding this add\-on, we recommend that you enable the OIDC provider for your cluster and create an IAM role with the [AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor) IAM policy attached to it, if you aren't already doing this for this add\-on\. For more information, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md) and [Configuring the Amazon VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.

Select the tab with the name of the tool that you want to use to add the `vpc-cni` Amazon EKS add\-on to your cluster with\.

------
#### [ eksctl ]

To add the `vpc-cni` Amazon EKS add\-on using `eksctl`\. Replace *`my-cluster`* \(including `<>`\) with the name of your cluster and the ARN with the ARN for your existing IAM role with your own\.

```
eksctl create addon \
    --name vpc-cni \
    --version latest \
    --cluster <my-cluster> \
    --service-account-role-arn arn:aws:iam::<111122223333>:role/<eksctl-my-cluster-addon-iamserviceaccount-kube-sys-Role1-UK9MQSLXK0MW> \
    --force
```

If you remove the `--force` option and any of the Amazon EKS add\-on settings conflict with your existing settings, then adding the Amazon EKS add\-on fails, and you receive an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------
#### [ AWS Management Console ]

**To add the Amazon VPC CNI Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation, select **Clusters**, and then select the name of the cluster that you want to configure the Amazon VPC CNI Amazon EKS add\-on for\.

1. Choose the **Configuration** tab and then choose the **Add\-ons** tab\.

1. Select **Add new**\.
   + Select **`vpc-cni`** for **Name**\.
   + Select the **Version** you'd like to use\. We recommend the version marked **Latest**\.
   + \(Optional, but recommended\) For **Service account role**, select the name of an IAM role that you've attached the [AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor) IAM policy to\. Doing so requires that you've enabled the OIDC provider for your cluster and have an existing IAM role\. For more information, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md) and [Configuring the Amazon VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.
   + If you select **Override existing configuration for this add\-on on the cluster\.**, then any setting for the existing add\-on can be overwritten with the Amazon EKS add\-on's settings\. If you don't enable this option and any of the Amazon EKS add\-on settings conflict with your existing settings, then adding the Amazon EKS add\-on fails, and you receive an error message to help you resolve the conflict\. Before selecting this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.
   + Select **Add**\.

------
#### [ AWS CLI ]

1. Determine which versions of the Amazon VPC CNI Amazon EKS add\-on are available for your cluster's version\.

   ```
   aws eks describe-addon-versions \
       --addon-name vpc-cni \
       --kubernetes-version 1.21 \
       --query "addons[].addonVersions[].[addonVersion, compatibilities[].defaultVersion]" \
       --output text
   ```

   Output

   ```
   ...
   1.7.x
   True
   ...
   1.8.x
   False
   ```

   The version with `True` underneath is the default version deployed with new clusters\.

1. To add the Amazon VPC CNI Amazon EKS add\-on using the AWS CLI, replace *<my\-cluster>* \(including `<>`\) with the name of your cluster, *`<AWS_ACCOUNT_ID>`*, with your account ID, *<AmazonEKSCNIRole>* with the name of your existing IAM role, *<1\.8\.*x*>* with the version you want to add, and run the command\.

   ```
   aws eks create-addon \
       --cluster-name <my-cluster> \
       --addon-name vpc-cni \
       --addon-version <1.8.x> \
       --service-account-role-arn arn:aws:iam::<AWS_ACCOUNT_ID>:role/<AmazonEKSCNIRole> \
       --resolve-conflicts OVERWRITE
   ```

   We recommend using the `--service-account-role-arn` `my-ARN` in the previous command, specifying the ARN of an IAM role that you've attached the [AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor) IAM policy to\. Doing so requires that you've enabled the OIDC provider for your cluster and have an existing IAM role\. For more information, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md) and [Configuring the Amazon VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\. 

   If you remove the `--resolve-conflicts OVERWRITE` option and any of the Amazon EKS add\-on settings conflict with your existing settings, then creating the add\-on fails, and you receive an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------

## Updating the Amazon VPC CNI Amazon EKS add\-on<a name="updating-vpc-cni-eks-add-on"></a>

This procedure is for updating the Amazon VPC CNI Amazon EKS add\-on\. If you haven't added the Amazon VPC CNI Amazon EKS add\-on, complete the procedure in [Updating the Amazon VPC CNI add\-on manually](#updating-vpc-cni-add-on) instead\. Amazon EKS does not automatically update the VPC CNI add\-on when new versions are released or after you [update your cluster](update-cluster.md) to a new Kubernetes minor version\. To update the Amazon VPC CNI add\-on for an existing cluster, you must initiate the update and then Amazon EKS updates the add\-on for you\.

We recommend that you update to the latest patch version for the latest minor version, but that you only update one minor version at a time\. For example, if your current version is 1\.6\.*x* and you want to update to 1\.8\.*x*, you should update to the latest patch version of 1\.7 first, then update to the latest patch version of 1\.8\.

------
#### [ eksctl ]

**To update the `vpc-cni` Amazon EKS add\-on using `eksctl`**

1. Check the current version of your `vpc-cni` Amazon EKS add\-on\. Replace *<my\-cluster>* \(including *<>*\) with your cluster name\.

   ```
   eksctl get addon --name vpc-cni --cluster <my-cluster>
   ```

   Output

   ```
   NAME    VERSION                 STATUS  ISSUES  IAMROLE                                                                                                   UPDATE AVAILABLE
   vpc-cni v1.7.x      ACTIVE  0       arn:aws:iam::<111122223333>:role/<eksctl-my-cluster-addon-iamserviceaccount-kube-sys-Role1-UK9MQSLXK0MW>  1.8.x
   ```

1. Update the add\-on to the version returned under `UPDATE AVAILABLE` in the output of the previous step\.

   ```
   eksctl update addon \
       --name vpc-cni \
       --version <1.8.x> \
       --cluster <my-cluster> \
       --force
   ```

   If you remove the `--force` option and any of the Amazon EKS add\-on settings conflict with your existing settings, then updating the add\-on fails, and you receive an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------
#### [ AWS Management Console ]

**To update the Amazon VPC CNI Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation, select **Clusters**, and then select the name of the cluster that you want to update the Amazon VPC CNI add\-on for\.

1. Choose the **Configuration** tab and then choose the **Add\-ons** tab\.

1. Select the box in the top right of the **vpc\-cni** box and then choose **Edit**\.
   + Select the **Version** of the Amazon EKS add\-on that you want to use\. We recommend the version marked **Latest**\.
   + \(Optional, but recommended\) For **Service account role**, select the name of an IAM role that you've attached the [AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor) IAM policy to, if one isn't already selected\. Selecting a role requires that you've enabled the OIDC provider for your cluster\. For more information, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md) and [Configuring the Amazon VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.
   + If you select **Override existing configuration for this add\-on on the cluster\.**, then any setting for the existing add\-on can be overwritten with the Amazon EKS add\-on's settings\. If you don't enable this option and any of the Amazon EKS add\-on settings conflict with your existing settings, then updating the add\-on to an Amazon EKS add\-on fail, and you receive an error message to help you resolve the conflict\. Before selecting this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.
   + Select **Update**\.

------
#### [ AWS CLI ]

**To update the Amazon VPC CNI Amazon EKS add\-on using the AWS CLI**

1. Check the current version of your Amazon VPC CNI Amazon EKS add\-on\. Replace *my\-cluster* with your cluster name\.

   ```
   aws eks describe-addon \
       --cluster-name my-cluster \
       --addon-name vpc-cni \
       --query "addon.addonVersion" \
       --output text
   ```

   Output:

   ```
   1.7.0
   ```

1. Determine which versions of the Amazon VPC CNI Amazon EKS add\-on are available for your cluster's version\.

   ```
   aws eks describe-addon-versions \
       --addon-name vpc-cni \
       --kubernetes-version 1.21 \
       --query "addons[].addonVersions[].[addonVersion, compatibilities[].defaultVersion]" \
       --output text
   ```

   Output

   ```
   ...
   1.7.x
   True
   ...
   1.8.x
   False
   ```

   The version with `True` underneath is the default version deployed with new clusters\.

1. Update the add\-on to the latest patch version of the latest minor version returned in the previous output\.

   ```
   aws eks update-addon \
       --cluster-name my-cluster \
       --addon-name vpc-cni \
       --addon-version 1.8.x \
       --resolve-conflicts OVERWRITE
   ```

   We recommend adding `--service-account-role-arn` `my-ARN` to the previous command, specifying the ARN of an IAM role that you've attached the [AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor) IAM policy to\. Doing so requires that you've enabled the OIDC provider for your cluster\. For more information, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md) and [Configuring the Amazon VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.

   If you remove the `--resolve-conflicts OVERWRITE` option and any of the Amazon EKS add\-on settings conflict with your existing settings, then updating the add\-on fails, and you receive an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------

## Removing the Amazon VPC CNI Amazon EKS add\-on<a name="removing-vpc-cni-eks-add-on"></a>

**Important**  
Removing the Amazon EKS add\-on from your cluster removes its pods from your cluster, not just the settings that were managed by Amazon EKS\. You should only remove the Amazon EKS add\-on from your cluster if none of the pods on your cluster are dependent on the functionality that the add\-on provides\. After removing the Amazon EKS add\-on, you can add it again if you want to\.

------
#### [ eksctl ]

Remove the `vpc-cni` Amazon EKS add\-on with the following command\. Replace *`my-cluster`* \(including `<>`\) with the name of your cluster\.

```
eksctl delete addon --cluster <my-cluster> --name vpc-cni
```

------
#### [ AWS Management Console ]

**To remove the Amazon VPC CNI Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation, select **Clusters**, and then select the name of the cluster that you want to remove the Amazon VPC CNI Amazon EKS add\-on for\.

1. Choose the **Configuration** tab and then choose the **Add\-ons** tab\.

1. Select the checkbox in the top right of the **`vpc-cni`** box and then choose **Remove**\. Type **`vpc-cni`** and then select **Remove**\.

------
#### [ AWS CLI ]

Remove the Amazon VPC CNI Amazon EKS add\-on with the following command\. Replace *my\-cluster* with the name of your cluster\.

```
aws eks delete-addon --cluster-name my-cluster --addon-name vpc-cni
```

------

## Updating the Amazon VPC CNI add\-on manually<a name="updating-vpc-cni-add-on"></a>

If you have a 1\.17 or earlier cluster, or a 1\.18 or later cluster that you have not added the Amazon VPC CNI add\-on to, complete the following steps to update the add\-on\. If you've added the Amazon VPC CNI Amazon EKS add\-on, complete the procedure in [Updating the Amazon VPC CNI Amazon EKS add\-on](#updating-vpc-cni-eks-add-on) instead\.

**To determine your current Amazon VPC CNI add\-on version**
+ Use the following command to determine your cluster's CNI version:

  ```
  kubectl describe daemonset aws-node --namespace kube-system | grep Image | cut -d "/" -f 2
  ```

  Output:

  ```
  amazon-k8s-cni:1.7.x
  ```

  In this example output, the CNI version is 1\.7\.*x*, which is earlier than the latest patch for minor version 1\.8\. Use the following procedure to update the Amazon VPC CNI plugin\.

**To update the Amazon VPC CNI add\-on**
+ If your CNI version is earlier than the latest patch for minor version 1\.8\.*x*, and you are managing the plugin yourself, then use the appropriate command below to update your CNI version to the latest patch for minor version 1\.8\.*x*\. You can view the [latest patch version](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/config/v1.7/aws-k8s-cni.yaml#L156) on GitHub\. If you have a cluster with version 1\.18 or later and are using the the Amazon VPC CNI Amazon EKS add\-on, then to update the add\-on, see [Updating the Amazon VPC CNI Amazon EKS add\-on](#updating-vpc-cni-eks-add-on)\.
**Important**  
Any changes you've made to the plugin's default settings on your cluster can be overwritten with default settings when applying the new version of the manifest\. To prevent loss of your custom settings, download the manifest, change the default settings as necessary, and then apply the modified manifest to your cluster\. You should only update one minor version at a time\. For example, if your current version is 1\.6 and you want to update to 1\.8, you should update to 1\.7 first, then update to 1\.8\.
  + China \(Beijing\) \(`cn-north-1`\) or China \(Ningxia\) \(`cn-northwest-1`\)

    ```
    kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.8/config/v1.8/aws-k8s-cni-cn.yaml
    ```
  + AWS GovCloud \(US\-East\) \(`us-gov-east-1`\)

    ```
    kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.8/config/v1.8/aws-k8s-cni-us-gov-east-1.yaml
    ```
  + AWS GovCloud \(US\-West\) \(`us-gov-west-1`\)

    ```
    kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.8/config/v1.8/aws-k8s-cni-us-gov-west-1.yaml
    ```
  + For all other Regions
    + Download the manifest file\.

      ```
      curl -o aws-k8s-cni.yaml https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.8/config/v1.8/aws-k8s-cni.yaml
      ```
    + If necessary, replace `<region-code>` in the following command with the Region that your cluster is in and then run the modified command to replace the Region code in the file \(currently `us-west-2`\)\.

      ```
      sed -i.bak -e 's/us-west-2/<region-code>/' aws-k8s-cni.yaml
      ```
    + If necessary, replace `<account>` in the following command with the account from [Amazon EKS add\-on container image addresses](add-ons-images.md) for the Region that your cluster is in and then run the modified command to replace the account in the file \(currently `602401143452`\)\.

      ```
      sed -i.bak -e 's/602401143452/<account>/' aws-k8s-cni.yaml
      ```
    + Apply the manifest file to your cluster\.

      ```
      kubectl apply -f aws-k8s-cni.yaml
      ```