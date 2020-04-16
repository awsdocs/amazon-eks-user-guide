# Updating a managed node group<a name="update-managed-node-group"></a>

There are several use cases for updating your Amazon EKS managed node group's version or configuration:
+ You have updated the Kubernetes version for your Amazon EKS cluster, and you want to update your worker nodes to use the same Kubernetes version\.
+ A new AMI release version is available for your managed node group\. For more information, see [Amazon EKS\-optimized Linux AMI versions](eks-linux-ami-versions.md)\.
+ You want to adjust the minimum, maximum, or desired count of the instances in your managed node group\.
+ You want to add or remove Kubernetes labels from the instances in your managed node group\.
+ You want to add or remove AWS tags from your managed node group\.

If there is a newer AMI release version for your managed node group's Kubernetes version than the one your node group is running, you can update it to use that new AMI version\. If your cluster is running a newer Kubernetes version than your node group, you can update the node group to use the latest AMI release version that matches your cluster's Kubernetes version\.

**Note**  
You cannot roll back a node group to an earlier Kubernetes version or AMI version\.

When a node in a managed node group is terminated due to a scaling action or update, the pods in that node are drained first\. For more information, see [Managed node update behavior](managed-node-update-behavior.md)\.

## Update a node group version<a name="mng-update"></a>

Select the tab with the name of the tool that you'd like to upgrade the version with\.

------
#### [ AWS Management Console ]

**To update a node group version**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the cluster that contains the node group to update\.

1. If at least one of your node groups has an update available, you'll see a notification under the cluster name letting your know how many of your node groups have an update available\. In the **Node Groups** table you will see **Update now** to the right of the value in the **AMI release version** column for each node group that can be updated\. Select **Update now** for a node group that you want to update\.

   If you select a node group from the table and an update is available for it, you'll receive a notification on the **Node Group configuration** page\. If so, you can select the **Update now** button on the **Node Group configuration** page\.
**Note**  
**Update now** only appears if there is an update available\. If you do not see this text, then your node group is running the latest available version\.

1. On the **Update AMI release version** page, select the **Available AMI release version** that you want to update to, select one of the following options for **Update strategy**, and choose **Update**\.
   + **Rolling update** — This option respects pod disruption budgets for your cluster and the update fails if Amazon EKS is unable to gracefully drain the pods that are running on this node group due to a pod disruption budget issue\.
   + **Force update** — This option does not respect pod disruption budgets and it forces node restarts\.

------
#### [ eksctl ]

Upgrade a managed nodegroup to the latest AMI release of the same Kubernetes version that is currently deployed on the worker nodes with the following command\.

```
eksctl upgrade nodegroup --name=node-group-name --cluster=cluster-name
```

You can upgrade a nodegroup to a version that is one major release later than the nodegroup's current Kubernetes version\. For example, you can upgrade workers currently running Kubernetes 1\.14 to version 1\.15 with the following command\.

```
eksctl upgrade nodegroup --name=node-group-name --cluster=cluster-name --kubernetes-version=1.15
```

------

## Edit a node group configuration<a name="mng-edit"></a>

You can change some of the configuration of a managed node group\.

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