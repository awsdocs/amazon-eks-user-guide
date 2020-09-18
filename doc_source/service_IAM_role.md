# Amazon EKS cluster IAM role<a name="service_IAM_role"></a>

Kubernetes clusters managed by Amazon EKS make calls to other AWS services on your behalf to manage the resources that you use with the service\. Before you can create Amazon EKS clusters, you must create an IAM role with the following IAM policies:
+ `[AmazonEKSClusterPolicy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSClusterPolicy%24jsonEditor)`

**Note**  
Prior to April 16, 2020, [AmazonEKSServicePolicy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSServicePolicy%24jsonEditor) was also required and the suggested name was `eksServiceRole`\. With the `AWSServiceRoleForAmazonEKS` service\-linked role, that policy is no longer required for clusters created on or after April 16, 2020\.

## Check for an existing cluster role<a name="check-service-role"></a>

You can use the following procedure to check and see if your account already has the Amazon EKS cluster role\.<a name="procedure_check_service_role"></a>

**To check for the `eksClusterRole` in the IAM console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the navigation panel, choose **Roles**\. 

1. Search the list of roles for `eksClusterRole`\. If a role that includes `eksClusterRole` does not exist, then see [Creating the Amazon EKS cluster role](#create-service-role) to create the role\. If a role that includes `eksClusterRole` does exist, then select the role to view the attached policies\.

1. Choose **Permissions**\.

1. Ensure that the **AmazonEKSClusterPolicy** managed policy is attached to the role\. If the policy is attached, your Amazon EKS cluster role is properly configured\.

1. Choose **Trust Relationships**, **Edit Trust Relationship**\.

1. Verify that the trust relationship contains the following policy\. If the trust relationship matches the policy below, choose **Cancel**\. If the trust relationship does not match, copy the policy into the **Policy Document** window and choose **Update Trust Policy**\.

   ```
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "Service": "eks.amazonaws.com"
         },
         "Action": "sts:AssumeRole"
       }
     ]
   }
   ```

## Creating the Amazon EKS cluster role<a name="create-service-role"></a>

You can use the AWS Management Console or AWS CloudFormation to create the cluster role if you do not already have one for your account\. Select the name of the tool that you'd like to use to create the role\.

------
#### [ AWS Management Console ]

**To create your Amazon EKS cluster role in the IAM console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. Choose **Roles**, then **Create role**\.

1. Choose **EKS** from the list of services, then **EKS \- Cluster** for your use case, and then **Next: Permissions**\.

1. Choose **Next: Tags**\.

1. \(Optional\) Add metadata to the role by attaching tags as key–value pairs\. For more information about using tags in IAM, see [Tagging IAM Entities](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html) in the *IAM User Guide*\. 

1. Choose **Next: Review**\.

1. For **Role name**, enter a unique name for your role, such as `eksClusterRole`, then choose **Create role**\.

------
#### [ AWS CloudFormation ]

**To create your Amazon EKS cluster role with AWS CloudFormation**

1. Save the following AWS CloudFormation template to a text file on your local system\.

   ```
   ---
   AWSTemplateFormatVersion: '2010-09-09'
   Description: 'Amazon EKS Cluster Role'
   
   
   Resources:
   
     eksClusterRole:
       Type: AWS::IAM::Role
       Properties:
         AssumeRolePolicyDocument:
           Version: '2012-10-17'
           Statement:
           - Effect: Allow
             Principal:
               Service:
               - eks.amazonaws.com
             Action:
             - sts:AssumeRole
         ManagedPolicyArns:
           - arn:aws:iam::aws:policy/AmazonEKSClusterPolicy
   
   Outputs:
   
     RoleArn:
       Description: The role that Amazon EKS will use to create AWS resources for Kubernetes clusters
       Value: !GetAtt eksClusterRole.Arn
       Export:
         Name: !Sub "${AWS::StackName}-RoleArn"
   ```
**Note**  
Prior to April 16, 2020, `ManagedPolicyArns` had an entry for `arn:aws:iam::aws:policy/AmazonEKSServicePolicy`\. With the `AWSServiceRoleForAmazonEKS` service\-linked role, that policy is no longer required\.

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. Choose **Create stack**\.

1. For **Specify template**, select **Upload a template file**, and then choose **Choose file**\.

1. Choose the file you created earlier, and then choose **Next**\.

1. For **Stack name**, enter a name for your role, such as `eksClusterRole`, and then choose **Next**\.

1. On the **Configure stack options** page, choose **Next**\.

1. On the **Review** page, review your information, acknowledge that the stack might create IAM resources, and then choose **Create stack**\.

------