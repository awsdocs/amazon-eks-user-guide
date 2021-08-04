# Managing the CoreDNS add\-on<a name="managing-coredns"></a>

CoreDNS is a flexible, extensible DNS server that can serve as the Kubernetes cluster DNS\. When you launch an Amazon EKS cluster with at least one node, two replicas of the CoreDNS image are deployed by default, regardless of the number of nodes deployed in your cluster\. The CoreDNS Pods provide name resolution for all Pods in the cluster\. The CoreDNS Pods can be deployed to Fargate nodes if your cluster includes an [AWS Fargate profile](fargate-profile.md) with a namespace that matches the namespace for the CoreDNS `Deployment`\. For more information about CoreDNS, see [Using CoreDNS for Service Discovery](https://kubernetes.io/docs/tasks/administer-cluster/coredns/) in the Kubernetes documentation\.

The following table lists the version of the CoreDNS add\-on that is deployed with each Amazon EKS cluster version\.<a name="coredns-versions"></a>


**CoreDNS version deployed with each Amazon EKS supported cluster version**  

| Kubernetes version | 1\.21 | 1\.20 | 1\.19 | 1\.18 | 1\.17 | 1\.16 | 
| --- | --- | --- | --- | --- | --- | --- | 
| CoreDNS | 1\.8\.3 | 1\.8\.3 | 1\.8\.0 | 1\.7\.0 | 1\.6\.6 | 1\.6\.6 | 

If you have a 1\.18 or later cluster that you have not added the CoreDNS Amazon EKS add\-on to, you can add it using the procedure in [Adding the CoreDNS Amazon EKS add\-on](#adding-coredns-eks-add-on)\. If you created your 1\.18 or later cluster using the AWS Management Console on or after May 19, 2021, the CoreDNS Amazon EKS add\-on is already on your cluster\. If you created your 1\.18 or later cluster using any other tool, and want to use the CoreDNS Amazon EKS add\-on, then you must add it to your cluster yourself\.

If you've added the CoreDNS Amazon EKS add\-on to your 1\.18 or later cluster, you can manage it using the procedures in the [Updating the CoreDNS Amazon EKS add\-on](#updating-coredns-eks-add-on) and [Removing the CoreDNS Amazon EKS add\-on](#removing-coredns-eks-add-on) sections\. For more information about Amazon EKS add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\.

If you have not added the CoreDNS Amazon EKS add\-on, the CoreDNS self\-managed add\-on is still running on your cluster\. You can update the CoreDNS self\-managed add\-on using the procedure in [Updating the CoreDNS self\-managed add\-on](#updating-coredns-add-on)\.

## Adding the CoreDNS Amazon EKS add\-on<a name="adding-coredns-eks-add-on"></a>

Select the tab with the name of the tool that you want to use to add the CoreDNS Amazon EKS add\-on to your cluster with\. 

**Important**  
Before adding the CoreDNS Amazon EKS add\-on, confirm that you do not self\-manage any settings that Amazon EKS will start managing\. To determine which settings Amazon EKS manages, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------
#### [ eksctl ]

**To add the CoreDNS Amazon EKS add\-on using `eksctl`**  
Replace *`my-cluster`* \(including `<>`\) with the name of your cluster and then run the following command\.

```
eksctl create addon --name coredns --cluster <my-cluster> --force
```

If you remove the `--force` option and any of the Amazon EKS add\-on settings conflict with your existing settings, then adding the Amazon EKS add\-on fails, and you receive an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------
#### [ AWS Management Console ]

**To add the CoreDNS Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation, select **Clusters**, and then select the name of the cluster that you want to configure the CoreDNS Amazon EKS add\-on for\.

1. Choose the **Configuration** tab and then choose the **Add\-ons** tab\.

1. Select **Add new**\.

   1. Select **CoreDNS** for **Name**\.

   1. Select the **Version** you'd like to use\.

   1. If you select **Override existing configuration for this add\-on on the cluster\.**, then any setting for the existing add\-on can be overwritten with the Amazon EKS add\-on's settings\. If you don't enable this option and any of the Amazon EKS add\-on settings conflict with your existing settings, then adding the Amazon EKS add\-on fails, and you receive an error message to help you resolve the conflict\. Before selecting this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

   1. Select **Add**\.

------
#### [ AWS CLI ]

**To add the CoreDNS Amazon EKS add\-on using the AWS CLI**  
Replace *my\-cluster* with the name of your cluster and then run the following command\.

```
aws eks create-addon \
    --cluster-name my-cluster \
    --addon-name coredns \
    --resolve-conflicts OVERWRITE
```

If you remove the `--resolve-conflicts OVERWRITE` option and any of the Amazon EKS add\-on settings conflict with your existing settings, then creating the add\-on fails, and you receive an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------

## Updating the CoreDNS Amazon EKS add\-on<a name="updating-coredns-eks-add-on"></a>

This procedure is for updating the CoreDNS Amazon EKS add\-on\. If you haven't added the CoreDNS Amazon EKS add\-on, complete the procedure in [Updating the CoreDNS self\-managed add\-on](#updating-coredns-add-on) instead, or [add the CoreDNS Amazon EKS add\-on](#adding-coredns-eks-add-on)\. Amazon EKS does not automatically update CoreDNS on your cluster when new versions are released or after you [update your cluster](update-cluster.md) to a new Kubernetes minor version\. To update CoreDNS on an existing cluster, you must initiate the update and then Amazon EKS updates the Amazon EKS add\-on for you\.

------
#### [ eksctl ]

**To update the CoreDNS Amazon EKS add\-on using `eksctl`**

1. Check the current version of your `coredns` Amazon EKS add\-on\. Replace *`<my-cluster>`* \(including *`<>`*\) with your cluster name\.

   ```
   eksctl get addon --name coredns --cluster <my-cluster>
   ```

   Output

   ```
   NAME            VERSION                 STATUS  ISSUES  IAMROLE UPDATE AVAILABLE
   coredns          v1.8.0-eksbuild.1      ACTIVE  0               v1.8.3-eksbuild.1
   ```

1. Update the add\-on to the version returned under `UPDATE AVAILABLE` in the output of the previous step\.

   ```
   eksctl update addon \
       --name coredns \
       --version <v1.8.3-eksbuild.1> \
       --cluster <my-cluster> \
       --force
   ```

   If you remove the `--force` option and any of the Amazon EKS add\-on settings conflict with your existing settings, then updating the Amazon EKS add\-on fails, and you receive an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------
#### [ AWS Management Console ]

**To update the CoreDNS Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation, select **Clusters**, and then select the name of the cluster that you want to update the CoreDNS Amazon EKS add\-on for\. 

1. Choose the **Configuration** tab and then choose the **Add\-ons** tab\.

1. Select the box in the top right of the **coredns** box and then choose **Edit**\.

   1. Select the **Version** of the Amazon EKS add\-on that you want to use\.

   1. If you select **Override existing configuration for this add\-on on the cluster\.**, then any setting for the existing add\-on can be overwritten with the Amazon EKS add\-on's settings\. If you don't enable this option and any of the Amazon EKS add\-on settings conflict with your existing settings, then updating the add\-on to an Amazon EKS add\-on fail, and you receive an error message to help you resolve the conflict\. Before selecting this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

   1. Select **Update**\.

------
#### [ AWS CLI ]

**To update the CoreDNS Amazon EKS add\-on using the AWS CLI**

1. Check the current version of your CoreDNS add\-on\. Replace *my\-cluster* with your cluster name\.

   ```
   aws eks describe-addon \
       --cluster-name my-cluster \
       --addon-name coredns \
       --query "addon.addonVersion" \
       --output text
   ```

   Output:

   ```
   1.7.0
   ```

1. Determine which versions of the CoreDNS add\-on are available for your cluster's version\.

   ```
   aws eks describe-addon-versions \
       --addon-name coredns \
       --kubernetes-version 1.19 \
       --query "addons[].addonVersions[].[addonVersion, compatibilities[].defaultVersion]" \
       --output text
   ```

   Output

   ```
   1.8.0
   True
   1.7.0
   False
   ```

   The version with `True` underneath is the default version deployed with new clusters\.

1. Update the add\-on to the version with `True` returned in the output of the previous step\. You can also update to a later version, if returned in the output\.

   ```
   aws eks update-addon \
       --cluster-name my-cluster \
       --addon-name coredns \
       --addon-version 1.8.0 \
       --resolve-conflicts OVERWRITE
   ```

   If you remove the `--resolve-conflicts OVERWRITE` option and any of the Amazon EKS add\-on settings conflict with your existing settings, then updating the add\-on fails, and you receive an error message to help you resolve the conflict\. Before specifying this option, make sure that the Amazon EKS add\-on doesn't manage settings that you need to manage, because those settings are overwritten with this option\. For more information about Amazon EKS add\-on configuration management, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

------

## Removing the CoreDNS Amazon EKS add\-on<a name="removing-coredns-eks-add-on"></a>

**Important**  
Removing the Amazon EKS add\-on from your cluster removes its pods from your cluster, not just the settings that were managed by Amazon EKS\. You should only remove the Amazon EKS add\-on from your cluster if none of the pods on your cluster are dependent on the functionality that the add\-on provides\. After removing the Amazon EKS add\-on, you can add it again if you want to\.

------
#### [ eksctl ]

**To remove the CoreDNS Amazon EKS add\-on using `eksctl`**  
Replace *`my-cluster`* \(including `<>`\) with the name of your cluster and then run the following command\.

```
eksctl delete addon --cluster <my-cluster> --name coredns
```

------
#### [ AWS Management Console ]

**To remove the CoreDNS Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation, select **Clusters**, and then select the name of the cluster that you want to remove the CoreDNS Amazon EKS add\-on for\.

1. Choose the **Configuration** tab and then choose the **Add\-ons** tab\.

1. Select the checkbox in the top right of the **coredns** box and then choose **Remove**\. Type **coredns** and then select **Remove**\.

------
#### [ AWS CLI ]

**To remove the CoreDNS Amazon EKS add\-on using the AWS CLI**  
Replace *my\-cluster* with the name of your cluster and then run the following command\.

```
aws eks delete-addon --cluster-name my-cluster --addon-name coredns
```

------

## Updating the CoreDNS self\-managed add\-on<a name="updating-coredns-add-on"></a>

If you have a 1\.17 or earlier cluster, or a 1\.18 or later cluster that you have not added the CoreDNS Amazon EKS add\-on to, complete the following steps to update the add\-on\. If you've added the CoreDNS Amazon EKS add\-on, complete the procedure in [Updating the CoreDNS Amazon EKS add\-on](#updating-coredns-eks-add-on) instead\.

**To update the CoreDNS self\-managed add\-on using `kubectl`**

1. Check the current version of your CoreDNS add\-on\.

   ```
   kubectl describe deployment coredns \
       --namespace kube-system \
       | grep Image \
       | cut -d "/" -f 3
   ```

   Output:

   ```
   coredns:v1.8.0
   ```

1. If your current CoreDNS version is 1\.5\.0 or later, but earlier than the version listed in the [CoreDNS versions](#coredns-versions) table, then skip this step\. If your current version is earlier than 1\.5\.0, then you need to modify the `ConfigMap` for CoreDNS to use the forward add\-on, rather than the proxy add\-on\.

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
   kubectl get deployment coredns \
       --namespace kube-system \
       -o=jsonpath='{$.spec.template.spec.containers[:1].image}'
   ```

1. If you're updating to CoreDNS 1\.8\.3, you need to add the `endpointslices` permission to the `system:coredns` Kubernetes `clusterrole`\.

   ```
   kubectl edit clusterrole system:coredns -n kube-system
   ```

   Add the following line under the existing permissions lines in the file\.

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

1. Update the CoreDNS add\-on by replacing *<602401143452>* \(including *`<>`*\) , *<cn\-north\-1>*, and *<com>* with the values from the output returned in the previous step\. Replace *`<1.8.3>`* with your cluster's [recommended CoreDNS version](#coredns-versions) or later:

   ```
   kubectl set image --namespace kube-system deployment.apps/coredns \
       coredns=<602401143452>.dkr.ecr.<us-west-2>.amazonaws.<com>/eks/coredns:v<1.8.3>-eksbuild.1
   ```