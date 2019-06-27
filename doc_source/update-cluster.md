# Updating an Amazon EKS Cluster Kubernetes Version<a name="update-cluster"></a>

When a new Kubernetes version is available in Amazon EKS, you can update your cluster to the latest version\. New Kubernetes versions introduce significant changes, so we recommend that you test the behavior of your applications against a new Kubernetes version before performing the update on your production clusters\. You can achieve this by building a continuous integration workflow to test your application behavior end\-to\-end before moving to a new Kubernetes version\.

The update process consists of Amazon EKS launching new API server nodes with the updated Kubernetes version to replace the existing ones\. Amazon EKS performs standard infrastructure and readiness health checks for network traffic on these new nodes to verify that they are working as expected\. If any of these checks fail, Amazon EKS reverts the infrastructure deployment, and your cluster remains on the prior Kubernetes version\. Running applications are not affected, and your cluster is never left in a non\-deterministic or unrecoverable state\. Amazon EKS regularly backs up all managed clusters, and mechanisms exist to recover clusters if necessary\. We are constantly evaluating and improving our Kubernetes infrastructure management processes\.

In order to upgrade the cluster, Amazon EKS requires 2\-3 free IP addresses from the subnets which were provided when you created the cluster\. If these subnets do not have available IP addresses, then the upgrade can fail\. Additionally, if any of the subnets or security groups that were provided during cluster creation have been deleted, the cluster upgrade process can fail\.

**Note**  
Although Amazon EKS runs a highly available control plane, you might experience minor service interruptions during an update\. For example, if you attempt to connect to an API server just before or just after it's terminated and replaced by a new API server running the new version of Kubernetes, you might experience API call errors or connectivity issues\. If this happens, retry your API operations until they succeed\.

Amazon EKS does not modify any of your Kubernetes add\-ons when you update a cluster\. After updating your cluster, we recommend that you update your add\-ons to the versions listed in the following table for the new Kubernetes version that you're updating to \(steps to accomplish this are included in the update procedures\)\.


| Kubernetes Version | 1\.10 | 1\.11 | 1\.12 | 1\.13 | 
| --- | --- | --- | --- | --- | 
| Amazon VPC CNI plug\-in | We recommend the latest available CNI version \(1\.5\.0\) | 
| DNS | kube\-dns 1\.14\.10 | CoreDNS 1\.1\.3 | CoreDNS 1\.2\.2 | CoreDNS 1\.2\.6 | 
| KubeProxy | 1\.10\.13 | 1\.11\.8 | 1\.12\.6 | 1\.13\.7 | 

**Important**  
Amazon EKS will deprecate Kubernetes version 1\.10 on July 22, 2019\. On this day, you will no longer be able to create new 1\.10 clusters, and all Amazon EKS clusters running Kubernetes version 1\.10 will be updated to the latest available platform version of Kubernetes version 1\.11\. For more information, see [Amazon EKS Version Deprecation](kubernetes-versions.md#version-deprecation)\.

If you're using additional add\-ons for your cluster that aren't listed in the previous table, update them to the latest compatible versions after updating your cluster\.

Choose the tab below that corresponds to your desired cluster update method:

------
#### [ eksctl ]

**To update an existing cluster with `eksctl`**

This procedure assumes that you have installed `eksctl`, and that your `eksctl` version is at least `0.1.37`\. You can check your version with the following command:

```
eksctl version
```

 For more information on installing or upgrading `eksctl`, see [Installing or Upgrading `eksctl`](eksctl.md#installing-eksctl)\.
**Note**  
This procedure only works for clusters that were created with `eksctl`\.

1. Compare the Kubernetes version of your cluster control plane to the Kubernetes version of your worker nodes\.
   + Get the Kubernetes version of your cluster control plane with the following command\.

     ```
     kubectl version --short
     ```
   + Get the Kubernetes version of your worker nodes with the following command\.

     ```
     kubectl get nodes
     ```

   If your worker nodes are more than one Kubernetes minor version older than your control plane, then you must upgrade your worker nodes to a newer Kubernetes minor version before you update your cluster's Kubernetes version\. For more information, see [Kubernetes version and version skew support policy](https://kubernetes.io/docs/setup/release/version-skew-policy/) in the Kubernetes documentation\.

   We recommend that you update your worker nodes to your cluster's current pre\-update Kubernetes minor version prior to your cluster update\. Your worker nodes must not run a newer Kubernetes version than your control plane\. For example, if your control plane is running version 1\.12 and your workers are running version 1\.10, update your worker nodes to version 1\.11 or 1\.12 \(recommended\) before you update your cluster’s Kubernetes version to 1\.13\. For more information, see [Worker Node Updates](update-workers.md)\.

1. Update your Amazon EKS cluster Kubernetes version with the following command, replacing the red text with your cluster name:

   ```
   eksctl update cluster --name dev --approve
   ```

   This process takes several minutes to complete\.

1. Patch the `kube-proxy` daemonset for your updated Kubernetes version with the following command, replacing the red text with your cluster name:

   ```
   eksctl utils update-kube-proxy --name dev --approve
   ```

1. Check your cluster's DNS provider\. Clusters that were created with Kubernetes version 1\.10 shipped with `kube-dns` as the default DNS and service discovery provider\. If you have updated a 1\.10 cluster to a newer version and you want to use CoreDNS for DNS and service discovery, you must install CoreDNS and remove `kube-dns`\.

   To check if your cluster is already running CoreDNS, use the following command\.

   ```
   kubectl get pod -n kube-system -l k8s-app=kube-dns
   ```

   If the output shows `coredns` in the pod names, you're already running CoreDNS in your cluster\. If not, run the following command to install `coredns`, replacing the red text with your cluster name:

   ```
   eksctl utils install-coredns --name dev --approve
   ```

1. Check the current version of your cluster's `coredns` deployment\.

   ```
   kubectl describe deployment coredns --namespace kube-system | grep Image | cut -d "/" -f 3
   ```

   The recommended `coredns` versions for their corresponding Kubernetes versions are as follows:
   + **Kubernetes 1\.13:** `1.2.6`
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
   amazon-k8s-cni:1.3.3
   ```

   If your CNI version is earlier than 1\.5\.0, use the following command to upgrade your CNI version to the latest version:
   + For Kubernetes 1\.10 clusters:

     ```
     kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.5/config/v1.5/aws-k8s-cni-1.10.yaml
     ```
   + For all other Kubernetes versions:

     ```
     kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.5/config/v1.5/aws-k8s-cni.yaml
     ```

1. \(Clusters with GPU workers only\) If your cluster has worker node groups with GPU support \(for example, `p3.2xlarge`\), you must update the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) daemon set on your cluster with the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/1.0.0-beta/nvidia-device-plugin.yml
   ```

1. After your cluster update is complete, update your worker nodes to the same Kubernetes version of your updated cluster\. For more information, see [Worker Node Updates](update-workers.md)\.

------
#### [ AWS Management Console ]

**To update an existing cluster with the console**

1. Compare the Kubernetes version of your cluster control plane to the Kubernetes version of your worker nodes\.
   + Get the Kubernetes version of your cluster control plane with the following command\.

     ```
     kubectl version --short
     ```
   + Get the Kubernetes version of your worker nodes with the following command\.

     ```
     kubectl get nodes
     ```

   If your worker nodes are more than one Kubernetes minor version older than your control plane, then you must upgrade your worker nodes to a newer Kubernetes minor version before you update your cluster's Kubernetes version\. For more information, see [Kubernetes version and version skew support policy](https://kubernetes.io/docs/setup/release/version-skew-policy/) in the Kubernetes documentation\.

   We recommend that you update your worker nodes to your cluster's current pre\-update Kubernetes minor version prior to your cluster update\. Your worker nodes must not run a newer Kubernetes version than your control plane\. For example, if your control plane is running version 1\.12 and your workers are running version 1\.10, update your worker nodes to version 1\.11 or 1\.12 \(recommended\) before you update your cluster’s Kubernetes version to 1\.13\. For more information, see [Worker Node Updates](update-workers.md)\.

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the name of the cluster to update and choose **Update cluster version**\.

1. For **Kubernetes version**, select the version to update your cluster to and choose **Update**\.
**Important**  
Amazon EKS will deprecate Kubernetes version 1\.10 on July 22, 2019\. On this day, you will no longer be able to create new 1\.10 clusters, and all Amazon EKS clusters running Kubernetes version 1\.10 will be updated to the latest available platform version of Kubernetes version 1\.11\. For more information, see [Amazon EKS Version Deprecation](kubernetes-versions.md#version-deprecation)\.
**Important**  
Because Amazon EKS runs a highly available control plane, you must update only one minor version at a time\. See [Kubernetes Version and Version Skew Support Policy](https://kubernetes.io/docs/setup/version-skew-policy/#kube-apiserver) for the rationale behind this requirement\. Therefore, if your current version is 1\.11 and you want to upgrade to 1\.13, you must first upgrade your cluster to 1\.12 and then upgrade it from 1\.12 to 1\.13\. If you try to update directly from 1\.11 to 1\.13, the update version command throws an error\.

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
   ```

   The recommended `coredns` versions for their corresponding Kubernetes versions are as follows:
   + **Kubernetes 1\.13:** `1.2.6`
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
   amazon-k8s-cni:1.3.3
   ```

   If your CNI version is earlier than 1\.5\.0, use the following command to upgrade your CNI version to the latest version\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/master/config/v1.5/aws-k8s-cni.yaml
   ```

1. \(Clusters with GPU workers only\) If your cluster has worker node groups with GPU support \(for example, `p3.2xlarge`\), you must update the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) daemon set on your cluster with the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/1.0.0-beta/nvidia-device-plugin.yml
   ```

1. After your cluster update is complete, update your worker nodes to the same Kubernetes version of your updated cluster\. For more information, see [Worker Node Updates](update-workers.md)\.

------
#### [ AWS CLI ]

**To update an existing cluster with the AWS CLI**

1. Compare the Kubernetes version of your cluster control plane to the Kubernetes version of your worker nodes\.
   + Get the Kubernetes version of your cluster control plane with the following command\.

     ```
     kubectl version --short
     ```
   + Get the Kubernetes version of your worker nodes with the following command\.

     ```
     kubectl get nodes
     ```

   If your worker nodes are more than one Kubernetes minor version older than your control plane, then you must upgrade your worker nodes to a newer Kubernetes minor version before you update your cluster's Kubernetes version\. For more information, see [Kubernetes version and version skew support policy](https://kubernetes.io/docs/setup/release/version-skew-policy/) in the Kubernetes documentation\.

   We recommend that you update your worker nodes to your cluster's current pre\-update Kubernetes minor version prior to your cluster update\. Your worker nodes must not run a newer Kubernetes version than your control plane\. For example, if your control plane is running version 1\.12 and your workers are running version 1\.10, update your worker nodes to version 1\.11 or 1\.12 \(recommended\) before you update your cluster’s Kubernetes version to 1\.13\. For more information, see [Worker Node Updates](update-workers.md)\.

1. Update your cluster with the following AWS CLI command\. Substitute your cluster name and desired Kubernetes minor version\.
**Important**  
Amazon EKS will deprecate Kubernetes version 1\.10 on July 22, 2019\. On this day, you will no longer be able to create new 1\.10 clusters, and all Amazon EKS clusters running Kubernetes version 1\.10 will be updated to the latest available platform version of Kubernetes version 1\.11\. For more information, see [Amazon EKS Version Deprecation](kubernetes-versions.md#version-deprecation)\.
**Important**  
Because Amazon EKS runs a highly available control plane, you must update only one minor version at a time\. See [Kubernetes Version and Version Skew Support Policy](https://kubernetes.io/docs/setup/version-skew-policy/#kube-apiserver) for the rationale behind this requirement\. Therefore, if your current version is 1\.11 and you want to upgrade to 1\.13, you must first upgrade your cluster to 1\.12 and then upgrade it from 1\.12 to 1\.13\. If you try to update directly from 1\.11 to 1\.13, the update version command throws an error\.

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
   ```

   The recommended `coredns` versions for their corresponding Kubernetes versions are as follows:
   + **Kubernetes 1\.13:** `1.2.6`
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
   amazon-k8s-cni:1.3.3
   ```

   If your CNI version is earlier than 1\.5\.0, use the following command to upgrade your CNI version to the latest version\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/master/config/v1.5/aws-k8s-cni.yaml
   ```

1. \(Clusters with GPU workers only\) If your cluster has worker node groups with GPU support \(for example, `p3.2xlarge`\), you must update the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) daemon set on your cluster with the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/1.0.0-beta/nvidia-device-plugin.yml
   ```

1. After your cluster update is complete, update your worker nodes to the same Kubernetes version of your updated cluster\. For more information, see [Worker Node Updates](update-workers.md)\.

------