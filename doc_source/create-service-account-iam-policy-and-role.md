# Creating an IAM role and policy for your service account<a name="create-service-account-iam-policy-and-role"></a>

You must create an IAM policy that specifies the permissions that you would like the containers in your pods to have\. You have several ways to create a new IAM permission policy\. One way is to copy a complete AWS managed policy that already does some of what you're looking for and then customize it to your specific requirements\. For more information, see [Creating a New Policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html) in the *IAM User Guide*\.

You must also create an IAM role for your Kubernetes service accounts to use before you associate it with a service account\. The trust relationship is scoped to your cluster and service account so that each cluster and service account combination requires its own role\. You can then attach a specific IAM policy to the role that gives the containers in your pods the permissions you desire\. The following procedures describe how to do this\.

## Create an IAM policy<a name="create-service-account-iam-policy"></a>

In this procedure, we offer two example policies that you can use for your application:
+ A policy to allow read\-only access to an Amazon S3 bucket\. You could store configuration information or a bootstrap script in this bucket, and the containers in your pod can read the file from the bucket and load it into your application\.
+ A policy to allow paid container images from AWS Marketplace\.

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the navigation panel, choose **Policies** and then choose **Create policy**\. 

1. Choose the **JSON** tab\.

1. In the **Policy Document** field, paste one of the following policies to apply to your service accounts, or paste your own policy document into the field\. You can also use the visual editor to construct your own policy\.

   The example below allows permission to the <my\-pod\-secrets\-bucket> Amazon S3 bucket\. You can modify the policy document to suit your specific needs\.

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
           "arn:aws:s3:::<my-pod-secrets-bucket>/*"
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

## Create an IAM role<a name="create-service-account-iam-role"></a>

Create an IAM role for your service accounts\. You can use[ `eksctl`](#create-service-account-eksctl), the [AWS Management Console](#create-service-account-console), or the [AWS CLI](#create-service-account-cli) to create the role\.
<a name="create-service-account-eksctl"></a>
**To create your service account with the `eksctl`**  
Create the service account and IAM role with the following command\. Substitute the <example values> with your own values\.

**Note**  
This command only works for clusters that were created with `eksctl`\. If you didn't create your cluster with `eksctl`, then use the instructions on the AWS Management Console or AWS CLI tabs\.

```
eksctl create iamserviceaccount \
    --name <service_account_name> \
    --namespace <service_account_namespace> \
    --cluster <cluster_name> \
    --attach-policy-arn <IAM_policy_ARN> \
    --approve \
    --override-existing-serviceaccounts
```

An AWS CloudFormation template was deployed that created an IAM role and attached the IAM policy to it\. The role was associated with a Kubernetes service account\.<a name="create-service-account-console"></a>

**To create your service account with the AWS Management Console**

1. Retrieve the OIDC issuer URL from the Amazon EKS console description of your cluster, or use the following AWS CLI command\.
**Important**  
You must use at least version 1\.18\.149 or 2\.0\.52 of the AWS CLI to receive the proper output from this command\. For more information, see [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) in the *AWS Command Line Interface User Guide*\.

   ```
   aws eks describe-cluster --name <cluster_name> --query "cluster.identity.oidc.issuer" --output text
   ```

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the navigation panel, choose **Roles**, **Create Role**\. 

1. In the **Select type of trusted entity** section, choose **Web identity**\.

1. In the **Choose a web identity provider** section:

   1. For **Identity provider**, choose the URL for your cluster\.

   1. For **Audience**, choose `sts.amazonaws.com`\.

1. Choose **Next: Permissions**\.

1. In the **Attach Policy** section, select the policy to use for your service account\. Choose **Next: Tags**\.

1. On the **Add tags \(optional\)** screen, you can add tags for the account\. Choose **Next: Review**\.

1. For **Role Name**, enter a name for your role and then choose **Create Role**\.

1. After the role is created, choose the role in the console to open it for editing\.

1. Choose the **Trust relationships** tab, and then choose **Edit trust relationship**\.

   1. Edit the OIDC provider suffix and change it from `:aud` to `:sub`\.

   1. Replace `sts.amazonaws.com` with your service account ID\.

   1. If necessary, change <region\-code> to the Region code returned in the output from step 1\.

   The resulting line should look like this\.

   ```
   "oidc.eks.<region-code>.amazonaws.com/id/<EXAMPLED539D4633E53DE1B716D3041E>:sub": "system:serviceaccount:<SERVICE_ACCOUNT_NAMESPACE>:<SERVICE_ACCOUNT_NAME>"
   ```

1. Choose **Update Trust Policy** to finish\.

1. Associate the IAM role with a Kubernetes service account\. For more information, see [Specifying an IAM role for your service account](specify-service-account-role.md)\.<a name="create-service-account-cli"></a>

**To create your service account with the AWS CLI**

1. Set your AWS account ID to an environment variable with the following command\.

   ```
   AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
   ```

1. Set your OIDC identity provider to an environment variable with the following command, replacing your cluster name\.
**Important**  
You must use at least version 1\.18\.149 or 2\.0\.52 of the AWS CLI to receive the proper output from this command\. For more information, see [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) in the *AWS Command Line Interface User Guide*\.

   ```
   OIDC_PROVIDER=$(aws eks describe-cluster --name <cluster-name> --query "cluster.identity.oidc.issuer" --output text | sed -e "s/^https:\/\///")
   ```

1. Copy the following code block to your computer and replace <namespace> and <service\-account\-name> with your own values\.

   ```
   read -r -d '' TRUST_RELATIONSHIP <<EOF
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "Federated": "arn:aws:iam::${AWS_ACCOUNT_ID}:oidc-provider/${OIDC_PROVIDER}"
         },
         "Action": "sts:AssumeRoleWithWebIdentity",
         "Condition": {
           "StringEquals": {
             "${OIDC_PROVIDER}:sub": "system:serviceaccount:<namespace>:<service-account-name>"
           }
         }
       }
     ]
   }
   EOF
   echo "${TRUST_RELATIONSHIP}" > trust.json
   ```

1. Run the modified code block from the previous step to create a file named `trust.json`\.

1. Run the following AWS CLI command to create the role, replacing your IAM role name and description\.

   ```
   aws iam create-role --role-name <IAM_ROLE_NAME> --assume-role-policy-document file://trust.json --description "<IAM_ROLE_DESCRIPTION>"
   ```

1. Run the following command to attach your IAM policy to your role, replacing your IAM role name and policy ARN\.

   ```
   aws iam attach-role-policy --role-name <IAM_ROLE_NAME> --policy-arn=<IAM_POLICY_ARN>
   ```

1. Associate the IAM role with a Kubernetes service account\. For more information, see [Specifying an IAM role for your service account](specify-service-account-role.md)\.