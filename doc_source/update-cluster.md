# Updating an Amazon EKS cluster Kubernetes version<a name="update-cluster"></a>

When a new Kubernetes version is available in Amazon EKS, you can update your Amazon EKS cluster to the latest version\. 

**Important**  
We recommend that, before you update to a new Kubernetes version, you review the information in [Amazon EKS Kubernetes versions](kubernetes-versions.md) and also review in the update steps in this topic\. If you're updating to version `1.22`, you must make the changes listed in [Kubernetes version `1.22` prerequisites](#update-1.22) to your cluster before updating it\.

New Kubernetes versions sometimes introduce significant changes\. Therefore, we recommend that you test the behavior of your applications against a new Kubernetes version before you update your production clusters\. You can do this by building a continuous integration workflow to test your application behavior before moving to a new Kubernetes version\.

The update process consists of Amazon EKS launching new API server nodes with the updated Kubernetes version to replace the existing ones\. Amazon EKS performs standard infrastructure and readiness health checks for network traffic on these new nodes to verify that they're working as expected\. If any of these checks fail, Amazon EKS reverts the infrastructure deployment, and your cluster remains on the prior Kubernetes version\. Running applications aren't affected, and your cluster is never left in a non\-deterministic or unrecoverable state\. Amazon EKS regularly backs up all managed clusters, and mechanisms exist to recover clusters if necessary\. We're constantly evaluating and improving our Kubernetes infrastructure management processes\.

To update the cluster, Amazon EKS requires up to five free IP addresses from the subnets that you specified when you created your cluster\. Amazon EKS creates new cluster elastic network interfaces \(network interfaces\) in any of the subnets that you specified\. The network interfaces may be created in different subnets than your existing network interfaces are in, so make sure that your security group rules allow [required cluster communication](sec-group-reqs.md) for any of the subnets that you specified when you created your cluster\. If any of the subnets that you specified when you created the cluster don't exist, don't have enough free IP addresses, or don't have security group rules that allows necessary cluster communication, then the update can fail\.

**Note**  
Even though Amazon EKS runs a highly available control plane, you might experience minor service interruptions during an update\. For example, assume that you attempt to connect to an API server around when it's terminated and replaced by a new API server that's running the new version of Kubernetes\. You might experience API call errors or connectivity issues\. If this happens, retry your API operations until they succeed\.

## Update the Kubernetes version for your Amazon EKS cluster<a name="update-existing-cluster"></a>

**To update the Kubernetes version for your cluster**

1. Compare the Kubernetes version of your cluster control plane to the Kubernetes version of your nodes\.
   + Get the Kubernetes version of your cluster control plane\.

     ```
     kubectl version --short
     ```
   + Get the Kubernetes version of your nodes\. This command returns all self\-managed and managed Amazon EC2 and Fargate nodes\. Each Fargate pod is listed as its own node\.

     ```
     kubectl get nodes
     ```

   Before updating your control plane to a new Kubernetes version, make sure that the Kubernetes minor version of both the managed nodes and Fargate nodes in your cluster are the same as your control plane's version\. For example, if your control plane is running version `1.23` and one of your nodes is running version `1.22`, then you must update your nodes to version `1.23` before updating your control plane to 1\.24\. We also recommend that you update your self\-managed nodes to the same version as your control plane before updating the control plane\. For more information, see [Updating a managed node group](update-managed-node-group.md) and [Self\-managed node updates](update-workers.md)\. If you have Fargate nodes with a minor version lower than the control plane version, first delete the pod that's represented by the node\. Then update your control plane\. Any remaining pods will update to the new version after you redeploy them\.

1. By default, the pod security policy admission controller is enabled on Amazon EKS clusters\. Before updating your cluster, ensure that the proper pod security policies are in place\. This is to avoid potential security issues\. You can check for the default policy with the **kubectl get psp eks\.privileged** command\.

   ```
   kubectl get psp eks.privileged
   ```

   If you receive the following error, see [default pod security policy](pod-security-policy.md#default-psp) before proceeding\.

   ```
   Error from server (NotFound): podsecuritypolicies.extensions "eks.privileged" not found
   ```

1. If the Kubernetes version that you originally deployed your cluster with was Kubernetes `1.18` or later, skip this step\.

   You might need to remove a discontinued term from your CoreDNS manifest\.

   1. Check to see if your CoreDNS manifest has a line that only has the word `upstream`\.

      ```
      kubectl get configmap coredns -n kube-system -o jsonpath='{$.data.Corefile}' | grep upstream
      ```

      If no output is returned, this means that your manifest doesn't have the line\. If this is the case, skip to the next step\. If the word `upstream` is returned, remove the line\.

   1. Remove the line near the top of the file that only has the word `upstream` in the configmap file\. Don't change anything else in the file\. After the line is removed, save the changes\.

      ```
      kubectl edit configmap coredns -n kube-system -o yaml
      ```

1. Update your cluster using `eksctl`, the AWS Management Console, or the AWS CLI\.
**Important**  
If you're updating to version `1.22`, you must make the changes listed in [Kubernetes version `1.22` prerequisites](#update-1.22) to your cluster before updating it\.
If you're updating to version `1.23` and use Amazon EBS volumes in your cluster, then you must install the Amazon EBS CSI driver in your cluster before updating your cluster to version `1.23` to avoid workload disruptions\. For more information, see [Kubernetes 1\.23](kubernetes-versions.md#kubernetes-1.23) and [Amazon EBS CSI driver](ebs-csi.md)\.
Because Amazon EKS runs a highly available control plane, you can update only one minor version at a time\. For more information about this requirement, see [Kubernetes Version and Version Skew Support Policy](https://kubernetes.io/docs/setup/version-skew-policy/#kube-apiserver)\. Assume that your current cluster version is version `1.22` and you want to update it to version `1.24`\. You must first update your version `1.22` cluster to version `1.23` and then update your version `1.23` cluster to version `1.24`\.
Make sure that the `kubelet` on your managed and Fargate nodes are at the same Kubernetes version as your control plane before you update\. We recommend that your self\-managed nodes are at the same version as the control plane\. They can be only up to one version behind the current version of the control plane\.
If your cluster is configured with a version of the Amazon VPC CNI plugin that is earlier than `1.8.0`, then we recommend that you update the plugin to the latest version before updating your cluster to version `1.21` or later\. To update the self\-managed add\-on type, see [Updating the Amazon VPC CNI plugin for Kubernetes self\-managed add\-on](managing-vpc-cni.md)\. To update the Amazon EKS add\-on type, see [Updating an add\-on](managing-add-ons.md#updating-an-add-on)\.

------
#### [ eksctl ]

   This procedure requires `eksctl` version `0.129.0` or later\. You can check your version with the following command:

   ```
   eksctl version
   ```

   For instructions on how to install and update `eksctl`, see [Installing or updating `eksctl`](eksctl.md)\.

   Update the Kubernetes version of your Amazon EKS control plane\. Replace *`my-cluster`* with your cluster name\. Replace *1\.24* with the Amazon EKS supported version number that you want to update your cluster to\. For a list of supported version numbers, see [Amazon EKS Kubernetes versions](kubernetes-versions.md)\.

   ```
   eksctl upgrade cluster --name my-cluster --version 1.24 --approve
   ```

   The update takes several minutes to complete\.

------
#### [ AWS Management Console ]

   1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

   1. Choose the name of the Amazon EKS cluster to update and choose **Update cluster version**\.

   1. For **Kubernetes version**, select the version to update your cluster to and choose **Update**\.

   1. For **Cluster name**, enter the name of your cluster and choose **Confirm**\.

      The update takes several minutes to complete\.

------
#### [ AWS CLI ]

   1. Update your Amazon EKS cluster with the following AWS CLI command\. Replace the *`example values`* with your own\. Replace *1\.24* with the Amazon EKS supported version number that you want to update your cluster to\. For a list of supported version numbers, see [Amazon EKS Kubernetes versions](kubernetes-versions.md)\.

      ```
      aws eks update-cluster-version --region region-code --name my-cluster --kubernetes-version 1.24
      ```

      The example output is as follows\.

      ```
      {
          "update": {
              "id": "b5f0ba18-9a87-4450-b5a0-825e6e84496f",
              "status": "InProgress",
              "type": "VersionUpdate",
              "params": [
                  {
                      "type": "Version",
                      "value": "1.24"
                  },
                  {
                      "type": "PlatformVersion",
                      "value": "eks.1"
                  }
              ],
      ...
              "errors": []
          }
      }
      ```

   1. Monitor the status of your cluster update with the following command\. Use the cluster name and update ID that the previous command returned\. When a `Successful` status is displayed, the update is complete\. The update takes several minutes to complete\.

      ```
      aws eks describe-update --region region-code --name my-cluster --update-id b5f0ba18-9a87-4450-b5a0-825e6e84496f
      ```

      The example output is as follows\.

      ```
      {
          "update": {
              "id": "b5f0ba18-9a87-4450-b5a0-825e6e84496f",
              "status": "Successful",
              "type": "VersionUpdate",
              "params": [
                  {
                      "type": "Version",
                      "value": "1.24"
                  },
                  {
                      "type": "PlatformVersion",
                      "value": "eks.1"
                  }
              ],
      ...
              "errors": []
          }
      }
      ```

------

1. After your cluster update is complete, update your nodes to the same Kubernetes minor version as your updated cluster\. For more information, see [Self\-managed node updates](update-workers.md) and [Updating a managed node group](update-managed-node-group.md)\. Any new pods that are launched on Fargate have a `kubelet` version that matches your cluster version\. Existing Fargate pods aren't changed\.

1. \(Optional\) If you deployed the Kubernetes Cluster Autoscaler to your cluster before updating the cluster, update the Cluster Autoscaler to the latest version that matches the Kubernetes major and minor version that you updated to\.

   1. Open the Cluster Autoscaler [releases](https://github.com/kubernetes/autoscaler/releases) page in a web browser and find the latest Cluster Autoscaler version that matches your cluster's Kubernetes major and minor version\. For example, if your cluster's Kubernetes version is `1.24` find the latest Cluster Autoscaler release that begins with `1.24`\. Record the semantic version number \(`1.24.n`, for example\) for that release to use in the next step\.

   1. Set the Cluster Autoscaler image tag to the version that you recorded in the previous step with the following command\. If necessary, replace `1.24.n` with your own value\.

      ```
      kubectl -n kube-system set image deployment.apps/cluster-autoscaler cluster-autoscaler=k8s.gcr.io/autoscaling/cluster-autoscaler:v1.24.n
      ```

1. \(Clusters with GPU nodes only\) If your cluster has node groups with GPU support \(for example, `p3.2xlarge`\), you must update the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) DaemonSet on your cluster with the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.9.0/nvidia-device-plugin.yml
   ```

1. Update the Amazon VPC CNI plugin for Kubernetes, CoreDNS, and `kube-proxy` add\-ons\. If you updated your cluster to version `1.21` or later, than we recommend updating the add\-ons to the minimum versions listed in [Service account tokens](service-accounts.md#boundserviceaccounttoken-validated-add-on-versions)\.
   + If you are using Amazon EKS add\-ons, select **Clusters** in the Amazon EKS console, then select the name of the cluster that you updated in the left navigation pane\. Notifications appear in the console\. They inform you that a new version is available for each add\-on that has an available update\. To update an add\-on, select the **Add\-ons** tab\. In one of the boxes for an add\-on that has an update available, select **Update now**, select an available version, and then select **Update**\.
   + Alternately, you can use the AWS CLI or `eksctl` to update add\-ons\. For more information, see [Updating an add\-on](managing-add-ons.md#updating-an-add-on)\.

1. If necessary, update your version of `kubectl`\. You must use a `kubectl` version that is within one minor version difference of your Amazon EKS cluster control plane\. For example, a `1.23` `kubectl` client works with Kubernetes `1.22`, `1.23`, and `1.24` clusters\. You can check your currently installed version with the following command\.

   ```
   kubectl version --short --client
   ```

### Kubernetes version `1.22` prerequisites<a name="update-1.22"></a>

A number of deprecated beta APIs \(`v1beta1`\) have been removed in version `1.22` in favor of the GA \(`v1`\) version of those same APIs\. As noted in the Kubernetes version `1.22` [API and Feature removal blog](https://blog.k8s.io/2021/07/14/upcoming-changes-in-kubernetes-1-22) and deprecated [API migration guide](https://kubernetes.io/docs/reference/using-api/deprecation-guide/#v1-22), API changes are required for the following deployed resources before updating a cluster to version `1.22`\.

Before updating your cluster to Kubernetes version `1.22`, make sure to do the following:
+ Change your YAML manifest files and clients to reference the new APIs\.
+ Update custom integrations and controllers to call the new APIs\.
+ Make sure that you use an updated version of any third\-party tools\. These tools include ingress controllers, service mesh controllers, continuous delivery systems, and other tools that call the new APIs\. To check for discontinued API usage in your cluster, enable [audit control plane logging](control-plane-logs.md) and specify `v1beta` as an event filter\. Replacement APIs are available in Kubernetes for several versions\. 
+ If you currently have the AWS Load Balancer Controller deployed to your cluster, you must update it to version `2.4.1` before updating your cluster to Kubernetes version `1.22`\.

**Important**  
When you update clusters to version `1.22`, existing persisted objects can be accessed using the new APIs\. However, you must migrate manifests and update clients to use these new APIs\. Updating the clusters prevents potential workload failures\.

Kubernetes version `1.22` removes support from the following beta APIs\. Migrate your manifests and API clients based on the following information:


| Resource | Beta version | GA version | Notes | 
| --- | --- | --- | --- | 
| ValidatingWebhookConfiguration MutatingWebhookConfiguration | admissionregistration\.k8s\.io/v1beta1 | admissionregistration\.k8s\.io/v1 |  [\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html)  | 
| CustomResourceDefinition | apiextensions\.k8s\.io/v1beta1 | apiextensions\.k8s\.io/v1 |  [\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html)  | 
| APIService | apiregistration\.k8s\.io/v1beta1 | apiregistration\.k8s\.io/v1 | None | 
| TokenReview | authentication\.k8s\.io/v1beta1 | authentication\.k8s\.io/v1 | None | 
| SubjectAccessReview LocalSubjectAccessReview SelfSubjectAccessReview | authorization\.k8s\.io/v1beta1 | authorization\.k8s\.io/v1 | spec\.group is renamed to spec\.groups | 
| CertificateSigningRequest | certificates\.k8s\.io/v1beta1 | certificates\.k8s\.io/v1 |  [\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html)  | 
|  `Lease`  | coordination\.k8s\.io/v1beta1 | coordination\.k8s\.io/v1 | None | 
|  `Ingress`   |  [\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html)  | networking\.k8s\.io/v1 |  [\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html)  | 
|  `IngressClass`   | networking\.k8s\.io/v1beta1 | networking\.k8s\.io/v1 | None | 
|  `RBAC`  | rbac\.authorization\.k8s\.io/v1beta1 | rbac\.authorization\.k8s\.io/v1 | None | 
| PriorityClass | scheduling\.k8s\.io/v1beta1 | scheduling\.k8s\.io/v1 | None | 
| CSIDriver CSINode StorageClass VolumeAttachment | storage\.k8s\.io/v1beta1 | storage\.k8s\.io/v1 | None | 

To learn more about the API removal, see the [Deprecated API migration guide](https://kubernetes.io/docs/reference/using-api/deprecation-guide/#v1-22)\.