# Amazon EKS\-Optimized AMI<a name="eks-optimized-ami"></a>

The Amazon EKS\-optimized AMI is built on top of Amazon Linux 2, and is configured to serve as the base image for Amazon EKS worker nodes\. The AMI is configured to work with Amazon EKS out of the box, and it includes Docker, kubelet, and the AWS IAM Authenticator\. 

**Note**  
You can track security or privacy events for Amazon Linux 2 at the [Amazon Linux Security Center](https://alas.aws.amazon.com/alas2.html) or subscribe to the associated [RSS feed](https://alas.aws.amazon.com/AL2/alas.rss)\. Security and privacy events include an overview of the issue, what packages are affected, and how to update your instances to correct the issue\.

The AMI IDs for the latest Amazon EKS\-optimized AMI \(with and without [GPU support](gpu-ami.md)\) are shown in the following table\.

**Note**  
The Amazon EKS\-optimized AMI with GPU support only supports P2 and P3 instance types\. Be sure to specify these instance types in your worker node AWS CloudFormation template\. Because this AMI includes third\-party software that requires an end user license agreement \(EULA\), you must subscribe to the AMI in the AWS Marketplace and accept the EULA before you can use the AMI in your worker node groups\. To subscribe to the AMI, visit [the AWS Marketplace](https://aws.amazon.com/marketplace/pp/B07GRHFXGM)\.


**Kubernetes version 1\.11\.5**  

| Region | Amazon EKS\-optimized AMI | with GPU support | 
| --- | --- | --- | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-094fa4044a2a3cf52 | ami\-014f4e495a19d3e4f | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-0b4eb1d8782fc3aea | ami\-08a0bb74d1c9a5e2f | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-053cbe66e0033ebcf | ami\-04a758678ae5ebad5 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-0a9006fb385703b54 | ami\-050db3f5f9dbd4439 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-082e6cf1c07e60241 | ami\-69b03e17  | 


**Kubernetes version 1\.10\.11**  

| Region | Amazon EKS\-optimized AMI | with GPU support | 
| --- | --- | --- | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-07af9511082779ae7 | ami\-08754f7ac73185331 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-027792c3cc6de7b5b | ami\-03c499c67bc65c089 | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-036130f4127a367f7 | ami\-081210a2fd7f3c487 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-03612357ac9da2c7d | ami\-047637529a86c7237 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-04b0f84e5a05e0b30 | ami\-24b43a5a | 

**Important**  
These AMIs require the latest AWS CloudFormation worker node template\. You cannot use these AMIs with a previous version of the worker node template; they will fail to join your cluster\. Be sure to upgrade any existing AWS CloudFormation worker stacks with the latest template \(URL shown below\) before you attempt to use these AMIs\.  

```
https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2018-12-10/amazon-eks-nodegroup.yaml
```

The AWS CloudFormation worker node template launches your worker nodes with Amazon EC2 user data that triggers a specialized [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) that allows them to discover and connect to your cluster's control plane automatically\. For more information, see [Launching Amazon EKS Worker Nodes](launch-workers.md)\.

## Amazon EKS\-Optimized AMI Build Scripts<a name="eks-ami-build-scripts"></a>

Amazon Elastic Container Service for Kubernetes \(Amazon EKS\) has open\-sourced the build scripts that are used to build the Amazon EKS\-optimized AMI\. These build scripts are now available [on GitHub](https://github.com/awslabs/amazon-eks-ami)\.

 The Amazon EKS\-optimized AMI is built on top of Amazon Linux 2, specifically for use as a worker node in Amazon EKS clusters\. You can use this repository to view the specifics of how the Amazon EKS team configures kubelet, Docker, the AWS IAM Authenticator for Kubernetes, and more\. 

 The build scripts repository includes a [HashiCorp Packer](https://www.packer.io/) template and build scripts to generate an AMI\. These scripts are the source of truth for Amazon EKS\-optimized AMI builds, so you can follow the GitHub repository to monitor changes to our AMIs\. For example, perhaps you want your own AMI to use the same version of Docker that the EKS team uses for the official AMI\. 

The GitHub repository also contains the specialized [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) that runs at boot time to configure your instance's certificate data, control plane endpoint, cluster name, and more\.

 Additionally, the GitHub repository contains our Amazon EKS worker node AWS CloudFormation templates\. These templates make it easier to spin up an instance running the Amazon EKS\-optimized AMI and register it with a cluster\.

 For more information, see the repositories on GitHub at [https://github\.com/awslabs/amazon\-eks\-ami](https://github.com/awslabs/amazon-eks-ami)\.