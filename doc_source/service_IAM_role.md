# Amazon EKS cluster IAM role<a name="service_IAM_role"></a>

Kubernetes clusters managed by Amazon EKS make calls to other AWS services on your behalf to manage the resources that you use with the service\. Before you can create Amazon EKS clusters, you must create an IAM role with the following IAM policies:
+ `[AmazonEKSClusterPolicy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSClusterPolicy%24jsonEditor)`

**Note**  
Prior to April 16, 2020, [AmazonEKSServicePolicy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSServicePolicy%24jsonEditor) was also required and the suggested name was `eksServiceRole`\. With the `AWSServiceRoleForAmazonEKS` service\-linked role, that policy is no longer required for clusters created on or after April 16, 2020\.

## Check for an existing cluster role<a name="check-service-role"></a>

You can use the following procedure to check and see if your account already has the Amazon EKS cluster role\.

**To check for the `eksClusterRole` in the IAM console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the left navigation pane, choose **Roles**\. 

1. Search the list of roles for `eksClusterRole`\. If a role that includes `eksClusterRole` doesn't exist, then see [Creating the Amazon EKS cluster role](#create-service-role) to create the role\. If a role that includes `eksClusterRole` does exist, then select the role to view the attached policies\.

1. Choose **Permissions**\.

1. Ensure that the **AmazonEKSClusterPolicy** managed policy is attached to the role\. If the policy is attached, your Amazon EKS cluster role is properly configured\.

1. Choose **Trust relationships**, and then choose **Edit trust policy**\.

1. Verify that the trust relationship contains the following policy\. If the trust relationship matches the following policy, choose **Cancel**\. If the trust relationship doesn't match, copy the policy into the **Edit trust policy** window and choose **Update policy**\. 

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

You can use the AWS Management Console or the AWS CLI to create the cluster role\.

------
#### [ AWS Management Console ]<a name="create-cluster-role-console"></a>

**To create your Amazon EKS cluster role in the IAM console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. Choose **Roles**, then **Create role**\.

1. Under **Trusted entity type**, select **AWS service**\.

1. From the **Use cases for other AWS services** dropdown list, choose **EKS**\.

1. Choose **EKS \- Cluster** for your use case, and then choose **Next**\.

1. On the **Add permissions** tab, choose **Next**\.

1. For **Role name**, enter a unique name for your role, such as **eksClusterRole**\.

1. For **Description**, enter descriptive text such as **Amazon EKS \- Cluster role**\.

1. Choose **Create role**\.

------
#### [ AWS CLI ]

1. Copy the following contents to a file named `cluster-trust-policy.json`\. 

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

1. Create the role\. You can replace ***eksClusterRole*** with any name that you choose\.

   ```
   aws iam create-role \
     --role-name eksClusterRole \
     --assume-role-policy-document file://"cluster-trust-policy.json"
   ```

1. Attach the required IAM policy to the role\.

   ```
   aws iam attach-role-policy \
     --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy \
     --role-name eksClusterRole
   ```

------