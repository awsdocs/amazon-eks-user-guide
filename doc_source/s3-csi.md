# Mountpoint for Amazon S3 CSI driver<a name="s3-csi"></a>

With the [Mountpoint for Amazon S3 Container Storage Interface \(CSI\) driver](https://github.com/awslabs/mountpoint-s3-csi-driver), your Kubernetes applications can access Amazon S3 objects through a file system interface, achieving high aggregate throughput without changing any application code\. Built on [Mountpoint for Amazon S3](https://github.com/awslabs/mountpoint-s3), the CSI driver presents an Amazon S3 bucket as a volume that can be accessed by containers in Amazon EKS and self\-managed Kubernetes clusters\.  This topic shows you how to deploy the Mountpoint for Amazon S3 CSI driver to your Amazon EKS cluster\.

**Considerations**
+ The Mountpoint for Amazon S3 CSI driver isn't presently compatible with Windows\-based container images\.
+ The Mountpoint for Amazon S3 CSI driver doesn't support AWS Fargate\. However, containers that are running in Amazon EC2 \(either with Amazon EKS or a custom Kubernetes installation\) are supported\.
+ The Mountpoint for Amazon S3 CSI driver supports only static provisioning\. Dynamic provisioning, or creation of new buckets, isn't supported\.
**Note**  
Static provisioning refers to using an existing Amazon S3 bucket that is specified as the `bucketName` in the `volumeHandle` in the `PersistentVolume` object\. For more information, see [Static Provisioning](https://github.com/awslabs/mountpoint-s3-csi-driver/blob/main/examples/kubernetes/static_provisioning/README.md) on GitHub\.
+ Volumes mounted with the Mountpoint for Amazon S3 CSI driver don't support all POSIX file\-system features\. For details about file\-system behavior, see [Mountpoint for Amazon S3 file system behavior](https://github.com/awslabs/mountpoint-s3/blob/main/doc/SEMANTICS.md) on GitHub\.

**Prerequisites**
+ An existing AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ Version 2\.12\.3 or later of the AWS CLI installed and configured on your device or AWS CloudShell\.
+ The `kubectl` command line tool is installed on your device or AWS CloudShell\. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster\. For example, if your cluster version is `1.28`, you can use `kubectl` version `1.27`, `1.28`, or `1.29` with it\. To install or upgrade `kubectl`, see [Installing or updating `kubectl`](install-kubectl.md)\.

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

   Directory buckets, introduced with the Amazon S3 Express One Zone storage class, use a different authentication mechanism from general purpose buckets\. Instead of using `s3:*` actions, you should use the `s3express:CreateSession` action\. For information about directory buckets, see [Directory buckets](https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-buckets-overview.html) in the *Amazon S3 User Guide*\.

   Below is an example of least\-privilege policy that you would use for a directory bucket\.

   ```
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": "s3express:CreateSession",
               "Resource": "arn:aws:s3express:aws-region:111122223333:bucket/DOC-EXAMPLE-BUCKET1--az_id--x-s3"
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
    --region $REGION \
    --role-only
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

You may install the Mountpoint for Amazon S3 CSI driver through the Amazon EKS add\-on\. You can use `eksctl`, the AWS Management Console, or the AWS CLI to add the add\-on to your cluster\.

You may optionally install Mountpoint for Amazon S3 CSI driver as a self\-managed installation\. For instructions on doing a self\-managed installation, see [Installation](https://github.com/awslabs/mountpoint-s3-csi-driver/blob/main/docs/install.md#deploy-driver) on GitHub\.

------
#### [ eksctl ]

**To add the Amazon S3 CSI add\-on using `eksctl`**  
Run the following command\. Replace `my-cluster` with the name of your cluster, `111122223333` with your account ID, and `AmazonEKS_S3_CSI_DriverRole` with the name of the [IAM role created earlier](#s3-create-iam-role)\.

```
eksctl create addon --name aws-mountpoint-s3-csi-driver --cluster my-cluster --service-account-role-arn arn:aws:iam::111122223333:role/AmazonEKS_S3_CSI_DriverRole --force
```

If you remove the **\-\-*force*** option and any of the Amazon EKS add\-on settings conflict with your existing settings, then updating the Amazon EKS add\-on fails, and you receive an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\. For more information about other options for this setting, see [Addons](https://eksctl.io/usage/addons/) in the `eksctl` documentation\. For more information about Amazon EKS Kubernetes field management, see [ Kubernetes field management](kubernetes-field-management.md)\.

------
#### [ AWS Management Console ]

**To add the Mountpoint for Amazon S3 CSI add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, choose **Clusters**\.

1. Choose the name of the cluster that you want to configure the Mountpoint for Amazon S3 CSI add\-on for\.

1. Choose the **Add\-ons** tab\.

1. Choose **Get more add\-ons**\.

1. On the **Select add\-ons** page, do the following:

   1. In the **Amazon EKS\-addons** section, select the **Mountpoint for Amazon S3 CSI Driver** check box\.

   1. Choose **Next**\.

1. On the **Configure selected add\-ons settings** page, do the following:

   1. Select the **Version** you'd like to use\.

   1. For **Select IAM role**, select the name of an IAM role that you attached the Mountpoint for Amazon S3 CSI driver IAM policy to\.

   1. \(Optional\) You can expand the **Optional configuration settings**\. If you select **Override** for the **Conflict resolution method**, one or more of the settings for the existing add\-on can be overwritten with the Amazon EKS add\-on settings\. If you don't enable this option and there's a conflict with your existing settings, the operation fails\. You can use the resulting error message to troubleshoot the conflict\. Before selecting this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to self\-manage\.

   1. Choose **Next**\.

1. On the **Review and add** page, choose **Create**\. After the add\-on installation is complete, you see your installed add\-on\.

------
#### [ AWS CLI ]

**To add the Mountpoint for Amazon S3 CSI add\-on using the AWS CLI**  
Run the following command\. Replace `my-cluster` with the name of your cluster, `111122223333` with your account ID, and `AmazonEKS_S3_CSI_DriverRole` with the name of the role that was created earlier\.

```
aws eks create-addon --cluster-name my-cluster --addon-name aws-mountpoint-s3-csi-driver \
  --service-account-role-arn arn:aws:iam::111122223333:role/AmazonEKS_S3_CSI_DriverRole
```

------

## Configuring Mountpoint for Amazon S3<a name="s3-configure-mountpoint"></a>

In most cases, you can configure Mountpoint for Amazon S3 with only a bucket name\. For instructions on configuring Mountpoint for Amazon S3, see [Configuring Mountpoint for Amazon S3](https://github.com/awslabs/mountpoint-s3/blob/main/doc/CONFIGURATION.md) on GitHub\.

## Deploying a sample application<a name="s3-sample-app"></a>

You can deploy static provisioning to the driver on an existing Amazon S3 bucket\. For more information, see [Static provisioning](https://github.com/awslabs/mountpoint-s3-csi-driver/blob/main/examples/kubernetes/static_provisioning/README.md) on GitHub\.

## Removing Mountpoint for Amazon S3 CSI Driver<a name="removing-s3-csi-eks-add-on"></a>

You have two options for removing an Amazon EKS add\-on\.
+ **Preserve add\-on software on your cluster** – This option removes Amazon EKS management of any settings\. It also removes the ability for Amazon EKS to notify you of updates and automatically update the Amazon EKS add\-on after you initiate an update\. However, it preserves the add\-on software on your cluster\. This option makes the add\-on a self\-managed installation, rather than an Amazon EKS add\-on\. With this option, there's no downtime for the add\-on\. The commands in this procedure use this option\.
+ **Remove add\-on software entirely from your cluster** – We recommend that you remove the Amazon EKS add\-on from your cluster only if there are no resources on your cluster that are dependent on it\. To do this option, delete `--preserve` from the command you use in this procedure\.

If the add\-on has an IAM account associated with it, the IAM account isn't removed\.

You can use `eksctl`, the AWS Management Console, or the AWS CLI to remove the Amazon S3 CSI add\-on\.

------
#### [ eksctl ]

**To remove the Amazon S3 CSI add\-on using `eksctl`**  
Replace `my-cluster` with the name of your cluster, and then run the following command\.

```
eksctl delete addon --cluster my-cluster --name aws-mountpoint-s3-csi-driver --preserve
```

------
#### [ AWS Management Console ]

**To remove the Amazon S3 CSI add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, choose **Clusters**\.

1. Choose the name of the cluster that you want to remove the Amazon EBS CSI add\-on for\.

1. Choose the **Add\-ons** tab\.

1. Choose **Mountpoint for Amazon S3 CSI Driver**\.

1. Choose **Remove**\.

1. In the **Remove: aws\-mountpoint\-s3\-csi\-driver** confirmation dialog box, do the following:

   1. If you want Amazon EKS to stop managing settings for the add\-on, select **Preserve on cluster**\. Do this if you want to retain the add\-on software on your cluster\. This is so that you can manage all of the settings of the add\-on on your own\.

   1. Enter **`aws-mountpoint-s3-csi-driver`**\.

   1. Select **Remove**\.

------
#### [ AWS CLI ]

**To remove the Amazon S3 CSI add\-on using the AWS CLI**  
Replace `my-cluster` with the name of your cluster, and then run the following command\.

```
aws eks delete-addon --cluster-name my-cluster --addon-name aws-mountpoint-s3-csi-driver --preserve
```

------