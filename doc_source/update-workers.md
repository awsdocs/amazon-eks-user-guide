--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Self\-managed node updates<a name="update-workers"></a>

When a new Amazon EKS optimized AMI is released, consider replacing the nodes in your self\-managed node group with the new AMI\. Likewise, if you have updated the Kubernetes version for your Amazon EKS cluster, update the nodes to use nodes with the same Kubernetes version\.

**Important**  

There are two basic ways to update self\-managed node groups in your clusters to use a new AMI:
+ Create a new node group and migrate your Pods to that group\. Migrating to a new node group is more graceful than simply updating the AMI ID in an existing AWS CloudFormation stack\. This is because the migration process [taints](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/) the old node group as `NoSchedule` and drains the nodes after a new stack is ready to accept the existing Pod workload\.
+ Update the AWS CloudFormation stack for an existing node group to use the new AMI\. This method isn’t supported for node groups that were created with `eksctl`\.