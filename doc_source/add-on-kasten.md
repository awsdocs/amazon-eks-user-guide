# Kasten<a name="add-on-kasten"></a>

 The add\-on name is `kasten_k10` and the namespace is `kasten-io`\. Kasten by Veeam publishes the add\-on\.

For information about the add\-on, see [Installing K10 on AWS using Amazon EKS Add\-on](https://docs.kasten.io/latest/install/aws-eks-addon/aws-eks-addon.html) in the Kasten documentation\.

 If your Amazon EKS cluster is version Kubernetes `1.23` or later, you must have the Amazon EBS CSI driver installed on your cluster with a default `StorageClass`\.

## Service account name<a name="add-on-kasten-service-account-name"></a>

The service account name is `k10-k10`\.

## AWS managed IAM policy<a name="add-on-kasten-managed-policy"></a>

The managed policy is AWSLicenseManagerConsumptionPolicy\. For more information, see [AWSLicenseManagerConsumptionPolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AWSLicenseManagerConsumptionPolicy.html) in the AWS Managed Policy Reference Guide\.\.

## Command to create required IAM role<a name="add-on-kasten-iam-command"></a>

The following command requires that you have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\. Replace `my-cluster` with the name of your cluster and `my-kasten-role` with the name for your role\. This command requires that you have [https://eksctl.io](https://eksctl.io) installed on your device\. If you need to use a different tool to create the role and annotate the Kubernetes service account, see [Assign IAM roles to Kubernetes service accounts](associate-service-account-role.md)\.

```
eksctl create iamserviceaccount --name k10-k10 --namespace kasten-io --cluster my-cluster --role-name my-kasten-role \
    --role-only --attach-policy-arn arn:aws:iam::aws:policy/service-role/AWSLicenseManagerConsumptionPolicy --approve
```

## Custom permissions<a name="add-on-kasten-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.