# Managing the Amazon EBS CSI driver as an Amazon EKS add\-on<a name="managing-ebs-csi"></a>

To improve security and reduce the amount of work, you can manage the Amazon EBS CSI driver as an Amazon EKS add\-on\. For information about Amazon EKS add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\. You can add the Amazon EBS CSI add\-on by following the steps in [Adding the Amazon EBS CSI add\-on](#adding-ebs-csi-eks-add-on)\.

If you added the Amazon EBS CSI add\-on, you can manage it by following the steps in the [Updating the Amazon EBS CSI driver as an Amazon EKS add\-on](#updating-ebs-csi-eks-add-on) and [Removing the Amazon EBS CSI add\-on](#removing-ebs-csi-eks-add-on) sections\.

**Prerequisites**
+ An existing cluster\. To see the required platform version, run the following command\.

  ```
  aws eks describe-addon-versions --addon-name aws-ebs-csi-driver
  ```
+ An existing AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see [Creating an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ An Amazon EBS CSI driver IAM role\. If you don't satisfy this prerequisite, attempting to install the add\-on and running `kubectl descibe pvc` will show `failed to provision volume with StorageClass` along with a `could not create volume in EC2: UnauthorizedOperation` error\. For more information, see [Creating the Amazon EBS CSI driver IAM role for service accounts](csi-iam-role.md)\.
+ If you're using a cluster wide restricted [`PodSecurityPolicy`](pod-security-policy.md), make sure that the add\-on is granted sufficient permissions to be deployed\. For the permissions required by each add\-on pod, see the [relevant add\-on manifest definition](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/tree/master/deploy/kubernetes/base) on GitHub\.

**Important**  
To use the snapshot functionality of the Amazon EBS CSI driver, you must install the external snapshotter before the installation of the add\-on\. The external snapshotter components must be installed in the following order:  
`[CustomResourceDefinition](https://github.com/kubernetes-csi/external-snapshotter/tree/master/client/config/crd)` \(CRD\) for `volumesnapshotclasses`, `volumesnapshots`, and `volumesnapshotcontents`
[RBAC](https://github.com/kubernetes-csi/external-snapshotter/blob/master/deploy/kubernetes/snapshot-controller/rbac-snapshot-controller.yaml) \(`ClusterRole`, `ClusterRoleBinding`, and so on\)
[controller deployment](https://github.com/kubernetes-csi/external-snapshotter/blob/master/deploy/kubernetes/snapshot-controller/setup-snapshot-controller.yaml)
For more information, see [CSI Snapshotter](https://github.com/kubernetes-csi/external-snapshotter) on GitHub\.

**Note**  
The Amazon EBS CSI driver version 1\.12 and above has support for Windows Server 2022, but it hasn't been released as an add\-on\. To enable support, you can install the driver using Helm\. Refer to the [`aws-ebs-csi-driver` Windows `README.md`](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/tree/master/examples/kubernetes/windows) on GitHub\.

## Adding the Amazon EBS CSI add\-on<a name="adding-ebs-csi-eks-add-on"></a>

**Important**  
Before adding the Amazon EBS CSI add\-on, confirm that you don't self\-manage any settings that Amazon EKS will start managing\. To determine which settings Amazon EKS manages, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

You can use `eksctl`, the AWS Management Console, or the AWS CLI to add the Amazon EBS CSI add\-on to your cluster \.

------
#### [ eksctl ]

**To add the Amazon EBS CSI add\-on using `eksctl`**  
Run the following command\. Replace `my-cluster` with the name of your cluster, `111122223333` with your account ID, and `AmazonEKS_EBS_CSI_DriverRole` with the name of the [IAM role created earlier](csi-iam-role.md)\. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-West\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:`\.

```
eksctl create addon --name aws-ebs-csi-driver --cluster my-cluster --service-account-role-arn arn:aws:iam::111122223333:role/AmazonEKS_EBS_CSI_DriverRole --force
```

If you remove the `--force` option and there's a conflict with your existing settings, the command fails\. You can use the resulting error message to troubleshoot the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to self\-manage\. This is because those settings are overwritten with this option\. For more information about managing Amazon EKS add\-ons, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------
#### [ AWS Management Console ]

**To add the Amazon EBS CSI add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, choose **Clusters**\.

1. Choose the name of the cluster that you want to configure the Amazon EBS CSI add\-on for\.

1. Choose the **Add\-ons** tab\.

1. Choose **Add new**\.

   1. Select **Amazon EBS CSI Driver** for **Name**\.

   1. Select the **Version** you'd like to use\.

   1. For **Service account role**, select the name of an IAM role that you attached the IAM policy to\.

   1. If you select **Override existing configuration for this add\-on on the cluster\.**, one or more of the settings for the existing add\-on can be overwritten with the Amazon EKS add\-on settings\. If you don't enable this option and there's a conflict with your existing settings, the operation fails\. You can use the resulting error message to troubleshoot the conflict\. Before selecting this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to self\-manage\. For more information about managing Amazon EKS add\-ons, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

   1. Choose **Add**\.

------
#### [ AWS CLI ]

**To add the Amazon EBS CSI add\-on using the AWS CLI**  
Run the following command\. Replace `my-cluster` with the name of your cluster, `111122223333` with your account ID, and `AmazonEKS_EBS_CSI_DriverRole` with the name of the role that was created earlier\. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-West\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:`\.

```
aws eks create-addon --cluster-name my-cluster --addon-name aws-ebs-csi-driver \
  --service-account-role-arn arn:aws:iam::111122223333:role/AmazonEKS_EBS_CSI_DriverRole
```

------

## Updating the Amazon EBS CSI driver as an Amazon EKS add\-on<a name="updating-ebs-csi-eks-add-on"></a>

Amazon EKS doesn't automatically update Amazon EBS CSI for your cluster when new versions are released or after you [update your cluster](update-cluster.md) to a new Kubernetes minor version\. To update Amazon EBS CSI on an existing cluster, you must initiate the update and then Amazon EKS updates the add\-on for you\.

**Important**  
Update your cluster and nodes to a new Kubernetes minor version before you update Amazon EBS CSI to the same minor version\.

------
#### [ eksctl ]

**To update the Amazon EBS CSI add\-on using `eksctl`**

1. Check the current version of your Amazon EBS CSI add\-on\. Replace `my-cluster` with your cluster name\.

   ```
   eksctl get addon --name aws-ebs-csi-driver --cluster my-cluster
   ```

   The example output is as follows\.

   ```
   NAME                    VERSION                      STATUS  ISSUES  IAMROLE UPDATE AVAILABLE
   aws-ebs-csi-driver      v1.11.2-eksbuild.1      ACTIVE  0               v1.11.4-eksbuild.1
   ```

1. Update the add\-on to the version returned under `UPDATE AVAILABLE` in the output of the previous step\.

   ```
   eksctl update addon --name aws-ebs-csi-driver --version v1.11.4-eksbuild.1 --cluster my-cluster --force
   ```

   If you remove the **\-\-*force*** option and any of the Amazon EKS add\-on settings conflict with your existing settings, then updating the Amazon EKS add\-on fails, and you receive an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\. For more information about other options for this setting, see [Addons](https://eksctl.io/usage/addons/) in the `eksctl` documentation\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------
#### [ AWS Management Console ]

**To update the Amazon EBS CSI add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, choose **Clusters**\.

1. Choose the name of the cluster that you want to update the Amazon EBS CSI add\-on for\. 

1. Choose the **Add\-ons** tab\.

1. Select the radio button in the upper right of the **aws\-ebs\-csi\-driver** box\.

1. Choose **Edit**\.

   1. Select the **Version** of the Amazon EKS add\-on that you want to use\.

   1. For **Service account role**, select the name of the IAM role that you've attached the Amazon EBS CSI driver IAM policy to\.

   1. For **Conflict resolution method**, select one of the options\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

   1. Select **Update**\.

------
#### [ AWS CLI ]

**To update the Amazon EBS CSI add\-on using the AWS CLI**

1. Check the current version of your Amazon EBS CSI add\-on\. Replace `my-cluster` with your cluster name\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name aws-ebs-csi-driver --query "addon.addonVersion" --output text
   ```

   The example output is as follows\.

   ```
   v1.11.2-eksbuild.1
   ```

1. Determine which versions of the Amazon EBS CSI add\-on are available for your cluster version\.

   ```
   aws eks describe-addon-versions --addon-name aws-ebs-csi-driver --kubernetes-version 1.23 \
     --query "addons[].addonVersions[].[addonVersion, compatibilities[].defaultVersion]" --output text
   ```

   The example output is as follows\.

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
     --resolve-conflicts PRESERVE
   ```

   The *PRESERVE* option preserves any custom settings that you've set for the add\-on\. For more information about other options for this setting, see [update\-addon](https://docs.aws.amazon.com/cli/latest/reference/eks/update-addon.html) in the Amazon EKS Command Line Reference\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------

## Removing the Amazon EBS CSI add\-on<a name="removing-ebs-csi-eks-add-on"></a>

You have two options for removing an Amazon EKS add\-on\.
+ **Preserve add\-on software on your cluster** – This option removes Amazon EKS management of any settings\. It also removes the ability for Amazon EKS to notify you of updates and automatically update the Amazon EKS add\-on after you initiate an update\. However, it preserves the add\-on software on your cluster\. This option makes the add\-on a self\-managed add\-on, rather than an Amazon EKS add\-on\. With this option, there's no downtime for the add\-on\. The commands in this procedure use this option\.
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

1. Select the radio button in the upper right of the **aws\-ebs\-csi\-driver** box\.

1. Choose **Remove**\.

1. Select **Preserve on cluster** if you want Amazon EKS to stop managing settings for the add\-on\. Do this if you want to retain the add\-on software on your cluster\. This is so that you can manage all of the settings of the add\-on on your own\.

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