# Updating the Amazon VPC CNI plugin for Kubernetes Amazon EKS add\-on<a name="vpc-add-on-update"></a>

Update the Amazon EKS type of the add\-on\. If you haven't added the Amazon EKS type of the add\-on to your cluster, either [add it](vpc-add-on-create.md) or see [Updating the self\-managed Amazon EKS add\-on](vpc-add-on-self-managed-update.md)\.

1. See which version of the add\-on is installed on your cluster\. Replace `my-cluster` with your cluster name\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name vpc-cni --query "addon.addonVersion" --output text
   ```

   An example output is as follows\.

   ```
   v1.16.4-eksbuild.2
   ```

   If the version returned is the same as the version for your cluster's Kubernetes version in the [latest version table](managing-vpc-cni.md#vpc-cni-latest-available-version), then you already have the latest version installed on your cluster and don't need to complete the rest of this procedure\. If you receive an error, instead of a version number in your output, then you don't have the Amazon EKS type of the add\-on installed on your cluster\. You need to [create the add\-on](vpc-add-on-create.md) before you can update it with this procedure\.

1. Save the configuration of your currently installed add\-on\.

   ```
   kubectl get daemonset aws-node -n kube-system -o yaml > aws-k8s-cni-old.yaml
   ```

1. Update your add\-on using the AWS CLI\. If you want to use the AWS Management Console or `eksctl` to update the add\-on, see [Updating an Amazon EKS add\-on](updating-an-add-on.md)\. Copy the command that follows to your device\. Make the following modifications to the command, as needed, and then run the modified command\.
   + Replace `my-cluster` with the name of your cluster\.
   + Replace *`v1.18.3-eksbuild.2`* with the latest version listed in the [latest version table](managing-vpc-cni.md#vpc-cni-latest-available-version) for your cluster version\.
   + Replace *111122223333* with your account ID and *AmazonEKSVPCCNIRole* with the name of an [existing IAM role](cni-iam-role.md#cni-iam-role-create-role) that you've created\. Specifying a role requires that you have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one for your cluster, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\. 
   + The **\-\-resolve\-conflicts** *PRESERVE* option preserves existing configuration values for the add\-on\. If you've set custom values for add\-on settings, and you don't use this option, Amazon EKS overwrites your values with its default values\. If you use this option, then we recommend testing any field and value changes on a non\-production cluster before updating the add\-on on your production cluster\. If you change this value to `OVERWRITE`, all settings are changed to Amazon EKS default values\. If you've set custom values for any settings, they might be overwritten with Amazon EKS default values\. If you change this value to `none`, Amazon EKS doesn't change the value of any settings, but the update might fail\. If the update fails, you receive an error message to help you resolve the conflict\. 
   + If you're not updating a configuration setting, remove **\-\-configuration\-values '\{*"env":\{"AWS\_VPC\_K8S\_CNI\_EXTERNALSNAT":"true"\}*\}'** from the command\. If you're updating a configuration setting, replace *"env":\{"AWS\_VPC\_K8S\_CNI\_EXTERNALSNAT":"true"\}* with the setting that you want to set\. In this example, the `AWS_VPC_K8S_CNI_EXTERNALSNAT` environment variable is set to `true`\. The value that you specify must be valid for the configuration schema\. If you don't know the configuration schema, run **aws eks describe\-addon\-configuration \-\-addon\-name vpc\-cni \-\-addon\-version *v1\.18\.3\-eksbuild\.2***, replacing *v1\.18\.3\-eksbuild\.2* with the version number of the add\-on that you want to see the configuration for\. The schema is returned in the output\. If you have any existing custom configuration, want to remove it all, and set the values for all settings back to Amazon EKS defaults, remove **"env":\{"AWS\_VPC\_K8S\_CNI\_EXTERNALSNAT":"true"\}** from the command, so that you have empty `{}`\. For an explanation of each setting, see [CNI Configuration Variables](https://github.com/aws/amazon-vpc-cni-k8s#cni-configuration-variables) on GitHub\.

     ```
     aws eks update-addon --cluster-name my-cluster --addon-name vpc-cni --addon-version v1.18.3-eksbuild.2 \
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
           "addonVersion": "v1.18.3-eksbuild.2",
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