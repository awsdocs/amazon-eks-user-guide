--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# What is Amazon EKS?<a name="what-is-eks"></a>

Amazon Elastic Kubernetes Service \(Amazon EKS\) is a managed service that eliminates the need to install, operate, and maintain your own Kubernetes control plane on Amazon Web Services \(AWS\)\. [Kubernetes](https://kubernetes.io/docs/concepts/overview/) is an open\-source system that automates the management, scaling, and deployment of containerized applications\.

## Features of Amazon EKS<a name="eks-features"></a>

The following are key features of Amazon EKS:

Secure networking and authenticationEasy cluster scalingManaged Kubernetes experienceHigh availabilityIntegration with AWS services  

For details about other features of Amazon EKS, see [Amazon EKS features](https://aws.amazon.com/eks/features)\.

## Get started with Amazon EKS<a name="how-eks-works"></a>

1.  **Create a cluster** – Start by creating your cluster using `eksctl`, AWS Management Console, AWS CLI, or one of the AWS SDKs\.

1.  **Choose your approach to compute resources** – Decide between AWS Fargate, Karpenter, managed node groups, and self\-managed nodes\.

1.  **Setup** – Set up the necessary controllers, drivers, and services\.

1.  **Deploy workloads** – Tailor your Kubernetes workloads to best utilize the resources and capabilities of your chosen node type\.

1.  **Management** – Oversee your workloads, integrating AWS services to streamline operations and enhance workload performance\. You can view information about your workloads using the AWS Management Console\.

![\[A basic flow diagram of the steps described previously.\]](http://docs.aws.amazon.com/eks/latest/userguide/images/what-is-eks.png)

## Pricing for Amazon EKS<a name="eks-pricing"></a>

An Amazon EKS cluster consists of a control plane and the [Amazon Elastic Compute Cloud](https://aws.amazon.com/ec2/) \(Amazon EC2\) or Fargate compute that you run Pods on\. For more information about pricing for the control plane, see [Amazon EKS pricing](https://aws.amazon.com/eks/pricing)\. Both Amazon EC2 and Fargate provide:

On\-Demand Instances  
+ Pay for the instances that you use by the second, with no long\-term commitments or upfront payments\.For more information, see [Amazon EC2 On\-Demand Pricing](https://aws.amazon.com/ec2/pricing/on-demand/) and [AWS Fargate Pricing](https://aws.amazon.com/fargate/pricing/)\.

:: :: \* You can reduce your costs by making a commitment to a consistent amount of usage, in USD per hour, for a term of one or three years\.For more information, see [Pricing with Savings Plans](https://aws.amazon.com/savingsplans/pricing/)\.