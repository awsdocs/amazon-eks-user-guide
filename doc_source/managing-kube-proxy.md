# Managing the `kube-proxy` add\-on<a name="managing-kube-proxy"></a>

`Kube-proxy` maintains network rules on each Amazon EC2 node\. It enables network communication to your pods\. `Kube-proxy` is not deployed to Fargate nodes\. For more information, see [https://kubernetes.io/docs/concepts/overview/components/#kube-proxy](https://kubernetes.io/docs/concepts/overview/components/#kube-proxy) in the Kubernetes documentation\. There are two types of the `kube-proxy` container image available for each Kubernetes version:
+ **Default** – This type is based on a Debian\-based Docker image that is maintained by the Kubernetes upstream community\.
+ **Minimal** – This type is based on a [minimal base image](https://gallery.ecr.aws/eks-distro-build-tooling/eks-distro-minimal-base-iptables) maintained by Amazon EKS Distro, which contains minimal packages and doesn't have shells\. For more information, see [Amazon EKS Distro](https://distro.eks.amazonaws.com/)\.<a name="kube-proxy-latest-versions-table"></a>


**Latest available `kube-proxy` container image version for each Amazon EKS cluster version**  

| Image type | `1.24` | `1.23` | `1.22` | `1.21` | `1.20` | `1.19` | 
| --- | --- | --- | --- | --- | --- | --- | 
| kube\-proxy \(default type\) | v1\.24\.7\-eksbuild\.1 | v1\.23\.8\-eksbuild\.2 | v1\.22\.11\-eksbuild\.2 | v1\.21\.14\-eksbuild\.2 | v1\.20\.15\-eksbuild\.2 | v1\.19\.16\-eksbuild\.2 | 
| kube\-proxy \(minimal type\) | v1\.24\.7\-minimal\-eksbuild\.2 | v1\.23\.13\-minimal\-eksbuild\.2 | v1\.22\.11\-minimal\-eksbuild\.2 | v1\.21\.14\-minimal\-eksbuild\.2 | v1\.20\.15\-minimal\-eksbuild\.3 | v1\.19\.16\-minimal\-eksbuild\.3 | 

You can check the current version of your `kube-proxy` container\-image with the following command\.

```
kubectl get daemonset kube-proxy --namespace kube-system -o=jsonpath='{$.spec.template.spec.containers[:1].image}' | cut -d : -f 2
```

The example output is as follows\.

```
v1.23.8-minimal-eksbuild.2
```

If you want to update the version on your cluster and your cluster is running the `kube-proxy` Amazon EKS add\-on, see [Updating the `kube-proxy` Amazon EKS add\-on](#updating-kube-proxy-eks-add-on) to update it\. If your cluster is running the self\-managed Amazon EKS add\-on, see [Updating the `kube-proxy` self\-managed add\-on](#updating-kube-proxy-add-on) to update it\.

Amazon EKS has the same [compatibility and skew policy as Kubernetes](https://kubernetes.io/releases/version-skew-policy/#kube-proxy) for `kube-proxy`\. `Kube-proxy` must meet the following requirements:
+ It must be the same minor version as `kubelet` on the node\.
+ It must not be newer than the version of your cluster's control plane\.
+ It's version can't be earlier than two minor versions from your control plane\. For example, if your control plane is running Kubernetes 1\.24, then the `kube-proxy` minor version can't be earlier than 1\.22\.

**Prerequisites**
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\.
+ If your cluster is `1.21` or later, make sure that your Amazon VPC and CoreDNS add\-ons are at the minimum versions listed in [Service account tokens](service-accounts.md#boundserviceaccounttoken-validated-add-on-versions)\.

## Creating the `kube-proxy` Amazon EKS add\-on<a name="adding-kube-proxy-eks-add-on"></a>

You can create the `kube-proxy` Amazon EKS add\-on to your cluster using `eksctl`, the AWS Management Console, or the AWS CLI\.

**Important**  
Before adding the `kube-proxy` Amazon EKS add\-on, confirm that you do not self\-manage any settings that Amazon EKS will start managing\. To determine which settings Amazon EKS manages, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.
The version number of the add\-on might not match a version in the [Latest available `kube-proxy` container image version table](#kube-proxy-latest-versions-table)\. `1.22.x` and earlier versions of the add\-on deploy the *default* image type\. `1.23.x` and later versions of the add\-on deploy the *minimal* image type\.

------
#### [ eksctl ]

**To create the `kube-proxy` Amazon EKS add\-on using `eksctl`**  
Replace *`my-cluster`* with the name of your cluster and then run the following command\. `Eksctl` adds the latest version of the add\-on that's available for your cluster version\.

```
eksctl create addon --name kube-proxy --cluster my-cluster --force
```

If you remove the `--force` option and any of the Amazon EKS add\-on settings conflict with your existing settings, then adding the Amazon EKS add\-on fails, and you receive an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------
#### [ AWS Management Console ]

**To create the `kube-proxy` Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to configure the `kube-proxy` Amazon EKS add\-on for\.

1. Choose the **Add\-ons** tab\.

1. Select **Add new**\.

   1. Select **`kube-proxy`** for **Name**\.

   1. Select the **Version** you'd like to use\. Select the version marked as **Latest**\.

   1. If you select **Override existing configuration for this add\-on on the cluster\.**, then any setting for the existing add\-on can be overwritten with the Amazon EKS add\-on's settings\. If you don't enable this option and any of the Amazon EKS add\-on settings conflict with your existing settings, then adding the Amazon EKS add\-on fails, and you receive an error message to help you resolve the conflict\. Before selecting this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

   1. Select **Add**\.

------
#### [ AWS CLI ]

**To create the `kube-proxy` Amazon EKS add\-on using the AWS CLI**

1. Determine the latest version of `kube-proxy` Amazon EKS add\-on that's available for your cluster's version\. Replace *1\.24* with your cluster's version\.

   ```
   aws eks describe-addon-versions --kubernetes-version 1.23 --addon-name kube-proxy --query addons[].addonVersions[].addonVersion | grep 1.23
   ```

   The example output is as follows\.

   ```
   "v1.23.8-eksbuild.2",
   "v1.23.7-eksbuild.1",
   ```

   In the example output, *v1\.23\.8\-eksbuild\.2* is the latest version\.

1. Create the add\-on\. Replace *`my-cluster`* with the name of your cluster and *v1\.23\.8\-eksbuild\.2* with the latest version returned in the output of the previous step\.

   ```
   aws eks create-addon --cluster-name my-cluster --addon-name kube-proxy --addon-version v1.23.8-eksbuild.2 --resolve-conflicts OVERWRITE
   ```

   If you remove the **\-\-resolve\-conflicts OVERWRITE** option and any of the Amazon EKS add\-on settings conflict with your existing settings, then creating the add\-on fails, and you receive an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------

## Updating the `kube-proxy` Amazon EKS add\-on<a name="updating-kube-proxy-eks-add-on"></a>

This procedure is for updating the `kube-proxy` Amazon EKS add\-on\. If you haven't added the `kube-proxy` Amazon EKS add\-on, complete the procedure in [Updating the `kube-proxy` self\-managed add\-on](#updating-kube-proxy-add-on) instead\. Amazon EKS does not automatically update `kube-proxy` on your cluster when new versions are released or after you [update your cluster](update-cluster.md) to a new Kubernetes minor version\. To update `kube-proxy` on an existing cluster, you must initiate the update and then Amazon EKS updates the add\-on for you\. 

**Important**  
Update your cluster and nodes to a new Kubernetes minor version before updating `kube-proxy` to the same minor version as your updated cluster's minor version\.
The version number of the add\-on might not match a version in the [Latest available `kube-proxy` container image version table](#kube-proxy-latest-versions-table)\. `1.22.x` and earlier versions of the add\-on deploy the *default* image type\. `1.23.x` and later versions of the add\-on deploy the *minimal* image type\.

------
#### [ eksctl ]

**To update the `kube-proxy` Amazon EKS add\-on using `eksctl`**

1. Check the current version of your `kube-proxy` Amazon EKS add\-on\. Replace *`my-cluster`* with your cluster name\.

   ```
   eksctl get addon --name kube-proxy --cluster my-cluster
   ```

   The example output is as follows\.

   ```
   NAME            VERSION                  STATUS  ISSUES  IAMROLE UPDATE AVAILABLE
   kube-proxy      v1.23.8-eksbuild.2      ACTIVE  0               v1.24.7-eksbuild.2
   ```

1. Update the add\-on to the version returned under `UPDATE AVAILABLE` in the output of the previous step\.

   ```
   eksctl update addon --name kube-proxy --version v1.24.7-eksbuild.2 --cluster my-cluster --force
   ```

   If you remove the **\-\-*force*** option and any of the Amazon EKS add\-on settings conflict with your existing settings, then updating the Amazon EKS add\-on fails, and you receive an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\. For more information about other options for this setting, see [Addons](https://eksctl.io/usage/addons/) in the `eksctl` documentation\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------
#### [ AWS Management Console ]

**To update the `kube-proxy` Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to update the `kube-proxy` Amazon EKS add\-on for\. 

1. Choose the **Add\-ons** tab\.

1. Select the box in the top right of the **`kube-proxy`** box and then choose **Edit**\.

   1. Select the **Version** marked as **Latest**\.

   1. For **Conflict resolution method**, select one of the options\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

   1. Select **Update**\.

------
#### [ AWS CLI ]

**To update the `kube-proxy` Amazon EKS add\-on using the AWS CLI**

1. Check the current version of your `kube-proxy` Amazon EKS add\-on\. Replace `my-cluster` with your cluster name\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name kube-proxy --query "addon.addonVersion" --output text
   ```

   The example output is as follows\.

   ```
   v1.23.8-eksbuild.2
   ```

1. Determine the latest version of the `kube-proxy` Amazon EKS add\-on that's available for your cluster's version\. Replace *1\.24* with your cluster's version\.

   ```
   aws eks describe-addon-versions --addon-name kube-proxy --kubernetes-version 1.23 \
       --query "addons[].addonVersions[].[addonVersion, compatibilities[].defaultVersion]" --output text
   ```

   The example output is as follows\.

   ```
   v1.23.8-eksbuild.2
   False
   v1.23.7-eksbuild.1
   True
   ```

   The version with `True` underneath is the default version deployed when the add\-on is created\. The version deployed when the add\-on is created might not be the latest available version\. In the previous output, a newer version than the version deployed when the add\-on is created is available\.

1. Update the add\-on to the latest version\. Replace *`my-cluster`* with the name of your cluster and v*1\.23\.8\-eksbuild\.2* with the latest version returned in the output of the previous step\.

   ```
   aws eks update-addon --cluster-name my-cluster --addon-name kube-proxy --addon-version v1.23.8-eksbuild.2 --resolve-conflicts PRESERVE
   ```

   The *PRESERVE* option preserves any custom settings that you've set for the add\-on\. For more information about other options for this setting, see [update\-addon](https://docs.aws.amazon.com/cli/latest/reference/eks/update-addon.html) in the Amazon EKS Command Line Reference\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------

## Deleting the `kube-proxy` Amazon EKS add\-on<a name="removing-kube-proxy-eks-add-on"></a>

You have two options when deleting an Amazon EKS add\-on:
+ **Preserve the add\-on software on your cluster** – This option removes Amazon EKS management of any settings and the ability for Amazon EKS to notify you of updates and automatically update the Amazon EKS add\-on after you initiate an update, but preserves the add\-on software on your cluster\. This option makes the add\-on a self\-managed add\-on, rather than an Amazon EKS add\-on\. There is no downtime for the add\-on\.
+ **Deleting the add\-on software entirely from your cluster** – You should only delete the Amazon EKS add\-on from your cluster if there are no resources on your cluster are dependent on the functionality that the add\-on provides\. After deleting the Amazon EKS add\-on, you can add it again if you want to\.

If the add\-on has an IAM account associated with it, the IAM account is not deleted\.

You can use `eksctl`, the AWS Management Console or the AWS CLI to delete the `kube-proxy` Amazon EKS add\-on from your cluster\.

------
#### [ eksctl ]

**To delete the `kube-proxy` Amazon EKS add\-on using `eksctl`**  
Replace *`my-cluster`* with the name of your cluster and then run the following command\. Removing **\-\-preserve** deletes the add\-on software from your cluster\.

```
eksctl delete addon --cluster my-cluster --name kube-proxy --preserve
```

------
#### [ AWS Management Console ]

**To delete the `kube-proxy` Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to remove the `kube-proxy` Amazon EKS add\-on from\.

1. Choose the **Add\-ons** tab\.

1. Select the check box in the top right of the **`kube-proxy`** box and then choose **Remove**\. Type **`kube-proxy`** and then select **Remove**\.

------
#### [ AWS CLI ]

**To delete the `kube-proxy` Amazon EKS add\-on using the AWS CLI**  
Replace *`my-cluster`* with the name of your cluster and then run the following command\. Removing `--preserve` removes the add\-on software from your cluster\.

```
aws eks delete-addon --cluster-name my-cluster --addon-name kube-proxy --preserve
```

------

## Updating the `kube-proxy` self\-managed add\-on<a name="updating-kube-proxy-add-on"></a>

If you have a cluster that you have not added the `kube-proxy` Amazon EKS add\-on to, complete the following steps to update the self\-managed add\-on\. If you've added the `kube-proxy` Amazon EKS add\-on, complete the procedure in [Updating the `kube-proxy` Amazon EKS add\-on](#updating-kube-proxy-eks-add-on) instead\.

**Important**  
Update your cluster and nodes to a new Kubernetes minor version before updating `kube-proxy` to the same minor version as your updated cluster's minor version\.
If you deployed a `1.22.x` and earlier cluster, the *default* image type was deployed with your cluster\. If you deployed a `1.23.x` and later version of your cluster, the *minimal* image type was deployed\.

**To update the `kube-proxy` self\-managed add\-on using `kubectl`**

1. Check the current version of your `kube-proxy` deployment\.

   ```
   kubectl get daemonset kube-proxy --namespace kube-system -o=jsonpath='{$.spec.template.spec.containers[:1].image}'
   ```

   The example output is as follows\.

   ```
   602401143452.dkr.ecr.region-code.amazonaws.com/eks/kube-proxy:v1.23.8-eksbuild.2
   ```

1. Update the `kube-proxy` add\-on by replacing `602401143452` and *`region-code`* with the values from your output\. Replace *1\.23\.8\-eksbuild\.2* with the `kube-proxy` version listed in the [Latest available `kube-proxy` container image version for each Amazon EKS cluster version](#kube-proxy-latest-versions-table) table\. You can specify a version number for the *default* or *minimal* image type\.

   ```
   kubectl set image daemonset.apps/kube-proxy -n kube-system kube-proxy=602401143452.dkr.ecr.region-code.amazonaws.com/eks/kube-proxy:v1.24.7-eksbuild.2
   ```

1. If you're using `x86` and `Arm` nodes in the same cluster and your cluster was deployed before August 17, 2020\. Then, edit your `kube-proxy` manifest to include a node selector for multiple hardware architectures with the following command\. This is a one\-time operation\. After you've added the selector to your manifest, you don't need to add it each time you update\. If your cluster was deployed on or after August 17, 2020, then `kube-proxy` is already multi\-architecture capable\.

   ```
   kubectl edit -n kube-system daemonset/kube-proxy
   ```

   Add the following node selector to the file in the editor and then save the file\. For an example of where to include this text in the editor, see the [CNI manifest](https://github.com/aws/amazon-vpc-cni-k8s/blob/release-1.11/config/master/aws-k8s-cni.yaml#L265-#L269) file on GitHub\. This enables Kubernetes to pull the correct hardware image based on the node's hardware architecture\.

   ```
   - key: "kubernetes.io/arch"
     operator: In
     values:
     - amd64
     - arm64
   ```

1. If your cluster was originally created with Kubernetes version `1.14` or later, then you can skip this step because `kube-proxy` already includes this `Affinity Rule`\. If you originally created an Amazon EKS cluster with Kubernetes version `1.13` or earlier and intend to use Fargate nodes, then edit your `kube-proxy` manifest to include a `NodeAffinity` rule to prevent `kube-proxy` pods from scheduling on Fargate nodes\. This is a one\-time edit\. Once you've added the `Affinity Rule` to your manifest, you don't need to add it each time you upgrade your cluster\. Edit your `kube-proxy` `DaemonSet`\.

   ```
   kubectl edit -n kube-system daemonset/kube-proxy
   ```

   Add the following `Affinity Rule` to the `DaemonSet` `spec` section of the file in the editor and then save the file\. For an example of where to include this text in the editor, see the [CNI manifest](https://github.com/aws/amazon-vpc-cni-k8s/blob/release-1.11/config/master/aws-k8s-cni.yaml#L270-#L273) file on GitHub\.

   ```
   - key: eks.amazonaws.com/compute-type
     operator: NotIn
     values:
     - fargate
   ```