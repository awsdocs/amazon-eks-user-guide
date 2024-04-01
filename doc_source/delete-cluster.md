# Deleting an Amazon EKS cluster<a name="delete-cluster"></a>

When you're done using an Amazon EKS cluster, you should delete the resources associated with it so that you don't incur any unnecessary costs\.

To remove a connected cluster, see [Deregistering a cluster](deregister-connected-cluster.md)

**Important**  
If you have active services in your cluster that are associated with a load balancer, you must delete those services before deleting the cluster so that the load balancers are deleted properly\. Otherwise, you can have orphaned resources in your VPC that prevent you from being able to delete the VPC\.
If you receive an error because the cluster creator has been removed, see [this article](https://aws.amazon.com/premiumsupport/knowledge-center/eks-api-server-unauthorized-error) to resolve\.
Amazon Managed Service for Prometheus resources are outside of the cluster lifecycle and need to be maintained independent of the cluster\. When you delete your cluster, make sure to also delete any applicable scrapers to stop applicable costs\. For more information, see [Find and delete scrapers](https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-collector-how-to.html#AMP-collector-list-delete) in the *Amazon Managed Service for Prometheus User Guide*\.

You can delete a cluster with `eksctl`, the AWS Management Console, or the AWS CLI\.

------
#### [ eksctl ]

**To delete an Amazon EKS cluster and nodes with `eksctl`**

This procedure requires `eksctl` version `0.175.0` or later\. You can check your version with the following command:

```
eksctl version
```

For instructions on how to install or upgrade `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.

1. List all services running in your cluster\.

   ```
   kubectl get svc --all-namespaces
   ```

1. Delete any services that have an associated `EXTERNAL-IP` value\. These services are fronted by an Elastic Load Balancing load balancer, and you must delete them in Kubernetes to allow the load balancer and associated resources to be properly released\.

   ```
   kubectl delete svc service-name
   ```

1. Delete the cluster and its associated nodes with the following command, replacing `prod` with your cluster name\.

   ```
   eksctl delete cluster --name prod
   ```

   Output:

   ```
   [ℹ]  using region region-code
   [ℹ]  deleting EKS cluster "prod"
   [ℹ]  will delete stack "eksctl-prod-nodegroup-standard-nodes"
   [ℹ]  waiting for stack "eksctl-prod-nodegroup-standard-nodes" to get deleted
   [ℹ]  will delete stack "eksctl-prod-cluster"
   [✔]  the following EKS cluster resource(s) for "prod" will be deleted: cluster. If in doubt, check CloudFormation console
   ```

------
#### [ AWS Management Console ]

**To delete an Amazon EKS cluster with the AWS Management Console**

1. List all services running in your cluster\.

   ```
   kubectl get svc --all-namespaces
   ```

1. Delete any services that have an associated `EXTERNAL-IP` value\. These services are fronted by an Elastic Load Balancing load balancer, and you must delete them in Kubernetes to allow the load balancer and associated resources to be properly released\.

   ```
   kubectl delete svc service-name
   ```

1. Delete all node groups and Fargate profiles\.

   1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

   1. In the left navigation pane, choose Amazon EKS **Clusters**, and then in the tabbed list of clusters, choose the name of the cluster that you want to delete\.

   1. Choose the **Compute** tab and choose a node group to delete\. Choose **Delete**, enter the name of the node group, and then choose **Delete**\. Delete all node groups in the cluster\.
**Note**  
The node groups listed are [managed node groups](managed-node-groups.md) only\.

   1. Choose a **Fargate Profile** to delete, select **Delete**, enter the name of the profile, and then choose **Delete**\. Delete all Fargate profiles in the cluster\.

1. Delete all self\-managed node AWS CloudFormation stacks\.

   1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

   1. Choose the node stack to delete, and then choose **Delete**\.

   1. In the **Delete stack** confirmation dialog box, choose **Delete stack**\. Delete all self\-managed node stacks in the cluster\.

1. Delete the cluster\.

   1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

   1. choose the cluster to delete and choose **Delete**\.

   1. On the delete cluster confirmation screen, choose **Delete**\.

1. \(Optional\) Delete the VPC AWS CloudFormation stack\.

   1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

   1. Select the VPC stack to delete, and then choose **Delete**\.

   1. In the **Delete stack** confirmation dialog box, choose **Delete stack**\.

------
#### [ AWS CLI ]

**To delete an Amazon EKS cluster with the AWS CLI**

1. List all services running in your cluster\.

   ```
   kubectl get svc --all-namespaces
   ```

1. Delete any services that have an associated `EXTERNAL-IP` value\. These services are fronted by an Elastic Load Balancing load balancer, and you must delete them in Kubernetes to allow the load balancer and associated resources to be properly released\.

   ```
   kubectl delete svc service-name
   ```

1. Delete all node groups and Fargate profiles\.

   1. List the node groups in your cluster with the following command\.

      ```
      aws eks list-nodegroups --cluster-name my-cluster
      ```
**Note**  
The node groups listed are [managed node groups](managed-node-groups.md) only\.

   1. Delete each node group with the following command\. Delete all node groups in the cluster\.

      ```
      aws eks delete-nodegroup --nodegroup-name my-nodegroup --cluster-name my-cluster
      ```

   1. List the Fargate profiles in your cluster with the following command\.

      ```
      aws eks list-fargate-profiles --cluster-name my-cluster
      ```

   1. Delete each Fargate profile with the following command\. Delete all Fargate profiles in the cluster\.

      ```
      aws eks delete-fargate-profile --fargate-profile-name my-fargate-profile --cluster-name my-cluster
      ```

1. Delete all self\-managed node AWS CloudFormation stacks\.

   1. List your available AWS CloudFormation stacks with the following command\. Find the node template name in the resulting output\.

      ```
      aws cloudformation list-stacks --query "StackSummaries[].StackName"
      ```

   1. Delete each node stack with the following command, replacing `node-stack` with your node stack name\. Delete all self\-managed node stacks in the cluster\.

      ```
      aws cloudformation delete-stack --stack-name node-stack
      ```

1. Delete the cluster with the following command, replacing `my-cluster` with your cluster name\.

   ```
   aws eks delete-cluster --name my-cluster
   ```

1. \(Optional\) Delete the VPC AWS CloudFormation stack\.

   1. List your available AWS CloudFormation stacks with the following command\. Find the VPC template name in the resulting output\.

      ```
      aws cloudformation list-stacks --query "StackSummaries[].StackName"
      ```

   1. Delete the VPC stack with the following command, replacing `my-vpc-stack` with your VPC stack name\.

      ```
      aws cloudformation delete-stack --stack-name my-vpc-stack
      ```

------