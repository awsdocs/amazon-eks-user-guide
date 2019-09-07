# Deleting a Cluster<a name="delete-cluster"></a>

When you're done using an Amazon EKS cluster, you should delete the resources associated with it so that you don't incur any unnecessary costs\.

**Important**  
If you have active services in your cluster that are associated with a load balancer, you must delete those services before deleting the cluster so that the load balancers are deleted properly\. Otherwise, you can have orphaned resources in your VPC that prevent you from being able to delete the VPC\.

Choose the tab below that corresponds to your preferred cluster deletion method\.

------
#### [ eksctl ]

**To delete an Amazon EKS cluster and worker nodes with `eksctl`**

This procedure assumes that you have installed `eksctl`, and that your `eksctl` version is at least `0.5.1`\. You can check your version with the following command:

```
eksctl version
```

 For more information on installing or upgrading `eksctl`, see [Installing or Upgrading `eksctl`](eksctl.md#installing-eksctl)\.
**Note**  
This procedure only works for clusters that were created with `eksctl`\.

1. List all services running in your cluster\.

   ```
   kubectl get svc --all-namespaces
   ```

1. Delete any services that have an associated `EXTERNAL-IP` value\. These services are fronted by an Elastic Load Balancing load balancer, and you must delete them in Kubernetes to allow the load balancer and associated resources to be properly released\.

   ```
   kubectl delete svc service-name
   ```

1. Delete the cluster and its associated worker nodes with the following command, substituting the red text with your cluster name\.

   ```
   eksctl delete cluster --name prod
   ```

   Output:

   ```
   [ℹ]  using region us-west-2
   [ℹ]  deleting EKS cluster "prod"
   [ℹ]  will delete stack "eksctl-prod-nodegroup-standard-workers"
   [ℹ]  waiting for stack "eksctl-prod-nodegroup-standard-workers" to get deleted
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

1. Delete the worker node AWS CloudFormation stack\.

   1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

   1. Select the worker node stack to delete and then choose **Actions**, **Delete Stack**\.

   1. On the **Delete Stack** confirmation screen, choose **Yes, Delete**\.

1. Delete the cluster\.

   1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

   1. Select the cluster to delete and choose **Delete**\.

   1. On the delete cluster confirmation screen, choose **Delete**\.

1. \(Optional\) Delete the VPC AWS CloudFormation stack\.

   1. Select the VPC stack to delete and choose **Actions** and then **Delete Stack**\.

   1. On the **Delete Stack** confirmation screen, choose **Yes, Delete**\.

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

1. Delete the worker node AWS CloudFormation stack\.

   1. List your available AWS CloudFormation stacks with the following command\. Find the worker node template name in the resulting output\.

      ```
      aws cloudformation list-stacks --query StackSummaries[].StackName
      ```

   1. Delete the worker node stack with the following command, substituting the red text with your worker node stack name\.

      ```
      aws cloudformation delete-stack --stack-name worker-node-stack
      ```

1. Delete the cluster with the following command, substituting the red text with your cluster name\.

   ```
   aws eks delete-cluster --name my-cluster
   ```

1. \(Optional\) Delete the VPC AWS CloudFormation stack\.

   1. List your available AWS CloudFormation stacks with the following command\. Find the VPC template name in the resulting output\.

      ```
      aws cloudformation list-stacks --query StackSummaries[].StackName
      ```

   1. Delete the VPC stack with the following command, substituting the red text with your VPC stack name\.

      ```
      aws cloudformation delete-stack --stack-name my-vpc-stack
      ```

------