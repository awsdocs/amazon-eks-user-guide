# Associate an IAM role to a service account<a name="specify-service-account-role"></a>

In Kubernetes, you define the IAM role to associate with a service account in your cluster by adding the following annotation to the service account\.

**Note**  
If you created an IAM role to use with your service account using `eksctl`, this has already been done for you with the service account that you specified when creating the role\.

```
apiVersion: v1
kind: ServiceAccount
metadata:
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::ACCOUNT_ID:role/IAM_ROLE_NAME
```

**Prerequisites**
+ An existing cluster\. If you don't have one, you can create one using one of the [Getting started with Amazon EKS](getting-started.md) guides\.
+ An existing IAM OIDC provider for your cluster\. For more information, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ An existing service account\. If you don't have one, see [Configure Service Accounts for Pods](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/) in the Kubernetes documentation\.
+ An existing IAM role with an attached IAM policy\. If you don't have one, see [Creating an IAM role and policy for your service account](create-service-account-iam-policy-and-role.md)\.

**To annotate a service account with an IAM role**

1. Use the following command to annotate your service account with the ARN of the IAM role that you want to use with your service account\. Be sure to replace the *example values* with your own\.

   ```
   kubectl annotate serviceaccount -n SERVICE_ACCOUNT_NAMESPACE SERVICE_ACCOUNT_NAME \
   eks.amazonaws.com/role-arn=arn:aws:iam::ACCOUNT_ID:role/IAM_ROLE_NAME
   ```
**Note**  
If you don't have an existing service account, then you need to create one\. For more information, see [Configure Service Accounts for Pods](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/) in the Kubernetes documentation\. For the service account to be able to use Kubernetes permissions, you must create a `Role`, or `ClusterRole` and then bind the role to the service account\. For more information, see [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) in the Kubernetes documentation\. When the [AWS VPC CNI plugin](pod-networking.md) is deployed, for example, the deployment manifest creates a service account, cluster role, and cluster role binding\. You can view the[ manifest](https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.10/config/v1.10/aws-k8s-cni.yaml) on GitHub to use as an example\.

1. <a name="sts-regional-endpoint"></a>\(Optional\) Use the following command to add an additional annotation to your service account to use the AWS Security Token Service AWS Regional endpoint, rather than the global endpoint\. AWS recommends using the AWS Regional AWS STS endpoints instead of the global endpoint to reduce latency, build in redundancy, and increase session token validity\. The AWS Security Token Service must be active in the AWS Region where the pod is running and your application should have redundancy built in to pick a different AWS Region in the event of a failure of the service in the AWS Region\. For more information, see [Managing AWS STS in an AWS Region](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_enable-regions.html) in the IAM User Guide\.

   To use this annotation, your cluster and platform version must be at or later than the following Kubernetes and Amazon EKS platform versions\.     
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/specify-service-account-role.html)

   ```
   kubectl annotate serviceaccount -n SERVICE_ACCOUNT_NAMESPACE SERVICE_ACCOUNT_NAME \
   eks.amazonaws.com/sts-regional-endpoints=true
   ```

1. Delete and re\-create any existing pods that are associated with the service account to apply the credential environment variables\. The mutating web hook does not apply them to pods that are already running\. For example, if you added the annotation to the service account used for the Amazon VPC CNI DaemonSet in a previous step, the following command deletes the existing `aws-node` DaemonSet pods and deploys them with the service account annotation\. You can replace *pods*, *kube\-system*, and *\-l k8s\-app=aws\-node* with the information for the pods that you set your annotation for\.

   ```
   kubectl delete pods -n kube-system -l k8s-app=aws-node
   ```

1. Confirm that the pods all restarted\.

   ```
   kubectl get pods -n kube-system  -l k8s-app=aws-node
   ```

1. View the environment variables for one of the pods and verify that the `AWS_WEB_IDENTITY_TOKEN_FILE` and `AWS_ROLE_ARN` environment variables exist\. The following example command returns the variables for one of the pods created by the Amazon VPC CNI DaemonSet\. The pod named *aws\-node\-5v6ws* was returned in the output of the example used in the previous step\.

   ```
   kubectl exec -n kube-system aws-node-5v6ws -- env  | grep AWS
   ```

   Output:

   ```
   ...
   AWS_WEB_IDENTITY_TOKEN_FILE=/var/run/secrets/eks.amazonaws.com/serviceaccount/token
   ...
   AWS_ROLE_ARN=arn:aws:iam::ACCOUNT_ID:role/IAM_ROLE_NAME
   ...
   ```

   If you added the annotation to your service account to use the AWS Security Token Service AWS Regional endpoint, rather than the global endpoint, then verify that the following line is also returned in the previous output\.

   ```
   AWS_STS_REGIONAL_ENDPOINTS=regional
   ```