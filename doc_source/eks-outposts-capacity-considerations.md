# Capacity considerations<a name="eks-outposts-capacity-considerations"></a>

This topic provides guidance for selecting the Kubernetes control plane instance type for your local Amazon EKS cluster on an Outpost\.

Before you select an instance type \(such as `m5`, `c5`, or `r5`\) to use for your local cluster’s Kubernetes control plane on Outposts, confirm the instance types that are available on your Outpost configuration\. After you identify the available instance types, select the instance size \(such as `large`, `xlarge`, or `2xlarge`\) based on the number of nodes that your workloads require\. The following table provides recommendations for choosing an instance size\.

**Note**  
The instance sizes must be slotted on your Outposts\. Make sure that you have enough capacity for three instances of the size available on your Outposts for the lifetime of your local cluster\. For a list of the available Amazon EC2 instance types, see the Compute and storage sections in [AWS Outposts rack features](http://aws.amazon.com/outposts/rack/features/)\.


| Number of nodes | Kubernetes control plane instance size | 
| --- | --- | 
| 1–20 | `large` | 
| 21–100 | `xlarge` | 
| 101–250 | `2xlarge` | 
| 251–500 | `4xlarge` | 

The storage for the Kubernetes control plane requires 246 GB of Amazon EBS storage for each local cluster to meet `etcd`’s required IOPS\. When the local cluster is created, the Amazon EBS volumes are provisioned automatically for you\.