# Amazon EKS nodes<a name="eks-compute"></a>

A Kubernetes node is a machine that runs containerized applications\. Each node has the following components:
+ **[Container runtime](https://kubernetes.io/docs/setup/production-environment/container-runtimes/)** – Software that's responsible for running the containers\.
+ **[https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/)** – Makes sure that containers are healthy and running within their associated Pod\.
+ **[https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/)** – Maintains network rules that allow communication to your Pods\.

For more information, see [Nodes](https://kubernetes.io/docs/concepts/architecture/nodes/) in the Kubernetes documentation\.

Your Amazon EKS cluster can schedule Pods on any combination of [self\-managed nodes](worker.md), [Amazon EKS managed node groups](managed-node-groups.md), and [AWS Fargate](fargate.md)\. To learn more about nodes deployed in your cluster, see [View Kubernetes resources](view-kubernetes-resources.md)\.

**Important**  
AWS Fargate with Amazon EKS isn't available in AWS GovCloud \(US\-East\) and AWS GovCloud \(US\-West\)\.

**Note**  
Nodes must be in the same VPC as the subnets you selected when you created the cluster\. However, the nodes don't have to be in the same subnets\.

The following table provides several criteria to evaluate when deciding which options best meet your requirements\. This table doesn't include [connected nodes](eks-connector.md) that were created outside of Amazon EKS, which can only be viewed\.

**Note**  
Bottlerocket has some specific differences from the general information in this table\. For more information, see the Bottlerocket [documentation](https://github.com/bottlerocket-os/bottlerocket/blob/develop/README.md) on GitHub\.


| Criteria | EKS managed node groups | Self managed nodes | AWS Fargate | 
| --- | --- | --- | --- | 
|  Can be deployed to [AWS Outposts](https://docs.aws.amazon.com/outposts/latest/userguide/what-is-outposts.html)  |  No  |  Yes  |  No  | 
|  Can be deployed to an [AWS Local Zone](https://aws.amazon.com/about-aws/global-infrastructure/localzones/)  |  No  |  Yes – For more information, see [Amazon EKS and AWS Local Zones](local-zones.md)\.  |  No  | 
|  Can run containers that require Windows  |  Yes  |  [Yes](windows-support.md) – Your cluster still requires at least one \(two recommended for availability\) Linux node though\.  |  No  | 
|  Can run containers that require Linux  |  Yes  |  Yes  |  Yes  | 
|  Can run workloads that require the Inferentia chip  |  [Yes](inferentia-support.md) – Amazon Linux nodes only  |  [Yes](inferentia-support.md) – Amazon Linux only  |  No  | 
|  Can run workloads that require a GPU  |  [Yes](eks-optimized-ami.md#gpu-ami) – Amazon Linux nodes only  |  [Yes](eks-optimized-ami.md#gpu-ami) – Amazon Linux only  | No | 
|  Can run workloads that require Arm processors  |  [Yes](eks-optimized-ami.md#arm-ami)  |  [Yes](eks-optimized-ami.md#arm-ami)  |  No  | 
| Can run AWS [Bottlerocket](https://aws.amazon.com/bottlerocket/) |  Yes  |  [Yes](launch-node-bottlerocket.md)  |  No  | 
| Pods share a kernel runtime environment with other Pods |  Yes – All of your Pods on each of your nodes  |  Yes – All of your Pods on each of your nodes  |  No – Each Pod has a dedicated kernel  | 
|  Pods share CPU, memory, storage, and network resources with other Pods\.  |  Yes – Can result in unused resources on each node  |  Yes – Can result in unused resources on each node  |  No – Each Pod has dedicated resources and can be sized independently to maximize resource utilization\.   | 
|  Pods can use more hardware and memory than requested in Pod specs  |  Yes – If the Pod requires more resources than requested, and resources are available on the node, the Pod can use additional resources\.  | Yes – If the Pod requires more resources than requested, and resources are available on the node, the Pod can use additional resources\. |  No – The Pod can be re\-deployed using a larger vCPU and memory configuration though\.  | 
|  Must deploy and manage Amazon EC2 instances  |  [Yes](create-managed-node-group.md) – automated through Amazon EKS if you deployed an Amazon EKS optimized AMI\. If you deployed a custom AMI, then you must update the instance manually\.  |  Yes – Manual configuration or using Amazon EKS provided AWS CloudFormation templates to deploy [Linux \(x86\)](launch-workers.md), [Linux \(Arm\)](eks-optimized-ami.md#arm-ami), or [Windows](windows-support.md) nodes\.  |  No  | 
|  Must secure, maintain, and patch the operating system of Amazon EC2 instances  |  Yes  |  Yes  |  No  | 
|  Can provide bootstrap arguments at deployment of a node, such as extra [https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/) arguments\.  | Yes – Using eksctl or a [launch template](launch-templates.md) with a custom AMI |  Yes – For more information, see the [bootstrap script usage information](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) on GitHub\.  |  No  | 
| Can assign IP addresses to Pods from a different CIDR block than the IP address assigned to the node\. | Yes – Using a launch template with a custom AMI\. For more information, see [Customizing managed nodes with launch templates](launch-templates.md)\. | Yes – For more information, see [Custom networking for pods](cni-custom-network.md)\. | No | 
|  Can SSH into node  |  Yes  |  Yes  |  No – There's no node host operating system to SSH to\.  | 
|  Can deploy your own custom AMI to nodes  |  Yes – Using a [launch template](launch-templates.md)  |  Yes  |  No  | 
|  Can deploy your own custom CNI to nodes  |  Yes – Using a [launch template](launch-templates.md) with a custom AMI  |  Yes  |  No  | 
|  Must update node AMI on your own  |  [Yes](update-managed-node-group.md) – If you deployed an Amazon EKS optimized AMI, you're notified in the Amazon EKS console when updates are available\. You can perform the update with one\-click in the console\. If you deployed a custom AMI, you're not notified in the Amazon EKS console when updates are available\. You must perform the update on your own\.  |  [Yes](update-stack.md) – Using tools other than the Amazon EKS console\. This is because self managed nodes can't be managed with the Amazon EKS console\.  |  No  | 
| Must update node Kubernetes version on your own |  [Yes](update-managed-node-group.md) – If you deployed an Amazon EKS optimized AMI, you're notified in the Amazon EKS console when updates are available\. You can perform the update with one\-click in the console\. If you deployed a custom AMI, you're not notified in the Amazon EKS console when updates are available\. You must perform the update on your own\.  |  [Yes](update-stack.md) – Using tools other than the Amazon EKS console\. This is because self managed nodes can't be managed with the Amazon EKS console\.  | No – You don't manage nodes\. | 
|  Can use Amazon EBS storage with Pods  |  [Yes](ebs-csi.md)  |  [Yes](ebs-csi.md)  |  No  | 
|  Can use Amazon EFS storage with Pods  |  [Yes](efs-csi.md)  |  [Yes](efs-csi.md)  |  [Yes](efs-csi.md)  | 
|  Can use Amazon FSx for Lustre storage with Pods  |  [Yes](fsx-csi.md)  |  [Yes](fsx-csi.md)  |  No  | 
|  Can use Network Load Balancer for services  |  [Yes](network-load-balancing.md)  |  [Yes](network-load-balancing.md)  |  Yes, when using the [Create a network load balancer](network-load-balancing.md#network-load-balancer)  | 
|  Pods can run in a public subnet  |  Yes  |  Yes  |  No  | 
|  Can assign different VPC security groups to individual Pods  |  [Yes](security-groups-for-pods.md) – Linux nodes only  | [Yes](security-groups-for-pods.md) – Linux nodes only |  Yes  | 
|  Can run Kubernetes DaemonSets  |  Yes  |  Yes  |  No  | 
|  Support `HostPort` and `HostNetwork` in the Pod manifest  |  Yes  |  Yes  |  No  | 
|  AWS Region availability  |  [All Amazon EKS supported regions](https://docs.aws.amazon.com/general/latest/gr/eks.html)  |  [All Amazon EKS supported regions](https://docs.aws.amazon.com/general/latest/gr/eks.html)  |  [Some Amazon EKS supported regions](fargate.md)  | 
|  Can run containers on Amazon EC2 dedicated hosts  |  Yes  |  Yes  |  No  | 
|  Pricing  |  Cost of Amazon EC2 instance that runs multiple Pods\. For more information, see [Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/)\.  |  Cost of Amazon EC2 instance that runs multiple Pods\. For more information, see [Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/)\.  |  Cost of an individual Fargate memory and CPU configuration\. Each Pod has its own cost\. For more information, see [AWS Fargate pricing](https://aws.amazon.com/fargate/pricing/)\.  | 