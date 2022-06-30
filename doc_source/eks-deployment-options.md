# Deployment options<a name="eks-deployment-options"></a>

You can use Amazon EKS with any, or all, of the following deployment options:
+ **Amazon EKS** – Amazon Elastic Kubernetes Service \(Amazon EKS\) is a managed service that you can use to run Kubernetes on AWS without needing to install, operate, and maintain your own Kubernetes control plane or nodes\. For more information, see [What is Amazon EKS?](what-is-eks.md)\.
+ **Amazon EKS on AWS Outposts** – Run Amazon EKS nodes on AWS Outposts\. AWS Outposts enables native AWS services, infrastructure, and operating models in on\-premises facilities\. For more information, see [Amazon EKS nodes on AWS Outposts](eks-on-outposts.md)\.
+ **Amazon EKS Anywhere** – Amazon EKS Anywhere is a deployment option for Amazon EKS that enables you to easily create and operate Kubernetes clusters on\-premises\. Both Amazon EKS and Amazon EKS Anywhere are built on the [Amazon EKS Distro](https://distro.eks.amazonaws.com/)\. To learn more about Amazon EKS Anywhere, and its differences with Amazon EKS, see [Overview](https://anywhere.eks.amazonaws.com/docs/overview) and [Comparing Amazon EKS Anywhere to Amazon EKS](https://anywhere.eks.amazonaws.com/docs/concepts/eksafeatures/#comparing-amazon-eks-anywhere-to-amazon-eks) in the Amazon EKS Anywhere documentation\.
+ **Amazon EKS Distro** – Amazon EKS Distro is a distribution of the same open\-source Kubernetes software and dependencies deployed by Amazon EKS in the cloud\. Amazon EKS Distro follows the same Kubernetes version release cycle as Amazon EKS and is provided as an open\-source project\. To learn more, see [Amazon EKS Distro](https://distro.eks.amazonaws.com/)\. You can also view and download the source code for the [Amazon EKS Distro](https://github.com/aws/eks-distro) on GitHub\.

When choosing which deployment options to use for your Kubernetes cluster, consider the following:


| Feature | Amazon EKS | Amazon EKS on AWS Outposts | Amazon EKS Anywhere | Amazon EKS Distro | 
| --- | --- | --- | --- | --- | 
| Hardware | AWS\-supplied | AWS\-supplied | Supplied by you | Supplied by you | 
| Deployment location | AWS cloud | Your data center | Your data center | Your datacenter | 
| Kubernetes control plane location | AWS cloud | AWS cloud | Your data center | Your datacenter | 
| Kubernetes data plane location | AWS cloud | Your data center | Your data center | Your datacenter | 
| Support | AWS support | AWS support | AWS support | OSS community support | 

**Frequently asked questions**
+ Q: Can I deploy Amazon EKS Anywhere in the AWS cloud?

  A: Amazon EKS Anywhere isn't designed to run in the AWS cloud\. It doesn't integrate with the [Kubernetes Cluster API Provider for AWS](https://github.com/kubernetes-sigs/cluster-api-provider-aws)\. If you plan to deploy Kubernetes clusters in the AWS cloud, we strongly recommend that you use Amazon EKS\. 
+ Q: Can I deploy Amazon EKS Anywhere on AWS Outposts?

  A: Amazon EKS Anywhere isn't designed to run on AWS Outposts\. If you’re planning to deploy Kubernetes clusters on AWS Outposts, we strongly recommend that you use Amazon EKS on AWS Outposts\. 