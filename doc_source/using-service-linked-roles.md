# Using Service\-Linked Roles for Amazon EKS<a name="using-service-linked-roles"></a>

Amazon Elastic Kubernetes Service uses AWS Identity and Access Management \(IAM\)[ service\-linked roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html#iam-term-service-linked-role)\. A service\-linked role is a unique type of IAM role that is linked directly to Amazon EKS\. Service\-linked roles are predefined by Amazon EKS and include all the permissions that the service requires to call other AWS services on your behalf\. 

A service\-linked role makes setting up Amazon EKS easier because you don’t have to manually add the necessary permissions\. Amazon EKS defines the permissions of its service\-linked roles, and unless defined otherwise, only Amazon EKS can assume its roles\. The defined permissions include the trust policy and the permissions policy, and that permissions policy cannot be attached to any other IAM entity\.

You can delete a service\-linked role only after first deleting their related resources\. This protects your Amazon EKS resources because you can't inadvertently remove permission to access the resources\.

For information about other services that support service\-linked roles, see [AWS Services That Work with IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-services-that-work-with-iam.html) and look for the services that have **Yes **in the **Service\-Linked Role** column\. Choose a **Yes** with a link to view the service\-linked role documentation for that service\.

## Service\-Linked Role Permissions for Amazon EKS<a name="slr-permissions"></a>

Amazon EKS uses the service\-linked role named **AWSServiceRoleForAmazonEKSNodegroup** – These permissions are required for managing nodegroups in your account\. These policies are related to management of the following resources: Auto Scaling groups, security groups, launch templates and IAM instance profiles\.\.

The AWSServiceRoleForAmazonEKSNodegroup service\-linked role trusts the following services to assume the role:
+ `eks-nodegroup.amazonaws.com`

The following role permissions policy allows Amazon EKS to complete AWS API actions on the specified resources:
+ [AWSServiceRoleForAmazonEKSNodegroup](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AWSServiceRoleForAmazonEKSNodegroup%24jsonEditor)

You must configure permissions to allow an IAM entity such as a user, group, or role to create, edit, or delete a service\-linked role\. For more information, see [Service\-Linked Role Permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html#service-linked-role-permissions) in the *IAM User Guide*\.

## Creating a Service\-Linked Role for Amazon EKS<a name="create-slr"></a>

You don't need to manually create a service\-linked role\. When you create a managed node group in the AWS Management Console, the AWS CLI, or the AWS API, Amazon EKS creates the service\-linked role for you\. 

If you delete this service\-linked role, and then need to create it again, you can use the same process to recreate the role in your account\. When you create another managed node group, Amazon EKS creates the service\-linked role for you again\. 

## Editing a Service\-Linked Role for Amazon EKS<a name="edit-slr"></a>

Amazon EKS does not allow you to edit the AWSServiceRoleForAmazonEKSNodegroup service\-linked role\. After you create a service\-linked role, you cannot change the name of the role because various entities might reference the role\.

## Deleting a Service\-Linked Role for Amazon EKS<a name="delete-slr"></a>

If you no longer need to use a feature or service that requires a service\-linked role, we recommend that you delete that role\. That way you don’t have an unused entity that is not actively monitored or maintained\. However, you must clean up the resources for your service\-linked role before you can manually delete it\.

**Note**  
If the Amazon EKS service is using the role when you try to delete the resources, then the deletion might fail\. If that happens, wait for a few minutes and try the operation again\.

**To delete Amazon EKS resources used by the AWSServiceRoleForAmazonEKSNodegroup**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose a cluster\.

1. On the cluster page, if there are any managed node groups in the **Node Groups** section, select each one individually, and then choose **Delete**\.

1. Type the name of the cluster in the deletion confirmation window, and then choose **Confirm** to delete\.

1. Repeat this procedure for any other node groups in the cluster and for any other clusters in your account\.

**To manually delete the service\-linked role using IAM**

Use the IAM console, the AWS CLI, or the AWS API to delete the AWSServiceRoleForAmazonEKSNodegroup service\-linked role\. For more information, see [Deleting a Service\-Linked Role](https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html#delete-service-linked-role) in the *IAM User Guide*\.

## Supported Regions for Amazon EKS Service\-Linked Roles<a name="slr-regions"></a>

Amazon EKS supports using service\-linked roles in all of the regions where the service is available\. For more information, see [Amazon EKS Regions and Endpoints](https://docs.aws.amazon.com/general/latest/gr/rande.html#eks_region)\.