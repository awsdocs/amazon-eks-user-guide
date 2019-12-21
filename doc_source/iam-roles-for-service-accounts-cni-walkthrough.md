# Walkthrough: Amazon VPC CNI Plugin for Kubernetes<a name="iam-roles-for-service-accounts-cni-walkthrough"></a>

The [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) is the networking plugin for pod networking in Amazon EKS clusters\. The CNI plugin is responsible for allocating VPC IP addresses to Kubernetes nodes and configuring the necessary networking for pods on each node\. The plugin requires IAM permissions, provided by the AWS managed policy `[AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor)`, to make calls to AWS APIs on your behalf\. By default, this policy is attached to your worker node IAM role\. However, using this method, all pods on the worker nodes have the same permissions as the CNI plugin\. You can use the IAM roles for service accounts feature to provide the `[AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor)` permissions, and then remove the policy from the worker node IAM role\.

For ease of use, this topic uses `eksctl` to configure IAM roles for service accounts\. However, if you would rather use the AWS Management Console, the AWS CLI, or one of the AWS SDKs, the same basic concepts apply, but you will have to modify the steps to use the procedures in [Enabling IAM Roles for Service Accounts on your Cluster](enable-iam-roles-for-service-accounts.md)

**To configure the CNI plugin to use IAM roles for service accounts**

1. Check your `eksctl` version with the following command\. This procedure assumes that you have installed `eksctl` and that your `eksctl` version is at least `0.11.0`\. 

   ```
   eksctl version
   ```

    For more information about installing or upgrading `eksctl`, see [Installing or Upgrading `eksctl`](eksctl.md#installing-eksctl)\.

1. Create your OIDC identity provider for your cluster with the following command\. Substitute the cluster name with your own value\.

   ```
   eksctl utils associate-iam-oidc-provider --cluster cluster_name --approve
   ```

1. Check the version of your cluster's Amazon VPC CNI Plugin for Kubernetes\. Use the following command to print your cluster's CNI version\.

   ```
   kubectl describe daemonset aws-node --namespace kube-system | grep Image | cut -d "/" -f 2
   ```

   Output:

   ```
   amazon-k8s-cni:1.5.4
   ```

   If your CNI version is earlier than 1\.5\.5, use the following command to upgrade your CNI version to the latest version:

   ```
   kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.5/config/v1.5/aws-k8s-cni.yaml
   ```

1. Create a role for your CNI plugin and annotate the `aws-node` service account with the following command\. Substitute the cluster name with your own value\.

   ```
   eksctl create iamserviceaccount --name aws-node --namespace kube-system \
   --cluster cluster_name --attach-policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy --approve  --override-existing-serviceaccounts
   ```

1. Trigger a roll out of the `aws-node` daemonset to apply the credential environment variables\. The mutating web hook does not apply them to pods that are already running\.

   ```
   kubectl rollout restart -n kube-system daemonset.apps/aws-node
   ```

1. Watch the roll out, and wait for the `DESIRED` count of the deployment matches the `UP-TO-DATE` count\. Press **Ctrl \+ c** to exit\. 

   ```
   kubectl get -n kube-system daemonset.apps/aws-node --watch
   ```

1. List the pods in the `aws-node` daemonset\.

   ```
   kubectl get pods -n kube-system  -l k8s-app=aws-node
   ```

   Output:

   ```
   NAME             READY   STATUS    RESTARTS   AGE
   aws-node-9rgzw   1/1     Running   0          87m
   aws-node-czjxf   1/1     Running   0          86m
   aws-node-lm2r8   1/1     Running   0          86m
   ```

1. Describe one of the pods and verify that the `AWS_WEB_IDENTITY_TOKEN_FILE` and `AWS_ROLE_ARN` environment variables exist\.

   ```
   kubectl exec -n kube-system aws-node-9rgzw env | grep AWS
   ```

   Output:

   ```
   AWS_WEB_IDENTITY_TOKEN_FILE=/var/run/secrets/eks.amazonaws.com/serviceaccount/token
   AWS_VPC_K8S_CNI_LOGLEVEL=DEBUG
   AWS_ROLE_ARN=arn:aws:iam::111122223333:role/eksctl-prod-addon-iamserviceaccount-kube-sys-Role1-13LTY0S1XC7Q9
   ```

1. Remove the `[AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor)` policy from your worker node IAM role\.

   1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

   1. In the left navigation, choose **Roles**, and then search for your node instance role\.

   1. Choose the **Permissions** tab for your node instance role and then choose the **X** to the right of the `[AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor)`\.

   1. Choose **Detach** to finish\.

Now your CNI plugin pods are getting their IAM permissions from their own role, and the instance role no longer can provide those permissions to other pods\.