# Using roles for Amazon EKS Fargate profiles<a name="using-service-linked-roles-eks-fargate"></a>

Amazon EKS uses AWS Identity and Access Management \(IAM\)[ service\-linked roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html#iam-term-service-linked-role)\. A service\-linked role is a unique type of IAM role that is linked directly to Amazon EKS\. Service\-linked roles are predefined by Amazon EKS and include all the permissions that the service requires to call other AWS services on your behalf\. 

A service\-linked role makes setting up Amazon EKS easier because you don't have to manually add the necessary permissions\. Amazon EKS defines the permissions of its service\-linked roles, and unless defined otherwise, only Amazon EKS can assume its roles\. The defined permissions include the trust policy and the permissions policy, and that permissions policy cannot be attached to any other IAM entity\.

You can delete a service\-linked role only after first deleting their related resources\. This protects your Amazon EKS resources because you can't inadvertently remove permission to access the resources\.

For information about other services that support service\-linked roles, see [AWS services that work with IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-services-that-work-with-iam.html) and look for the services that have **Yes **in the **Service\-linked role** column\. Choose a **Yes** with a link to view the service\-linked role documentation for that service\.

## Service\-linked role permissions for Amazon EKS<a name="service-linked-role-permissions-eks-fargate"></a>

Amazon EKS uses the service\-linked role named `AWSServiceRoleForAmazonEKSForFargate` – The role allows Amazon EKS Fargate to configure VPC networking required for Fargate Pods\. The attached policies allow the role to create and delete Elastic Network Interfaces and describe Elastic Network Interfaces and resources\.

The `AWSServiceRoleForAmazonEKSForFargate` service\-linked role trusts the following services to assume the role:
+ `eks-fargate.amazonaws.com`

The role permissions policy allows Amazon EKS to complete the following actions on the specified resources:
+ [https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/aws-service-role/AmazonEKSForFargateServiceRolePolicy$jsonEditor](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/aws-service-role/AmazonEKSForFargateServiceRolePolicy$jsonEditor)

You must configure permissions to allow an IAM entity \(such as a user, group, or role\) to create, edit, or delete a service\-linked role\. For more information, see [Service\-linked role permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html#service-linked-role-permissions) in the *IAM User Guide*\.

## Creating a service\-linked role for Amazon EKS<a name="create-service-linked-role-eks-fargate"></a>

You don't need to manually create a service\-linked role\. When you create a Fargate profile in the AWS Management Console, the AWS CLI, or the AWS API, Amazon EKS creates the service\-linked role for you\. 

**Important**  
  This service\-linked role can appear in your account if you completed an action in another service that uses the features supported by this role\.  If you were using the Amazon EKS service before December 13, 2019, when it began supporting service\-linked roles, then Amazon EKS created the AWSServiceRoleForAmazonEKSForFargate role in your account\.  To learn more, see [A New Role Appeared in My IAM Account](https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_roles.html#troubleshoot_roles_new-role-appeared)\.

### Creating a service\-linked role in Amazon EKS \(AWS API\)<a name="create-service-linked-role-service-api-eks-fargate"></a>

You don't need to manually create a service\-linked role\. When you create a Fargate profile in the AWS Management Console, the AWS CLI, or the AWS API, Amazon EKS creates the service\-linked role for you\. 

If you delete this service\-linked role, and then need to create it again, you can use the same process to recreate the role in your account\. When you create another managed node group, Amazon EKS creates the service\-linked role for you again\. 

## Editing a service\-linked role for Amazon EKS<a name="edit-service-linked-role-eks-fargate"></a>

Amazon EKS does not allow you to edit the `AWSServiceRoleForAmazonEKSForFargate` service\-linked role\. After you create a service\-linked role, you cannot change the name of the role because various entities might reference the role\. However, you can edit the description of the role using IAM\. For more information, see [Editing a service\-linked role](https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html#edit-service-linked-role) in the *IAM User Guide*\.

## Deleting a service\-linked role for Amazon EKS<a name="delete-service-linked-role-eks-fargate"></a>

If you no longer need to use a feature or service that requires a service\-linked role, we recommend that you delete that role\. That way you don't have an unused entity that is not actively monitored or maintained\. However, you must clean up your service\-linked role before you can manually delete it\.

### Cleaning up a service\-linked role<a name="service-linked-role-review-before-delete-eks-fargate"></a>

Before you can use IAM to delete a service\-linked role, you must first delete any resources used by the role\.

**Note**  
If the Amazon EKS service is using the role when you try to delete the resources, then the deletion might fail\. If that happens, wait for a few minutes and try the operation again\.

**To delete Amazon EKS resources used by the `AWSServiceRoleForAmazonEKSForFargate` role\.**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select **Clusters**\.

1. On the **Clusters** page, select your cluster\.

1. Select the **Configuration** tab and then select the **Compute** tab\.

1. If there are any Fargate profiles in the **Fargate Profiles** section, select each one individually, and then choose **Delete**\.

1. Type the name of the profile in the deletion confirmation window, and then choose **Delete**\.

1. Repeat this procedure for any other Fargate profiles in the cluster and for any other clusters in your account\.

### Manually delete the service\-linked role<a name="slr-manual-delete-eks-fargate"></a>

Use the IAM console, the AWS CLI, or the AWS API to delete the AWSServiceRoleForAmazonEKSForFargate service\-linked role\. For more information, see [Deleting a service\-linked role](https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html#delete-service-linked-role) in the *IAM User Guide*\.

## Supported regions for Amazon EKS service\-linked roles<a name="slr-regions-eks-fargate"></a>

Amazon EKS supports using service\-linked roles in all of the regions where the service is available\. For more information, see [Amazon EKS Service Endpoints and Quotas](https://docs.aws.amazon.com/general/latest/gr/eks.html)\.