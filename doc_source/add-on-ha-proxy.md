# HA Proxy<a name="add-on-ha-proxy"></a>

The name is `haproxy-technologies_kubernetes-ingress-ee` and the namespace is `haproxy-controller`\. HA Proxy publishes the add\-on\.

For information about the add\-on, see [Amazon EKS\-intergration](https://hub.datree.io/integrations/eks-integration) in the Datree documentation\.

## Service account name<a name="add-on-ha-proxy-service-account-name"></a>

The service account name is `customer defined`\.

## AWS managed IAM policy<a name="add-on-ha-proxy-managed-policy"></a>

The managed policy is AWSLicenseManagerConsumptionPolicy\.For more information, see [AWSLicenseManagerConsumptionPolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AWSLicenseManagerConsumptionPolicy.html) in the AWS Managed Policy Reference Guide\.\.

## Command to create required IAM role<a name="add-on-ha-proxy-iam-command"></a>

The following command requires that you have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\. Replace `my-cluster` with the name of your cluster and `my-haproxy-role` with the name for your role\. This command requires that you have [https://eksctl.io](https://eksctl.io) installed on your device\. If you need to use a different tool to create the role and annotate the Kubernetes service account, see [Assign IAM roles to Kubernetes service accounts](associate-service-account-role.md)\.

```
eksctl create iamserviceaccount --name service-account-name  --namespace haproxy-controller --cluster my-cluster --role-name my-haproxy-role \
    --role-only --attach-policy-arn arn:aws:iam::aws:policy/service-role/AWSLicenseManagerConsumptionPolicy --approve
```

## Custom permissions<a name="add-on-ha-proxy-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.