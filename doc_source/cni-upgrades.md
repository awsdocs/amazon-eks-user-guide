# Amazon VPC CNI plugin for Kubernetes upgrades<a name="cni-upgrades"></a>

When you launch an Amazon EKS cluster, a recent version of the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) is deployed to your cluster\. The absolute latest version of the plugin is available on [GitHub](https://github.com/aws/amazon-vpc-cni-k8s/releases) for a short grace period before new clusters are switched over to use it\. Amazon EKS does not automatically upgrade the CNI plugin on your cluster when new versions are released\. To get a newer version of the CNI plugin on existing clusters, you must manually upgrade the plugin\.

We recommend that latest 1\.7 patch version\. You can view the [latest patch version](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/config/v1.7/aws-k8s-cni.yaml#L156), view the different releases available for the plugin, and read the release notes for each version on [GitHub](https://github.com/aws/amazon-vpc-cni-k8s/releases)\. With version 1\.7\.0 and later, the `privileged` container capability was removed from the CNI pod \(`aws-node`\)\. The pod has the `NET_ADMIN` capability in its `securityContext` `capabilities`, which is required for the `aws-node` container to add `iptables`, routes, and rules to setup pod networking\. An `init` container was also added to the `aws-node` pod, which has the `privileged` capability, so that it can setup reverse path filters and copy loopback plugins during `aws-node` pod start up\. 

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

  In this example output, the CNI version is 1\.6\.3, which is earlier than the latest patch for version 1\.7\. Use the following procedure to upgrade the CNI\.

**To upgrade the Amazon VPC CNI plugin for Kubernetes**
+ If your CNI version is earlier than 1\.7\.5, and you are managing the plugin yourself, then use the appropriate command below to update your CNI version to the latest recommended version\. If your cluster is running Kubernetes `1.18` or later with `eks.3` platform version or later, and the plugin is managed by Amazon EKS, then to update the plugin, see [Configure an Amazon EKS add\-on](update-cluster.md#update-cluster-add-ons)\.

**Important**  
When applying the new manifest file, some of the custom settings might be overwritten\. For an example, environment variable AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG is reset to false and might cause undesirable behavior leading to application downtime as Pods get assigned to default subnets\. The roadmap for CNI include items to make this process easier and seamless. Meanwhile, consider custom upgrade scenarios if you have CNI custom networking in place\. 

Also, check [Configure an Amazon EKS add\-on](update-cluster.md#update-cluster-add-ons) for configuring VPC CNI. The VPC CNI add-on reduces the amount of work you need to do handle the upgraes when custom networking settings are involved.

  + US West \(Oregon\) \(`us-west-2`\)

    ```
    kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.7/config/v1.7/aws-k8s-cni.yaml
    ```
  + China \(Beijing\) \(`cn-north-1`\) or China \(Ningxia\) \(`cn-northwest-1`\)

    ```
    kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.7/config/v1.7/aws-k8s-cni-cn.yaml
    ```
  + AWS GovCloud \(US\-East\) \(`us-gov-east-1`\)

    ```
    kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.7/config/v1.7/aws-k8s-cni-us-gov-east-1.yaml
    ```
  + AWS GovCloud \(US\-West\) \(`us-gov-west-1`\)

    ```
    kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.7/config/v1.7/aws-k8s-cni-us-gov-west-1.yaml
    ```
  + For all other Regions
    + Download the manifest file\.

      ```
      curl -o aws-k8s-cni.yaml https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.7/config/v1.7/aws-k8s-cni.yaml
      ```
    + If necessary, replace `<region-code>` in the following command with the Region that your cluster is in and then run the modified command to replace the Region code in the file \(currently `us-west-2`\)\.

      ```
      sed -i.bak -e 's/us-west-2/<region-code>/' aws-k8s-cni.yaml
      ```
    + Apply the manifest file to your cluster\.

      ```
      kubectl apply -f aws-k8s-cni.yaml
      ```
**Custom upgrade scenarios when CNI custom networking in place**

The upgrade is not always a straight forward process when custom networking is in place\. Applying a manifest might override the custom resources and environment variables which might be added as part of CNI custom configurations\. The best practice is to consider backuping up existing resource manifests, analyzing the changes, and updating resources carefully to minimize undesirable application downtime\. 

Please make sure to check [release notes](
https://github.com/aws/amazon-vpc-cni-k8s/releases) to understand the scope of change. Some upgrades might mandate to apply the entire manifest or atleast the newly introduced dependencies.

The below steps work best when only an image change is required.

***Backup***
  + Take a backup of current CNI daemonset\.

    ```
    kubectl get daemonset aws-node -n kube-system -o yaml > aws-k8s-cni-old.yaml
    ```
  + Download the manifest file\.

    ```
    curl -o aws-k8s-cni.yaml https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/v1.7.5/config/v1.7/aws-k8s-cni.yaml
    ``` 
  + Compare the ENV differences, image version changes\.

All of the below methods achieve the same result, chose one method only to upgrade CNI image.

***Inplace update***
  + Inplace edit
    + Edit manifest\.
      ```
      kubectl edit daemonset aws-node -n kube-system 
      ```
    + Change the container image version and save\.
    + Wait for daemonset to be available, ready, available, up-to-date count to match desired count
      ```
      kubectl get daemonset aws-node -n kube-system -o wide
      ```
    + View the patched daemonset to confirm changes\.
      ```
      kubectl get daemonset aws-node -n kube-system -o yaml
      ``` 
  + Patch
    + Create a patch file carefully based on the change identified\.
      ```
      cat <<EoF > ~/patch-file.yaml
      spec:
      template:
        spec:
          containers:
          - name: aws-node
            image: 602401143452.dkr.ecr.us-west-2.amazonaws.com/amazon-k8s-cni:v1.7.5
      EoF
      ``` 
    + Apply the patch\.
      ```
      kubectl patch daemonset/aws-node -n kube-system -p "$(cat patch-file.yaml)"
      ```
    + View the patched daemonset to confirm changes\.
      ```
      kubectl get daemonset aws-node -n kube-system -o yaml
      ```

***Helm***

Use Helm upgrade method if you had installed CNI via Helm install. Helm upgrade is tested to preserve the custom settings. 
  + Apply helm upgrade\.
    ```
    helm upgrade aws-vpc-cni --namespace kube-system eks/aws-vpc-cni --values values.yaml --set image.tag=v1.7.5
    ```
  + Wait for daemonset to be available, ready, available, up-to-date count to match desired count\.
    ```
    kubectl get daemonset aws-node -n kube-system -o wide
    ```
  + View the daemonset to confirm changes\.
    ```
    kubectl get daemonset aws-node -n kube-system -o yaml
    ```
