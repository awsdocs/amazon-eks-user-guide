# Amazon EKS\-Optimized AMI<a name="eks-optimized-ami"></a>

The Amazon EKS\-optimized AMI is built on top of Amazon Linux 2, and is configured to serve as the base image for Amazon EKS worker nodes\. The AMI is configured to work with Amazon EKS out of the box, and it includes Docker, kubelet, and the AWS IAM Authenticator\. 

**Note**  
You can track security or privacy events for Amazon Linux 2 at the [Amazon Linux Security Center](https://alas.aws.amazon.com/alas2.html) or subscribe to the associated [RSS feed](https://alas.aws.amazon.com/AL2/alas.rss)\. Security and privacy events include an overview of the issue, what packages are affected, and how to update your instances to correct the issue\.

The AMI IDs for the latest Amazon EKS\-optimized AMI \(with and without [GPU support](gpu-ami.md)\) are shown in the following table\.

**Note**  
The Amazon EKS\-optimized AMI with GPU support only supports P2 and P3 instance types\. Be sure to specify these instance types in your worker node AWS CloudFormation template\. By using the Amazon EKS\-optimized AMI with GPU support, you agree to [NVIDIA's end user license agreement \(EULA\)](https://www.nvidia.com/en-us/about-nvidia/eula-agreement/)\.

------
#### [ Kubernetes version 1\.13\.8 ]


| Region | Amazon EKS\-optimized AMI | with GPU support | 
| --- | --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-027683840ad78d833 | ami\-0af8403c143fd4a07 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-0d3998d69ebe9b214 | ami\-0484012ada3522476 | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-00b95829322267382 | ami\-0d24da600cc96ae6b | 
| Asia Pacific \(Hong Kong\) \(ap\-east\-1\) | ami\-03f8634a8fd592414 | ami\-080eb165234752969 | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-0062e5b0411e77c1a | ami\-010dbb7183ab64b39 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0a67c71d2ab43d36f | ami\-069303796840f8155 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-0d66d2fefbc86831a | ami\-04f71dc710ff5baf4 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-06206d907abb34bbc | ami\-0213fc532b1c2e05f | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-09f2d86f2d8c4f77d | ami\-01fc0a4c67f82532b | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-038bd8d3a2345061f | ami\-07b7cbb235789cc31 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-0199284372364b02a | ami\-00bfeece5b673b69f | 
| EU \(London\) \(eu\-west\-2\) | ami\-0f454b09349248e29 | ami\-0babebc79dbf6016c | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-00b44348ab3eb2c9f | ami\-03136b5b83c5b61ba | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-02218be9004537a65 | ami\-057821acea15c1a98 | 

------
#### [ Kubernetes version 1\.12\.10 ]


| Region | Amazon EKS\-optimized AMI | with GPU support | 
| --- | --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0ebb1c51e5fe9c376 | ami\-0b42bfc7af8bb3abc | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-01e370f796735b244 | ami\-0eb0119f55d589a03 | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-0b520e822d42998c1 | ami\-0c9156d7fcd3c2948 | 
| Asia Pacific \(Hong Kong\) \(ap\-east\-1\) | ami\-0aa07b9e8bfcdaaff | ami\-0a5e7de0e5d22a988 | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-03b7b0e3088a72394 | ami\-0c1bc87ff613a979b | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0f554256ac7b33081 | ami\-0e2f87975f5aa9908 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-066a40f5f0e0b90f4 | ami\-08101c357b41e9f9a | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-06a42a7479836d402 | ami\-0420c66a82472f4b2 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-0f93997f60ca40d26 | ami\-04a085528a6af6499 | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-04341c15c2f941589 | ami\-09c45f4e40a56254b | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-018b4a3f81f517183 | ami\-04668c090ff8c1f50 | 
| EU \(London\) \(eu\-west\-2\) | ami\-0fd0b45d54f80a0e9 | ami\-0b925567bd252e74c | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-0b12420c7f7281432 | ami\-0f975ac243bcd0da0 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-01c1b0b8dcbd02b11 | ami\-093da2874a5426ce3 | 

------
#### [ Kubernetes version 1\.11\.10 ]


| Region | Amazon EKS\-optimized AMI | with GPU support | 
| --- | --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0e565ff1ccb9b6979 | ami\-0f9e62727a55f68d3 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-08571c6cee1adbb62 | ami\-0c3d92683a7946ac3 | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-0566833f0c8e9031e | ami\-058b22acd515ec20b | 
| Asia Pacific \(Hong Kong\) \(ap\-east\-1\) | ami\-0e2e431905d176277 | ami\-0baf9ac8446e87fb5 | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-073c3d075aeb53d1f | ami\-0c709282458d1114c | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0644b094efc34d888 | ami\-023f507ec007de487 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-0ab0067299faa5229 | ami\-0ccbbe6530310b01d | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-087f58c635bb8283b | ami\-0341435cf966cb837 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-06caef7a88fd74af2 | ami\-0987b07bd338f97db | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-099b3f8db68693895 | ami\-060f13bd7397f782d | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-06b60c5852910e7b5 | ami\-0d84963dfda5af073 | 
| EU \(London\) \(eu\-west\-2\) | ami\-0b56c1f39e4b1eb8e | ami\-0189e53a00d37a0b6 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-036237d1951bfeabc | ami\-0baea83f5f5d2abfe | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-0612e10dfe00c5ff6 | ami\-0d5b7823e58094232 | 

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