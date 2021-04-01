# Updating a cluster<a name="update-cluster"></a>

You can update an existing cluster to a new Kubernetes version or configure managed add\-ons for your cluster\.

## Updating an Amazon EKS cluster Kubernetes version<a name="update-kubernetes-version"></a>

When a new Kubernetes version is available in Amazon EKS, you can update your cluster to the latest version\. 

**Important**  
We recommend that before updating to a new Kubernetes version that you review the information in [Amazon EKS Kubernetes versions](kubernetes-versions.md) and in the update steps in this topic\.

New Kubernetes versions have introduced significant changes\. Therefore, we recommend that you test the behavior of your applications against a new Kubernetes version before you update your production clusters\. You can achieve this by building a continuous integration workflow to test your application behavior before moving to a new Kubernetes version\.

The update process consists of Amazon EKS launching new API server nodes with the updated Kubernetes version to replace the existing ones\. Amazon EKS performs standard infrastructure and readiness health checks for network traffic on these new nodes to verify that they're working as expected\. If any of these checks fail, Amazon EKS reverts the infrastructure deployment, and your cluster remains on the prior Kubernetes version\. Running applications aren't affected, and your cluster is never left in a non\-deterministic or unrecoverable state\. Amazon EKS regularly backs up all managed clusters, and mechanisms exist to recover clusters if necessary\. We're constantly evaluating and improving our Kubernetes infrastructure management processes\.

To update the cluster, Amazon EKS requires two to three free IP addresses from the subnets that were provided when you created the cluster\. If these subnets don't have available IP addresses, then the update can fail\. Additionally, if any of the subnets or security groups that were provided during cluster creation have been deleted, the cluster update process can fail\.

**Note**  
Even though Amazon EKS runs a highly available control plane, you might experience minor service interruptions during an update\. For example, if you attempt to connect to an API server just before or just after it's terminated and replaced by a new API server running the new version of Kubernetes, you might experience API call errors or connectivity issues\. If this happens, retry your API operations until they succeed\.

Amazon EKS doesn't modify any of your Kubernetes add\-ons when you update a cluster\. After updating your cluster, we recommend that you update your add\-ons to the versions listed in the following table for the new Kubernetes version that you're updating to\. Steps to accomplish this are included in the update procedures\.


| Kubernetes version | 1\.19 | 1\.18 | 1\.17 | 1\.16 | 1\.15 | 
| --- | --- | --- | --- | --- | --- | 
| Amazon VPC CNI plug\-in | 1\.7\.5 | 1\.7\.5 | 1\.7\.5 | 1\.7\.5 | 1\.7\.5 | 
| DNS \(CoreDNS\) | 1\.8\.0 | 1\.7\.0 | 1\.6\.6 | 1\.6\.6 | 1\.6\.6 | 
| KubeProxy | 1\.19\.6 | 1\.18\.8 | 1\.17\.9 | 1\.16\.13 | 1\.15\.11 | 

If you're using additional add\-ons for your cluster that aren't listed in the previous table, update them to the latest compatible versions after updating your cluster\.

### Update an existing cluster<a name="update-existing-cluster"></a>

Update the cluster and Kubernetes add\-ons\.

**To update an existing cluster**

1. Compare the Kubernetes version of your cluster control plane to the Kubernetes version of your nodes\.
   + Get the Kubernetes version of your cluster control plane with the following command\.

     ```
     kubectl version --short
     ```
   + Get the Kubernetes version of your nodes with the following command\. This command returns all self\-managed and managed Amazon EC2 and Fargate nodes\. Each Fargate pod is listed as its own node\.

     ```
     kubectl get nodes
     ```

   The Kubernetes minor version of the managed and Fargate nodes in your cluster must be the same as the version of your control plane's current version before you update your control plane to a new Kubernetes version\. For example, if your control plane is running version 1\.18 and any of your nodes are running version 1\.17, update your nodes to version 1\.18 before updating your control plane's Kubernetes version to 1\.19\. We also recommend that you update your self\-managed nodes to the same version as your control plane before updating the control plane\. For more information see [Updating a managed node group](update-managed-node-group.md) and [Self\-managed node updates](update-workers.md)\. To update the version of a Fargate node, delete the pod that is represented by the node and redeploy the pod after you update your control plane\.

1. The pod security policy admission controller is enabled by default on Amazon EKS clusters\. Before updating your cluster, ensure that the proper pod security policies are in place before you update to avoid any issues\. You can check for the default policy with the following command:

   ```
   kubectl get psp eks.privileged
   ```

   If you receive the following error, see [default pod security policy](pod-security-policy.md#default-psp) before proceeding\.

   ```
   Error from server (NotFound): podsecuritypolicies.extensions "eks.privileged" not found
   ```

1. If you originally deployed your cluster on Kubernetes `1.17` or earlier, then you may need to remove a discontinued term from your CoreDNS manifest\.

   1. Check to see if your CoreDNS manifest has a line that only has the word `upstream`\.

      ```
      kubectl get configmap coredns -n kube-system -o jsonpath='{$.data.Corefile}' | grep upstream
      ```

      If no output is returned, your manifest doesn't have the line and you can skip to the next step to update your cluster\. If the word `upstream` is returned, then you need to remove the line\.

   1. Edit the configmap, removing the line near the top of the file that only has the word `upstream`\. Don't change anything else in the file\. After the line is removed, save the changes\.

      ```
      kubectl edit configmap coredns -n kube-system -o yaml
      ```

1. Update your cluster using `eksctl`, the AWS Management Console, or the AWS CLI\.
**Important**  
Because Amazon EKS runs a highly available control plane, you can update only one minor version at a time\. See [Kubernetes Version and Version Skew Support Policy](https://kubernetes.io/docs/setup/version-skew-policy/#kube-apiserver) for the rationale behind this requirement\. Therefore, if your current version is 1\.17 and you want to update to 1\.19, then you must first update your cluster to 1\.18 and then update it from 1\.18 to 1\.19\.
Make sure that the `kubelet` on your managed and Fargate nodes are at the same Kubernetes version as your control plane before you update\. We also recommend that your self\-managed nodes are at the same version as the control plane, though they can be up to one version behind the control plane's current version\. 
Updating a cluster from 1\.16 to 1\.17 will fail if you have any AWS Fargate pods that have a `kubelet` minor version earlier than 1\.16\. Before updating your cluster from 1\.16 to 1\.17, you need to recycle your Fargate pods so that their `kubelet` is 1\.16 before attempting to update the cluster to 1\.17\.
You may need to update some of your deployed resources before you can update to 1\.16\. For more information, see [Kubernetes 1\.16 update prerequisites](#1-16-prerequisites)\. 
Updating your cluster to a newer version may overwrite custom configurations\.

------
#### [ eksctl ]

   This procedure requires `eksctl` version `0.43.0-rc.0` or later\. You can check your version with the following command:

   ```
   eksctl version
   ```

   For more information about installing or updating `eksctl`, see [Installing or upgrading `eksctl`](eksctl.md#installing-eksctl)\.

   Update your Amazon EKS control plane's Kubernetes version one minor version later than its current version with the following command\. Replace *`<my-cluster>`* \(including *`<>`*\) with your cluster name\.

   ```
   eksctl upgrade cluster --name <my-cluster> --approve
   ```

   The update takes several minutes to complete\.

------
#### [ AWS Management Console ]

   1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

   1. Choose the name of the cluster to update and choose **Update cluster version**\.

   1. For **Kubernetes version**, select the version to update your cluster to and choose **Update**\.

   1. For **Cluster name**, type the name of your cluster and choose **Confirm**\.

      The update takes several minutes to complete\.

------
#### [ AWS CLI ]

   1. Update your cluster with the following AWS CLI command\. Replace the *`<example-values>`* \(including *`<>`*\) with your own\.

      ```
      aws eks update-cluster-version \
       --region <region-code> \
       --name <my-cluster> \
       --kubernetes-version <1.19>
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
                      "value": "1.19"
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

   1. Monitor the status of your cluster update with the following command\. Use the cluster name and update ID that the previous command returned\. Your update is complete when the status appears as `Successful`\. The update takes several minutes to complete\.

      ```
      aws eks describe-update \
        --region <region-code> \
        --name <my-cluster> \
        --update-id <b5f0ba18-9a87-4450-b5a0-825e6e84496f>
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
                      "value": "1.19"
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

1. Patch the `kube-proxy` daemonset to use the image that corresponds to your cluster's Region and current Kubernetes version \(in this example, `1.19.6`\)\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html)

   1. First, retrieve your current `kube-proxy` image:

      ```
      kubectl get daemonset kube-proxy --namespace kube-system -o=jsonpath='{$.spec.template.spec.containers[:1].image}'
      ```

      Example output

      ```
      602401143452.dkr.ecr.us-west-2.amazonaws.com/eks/kube-proxy:v1.18.8-eksbuild.1
      ```

   1. Update `kube-proxy` to the recommended version by replacing *`602401143452`* and *`us-west-2`* with the values from your output and replace *`1.19.6`* with your cluster's recommended `kube-proxy` version\. If you're deploying a version that is earlier than `1.19.6`, then replace *`eksbuild.2`* with `eksbuild.1`\.

      ```
      kubectl set image daemonset.apps/kube-proxy \
        -n kube-system \
        kube-proxy=602401143452.dkr.ecr.us-west-2.amazonaws.com/eks/kube-proxy:v1.19.6-eksbuild.2
      ```

   1. \(Optional\) If you're using x86 and Arm nodes in the same cluster and your cluster was deployed before August 17,2020\. Then, edit your `kube-proxy` manifest to include a node selector for multiple hardware architectures with the following command\. This is a one\-time operation\. After you've added the selector to your manifest, you don't need to do it each time you update\. If your cluster was deployed on or after August 17, 2020, then `kube-proxy` is already multi\-architecture capable\.

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

   1. \(Optional\) If your cluster was oriniginally created with Kubernetes v1\.14 or later, then you can skip this step because `kube-proxy` already includes this `Affinity Rule`\. If you originally created an Amazon EKS cluster with Kubernetes version 1\.13 or earilier and intend to use Fargate nodes, then edit your `kube-proxy` manifest to include a `NodeAffinity` rule to prevent `kube-proxy` pods from sheduling on Fargate nodes\. This is a one\-time edit\. Once you've added the `Affinity Rule` to your manifest, you don't need to do it each time you upgrade your cluster\. Edit your `kube-proxy` daemonset\.

      ```
      kubectl edit -n kube-system daemonset/kube-proxy
      ```

      Add the following `Affinity Rule` to the `Daemonset` `spec` section of the file in the editor and then save the file\. For an example of where to include this text in the editor, see the [CNI manifest](https://github.com/aws/amazon-vpc-cni-k8s/blob/release-1.6/config/v1.6/aws-k8s-cni.yaml#L95-%23L97) file on GitHub\.

      ```
      - key: eks.amazonaws.com/compute-type
        operator: NotIn
        values:
        - fargate
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
   coredns:v<1.6.6>
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

1. Update `coredns` to the recommended version by replacing *`602401143452`*, *`us-west-2`*, and *`amazonaws.com`* in the following command with your output from the previous command\. Replace *`1.8.0`* with the version recommended for your cluster's Kubernetes version and then run the modified command\.

   ```
   kubectl set image --namespace kube-system deployment.apps/coredns \
               coredns=602401143452.dkr.ecr.us-west-2.amazonaws.com/eks/coredns:v1.8.0-eksbuild.1
   ```

1. \(Optional\) If you're using x86 and Arm nodes in the same cluster and your cluster was deployed before August 17,2020, then edit your `coredns` manifest to include a node selector for multiple hardware architectures with the following command\. This is a one\-time operation\. After you've added the selector to your manifest, you don't need to do it each time you update\. If you cluster was deployed on or after August 17, 2020, then `coredns` is already multi\-architecture capable\.

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

   The output is as follows:

   ```
   amazon-k8s-cni:<1.6.3>
   ```

   If your CNI version is earlier than 1\.7\.5, then use the appropriate command below to update your CNI version to the latest recommended version\.
**Important**  
Any changes you've made to the plugin's default settings on your cluster can be overwritten with default settings when applying the new version of the manifest\. To prevent loss of your custom settings, download the manifest, change the default settings as necessary, and then apply the modified manifest to your cluster\. 
   + US West \(Oregon\) \(`us-west-2`\)

     ```
     kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/v1.7.5/config/v1.7/aws-k8s-cni.yaml
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
     + Replace *`<region-code>`* in the following command with the Region that your cluster is in\. Then, run the modified command to replace the Region code in the file \(currently `us-west-2`\)\.

       ```
       sed -i -e 's/us-west-2/<region-code>/' aws-k8s-cni.yaml
       ```
     + Apply the modified manifest file to your cluster\.

       ```
       kubectl apply -f aws-k8s-cni.yaml
       ```

1. \(Optional\) If you deployed the Kubernetes Cluster Autoscaler to your cluster before updating the cluster, update the Cluster Autoscaler to the latest version that matches the Kubernetes major and minor version that you updated to\.
**Important**  
You can't use the Kubernetes Cluster Autoscaler with Arm\.

   1. Open the Cluster Autoscaler [releases](https://github.com/kubernetes/autoscaler/releases) page in a web browser and find the latest Cluster Autoscaler version that matches your cluster's Kubernetes major and minor version\. For example, if your cluster's Kubernetes version is 1\.19 find the latest Cluster Autoscaler release that begins with 1\.19\. Record the semantic version number \(`<1.19.n>`\) for that release to use in the next step\.

   1. Set the Cluster Autoscaler image tag to the version that you recorded in the previous step with the following command\. If necessary, replace *1\.19*\.*n* with your own value\.

      ```
      kubectl -n kube-system set image deployment.apps/cluster-autoscaler cluster-autoscaler=k8s.gcr.io/autoscaling/cluster-autoscaler:v1.19.n
      ```

1. \(Clusters with GPU nodes only\) If your cluster has node groups with GPU support \(for example, `p3.2xlarge`\), you must update the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) DaemonSet on your cluster with the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.8.0/nvidia-device-plugin.yml
   ```

1. After your cluster update is complete, update your nodes to the same Kubernetes version of your updated cluster\. For more information, see [Self\-managed node updates](update-workers.md) or [Updating a managed node group](update-managed-node-group.md)\. Any new pods launched on Fargate will have a `kubelet` version that matches your cluster version\. Existing Fargate pods won't be changed\.

### Kubernetes 1\.16 update prerequisites<a name="1-16-prerequisites"></a>

As noted in the [Kubernetes 1\.15 changelog](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.15.md#deprecations-and-removals) and [Deprecated APIs Removed In 1\.16: Here's What You Need To Know](https://kubernetes.io/blog/2019/07/18/api-deprecations-in-1-16/) documents, if you have an existing cluster, API changes are required for the following deployed resources before updating a cluster to 1\.16\.

**Warning**  
If you don't change these APIs before updating to 1\.16, workloads fail after the update is complete\.
+ NetworkPolicy resources will no longer be served from `extensions/v1beta1` in v1\.16\. Migrate use to the `networking.k8s.io/v1` API, available since v1\.8\. Existing persisted data can be retrieved through the `networking.k8s.io/v1` API\.
+ PodSecurityPolicy resources will no longer be served from `extensions/v1beta1` in v1\.16\. Migrate to the `policy/v1beta1` API, available since v1\.10\. Existing persisted data can be retrieved through the `policy/v1beta1` API\.
+ DaemonSet, Deployment, StatefulSet, and ReplicaSet resources will no longer be served from `extensions/v1beta1`, `apps/v1beta1`, or `apps/v1beta2` in v1\.16\. Migrate to the `apps/v1` API, available since v1\.9\. Existing persisted data can be retrieved through the `apps/v1` API\. For example, to convert a Deployment that currently uses `apps/v1beta1`, enter the following command\.

  ```
  kubectl convert -f ./<my-deployment.yaml> --output-version apps/v1
  ```
**Note**  
The previous command may use different default values from what is set in your current manifest file\. To learn more about a specific resource, see the Kubernetes [API reference](https://kubernetes.io/docs/reference/#api-reference)\.

If you originally created an Amazon EKS cluster with Kubernetes version 1\.11 or earlier and haven't removed the `--resource-container` flag from the `kube-proxy` DaemonSet, then updating to Kubernetes 1\.16 will cause `kube-proxy` failures\. This flag is no longer supported in Kubernetes 1\.16\. For more information, see `kube-proxy` in [Kubernetes 1\.16 Deprecations and removals](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.16.md#deprecations-and-removals)\. You must remove this flag before updating to Kubernetes 1\.16\.<a name="1-16-do-now"></a>

**What you need to do before updating to 1\.16**
+ Change your YAML files to reference the new APIs\.
+ Update custom integrations and controllers to call the new APIs\.
+ Ensure that you use an updated version of any third party tools, such as ingress controllers, continuous delivery systems, and other tools that call the new APIs\.

  To easily check for discontinued API usage in your cluster, make sure that the `audit` [control plane log](control-plane-logs.md) is enabled, and specify `v1beta` as a filter for the events\. All of the replacement APIs are in Kubernetes versions later than 1\.10\. Applications on any supported version of Amazon EKS can begin using the updated APIs now\.
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

  The output is as follows:

  ```
  https://<A89DBB2140C8AC0C2F920A36CCC6E18C>.sk1.<region-code>.eks.amazonaws.com
  ```

  Edit the` kube-proxy-daemonset.yaml` file that you downloaded\. In your editor, replace `<MASTER_ENDPOINT>` \(including `<>`\) with the output from the previous command\. Replace `<REGION>` with your cluster's Region\. On the same line, replace the version with the version of your cluster if necessary\. Apply the file with the following command\.

  ```
  kubectl apply -f kube-proxy-daemonset.yaml
  ```

## Configure an Amazon EKS add\-on<a name="update-cluster-add-ons"></a>

An add\-on is Kubernetes operational software that provides capabilities like observability, scaling, networking, and AWS cloud resource integrations for your Amazon EKS cluster\. You can manage add\-ons yourself, or let Amazon EKS control the launch and version of the add\-on through the Amazon EKS API for clusters running Kubernetes version 1\.18 with platform version `eks.3` or later\. Amazon EKS add\-ons use the Kubernetes *Server\-Side Apply* feature, which is only available with Kubernetes version 1\.18 or later\. For more information, see [Server\-Side Apply](https://kubernetes.io/docs/reference/using-api/server-side-apply/) in the Kubernetes documentation\.

You can configure an `eksctl` using eksctl or the AWS Management Console\.

------
#### [ eksctl ]

Replace the *`<example values>`* \(including *`<>`*\) with your own values\.

1. Add an Amazon EKS add\-on to your cluster\.

   1. Determine which Amazon EKS add\-ons are available for your cluster\.

      ```
      eksctl utils describe-addon-versions --cluster <my-cluster>
      ```

   1. Add an Amazon EKS add\-on to your cluster\. When specifying `<name-of-addon>`, specify a name returned from the previous command\. The `--force` option overwrites any existing configuration if the add\-on is already installed on your cluster, but you're managing it yourself\. You can specify the ARN of an IAM role, policy, or both\. The add\-on's Kubernetes service account is then annotated with the role\. If you don't specify an existing role or policy, `eksctl` creates a default role and attaches the necessary policy to it for you\.

      ```
      eksctl create addon --name <name--of-addon-from-previous-command> --cluster <my-cluster> --force
      ```

1. You can update an add\-on to a newer version\. See other update options with `eksctl update addon -h`\.

   1. Determine which versions are available for an add\-on\.

      ```
      eksctl utils describe-addon-versions --name <name-of-addon> --cluster <my-cluster>
      ```

   1. Update the add\-on to a newer version\.

      ```
      eksctl update addon --name <name-from-previous-command> --version <version-from-previous-command> --cluster <my-cluster>
      ```

1. Delete an Amazon EKS add\-on from your cluster\.

   1. See which add\-ons are currently enabled for your cluster\.

      ```
      eksctl get addons --cluster <my-cluster>
      ```

   1. Delete an Amazon EKS add\-on from your cluster\. Deleting the add\-on also deletes any IAM roles associated to it\.

      ```
      eksctl delete addon --cluster <my-cluster> --name <addon-name-from-previous-command>
      ```

------
#### [ AWS Management Console ]

**To configure an Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation, select **Clusters**, and then select the name of the cluster that you want to configure an Amazon EKS add\-on for\.

1. Choose the **Configuration** tab and then choose the **Add\-ons** tab\.

1. Configure the add\-on\. To add a new Amazon EKS add\-on, select **Add new**\. To change an existing Amazon EKS add\-on, select the add\-on and choose **Edit**\. To remove an add\-on, select the add\-on and select **Remove**\. Removing the add\-on also removes it from your cluster\. You can always manually add the add\-on back to your cluster, but be aware that its removal and addition could cause service disruption to your cluster\.

   1. Select the **Name** of the Amazon EKS add\-on that you want to add or edit\.

   1. Select the **Version** of the Amazon EKS add\-on that you want to use\.

   1. Select the **Service account role** that you want the add\-on to run as\. If you don't select an existing IAM role, then the [Amazon EKS node IAM role](create-node-role.md) is used\. However, we recommend specifying your own role so that the node IAM role isn't assigned more than the minimum permissions that it requires\. 

      Whichever role you choose must be assigned the permissions required by the add\-on\. For example, the role that you specify for the **vpc\-cni** add\-on must have the `[AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor)` IAM policy assigned to it, and the role must have unique settings in its trust relationship\. For more information, see [Create your CNI plugin IAM role with the AWS Management Console](cni-iam-role.md#configure-cni-iam-console-create-iam-account)\. If the Kubernetes service account used by the add\-on isn't currently annotated with the IAM role that you specify, then the API will annotate the service account with the IAM role for you\.
**Important**  
To specify an IAM role, you must have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To create an OIDC provider, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.

   1. If you currently have the add\-on deployed to your cluster, are managing it yourself, and want Amazon EKS to manage the add\-on you can **Enable Override existing configuration for this add\-on on the cluster**\. If you enable this option, then any setting for the existing add\-on can be overwritten with the Amazon EKS add\-on's settings\. If you currently have the add\-on deployed to your cluster and don't enable this option and any of the Amazon EKS add\-on settings conflict with your existing settings, then migrating the add\-on to an Amazon EKS add\-on will fail, and you'll receive an error message to help you resolve the conflict\.

   1. Select **Add** or **Update**\.

------

## Enabling envelope encryption on an existing cluster<a name="enable-kms"></a>

If you enable secret encryption, the Kubernetes secrets are encrypted using the AWS Key Management Service \(KMS\) customer master key \(CMK\) that you select\. The CMK must be symmetric, created in the same region as the cluster, and if the CMK was created in a different account, the user must have access to the CMK\. For more information, see [Allowing users in other accounts to use a CMK](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html) in the *AWS Key Management Service Developer Guide*\. Enabling envelope encryption on an existing cluster is supported for Kubernetes version `1.13` or later\.

**Warning**  
You cannot disable envelope encryption after enabling it\. This action is irreversible\.

------
#### [ eksctl  ]

You can enable encryption in two ways:
+ Add encryption to your cluster with a single command\.

  To automatically re\-encrypt your secrets:

  ```
  eksctl utils enable-secrets-encryption /
      --cluster <my-cluster> /
      --key-arn arn:aws:kms:<Region-code>:<account>:key/<key>
  ```

  To opt\-out of automatically re\-encrypting your secrets:

  ```
  eksctl utils enable-secrets-encryption 
      --cluster <my-cluster> /
      --key-arn arn:aws:kms:<Region-code>:<account>:key/<key> /
      --encrypt-existing-secrets=false
  ```
+ Add encryption to your cluster with a \.yaml file\.

  ```
  # cluster.yaml
  
  apiVersion: eksctl.io/v1alpha5
  kind: ClusterConfig
  
  metadata:
    name: <my-cluster>
    region: <Region-code>
    
  secretsEncryption:
    keyARN: arn:aws:kms:<Region-code>:<account>:key/<key>
  ```

  To automatically re\-encrypt your secrets:

  ```
  eksctl utils enable-secrets-encryption -f kms-cluster.yaml
  ```

  To opt\-out of automatically re\-encrypting your secrets:

  ```
  eksctl utils enable-secrets-encryption -f kms-cluster.yaml --encrypt-existing-secrets=false
  ```

------
#### [ AWS Management Console ]

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the cluster to which you want to add KMS encryption\.

1. Click on the **Configuration** tab\.

1. Scroll down to the **Secrets encryption** section and click on the **Enable** button\.

1. Select a key from the dropdown menu and click the **Enable** button\. If no keys are listed, you must create one first\. For more information, see [Creating keys](https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html)

1. Click the **Confirm** button to use the chosen key\.

------
#### [ AWS CLI  ]

1. Associate envelope encryption configuration with your cluster using the following AWS CLI command\. Replace the *`<example-values>`* \(including *`<>`*\) with your own\.

   ```
   aws eks associate-encryption-config \
       --cluster-name <my-cluster> \
       --encryption-config '[{"resources":["secrets"],"provider":{"keyArn":"arn:aws:kms:<Region-code>:<account>:key/<key>"}}]'
   ```

   **Output**:

   ```
   {
     "update": {
       "id": "<3141b835-8103-423a-8e68-12c2521ffa4d>",
       "status": "InProgress",
       "type": "AssociateEncryptionConfig",
       "params": [
         {
           "type": "EncryptionConfig",
           "value": "[{\"resources\":[\"secrets\"],\"provider\":{\"keyArn\":\"arn:aws:kms:<Region-code>:<account>:key/<key>\"}}]"
         }
       ],
       "createdAt": <1613754188.734>,
       "errors": []
     }
   }
   ```

1. You can monitor the status of your encryption update with the following command\. Use the `cluster name` and `update ID` that was returned in the **Output** of the step above\. Your update is complete when the status is shown as `Successful`\.

   ```
   aws eks describe-update \
       --region <Region-code> \
       --name <my-cluster> \
       --update-id <3141b835-8103-423a-8e68-12c2521ffa4d>
   ```

   **Output**:

   ```
   {
     "update": {
       "id": "<3141b835-8103-423a-8e68-12c2521ffa4d>",
       "status": "Successful",
       "type": "AssociateEncryptionConfig",
       "params": [
         {
           "type": "EncryptionConfig",
           "value": "[{\"resources\":[\"secrets\"],\"provider\":{\"keyArn\":\"arn:aws:kms:<region-code>:<account>:key/<key>\"}}]"
         }
       ],
       "createdAt": <1613754188.734>,
       "errors": []
     }
   }
   ```

1. To verify that encryption is enabled in your cluster, run the `describe-cluster` command\. The response will contain `EncryptionConfig`\. 

   ```
   aws eks describe-cluster --region <Region-code> --name <my-cluster>
   ```

------

After you have enabled encryption on your cluster, you will need to encrypt all existing secrets with the new key:

**Note**  
`eksctl` users do not need to run the following command unless they chose to opt\-out of re\-encrypting their secrets automatically\.

```
kubectl get secrets --all-namespaces -o json | kubectl annotate --overwrite -f - kms-encryption-timestamp="<time value>"
```

**Warning**  
If you enable envelope encryption for an existing cluster and the key that you use is ever deleted, then there is no path to recovery for the cluster\. Deletion of the CMK will permanently put the cluster in a degraded state\.

**Note**  
By default, the `create-key` command creates a [symmetric key](https://docs.aws.amazon.com/kms/latest/developerguide/symmetric-asymmetric.html) with a key policy that gives the account's root user admin access on AWS KMS actions and resources\. If you want to scope down the permissions, make sure that the `kms:DescribeKey` and `kms:CreateGrant` actions are permitted on the key policy for the principal that will be calling the `create-cluster` API\.  
 Amazon EKS does not support the key policy condition `[kms:GrantIsForAWSResource](https://docs.aws.amazon.com/kms/latest/developerguide/policy-conditions.html#conditions-kms-grant-is-for-aws-resource)`\. Creating a cluster will not work if this action is in the key policy statement\.