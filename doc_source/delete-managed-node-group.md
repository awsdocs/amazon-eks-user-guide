# Deleting a Managed Node Group<a name="delete-managed-node-group"></a>

This topic helps you to delete an Amazon EKS managed node group\.

When you delete a managed node group, Amazon EKS randomly selects a node in your node group and sends a termination signal to the Auto Scaling group\. Then Amazon EKS sends a signal to drain the pods from the node\. If pods do not drain from a node \(for example, if a pod disruption budget is too restrictive\) for 15 minutes, then the pods are deleted\. After the node is drained, it is terminated\. This step is repeated until all of the nodes in the Auto Scaling group are terminated, and then the Auto Scaling group is deleted\.

**To delete a managed node group**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the cluster that contains the node group to delete\.

1. Select the node group to delete, and choose **Delete**\.

1. On the **Delete *nodegroup*** page, type the name of the cluster in the text field and choose **Confirm**