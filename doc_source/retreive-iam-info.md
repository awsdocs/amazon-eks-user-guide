# Retrieve IAM information about an Amazon EKS add\-on<a name="retreive-iam-info"></a>

Before you create an add\-on, use the AWS CLI to determine;
+ If the add\-on requires IAM perfmissions 
+ The suggested IAM policy to use

**Retrieve IAM info about an Amazon EKS Add\-on \(AWS CLI\)**

1. Determine the name of the add\-on you want to install, and the Kubernetes version of your cluster\. For more information about add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\. 

1. Use the AWS CLI to determine if the add\-on requires IAM permissions\. 

   ```
   aws eks describe-addon-versions \
   --addon-name <addon-name> \
   --kubernetes-version <kubernetes-version>
   ```

   For example:

   ```
   aws eks describe-addon-versions \
   --addon-name aws-ebs-csi-driver \
   --kubernetes-version 1.30
   ```

   Review the following sample output\. Note that `requiresIamPermissions` is `true`, and the default add\-on version\. You need to specify the add\-on version when retrieving the recommended IAM policy\.

   ```
   {
       "addons": [
           {
               "addonName": "aws-ebs-csi-driver",
               "type": "storage",
               "addonVersions": [
                   {
                       "addonVersion": "v1.31.0-eksbuild.1",
                       "architecture": [
                           "amd64",
                           "arm64"
                       ],
                       "compatibilities": [
                           {
                               "clusterVersion": "1.30",
                               "platformVersions": [
                                   "*"
                               ],
                               "defaultVersion": true
                           }
                       ],
                       "requiresConfiguration": false,
                       "requiresIamPermissions": true
                   },
   [...]
   ```

1. If the add\-on requires IAM permissions, use the AWS CLI to retrieve a recommended IAM policy\. 

   ```
   aws eks describe-addon-configuration \
   --query podIdentityConfiguration \
   --addon-name <addon-name> \
   --addon-version <addon-version>
   ```

   For example:

   ```
   aws eks describe-addon-configuration \
   --query podIdentityConfiguration \
   --addon-name aws-ebs-csi-driver \
   --addon-version v1.31.0-eksbuild.1
   ```

   Review the following output\. Note the `recommendedManagedPolicies`\.

   ```
   [
       {
           "serviceAccount": "ebs-csi-controller-sa",
           "recommendedManagedPolicies": [
               "arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy"
           ]
       }
   ]
   ```

1. Create an IAM role and attach the recommended Managed Policy\. Alternatively, review the managed policy and scope down the permissions as appropriate\. For more information see [Creating the EKS Pod Identity association](pod-id-association.md#pod-id-association-create)\. 