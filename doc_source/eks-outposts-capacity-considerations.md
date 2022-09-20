# Capacity considerations<a name="eks-outposts-capacity-considerations"></a>

This topic provides guidance for selecting the Kubernetes control plane instance type for your local Amazon EKS cluster on an Outpost\.

When selecting an instance type \(`m5`, `c5`, `r5`, or other\) to use for your local cluster’s Kubernetes control plane on Outposts, you must first confirm the instance types that are available on your Outpost configuration\. Once you have identified the available instance types, you must then select the instance size \(`large`, `xlarge`, `2xlarge`, or other\) based on the number of nodes that your workloads require\. The following table provides recommendations for choosing an instance size\.

**Note**  
The instance sizes must have been slotted on your Outposts, and you must have spare capacity for three instances of the size available on your Outposts for the lifetime of your local cluster\. For a list of the available Amazon EC2 instance types, see Compute and storage in [AWS Outposts rack features](http://aws.amazon.com/outposts/rack/features/)\.


| Number of nodes | Kubernetes control plane instance size | 
| --- | --- | 
| 1–20 | `large` | 
| 21–100 | `xlarge` | 
| 101–250 | `2xlarge` | 
| 251–500 | `4xlarge` | 

The storage for the Kubernetes control plane requires 246 GB of Amazon EBS storage per local cluster to meet `etcd`’s required IOPS\. The Amazon EBS volumes are provisioned automatically for you during local cluster creation\.