# Updating a cluster<a name="update-cluster"></a>

You can update an existing Amazon EKS cluster to a new Kubernetes version or [secrets encryption](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) for your cluster\.

## Updating an Amazon EKS cluster Kubernetes version<a name="update-kubernetes-version"></a>

When a new Kubernetes version is available in Amazon EKS, you can update your Amazon EKS cluster to the latest version\. 

**Important**  
We recommend that, before you update to a new Kubernetes version, you review the information in [Amazon EKS Kubernetes versions](kubernetes-versions.md) and also review in the update steps in this topic\.

New Kubernetes versions have introduced significant changes\. Therefore, we recommend that you test the behavior of your applications against a new Kubernetes version before you update your production clusters\. You can do this by building a continuous integration workflow to test your application behavior before moving to a new Kubernetes version\.

The update process consists of Amazon EKS launching new API server nodes with the updated Kubernetes version to replace the existing ones\. Amazon EKS performs standard infrastructure and readiness health checks for network traffic on these new nodes to verify that they're working as expected\. If any of these checks fail, Amazon EKS reverts the infrastructure deployment, and your cluster remains on the prior Kubernetes version\. Running applications aren't affected, and your cluster is never left in a non\-deterministic or unrecoverable state\. Amazon EKS regularly backs up all managed clusters, and mechanisms exist to recover clusters if necessary\. We're constantly evaluating and improving our Kubernetes infrastructure management processes\.

To update the cluster, Amazon EKS requires up to five free IP addresses from the subnets that were provided when you created the cluster\. If these subnets don't have available IP addresses, then the update can fail\. Additionally, if any of the subnets or security groups that were provided when the cluster was created are deleted, the cluster update process might fail\.

**Note**  
Even though Amazon EKS runs a highly available control plane, you might experience minor service interruptions during an update\. For example, assume that you attempt to connect to an API server around when it's terminated and replaced by a new API server that's running the new version of Kubernetes\. You might experience API call errors or connectivity issues\. If this happens, retry your API operations until they succeed\.

## Kubernetes version 1\.22 prerequisites<a name="update-1.22"></a>

A number of deprecated beta APIs \(v1beta1\) have been removed in version 1\.22 in favor of the GA \(v1\) version of those same APIs\. As noted in the Kubernetes 1\.22 [API and Feature removal blog](https://blog.k8s.io/2021/07/14/upcoming-changes-in-kubernetes-1-22) and deprecated [API migration guide](https://kubernetes.io/docs/reference/using-api/deprecation-guide/#v1-22), API changes are required for the following deployed resources before updating a cluster to v1\.22\.

Before updating to 1\.22, make sure to do the following:
+ Change your YAML manifest files and clients to reference the new APIs\.
+ Update custom integrations and controllers to call the new APIs\.
+ Make sure that you use an updated version of any third\-party tools\. These tools include ingress controllers, service mesh controllers, continuous delivery systems, and other tools that call the new APIs\. To check for discontinued API usage in your cluster, enable [audit control plane logging](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html) and specify `v1beta` as an event filter\. Replacement APIs are available in Kubernetes for several versions\. 
+ If applicable, update load balance controller to v2\.4\.1 before updating to v1\.22\.

**Important**  
If you update the clusters to version 1\.22, existing persisted objects can be accessed using the new APIs \. However, you must migrate manifests and update clients to use these new APIs\. Updating the clusters prevents potential workload failures\.

The v1\.22 release removes support from the following Beta APIs\. Migrate your manifests and API clients with regard to the following information\.


| Resource | Beta version | GA version | Notes | 
| --- | --- | --- | --- | 
| ValidatingWebhookConfiguration MutatingWebhookConfiguration | admissionregistration\.k8s\.io/v1beta1 | admissionregistration\.k8s\.io/v1 |  [\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html)  | 
| CustomResourceDefinition | apiextensions\.k8s\.io/v1beta1 | apiextensions\.k8s\.io/v1 |  [\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html)  | 
| APIService | apiregistration\.k8s\.io/v1beta1 | apiregistration\.k8s\.io/v1 | None | 
| TokenReview | authentication\.k8s\.io/v1beta1 | authentication\.k8s\.io/v1 | None | 
| SubjectAccessReview LocalSubjectAccessReview SelfSubjectAccessReview | authorization\.k8s\.io/v1beta1 | authorization\.k8s\.io/v1 | spec\.group is renamed to spec\.groups | 
| CertificateSigningRequest | certificates\.k8s\.io/v1beta1 | certificates\.k8s\.io/v1 |  [\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html)  | 
|  Lease  | coordination\.k8s\.io/v1beta1 | coordination\.k8s\.io/v1 | None | 
|  Ingress   |  [\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html)  | networking\.k8s\.io/v1 |  [\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html)  | 
|  IngressClass   | networking\.k8s\.io/v1beta1 | networking\.k8s\.io/v1 | None | 
|  RBAC  | rbac\.authorization\.k8s\.io/v1beta1 | rbac\.authorization\.k8s\.io/v1 | None | 
| PriorityClass | scheduling\.k8s\.io/v1beta1 | scheduling\.k8s\.io/v1 | None | 
| CSIDriver CSINode StorageClass VolumeAttachment | storage\.k8s\.io/v1beta1 | storage\.k8s\.io/v1 | None | 

To learn more about the API removal, see the [Deprecated API migration guide](https://kubernetes.io/docs/reference/using-api/deprecation-guide/#v1-22)\.

## To update the Kubernetes version for your Amazon EKS cluster<a name="update-existing-cluster"></a>

Update the Kubernetes version for your cluster\.

**To update the Kubernetes version for your cluster**

1. Compare the Kubernetes version of your cluster control plane to the Kubernetes version of your nodes\.
   + Get the Kubernetes version of your cluster control plane with the **kubectl version \-\-short** command\.

     ```
     kubectl version --short
     ```
   + Get the Kubernetes version of your nodes with the **kubectl get nodes** command\. This command returns all self\-managed and managed Amazon EC2 and Fargate nodes\. Each Fargate pod is listed as its own node\.

     ```
     kubectl get nodes
     ```

   Before updating your control plane to a new Kubernetes version, make sure that the Kubernetes minor version of both the managed nodes and Fargate nodes in your cluster are the same as your control plane's version\. For example, if your control plane is running version 1\.21 and one of your nodes is running version 1\.20, you must update your nodes to version 1\.21\. We also recommend that you update your self\-managed nodes to the same version as your control plane before updating the control plane\. For more information, see [Updating a managed node group](update-managed-node-group.md) and [Self\-managed node updates](update-workers.md)\. To update the version of a Fargate node, delete the pod that's represented by the node\. Then, redeploy the pod after you update your control plane\.

1. By default, the pod security policy admission controller is enabled on Amazon EKS clusters\. Before updating your cluster, ensure that the proper pod security policies are in place\. This is to avoid potential security issues\. You can check for the default policy with the **kubectl get psp eks\.privileged** command\.

   ```
   kubectl get psp eks.privileged
   ```

   If you receive the following error, see [default pod security policy](pod-security-policy.md#default-psp) before proceeding\.

   ```
   Error from server (NotFound): podsecuritypolicies.extensions "eks.privileged" not found
   ```

1. If you originally deployed your cluster on Kubernetes `1.17` or earlier, you might need to remove a discontinued term from your CoreDNS manifest\.

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
Because Amazon EKS runs a highly available control plane, you can update only one minor version at a time\. For more information about this requirement, see [Kubernetes Version and Version Skew Support Policy](https://kubernetes.io/docs/setup/version-skew-policy/#kube-apiserver)\. Assume that your current version is 1\.20 and you want to update to 1\.22\. Then, you must first update your cluster to 1\.21 and then later update it from 1\.21 to 1\.22\.
Make sure that the `kubelet` on your managed and Fargate nodes are at the same Kubernetes version as your control plane before you update\. We recommend that your self\-managed nodes are at the same version as the control plane\. They can be only up to one version behind the current version of the control plane\.
If your cluster is configured with a version of the Amazon VPC CNI plugin that is earlier than 1\.8\.0, then we recommend that you update the plugin to version 1\.10\.1 before updating your cluster to version 1\.21 or later\. For more information, see [Updating the Amazon VPC CNI Amazon EKS add\-on](managing-vpc-cni.md#updating-vpc-cni-eks-add-on) or [Updating the Amazon VPC CNI self\-managed add\-on](managing-vpc-cni.md#updating-vpc-cni-add-on)\.

------
#### [ eksctl ]

   This procedure requires `eksctl` version `0.93.0` or later\. You can check your version with the following command:

   ```
   eksctl version
   ```

   For instructions on how to install and update `eksctl`, see [Installing or upgrading `eksctl`](eksctl.md#installing-eksctl)\.

   Update the Kubernetes version of your Amazon EKS control plane to one minor version later than its current version with the following command\. Replace *`<my-cluster>`* \(including *`<>`*\) with your cluster name\.

   ```
   eksctl upgrade cluster --name <my-cluster> --approve
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

   1. Update your Amazon EKS cluster with the following AWS CLI command\. Replace the *`example-values`* with your own\.

      ```
      aws eks update-cluster-version \
       --region <region-code> \
       --name <my-cluster> \
       --kubernetes-version <1.21>
      ```

      The output is as follows\.

      ```
      {
          "update": {
              "id": "b5f0ba18-9a87-4450-b5a0-825e6e84496f",
              "status": "InProgress",
              "type": "VersionUpdate",
              "params": [
                  {
                      "type": "Version",
                      "value": "1.21"
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
      aws eks describe-update \
        --region <region-code> \
        --name <my-cluster> \
        --update-id <b5f0ba18-9a87-4450-b5a0-825e6e84496f>
      ```

      The output is as follows\.

      ```
      {
          "update": {
              "id": "b5f0ba18-9a87-4450-b5a0-825e6e84496f",
              "status": "Successful",
              "type": "VersionUpdate",
              "params": [
                  {
                      "type": "Version",
                      "value": "1.21"
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

   1. Open the Cluster Autoscaler [releases](https://github.com/kubernetes/autoscaler/releases) page in a web browser and find the latest Cluster Autoscaler version that matches your cluster's Kubernetes major and minor version\. For example, if your cluster's Kubernetes version is 1\.22 find the latest Cluster Autoscaler release that begins with 1\.22\. Record the semantic version number \(`<1.22.n>`\) for that release to use in the next step\.

   1. Set the Cluster Autoscaler image tag to the version that you recorded in the previous step with the following command\. If necessary, replace *1\.22*\.*n* with your own value\.

      ```
      kubectl -n kube-system set image deployment.apps/cluster-autoscaler cluster-autoscaler=k8s.gcr.io/autoscaling/cluster-autoscaler:v1.22.n
      ```

1. \(Clusters with GPU nodes only\) If your cluster has node groups with GPU support \(for example, `p3.2xlarge`\), you must update the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) DaemonSet on your cluster with the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.9.0/nvidia-device-plugin.yml
   ```

1. Update the VPC CNI, CoreDNS, and `kube-proxy` add\-ons\.
   + If you updated your cluster to version 1\.17 or earlier, refer to the instructions in [Updating the Amazon VPC CNI self\-managed add\-on](managing-vpc-cni.md#updating-vpc-cni-add-on), [Updating the CoreDNS self\-managed add\-on](managing-coredns.md#updating-coredns-add-on), and [Updating the `kube-proxy` self\-managed add\-on](managing-kube-proxy.md#updating-kube-proxy-add-on) to update your Amazon VPC CNI, CoreDNS, and `kube-proxy` add\-ons\.
   + If you updated your cluster to version 1\.18, you can add Amazon EKS add\-ons\. For instructions, see [Adding the Amazon VPC CNI Amazon EKS add\-on](managing-vpc-cni.md#adding-vpc-cni-eks-add-on), [Adding the CoreDNS Amazon EKS add\-on](managing-coredns.md#adding-coredns-eks-add-on), and [Adding the `kube-proxy` Amazon EKS add\-on](managing-kube-proxy.md#adding-kube-proxy-eks-add-on)\. To learn more about Amazon EKS add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\.
   + If you updated to version 1\.19 or later and are using Amazon EKS add\-ons, in the Amazon EKS console, select **Clusters**, then select the name of the cluster that you updated in the left navigation pane\. Notifications appear in the console\. They inform you that a new version is available for each addon that has an available update\. To update an add\-on, select the **Configuration** tab, and then select the **Add\-ons** tab\. In one of the boxes for an add\-on that has an update available, select **Update now**, select an available version, and then select **Update**\.
   + Alternately, you can use the AWS CLI or `eksctl` to update the [Amazon VPC CNI](managing-vpc-cni.md#updating-vpc-cni-add-on), [CoreDNS](managing-coredns.md#updating-coredns-eks-add-on), and [`kube-proxy`](managing-kube-proxy.md#updating-kube-proxy-eks-add-on) Amazon EKS add\-ons\.

## Enabling secret encryption on an existing cluster<a name="enable-kms"></a>

If you enable [secrets encryption](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/), the Kubernetes secrets are encrypted using the AWS KMS key that you select\. The KMS key must meet the following conditions:
+ Symmetric
+ Can encrypt and decrypt data
+ Created in the same AWS Region as the cluster
+ If the KMS key was created in a different account, the user must have access to the KMS key\.

For more information, see [Allowing users in other accounts to use a KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html) in the *[AWS Key Management Service Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/)*\.

**Warning**  
You can't disable secrets encryption after enabling it\. This action is irreversible\.

------
#### [ eksctl  ]

You can enable encryption in two ways:
+ Add encryption to your cluster with a single command\.

  To automatically re\-encrypt your secrets, run the following command\.

  ```
  eksctl utils enable-secrets-encryption \
  
      --cluster <my-cluster> \
      --key-arn arn:aws:kms:<Region-code>:<account>:key/<key>
  ```

  To opt\-out of automatically re\-encrypting your secrets, run the following command\.

  ```
  eksctl utils enable-secrets-encryption 
      --cluster my-cluster \
      --key-arn arn:aws:kms:region-code:account:key/key \
      --encrypt-existing-secrets=false
  ```
+ Add encryption to your cluster with a `.yaml` file\.

  ```
  # cluster.yaml
  
  apiVersion: eksctl.io/v1alpha5
  kind: ClusterConfig
  
  metadata:
    name: my-cluster
    region: region-code
    
  secretsEncryption:
    keyARN: arn:aws:kms:<Region-code>:<account>:key/<key>
  ```

  To have your secrets re\-encrypt automatically, run the following command\.

  ```
  eksctl utils enable-secrets-encryption -f kms-cluster.yaml
  ```

  To opt out of automatically re\-encrypting your secrets, run the following command\.

  ```
  eksctl utils enable-secrets-encryption -f kms-cluster.yaml --encrypt-existing-secrets=false
  ```

------
#### [ AWS Management Console ]

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the cluster that you want to add KMS encryption to\.

1. Choose the **Configuration** tab\.

1. Scroll down to the **Secrets encryption** section and choose **Enable**\.

1. Select a key from the dropdown list and choose the **Enable** button\. If no keys are listed, you must create one first\. For more information, see [Creating keys](https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html)

1. Choose the **Confirm** button to use the chosen key\.

------
#### [ AWS CLI ]

1. Associate the [secrets encryption](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) configuration with your cluster using the following AWS CLI command\. Replace the *`example-values`* with your own\.

   ```
   aws eks associate-encryption-config \
       --cluster-name <my-cluster> \
       --encryption-config '[{"resources":["secrets"],"provider":{"keyArn":"arn:aws:kms:<Region-code>:<account>:key/<key>"}}]'
   ```

   The output is as follows\.

   ```
   {
     "update": {
       "id": "3141b835-8103-423a-8e68-12c2521ffa4d",
       "status": "InProgress",
       "type": "AssociateEncryptionConfig",
       "params": [
         {
           "type": "EncryptionConfig",
           "value": "[{\"resources\":[\"secrets\"],\"provider\":{\"keyArn\":\"arn:aws:kms:region-code:account:key/key\"}}]"
         }
       ],
       "createdAt": 1613754188.734,
       "errors": []
     }
   }
   ```

1. You can monitor the status of your encryption update with the following command\. Use the specific `cluster name` and `update ID` that was returned in the previous output\. When a `Successful` status is displayed, the update is complete\.

   ```
   aws eks describe-update \
       --region <Region-code> \
       --name <my-cluster> \
       --update-id <3141b835-8103-423a-8e68-12c2521ffa4d>
   ```

   The output is as follows\.

   ```
   {
     "update": {
       "id": "3141b835-8103-423a-8e68-12c2521ffa4d",
       "status": "Successful",
       "type": "AssociateEncryptionConfig",
       "params": [
         {
           "type": "EncryptionConfig",
           "value": "[{\"resources\":[\"secrets\"],\"provider\":{\"keyArn\":\"arn:aws:kms:region-code:account:key/key\"}}]"
         }
       ],
       "createdAt": 1613754188.734>,
       "errors": []
     }
   }
   ```

1. To verify that encryption is enabled in your cluster, run the `describe-cluster` command\. The response contains an `EncryptionConfig` string\. 

   ```
   aws eks describe-cluster --region <Region-code> --name <my-cluster>
   ```

------

After you enabled encryption on your cluster, you must encrypt all existing secrets with the new key:

**Note**  
If you use `eksctl`, running the following command is necessary only if you opt out of re\-encrypting your secrets automatically\.

```
kubectl get secrets --all-namespaces -o json | kubectl annotate --overwrite -f - kms-encryption-timestamp="time value"
```

**Warning**  
If you enable [secrets encryption](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) for an existing cluster and the KMS key that you use is ever deleted, then there's no way to recovery the cluster\. If you delete the KMS key, you permanently put the cluster in a degraded state\. For more information, see [Deleting AWS KMS keys](https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html)\.

**Note**  
By default, the `create-key` command creates a [symmetric key](https://docs.aws.amazon.com/kms/latest/developerguide/symmetric-asymmetric.html) with a key policy\. This key policy gives the account root admin access on AWS KMS actions and resources\. Assume that you want to scope down the permissions\. Make sure that the `kms:DescribeKey` and `kms:CreateGrant` actions are permitted on the policy for the principal that calls the `create-cluster` API\.  
 Amazon EKS doesn't support the policy condition `[kms:GrantIsForAWSResource](https://docs.aws.amazon.com/kms/latest/developerguide/policy-conditions.html#conditions-kms-grant-is-for-aws-resource)`\. If this action is in the KMS key policy statement, creating a cluster doesn't work\.