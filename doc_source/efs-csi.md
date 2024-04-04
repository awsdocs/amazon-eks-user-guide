# Amazon EFS CSI driver<a name="efs-csi"></a>

[Amazon Elastic File System](https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html) \(Amazon EFS\) provides serverless, fully elastic file storage so that you can share file data without provisioning or managing storage capacity and performance\. The [Amazon EFS Container Storage Interface \(CSI\) driver](https://github.com/kubernetes-sigs/aws-efs-csi-driver) provides a CSI interface that allows Kubernetes clusters running on AWS to manage the lifecycle of Amazon EFS file systems\. This topic shows you how to deploy the Amazon EFS CSI driver to your Amazon EKS cluster\.

**Considerations**
+ The Amazon EFS CSI driver isn't compatible with Windows\-based container images\.
+ You can't use [dynamic provisioning](https://github.com/kubernetes-sigs/aws-efs-csi-driver/blob/master/examples/kubernetes/dynamic_provisioning/README.md) for persistent volumes with Fargate nodes, but you can use [static provisioning](https://github.com/kubernetes-sigs/aws-efs-csi-driver/blob/master/examples/kubernetes/static_provisioning/README.md)\.
+ [Dynamic provisioning](https://github.com/kubernetes-sigs/aws-efs-csi-driver/blob/master/examples/kubernetes/dynamic_provisioning/README.md) requires `1.2` or later of the driver\. You can use [static provisioning](https://github.com/kubernetes-sigs/aws-efs-csi-driver/blob/master/examples/kubernetes/static_provisioning/README.md) for persistent volumes using version `1.1` of the driver on any [supported Amazon EKS cluster version](kubernetes-versions.md)\.
+ Version `1.3.2` or later of this driver supports the Arm64 architecture, including Amazon EC2 Graviton\-based instances\.
+ Version `1.4.2` or later of this driver supports using FIPS for mounting file systems\.
+ Take note of the resource quotas for Amazon EFS\. For example, there's a quota of 1000 access points that can be created for each Amazon EFS file system\. For more information, see [Amazon EFS resource quotas that you cannot change](https://docs.aws.amazon.com/efs/latest/ug/limits.html#limits-efs-resources-per-account-per-region)\.

**Prerequisites**
+ An existing AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ Version `2.12.3` or later or version `1.27.160` or later of the AWS Command Line Interface \(AWS CLI\) installed and configured on your device or AWS CloudShell\. To check your current version, use `aws --version | cut -d / -f2 | cut -d ' ' -f1`\. Package managers such `yum`, `apt-get`, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI\. To install the latest version, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with aws configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the *AWS Command Line Interface User Guide*\. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version\. To update it, see [Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the *AWS CloudShell User Guide*\.
+ The `kubectl` command line tool is installed on your device or AWS CloudShell\. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster\. For example, if your cluster version is `1.28`, you can use `kubectl` version `1.27`, `1.28`, or `1.29` with it\. To install or upgrade `kubectl`, see [Installing or updating `kubectl`](install-kubectl.md)\.

**Note**  
A Pod running on AWS Fargate automatically mounts an Amazon EFS file system\.

## Creating an IAM role<a name="efs-create-iam-resources"></a>

The Amazon EFS CSI driver requires IAM permissions to interact with your file system\. Create an IAM role and attach the required AWS managed policy to it\. You can use `eksctl`, the AWS Management Console, or the AWS CLI\.

**Note**  
The specific steps in this procedure are written for using the driver as an Amazon EKS add\-on\. For details on self\-managed installations, see [Set up driver permission](https://github.com/kubernetes-sigs/aws-efs-csi-driver#set-up-driver-permission) on GitHub\.

------
#### [ eksctl ]

**To create your Amazon EFS CSI driver IAM role with `eksctl`**

Run the following commands to create the IAM role\. Replace `my-cluster` with your cluster name and `AmazonEKS_EFS_CSI_DriverRole` with the name for your role\.

```
export cluster_name=my-cluster
export role_name=AmazonEKS_EFS_CSI_DriverRole
eksctl create iamserviceaccount \
    --name efs-csi-controller-sa \
    --namespace kube-system \
    --cluster $cluster_name \
    --role-name $role_name \
    --role-only \
    --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEFSCSIDriverPolicy \
    --approve
TRUST_POLICY=$(aws iam get-role --role-name $role_name --query 'Role.AssumeRolePolicyDocument' | \
    sed -e 's/efs-csi-controller-sa/efs-csi-*/' -e 's/StringEquals/StringLike/')
aws iam update-assume-role-policy --role-name $role_name --policy-document "$TRUST_POLICY"
```

------
#### [ AWS Management Console ]

**To create your Amazon EFS CSI driver IAM role with the AWS Management Console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the left navigation pane, choose **Roles**\.

1. On the **Roles** page, choose **Create role**\.

1. On the **Select trusted entity** page, do the following:

   1. In the **Trusted entity type** section, choose **Web identity**\.

   1. For **Identity provider**, choose the **OpenID Connect provider URL** for your cluster \(as shown under **Overview** in Amazon EKS\)\.

   1. For **Audience**, choose `sts.amazonaws.com`\.

   1. Choose **Next**\.

1. On the **Add permissions** page, do the following:

   1. In the **Filter policies** box, enter `AmazonEFSCSIDriverPolicy`\.

   1. Select the check box to the left of the `AmazonEFSCSIDriverPolicy` returned in the search\.

   1. Choose **Next**\.

1. On the **Name, review, and create** page, do the following:

   1. For **Role name**, enter a unique name for your role, such as ***AmazonEKS\_EFS\_CSI\_DriverRole***\.

   1. Under **Add tags \(Optional\)**, add metadata to the role by attaching tags as key\-value pairs\. For more information about using tags in IAM, see [Tagging IAM resources](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html) in the *IAM User Guide*\.

   1. Choose **Create role**\.

1. After the role is created, choose the role in the console to open it for editing\.

1. Choose the **Trust relationships** tab, and then choose **Edit trust policy**\.

1. Find the line that looks similar to the following line:

   ```
   "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:aud": "sts.amazonaws.com"
   ```

   Add the following line above the previous line\. Replace `region-code` with the AWS Region that your cluster is in\. Replace `EXAMPLED539D4633E53DE1B71EXAMPLE` with your cluster's OIDC provider ID\.

   ```
   "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:sub": "system:serviceaccount:kube-system:efs-csi-*",
   ```

1. Modify the `Condition` operator from `"StringEquals"` to `"StringLike"`\.

1. Choose **Update policy** to finish\.

------
#### [ AWS CLI ]

**To create your Amazon EFS CSI driver IAM role with the AWS CLI**

1. View your cluster's OIDC provider URL\. Replace `my-cluster` with your cluster name\. If the output from the command is `None`, review the **Prerequisites**\.

   ```
   aws eks describe-cluster --name my-cluster --query "cluster.identity.oidc.issuer" --output text
   ```

   An example output is as follows\.

   ```
   https://oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE
   ```

1. Create the IAM role that grants the `AssumeRoleWithWebIdentity` action\.

   1. Copy the following contents to a file named `aws-efs-csi-driver-trust-policy.json`\. Replace `111122223333` with your account ID\. Replace `EXAMPLED539D4633E53DE1B71EXAMPLE` and `region-code` with the values returned in the previous step\. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-West\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:`\.

      ```
      {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect": "Allow",
            "Principal": {
              "Federated": "arn:aws:iam::111122223333:oidc-provider/oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
              "StringLike": {
                "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:sub": "system:serviceaccount:kube-system:efs-csi-*",
                "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:aud": "sts.amazonaws.com"
              }
            }
          }
        ]
      }
      ```

   1. Create the role\. You can change `AmazonEKS_EFS_CSI_DriverRole` to a different name, but if you do, make sure to change it in later steps too\.

      ```
      aws iam create-role \
        --role-name AmazonEKS_EFS_CSI_DriverRole \
        --assume-role-policy-document file://"aws-efs-csi-driver-trust-policy.json"
      ```

1. Attach the required AWS managed policy to the role with the following command\. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-West\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:`\.

   ```
   aws iam attach-role-policy \
     --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEFSCSIDriverPolicy \
     --role-name AmazonEKS_EFS_CSI_DriverRole
   ```

------

## Installing the Amazon EFS CSI driver<a name="efs-install-driver"></a>

We recommend that you install the Amazon EFS CSI driver through the Amazon EKS add\-on\. To add an Amazon EKS add\-on to your cluster, see [Creating an add\-on](managing-add-ons.md#creating-an-add-on)\. For more information about add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\. If you're unable to use the Amazon EKS add\-on, we encourage you to submit an issue about why you can't to the [Containers roadmap GitHub repository](https://github.com/aws/containers-roadmap/issues)\.

Alternatively, if you want a self\-managed installation of the Amazon EFS CSI driver, see [Installation](https://github.com/kubernetes-sigs/aws-efs-csi-driver/blob/master/docs/README.md#installation) on GitHub\.

## Creating an Amazon EFS file system<a name="efs-create-filesystem"></a>

To create an Amazon EFS file system, see [Create an Amazon EFS file system for Amazon EKS](https://github.com/kubernetes-sigs/aws-efs-csi-driver/blob/master/docs/efs-create-filesystem.md) on GitHub\.

## Deploying a sample application<a name="efs-sample-app"></a>

You can deploy a variety of sample apps and modify them as needed\. For more information, see [Examples](https://github.com/kubernetes-sigs/aws-efs-csi-driver/blob/master/docs/README.md#examples) on GitHub\.