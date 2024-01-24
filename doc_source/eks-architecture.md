# Amazon EKS architecture<a name="eks-architecture"></a>

Amazon EKS aligns with the general cluster architecture of Kubernetes\. For more information, see [Kubernetes Components](https://kubernetes.io/docs/concepts/overview/components/) in the Kubernetes documentation\. The following sections summarize some extra architecture details for Amazon EKS\.

## Control plane<a name="control-plane"></a>

Amazon EKS ensures every cluster has its own unique Kubernetes control plane\. This design keeps each cluster's infrastructure separate, with no overlaps between clusters or AWS accounts\. The setup includes:

**Distributed components**  
The control plane positions at least two API server instances and three [https://etcd.io/](https://etcd.io/) instances across three AWS Availability Zones within an AWS Region\.

**Optimal performance**  
Amazon EKS actively monitors and adjusts control plane instances to maintain peak performance\.

**Resilience**  
If a control plane instance falters, Amazon EKS quickly replaces it, using different Availability Zone if needed\.

**Consistent uptime**  
By running clusters across multiple Availability Zones, a reliable [API server endpoint availability Service Level Agreement \(SLA\)](https://aws.amazon.com/eks/sla) is achieved\.

Amazon EKS uses Amazon Virtual Private Cloud \(Amazon VPC\) to limit traffic between control plane components within a single cluster\. Cluster components can't view or receive communication from other clusters or AWS accounts, except when authorized by Kubernetes role\-based access control \(RBAC\) policies\.

## Compute<a name="nodes"></a>

In addition to the control plane, an Amazon EKS cluster has a set of worker machines called nodes\. Selecting the appropriate Amazon EKS cluster node type is crucial for meeting your specific requirements and optimizing resource utilization\. Amazon EKS offers the following primary node types:

**AWS Fargate**  
[Fargate](fargate.md) is a serverless compute engine for containers that eliminates the need to manage the underlying instances\. With Fargate, you specify your application's resource needs, and AWS automatically provisions, scales, and maintains the infrastructure\. This option is ideal for users who prioritize ease\-of\-use and want to concentrate on application development and deployment rather than managing infrastructure\.

**Karpenter**  
[https://karpenter.sh/](https://karpenter.sh/) is a flexible, high\-performance Kubernetes cluster autoscaler that helps improve application availability and cluster efficiency\. Karpenter launches right\-sized compute resources in response to changing application load\. This option can provision just\-in\-time compute resources that meet the requirements of your workload\.

**Managed node groups**  
[Managed node groups](managed-node-groups.md) are a blend of automation and customization for managing a collection of Amazon EC2 instances within an Amazon EKS cluster\. AWS takes care of tasks like patching, updating, and scaling nodes, easing operational aspects\. In parallel, custom `kubelet` arguments are supported, opening up possibilities for advanced CPU and memory management policies\. Moreover, they enhance security via AWS Identity and Access Management \(IAM\) roles for service accounts, while curbing the need for separate permissions per cluster\.

**Self\-managed nodes**  
[Self\-managed nodes](worker.md) offer full control over your Amazon EC2 instances within an Amazon EKS cluster\. You are in charge of managing, scaling, and maintaining the nodes, giving you total control over the underlying infrastructure\. This option is suitable for users who need granular control and customization of their nodes and are ready to invest time in managing and maintaining their infrastructure\.