# Updating the CoreDNS add\-on<a name="managing-coredns"></a>

CoreDNS is a flexible, extensible DNS server that can serve as the Kubernetes cluster DNS\. When you launch an Amazon EKS cluster with at least one node, two replicas of the CoreDNS image are deployed by default, regardless of the number of nodes deployed in your cluster\. The CoreDNS pods provide name resolution for all pods in the cluster\. The CoreDNS pods can be deployed to Fargate nodes if your cluster includes an [AWS Fargate profile](fargate-profile.md) with a namespace that matches the namespace for the CoreDNS `deployment`\. For more information about CoreDNS, see [Using CoreDNS for Service Discovery](https://kubernetes.io/docs/tasks/administer-cluster/coredns/) in the Kubernetes documentation\.

The following table lists the latest version of the CoreDNS add\-on that is available for each Amazon EKS cluster version\.<a name="coredns-versions"></a>


**Latest available CoreDNS container image version for each Amazon EKS cluster version**

| Kubernetes version | `1.24` | `1.23` | `1.22` | `1.21` | `1.20` | `1.19` |
| --- | --- | --- | --- | --- | --- | --- |
| CoreDNS | v1\.8\.7\-eksbuild\.3 | v1\.8\.7\-eksbuild\.3 | v1\.8\.7\-eksbuild\.1 | v1\.8\.4\-eksbuild\.2 | v1\.8\.3\-eksbuild\.1 | 1\.8\.0 |

You can see which version is installed on your cluster with the following command\.

```
kubectl describe deployment coredns -n kube-system | grep Image | cut -d ":" -f 3
```

The example output is as follows\.

```
v1.8.7-eksbuild.2
```

Before updating your CoreDNS version, consider the following points:

**Prerequisites**
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\.
+ If your cluster is `1.21` or later, make sure that your Amazon VPC CNI plugin for Kubernetes and `kube-proxy` add\-ons are at the minimum versions listed in [Service account tokens](service-accounts.md#boundserviceaccounttoken-validated-add-on-versions)\.

**To update your CoreDNS add\-on version**

1. Determine whether you have the Amazon EKS or self\-managed type of the add\-on installed on your cluster\. Replace *my\-cluster* with the name of your cluster\. If you don't know the difference between the two types of add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name coredns --query addon.addonVersion --output text
   ```

   The output returned is different, depending on the add\-on type installed on your cluster\.
   + **Amazon EKS add\-on**

     ```
     v1.8.7-eksbuild.2
     ```
   + **Self\-managed add\-on**

     ```
     An error occurred (ResourceNotFoundException) when calling the DescribeAddon operation: No addon: coredns found in cluster: my-cluster
     ```

1. Update your CoreDNS add\-on using the procedure for the type of add\-on that you have installed on your cluster\.

------
#### [ Amazon EKS add\-on ]

   Follow the procedure in [Updating an add\-on](managing-add-ons.md#updating-an-add-on)\. When using that procedure, you're asked to provide the following information:
   + **Add\-on name** – Specify `coredns`\.
   + **Version** – If you use the AWS Management Console to update the add\-on, you can select any available version shown in the console\. If you use any other tool to update the add\-on, you can specify any version returned by the AWS CLI or `eksctl` using the procedure in [Updating an add\-on](managing-add-ons.md#updating-an-add-on)\. The version of the add\-on that you install might not match a version in the [Latest available CoreDNS container image version for each Amazon EKS cluster version](#coredns-versions) table\.
   + **IAM role** – An IAM role isn't used for this add\-on\.

   You can also [create](managing-add-ons.md#creating-an-add-on) or [delete](managing-add-ons.md#removing-an-add-on) the add\-on\. When creating or deleting the add\-on, you can use the same information listed for updating the add\-on\.

------
#### [ Self\-managed add\-on ]

   If you want to install the Amazon EKS type of the add\-on, see [Creating an add\-on](managing-add-ons.md#creating-an-add-on)\. When following the procedure in that topic, specify the add\-on with the name `coredns`\. Complete the following procedure to update the self\-managed add\-on\.

**To update the CoreDNS add\-on**

   1. Check the current version of your CoreDNS add\-on\.

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

   1. Update the CoreDNS add\-on by replacing *602401143452* and `region-code` with the values from the output returned in a previous step\. Replace *`1.8.7-eksbuild.3`* with the version that you want to update to\.

      ```
      kubectl set image deployment.apps/coredns -n kube-system  coredns=602401143452.dkr.ecr.region-code.amazonaws.com/eks/coredns:v1.8.7-eksbuild.3
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

------
