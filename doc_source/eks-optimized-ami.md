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
| US East \(Ohio\) \(us\-east\-2\) | ami\-07ebcae043cf995aa | ami\-01f82bb66c17faf20 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-08c4955bcc43b124e | ami\-02af865c0f3b337f2 | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-089d3b6350c1769a6 | ami\-08e5329e1dbf22c6a | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-0410a80d323371237 | ami\-094beaac92afd72eb | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-04c0f02f5e148c80a | ami\-0f409159b757b0292 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-0b7997a20f8424fb1 | ami\-066623eb3f5a82878 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-087e0fca60fb5737a | ami\-0d660fb17b06078d9 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-082dfea752d9163f6 | ami\-0d11124f8f06f8a4f | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-02d5e7ca7bc498ef9 | ami\-085b174e2e2b41f33 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-09bbefc07310f7914 | ami\-093009474b04965b3 | 
| EU \(London\) \(eu\-west\-2\) | ami\-0f03516f22468f14e | ami\-08a5d542db43e17ab | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-051015c2c2b73aaea | ami\-05cbcb1bc3dbe7a3d | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-0c31ee32297e7397d | ami\-0f66f596ae68c0353 | 

------
#### [ Kubernetes version 1\.12\.7 ]


| Region | Amazon EKS\-optimized AMI | with GPU support | 
| --- | --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0e8d353285e26a68c | ami\-09279e76127f808b2 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-0200e65a38edfb7e1 | ami\-0ae641b4b7ed88d72 | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-0f11fd98b02f12a4c | ami\-08142df4834399a6b | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-0644de45344ce867e | ami\-000721b659ba73311 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0dfbca8d183884f02 | ami\-0b11aeca80a60fbb5 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-0a9d12fe9c2a31876 | ami\-08ace4be4e6e52c62 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-040bdde117f3828ab | ami\-054db05dce73fc060 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-01bfe815f644becc0 | ami\-0045324a51592dbeb | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-09ed3f40a2b3c11f1 | ami\-0bd21d3112638aa26 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-091fc251b67b776c3 | ami\-0ae2f64856228879f | 
| EU \(London\) \(eu\-west\-2\) | ami\-0bc8d0262346bd65e | ami\-06cc142c64830e356 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-0084dea61e480763e | ami\-02461867f991941f2 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-022cd6a50742d611a | ami\-04870dc2b156b47fb | 

------
#### [ Kubernetes version 1\.11\.9 ]


| Region | Amazon EKS\-optimized AMI | with GPU support | 
| --- | --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-088dad958fbfa643e | ami\-05ad04ed51d006bc9 | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-053e2ac42d872cc20 | ami\-06fb2eb20652dafea | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-0743039b7c66a18f5 | ami\-0d6743e4d45d710f4 | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-01d152acba5840ba2 | ami\-0d888cb5eaaba12d4 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-07765e1384d2e372c | ami\-05ab4ae12fa19bfb5 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-0656df091f27461cd | ami\-0bfd390f3bd942923 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-084e9f3625a1a4a09 | ami\-0726645aa38e7fe38 | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-03050c93b7e745696 | ami\-0d2ed580683a2ef3c | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-020f08a17c3c4251c | ami\-096075e3334201678 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-07d0c92a42077ec9b | ami\-0fb8e730ee4b17f98 | 
| EU \(London\) \(eu\-west\-2\) | ami\-0ff8a4dc1632ee425 | ami\-0c420fc6a2ab8a140 | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-0569332dde21e3f1a | ami\-009bd30954d1cdf61 | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-0fc8c638bc80fcecf | ami\-07fa78fe686748c79 | 

------
#### [ Kubernetes version 1\.10\.13 ]


| Region | Amazon EKS\-optimized AMI | with GPU support | 
| --- | --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | ami\-0295a10750423107d | ami\-0a0d326e98757aa1b | 
| US East \(N\. Virginia\) \(us\-east\-1\) | ami\-05c9fba3332ccbc43 | ami\-0e261247a4b523354 | 
| US West \(Oregon\) \(us\-west\-2\) | ami\-0fc349241eb7b1222 | ami\-067089d967e068569 | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | ami\-0a183946b284a9841 | ami\-014cc26f091950263 | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | ami\-0f93f5579e6e79e96 | ami\-02fe5649049614901 | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | ami\-0412ddfd70b9c54bd | ami\-011a0f131a7148431 | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | ami\-0538e8e564078659c | ami\-0654c7681c0b39e0c | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | ami\-009caed75bdc3a2f0 | ami\-0d120c3ce6fba36d8 | 
| EU \(Frankfurt\) \(eu\-central\-1\) | ami\-032fc49751b7a5f83 | ami\-0be7b531dd58c5df1 | 
| EU \(Ireland\) \(eu\-west\-1\) | ami\-03f9c85cd73fb9f4a | ami\-0b01f474bfc6c1260 | 
| EU \(London\) \(eu\-west\-2\) | ami\-05c9cec73d17bf97f | ami\-0513d2fbf2aa77b8c | 
| EU \(Paris\) \(eu\-west\-3\) | ami\-0df95e4cd302d42f7 | ami\-0032d4bbdc242c41c | 
| EU \(Stockholm\) \(eu\-north\-1\) | ami\-0ef218c64404e4bdf | ami\-0b9102084fa8d4e01 | 

------

**Important**  
These AMIs require the latest AWS CloudFormation worker node template\. You can't use these AMIs with a previous version of the worker node template; they will fail to join your cluster\. Be sure to upgrade any existing AWS CloudFormation worker stacks with the latest template \(URL shown below\) before you attempt to use these AMIs\.  

```
https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-02-11/amazon-eks-nodegroup.yaml
```

The AWS CloudFormation worker node template launches your worker nodes with Amazon EC2 user data that triggers a specialized [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh)\. This script allows your worker nodes to discover and connect to your cluster's control plane automatically\. For more information, see [Launching Amazon EKS Worker Nodes](launch-workers.md)\.

## Amazon EKS\-Optimized AMI Build Scripts<a name="eks-ami-build-scripts"></a>

Amazon Elastic Container Service for Kubernetes \(Amazon EKS\) has open\-sourced the build scripts that are used to build the Amazon EKS\-optimized AMI\. These build scripts are now available [on GitHub](https://github.com/awslabs/amazon-eks-ami)\.

 The Amazon EKS\-optimized AMI is built on top of Amazon Linux 2, specifically for use as a worker node in Amazon EKS clusters\. You can use this repository to view the specifics of how the Amazon EKS team configures kubelet, Docker, the AWS IAM Authenticator for Kubernetes, and more\. 

 The build scripts repository includes a [HashiCorp Packer](https://www.packer.io/) template and build scripts to generate an AMI\. These scripts are the source of truth for Amazon EKS\-optimized AMI builds, so you can follow the GitHub repository to monitor changes to our AMIs\. For example, perhaps you want your own AMI to use the same version of Docker that the EKS team uses for the official AMI\. 

The GitHub repository also contains the specialized [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) that runs at boot time to configure your instance's certificate data, control plane endpoint, cluster name, and more\.

 Additionally, the GitHub repository contains our Amazon EKS worker node AWS CloudFormation templates\. These templates make it easier to spin up an instance running the Amazon EKS\-optimized AMI and register it with a cluster\.

 For more information, see the repositories on GitHub at [https://github\.com/awslabs/amazon\-eks\-ami](https://github.com/awslabs/amazon-eks-ami)\.