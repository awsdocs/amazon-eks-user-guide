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

   The example below allows permission to the *<my\-pod\-secrets\-bucket>* Amazon S3 bucket\. You can modify the policy document to suit your specific needs\.

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

## Create an IAM role for a service account<a name="create-service-account-iam-role"></a>

Create an IAM role for your service account\. You can use `eksctl`, the AWS Management Console, or the AWS CLI to create the role\.

**Prerequisites**
+ An existing cluster\. If you don't have one, you can create one using one of the [Getting started with Amazon EKS](getting-started.md) guides\.
+ If using the AWS Management Console or AWS CLI to create the role, then you must have an existing IAM OIDC provider for your cluster\. For more information, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ An existing IAM policy that includes the permissions for the AWS resources that your service account needs access to\. For more information, see [Create an IAM policy](#create-service-account-iam-policy)\.

You can create the IAM role with `eksctl`, the AWS Management Console, or the AWS CLI\. Select the tab with the name of the tool that you want to create the role with\.

------
#### [ eksctl ]

Create the service account and IAM role with the following command\. Replace the *`<example values>`* \(including *`<>`*\) with your own values\.

```
eksctl create iamserviceaccount \
    --name <service_account_name> \
    --namespace <service_account_namespace> \
    --cluster <cluster_name> \
    --attach-policy-arn <IAM_policy_ARN> \
    --approve \
    --override-existing-serviceaccounts
```

An AWS CloudFormation template is deployed that creates an IAM role and attaches the IAM policy to it\. The role is associated with a Kubernetes service account\. If your cluster didn't have an existing IAM OIDC provider, one was created\. If the service account doesn't exist, it is created in the namespace that you provided\. If the service account does exist, then it is annotated with `eks.amazonaws.com/role-arn: arn:aws:iam::<your-account-id>:role/<iam-role-name-that-was-created>`\.

------
#### [ AWS Management Console ]

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Select the name of your cluster and then select the **Configuration** tab\.

1. In the **Details** section, note the value of the **OpenID Connect provider URL**\.

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the navigation panel, choose **Roles**, **Create Role**\.

1. In the **Select type of trusted entity** section, choose **Web identity**\.

1. In the **Choose a web identity provider** section:

   1. For **Identity provider**, choose the URL for your cluster\.

   1. For **Audience**, choose `sts.amazonaws.com`\.

1. Choose **Next: Permissions**\.

1. In the **Attach Policy** section, select the IAM policy that has the permissions that you want your service account to use\.

1. Choose **Next: Tags**\.

1. On the **Add tags \(optional\)** screen, you can add tags for the account\. Choose **Next: Review**\.

1. For **Role Name**, enter a name for your role and then choose **Create Role**\.

1. After the role is created, choose the role in the console to open it for editing\.

1. Choose the **Trust relationships** tab, and then choose **Edit trust relationship**\.

1. Find the line that looks similar to the following:

   ```
   "oidc.eks.us-west-2.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E:aud": "sts.amazonaws.com"
   ```

   Change the line to look like the following line\. Replace *`<EXAMPLED539D4633E53DE1B716D3041E>`* \(including *`<>`*\)with your cluster's OIDC provider ID and replace <region\-code> with the Region code that your cluster is in\.

   ```
   "oidc.eks.<region-code>.amazonaws.com/id/<EXAMPLED539D4633E53DE1B716D3041E>:sub": "system:serviceaccount:<SERVICE_ACCOUNT_NAMESPACE>:<SERVICE_ACCOUNT_NAME>"
   ```
**Note**  
If you don't have an existing service account, then you need to create one\. For more information, see [Configure Service Accounts for Pods](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/) in the Kubernetes documentation\. For the service account to be able to use Kubernetes permissions, you must create a `Role`, or `ClusterRole` and then bind the role to the service account\. For more information, see [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) in the Kubernetes documentation\. When the [AWS VPC CNI plugin](pod-networking.md) is deployed, for example, the deployment manifest creates a service account, cluster role, and cluster role binding\. You can view the[ manifest](https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/v1.7.5/config/v1.7.5/aws-k8s-cni.yaml) on GitHub\.

1. Choose **Update Trust Policy** to finish\.

------
#### [ AWS CLI ]

1. Set your AWS account ID to an environment variable with the following command\.

   ```
   ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
   ```

1. Set your OIDC identity provider to an environment variable with the following command\. Replace the *`<example values>`* \(including *`<>`*\) with your own values\.
**Important**  
You must use at least version 1\.19\.7 or 2\.1\.26 of the AWS CLI to receive the proper output from this command\. For more information, see [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) in the *AWS Command Line Interface User Guide*\.

   ```
   OIDC_PROVIDER=$(aws eks describe-cluster --name <cluster-name> --query "cluster.identity.oidc.issuer" --output text | sed -e "s/^https:\/\///")
   ```

1. Copy the following code block to your computer and replace the *`<example values>`* \(including *`<>`*\) with your own values\.

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
             "${OIDC_PROVIDER}:sub": "system:serviceaccount:<my-namespace>:<my-service-account>"
           }
         }
       }
     ]
   }
   EOF
   echo "${TRUST_RELATIONSHIP}" > trust.json
   ```

1. Run the modified code block from the previous step to create a file named *`trust.json`*\.

1. Run the following AWS CLI command to create the role\.

   ```
   aws iam create-role --role-name <IAM_ROLE_NAME> --assume-role-policy-document file://trust.json --description "<IAM_ROLE_DESCRIPTION>"
   ```

1. Run the following command to attach your IAM policy to your role\.

   ```
   aws iam attach-role-policy --role-name <IAM_ROLE_NAME> --policy-arn=<IAM_POLICY_ARN>
   ```

------