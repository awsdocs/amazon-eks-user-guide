# Granting access to a user to view a cluster<a name="connector-grant-access"></a>

Grant additional IAM users access to the Amazon EKS console to view information about the Kubernetes workloads and pods running on your connected cluster\.

## Prerequisites<a name="connector-grant-access-prereqs"></a>

The IAM user or role that you use to access the AWS Management Console must meet the following requirements\.
+ It has the `eks:AccessKubernetesApi` permission\.
+ The Amazon EKS Connector Service account can impersonate the IAM or role in the cluster\. This allows the eks\-connector to map the IAM user or role to a Kubernetes user\.

**To create and apply the Amazon EKS Connector cluster role**

1. Download the `eks-connector` cluster role template\.

   ```
   curl -o eks-connector-clusterrole.yaml https://amazon-eks.s3.us-west-2.amazonaws.com/eks-connector/manifests/eks-connector-console-roles/eks-connector-clusterrole.yaml
   ```

1. Edit the cluster role template YAML file\. Replace references of `%IAM_ARN%` with the Amazon Resource Name \(ARN\) of your IAM user or role\.

1. Apply the Amazon EKS Connector cluster role YAML to your Kubernetes cluster\.

   ```
   kubectl apply -f eks-connector-clusterrole.yaml
   ```

For an IAM user or role to vizualize the workloads on the Amazon EKS console, they must be associated with a Kubernetes `role` or `clusterrole` with necessary permissions to read these resources\. For more information, see [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) in the Kubernetes documentation\.

**To configure an IAM user to access the connected cluster**

1. You can download the example manifest file to create a `clusterrole` and `clusterrolebinding` or a `role` and `rolebinding`:
   + **View Kubernetes resources in all namespaces** – The `eks-connector-console-dashboard-full-access-clusterrole` cluster role gives access to all namespaces and resources that can be visualized in the console\. You can change the name of the `role`, `clusterrole` and their corresponding binding before applying it to your cluster\. Use the following command to download a sample file\.

     ```
     curl -o eks-connector-console-dashboard-full-access-group.yaml https://amazon-eks.s3.us-west-2.amazonaws.com/eks-connector/manifests/eks-connector-console-roles/eks-connector-console-dashboard-full-access-group.yaml
     ```
   + **View Kubernetes resources in a specific namespace** – The namespace in this file is `default`, so if you want to specify a different namespace, edit the file before applying it to your cluster\.Use the following command to download a sample file\.

     ```
     curl -o eks-connector-console-dashboard-restricted-access-group.yaml https://amazon-eks.s3.us-west-2.amazonaws.com/eks-connector/manifests/eks-connector-console-roles/eks-connector-console-dashboard-restricted-access-group.yaml
     ```

1. Edit the full access or restricted access YAML file to replace references of `%IAM_ARN%` with the Amazon Resource Name \(ARN\) of your IAM user or role\.

1. Apply the full access or restricted access YAML files to your Kubernetes cluster\. Replace the YAML file value with your own\.

   ```
   kubectl apply -f eks-connector-console-dashboard-full-access-group.yaml
   ```

To view your connected cluster and nodes, see [View nodes](view-nodes.md)\. To view workloads, see [View workloads](view-workloads.md)\. Keep in mind that some node and workload data aren't populated for connected clusters\.