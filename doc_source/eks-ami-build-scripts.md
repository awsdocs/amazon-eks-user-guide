# Amazon EKS optimized Amazon Linux AMI build script<a name="eks-ami-build-scripts"></a>

Amazon Elastic Kubernetes Service \(Amazon EKS\) has open\-source scripts that are used to build the Amazon EKS optimized AMI\. These build scripts are available [on GitHub](https://github.com/awslabs/amazon-eks-ami)\.

The Amazon EKS optimized Amazon Linux AMI is built on top of Amazon Linux 2 \(AL2\) and Amazon Linux 2023 \(AL2023\), specifically for use as a node in Amazon EKS clusters\. You can use this repository to view the specifics of how the Amazon EKS team configures `kubelet` , Docker, the AWS IAM Authenticator for Kubernetes, and build your own Amazon Linux based AMI from scratch\. 

The build scripts repository includes a [HashiCorp packer](https://www.packer.io/) template and build scripts to generate an AMI\. These scripts are the source of truth for Amazon EKS optimized AMI builds, so you can follow the GitHub repository to monitor changes to our AMIs\. For example, perhaps you want your own AMI to use the same version of Docker that the Amazon EKS team uses for the official AMI\. 

The GitHub repository also contains the specialized [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) and [nodeadm script](https://awslabs.github.io/amazon-eks-ami/nodeadm/) that runs at boot time to configure your instance's certificate data, control plane endpoint, cluster name, and more\.

Additionally, the GitHub repository contains our Amazon EKS node AWS CloudFormation templates\. These templates make it easier to spin up an instance running the Amazon EKS optimized AMI and register it with a cluster\.

For more information, see the repositories on GitHub at [https://github\.com/awslabs/amazon\-eks\-ami](https://github.com/awslabs/amazon-eks-ami)\.

Amazon EKS optimized AL2 contains an optional bootstrap flag to enable the `containerd` runtime\.