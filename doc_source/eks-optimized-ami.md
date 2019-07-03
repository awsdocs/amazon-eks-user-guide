# Amazon EKS\-Optimized AMI<a name="eks-optimized-ami"></a>

The Amazon EKS\-optimized AMI is built on top of Amazon Linux 2, and is configured to serve as the base image for Amazon EKS worker nodes\. The AMI is configured to work with Amazon EKS out of the box, and it includes Docker, kubelet, and the AWS IAM Authenticator\. 

**Note**  
You can track security or privacy events for Amazon Linux 2 at the [Amazon Linux Security Center](https://alas.aws.amazon.com/alas2.html) or subscribe to the associated [RSS feed](https://alas.aws.amazon.com/AL2/alas.rss)\. Security and privacy events include an overview of the issue, what packages are affected, and how to update your instances to correct the issue\.

The AMI IDs for the latest Amazon EKS\-optimized AMI \(with and without [GPU support](gpu-ami.md)\) are shown in the following table\.

**Note**  
The Amazon EKS\-optimized AMI with GPU support only supports P2 and P3 instance types\. Be sure to specify these instance types in your worker node AWS CloudFormation template\. By using the Amazon EKS\-optimized AMI with GPU support, you agree to [NVIDIA's end user license agreement \(EULA\)](https://www.nvidia.com/en-us/about-nvidia/eula-agreement/)\.

------
#### [ Kubernetes version 1\.13\.7 ]


| Region | Amazon EKS\-optimized AMI | with GPU support | 
| --- | --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0485258c2d1c3608f | ami\-0ccac9d9b57864000 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-0f2e8e5663e16b436 | ami\-0017d945a10387606 | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-03a55127c613349a7 | ami\-08335952e837d087b | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-0a9b1c1807b1a40ab | ami\-005b754faac73f0cc | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0fde798d17145fae1 | ami\-04cf69bbd6c0fae0b | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-07fd7609df6c8e39b | ami\-0730e699ed0118737 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-0361e14efd56a71c7 | ami\-07be5e97a529cd146 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-0237d87bc27daba65 | ami\-0a2f4c3aeb596aa7e | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-0b7127e7a2a38802a | ami\-0fbbd205f797ecccd | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-00ac2e6b3cb38a9b9 | ami\-0f9571a3e65dc4e20 | 
| EU \(London\) \(eu\-west\-2\) | ami\-0147919d2ff9a6ad5 | ami\-032348bd69c5dd665 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-0537ee9329c1628a2 | ami\-053962359d6859fec | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-0fd05922165907b85 | ami\-0641def7f02a4cac5 | 

------
#### [ Kubernetes version 1\.12\.7 ]


| Region | Amazon EKS\-optimized AMI | with GPU support | 
| --- | --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0fe61ae4c397e710d | ami\-067d88fb64d3d7990 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-0e380e0a62d368837 | ami\-06e46a15650294dfa | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-0355c210cb3f58aa2 | ami\-084e8e620163aa50e | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-01b6a163133c31994 | ami\-09ad3a49fb13389a0 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0a9b3f8b4b65b402b | ami\-0cd09d7293f31df8a | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-069f6a654a8795f72 | ami\-006549812c03748cb | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-03737a1ac334a5767 | ami\-01be8fddd9b16320c | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-07580768e8538626f | ami\-0a1bf783357dd8492 | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-0ee5ca4231511cafc | ami\-0ae5976723472b6d4 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-0404d23c7e8188740 | ami\-042f9abf2f96a0097 | 
| EU \(London\) \(eu\-west\-2\) | ami\-07346d8553f83f9d6 | ami\-0b87e9246afd42760 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-038cb36289174bac4 | ami\-0d9405868a6e9ee11 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-03e60b5a990893129 | ami\-0122b7e2a6736e3c5 | 

------
#### [ Kubernetes version 1\.11\.9 ]


| Region | Amazon EKS\-optimized AMI | with GPU support | 
| --- | --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-03c6648b74285020f | ami\-0b87186dda80931ee | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-0a5f5d5b0f6f58199 | ami\-07207754196c1a8fc | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-057d1c0dcb254a878 | ami\-052da6a4e0ae156ad | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-00f1adebe5ab9a431 | ami\-04645af6384529c5d | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0a0b6606652f9b3b9 | ami\-0a8f4e1f9bf09a81f | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-0c84b3f055cda1afb | ami\-01db6bb089f6adfcf | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-05e92412054db3f87 | ami\-0e001196bd450aa0c | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-07eb76498b1ba6cd6 | ami\-0c7132a332aa55aa6 | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-0234bc9c2b341aa02 | ami\-05cb4f6e8be8b83f1 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-06902949103360023 | ami\-02f337476a5c33f1b | 
| EU \(London\) \(eu\-west\-2\) | ami\-0db100ad46c7966d2 | ami\-0aa2208dbb9bb7cc5 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-052046d313576d0ba | ami\-0f6ea479cb4e7a4d2 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-02ebf24da505128f9 | ami\-078c260b9a737fc35 | 

------
#### [ Kubernetes version 1\.10\.13 ]


| Region | Amazon EKS\-optimized AMI | with GPU support | 
| --- | --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0523ec257fff1261d | ami\-006382264ad5fc773 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-01c1c96b9aa69de37 | ami\-0f1b9925c9ace2043 | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-021dd1fb7ba7e6e51 | ami\-0c3c59a4a7bea5678 | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-04c2ed5ff15a580f4 | ami\-0ea42cc96a8375851 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-02ffa4511b4baa5fa | ami\-00f64026212ad62c0 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-06295f3e6390dae00 | ami\-060b7aed71dfaa5f5 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-07f8ccb046b3ce697 | ami\-029b65710f075da3d | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-03ebcd449b224e0a3 | ami\-0f13220d49a34e787 | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-0c40973ffcf8bca40 | ami\-08d32cef88aa48343 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-06a96b4cfd627430b | ami\-058a8eec818dc3910 | 
| EU \(London\) \(eu\-west\-2\) | ami\-03356e704fb004162 | ami\-0cd6f7f1f7ceedc27 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-0eb77a4ca7135122b | ami\-01e3c54f23b6b02b3 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-028df8ba9b8603bdd | ami\-0d1ee923abbb8cf6c | 

------

**Important**  
These AMIs require the latest AWS CloudFormation worker node template\. You can't use these AMIs with a previous version of the worker node template; they will fail to join your cluster\. Be sure to upgrade any existing AWS CloudFormation worker stacks with the latest template \(URL shown below\) before you attempt to use these AMIs\.  

```
https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-02-11/amazon-eks-nodegroup.yaml
```

The AWS CloudFormation worker node template launches your worker nodes with Amazon EC2 user data that triggers a specialized [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh)\. This script allows your worker nodes to discover and connect to your cluster's control plane automatically\. For more information, see [Launching Amazon EKS Worker Nodes](launch-workers.md)\.

## Amazon EKS\-Optimized AMI Build Scripts<a name="eks-ami-build-scripts"></a>

Amazon Elastic Kubernetes Service \(Amazon EKS\) has open\-sourced the build scripts that are used to build the Amazon EKS\-optimized AMI\. These build scripts are now available [on GitHub](https://github.com/awslabs/amazon-eks-ami)\.

 The Amazon EKS\-optimized AMI is built on top of Amazon Linux 2, specifically for use as a worker node in Amazon EKS clusters\. You can use this repository to view the specifics of how the Amazon EKS team configures kubelet, Docker, the AWS IAM Authenticator for Kubernetes, and more\. 

 The build scripts repository includes a [HashiCorp Packer](https://www.packer.io/) template and build scripts to generate an AMI\. These scripts are the source of truth for Amazon EKS\-optimized AMI builds, so you can follow the GitHub repository to monitor changes to our AMIs\. For example, perhaps you want your own AMI to use the same version of Docker that the EKS team uses for the official AMI\. 

The GitHub repository also contains the specialized [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) that runs at boot time to configure your instance's certificate data, control plane endpoint, cluster name, and more\.

 Additionally, the GitHub repository contains our Amazon EKS worker node AWS CloudFormation templates\. These templates make it easier to spin up an instance running the Amazon EKS\-optimized AMI and register it with a cluster\.

 For more information, see the repositories on GitHub at [https://github\.com/awslabs/amazon\-eks\-ami](https://github.com/awslabs/amazon-eks-ami)\.