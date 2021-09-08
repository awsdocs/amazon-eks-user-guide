# Deregister a cluster<a name="deregister-connected-cluster"></a>


|  | 
| --- |
| The Amazon EKS Connector in preview release for Amazon EKS and is subject to change\. | 

If you are finished using a connected cluster, you can deregister it\. Once deregistered, the cluster will no longer be visible in the Amazon EKS console\.

**To deregister a connected cluster \(AWS CLI\)**
+ Deregister the connected cluster\.

  ```
  aws eks deregister-cluster \
       --name "my-first-registered-cluster" \
       --region AWS_REGION
  ```

**To deregister a connected cluster \(AWS Management Console\)**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose **Clusters**\.

1. On the **Clusters** page, select the connected cluster and select **Deregister**\.

1. Confirm that you want to deregister the cluster\.

**To clean up the resources on your Kubernetes cluster**

1. Delete the Amazon EKS Connector YAML file from your Kubernetes cluster\.

   ```
   kubectl delete -f eks-connector.yaml
   ```

1. If you created a `clusterrole` or `clusterrolebinding` to provide additional IAM user accesss to the cluster, ensure that you delete them from your Kubernetes cluster as well\.