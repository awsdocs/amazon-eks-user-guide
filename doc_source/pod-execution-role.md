# Amazon EKS Pod execution IAM role<a name="pod-execution-role"></a>

The Amazon EKS Pod execution role is required to run Pods on AWS Fargate infrastructure\.

When your cluster creates Pods on AWS Fargate infrastructure, the components running on the Fargate infrastructure must make calls to AWS APIs on your behalf\. This is so that they can do actions such as pull container images from Amazon ECR or route logs to other AWS services\. The Amazon EKS Pod execution role provides the IAM permissions to do this\.

When you create a Fargate profile, you must specify a Pod execution role for the Amazon EKS components that run on the Fargate infrastructure using the profile\. This role is added to the cluster's Kubernetes [Role based access control](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) \(RBAC\) for authorization\. This allows the `kubelet` that's running on the Fargate infrastructure to register with your Amazon EKS cluster so that it can appear in your cluster as a node\.

**Note**  
The Fargate profile must have a different IAM role than Amazon EC2 node groups\.

**Important**  
The containers running in the Fargate Pod can't assume the IAM permissions associated with a Pod execution role\. To give the containers in your Fargate Pod permissions to access other AWS services, you must use [IAM roles for service accounts](iam-roles-for-service-accounts.md)\.

Before you create a Fargate profile, you must create an IAM role with the `[AmazonEKSFargatePodExecutionRolePolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSFargatePodExecutionRolePolicy.html)`\.

## Check for a correctly configured existing Pod execution role<a name="check-pod-execution-role"></a>

You can use the following procedure to check and see if your account already has a correctly configured Amazon EKS Pod execution role\. To avoid a confused deputy security problem, it's important that the role restricts access based on `SourceArn`\. You can modify the execution role as needed to include support for Fargate profiles on other clusters\.

**To check for an Amazon EKS Pod execution role in the IAM console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the left navigation pane, choose **Roles**\. 

1. On the **Roles** page, search the list of roles for **AmazonEKSFargatePodExecutionRole**\. If the role doesn't exist, see [Creating the Amazon EKS Pod execution role](#create-pod-execution-role) to create the role\. If the role does exist, choose the role\.

1. On the **AmazonEKSFargatePodExecutionRole** page, do the following:

   1. Choose **Permissions**\.

   1. Ensure that the **AmazonEKSFargatePodExecutionRolePolicy** Amazon managed policy is attached to the role\.

   1. Choose **Trust relationships**\.

   1. Choose **Edit trust policy**\.

1. On the **Edit trust policy** page, verify that the trust relationship contains the following policy and has a line for Fargate profiles on your cluster\. If so, choose **Cancel**\.

   ```
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Condition": {
            "ArnLike": {
               "aws:SourceArn": "arn:aws:eks:region-code:111122223333:fargateprofile/my-cluster/*"
            }
         },
         "Principal": {
           "Service": "eks-fargate-pods.amazonaws.com"
         },
         "Action": "sts:AssumeRole"
       }
     ]
   }
   ```

   If the policy matches but doesn't have a line specifying the Fargate profiles on your cluster, you can add the following line at the top of the `ArnLike` object\. Replace `region-code` with the AWS Region that your cluster is in, `111122223333` with your account ID, and `my-cluster` with the name of your cluster\.

   ```
   "aws:SourceArn": "arn:aws:eks:region-code:111122223333:fargateprofile/my-cluster/*",
   ```

   If the policy doesn't match, copy the full previous policy into the form and choose **Update policy**\. Replace `region-code` with the AWS Region that your cluster is in\. If you want to use the same role in all AWS Regions in your account, replace *region\-code* with `*`\. Replace `111122223333` with your account ID and `my-cluster` with the name of your cluster\. If you want to use the same role for all clusters in your account, replace `my-cluster` with `*`\.

## Creating the Amazon EKS Pod execution role<a name="create-pod-execution-role"></a>

If you don't already have the Amazon EKS Pod execution role for your cluster, you can use the AWS Management Console or the AWS CLI to create it\.

------
#### [ AWS Management Console ]

**To create an AWS FargatePod execution role with the AWS Management Console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the left navigation pane, choose **Roles**\.

1. On the **Roles** page, choose **Create role**\.

1. On the **Select trusted entity** page, do the following:

   1. In the **Trusted entity type** section, choose **AWS service**\. 

   1. From the **Use cases for other AWS services** dropdown list, choose **EKS**\.

   1. Choose **EKS \- Fargate Pod**\.

   1. Choose **Next**\.

1. On the **Add permissions** page, choose **Next**\.

1. On the **Name, review, and create** page, do the following:

   1. For **Role name**, enter a unique name for your role, such as **AmazonEKSFargatePodExecutionRole**\.

   1. Under **Add tags \(Optional\)**, add metadata to the role by attaching tags as key\-value pairs\. For more information about using tags in IAM, see [Tagging IAM resources](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html) in the *IAM User Guide*\.

   1. Choose **Create role**\.

1. On the **Roles** page, search the list of roles for **AmazonEKSFargatePodExecutionRole**\. Choose the role\.

1. On the **AmazonEKSFargatePodExecutionRole** page, do the following:

   1. Choose **Trust relationships**\.

   1. Choose **Edit trust policy**\.

1. On the **Edit trust policy** page, do the following:

   1. Copy and paste the following contents into the **Edit trust policy** form\. Replace *region\-code* with the AWS Region that your cluster is in\. If you want to use the same role in all AWS Regions in your account, replace *region\-code* with `*`\. Replace `111122223333` with your account ID and `my-cluster` with the name of your cluster\. If you want to use the same role for all clusters in your account, replace `my-cluster` with `*`\.

      ```
      {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect": "Allow",
            "Condition": {
               "ArnLike": {
                  "aws:SourceArn": "arn:aws:eks:region-code:111122223333:fargateprofile/my-cluster/*"
               }
            },
            "Principal": {
              "Service": "eks-fargate-pods.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
          }
        ]
      }
      ```

   1. Choose **Update policy**\.

------
#### [ AWS CLI ]

**To create an AWS FargatePod execution role with the AWS CLI**

1. Copy and paste the following contents to a file named `pod-execution-role-trust-policy.json`\. Replace *region\-code* with the AWS Region that your cluster is in\. If you want to use the same role in all AWS Regions in your account, replace *region\-code* with `*`\. Replace `111122223333` with your account ID and `my-cluster` with the name of your cluster\. If you want to use the same role for all clusters in your account, replace `my-cluster` with `*`\.

   ```
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Condition": {
            "ArnLike": {
               "aws:SourceArn": "arn:aws:eks:region-code:111122223333:fargateprofile/my-cluster/*"
            }
         },
         "Principal": {
           "Service": "eks-fargate-pods.amazonaws.com"
         },
         "Action": "sts:AssumeRole"
       }
     ]
   }
   ```

1. Create a Pod execution IAM role\.

   ```
   aws iam create-role \
     --role-name AmazonEKSFargatePodExecutionRole \
     --assume-role-policy-document file://"pod-execution-role-trust-policy.json"
   ```

1. Attach the required Amazon EKS managed IAM policy to the role\.

   ```
   aws iam attach-role-policy \
     --policy-arn arn:aws:iam::aws:policy/AmazonEKSFargatePodExecutionRolePolicy \
     --role-name AmazonEKSFargatePodExecutionRole
   ```

------