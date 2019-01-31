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
| US West \(Oregon\) \(us\-west\-2\) | ami\-0a2abab4107669c1b | ami\-0c9e5e2d8caa9fb5e | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-0c24db5df6badc35a | ami\-0ff0241c02b279f50 | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0c2e8d28b1f854c68 | ami\-006a12f54eaafc2b1 | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-010caa98bae9a09e2 | ami\-0d6f0554fd4743a9d | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-06ee67302ab7cf838 | ami\-0b159b75  | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-01e08d22b9439c15a | ami\-097978e7acde1fd7c | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0f0e8066383e7a2cb | ami\-036b3969c5eb8d3cf | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-0b7baa90de70f683f | ami\-0b7f163f7194396f7 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-019966ed970c18502 | ami\-093f742654a955ee6 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-06ade0abbd8eca425 | ami\-05e09575123ff498b | 


**Kubernetes version 1\.10**  

| Region | Amazon EKS\-optimized AMI | with GPU support | 
| --- | --- | --- | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-09e1df3bad220af0b | ami\-0ebf0561e61a2be02 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-04358410d28eaab63 | ami\-0131c0ca222183def | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0b779e8ab57655b4b | ami\-0abfb3be33c196cbf | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-08eb700778f03ea94 | ami\-000622b1016d2a5bf | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-068b8a1efffd30eda | ami\-cc149ab2 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-0de10c614955da932 | ami\-0dafd3a1dc43781f7 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-06398bdd37d76571d | ami\-0afc9d14b2fe11ad9 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-08a87e0a7c32fa649 | ami\-0d75b9ab57bfc8c9a | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-0ac3510e44b5bf8ef | ami\-0ecce0670cb66d17b | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-0d2c929ace88cfebe | ami\-03b048bd9d3861ce9 | 

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