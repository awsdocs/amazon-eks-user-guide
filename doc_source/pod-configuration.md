# Configure Pods to use a Kubernetes service account<a name="pod-configuration"></a>

If a Pod needs to access AWS services, then you must configure it to use a Kubernetes service account\. The service account must be associated to an AWS Identity and Access Management \(IAM\) role that has permissions to access the AWS services\.<a name="pod-configuration-prerequisites"></a>

**Prerequisites**
+ An existing cluster\. If you don't have one, you can create one using one of the [Getting started with Amazon EKS](getting-started.md) guides\.
+ An existing IAM OpenID Connect \(OIDC\) provider for your cluster\. To learn if you already have one or how to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ An existing Kubernetes service account that's associated with an IAM role\. The service account must be annotated with the Amazon Resource Name \(ARN\) of the IAM role\. The role must have an associated IAM policy that contains the permissions that you want your Pods to have to use AWS services\. For more information about how to create the service account and role, and configure them, see [Configure a Kubernetes service account to assume an IAM role](associate-service-account-role.md)\.
+ Version `2.12.3` or later or version `1.27.160` or later of the AWS Command Line Interface \(AWS CLI\) installed and configured on your device or AWS CloudShell\. To check your current version, use `aws --version | cut -d / -f2 | cut -d ' ' -f1`\. Package managers such `yum`, `apt-get`, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI\. To install the latest version, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with aws configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the *AWS Command Line Interface User Guide*\. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version\. To update it, see [Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the *AWS CloudShell User Guide*\.
+ The `kubectl` command line tool is installed on your device or AWS CloudShell\. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster\. For example, if your cluster version is `1.28`, you can use `kubectl` version `1.27`, `1.28`, or `1.29` with it\. To install or upgrade `kubectl`, see [Installing or updating `kubectl`](install-kubectl.md)\.
+ An existing `kubectl` `config` file that contains your cluster configuration\. To create a `kubectl` `config` file, see [Creating or updating a `kubeconfig` file for an Amazon EKS cluster](create-kubeconfig.md)\.

**To configure a Pod to use a service account**

1. Use the following command to create a deployment manifest that you can deploy a Pod to confirm configuration with\. Replace the `example values` with your own values\.

   ```
   cat >my-deployment.yaml <<EOF
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: my-app
   spec:
     selector:
       matchLabels:
         app: my-app
     template:
       metadata:
         labels:
           app: my-app
       spec:
         serviceAccountName: my-service-account
         containers:
         - name: my-app
           image: public.ecr.aws/nginx/nginx:X.XX
   EOF
   ```

1. Deploy the manifest to your cluster\.

   ```
   kubectl apply -f my-deployment.yaml
   ```

1. Confirm that the required environment variables exist for your Pod\.

   1. View the Pods that were deployed with the deployment in the previous step\.

      ```
      kubectl get pods | grep my-app
      ```

      An example output is as follows\.

      ```
      my-app-6f4dfff6cb-76cv9   1/1     Running   0          3m28s
      ```

   1. View the ARN of the IAM role that the Pod is using\.

      ```
      kubectl describe pod my-app-6f4dfff6cb-76cv9 | grep AWS_ROLE_ARN:
      ```

      An example output is as follows\.

      ```
      AWS_ROLE_ARN:                 arn:aws:iam::111122223333:role/my-role
      ```

      The role ARN must match the role ARN that you annotated the existing service account with\. For more about annotating the service account, see [Configure a Kubernetes service account to assume an IAM role](associate-service-account-role.md)\.

   1. Confirm that the Pod has a web identity token file mount\.

      ```
      kubectl describe pod my-app-6f4dfff6cb-76cv9 | grep AWS_WEB_IDENTITY_TOKEN_FILE:
      ```

      An example output is as follows\.

      ```
      AWS_WEB_IDENTITY_TOKEN_FILE:  /var/run/secrets/eks.amazonaws.com/serviceaccount/token
      ```

      The `kubelet` requests and stores the token on behalf of the Pod\. By default, the `kubelet` refreshes the token if the token is older than 80 percent of its total time to live or older than 24 hours\. You can modify the expiration duration for any account other than the default service account by using the settings in your Pod spec\. For more information, see [Service Account Token Volume Projection](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#service-account-token-volume-projection) in the Kubernetes documentation\.

      The [Amazon EKS Pod Identity Webhook](https://github.com/aws/amazon-eks-pod-identity-webhook#amazon-eks-pod-identity-webhook) on the cluster watches for Pods that use a service account with the following annotation:

      ```
      eks.amazonaws.com/role-arn: arn:aws:iam::111122223333:role/my-role
      ```

      The webhook applies the previous environment variables to those Pods\. Your cluster doesn't need to use the webhook to configure the environment variables and token file mounts\. You can manually configure Pods to have these environment variables\. The [supported versions of the AWS SDK](iam-roles-for-service-accounts-minimum-sdk.md) look for these environment variables first in the credential chain provider\. The role credentials are used for Pods that meet this criteria\.

1. Confirm that your Pods can interact with the AWS services using the permissions that you assigned in the IAM policy attached to your role\.
**Note**  
When a Pod uses AWS credentials from an IAM role that's associated with a service account, the AWS CLI or other SDKs in the containers for that Pod use the credentials that are provided by that role\. If you don't restrict access to the credentials that are provided to the [Amazon EKS node IAM role](create-node-role.md), the Pod still has access to these credentials\. For more information, see [Restrict access to the instance profile assigned to the worker node](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node)\.

   If your Pods can't interact with the services as you expected, complete the following steps to confirm that everything is properly configured\.

   1. Confirm that your Pods use an AWS SDK version that supports assuming an IAM role through an OpenID Connect web identity token file\. For more information, see [Using a supported AWS SDK](iam-roles-for-service-accounts-minimum-sdk.md)\.

   1. Confirm that the deployment is using the service account\.

      ```
      kubectl describe deployment my-app | grep "Service Account"
      ```

      An example output is as follows\.

      ```
      Service Account:  my-service-account
      ```

   1. If your Pods still can't access services, review the [steps](associate-service-account-role.md#irsa-confirm-role-configuration) that are described in [Configure a Kubernetes service account to assume an IAM role](associate-service-account-role.md) to confirm that your role and service account are configured properly\.