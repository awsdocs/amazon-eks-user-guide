--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Deleting a managed node group<a name="delete-managed-node-group"></a>

This topic describes how you can delete an Amazon EKS managed node group\. When you delete a managed node group, Amazon EKS first sets the minimum, maximum, and desired size of your Auto Scaling group to zero\. This then causes your node group to scale down\.

Before each instance is terminated, Amazon EKS sends a signal to drain the Pods from that node\. If the Pods haven’t drained after a few minutes, Amazon EKS lets Auto Scaling continue the termination of the instance\. After every instance is terminated, the Auto Scaling group is deleted\.

**Important**  

You can delete a managed node group with `eksctl` or the AWS Management Console\.

eksctl  
\* \.To delete a managed node group with `eksctl` Enter the following command\. Replace every ` example value ` with your own values\.  

```
eksctl delete nodegroup \
  --cluster my-cluster \
  --name my-mng \
  --region region-code
```
For more options, see [Deleting and draining nodegroups](https://eksctl.io/usage/nodegroups/#deleting-and-draining-nodegroups) in the `eksctl` documentation\.

 AWS Management Console  

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. On the **Clusters** page, choose the cluster that contains the node group to delete\.

1. On the selected cluster page, choose the **Compute** tab\.

1. In the **Node groups** section, choose the node group to delete\. Then choose **Delete**\.

1. In the **Delete node group** confirmation dialog box, enter the name of the node group\. Then choose **Delete**\.

 AWS CLI  
\*  

1. Enter the following command\. Replace every ` example value ` with your own values\.

   ```
   aws eks delete-nodegroup \
     --cluster-name my-cluster \
     --nodegroup-name my-mng \
     --region region-code
   ```

1. Use the arrow keys on your keyboard to scroll through the response output\. Press the ` q key when you’re finished.` 
For more options, see the ` [delete\-nodegroup](https://docs.aws.amazon.com/cli/latest/reference/eks/delete-nodegroup.html) ` command in the * AWS CLI Command Reference*\.