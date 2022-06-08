# Create an IAM OIDC provider for your cluster<a name="enable-iam-roles-for-service-accounts"></a>

 Your cluster has an [OpenID Connect](https://openid.net/connect/) issuer URL associated with it\. To use IAM roles for service accounts, an IAM OIDC provider must exist for your cluster\.

**Prerequisites**  
An existing cluster\. If you don't have one, you can create one using one of the [Getting started with Amazon EKS](getting-started.md) guides\.

You can create an OIDC provider for your cluster using `eksctl` or the AWS Management Console\.

------
#### [ eksctl ]

**To create an IAM OIDC identity provider for your cluster with `eksctl`**

1. Determine whether you have an existing IAM OIDC provider for your cluster\.

   View your cluster's OIDC provider URL\.

   ```
   aws eks describe-cluster --name my-cluster --query "cluster.identity.oidc.issuer" --output text
   ```

   The example output is as follows\.

   ```
   https://oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE
   ```

   List the IAM OIDC providers in your account\. Replace `EXAMPLED539D4633E53DE1B71EXAMPLE` with the value returned from the previous command\.

   ```
   aws iam list-open-id-connect-providers | grep EXAMPLED539D4633E53DE1B71EXAMPLE
   ```

   The example output is as follows\.

   ```
   "Arn": "arn:aws:iam::111122223333:oidc-provider/oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE"
   ```

   If output is returned from the previous command, then you already have a provider for your cluster\. If no output is returned, then you must create an IAM OIDC provider\.

1. Create an IAM OIDC identity provider for your cluster with the following command\. Replace *my\-cluster* with your own value\.

   ```
   eksctl utils associate-iam-oidc-provider --cluster my-cluster --approve
   ```

------
#### [ AWS Management Console ]<a name="create-oidc-console"></a>

**To create an IAM OIDC identity provider for your cluster with the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Select the name of your cluster\.

1. In the **Details** section on the **Overview** tab, note the value of the **OpenID Connect provider URL**\.

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the left navigation pane, choose **Identity Providers** under **Access management**\. If a **Provider** is listed that matches the URL for your cluster, then you already have a provider for your cluster\. If a provider isn't listed that matches the URL for your cluster, then you must create one\.

1. To create a provider, choose **Add Provider**\.

1. For **Provider Type**, choose **OpenID Connect**\.

1. For **Provider URL**, paste the OIDC issuer URL for your cluster, and then choose **Get thumbprint**\.

1. For **Audience**, enter `sts.amazonaws.com` and choose **Add provider**\.

------