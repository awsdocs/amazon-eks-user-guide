# Enabling IAM Roles for Service Accounts on your Cluster<a name="enable-iam-roles-for-service-accounts"></a>

The IAM roles for service accounts feature is available on new Amazon EKS Kubernetes version 1\.14 clusters, and clusters that were updated to versions 1\.14 or 1\.13 on or after September 3rd, 2019\. Existing clusters can update to version 1\.13 or 1\.14 to take advantage of this feature\. For more information, see [Updating an Amazon EKS Cluster Kubernetes Version](update-cluster.md)\.

If your cluster supports IAM roles for service accounts, it will have an [OpenID Connect](https://openid.net/connect/) issuer URL associated with it\. You can view this URL in the Amazon EKS console, or you can use the following AWS CLI command to retrieve it\.

**Important**  
You must use at least version 1\.18\.10 of the AWS CLI to receive the proper output from this command\. For more information, see [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) in the *AWS Command Line Interface User Guide*\.

```
aws eks describe-cluster --name cluster_name --query "cluster.identity.oidc.issuer" --output text
```

Output:

```
https://oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E
```

To use IAM roles for service accounts in your cluster, you must create an OIDC identity provider in the IAM console\.

------
#### [ eksctl ]

**To create an IAM OIDC identity provider for your cluster with `eksctl`**

1. Check your `eksctl` version with the following command\. This procedure assumes that you have installed `eksctl` and that your `eksctl` version is at least `0.14.0`\. 

   ```
   eksctl version
   ```

    For more information about installing or upgrading `eksctl`, see [Installing or Upgrading `eksctl`](eksctl.md#installing-eksctl)\.

1. Create your OIDC identity provider for your cluster with the following command\. Substitute *cluster\_name* with your own value\.

   ```
   eksctl utils associate-iam-oidc-provider --cluster cluster_name --approve
   ```

------
#### [ AWS Management Console ]

**To create an IAM OIDC identity provider for your cluster with the AWS Management Console**

1. Retrieve the OIDC issuer URL from the Amazon EKS console description of your cluster or use the following AWS CLI command\.
**Important**  
You must use at least version 1\.18\.10 of the AWS CLI to receive the proper output from this command\. For more information, see [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) in the *AWS Command Line Interface User Guide*\.

   ```
   aws eks describe-cluster --name cluster_name --query "cluster.identity.oidc.issuer" --output text
   ```

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the navigation pane, choose **Identity Providers**, and then choose **Create Provider**\.

1. For **Provider Type**, choose **Choose a provider type**, and then choose **OpenID Connect**\.

1. For **Provider URL**, paste the OIDC issuer URL for your cluster\.

1. For Audience, type `sts.amazonaws.com` and choose **Next Step**\.

1. Verify that the provider information is correct, and then choose **Create** to create your identity provider\.

------

After you have enabled the IAM OIDC identity provider for your cluster, you can create IAM roles to associate with a service account in your cluster\. For more information, see [Creating an IAM Role and Policy for your Service Account](create-service-account-iam-policy-and-role.md)