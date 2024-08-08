# Kpow<a name="add-on-kpow"></a>

The add\-on name is `factorhouse_kpow` and the namespace is `factorhouse`\. Factorhouse publishes the add\-on\.

For information about the add\-on, see [AWS Marketplace LM](https://docs.kpow.io/installation/aws-marketplace-lm/) in the Kpow documentation\.

## Service account name<a name="add-on-kpow-service-account-name"></a>

The service account name is `kpow`\.

## AWS managed IAM policy<a name="add-on-kpow-managed-policy"></a>

The managed policy is AWSLicenseManagerConsumptionPolicy\. For more information, see [AWSLicenseManagerConsumptionPolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AWSLicenseManagerConsumptionPolicy.html) in the AWS Managed Policy Reference Guide\.\.

## Command to create required IAM role<a name="add-on-kpow-iam-command"></a>

The following command requires that you have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\. Replace `my-cluster` with the name of your cluster and `my-kpow-role` with the name for your role\. This command requires that you have [https://eksctl.io](https://eksctl.io) installed on your device\. If you need to use a different tool to create the role and annotate the Kubernetes service account, see [Assign IAM roles to Kubernetes service accounts](associate-service-account-role.md)\.

```
eksctl create iamserviceaccount --name kpow --namespace factorhouse --cluster my-cluster --role-name my-kpow-role \
    --role-only --attach-policy-arn arn:aws:iam::aws:policy/service-role/AWSLicenseManagerConsumptionPolicy --approve
```

## Custom permissions<a name="add-on-kpow-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.