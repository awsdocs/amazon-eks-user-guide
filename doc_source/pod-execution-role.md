# Amazon EKS pod execution IAM role<a name="pod-execution-role"></a>

The Amazon EKS pod execution role is required to run pods on AWS Fargate infrastructure\.

When your cluster creates pods on AWS Fargate infrastructure, the components running on the Fargate infrastructure need to make calls to AWS APIs on your behalf to do things like pull container images from Amazon ECR or route logs to other AWS services\. The Amazon EKS pod execution role provides the IAM permissions to do this\.

When you create a Fargate profile, you must specify a pod execution role for the Amazon EKS components that run on the Fargate infrastructure using the profile\. This role is added to the cluster's Kubernetes [Role based access control](https://kubernetes.io/docs/admin/authorization/rbac/) \(RBAC\) for authorization, so that the `kubelet` that is running on the Fargate infrastructure can register with your Amazon EKS cluster\. This is what allows Fargate infrastructure to appear in your cluster as nodes\.

**Note**  
The Fargate profile must have a different IAM role than Amazon EC2 node groups\.

The containers running in the Fargate pod cannot assume the IAM permissions associated with the pod execution role\. To give the containers in your Fargate pod permissions to access other AWS services, you must use [IAM roles for service accounts](iam-roles-for-service-accounts.md)\.

Before you create a Fargate profile, you must create an IAM role with the following IAM policy:
+ `[AmazonEKSFargatePodExecutionRolePolicy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSFargatePodExecutionRolePolicy%24jsonEditor)`

## Check for an existing pod execution role<a name="check-pod-execution-role"></a>

You can use the following procedure to check and see if your account already has the Amazon EKS pod execution role\.<a name="procedure_check_worker_node_role"></a>

**To check for the `AmazonEKSFargatePodExecutionRole` in the IAM console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the left navigation pane, choose **Roles**\. 

1. Search the list of roles for `AmazonEKSFargatePodExecutionRole`\. If the role does not exist, see [Creating the Amazon EKS pod execution role](#create-pod-execution-role) to create the role\. If the role does exist, select the role to view the attached policies\.

1. Choose **Permissions**\.

1. Ensure that the **AmazonEKSFargatePodExecutionRolePolicy** Amazon managed policy is attached to the role\. If the policy is attached, then your Amazon EKS pod execution role is properly configured\.

1. Choose **Trust relationships**, **Edit trust policy**\.

1. Verify that the trust relationship contains the following policy\. If the trust relationship matches the policy below, choose **Cancel**\. If the trust relationship does not match, copy the policy into the **Edit trust policy** window and choose **Update policy**\.

   ```
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "Service": "eks-fargate-pods.amazonaws.com"
         },
         "Action": "sts:AssumeRole"
       }
     ]
   }
   ```

## Creating the Amazon EKS pod execution role<a name="create-pod-execution-role"></a>

You can use the following procedure to create the Amazon EKS pod execution role if you do not already have one for your account\.

**To create an AWS Fargate pod execution role with the AWS Management Console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. Choose **Roles**, then **Create role**\.

1. Under **Use case**, choose **EKS** from the list of services under **Use cases for other AWS services**\.

1. Choose **EKS \- Fargate pod** for your use case, and then choose**Next**\.

1. On the **Add permissions** tab, choose **Next**\. 

1. For **Role name**, enter a unique name for your role, such as **AmazonEKSFargatePodExecutionRole**\.

1. or **Description**, replace the current text with descriptive text such as **Amazon EKS \- Pod execution role**\.

1. Choose **Create role**\.