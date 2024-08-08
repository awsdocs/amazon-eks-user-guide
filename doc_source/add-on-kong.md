# Kong<a name="add-on-kong"></a>

The add\-on name is `kong_konnect-ri` and the namespace is `kong`\. Kong publishes the add\-on\.

For information about the add\-on, see [Installing the Kong Gateway EKS Add\-on](https://kong.github.io/aws-marketplace-addon-kong-gateway/) in the Kong documentation\.

If your cluster is version `1.23` or later, you must have the [Store Kuberentes volumes with Amazon EBS](ebs-csi.md) installed on your cluster\. otherwise you will receive an error\.

## Service account name<a name="add-on-kong-service-account-name"></a>

A service account isn't used with this add\-on\.

## AWS managed IAM policy<a name="add-on-kong-managed-policy"></a>

A managed policy isn't used with this add\-on\.

## Custom IAM permissions<a name="add-on-kong-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.