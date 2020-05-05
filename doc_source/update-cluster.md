# Updating an Amazon EKS cluster Kubernetes version<a name="update-cluster"></a>

When a new Kubernetes version is available in Amazon EKS, you can update your cluster to the latest version\. 

**Important**  
We recommend that before updating to a new Kubernetes version that you review the information in [Amazon EKS Kubernetes versions](kubernetes-versions.md) and in the update steps in this topic\.

New Kubernetes versions introduce significant changes, so we recommend that you test the behavior of your applications against a new Kubernetes version before performing the update on your production clusters\. You can achieve this by building a continuous integration workflow to test your application behavior end\-to\-end before moving to a new Kubernetes version\.

The update process consists of Amazon EKS launching new API server nodes with the updated Kubernetes version to replace the existing ones\. Amazon EKS performs standard infrastructure and readiness health checks for network traffic on these new nodes to verify that they are working as expected\. If any of these checks fail, Amazon EKS reverts the infrastructure deployment, and your cluster remains on the prior Kubernetes version\. Running applications are not affected, and your cluster is never left in a non\-deterministic or unrecoverable state\. Amazon EKS regularly backs up all managed clusters, and mechanisms exist to recover clusters if necessary\. We are constantly evaluating and improving our Kubernetes infrastructure management processes\.

In order to upgrade the cluster, Amazon EKS requires 2\-3 free IP addresses from the subnets which were provided when you created the cluster\. If these subnets do not have available IP addresses, then the upgrade can fail\. Additionally, if any of the subnets or security groups that were provided during cluster creation have been deleted, the cluster upgrade process can fail\.

**Note**  
Although Amazon EKS runs a highly available control plane, you might experience minor service interruptions during an update\. For example, if you attempt to connect to an API server just before or just after it's terminated and replaced by a new API server running the new version of Kubernetes, you might experience API call errors or connectivity issues\. If this happens, retry your API operations until they succeed\.

Amazon EKS does not modify any of your Kubernetes add\-ons when you update a cluster\. After updating your cluster, we recommend that you update your add\-ons to the versions listed in the following table for the new Kubernetes version that you're updating to\. Steps to accomplish this are included in the update procedures\.


| Kubernetes version | 1\.16 | 1\.15 | 1\.14 | 1\.13 | 1\.12 | 
| --- | --- | --- | --- | --- | --- | 
| Amazon VPC CNI plug\-in | 1\.6\.1 | 1\.6\.1 | 1\.6\.1 | 1\.6\.1 | 1\.6\.1 | 
| DNS \(CoreDNS\) | 1\.6\.6 | 1\.6\.6 | 1\.6\.6 | 1\.6\.6 | 1\.6\.6 | 
| KubeProxy | 1\.16\.8 | 1\.15\.11 | 1\.14\.9 | 1\.13\.12 | 1\.12\.10 | 

If you're using additional add\-ons for your cluster that aren't listed in the previous table, update them to the latest compatible versions after updating your cluster\.

## Update an existing cluster<a name="update-existing-cluster"></a>

Update the cluster and Kubnernete add\-ons\.

**To update an existing cluster**

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

   We recommend that you update your worker nodes to your cluster's current pre\-update Kubernetes minor version prior to your cluster update\. Your worker nodes must not run a newer Kubernetes version than your control plane\. For example, if your control plane is running version 1\.15 and your workers are running version 1\.13, update your worker nodes to version 1\.14 or 1\.15 \(recommended\) before you update your cluster’s Kubernetes version to 1\.16\. For more information, see [Self\-managed worker node updates](update-workers.md)\.

1. The pod security policy admission controller is enabled on Amazon EKS clusters running Kubernetes version 1\.13 or later\. If you are upgrading your cluster to Kubernetes version 1\.13 or later, ensure that the proper pod security policies are in place before you update to avoid any issues\. You can check for the default policy with the following command:

   ```
   kubectl get psp eks.privileged
   ```

   If you receive the following error, see [To install or restore the default pod security policy](pod-security-policy.md#install-default-psp) before proceeding\.

   ```
   Error from server (NotFound): podsecuritypolicies.extensions "eks.privileged" not found
   ```

1. Update your cluster\. For instructions, select the tab with the name of the tool that you want to use to update your cluster\.

------
#### [ eksctl ]

   This procedure assumes that you have installed `eksctl`, and that your `eksctl` version is at least `0.19.0-rc.0`\. You can check your version with the following command:

   ```
   eksctl version
   ```

   For more information on installing or upgrading `eksctl`, see [Installing or upgrading `eksctl`](eksctl.md#installing-eksctl)\.

**Note**  
This procedure only works for clusters that were created with `eksctl`\.

   Update your Amazon EKS cluster Kubernetes version to the latest version with the following command, replacing *dev* with your cluster name\.

**Important**  
You may need to update some of your deployed resources before you can update to 1\.16\. For more information, see [Kubernetes 1\.16 upgrade prerequisites](#1-16-prequisites)\. 

   ```
   eksctl update cluster --name dev --approve
   ```

   This process takes several minutes to complete\.

------
#### [ AWS Management Console ]

   1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

   1. Choose the name of the cluster to update and choose **Update cluster version**\.

   1. For **Kubernetes version**, select the version to update your cluster to and choose **Update**\.
**Important**  
You may need to update some of your deployed resources before you can update to 1\.16\. For more information, see [Kubernetes 1\.16 upgrade prerequisites](#1-16-prequisites)\. 
**Important**  
Kubernetes version 1\.13 is now deprecated on Amazon EKS\. On **June 30th, 2020**, Kubernetes version 1\.13 will no longer be supported on Amazon EKS\. On or after this date, you will no longer be able to create new 1\.13 clusters, and all existing Amazon EKS clusters running Kubernetes version 1\.13 will eventually be automatically updated to version 1\.14\. We recommend that you update any 1\.13 clusters to version 1\.14 or later in order to avoid service interruption\. For more information, see [Amazon EKS version deprecation](kubernetes-versions.md#version-deprecation)\.  
Kubernetes version 1\.12 is now deprecated on Amazon EKS\. On **May 11th, 2020**, Kubernetes version 1\.12 will no longer be supported on Amazon EKS\. On or after this date, you will no longer be able to create new 1\.12 clusters, and all existing Amazon EKS clusters running Kubernetes version 1\.12 will eventually be automatically updated to version 1\.13\. We recommend that you update any 1\.12 clusters to version 1\.13 or later in order to avoid service interruption\. For more information, see [Amazon EKS version deprecation](kubernetes-versions.md#version-deprecation)\.  
Kubernetes API versions available through Amazon EKS are officially supported by AWS, until we remove the ability to create clusters using that version\. This is true even if upstream Kubernetes is no longer supporting a version available on Amazon EKS\. We backport security fixes that are applicable to the Kubernetes versions supported on Amazon EKS\. Existing clusters are always supported, and Amazon EKS will automatically update your cluster to a supported version if you have not done so manually by the version end of life date\.
**Important**  
Because Amazon EKS runs a highly available control plane, you must update only one minor version at a time\. See [Kubernetes Version and Version Skew Support Policy](https://kubernetes.io/docs/setup/version-skew-policy/#kube-apiserver) for the rationale behind this requirement\. Therefore, if your current version is 1\.14 and you want to upgrade to 1\.16, you must first upgrade your cluster to 1\.15 and then upgrade it from 1\.15 to 1\.16\. If you try to update directly from 1\.14 to 1\.16, the update version command throws an error\.

   1. For **Cluster name**, type the name of your cluster and choose **Confirm**\.
**Note**  
The cluster update should finish in a few minutes\.

------
#### [ AWS CLI ]

   1. Update your cluster with the following AWS CLI command\. Substitute your cluster name and desired Kubernetes minor version\.
**Important**  
You may need to update some of your deployed resources before you can update to 1\.16\. For more information, see [Kubernetes 1\.16 upgrade prerequisites](#1-16-prequisites)\. 
**Important**  
Kubernetes version 1\.13 is now deprecated on Amazon EKS\. On **June 30th, 2020**, Kubernetes version 1\.13 will no longer be supported on Amazon EKS\. On or after this date, you will no longer be able to create new 1\.13 clusters, and all existing Amazon EKS clusters running Kubernetes version 1\.13 will eventually be automatically updated to version 1\.14\. We recommend that you update any 1\.13 clusters to version 1\.14 or later in order to avoid service interruption\. For more information, see [Amazon EKS version deprecation](kubernetes-versions.md#version-deprecation)\.  
Kubernetes version 1\.12 is now deprecated on Amazon EKS\. On **May 11th, 2020**, Kubernetes version 1\.12 will no longer be supported on Amazon EKS\. On or after this date, you will no longer be able to create new 1\.12 clusters, and all existing Amazon EKS clusters running Kubernetes version 1\.12 will eventually be automatically updated to version 1\.13\. We recommend that you update any 1\.12 clusters to version 1\.13 or later in order to avoid service interruption\. For more information, see [Amazon EKS version deprecation](kubernetes-versions.md#version-deprecation)\.  
Kubernetes API versions available through Amazon EKS are officially supported by AWS, until we remove the ability to create clusters using that version\. This is true even if upstream Kubernetes is no longer supporting a version available on Amazon EKS\. We backport security fixes that are applicable to the Kubernetes versions supported on Amazon EKS\. Existing clusters are always supported, and Amazon EKS will automatically update your cluster to a supported version if you have not done so manually by the version end of life date\.
**Important**  
Because Amazon EKS runs a highly available control plane, you must update only one minor version at a time\. See [Kubernetes Version and Version Skew Support Policy](https://kubernetes.io/docs/setup/version-skew-policy/#kube-apiserver) for the rationale behind this requirement\. Therefore, if your current version is 1\.14 and you want to upgrade to 1\.16, you must first upgrade your cluster to 1\.15 and then upgrade it from 1\.15 to 1\.16\. If you try to update directly from 1\.14 to 1\.16, the update version command throws an error\.

      ```
      aws eks --region region-code update-cluster-version --name prod --kubernetes-version 1.16
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
                      "value": "1.16"
                  },
                  {
                      "type": "PlatformVersion",
                      "value": "eks.1"
                  }
              ],
              "createdAt": 1577485455.5,
              "errors": []
          }
      }
      ```

   1. Monitor the status of your cluster update with the following command, using the cluster name and update ID that the previous command returned\. Your update is complete when the status appears as `Successful`\.
**Note**  
The cluster update should finish in a few minutes\.

      ```
      aws eks --region region-code describe-update --name prod --update-id b5f0ba18-9a87-4450-b5a0-825e6e84496f
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
                      "value": "1.16"
                  },
                  {
                      "type": "PlatformVersion",
                      "value": "eks.1"
                  }
              ],
              "createdAt": 1577485455.5,
              "errors": []
          }
      }
      ```

------

1. Patch the `kube-proxy` daemonset to use the image that corresponds to your cluster's Region and current Kubernetes version \(in this example, `1.16.8`\)\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html)

   ```
   kubectl set image daemonset.apps/kube-proxy \
       -n kube-system \
       kube-proxy=602401143452.dkr.ecr.us-west-2.amazonaws.com/eks/kube-proxy:v1.16.8
   ```

1. Check your cluster's DNS provider\. Clusters that were created with Kubernetes version 1\.10 shipped with `kube-dns` as the default DNS and service discovery provider\. If you have updated a 1\.10 cluster to a newer version and you want to use CoreDNS for DNS and service discovery, then you must install CoreDNS and remove `kube-dns`\.

   To check if your cluster is already running CoreDNS, use the following command\.

   ```
   kubectl get pod -n kube-system -l k8s-app=kube-dns
   ```

   If the output shows `coredns` in the pod names, you're already running CoreDNS in your cluster\. If not, see [Installing or upgrading CoreDNS](coredns.md) to install CoreDNS on your cluster, update it to the recommended version, return here, and skip steps 6\-8\.

1. Check the current version of your cluster's `coredns` deployment\.

   ```
   kubectl describe deployment coredns --namespace kube-system | grep Image | cut -d "/" -f 3
   ```

   Output:

   ```
   coredns:v1.1.3
   ```

   The recommended `coredns` versions for the corresponding Kubernetes versions are as follows:    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html)

1. If your current `coredns` version is 1\.5\.0 or later, but earlier than the recommended version, then skip this step\. If your current version is earlier than 1\.5\.0, then you need to modify the config map for `coredns` to use the `forward` plug\-in, rather than the `proxy` plug\-in\.

   1. Open the configmap with the following command\.

      ```
      kubectl edit configmap coredns -n kube-system
      ```

   1. Replace *`proxy`* in the following line with `forward`\. Save the file and exit the editor\.

      ```
      proxy . /etc/resolv.conf
      ```

1. Update `coredns` to the recommended version, replacing *region\-code* with your Region and *1\.6\.6* with your cluster's recommended `coredns` version:

   ```
   kubectl set image --namespace kube-system deployment.apps/coredns \
               coredns=602401143452.dkr.ecr.us-west-2.amazonaws.com/eks/coredns:v1.6.6
   ```

1. Check the version of your cluster's Amazon VPC CNI Plugin for Kubernetes\. Use the following command to print your cluster's CNI version\.

   ```
   kubectl describe daemonset aws-node --namespace kube-system | grep Image | cut -d "/" -f 2
   ```

   Output:

   ```
   amazon-k8s-cni:1.5.7
   ```

   If your CNI version is earlier than 1\.6\.1, then use the following command to update your CNI version to the latest recommended version:

   ```
   kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.6/config/v1.6/aws-k8s-cni.yaml
   ```

1. \(Optional\) If you deployed the Kubernetes Cluster Autoscaler to your cluster prior to upgrading the cluster, update the Cluster Autoscaler to the latest version that matches the Kubernetes major and minor version that you upgraded to\.

   1. Open the Cluster Autoscaler [releases](https://github.com/kubernetes/autoscaler/releases) page in a web browser and find the latest Cluster Autoscaler version that matches your cluster's Kubernetes major and minor version\. For example, if your cluster's Kubernetes version is 1\.16 find the latest Cluster Autoscaler release that begins with 1\.16\. Record the semantic version number \(1\.16\.*`n`*\) for that release to use in the next step\.

   1. Set the Cluster Autoscaler image tag to the version that you recorded in the previous step with the following command\. Replace *1\.16\.n* with your own value\. You can replace `us` with `asia` or `eu`\.

      ```
      kubectl -n kube-system set image deployment.apps/cluster-autoscaler cluster-autoscaler=us.gcr.io/k8s-artifacts-prod/autoscaling/cluster-autoscaler:v1.16.n
      ```
**Note**  
Depending on the version that you need, you may need to change the previous address to `gcr.io/google-containers/cluster-autoscaler:v1.n.n` \. The image address is listed on the [releases](https://github.com/kubernetes/autoscaler/releases) page\.

1. \(Clusters with GPU workers only\) If your cluster has worker node groups with GPU support \(for example, `p3.2xlarge`\), you must update the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) DaemonSet on your cluster with the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/1.0.0-beta/nvidia-device-plugin.yml
   ```

1. After your cluster update is complete, update your worker nodes to the same Kubernetes version of your updated cluster\. For more information, see [Self\-managed worker node updates](update-workers.md)\. Any new pods launched on Fargate will have a `kubelet` version that matches your cluster version\. Existing Fargate pods will not be changed\.

## Kubernetes 1\.16 upgrade prerequisites<a name="1-16-prequisites"></a>

As noted in the [Kubernetes 1\.15 changelog](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.15.md#deprecations-and-removals), and [Deprecated APIs Removed In 1\.16: Here’s What You Need To Know](https://kubernetes.io/blog/2019/07/18/api-deprecations-in-1-16/) documents, if you have an existing cluster, API changes are required for the following deployed resources before upgrading a cluster to 1\.16\.

**Warning**  
If you do not change these APIs before upgrading to 1\.16, workloads will fail after the upgrade is complete\.
+ NetworkPolicy resources will no longer be served from `extensions/v1beta1` in v1\.16\. Migrate use to the `networking.k8s.io/v1` API, available since v1\.8\. Existing persisted data can be retrieved through the `networking.k8s.io/v1` API\.
+ PodSecurityPolicy resources will no longer be served from `extensions/v1beta1` in v1\.16\. Migrate to the `policy/v1beta1` API, available since v1\.10\. Existing persisted data can be retrieved through the `policy/v1beta1` API\.
+ DaemonSet, Deployment, StatefulSet, and ReplicaSet resources will no longer be served from `extensions/v1beta1`, `apps/v1beta1`, or `apps/v1beta2` in v1\.16\. Migrate to the `apps/v1` API, available since v1\.9\. Existing persisted data can be retrieved through the `apps/v1` API\. For example, to convert a Deployment that currently uses `apps/v1beta1`, enter the following command\.

  ```
  kubectl convert -f ./my-deployment.yaml --output-version apps/v1
  ```
**Note**  
The previous command may use different default values from what is set in your current manifest file\. To learn more about a specific resource, see the Kubernetes [API reference](https://kubernetes.io/docs/reference/#api-reference)\.<a name="1-16-do-now"></a>

**What you need to do before upgrading to 1\.16**
+ Change your YAML files to reference the new APIs\.
+ Update custom integrations and controllers to call the new APIs\.
+ Ensure that you use an updated version of any third party tools, such as ingress controllers, continuous delivery systems, and others, that call the new APIs\.

To easily check for deprecated API usage in your cluster, make sure that the `audit` [control plane log](control-plane-logs.md) is enabled, and specify `v1beta` as a filter for the events\. All of the replacement APIs are in Kubernetes versions later than 1\.10\. Applications on any supported version of Amazon EKS can begin using the updated APIs now\.