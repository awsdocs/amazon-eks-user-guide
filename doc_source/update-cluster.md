# Updating an Amazon EKS Cluster<a name="update-cluster"></a>

When a new Kubernetes version is available in Amazon EKS, you can update your cluster to the latest version\.

New Kubernetes versions introduce significant changes, and as such, we recommend that you test the behavior of your applications against a new Kubernetes version before performing the update on your production clusters\. You can achieve this by building a continuous integration workflow to test your application behavior end\-to\-end before moving to a new Kubernetes version\.

**Note**  
Although Amazon EKS runs a highly available control plane, it is possible to experience minor service interruptions during an update\. For example, if you attempt to connect to an API server just before or just after it is terminated and replaced by a new API server running the new version of Kubernetes, you may experience API call errors or connectivity issues\. If this happens, retry your API operations until they succeed\.

**To update an existing cluster with the console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the name of the cluster to update and choose **Update cluster version**\.

1. For **Kubernetes version**, select the version to update your cluster to and choose **Update**\.

1. For **Cluster name**, type the name of your cluster and choose **Confirm**\.
**Note**  
The cluster update should finish within a few minutes\.

1. Patch the `kube-proxy` daemonset to use the image that corresponds to your current cluster Kubernetes version \(in this example, `1.11.5`\)\.

   ```
   kubectl patch daemonset kube-proxy \
   -n kube-system \
   -p '{"spec": {"template": {"spec": {"containers": [{"image": "602401143452.dkr.ecr.us-west-2.amazonaws.com/eks/kube-proxy:v1.11.5","name":"kube-proxy"}]}}}}'
   ```

1. Clusters that were created with Kubernetes version 1\.10 shipped with `kube-dns` as the default DNS and service discovery provider\. If you have updated a 1\.10 cluster to 1\.11, and you would like to use CoreDNS for DNS and service discovery, you must install CoreDNS and remove `kube-dns`\. For more information, see [Installing CoreDNS](coredns.md)

1. After your cluster update is complete, update your worker nodes to the same Kubernetes version of your updated cluster\. For more information, see [Worker Node Updates](update-workers.md)\.

**To update an existing cluster with the AWS CLI**

1. Update your cluster with the following AWS CLI command\. Substitute your cluster name and desired Kubernetes minor version\.

   ```
   aws eks update-cluster-version --name prod --kubernetes-version 1.11
   ```

   Output:

   ```
   {
       "update": {
           "id": "b5f0ba18-9a87-4450-b5a0-825e6e84496f",
           "status": "InProgress",
           "type": "VersionUpdate",
           "params": [
               {
                   "type": "Version",
                   "value": "1.11"
               },
               {
                   "type": "PlatformVersion",
                   "value": "eks.1"
               }
           ],
           "createdAt": 1544051347.305,
           "errors": []
       }
   }
   ```

1. Monitor the status of your cluster update with the following command, using the cluster name and update ID that was returned by the previous command\. Your update is complete when the status is shown as `Successful`\.

   ```
   aws eks describe-update --name prod --update-id b5f0ba18-9a87-4450-b5a0-825e6e84496f
   ```

   Output:

   ```
   {
       "update": {
           "id": "b5f0ba18-9a87-4450-b5a0-825e6e84496f",
           "status": "Successful",
           "type": "VersionUpdate",
           "params": [
               {
                   "type": "Version",
                   "value": "1.11"
               },
               {
                   "type": "PlatformVersion",
                   "value": "eks.1"
               }
           ],
           "createdAt": 1544051347.305,
           "errors": []
       }
   }
   ```

1. Patch the `kube-proxy` daemonset to use the image that corresponds to your current cluster Kubernetes version \(in this example, `1.11.5`\)\.

   ```
   kubectl patch daemonset kube-proxy \
   -n kube-system \
   -p '{"spec": {"template": {"spec": {"containers": [{"image": "602401143452.dkr.ecr.us-west-2.amazonaws.com/eks/kube-proxy:v1.11.5","name":"kube-proxy"}]}}}}'
   ```

1. Clusters that were created with Kubernetes version 1\.10 shipped with `kube-dns` as the default DNS and service discovery provider\. If you have updated a 1\.10 cluster to 1\.11, and you would like to use CoreDNS for DNS and service discovery, you must install CoreDNS and remove `kube-dns`\. For more information, see [Installing CoreDNS](coredns.md)

1. After your cluster update is complete, update your worker nodes to the same Kubernetes version of your updated cluster\. For more information, see [Worker Node Updates](update-workers.md)\.