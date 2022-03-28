# Updating a cluster<a name="update-cluster"></a>

You can update an existing Amazon EKS cluster to a new Kubernetes version or [secrets encyption](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) for your cluster\.

## Updating an Amazon EKS cluster Kubernetes version<a name="update-kubernetes-version"></a>

When a new Kubernetes version is available in Amazon EKS, you can update your Amazon EKS cluster to the latest version\. 

**Important**  
We recommend that before updating to a new Kubernetes version that you review the information in [Amazon EKS Kubernetes versions](kubernetes-versions.md) and in the update steps in this topic\.

New Kubernetes versions have introduced significant changes\. Therefore, we recommend that you test the behavior of your applications against a new Kubernetes version before you update your production clusters\. You can achieve this by building a continuous integration workflow to test your application behavior before moving to a new Kubernetes version\.

The update process consists of Amazon EKS launching new API server nodes with the updated Kubernetes version to replace the existing ones\. Amazon EKS performs standard infrastructure and readiness health checks for network traffic on these new nodes to verify that they're working as expected\. If any of these checks fail, Amazon EKS reverts the infrastructure deployment, and your cluster remains on the prior Kubernetes version\. Running applications aren't affected, and your cluster is never left in a non\-deterministic or unrecoverable state\. Amazon EKS regularly backs up all managed clusters, and mechanisms exist to recover clusters if necessary\. We're constantly evaluating and improving our Kubernetes infrastructure management processes\.

To update the cluster, Amazon EKS requires two to three free IP addresses from the subnets that were provided when you created the cluster\. If these subnets don't have available IP addresses, then the update can fail\. Additionally, if any of the subnets or security groups that were provided during cluster creation have been deleted, the cluster update process can fail\.

**Note**  
Even though Amazon EKS runs a highly available control plane, you might experience minor service interruptions during an update\. For example, if you attempt to connect to an API server just before or just after it's terminated and replaced by a new API server running the new version of Kubernetes, you might experience API call errors or connectivity issues\. If this happens, retry your API operations until they succeed\.

### To update the Kubernetes version for your Amazon EKS cluster<a name="update-existing-cluster"></a>

Update the Kubernetes version for your cluster\.

**To update the Kubernetes version for your cluster**

1. Compare the Kubernetes version of your cluster control plane to the Kubernetes version of your nodes\.
   + Get the Kubernetes version of your cluster control plane with the following command\.

     ```
     kubectl version --short
     ```
   + Get the Kubernetes version of your nodes with the following command\. This command returns all self\-managed and managed Amazon EC2 and Fargate nodes\. Each Fargate pod is listed as its own node\.

     ```
     kubectl get nodes
     ```

   The Kubernetes minor version of the managed and Fargate nodes in your cluster must be the same as the version of your control plane's current version before you update your control plane to a new Kubernetes version\. For example, if your control plane is running version 1\.20 and any of your nodes are running version 1\.19, update your nodes to version 1\.20 before updating your control plane's Kubernetes version to 1\.21\. We also recommend that you update your self\-managed nodes to the same version as your control plane before updating the control plane\. For more information see [Updating a managed node group](update-managed-node-group.md) and [Self\-managed node updates](update-workers.md)\. To update the version of a Fargate node, delete the pod that is represented by the node and redeploy the pod after you update your control plane\.

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
Because Amazon EKS runs a highly available control plane, you can update only one minor version at a time\. See [Kubernetes Version and Version Skew Support Policy](https://kubernetes.io/docs/setup/version-skew-policy/#kube-apiserver) for the rationale behind this requirement\. Therefore, if your current version is 1\.19 and you want to update to 1\.21, then you must first update your cluster to 1\.20 and then update it from 1\.20 to 1\.21\.
Make sure that the `kubelet` on your managed and Fargate nodes are at the same Kubernetes version as your control plane before you update\. We also recommend that your self\-managed nodes are at the same version as the control plane, though they can be up to one version behind the control plane's current version\.

------
#### [ eksctl ]

   This procedure requires `eksctl` version `0.89.0` or later\. You can check your version with the following command:

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

   1. Choose the name of the Amazon EKS cluster to update and choose **Update cluster version**\.

   1. For **Kubernetes version**, select the version to update your cluster to and choose **Update**\.

   1. For **Cluster name**, type the name of your cluster and choose **Confirm**\.

      The update takes several minutes to complete\.

------
#### [ AWS CLI ]

   1. Update your Amazon EKS cluster with the following AWS CLI command\. Replace the *`<example-values>`* \(including *`<>`*\) with your own\.

      ```
      aws eks update-cluster-version \
       --region <region-code> \
       --name <my-cluster> \
       --kubernetes-version <1.21>
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

1. After your cluster update is complete, update your nodes to the same Kubernetes minor version as your updated cluster\. For more information, see [Self\-managed node updates](update-workers.md) or [Updating a managed node group](update-managed-node-group.md)\. Any new pods launched on Fargate will have a `kubelet` version that matches your cluster version\. Existing Fargate pods aren't changed\.

1. \(Optional\) If you deployed the Kubernetes Cluster Autoscaler to your cluster before updating the cluster, update the Cluster Autoscaler to the latest version that matches the Kubernetes major and minor version that you updated to\.

   1. Open the Cluster Autoscaler [releases](https://github.com/kubernetes/autoscaler/releases) page in a web browser and find the latest Cluster Autoscaler version that matches your cluster's Kubernetes major and minor version\. For example, if your cluster's Kubernetes version is 1\.21 find the latest Cluster Autoscaler release that begins with 1\.21\. Record the semantic version number \(`<1.21.n>`\) for that release to use in the next step\.

   1. Set the Cluster Autoscaler image tag to the version that you recorded in the previous step with the following command\. If necessary, replace *1\.21*\.*n* with your own value\.

      ```
      kubectl -n kube-system set image deployment.apps/cluster-autoscaler cluster-autoscaler=k8s.gcr.io/autoscaling/cluster-autoscaler:v1.21.n
      ```

1. \(Clusters with GPU nodes only\) If your cluster has node groups with GPU support \(for example, `p3.2xlarge`\), you must update the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) DaemonSet on your cluster with the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.9.0/nvidia-device-plugin.yml
   ```

1. Update the VPC CNI, CoreDNS, and `kube-proxy` add\-ons\.
   + If you updated your cluster to 1\.17 or earlier, then see [Updating the Amazon VPC CNI self\-managed add\-on](managing-vpc-cni.md#updating-vpc-cni-add-on), [Updating the CoreDNS self\-managed add\-on](managing-coredns.md#updating-coredns-add-on), and [Updating the `kube-proxy` self\-managed add\-on](managing-kube-proxy.md#updating-kube-proxy-add-on) to update your Amazon VPC CNI, CoreDNS, and `kube-proxy` add\-ons\.
   + If you updated your cluster to 1\.18, you can add Amazon EKS add\-ons\. For more information see [Adding the Amazon VPC CNI Amazon EKS add\-on](managing-vpc-cni.md#adding-vpc-cni-eks-add-on), [Adding the CoreDNS Amazon EKS add\-on](managing-coredns.md#adding-coredns-eks-add-on), or [Adding the `kube-proxy` Amazon EKS add\-on](managing-kube-proxy.md#adding-kube-proxy-eks-add-on)\. To learn more about Amazon EKS add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\.
   + If you updated to 1\.19 or later and are using Amazon EKS add\-ons, in the Amazon EKS console, select **Clusters**, then select the name of the cluster that you updated in the left navigation pane\. Notifications appear in the console informing you that a new version is available for each addon that has an available update\. To update an add\-on, select the **Configuration** tab, then select the **Add\-ons** tab\. In one of the boxes for an add\-on that has an update available, select **Update now**, select an available version, and then select **Update**\.
   + Alternately, you can use the AWS CLI or `eksctl` to update the [Amazon VPC CNI](managing-vpc-cni.md#updating-vpc-cni-add-on), [CoreDNS](managing-coredns.md#updating-coredns-eks-add-on), and [`kube-proxy`](managing-kube-proxy.md#updating-kube-proxy-eks-add-on) Amazon EKS add\-ons\.

## Enabling secret encryption on an existing cluster<a name="enable-kms"></a>

If you enable [secrets encyption](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/), the Kubernetes secrets are encrypted using the AWS KMS key that you select\. The KMS key must be:
+ Symmetric
+ Able to encrypt and decrypt data
+ Created in the same region as the cluster
+ If the KMS key was created in a different account, the user must have access to the KMS key\.

For more information, see [Allowing users in other accounts to use a KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html) in the *[AWS Key Management Service Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/)*\.

**Warning**  
You cannot disable secrets encryption after enabling it\. This action is irreversible\.

------
#### [ eksctl  ]

You can enable encryption in two ways:
+ Add encryption to your cluster with a single command\.

  To automatically re\-encrypt your secrets:

  ```
  eksctl utils enable-secrets-encryption \
      --cluster <my-cluster> \
      --key-arn arn:aws:kms:<Region-code>:<account>:key/<key>
  ```

  To opt\-out of automatically re\-encrypting your secrets:

  ```
  eksctl utils enable-secrets-encryption 
      --cluster <my-cluster> \
      --key-arn arn:aws:kms:<Region-code>:<account>:key/<key> \
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

1. Choose the **Configuration** tab\.

1. Scroll down to the **Secrets encryption** section and choose **Enable**\.

1. Select a key from the dropdown list and choose the **Enable** button\. If no keys are listed, you must create one first\. For more information, see [Creating keys](https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html)

1. Choose the **Confirm** button to use the chosen key\.

------
#### [ AWS CLI ]

1. Associate [secrets encryption](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) configuration with your cluster using the following AWS CLI command\. Replace the *`<example-values>`* \(including *`<>`*\) with your own\.

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
If you're using `eksctl`, you don't need to run the following command unless you chose to opt\-out of re\-encrypting your secrets automatically\.

```
kubectl get secrets --all-namespaces -o json | kubectl annotate --overwrite -f - kms-encryption-timestamp="<time value>"
```

**Warning**  
If you enable [secrets encyption](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) for an existing cluster and the KMS key that you use is ever deleted, then there is no path to recovery for the cluster\. Deletion of the KMS key will permanently put the cluster in a degraded state\. For more information, see [Deleting AWS KMS keys](https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html)\.

**Note**  
By default, the `create-key` command creates a [symmetric key](https://docs.aws.amazon.com/kms/latest/developerguide/symmetric-asymmetric.html) with a key policy that gives the account root admin access on AWS KMS actions and resources\. If you want to scope down the permissions, make sure that the `kms:DescribeKey` and `kms:CreateGrant` actions are permitted on the policy for the principal that will be calling the `create-cluster` API\.  
 Amazon EKS does not support the policy condition `[kms:GrantIsForAWSResource](https://docs.aws.amazon.com/kms/latest/developerguide/policy-conditions.html#conditions-kms-grant-is-for-aws-resource)`\. Creating a cluster will not work if this action is in the KMS key policy statement\.