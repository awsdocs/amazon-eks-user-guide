# Creating or updating a `kubeconfig` file for an Amazon EKS cluster<a name="create-kubeconfig"></a>

In this topic, you create a `kubeconfig` file for your cluster \(or update an existing one\)\.

The `kubectl` command\-line tool uses configuration information in `kubeconfig` files to communicate with the API server of a cluster\. For more information, see [Organizing Cluster Access Using kubeconfig Files](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/) in the Kubernetes documentation\.

Amazon EKS uses the `aws eks get-token` command with `kubectl` for cluster authentication\. By default, the AWS CLI uses the same credentials that are returned with the following command:

```
aws sts get-caller-identity
```

**Prerequisites**
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\.
+ The `kubectl` command line tool is installed on your device or AWS CloudShell\. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster\. For example, if your cluster version is `1.28`, you can use `kubectl` version `1.27`, `1.28`, or `1.29` with it\. To install or upgrade `kubectl`, see [Installing or updating `kubectl`](install-kubectl.md)\.
+ Version `2.12.3` or later or version `1.27.160` or later of the AWS Command Line Interface \(AWS CLI\) installed and configured on your device or AWS CloudShell\. To check your current version, use `aws --version | cut -d / -f2 | cut -d ' ' -f1`\. Package managers such `yum`, `apt-get`, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI\. To install the latest version, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with aws configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the *AWS Command Line Interface User Guide*\. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version\. To update it, see [Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the *AWS CloudShell User Guide*\.
+ An IAM user or role with permission to use the `eks:DescribeCluster` API action for the cluster that you specify\. For more information, see [Amazon EKS identity\-based policy examples](security_iam_id-based-policy-examples.md)\. If you use an identity from your own OpenID Connect provider to access your cluster, then see [Using `kubectl`](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#using-kubectl) in the Kubernetes documentation to create or update your `kube config` file\.

## Create `kubeconfig` file automatically<a name="create-kubeconfig-automatically"></a>

**Prerequisites**
+ Version `2.12.3` or later or version `1.27.160` or later of the AWS Command Line Interface \(AWS CLI\) installed and configured on your device or AWS CloudShell\. To check your current version, use `aws --version | cut -d / -f2 | cut -d ' ' -f1`\. Package managers such `yum`, `apt-get`, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI\. To install the latest version, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with aws configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the *AWS Command Line Interface User Guide*\. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version\. To update it, see [Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the *AWS CloudShell User Guide*\. 
+ Permission to use the `eks:DescribeCluster` API action for the cluster that you specify\. For more information, see [Amazon EKS identity\-based policy examples](security_iam_id-based-policy-examples.md)\.

**To create your `kubeconfig` file with the AWS CLI**

1. Create or update a `kubeconfig` file for your cluster\. Replace *region\-code* with the AWS Region that your cluster is in and replace *my\-cluster* with the name of your cluster\.

   ```
   aws eks update-kubeconfig --region region-code --name my-cluster
   ```

   By default, the resulting configuration file is created at the default `kubeconfig` path \(`.kube`\) in your home directory or merged with an existing `config` file at that location\. You can specify another path with the **\-\-kubeconfig** option\.

   You can specify an IAM role ARN with the **\-\-role\-arn** option to use for authentication when you issue `kubectl` commands\. Otherwise, the [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) in your default AWS CLI or SDK credential chain is used\. You can view your default AWS CLI or SDK identity by running the `aws sts get-caller-identity` command\.

   For all available options, run the `aws eks update-kubeconfig help` command or see [https://docs.aws.amazon.com/cli/latest/reference/eks/update-kubeconfig.html](https://docs.aws.amazon.com/cli/latest/reference/eks/update-kubeconfig.html) in the *AWS CLI Command Reference*\.

1. Test your configuration\.

   ```
   kubectl get svc
   ```

   An example output is as follows\.

   ```
   NAME             TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
   svc/kubernetes   ClusterIP   10.100.0.1   <none>        443/TCP   1m
   ```

   If you receive any authorization or resource type errors, see [Unauthorized or access denied \(`kubectl`\)](troubleshooting.md#unauthorized) in the troubleshooting topic\.