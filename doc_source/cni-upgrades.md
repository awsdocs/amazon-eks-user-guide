# Amazon VPC CNI plugin for Kubernetes upgrades<a name="cni-upgrades"></a>

When you launch an Amazon EKS cluster, we apply a recent version of the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) to your cluster\. The absolute latest version of the plugin is available on [GitHub](https://github.com/aws/amazon-vpc-cni-k8s/releases) for a short grace period before new clusters are switched over to use it\. Amazon EKS does not automatically upgrade the CNI plugin on your cluster when new versions are released\. To get a newer version of the CNI plugin on existing clusters, you must manually upgrade the plugin\.

The latest version that we recommend  is version 1\.6\.3\. You can view the different releases available for the plugin, and read the release notes for each version [on GitHub](https://github.com/aws/amazon-vpc-cni-k8s/releases)\.

Use the following procedures to check your CNI plugin version and upgrade to the latest recommended version\.

**To check your Amazon VPC CNI plugin for Kubernetes version**
+ Use the following command to print your cluster's CNI version:

  ```
  kubectl describe daemonset aws-node --namespace kube-system | grep Image | cut -d "/" -f 2
  ```

  Output:

  ```
  amazon-k8s-cni:1.6.2
  ```

  In this example output, the CNI version is 1\.6\.2, which is earlier than the current recommended version, 1\.6\.3\. Use the following procedure to upgrade the CNI\.

**To upgrade the Amazon VPC CNI plugin for Kubernetes**
+ If your CNI version is earlier than 1\.6\.3, then use the appropriate command below to update your CNI version to the latest recommended version:
  + US West \(Oregon\) \(`us-west-2`\)

    ```
    kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.6/config/v1.6/aws-k8s-cni.yaml
    ```
  + China \(Beijing\) \(`cn-north-1`\) or China \(Ningxia\) \(`cn-northwest-1`\)

    ```
    kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.6/config/v1.6/aws-k8s-cni-cn.yaml
    ```
  + AWS GovCloud \(US\-East\) \(`us-gov-east-1`\)

    ```
    kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.6/config/v1.6/aws-k8s-cni-us-gov-east-1.yaml
    ```
  + AWS GovCloud \(US\-West\) \(`us-gov-west-1`\)

    ```
    kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.6/config/v1.6/aws-k8s-cni-us-gov-west-1.yaml
    ```
  + For all other Regions
    + Download the manifest file\.

      ```
      curl -o aws-k8s-cni.yaml https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.6/config/v1.6/aws-k8s-cni.yaml
      ```
    + Replace `<region-code>` in the following command with the Region that your cluster is in and then run the modified command to replace the Region code in the file \(currently `us-west-2`\)\.

      ```
      sed -i -e 's/us-west-2/<region-code>/' aws-k8s-cni.yaml
      ```
    + Apply the manifest file to your cluster\.

      ```
      kubectl apply -f aws-k8s-cni.yaml
      ```