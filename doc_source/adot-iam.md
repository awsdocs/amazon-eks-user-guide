# Create an IAM role<a name="adot-iam"></a>

Each cluster where you [install AWS Distro for OpenTelemetry \(ADOT\)](adot-manage.md#adot-install) must have this role to grant your AWS service account permissions\. Follow these steps to create and associate your IAM role to your Amazon EKS service account using [ IRSA](iam-roles-for-service-accounts.md):

1.  [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\. 

1. Create your service account and IAM role\. Note the following flags included in this command: 
   + For the `--name` flag, add the name of the service account you want to create\. In this example, it is `adot-collector` \.
   + For the `--namespace` flag, use the namespace your service account will reside in; for our example we will use the `default` namespace\.
   + For the `--cluster` flag, use the name of your cluster\.
   + The three `--attach-policy-arn` values are the policies to be attached to the respective services\. You can add at least one or all of these services and [configure the ADOT Collector](deploy-collector.md) to support it/them\.
   +  The `--override-existing-serviceaccounts` flag is for a service account already created in the cluster without an IAM Role\. You can exclude this if that is not the case\. 

     Enter the following command considering the notes above:

```
eksctl create iamserviceaccount \
    --name adot-collector \
    --namespace default \
    --cluster cluster_name \
    --attach-policy-arn arn:aws:iam::111122223333:policy/AmazonPrometheusRemoteWriteAccess \
    --attach-policy-arn arn:aws:iam::111122223333:policy/AWSXrayWriteOnlyAccess \
    --attach-policy-arn arn:aws:iam::111122223333:policy/CloudWatchAgentServerPolicy \
    --approve \
    --override-existing-serviceaccounts
```

We will see in our collector configurations in the following sections that we add the `serviceAccount: adot-collector` field to our configuration to use IRSA\.