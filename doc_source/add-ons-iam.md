# Attach an IAM Role to an Amazon EKS add\-on using Pod Identity<a name="add-ons-iam"></a>

Certain Amazon EKS add\-ons need IAM role permissions to call AWS APIs\. For example, the Amazon VPC CNI add\-on calls certain AWS APIs to configure networking resources in your account\. These add\-ons need to be granted permission using AWS IAM\. More specifically, the service account of the pod running the add\-on needs to be associated with an IAM Role with a sufficient IAM Policy\. 

The recommended way to grant AWS permissions to cluster workloads is using the Amazon EKS feature Pod Identities\. You can use a **Pod Identity Association **to map the service account of an add\-on to an IAM role\. If a pod uses a service account that has an association, Amazon EKS sets environment variables in the containers of the pod\. The environment variables configure the AWS SDKs, including the AWS CLI, to use the EKS Pod Identity credentials\. [Learn more about EKS Pod Identities\. ](pod-identities.md)

Amazon EKS add\-ons can help manage the life cycle of pod identity associations corresponding to the add\-on\. For example, you can create or update an Amazon EKS add\-on and the necessary pod identity association in a single API call\. Amazon EKS also provides an API for retrieving suggested IAM policies\.

**Suggested Usage:**

1. Confirm that [Amazon EKS pod identity agent](pod-id-agent-setup.md) is setup on your cluster\.

1. Determine if the add\-on you want to install requires IAM permissions using the `describe-addon-versions` AWS CLI operation\. If the `requiresIamPermissions` flag is `true`, then you should use the `describe-addon-configurations` operation to determine the permissions needed by the addon\. The response includes a list of suggested managed IAM policies\. 

1. Retrieve the name of the Kubernetes Service Account and the suggested IAM policy using the `describe-addon-configuration` CLI operation\. Evaluate the scope of the suggested policy against your security requirements\.

1. Create an IAM role using the suggested permissions policy, and the trust policy required by Pod Identity\. For more information, see [Creating the EKS Pod Identity association](pod-id-association.md#pod-id-association-create)\. 

1. Create or update an Amazon EKS add\-on using the CLI\. Specify at least one pod identity association\. A pod identity association is \(1\) the name of a Kubernetes service account, and \(2\) the ARN of an IAM role\. 

**Considerations:**
+ Pod identity associations created using the add\-on APIs are owned by the respective add\-on\. If you delete the add\-on, the pod identity association is also deleted\. You can prevent this cascading delete by using the `preserve` option when deleting an addon using the AWS CLI or API\. You also can directly update or delete the pod identity association if necessary\. Add\-ons cannot assume ownership of existing pod identity associations\. You must delete the existing association and re\-create it using an add\-on create or update operation\. 
+ Amazon EKS recommends using pod identity associations to manage IAM permissions for add\-ons\. The previous method, IAM roles for service accounts \(IRSA\), is still supported\. You can specify both an IRSA `serviceAccountRoleArn` and a pod identity association for an add\-on\. If the EKS pod identity agent is installed on the cluster, the `serviceAccountRoleArn` will be ignored, and EKS will use the provided pod identity association\. If Pod Identity is not enabled, the `serviceAccountRoleArn` will be used\. 
+ If you update the pod identity associations for an existing add\-on, Amazon EKS initiates a rolling restart of the add\-on pods\.

 

## Retrieve IAM info about an Add\-on<a name="retreive-iam-info"></a>

You can use the AWS CLI to determine \(1\) if an add\-on requires IAM permissions, and \(2\) a suggested IAM policy for that add\-on\. 

**Retrieve IAM info about an Amazon EKS Add\-on \(AWS CLI\)**

1. Determine the name of the add\-on you want to install, and the Kubernetes version of your cluster\. [Learn more about available Amazon EKS Add\-ons\.](eks-add-ons.md#workloads-add-ons-available-eks) 

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

1. Create an IAM role and attach the recommended Managed Policy\. Alternatively, review the managed policy and scope down the permissions as appropriate\. [Review the instructions for creating an IAM Role for use with EKS Pod Identities\.](pod-id-association.md#pod-id-association-create) 

## Update Add\-on with IAM Role<a name="update-addon-role"></a>

**Update an Amazon EKS Add\-on to use a Pod Identity Association \(AWS CLI\)**

1. Determine:
   + `cluster-name` – The name of the EKS cluster to install the add\-on onto\.
   + `addon-name` – The name of the Amazon EKS add\-on to install\.
   + `service-account-name` – The name of the Kubernetes Service Account used by the add\-on\.
   + `iam-role-arn` – The ARN of an IAM role with sufficient permissions for the add\-on\. [The IAM Role must have the required trust policy for EKS Pod Identity\. ](pod-id-association.md#pod-id-association-create)

1. Update the add\-on using the AWS CLI\. You can also specify pod identity associations when creating an add\-on, using the same `--pod-identity-assocations` syntax\. Note that when you specify pod identity associations while updating an add\-on, all previous pod identity associations are overwritten\. 

   ```
   aws eks update-addon --cluster-name <cluster-name> \
   --addon-name <addon-name> \
   --pod-identity-associations 'serviceAccount=<service-account-name>,roleArn=<role-arn>'
   ```

   For example:

   ```
   aws eks update-addon --cluster-name mycluster \
   --addon-name aws-ebs-csi-driver \
   --pod-identity-associations 'serviceAccount=ebs-csi-controller-sa,roleArn=arn:aws:iam::123456789012:role/StorageDriver'
   ```

1. Validate the pod identity association was created:

   ```
   aws eks list-pod-identity-associations --cluster-name <cluster-name> 
   ```

   If successful, you should see output similar to the following\. Note the OwnerARN of the EKS add\-on\. 

   ```
   {
       "associations": [
           {
               "clusterName": "mycluster",
               "namespace": "kube-system",
               "serviceAccount": "ebs-csi-controller-sa",
               "associationArn": "arn:aws:eks:us-west-2:123456789012:podidentityassociation/mycluster/a-4wvljrezsukshq1bv",
               "associationId": "a-4wvljrezsukshq1bv",
               "ownerArn": "arn:aws:eks:us-west-2:123456789012:addon/mycluster/aws-ebs-csi-driver/9cc7ce8c-2e15-b0a7-f311-426691cd8546"
           }
       ]
   }
   ```

## Remove Associations from Add\-on<a name="remove-addon-role"></a>

**Remove all pod identity associations from an Amazon EKS Add\-on \(AWS CLI\)**

1. Determine:
   + `cluster-name` – The name of the EKS cluster to install the add\-on onto\.
   + `addon-name` – The name of the Amazon EKS add\-on to install\.

1. Update the addon to specify an empty array of pod identity associations\. 

   ```
   aws eks update-addon --cluster-name <cluster-name> \
   --addon-name <addon-name> \
   --pod-identity-associations "[]"
   ```

## Troubleshoot Pod Identities for EKS Add\-ons<a name="addon-id-troubleshoot"></a>

If your add\-ons are encountering errors while attempting AWS API, SDK, or CLI operations, confirm the following:
+ The Pod Identity Agent is installed in your cluster\. 
  + [Review how to setup the Pod Identity Agent\.](pod-id-agent-setup.md)
+ The Add\-on has a valid pod identity association\.
  + Use the AWS CLI to retrieve the associations for service account name used by the add\-on\. 

    ```
    aws eks list-pod-identity-associations --cluster-name <cluster-name>
    ```
+ The intended IAM role has the required trust policy for EKS Pod Identities\. 
  + Use the AWS CLI to retrieve the trust policy for an add\-on\. 

    ```
    aws iam get-role --role-name <role-name> --query Role.AssumeRolePolicyDocument
    ```
+ The intended IAM role has the necessary permissions for the add\-on\.
  + Use AWS CloudTrail to review `AccessDenied` or `UnauthorizedOperation` events \.
+ The service account name in the pod identity association matches the service account name used by the add\-on\. 
  + [Review the documentation](eks-add-ons.md#workloads-add-ons-available-eks) for the add\-on to determine the service account name\. 