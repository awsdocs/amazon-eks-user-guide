# Update the CoreDNS Amazon EKS add\-on<a name="coredns-add-on-update"></a>

Update the Amazon EKS type of the add\-on\. If you haven't added the Amazon EKS add\-on to your cluster, either [add it](coredns-add-on-create.md) or see [Update the CoreDNS Amazon EKS self\-managed add\-on](coredns-add-on-self-managed-update.md)\.

Before you begin, review the upgrade considerations\. For more information, see [Important CoreDNS upgrade considerations](managing-coredns.md#coredns-upgrade)\.

1. See which version of the add\-on is installed on your cluster\. Replace `my-cluster` with your cluster name\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name coredns --query "addon.addonVersion" --output text
   ```

   An example output is as follows\.

   ```
   v1.10.1-eksbuild.11
   ```

   If the version returned is the same as the version for your cluster's Kubernetes version in the [latest version table](managing-coredns.md#coredns-versions), then you already have the latest version installed on your cluster and don't need to complete the rest of this procedure\. If you receive an error, instead of a version number in your output, then you don't have the Amazon EKS type of the add\-on installed on your cluster\. You need to [create the add\-on](coredns-add-on-create.md) before you can update it with this procedure\.

1. Save the configuration of your currently installed add\-on\.

   ```
   kubectl get deployment coredns -n kube-system -o yaml > aws-k8s-coredns-old.yaml
   ```

1. Update your add\-on using the AWS CLI\. If you want to use the AWS Management Console or `eksctl` to update the add\-on, see [Updating an Amazon EKS add\-on](updating-an-add-on.md)\. Copy the command that follows to your device\. Make the following modifications to the command, as needed, and then run the modified command\.
   + Replace `my-cluster` with the name of your cluster\.
   + Replace *v1\.11\.1\-eksbuild\.9* with the latest version listed in the [latest version table](managing-coredns.md#coredns-versions) for your cluster version\.
   + The **\-\-resolve\-conflicts** *PRESERVE* option preserves existing configuration values for the add\-on\. If you've set custom values for add\-on settings, and you don't use this option, Amazon EKS overwrites your values with its default values\. If you use this option, then we recommend testing any field and value changes on a non\-production cluster before updating the add\-on on your production cluster\. If you change this value to `OVERWRITE`, all settings are changed to Amazon EKS default values\. If you've set custom values for any settings, they might be overwritten with Amazon EKS default values\. If you change this value to `none`, Amazon EKS doesn't change the value of any settings, but the update might fail\. If the update fails, you receive an error message to help you resolve the conflict\. 
   + If you're not updating a configuration setting, remove **\-\-configuration\-values '\{*"replicaCount":3*\}'** from the command\. If you're updating a configuration setting, replace *"replicaCount":3* with the setting that you want to set\. In this example, the number of replicas of CoreDNS is set to `3`\. The value that you specify must be valid for the configuration schema\. If you don't know the configuration schema, run **aws eks describe\-addon\-configuration \-\-addon\-name coredns \-\-addon\-version *v1\.11\.1\-eksbuild\.9***, replacing *v1\.11\.1\-eksbuild\.9* with the version number of the add\-on that you want to see the configuration for\. The schema is returned in the output\. If you have any existing custom configuration, want to remove it all, and set the values for all settings back to Amazon EKS defaults, remove *"replicaCount":3* from the command, so that you have empty `{}`\. For more information about CoreDNS settings, see [Customizing DNS Service](https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/) in the Kubernetes documentation\.

     ```
     aws eks update-addon --cluster-name my-cluster --addon-name coredns --addon-version v1.11.1-eksbuild.9 \
         --resolve-conflicts PRESERVE --configuration-values '{"replicaCount":3}'
     ```

     It might take several seconds for the update to complete\.

1. Confirm that the add\-on version was updated\. Replace `my-cluster` with the name of your cluster\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name coredns
   ```

   It might take several seconds for the update to complete\.

   An example output is as follows\.

   ```
   {
       "addon": {
           "addonName": "coredns",
           "clusterName": "my-cluster",
           "status": "ACTIVE",
           "addonVersion": "v1.11.1-eksbuild.9",
           "health": {
               "issues": []
           },
           "addonArn": "arn:aws:eks:region:111122223333:addon/my-cluster/coredns/d2c34f06-1111-2222-1eb0-24f64ce37fa4",
           "createdAt": "2023-03-01T16:41:32.442000+00:00",
           "modifiedAt": "2023-03-01T18:16:54.332000+00:00",
           "tags": {},
           "configurationValues": "{\"replicaCount\":3}"
       }
   }
   ```