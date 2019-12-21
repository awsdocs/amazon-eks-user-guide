# Worker Node Updates<a name="update-workers"></a>

When a new Amazon EKS\-optimized AMI is released, you should consider replacing the nodes in your worker node group with the new AMI\. Likewise, if you have updated the Kubernetes version for your Amazon EKS cluster, you should also update the worker nodes to use worker nodes with the same Kubernetes version\.

**Important**  
This topic covers worker node updates for unmanaged node groups\. If you are using [Managed Node Groups](managed-node-groups.md), see [Updating a Managed Node Group](update-managed-node-group.md)\.

There are two basic ways to update unmanaged node groups in your clusters to use a new AMI: create a new worker node group and migrate your pods to that group, or update the AWS CloudFormation stack for an existing worker node group to use the new AMI\. This latter method is not supported for worker node groups that were created with `eksctl`\.

Migrating to a new worker node group is more graceful than simply updating the AMI ID in an existing AWS CloudFormation stack, because the migration process taints the old node group as `NoSchedule` and drains the nodes after a new stack is ready to accept the existing pod workload\.

**Topics**
+ [Migrating to a New Worker Node Group](migrate-stack.md)
+ [Updating an Existing Worker Node Group](update-stack.md)