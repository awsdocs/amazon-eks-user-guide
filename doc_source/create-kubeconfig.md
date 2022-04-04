# Create a `kubeconfig` for Amazon EKS<a name="create-kubeconfig"></a>

In this section, you create a `kubeconfig` file for your cluster \(or update an existing one\)\.

This section offers two procedures to create or update your *kubeconfig* file\. You can quickly create or update a `kubeconfig` file with the AWS CLI `update-kubeconfig` command automatically by using the AWS CLI, or you can create a `kubeconfig` file manually using the AWS CLI or the `aws-iam-authenticator`\.

Amazon EKS uses the `aws eks get-token` command, available in version 1\.16\.156 or later of the AWS CLI or the [AWS IAM Authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator) with `kubectl` for cluster authentication\. If you have installed the AWS CLI on your system, then by default the AWS IAM Authenticator for Kubernetes uses the same credentials that are returned with the following command:

```
aws sts get-caller-identity
```

For more information, see [Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) in the *AWS Command Line Interface User Guide*\.

## Create `kubeconfig` file automatically<a name="create-kubeconfig-automatically"></a>

**To create your `kubeconfig` file with the AWS CLI**

1. Ensure that you have version 1\.16\.156 or later of the AWS CLI installed\. To install or upgrade the AWS CLI, see [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) in the *AWS Command Line Interface User Guide*\.
**Note**  
Your system's Python version must be 2\.7\.9 or later\. Otherwise, you receive `hostname doesn't match` errors with AWS CLI calls to Amazon EKS\.

   You can check your AWS CLI version with the following command:

   ```
   aws --version
   ```
**Important**  
Package managers such `yum`, `apt-get`, or Homebrew for macOS are often behind several versions of the AWS CLI\. To ensure that you have the latest version, see [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) in the *AWS Command Line Interface User Guide*\.

1. Create or update a `kubeconfig` file for your cluster\. Replace the *example values* with your own\.
   + By default, the resulting configuration file is created at the default `kubeconfig` path \(`.kube/config`\) in your home directory or merged with an existing `kubeconfig` file at that location\. You can specify another path with the **\-\-kubeconfig** option\.
   + You can specify an IAM role ARN with the **\-\-role\-arn** option to use for authentication when you issue `kubectl` commands\. Otherwise, the IAM entity in your default AWS CLI or SDK credential chain is used\. You can view your default AWS CLI or SDK identity by running the `aws sts get-caller-identity` command\.
   + For more information, see the help page with the `aws eks update-kubeconfig help` command or see [update\-kubeconfig](https://docs.aws.amazon.com/cli/latest/reference/eks/update-kubeconfig.html) in the *AWS CLI Command Reference*\.
**Note**  
To run the following command, you must have permission to use the `eks:DescribeCluster` API action with the cluster that you specify\. For more information, see [Amazon EKS identity\-based policy examples](security_iam_id-based-policy-examples.md)\.

   ```
   aws eks update-kubeconfig --region region-code --name cluster-name
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

1. Retrieve the endpoint for your cluster\. Replace the *example values* with the values for your cluster\.

   ```
   aws eks describe-cluster \
       --region region-code \
       --name my-cluster \
       --query "cluster.endpoint" \
       --output text
   ```

   Example output

   ```
   https://E0EED553387FD639757D97A76EXAMPLE.gr7.region-code.eks.amazonaws.com
   ```

1. Retrieve the Base64\-encoded certificate data required to communicate with your cluster\.

   ```
   aws eks describe-cluster \
       --region region-code \
       --name my-cluster \
       --query "cluster.certificateAuthority.data" \
       --output text
   ```

   The output is a very long string\.

1. Create the default `~/.kube` directory if it does not already exist\.

   ```
   mkdir -p ~/.kube
   ```

1. Copy the contents from one of the following code blocks \(depending on your preferred client token method\) with your text editor\.
   + To use the AWS CLI `aws eks get-token` command \(requires version 1\.16\.156 or later of the AWS CLI\)\.

     ```
     apiVersion: v1
     clusters:
     - cluster:
         server: endpoint
         certificate-authority-data: certificate-data
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
             - "cluster-name"
             # - "--role-arn"
             # - "role-arn"
           # env:
             # - name: AWS_PROFILE
             #   value: "aws-profile"
     ```
   + To use the [AWS IAM authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator):

     ```
     apiVersion: v1
     clusters:
     - cluster:
         server: endpoint
         certificate-authority-data: certificate-data
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
             - "cluster-name"
             # - "-r"
             # - "role-arn"
           # env:
             # - name: AWS_PROFILE
             #   value: "aws-profile"
     ```

1. Replace *endpoint* with the endpoint that you obtained in a previous step\.

1. Replace *certificate\-data* with the Base64\-encoded certificate data that you obtained in a previous step\.

1. Replace *cluster\-name* with your cluster name\.

1. \(Optional\) To assume an IAM role to perform cluster operations instead of the default AWS credential provider chain, uncomment the `-r` and `role-arn` lines and replace them with an IAM role ARN to use with your user\.

1. Save the file to the default `kubectl` folder, with your cluster name in the file name\. For example, if your cluster name is *my\-cluster*, save the file to `~/.kube/config-my-cluster`\.

1. Add that file path to your `KUBECONFIG` environment variable so that `kubectl` knows where to look for your cluster configuration\.
   + For Bash shells on macOS or Linux:

     ```
     export KUBECONFIG=$KUBECONFIG:~/.kube/config-my-cluster
     ```
   + For PowerShell on Windows:

     ```
     $ENV:KUBECONFIG="{0};{1}" -f  $ENV:KUBECONFIG, "$ENV:userprofile\.kube\config-my-cluster"
     ```

1. \(Optional\) Add the configuration to your shell initialization file so that it is configured when you open a shell\.
   + For Bash shells on macOS:

     ```
     echo 'export KUBECONFIG=$KUBECONFIG:~/.kube/config-my-cluster' >> ~/.bash_profile
     ```
   + For Bash shells on Linux:

     ```
     echo 'export KUBECONFIG=$KUBECONFIG:~/.kube/config-my-cluster' >> ~/.bashrc
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