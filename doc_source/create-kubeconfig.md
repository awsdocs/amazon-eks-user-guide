# Create a `kubeconfig` for Amazon EKS<a name="create-kubeconfig"></a>

In this section, you create a `kubeconfig` file for your cluster \(or update an existing one\)\.

This section offers two procedures to create or update your kubeconfig\. You can quickly create or update a kubeconfig with the AWS CLI `update-kubeconfig` command automatically by using the AWS CLI, or you can create a kubeconfig manually using the AWS CLI or the `aws-iam-authenticator`\.

Amazon EKS uses the `aws eks get-token` command, available in version 1\.16\.156 or later of the AWS CLI or the [AWS IAM Authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator) with `kubectl` for cluster authentication\. If you have installed the AWS CLI on your system, then by default the AWS IAM Authenticator for Kubernetes will use the same credentials that are returned with the following command:

```
aws sts get-caller-identity
```

For more information, see [Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) in the *AWS Command Line Interface User Guide*\.

## Create `kubeconfig` automatically<a name="create-kubeconfig-automatically"></a>

**To create your `kubeconfig` file with the AWS CLI**

1. Ensure that you have version 1\.16\.156 or later of the AWS CLI installed\. To install or upgrade the AWS CLI, see [Installing the AWS Command Line Interface](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) in the *AWS Command Line Interface User Guide*\.
**Note**  
Your system's Python version must be 2\.7\.9 or later\. Otherwise, you receive `hostname doesn't match` errors with AWS CLI calls to Amazon EKS\.

   You can check your AWS CLI version with the following command:

   ```
   aws --version
   ```
**Important**  
Package managers such  `yum`  ,  `apt-get`  , or Homebrew for macOS are often behind several versions of the AWS CLI\. To ensure that you have the latest version, see [Installing the AWS Command Line Interface](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) in the *AWS Command Line Interface User Guide*\.

1. Use the AWS CLI  `update-kubeconfig`  command to create or update your kubeconfig for your cluster\.
   + By default, the resulting configuration file is created at the default kubeconfig path \(`.kube/config`\) in your home directory or merged with an existing kubeconfig at that location\. You can specify another path with the `--kubeconfig` option\.
   + You can specify an IAM role ARN with the `--role-arn` option to use for authentication when you issue  `kubectl`  commands\. Otherwise, the IAM entity in your default AWS CLI or SDK credential chain is used\. You can view your default AWS CLI or SDK identity by running the  `aws sts get-caller-identity`  command\.
   + For more information, see the help page with the  `aws eks update-kubeconfig help`  command or see [update\-kubeconfig](https://docs.aws.amazon.com/cli/latest/reference/eks/update-kubeconfig.html) in the *AWS CLI Command Reference*\.
**Note**  
To run the following command, you must have permission to the use the `eks:DescribeCluster` API action with the cluster that you specify\. For more information, see [Amazon EKS identity\-based policy examples](security_iam_id-based-policy-examples.md)\.

   ```
   aws eks --region <region-code> update-kubeconfig --name <cluster_name>
   ```

1. Test your configuration\.

   ```
   kubectl get svc
   ```
**Note**  
If you receive any authorization or resource type errors, see [Unauthorized or access denied \(`kubectl`\)](troubleshooting.md#unauthorized) in the troubleshooting section\.

   Output:

   ```
   NAME             TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
   svc/kubernetes   ClusterIP   10.100.0.1   <none>        443/TCP   1m
   ```

## Create `kubeconfig` manually<a name="create-kubeconfig-manually"></a>

**To create your `kubeconfig` file manually**

1. Create the default `~/.kube` directory if it does not already exist\.

   ```
   mkdir -p ~/.kube
   ```

1. Open your favorite text editor and copy one of the `kubeconfig` code blocks below into it, depending on your preferred client token method\.
   + To use the AWS CLI  `aws eks get-token`  command \(requires version 1\.16\.156 or later of the AWS CLI\):

     ```
     apiVersion: v1
     clusters:
     - cluster:
         server: <endpoint-url>
         certificate-authority-data: <base64-encoded-ca-cert>
       name: kubernetes
     contexts:
     - context:
         cluster: kubernetes
         user: aws
       name: aws
     current-context: aws
     kind: Config
     preferences: {}
     users:
     - name: aws
       user:
         exec:
           apiVersion: client.authentication.k8s.io/v1alpha1
           command: aws
           args:
             - "eks"
             - "get-token"
             - "--cluster-name"
             - "<cluster-name>"
             # - "--role"
             # - "<role-arn>"
           # env:
             # - name: AWS_PROFILE
             #   value: "<aws-profile>"
     ```
   + To use the [AWS IAM authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator):

     ```
     apiVersion: v1
     clusters:
     - cluster:
         server: <endpoint-url>
         certificate-authority-data: <base64-encoded-ca-cert>
       name: kubernetes
     contexts:
     - context:
         cluster: kubernetes
         user: aws
       name: aws
     current-context: aws
     kind: Config
     preferences: {}
     users:
     - name: aws
       user:
         exec:
           apiVersion: client.authentication.k8s.io/v1alpha1
           command: aws-iam-authenticator
           args:
             - "token"
             - "-i"
             - "<cluster-name>"
             # - "-r"
             # - "<role-arn>"
           # env:
             # - name: AWS_PROFILE
             #   value: "<aws-profile>"
     ```

1. Replace the `<endpoint-url>` with the endpoint URL that was created for your cluster\.

1. Replace the `<base64-encoded-ca-cert>` with the `certificateAuthority.data` that was created for your cluster\.

1. Replace the `<cluster-name>` with your cluster name\.

1. \(Optional\) To assume an IAM role to perform cluster operations instead of the default AWS credential provider chain, uncomment the `-r` or `--role` and `<role-arn>` lines and substitute an IAM role ARN to use with your user\.

1. \(Optional\) To always use a specific named AWS credential profile \(instead of the default AWS credential provider chain\), uncomment the `env` lines and substitute `<aws-profile>` with the profile name to use\.

1. Save the file to the default  `kubectl`  folder, with your cluster name in the file name\. For example, if your cluster name is `<devel>`, save the file to `~/.kube/config-<devel>`\.

1. Add that file path to your `KUBECONFIG` environment variable so that  `kubectl`  knows where to look for your cluster configuration\.
   + For Bash shells on macOS or Linux:

     ```
     export KUBECONFIG=$KUBECONFIG:~/.kube/config-<devel>
     ```
   + For PowerShell on Windows:

     ```
     $ENV:KUBECONFIG="{0};{1}" -f  $ENV:KUBECONFIG, "$ENV:userprofile\.kube\config-<devel>"
     ```

1. \(Optional\) Add the configuration to your shell initialization file so that it is configured when you open a shell\.
   + For Bash shells on macOS:

     ```
     echo 'export KUBECONFIG=$KUBECONFIG:~/.kube/config-<devel>' >> ~/.bash_profile
     ```
   + For Bash shells on Linux:

     ```
     echo 'export KUBECONFIG=$KUBECONFIG:~/.kube/config-<devel>' >> ~/.bashrc
     ```
   + For PowerShell on Windows:

     ```
     [System.Environment]::SetEnvironmentVariable('KUBECONFIG', $ENV:KUBECONFIG, 'Machine')
     ```

1. Test your configuration\.

   ```
   kubectl get svc
   ```
**Note**  
If you receive any authorization or resource type errors, see [Unauthorized or access denied \(`kubectl`\)](troubleshooting.md#unauthorized) in the troubleshooting section\.

   Output:

   ```
   NAME             TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
   svc/kubernetes   ClusterIP   10.100.0.1   <none>        443/TCP   1m
   ```