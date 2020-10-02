# Deleting a cluster<a name="delete-cluster"></a>

When you're done using an Amazon EKS cluster, you should delete the resources associated with it so that you don't incur any unnecessary costs\.

**Important**  
If you have active services in your cluster that are associated with a load balancer, you must delete those services before deleting the cluster so that the load balancers are deleted properly\. Otherwise, you can have orphaned resources in your VPC that prevent you from being able to delete the VPC\.

You can delete a cluster with [`eksctl`](#delete-cluster-eksctl), the [AWS Management Console](#delete-cluster-console), or the[ AWS CLI](#delete-cluster-cli)\.<a name="delete-cluster-eksctl"></a>

**\[ To delete an Amazon EKS cluster and nodes with `eksctl` \]**

This procedure requires `eksctl` version `0.29.0-rc.1` or later\. You can check your version with the following command:

```
eksctl version
```

For more information on installing or upgrading `eksctl`, see [Installing or upgrading `eksctl`](eksctl.md#installing-eksctl)\.
**Note**  
This procedure only works for clusters that were created with `eksctl`\.

1. List all services running in your cluster\.

   ```
   kubectl get svc --all-namespaces
   ```

1. Delete any services that have an associated `EXTERNAL-IP` value\. These services are fronted by an Elastic Load Balancing load balancer, and you must delete them in Kubernetes to allow the load balancer and associated resources to be properly released\.

   ```
   kubectl delete svc <service-name>
   ```

1. Delete the cluster and its associated nodes with the following command, replacing <prod> with your cluster name\.

   ```
   eksctl delete cluster --name <prod>
   ```

   Output:

   ```
   [ℹ]  using region <region-code>
   [ℹ]  deleting EKS cluster "prod"
   [ℹ]  will delete stack "eksctl-prod-nodegroup-standard-nodes"
   [ℹ]  waiting for stack "eksctl-prod-nodegroup-standard-nodes" to get deleted
   [ℹ]  will delete stack "eksctl-prod-cluster"
   [✔]  the following EKS cluster resource(s) for "prod" will be deleted: cluster. If in doubt, check CloudFormation console
   ```<a name="delete-cluster-console"></a>

**\[ To delete an Amazon EKS cluster with the AWS Management Console \]**

1. List all services running in your cluster\.

   ```
   kubectl get svc --all-namespaces
   ```

1. Delete any services that have an associated `EXTERNAL-IP` value\. These services are fronted by an Elastic Load Balancing load balancer, and you must delete them in Kubernetes to allow the load balancer and associated resources to be properly released\.

   ```
   kubectl delete svc <service-name>
   ```

1. Delete all node groups and Fargate profiles\.

   1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

   1. In the left navigation, select **Clusters**, and then in the tabbed list of clusters, select the name of the cluster that you want to delete\.

   1. Select the **Compute** tab, select a node group to delete, select **Delete**, enter the name of the node group, and then select **Delete**\. Delete all node groups in the cluster\.
**Note**  
The node groups listed are [managed node groups](managed-node-groups.md) only\.

   1. Select a **Fargate Profile** to delete, select **Delete**, enter the name of the profile, and then select **Delete**\. Delete all Fargate profiles in the cluster\.

1. Delete all self\-managed node AWS CloudFormation stacks\.

   1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

   1. Select the node stack to delete and then choose **Actions**, **Delete Stack**\.

   1. On the **Delete Stack** confirmation screen, choose **Yes, Delete**\. Delete all self\-managed node stacks in the cluster\.

1. Delete the cluster\.

   1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

   1. Select the cluster to delete and choose **Delete**\.

   1. On the delete cluster confirmation screen, choose **Delete**\.

1. \(Optional\) Delete the VPC AWS CloudFormation stack\.

   1. Select the VPC stack to delete and choose **Actions** and then **Delete Stack**\.

   1. On the **Delete Stack** confirmation screen, choose **Yes, Delete**\.<a name="delete-cluster-cli"></a>

**\[ To delete an Amazon EKS cluster with the AWS CLI \]**

1. List all services running in your cluster\.

   ```
   kubectl get svc --all-namespaces
   ```

1. Delete any services that have an associated `EXTERNAL-IP` value\. These services are fronted by an Elastic Load Balancing load balancer, and you must delete them in Kubernetes to allow the load balancer and associated resources to be properly released\.

   ```
   kubectl delete svc <service-name>
   ```

1. Delete all node groups and Fargate profiles\.

   1. List the node groups in your cluster with the following command\.

      ```
      aws eks list-nodegroups --cluster-name <my-cluster>
      ```
**Note**  
The node groups listed are [managed node groups](managed-node-groups.md) only\.

   1. Delete each node group with the following command\. Delete all node groups in the cluster\.

      ```
      aws eks delete-nodegroup --nodegroup-name <my-nodegroup> --cluster-name <my-cluster>
      ```

   1. List the Fargate profiles in your cluster with the following command\.

      ```
      aws eks list-fargate-profiles --cluster-name <my-cluster>
      ```

   1. Delete each Fargate profile with the following command\. Delete all Fargate profiles in the cluster\.

      ```
      aws eks delete-fargate-profile --fargate-profile-name <my-fargate-profile> --cluster-name <my-cluster>
      ```

1. Delete all self\-managed node AWS CloudFormation stacks\.

   1. List your available AWS CloudFormation stacks with the following command\. Find the node template name in the resulting output\.

      ```
      aws cloudformation list-stacks --query "StackSummaries[].StackName"
      ```

   1. Delete each node stack with the following command, replacing <node\-stack> with your node stack name\. Delete all self\-managed node stacks in the cluster\.

      ```
      aws cloudformation delete-stack --stack-name <node-stack>
      ```

1. Delete the cluster with the following command, replacing <my\-cluster> with your cluster name\.

   ```
   aws eks delete-cluster --name <my-cluster>
   ```

1. \(Optional\) Delete the VPC AWS CloudFormation stack\.

   1. List your available AWS CloudFormation stacks with the following command\. Find the VPC template name in the resulting output\.

      ```
      aws cloudformation list-stacks --query "StackSummaries[].StackName"
      ```

   1. Delete the VPC stack with the following command, replacing <my\-vpc\-stack> with your VPC stack name\.

      ```
      aws cloudformation delete-stack --stack-name <my-vpc-stack>
      ```