# Amazon EKS\-Optimized AMI<a name="eks-optimized-ami"></a>

The Amazon EKS\-optimized AMI is built on top of Amazon Linux 2, and is configured to serve as the base image for Amazon EKS worker nodes\. The AMI is configured to work with Amazon EKS out of the box, and it includes Docker, kubelet, and the AWS IAM Authenticator\. 

**Note**  
You can track security or privacy events for Amazon Linux 2 at the [Amazon Linux Security Center](https://alas.aws.amazon.com/alas2.html) or subscribe to the associated [RSS feed](https://alas.aws.amazon.com/AL2/alas.rss)\. Security and privacy events include an overview of the issue, what packages are affected, and how to update your instances to correct the issue\.

The AMI IDs for the latest Amazon EKS\-optimized AMI \(with and without [GPU support](gpu-ami.md)\) are shown in the following table\.

**Note**  
The Amazon EKS\-optimized AMI with GPU support only supports P2 and P3 instance types\. Be sure to specify these instance types in your worker node AWS CloudFormation template\. By using the Amazon EKS\-optimized AMI with GPU support, you agree to [NVIDIA's end user license agreement \(EULA\)](https://www.nvidia.com/en-us/about-nvidia/eula-agreement/)\.

------
#### [ Kubernetes version 1\.14\.6 ]


| Region | Amazon EKS\-optimized AMI | with GPU support | 
| --- | --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0f841722be384ed96 | ami\-02ed30745089113eb | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-08739803f18dcc019 | ami\-0d5628765ec5d0c5a | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-038a987c6425a84ad | ami\-02ce33febfee0b888 | 
| Asia Pacific \(Hong Kong\) \(ap\-east\-1\) | ami\-0fc4b0a16426993b5 | ami\-0c23d82cc7e2b0f53 | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-0e9f7f3edab94472d | ami\-0981d2926d2260939 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-055d09694b6e5591a | ami\-0515f3ce5064036dc | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-023bb403131889300 | ami\-0cba72a7e9b560b06 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-0d26e45a1e5422b8e | ami\-0503f4de442edeef2 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-0d8e3da32bd74f39b | ami\-09a0ec306d79ed058 | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-0f64557dd6506a4aa | ami\-0698f87b093bbcdda | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-0497f6feb9d494baf | ami\-04cef31a7c7bf1169 | 
| EU \(London\) \(eu\-west\-2\) | ami\-010d34c5744286662 | ami\-04f1bbad31585405d | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-04fada31d8c50b7a8 | ami\-0ebcd2fd2eb614793 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-0a4a5386eb62c775e | ami\-04e7d365014dee49c | 
| Middle East \(Bahrain\) \(me\-south\-1\) | ami\-0b7e753bbd3a0ae24 | ami\-07ca0892ebe2c442e | 

------
#### [ Kubernetes version 1\.13\.10 ]


| Region | Amazon EKS\-optimized AMI | with GPU support | 
| --- | --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0355b5edf93d47112 | ami\-080eaa48408e4cce8 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-08198f90fe8bc57f0 | ami\-0b2f191b2ddb13526 | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-0dc5bf48daa40eb35 | ami\-0842679a8337cad05 | 
| Asia Pacific \(Hong Kong\) \(ap\-east\-1\) | ami\-056314bd2d2acbdc1 | ami\-0a63a7853310f3111 | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-00f4cff050d28ee2d | ami\-0e80f1d31941f6010 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0262013b4d50142a2 | ami\-0a443fa8decd2df67 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-0d9a543e7c4279c11 | ami\-019966f3e72baba33 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-0013f4890e2ce167b | ami\-07f34d09a8d7fe5a4 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-01cd15b342b7edf5e | ami\-03563e56d0af30647 | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-01ffee931e45bb6bf | ami\-0e262bd06b1cbc1d6 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-00ea6211202297fe8 | ami\-05cded29b25d50f91 | 
| EU \(London\) \(eu\-west\-2\) | ami\-0ef7099142dae7023 | ami\-0163f3b1681613866 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-00cc28b5bcb9dc724 | ami\-0bc7f58961988d81e | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-01d7a7c38f882ef68 | ami\-0b219ca1c6aa2f7fb | 
| Middle East \(Bahrain\) \(me\-south\-1\) | ami\-0ae4a6a2950a3546e | ami\-0dd405f6294e0414d | 

------
#### [ Kubernetes version 1\.12\.10 ]


| Region | Amazon EKS\-optimized AMI | with GPU support | 
| --- | --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0d60b7264ed85e022 | ami\-043355c6f9c7b980c | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-0259ce67309f76e0b | ami\-0585963de7ab8b964 | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-0315dd35bf204311d | ami\-04f40a6dd1cd12b3c | 
| Asia Pacific \(Hong Kong\) \(ap\-east\-1\) | ami\-0fafd65fe31195cb5 | ami\-0f6b904acd6b3add8 | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-0d9c7adc50f0c3f04 | ami\-008ab31273984feb4 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-08b2cecec9f2d5964 | ami\-0364b5f7211f80363 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-0bbe543cd7fc2acd1 | ami\-08704c644f2f284bb | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-07696966feacc8e7b | ami\-044d6be5df6aa258e | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-07621fc1a7675f06c | ami\-002dcfad1b6044f1d | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-0fe22fc725c19301f | ami\-0a697401e7cfa02bd | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-0a6be9528ebb8999d | ami\-049574de1981b69dc | 
| EU \(London\) \(eu\-west\-2\) | ami\-0a8dc5b3290842d3e | ami\-009594e276ffd81b0 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-01dbd2d713c939649 | ami\-06cb6ffbba9a766eb | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-0586fb63f5c466e3c | ami\-0051b31561a86c5fb | 
| Middle East \(Bahrain\) \(me\-south\-1\) | ami\-08eab8b7cd9f43bd0 | ami\-0d4ec4bd32daaae1c | 

------
#### [ Kubernetes version 1\.11\.10 ]


| Region | Amazon EKS\-optimized AMI | with GPU support | 
| --- | --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0f01aa60d08b56b51 | ami\-06352290702ae9aa4 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-0277d42c17d2fd9f6 | ami\-06dbf81822c5d802d | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-0e024bc930f00f7a2 | ami\-01ccb69d4e42d3098 | 
| Asia Pacific \(Hong Kong\) \(ap\-east\-1\) | ami\-01efe02a8386b4448 | ami\-0bf87f2c6a31cf83c | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-0fee6e6300019359b | ami\-067c840a5dce7fe27 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0acea8b886f0e3f8f | ami\-0dc2541c99f0623e1 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-01e754bb06dedfd13 | ami\-013299f00c1c965d4 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-04aff8301e51a47e4 | ami\-07e5bc491d2ec43e1 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-0cb611c369549e9c9 | ami\-04b5a2ebc54d30b11 | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-0157324517811932f | ami\-0147c8fcfea398609 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-0ed6bcde59efbec8a | ami\-01f0f9e4092c0f784 | 
| EU \(London\) \(eu\-west\-2\) | ami\-0b2d004b35f3153c4 | ami\-024af210119b7a9f8 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-0c592c8c15d5a2824 | ami\-00d28dcaaa9b1010a | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-019c885c71264830f | ami\-0a2aefc5b3775e1da | 
| Middle East \(Bahrain\) \(me\-south\-1\) | ami\-0f19239ec6bfc1fd4 | ami\-03ba561b225de5fc7 | 

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