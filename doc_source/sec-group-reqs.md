# Amazon EKS security group considerations<a name="sec-group-reqs"></a>

The following sections describe the minimum required and recommended security group settings for the cluster, control plane, and node security groups for your cluster, depending on your Kubernetes version and Amazon EKS platform version\.

## Cluster security group \(available starting with Amazon EKS clusters running Kubernetes 1\.14 and `eks.3` platform version\)<a name="cluster-sg"></a>

Amazon EKS clusters beginning with Kubernetes version 1\.14 and [platform version](platform-versions.md) `eks.3` create a cluster security group as part of cluster creation \(or when a cluster is upgraded to this Kubernetes version and platform version\)\. This security group is designed to allow all traffic from the control plane and [managed node groups](managed-node-groups.md) to flow freely between each other\. By assigning the cluster security group to the control plane cross\-account elastic network interfaces and the managed node group instances, you do not need to configure complex security group rules to allow this communication\. Any instance or network interface that is assigned this security group can freely communicate with other resources with this security group\.

You can check for a cluster security group for your cluster in the AWS Management Console under the cluster's **Networking** section, or with the following AWS CLI command:

```
aws eks describe-cluster --name cluster_name --query cluster.resourcesVpcConfig.clusterSecurityGroupId
```

If your cluster is running Kubernetes version 1\.14 and [platform version](platform-versions.md) `eks.3` or later, then we recommend that you add the cluster security group to all existing and future node groups\. For more information, see [Security Groups for Your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html) in the *Amazon VPC User Guide*\. Amazon EKS [managed node groups](managed-node-groups.md) are automatically configured to use the cluster security group\.


|  | Protocol | Ports | Source | Destination | 
| --- | --- | --- | --- | --- | 
|  Recommended inbound traffic  |  All  |  All  | Self |  | 
|  Recommended outbound traffic  |  All  |  All  |  |  0\.0\.0\.0/0  | 

**Restricting cluster traffic**  
If you need to limit the open ports between the control plane and nodes, the default cluster security group can be modified to allow only the following required minimum ports\. The required minimum ports are the same as they were in previous Amazon EKS versions\. 


|  | Protocol | Port | Source | Destination | 
| --- | --- | --- | --- | --- | 
| Minimum inbound traffic | TCP |  443  | Cluster security group |  | 
| Minimum inbound traffic\* | TCP |  10250  | Cluster security group |  | 
| Minimum outbound traffic | TCP |  443  |  |  Cluster security group  | 
| Minimum outbound traffic\* | TCP |  10250  |  |  Cluster security group  | 

\*Any protocol and ports that you expect your nodes to use for inter\-node communication should be included, if required\. Nodes also require outbound internet access to the Amazon EKS APIs for cluster introspection and node registration at launch time, or that you've implemented the required necessary settings in [Private clusters](private-clusters.md)\. To pull container images, they require access to Amazon S3, Amazon ECR APIs, and any other container registries that they need to pull images from, such as DockerHub\. For more information, see [AWS IP address ranges](https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html) in the AWS General Reference\.

## Control plane and node security groups \(for Amazon EKS clusters earlier than Kubernetes version 1\.14 and [platform version](platform-versions.md) `eks.3`\)<a name="control-plane-worker-node-sgs"></a>

For Amazon EKS clusters earlier than Kubernetes version 1\.14 and [platform version](platform-versions.md) `eks.3`, control plane to node communication is configured by manually creating a control plane security group and specifying that security group when you create the cluster\. At cluster creation, this security group is then attached to the cross\-account elastic network interfaces for the cluster\.

**Note**  
If you used the API directly, or a tool such as AWS CloudFormation to create your cluster and didn't specify a security group, then the default security group for the VPC was applied to the control plane cross\-account elastic network interfaces\.

You can check the control plane security group for your cluster in the AWS Management Console under the cluster's **Networking** section \(listed as **Additional security groups**\), or with the following AWS CLI command:

```
aws eks describe-cluster --name cluster_name --query cluster.resourcesVpcConfig.securityGroupIds
```

If you launch nodes with the AWS CloudFormation template in the [Getting started with Amazon EKS](getting-started.md) walkthrough, AWS CloudFormation modifies the control plane security group to allow communication with the nodes\. **Amazon EKS strongly recommends that you use a dedicated security group for each control plane \(one per cluster\)**\. If you share a control plane security group with other Amazon EKS clusters or resources, you may block or disrupt connections to those resources\.

The security group for the nodes and the security group for the control plane communication to the nodes have been set up to prevent communication to privileged ports in the nodes\. If your applications require added inbound or outbound access from the control plane or nodes, you must add these rules to the security groups associated with your cluster\. For more information, see [Security Groups for Your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html) in the *Amazon VPC User Guide*\.

**Note**  
To allow proxy functionality on privileged ports or to run the CNCF conformance tests yourself, you must edit the security groups for your control plane and the nodes\. The security group on the nodes' side needs to allow inbound access for ports 0\-65535 from the control plane, and the control plane side needs to allow outbound access to the nodes on ports 0\-65535\.


**Control Plane Security Group**  

|  | Protocol | Port range | Source | Destination | 
| --- | --- | --- | --- | --- | 
| Minimum inbound traffic |  TCP  |  443  |  All node security groups **When [cluster endpoint private access](cluster-endpoint.md) is enabled:** Any security groups that generate API server client traffic \(such as `kubectl` commands on a bastion host within your cluster's VPC\)  |  | 
| Recommended inbound traffic |  TCP  |  443  |  All node security groups **When [cluster endpoint private access](cluster-endpoint.md) is enabled:** Any security groups that generate API server client traffic \(such as `kubectl` commands on a bastion host within your cluster's VPC\)  |  | 
| Minimum outbound traffic |  TCP  |  10250  |  |  All node security groups  | 
| Recommended outbound traffic |  TCP  |  1025\-65535  |  |  All node security groups  | 


**Node security group**  

|  | Protocol | Port range | Source | Destination | 
| --- | --- | --- | --- | --- | 
| Minimum inbound traffic \(from other nodes\) |  Any protocol that you expect your nodes to use for inter\-node communication  |  Any ports that you expect your nodes to use for inter\-node communication  |  All node security groups  |  | 
| Minimum inbound traffic \(from control plane\) |  TCP  |  10250  |  Control plane security group  |  | 
| Recommended inbound traffic |  All TCP  |  All 443, 1025\-65535  |  All node security groups Control plane security group  |  | 
| Minimum outbound traffic\* |  TCP  |  443  |  |  Control plane security group  | 
| Recommended outbound traffic |  All  |  All  |  |  0\.0\.0\.0/0  | 

\*Nodes also require access to the Amazon EKS APIs for cluster introspection and node registration at launch time either through the internet or VPC endpoints\. To pull container images, they require access to the Amazon S3 and Amazon ECR APIs \(and any other container registries, such as DockerHub\)\. For more information, see [AWS IP address ranges](https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html) in the *AWS General Reference* and [Private clusters](private-clusters.md)\.

If you have more than one security group associated to your nodes, then one of the security groups must have the following tag applied to it\. If you have only one security group associated to your nodes, then the tag is optional\. For more information about tagging, see [Working with tags using the console](eks-using-tags.md#tag-resources-console)\.


| Key | Value | 
| --- | --- | 
| `kubernetes.io/cluster/<cluster-name>` | `owned` | 