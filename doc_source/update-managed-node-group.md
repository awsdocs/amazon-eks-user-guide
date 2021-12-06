# Updating a managed node group<a name="update-managed-node-group"></a>

When you initiate a managed node group update, Amazon EKS automatically updates your nodes for you, completing the steps listed in [Managed node update behavior](managed-node-update-behavior.md)\. If you're using an Amazon EKS optimized AMI, Amazon EKS automatically applies the latest security patches and operating system updates to your nodes as part of the latest AMI release version\.

There are several scenarios where it's useful to update your Amazon EKS managed node group's version or configuration:
+ You have updated the Kubernetes version for your Amazon EKS cluster and want to update your nodes to use the same Kubernetes version\.
+ A new AMI release version is available for your managed node group\. For more information about AMI versions, see these sections:
  + [Amazon EKS optimized Amazon Linux AMI versions](eks-linux-ami-versions.md)
  + [Amazon EKS optimized Bottlerocket AMIs](eks-optimized-ami-bottlerocket.md)
  + [Amazon EKS optimized Windows AMI versions](eks-ami-versions-windows.md)
+ You want to adjust the minimum, maximum, or desired count of the instances in your managed node group\.
+ You want to add or remove Kubernetes labels from the instances in your managed node group\.
+ You want to add or remove AWS tags from your managed node group\.
+ You need to deploy a new version of a launch template with configuration changes, such as an updated custom AMI\.
+ You have deployed version 1\.9\.0 or later of the Amazon VPC CNI add\-on, enabled the add\-on for prefix delegation, and want new AWS Nitro System instances in a node group to support a significantly increased number of pods\. For more information, see [Increase the amount of available IP addresses for your Amazon EC2 nodes](cni-increase-ip-addresses.md)\.

If there's a newer AMI release version for your managed node group's Kubernetes version, you can update your node group's version to use the newer AMI version\. Similarly, if your cluster is running a Kubernetes version that's newer than your node group, you can update the node group to use the latest AMI release version to match your cluster's Kubernetes version\.

When a node in a managed node group is terminated due to a scaling operation or update, the pods in that node are drained first\. For more information, see [Managed node update behavior](managed-node-update-behavior.md)\.

## Update a node group version<a name="mng-update"></a>

You can update a node group version with `eksctl` or the AWS Management Console\. Select the tab with the name of the tool that you want to use to update your node group\. The version that you update to can't be later than the control plane's version\.

------
#### [ eksctl ]<a name="update-node-group-version-eksctl"></a>

**To update a node group version with `eksctl`**
+ Update a managed node group to the latest AMI release of the same Kubernetes version that's currently deployed on the nodes with the following command\. Replace the *`<example values>`* \(include *`<>`*\) with your own\.

  ```
  eksctl upgrade nodegroup --name=<node-group-name> --cluster=<cluster-name>
  ```
**Note**  
If you're upgrading a node group that's deployed with a launch template to a new launch template version, add `--launch-template-<version>` to the preceding command\. The launch template must meet the requirements described in [Launch template support](launch-templates.md)\. If the launch template includes a custom AMI, the AMI must meet the requirements in [Specifying an AMI](launch-templates.md#launch-template-custom-ami)\. When you upgrade your node group to a newer version of your launch template, every node is recycled to match the new configuration of the launch template version that's specified\.  
You can't directly upgrade a node group that's deployed without a launch template to a new launch template version\. Instead, you must deploy a new node group using the launch template to update the node group to a new launch template version\.

  You can upgrade a node group to the same version as the control plane's Kubernetes version\. For example, if you have a cluster running Kubernetes 1\.21, you can upgrade nodes currently running Kubernetes 1\.20 to version 1\.21 with the following command\.

  ```
  eksctl upgrade nodegroup \
      --name=<node-group-name> \
      --cluster=<cluster-name> \
      --kubernetes-version=<1.21>
  ```

------
#### [ AWS Management Console ]<a name="update-node-group-version-console"></a>

**To update a node group version with the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the cluster that contains the node group to update\.

1. If at least one node group has an available update, a box appears at the top of the page notifying you of the available update\. If you select the **Configuration** tab and then the **Compute** tab, you'll see **Update now** in the **AMI release version** column in the **Node Groups** table for the node group that has an available update\. To update the node group, select **Update now**\. You won't see a notification for node groups that were deployed with a custom AMI\. If your nodes are deployed with a custom AMI, complete the following steps to deploy a new updated custom AMI\.
   + 

     1. Create a new version of your AMI\.

     1. Create a new launch template version with the new AMI ID\.

     1. Upgrade the nodes to the new version of the launch template\.

1. On the **Update Node Group version** page, select:
   + **Update Node Group version** – This option is unavailable if you deployed a custom AMI or your Amazon EKS optimized AMI is currently on the latest version for your cluster\.
   + **Launch template version** – This option is unavailable if the node group is deployed without a custom launch template\. You can only update the launch template version for a node group that has been deployed with a custom launch template\. Select the version that you want to update the node group to\. If your node group is configured with a custom AMI, then the version that you select must also specify an AMI\. When you upgrade to a newer version of your launch template, every node is recycled to match the new configuration of the launch template version specified\.

1. For **Update strategy**, select one of the following options and then choose **Update**\.
   + **Rolling update** – This option respects the pod disruption budgets for your cluster\. Updates fail if there's a pod disruption budget issue that causes Amazon EKS to be unable to gracefully drain the pods that are running on this node group\.
   + **Force update** – This option doesn't respect pod disruption budgets\. Updates occur regardless of pod disruption budget issues by forcing node restarts to occur\.

------

## Edit a node group configuration<a name="mng-edit"></a>

You can modify some of the configurations of a managed node group\.

**To edit a node group configuration**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the cluster that contains the node group to edit\.

1. Select the **Configuration** tab\. On the **Compute** tab, select the node group to edit, and choose **Edit**\.

1. \(Optional\) On the **Edit node group** page, edit the **Group configuration**\.
   + **Tags** – Add tags to or remove tags from your node group resource\. These tags are only applied to the Amazon EKS node group\. They don't propagate to other resources, such as subnets or Amazon EC2 instances in the node group\.
   + **Kubernetes labels** – Add or remove Kubernetes labels to the nodes in your node group\. The labels shown here are only the labels that you have applied with Amazon EKS\. Other labels may exist on your nodes that aren't shown here\.
   + **Kubernetes taints** – Add or remove Kubernetes taints to the nodes in your node group\. Added taints can have the effect of either `No_Schedule`, `Prefer_No_Schedule`, or `No_Execute`\.

1. \(Optional\) On the **Edit node group** page, edit the **Group size**\.
   + **Minimum size** – Specify the minimum number of nodes that the managed node group can scale in to\.
   + **Maximum size** – Specify the maximum number of nodes that the managed node group can scale out to\. For the maximum number of nodes supported in a node group, see [Amazon EKS service quotas](service-quotas.md)\.
   + **Desired size** – Specify the current number of nodes that the managed node group should maintain\.

1. \(Optional\) Edit the **Node Group update configuration**\. Select either **Number** or **Percentage**\. 
   + **Number** – Select and specify the number of nodes in your node group that can be updated in parallel\. These nodes will be unavailable during update\.
   + **Percentage** – Select and specify the percentage of nodes in your node group that can be updated in parallel\. These nodes will be unavailable during update\. This is useful if you have many nodes in your node group\.

1. When you're finished editing, choose **Save changes**\.