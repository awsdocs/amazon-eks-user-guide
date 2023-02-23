# Updating the CoreDNS self\-managed add\-on<a name="managing-coredns"></a>

**Important**  
This topic will be removed from this guide on July 1, 2023\. We recommend adding the Amazon EKS type of the add\-on to your cluster instead of using the self\-managed type of the add\-on\. If you're not familiar with the difference between the types, see [Amazon EKS add\-ons](eks-add-ons.md)\. For more information about adding an Amazon EKS add\-on, to your cluster, see [Creating an add\-on](managing-add-ons.md#creating-an-add-on)\.

CoreDNS is a flexible, extensible DNS server that can serve as the Kubernetes cluster DNS\. When you launch an Amazon EKS cluster with at least one node, two replicas of the CoreDNS image are deployed by default, regardless of the number of nodes deployed in your cluster\. The CoreDNS pods provide name resolution for all pods in the cluster\. The CoreDNS pods can be deployed to Fargate nodes if your cluster includes an [AWS Fargate profile](fargate-profile.md) with a namespace that matches the namespace for the CoreDNS `deployment`\. For more information about CoreDNS, see [Using CoreDNS for Service Discovery](https://kubernetes.io/docs/tasks/administer-cluster/coredns/) in the Kubernetes documentation\.

The following table lists the latest version of the CoreDNS container image available for each Amazon EKS cluster version\.<a name="coredns-versions"></a>


**Latest available self\-managed CoreDNS container image version for each Amazon EKS cluster version**  

| Kubernetes version | `1.25` | `1.24` | `1.23` | `1.22` | `1.21` | `1.20` | `1.19` | 
| --- | --- | --- | --- | --- | --- | --- | --- | 
|  | v1\.9\.3\-eksbuild\.2 | v1\.8\.7\-eksbuild\.3 | v1\.8\.7\-eksbuild\.3 | v1\.8\.7\-eksbuild\.3 | v1\.8\.4\-eksbuild\.2 | v1\.8\.3\-eksbuild\.1 | 1\.8\.0 | 

**Important**  
When you [update an Amazon EKS add\-on type](managing-add-ons.md#updating-an-add-on), you specify a valid Amazon EKS add\-on version, which might not be a version listed in this table\. This is because [Amazon EKS add\-on](eks-add-ons.md#add-ons-coredns) versions don't always match container image versions specified when updating the self\-managed type of this add\-on\. When you update the self\-managed type of this add\-on, you specify a valid container image version listed in this table\. 

**Prerequisites**
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\.
+ If your cluster is `1.21` or later, make sure that your Amazon VPC CNI plugin for Kubernetes and CoreDNS add\-ons are at the minimum versions listed in [Cluster add\-ons](service-accounts.md#boundserviceaccounttoken-validated-add-on-versions)\.

**To update the CoreDNS self\-managed add\-on**

1. Confirm that you have the self\-managed type of the add\-on installed on your cluster\. Replace *my\-cluster* with the name of your cluster\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name coredns --query addon.addonVersion --output text
   ```

   If an error message is returned, you have the self\-managed type of the add\-on installed on your cluster\. The remaining steps in this topic are for updating the self\-managed type of the add\-on\. If a version number is returned, you have the Amazon EKS type of the add\-on installed on your cluster\. To update it, use the procedure in [Updating an add\-on](managing-add-ons.md#updating-an-add-on), rather than using the procedure in this topic\. If you're not familiar with the differences between the add\-on types, see [Amazon EKS add\-ons](eks-add-ons.md)\.

1. See which version of the container image is currently installed on your cluster\.

   ```
   kubectl describe deployment coredns -n kube-system | grep Image | cut -d ":" -f 3
   ```

   The example output is as follows\.

   ```
   v1.8.7-eksbuild.2
   ```

1. If your current CoreDNS version is `v1.5.0` or later, but earlier than the version listed in the [CoreDNS versions](#coredns-versions) table, then skip this step\. If your current version is earlier than `1.5.0`, then you need to modify the `ConfigMap` for CoreDNS to use the forward add\-on, rather than the proxy add\-on\.

   1. Open the configmap with the following command\.

      ```
      kubectl edit configmap coredns -n kube-system
      ```

   1. Replace `proxy` in the following line with `forward`\. Save the file and exit the editor\.

      ```
      proxy . /etc/resolv.conf
      ```

1. If you originally deployed your cluster on Kubernetes `1.17` or earlier, then you may need to remove a discontinued line from your CoreDNS manifest\.
**Important**  
You must complete this step before updating to CoreDNS version `1.7.0`, but it's recommended that you complete this step even if you're updating to an earlier version\. 

   1. Check to see if your CoreDNS manifest has the line\.

      ```
      kubectl get configmap coredns -n kube-system -o jsonpath='{$.data.Corefile}' | grep upstream
      ```

      If no output is returned, your manifest doesn't have the line and you can skip to the next step to update CoreDNS\. If output is returned, then you need to remove the line\.

   1. Edit the `ConfigMap` with the following command, removing the line in the file that has the word `upstream` in it\. Do not change anything else in the file\. Once the line is removed, save the changes\.

      ```
      kubectl edit configmap coredns -n kube-system -o yaml
      ```

1. Retrieve your current CoreDNS image version:

   ```
   kubectl describe deployment coredns -n kube-system | grep Image
   ```

   The example output is as follows\.

   ```
   602401143452.dkr.ecr.region-code.amazonaws.com/eks/coredns:v1.8.7-eksbuild.2
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

1. Update the CoreDNS add\-on by replacing *602401143452* and `region-code` with the values from the output returned in a previous step\. Replace *`1.9.3-eksbuild.2`* with the CoreDNS version listed in the [Latest available self\-managed CoreDNS container image version for each Amazon EKS cluster version](#coredns-versions) table\.

   ```
   kubectl set image deployment.apps/coredns -n kube-system  coredns=602401143452.dkr.ecr.region-code.amazonaws.com/eks/coredns:v1.9.3-eksbuild.2
   ```

   The example output is as follows\.

   ```
   deployment.apps/coredns image updated
   ```

1. Check the container image version again to confirm that it was updated to the version that you specified in the previous step\.

   ```
   kubectl describe deployment coredns -n kube-system | grep Image | cut -d ":" -f 3
   ```

   The example output is as follows\.

   ```
   v1.8.7-eksbuild.3
   ```