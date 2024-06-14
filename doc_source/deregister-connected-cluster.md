# Deregistering a cluster<a name="deregister-connected-cluster"></a>

If you are finished using a connected cluster, you can deregister it\. After it's deregistered, the cluster is no longer visible in the Amazon EKS console\.

You must have the following permissions to call the deregisterCluster API:
+ `eks:DeregisterCluster`
+ `ssm:DeleteActivation`
+ `ssm:DeregisterManagedInstance`

This process involves two steps: Deregistering the cluster with Amazon EKS and uninstalling the eks\-connector agent in the cluster\.

## To deregister the Kubernetes cluster<a name="deregister-connected-cluster-eks"></a>

------
#### [ AWS CLI ]

**Prerequisites**
+ AWS CLI must be installed\. To install or upgrade it, see [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)\.
+ Ensure the Amazon EKS Connector agent role was created\. \.

Deregister the connected cluster\.

```
aws eks deregister-cluster \
    --name my-cluster \
    --region region-code
```

------
#### [ AWS Management Console ]

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose **Clusters**\.

1. On the **Clusters** page, select the connected cluster and select **Deregister**\.

1. Confirm that you want to deregister the cluster\.

------
#### [ eksctl ]

**Prerequisites**
+ `eksctl` version `0.68` or later must be installed\. To install or upgrade it, see [Getting started with Amazon EKS – `eksctl`](getting-started-eksctl.md)\.
+ Ensure the Amazon EKS Connector agent role was created\. \.

**To deregister your cluster with `eksctl`**
+ For the Connector configuration, specify your Amazon EKS Connector agent IAM role\. For more information, see [Required IAM roles for Amazon EKS Connector](eks-connector.md#connector-iam-permissions)\.

  ```
  eksctl deregister cluster --name my-cluster
  ```

------

## To clean up the resources in your Kubernetes cluster<a name="deregister-connected-cluster-k8s"></a>

------
#### [ Helm ]
+ Run the following command to uninstall the agent\.

  ```
  helm -n eks-connector uninstall eks-connector
  ```

------
#### [ YAML manifest ]

1. Delete the Amazon EKS Connector YAML file from your Kubernetes cluster\.

   ```
   kubectl delete -f eks-connector.yaml
   ```

1. If you created `clusterrole` or `clusterrolebindings` for additional [IAM principals](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) to access the cluster, delete them from your Kubernetes cluster\.

------