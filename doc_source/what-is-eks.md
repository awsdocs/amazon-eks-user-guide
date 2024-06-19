# What is Amazon EKS?<a name="what-is-eks"></a>

Amazon Elastic Kubernetes Service \(Amazon EKS\) is a managed service that eliminates the need to install, operate, and maintain your own Kubernetes control plane on Amazon Web Services \(AWS\)\. [https://kubernetes.io/docs/concepts/overview/](https://kubernetes.io/docs/concepts/overview/) is an open\-source system that automates the management, scaling, and deployment of containerized applications\.

## Features of Amazon EKS<a name="eks-features"></a>

The following are key features of Amazon EKS:

**Secure networking and authentication**  
Amazon EKS integrates your Kubernetes workloads with AWS [ networking](eks-networking.md) and security services\. It also integrates with AWS Identity and Access Management \(IAM\) to provide [authentication](cluster-auth.md) for your Kubernetes clusters\.

**Easy cluster scaling**  
Amazon EKS enables you to scale your Kubernetes clusters up and down easily based on the demand of your workloads\. Amazon EKS supports [horizontal Pod autoscaling](horizontal-pod-autoscaler.md) based on CPU or custom metrics, and [cluster autoscaling](autoscaling.md) based on the demand of the entire workload\.

**Managed Kubernetes experience**  
You can make changes to your Kubernetes clusters using `[https://eksctl.io/](https://eksctl.io/)`, [AWS Management Console](https://console.aws.amazon.com/eks/), [AWS Command Line Interface \(AWS CLI\)](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/eks/index.html), [the API](https://docs.aws.amazon.com/eks/latest/APIReference/Welcome.html), [`kubectl`](install-kubectl.md), and [Terraform](https://tf-eks-workshop.workshop.aws/)\.

**High availability**  
Amazon EKS provides [high availability](disaster-recovery-resiliency.md) for your control plane across multiple Availability Zones\.

**Integration with AWS services**  
Amazon EKS integrates with other [AWS services](eks-integrations.md), providing a comprehensive platform for deploying and managing your containerized applications\. You can also more easily troubleshoot your Kubernetes workloads with various [observability](eks-observe.md) tools\.

For details about other features of Amazon EKS, see [Amazon EKS features](https://aws.amazon.com/eks/features)\.

## Get started with Amazon EKS<a name="how-eks-works"></a>

To create your first cluster and its associated resources, see [Getting started with Amazon EKS](getting-started.md)\. In general, getting started with Amazon EKS involves the following steps\.

1. **Create a cluster** – Start by creating your cluster using `eksctl`, AWS Management Console, AWS CLI, or one of the AWS SDKs\.

1. **Choose your approach to compute resources** – Decide between AWS Fargate, Karpenter, managed node groups, and self\-managed nodes\.

1. **Setup** – Set up the necessary controllers, drivers, and services\. 

1. **Deploy workloads** – Tailor your Kubernetes workloads to best utilize the resources and capabilities of your chosen node type\.

1. **Management** – Oversee your workloads, integrating AWS services to streamline operations and enhance workload performance\. You can view information about your workloads using the AWS Management Console\.

The following diagram shows a basic flow of running Amazon EKS in the cloud\. To learn about other Kubernetes deployment options, see [Deployment options](eks-deployment-options.md)\.

![\[A basic flow diagram of the steps described previously.\]](http://docs.aws.amazon.com/eks/latest/userguide/images/what-is-eks.png)

## Pricing for Amazon EKS<a name="eks-pricing"></a>

An Amazon EKS cluster consists of a control plane and the [Amazon Elastic Compute Cloud](https://aws.amazon.com/ec2/) \(Amazon EC2\) or Fargate compute that you run Pods on\. For more information about pricing for the control plane, see [Amazon EKS pricing](https://aws.amazon.com/eks/pricing)\. Both Amazon EC2 and Fargate provide:

**On\-Demand Instances**  
Pay for the instances that you use by the second, with no long\-term commitments or upfront payments\. For more information, see [Amazon EC2 On\-Demand Pricing](https://aws.amazon.com/ec2/pricing/on-demand/) and [AWS Fargate Pricing](https://aws.amazon.com/fargate/pricing/)\.

**Savings Plans**  
You can reduce your costs by making a commitment to a consistent amount of usage, in USD per hour, for a term of one or three years\. For more information, see [Pricing with Savings Plans](https://aws.amazon.com/savingsplans/pricing/)\.