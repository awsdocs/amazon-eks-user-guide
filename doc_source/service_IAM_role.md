# Amazon EKS Service IAM Role<a name="service_IAM_role"></a>

Amazon EKS makes calls to other AWS services on your behalf to manage the resources that you use with the service\. Before you can use the service, you must create an IAM role that implements the following IAM policies:

* [`AmazonEKSServicePolicy`](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSServicePolicy$jsonEditor)
* [`AmazonEKSClusterPolicy`](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSClusterPolicy$jsonEditor)

Before you create this new role, you may wish to first check if it exists and verify that it is configured correctly. 

## Check for an existing `AWSServiceRoleForAmazonEKS` role in the IAM console

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the navigation pane, choose **Roles**\. 

1. Search the list of roles for `AWSServiceRoleForAmazonEKS`\. If the role exists, select the role to view the attached policies\.

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

If you were unable to verify the presence of an existing ```AWSServiceRoleForAmazonEKS``` role, one can easily be created via the console or CloudFormation.

## Creating the AWSServiceRoleForAmazonEKS role

The ```AWSServiceRoleForAmazonEKS``` role can be created [through the console](getting-started.md#role-create), or via a CloudFormation template:

```
AWSTemplateFormatVersion: 2010-09-09

Description: Creates AWS EKS Service Role

Resources:
  AWSEKSServiceRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: AWSServiceRoleForAmazonEKS
      AssumeRolePolicyDocument:
        Version: 2012-10-17
        Statement:
        -
          Effect: Allow
          Principal:
            Service:
              - eks.amazonaws.com
          Action:
            - sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonEKSClusterPolicy
        - arn:aws:iam::aws:policy/AmazonEKSServicePolicy
```
