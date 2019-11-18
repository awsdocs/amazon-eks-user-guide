# Updating a Managed Node Group<a name="update-managed-node-group"></a>

There are several use cases for updating your Amazon EKS managed node group's version or configuration:
+ You have updated the Kubernetes version for your Amazon EKS cluster, and you want to update your worker nodes to use the same Kubernetes version\.
+ A new AMI release version is available for your managed node group\. For more information, see [Amazon EKS\-Optimized Linux AMI Versions](eks-linux-ami-versions.md)\.
+ You want to adjust the minimum, maximum, or desired count of the instances in your managed node group\.
+ You want to add or remove Kubernetes labels from the instances in your managed node group\.
+ You want to add or remove AWS tags from your managed node group\.

If there is a newer AMI release version for your managed node group's Kubernetes version than the one your node group is running, you can update it to use that new AMI version\. If your cluster is running a newer Kubernetes version than your node group, you can update the node group to use the latest AMI release version that matches your cluster's Kubernetes version\.

**Note**  
You cannot roll back a node group to an earlier Kubernetes version or AMI version\.

When a node in a managed node group is terminated due to a scaling action or update, the pods in that node are drained first\. For more information, see [Managed Node Update Behavior](managed-node-update-behavior.md)

**To update a node group version**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the cluster that contains the node group to update\.

1. Select the node group to update, and choose **Update group version**\.
**Note**  
The **Update group version** only appears if there is an update available\. If you do not see this button, then your node group is running the latest available version\.

1. On the **Update AMI release version** page, select one of the following options and choose **Confirm**\.
   + **Rolling update** — This option respects pod disruption budgets for your cluster and the update fails if Amazon EKS is unable to gracefully drain the pods that are running on this node group due to a pod disruption budget issue\.
   + **Force update** — This option does not respect pod disruption budgets and it forces node restarts\.

**To edit a node group configuration**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the cluster that contains the node group to edit\.

1. Select the node group to edit, and choose **Edit**\.

1. On the **Edit node group** page edit the **Group configuration** if necessary\.
   + **Tags** — Add tags to or remove tags from your node group resource\. These tags are only applied to the Amazon EKS node group, and they do not propagate to other resources, such as subnets or Amazon EC2 instances in the node group\.
   + **Kubernetes labels** — Add or remove Kubernetes labels to the nodes in your node group\. The labels shown here are only the labels that you have applied with Amazon EKS\. Other labels may exist on your nodes that are not shown here\.

1. On the **Edit node group** page edit the **Group size** if necessary\.
   + **Minimum size** — Specify the current number of worker nodes that the managed node group should maintain\.
   + **Maximum size** — Specify the maximum number of worker nodes that the managed node group can scale out to\. Managed node groups can support up to 100 nodes by default\.
   + **Desired size** — Specify the current number of worker nodes that the managed node group should maintain\.

1. When you are finished editing, choose **Save changes**\.