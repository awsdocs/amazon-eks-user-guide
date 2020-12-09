# Enabling IAM roles for service accounts on your cluster<a name="enable-iam-roles-for-service-accounts"></a>

 Your cluster has an [OpenID Connect](https://openid.net/connect/) issuer URL associated with it\. You can view the URL within the Amazon EKS console, or you can use the following AWS CLI command to retrieve it\.

**Important**  
You must use at least version 1\.18\.190 or 2\.1\.7 of the AWS CLI to receive the proper output from this command\. For more information, see [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) in the *AWS Command Line Interface User Guide*\.

```
aws eks describe-cluster --name <cluster_name> --query "cluster.identity.oidc.issuer" --output text
```

Output:

```
https://oidc.eks.<region-code>.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E
```

To use IAM roles for service accounts in your cluster, you must create an IAM OIDC identity provider using either [`eksctl`](#create-oidc-eksctl) or the [AWS Management Console](#create-oidc-console)\.<a name="create-oidc-eksctl"></a>

**To create an IAM OIDC identity provider for your cluster with `eksctl`**

1. Check your `eksctl` version with the following command\. This procedure assumes that you have installed `eksctl` and that your `eksctl` version is at least `0.33.0`\. 

   ```
   eksctl version
   ```

    For more information about installing or upgrading `eksctl`, see [Installing or upgrading `eksctl`](eksctl.md#installing-eksctl)\.

1. Create your OIDC identity provider for your cluster with the following command\. Substitute <cluster\_name> with your own value\.

   ```
   eksctl utils associate-iam-oidc-provider --cluster <cluster_name> --approve
   ```<a name="create-oidc-console"></a>

**To create an IAM OIDC identity provider for your cluster with the AWS Management Console**

1. Retrieve the OIDC issuer URL from the Amazon EKS console description of your cluster or use the following AWS CLI command\. Replace `<cluster_name>` \(including `<>`\) with your own value\.
**Important**  
You must use at least version 1\.18\.190 or 2\.1\.7 of the AWS CLI to receive the proper output from this command\. For more information, see [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) in the *AWS Command Line Interface User Guide*\.

   ```
   aws eks describe-cluster --name <cluster_name> --query "cluster.identity.oidc.issuer" --output text
   ```

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the navigation panel, choose **Identity Providers**, and then choose **Add Provider**\.

1. For **Provider Type**, choose **OpenID Connect**\.

1. For **Provider URL**, paste the OIDC issuer URL for your cluster, and then choose **Get thumbprint**\.

1. For **Audience**, enter `sts.amazonaws.com` and choose **Add provider**\.

After you have enabled the IAM OIDC identity provider for your cluster, you can create IAM roles to associate with a service account in your cluster\. For more information, see [Creating an IAM role and policy for your service account](create-service-account-iam-policy-and-role.md)