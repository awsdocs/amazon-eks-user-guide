# Working with the Amazon VPC CNI plugin for Kubernetes Amazon EKS add\-on<a name="managing-vpc-cni"></a>

The Amazon VPC CNI plugin for Kubernetes add\-on is deployed on each Amazon EC2 node in your Amazon EKS cluster\. The add\-on creates [elastic network interfaces](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html) and attaches them to your Amazon EC2 nodes\. The add\-on also assigns a private `IPv4` or `IPv6` address from your VPC to each Pod and service\.

A version of the add\-on is deployed with each Fargate node in your cluster, but you don't update it on Fargate nodes\. [Other compatible CNI plugins](alternate-cni-plugins.md) are available for use on Amazon EKS clusters, but this is the only CNI plugin supported by Amazon EKS\.

The following table lists the latest available version of the Amazon EKS add\-on type for each Kubernetes version\.<a name="vpc-cni-latest-available-version"></a>


| Kubernetes version | `1.29` | `1.28` | `1.27` | `1.26` | `1.25` | `1.24` | `1.23` | 
| --- | --- | --- | --- | --- | --- | --- | --- | 
| Amazon EKS type of VPC CNI version | v1\.18\.0\-eksbuild\.1 | v1\.18\.0\-eksbuild\.1 | v1\.18\.0\-eksbuild\.1 | v1\.18\.0\-eksbuild\.1 | v1\.18\.0\-eksbuild\.1 | v1\.18\.0\-eksbuild\.1 | v1\.18\.0\-eksbuild\.1 | 

**Important**  
If you're self\-managing this add\-on, the versions in the table might not be the same as the available self\-managed versions\. For more information about updating the self\-managed type of this add\-on, see [Updating the self\-managed add\-on](#vpc-add-on-self-managed-update)\.<a name="manage-vpc-cni-add-on-on-prerequisites"></a>

**Prerequisites**
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\.
+ An existing AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ An IAM role with the [AmazonEKS\_CNI\_Policy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKS_CNI_Policy.html) IAM policy \(if your cluster uses the `IPv4` family\) or an [IPv6 policy](cni-iam-role.md#cni-iam-role-create-ipv6-policy) \(if your cluster uses the `IPv6` family\) attached to it\. For more information, see [Configuring the Amazon VPC CNI plugin for Kubernetes to use IAM roles for service accounts \(IRSA\)](cni-iam-role.md)\.
+ If you're using version `1.7.0` or later of the Amazon VPC CNI plugin for Kubernetes and you use custom Pod security policies, see [Delete the default Amazon EKS Pod security policy](pod-security-policy.md#psp-delete-default)[Pod security policy](pod-security-policy.md)\.
+ 
**Important**  
Amazon VPC CNI plugin for Kubernetes versions `v1.16.0` to `v1.16.1` removed compatibility with Kubernetes versions `1.23` and earlier\. VPC CNI version `v1.16.2` restores compatibility with Kubernetes versions `1.23` and earlier and CNI spec `v0.4.0`\.

  Amazon VPC CNI plugin for Kubernetes versions `v1.16.0` to `v1.16.1` implement CNI specification version `v1.0.0`\. CNI spec `v1.0.0` is supported on EKS clusters that run the Kubernetes versions `v1.24` or later\. VPC CNI version `v1.16.0` to `v1.16.1` and CNI spec `v1.0.0` aren't supported on Kubernetes version `v1.23` or earlier\.  For more information about `v1.0.0` of the CNI spec, see [Container Network Interface \(CNI\) Specification](https://github.com/containernetworking/cni/blob/spec-v1.0.0/SPEC.md) on 

**Considerations**
+ Versions are specified as `major-version.minor-version.patch-version-eksbuild.build-number`\.
+ 

**Check version compatibility for each feature**  
Some features of each release of the Amazon VPC CNI plugin for Kubernetes require certian Kubernetes versions\. When using different Amazon EKS features, if a specific version of the add\-on is required, then it's noted in the feature documentation\. Unless you have a specific reason for running an earlier version, we recommend running the latest version\.

## Creating the Amazon EKS add\-on<a name="vpc-add-on-create"></a>

Create the Amazon EKS type of the add\-on\.

1. See which version of the add\-on is installed on your cluster\.

   ```
   kubectl describe daemonset aws-node --namespace kube-system | grep amazon-k8s-cni: | cut -d : -f 3
   ```

   An example output is as follows\.

   ```
   v1.12.6-eksbuild.2
   ```

1. See which type of the add\-on is installed on your cluster\. Depending on the tool that you created your cluster with, you might not currently have the Amazon EKS add\-on type installed on your cluster\. Replace *my\-cluster* with the name of your cluster\.

   ```
   $ aws eks describe-addon --cluster-name my-cluster --addon-name vpc-cni --query addon.addonVersion --output text
   ```

   If a version number is returned, you have the Amazon EKS type of the add\-on installed on your cluster and don't need to complete the remaining steps in this procedure\. If an error is returned, you don't have the Amazon EKS type of the add\-on installed on your cluster\. Complete the remaining steps of this procedure to install it\.

1. Save the configuration of your currently installed add\-on\.

   ```
   kubectl get daemonset aws-node -n kube-system -o yaml > aws-k8s-cni-old.yaml
   ```

1. Create the add\-on using the AWS CLI\. If you want to use the AWS Management Console or `eksctl` to create the add\-on, see [Creating an add\-on](managing-add-ons.md#creating-an-add-on) and specify `vpc-cni` for the add\-on name\. Copy the command that follows to your device\. Make the following modifications to the command, as needed, and then run the modified command\.
   + Replace `my-cluster` with the name of your cluster\.
   + Replace *`v1.18.0-eksbuild.1`* with the latest version listed in the [latest version table](#vpc-cni-latest-available-version) for your cluster version\.
   + Replace *111122223333* with your account ID and *AmazonEKSVPCCNIRole* with the name of an [existing IAM role](cni-iam-role.md#cni-iam-role-create-role) that you've created\. Specifying a role requires that you have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one for your cluster, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\. 

   ```
   aws eks create-addon --cluster-name my-cluster --addon-name vpc-cni --addon-version v1.18.0-eksbuild.1 \
       --service-account-role-arn arn:aws:iam::111122223333:role/AmazonEKSVPCCNIRole
   ```

   If you've applied custom settings to your current add\-on that conflict with the default settings of the Amazon EKS add\-on, creation might fail\. If creation fails, you receive an error that can help you resolve the issue\. Alternatively, you can add **\-\-resolve\-conflicts OVERWRITE** to the previous command\. This allows the add\-on to overwrite any existing custom settings\. Once you've created the add\-on, you can update it with your custom settings\.

1. Confirm that the latest version of the add\-on for your cluster's Kubernetes version was added to your cluster\. Replace `my-cluster` with the name of your cluster\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name vpc-cni --query addon.addonVersion --output text
   ```

   It might take several seconds for add\-on creation to complete\.

   An example output is as follows\.

   ```
   v1.18.0-eksbuild.1
   ```

1. If you made custom settings to your original add\-on, before you created the Amazon EKS add\-on, use the configuration that you saved in a previous step to [update](#vpc-add-on-update) the Amazon EKS add\-on with your custom settings\.

1. \(Optional\) Install the `cni-metrics-helper` to your cluster\. It scrapes elastic network interface and IP address information, aggregates it at a cluster level, and publishes the metrics to Amazon CloudWatch\. For more information, see [cni\-metrics\-helper](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/cmd/cni-metrics-helper/README.md) on GitHub\.

## Updating the Amazon EKS add\-on<a name="vpc-add-on-update"></a>

Update the Amazon EKS type of the add\-on\. If you haven't added the Amazon EKS type of the add\-on to your cluster, either [add it](#vpc-add-on-create) or see [Updating the self\-managed add\-on](#vpc-add-on-self-managed-update), instead of completing this procedure\.

1. See which version of the add\-on is installed on your cluster\. Replace `my-cluster` with your cluster name\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name vpc-cni --query "addon.addonVersion" --output text
   ```

   An example output is as follows\.

   ```
   v1.12.6-eksbuild.2
   ```

   If the version returned is the same as the version for your cluster's Kubernetes version in the [latest version table](#vpc-cni-latest-available-version), then you already have the latest version installed on your cluster and don't need to complete the rest of this procedure\. If you receive an error, instead of a version number in your output, then you don't have the Amazon EKS type of the add\-on installed on your cluster\. You need to [create the add\-on](#vpc-add-on-create) before you can update it with this procedure\.

1. Save the configuration of your currently installed add\-on\.

   ```
   kubectl get daemonset aws-node -n kube-system -o yaml > aws-k8s-cni-old.yaml
   ```

1. Update your add\-on using the AWS CLI\. If you want to use the AWS Management Console or `eksctl` to update the add\-on, see [Updating an add\-on](managing-add-ons.md#updating-an-add-on)\. Copy the command that follows to your device\. Make the following modifications to the command, as needed, and then run the modified command\.
   + Replace `my-cluster` with the name of your cluster\.
   + Replace *`v1.18.0-eksbuild.1`* with the latest version listed in the [latest version table](#vpc-cni-latest-available-version) for your cluster version\.
   + Replace *111122223333* with your account ID and *AmazonEKSVPCCNIRole* with the name of an [existing IAM role](cni-iam-role.md#cni-iam-role-create-role) that you've created\. Specifying a role requires that you have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one for your cluster, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\. 
   + The **\-\-resolve\-conflicts** *PRESERVE* option preserves existing configuration values for the add\-on\. If you've set custom values for add\-on settings, and you don't use this option, Amazon EKS overwrites your values with its default values\. If you use this option, then we recommend testing any field and value changes on a non\-production cluster before updating the add\-on on your production cluster\. If you change this value to `OVERWRITE`, all settings are changed to Amazon EKS default values\. If you've set custom values for any settings, they might be overwritten with Amazon EKS default values\. If you change this value to `none`, Amazon EKS doesn't change the value of any settings, but the update might fail\. If the update fails, you receive an error message to help you resolve the conflict\. 
   + If you're not updating a configuration setting, remove **\-\-configuration\-values '\{*"env":\{"AWS\_VPC\_K8S\_CNI\_EXTERNALSNAT":"true"\}*\}'** from the command\. If you're updating a configuration setting, replace *"env":\{"AWS\_VPC\_K8S\_CNI\_EXTERNALSNAT":"true"\}* with the setting that you want to set\. In this example, the `AWS_VPC_K8S_CNI_EXTERNALSNAT` environment variable is set to `true`\. The value that you specify must be valid for the configuration schema\. If you don't know the configuration schema, run **aws eks describe\-addon\-configuration \-\-addon\-name vpc\-cni \-\-addon\-version *v1\.18\.0\-eksbuild\.1***, replacing *v1\.18\.0\-eksbuild\.1* with the version number of the add\-on that you want to see the configuration for\. The schema is returned in the output\. If you have any existing custom configuration, want to remove it all, and set the values for all settings back to Amazon EKS defaults, remove **"env":\{"AWS\_VPC\_K8S\_CNI\_EXTERNALSNAT":"true"\}** from the command, so that you have empty `{}`\. For an explanation of each setting, see [CNI Configuration Variables](https://github.com/aws/amazon-vpc-cni-k8s#cni-configuration-variables) on GitHub\.

     ```
     aws eks update-addon --cluster-name my-cluster --addon-name vpc-cni --addon-version v1.18.0-eksbuild.1 \
         --service-account-role-arn arn:aws:iam::111122223333:role/AmazonEKSVPCCNIRole \
         --resolve-conflicts PRESERVE --configuration-values '{"env":{"AWS_VPC_K8S_CNI_EXTERNALSNAT":"true"}}'
     ```

     It might take several seconds for the update to complete\.

1. Confirm that the add\-on version was updated\. Replace `my-cluster` with the name of your cluster\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name vpc-cni
   ```

   It might take several seconds for the update to complete\.

   An example output is as follows\.

   ```
   {
       "addon": {
           "addonName": "vpc-cni",
           "clusterName": "my-cluster",
           "status": "ACTIVE",
           "addonVersion": "v1.18.0-eksbuild.1",
           "health": {
               "issues": []
           },
           "addonArn": "arn:aws:eks:region:111122223333:addon/my-cluster/vpc-cni/74c33d2f-b4dc-8718-56e7-9fdfa65d14a9",
           "createdAt": "2023-04-12T18:25:19.319000+00:00",
           "modifiedAt": "2023-04-12T18:40:28.683000+00:00",
           "serviceAccountRoleArn": "arn:aws:iam::111122223333:role/AmazonEKSVPCCNIRole",
           "tags": {},
           "configurationValues": "{\"env\":{\"AWS_VPC_K8S_CNI_EXTERNALSNAT\":\"true\"}}"
       }
   }
   ```

## Updating the self\-managed add\-on<a name="vpc-add-on-self-managed-update"></a>

**Important**  
We recommend adding the Amazon EKS type of the add\-on to your cluster instead of using the self\-managed type of the add\-on\. If you're not familiar with the difference between the types, see [Amazon EKS add\-ons](eks-add-ons.md)\. For more information about adding an Amazon EKS add\-on to your cluster, see [Creating an add\-on](managing-add-ons.md#creating-an-add-on)\. If you're unable to use the Amazon EKS add\-on, we encourage you to submit an issue about why you can't to the [Containers roadmap GitHub repository](https://github.com/aws/containers-roadmap/issues)\.

1. Confirm that you don't have the Amazon EKS type of the add\-on installed on your cluster\. Replace *my\-cluster* with the name of your cluster\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name vpc-cni --query addon.addonVersion --output text
   ```

   If an error message is returned, you don't have the Amazon EKS type of the add\-on installed on your cluster\. To self\-manage the add\-on, complete the remaining steps in this procedure to update the add\-on\. If a version number is returned, you have the Amazon EKS type of the add\-on installed on your cluster\. To update it, use the procedure in [Updating an add\-on](managing-add-ons.md#updating-an-add-on), rather than using this procedure\. If you're not familiar with the differences between the add\-on types, see [Amazon EKS add\-ons](eks-add-ons.md)\.

1. See which version of the container image is currently installed on your cluster\.

   ```
   kubectl describe daemonset aws-node --namespace kube-system | grep amazon-k8s-cni: | cut -d : -f 3
   ```

   An example output is as follows\.

   ```
   v1.12.6-eksbuild.2
   ```

   Your output might not include the build number\.

1. Backup your current settings so you can configure the same settings once you've updated your version\.

   ```
   kubectl get daemonset aws-node -n kube-system -o yaml > aws-k8s-cni-old.yaml
   ```

1. To review the available versions and familiarize yourself with the changes in the version that you want to update to, see `[releases](https://github.com/aws/amazon-vpc-cni-k8s/releases)` on GitHub\. Note that we recommend updating to the same `major`\.`minor`\.`patch` version listed in the [latest available versions table](#vpc-cni-latest-available-version), even if later versions are available on GitHub\.\. The build versions listed in the table aren't specified in the self\-managed versions listed on GitHub\. Update your version by completing the tasks in one of the following options:
   + If you don't have any custom settings for the add\-on, then run the command under the `To apply this release:` heading on GitHub for the [release](https://github.com/aws/amazon-vpc-cni-k8s/releases) that you're updating to\.
   + If you have custom settings, download the manifest file with the following command\. Change *https://raw\.githubusercontent\.com/aws/amazon\-vpc\-cni\-k8s/v1\.18\.0/config/master/aws\-k8s\-cni\.yaml* to the URL for the release on GitHub that you're updating to\.

     ```
     curl -O https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/v1.18.0/config/master/aws-k8s-cni.yaml
     ```

     If necessary, modify the manifest with the custom settings from the backup you made in a previous step and then apply the modified manifest to your cluster\. If your nodes don't have access to the private Amazon EKS Amazon ECR repositories that the images are pulled from \(see the lines that start with `image:` in the manifest\), then you'll have to download the images, copy them to your own repository, and modify the manifest to pull the images from your repository\. For more information, see [Copy a container image from one repository to another repository](copy-image-to-repository.md)\.

     ```
     kubectl apply -f aws-k8s-cni.yaml
     ```

1. Confirm that the new version is now installed on your cluster\.

   ```
   kubectl describe daemonset aws-node --namespace kube-system | grep amazon-k8s-cni: | cut -d : -f 3
   ```

   An example output is as follows\.

   ```
   v1.18.0
   ```

1. \(Optional\) Install the `cni-metrics-helper` to your cluster\. It scrapes elastic network interface and IP address information, aggregates it at a cluster level, and publishes the metrics to Amazon CloudWatch\. For more information, see [cni\-metrics\-helper](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/cmd/cni-metrics-helper/README.md) on GitHub\.