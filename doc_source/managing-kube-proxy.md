# Managing the `kube-proxy` add\-on<a name="managing-kube-proxy"></a>

`Kube-proxy` maintains network rules on each Amazon EC2 node\. It enables network communication to your pods\. `Kube-proxy` is not deployed to Fargate nodes\. For more information, see [kube\-proxy](https://kubernetes.io/docs/concepts/overview/components/#kube-proxy) in the Kubernetes documentation\.

The `kube-proxy` version deployed to your nodes is the same major, minor, and patch version that was deployed with the platform version that was current for the Kubernetes version that you initially deployed with your cluster\. For more information, see [Amazon EKS platform versions](platform-versions.md)\. 


**`kube-proxy` version deployed with each Amazon EKS supported cluster version**  

| Kubernetes version | 1\.20 | 1\.19 | 1\.18 | 1\.17 | 1\.16 | 
| --- | --- | --- | --- | --- | --- | 
| kube\-proxy | 1\.20\.4 | 1\.19\.6 | 1\.18\.8 | 1\.17\.9 | 1\.16\.13 | 

If you have a 1\.18 or later cluster that you have not added the `kube-proxy` Amazon EKS add\-on to, you can add it using the procedure in [Adding the `kube-proxy` Amazon EKS add\-on](#adding-kube-proxy-eks-add-on)\. If you created your 1\.18 or later cluster using the AWS Management Console after May 3, 2021, the `kube-proxy` Amazon EKS add\-on is already on your cluster\. If you created your 1\.18 or later cluster using any other tool, and want to use the `kube-proxy` Amazon EKS add\-on, then you must add it to your cluster yourself\.

If you've added the `kube-proxy` Amazon EKS add\-on to your 1\.18 or later cluster, you can manage it using the procedures in the [Updating the `kube-proxy` Amazon EKS add\-on](#updating-kube-proxy-eks-add-on) and [Removing the `kube-proxy` Amazon EKS add\-on](#removing-kube-proxy-eks-add-on) sections\. For more information about Amazon EKS add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\.

If you have not added the `kube-proxy` Amazon EKS add\-on, the `kube-proxy` add\-on is still running on your cluster\. You can manually update the `kube-proxy` add\-on using the procedure in the [Updating the `kube-proxy` add\-on manually](#updating-kube-proxy-add-on) section\.

## Adding the `kube-proxy` Amazon EKS add\-on<a name="adding-kube-proxy-eks-add-on"></a>

Select the tab with the name of the tool that you want to use to add the `kube-proxy` Amazon EKS add\-on to your cluster with\.

------
#### [ AWS Management Console ]

**To add the `kube-proxy` Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation, select **Clusters**, and then select the name of the cluster that you want to configure the `kube-proxy` Amazon EKS add\-on for\.

1. Choose the **Configuration** tab and then choose the **Add\-ons** tab\.

1. Select **Add new**\.

   1. Select **`kube-proxy`** for **Name**\.

   1. Select the **Version** you'd like to use\.

   1. If you select **Enable Override existing configuration for this add\-on on the cluster**, then any setting for the existing add\-on can be overwritten with the Amazon EKS add\-on's settings\. If you don't enable this option and any of the Amazon EKS add\-on settings conflict with your existing settings, then migrating the add\-on to an Amazon EKS add\-on fail, and you receive an error message to help you resolve the conflict\. 

   1. Select **Add**\.

------
#### [ AWS CLI ]

To add the `kube-proxy` Amazon EKS add\-on using the AWS CLI\. Replace *my\-cluster* with the name of your cluster\.

```
aws eks create-addon --cluster-name my-cluster --addon-name kube-proxy
```

If you want the add\-on to overwrite any changes you've made to the add\-on with its own settings, add the `--resolve-conflicts OVERWRITE` option to the previous command\. If you don't enable this option and any of the Amazon EKS add\-on settings conflict with your existing settings, then migrating the add\-on to an Amazon EKS add\-on fails, and you receive an error message to help you resolve the conflict\. 

------

## Updating the `kube-proxy` Amazon EKS add\-on<a name="updating-kube-proxy-eks-add-on"></a>

This procedure is for updating the `kube-proxy` Amazon EKS add\-on\. If you haven't added the `kube-proxy` Amazon EKS add\-on, complete the procedure in [Updating the `kube-proxy` add\-on manually](#updating-kube-proxy-add-on) instead\. Amazon EKS does not automatically update `kube-proxy` on your cluster when new versions are released or after you [update your cluster](update-cluster.md) to a new Kubernetes minor version\. To update `kube-proxy` on an existing cluster, you must initiate the update and then Amazon EKS updates the add\-on for you\. 

**Important**  
`Kube-proxy` must be the same minor version as `kubelet` on the node\. You should update your cluster and nodes before updating `kube-proxy` to a new version\.

------
#### [ AWS Management Console ]

**To update the `kube-proxy` Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation, select **Clusters**, and then select the name of the cluster that you want to update the `kube-proxy` Amazon EKS add\-on for\. 

1. Choose the **Configuration** tab and then choose the **Add\-ons** tab\.

1. Select the box in the top right of the **`kube-proxy`** box and then choose **Edit**\.

   1. Select the **Version** of the Amazon EKS add\-on that you want to use\.

   1. If you select **Enable Override existing configuration for this add\-on on the cluster**, then any setting for the existing add\-on can be overwritten with the Amazon EKS add\-on's settings\. If you don't enable this option and any of the Amazon EKS add\-on settings conflict with your existing settings, then migrating the add\-on to an Amazon EKS add\-on will fail, and you'll receive an error message to help you resolve the conflict\. 

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

   Output:

   ```
   1.7.0
   ```

1. Determine which versions of the `kube-proxy` add\-on are available for your cluster's version\.

   ```
   aws eks describe-addon-versions \
       --addon-name kube-proxy \
       --kubernetes-version 1.19 \
       --query "addons[].addonVersions[].[addonVersion, compatibilities[].defaultVersion]" \
       --output text
   ```

   Output

   ```
   1.19.6
   True
   1.18.8
   False
   ```

   The version with `True` underneath is the default version deployed with new clusters\.

1. Update the add\-on to a version returned in the output of the previous step\. The version should be the same, or later than the version in the [`kube-proxy` versions](#kube-proxy-versions) table\.

   ```
   aws eks update-addon \
       --cluster-name my-cluster \
       --addon-name kube-proxy \
       --addon-version 1.8.0 \
       --resolve-conflicts
   ```

------

## Removing the `kube-proxy` Amazon EKS add\-on<a name="removing-kube-proxy-eks-add-on"></a>

Removing the Amazon EKS add\-on from your cluster removes its functionality\. You should only remove the add\-on from your cluster if none of your pods are dependent on the functionality that the add\-on provides\. After removing the add\-on, you can add it again if you want to\.

------
#### [ AWS Management Console ]

**To remove the `kube-proxy` Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation, select **Clusters**, and then select the name of the cluster that you want to remove the `kube-proxy` Amazon EKS add\-on for\.

1. Choose the **Configuration** tab and then choose the **Add\-ons** tab\.

1. Select the check box in the top right of the **`kube-proxy`** box and then choose **Remove**\. Type **`kube-proxy`** and then select **Remove**\.

------
#### [ AWS CLI ]

Remove the `kube-proxy` Amazon EKS add\-on with the following command\. Replace *my\-cluster* with the name of your cluster\.

```
aws eks delete-addon --cluster-name my-cluster --addon-name kube-proxy
```

------

## Updating the `kube-proxy` add\-on manually<a name="updating-kube-proxy-add-on"></a>

If you have a 1\.17 or earlier cluster, or a 1\.18 or later cluster that you have not added the `kube-proxy` Amazon EKS add\-on to, complete the following steps to update the add\-on\. If you've added the `kube-proxy` Amazon EKS add\-on, complete the procedure in [Updating the `kube-proxy` Amazon EKS add\-on](#updating-kube-proxy-eks-add-on) instead\.

**Important**  
`Kube-proxy` is backward, but not forward compatible with `kubelet`\. You should update your cluster and nodes before updating `kube-proxy` to a new version\.

Check the current version of your `kube-proxy` deployment\.

```
kubectl get daemonset kube-proxy --namespace kube-system -o=jsonpath='{$.spec.template.spec.containers[:1].image}'
```

Example output

```
602401143452.dkr.ecr.us-west-2.amazonaws.com/eks/kube-proxy:v1.19.6-eksbuild.1
```
+ Patch the `kube-proxy` Daemonset to use the image that corresponds to your cluster's Region and current Kubernetes version\.

  1. First, retrieve your current `kube-proxy` image:

  1. Update `kube-proxy` to the version that Amazon EKS deploys with new clusters from the previous [table](#kube-proxy-versions) by replacing *`602401143452`*, *`us-west-2`*, and *`com`* with the values from your output and replace *`1.20.4`* with your cluster's recommended `kube-proxy` version\. If you're deploying a version that is earlier than `1.20.4`, then replace `eksbuild.2` with `eksbuild.1`\.

     ```
     kubectl set image daemonset.apps/kube-proxy \
          -n kube-system \
          kube-proxy=602401143452.dkr.ecr.us-west-2.amazonaws.com/eks/kube-proxy:v1.20.4-eksbuild.2
     ```

  1. \(Optional\) If you're using x86 and Arm nodes in the same cluster and your cluster was deployed before August 17,2020\. Then, edit your `kube-proxy` manifest to include a node selector for multiple hardware architectures with the following command\. This is a one\-time operation\. After you've added the selector to your manifest, you don't need to do it each time you update\. If your cluster was deployed on or after August 17, 2020, then `kube-proxy` is already multi\-architecture capable\.

     ```
     kubectl edit -n kube-system daemonset/kube-proxy
     ```

     Add the following node selector to the file in the editor and then save the file\. For an example of where to include this text in the editor, see the [CNI manifest](https://github.com/aws/amazon-vpc-cni-k8s/blob/release-1.6/config/v1.6/aws-k8s-cni.yaml#L76-%23L80) file on GitHub\. This enables Kubernetes to pull the correct hardware image based on the node's hardware architecture\.

     ```
     - key: "beta.kubernetes.io/arch"
                         operator: In
                         values:
                           - amd64
                           - arm64
     ```

  1. \(Optional\) If your cluster was originally created with Kubernetes v1\.14 or later, then you can skip this step because `kube-proxy` already includes this `Affinity Rule`\. If you originally created an Amazon EKS cluster with Kubernetes version 1\.13 or earlier and intend to use Fargate nodes, then edit your `kube-proxy` manifest to include a `NodeAffinity` rule to prevent `kube-proxy` pods from scheduling on Fargate nodes\. This is a one\-time edit\. Once you've added the `Affinity Rule` to your manifest, you don't need to do it each time you upgrade your cluster\. Edit your `kube-proxy` Daemonset\.

     ```
     kubectl edit -n kube-system daemonset/kube-proxy
     ```

     Add the following `Affinity Rule` to the `Daemonset` `spec` section of the file in the editor and then save the file\. For an example of where to include this text in the editor, see the [CNI manifest](https://github.com/aws/amazon-vpc-cni-k8s/blob/release-1.6/config/v1.6/aws-k8s-cni.yaml#L95-%23L97) file on GitHub\.

     ```
     - key: eks.amazonaws.com/compute-type
       operator: NotIn
       values:
       - fargate
     ```