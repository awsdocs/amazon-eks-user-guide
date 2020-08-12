# Managed node update behavior<a name="managed-node-update-behavior"></a>

When you update a managed node group version to the latest AMI release version for your node group's Kubernetes version or to a newer Kubernetes version to match your cluster, Amazon EKS triggers the following logic:

1. Amazon EKS creates a new Amazon EC2 launch template version for the Auto Scaling group associated with your node group\. The new template uses the target AMI for the update\.

1. The Auto Scaling group is updated to use the latest launch template with the new AMI\.

1. The Auto Scaling group maximum size and desired size are incremented by one up to twice the number of Availability Zones in the Region that the Auto Scaling group is deployed in\. This is to ensure that at least one new instance comes up in every Availability Zone in the Region that your node group is deployed in\.

1. Amazon EKS checks the nodes in the node group for the `eks.amazonaws.com/nodegroup-image` label, and applies a `eks.amazonaws.com/nodegroup=unschedulable:NoSchedule` taint on all of the nodes in the node group that are not labeled with the latest AMI ID\. This prevents nodes that have already been updated from a previous failed update from being tainted\.

1. Amazon EKS randomly selects a node in the node group and evicts all pods from it\.

1. Once all of the pods are evicted, Amazon EKS cordons the node\. This is done so that the service controller doesn't send any new request to this node and removes this node from its list of healthy, active nodes\.

1. Amazon EKS sends a termination request to the Auto Scaling group for the cordoned node\.

1. Steps 5\-7 are repeated until there are no nodes in the node group that were deployed with the earlier version of the launch template\.

1. The Auto Scaling group maximum size and desired size are decremented by 1 to return to your pre\-update values\.