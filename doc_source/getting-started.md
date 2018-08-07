# Getting Started with Amazon EKS<a name="getting-started"></a>

This getting started guide helps you to create all of the required resources to get started with Amazon EKS\.

## Amazon EKS Prerequisites<a name="eks-prereqs"></a>

Before you can create an Amazon EKS cluster, you must create an IAM role that Kubernetes can assume to create AWS resources\. For example, when a load balancer is created, Kubernetes assumes the role to create an Elastic Load Balancing load balancer in your account\. This only needs to be done one time and can be used for multiple EKS clusters\.

You must also create a VPC and a security group for your cluster to use\. Although the VPC and security groups can be used for multiple EKS clusters, we recommend that you use a separate VPC for each EKS cluster to provide better network isolation\.

This section also helps you to install the kubectl binary and configure it to work with Amazon EKS\.

### Create your Amazon EKS Service Role<a name="role-create"></a>

**To create your Amazon EKS service role**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. Choose **Roles**, then **Create role**\.

1. Choose **EKS** from the list of services, then **Allows Amazon EKS to manage your clusters on your behalf** for your use case, then **Next: Permissions**\.

1. Choose **Next: Review**\.

1. For **Role name**, enter a unique name for your role, such as `eksServiceRole`, then choose **Create role**\.

### Create your Amazon EKS Cluster VPC<a name="vpc-create"></a>

**To create your cluster VPC**

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. From the navigation bar, select a Region that supports Amazon EKS\.
**Note**  
Amazon EKS is available in the following Regions at this time:  
**US West \(Oregon\)** \(`us-west-2`\)
**US East \(N\. Virginia\)** \(`us-east-1`\)

1. Choose **Create stack**\.

1. For **Choose a template**, select **Specify an Amazon S3 template URL**\.

1. Paste the following URL into the text area and choose **Next**:

   ```
   https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/amazon-eks-vpc-sample.yaml
   ```

1. On the **Specify Details** page, fill out the parameters accordingly, and then choose **Next**\.
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it **eks\-vpc**\.
   + **VpcBlock**: Choose a CIDR range for your VPC\. You may leave the default value\.
   + **Subnet01Block**: Choose a CIDR range for subnet 1\. You may leave the default value\.
   + **Subnet02Block**: Choose a CIDR range for subnet 2\. You may leave the default value\.
   + **Subnet03Block**: Choose a CIDR range for subnet 3\. You may leave the default value\.

1. \(Optional\) On the **Options** page, tag your stack resources\. Choose **Next**\.

1. On the **Review** page, choose **Create**\.

1. When your stack is created, select it in the console and choose **Outputs**\.

1. Record the **SecurityGroups** value for the security group that was created\. You need this when you create your EKS cluster; this security group is applied to the cross\-account elastic network interfaces that are created in your subnets that allow the Amazon EKS control plane to communicate with your worker nodes\.

1. Record the **VpcId** for the subnets that were created\. You need this when you launch your worker node group template\.

1. Record the **SubnetIds** for the subnets that were created\. You need this when you create your EKS cluster; these are the subnets that your worker nodes are launched into\.

### Install and Configure kubectl for Amazon EKS<a name="get-started-kubectl"></a>

Amazon EKS clusters require kubectl and kubelet binaries and the [AWS IAM Authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator) to allow IAM authentication for your Kubernetes cluster\. Beginning with Kubernetes version 1\.10, you can configure the stock kubectl client to work with Amazon EKS by installing the AWS IAM Authenticator for Kubernetes and modifying your kubectl configuration file to use it for authentication\.

If you do not already have a local `kubectl` version 1\.10 client on your system, you can use the steps below to install one\. You can also refer to the [Kubernetes documentation](https://kubernetes.io/docs/tasks/tools/install-kubectl/) to install kubectl\.

**To install kubectl for Amazon EKS**

1. Download and install kubectl for your operating system\. Amazon EKS vends kubectl binaries that you can use, or you can follow the instructions in the Kubernetes documentation to install\.
   + To install the Amazon EKS\-vended version of kubectl:

     1. Download the Amazon EKS\-vended kubectl binary from Amazon S3:
        + **Linux**: [https://amazon\-eks\.s3\-us\-west\-2\.amazonaws\.com/1\.10\.3/2018\-07\-26/bin/linux/amd64/kubectl](https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/bin/linux/amd64/kubectl)
        + **MacOS**: [https://amazon\-eks\.s3\-us\-west\-2\.amazonaws\.com/1\.10\.3/2018\-07\-26/bin/darwin/amd64/kubectl](https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/bin/darwin/amd64/kubectl)
        + **Windows**: [https://amazon\-eks\.s3\-us\-west\-2\.amazonaws\.com/1\.10\.3/2018\-07\-26/bin/windows/amd64/kubectl\.exe](https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/bin/windows/amd64/kubectl.exe)

        Use the command below to download the binary, substituting the correct URL for your platform\. The example below is for macOS clients\.

        ```
        curl -o kubectl https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/bin/darwin/amd64/kubectl
        ```

     1. \(Optional\) Verify the downloaded binary with the SHA\-256 sum provided in the same bucket prefix, substituting the correct URL for your platform\.

        1. Download the SHA\-256 sum for your system\. The example below is to download the SHA\-256 sum for macOS clients\.

           ```
           curl -o kubectl.sha256 https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/bin/darwin/amd64/kubectl.sha256
           ```

        1. Check the SHA\-256 sum for your downloaded binary\. The example `openssl` command below was tested for macOS and Ubuntu clients\. Your operating system may use a different command or syntax to check SHA\-256 sums\. Consult your operating system documentation if necessary\.

           ```
           openssl sha -sha256 kubectl
           ```

        1. Compare the generated SHA\-256 sum in the command output against your downloaded `kubectl.sha256` file\. The two should match\.

     1. Apply execute permissions to the binary\.

        ```
        chmod +x ./kubectl
        ```

     1. Copy the binary to a folder in your `$PATH`\. If you have already installed a version of kubectl \(from Homebrew or Apt\), then we recommend creating a `$HOME/bin/kubectl` and ensuring that `$HOME/bin` comes first in your `$PATH`\.

        ```
        cp ./kubectl $HOME/bin/kubectl && export PATH=$HOME/bin:$PATH
        ```

     1. \(Optional\) Add the `$HOME/bin` path to your shell initialization file so that it is configured when you open a shell\.
        + For Bash shells on macOS:

          ```
          echo 'export PATH=$HOME/bin:$PATH' >> ~/.bash_profile
          ```
        + For Bash shells on Linux:

          ```
          echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc
          ```
   + Or, to install kubectl using the Kubernetes documentation, see [Install and Set Up kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) in the Kubernetes documentation\.

1. After you install kubectl, you can verify its version with the following command:

   ```
   kubectl version --short --client
   ```

   Example output:

   ```
   Client Version: v1.10.3
   ```

**To install `aws-iam-authenticator` for Amazon EKS**
+ Download and install the `aws-iam-authenticator` binary\.

  Amazon EKS vends `aws-iam-authenticator` binaries that you can use, or you can use go get to fetch the binary from the [AWS IAM Authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator) project on GitHub for other operating systems\.
  + To download and install the Amazon EKS\-vended `aws-iam-authenticator` binary:

    1. Download the Amazon EKS\-vended `aws-iam-authenticator` binary from Amazon S3:
       + **Linux**: [https://amazon\-eks\.s3\-us\-west\-2\.amazonaws\.com/1\.10\.3/2018\-07\-26/bin/linux/amd64/aws\-iam\-authenticator](https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/bin/linux/amd64/aws-iam-authenticator)
       + **MacOS**: [https://amazon\-eks\.s3\-us\-west\-2\.amazonaws\.com/1\.10\.3/2018\-07\-26/bin/darwin/amd64/aws\-iam\-authenticator](https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/bin/darwin/amd64/aws-iam-authenticator)
       + **Windows**: [https://amazon\-eks\.s3\-us\-west\-2\.amazonaws\.com/1\.10\.3/2018\-07\-26/bin/windows/amd64/aws\-iam\-authenticator\.exe](https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/bin/windows/amd64/aws-iam-authenticator.exe)

       Use the command below to download the binary, substituting the correct URL for your platform\. The example below is for macOS clients\.

       ```
       curl -o aws-iam-authenticator https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/bin/darwin/amd64/aws-iam-authenticator
       ```

    1. \(Optional\) Verify the downloaded binary with the SHA\-256 sum provided in the same bucket prefix, substituting the correct URL for your platform\. 

       1. Download the SHA\-256 sum for your system\. The example below is to download the SHA\-256 sum for macOS clients\.

          ```
          curl -o aws-iam-authenticator.sha256 https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/bin/darwin/amd64/aws-iam-authenticator.sha256
          ```

       1. Check the SHA\-256 sum for your downloaded binary\. The example `openssl` command below was tested for macOS and Ubuntu clients\. Your operating system may use a different command or syntax to check SHA\-256 sums\. Consult your operating system documentation if necessary\.

          ```
          openssl sha -sha256 aws-iam-authenticator
          ```

       1. Compare the generated SHA\-256 sum in the command output against your downloaded `aws-iam-authenticator.sha256` file\. The two should match\.

    1. Apply execute permissions to the binary\.

       ```
       chmod +x ./aws-iam-authenticator
       ```

    1. Copy the binary to a folder in your `$PATH`\. We recommend creating a `$HOME/bin/aws-iam-authenticator` and ensuring that `$HOME/bin` comes first in your `$PATH`\.

       ```
       cp ./aws-iam-authenticator $HOME/bin/aws-iam-authenticator && export PATH=$HOME/bin:$PATH
       ```

    1. Add `$HOME/bin` to your `PATH` environment variable\.
       + For Bash shells on macOS:

         ```
         echo 'export PATH=$HOME/bin:$PATH' >> ~/.bash_profile
         ```
       + For Bash shells on Linux:

         ```
         echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc
         ```

    1. Test that the `aws-iam-authenticator` binary works\.

       ```
       aws-iam-authenticator help
       ```
  + Or, to install the `aws-iam-authenticator` binary from GitHub using go get:

    1. Install the Go programming language for your operating system if you do not already have go installed\. For more information, see [Install the Go tools](https://golang.org/doc/install#install) in the Go documentation\.

    1. Use go get to install the `aws-iam-authenticator` binary\.

       ```
       go get -u -v github.com/kubernetes-sigs/aws-iam-authenticator/cmd/aws-iam-authenticator
       ```
**Note**  
If you receive the following error, you must upgrade your Go language to 1\.7 or greater\. For more information, see [Install the Go tools](https://golang.org/doc/install#install) in the Go documentation\.  

       ```
       package context: unrecognized import path "context" (import path does not begin with hostname)
       ```

    1. Add `$HOME/go/bin` to your `PATH` environment variable\.
       + For Bash shells on macOS:

         ```
         export PATH=$HOME/go/bin:$PATH && echo 'export PATH=$HOME/go/bin:$PATH' >> ~/.bash_profile
         ```
       + For Bash shells on Linux:

         ```
         export PATH=$HOME/go/bin:$PATH && echo 'export PATH=$HOME/go/bin:$PATH' >> ~/.bashrc
         ```

    1. Test that the `aws-iam-authenticator` binary works\.

       ```
       aws-iam-authenticator help
       ```

### \(Optional\) Download and Install the Latest AWS CLI<a name="custom-aws-cli"></a>

Amazon EKS requires at least version 1\.15\.32 of the AWS CLI\. To install or upgrade the AWS CLI, see [Installing the AWS Command Line Interface](http://docs.aws.amazon.com/cli/latest/userguide/installing.html) in the *AWS Command Line Interface User Guide*\.

**Note**  
Your system's Python version must be Python 3, or Python 2\.7\.9 or greater\. Otherwise, you receive `hostname doesn't match` errors with AWS CLI calls to Amazon EKS\. For more information, see [What are "hostname doesn't match" errors?](http://docs.python-requests.org/en/master/community/faq/#what-are-hostname-doesn-t-match-errors) in the Python Requests FAQ\.

## Step 1: Create Your Amazon EKS Cluster<a name="eks-create-cluster"></a>

Now you can create your Amazon EKS cluster\.

**Important**  
When an Amazon EKS cluster is created, the IAM entity \(user or role\) that creates the cluster is added to the Kubernetes RBAC authorization table as the administrator\. Initially, only that IAM user can make calls to the Kubernetes API server using kubectl\. Also, the [AWS IAM Authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator) uses the AWS SDK for Go to authenticate against your Amazon EKS cluster\. If you use the console to create the cluster, you must ensure that the same IAM user credentials are in the AWS SDK credential chain when you are running kubectl commands on your cluster\.  
If you install and configure the AWS CLI, you can configure the IAM credentials for your user\. These also work for the [AWS IAM Authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator)\. If the AWS CLI is configured properly for your user, then the [AWS IAM Authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator) can find those credentials as well\. For more information, see [Configuring the AWS CLI](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) in the *AWS Command Line Interface User Guide*\.

**To create your cluster with the console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose **Create cluster**\.
**Note**  
If your IAM user does not have administrative privileges, you must explicitly add permissions for that user to call the Amazon EKS API operations\. For more information, see [Creating Amazon EKS IAM Policies](EKS_IAM_user_policies.md)\.

1. On the **Create cluster** page, fill in the following fields and then choose **Create**:
   + **Cluster name**: A unique name for your cluster\.
   + **Kubernetes version**: The version of Kubernetes to use for your cluster\. By default, the latest available version is selected\.
   + **Role ARN**: Select the IAM role that you created with [Create your Amazon EKS Service Role](#role-create)\.
   + **VPC**: The VPC you created with [Create your Amazon EKS Cluster VPC](#vpc-create)\. You can find the name of your VPC in the drop\-down list\.
   + **Subnets**: The **SubnetIds** values \(comma\-separated\) from the AWS CloudFormation output that you generated with [Create your Amazon EKS Cluster VPC](#vpc-create)\. By default, the available subnets in the above VPC are preselected\.
   + **Security Groups**: The **SecurityGroups** value from the AWS CloudFormation output that you generated with [Create your Amazon EKS Cluster VPC](#vpc-create)\. This security group has **ControlPlaneSecurityGroup** in the drop\-down name\.
**Important**  
The worker node AWS CloudFormation template modifies the security group that you specify here, so we recommend that you use a dedicated security group for your cluster control plane\. If you share it with other resources, you may block or disrupt connections to those resources\.
**Note**  
You may receive an error that one of the Availability Zones in your request does not have sufficient capacity to create an Amazon EKS cluster\. If this happens, the error output contains the Availability Zones that can support a new cluster\. Retry creating your cluster with at least two subnets that are located in the supported Availability Zones for your account\.

1. On the **Clusters** page, choose the name of your newly created cluster to view the cluster information\.

1. The **Status** field shows **CREATING** until the cluster provisioning process completes\. When your cluster provisioning is complete \(usually less than 10 minutes\), and note the **API server endpoint** and **Certificate authority** values\. These are used in your kubectl configuration\.

**To create your cluster with the AWS CLI**

1. Create your cluster with the following command\. Substitute your cluster name, the Amazon Resource Name \(ARN\) of your Amazon EKS service role that you created in [Create your Amazon EKS Service Role](#role-create), and the subnet and security group IDs for the VPC that you created in [Create your Amazon EKS Cluster VPC](#vpc-create)\.

   ```
   aws eks create-cluster --name devel --role-arn arn:aws:iam::111122223333:role/eks-service-role-AWSServiceRoleForAmazonEKS-EXAMPLEBKZRQR --resources-vpc-config subnetIds=subnet-a9189fe2,subnet-50432629,securityGroupIds=sg-f5c54184
   ```
**Important**  
If you receive a syntax error similar to the following, you may using a preview version of the AWS CLI for Amazon EKS\. The syntax for many Amazon EKS commands has changed since the public service launch\. Please update your AWS CLI version to the latest available and be sure to delete the custom service model directory at `~/.aws/models/eks`\.  

   ```
   aws: error: argument --cluster-name is required
   ```
**Note**  
If your IAM user does not have administrative privileges, you must explicitly add permissions for that user to call the Amazon EKS API operations\. For more information, see [Creating Amazon EKS IAM Policies](EKS_IAM_user_policies.md)\.

   Output:

   ```
   {
       "cluster": {
           "name": "devel",
           "arn": "arn:aws:eks:us-west-2:111122223333:cluster/devel",
           "createdAt": 1527785885.159,
           "version": "1.10",
           "roleArn": "arn:aws:iam::111122223333:role/eks-service-role-AWSServiceRoleForAmazonEKS-AFNL4H8HB71F",
           "resourcesVpcConfig": {
               "subnetIds": [
                   "subnet-a9189fe2",
                   "subnet-50432629"
               ],
               "securityGroupIds": [
                   "sg-f5c54184"
               ],
               "vpcId": "vpc-a54041dc"
           },
           "status": "CREATING",
           "certificateAuthority": {}
       }
   }
   ```

1. Cluster provisioning usually takes less than 10 minutes\. You can query the status of your cluster with the following command\. When your cluster status is `ACTIVE`, you can proceed\.

   ```
   aws eks describe-cluster --name devel --query cluster.status
   ```

1. When your cluster provisioning is complete, retrieve the `endpoint` and `certificateAuthority.data` values with the following commands\. These must be added to your kubectl configuration so that you can communicate with your cluster\.

   1. Retrieve the `endpoint`\.

      ```
      aws eks describe-cluster --name devel  --query cluster.endpoint
      ```

   1. Retrieve the `certificateAuthority.data`\.

      ```
      aws eks describe-cluster --name devel  --query cluster.certificateAuthority.data
      ```

## Step 2: Configure `kubectl` for Amazon EKS<a name="eks-configure-kubectl"></a>

In this section, you create a `kubeconfig` file for your cluster\. The code block in the procedure below shows the `kubeconfig` elements to add to your configuration\. If you have an existing configuration and you are comfortable working with `kubeconfig` files, you can merge these elements into your existing setup\. Be sure to replace the *<endpoint\-url>* value with the full endpoint URL \(for example, *https://API\_SERVER\_ENDPOINT\.yl4\.us\-west\-2\.eks\.amazonaws\.com*\) that was created for your cluster, replace the *<base64\-encoded\-ca\-cert>* with the `certificateAuthority.data` value you retrieved earlier, and replace the *<cluster\-name>* with your cluster name\.

Amazon EKS uses the [AWS IAM Authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator) with kubectl for cluster authentication, which uses the same default AWS credential provider chain as the AWS CLI and AWS SDKs\. If you have installed the AWS CLI on your system, then by default the AWS IAM Authenticator for Kubernetes will use the same credentials that are returned with the following command:

```
aws sts get-caller-identity
```

For more information, see [Configuring the AWS CLI](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) in the *AWS Command Line Interface User Guide*\.

To instead have the AWS IAM Authenticator for Kubernetes assume a role to perform cluster operations, uncomment the `-r` and `<role-arn>` lines and substitute an IAM role ARN to use with your user\.

If you manage multiple AWS credential profiles, you can either set the `AWS_PROFILE` variable in your shell or specify the profile name in an environment variable value for the authenticator to use in your `kubeconfig` as shown in the procedure below\.

If you do not have an existing configuration, or to add the Amazon EKS cluster without modifying your existing configuration files, you can use the following procedure to add the Amazon EKS cluster to your configuration\.

**To retrieve your cluster information with the AWS CLI**

When your cluster provisioning is complete, retrieve the `endpoint` and `certificateAuthority.data` values with the following commands\. These must be added to your kubectl configuration so that you can communicate with your cluster\.

1. Retrieve the `endpoint` for your cluster\. Use this for the *<endpoint\-url>* in your `kubeconfig` file\.

   ```
   aws eks describe-cluster --name devel  --query cluster.endpoint
   ```

1. Retrieve the `certificateAuthority.data` for your cluster\. Use this for the *<base64\-encoded\-ca\-cert>* in your `kubeconfig` file\.

   ```
   aws eks describe-cluster --name devel  --query cluster.certificateAuthority.data
   ```

**To create your `kubeconfig` file**

1. Create the default `~/.kube` directory if it does not already exist\.

   ```
   mkdir -p ~/.kube
   ```

1. Open your favorite text editor and copy the `kubeconfig` code block below into it\.

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

1. Replace the *<endpoint\-url>* with the endpoint URL that was created for your cluster\.

1. Replace the *<base64\-encoded\-ca\-cert>* with the `certificateAuthority.data` that was created for your cluster\.

1. Replace the *<cluster\-name>* with your cluster name\.

1. \(Optional\) To have the AWS IAM Authenticator for Kubernetes assume a role to perform cluster operations instead of the default AWS credential provider chain, uncomment the `-r` and `<role-arn>` lines and substitute an IAM role ARN to use with your user\.

1. \(Optional\) To have the AWS IAM Authenticator for Kubernetes always use a specific named AWS credential profile \(instead of the default AWS credential provider chain\), uncomment the `env` lines and substitute *<aws\-profile>* with the profile name to use\.

1. Save the file to the default kubectl folder, with your cluster name in the file name\. For example, if your cluster name is *devel*, save the file to `~/.kube/config-devel`\.

1. Add that file path to your `KUBECONFIG` environment variable so that kubectl knows where to look for your cluster configuration\.

   ```
   export KUBECONFIG=$KUBECONFIG:~/.kube/config-devel
   ```

1. \(Optional\) Add the configuration to your shell initialization file so that it is configured when you open a shell\.
   + For Bash shells on macOS:

     ```
     echo 'export KUBECONFIG=$KUBECONFIG:~/.kube/config-devel' >> ~/.bash_profile
     ```
   + For Bash shells on Linux:

     ```
     echo 'export KUBECONFIG=$KUBECONFIG:~/.kube/config-devel' >> ~/.bashrc
     ```

1. Test your configuration\.

   ```
   kubectl get svc
   ```
**Note**  
If you receive the error `"aws-iam-authenticator": executable file not found in $PATH`, then your kubectl is not configured for Amazon EKS\. For more information, see [Configure kubectl for Amazon EKS](configure-kubectl.md)\.

   Output:

   ```
   NAME             TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
   svc/kubernetes   ClusterIP   10.100.0.1   <none>        443/TCP   1m
   ```

## Step 3: Launch and Configure Amazon EKS Worker Nodes<a name="eks-launch-workers"></a>

Now that your VPC and Kubernetes control plane are created, you can launch and configure your worker nodes\.

**Important**  
Amazon EKS worker nodes are standard Amazon EC2 instances, and you are billed for them based on normal Amazon EC2 On\-Demand Instance prices\. For more information, see [Amazon EC2 Pricing](https://aws.amazon.com/ec2/pricing/on-demand/)\.

**To launch your worker nodes**

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. From the navigation bar, select a Region that supports Amazon EKS\.
**Note**  
Amazon EKS is available in the following Regions at this time:  
**US West \(Oregon\)** \(`us-west-2`\)
**US East \(N\. Virginia\)** \(`us-east-1`\)

1. Choose **Create stack**\.

1. For **Choose a template**, select **Specify an Amazon S3 template URL**\.

1. Paste the following URL into the text area and choose **Next**:

   ```
   https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/amazon-eks-nodegroup.yaml
   ```

1. On the **Specify Details** page, fill out the following parameters accordingly, and choose **Next**\.
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it ***<cluster\-name>*\-worker\-nodes**\.
   + **ClusterName**: Enter the name that you used when you created your Amazon EKS cluster\.
**Important**  
This name must exactly match the name you used in [Step 1: Create Your Amazon EKS Cluster](#eks-create-cluster); otherwise, your worker nodes cannot join the cluster\.
   + **ClusterControlPlaneSecurityGroup**: Choose the **SecurityGroups** value from the AWS CloudFormation output that you generated with [Create your Amazon EKS Cluster VPC](#vpc-create)\.
   + **NodeGroupName**: Enter a name for your node group that will be included in your Auto Scaling node group name\.
   + **NodeAutoScalingGroupMinSize**: Enter the minimum number of nodes that your worker node Auto Scaling group can scale in to\.
   + **NodeAutoScalingGroupMaxSize**: Enter the maximum number of nodes that your worker node Auto Scaling group can scale out to\.
   + **NodeInstanceType**: Choose an instance type for your worker nodes\.
   + **NodeImageId**: Enter the current Amazon EKS worker node AMI ID for your Region\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/getting-started.html)
**Note**  
The Amazon EKS worker node AMI is based on Amazon Linux 2\. You can track security or privacy events for Amazon Linux 2 at the [Amazon Linux Security Center](https://alas.aws.amazon.com/alas2.html) or subscribe to the associated [RSS feed](https://alas.aws.amazon.com/AL2/alas.rss)\. Security and privacy events include an overview of the issue, what packages are affected, and how to update your instances to correct the issue\.
   + **KeyName**: Enter the name of an Amazon EC2 SSH key pair that you can use to connect using SSH into your worker nodes with after they launch\.
   + **VpcId**: Enter the ID for the VPC that you created in [Create your Amazon EKS Cluster VPC](#vpc-create)\.
   + **Subnets**: Choose the subnets that you created in [Create your Amazon EKS Cluster VPC](#vpc-create)\.

1. On the **Options** page, you can choose to tag your stack resources\. Choose **Next**\.

1. On the **Review** page, review your information, acknowledge that the stack might create IAM resources, and then choose **Create**\.

1. When your stack has finished creating, select it in the console and choose the **Outputs** tab\.

1. Record the **NodeInstanceRole** for the node group that was created\. You need this when you configure your Amazon EKS worker nodes\.

**To enable worker nodes to join your cluster**

1. Download, edit, and apply the AWS authenticator configuration map:

   1. Download the configuration map\.

      ```
      curl -O https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/aws-auth-cm.yaml
      ```

   1. Open the file with your favorite text editor\. Replace the *<ARN of instance role \(not instance profile\)>* snippet with the **NodeInstanceRole** value that you recorded in the previous procedure, and save the file\.
**Important**  
Do not modify any other lines in this file\.

      ```
      apiVersion: v1
      kind: ConfigMap
      metadata:
        name: aws-auth
        namespace: kube-system
      data:
        mapRoles: |
          - rolearn: <ARN of instance role (not instance profile)>
            username: system:node:{{EC2PrivateDNSName}}
            groups:
              - system:bootstrappers
              - system:nodes
      ```

   1. Apply the configuration\. This command may take a few minutes to finish\.

      ```
      kubectl apply -f aws-auth-cm.yaml
      ```
**Note**  
If you receive the error `"aws-iam-authenticator": executable file not found in $PATH`, then your kubectl is not configured for Amazon EKS\. For more information, see [Configure kubectl for Amazon EKS](configure-kubectl.md)\.

1. Watch the status of your nodes and wait for them to reach the `Ready` status\.

   ```
   kubectl get nodes --watch
   ```

## Step 4: Launch a Guest Book Application<a name="eks-guestbook"></a>

In this section, you create a sample guest book application to test your new cluster\.

**Note**  
For more information about setting up the guest book example, see [https://github\.com/kubernetes/examples/blob/master/guestbook\-go/README\.md](https://github.com/kubernetes/examples/blob/master/guestbook-go/README.md) in the Kubernetes documentation\.

**To create your guest book application**

1. Create the Redis master replication controller\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/kubernetes/v1.10.3/examples/guestbook-go/redis-master-controller.json
   ```
**Note**  
If you receive the error `"aws-iam-authenticator": executable file not found in $PATH`, then your kubectl is not configured for Amazon EKS\. For more information, see [Configure kubectl for Amazon EKS](configure-kubectl.md)\.

   Output:

   ```
   replicationcontroller "redis-master" created
   ```

1. Create the Redis master service\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/kubernetes/v1.10.3/examples/guestbook-go/redis-master-service.json
   ```

   Output:

   ```
   service "redis-master" created
   ```

1. Create the Redis slave replication controller\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/kubernetes/v1.10.3/examples/guestbook-go/redis-slave-controller.json
   ```

   Output:

   ```
   replicationcontroller "redis-slave" created
   ```

1. Create the Redis slave service\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/kubernetes/v1.10.3/examples/guestbook-go/redis-slave-service.json
   ```

   Output:

   ```
   service "redis-slave" created
   ```

1. Create the guestbook replication controller\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/kubernetes/v1.10.3/examples/guestbook-go/guestbook-controller.json
   ```

   Output:

   ```
   replicationcontroller "guestbook" created
   ```

1. Create the guestbook service\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/kubernetes/v1.10.3/examples/guestbook-go/guestbook-service.json
   ```

   Output:

   ```
   service "guestbook" created
   ```

1. Query the services in your cluster and wait until the **External IP** column for the `guestbook` service is populated\.
**Note**  
It may take several minutes before the IP address is available\.

   ```
   kubectl get services -o wide
   ```

1. After your external IP address is available, point a web browser to that address at port 3000 to view your guest book\. For example, *http://a7a95c2b9e69711e7b1a3022fdcfdf2e\-1985673473\.us\-west\-2\.elb\.amazonaws\.com:3000*
**Note**  
It may take several minutes for DNS to propagate and for your guest book to show up\.  
![\[Guest book\]](http://docs.aws.amazon.com/eks/latest/userguide/images/guestbook.png)
**Important**  
If you are unable to connect to the external IP address with your browser, be sure that your corporate firewall is not blocking non\-standards ports, like 3000\. You can try switching to a guest network to verify\.

## Step 5: Cleaning Up Guest Book Objects<a name="eks-guestbook-cleanup"></a>

When you are finished experimenting with your guest book application, you should clean up the resources that you created for it\. The following command deletes all of the services and replication controllers for the guest book application:

```
kubectl delete rc/redis-master rc/redis-slave rc/guestbook svc/redis-master svc/redis-slave svc/guestbook
```

**Note**  
If you receive the error `"aws-iam-authenticator": executable file not found in $PATH`, then your kubectl is not configured for Amazon EKS\. For more information, see [Configure kubectl for Amazon EKS](configure-kubectl.md)\.