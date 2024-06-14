# Node taints on managed node groups<a name="node-taints-managed-node-groups"></a>

Amazon EKS supports configuring Kubernetes taints through managed node groups\. Taints and tolerations work together to ensure that Pods aren't scheduled onto inappropriate nodes\. One or more taints can be applied to a node\. This marks that the node shouldn't accept any Pods that don't tolerate the taints\. Tolerations are applied to Pods and allow, but don't require, the Pods to schedule onto nodes with matching taints\. For more information, see [Taints and Tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/) in the Kubernetes documentation\.

Kubernetes node taints can be applied to new and existing managed node groups using the AWS Management Console or through the Amazon EKS API\.
+ For information on creating a node group with a taint using the AWS Management Console, see [Creating a managed node group](create-managed-node-group.md)\.
+ The following is an example of creating a node group with a taint using the AWS CLI:

  ```
  aws eks create-nodegroup \
   --cli-input-json '
  {
    "clusterName": "my-cluster",
    "nodegroupName": "node-taints-example",
    "subnets": [
       "subnet-1234567890abcdef0",
       "subnet-abcdef01234567890",
       "subnet-021345abcdef67890"
     ],
    "nodeRole": "arn:aws:iam::111122223333:role/AmazonEKSNodeRole",
    "taints": [
       {
           "key": "dedicated",
           "value": "gpuGroup",
           "effect": "NO_SCHEDULE"
       }
     ]
  }'
  ```

For more information and examples of usage, see [taint](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#taint) in the Kubernetes reference documentation\.

**Note**  
Taints can be updated after you create the node group using the `UpdateNodegroupConfig` API\.
The taint key must begin with a letter or number\. It can contain letters, numbers, hyphens \(`-`\), periods \(`.`\), and underscores \(`_`\)\. It can be up to 63 characters long\.
Optionally, the taint key can begin with a DNS subdomain prefix and a single `/`\. If it begins with a DNS subdomain prefix, it can be 253 characters long\.
The value is optional and must begin with a letter or number\. It can contain letters, numbers, hyphens \(`-`\), periods \(`.`\), and underscores \(`_`\)\. It can be up to 63 characters long\.
When using Kubernetes directly or the AWS Management Console, the taint effect must be `NoSchedule`, `PreferNoSchedule`, or `NoExecute`\. However, when using the AWS CLI or API, the taint effect must be `NO_SCHEDULE`, `PREFER_NO_SCHEDULE`, or `NO_EXECUTE`\.
A maximum of 50 taints are allowed per node group\.
If taints that were created using a managed node group are removed manually from a node, then Amazon EKS doesn't add the taints back to the node\. This is true even if the taints are specified in the managed node group configuration\.

You can use the [https://docs.aws.amazon.com/cli/latest/reference/eks/update-nodegroup-config.html](https://docs.aws.amazon.com/cli/latest/reference/eks/update-nodegroup-config.html) AWS CLI command to add, remove, or replace taints for managed node groups\.