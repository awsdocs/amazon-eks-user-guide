# Updating an Amazon EKS cluster Kubernetes version<a name="update-cluster"></a>

When a new Kubernetes version is available in Amazon EKS, you can update your Amazon EKS cluster to the latest version\. 

**Important**  
Once you upgrade a cluster, you can't downgrade to a previous version\. We recommend that, before you update to a new Kubernetes version, you review the information in [Amazon EKS Kubernetes versions](kubernetes-versions.md) and also review in the update steps in this topic\.

New Kubernetes versions sometimes introduce significant changes\. Therefore, we recommend that you test the behavior of your applications against a new Kubernetes version before you update your production clusters\. You can do this by building a continuous integration workflow to test your application behavior before moving to a new Kubernetes version\.

The update process consists of Amazon EKS launching new API server nodes with the updated Kubernetes version to replace the existing ones\. Amazon EKS performs standard infrastructure and readiness health checks for network traffic on these new nodes to verify that they're working as expected\. However, once you've started the cluster upgrade, you can't pause or stop it\. If any of these checks fail, Amazon EKS reverts the infrastructure deployment, and your cluster remains on the prior Kubernetes version\. Running applications aren't affected, and your cluster is never left in a non\-deterministic or unrecoverable state\. Amazon EKS regularly backs up all managed clusters, and mechanisms exist to recover clusters if necessary\. We're constantly evaluating and improving our Kubernetes infrastructure management processes\.

To update the cluster, Amazon EKS requires up to five available IP addresses from the subnets that you specified when you created your cluster\. Amazon EKS creates new cluster elastic network interfaces \(network interfaces\) in any of the subnets that you specified\. The network interfaces may be created in different subnets than your existing network interfaces are in, so make sure that your security group rules allow [required cluster communication](sec-group-reqs.md) for any of the subnets that you specified when you created your cluster\. If any of the subnets that you specified when you created the cluster don't exist, don't have enough available IP addresses, or don't have security group rules that allows necessary cluster communication, then the update can fail\.

**Note**  
To ensure that the API server endpoint for your cluster is always accessible, Amazon EKS provides a highly available Kubernetes control plane and performs rolling updates of API server instances during update operations\. In order to account for changing IP addresses of API server instances supporting your Kubernetes API server endpoint, you must ensure that your API server clients manage reconnects effectively\. Recent versions of `kubectl` and the Kubernetes client [libraries](https://kubernetes.io/docs/tasks/administer-cluster/access-cluster-api/#programmatic-access-to-the-api) that are officially supported, perform this reconnect process transparently\.

## Update the Kubernetes version for your Amazon EKS cluster<a name="update-existing-cluster"></a>

**To update the Kubernetes version for your cluster**

1. Compare the Kubernetes version of your cluster control plane to the Kubernetes version of your nodes\.
   + Get the Kubernetes version of your cluster control plane\.

     ```
     kubectl version
     ```
   + Get the Kubernetes version of your nodes\. This command returns all self\-managed and managed Amazon EC2 and Fargate nodes\. Each Fargate Pod is listed as its own node\.

     ```
     kubectl get nodes
     ```

   Before updating your control plane to a new Kubernetes version, make sure that the Kubernetes minor version of both the managed nodes and Fargate nodes in your cluster are the same as your control plane's version\. For example, if your control plane is running version `1.28` and one of your nodes is running version `1.27`, then you must update your nodes to version `1.28` before updating your control plane to 1\.29\. We also recommend that you update your self\-managed nodes to the same version as your control plane before updating the control plane\. For more information, see [Updating a managed node group](update-managed-node-group.md) and [Self\-managed node updates](update-workers.md)\. If you have Fargate nodes with a minor version lower than the control plane version, first delete the Pod that's represented by the node\. Then update your control plane\. Any remaining Pods will update to the new version after you redeploy them\.

1. If the Kubernetes version that you originally deployed your cluster with was Kubernetes `1.25` or later, skip this step\.

   By default, the Pod security policy admission controller is enabled on Amazon EKS clusters\. Before updating your cluster, ensure that the proper Pod security policies are in place\. This is to avoid potential security issues\. You can check for the default policy with the **kubectl get psp eks\.privileged** command\.

   ```
   kubectl get psp eks.privileged
   ```

   If you receive the following error, see [Amazon EKS default Pod security policy](pod-security-policy.md#default-psp) before proceeding\.

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
If you're updating to version `1.23` and use Amazon EBS volumes in your cluster, then you must install the Amazon EBS CSI driver in your cluster before updating your cluster to version `1.23` to avoid workload disruptions\. For more information, see [Kubernetes 1\.23](kubernetes-versions-extended.md#kubernetes-1.23) and [Amazon EBS CSI driver](ebs-csi.md)\.
 Kubernetes `1.24` and later use `containerd` as the default container runtime\. If you're switching to the `containerd` runtime and already have Fluentd configured for Container Insights, then you must migrate Fluentd to Fluent Bit before updating your cluster\. The Fluentd parsers are configured to only parse log messages in JSON format\. Unlike `dockerd`, the `containerd` container runtime has log messages that aren't in JSON format\. If you don't migrate to Fluent Bit, some of the configured Fluentd's parsers will generate a massive amount of errors inside the Fluentd container\. For more information on migrating, see [Set up Fluent Bit as a DaemonSet to send logs to CloudWatch Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Container-Insights-setup-logs-FluentBit.html)\.
Because Amazon EKS runs a highly available control plane, you can update only one minor version at a time\. For more information about this requirement, see [Kubernetes Version and Version Skew Support Policy](https://kubernetes.io/docs/setup/version-skew-policy/#kube-apiserver)\. Assume that your current cluster version is version `1.27` and you want to update it to version `1.29`\. You must first update your version `1.27` cluster to version `1.28` and then update your version `1.28` cluster to version `1.29`\.
Review the version skew between the Kubernetes `kube-apiserver` and the `kubelet` on your nodes\.   
Starting from Kubernetes version `1.28`, `kubelet` may be up to three minor versions older than `kube-apiserver`\. See [Kubernetes upstream version skew policy](https://kubernetes.io/releases/version-skew-policy/#kubelet)\. 
If the `kubelet` on your managed and Fargate nodes is on Kubernetes version `1.25` or newer, you can update your cluster up to three versions ahead without updating the `kubelet` version\. For example, if the `kubelet` is on version `1.25`, you can update your Amazon EKS cluster version from `1.25` to `1.26`, to `1.27`, and to `1.28` while the `kubelet` remains on version `1.25`\. 
If the `kubelet` on your managed and Fargate nodes is on Kubernetes version `1.24` or older, it may only be up to two minor versions older than the `kube-apiserver`\. In other words, if the `kubelet` is version `1.24` or older, you can only update your cluster up to two versions ahead\. For example, if the `kubelet` is on version `1.21`, you can update your Amazon EKS cluster version from `1.21` to `1.22`, and to `1.23`, but you will not be able to update the cluster to `1.24` while the `kubelet` remains on `1.21`\. 
As a best practice before starting an update, make sure that the `kubelet` on your nodes is at the same Kubernetes version as your control plane\. 
If your cluster is configured with a version of the Amazon VPC CNI plugin for Kubernetes that is earlier than `1.8.0`, then we recommend that you update the plugin to the latest version before updating your cluster\. To update the plugin, see [Working with the Amazon VPC CNI plugin for Kubernetes Amazon EKS add\-on](managing-vpc-cni.md)\.
If you're updating your cluster to version `1.25` or later and have the AWS Load Balancer Controller deployed in your cluster, then update the controller to version `2.4.7` or later *before* updating your cluster version to `1.25`\. For more information, see the [Kubernetes 1\.25](kubernetes-versions-standard.md#kubernetes-1.25) release notes\.

------
#### [ eksctl ]

   This procedure requires `eksctl` version `0.175.0` or later\. You can check your version with the following command:

   ```
   eksctl version
   ```

   For instructions on how to install and update `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.

   Update the Kubernetes version of your Amazon EKS control plane\. Replace *`my-cluster`* with your cluster name\. Replace *1\.29* with the Amazon EKS supported version number that you want to update your cluster to\. For a list of supported version numbers, see [Amazon EKS Kubernetes versions](kubernetes-versions.md)\.

   ```
   eksctl upgrade cluster --name my-cluster --version 1.29 --approve
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

   1. Update your Amazon EKS cluster with the following AWS CLI command\. Replace the *`example values`* with your own\. Replace *1\.29* with the Amazon EKS supported version number that you want to update your cluster to\. For a list of supported version numbers, see [Amazon EKS Kubernetes versions](kubernetes-versions.md)\.

      ```
      aws eks update-cluster-version --region region-code --name my-cluster --kubernetes-version 1.29
      ```

      An example output is as follows\.

      ```
      {
          "update": {
              "id": "b5f0ba18-9a87-4450-b5a0-825e6e84496f",
              "status": "InProgress",
              "type": "VersionUpdate",
              "params": [
                  {
                      "type": "Version",
                      "value": "1.29"
                  },
                  {
                      "type": "PlatformVersion",
                      "value": "eks.1"
                  }
              ],
      [...]
              "errors": []
          }
      }
      ```

   1. Monitor the status of your cluster update with the following command\. Use the cluster name and update ID that the previous command returned\. When a `Successful` status is displayed, the update is complete\. The update takes several minutes to complete\.

      ```
      aws eks describe-update --region region-code --name my-cluster --update-id b5f0ba18-9a87-4450-b5a0-825e6e84496f
      ```

      An example output is as follows\.

      ```
      {
          "update": {
              "id": "b5f0ba18-9a87-4450-b5a0-825e6e84496f",
              "status": "Successful",
              "type": "VersionUpdate",
              "params": [
                  {
                      "type": "Version",
                      "value": "1.29"
                  },
                  {
                      "type": "PlatformVersion",
                      "value": "eks.1"
                  }
              ],
      [...]
              "errors": []
          }
      }
      ```

------

1. After your cluster update is complete, update your nodes to the same Kubernetes minor version as your updated cluster\. For more information, see [Self\-managed node updates](update-workers.md) and [Updating a managed node group](update-managed-node-group.md)\. Any new Pods that are launched on Fargate have a `kubelet` version that matches your cluster version\. Existing Fargate Pods aren't changed\.

1. \(Optional\) If you deployed the Kubernetes Cluster Autoscaler to your cluster before updating the cluster, update the Cluster Autoscaler to the latest version that matches the Kubernetes major and minor version that you updated to\.

   1. Open the Cluster Autoscaler [releases](https://github.com/kubernetes/autoscaler/releases) page in a web browser and find the latest Cluster Autoscaler version that matches your cluster's Kubernetes major and minor version\. For example, if your cluster's Kubernetes version is `1.29` find the latest Cluster Autoscaler release that begins with `1.29`\. Record the semantic version number \(`1.29.n`, for example\) for that release to use in the next step\.

   1. Set the Cluster Autoscaler image tag to the version that you recorded in the previous step with the following command\. If necessary, replace `1.29.n` with your own value\.

      ```
      kubectl -n kube-system set image deployment.apps/cluster-autoscaler cluster-autoscaler=registry.k8s.io/autoscaling/cluster-autoscaler:v1.29.n
      ```

1. \(Clusters with GPU nodes only\) If your cluster has node groups with GPU support \(for example, `p3.2xlarge`\), you must update the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) DaemonSet on your cluster\. Replace `vX.X.X` with your desired [NVIDIA/k8s\-device\-plugin](https://github.com/NVIDIA/k8s-device-plugin/releases) version before running the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/vX.X.X/nvidia-device-plugin.yml
   ```

1. Update the Amazon VPC CNI plugin for Kubernetes, CoreDNS, and `kube-proxy` add\-ons\. We recommend updating the add\-ons to the minimum versions listed in [Service account tokens](service-accounts.md#boundserviceaccounttoken-validated-add-on-versions)\.
   + If you are using Amazon EKS add\-ons, select **Clusters** in the Amazon EKS console, then select the name of the cluster that you updated in the left navigation pane\. Notifications appear in the console\. They inform you that a new version is available for each add\-on that has an available update\. To update an add\-on, select the **Add\-ons** tab\. In one of the boxes for an add\-on that has an update available, select **Update now**, select an available version, and then select **Update**\.
   + Alternately, you can use the AWS CLI or `eksctl` to update add\-ons\. For more information, see [Updating an add\-on](managing-add-ons.md#updating-an-add-on)\.

1. If necessary, update your version of `kubectl`\. You must use a `kubectl` version that is within one minor version difference of your Amazon EKS cluster control plane\. For example, a `1.28` `kubectl` client works with Kubernetes `1.27`, `1.28`, and `1.29` clusters\. You can check your currently installed version with the following command\.

   ```
   kubectl version --client
   ```