# Associate an IAM role to a service account<a name="specify-service-account-role"></a>

In Kubernetes, you define the IAM role to associate with a service account in your cluster by adding the following annotation to the service account\.

**Note**  
If you created an IAM role to use with your service account using `eksctl`, this has already been done for you with the service account that you specified when creating the role\.

```
apiVersion: v1
kind: ServiceAccount
metadata:
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::<ACCOUNT_ID>:role/<IAM_ROLE_NAME>
```

**Prerequisites**
+ An existing cluster\. If you don't have one, you can create one using one of the [Getting started with Amazon EKS](getting-started.md) guides\.
+ An existing IAM OIDC provider for your cluster\. For more information, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ An existing service account\. If you don't have one, see [Configure Service Accounts for Pods](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/) in the Kubernetes documentation\.
+ An existing IAM role with an attached IAM policy\. If you don't have one, see [Creating an IAM role and policy for your service account](create-service-account-iam-policy-and-role.md)\.

**To annotate a service account with an IAM role**

1. Use the following command to annotate your service account with the ARN of the IAM role that you want to use with your service account\. Be sure to replace the `<example values>` \(including `<>`\) with your own\.

   ```
   kubectl annotate serviceaccount -n <SERVICE_ACCOUNT_NAMESPACE> <SERVICE_ACCOUNT_NAME> \
   eks.amazonaws.com/role-arn=arn:aws:iam::<ACCOUNT_ID>:role/<IAM_ROLE_NAME>
   ```
**Note**  
If you don't have an existing service account, then you need to create one\. For more information, see [Configure Service Accounts for Pods](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/) in the Kubernetes documentation\. For the service account to be able to use Kubernetes permissions, you must create a `Role`, or `ClusterRole` and then bind the role to the service account\. For more information, see [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) in the Kubernetes documentation\. When the [AWS VPC CNI plugin](pod-networking.md) is deployed, for example, the deployment manifest creates a service account, cluster role, and cluster role binding\. You can view the[ manifest](https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.10/config/v1.10/aws-k8s-cni.yaml) on GitHub to use as an example\.

1. Delete and re\-create any existing pods that are associated with the service account to apply the credential environment variables\. The mutating web hook does not apply them to pods that are already running\. The following command deletes the existing the `aws-node` DaemonSet pods and deploys them with the service account annotation\. You can modify the namespace, deployment type, and label to update your specific pods\.

   ```
   kubectl delete pods -n <kube-system> -l <k8s-app=aws-node>
   ```

1. Confirm that the pods all restarted\.

   ```
   kubectl get pods -n <kube-system>  -l <k8s-app=aws-node>
   ```

1. Describe one of the pods and verify that the `AWS_WEB_IDENTITY_TOKEN_FILE` and `AWS_ROLE_ARN` environment variables exist\.

   ```
   kubectl exec -n kube-system <aws-node-9rgzw> env | grep AWS
   ```

   Output:

   ```
   AWS_VPC_K8S_CNI_LOGLEVEL=DEBUG
   AWS_ROLE_ARN=arn:aws:iam::<ACCOUNT_ID>:role/<IAM_ROLE_NAME>
   AWS_WEB_IDENTITY_TOKEN_FILE=/var/run/secrets/eks.amazonaws.com/serviceaccount/token
   ```