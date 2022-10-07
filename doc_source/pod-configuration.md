# Configuring pods to use a Kubernetes service account<a name="pod-configuration"></a>

If a pod needs to access AWS services, then you must configure it to use a Kubernetes service account\. The service account must be associated to an AWS Identity and Access Management \(IAM\) role that has permissions to access the AWS services\.<a name="pod-configuration-prerequisites"></a>

**Prerequisites**
+ An existing cluster\. If you don't have one, you can create one using one of the [Getting started with Amazon EKS](getting-started.md) guides\.
+ An existing IAM OpenID Connect \(OIDC\) provider for your cluster\. To learn if you already have one or how to create one, see [Creating an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ An existing Kubernetes service account that's associated with an IAM role\. The service account must be annotated with the Amazon Resource Name \(ARN\) of the IAM role\. The role must have an associated IAM policy that contains the permissions that you want your pods to have to use AWS services\. For more information about how to create the service account and role, and configure them, see [Configuring a Kubernetes service account to assume an IAM role](associate-service-account-role.md)\.
+ Version `2.8.0` or later or `1.25.87` or later of the AWS CLI installed and configured on your device or AWS CloudShell\. You can check your current version with `aws --version | cut -d / -f2 | cut -d ' ' -f1`\. Package managers such `yum`, `apt-get`, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI\. To install the latest version, see [ Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with `aws configure`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the AWS Command Line Interface User Guide\. The AWS CLI version installed in the AWS CloudShell may also be several versions behind the latest version\. To update it, see [ Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the AWS CloudShell User Guide\.
+ The `kubectl` command line tool is installed on your device or AWS CloudShell\. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster\. For example, if your cluster version is `1.22`, you can use `kubectl` version `1.21`,`1.22`, or `1.23` with it\. To install or upgrade `kubectl`, see [Installing or updating `kubectl`](install-kubectl.md)\.
+ An existing `kubectl` `config` file that contains your cluster configuration\. To create a `kubectl` `config` file, see [Creating or updating a `kubeconfig` file for an Amazon EKS cluster](create-kubeconfig.md)\.

**To configure a pod to use a service account**

1. Use the following command to create a deployment manifest that you can deploy a pod to confirm configuration with\. The pod uses an existing Kubernetes service account\. The service account must be properly configured\. For more information, see [Configuring a Kubernetes service account to assume an IAM role](associate-service-account-role.md)\. Replace the *example values* with your own values\.

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
           image: public.ecr.aws/nginx/nginx:1.21
   EOF
   ```

1. Deploy the manifest to your cluster\.

   ```
   kubectl apply -f my-deployment.yaml
   ```

1. Confirm that the required environment variables exist for your pod\.

   1. View the pods that were deployed with the deployment in the previous step\.

      ```
      kubectl get pods | grep my-app
      ```

      The example output is as follows\.

      ```
      my-app-6f4dfff6cb-76cv9   1/1     Running   0          3m28s
      ```

   1. View the ARN of the IAM role that the pod is using\.

      ```
      kubectl describe pod my-app-6f4dfff6cb-76cv9 | grep AWS_ROLE_ARN:
      ```

      The example output is as follows\.

      ```
      AWS_ROLE_ARN:                 arn:aws:iam::111122223333:role/my-role
      ```

      The role ARN must match the role ARN that you annotated the existing service account with\. For more about annotating the service account, see [Configuring a Kubernetes service account to assume an IAM role](associate-service-account-role.md)\.

   1. Confirm that the pod has a web identity token file mount\.

      ```
      kubectl describe pod my-app-6f4dfff6cb-76cv9 | grep AWS_WEB_IDENTITY_TOKEN_FILE:
      ```

      The example output is as follows\.

      ```
      AWS_WEB_IDENTITY_TOKEN_FILE:  /var/run/secrets/eks.amazonaws.com/serviceaccount/token
      ```

      The `kubelet` requests and stores the token on behalf of the pod\. By default, the `kubelet` refreshes the token if the token is older than 80 percent of its total time to live or older than 24 hours\. You can modify the expiration duration for any account other than the default service account by using the settings in your pod spec\. For more information, see [Service Account Token Volume Projection](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#service-account-token-volume-projection) in the Kubernetes documentation\.

      The [Amazon EKS Pod Identity Webhook](https://github.com/aws/amazon-eks-pod-identity-webhook#amazon-eks-pod-identity-webhook) on the cluster watches for pods that use a service account with the following annotation:

      ```
      eks.amazonaws.com/role-arn: arn:aws:iam::111122223333:role/my-role
      ```

      The webhook applies the previous environment variables to those pods\. Your cluster doesn't need to use the webhook to configure the environment variables and token file mounts\. You can manually configure pods to have these environment variables\. The [supported versions of the AWS SDK](iam-roles-for-service-accounts-minimum-sdk.md) look for these environment variables first in the credential chain provider\. The role credentials are used for pods that meet this criteria\.

1. Confirm that your pods can interact with the AWS services using the permissions that you assigned in the IAM policy attached to your role\.
**Note**  
When a pod uses AWS credentials from an IAM role that's associated with a service account, the AWS CLI or other SDKs in the containers for that pod use the credentials that are provided by that role\. If you don't restrict access to the credentials that are provided to the [Amazon EKS node IAM role](create-node-role.md), the pod still has access to these credentials\. For more information, see [Restrict access to the instance profile assigned to the worker node](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node)\.

   If your pods can't interact with the services as you expected, complete the following steps to confirm that everything is properly configured\.

   1. Confirm that your pods use an AWS SDK version that supports assuming an IAM role through an OpenID Connect web identity token file\. For more information, see [Using a supported AWS SDK](iam-roles-for-service-accounts-minimum-sdk.md)\.

   1. Confirm that the deployment is using the service account\.

      ```
      kubectl describe deployment my-app | grep "Service Account"
      ```

      The example output is as follows\.

      ```
      Service Account:  my-service-account
      ```

   1. If your pods still can't access services, review the [steps](associate-service-account-role.md#irsa-confirm-role-configuration) that are described in [Configuring a Kubernetes service account to assume an IAM role](associate-service-account-role.md) to confirm that your role and service account are configured properly\.