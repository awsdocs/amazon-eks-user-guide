# What is Amazon EKS?<a name="what-is-eks"></a>

Amazon Elastic Kubernetes Service \(Amazon EKS\) is a managed service that makes it easy for you to run Kubernetes on AWS without needing to stand up or maintain your own Kubernetes control plane\. Kubernetes is an open\-source system for automating the deployment, scaling, and management of containerized applications\. 

Amazon EKS runs Kubernetes control plane instances across multiple Availability Zone to ensure high availability\. Amazon EKS automatically detects and replaces unhealthy control plane instances, and it provides automated version upgrades and patching for them\.

Amazon EKS is also integrated with many AWS services to provide scalability and security for your applications, including the following: 
+ Amazon ECR for container images
+ Elastic Load Balancing for load distribution
+ IAM for authentication
+ Amazon VPC for isolation

Amazon EKS runs up\-to\-date versions of the open\-source Kubernetes software, so you can use all the existing plugins and tooling from the Kubernetes community\. Applications running on Amazon EKS are fully compatible with applications running on any standard Kubernetes environment, whether running in on\-premises data centers or public clouds\. This means that you can easily migrate any standard Kubernetes application to Amazon EKS without any code modification required\.

## Amazon EKS control plane architecture<a name="eks-architecture"></a>

Amazon EKS runs a single tenant Kubernetes control plane for each cluster, and control plane infrastructure is not shared across clusters or AWS accounts\.

This control plane consists of at least two API server nodes and three `etcd` nodes that run across three Availability Zones within a Region\. Amazon EKS automatically detects and replaces unhealthy control plane instances, restarting them across the Availability Zones within the Region as needed\. Amazon EKS leverages the architecture of AWS Regions in order to maintain high availability\. Because of this, Amazon EKS is able to offer an [SLA for API server endpoint availability](http://aws.amazon.com/eks/sla)\.

Amazon EKS uses Amazon VPC network policies to restrict traffic between control plane components to within a single cluster\. Control plane components for a cluster cannot view or receive communication from other clusters or other AWS accounts, except as authorized with Kubernetes RBAC policies\.

This secure and highly\-available configuration makes Amazon EKS reliable and recommended for production workloads\.

## How does Amazon EKS work?<a name="how-eks-works"></a>

![\[How Amazon EKS works\]](http://docs.aws.amazon.com/eks/latest/userguide/images/what-is-eks.png)

Getting started with Amazon EKS is easy:

1. First, create an Amazon EKS cluster in the AWS Management Console or with the AWS CLI or one of the AWS SDKs\.

1. Then, launch worker nodes that register with the Amazon EKS cluster\. We provide you with an AWS CloudFormation template that automatically configures your nodes\.

1. When your cluster is ready, you can configure your favorite Kubernetes tools \(such as kubectl\) to communicate with your cluster\.

1. Deploy and manage applications on your Amazon EKS cluster the same way that you would with any other Kubernetes environment\.

For more information about creating your required resources and your first Amazon EKS cluster, see [Getting started with Amazon EKS](getting-started.md)\.