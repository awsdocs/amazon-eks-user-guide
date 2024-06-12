# Capacity considerations<a name="eks-outposts-capacity-considerations"></a>

This topic provides guidance for selecting the Kubernetes control plane instance type and \(optionally\) using placement groups to meet high\-availability requirements for your local Amazon EKS cluster on an Outpost\.

Before you select an instance type \(such as `m5`, `c5`, or `r5`\) to use for your local cluster's Kubernetes control plane on Outposts, confirm the instance types that are available on your Outpost configuration\. After you identify the available instance types, select the instance size \(such as `large`, `xlarge`, or `2xlarge`\) based on the number of nodes that your workloads require\. The following table provides recommendations for choosing an instance size\.

**Note**  
The instance sizes must be slotted on your Outposts\. Make sure that you have enough capacity for three instances of the size available on your Outposts for the lifetime of your local cluster\. For a list of the available Amazon EC2 instance types, see the Compute and storage sections in [AWS Outposts rack features](https://aws.amazon.com/outposts/rack/features/)\.


| Number of nodes | Kubernetes control plane instance size | 
| --- | --- | 
| 1–20 | `large` | 
| 21–100 | `xlarge` | 
| 101–250 | `2xlarge` | 
| 251–500 | `4xlarge` | 

The storage for the Kubernetes control plane requires 246 GB of Amazon EBS storage for each local cluster to meet `etcd`'s required IOPS\. When the local cluster is created, the Amazon EBS volumes are provisioned automatically for you\.

## Control plane placement<a name="outpost-capacity-considerations-control-plane-placement"></a>

When you don't specify a placement group with the `OutpostConfig.ControlPlanePlacement.GroupName` property, the Amazon EC2 instances provisioned for your Kubernetes control plane don't receive any specific hardware placement enforcement across the underlying capacity available on your Outpost\.

You can use placement groups to meet the high\-availability requirements for your local Amazon EKS cluster on an Outpost\. By specifying a placement group during cluster creation, you influence the placement of the Kubernetes control plane instances\. The instances are spread across independent underlying hardware \(racks or hosts\), minimizing correlated instance impact on the event of hardware failures\.

**Requirements**

The type of spread that you can configure depends on the number of Outpost racks you have in your deployment\.
+ **Deployments with one or two physical racks in a single logical Outpost** – You must have at least three hosts that are configured with the instance type that you choose for your Kubernetes control plane instances\. A *spread* placement group using *host\-level spread* ensures that all Kubernetes control plane instances run on distinct hosts within the underlying racks available in your Outpost deployment\.
+ **Deployments with three or more physical racks in a single logical Outpost** – You must have at least three hosts configured with the instance type you choose for your Kubernetes control plane instances\. A *spread* placement group using *rack\-level spread* ensures that all Kubernetes control plane instances run on distinct racks in your Outpost deployment\. You can alternatively use the *host\-level spread* placement group as described in the previous option\.

You are responsible for creating the desired placement group\. You specify the placement group when calling the `CreateCluster` API\. For more information about placement groups and how to create them, see [Placement Groups](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html) in the Amazon EC2 User Guide for Linux Instances\.

**Considerations**
+ When a placement group is specified, there must be available slotted capacity on your Outpost to successfully create a local Amazon EKS cluster\. The capacity varies based on whether you use the host or rack spread type\. If there isn't enough capacity, the cluster remains in the `Creating` state\. You are able to check the `Insufficient Capacity Error` on the health field of the `[DescribeCluster](https://docs.aws.amazon.com/eks/latest/APIReference/API_DescribeCluster.html)` API response\. You must free capacity for the creation process to progress\.
+ During Amazon EKS local cluster platform and version updates, the Kubernetes control plane instances from your cluster are replaced by new instances using a rolling update strategy\. During this replacement process, each control plane instance is terminated, freeing up its respective slot\. A new updated instance is provisioned in its place\. The updated instance might be placed in the slot that was released\. If the slot is consumed by another unrelated instance and there is no more capacity left that respects the required spread topology requirement, then the cluster remains in the `Updating` state\. You are able to see the respective `Insufficient Capacity Error` on the health field of the `[DescribeCluster](https://docs.aws.amazon.com/eks/latest/APIReference/API_DescribeCluster.html)` API response\. You must free capacity so the update process can progress and reestablish prior high availability levels\.
+ You can create a maximum of 500 placement groups per account in each AWS Region\. For more information, see [General rules and limitations](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html#placement-groups-limitations-general) in the Amazon EC2 User Guide for Linux Instances\.