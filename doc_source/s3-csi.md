# Mountpoint for Amazon S3 CSI driver<a name="s3-csi"></a>

With the [Mountpoint for Amazon S3 Container Storage Interface \(CSI\) driver](https://github.com/awslabs/mountpoint-s3-csi-driver), your Kubernetes applications can access S3 objects through a file system interface, achieving high aggregate throughput without changing any application code\. Built on [Mountpoint for Amazon S3](https://github.com/awslabs/mountpoint-s3), the CSI driver presents an Amazon S3 bucket as a volume that can be accessed by containers in Amazon EKS and self\-managed Kubernetes clusters\. This topic shows you how to deploy the Mountpoint for Amazon S3 CSI driver to your Amazon EKS cluster\.

**Considerations**
+ The Mountpoint for Amazon S3 CSI driver isn't presently compatible with Windows\-based container images\.
+ The Mountpoint for Amazon S3 CSI driver doesn't support AWS Fargate\. However, containers that are running in Amazon EC2 \(either with Amazon EKS or a custom Kubernetes installation\) are supported\.
+ The Mountpoint for Amazon S3 CSI driver supports only static provisioning\. Dynamic provisioning, or creation of new buckets, isn't supported\.
**Note**  
Static provisioning refers to using an existing S3 bucket that is specified as the `bucketName` in the `volumeHandle` in the `PersistentVolume` object\. For more information, see [Static Provisioning](https://github.com/awslabs/mountpoint-s3-csi-driver/blob/main/examples/kubernetes/static_provisioning/README.md) on GitHub\.
+ Volumes mounted with the Mountpoint for Amazon S3 CSI driver don't support all POSIX file\-system features\. For details about file\-system behavior, see [Mountpoint for Amazon S3 file system behavior](https://github.com/awslabs/mountpoint-s3/blob/main/doc/SEMANTICS.md) on GitHub\.

**Prerequisites**
+ An existing AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see [Creating an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ Version 2\.12\.3 or later of the AWS CLI installed and configured on your device or AWS CloudShell\.
+ The `kubectl` command line tool is installed on your device or AWS CloudShell\. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster\. For example, if your cluster version is `1.27`, you can use `kubectl` version `1.26`, `1.27`, or `1.28` with it\. To install or upgrade `kubectl`, see [Installing or updating `kubectl`](install-kubectl.md)\.

## Creating an IAM policy<a name="s3-create-iam-policy"></a>

The Mountpoint for Amazon S3 CSI driver requires Amazon S3 permissions to interact with your file system\. This section shows how to create an IAM policy that grants the necessary permissions\.

The following example policy follows the IAM permission recommendations for Mountpoint\. Alternatively, you can use the AWS managed policy [https://console.aws.amazon.com/iam/home?#/policies/arn:aws:iam::aws:policy/AmazonS3FullAccess$jsonEditor](https://console.aws.amazon.com/iam/home?#/policies/arn:aws:iam::aws:policy/AmazonS3FullAccess$jsonEditor), but this managed policy grants more permissions than are needed for Mountpoint\. 

For more information about the recommended permissions for Mountpoint, see [Mountpoint IAM permissions](https://github.com/awslabs/mountpoint-s3/blob/main/doc/CONFIGURATION.md#iam-permissions) on GitHub\.

**Create an IAM policy with the IAM console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the left navigation pane, choose **Policies**\.

1. On the **Policies** page, choose **Create policy**\.

1. For **Policy editor**, choose **JSON**\.

1. Under **Policy editor**, copy and paste the following:
**Important**  
Replace `DOC-EXAMPLE-BUCKET1` with your own Amazon S3 bucket name\.

   ```
   {
      "Version": "2012-10-17",
      "Statement": [
           {
               "Sid": "MountpointFullBucketAccess",
               "Effect": "Allow",
               "Action": [
                   "s3:ListBucket"
               ],
               "Resource": [
                   "arn:aws:s3:::DOC-EXAMPLE-BUCKET1"
               ]
           },
           {
               "Sid": "MountpointFullObjectAccess",
               "Effect": "Allow",
               "Action": [
                   "s3:GetObject",
                   "s3:PutObject",
                   "s3:AbortMultipartUpload",
                   "s3:DeleteObject"
               ],
               "Resource": [
                   "arn:aws:s3:::DOC-EXAMPLE-BUCKET1/*"
               ]
           }
      ]
   }
   ```

1. Choose **Next**\.

1. On the **Review and create** page, name your policy\. This example walkthrough uses the name `AmazonS3CSIDriverPolicy`\.

1. Choose **Create policy**\.

## Creating an IAM role<a name="s3-create-iam-role"></a>

The Mountpoint for Amazon S3 CSI driver requires Amazon S3 permissions to interact with your file system\. This section shows how to create an IAM role to delegate these permissions\. To create this role, you can use `eksctl`, the IAM console, or the AWS CLI\.

**Note**  
The IAM policy `AmazonS3CSIDriverPolicy` was created in the previous section\.

For more information, see [Set up driver permissions](https://github.com/kubernetes-sigs/aws-efs-csi-driver#set-up-driver-permission) on GitHub\.

------
#### [ eksctl ]

**To create your Mountpoint for Amazon S3 CSI driver IAM role with `eksctl`**

To create the IAM role and the Kubernetes service account, run the following commands\. These commands also attach the `AmazonS3CSIDriverPolicy` IAM policy to the role, annotate the Kubernetes service account \(`s3-csi-controller-sa`\) with the IAM role's Amazon Resource Name \(ARN\), and add the Kubernetes service account name to the trust policy for the IAM role\.

```
CLUSTER_NAME=my-cluster
REGION=region-code
ROLE_NAME=AmazonEKS_S3_CSI_DriverRole
POLICY_ARN=AmazonEKS_S3_CSI_DriverRole_ARN
eksctl create iamserviceaccount \
    --name s3-csi-driver-sa \
    --namespace kube-system \
    --cluster $CLUSTER_NAME \
    --attach-policy-arn $POLICY_ARN \
    --approve \
    --role-name $ROLE_NAME \
    --region $REGION
```

------
#### [ IAM console ]

**To create your Mountpoint for Amazon S3 CSI driver IAM role with the AWS Management Console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the left navigation pane, choose **Roles**\.

1. On the **Roles** page, choose **Create role**\.

1. On the **Select trusted entity** page, do the following:

   1. In the **Trusted entity type** section, choose **Web identity**\.

   1. For **Identity provider**, choose the **OpenID Connect provider URL** for your cluster \(as shown under **Overview** in Amazon EKS\)\.

      If no URLs are shown, review the [Prerequisites](#prereqs) section\.

   1. For **Audience**, choose `sts.amazonaws.com`\.

   1. Choose **Next**\.

1. On the **Add permissions** page, do the following:

   1. In the **Filter policies** box, enter **AmazonS3CSIDriverPolicy**\.
**Note**  
This policy was created in the previous section\.

   1. Select the check box to the left of the `AmazonS3CSIDriverPolicy` result that was returned in the search\.

   1. Choose **Next**\.

1. On the **Name, review, and create** page, do the following:

   1. For **Role name**, enter a unique name for your role, such as **AmazonEKS\_S3\_CSI\_DriverRole**\.

   1. Under **Add tags \(Optional\)**, add metadata to the role by attaching tags as key\-value pairs\. For more information about using tags in IAM, see [Tagging IAM resources](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html) in the *IAM User Guide*\.

   1. Choose **Create role**\.

1. After the role is created, choose the role in the console to open it for editing\.

1. Choose the **Trust relationships** tab, and then choose **Edit trust policy**\.

1. Find the line that looks similar to the following:

   ```
   "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:aud": "sts.amazonaws.com"
   ```

   Add a comma to the end of the previous line, and then add the following line after it\. Replace `region-code` with the AWS Region that your cluster is in\. Replace `EXAMPLED539D4633E53DE1B71EXAMPLE` with your cluster's OIDC provider ID\.

   ```
   "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:sub": "system:serviceaccount:kube-system:s3-csi-*"
   ```

1. Change the `Condition` operator from `"StringEquals"` to `"StringLike"`\.

1. Choose **Update policy** to finish\.

------
#### [ AWS CLI ]

**To create your Mountpoint for Amazon S3 CSI driver IAM role with the AWS CLI**

1. View the OIDC provider URL for your cluster\. Replace `my-cluster` with the name of your cluster\. If the output from the command is `None`, review the [Prerequisites](#prereqs)\.

   ```
   aws eks describe-cluster --name my-cluster --query "cluster.identity.oidc.issuer" --output text
   ```

   An example output is as follows\.

   ```
   https://oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE
   ```

1. Create the IAM role, granting the Kubernetes service account the `AssumeRoleWithWebIdentity` action\.

   1. Copy the following contents to a file named `aws-s3-csi-driver-trust-policy.json`\. Replace `111122223333` with your account ID\. Replace `EXAMPLED539D4633E53DE1B71EXAMPLE` and `region-code` with the values returned in the previous step\.

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
                "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:sub": "system:serviceaccount:kube-system:s3-csi-*",
                "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:aud": "sts.amazonaws.com"
              }
            }
          }
        ]
      }
      ```

   1. Create the role\. You can change `AmazonEKS_S3_CSI_DriverRole` to a different name, but if you do, make sure to change it in later steps too\.

      ```
      aws iam create-role \
        --role-name AmazonEKS_S3_CSI_DriverRole \
        --assume-role-policy-document file://"aws-s3-csi-driver-trust-policy.json"
      ```

1. Attach the previously created IAM policy to the role with the following command\.

   ```
   aws iam attach-role-policy \
     --policy-arn arn:aws:iam::aws:policy/AmazonS3CSIDriverPolicy \
     --role-name AmazonEKS_S3_CSI_DriverRole
   ```
**Note**  
The IAM policy `AmazonS3CSIDriverPolicy` was created in the previous section\.

1. Skip this step if you're installing the driver as an Amazon EKS add\-on\. For self\-managed installations of the driver, create Kubernetes service accounts that are annotated with the ARN of the IAM role that you created\.

   1. Save the following contents to a file named `mountpoint-s3-service-account.yaml`\. Replace `111122223333` with your account ID\.

      ```
      ---
      apiVersion: v1
      kind: ServiceAccount
      metadata:
        labels:
          app.kubernetes.io/name: aws-mountpoint-s3-csi-driver
        name: mountpoint-s3-csi-controller-sa
        namespace: kube-system
        annotations:
          eks.amazonaws.com/role-arn: arn:aws:iam::111122223333:role/AmazonEKS_S3_CSI_DriverRole
      ```

   1. Create the Kubernetes service account on your cluster\. The Kubernetes service account \(`mountpoint-s3-csi-controller-sa`\) is annotated with the IAM role that you created named `AmazonEKS_S3_CSI_DriverRole`\.

      ```
      kubectl apply -f mountpoint-s3-service-account.yaml
      ```
**Note**  
When you deploy the plugin in this procedure, it creates and is configured to use a service account named `s3-csi-driver-sa`\. 

------

## Installing the Mountpoint for Amazon S3 CSI driver<a name="s3-install-driver"></a>

You may install the Mountpoint for Amazon S3 CSI driver through the Amazon EKS add\-on\. To add an Amazon EKS add\-on to your cluster, see [Creating an add\-on](managing-add-ons.md#creating-an-add-on)\. For more information about add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\.

For instructions on doing a self\-managed installation, see [Installation](https://github.com/awslabs/mountpoint-s3-csi-driver/blob/main/docs/install.md#deploy-driver) on GitHub\.

## Configuring Mountpoint for Amazon S3<a name="s3-configure-mountpoint"></a>

In most cases, you can configure Mountpoint for Amazon S3 with only a bucket name\. For instructions on configuring Mountpoint for Amazon S3, see [Configuring Mountpoint for Amazon S3](https://github.com/awslabs/mountpoint-s3/blob/main/doc/CONFIGURATION.md) on GitHub\.

## Deploying a sample application<a name="s3-sample-app"></a>

You can deploy static provisioning to the driver on an existing Amazon S3 bucket\. For more information, see [Static provisioning](https://github.com/awslabs/mountpoint-s3-csi-driver/blob/main/examples/kubernetes/static_provisioning/README.md) on GitHub\.