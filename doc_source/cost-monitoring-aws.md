# View costs by pod in AWS billing with split cost allocation<a name="cost-monitoring-aws"></a>

**Cost monitoring using AWS split cost allocation data for Amazon EKS**  
You can use AWS split cost allocation data for Amazon EKS to get granular cost visibility for your Amazon EKS clusters\. This enables you to analyze, optimize, and chargeback cost and usage for your Kubernetes applications\. You allocate application costs to individual business units and teams based on Amazon EC2 CPU and memory resources consumed by your Kubernetes application\. Split cost allocation data for Amazon EKS gives visibility into cost per Pod, and enables you to aggregate the cost data per Pod using namespace, cluster, and other Kubernetes primitives\. The following are examples of Kubernetes primitives that you can use to analyze Amazon EKS cost allocation data\. 
+  Cluster name 
+  Deployment 
+  Namespace 
+  Node 
+  Workload Name 
+  Workload Type 

For more information about using split cost allocation data, see [Understanding split cost allocation data](https://docs.aws.amazon.com/cur/latest/userguide/split-cost-allocation-data.html) in the AWS Billing User Guide\.

## Set up Cost and Usage Reports<a name="task-cur-setup"></a>

You can turn on Split Cost Allocation Data for EKS in the Cost Management Console, AWS Command Line Interface, or the AWS SDKs\.

Use the following for *Split Cost Allocation Data*:

1. Opt in to Split Cost Allocation Data\. For more information, see [Enabling split cost allocation data](https://docs.aws.amazon.com/cur/latest/userguide/enabling-split-cost-allocation-data.html) in the AWS Cost and Usage Report User Guide\.

1. Include the data in a new or existing report\.

1. View the report\. You can use the Billing and Cost Management console or view the report files in Amazon Simple Storage Service\.