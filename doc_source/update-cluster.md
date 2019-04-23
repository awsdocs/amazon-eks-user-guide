# Updating an Amazon EKS Cluster Kubernetes Version<a name="update-cluster"></a>

When a new Kubernetes version is available in Amazon EKS, you can update your cluster to the latest version\. New Kubernetes versions introduce significant changes, so we recommend that you test the behavior of your applications against a new Kubernetes version before performing the update on your production clusters\. You can achieve this by building a continuous integration workflow to test your application behavior end\-to\-end before moving to a new Kubernetes version\.

**Note**  
Although Amazon EKS runs a highly available control plane, you might experience minor service interruptions during an update\. For example, if you attempt to connect to an API server just before or just after it's terminated and replaced by a new API server running the new version of Kubernetes, you might experience API call errors or connectivity issues\. If this happens, retry your API operations until they succeed\.

After updating your cluster, we recommend that you update your add\-ons to the versions listed in the following table for the new Kubernetes version that you're updating to\.


| Kubernetes Version | 1\.10 | 1\.11 | 1\.12 | 
| --- | --- | --- | --- | 
| Amazon VPC CNI plug\-in | We recommend the latest available CNI version \(1\.4\.0\) | 
| DNS | kube\-dns 1\.14\.10 | CoreDNS 1\.1\.3 | CoreDNS 1\.2\.2 | 
| KubeProxy | 1\.10\.3 | 1\.11\.5 | 1\.12\.6 | 

If you're using additional add\-ons for your cluster that aren't listed in the previous table, update them to the latest compatible versions after updating your cluster\.

**To update an existing cluster with the console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the name of the cluster to update and choose **Update cluster version**\.

1. For **Kubernetes version**, select the version to update your cluster to and choose **Update**\.
**Important**  
Because Amazon EKS runs a highly available control plane, it's required that you update only one minor version at a time\. See [Kubernetes Version and Version Skew Support Policy](https://kubernetes.io/docs/setup/version-skew-policy/#kube-apiserver) for the rationale behind this\. Therefore, if your current version is 1\.10 and you want to upgrade to 1\.12, you must first upgrade your cluster to 1\.11 and then upgrade it from 1\.11 to 1\.12\. If you try updating directly from 1\.10 to 1\.12, the update version command throws an error\.

1. For **Cluster name**, type the name of your cluster and choose **Confirm**\.
**Note**  
The cluster update should finish in a few minutes\.

1. After the update is complete, find the current Kubernetes version for your cluster\.

   ```
   kubectl version --short
   Client Version: v1.13.4
   Server Version: v1.12.6-eks-d69f1b
   ```

1. Patch the `kube-proxy` daemonset to use the image that corresponds to your current cluster Kubernetes version \(in this example, `1.12.6`\)\.

   ```
   kubectl patch daemonset kube-proxy \
   -n kube-system \
   -p '{"spec": {"template": {"spec": {"containers": [{"image": "602401143452.dkr.ecr.us-west-2.amazonaws.com/eks/kube-proxy:v1.12.6","name":"kube-proxy"}]}}}}'
   ```

1. Check your cluster's DNS provider\. Clusters that were created with Kubernetes version 1\.10 shipped with `kube-dns` as the default DNS and service discovery provider\. If you have updated a 1\.10 cluster to a newer version and you want to use CoreDNS for DNS and service discovery, you must install CoreDNS and remove `kube-dns`\.

   To check if your cluster is already running CoreDNS, use the following command\.

   ```
   kubectl get pod -n kube-system -l k8s-app=kube-dns
   ```

   If the output shows `coredns` in the pod names, you're already running CoreDNS in your cluster\. If not, see [Installing CoreDNS](coredns.md) to install CoreDNS on your cluster and then return here\.

1. Check the current version of your cluster's `coredns` deployment\.

   ```
   kubectl describe deployment coredns --namespace kube-system | grep Image | cut -d "/" -f 3
   coredns:v1.1.3
   ```

   The recommended `coredns` versions for their corresponding Kubernetes versions are as follows:
   + **Kubernetes 1\.12:** `1.2.2`
   + **Kubernetes 1\.11:** `1.1.3`

   If your current `coredns` version doesn't match the recommendation for your cluster version, update the `coredns` deployment to use the recommended image\.

   ```
   kubectl set image --namespace kube-system deployment.apps/coredns \
   coredns=602401143452.dkr.ecr.us-west-2.amazonaws.com/eks/coredns:v1.2.2
   ```

1. Check the version of your cluster's Amazon VPC CNI Plugin for Kubernetes\. Use the following command to print your cluster's CNI version\.

   ```
   kubectl describe daemonset aws-node --namespace kube-system | grep Image | cut -d "/" -f 2
   ```

   Output:

   ```
   amazon-k8s-cni:1.4.0
   ```

   If your CNI version is earlier than 1\.4\.0, use the following command to upgrade your CNI version to the latest version\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.4/config/v1.4/aws-k8s-cni.yaml
   ```

   *Note!* If you are still running a Kubernetes 1.10 or older, you need to use the old CRD configuration:

   ```
   kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.4/config/v1.4/aws-k8s-cni-1.10.yaml
   ```

1. After your cluster update is complete, update your worker nodes to the same Kubernetes version of your updated cluster\. For more information, see [Worker Node Updates](update-workers.md)\.

**To update an existing cluster with the AWS CLI**

1. Update your cluster with the following AWS CLI command\. Substitute your cluster name and desired Kubernetes minor version\.

   ```
   aws eks --region region update-cluster-version --name prod --kubernetes-version 1.12
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
                   "value": "1.12"
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
**Important**  
Because Amazon EKS runs a highly available control plane, it's required that you update only one minor version at a time\. See [Kubernetes Version and Version Skew Support Policy](https://kubernetes.io/docs/setup/version-skew-policy/#kube-apiserver) for the rationale behind this\. Therefore, if your current version is 1\.10 and you want to upgrade to 1\.12, you must first upgrade your cluster to 1\.11 and then upgrade it from 1\.11 to 1\.12\. If you try updating directly from 1\.10 to 1\.12, the update version command throws an error\.

1. Monitor the status of your cluster update with the following command, using the cluster name and update ID that the previous command returned\. Your update is complete when the status appears as `Successful`\.
**Note**  
The cluster update should finish in a few minutes\.

   ```
   aws eks --region region describe-update --name prod --update-id b5f0ba18-9a87-4450-b5a0-825e6e84496f
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
                   "value": "1.12"
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

1. After the update is complete, find the current Kubernetes version for your cluster\.

   ```
   kubectl version --short
   Client Version: v1.13.4
   Server Version: v1.12.6-eks-d69f1b
   ```

1. Patch the `kube-proxy` daemonset to use the image that corresponds to your current cluster Kubernetes version \(in this example, `1.12.6`\)\.

   ```
   kubectl patch daemonset kube-proxy \
   -n kube-system \
   -p '{"spec": {"template": {"spec": {"containers": [{"image": "602401143452.dkr.ecr.us-west-2.amazonaws.com/eks/kube-proxy:v1.12.6","name":"kube-proxy"}]}}}}'
   ```

1. Check your cluster's DNS provider\. Clusters that were created with Kubernetes version 1\.10 shipped with `kube-dns` as the default DNS and service discovery provider\. If you have updated a 1\.10 cluster to a newer version and you want to use CoreDNS for DNS and service discovery, you must install CoreDNS and remove `kube-dns`\.

   To check if your cluster is already running CoreDNS, use the following command\.

   ```
   kubectl get pod -n kube-system -l k8s-app=kube-dns
   ```

   If the output shows `coredns` in the pod names, you're already running CoreDNS in your cluster\. If not, see [Installing CoreDNS](coredns.md) to install CoreDNS on your cluster and then return here\.

1. Check the current version of your cluster's `coredns` deployment\.

   ```
   kubectl describe deployment coredns --namespace kube-system | grep Image | cut -d "/" -f 3
   coredns:v1.1.3
   ```

   The recommended `coredns` versions for their corresponding Kubernetes versions are as follows:
   + **Kubernetes 1\.12:** `1.2.2`
   + **Kubernetes 1\.11:** `1.1.3`

   If your current `coredns` version doesn't match the recommendation for your cluster version, update the `coredns` deployment to use the recommended image\.

   ```
   kubectl set image --namespace kube-system deployment.apps/coredns \
   coredns=602401143452.dkr.ecr.us-west-2.amazonaws.com/eks/coredns:v1.2.2
   ```

1. Check the version of your cluster's Amazon VPC CNI Plugin for Kubernetes\. Use the following command to print your cluster's CNI version\.

   ```
   kubectl describe daemonset aws-node --namespace kube-system | grep Image | cut -d "/" -f 2
   ```

   Output:

   ```
   amazon-k8s-cni:1.4.0
   ```

   If your CNI version is earlier than 1\.4\.0, use the following command to upgrade your CNI version to the latest version\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.4/config/v1.4/aws-k8s-cni.yaml
   ```

1. After your cluster update is complete, update your worker nodes to the same Kubernetes version of your updated cluster\. For more information, see [Worker Node Updates](update-workers.md)\.