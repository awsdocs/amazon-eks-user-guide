# Create an IAM OIDC provider for your cluster<a name="enable-iam-roles-for-service-accounts"></a>

Your cluster has an [https://openid.net/connect/](https://openid.net/connect/) \(OIDC\) issuer URL associated with it\. To use AWS Identity and Access Management \(IAM\) roles for service accounts, an IAM OIDC provider must exist for your cluster's OIDC issuer URL\.

**Prerequisites**
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\.
+ Version `2.12.3` or later or version `1.27.160` or later of the AWS Command Line Interface \(AWS CLI\) installed and configured on your device or AWS CloudShell\. To check your current version, use `aws --version | cut -d / -f2 | cut -d ' ' -f1`\. Package managers such `yum`, `apt-get`, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI\. To install the latest version, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with aws configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the *AWS Command Line Interface User Guide*\. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version\. To update it, see [Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the *AWS CloudShell User Guide*\.
+ The `kubectl` command line tool is installed on your device or AWS CloudShell\. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster\. For example, if your cluster version is `1.28`, you can use `kubectl` version `1.27`, `1.28`, or `1.29` with it\. To install or upgrade `kubectl`, see [Installing or updating `kubectl`](install-kubectl.md)\.
+ An existing `kubectl` `config` file that contains your cluster configuration\. To create a `kubectl` `config` file, see [Creating or updating a `kubeconfig` file for an Amazon EKS cluster](create-kubeconfig.md)\.

You can create an IAM OIDC provider for your cluster using `eksctl` or the AWS Management Console\.

------
#### [ eksctl ]

**Prerequisite**  
Version `0.175.0` or later of the `eksctl` command line tool installed on your device or AWS CloudShell\. To install or update `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.

**To create an IAM OIDC identity provider for your cluster with `eksctl`**

1. Determine the OIDC issuer ID for your cluster\.

   Retrieve your cluster's OIDC issuer ID and store it in a variable\. Replace `my-cluster` with your own value\.

   ```
   cluster_name=my-cluster
   ```

   ```
   oidc_id=$(aws eks describe-cluster --name $cluster_name --query "cluster.identity.oidc.issuer" --output text | cut -d '/' -f 5)
   ```

   ```
   echo $oidc_id
   ```

1. Determine whether an IAM OIDC provider with your cluster's issuer ID is already in your account\.

   ```
   aws iam list-open-id-connect-providers | grep $oidc_id | cut -d "/" -f4
   ```

   If output is returned, then you already have an IAM OIDC provider for your cluster and you can skip the next step\. If no output is returned, then you must create an IAM OIDC provider for your cluster\.

1. Create an IAM OIDC identity provider for your cluster with the following command\.

   ```
   eksctl utils associate-iam-oidc-provider --cluster $cluster_name --approve
   ```
**Note**  
If you enable the EKS VPC endpoint, the EKS OIDC service endpoint can't be accessed from inside that VPC\. Consequently, your operations such as creating an OIDC provider with `eksctl` in the VPC will not work and will result in a timeout when attempting to request `https://oidc.eks.region.amazonaws.com`\. An example error message follows:  

   ```
   ** server can't find oidc.eks.region.amazonaws.com: NXDOMAIN
   ```
To complete this step, you can run the command outside the VPC, for example in AWS CloudShell or on a computer connected to the internet\.

------
#### [ AWS Management Console ]<a name="create-oidc-console"></a>

**To create an IAM OIDC identity provider for your cluster with the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left pane, select **Clusters**, and then select the name of your cluster on the **Clusters** page\.

1. In the **Details** section on the **Overview** tab, note the value of the **OpenID Connect provider URL**\.

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the left navigation pane, choose **Identity Providers** under **Access management**\. If a **Provider** is listed that matches the URL for your cluster, then you already have a provider for your cluster\. If a provider isn't listed that matches the URL for your cluster, then you must create one\.

1. To create a provider, choose **Add provider**\.

1. For **Provider type**, select **OpenID Connect**\.

1. For **Provider URL**, enter the OIDC provider URL for your cluster, and then choose **Get thumbprint**\.

1. For **Audience**, enter **sts\.amazonaws\.com** and choose **Add provider**\.

------

**Next step**  
[Configure a Kubernetes service account to assume an IAM role](associate-service-account-role.md)