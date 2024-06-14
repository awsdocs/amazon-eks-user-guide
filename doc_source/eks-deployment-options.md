# Deployment options<a name="eks-deployment-options"></a>

You can deploy Amazon EKS using any of the following options:

**Amazon EKS in the cloud**  
You can run Kubernetes in the AWS cloud without needing to install, operate, and maintain your own Kubernetes control plane or nodes\. This option is what is covered in this guide\.

**Amazon EKS on Outposts**  
AWS Outposts enables native AWS services, infrastructure, and operating models in your on\-premises facilities\. With Amazon EKS on Outposts, you can choose to run extended or local clusters\. With extended clusters, the Kubernetes control plane runs in an AWS Region, and the nodes run on Outposts\. With local clusters, the entire Kubernetes cluster runs locally on Outposts, including both the Kubernetes control plane and nodes\. For more information, see [Amazon EKS on AWS Outposts](eks-outposts.md)\.

**Amazon EKS Anywhere**  
Amazon EKS Anywhere is a deployment option for Amazon EKS that enables you to easily create and operate Kubernetes clusters on\-premises\. Both Amazon EKS and Amazon EKS Anywhere are built on the [Amazon EKS Distro](https://distro.eks.amazonaws.com/)\. To learn more about Amazon EKS Anywhere, and its differences with Amazon EKS, see [Overview](https://anywhere.eks.amazonaws.com/docs/overview) and [Comparing Amazon EKS Anywhere to Amazon EKS](https://anywhere.eks.amazonaws.com/docs/concepts/eksafeatures/#comparing-amazon-eks-anywhere-to-amazon-eks) in the Amazon EKS Anywhere documentation\. For answers to some common questions, see [Amazon EKS Anywhere FAQs](https://aws.amazon.com/eks/eks-anywhere/faqs/)\.

**Amazon EKS Distro**  
Amazon EKS Distro is a distribution of the same open\-source Kubernetes software and dependencies deployed by Amazon EKS in the cloud\. Amazon EKS Distro follows the same Kubernetes version release cycle as Amazon EKS and is provided as an open\-source project\. To learn more, see [Amazon EKS Distro](https://distro.eks.amazonaws.com/)\. You can also view and download the source code for the [Amazon EKS Distro](https://github.com/aws/eks-distro) on GitHub\.

When choosing which deployment options to use for your Kubernetes cluster, consider the following:


| Feature | Amazon EKS | Amazon EKS on Outposts | Amazon EKS Anywhere | Amazon EKS Distro | 
| --- | --- | --- | --- | --- | 
| Hardware | AWS\-supplied | AWS\-supplied | Supplied by you | Supplied by you | 
| Deployment location | AWS cloud | Your data center | Your data center | Your data center | 
| Kubernetes control plane location | AWS cloud | AWS cloud or your data center | Your data center | Your data center | 
| Kubernetes data plane location | AWS cloud | Your data center | Your data center | Your data center | 
| Support | AWS Support | AWS Support | AWS Support | OSS community support | 