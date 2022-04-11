# Associate an IAM role to a service account<a name="specify-service-account-role"></a>

In Kubernetes, you define the IAM role to associate with a service account in your cluster by adding the following annotation to the service account\.

```
apiVersion: v1
kind: ServiceAccount
metadata:
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::account-id:role/iam-role-name
```

**Note**  
If you [created an IAM role to use with your service account](create-service-account-iam-policy-and-role.md#create-service-account-iam-role) using `eksctl`, `eksctl` annotated the service account that you specified when creating the role\.

**Prerequisites**
+ An existing cluster\. If you don't have one, you can create one using one of the [Getting started with Amazon EKS](getting-started.md) guides\.
+ An existing IAM OIDC provider for your cluster\. For more information, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ An existing Kubernetes service account\. If you don't have one, see [Configure Service Accounts for Pods](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/) in the Kubernetes documentation\.
+ An existing IAM role with an attached IAM policy\. If you don't have one, see [Creating an IAM role and policy for your service account](create-service-account-iam-policy-and-role.md)\.

**To annotate a service account with an IAM role**

1. Use the following command to annotate your service account with the ARN of the IAM role that you want to use with your service account\. Replace *service\-account\-namespace* with the Kubernetes namespace of your service account, *service\-account\-name* with the name of your existing Kubernetes service account\. Replace *account\-id* with your AWS account ID and *iam\-role\-name* with the name of your existing AWS Identity and Access Management \(IAM\) role\.

   ```
   kubectl annotate serviceaccount -n service-account-namespace service-account-name \
   eks.amazonaws.com/role-arn=arn:aws:iam::account-id:role/iam-role-name
   ```
**Note**  
If you don't have an existing service account, then you need to create one\. For more information, see [Configure Service Accounts for Pods](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/) in the Kubernetes documentation\. For the service account to be able to use Kubernetes permissions, you must create a `Role`, or `ClusterRole` and then bind the role to the service account\. For more information, see [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) in the Kubernetes documentation\. When the [AWS VPC CNI plugin](pod-networking.md) is deployed, for example, the deployment manifest creates a service account, cluster role, and cluster role binding\. You can view the[ manifest](https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.10/config/v1.10/aws-k8s-cni.yaml) on GitHub to use as an example\.

1. <a name="sts-regional-endpoint"></a>\(Optional\) Annotate your service account to use the AWS Security Token Service AWS Regional endpoint if your cluster's Kubernetes version is listed in the following table and its platform version is the same or later than the version listed in the table\. If your cluster's Kubernetes version is listed in the following table and you have a platform version that is earlier than the version listed in the following table, then you can't enable your service accounts to use the AWS Security Token Service AWS Regional endpoint\. You must use the global endpoint\. If your cluster is 1\.22 or later, the AWS Regional endpoint is used by default, so you don't need to annotate your Kubernetes service accounts to use it\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/specify-service-account-role.html)

   Add the following annotation to your service accounts\.

   ```
   kubectl annotate serviceaccount -n service-account-namespace service-account-name \
   eks.amazonaws.com/sts-regional-endpoints=true
   ```

   AWS recommends using the AWS Regional AWS STS endpoints instead of the global endpoint to reduce latency, build in redundancy, and increase session token validity\. The AWS Security Token Service must be active in the AWS Region where the pod is running and your application should have redundancy built in to pick a different AWS Region in the event of a failure of the service in the AWS Region\. For more information, see [Managing AWS STS in an AWS Region](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_enable-regions.html) in the IAM User Guide\.

1.  \(Optional\) In Amazon EKS v1\.22 and later, the default AWS STS endpoint used for the IAM Role for Service Account \(IRSA\) to be the regional endpoint instead of the global endpoint\. To use the global STS endpoint, add the following annotation to your service account:

   ```
   kubectl annotate serviceaccount -n service-account-namespace service-account-name \
   eks.amazonaws.com/sts-regional-endpoints=false
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
   AWS_ROLE_ARN=arn:aws:iam::account-id:role/iam-role-name
   ...
   ```

   If your pod is using the AWS Regional endpoint, then the following line is also returned in the previous output\.

   ```
   AWS_STS_REGIONAL_ENDPOINTS=regional
   ```