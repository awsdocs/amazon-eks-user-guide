# Amazon EKS\-Optimized AMI<a name="eks-optimized-ami"></a>

The Amazon EKS\-optimized AMI is built on top of Amazon Linux 2, and is configured to serve as the base image for Amazon EKS worker nodes\. The AMI is configured to work with Amazon EKS out of the box, and it includes Docker, kubelet, and the AWS IAM Authenticator\. 

**Note**  
You can track security or privacy events for Amazon Linux 2 at the [Amazon Linux Security Center](https://alas.aws.amazon.com/alas2.html) or subscribe to the associated [RSS feed](https://alas.aws.amazon.com/AL2/alas.rss)\. Security and privacy events include an overview of the issue, what packages are affected, and how to update your instances to correct the issue\.

The AMI IDs for the latest Amazon EKS\-optimized AMI \(with and without [GPU support](gpu-ami.md)\) are shown in the following table\.

**Note**  
The Amazon EKS\-optimized AMI with GPU support only supports P2 and P3 instance types\. Be sure to specify these instance types in your worker node AWS CloudFormation template\. Because this AMI includes third\-party software that requires an end user license agreement \(EULA\), you must subscribe to the AMI in the AWS Marketplace and accept the EULA before you can use the AMI in your worker node groups\. To subscribe to the AMI, visit [the AWS Marketplace](https://aws.amazon.com/marketplace/pp/B07GRHFXGM)\.


**Kubernetes version 1\.11**  

| Region | Amazon EKS\-optimized AMI | with GPU support | 
| --- | --- | --- | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-081099ec932b99961 | ami\-095922d81242d0528 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-0c5b63ec54dd3fc38 | ami\-0a0cbb44e651c5e22 | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0b10ebfc82e446296 | ami\-08697e581e49ffecf | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-05e062a123092066a | ami\-0444fdaca5263be70 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-0da59d86953d1c266 | ami\-fe810880  | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-0b469c0fef0445d29 | ami\-03b9f52d2b707ce0a | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-04ef881404deec134 | ami\-02bacb819e2777536 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-0d87105164496b94b | ami\-0e35cc17cf9675a1f | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-030c789a75c8bfbca | ami\-031361e2106e79386 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-0a9b90002a9a1c111 | ami\-0fde112efc845caec | 


**Kubernetes version 1\.10**  

| Region | Amazon EKS\-optimized AMI | with GPU support | 
| --- | --- | --- | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-0e36fae01a5fa0d76 | ami\-0796d47bbb4361153 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-0de0b13514617a168 | ami\-04c29548028d8a4a0 | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0d885462fa1a40e3a | ami\-0a6f0cc2cbef07ba9 | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-074583f8d5a05e27b | ami\-0e24c510ebe972f26 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-0e1d5399bfbe402e0 | ami\-f9810887 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-076c1952dd7a28909 | ami\-098171628d39d4d6c | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-049090cdbc5e3c080 | ami\-03c93f6816f8652c7 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-0b39dee42365df927 | ami\-0089fa930c7f3e830 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-0a3df91af7c8225db | ami\-014ed22ec2f34c4bf | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-0f4d387d27ad36792 | ami\-096064ec61eaa29df | 

**Important**  
These AMIs require the latest AWS CloudFormation worker node template\. You cannot use these AMIs with a previous version of the worker node template; they will fail to join your cluster\. Be sure to upgrade any existing AWS CloudFormation worker stacks with the latest template \(URL shown below\) before you attempt to use these AMIs\.  

```
https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-01-09/amazon-eks-nodegroup.yaml
```

The AWS CloudFormation worker node template launches your worker nodes with Amazon EC2 user data that triggers a specialized [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) that allows them to discover and connect to your cluster's control plane automatically\. For more information, see [Launching Amazon EKS Worker Nodes](launch-workers.md)\.

## Amazon EKS\-Optimized AMI Build Scripts<a name="eks-ami-build-scripts"></a>

Amazon Elastic Container Service for Kubernetes \(Amazon EKS\) has open\-sourced the build scripts that are used to build the Amazon EKS\-optimized AMI\. These build scripts are now available [on GitHub](https://github.com/awslabs/amazon-eks-ami)\.

 The Amazon EKS\-optimized AMI is built on top of Amazon Linux 2, specifically for use as a worker node in Amazon EKS clusters\. You can use this repository to view the specifics of how the Amazon EKS team configures kubelet, Docker, the AWS IAM Authenticator for Kubernetes, and more\. 

 The build scripts repository includes a [HashiCorp Packer](https://www.packer.io/) template and build scripts to generate an AMI\. These scripts are the source of truth for Amazon EKS\-optimized AMI builds, so you can follow the GitHub repository to monitor changes to our AMIs\. For example, perhaps you want your own AMI to use the same version of Docker that the EKS team uses for the official AMI\. 

The GitHub repository also contains the specialized [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) that runs at boot time to configure your instance's certificate data, control plane endpoint, cluster name, and more\.

 Additionally, the GitHub repository contains our Amazon EKS worker node AWS CloudFormation templates\. These templates make it easier to spin up an instance running the Amazon EKS\-optimized AMI and register it with a cluster\.

 For more information, see the repositories on GitHub at [https://github\.com/awslabs/amazon\-eks\-ami](https://github.com/awslabs/amazon-eks-ami)\.