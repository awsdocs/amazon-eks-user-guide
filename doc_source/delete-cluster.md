# Deleting a Cluster<a name="delete-cluster"></a>

When you are done using an Amazon EKS cluster, you should delete the resources associated with it so that you do not incur any unnecessary costs\.

**Important**  
If you have active services in your cluster that are associated with a load balancer, you must delete those services before deleting the cluster so that the load balancers are deleted properly\. Otherwise, you can have orphaned resources in your VPC that prevent you from being able to delete the VPC\.

**To delete an Amazon EKS cluster**

1. List all services running in your cluster:

   ```
   kubectl get svc --all-namespaces
   ```

1. Delete any services that have an associated `EXTERNAL-IP` value\. These services are fronted by an Elastic Load Balancing load balancer, and you must delete them in Kubernetes to allow the load balancer and associated resources to be properly released\.

   ```
   kubectl delete svc service-name
   ```

1. Delete the worker node AWS CloudFormation stack:

   1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

   1. Select the worker node stack to delete, and then choose **Actions**, **Delete Stack**\.

   1. On the **Delete Stack** confirmation screen, choose **Yes, Delete**\.

1. Delete the cluster:

   1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

   1. Select the cluster to delete and choose **Delete**\.

   1. On the delete cluster confirmation screen, choose **Delete**\.

1. \(Optional\) Delete the VPC AWS CloudFormation stack:

   1. Select the VPC stack to delete and choose **Actions**, **Delete Stack**\.

   1. On the **Delete Stack** confirmation screen, choose **Yes, Delete**\.