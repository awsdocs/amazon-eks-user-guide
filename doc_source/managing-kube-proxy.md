# Managing the `kube-proxy` add\-on<a name="managing-kube-proxy"></a>

`Kube-proxy` maintains network rules on each Amazon EC2 node\. It enables network communication to your pods\. `Kube-proxy` is not deployed to Fargate nodes\. For more information, see [kube\-proxy](https://kubernetes.io/docs/concepts/overview/components/#kube-proxy) in the Kubernetes documentation\. Two versions of the `kube-proxy` image are available for each Kubernetes version\.
+ **Default** – The version deployed by default with new clusters\. This is the only version that you can use with the Amazon EKS add\-on\.
+ **Minimal** – Unlike the default version, this image version is based on a [minimal base image](https://gallery.ecr.aws/eks-distro-build-tooling/eks-distro-minimal-base-iptables) maintained by Amazon EKS Distro, which contains minimal packages and doesn't have shells\. For more information, see [Amazon EKS Distro](https://distro.eks.amazonaws.com/)\. This version is available as a self\-managed add\-on, but not as an Amazon EKS add\-on\. If you choose to install this version, complete the steps in Step 2 of [Updating the `kube-proxy` self\-managed add\-on](#updating-kube-proxy-add-on), specifying this version\.<a name="kube-proxy-default-versions-table"></a>


**`kube-proxy` image version for each Amazon EKS supported cluster version**  

| Kubernetes version | 1\.22 | 1\.21 | 1\.20 | 1\.19 | 1\.18 | 1\.17 | 
| --- | --- | --- | --- | --- | --- | --- | 
| kube\-proxy \(default version\) | 1\.22\.6\-eksbuild\.1 | 1\.21\.2\-eksbuild\.2 | 1\.20\.4\-eksbuild\.2 | 1\.19\.6\-eksbuild\.2 | 1\.18\.8\-eksbuild\.1 | 1\.17\.9\-eksbuild\.1 | 
| kube\-proxy \(minimal\) | 1\.22\.6\-minimal\-eksbuild\.2 | 1\.21\.9\-minimal\-eksbuild\.2 | 1\.20\.15\-minimal\-eksbuild\.2 | 1\.19\.16\-minimal\-eksbuild\.2 | 1\.18\.20\-minimal\-eksbuild\.1 | 1\.17\.17\-minimal\-eksbuild\.1 | 

If you have a 1\.18 or later cluster that you have not added the `kube-proxy` Amazon EKS add\-on to, you can add it using the procedure in [Adding the `kube-proxy` Amazon EKS add\-on](#adding-kube-proxy-eks-add-on)\. If you created your 1\.18 or later cluster using the AWS Management Console after May 3, 2021, the `kube-proxy` Amazon EKS add\-on is already on your cluster\. If you created your 1\.18 or later cluster using any other tool, and want to use the `kube-proxy` Amazon EKS add\-on, then you must add it to your cluster yourself\.

If you've added the `kube-proxy` Amazon EKS add\-on to your 1\.18 or later cluster, you can manage it using the procedures in the [Updating the `kube-proxy` Amazon EKS add\-on](#updating-kube-proxy-eks-add-on) and [Removing the `kube-proxy` Amazon EKS add\-on](#removing-kube-proxy-eks-add-on) sections\. For more information about Amazon EKS add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\.

If you have not added the `kube-proxy` Amazon EKS add\-on, the `kube-proxy` self\-managed add\-on is still running on your cluster\. You can manually update the `kube-proxy` self\-managed add\-on using the procedure in [Updating the `kube-proxy` self\-managed add\-on](#updating-kube-proxy-add-on)\.

**Prerequisites**
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\.
+ If your cluster is 1\.21 or later, make sure that your Amazon VPC and `CoreDNS` add\-ons are at the minimum versions listed in [Service account tokens](service-accounts.md#boundserviceaccounttoken-validated-add-on-versions)\.

## Adding the `kube-proxy` Amazon EKS add\-on<a name="adding-kube-proxy-eks-add-on"></a>

Select the tab with the name of the tool that you want to use to add the `kube-proxy` Amazon EKS add\-on to your cluster with\.

**Important**  
Before adding the `kube-proxy` Amazon EKS add\-on, confirm that you do not self\-manage any settings that Amazon EKS will start managing\. To determine which settings Amazon EKS manages, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------
#### [ eksctl ]

**To add the `kube-proxy` Amazon EKS add\-on using `eksctl`**  
Replace *`my-cluster`* with the name of your cluster and then run the following command\.

```
eksctl create addon --name kube-proxy --cluster my-cluster --force
```

If you remove the `--force` option and any of the Amazon EKS add\-on settings conflict with your existing settings, then adding the Amazon EKS add\-on fails, and you receive an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------
#### [ AWS Management Console ]

**To add the `kube-proxy` Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to configure the `kube-proxy` Amazon EKS add\-on for\.

1. Choose the **Add\-ons** tab\.

1. Select **Add new**\.

   1. Select **`kube-proxy`** for **Name**\.

   1. Select the **Version** you'd like to use\.

   1. If you select **Override existing configuration for this add\-on on the cluster\.**, then any setting for the existing add\-on can be overwritten with the Amazon EKS add\-on's settings\. If you don't enable this option and any of the Amazon EKS add\-on settings conflict with your existing settings, then adding the Amazon EKS add\-on fails, and you receive an error message to help you resolve the conflict\. Before selecting this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

   1. Select **Add**\.

------
#### [ AWS CLI ]

**To add the `kube-proxy` Amazon EKS add\-on using the AWS CLI**  
Replace *`my-cluster`* with the name of your cluster and then run the following command\.

```
aws eks create-addon \
    --cluster-name my-cluster \
    --addon-name kube-proxy \
    --resolve-conflicts OVERWRITE
```

If you remove the `--resolve-conflicts OVERWRITE` option and any of the Amazon EKS add\-on settings conflict with your existing settings, then creating the add\-on fails, and you receive an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------

## Updating the `kube-proxy` Amazon EKS add\-on<a name="updating-kube-proxy-eks-add-on"></a>

This procedure is for updating the `kube-proxy` Amazon EKS add\-on\. If you haven't added the `kube-proxy` Amazon EKS add\-on, complete the procedure in [Updating the `kube-proxy` self\-managed add\-on](#updating-kube-proxy-add-on) instead\. Amazon EKS does not automatically update `kube-proxy` on your cluster when new versions are released or after you [update your cluster](update-cluster.md) to a new Kubernetes minor version\. To update `kube-proxy` on an existing cluster, you must initiate the update and then Amazon EKS updates the add\-on for you\. 

**Important**  
Update your cluster and nodes to a new Kubernetes minor version before updating `kube-proxy` to the same minor version as your updated cluster's minor version\.

------
#### [ eksctl ]

**To update the `kube-proxy` Amazon EKS add\-on using `eksctl`**

1. Check the current version of your `kube-proxy` Amazon EKS add\-on\. Replace *`my-cluster`* with your cluster name\.

   ```
   eksctl get addon --name kube-proxy --cluster my-cluster
   ```

   Output

   ```
   NAME            VERSION                 STATUS  ISSUES  IAMROLE UPDATE AVAILABLE
   kube-proxy      v1.19.6-eksbuild.2      ACTIVE  0               v1.20.4-eksbuild.2
   ```

1. Update the add\-on to the version returned under `UPDATE AVAILABLE` in the output of the previous step\.

   ```
   eksctl update addon \
       --name kube-proxy \
       --version v1.20.4-eksbuild.2 \
       --cluster my-cluster \
       --force
   ```

   If you remove the `--force` option and any of the Amazon EKS add\-on settings conflict with your existing settings, then updating the add\-on fails, and you receive an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------
#### [ AWS Management Console ]

**To update the `kube-proxy` Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to update the `kube-proxy` Amazon EKS add\-on for\. 

1. Choose the **Add\-ons** tab\.

1. Select the box in the top right of the **`kube-proxy`** box and then choose **Edit**\.

   1. Select the **Version** of the Amazon EKS add\-on that you want to use\.

   1. If you select **Override existing configuration for this add\-on on the cluster\.**, then any setting for the existing add\-on can be overwritten with the Amazon EKS add\-on's settings\. If you don't enable this option and any of the Amazon EKS add\-on settings conflict with your existing settings, then updating the add\-on to an Amazon EKS add\-on fail, and you receive an error message to help you resolve the conflict\. Before selecting this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

   1. Select **Update**\.

------
#### [ AWS CLI ]

**To update the `kube-proxy` Amazon EKS add\-on using the AWS CLI**

1. Check the current version of your `kube-proxy` Amazon EKS add\-on\. Replace *my\-cluster* with your cluster name\.

   ```
   aws eks describe-addon \
       --cluster-name my-cluster \
       --addon-name kube-proxy \
       --query "addon.addonVersion" \
       --output text
   ```

   The example output is as follows\.

   ```
   v1.19.6-eksbuild.2
   ```

1. Determine which versions of the `kube-proxy` add\-on are available for your cluster version\.

   ```
   aws eks describe-addon-versions \
       --addon-name kube-proxy \
       --kubernetes-version 1.20 \
       --query "addons[].addonVersions[].[addonVersion, compatibilities[].defaultVersion]" \
       --output text
   ```

   Output

   ```
   v1.20.4-eksbuild.2
   True
   v1.19.6-eksbuild.2
   False
   v1.18.8-eksbuild.1
   False
   ```

   The version with `True` underneath is the default version deployed with new clusters with the version that you specified\.

1. Update the add\-on to the version with `True` returned in the output of the previous step\. You can also update to a later version, if returned in the output\.

   ```
   aws eks update-addon \
       --cluster-name my-cluster \
       --addon-name kube-proxy \
       --addon-version v1.20.4-eksbuild.2 \
       --resolve-conflicts OVERWRITE
   ```

   If you remove the `--resolve-conflicts OVERWRITE` option and any of the Amazon EKS add\-on settings conflict with your existing settings, then updating the add\-on fails, and you receive an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------

## Removing the `kube-proxy` Amazon EKS add\-on<a name="removing-kube-proxy-eks-add-on"></a>

You have two options when removing an Amazon EKS add\-on:
+ **Preserve the add\-on's software on your cluster** – This option removes Amazon EKS management of any settings and the ability for Amazon EKS to notify you of updates and automatically update the Amazon EKS add\-on after you initiate an update, but preserves the add\-on's software on your cluster\. This option makes the add\-on a self\-managed add\-on, rather than an Amazon EKS add\-on\. There is no downtime for the add\-on\.
+ **Removing the add\-on software entirely from your cluster** – You should only remove the Amazon EKS add\-on from your cluster if there are no resources on your cluster are dependent on the functionality that the add\-on provides\. After removing the Amazon EKS add\-on, you can add it again if you want to\.

If the add\-on has an IAM account associated with it, the IAM account is not removed\.

Select the tab with the name of the tool that you want to use to remove the `kube-proxy` Amazon EKS add\-on from your 1\.18 or later cluster with\.

------
#### [ eksctl ]

**To remove the `kube-proxy` Amazon EKS add\-on using `eksctl`**  
Replace *`my-cluster`* with the name of your cluster and then run the following command\. Removing `--preserve` removes the add\-on software from your cluster\.

```
eksctl delete addon --cluster my-cluster --name kube-proxy --preserve
```

------
#### [ AWS Management Console ]

**To remove the `kube-proxy` Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to remove the `kube-proxy` Amazon EKS add\-on for\.

1. Choose the **Add\-ons** tab\.

1. Select the check box in the top right of the **`kube-proxy`** box and then choose **Remove**\. Type **`kube-proxy`** and then select **Remove**\.

------
#### [ AWS CLI ]

**To remove the `kube-proxy` Amazon EKS add\-on using the AWS CLI**  
Replace *`my-cluster`* with the name of your cluster and then run the following command\. Removing `--preserve` removes the add\-on software from your cluster\.

```
aws eks delete-addon --cluster-name my-cluster --addon-name kube-proxy --preserve
```

------

## Updating the `kube-proxy` self\-managed add\-on<a name="updating-kube-proxy-add-on"></a>

If you have a 1\.17 or earlier cluster, or a 1\.18 or later cluster that you have not added the `kube-proxy` Amazon EKS add\-on to, complete the following steps to update the self\-managed add\-on\. If you've added the `kube-proxy` Amazon EKS add\-on, complete the procedure in [Updating the `kube-proxy` Amazon EKS add\-on](#updating-kube-proxy-eks-add-on) instead\.

**Important**  
Update your cluster and nodes to a new Kubernetes minor version before updating `kube-proxy` to the same minor version as your updated cluster's minor version\.

**To update the `kube-proxy` self\-managed add\-on using `kubectl`**

1. Check the current version of your `kube-proxy` deployment\.

   ```
   kubectl get daemonset kube-proxy \
       --namespace kube-system \
       -o=jsonpath='{$.spec.template.spec.containers[:1].image}'
   ```

   The example output is as follows\.

   ```
   602401143452.dkr.ecr.region-code.amazonaws.com/eks/kube-proxy:v1.21.2-eksbuild.2
   ```

1. Update the `kube-proxy` add\-on by replacing `602401143452` and *`region-code`* with the values from your output\. Replace *`1.22.6-eksbuild.1`* with the `kube-proxy` version listed in the [`kube-proxy` version deployed with each Amazon EKS supported cluster version](#kube-proxy-default-versions-table) table for your cluster version\.

   ```
   kubectl set image daemonset.apps/kube-proxy \
        -n kube-system \
        kube-proxy=602401143452.dkr.ecr.region-code.amazonaws.com/eks/kube-proxy:v1.22.6-eksbuild.1
   ```

1. \(Optional\) If you're using x86 and Arm nodes in the same cluster and your cluster was deployed before August 17, 2020\. Then, edit your `kube-proxy` manifest to include a node selector for multiple hardware architectures with the following command\. This is a one\-time operation\. After you've added the selector to your manifest, you don't need to add it each time you update\. If your cluster was deployed on or after August 17, 2020, then `kube-proxy` is already multi\-architecture capable\.

   ```
   kubectl edit -n kube-system daemonset/kube-proxy
   ```

   Add the following node selector to the file in the editor and then save the file\. For an example of where to include this text in the editor, see the [CNI manifest](https://github.com/aws/amazon-vpc-cni-k8s/blob/release-1.11/config/master/aws-k8s-cni.yaml#L261-#L265) file on GitHub\. This enables Kubernetes to pull the correct hardware image based on the node's hardware architecture\.

   ```
   - key: "kubernetes.io/arch"
     operator: In
     values:
     - amd64
     - arm64
   ```

1. \(Optional\) If your cluster was originally created with Kubernetes v1\.14 or later, then you can skip this step because `kube-proxy` already includes this `Affinity Rule`\. If you originally created an Amazon EKS cluster with Kubernetes version 1\.13 or earlier and intend to use Fargate nodes, then edit your `kube-proxy` manifest to include a `NodeAffinity` rule to prevent `kube-proxy` pods from scheduling on Fargate nodes\. This is a one\-time edit\. Once you've added the `Affinity Rule` to your manifest, you don't need to add it each time you upgrade your cluster\. Edit your `kube-proxy` `DaemonSet`\.

   ```
   kubectl edit -n kube-system daemonset/kube-proxy
   ```

   Add the following `Affinity Rule` to the `DaemonSet` `spec` section of the file in the editor and then save the file\. For an example of where to include this text in the editor, see the [CNI manifest](https://github.com/aws/amazon-vpc-cni-k8s/blob/release-1.11/config/master/aws-k8s-cni.yaml#L266-#L269) file on GitHub\.

   ```
   - key: eks.amazonaws.com/compute-type
     operator: NotIn
     values:
     - fargate
   ```