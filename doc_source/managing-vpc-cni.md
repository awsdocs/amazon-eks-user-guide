# Managing the Amazon VPC CNI add\-on<a name="managing-vpc-cni"></a>

Amazon EKS supports native VPC networking with the Amazon VPC Container Network Interface \(CNI\) plugin for Kubernetes\. Using this plugin allows Kubernetes pods to have the same IP address inside the pod as they do on the VPC network\. For more information, see [Pod networking \(CNI\)](pod-networking.md)\. 

If you have a 1\.18 or later cluster that you've not added the Amazon VPC CNI Amazon EKS add\-on to, you can add it using the procedure in [Adding the Amazon VPC CNI Amazon EKS add\-on](#adding-vpc-cni-eks-add-on)\. If you have a cluster that you've already added the Amazon VPC CNI Amazon EKS add\-on to, you can manage it using the procedures in the [Updating the Amazon VPC CNI Amazon EKS add\-on](#updating-vpc-cni-eks-add-on) and [Removing the Amazon VPC CNI Amazon EKS add\-on](#removing-vpc-cni-eks-add-on) sections\. For more information about Amazon EKS add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\.

If you have not added the Amazon VPC CNI Amazon EKS add\-on, the Amazon VPC CNI self\-managed add\-on is running on your cluster, by default\. You can update the add\-on using the procedure in [Updating the Amazon VPC CNI self\-managed add\-on](#updating-vpc-cni-add-on)\.


**Version of Amazon VPC CNI add\-on deployed with new clusters**  

| Amazon VPC CNI version | 1\.20 or earlier cluster | 1\.21 or later cluster | 
| --- | --- | --- | 
| Self\-managed add\-on | 1\.7\.5\-eksbuild\.1 | 1\.10\.1\-eksbuild\.1 | 
| Amazon EKS add\-on | 1\.7\.5\-eksbuild\.2 | 1\.10\.1\-eksbuild\.1 | <a name="manage-vpc-cni-add-on-on-prerequisites"></a>

**Prerequisites**
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\.
+ An existing AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ An IAM role with the [AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor) IAM policy \(if your cluster uses the IPv4 family\) or an [IPv6 policy](cni-iam-role.md#cni-iam-role-create-ipv6-policy) \(if your cluster uses the IPv6 family\) attached to it\. For more information, see [Configuring the Amazon VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.
+ If you are using version 1\.7\.0 or later of the CNI plugin and you use custom pod security policies, see [Delete the default Amazon EKS pod security policy](pod-security-policy.md#psp-delete-default)[Pod security policy](pod-security-policy.md)\.

## Adding the Amazon VPC CNI Amazon EKS add\-on<a name="adding-vpc-cni-eks-add-on"></a>

Select the tab with the name of the tool that you want to use to add the Amazon VPC CNI Amazon EKS add\-on to your 1\.18 or later cluster with\.

**Important**  
Before adding the Amazon VPC CNI Amazon EKS add\-on, confirm that you do not self\-manage any settings that Amazon EKS will start managing\. To determine which settings Amazon EKS manages, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------
#### [ eksctl ]

**To add the latest minor, patch, and build version of the Amazon EKS add\-on using `eksctl`**  
Replace *`my-cluster`* with the name of your cluster and `arn:aws:iam::111122223333:role/eksctl-my-cluster-addon-iamserviceaccount-kube-sys-Role1-UK9MQSLXK0MW` with your existing IAM role \(see [Prerequisites](#manage-vpc-cni-add-on-on-prerequisites)\)\.

```
eksctl create addon \
    --name vpc-cni \
    --version latest \
    --cluster my-cluster \
    --service-account-role-arn arn:aws:iam::111122223333:role/eksctl-my-cluster-addon-iamserviceaccount-kube-sys-Role1-UK9MQSLXK0MW \
    --force
```

If any of the Amazon EKS add\-on settings conflict with the existing settings for the self\-managed add\-on, then adding the Amazon EKS add\-on fails, and you receive an error message to help you resolve the conflict\.

------
#### [ AWS Management Console ]

**To add the latest minor, patch, and build version of the Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation, select **Clusters**, and then select the name of the cluster that you want to configure the Amazon VPC CNI Amazon EKS add\-on for\.

1. Choose the **Configuration** tab and then choose the **Add\-ons** tab\.

1. Select **Add new**\.
   + Select **`vpc-cni`** for **Name**\.
   + Select the **Version** you'd like to use\. We recommend the version marked **Latest**\.
   + For **Service account role**, select the name of an IAM role that you've attached the [AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor) IAM policy to \(see [Prerequisites](#manage-vpc-cni-add-on-on-prerequisites)\)\.
   + Select **Override existing configuration for this add\-on on the cluster\.** If any of the Amazon EKS add\-on settings conflict with the existing settings for the self\-managed add\-on, then adding the Amazon EKS add\-on fails, and you receive an error message to help you resolve the conflict\.
   + Select **Add**\.

------
#### [ AWS CLI ]

**To add the latest minor, patch, and build version of the Amazon EKS add\-on using the AWS CLI**

1. Determine which versions of the Amazon VPC CNI Amazon EKS add\-on are available for your cluster's version\. In the following command, replace *1\.20* with your cluster's version\.

   ```
   aws eks describe-addon-versions \
       --addon-name vpc-cni \
       --kubernetes-version 1.20 \
       --query "addons[].addonVersions[].[addonVersion, compatibilities[].defaultVersion]" \
       --output text
   ```

   Output

   ```
   v1.10.1-eksbuild.1
   False
   ...
   v1.7.5-eksbuild.2
   True
   ...
   ```

   The version with `True` underneath is the default version deployed with new clusters\. In the previous output, *v1\.10\.1\-eksbuild\.1* is the latest available version\.

1. In the following command, replace *my\-cluster* with the name of your cluster, *v1\.10\.1\-eksbuild\.1* with the latest available version, `arn:aws:iam::AWS_ACCOUNT_ID:role/AmazonEKSCNIRole` with the ARN of an IAM role that you've attached the [AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor) IAM policy to \(see [Prerequisites](#manage-vpc-cni-add-on-on-prerequisites)\), and then run the command\.

   ```
   aws eks create-addon \
       --cluster-name my-cluster \
       --addon-name vpc-cni \
       --addon-version v1.10.1-eksbuild.1 \
       --service-account-role-arn arn:aws:iam::AWS_ACCOUNT_ID:role/AmazonEKSCNIRole \
       --resolve-conflicts OVERWRITE
   ```

   If any of the Amazon EKS add\-on settings conflict with the existing settings for the self\-managed add\-on, then adding the Amazon EKS add\-on fails, and you receive an error message to help you resolve the conflict\.

------

## Updating the Amazon VPC CNI Amazon EKS add\-on<a name="updating-vpc-cni-eks-add-on"></a>

**Important**  
Before updating the Amazon VPC CNI Amazon EKS add\-on, confirm that you do not self\-manage any settings that Amazon EKS manages\. To determine which settings Amazon EKS manages, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

This procedure is for updating the Amazon VPC CNI Amazon EKS add\-on\. If you haven't added the Amazon VPC CNI Amazon EKS add\-on, complete the procedure in [Updating the Amazon VPC CNI self\-managed add\-on](#updating-vpc-cni-add-on) instead\. Amazon EKS does not automatically update the Amazon VPC CNI add\-on when new versions are released or after you [update your cluster](update-cluster.md) to a new Kubernetes minor version\. To update the Amazon VPC CNI add\-on for an existing cluster, you must initiate the update and then Amazon EKS updates the add\-on for you\.

We recommend that you update to the latest build and patch version for the latest minor version, but that you only update one minor version at a time\. For example, if your current minor version is `1.8` and you want to update to `1.10`, you should update to the latest patch and build version of `1.9` first, then update to the latest patch and build version of `1.10`\.

Select the tab with the name of the tool that you want to use to update the Amazon VPC CNI Amazon EKS add\-on on your 1\.18 or later cluster with\.

------
#### [ eksctl ]

**To update the Amazon EKS add\-on to the latest minor, patch, and build version using `eksctl`**

1. Check the current version of your `vpc-cni` Amazon EKS add\-on\. Replace *my\-cluster* with your cluster name\.

   ```
   eksctl get addon --name vpc-cni --cluster my-cluster
   ```

   Output

   ```
   NAME    VERSION                 STATUS  ISSUES  IAMROLE                                                                                                   UPDATE AVAILABLE
   vpc-cni v1.7.5-eksbuild.2       ACTIVE  0       arn:aws:iam::111122223333:role/eksctl-my-cluster-addon-iamserviceaccount-kube-sys-Role1-UK9MQSLXK0MW      v1.10.1-eksbuild.1
   ```

1. Update the add\-on to the latest minor, patch, and build version\.

   ```
   eksctl update addon \
       --name vpc-cni \
       --version latest \
       --cluster my-cluster \
       --force
   ```

------
#### [ AWS Management Console ]

**To update the Amazon EKS add\-on to the latest minor, patch, and build version using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation, select **Clusters**, and then select the name of the cluster that you want to update the Amazon VPC CNI add\-on for\.

1. Choose the **Configuration** tab and then choose the **Add\-ons** tab\.

1. Select the box in the top right of the **vpc\-cni** box and then choose **Edit**\.
   + Select the **Version** of the Amazon EKS add\-on that you want to use\. We recommend the version marked **Latest**\.
   + For **Service account role**, select the name of an IAM role that you've attached the [AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor) IAM policy to \(see [Prerequisites](#manage-vpc-cni-add-on-on-prerequisites)\), if one isn't already selected\.
   + Select **Override existing configuration for this add\-on on the cluster\.**
   + Select **Update**\.

------
#### [ AWS CLI ]

**To update the Amazon EKS add\-on to the latest minor, patch, and build version using the AWS CLI**

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
   v1.7.5-eksbuild.2
   ```

1. Determine which versions of the Amazon VPC CNI Amazon EKS add\-on are available for your cluster's version\. Replace *1\.20* with your cluster's version\.

   ```
   aws eks describe-addon-versions \
       --addon-name vpc-cni \
       --kubernetes-version 1.20 \
       --query "addons[].addonVersions[].[addonVersion, compatibilities[].defaultVersion]" \
       --output text
   ```

   Output

   ```
   v1.10.1-eksbuild.1
   False
   ...
   v1.7.5-eksbuild.2
   True
   ...
   ```

   The version with `True` underneath is the default version deployed with new clusters\. In the previous output, *v1\.10\.1\-eksbuild\.1* is the latest available version\.

1. Update the add\-on to the latest build version of the latest patch version of the latest minor version returned in the previous output\. Replace *my\-cluster* with your cluster name and *v1\.10\.1\-eksbuild\.1* with the version of the add\-on that you want to update to\.

   ```
   aws eks update-addon \
       --cluster-name my-cluster \
       --addon-name vpc-cni \
       --addon-version v1.10.1-eksbuild.1 \
       --resolve-conflicts OVERWRITE
   ```

------

## Removing the Amazon VPC CNI Amazon EKS add\-on<a name="removing-vpc-cni-eks-add-on"></a>

You have two options when removing an Amazon EKS add\-on:
+ **Preserve the add\-on's software on your cluster** – This option removes Amazon EKS management of any settings and the ability for Amazon EKS to notify you of updates and automatically update the Amazon EKS add\-on after you initiate an update, but preserves the add\-on's software on your cluster\. This option makes the add\-on a self\-managed add\-on, rather than an Amazon EKS add\-on\. There is no downtime for the add\-on\.
+ **Removing the add\-on software entirely from your cluster** – You should only remove the Amazon EKS add\-on from your cluster if there are no resources on your cluster are dependent on the functionality that the add\-on provides\. After removing the Amazon EKS add\-on, you can add it again if you want to\.

If the add\-on has an IAM account associated with it, the IAM account is not removed\.

Select the tab with the name of the tool that you want to use to remove the Amazon VPC CNI Amazon EKS add\-on from your 1\.18 or later cluster with\.

------
#### [ eksctl ]

**To remove the Amazon EKS add\-on using `eksctl`**  
Replace *`my-cluster`* with the name of your cluster and then run the following command\. Removing `--preserve` removes the add\-on software from your cluster\.

```
eksctl delete addon --cluster my-cluster --name vpc-cni --preserve
```

------
#### [ AWS Management Console ]

**To remove the Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation, select **Clusters**, and then select the name of the cluster that you want to remove the Amazon VPC CNI Amazon EKS add\-on for\.

1. Choose the **Configuration** tab and then choose the **Add\-ons** tab\.

1. Select the checkbox in the top right of the **`vpc-cni`** box and then choose **Remove**\. Select **Preserve on cluster** if you want Amazon EKS to stop managing settings for the add\-on, but want to retain the add\-on software on your cluster so that you can self\-managed all of the add\-on's settings\. Type **`vpc-cni`** and then select **Remove**\.

------
#### [ AWS CLI ]

**To remove the Amazon EKS add\-on using the AWS CLI**  
Replace *my\-cluster* with the name of your cluster and then run the following command\. Removing `--preserve` removes the add\-on software from your cluster\.

```
aws eks delete-addon --cluster-name my-cluster --addon-name vpc-cni --preserve
```

------

## Updating the Amazon VPC CNI self\-managed add\-on<a name="updating-vpc-cni-add-on"></a>

If you have a 1\.17 or earlier cluster, or a 1\.18 or later cluster that you have not added the Amazon VPC CNI Amazon EKS add\-on to, complete the following steps to update the add\-on\. If you've added the Amazon VPC CNI Amazon EKS add\-on, complete the procedure in [Updating the Amazon VPC CNI Amazon EKS add\-on](#updating-vpc-cni-eks-add-on) instead\.

**To update the self\-managed add\-on to the latest minor and patch version using `kubectl`**

1. Determine the latest available minor version by viewing the `[Releases](https://github.com/aws/amazon-vpc-cni-k8s/releases)` on GitHub\.

1. Use the following command to determine your cluster's Amazon VPC CNI add\-on version:

   ```
   kubectl describe daemonset aws-node --namespace kube-system | grep Image | cut -d "/" -f 2
   ```

   Output:

   ```
   amazon-k8s-cni-init:1.7.5-eksbuild.1
   amazon-k8s-cni:1.7.5-eksbuild.1
   ```

   In this example output, the Amazon VPC CNI add\-on version is *1\.7*, which is earlier than the latest version listed in the `[Releases](https://github.com/aws/amazon-vpc-cni-k8s/releases)` on GitHub\.

1. Use the appropriate command below to update your Amazon VPC CNI add\-on to the latest minor and patch version available\. If necessary, replace *1\.10* with the latest minor version from the `[Releases](https://github.com/aws/amazon-vpc-cni-k8s/releases)` on GitHub\. The manifest installs the latest patch version \(for example, `.1`\) for the minor version that you specify\.
**Important**  
Any changes you've made to the add\-on's default settings on your cluster can be overwritten with default settings when applying the new version of the manifest\. To prevent loss of your custom settings, download the manifest, change the default settings as necessary, and then apply the modified manifest to your cluster\. You should only update one minor version at a time\. For example, if your current minor version is `1.8` and you want to update to `1.10`, you should update to `1.9` first, then update to `1.10`\.
   + China \(Beijing\) \(`cn-north-1`\) or China \(Ningxia\) \(`cn-northwest-1`\)

     ```
     kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.10/config/master/aws-k8s-cni-cn.yaml
     ```
   + AWS GovCloud \(US\-East\) \(`us-gov-east-1`\)

     ```
     kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.10/config/master/aws-k8s-cni-us-gov-east-1.yaml
     ```
   + AWS GovCloud \(US\-West\) \(`us-gov-west-1`\)

     ```
     kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.10/config/master/aws-k8s-cni-us-gov-west-1.yaml
     ```
   + For all other Regions
     + Download the manifest file\.

       ```
       curl -o aws-k8s-cni.yaml https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.10/config/master/aws-k8s-cni.yaml
       ```
     + If necessary, replace `region-code` in the following command with the Region that your cluster is in and then run the modified command to replace the Region code in the file \(currently `us-west-2`\)\.

       ```
       sed -i.bak -e 's/us-west-2/region-code/' aws-k8s-cni.yaml
       ```
     + If necessary, replace `account` in the following command with the account from [Amazon EKS add\-on container image addresses](add-ons-images.md) for the Region that your cluster is in and then run the modified command to replace the account in the file \(currently `602401143452`\)\.

       ```
       sed -i.bak -e 's/602401143452/account/' aws-k8s-cni.yaml
       ```
     + Apply the manifest file to your cluster\.

       ```
       kubectl apply -f aws-k8s-cni.yaml
       ```