# Verifying Amazon EKS add\-on version compatibility with a cluster<a name="addon-compat"></a>

Before you create an Amazon EKS add\-on you need to verify that the Amazon EKS add\-on version is compatable with your cluster\.

Use the [`describe-addon-verisions` API ](https://docs.aws.amazon.com/eks/latest/APIReference/API_DescribeAddonVersions.html)to list the available versions of EKS add\-ons, and which Kubernetes versions each addon version supports\. 

**Verify add\-on compatability \(AWS CLI\)**

1. Verify the AWS CLI is installed and working with `aws sts get-caller-identity`\. If this command doesn't work, learn how to [Get started with the AWS CLI\.](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) 

1. Determine the name of the add\-on you want to retrieve version compatibility information for, such as `amazon-cloudwatch-observability`\.

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