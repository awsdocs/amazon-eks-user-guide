# Amazon EKS Service IAM Role<a name="service_IAM_role"></a>

Amazon EKS makes calls to other AWS services on your behalf to manage the resources that you use with the service\. Before you can use the service, you must create an IAM role with the following IAM policies:
+ `[AmazonEKSServicePolicy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSServicePolicy%24jsonEditor)`
+ `[AmazonEKSClusterPolicy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSClusterPolicy%24jsonEditor)`

## Check for an Existing `AWSServiceRoleForAmazonEKS` Role<a name="check-service-role"></a>

You can use the following procedure to check and see if your account already has the Amazon EKS service role\.<a name="procedure_check_service_role"></a>

**To check for the `AWSServiceRoleForAmazonEKS` in the IAM console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the navigation pane, choose **Roles**\. 

1. Search the list of roles for `AWSServiceRoleForAmazonEKS`\. If the role does not exist, see [Creating the `AWSServiceRoleForAmazonEKS` role](#create-service-role) to create the role\. If the role does exist, select the role to view the attached policies\.

1. Choose **Permissions**\.

1. Ensure that the **AmazonEKSServicePolicy** and **AmazonEKSClusterPolicy** managed policies are attached to the role\. If the policies are attached, your Amazon EKS service role is properly configured\.

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

## Creating the `AWSServiceRoleForAmazonEKS` role<a name="create-service-role"></a>

You can use the following procedure to create the Amazon EKS service role if you do not already have one for your account\.

**To create your Amazon EKS service role in the IAM console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. Choose **Roles**, then **Create role**\.

1. Choose **EKS** from the list of services, then **Allows Amazon EKS to manage your clusters on your behalf** for your use case, then **Next: Permissions**\.

1. Choose **Next: Review**\.

1. For **Role name**, enter a unique name for your role, such as `eksServiceRole`, then choose **Create role**\.

**To create your Amazon EKS service role with AWS CloudFormation**

1. Save the following AWS CloudFormation template to a text file on your local system\.

   ```
   ---
   AWSTemplateFormatVersion: '2010-09-09'
   Description: 'Amazon EKS Service Role'
   
   
   Resources:
   
     AWSServiceRoleForAmazonEKS:
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
           - arn:aws:iam::aws:policy/AmazonEKSServicePolicy
           - arn:aws:iam::aws:policy/AmazonEKSClusterPolicy
   
   Outputs:
   
     RoleArn:
       Description: The role that EKS will use to create AWS resources for Kubernetes clusters
       Value: !GetAtt AWSServiceRoleForAmazonEKS.Arn
       Export:
         Name: !Sub "${AWS::StackName}-RoleArn"
   ```

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. Choose **Create stack**\.

1. For **Choose a template**, select **Upload a template to Amazon S3**, and then choose **Browse**\.

1. Choose the file you created earlier, and then choose **Next**\.

1. For **Stack name**, enter a name for your role, such as `eksServiceRole`, and then choose **Next**\.

1. On the **Options** page, choose **Next**\.

1. On the **Review** page, review your information, acknowledge that the stack might create IAM resources, and then choose **Create**\.