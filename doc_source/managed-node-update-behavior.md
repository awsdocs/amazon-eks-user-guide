# Managed node update behavior<a name="managed-node-update-behavior"></a>

The Amazon EKS managed worker node upgrade strategy has four different phases described in the following sections\.

## Setup phase<a name="managed-node-update-set-up"></a>

The setup phase has these steps:

1. Creates a new Amazon EC2 launch template version for the Auto Scaling group that's associated with your node group\. The new launch template version uses the target AMI or customer\-provided launch template version for the update\.

1. Updates the Auto Scaling group to use the latest launch template version\.

1. Determines the maximum quantity of nodes to upgrade in parallel using the `updateConfig` property for the node group\. The maximum unavailable has a quota of 100 nodes\. The default value is one node\. For more information, see the [https://docs.aws.amazon.com/eks/latest/APIReference/API_UpdateNodegroupConfig.html#API_UpdateNodegroupConfig_RequestSyntax](https://docs.aws.amazon.com/eks/latest/APIReference/API_UpdateNodegroupConfig.html#API_UpdateNodegroupConfig_RequestSyntax) property in the *Amazon EKS API Reference*\.

## Scale up phase<a name="managed-node-update-scale-up"></a>

When upgrading the nodes in a managed node group, the upgraded nodes are launched in the same Availability Zone as those that are being upgraded\. To guarantee this placement, we use Amazon EC2's Availability Zone Rebalancing\. For more information, see [Availability Zone Rebalancing](https://docs.aws.amazon.com/autoscaling/ec2/userguide/auto-scaling-benefits.html#AutoScalingBehavior.InstanceUsage) in the *Amazon EC2 Auto Scaling User Guide*\. To meet this requirement, it's possible that we’d launch up to two instances per Availability Zone in your Managed Node Group\.

The scale up phase has these steps:

1. Increments the Auto Scaling Group’s maximum size and desired size by the larger of either:
   + Up to twice the number of Availability Zones that the Auto Scaling group is deployed in\.
   + The maximum unavailable of upgrade\.

     For example, if your node group has five Availability Zones and `maxUnavailable` as one, the upgrade process can launch a maximum of 10 nodes\. However when `maxUnavailable` is 20 \(or anything greater than 10, the process would launch 20 new nodes\)\.

1. After scaling the Auto Scaling Group, it checks if the nodes using the latest configuration are present in the node group\. This step succeeds only when it meets these criteria:
   + At least one new node is launched in every Availability Zone where the node exists\.
   + Every new node should be in `Ready` state\.
   + New nodes should have Amazon EKS applied labels\.

     These are the Amazon EKS applied labels on the worker nodes in a regular node group:
     + `eks.amazonaws.com/nodegroup-image=<$amiName>`
     + `eks.amazonaws.com/nodegroup=<$nodeGroupName>`

     These are the Amazon EKS applied labels on the worker nodes in a custom launch template or AMI node group:
     + `eks.amazonaws.com/nodegroup-image=<$amiName>`
     + `eks.amazonaws.com/nodegroup=<$nodeGroupName>`
     + `eks.amazonaws.com/sourceLaunchTemplateId=<$launchTemplateId>`
     + `eks.amazonaws.com/sourceLaunchTemplateVersion=<$launchTemplateVersion>`

1. Applies an `eks.amazonaws.com/nodegroup=unschedulable:NoSchedule` taint on every node in the node group without the latest labels\. This prevents nodes that have already been updated from a previous failed update from being tainted\.

The following are known reasons which lead to a `NodeCreationFailure` error in this phase:
+ **Insufficient capacity in the Availability Zone** – There is a possibility that the Availability Zone might not have capacity of requested instance types\. It's recommended to configure multiple instance types while creating a managed node group\.
+ **Customers hitting EC2 instance limits in their account** – You may need to increase the number of Amazon EC2 instances your account can run simultaneously using Service Quotas\. For more information, see [EC2 Service Quotas](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html) in the *Amazon Elastic Compute Cloud User Guide for Linux Instances*\.
+ **Custom user data** – Custom user data can sometimes break the bootstrap process\. This scenario can lead to the `kubelet` not starting on the node or nodes not getting expected Amazon EKS labels on them\. For more information on handling custom LT/AMI, see [Specifying an AMI](launch-templates.md#launch-template-custom-ami)\.
+ **Any changes which make a node unhealthy or not ready** – Node disk pressure, memory pressure, and similar conditions can lead to a node not going to `Ready` state\.

## Upgrade phase<a name="managed-node-update-upgrade"></a>

The upgrade phase has these steps:

1. Randomly selects a node, up to the maximum unavailable configured for the node group\.

1. Drains the pods from the node\. If the pods don't leave the node within 15 mins, it would force delete the pods if force flag is applied with update-nodegroup-version request, otherwise it fails with a PodEvictionFailure error.

1. Cordons the node after every pod is evicted and waits for 60 seconds\. This is done so that the service controller doesn't send any new requests to this node and removes this node from its list of active nodes\.

1. Sends a termination request to the Auto Scaling Group for the cordoned node\.

1. Repeats the previous upgrade steps until there are no nodes in the node group that are deployed with the earlier version of the launch template\.

The following are known reasons which lead to a `PodEvictionFailure` error in this phase:
+ **Aggressive PDB** – Aggressive PDB is defined on the pod or there are multiple PDBs pointing to the same pod\.
+ **Deployment tolerating all the taints** – Once every pod is evicted, it's expected for the node to be empty because the node is tainted in the earlier steps\. However, if the deployment tolerates every taint, then the node is more likely to be non\-empty, leading to pod eviction failure\.

## Scale down phase<a name="managed-node-update-scale-down"></a>

The scale down phase decrements the Auto Scaling group maximum size and desired size by one to return to values before the update started\.

If the Upgrade workflow determines that the Cluster Autoscaler is scaling up the node group during the scale down phase of the workflow, it exits immediately without bringing the node group back to its original size\.