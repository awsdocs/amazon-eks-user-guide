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


| Kubernetes version | 1\.18 | 1\.17 | 1\.16 | 1\.15 | 1\.14 | 
| --- | --- | --- | --- | --- | --- | 
| Amazon VPC CNI plug\-in | 1\.7\.5 | 1\.7\.5 | 1\.7\.5 | 1\.7\.5 | 1\.7\.5 | 
| DNS \(CoreDNS\) | 1\.7\.0 | 1\.6\.6 | 1\.6\.6 | 1\.6\.6 | 1\.6\.6 | 
| KubeProxy | 1\.18\.8 | 1\.17\.9 | 1\.16\.13 | 1\.15\.11 | 1\.14\.9 | 

If you're using additional add\-ons for your cluster that aren't listed in the previous table, update them to the latest compatible versions after updating your cluster\.

## Update an existing cluster<a name="update-existing-cluster"></a>

Update the cluster and Kubnernetes add\-ons\.

**To update an existing cluster**

1. Compare the Kubernetes version of your cluster control plane to the Kubernetes version of your nodes\.
   + Get the Kubernetes version of your cluster control plane with the following command\.

     ```
     kubectl version --short
     ```
   + Get the Kubernetes version of your nodes with the following command\.

     ```
     kubectl get nodes
     ```

   If your nodes are more than one Kubernetes minor version older than your control plane, then you must upgrade your nodes to a newer Kubernetes minor version before you update your cluster's Kubernetes version\. For more information, see [Kubernetes version and version skew support policy](https://kubernetes.io/docs/setup/release/version-skew-policy/) in the Kubernetes documentation\.

   We recommend that you update your nodes to your cluster's current pre\-update Kubernetes minor version prior to your cluster update\. Your nodes must not run a newer Kubernetes version than your control plane\. For example, if your control plane is running version 1\.17 and your nodes are running version 1\.15, update your nodes to version 1\.16 or 1\.17 \(recommended\) before you update your cluster’s Kubernetes version to 1\.18\. For more information, see [Self\-managed node updates](update-workers.md)\.

1. The pod security policy admission controller is enabled on Amazon EKS clusters running Kubernetes version 1\.13 or later\. If you are upgrading your cluster to Kubernetes version 1\.13 or later, ensure that the proper pod security policies are in place before you update to avoid any issues\. You can check for the default policy with the following command:

   ```
   kubectl get psp eks.privileged
   ```

   If you receive the following error, see [To install or restore the default pod security policy](pod-security-policy.md#install-default-psp) before proceeding\.

   ```
   Error from server (NotFound): podsecuritypolicies.extensions "eks.privileged" not found
   ```

1. If you originally deployed your cluster on Kubernetes `1.17` or earlier, then you may need to remove a deprecated term from your CoreDNS manifest\.

   1. Check to see if your CoreDNS manifest has the line\.

      ```
      kubectl get configmap coredns -n kube-system -o jsonpath='{$.data.Corefile}' | grep upstream
      ```

      If no output is returned, your manifest doesn't have the line and you can skip to the next step to update your cluster\. If output is returned, then you need to remove the line\.

   1. Edit the configmap, removing the line in the file that has the word `upstream` in it\. Do not change anything else in the file\. Once the line is removed, save the changes\.

      ```
      kubectl edit configmap coredns -n kube-system -o yaml
      ```

1. Update your cluster using `eksctl`, the AWS Management Console, or the AWS CLI\.
   + `eksctl` – This procedure requires `eksctl` version `0.30.0-rc.0` or later\. You can check your version with the following command:

     ```
     eksctl version
     ```

     For more information on installing or upgrading `eksctl`, see [Installing or upgrading `eksctl`](eksctl.md#installing-eksctl)\.
**Note**  
This procedure only works for clusters that were created with `eksctl`\.

     Update your Amazon EKS cluster Kubernetes version one minor version later than its current version with the following command, replacing <dev> with your cluster name\. Because Amazon EKS runs a highly available control plane, you can update only one minor version at a time\. See [Kubernetes Version and Version Skew Support Policy](https://kubernetes.io/docs/setup/version-skew-policy/#kube-apiserver) for the rationale behind this requirement\.
**Important**  
You may need to update some of your deployed resources before you can update to 1\.16\. For more information, see [Kubernetes 1\.16 upgrade prerequisites](#1-16-prerequisites)\. Upgrading a cluster from 1\.16 to 1\.17 will fail if any of your AWS Fargate pods have a kubelet minor version earlier than 1\.16\. Before upgrading your cluster from 1\.16 to 1\.17, you need to recycle your Fargate pods so that their kubelet is 1\.16 before attempting to upgrade the cluster to 1\.17\.

     ```
     eksctl upgrade cluster --name <dev> --approve
     ```

     This process takes several minutes to complete\.
   + AWS Management Console

     1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

     1. Choose the name of the cluster to update and choose **Update cluster version**\.

     1. For **Kubernetes version**, select the version to update your cluster to and choose **Update**\.
**Important**  
Upgrading a cluster from 1\.16 to 1\.17 will fail if any of your AWS Fargate pods have a `kubelet` minor version earlier than 1\.16\. Before upgrading your cluster from 1\.16 to 1\.17, you need to recycle your Fargate pods so that their `kubelet` is 1\.16 before attempting to upgrade the cluster to 1\.17\.
You may need to update some of your deployed resources before you can update to 1\.16\. For more information, see [Kubernetes 1\.16 upgrade prerequisites](#1-16-prerequisites)\. 
**Important**  
Because Amazon EKS runs a highly available control plane, you can update only one minor version at a time\. See [Kubernetes Version and Version Skew Support Policy](https://kubernetes.io/docs/setup/version-skew-policy/#kube-apiserver) for the rationale behind this requirement\. Therefore, if your current version is 1\.16 and you want to upgrade to 1\.18, then you must first upgrade your cluster to 1\.17 and then upgrade it from 1\.17 to 1\.18\. If you try to update directly from 1\.16 to 1\.18, then the update version command throws an error\.

     1. For **Cluster name**, type the name of your cluster and choose **Confirm**\.
**Note**  
The cluster update should finish in a few minutes\.
   + AWS CLI

     1. Update your cluster with the following AWS CLI command\. Substitute your cluster name and desired Kubernetes minor version\.
**Important**  
You may need to update some of your deployed resources before you can update to 1\.16\. For more information, see [Kubernetes 1\.16 upgrade prerequisites](#1-16-prerequisites)\. Upgrading a cluster from 1\.16 to 1\.17 will fail if any of your AWS Fargate pods have a kubelet minor version earlier than 1\.16\. Before upgrading your cluster from 1\.16 to 1\.17, you need to recycle your Fargate pods so that their kubelet is 1\.16 before attempting to upgrade the cluster to 1\.17\.
**Important**  
Because Amazon EKS runs a highly available control plane, you can update only one minor version at a time\. See [Kubernetes Version and Version Skew Support Policy](https://kubernetes.io/docs/setup/version-skew-policy/#kube-apiserver) for the rationale behind this requirement\. Therefore, if your current version is 1\.16 and you want to upgrade to 1\.18, then you must first upgrade your cluster to 1\.17 and then upgrade it from 1\.17 to 1\.18\. If you try to update directly from 1\.16 to 1\.18, then the update version command throws an error\.

        ```
        aws eks --region <region-code> update-cluster-version --name <my-cluster> --kubernetes-version <1.18>
        ```

        Output:

        ```
        {
            "update": {
                "id": "<b5f0ba18-9a87-4450-b5a0-825e6e84496f>",
                "status": "InProgress",
                "type": "VersionUpdate",
                "params": [
                    {
                        "type": "Version",
                        "value": "1.18"
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

     1. Monitor the status of your cluster update with the following command, using the cluster name and update ID that the previous command returned\. Your update is complete when the status appears as `Successful`\.
**Note**  
The cluster update should finish in a few minutes\.

        ```
        aws eks --region <region-code> describe-update --name <my-cluster> --update-id <b5f0ba18-9a87-4450-b5a0-825e6e84496f>
        ```

        Output:

        ```
        {
            "update": {
                "id": "b5f0ba18-9a87-4450-b5a0-825e6e84496f",
                "status": "<Successful>",
                "type": "VersionUpdate",
                "params": [
                    {
                        "type": "Version",
                        "value": "1.18"
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

1. Patch the `kube-proxy` daemonset to use the image that corresponds to your cluster's Region and current Kubernetes version \(in this example, `1.18.8`\)\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html)

   1. First, retrieve your current `kube-proxy` image:

      ```
      kubectl get daemonset kube-proxy --namespace kube-system -o=jsonpath='{$.spec.template.spec.containers[:1].image}'
      ```

   1. Update `kube-proxy` to the recommended version by taking the output from the previous step and replacing the version tag with your cluster's recommended `kube-proxy` version:

      ```
      kubectl set image daemonset.apps/kube-proxy \
          -n kube-system \
          kube-proxy=<602401143452.dkr.ecr.us-west-2.amazonaws.com>/eks/kube-proxy:v<1.18.8>-eksbuild.1
      ```

      Your account ID and region may differ from the example above\.

   1. \(Optional\) If using x86 and Arm nodes in the same cluster, and your cluster was deployed before August 17,2020, then edit your `kube-proxy` manifest to include a node selector for multiple hardware architectures with the following command\. This is a one\-time operation\. Once you've added the selector to your manifest, you don't need to do it each time you upgrade\. If you cluster was deployed on or after August 17, 2020, then `kube-proxy` is already multi\-architecture capable\.

      ```
      kubectl edit -n kube-system daemonset/kube-proxy
      ```

      Add the following node selector to the file in the editor and then save the file\. For an example of where to include this text in the editor, see the [CNI manifest](https://github.com/aws/amazon-vpc-cni-k8s/blob/release-1.6/config/v1.6/aws-k8s-cni.yaml#L76-%23L80) file on GitHub\. This enables Kubernetes to pull the correct hardware image based on the node's hardware architecture\.

      ```
      - key: "beta.kubernetes.io/arch"
                          operator: In
                          values:
                            - amd64
                            - arm64
      ```

1. Check your cluster's DNS provider\. Clusters that were created with Kubernetes version 1\.10 shipped with `kube-dns` as the default DNS and service discovery provider\. If you have updated a 1\.10 cluster to a newer version and you want to use CoreDNS for DNS and service discovery, then you must install CoreDNS and remove `kube-dns`\.

   To check if your cluster is already running CoreDNS, use the following command\.

   ```
   kubectl get pod -n kube-system -l k8s-app=kube-dns
   ```

   If the output shows `coredns` in the pod names, you're already running CoreDNS in your cluster\. If not, see [Installing or upgrading CoreDNS](coredns.md) to install CoreDNS on your cluster, update it to the recommended version, return here, and skip steps 7\-8\.

1. Check the current version of your cluster's `coredns` deployment\.

   ```
   kubectl describe deployment coredns --namespace kube-system | grep Image | cut -d "/" -f 3
   ```

   Output:

   ```
   coredns:v<1.1.3>
   ```

   The recommended `coredns` versions for the corresponding Kubernetes versions are as follows:    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html)

1. If your current `coredns` version is 1\.5\.0 or later, but earlier than the recommended version, then skip this step\. If your current version is earlier than 1\.5\.0, then you need to modify the config map for `coredns` to use the `forward` plug\-in, rather than the `proxy` plug\-in\.

   1. Open the configmap with the following command\.

      ```
      kubectl edit configmap coredns -n kube-system
      ```

   1. Replace `proxy` in the following line with `forward`\. Save the file and exit the editor\.

      ```
      proxy . /etc/resolv.conf
      ```

1. Retrieve your current `coredns` image:

   ```
   kubectl get deployment coredns --namespace kube-system -o=jsonpath='{$.spec.template.spec.containers[:1].image}'
   ```

1. Update `coredns` to the recommended version by taking the output from the previous step and replacing the version tag with your cluster's recommended `coredns` version:

   ```
   kubectl set image --namespace kube-system deployment.apps/coredns \
               coredns=<602401143452.dkr.ecr.us-west-2.amazonaws.com>/eks/coredns:v<1.7.0>-eksbuild.1
   ```
**Note**  
If you're updating to the latest 1\.14 version, then remove `-eksbuild.1` from the end of the image above\.

1. \(Optional\) If using x86 and Arm nodes in the same cluster, and your cluster was deployed before August 17,2020, then edit your `coredns` manifest to include a node selector for multiple hardware architectures with the following command\. This is a one\-time operation\. Once you've added the selector to your manifest, you don't need to do it each time you upgrade\. If you cluster was deployed on or after August 17, 2020, then `coredns` is already multi\-architecture capable\.

   ```
   kubectl edit -n kube-system deployment/coredns
   ```

   Add the following node selector to the file in the editor and then save the file\. For an example of where to include this text in the editor, see the [CNI manifest](https://github.com/aws/amazon-vpc-cni-k8s/blob/release-1.6/config/v1.6/aws-k8s-cni.yaml#L76-%23L80) file on GitHub\.

   ```
   - key: "beta.kubernetes.io/arch"
                       operator: In
                       values:
                         - amd64
                         - arm64
   ```

1. Check the version of your cluster's Amazon VPC CNI Plugin for Kubernetes\. Use the following command to print your cluster's CNI version\.

   ```
   kubectl describe daemonset aws-node --namespace kube-system | grep Image | cut -d "/" -f 2
   ```

   Output:

   ```
   amazon-k8s-cni:<1.6.3>
   ```

   If your CNI version is earlier than 1\.7\.5, then use the appropriate command below to update your CNI version to the latest recommended version:
   + US West \(Oregon\) \(`us-west-2`\)

     ```
     kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/v1.7.5/config/v1.7/aws-k8s-cni.yaml
     ```
   + China \(Beijing\) \(`cn-north-1`\) or China \(Ningxia\) \(`cn-northwest-1`\)

     ```
     kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/v1.7.5/config/v1.7/aws-k8s-cni-cn.yaml
     ```
   + AWS GovCloud \(US\-East\) \(`us-gov-east-1`\)

     ```
     kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/v1.7.5/config/v1.7/aws-k8s-cni-us-gov-east-1.yaml
     ```
   + AWS GovCloud \(US\-West\) \(`us-gov-west-1`\)

     ```
     kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/v1.7.5/config/v1.7/aws-k8s-cni-us-gov-west-1.yaml
     ```
   + For all other Regions
     + Download the manifest file\.

       ```
       curl -o aws-k8s-cni.yaml https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/v1.7.5/config/v1.7/aws-k8s-cni.yaml
       ```
     + Replace `<region-code>` in the following command with the Region that your cluster is in and then run the modified command to replace the Region code in the file \(currently `us-west-2`\)\.

       ```
       sed -i -e 's/us-west-2/<region-code>/' aws-k8s-cni.yaml
       ```
     + Apply the modified manifest file to your cluster\.

       ```
       kubectl apply -f aws-k8s-cni.yaml
       ```

1. \(Optional\) If you deployed the Kubernetes Cluster Autoscaler to your cluster prior to upgrading the cluster, update the Cluster Autoscaler to the latest version that matches the Kubernetes major and minor version that you upgraded to\.
**Important**  
You can't use the Kubernetes Cluster Autoscaler with Arm\.

   1. Open the Cluster Autoscaler [releases](https://github.com/kubernetes/autoscaler/releases) page in a web browser and find the latest Cluster Autoscaler version that matches your cluster's Kubernetes major and minor version\. For example, if your cluster's Kubernetes version is 1\.18 find the latest Cluster Autoscaler release that begins with 1\.18\. Record the semantic version number \(`<1.18.n>`\) for that release to use in the next step\.

   1. Set the Cluster Autoscaler image tag to the version that you recorded in the previous step with the following command\. Replace <1\.18\.n> with your own value\. You can replace `us` with `<asia>` or `<eu>`\.

      ```
      kubectl -n kube-system set image deployment.apps/cluster-autoscaler cluster-autoscaler=<us>.gcr.io/k8s-artifacts-prod/autoscaling/cluster-autoscaler:v<1.18.n>
      ```
**Note**  
Depending on the version that you need, you may need to change the previous address to `gcr.io/google-containers/cluster-autoscaler:v1.<n.n>` \. The image address is listed on the [releases](https://github.com/kubernetes/autoscaler/releases) page\.

1. \(Clusters with GPU nodes only\) If your cluster has node groups with GPU support \(for example, `p3.2xlarge`\), you must update the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) DaemonSet on your cluster with the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.6.0/nvidia-device-plugin.yml
   ```

1. After your cluster update is complete, update your nodes to the same Kubernetes version of your updated cluster\. For more information, see [Self\-managed node updates](update-workers.md) or [Updating a managed node group](update-managed-node-group.md)\. Any new pods launched on Fargate will have a `kubelet` version that matches your cluster version\. Existing Fargate pods will not be changed\.

## Kubernetes 1\.16 upgrade prerequisites<a name="1-16-prerequisites"></a>

As noted in the [Kubernetes 1\.15 changelog](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.15.md#deprecations-and-removals), and [Deprecated APIs Removed In 1\.16: Here’s What You Need To Know](https://kubernetes.io/blog/2019/07/18/api-deprecations-in-1-16/) documents, if you have an existing cluster, API changes are required for the following deployed resources before upgrading a cluster to 1\.16\.

**Warning**  
If you do not change these APIs before upgrading to 1\.16, workloads will fail after the upgrade is complete\.
+ NetworkPolicy resources will no longer be served from `extensions/v1beta1` in v1\.16\. Migrate use to the `networking.k8s.io/v1` API, available since v1\.8\. Existing persisted data can be retrieved through the `networking.k8s.io/v1` API\.
+ PodSecurityPolicy resources will no longer be served from `extensions/v1beta1` in v1\.16\. Migrate to the `policy/v1beta1` API, available since v1\.10\. Existing persisted data can be retrieved through the `policy/v1beta1` API\.
+ DaemonSet, Deployment, StatefulSet, and ReplicaSet resources will no longer be served from `extensions/v1beta1`, `apps/v1beta1`, or `apps/v1beta2` in v1\.16\. Migrate to the `apps/v1` API, available since v1\.9\. Existing persisted data can be retrieved through the `apps/v1` API\. For example, to convert a Deployment that currently uses `apps/v1beta1`, enter the following command\.

  ```
  kubectl convert -f ./<my-deployment.yaml> --output-version apps/v1
  ```
**Note**  
The previous command may use different default values from what is set in your current manifest file\. To learn more about a specific resource, see the Kubernetes [API reference](https://kubernetes.io/docs/reference/#api-reference)\.

If you originally created an Amazon EKS cluster with Kubernetes version 1\.11 or earlier and have not removed the `--resource-container` flag from the `kube-proxy` DaemonSet, then updating to Kubernetes 1\.16 will cause `kube-proxy` failures\. This flag is deprecated in Kubernetes 1\.16\. For more information, see `kube-proxy` in [Kubernetes 1\.16 Deprecations and removals](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.16.md#deprecations-and-removals)\. You must remove this flag before updating to Kubernetes 1\.16\.<a name="1-16-do-now"></a>

**What you need to do before upgrading to 1\.16**
+ Change your YAML files to reference the new APIs\.
+ Update custom integrations and controllers to call the new APIs\.
+ Ensure that you use an updated version of any third party tools, such as ingress controllers, continuous delivery systems, and others, that call the new APIs\.

  To easily check for deprecated API usage in your cluster, make sure that the `audit` [control plane log](control-plane-logs.md) is enabled, and specify `v1beta` as a filter for the events\. All of the replacement APIs are in Kubernetes versions later than 1\.10\. Applications on any supported version of Amazon EKS can begin using the updated APIs now\.
+ Remove the `--resource-container=""` flag from your `kube-proxy` DaemonSet, if your cluster was originally deployed with Kubernetes 1\.11 or earlier or use a kube\-proxy configuration file \(recommended\)\. To determine whether your current version of `kube-proxy` has the flag, enter the following command\.

  ```
  kubectl get daemonset kube-proxy --namespace kube-system -o yaml | grep 'resource-container='
  ```

  If you receive no output, then you don't need to remove anything\. If you receive output similar to `--resource-container=""`, then you need to remove the flag\. Enter the following command to edit your current `kube-proxy` config\.

  ```
  kubectl edit daemonset kube-proxy --namespace kube-system
  ```

  With the editor open, remove the `--resource-container=""` line, and save the file\. We recommend that you instead, start using a kube\-proxy configuration file\. To do so, download the following manifest\.

  ```
  curl -o kube-proxy-daemonset.yaml https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2020-06-10/kube-proxy-daemonset.yaml
  ```

  Determine your cluster's endpoint with the following command\.

  ```
  aws eks describe-cluster \
      --name <cluster-name> \
      --region <region-code> \
      --query 'cluster.endpoint' \
      --output text
  ```

  Output

  ```
  https://<A89DBB2140C8AC0C2F920A36CCC6E18C>.sk1.<region-code>.eks.amazonaws.com
  ```

  Edit the` kube-proxy-daemonset.yaml` file that you downloaded\. In your editor, replace <MASTER\_ENDPOINT> with the output from the previous command\. Replace <REGION> with your cluster's region\. On the same line, replace the version with the version of your cluster, if necessary\. Apply the file with the following command\.

  ```
  kubectl apply -f kube-proxy-daemonset.yaml
  ```