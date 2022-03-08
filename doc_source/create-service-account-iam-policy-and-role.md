# Creating an IAM role and policy for your service account<a name="create-service-account-iam-policy-and-role"></a>

You must create an IAM policy that specifies the permissions that you would like the containers in your pods to have\. You have several ways to create a new IAM permission policy\. One way is to copy a complete AWS managed policy that already does some of what you're looking for and then customize it to your specific requirements\. For more information, see [Creating a New Policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html) in the *IAM User Guide*\.

You must also create an IAM role for your Kubernetes service accounts to use before you associate it with a service account\. The trust relationship is scoped to your cluster and service account so that each cluster and service account combination requires its own role\. You can then attach a specific IAM policy to the role that gives the containers in your pods the permissions you desire\. The following procedures describe how to do this\.

## Create an IAM policy<a name="create-service-account-iam-policy"></a>

In this procedure, we offer two example policies that you can use for your application:
+ A policy to allow read\-only access to an Amazon S3 bucket\. You could store configuration information or a bootstrap script in this bucket, and the containers in your pod can read the file from the bucket and load it into your application\.
+ A policy to allow paid container images from AWS Marketplace\.

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the left navigation pane, choose **Policies** and then choose **Create policy**\. 

1. Choose the **JSON** tab\.

1. In the **Policy Document** field, paste one of the following policies to apply to your service accounts, or paste your own policy document into the field\. You can also use the visual editor to construct your own policy\.

   The example below allows permission to the *my\-pod\-secrets\-bucket* Amazon S3 bucket\. You can modify the policy document to suit your specific needs\.

   ```
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "s3:GetObject"
         ],
         "Resource": [
           "arn:aws:s3:::my-pod-secrets-bucket/*"
         ]
       }
     ]
   }
   ```

   The example below gives the required permissions to use a paid container image from AWS Marketplace\.

   ```
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Action": [
           "aws-marketplace:RegisterUsage"
         ],
         "Effect": "Allow",
         "Resource": "*"
       }
     ]
   }
   ```

1. Choose **Review policy**\.

1. Enter a name and description for your policy and then choose **Create policy**\.

1. Record the Amazon Resource Name \(ARN\) of the policy to use later when you create your role\.

## Create an IAM role for a service account<a name="create-service-account-iam-role"></a>

Create an IAM role for your Kubernetes service account\. You can use `eksctl`, the AWS Management Console, or the AWS CLI to create the role\.

**Prerequisites**
+ An existing cluster\. If you don't have one, you can create one using one of the [Getting started with Amazon EKS](getting-started.md) guides\.
+ If using the AWS Management Console or AWS CLI to create the role, then you must have an existing IAM OIDC provider for your cluster\. For more information, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ An existing IAM policy that includes the permissions for the AWS resources that your service account needs access to\. For more information, see [Create an IAM policy](#create-service-account-iam-policy)\.

You can create the IAM role with `eksctl` or the AWS CLI\.

------
#### [ eksctl ]

Create the service account and IAM role with the following command\. Replace *my\-service\-account* and *my\-namespace* with the Kubernetes service account and namespace that you want to associate the role to\. Replace *my\-cluster* with the name of your cluster\. Replace *111122223333* with your account ID \(or with **aws**, if you're attaching an AWS managed policy\) and replace *my\-iam\-policy* with the name of an existing policy that you created or an managed AWS IAM policy\.

```
eksctl create iamserviceaccount \
    --name my-service-account \
    --namespace my-namespace \
    --cluster my-cluster \
    --attach-policy-arn arn:aws:iam::111122223333:policy/my-iam-policy \
    --approve \
    --override-existing-serviceaccounts
```

`Eksctl` creates and deploys an AWS CloudFormation template\. The template creates an IAM role and attaches the IAM policy that you specified to it\. The role is associated with the Kubernetes service account that you specified\. If the Kubernetes service account didn't exist, `eksctl` created it in the namespace that you specified\. Whether `eksctl` created the service account or it already existed, `eksctl` annotated the service account with `eks.amazonaws.com/role-arn:arn:aws:iam::111122223333:role/eksctl-my-cluster-addon-iamserviceaccount-kube-s-Role1-1MKQC6VB7XEGT`\. This is the name of the IAM role created by the AWS CloudFormation template\.

------
#### [ AWS CLI ]

1. Set your AWS account ID to an environment variable with the following command\.

   ```
   ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
   ```

1. Set your OIDC identity provider to an environment variable with the following command\. Replace *my\-cluster* with the name of your cluster\.
**Important**  
You must use at least version 1\.22\.30 or 2\.4\.9 of the AWS CLI to receive the proper output from this command\. For more information, see [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) in the *AWS Command Line Interface User Guide*\.

   ```
   OIDC_PROVIDER=$(aws eks describe-cluster --name my-cluster --query "cluster.identity.oidc.issuer" --output text | sed -e "s/^https:\/\///")
   ```

1. Copy the following code block to your computer\. Replace *my\-namespace* and *my\-service\-account* with the Kubernetes namespace and service account that you want to associate the role to\.

   ```
   read -r -d '' TRUST_RELATIONSHIP <<EOF
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "Federated": "arn:aws:iam::${ACCOUNT_ID}:oidc-provider/${OIDC_PROVIDER}"
         },
         "Action": "sts:AssumeRoleWithWebIdentity",
         "Condition": {
           "StringEquals": {
             "${OIDC_PROVIDER}:aud": "sts.amazonaws.com",
             "${OIDC_PROVIDER}:sub": "system:serviceaccount:my-namespace:my-service-account"
           }
         }
       }
     ]
   }
   EOF
   echo "${TRUST_RELATIONSHIP}" > trust.json
   ```

1. Run the modified code block from the previous step to create a file named *`trust.json`*\.

1. Run the following AWS CLI command to create the role\. Replace *my\-iam\-role* with a name for your IAM role, and *my\-role\-description* with a description for your role\.

   ```
   aws iam create-role --role-name my-iam-role --assume-role-policy-document file://trust.json --description "my-role-description"
   ```

1. Run the following command to attach an IAM policy to your role\. Replace *my\-iam\-role* with the name of your IAM role, *111122223333* with your account ID \(or with **aws**, if you're attaching an AWS managed policy\), and *my\-iam\-policy* with the name of an existing policy that you created or an IAM AWS managed policy\.

   ```
   aws iam attach-role-policy --role-name my-iam-role --policy-arn=arn:aws:iam::111122223333:policy/my-iam-policy
   ```

------