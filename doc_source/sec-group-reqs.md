# Amazon EKS security group requirements and considerations<a name="sec-group-reqs"></a>

This topic describes the security group requirements of an Amazon EKS cluster\.<a name="security-group-default-rules"></a>

When you create a cluster, Amazon EKS creates a security group that's named `eks-cluster-sg-my-cluster-uniqueID`\. This security group has the following default rules:


| Rule type | Protocol | Ports | Source | Destination | 
| --- | --- | --- | --- | --- | 
|  Inbound  |  All  |  All  | Self  |  | 
|  Outbound  |  All  |  All  |  |  0\.0\.0\.0/0 \(`IPv4`\) or ::/0 \(`IPv6`\)  | 

**Important**  
If your cluster doesn't need the outbound rule, you can remove it\. If you remove it, you must still have the minimum rules listed in [Restricting cluster traffic](#security-group-restricting-cluster-traffic)\. If you remove the inbound rule, Amazon EKS recreates it whenever the cluster is updated\.

Amazon EKS adds the following tags to the security group\. If you remove the tags, Amazon EKS adds them back to the security group whenever your cluster is updated\.


| Key | Value | 
| --- | --- | 
| kubernetes\.io/cluster/my\-cluster | owned | 
| aws:eks:cluster\-name | my\-cluster | 
| Name | eks\-cluster\-sg\-my\-cluster\-uniqueid | 

Amazon EKS automatically associates this security group to the following resources that it also creates:
+ 2–4 elastic network interfaces \(referred to for the rest of this document as *network interface*\) that are created when you create your cluster\.
+ Network interfaces of the nodes in any managed node group that you create\.

The default rules allow all traffic to flow freely between your cluster and nodes, and allows all outbound traffic to any destination\. When you create a cluster, you can \(optionally\) specify your own security groups\. If you do, then Amazon EKS also associates the security groups that you specify to the network interfaces that it creates for your cluster\. However, it doesn't associate them to any node groups that you create\.

You can determine the ID of your cluster security group in the AWS Management Console under the cluster's **Networking** section\. Or, you can do so by running the following AWS CLI command\.

```
aws eks describe-cluster --name my-cluster --query cluster.resourcesVpcConfig.clusterSecurityGroupId
```<a name="security-group-restricting-cluster-traffic"></a>

**Restricting cluster traffic**  
If you need to limit the open ports between the cluster and nodes, you can remove the [default outbound rule](#security-group-default-rules) and add the following minimum rules that are required for the cluster\. If you remove the [default inbound rule](#security-group-default-rules), Amazon EKS recreates it whenever the cluster is updated\.


| Rule type | Protocol | Port | Destination | 
| --- | --- | --- | --- | 
| Outbound | TCP |  443  |  Cluster security group  | 
| Outbound | TCP |  10250  |  Cluster security group  | 
| Outbound \(DNS\) | TCP and UDP | 53 | Cluster security group | 

You must also add rules for the following traffic:
+ Any protocol and ports that you expect your nodes to use for inter\-node communication\.
+ Outbound internet access so that nodes can access the Amazon EKS APIs for cluster introspection and node registration at launch time\. If your nodes don't have internet access, review [Private cluster requirements](private-clusters.md) for additional considerations\.
+ Node access to pull container images from Amazon ECR or other container registries APIs that they need to pull images from, such as DockerHub\. For more information, see [AWS IP address ranges](https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html) in the AWS General Reference\.
+ Node access to Amazon S3\.
+ Separate rules are required for `IPv4` and `IPv6` addresses\.

If you're considering limiting the rules, we recommend that you thoroughly test all of your Pods before you apply your changed rules to a production cluster\.

If you originally deployed a cluster with Kubernetes `1.14` and a platform version of `eks.3` or earlier, then consider the following:
+ You might also have control plane and node security groups\. When these groups were created, they included the restricted rules listed in the previous table\. These security groups are no longer required and can be removed\. However, you need to make sure your cluster security group contains the rules that those groups contain\.
+ If you deployed the cluster using the API directly or you used a tool such as the AWS CLI or AWS CloudFormation to create the cluster and you didn't specify a security group at cluster creation, then the default security group for the VPC was applied to the cluster network interfaces that Amazon EKS created\.