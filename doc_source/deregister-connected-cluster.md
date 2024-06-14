--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Deregistering a cluster<a name="deregister-connected-cluster"></a>

If you are finished using a connected cluster, you can deregister it\. After it’s deregistered, the cluster is no longer visible in the Amazon EKS console\.

You must have the following permissions to call the deregisterCluster API:
+  `eks:DeregisterCluster` 
+  `ssm:DeleteActivation` 
+  `ssm:DeregisterManagedInstance` 

This process involves two steps: Deregistering the cluster with Amazon EKS and uninstalling the eks\-connector agent in the cluster\.

## To deregister the Kubernetes cluster<a name="deregister-connected-cluster-eks"></a>

 AWS CLI  
\*  
+  AWS CLI must be installed\. To install or upgrade it, see [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)\.
+ Ensure the Amazon EKS Connector agent role was created\. \.
Deregister the connected cluster\.  
\+  

```
aws eks deregister-cluster \
    --name my-cluster \
    --region region-code
```

 AWS Management Console  

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose **Clusters**\.

1. On the **Clusters** page, select the connected cluster and select **Deregister**\.

1. Confirm that you want to deregister the cluster\.

eksctl  
\*  
+ Ensure the Amazon EKS Connector agent role was created\. \.

  ```
  eksctl deregister cluster --name my-cluster
  ```

## To clean up the resources in your Kubernetes cluster<a name="deregister-connected-cluster-k8s"></a>

Helm  

1. Run the following command to uninstall the agent\.

   ```
   helm -n eks-connector uninstall eks-connector
   ```

YAML manifest  

1. Delete the Amazon EKS Connector YAML file from your Kubernetes cluster\.

   ```
   kubectl delete -f eks-connector.yaml
   ```

1. If you created `clusterrole` or `clusterrolebindings` for additional [IAM principals](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) to access the cluster, delete them from your Kubernetes cluster\.