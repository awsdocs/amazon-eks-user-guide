# Amazon EKS connector IAM role<a name="connector_IAM_role"></a>

You can connect Kubernetes clusters to view them in your AWS Management Console\. To connect to a Kubernetes cluster, create an IAM role\.

## Check for an existing EKS connector role<a name="check-connector-role"></a>

You can use the following procedure to check and see if your account already has the Amazon EKS connector role\.

**To check for the `AmazonEKSConnectorAgentRole` in the IAM console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the left navigation pane, choose **Roles**\. 

1. Search the list of roles for `AmazonEKSConnectorAgentRole`\. If a role that includes `AmazonEKSConnectorAgentRole` doesn't exist, then see [Creating the Amazon EKS connector agent role](#create-connector-role) to create the role\. If a role that includes `AmazonEKSConnectorAgentRole` does exist, then select the role to view the attached policies\.

1. Choose **Permissions**\.

1. Ensure that the **AmazonEKSConnectorAgentPolicy** managed policy is attached to the role\. If the policy is attached, your Amazon EKS connector role is properly configured\.

1. Choose **Trust relationships**, and then choose **Edit trust policy**\.

1. Verify that the trust relationship contains the following policy\. If the trust relationship matches the following policy, choose **Cancel**\. If the trust relationship doesn't match, copy the policy into the **Edit trust policy** window and choose **Update policy**\.

   ```
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Principal": {
                   "Service": [
                       "ssm.amazonaws.com"
                   ]
               },
               "Action": "sts:AssumeRole"
           }
       ]
   }
   ```

## Creating the Amazon EKS connector agent role<a name="create-connector-role"></a>

You can use the AWS Management Console or AWS CloudFormation to create the connector agent role\.

------
#### [ AWS CLI ]

1. Create a file named `eks-connector-agent-trust-policy.json` that contains the following JSON to use for the IAM role\.

   ```
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Principal": {
                   "Service": [
                       "ssm.amazonaws.com"
                   ]
               },
               "Action": "sts:AssumeRole"
           }
       ]
   }
   ```

1. Create a file named `eks-connector-agent-policy.json` that contains the following JSON to use for the IAM role\.

   ```
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Sid": "SsmControlChannel",
               "Effect": "Allow",
               "Action": [
                   "ssmmessages:CreateControlChannel"
               ],
               "Resource": "arn:aws:eks:*:*:cluster/*"
           },
           {
               "Sid": "ssmDataplaneOperations",
               "Effect": "Allow",
               "Action": [
                   "ssmmessages:CreateDataChannel",
                   "ssmmessages:OpenDataChannel",
                   "ssmmessages:OpenControlChannel"
               ],
               "Resource": "*"
           }
       ]
   }
   ```

1. Create the Amazon EKS Connector agent role using the trust policy and policy you created in the previous list items\.

   ```
   aws iam create-role \
        --role-name AmazonEKSConnectorAgentRole \
        --assume-role-policy-document file://eks-connector-agent-trust-policy.json
   ```

1. Attach the policy to your Amazon EKS Connector agent role\.

   ```
   aws iam put-role-policy \
        --role-name AmazonEKSConnectorAgentRole \
        --policy-name AmazonEKSConnectorAgentPolicy \
        --policy-document file://eks-connector-agent-policy.json
   ```

------
#### [ AWS CloudFormation ]<a name="create-connector-role-cfn"></a>

**To create your Amazon EKS connector agent role with AWS CloudFormation\.**

1. Save the following AWS CloudFormation template to a text file on your local system\.
**Note**  
This template also creates the service\-linked role that would otherwise be created when the `registerCluster` API is called\. See [Using roles to connect a Kubernetes cluster to Amazon EKS](using-service-linked-roles-eks-connector.md) for details\.

   ```
   ---
   AWSTemplateFormatVersion: '2010-09-09'
   Description: 'Provisions necessary resources needed to register clusters in EKS'
   Parameters: {}
   Resources:
     EKSConnectorSLR:
       Type: AWS::IAM::ServiceLinkedRole
       Properties:
         AWSServiceName: eks-connector.amazonaws.com
   
     EKSConnectorAgentRole:
       Type: AWS::IAM::Role
       Properties:
         AssumeRolePolicyDocument:
           Version: '2012-10-17'
           Statement:
             - Effect: Allow
               Action: [ 'sts:AssumeRole' ]
               Principal:
                 Service: 'ssm.amazonaws.com'
   
     EKSConnectorAgentPolicy:
       Type: AWS::IAM::Policy
       Properties:
         PolicyName: EKSConnectorAgentPolicy
         Roles:
           - {Ref: 'EKSConnectorAgentRole'}
         PolicyDocument:
           Version: '2012-10-17'
           Statement:
             - Effect: 'Allow'
               Action: [ 'ssmmessages:CreateControlChannel' ]
               Resource:
               - Fn::Sub: 'arn:${AWS::Partition}:eks:*:*:cluster/*'
             - Effect: 'Allow'
               Action: [ 'ssmmessages:CreateDataChannel', 'ssmmessages:OpenDataChannel', 'ssmmessages:OpenControlChannel' ]
               Resource: "*"
   Outputs:
     EKSConnectorAgentRoleArn:
       Description: The agent role that EKS connector uses to communicate with AWS services.
       Value: !GetAtt EKSConnectorAgentRole.Arn
   ```

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. Choose **Create stack** \(either with new resources or existing resources\.

1. For **Specify template**, select **Upload a template file**, and then choose **Choose file**\.

1. Choose the file you created earlier, and then choose **Next**\.

1. For **Stack name**, enter a name for your role, such as `eksConnectorAgentRole`, and then choose **Next**\.

1. On the **Configure stack options** page, choose **Next**\.

1. On the **Review** page, review your information, acknowledge that the stack might create IAM resources, and then choose **Create stack**\.

------