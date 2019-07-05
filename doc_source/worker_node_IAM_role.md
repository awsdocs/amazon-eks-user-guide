# Amazon EKS Worker Node IAM Role<a name="worker_node_IAM_role"></a>

The Amazon EKS worker node `kubelet` daemon makes calls to AWS APIs on your behalf\. Worker nodes receive permissions for these API calls through an IAM instance profile and associated policies\. Before you can launch worker nodes and register them into a cluster, you must create an IAM role for those worker nodes to use when they are launched\. This requirement applies to worker nodes launched with the Amazon EKS\-optimized AMI provided by Amazon, or with any other worker node AMIs that you intend to use\. Before you create worker nodes, you must create an IAM role with the following IAM policies:
+ `[AmazonEKSWorkerNodePolicy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy%24jsonEditor)`
+ `[AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor)`
+ `[AmazonEC2ContainerRegistryReadOnly](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly%24jsonEditor)`

## Check for an Existing Worker Node Role<a name="check-worker-node-role"></a>

You can use the following procedure to check and see if your account already has the Amazon EKS worker node role\.<a name="procedure_check_worker_node_role"></a>

**To check for the `NodeInstanceRole` in the IAM console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the navigation pane, choose **Roles**\. 

1. Search the list of roles for `NodeInstanceRole`\. If the role does not exist, see [Creating the Amazon EKS Worker Node Role](#create-worker-node-role) to create the role\. If the role does exist, select the role to view the attached policies\.

1. Choose **Permissions**\.

1. Ensure that the **AmazonEKSWorkerNodePolicy**, **AmazonEKS\_CNI\_Policy**, and **AmazonEC2ContainerRegistryReadOnly** managed policies are attached to the role\. If the policies are attached, your Amazon EKS worker node role is properly configured\.

1. Choose **Trust Relationships**, **Edit Trust Relationship**\.

1. Verify that the trust relationship contains the following policy\. If the trust relationship matches the policy below, choose **Cancel**\. If the trust relationship does not match, copy the policy into the **Policy Document** window and choose **Update Trust Policy**\.

   ```
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "Service": "ec2.amazonaws.com"
         },
         "Action": "sts:AssumeRole"
       }
     ]
   }
   ```

## Creating the Amazon EKS Worker Node Role<a name="create-worker-node-role"></a>

If you created your worker nodes by following the steps in the [Getting Started with the AWS Management Console](getting-started-console.md) or [Getting Started with `eksctl`](getting-started-eksctl.md) topics, then the worker node role account already exists and you don't need to manually create it\. You can use the following procedure to create the Amazon EKS worker node role if you do not already have one for your account\.

**To create your Amazon EKS worker node role in the IAM console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. Choose **Roles**, then **Create role**\.

1. Choose **EC2** from the list of services, then **Next: Permissions**\.

1. Select the following policies:
   + **AmazonEKSWorkerNodePolicy**
   + **AmazonEKS\_CNI\_Policy**
   + **AmazonEC2ContainerRegistryReadOnly**

1. Choose **Next: Tags**\.

1. \(Optional\) Add metadata to the role by attaching tags as key–value pairs\. For more information about using tags in IAM, see [Tagging IAM Entities](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html) in the *IAM User Guide*\. 

1. Choose **Next: Review**\.

1. For **Role name**, enter a unique name for your role, such as `NodeInstanceRole`, then choose **Create role**\.

**To create your Amazon EKS instance role with AWS CloudFormation**

1. Save the following AWS CloudFormation template to a text file on your local system\.

   ```
   ---
   AWSTemplateFormatVersion: '2010-09-09'
   Description: 'Amazon EKS Worker Node Role'
   
   
   Resources:
   
     NodeInstanceRole:
       Type: AWS::IAM::Role
       Properties:
         AssumeRolePolicyDocument:
           Version: 2012-10-17
           Statement:
             - Effect: Allow
               Principal:
                 Service: ec2.amazonaws.com
               Action: sts:AssumeRole
         Path: "/"
         ManagedPolicyArns:
           - arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy
           - arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy
           - arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly
   
   Outputs:
   
     RoleArn:
       Description: The role that the worker node kubelet uses to make calls to the Amazon EKS API on your behalf.
       Value: !GetAtt NodeInstanceRole.Arn
       Export:
         Name: !Sub "${AWS::Stack Name}-RoleARN"
   ```

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. Choose **Create stack**\.

1. For **Specify template**, select **Upload a template file**, and then choose **Choose file**\.

1. Choose the file you created earlier, and then choose **Next**\.

1. For **Stack name**, enter a name for your role, such as `NodeInstanceRole`, and then choose **Next**\.

1. On the **Configure stack options** page, choose **Next**\.

1. On the **Review** page, review your information, acknowledge that the stack might create IAM resources, and then choose **Create stack**\.
