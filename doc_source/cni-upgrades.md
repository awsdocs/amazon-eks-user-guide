# Amazon VPC CNI plugin for Kubernetes upgrades<a name="cni-upgrades"></a>

When you launch an Amazon EKS cluster, a recent version of the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) is deployed to your cluster\. The absolute latest version of the plugin is available on [GitHub](https://github.com/aws/amazon-vpc-cni-k8s/releases) for a short grace period before new clusters are switched over to use it\. Amazon EKS does not automatically upgrade the CNI plugin on your cluster when new versions are released\. To get a newer version of the CNI plugin on existing clusters, you must manually upgrade the plugin\.

The latest version that we recommend is version 1\.7\.5\. You can view the different releases available for the plugin, and read the release notes for each version on [GitHub](https://github.com/aws/amazon-vpc-cni-k8s/releases)\. With version 1\.7\.0 and later, the `privileged` container capability was removed from the CNI pod \(`aws-node`\)\. The pod has the `NET_ADMIN` capability in its `securityContext` `capabilities`, which is required for the `aws-node` container to add `iptables`, routes, and rules to setup pod networking\. An `init` container was also added to the `aws-node` pod, which has the `privileged` capability, so that it can setup reverse path filters and copy loopback plugins during `aws-node` pod start up\. 

**Important**  
If you have assigned a custom pod security policy to the `aws-node` Kubernetes service account used for the `aws-node` pod, then the policy must have `NET_ADMIN` in its `allowedCapabilities` section along with `hostNetwork: true` and `privileged: true` in the policy's `spec`\. For more information, see [Pod security policy](pod-security-policy.md)\.

Use the following procedures to check your CNI plugin version and upgrade to the latest recommended version\.

**To check your Amazon VPC CNI plugin for Kubernetes version**
+ Use the following command to print your cluster's CNI version:

  ```
  kubectl describe daemonset aws-node --namespace kube-system | grep Image | cut -d "/" -f 2
  ```

  Output:

  ```
  amazon-k8s-cni:1.6.3
  ```

  In this example output, the CNI version is 1\.6\.3, which is earlier than the current recommended version, 1\.7\.5\. Use the following procedure to upgrade the CNI\.

**To upgrade the Amazon VPC CNI plugin for Kubernetes**
+ If your CNI version is earlier than 1\.7\.5, and you are managing the plugin yourself, then use the appropriate command below to update your CNI version to the latest recommended version\. If your cluster is running Kubernetes `1.18` or later with `eks.3` platform version or later, and the plugin is managed by Amazon EKS, then to update the plugin, see [Configure an Amazon EKS add\-on](update-cluster.md#update-cluster-add-ons)\.
**Important**  
Any changes you've made to the plugin's default settings on your cluster can be overwritten with default settings when applying the new version of the manifest\. To prevent loss of your custom settings, download the manifest, change the default settings as necessary, and then apply the modified manifest to your cluster\. 
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
    + If necessary, replace `<region-code>` in the following command with the Region that your cluster is in and then run the modified command to replace the Region code in the file \(currently `us-west-2`\)\.

      ```
      sed -i.bak -e 's/us-west-2/<region-code>/' aws-k8s-cni.yaml
      ```
    + Apply the manifest file to your cluster\.

      ```
      kubectl apply -f aws-k8s-cni.yaml
      ```