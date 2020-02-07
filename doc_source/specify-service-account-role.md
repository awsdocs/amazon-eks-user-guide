# Specifying an IAM Role for your Service Account<a name="specify-service-account-role"></a>

In Kubernetes, you define the IAM role to associate with a service account in your cluster by adding the following annotation to the service account\.

**Note**  
If you created an IAM role to use with your service account using `eksctl`, this has already been done for you with the service account that you specified when creating the role\.

```
apiVersion: v1
kind: ServiceAccount
metadata:
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::AWS_ACCOUNT_ID:role/IAM_ROLE_NAME
```

**To patch a service account to use with IAM roles**

1. Use the following command to annotate your service account with the ARN of the IAM role that you want to use with your service account\. Be sure to substitute your own values for the *alternate\-colored* example values to use with your pods\.

   ```
   kubectl annotate serviceaccount -n SERVICE_ACCOUNT_NAMESPACE SERVICE_ACCOUNT_NAME \
   eks.amazonaws.com/role-arn=arn:aws:iam::AWS_ACCOUNT_ID:role/IAM_ROLE_NAME
   ```

1. Delete and re\-create any existing pods that are associated with the service account to apply the credential environment variables\. The mutating web hook does not apply them to pods that are already running\. The following command deletes the existing the `aws-node` DaemonSet pods and deploys them with the service account annotation\. You can modify the namespace, deployment type, and label to update your specific pods\.

   ```
   kubectl delete pods -n kube-system -l k8s-app=aws-node
   ```

1. Confirm that the pods all restarted\.

   ```
   kubectl get pods -n kube-system  -l k8s-app=aws-node
   ```

1. Describe one of the pods and verify that the `AWS_WEB_IDENTITY_TOKEN_FILE` and `AWS_ROLE_ARN` environment variables exist\.

   ```
   kubectl exec -n kube-system aws-node-9rgzw env | grep AWS
   ```

   Output:

   ```
   AWS_VPC_K8S_CNI_LOGLEVEL=DEBUG
   AWS_ROLE_ARN=arn:aws:iam::AWS_ACCOUNT_ID:role/IAM_ROLE_NAME
   AWS_WEB_IDENTITY_TOKEN_FILE=/var/run/secrets/eks.amazonaws.com/serviceaccount/token
   ```

   The IAM role was created by `eksctl` when you created the Kubernetes service account in a previous step\.