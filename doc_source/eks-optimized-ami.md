# Amazon EKS\-Optimized AMI<a name="eks-optimized-ami"></a>

The Amazon EKS\-optimized AMI is built on top of Amazon Linux 2, and is configured to serve as the base image for Amazon EKS worker nodes\. The AMI is configured to work with Amazon EKS out of the box, and it includes Docker, kubelet, and the AWS IAM Authenticator\. 

**Note**  
You can track security or privacy events for Amazon Linux 2 at the [Amazon Linux Security Center](https://alas.aws.amazon.com/alas2.html) or subscribe to the associated [RSS feed](https://alas.aws.amazon.com/AL2/alas.rss)\. Security and privacy events include an overview of the issue, what packages are affected, and how to update your instances to correct the issue\.

The AMI IDs for the latest Amazon EKS\-optimized AMI \(with and without [GPU support](gpu-ami.md)\) are shown in the following table\.

**Note**  
The Amazon EKS\-optimized AMI with GPU support only supports P2 and P3 instance types\. Be sure to specify these instance types in your worker node AWS CloudFormation template\. By using the Amazon EKS\-optimized AMI with GPU support, you agree to [NVIDIA's end user license agreement \(EULA\)](https://www.nvidia.com/en-us/about-nvidia/eula-agreement/)\.


**Kubernetes version 1\.12\.7**  

| Region | Amazon EKS\-optimized AMI | with GPU support | 
| --- | --- | --- | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-0923e4b35a30a5f53 | ami\-0bebf2322fd52a42e | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-0abcb9f9190e867ab | ami\-0cb7959f92429410a | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-04ea7cb66af82ae4a | ami\-0118b61dc2312dee2 | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-0d741ed58ca5b342e | ami\-0c57db5b204001099 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-0c65a309fc58f6907 | ami\-09354b076296f5946 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-08716b70cac884aaa | ami\-0fbc930681258db86 | 
| EU \(London\) \(eu\-west\-2\) | ami\-0c7388116d474ee10 | ami\-0d832fced2cfe0f7b | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-0560aea042fec8b12 | ami\-0f8fa088b406ebba2 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0bfedee6a7845c26d | ami\-08e41cc84f4b3f27f | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-0a904348b703e620c | ami\-0c43b885e33fdc29e | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-09c3eb35bb3be46a4 | ami\-0d3ecaf4f3318c714 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-07b922b9b94d9a6d2 | ami\-0655b4dbbe2d46703 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-0f0121e9e64ebd3dc | ami\-07079cd9ff1b312da | 


**Kubernetes version 1\.11\.9**  

| Region | Amazon EKS\-optimized AMI | with GPU support | 
| --- | --- | --- | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-05ecac759c81e0b0c | ami\-08377056d89909b2a | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-02c1de421df89c58d | ami\-06ec2ea207616c078 | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-03b1b6cc34c010f9c | ami\-0e6993a35aae3407b | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-0c2709025eb548246 | ami\-0bf09c13f4204ce9d | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-084bd3569d08c6e67 | ami\-0a1714bb5be631b59 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-0e82e73403dd69fa3 | ami\-0b4d0f56587640d5a | 
| EU \(London\) \(eu\-west\-2\) | ami\-0da9aa88dd2ec8297 | ami\-00e98f9e6fd2319e5 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-099369bc73d1cc66f | ami\-0039e2556e6290828 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0d555d5f56c843803 | ami\-07fc636e8f6d3e18b | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-0144ae839b1111571 | ami\-002057772097fcef9 | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-02071c0110dc365ba | ami\-04fe7f4c75aac7196 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-00c91afdb73cf7f93 | ami\-08d5da0b12751a31f | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-05f4510fcfe56961c | ami\-04024dd8e0b9e36ff | 


**Kubernetes version 1\.10\.13**  

| Region | Amazon EKS\-optimized AMI | with GPU support | 
| --- | --- | --- | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-05a71d034119ffc12 | ami\-0901518d7557125c8 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-03a1e71fb42fc37dd | ami\-00f74c3728d4ca27d | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-093d55c2ba99ab2c8 | ami\-0a788defb66cdfffb | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-03bdf8079f6c013c5 | ami\-0a8536a894bd4ea06 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-0be77fe86d741fc81 | ami\-05baf7a6c293fe2ed | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-06368da7f495b68e9 | ami\-0f6f3929a9d7a418e | 
| EU \(London\) \(eu\-west\-2\) | ami\-0f1f2189b4741bc60 | ami\-0a12396b818bc2383 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-03a9acb0f6e0d424d | ami\-086d5edcaacd0ccfd | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0c9fb6a3fda95d373 | ami\-073f06a1edd22ae2e | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-00ea4ea959f28b4cf | ami\-0baff950f5217e54e | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-0f07478f5c5eb9e20 | ami\-033bd2c2a3431923e | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-05dac5d0ada75e22f | ami\-09defa93988984fa1 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-00513f18e1900ce1e | ami\-00d9364d705e902c9 | 

**Important**  
These AMIs require the latest AWS CloudFormation worker node template\. You cannot use these AMIs with a previous version of the worker node template; they will fail to join your cluster\. Be sure to upgrade any existing AWS CloudFormation worker stacks with the latest template \(URL shown below\) before you attempt to use these AMIs\.  

```
https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-02-11/amazon-eks-nodegroup.yaml
```

The AWS CloudFormation worker node template launches your worker nodes with Amazon EC2 user data that triggers a specialized [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) that allows them to discover and connect to your cluster's control plane automatically\. For more information, see [Launching Amazon EKS Worker Nodes](launch-workers.md)\.

## Amazon EKS\-Optimized AMI Build Scripts<a name="eks-ami-build-scripts"></a>

Amazon Elastic Container Service for Kubernetes \(Amazon EKS\) has open\-sourced the build scripts that are used to build the Amazon EKS\-optimized AMI\. These build scripts are now available [on GitHub](https://github.com/awslabs/amazon-eks-ami)\.

 The Amazon EKS\-optimized AMI is built on top of Amazon Linux 2, specifically for use as a worker node in Amazon EKS clusters\. You can use this repository to view the specifics of how the Amazon EKS team configures kubelet, Docker, the AWS IAM Authenticator for Kubernetes, and more\. 

 The build scripts repository includes a [HashiCorp Packer](https://www.packer.io/) template and build scripts to generate an AMI\. These scripts are the source of truth for Amazon EKS\-optimized AMI builds, so you can follow the GitHub repository to monitor changes to our AMIs\. For example, perhaps you want your own AMI to use the same version of Docker that the EKS team uses for the official AMI\. 

The GitHub repository also contains the specialized [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) that runs at boot time to configure your instance's certificate data, control plane endpoint, cluster name, and more\.

 Additionally, the GitHub repository contains our Amazon EKS worker node AWS CloudFormation templates\. These templates make it easier to spin up an instance running the Amazon EKS\-optimized AMI and register it with a cluster\.

 For more information, see the repositories on GitHub at [https://github\.com/awslabs/amazon\-eks\-ami](https://github.com/awslabs/amazon-eks-ami)\.