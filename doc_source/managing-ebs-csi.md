# Managing the Amazon EBS CSI driver as an Amazon EKS add\-on<a name="managing-ebs-csi"></a>

To improve security and reduce the amount of work, you can manage the Amazon EBS CSI driver as an Amazon EKS add\-on\. For information about Amazon EKS add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\. You can add the Amazon EBS CSI add\-on by following the steps in [Adding the Amazon EBS CSI driver add\-on](#adding-ebs-csi-eks-add-on)\.

If you added the Amazon EBS CSI add\-on, you can manage it by following the steps in the [Updating the Amazon EBS CSI driver as an Amazon EKS add\-on](#updating-ebs-csi-eks-add-on) and [Removing the Amazon EBS CSI add\-on](#removing-ebs-csi-eks-add-on) sections\.

**Prerequisites**
+ An existing cluster\. To see the required platform version, run the following command\.

  ```
  aws eks describe-addon-versions --addon-name aws-ebs-csi-driver
  ```
+ An existing AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ An Amazon EBS CSI driver IAM role\. If you don't satisfy this prerequisite, attempting to install the add\-on and running `kubectl describe pvc` will show `failed to provision volume with StorageClass` along with a `could not create volume in EC2: UnauthorizedOperation` error\. For more information, see [Creating the Amazon EBS CSI driver IAM role](csi-iam-role.md)\.
+ If you're using a cluster wide restricted [`PodSecurityPolicy`](pod-security-policy.md), make sure that the add\-on is granted sufficient permissions to be deployed\. For the permissions required by each add\-on Pod, see the [relevant add\-on manifest definition](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/tree/master/deploy/kubernetes/base) on GitHub\.

**Important**  
To use the snapshot functionality of the Amazon EBS CSI driver, you must install the external snapshotter before the installation of the add\-on\. The external snapshotter components must be installed in the following order:  
`[CustomResourceDefinition](https://github.com/kubernetes-csi/external-snapshotter/tree/master/client/config/crd)` \(CRD\) for `volumesnapshotclasses`, `volumesnapshots`, and `volumesnapshotcontents`
[RBAC](https://github.com/kubernetes-csi/external-snapshotter/blob/master/deploy/kubernetes/snapshot-controller/rbac-snapshot-controller.yaml) \(`ClusterRole`, `ClusterRoleBinding`, and so on\)
[controller deployment](https://github.com/kubernetes-csi/external-snapshotter/blob/master/deploy/kubernetes/snapshot-controller/setup-snapshot-controller.yaml)
For more information, see [CSI Snapshotter](https://github.com/kubernetes-csi/external-snapshotter) on GitHub\.

## Adding the Amazon EBS CSI driver add\-on<a name="adding-ebs-csi-eks-add-on"></a>

**Important**  
Before adding the Amazon EBS driver as an Amazon EKS add\-on, confirm that you don't have a self\-managed version of the driver installed on your cluster\. If so, see [ Uninstalling a self\-managed Amazon EBS CSI driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/docs/install.md#uninstalling-the-ebs-csi-driver) on GitHub\. 

You can use `eksctl`, the AWS Management Console, or the AWS CLI to add the Amazon EBS CSI add\-on to your cluster\.

------
#### [ eksctl ]

**To add the Amazon EBS CSI add\-on using `eksctl`**  
Run the following command\. Replace `my-cluster` with the name of your cluster, `111122223333` with your account ID, and `AmazonEKS_EBS_CSI_DriverRole` with the name of the [IAM role created earlier](csi-iam-role.md)\. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-West\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:`\.

```
eksctl create addon --name aws-ebs-csi-driver --cluster my-cluster --service-account-role-arn arn:aws:iam::111122223333:role/AmazonEKS_EBS_CSI_DriverRole --force
```

If you remove the **\-\-*force*** option and any of the Amazon EKS add\-on settings conflict with your existing settings, then updating the Amazon EKS add\-on fails, and you receive an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\. For more information about other options for this setting, see [Addons](https://eksctl.io/usage/addons/) in the `eksctl` documentation\. For more information about Amazon EKS Kubernetes field management, see [ Kubernetes field management](kubernetes-field-management.md)\.

------
#### [ AWS Management Console ]

**To add the Amazon EBS CSI add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, choose **Clusters**\.

1. Choose the name of the cluster that you want to configure the Amazon EBS CSI add\-on for\.

1. Choose the **Add\-ons** tab\.

1. Choose **Get more add\-ons**\.

1. On the **Select add\-ons** page, do the following:

   1. In the **Amazon EKS\-addons** section, select the **Amazon EBS CSI Driver** check box\.

   1. Choose **Next**\.

1. On the **Configure selected add\-ons settings** page, do the following:

   1. Select the **Version** you'd like to use\.

   1. For **Select IAM role**, select the name of an IAM role that you attached the Amazon EBS CSI driver IAM policy to\.

   1. \(Optional\) You can expand the **Optional configuration settings**\. If you select **Override** for the **Conflict resolution method**, one or more of the settings for the existing add\-on can be overwritten with the Amazon EKS add\-on settings\. If you don't enable this option and there's a conflict with your existing settings, the operation fails\. You can use the resulting error message to troubleshoot the conflict\. Before selecting this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to self\-manage\.

   1. Choose **Next**\.

1. On the **Review and add** page, choose **Create**\. After the add\-on installation is complete, you see your installed add\-on\.

------
#### [ AWS CLI ]

**To add the Amazon EBS CSI add\-on using the AWS CLI**  
Run the following command\. Replace `my-cluster` with the name of your cluster, `111122223333` with your account ID, and `AmazonEKS_EBS_CSI_DriverRole` with the name of the role that was created earlier\. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-West\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:`\.

```
aws eks create-addon --cluster-name my-cluster --addon-name aws-ebs-csi-driver \
  --service-account-role-arn arn:aws:iam::111122223333:role/AmazonEKS_EBS_CSI_DriverRole
```

------

Now that you have added the Amazon EBS CSI driver as an Amazon EKS add\-on, you can continue to [Deploy a sample application and verify that the CSI driver is working](ebs-sample-app.md)\. That procedure includes setting up the storage class\.

## Updating the Amazon EBS CSI driver as an Amazon EKS add\-on<a name="updating-ebs-csi-eks-add-on"></a>

Amazon EKS doesn't automatically update Amazon EBS CSI for your cluster when new versions are released or after you [update your cluster](update-cluster.md) to a new Kubernetes minor version\. To update Amazon EBS CSI on an existing cluster, you must initiate the update and then Amazon EKS updates the add\-on for you\.

------
#### [ eksctl ]

**To update the Amazon EBS CSI add\-on using `eksctl`**

1. Check the current version of your Amazon EBS CSI add\-on\. Replace `my-cluster` with your cluster name\.

   ```
   eksctl get addon --name aws-ebs-csi-driver --cluster my-cluster
   ```

   An example output is as follows\.

   ```
   NAME                    VERSION                      STATUS  ISSUES  IAMROLE UPDATE AVAILABLE
   aws-ebs-csi-driver      v1.11.2-eksbuild.1           ACTIVE  0               v1.11.4-eksbuild.1
   ```

1. Update the add\-on to the version returned under `UPDATE AVAILABLE` in the output of the previous step\.

   ```
   eksctl update addon --name aws-ebs-csi-driver --version v1.11.4-eksbuild.1 --cluster my-cluster \
     --service-account-role-arn arn:aws:iam::111122223333:role/AmazonEKS_EBS_CSI_DriverRole --force
   ```

   If you remove the **\-\-*force*** option and any of the Amazon EKS add\-on settings conflict with your existing settings, then updating the Amazon EKS add\-on fails, and you receive an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\. For more information about other options for this setting, see [Addons](https://eksctl.io/usage/addons/) in the `eksctl` documentation\. For more information about Amazon EKS Kubernetes field management, see [ Kubernetes field management](kubernetes-field-management.md)\.

------
#### [ AWS Management Console ]

**To update the Amazon EBS CSI add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, choose **Clusters**\.

1. Choose the name of the cluster that you want to update the Amazon EBS CSI add\-on for\. 

1. Choose the **Add\-ons** tab\.

1. Choose **Amazon EBS CSI Driver**\.

1. Choose **Edit**\.

1. On the **Configure Amazon EBS CSI Driver** page, do the following:

   1. Select the **Version** you'd like to use\.

   1. For **Select IAM role**, select the name of an IAM role that you attached the Amazon EBS CSI driver IAM policy to\.

   1. \(Optional\) You can expand the **Optional configuration settings** and modify as needed\.

   1. Choose **Save changes**\.

------
#### [ AWS CLI ]

**To update the Amazon EBS CSI add\-on using the AWS CLI**

1. Check the current version of your Amazon EBS CSI add\-on\. Replace `my-cluster` with your cluster name\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name aws-ebs-csi-driver --query "addon.addonVersion" --output text
   ```

   An example output is as follows\.

   ```
   v1.11.2-eksbuild.1
   ```

1. Determine which versions of the Amazon EBS CSI add\-on are available for your cluster version\.

   ```
   aws eks describe-addon-versions --addon-name aws-ebs-csi-driver --kubernetes-version 1.23 \
     --query "addons[].addonVersions[].[addonVersion, compatibilities[].defaultVersion]" --output text
   ```

   An example output is as follows\.

   ```
   v1.11.4-eksbuild.1
   True
   v1.11.2-eksbuild.1
   False
   ```

   The version with `True` underneath is the default version deployed when the add\-on is created\. The version deployed when the add\-on is created might not be the latest available version\. In the previous output, the latest version is deployed when the add\-on is created\.

1. Update the add\-on to the version with `True` that was returned in the output of the previous step\. If it was returned in the output, you can also update to a later version\.

   ```
   aws eks update-addon --cluster-name my-cluster --addon-name aws-ebs-csi-driver --addon-version v1.11.4-eksbuild.1 \
     --service-account-role-arn arn:aws:iam::111122223333:role/AmazonEKS_EBS_CSI_DriverRole --resolve-conflicts PRESERVE
   ```

   The *PRESERVE* option preserves any custom settings that you've set for the add\-on\. For more information about other options for this setting, see [update\-addon](https://docs.aws.amazon.com/cli/latest/reference/eks/update-addon.html) in the Amazon EKS Command Line Reference\. For more information about Amazon EKS add\-on configuration management, see [ Kubernetes field management](kubernetes-field-management.md)\.

------

## Removing the Amazon EBS CSI add\-on<a name="removing-ebs-csi-eks-add-on"></a>

You have two options for removing an Amazon EKS add\-on\.
+ **Preserve add\-on software on your cluster** – This option removes Amazon EKS management of any settings\. It also removes the ability for Amazon EKS to notify you of updates and automatically update the Amazon EKS add\-on after you initiate an update\. However, it preserves the add\-on software on your cluster\. This option makes the add\-on a self\-managed installation, rather than an Amazon EKS add\-on\. With this option, there's no downtime for the add\-on\. The commands in this procedure use this option\.
+ **Remove add\-on software entirely from your cluster** – We recommend that you remove the Amazon EKS add\-on from your cluster only if there are no resources on your cluster that are dependent on it\. To do this option, delete `--preserve` from the command you use in this procedure\.

If the add\-on has an IAM account associated with it, the IAM account isn't removed\.

You can use `eksctl`, the AWS Management Console, or the AWS CLI to remove the Amazon EBS CSI add\-on\.

------
#### [ eksctl ]

**To remove the Amazon EBS CSI add\-on using `eksctl`**  
Replace `my-cluster` with the name of your cluster, and then run the following command\.

```
eksctl delete addon --cluster my-cluster --name aws-ebs-csi-driver --preserve
```

------
#### [ AWS Management Console ]

**To remove the Amazon EBS CSI add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, choose **Clusters**\.

1. Choose the name of the cluster that you want to remove the Amazon EBS CSI add\-on for\.

1. Choose the **Add\-ons** tab\.

1. Choose **Amazon EBS CSI Driver**\.

1. Choose **Remove**\.

1. In the **Remove: aws\-ebs\-csi\-driver** confirmation dialog box, do the following:

   1. If you want Amazon EKS to stop managing settings for the add\-on, select **Preserve on cluster**\. Do this if you want to retain the add\-on software on your cluster\. This is so that you can manage all of the settings of the add\-on on your own\.

   1. Enter **`aws-ebs-csi-driver`**\.

   1. Select **Remove**\.

------
#### [ AWS CLI ]

**To remove the Amazon EBS CSI add\-on using the AWS CLI**  
Replace `my-cluster` with the name of your cluster, and then run the following command\.

```
aws eks delete-addon --cluster-name my-cluster --addon-name aws-ebs-csi-driver --preserve
```

------