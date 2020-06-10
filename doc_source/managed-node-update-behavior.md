# Managed node update behavior<a name="managed-node-update-behavior"></a>

When you update a managed node group version to the latest AMI release version for your node group's Kubernetes version or to a newer Kubernetes version to match your cluster, Amazon EKS triggers the following logic:

1. Amazon EKS creates a new Amazon EC2 launch template version for the Auto Scaling group associated with your node group\. The new template uses the target AMI for the update\.

1. The Auto Scaling group is updated to use the latest launch template with the new AMI\.

1. The Auto Scaling group maximum size and desired size are incremented by the number of distinct Availability Zones of all running nodes\. When at least one new instance runs in every Availability Zone of your node group, go to next step\. If not, the Auto Scaling group maximum size and desired size are incremented by one repeatedly until the condition is met\. In case increased number of the Auto Scaling group maximum size reaches twice the number of distinct Availability Zones of your node group, the update fails\.

1. The Auto Scaling group launches a new instance with the new AMI to satisfy the increased desired size of the node group\.

1. Amazon EKS checks the nodes in the node group for the `eks.amazonaws.com/nodegroup-image` label, and it cordons all of the nodes in the node group that are not labeled with the latest AMI ID\. This prevents nodes that have already been updated from a previous failed update from being cordoned\.

1. Amazon EKS randomly selects a node in your node group and sends a termination signal to the Auto Scaling group, Then Amazon EKS sends a signal to drain the pods from the node\.\* After the node is drained, it is terminated\. This step is repeated until all of the nodes are using the new AMI version\.

1. The Auto Scaling group maximum size and desired size are decremented by 1 to return to your pre\-update values\.

\* If pods do not drain from a node \(for example, if a pod disruption budget is too restrictive\) for 15 minutes, then one of two things happens:
+ If the update is not forced, then the update fails and reports an error\.
+ If the update is forced, then the pods that could not be drained are deleted\.