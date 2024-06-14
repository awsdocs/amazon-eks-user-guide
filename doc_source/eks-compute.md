--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Amazon EKS nodes<a name="eks-compute"></a>

A Kubernetes node is a machine that runs containerized applications\. Each node has the following components:
+  ** [Container runtime](https://kubernetes.io/docs/setup/production-environment/container-runtimes/) ** – Software that’s responsible for running the containers\.
+  ** [kubelet](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/) ** – Makes sure that containers are healthy and running within their associated Pod\.
+  ** [kube\-proxy](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/) ** – Maintains network rules that allow communication to your Pods\.

For more information, see [Nodes](https://kubernetes.io/docs/concepts/architecture/nodes/) in the Kubernetes documentation\.

**Important**  
 AWS Fargate with Amazon EKS isn’t available in AWS GovCloud \(US\-East\) and AWS GovCloud \(US\-West\)\.

**Note**  
Nodes must be in the same VPC as the subnets you selected when you created the cluster\. However, the nodes don’t have to be in the same subnets\.

**Note**  
 Bottlerocket has some specific differences from the general information in this table\. For more information, see the Bottlerocket [documentation](https://github.com/bottlerocket-os/bottlerocket/blob/develop/README.md) on GitHub\.

Can be deployed to [AWS Outposts](https://docs.aws.amazon.com/outposts/latest/userguide/what-is-outposts.html) 

No

Yes

No

Can be deployed to an [AWS Local Zone](https://aws.amazon.com/about-aws/global-infrastructure/localzones/) 

No

No

Can run containers that require Windows 

Yes

No

Can run containers that require Linux 

Yes

Yes

Yes

Can run workloads that require the Inferentia chip

No

Can run workloads that require a GPU

Can run workloads that require Arm processors

No

Yes

No

Yes – All of your Pods on each of your nodes

Yes – All of your Pods on each of your nodes

No – Each Pod has a dedicated kernel

Pods share CPU, memory, storage, and network resources with other Pods\.

Yes – Can result in unused resources on each node

Yes – Can result in unused resources on each node

No – Each Pod has dedicated resources and can be sized independently to maximize resource utilization\.

Pods can use more hardware and memory than requested in Pod specs

Yes – If the Pod requires more resources than requested, and resources are available on the node, the Pod can use additional resources\.

No – The Pod can be re\-deployed using a larger vCPU and memory configuration though\.

Must deploy and manage Amazon EC2 instances

No

Must secure, maintain, and patch the operating system of Amazon EC2 instances

Yes

Yes

No

Can provide bootstrap arguments at deployment of a node, such as extra [kubelet](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/) arguments\.

Yes – For more information, see the [bootstrap script usage information](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) on GitHub\.

No

Can SSH into node

Yes

Yes

No – There’s no node host operating system to SSH to\.

Can deploy your own custom AMI to nodes

Yes

No

Can deploy your own custom CNI to nodes

Yes

No

Must update node AMI on your own

No

Can use Amazon EBS storage with Pods 

No

Can use Amazon EFS storage with Pods 

Can use Amazon FSx for Lustre storage with Pods 

No

Can use Network Load Balancer for services

Pods can run in a public subnet

Yes

Yes

No

Can assign different VPC security groups to individual Pods 

Yes

Can run Kubernetes DaemonSets 

Yes

Yes

No

Support `HostPort` and `HostNetwork` in the Pod manifest

Yes

Yes

No

 AWS Region availability

 [All Amazon EKS supported regions](https://docs.aws.amazon.com/general/latest/gr/eks.html) 

 [All Amazon EKS supported regions](https://docs.aws.amazon.com/general/latest/gr/eks.html) 

Can run containers on Amazon EC2 dedicated hosts

Yes

Yes

No

Pricing

Cost of Amazon EC2 instance that runs multiple Pods\. For more information, see [Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/)\.

Cost of Amazon EC2 instance that runs multiple Pods\. For more information, see [Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/)\.

Cost of an individual Fargate memory and CPU configuration\. Each Pod has its own cost\. For more information, see [AWS Fargate pricing](https://aws.amazon.com/fargate/pricing/)\.