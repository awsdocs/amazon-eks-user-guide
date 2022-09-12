# Create a `kubeconfig` for Amazon EKS<a name="create-kubeconfig"></a>

In this section, you create a `kubeconfig` file for your cluster \(or update an existing one\)\.

This section offers two procedures to create or update your `kubeconfig` file\. You can quickly create or update a `kubeconfig` file with the AWS CLI `update-kubeconfig` command automatically by using the AWS CLI, or you can create a `kubeconfig` file manually using the AWS CLI or the `aws-iam-authenticator`\.

Amazon EKS uses the `aws eks get-token` command, available in version `1.16.156` or later of the AWS CLI or the [AWS IAM Authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator) with `kubectl` for cluster authentication\. If you have installed the AWS CLI on your system, then by default the AWS IAM Authenticator for Kubernetes uses the same credentials that are returned with the following command:

```
aws sts get-caller-identity
```

For more information, see [Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) in the *AWS Command Line Interface User Guide*\.

## Create `kubeconfig` file automatically<a name="create-kubeconfig-automatically"></a>

**To create your `kubeconfig` file with the AWS CLI**

1. Make sure that you have version  `1.25.71` or `2.7.31` or later installed\. To install or upgrade the AWS CLI, see [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) in the *AWS Command Line Interface User Guide*\.
**Note**  
Your system's Python version must be `2.7.9` or later\. Otherwise, you receive `hostname doesn't match` errors with AWS CLI calls to Amazon EKS\.

   You can check your AWS CLI version with the following command:

   ```
   aws --version
   ```
**Important**  
Package managers such `yum`, `apt-get`, or Homebrew for macOS are often behind several versions of the AWS CLI\. To ensure that you have the latest version, see [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) in the *AWS Command Line Interface User Guide*\.

1. Create or update a `kubeconfig` file for your cluster\. Replace the `example values` with your own\.
   + By default, the resulting configuration file is created at the default `kubeconfig` path \(`.kube`\) in your home directory or merged with an existing `config` file at that location\. You can specify another path with the **\-\-kubeconfig** option\.
   + You can specify an IAM role ARN with the **\-\-role\-arn** option to use for authentication when you issue `kubectl` commands\. Otherwise, the IAM entity in your default AWS CLI or SDK credential chain is used\. You can view your default AWS CLI or SDK identity by running the `aws sts get-caller-identity` command\.
   + For more information, see the help page with the `aws eks update-kubeconfig help` command or see [update\-kubeconfig](https://docs.aws.amazon.com/cli/latest/reference/eks/update-kubeconfig.html) in the *AWS CLI Command Reference*\.
**Note**  
To run the following command, you must have permission to use the `eks:DescribeCluster` API action with the cluster that you specify\. For more information, see [Amazon EKS identity\-based policy examples](security_iam_id-based-policy-examples.md)\.

   ```
   aws eks update-kubeconfig --region region-code --name my-cluster
   ```

1. Test your configuration\.

   ```
   kubectl get svc
   ```
**Note**  
If you receive any authorization or resource type errors, see [Unauthorized or access denied \(`kubectl`\)](troubleshooting.md#unauthorized) in the troubleshooting section\.

   The example output is as follows\.

   ```
   NAME             TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
   svc/kubernetes   ClusterIP   10.100.0.1   <none>        443/TCP   1m
   ```

## Create `kubeconfig` file manually<a name="create-kubeconfig-manually"></a>

**To create your `kubeconfig` file manually**

1. Set values for a few variables by replacing the `example values` with your own and then running the modified commands\.

   ```
   export region_code=region-code
   export cluster_name=my-cluster
   export account_id=111122223333
   ```

1. Retrieve the endpoint for your cluster and store the value in a variable\.

   ```
   cluster_endpoint=$(aws eks describe-cluster \
       --region $region_code \
       --name $cluster_name \
       --query "cluster.endpoint" \
       --output text)
   ```

1. Retrieve the Base64\-encoded certificate data required to communicate with your cluster and store the value in a variable\.

   ```
   certificate_data=$(aws eks describe-cluster \
       --region $region_code \
       --name $cluster_name \
       --query "cluster.certificateAuthority.data" \
       --output text)
   ```

1. Create the default `~/.kube` directory if it doesn't already exist\.

   ```
   mkdir -p ~/.kube
   ```

1. Run the command for your preferred client token method \(AWS CLI or AWS IAM authenticator for Kubernetes\) to create the `config` file in the `~/.kube` directory\. You can specify the following before running one of the commands by modifying the command to include the following:
   + **An IAM role –** Remove the `#` at the start of the lines under `args:`\. Replace `my-role` with the name of the IAM role that you want to perform cluster operations with instead of the default AWS credential provider chain\. For more information, see [Set up `kubectl` to use authentication tokens provided by AWS IAM Authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator#5-set-up-kubectl-to-use-authentication-tokens-provided-by-aws-iam-authenticator-for-kubernetes) on GitHub\.
   + **An AWS CLI [named profile](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html)** – Remove the `#` at the start of the `env:` line, and remove `#` at the start of the lines under it\. Replace `aws-profile` with the name of the profile to use\. If you don't specify a profile, then the default profile is used\. For additional information, see [Specifying Credentials & Using AWS Profiles](https://github.com/kubernetes-sigs/aws-iam-authenticator#specifying-credentials--using-aws-profiles) on GitHub\.

------
#### [ AWS CLI ]

**Prerequisite**  
Version `1.16.156` or later of the AWS CLI must be installed on your device\.

   ```
   #!/bin/bash
   read -r -d '' KUBECONFIG <<EOF
   apiVersion: v1
   clusters:
   - cluster:
       certificate-authority-data: $certificate_data
       server: $cluster_endpoint
     name: arn:aws:eks:$region_code:$account_id:cluster/$cluster_name
   contexts:
   - context:
       cluster: arn:aws:eks:$region_code:$account_id:cluster/$cluster_name
       user: arn:aws:eks:$region_code:$account_id:cluster/$cluster_name
     name: arn:aws:eks:$region_code:$account_id:cluster/$cluster_name
   current-context: arn:aws:eks:$region_code:$account_id:cluster/$cluster_name
   kind: Config
   preferences: {}
   users:
   - name: arn:aws:eks:$region_code:$account_id:cluster/$cluster_name
     user:
       exec:
         apiVersion: client.authentication.k8s.io/v1beta1
         command: aws
         args:
           - --region
           - $region_code
           - eks
           - get-token
           - --cluster-name
           - $cluster_name
           # - "- --role-arn"
           # - "arn:aws:iam::$account_id:role/my-role"
         # env:
           # - name: "AWS_PROFILE"
           #   value: "aws-profile"
   EOF
   echo "${KUBECONFIG}" > ~/.kube/config
   ```

------
#### [ AWS IAM Authenticator for Kubernetes ]

**Prerequisite**  
The AWS IAM Authenticator for Kubernetes must be installed on your device\. To install it, see [Installing `aws-iam-authenticator`](install-aws-iam-authenticator.md)\.

   ```
   #!/bin/bash
   read -r -d '' KUBECONFIG <<EOF
   apiVersion: v1
   clusters:
   - cluster:
       server: $cluster_endpoint
       certificate-authority-data: $certificate_data
     name: arn:aws:eks:$region_code:$account_id:cluster/$cluster_name
   contexts:
   - context:
       cluster: arn:aws:eks:$region_code:$account_id:cluster/$cluster_name
       user: arn:aws:eks:$region_code:$account_id:cluster/$cluster_name
     name: arn:aws:eks:$region_code:$account_id:cluster/$cluster_name
   current-context: arn:aws:eks:$region_code:$account_id:cluster/$cluster_name
   kind: Config
   preferences: {}
   users:
   - name: arn:aws:eks:$region_code:$account_id:cluster/$cluster_name
     user:
       exec:
         apiVersion: client.authentication.k8s.io/v1beta1
         command: aws-iam-authenticator
         args:
           - "token"
           - "-i"
           - "$cluster_name"
           # - "- --role-arn"
           # - "arn:aws:iam::$account_id:role/my-role"
         # env:
           # - name: "AWS_PROFILE"
           #   value: "aws-profile"
   EOF
   echo "${KUBECONFIG}" > ~/.kube/config
   ```

------

1. Add the file path to your `KUBECONFIG` environment variable so that `kubectl` knows where to look for your cluster configuration\.
   + For Bash shells on macOS or Linux:

     ```
     export KUBECONFIG=$KUBECONFIG:~/.kube/config
     ```
   + For PowerShell on Windows:

     ```
     $ENV:KUBECONFIG="{0};{1}" -f  $ENV:KUBECONFIG, "$ENV:userprofile\.kube\config"
     ```

1. \(Optional\) Add the configuration to your shell initialization file so that it is configured when you open a shell\.
   + For Bash shells on macOS:

     ```
     echo 'export KUBECONFIG=$KUBECONFIG:~/.kube/config' >> ~/.bash_profile
     ```
   + For Bash shells on Linux:

     ```
     echo 'export KUBECONFIG=$KUBECONFIG:~/.kube/config' >> ~/.bashrc
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

   The example output is as follows\.

   ```
   NAME             TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
   svc/kubernetes   ClusterIP   10.100.0.1   <none>        443/TCP   1m
   ```