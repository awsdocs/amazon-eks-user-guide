# Create an IAM role<a name="adot-iam"></a>

Each cluster where you [install AWS Distro for OpenTelemetry \(ADOT\)](adot-manage.md#adot-install) must have this role to grant your AWS service account permissions\. Follow these steps to create and associate your IAM role to your Amazon EKS service account using [ IRSA](iam-roles-for-service-accounts.md):

1.  [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.

1. Create your service account and IAM role\. Note the following flags included in this command: 
   + For the `--name` flag, specify the name of the service account you want to create\. In this example, it is `adot-collector`\.
   + For the `--namespace` flag, specify the namespace your service account will reside in; for this example you will use the `default` namespace\.
   + For the `--cluster` flag, specify the name of your cluster\.
   + Use the `--attach-policy-arn` parameter to specify the managed IAM policy for the integration you are using to the role\. For example, if you are using ADOT Collector to send metric data to CloudWatch, you specify the `CloudWatchAgentServerPolicy` managed policy\.
   + The `--override-existing-serviceaccounts` flag is for a service account already created in the cluster without an IAM role\. You can exclude this if the service account does not have an IAM role\. 

     Enter the following command considering the notes above:

```
eksctl create iamserviceaccount \
    --name adot-collector \
    --namespace default \
    --cluster my-cluster \
    --attach-policy-arn arn:aws:iam::aws:policy/AmazonPrometheusRemoteWriteAccess \
    --attach-policy-arn arn:aws:iam::aws:policy/AWSXrayWriteOnlyAccess \
    --attach-policy-arn arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy \
    --approve \
    --override-existing-serviceaccounts
```

In the following collector configurations, the `serviceAccount: adot-collector` field to the configuration has been added to use IRSA\.