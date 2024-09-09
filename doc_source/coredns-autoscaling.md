# Scale CoreDNSPods for high DNS traffic<a name="coredns-autoscaling"></a>

When you launch an Amazon EKS cluster with at least one node, a Deployment of two replicas of the CoreDNS image are deployed by default, regardless of the number of nodes deployed in your cluster\. The CoreDNS Pods provide name resolution for all Pods in the cluster\. Applications use name resolution to connect to pods and services in the cluster as well as connecting to services outside the cluster\. As the number of requests for name resolution \(queries\) from pods increase, the CoreDNS pods can get overwhelmed and slow down, and reject requests that the pods can’t handle\.

To handle the increased load on the CoreDNS pods, consider an autoscaling system for CoreDNS\. Amazon EKS can manage the autoscaling of the CoreDNS Deployment in the EKS Add\-on version of CoreDNS\. This CoreDNS autoscaler continuously monitors the cluster state, including the number of nodes and CPU cores\. Based on that information, the controller will dynamically adapt the number of replicas of the CoreDNS deployment in an EKS cluster\. This feature works for CoreDNS `v1.9` and EKS release version `1.25` and later\. For more information about which versions are compatible with CoreDNS Autoscaling, see the following section\.

We recommend using this feature in conjunction with other [EKS Cluster Autoscaling best practices](https://aws.github.io/aws-eks-best-practices/cluster-autoscaling/) to improve overall application availability and cluster scalability\.

## Prerequisites<a name="coredns-autoscaling-prereqs"></a>

For Amazon EKS to scale your CoreDNS deployment, there are three prerequisites:
+ You must be using the *EKS Add\-on* version of CoreDNS\.
+ Your cluster must be running at least the minimum cluster versions and platform versions\.
+ Your cluster must be running at least the minimum version of the EKS Add\-on of CoreDNS\.

### Minimum cluster version<a name="coredns-autoscaling-cluster-version"></a>

Autoscaling of CoreDNS is done by a new component in the cluster control plane, managed by Amazon EKS\. Because of this, you must upgrade your cluster to an EKS release that supports the minimum platform version that has the new component\.

A new Amazon EKS cluster\. To deploy one, see [Get started with Amazon EKS](getting-started.md)\. The cluster must be Kubernetes version `1.25` or later\. The cluster must be running one of the Kubernetes versions and platform versions listed in the following table or a later version\. Note that any Kubernetes and platform versions later than those listed are also supported\. You can check your current Kubernetes version by replacing *my\-cluster* in the following command with the name of your cluster and then running the modified command:

```
aws eks describe-cluster
              --name my-cluster --query cluster.version --output
              text
```


| Kubernetes version | Platform version | 
| --- | --- | 
| `1.29.3` | `eks.7` | 
| `1.28.8` | `eks.13` | 
| `1.27.12` | `eks.17` | 
| `1.26.15` | `eks.18` | 
| `1.25.16` | `eks.19` | 

**Note**  
Every platform version of later Kubernetes versions are also supported, for example Kubernetes version `1.30` from `eks.1` and on\.

### Minimum EKS Add\-on version<a name="coredns-autoscaling-coredns-version"></a>


| Kubernetes version | `1.29` | `1.28` | `1.27` | `1.26` | `1.25` | 
| --- | --- | --- | --- | --- | --- | 
|  | v1\.11\.1\-eksbuild\.9 | v1\.10\.1\-eksbuild\.11 | v1\.10\.1\-eksbuild\.11 | v1\.9\.3\-eksbuild\.15 | v1\.9\.3\-eksbuild\.15 | 

## Configuring CoreDNS autoscaling in the AWS Management Console<a name="coredns-autoscaling-console"></a>

1. Ensure that your cluster is at or above the minimum cluster version\.

   Amazon EKS upgrades clusters between platform versions of the same Kubernetes version automatically, and you can’t start this process yourself\. Instead, you can upgrade your cluster to the next Kubernetes version, and the cluster will be upgraded to that K8s version and the latest platform version\. For example, if you upgrade from `1.25` to `1.26`, the cluster will upgrade to `1.26.15 eks.18`\.

   New Kubernetes versions sometimes introduce significant changes\. Therefore, we recommend that you test the behavior of your applications by using a separate cluster of the new Kubernetes version before you update your production clusters\.

   To upgrade a cluster to a new Kubernetes version, follow the procedure in [Update existing cluster to new Kubernetes version](update-cluster.md)\.

1. Ensure that you have the EKS Add\-on for CoreDNS, not the self\-managed CoreDNS Deployment\.

   Depending on the tool that you created your cluster with, you might not currently have the Amazon EKS add\-on type installed on your cluster\. To see which type of the add\-on is installed on your cluster, you can run the following command\. Replace `my-cluster` with the name of your cluster\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name coredns --query addon.addonVersion --output text
   ```

   If a version number is returned, you have the Amazon EKS type of the add\-on installed on your cluster and you can continue with the next step\. If an error is returned, you don't have the Amazon EKS type of the add\-on installed on your cluster\. Complete the remaining steps of the procedure [Create the CoreDNS Amazon EKS add\-on](coredns-add-on-create.md) to replace the self\-managed version with the Amazon EKS add\-on\.

1. Ensure that your EKS Add\-on for CoreDNS is at a version the same or higher than the minimum EKS Add\-on version\.

   See which version of the add\-on is installed on your cluster\. You can check in the AWS Management Console or run the following command:

   ```
   kubectl describe deployment coredns --namespace kube-system | grep coredns: | cut -d : -f 3
   ```

   An example output is as follows\.

   ```
   v1.10.1-eksbuild.13
   ```

   Compare this version with the minimum EKS Add\-on version in the previous section\. If needed, upgrade the EKS Add\-on to a higher version by following the procedure [Update the CoreDNS Amazon EKS add\-on](coredns-add-on-update.md)\.

1. Add the autoscaling configuration to the **Optional configuration settings** of the EKS Add\-on\.

   1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

   1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to configure the add\-on for\.

   1. Choose the **Add\-ons** tab\.

   1. Select the box in the top right of the CoreDNS add\-on box and then choose **Edit**\.

   1. On the **Configure CoreDNS** page:

      1. Select the **Version** that you'd like to use\. We recommend that you keep the same version as the previous step, and update the version and configuration in separate actions\.

      1. Expand the **Optional configuration settings**\.

      1. Enter the JSON key `"autoscaling":` and value of a nested JSON object with a key `"enabled":` and value `true` in **Configuration values**\. The resulting text must be a valid JSON object\. If this key and value are the only data in the text box, surround the key and value with curly braces `{}`\. The following example shows autoscaling is enabled:

         ```
         {
           "autoScaling": {
             "enabled": true
           }
         }
         ```

      1. \(Optional\) You can provide minimum and maximum values that autoscaling can scale the number of CoreDNS pods to\.

         The following example shows autoscaling is enabled and all of the optional keys have values\. We recommend that the minimum number of CoreDNS pods is always greater than 2 to provide resilience for the DNS service in the cluster\.

         ```
         {
           "autoScaling": {
             "enabled": true,
             "minReplicas": 2,
             "maxReplicas": 10
           }
         }
         ```

   1. To apply the new configuration by replacing the CoreDNS pods, choose **Save changes**\.

      Amazon EKS applies changes to the EKS Add\-ons by using a *rollout* of the Kubernetes Deployment for CoreDNS\. You can track the status of the rollout in the **Update history** of the add\-on in the AWS Management Console and with `kubectl rollout status deployment/coredns --namespace kube-system`\.

      `kubectl rollout` has the following commands:

      ```
      $ kubectl rollout
                                  
      history  -- View rollout history
      pause    -- Mark the provided resource as paused
      restart  -- Restart a resource
      resume   -- Resume a paused resource
      status   -- Show the status of the rollout
      undo     -- Undo a previous rollout
      ```

      If the rollout takes too long, Amazon EKS will undo the rollout, and a message with the type of **Addon Update** and a status of **Failed** will be added to the **Update history** of the add\-on\. To investigate any issues, start from the history of the rollout, and run `kubectl logs` on a CoreDNS pod to see the logs of CoreDNS\.

1. If the new entry in the **Update history** has a status of **Successful**, then the rollout has completed and the add\-on is using the new configuration in all of the CoreDNS pods\. As you change the number of nodes and CPU cores of nodes in the cluster, Amazon EKS scales the number of replicas of the CoreDNS deployment\.

## Configuring CoreDNS autoscaling in the AWS Command Line Interface<a name="coredns-autoscaling-cli"></a>

1. Ensure that your cluster is at or above the minimum cluster version\.

   Amazon EKS upgrades clusters between platform versions of the same Kubernetes version automatically, and you can’t start this process yourself\. Instead, you can upgrade your cluster to the next Kubernetes version, and the cluster will be upgraded to that K8s version and the latest platform version\. For example, if you upgrade from `1.25` to `1.26`, the cluster will upgrade to `1.26.15 eks.18`\.

   New Kubernetes versions sometimes introduce significant changes\. Therefore, we recommend that you test the behavior of your applications by using a separate cluster of the new Kubernetes version before you update your production clusters\.

   To upgrade a cluster to a new Kubernetes version, follow the procedure in [Update existing cluster to new Kubernetes version](update-cluster.md)\.

1. Ensure that you have the EKS Add\-on for CoreDNS, not the self\-managed CoreDNS Deployment\.

   Depending on the tool that you created your cluster with, you might not currently have the Amazon EKS add\-on type installed on your cluster\. To see which type of the add\-on is installed on your cluster, you can run the following command\. Replace `my-cluster` with the name of your cluster\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name coredns --query addon.addonVersion --output text
   ```

   If a version number is returned, you have the Amazon EKS type of the add\-on installed on your cluster\. If an error is returned, you don't have the Amazon EKS type of the add\-on installed on your cluster\. Complete the remaining steps of the procedure [Create the CoreDNS Amazon EKS add\-on](coredns-add-on-create.md) to replace the self\-managed version with the Amazon EKS add\-on\.

1. Ensure that your EKS Add\-on for CoreDNS is at a version the same or higher than the minimum EKS Add\-on version\.

   See which version of the add\-on is installed on your cluster\. You can check in the AWS Management Console or run the following command:

   ```
   kubectl describe deployment coredns --namespace kube-system | grep coredns: | cut -d : -f 3
   ```

   An example output is as follows\.

   ```
   v1.10.1-eksbuild.13
   ```

   Compare this version with the minimum EKS Add\-on version in the previous section\. If needed, upgrade the EKS Add\-on to a higher version by following the procedure [Update the CoreDNS Amazon EKS add\-on](coredns-add-on-update.md)\.

1. Add the autoscaling configuration to the **Optional configuration settings** of the EKS Add\-on\.

   Run the following AWS CLI command\. Replace `my-cluster` with the name of your cluster and the IAM role ARN with the role that you are using\.

   ```
   aws eks update-addon --cluster-name my-cluster --addon-name coredns \
       --resolve-conflicts PRESERVE --configuration-values '{"autoScaling":{"enabled":true}}'
   ```

   Amazon EKS applies changes to the EKS Add\-ons by using a *rollout* of the Kubernetes Deployment for CoreDNS\. You can track the status of the rollout in the **Update history** of the add\-on in the AWS Management Console and with `kubectl rollout status deployment/coredns --namespace kube-system`\.

   `kubectl rollout` has the following commands:

   ```
   kubectl rollout
                               
   history  -- View rollout history
   pause    -- Mark the provided resource as paused
   restart  -- Restart a resource
   resume   -- Resume a paused resource
   status   -- Show the status of the rollout
   undo     -- Undo a previous rollout
   ```

   If the rollout takes too long, Amazon EKS will undo the rollout, and a message with the type of **Addon Update** and a status of **Failed** will be added to the **Update history** of the add\-on\. To investigate any issues, start from the history of the rollout, and run `kubectl logs` on a CoreDNS pod to see the logs of CoreDNS\.

1. \(Optional\) You can provide minimum and maximum values that autoscaling can scale the number of CoreDNS pods to\.

   The following example shows autoscaling is enabled and all of the optional keys have values\. We recommend that the minimum number of CoreDNS pods is always greater than 2 to provide resilience for the DNS service in the cluster\.

   ```
   aws eks update-addon --cluster-name my-cluster --addon-name coredns \
       --resolve-conflicts PRESERVE --configuration-values '{"autoScaling":{"enabled":true,"minReplicas":2,"maxReplicas":10}}'
   ```

1. Check the status of the update to the add\-on by running the following command:

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name coredns \
   ```

   If you see this line: `"status": "ACTIVE"`, then the rollout has completed and the add\-on is using the new configuration in all of the CoreDNS pods\. As you change the number of nodes and CPU cores of nodes in the cluster, Amazon EKS scales the number of replicas of the CoreDNS deployment\.