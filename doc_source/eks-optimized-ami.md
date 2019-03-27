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
| US West \(Oregon\) \(us\-west\-2\) | ami\-0c28139856aaf9c3b | ami\-0805ff53a28e7b904 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-0eeeef929db40543c | ami\-000412c12949aa8dd | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0484545fe7d3da96f | ami\-018bc34828bcbf65e | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-032ed5525d4df2de3 | ami\-0b82a79b011122da0 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-0154b2479ba20f8bb | ami\-d6159ca8 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-098fb7e9b507904e7 | ami\-0fab91784768ff07a | 
| EU \(London\) \(eu\-west\-2\) | ami\-0d69ab00cb41d6eda | ami\-02ab85779351ea872 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-018ebb030cf6ae00b | ami\-08b97dd0252bd9e51 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-07fdc9272ce5b0ce5 | ami\-0ed8c50e848425cb3 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-091e0e1906e653417 | ami\-042e93c5dc384f6b8 | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-0b6f791fc54125a8a | ami\-0f8881c15c47755a9 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-038d55c26bf01998f | ami\-0c1b23fe04eafb5a0 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-0e07b5081bb77d540 | ami\-0fe2e260f573c02a8 | 


**Kubernetes version 1\.10**  

| Region | Amazon EKS\-optimized AMI | with GPU support | 
| --- | --- | --- | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-0e7ee8863c8536cce | ami\-003a551d4d2e5c75d | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-09a7630ca9ee4ee22 | ami\-0c67dfb2298cf554a | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-02a8a05e480e902e2 | ami\-0fb4bb0f84f4a0049 | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-0b8d223ce03e6fabc | ami\-0290406a183d6587d | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-09be5053dbb1a515d | ami\-d3169fad | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-0103822d44fc52f97 | ami\-086252e9df9c3a21e | 
| EU \(London\) \(eu\-west\-2\) | ami\-017c4d847b606e125 | ami\-06389f3a72966a326 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-0c7fc5c0784b58207 | ami\-0dce0fff5c4af413e | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0e831f9f650f2f8ab | ami\-0bb5892624403ca87 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-0378f1fac83cbf438 | ami\-02ef4162c5ee1e443 | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-0ac369c3b2206d2ea | ami\-09865c928b7d38fcd | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-0fa3f3282eb89b795 | ami\-09496affecfe51b86 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-01d0ab2e9506b8db0 | ami\-0dae5c0d203e32e9f | 

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