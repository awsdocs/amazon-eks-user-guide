# Managing the Amazon VPC CNI add\-on<a name="managing-vpc-cni"></a>

Amazon EKS supports native VPC networking with the Amazon VPC Container Network Interface \(CNI\) plugin for Kubernetes\. Using this plugin allows Kubernetes pods to have the same IP address inside the pod as they do on the VPC network\. For more information, see [Pod networking \(CNI\)](pod-networking.md)\. 

If you created a 1\.18 or later cluster using the AWS Management Console, then Amazon EKS installed the Amazon EKS add\-on for you\. If you created a 1\.18 or later cluster using any method other than the AWS Management Console, then Amazon EKS installed the self\-managed add\-on for you\. You can migrate the self\-managed add\-on to the Amazon EKS add\-on using the procedure in [Adding the Amazon VPC CNI Amazon EKS add\-on](#adding-vpc-cni-eks-add-on)\. If you have a cluster that you've already added the Amazon VPC CNI Amazon EKS add\-on to, you can manage it using the procedures in the [Updating the Amazon VPC CNI Amazon EKS add\-on](#updating-vpc-cni-eks-add-on) and [Removing the Amazon VPC CNI Amazon EKS add\-on](#removing-vpc-cni-eks-add-on) sections\. For more information about Amazon EKS add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\.<a name="manage-vpc-cni-recommended-versions"></a>


**Recommended version of the Amazon VPC CNI add\-on for each cluster version**  

|  | 1\.21 | 1\.20 | 1\.19 | 1\.18 | 1\.17 | 
| --- | --- | --- | --- | --- | --- | 
| Add\-on version | 1\.10\.1\-eksbuild\.1 | 1\.10\.1\-eksbuild\.1 | 1\.10\.1\-eksbuild\.1 | 1\.10\.1\-eksbuild\.1 | 1\.10\.1\-eksbuild\.1 | 

To update your Amazon EKS add\-on version, see [Updating the Amazon VPC CNI Amazon EKS add\-on](#updating-vpc-cni-eks-add-on)\. To update your self\-managed add\-on version using container images in the Amazon EKS Amazon Elastic Container Registry or your own repository, see [Updating the Amazon VPC CNI self\-managed add\-on](#updating-vpc-cni-add-on)\.

**Important**  
The version of the add\-on that was deployed when you created your cluster may be earlier than the recommended version\. If you've updated the self\-managed add\-on using a manifest, then the version doesn't include `-eksbuild.1`\.<a name="manage-vpc-cni-add-on-on-prerequisites"></a>

**Prerequisites**
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\.
+ An existing AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ An IAM role with the [AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor) IAM policy \(if your cluster uses the IPv4 family\) or an [IPv6 policy](cni-iam-role.md#cni-iam-role-create-ipv6-policy) \(if your cluster uses the IPv6 family\) attached to it\. For more information, see [Configuring the Amazon VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.
+ If you are using version 1\.7\.0 or later of the CNI plugin and you use custom pod security policies, see [Delete the default Amazon EKS pod security policy](pod-security-policy.md#psp-delete-default)[Pod security policy](pod-security-policy.md)\.

## Adding the Amazon VPC CNI Amazon EKS add\-on<a name="adding-vpc-cni-eks-add-on"></a>

You can add the Amazon VPC CNI Amazon EKS add\-on to your 1\.18 or later cluster with `eksctl`, the AWS Management Console, or the AWS CLI\.

**Important**  
Before adding the Amazon VPC CNI Amazon EKS add\-on, confirm that you do not self\-manage any settings that Amazon EKS will start managing\. To determine which settings Amazon EKS manages, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------
#### [ eksctl ]

**To add the [recommended version](#manage-vpc-cni-recommended-versions) of the Amazon EKS add\-on using `eksctl`**  
Replace *`my-cluster`* with the name of your cluster and `arn:aws:iam::111122223333:role/AmazonEKSVPCCNIRole` with your existing IAM role \(see [Prerequisites](#manage-vpc-cni-add-on-on-prerequisites)\)\.

```
eksctl create addon \
    --name vpc-cni \
    --version v1.10.1-eksbuild.1 \
    --cluster my-cluster \
    --service-account-role-arn arn:aws:iam::111122223333:role/AmazonEKSVPCCNIRole \
    --force
```

If any of the Amazon EKS add\-on settings conflict with the existing settings for the self\-managed add\-on, then adding the Amazon EKS add\-on fails, and you receive an error message to help you resolve the conflict\.

If you want to add a different version of the add\-on instead, then you can view all versions available for the add\-on and your cluster's version with the following command\. Replace *1\.21* with your cluster's version\.

```
eksctl utils describe-addon-versions --name vpc-cni --kubernetes-version 1.21 | grep AddonVersion:
```

Replace `v1.10.1-eksbuild.1` in the `create addon` command with the version returned in the output that you want to add and then run the `create addon` command\.

------
#### [ AWS Management Console ]

**To add the [recommended version](#manage-vpc-cni-recommended-versions) of the Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select Amazon EKS **Clusters**, and then select the name of the cluster that you want to configure the Amazon VPC CNI Amazon EKS add\-on for\.

1. Choose the **Configuration** tab and then choose the **Add\-ons** tab\.

1. Select **Add new**\.
   + Select **`vpc-cni`** for **Name**\.
   + Select the **Version** you'd like to use\. We recommend the **1\.10\.1\-eksbuild\.1** version, but you can select a different version if necessary\.
   + For **Service account role**, select the name of an IAM role that you've attached the [AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor) IAM policy to \(see [Prerequisites](#manage-vpc-cni-add-on-on-prerequisites)\)\.
   + Select **Override existing configuration for this add\-on on the cluster\.** If any of the Amazon EKS add\-on settings conflict with the existing settings for the self\-managed add\-on, then adding the Amazon EKS add\-on fails, and you receive an error message to help you resolve the conflict\.
   + Select **Add**\.

------
#### [ AWS CLI ]

To add the [recommended version](#manage-vpc-cni-recommended-versions) of the Amazon EKS add\-on using the AWS CLI, replace *my\-cluster* with the name of your cluster, `arn:aws:iam::AWS_ACCOUNT_ID:role/AmazonEKSCNIRole` with the ARN of an IAM role that you've attached the [AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor) IAM policy to \(see [Prerequisites](#manage-vpc-cni-add-on-on-prerequisites)\), and then run the command\.

```
aws eks create-addon \
    --cluster-name my-cluster \
    --addon-name vpc-cni \
    --addon-version v1.10.1-eksbuild.1 \
    --service-account-role-arn arn:aws:iam::AWS_ACCOUNT_ID:role/AmazonEKSVPCCNIRole \
    --resolve-conflicts OVERWRITE
```

If any of the Amazon EKS add\-on settings conflict with the existing settings for the self\-managed add\-on, then adding the Amazon EKS add\-on fails, and you receive an error message to help you resolve the conflict\.

If you want to add a different version of the add\-on instead, then you can view all versions available for the add\-on and your cluster's version with the following command\. Replace *1\.21* with your cluster's version\.

```
aws eks describe-addon-versions \
    --addon-name vpc-cni \
    --kubernetes-version 1.21 \
    --query "addons[].addonVersions[].[addonVersion, compatibilities[].Version]" \
    --output text
```

Replace `v1.10.1-eksbuild.1` in the `create-addon` command with the version returned in the output that you want to add and then run the `create-addon` command\.

------

## Updating the Amazon VPC CNI Amazon EKS add\-on<a name="updating-vpc-cni-eks-add-on"></a>

**Important**  
Before updating the Amazon VPC CNI Amazon EKS add\-on, confirm that you do not self\-manage any settings that Amazon EKS manages\. To determine which settings Amazon EKS manages, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

This procedure is for updating the Amazon VPC CNI Amazon EKS add\-on\. If you haven't added the Amazon VPC CNI Amazon EKS add\-on, complete the procedure in [Updating the Amazon VPC CNI self\-managed add\-on](#updating-vpc-cni-add-on) instead\. Amazon EKS does not automatically update the Amazon VPC CNI add\-on when new versions are released or after you [update your cluster](update-cluster.md) to a new Kubernetes minor version\. To update the Amazon VPC CNI add\-on for an existing cluster, you must initiate the update and then Amazon EKS updates the add\-on for you\.

We recommend that you update one minor version at a time\. For example, if your current minor version is `1.8` and you want to update to `1.10`, you should update to the latest patch version of `1.9` first, then update to the latest patch version of `1.10`\.

You can update the Amazon VPC CNI Amazon EKS add\-on on your 1\.18 or later cluster using `eksctl`, the AWS Management Console, or the AWS CLI\.

------
#### [ eksctl ]

**To update the Amazon EKS add\-on to the [recommended version](#manage-vpc-cni-recommended-versions) using `eksctl`**

1. Check the current version of your `vpc-cni` Amazon EKS add\-on\. Replace *my\-cluster* with your cluster name\.

   ```
   eksctl get addon --name vpc-cni --cluster my-cluster
   ```

   Example output:

   ```
   NAME    VERSION                 STATUS  ISSUES  IAMROLE                                                                                                   UPDATE AVAILABLE
   vpc-cni v1.7.5-eksbuild.2       ACTIVE  0       arn:aws:iam::111122223333:role/AmazonEKSVPCCNIRole      v1.10.1-eksbuild.1
   ```

1. Update the add\-on to the [recommended version](#manage-vpc-cni-recommended-versions)\.

   ```
   eksctl update addon \
       --name vpc-cni \
       --version 1.10.1-eksbuild.1 \
       --cluster my-cluster \
       --force
   ```

   If you want to update to a different version of the add\-on instead, then you can view all versions available for the add\-on and your cluster's version with the following command\. Replace *1\.21* with your cluster's version\.

   ```
   eksctl utils describe-addon-versions --name vpc-cni --kubernetes-version 1.21 | grep AddonVersion:
   ```

   Replace `v1.10.1-eksbuild.1` in the `update addon` command with the version returned in the output that you want to add and then run the `update addon` command\.

------
#### [ AWS Management Console ]

**To update the Amazon EKS add\-on to the [recommended version](#manage-vpc-cni-recommended-versions) using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select Amazon EKS **Clusters**, and then select the name of the cluster that you want to update the Amazon VPC CNI add\-on for\.

1. Choose the **Configuration** tab and then choose the **Add\-ons** tab\.

1. Select the box in the top right of the **vpc\-cni** box and then choose **Edit**\.
   + Select the **Version** of the Amazon EKS add\-on that you want to use\. We recommend the **1\.10\.1\-eksbuild\.1** version, but you can select a different version if necessary\.
   + For **Service account role**, select the name of an IAM role that you've attached the [AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor) IAM policy to \(see [Prerequisites](#manage-vpc-cni-add-on-on-prerequisites)\), if one isn't already selected\.
   + Select **Override existing configuration for this add\-on on the cluster\.**
   + Select **Update**\.

------
#### [ AWS CLI ]

**To update the Amazon EKS add\-on to the [recommended version](#manage-vpc-cni-recommended-versions) using the AWS CLI**

1. Check the current version of your Amazon VPC CNI Amazon EKS add\-on\. Replace *my\-cluster* with your cluster name\.

   ```
   aws eks describe-addon \
       --cluster-name my-cluster \
       --addon-name vpc-cni \
       --query "addon.addonVersion" \
       --output text
   ```

   Example output:

   ```
   v1.7.5-eksbuild.2
   ```

   The version returned for you may be different\.

1. Update the add\-on to the [recommended version](#manage-vpc-cni-recommended-versions)\. Replace *my\-cluster* with your cluster name\.

   ```
   aws eks update-addon \
       --cluster-name my-cluster \
       --addon-name vpc-cni \
       --addon-version v1.10.1-eksbuild.1 \
       --resolve-conflicts OVERWRITE
   ```

   If you want to update to a different version of the add\-on instead, then you can view all versions available for the add\-on and your cluster's version with the following command\. Replace *1\.21* with your cluster's version\.

   ```
   aws eks describe-addon-versions \
       --addon-name vpc-cni \
       --kubernetes-version 1.21 \
       --query "addons[].addonVersions[].[addonVersion, compatibilities[].Version]" \
       --output text
   ```

   Replace `v1.10.1-eksbuild.1` in the `update-addon` command with the version returned in the output that you want to add and then run the `update-addon` command\.

------

## Removing the Amazon VPC CNI Amazon EKS add\-on<a name="removing-vpc-cni-eks-add-on"></a>

You have two options when removing an Amazon EKS add\-on:
+ **Preserve the add\-on's software on your cluster** – This option removes Amazon EKS management of any settings and the ability for Amazon EKS to notify you of updates and automatically update the Amazon EKS add\-on after you initiate an update, but preserves the add\-on's software on your cluster\. This option makes the add\-on a self\-managed add\-on, rather than an Amazon EKS add\-on\. There is no downtime for the add\-on\.
+ **Removing the add\-on software entirely from your cluster** – You should only remove the Amazon EKS add\-on from your cluster if there are no resources on your cluster are dependent on the functionality that the add\-on provides\. After removing the Amazon EKS add\-on, you can add it again if you want to\.

If the add\-on has an IAM account associated with it, the IAM account is not removed\.

You can remove the Amazon VPC CNI Amazon EKS add\-on from your 1\.18 or later cluster with `eksctl`, the AWS Management Console, or the AWS CLI\.

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

1. In the left navigation pane, select Amazon EKS **Clusters**, and then select the name of the cluster that you want to remove the Amazon VPC CNI Amazon EKS add\-on for\.

1. Choose the **Configuration** tab, and then choose the **Add\-ons** tab\.

1. Select the check box in the top right of the **`vpc-cni`** box and then choose **Remove**\. Select **Preserve on cluster** if you want Amazon EKS to stop managing settings for the add\-on, but want to retain the add\-on software on your cluster so that you can self\-managed all of the add\-on's settings\. Type **`vpc-cni`** and then select **Remove**\.

------
#### [ AWS CLI ]

**To remove the Amazon EKS add\-on using the AWS CLI**  
Replace *my\-cluster* with the name of your cluster and then run the following command\. Removing `--preserve` removes the add\-on software from your cluster\.

```
aws eks delete-addon --cluster-name my-cluster --addon-name vpc-cni --preserve
```

------

## Updating the Amazon VPC CNI self\-managed add\-on<a name="updating-vpc-cni-add-on"></a>

If you have a 1\.17 cluster, or a 1\.18 or later cluster that you haven't added the Amazon VPC CNI Amazon EKS add\-on to, complete the following steps to update the add\-on\. If you've added the Amazon VPC CNI Amazon EKS add\-on, complete the procedure in [Updating the Amazon VPC CNI Amazon EKS add\-on](#updating-vpc-cni-eks-add-on) instead\.

**To update the self\-managed add\-on to the [recommended version](#manage-vpc-cni-recommended-versions)**

1. To view the available versions and familiarize yourself with the changes in the version that you want to update to, see the `[releases](https://github.com/aws/amazon-vpc-cni-k8s/releases)` on GitHub\.

1. Use the following command to determine your cluster's current Amazon VPC CNI add\-on version:

   ```
   kubectl describe daemonset aws-node --namespace kube-system | grep Image | cut -d "/" -f 2
   ```

   Example output:

   ```
   amazon-k8s-cni-init:v1.7.5-eksbuild.1
   amazon-k8s-cni:v1.7.5-eksbuild.1
   ```

   Your output might look different than the example output\. In this example output, the Amazon VPC CNI add\-on version is `1.7.5-eksbuild.1`, which is earlier than the [recommended version](#manage-vpc-cni-recommended-versions)\. The version that Amazon EKS originally deployed with your cluster looks similar to the previous output\. If you've already updated the add\-on at least once using a manifest however, your output doesn't include `-eksbuild.1`\.

1. Update the daemonset using [Helm V3](helm.md) or later, or by using a manifest\.

------
#### [ Helm ]

   1. Add the `eks-charts` repository to Helm\.

      ```
      helm repo add eks https://aws.github.io/eks-charts
      ```

   1. Update your local repository to make sure that you have the most recent charts\.

      ```
      helm repo update
      ```

   1. Backup your current settings so that you can determine which settings you need to specify values for in a later step\.

      ```
      kubectl get daemonset aws-node -n kube-system -o yaml > aws-k8s-cni-old.yaml
      ```

   1. If you installed the existing AWS VPC CNI daemonset using Helm, then skip to the next step\.

      Complete one of the following options so that Helm can manage the daemonset's resources:
      + Add the Helm annotations and labels to your existing resources\.

        1. Save the following contents to a file named *`helm-cni.sh`*\. Replace *aws\-vpc\-cni* if you want to use a different release name\.

           ```
           #!/usr/bin/env bash
           
           set -euo pipefail
           
           for kind in daemonSet clusterRole clusterRoleBinding serviceAccount; do
             echo "setting annotations and labels on $kind/aws-node"
             kubectl -n kube-system annotate --overwrite $kind aws-node meta.helm.sh/release-name=aws-vpc-cni
             kubectl -n kube-system annotate --overwrite $kind aws-node meta.helm.sh/release-namespace=kube-system
             kubectl -n kube-system label --overwrite $kind aws-node app.kubernetes.io/managed-by=Helm
           done
           ```

        1. Make the script executable\.

           ```
           chmod +x helm-cni.sh
           ```

        1. Run the script

           ```
           ./helm-cni.sh
           ```
      + Remove the existing daemonset's resources\.
**Important**  
Your cluster will experience downtime between completing this step and the next step\.

        ```
        kubectl delete serviceaccount aws-node -n kube-system
        kubectl delete customresourcedefinition eniconfigs.crd.k8s.amazonaws.com
        kubectl delete clusterrole aws-node
        kubectl delete clusterrolebinding aws-node
        kubectl delete daemonset aws-node -n kube-system
        ```

   1. Install the chart using one of the following options\. Before running the installation, review the backup you made of the settings for your daemonset in a previous step and then review the [configuration settings](https://github.com/aws/amazon-vpc-cni-k8s/tree/master/charts/aws-vpc-cni#configuration) to determine if you need to set any of them\. We recommend using the version in the following commands, but if necessary, you can replace it with any [release version](https://github.com/aws/amazon-vpc-cni-k8s/releases)\.
**Important**  
You should only update one minor version at a time\. For example, if your current minor version is `1.8` and you want to update to `1.10`, you should update to `1.9` first, then update to `1.10` by changing the version number in the one of the following commands\.
The latest and recommended versions work with all Amazon EKS supported Kubernetes versions\.

      If you have an existing IAM role to use with the daemonset, then add the following line at the end of the install options that follow\. If you don't have an IAM role associated to the `aws-node` Kubernetes service account, then we recommend creating one\. Replace *111122223333* with your account ID and **AmazonEKSVPCCNIRole** with the name of your role\. To create a role, see [Configuring the Amazon VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.

      ```
      --set serviceAccount.annotations."eks\.amazonaws\.com/role-arn"=arn:aws:iam::111122223333:role/AmazonEKSVPCCNIRole
      ```

      If you added the Helm annotations and labels in the previous step, then add the following settings to any of the following options\.

      ```
      --set originalMatchLabels=true
      --set crd.create=false
      ```
      + If your nodes have access to the Amazon EKS Amazon ECR repositories and are in the `us-west-2` AWS Region, then install the chart with the release name `aws-vpc-cni` and default configuration\.

        ```
        helm upgrade -i aws-vpc-cni eks/aws-vpc-cni \
        --namespace kube-system \
        --set image.tag=v1.10.1 \
        --set init.image.tag=v1.10.1
        ```
      + If your nodes have access to the Amazon EKS Amazon ECR repositories and are in an AWS Region other than `us-west-2`, then install the chart with the release name `aws-vpc-cni`\. Replace *eks\-ecr\-account* and *region\-code* with values from [Amazon container image registries](add-ons-images.md) for the AWS Region that your cluster is in\.

        ```
        helm upgrade -i aws-vpc-cni eks/aws-vpc-cni \
        --namespace kube-system \
        --set image.account=eks-ecr-account \
        --set image.region=region-code \
        --set image.tag=v1.10.1 \
        --set init.image.account=eks-ecr-account
        --set init.image.region=region-code \
        --set init.image.tag=v1.10.1 \
        ```
      + If your nodes don't have access to the Amazon EKS Amazon ECR repositories 

        1. Pull the following container images and push them to a repository that your nodes have access to\. For more information on how to pull, tag, and push an image to your own repository, see [Copy a container image from one repository to another repository](copy-image-to-repository.md)\. We recommend using the version in the following commands, but if necessary, you can replace it with any [release version](https://github.com/aws/amazon-vpc-cni-k8s/releases)\. Replace *eks\-ecr\-account* and *region\-code* with values from [Amazon container image registries](add-ons-images.md) for the AWS Region that your cluster is in\.

           ```
           eks-ecr-account.dkr.ecr.region-code.amazonaws.com/amazon-k8s-cni-init:v1.10.1
           eks-ecr-account.dkr.ecr.region-code.amazonaws.com/amazon-k8s-cni:v1.10.1
           ```

        1. Install the chart with the release name `aws-vpc-cni` and default configuration\. Before running the installation, review the backup you made of the settings for your daemonset in a previous step and then review the [configuration settings](https://github.com/aws/amazon-vpc-cni-k8s/tree/master/charts/aws-vpc-cni#configuration) to determine if you need to set any of them\. Replace *registry/repo:tag* with your registry, repository, and tag\.

           ```
           helm upgrade -i aws-vpc-cni eks/aws-vpc-cni \
               --namespace kube-system \
               --set image.override=registry/repo:tag \
               --set init.image.override=registry/repo:tag
           ```

------
#### [ Manifest ]

   1. If you've changed any default settings for your current VPC CNI daemonset or you need to pull the container image from your own repository to update it, then skip to the next step\.

      Update your Amazon VPC CNI add\-on\. We recommend using the version in the following commands, but if necessary, you can replace it with any [release version](https://github.com/aws/amazon-vpc-cni-k8s/releases)\.
**Important**  
You should only update one minor version at a time\. For example, if your current minor version is `1.8` and you want to update to `1.10`, you should update to `1.9` first, then update to `1.10` by changing the version number in the one of the following commands\.
The latest and recommended versions work with all Amazon EKS supported Kubernetes versions\.

      Complete the instruction for the AWS Region that your cluster is in to update your Amazon VPC CNI add\-on to the [recommended version](#manage-vpc-cni-recommended-versions)\.
      + If your cluster is in the AWS GovCloud \(US\-East\) \(`us-gov-east-1`\) AWS Region then run the following command\.

        ```
        kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/v1.10.1/config/master/aws-k8s-cni-us-gov-east-1.yaml
        ```
      + If your cluster is in the AWS GovCloud \(US\-West\) \(`us-gov-west-1`\) AWS Region then run the following command\.

        ```
        kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/v1.10.1/config/master/aws-k8s-cni-us-gov-west-1.yaml
        ```
      + If your cluster is in the US West \(Oregon\) \(`us-west-2`\) AWS Region then run the following command\.

        ```
        kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/v1.10.1/config/master/aws-k8s-cni.yaml
        ```
      + If your cluster is in any other AWS Region, then complete the following steps\.

        1. Download the manifest file\.

           ```
           curl -o aws-k8s-cni.yaml https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/v1.10.1/config/master/aws-k8s-cni.yaml
           ```

        1. Modify the file:

           1. Replace `region-code` in the following command with the AWS Region that your cluster is in and then run the modified command to replace `us-west-2` in the file\.

              ```
              sed -i.bak -e 's|us-west-2|region-code|' aws-k8s-cni.yaml
              ```

           1. Replace `account` in the following command with the account from [Amazon container image registries](add-ons-images.md) for the AWS Region that your cluster is in and then run the modified command to replace `602401143452` in the file\.

              ```
              sed -i.bak -e 's|602401143452|account|' aws-k8s-cni.yaml
              ```

        1. Apply the manifest file to your cluster\.

           ```
           kubectl apply -f aws-k8s-cni.yaml
           ```

   1. If you've changed any default settings for your current VPC CNI daemonset or need to pull the container image from your own repository when updating it, then complete the following steps to update your Amazon VPC CNI add\-on to the [recommended version](#manage-vpc-cni-recommended-versions)\.
**Important**  
You should only update one minor version at a time\. For example, if your current minor version is `1.8` and you want to update to `1.10`, you should update to `1.9` first, then update to `1.10` by changing the version number in the following commands\.
The latest and recommended versions work with all Amazon EKS supported Kubernetes versions\.

      1. If your nodes have access to the Amazon EKS Amazon ECR image repositories, then skip to the next sub\-step\.

         Pull the following container images and push them to a repository that your nodes have access to\. For more information on how to pull, tag, and push an image to your own repository, see [Copy a container image from one repository to another repository](copy-image-to-repository.md)\. Replace *account* and *region\-code* with values from [Amazon container image registries](add-ons-images.md) for the AWS Region that your cluster is in\. We recommend using the version in the following commands, but if necessary, you can replace it with any [release version](https://github.com/aws/amazon-vpc-cni-k8s/releases)\.

         ```
         account.dkr.ecr.region-code.amazonaws.com/amazon-k8s-cni-init:v1.10.1
         account.dkr.ecr.region-code.amazonaws.com/amazon-k8s-cni:v1.10.1
         ```

      1. Backup your current settings so that you can compare your settings to the default settings in the new manifest\.

         ```
         kubectl get daemonset aws-node -n kube-system -o yaml > aws-k8s-cni-old.yaml
         ```

      1. Download the manifest for the Amazon VPC CNI add\-on for your AWS Region\. We recommend using the version in the following commands, but if necessary, you can replace it with any [release version](https://github.com/aws/amazon-vpc-cni-k8s/releases)\.
         + AWS GovCloud \(US\-East\) \(`us-gov-east-1`\)

           ```
           curl -o aws-k8s-cni-us-gov-east-1.yaml https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/v1.10.1/config/master/aws-k8s-cni-us-gov-east-1.yaml
           ```
         + AWS GovCloud \(US\-West\) \(`us-gov-west-1`\)

           ```
           curl -o aws-k8s-cni-us-gov-west-1.yaml https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/v1.10.1/config/master/aws-k8s-cni-us-gov-west-1.yaml
           ```
         + Any other AWS Region, or if you copied the images to your own repository in a previous step

           ```
           curl -o aws-k8s-cni.yaml https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/v1.10.1/config/master/aws-k8s-cni.yaml
           ```

      1. Modify the file with one of the following options:
         + If you didn't copy the container images to your own repository in a previous step, then run the following commands:

           1. Replace `region-code` in the following command with the AWS Region that your cluster is in and then run the modified command to replace `us-west-2` in the file\.

              ```
              sed -i.bak -e 's|us-west-2|region-code|' aws-k8s-cni.yaml
              ```

           1. Replace `account` in the following command with the account from [Amazon container image registries](add-ons-images.md) for the AWS Region that your cluster is in and then run the modified command to replace `602401143452` in the file\.

              ```
              sed -i.bak -e 's|602401143452|account|' aws-k8s-cni.yaml
              ```
         + If you copied the container images to your own repository in a previous step, then make the following replacements and run the following commands:

           1. Replace *your\-registry* in the following command with your registry and then run the modified command to replace `602401143452.dkr.ecr.us-west-2.amazonaws.com` in the file\.

              ```
              sed -i.bak -e 's|602401143452.dkr.ecr.us-west-2.amazonaws.com|your-registry|' aws-k8s-cni.yaml
              ```

           1. Replace *your\-repository* and *tag* in the following command with your repository and tag and then run the modified command to replace `amazon-k8s-cni-init:v1.10.1` in the file\. Replace *`1.10.1`* with the version of the manifest that you downloaded\. 

              ```
              sed -i.bak -e 's|amazon-k8s-cni-init:v1.10.1|your-repository:tag|' aws-k8s-cni.yaml
              ```

           1. Replace *your\-repository* and *tag* in the following command with your repository and tag and then run the modified command to replace `amazon-k8s-cni:v1.10.1` in the file\. Replace *`1.10.1`* with the version of the manifest that you downloaded\.

              ```
              sed -i.bak -e 's|amazon-k8s-cni:v1.10.1|your-repository:tag|' aws-k8s-cni.yaml
              ```

      1. If you've changed any default settings for your current VPC CNI daemonset then compare the settings in the new manifest to the backup file you made in a previous step and make changes to settings in the new manifest so that it matches the settings in your backup file\.

      1. Apply the manifest file to your cluster\.

         ```
         kubectl apply -f aws-k8s-cni.yaml
         ```

------

1. View the status of the daemonset\.

   ```
   kubectl get daemonset aws-node -n kube-system
   ```

   Example output:

   ```
   NAME       DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
   aws-node   2         2         2       2            2           <none>          4h39m
   ```

   Once the numbers in the `READY`, `UP-TO-DATE`, and `AVAILABLE` columns are the same, then your update is complete\. Your numbers may be different than those in the previous output\.

1. View the daemonset to confirm the changes that you made\.

   ```
   kubectl get daemonset aws-node -n kube-system -o yaml
   ```
