# Managed node update behavior<a name="managed-node-update-behavior"></a>

When you update a managed node group version to the latest AMI release version for your node group's Kubernetes version or to a newer Kubernetes version to match your cluster, Amazon EKS automatically completes the following tasks:

1. Creates a new Amazon EC2 launch template version for the Auto Scaling group associated with your node group\. The new template uses the target AMI for the update\.

1. Updates the Auto Scaling group to use the latest launch template with the new AMI\.

1. Determine maximum nodes to upgrade in parallel using updateConfig configured for the node group\. The maximum concurrency \(unavailable\) is capped at 100 nodes\. 

1. Increments the Auto Scaling group maximum size and desired size by one of the following conditions:

   \- After up to twice the number of Availability Zones in the Region that the Auto Scaling group is deployed in

   \- The max concurrency of upgrade\.

1. Checks the nodes in the node group for the `eks.amazonaws.com/nodegroup-image` label, and applies a `eks.amazonaws.com/nodegroup=unschedulable:NoSchedule` taint on all of the nodes in the node group that aren't labeled with the latest AMI ID\. This prevents nodes that have already been updated from a previous failed update from being tainted\.

1. Randomly selects up to max nodes to upgrade in parallel\.

1. Cordons the node after all of the pods are evicted\. This is done so that the service controller doesn't send any new requests to this node and removes this node from its list of healthy, active nodes\.

1. Sends a termination request to the Auto Scaling group for the cordoned node\.

1. Repeats steps 6\-8 until there are no nodes in the node group that are deployed with the earlier version of the launch template\.

1. Decrements the Auto Scaling group maximum size and desired size by 1 to return to your pre\-update values\.