# Node taints on managed node groups<a name="node-taints-managed-node-groups"></a>

Amazon EKS supports configuring Kubernetes taints through managed node groups\. Taints and tolerations work together to ensure that pods aren't scheduled onto inappropriate nodes\.

One or more taints can be applied to a node\. This marks that the node shouldn't accept any pods that don't tolerate the taints\. Tolerations are applied to pods and allow, but don't require, the pods to schedule onto nodes with matching taints\.

Kubernetes node taints can be applied to new and existing managed node groups using the AWS Management Console or through the Amazon EKS API\.

The following is an example of creating a node group with a taint using the AWS CLI:

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

For more information on taints and tolerations, see the [Kubernetes documentation](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)\. For more information and examples of usage, see the [Kubernetes reference documentation](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#taint)\.

**Note**  
Maximum of 50 taints are allowed for one node group\.
Taints can be updated after you create the node group using the `UpdateNodegroupConfig` API\.
The taint key must begin with a letter or number\. It can contain letters, numbers, hyphens \(`-`\), periods \(`.`\), and underscores \(`_`\)\. It can be up to 63 characters long\.
Optionally, the taint key can begin with a DNS subdomain prefix and a single `/`\. If it begins with a DNS subdomain prefix, it can be 253 characters long\.
The value is optional and must begin with a letter or number\. It can contain letters, numbers, hyphens \(`-`\), periods \(`.`\), and underscores \(`_`\)\. It can be up to 63 characters long\.
The effect must be `NO_SCHEDULE`, `NO_EXECUTE`, or `PREFER_NO_SCHEDULE`\.