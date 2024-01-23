# Granting access to an IAM principal to view Kubernetes resources on a cluster<a name="connector-grant-access"></a>

Grant [IAM principals](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) access to the Amazon EKS console to view information about Kubernetes resources running on your connected cluster\.

## Prerequisites<a name="connector-grant-access-prereqs"></a>

The [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) that you use to access the AWS Management Console must meet the following requirements:
+ It must have the `eks:AccessKubernetesApi` IAM permission\.
+ The Amazon EKS Connector service account can impersonate the IAM principal in the cluster\. This allows the Amazon EKS Connector to map the IAM principal to a Kubernetes user\.

**To create and apply the Amazon EKS Connector cluster role**

1. Download the `eks-connector` cluster role template\.

   ```
   curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/eks-connector/manifests/eks-connector-console-roles/eks-connector-clusterrole.yaml
   ```

1. Edit the cluster role template YAML file\. Replace references of `%IAM_ARN%` with the Amazon Resource Name \(ARN\) of your IAM principal\.

1. Apply the Amazon EKS Connector cluster role YAML to your Kubernetes cluster\.

   ```
   kubectl apply -f eks-connector-clusterrole.yaml
   ```

For an IAM principal to view Kubernetes resources in Amazon EKS console, the principal must be associated with a Kubernetes `role` or `clusterrole` with necessary permissions to read the resources\. For more information, see [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) in the Kubernetes documentation\.

**To configure an IAM principal to access the connected cluster**

1. You can download either of these example manifest files to create a `clusterrole` and `clusterrolebinding` or a `role` and `rolebinding`, respectively:  
**View Kubernetes resources in all namespaces**  
The `eks-connector-console-dashboard-full-access-clusterrole` cluster role gives access to all namespaces and resources that can be visualized in the console\. You can change the name of the `role`, `clusterrole` and their corresponding binding before applying it to your cluster\. Use the following command to download a sample file\.  

   ```
   curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/eks-connector/manifests/eks-connector-console-roles/eks-connector-console-dashboard-full-access-group.yaml
   ```  
**View Kubernetes resources in a specific namespace**  
The namespace in this file is `default`, so if you want to specify a different namespace, edit the file before applying it to your cluster\.Use the following command to download a sample file\.  

   ```
   curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/eks-connector/manifests/eks-connector-console-roles/eks-connector-console-dashboard-restricted-access-group.yaml
   ```

1. Edit the full access or restricted access YAML file to replace references of `%IAM_ARN%` with the Amazon Resource Name \(ARN\) of your IAM principal\.

1. Apply the full access or restricted access YAML files to your Kubernetes cluster\. Replace the YAML file value with your own\.

   ```
   kubectl apply -f eks-connector-console-dashboard-full-access-group.yaml
   ```

To view Kubernetes resources in your connected cluster, see [View Kubernetes resources](view-kubernetes-resources.md)\. Data for some resource types on the **Resources** tab isn't available for connected clusters\.