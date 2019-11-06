# Specifying an IAM Role for your Service Account<a name="specify-service-account-role"></a>

In Kubernetes, you define the IAM role to associate with a service account in your cluster by adding the following annotation to the service account\.

**Note**  
If you created an IAM role to use with your service account using `eksctl`, this has already been done for you with the service account you specified when creating the role\.

```
apiVersion: v1
kind: ServiceAccount
metadata:
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::AWS_ACCOUNT_ID:role/IAM_ROLE_NAME
```

**To patch a service account to use with IAM roles**

1. Use the following command to annotate your service account with the ARN of the IAM role that you want to use with your service account\. Be sure to substitute the service account namespace, name, and IAM role ARN for the service account and IAM role to use with your pods\.

   ```
   kubectl annotate serviceaccount -n SERVICE_ACCOUNT_NAMESPACE SERVICE_ACCOUNT_NAME \
   eks.amazonaws.com/role-arn=arn:aws:iam::AWS_ACCOUNT_ID:role/IAM_ROLE_NAME
   ```

1. Delete and re\-create any existing pods that are associated with the service account to apply the credential environment variables\. The mutating web hook does not apply them to pods that are already running\. The following command triggers a rollout of the `aws-node` DaemonSet\. You can modify the namespace and deployment type to update your specific pods\.

   ```
   kubectl rollout restart -n kube-system daemonset.apps/aws-node
   ```