# View nodes<a name="view-nodes"></a>

The Amazon EKS console shows information about all of your cluster's nodes\. This includes Amazon EKS managed nodes, self managed nodes, connected nodes, and Fargate\. Nodes represent the compute resources provisioned for your cluster from the perspective of the Kubernetes API\. For more information, see [Nodes](https://kubernetes.io/docs/concepts/architecture/nodes/) in the Kubernetes documentation\. To learn more about the different types of Amazon EKS nodes that you can deploy your [workloads](view-workloads.md) to, see [Amazon EKS nodes](eks-compute.md)\.

**Prerequisites**

The IAM user or IAM role that you sign into the AWS Management Console with must meet the following requirements\.
+ Have the `eks:AccessKubernetesApi` and other necessary IAM permissions to view nodes attached to it\. For an example IAM policy, see [View nodes and workloads for all clusters in the AWS Management Console](security_iam_id-based-policy-examples.md#policy_example3)\.
+ For nodes in connected clusters, the Amazon EKS Connector Service account can impersonate the IAM or role in the cluster\. This allows the eks\-connector to map the IAM user or role to a Kubernetes user\. 
+ Is mapped to Kubernetes user or group in the `aws-auth` `configmap`\. For more information, see [Enabling IAM user and role access to your cluster](add-user-role.md)\.
+ The Kubernetes user or group that the IAM user or role is mapped to in the configmap must be bound to a Kubernetes `role` or `clusterrole`\. Additionally, this `role` or `clusterrole` must have the permissions to view the resources in the namespaces that you want to view\. For more information, see [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) in the Kubernetes documentation\. You can download the following example manifests that create a `clusterrole` and `clusterrolebinding` or a `role` and `rolebinding`:
  + **View Kubernetes resources in all namespaces** – The group name in the file is `eks-console-dashboard-full-access-group`\. It is the group that your IAM user or role must be mapped to in the `aws-auth` configmap\. You can change the name of the group before applying it to your cluster, if you want\. Then, you can map your IAM user or role to that group in the configmap\. To download the file, select the appropriate link for the AWS Region that your cluster is in\.
    + [All Regions other than Beijing and Ningxia China](https://amazon-eks.s3.us-west-2.amazonaws.com/docs/eks-console-full-access.yaml)
    + [Beijing and Ningxia China Regions](https://amazon-eks.s3.cn-north-1.amazonaws.com.cn/docs/eks-console-full-access.yaml)
  + **View Kubernetes resources in a specific namespace** – The namespace in this file is `default`\. So, if you want to specify a different namespace, edit the file before applying it to your cluster\. The group name in the file is `eks-console-dashboard-restricted-access-group`\. This is the group that your IAM user or role must be mapped to in the `aws-auth` configmap\. You can change the name of the group before applying it to your cluster, if you want\. Then, map your IAM user or role to that group in the configmap\. To download the file, select the appropriate link for the Region that your cluster is in\.
    + [All Regions other than Beijing and Ningxia China](https://amazon-eks.s3.us-west-2.amazonaws.com/docs/eks-console-restricted-access.yaml)
    + [Beijing and Ningxia China Regions](https://amazon-eks.s3.cn-north-1.amazonaws.com.cn/docs/eks-console-restricted-access.yaml)

**To view nodes using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation panel, select **Clusters**, and then in the **Clusters** list, select the cluster that you want to view compute resources for\.

1. On the **Overview** tab, you see a list of all compute **Nodes** for your cluster and the nodes' status\.
**Important**  
If you can't see any **Nodes** on the **Overview** tab, or you see a **Your current user or role does not have access to Kubernetes objects on this EKS cluster** error, see the prerequisites for this topic\. If you don't resolve the issue, you can still view and manage your Amazon EKS cluster on the **Configuration** tab\.
**Note**  
Each pod that runs on Fargate is registered as a separate Kubernetes node within the cluster\. This is because Fargate runs each pod in an isolated compute environment and independently connects to the cluster control plane\. For more information, see [AWS Fargate](fargate.md)\.

1. In the **Nodes** list, you see a list of all of the managed, self\-managed, connected, and Fargate nodes for your cluster\. Selecting the link for one of the nodes provides the following information about the node:
   + The Amazon EC2 **Instance type**, **Kernel version**, **Kubelet version**, **Container runtime**, **OS** and **OS image** for managed and self\-managed nodes\. Connected clusters don't display the **Instance type**\.
   + Deep links to the Amazon EC2 console and the Amazon EKS managed node group \(if applicable\) for the node\.
   + The **Resource allocation**, which shows baseline and allocatable capacity for the node\.
   + **Conditions** describe the current operational status of the node\. This is useful information for troubleshooting issues on the node\. 

     Conditions are reported back to the Kubernetes control plane by the Kubernetes agent `kubelet` that runs locally on each node\. For more information, see [kubelet](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/) in the Kubernetes documentation\. Conditions on the node are always reported as part of the node detail and the **Status** of each condition along with its **Message** indicates the health of the node for that condition\. The following common conditions are reported for a node:
     + **Ready** – This condition is **TRUE** if the node is healthy and can accept pods\. The condition is **FALSE** if the node isn't ready and can't accept pods\. **UNKNOWN** indicates that the Kubernetes control plane has not recently received a heartbeat signal from the node\. The heartbeat timeout period is set to the Kubernetes default of 40 seconds for Amazon EKS clusters\.
     + **Memory pressure** – This condition is **FALSE** under normal operation and **TRUE** if node memory is low\.
     + **Disk pressure** – This condition is **FALSE** under normal operation and **TRUE** if disk capacity for the node is low\.
     + **PID pressure** – This condition is **FALSE** under normal operation and **TRUE** if there are too many processes running on the node\. On the node, each container runs as a process with a unique *Process ID*, or PID\.
     + **NetworkUnavailable** – This condition is **FALSE**, or not present, under normal operation\. If **TRUE**, the network for the node isn't properly configured\.
   + The Kubernetes **Labels** and **Annotations** assigned to the node\. These could have been assigned by you, by Kubernetes, or by the Amazon EKS API when the node was created\. These values can be used by your workloads for scheduling pods\.