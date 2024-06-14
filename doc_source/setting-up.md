# Setting up to use Amazon EKS<a name="setting-up"></a>

AWS resources typically have access restrictions that limit access to the AWS entity that created them\. Therefore, it's crucial to establish proper user configuration in the AWS Command Line Interface from the beginning\. Additionally, you need to equip your local machine with essential tools for efficient command\-line management of your Amazon EKS cluster\. This topic will help you prepare for the command\-line management of your cluster\.

## Step 1: Set up the AWS CLI<a name="setup-awscli"></a>

The [AWS CLI](https://aws.amazon.com/cli/) is a command line tool for working with AWS services, including Amazon EKS\. It is also used to authenticate IAM users or roles for access to the Amazon EKS cluster and other AWS resources from your local machine\. To provision resources in AWS from the command line, you need to obtain an AWS access key ID and secret key to use in the command line\. Then you need to configure these credentials in the AWS CLI\. If you haven't already installed the AWS CLI, see [Install or update the latest version of the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) in the *AWS Command Line Interface User Guide*\.

### To create an access key<a name="create-access-key"></a>

1. Sign into the [AWS Management Console](https://console.aws.amazon.com/)\.

1. In the top right, choose your AWS user name to open the navigation menu\. For example, choose **`webadmin`**\. Then choose **Security credentials**\.

1. Under **Access keys**, choose **Create access key**\.

1. Choose **Command Line Interface \(CLI\)**, then choose **Next**\.

1. Choose **Create access key**\.

1. Choose **Download \.csv file**\.

### To configure the AWS CLI<a name="configure-cli"></a>

After installing the AWS CLI, do the following steps to configure it\. For more information, see [Configure the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) in the *AWS Command Line Interface User Guide*\.

1. In a terminal window, enter the following command:

   ```
   aws configure
   ```

   Optionally, you can configure a named profile, such as `--profile cluster-admin`\. If you configure a named profile in the AWS CLI, you must **always** pass this flag in subsequent commands\.

1. Enter your AWS credentials\. For example:

   ```
   AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
   AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
   Default region name [None]: region-code
   Default output format [None]: json
   ```

### To get a security token<a name="get-security-token"></a>

If needed, run the following command to get a new security token for the AWS CLI\. For more information, see [https://docs.aws.amazon.com/cli/latest/reference/sts/get-session-token.html](https://docs.aws.amazon.com/cli/latest/reference/sts/get-session-token.html) in the *AWS CLI Command Reference*\.

By default, the token is valid for 15 minutes\. To change the default session timeout, pass the `--duration-seconds` flag\. For example:

```
aws sts get-session-token --duration-seconds 3600
```

This command returns the temporary security credentials for an AWS CLI session\. You should see the following response output:

```
{
    "Credentials": {
        "AccessKeyId": "ASIA5FTRU3LOEXAMPLE",
        "SecretAccessKey": "JnKgvwfqUD9mNsPoi9IbxAYEXAMPLE",
        "SessionToken": "VERYLONGSESSIONTOKENSTRING",
        "Expiration": "2023-02-17T03:14:24+00:00"
    }
}
```

### To verify the user identity<a name="verify-user-id"></a>

If needed, run the following command to verify the AWS credentials for your IAM user identity \(such as `ClusterAdmin`\) for the terminal session\.

```
aws sts get-caller-identity
```

This command returns the Amazon Resource Name \(ARN\) of the IAM entity that's configured for the AWS CLI\. You should see the following example response output:

```
{
    "UserId": "AKIAIOSFODNN7EXAMPLE",
    "Account": "01234567890",
    "Arn": "arn:aws:iam::01234567890:user/ClusterAdmin"
}
```

## Step 2: Install Kubernetes tools<a name="setup-tools"></a>

To communicate with a Kubernetes cluster, you will need a tool to interact with the Kubernetes API\. Additionally, you need a few other tools, such as one to manage Kubernetes environments on your local machine\.

### To create AWS resources<a name="create-resources"></a>
+ **Amazon EKS cluster resources** – If you're new to AWS, we recommend installing [https://eksctl.io/](https://eksctl.io/)\. `eksctl` is an infrastructure as code \(IaC\) utility that uses AWS CloudFormation to easily create your Amazon EKS cluster\. It also creates additional Kubernetes resources, such as service accounts\. For instructions on how to install `eksctl`, see [Installation](https://eksctl.io/installation/) in the `eksctl` documentation\.
+ **AWS resources** – If you're accustomed to automating the provisioning and deployment of your AWS infrastructure, we recommend installing Terraform\. Terraform is an open\-source infrastructure as code \(IaC\) tool developed by HashiCorp\. It allows you to define and provision infrastructure using a high\-level configuration language such as HashiCorp Configuration Language \(HCL\) or JSON\. For instructions on how to install Terraform, see [Install Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) in the Terraform documentation\.

### To install `kubectl`<a name="setting-up-install-kubectl"></a>

`kubectl` is an open source command line tool used to communicate with the Kubernetes API server on your Amazon EKS cluster\. If you don't already have it installed on your local machine, choose from the following options\.
+ **AWS versions** – To install an Amazon EKS\-supported `kubectl` version, see [Installing or updating `kubectl`](install-kubectl.md)\.
+ **Community versions** – To install the latest community version of `kubectl`, see the [Install tools](https://kubernetes.io/docs/tasks/tools/#kubectl) page in Kubernetes documentation\.

### To set up a development environment<a name="dev-environment"></a>
+ **Local deployment tool** – If you're new to Kubernetes, consider installing a local deployment tool like [https://minikube.sigs.k8s.io/docs/](https://minikube.sigs.k8s.io/docs/) or [https://kind.sigs.k8s.io/](https://kind.sigs.k8s.io/)\. These tools allow you to manage an Amazon EKS cluster on your local machine\.
+ **Package manager** – [https://helm.sh/docs/intro/install/](https://helm.sh/docs/intro/install/) is a popular package manager for Kubernetes that simplifies the installation and management of complex packages\. With Helm, it's easier to install and manage packages like the AWS Load Balancer Controller on your Amazon EKS cluster\.

## Next steps<a name="setting-up-next-steps"></a>
+ [Getting started with Amazon EKS](getting-started.md)