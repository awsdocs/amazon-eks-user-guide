# Deleting a managed node group<a name="delete-managed-node-group"></a>

This topic describes how you can delete an Amazon EKS managed node group\.

When you delete a managed node group, Amazon EKS first sets the minimum, maximum, and desired size of your Auto Scaling group to zero\. This then causes your node group to scale down\. Before each instance is terminated, Amazon EKS sends a signal to drain the Pods from that node and then waits a few minutes\. If the Pods haven't drained after a few minutes, Amazon EKS lets Auto Scaling continue the termination of the instance\. After every instance is terminated, the Auto Scaling group is deleted\.

**Important**  
If you delete a managed node group that uses a node IAM role that isn't used by any other managed node group in the cluster, the role is removed from the [`aws-auth` ConfigMap](add-user-role.md)\. If any of the self\-managed node groups in the cluster are using the same node IAM role, the self\-managed nodes move to the `NotReady` status\. Additionally, the cluster operation are also disrupted\. You can add the mapping back to the ConfigMap to minimize disruption\.

You can delete a managed node group with `eksctl` or the AWS Management Console\.

------
#### [ eksctl ]

**To delete a managed node group with `eksctl`**
+ Enter the following command\. Replace every *`example value`* with your own values\.

  ```
  eksctl delete nodegroup \
    --cluster my-cluster \
    --region region-code \
    --name my-mng
  ```

------
#### [ AWS Management Console ]

**To delete your managed node group using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the cluster that contains the node group to delete\.

1. Select the **Compute** tab\.

1. Select the node group to delete, and choose **Delete**\.

1. On the **Delete node group: *my\-mng*** page, enter the name of the node group in the text field and choose **Delete**\.

------