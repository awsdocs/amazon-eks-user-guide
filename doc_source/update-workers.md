# Self\-managed node updates<a name="update-workers"></a>

When a new Amazon EKS\-optimized AMI is released, you should consider replacing the nodes in your self\-managed node group with the new AMI\. Likewise, if you have updated the Kubernetes version for your Amazon EKS cluster, you should also update the nodes to use nodes with the same Kubernetes version\.

**Important**  
This topic covers node updates for self\-managed nodes\. If you are using [Managed node groups](managed-node-groups.md), see [Updating a managed node group](update-managed-node-group.md)\.

There are two basic ways to update self\-managed node groups in your clusters to use a new AMI:
+ [Migrating to a new node group](migrate-stack.md) – Create a new node group and migrate your pods to that group\. Migrating to a new node group is more graceful than simply updating the AMI ID in an existing AWS CloudFormation stack, because the migration process taints the old node group as `NoSchedule` and drains the nodes after a new stack is ready to accept the existing pod workload\.
+ [Updating an existing self\-managed node group](update-stack.md) – Update the AWS CloudFormation stack for an existing node group to use the new AMI\. This method is not supported for node groups that were created with `eksctl`\.