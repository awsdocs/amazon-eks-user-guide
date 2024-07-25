# Calyptia<a name="add-on-calyptia"></a>

The add\-on name is `calyptia_fluent-bit` and the namespace is `calytia-fluentbit`\. Calyptia publishes the add\-on\.

For information about the add\-on, see [Getting Started with Calyptia Core Agent](https://docs.akuity.io/tutorials/eks-addon-agent-install/) on the Calyptia documentation website\.

## Service account name<a name="add-on-calyptia-service-account-name"></a>

The service account name is `clyptia-fluentbit`\.

## AWS managed IAM policy<a name="add-on-calyptia-managed-policy"></a>

This add\-on uses the `AWSMarketplaceMeteringRegisterUsage` managed policy\. For more information, see [AWSMarketplaceMeteringRegisterUsage](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AWSMarketplaceMeteringRegisterUsage.html) in the AWS Managed Policy Reference Guide\.

## Command to create required IAM role<a name="add-on-calyptia-custom-permissions"></a>

The following command requires that you have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\. Replace `my-cluster` with the name of your cluster and `my-calyptia-role` with the name for your role\. This command requires that you have [https://eksctl.io](https://eksctl.io) installed on your device\. If you need to use a different tool to create the role and annotate the Kubernetes service account, see [Assign IAM roles to Kubernetes service accounts](associate-service-account-role.md)\.

```
eksctl create iamserviceaccount --name service-account-name  --namespace calyptia-fluentbit --cluster my-cluster --role-name my-calyptia-role \
    --role-only --attach-policy-arn arn:aws:iam::aws:policy/AWSMarketplaceMeteringRegisterUsage --approve
```