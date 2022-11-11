# Managing the CoreDNS add\-on<a name="managing-coredns"></a>

CoreDNS is a flexible, extensible DNS server that can serve as the Kubernetes cluster DNS\. When you launch an Amazon EKS cluster with at least one node, two replicas of the CoreDNS image are deployed by default, regardless of the number of nodes deployed in your cluster\. The CoreDNS pods provide name resolution for all pods in the cluster\. The CoreDNS pods can be deployed to Fargate nodes if your cluster includes an [AWS Fargate profile](fargate-profile.md) with a namespace that matches the namespace for the CoreDNS `deployment`\. For more information about CoreDNS, see [Using CoreDNS for Service Discovery](https://kubernetes.io/docs/tasks/administer-cluster/coredns/) in the Kubernetes documentation\.

The following table lists the version of the CoreDNS add\-on that is deployed with each Amazon EKS cluster version\.<a name="coredns-versions"></a>


**CoreDNS version deployed with each Amazon EKS supported cluster version**  

| Kubernetes version | `1.23` | `1.22` | `1.21` | `1.20` | `1.19` | 
| --- | --- | --- | --- | --- | --- | 
| CoreDNS | 1\.8\.7\-eksbuild\.2 | 1\.8\.7 | 1\.8\.4 | 1\.8\.3 | 1\.8\.0 | 

If you created a `1.18` or later cluster using the AWS Management Console, then Amazon EKS installed the add\-on for you as an Amazon EKS add\-on\. If you originally created a `1.17` or earlier cluster using any tool, or you created a `1.18` or later cluster using any tool other than the AWS Management Console, then Amazon EKS installed the plugin as a self\-managed add\-on for you\.

You can migrate the self\-managed add\-on to the Amazon EKS add\-on using the procedure in [Creating the CoreDNS Amazon EKS add\-on](#adding-coredns-eks-add-on)\. If you have a cluster that you've already added the CoreDNS add\-on to, you can manage it using the procedures in the [Updating the CoreDNS Amazon EKS add\-on](#updating-coredns-eks-add-on) and [Deleting the CoreDNS Amazon EKS add\-on](#removing-coredns-eks-add-on) sections\. For more information about Amazon EKS add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\.

If you haven't added the CoreDNS Amazon EKS add\-on, the CoreDNS self\-managed add\-on is still running on your cluster\. You can update the CoreDNS self\-managed add\-on using the procedure in [Updating the CoreDNS self\-managed add\-on](#updating-coredns-add-on)\.

**Prerequisites**
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\.
+ If your cluster is `1.21` or later, make sure that your Amazon VPC CNI plugin for Kubernetes and `kube-proxy` add\-ons are at the minimum versions listed in [Service account tokens](service-accounts.md#boundserviceaccounttoken-validated-add-on-versions)\.

## Creating the CoreDNS Amazon EKS add\-on<a name="adding-coredns-eks-add-on"></a>

Select the tab with the name of the tool that you want to use to add the CoreDNS Amazon EKS add\-on to your cluster with\. 

**Important**  
Before adding the CoreDNS Amazon EKS add\-on, confirm that you do not self\-manage any settings that Amazon EKS will start managing\. To determine which settings Amazon EKS manages, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------
#### [ eksctl ]

**To create the CoreDNS Amazon EKS add\-on using `eksctl`**  
Replace *`my-cluster`* with the name of your cluster and then run the following command\.

```
eksctl create addon --name coredns --cluster my-cluster --force
```

If you remove the **\-\-*force*** option and any of the Amazon EKS add\-on settings conflict with your existing settings, then updating the Amazon EKS add\-on fails, and you receive an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\. For more information about other options for this setting, see [Addons](https://eksctl.io/usage/addons/) in the `eksctl` documentation\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------
#### [ AWS Management Console ]

**To create the CoreDNS Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, choose **Clusters**, and then select the name of the cluster that you want to configure the CoreDNS Amazon EKS add\-on for\.

1. Choose the **Add\-ons** tab\.

1. Select **Add new**\.

   1. Select **CoreDNS** for **Name**\.

   1. Select the **Version** you'd like to use\.

   1. For **Conflict resolution method**, select one of the options\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

   1. Select **Add**\.

------
#### [ AWS CLI ]

**To create the CoreDNS Amazon EKS add\-on using the AWS CLI**  
Replace `my-cluster` with the name of your cluster and then run the following command\.

```
aws eks create-addon --cluster-name my-cluster --addon-name coredns --resolve-conflicts OVERWRITE
```

If you remove the **\-\-resolve\-conflicts OVERWRITE** option and any of the Amazon EKS add\-on settings conflict with your existing settings, then creating the add\-on fails, and you receive an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------

## Updating the CoreDNS Amazon EKS add\-on<a name="updating-coredns-eks-add-on"></a>

This procedure is for updating the CoreDNS Amazon EKS add\-on\. If you haven't added the CoreDNS Amazon EKS add\-on, complete the procedure in [Updating the CoreDNS self\-managed add\-on](#updating-coredns-add-on) instead, or [add the CoreDNS Amazon EKS add\-on](#adding-coredns-eks-add-on)\. Amazon EKS does not automatically update CoreDNS on your cluster when new versions are released or after you [update your cluster](update-cluster.md) to a new Kubernetes minor version\. To update CoreDNS on an existing cluster, you must initiate the update and then Amazon EKS updates the Amazon EKS add\-on for you\.

------
#### [ eksctl ]

**To update the CoreDNS Amazon EKS add\-on using `eksctl`**

1. Check the current version of your `coredns` Amazon EKS add\-on\. Replace *`my-cluster`* with your cluster name\.

   ```
   eksctl get addon --name coredns --cluster my-cluster
   ```

   The example output is as follows\.

   ```
   NAME            VERSION                 STATUS  ISSUES  IAMROLE UPDATE AVAILABLE
   coredns          v1.8.7-eksbuild.2      ACTIVE  0               v1.8.7-eksbuild.3
   ```

1. Update the add\-on to the version returned under `UPDATE AVAILABLE` in the output of the previous step\.

   ```
   eksctl update addon --name coredns --version v1.8.7-eksbuild.3 --cluster my-cluster --force
   ```

   If you remove the **\-\-*force*** option and any of the Amazon EKS add\-on settings conflict with your existing settings, then updating the Amazon EKS add\-on fails, and you receive an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\. For more information about other options for this setting, see [Addons](https://eksctl.io/usage/addons/) in the `eksctl` documentation\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------
#### [ AWS Management Console ]

**To update the CoreDNS Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, choose **Clusters**, and then select the name of the cluster that you want to update the CoreDNS Amazon EKS add\-on for\. 

1. Choose the **Add\-ons** tab\.

1. Select the radio button in the upper right of the **coredns** box and then choose **Edit**\.

   1. Select the **Version** of the Amazon EKS add\-on that you want to use\. We recommend selecting the latest version\.

   1. For **Conflict resolution method**, select one of the options\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

   1. Select **Update**\.

------
#### [ AWS CLI ]

**To update the CoreDNS Amazon EKS add\-on using the AWS CLI**

1. Check the current version of your CoreDNS add\-on\. Replace `my-cluster` with your cluster name\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name coredns --query "addon.addonVersion" --output text
   ```

   The example output is as follows\.

   ```
   v1.8.7-eksbuild.3
   ```

1. Determine which versions of the CoreDNS add\-on are available for your cluster's version\.

   ```
   aws eks describe-addon-versions --addon-name coredns --kubernetes-version 1.23 \
       --query "addons[].addonVersions[].[addonVersion, compatibilities[].defaultVersion]" --output text
   ```

   The example output is as follows\.

   ```
   v1.8.7-eksbuild.3
   False
   v1.8.7-eksbuild.2
   True
   ```

   The version with `True` underneath is the default version deployed when the add\-on is created\. The version deployed when the add\-on is created might not be the latest available version\. In the previous output, a newer version than the version deployed when the add\-on is created is available\.

1. Update the add\-on to the latest version\.

   ```
   aws eks update-addon --cluster-name my-cluster --addon-name coredns --addon-version v1.8.7-eksbuild.3 --resolve-conflicts PRESERVE
   ```

   The *PRESERVE* option preserves any custom settings that you've set for the add\-on\. For more information about other options for this setting, see [update\-addon](https://docs.aws.amazon.com/cli/latest/reference/eks/update-addon.html) in the Amazon EKS Command Line Reference\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------

## Deleting the CoreDNS Amazon EKS add\-on<a name="removing-coredns-eks-add-on"></a>

You have two options when deleting an Amazon EKS add\-on:
+ **Preserve the add\-on's software on your cluster** – This option removes Amazon EKS management of any settings and the ability for Amazon EKS to notify you of updates and automatically update the Amazon EKS add\-on after you initiate an update, but preserves the add\-on's software on your cluster\. This option makes the add\-on a self\-managed add\-on, rather than an Amazon EKS add\-on\. There is no downtime for the add\-on\.
+ **Deleting the add\-on software entirely from your cluster** – You should only delete the Amazon EKS add\-on from your cluster if there are no resources on your cluster are dependent on the functionality that the add\-on provides\. After deleting the Amazon EKS add\-on, you can add it again if you want to\.

If the add\-on has an IAM account associated with it, the IAM account is not deleted\.

Select the tab with the name of the tool that you want to use for deleting the CoreDNS Amazon EKS add\-on\.

------
#### [ eksctl ]

**To delete the CoreDNS Amazon EKS add\-on using `eksctl`**  
Replace *`my-cluster`* with the name of your cluster and then run the following command\. Removing `--preserve` deletes the add\-on software from your cluster\.

```
eksctl delete addon --cluster my-cluster --name coredns --preserve
```

------
#### [ AWS Management Console ]

**To delete the CoreDNS Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, choose **Clusters**, and then select the name of the cluster that you want to remove the CoreDNS Amazon EKS add\-on from\.

1. Choose the **Add\-ons** tab\.

1. Select the radio button in the upper right of the **coredns** box and then choose **Remove**\. Type **coredns** and then select **Remove**\.

------
#### [ AWS CLI ]

**To delete the CoreDNS Amazon EKS add\-on using the AWS CLI**  
Replace `my-cluster` with the name of your cluster and then run the following command\. Removing `--preserve` deletes the add\-on software from your cluster\.

```
aws eks delete-addon --cluster-name my-cluster --addon-name coredns --preserve
```

------

## Updating the CoreDNS self\-managed add\-on<a name="updating-coredns-add-on"></a>

If you have a cluster that you have not added the CoreDNS Amazon EKS add\-on to, complete the following steps to update the add\-on\. If you've added the CoreDNS Amazon EKS add\-on, complete the procedure in [Updating the CoreDNS Amazon EKS add\-on](#updating-coredns-eks-add-on) instead\.

**To update the CoreDNS self\-managed add\-on using `kubectl`**

1. Check the current version of your CoreDNS add\-on\.

   ```
   kubectl describe deployment coredns --namespace kube-system | grep Image | cut -d "/" -f 3
   ```

   The example output is as follows\.

   ```
   coredns:v1.8.0
   ```

1. If your current CoreDNS version is `1.5.0` or later, but earlier than the version listed in the [CoreDNS versions](#coredns-versions) table, then skip this step\. If your current version is earlier than `1.5.0`, then you need to modify the `ConfigMap` for CoreDNS to use the forward add\-on, rather than the proxy add\-on\.

   1. Open the configmap with the following command\.

      ```
      kubectl edit configmap coredns -n kube-system
      ```

   1. Replace `proxy` in the following line with `forward`\. Save the file and exit the editor\.

      ```
      proxy . /etc/resolv.conf
      ```

1. If you originally deployed your cluster on Kubernetes `1.17` or earlier, then you may need to remove a discontinued term from your CoreDNS manifest\.
**Important**  
You must complete this before upgrading to CoreDNS version `1.7.0`, but it's recommended that you complete this step even if you're upgrading to an earlier version\. 

   1. Check to see if your CoreDNS manifest has the line\.

      ```
      kubectl get configmap coredns -n kube-system -o jsonpath='{$.data.Corefile}' | grep upstream
      ```

      If no output is returned, your manifest doesn't have the line and you can skip to the next step to update CoreDNS\. If output is returned, then you need to remove the line\.

   1. Edit the `ConfigMap` with the following command, removing the line in the file that has the word `upstream` in it\. Do not change anything else in the file\. Once the line is removed, save the changes\.

      ```
      kubectl edit configmap coredns -n kube-system -o yaml
      ```

1. Retrieve your current CoreDNS image:

   ```
   kubectl get deployment coredns --namespace kube-system \
       -o=jsonpath='{$.spec.template.spec.containers[:1].image}'
   ```

1. If you're updating to CoreDNS `1.8.3` or later, then you need to add the `endpointslices` permission to the `system:coredns` Kubernetes `clusterrole`\.

   ```
   kubectl edit clusterrole system:coredns -n kube-system
   ```

   Add the following lines under the existing permissions lines in the `rules` section of the file\.

   ```
   ...
   - apiGroups:
     - discovery.k8s.io
     resources:
     - endpointslices
     verbs:
     - list
     - watch
   ...
   ```

1. Update the CoreDNS add\-on by replacing *602401143452* and `region-code` with the values from the output returned in a previous step\.Replace *`1.8.7-eksbuild.2`* with your cluster's [recommended CoreDNS version](#coredns-versions) or later:

   ```
   kubectl set image --namespace kube-system deployment.apps/coredns \
       coredns=602401143452.dkr.ecr.region-code.amazonaws.com/eks/coredns:v1.8.7-eksbuild.2
   ```