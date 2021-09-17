# Amazon EKS optimized Amazon Linux AMI build script<a name="eks-ami-build-scripts"></a>

Amazon Elastic Kubernetes Service \(Amazon EKS\) has open\-sourced the build scripts that are used to build the Amazon EKS optimized AMI\. These build scripts are now available [on GitHub](https://github.com/awslabs/amazon-eks-ami)\.

The Amazon EKS optimized Amazon Linux AMI is built on top of Amazon Linux 2, specifically for use as a node in Amazon EKS clusters\. You can use this repository to view the specifics of how the Amazon EKS team configures  `kubelet`  , Docker, the AWS IAM Authenticator for Kubernetes, and more\. 

The build scripts repository includes a [HashiCorp packer](https://www.packer.io/) template and build scripts to generate an AMI\. These scripts are the source of truth for Amazon EKS optimized AMI builds, so you can follow the GitHub repository to monitor changes to our AMIs\. For example, perhaps you want your own AMI to use the same version of Docker that the EKS team uses for the official AMI\. 

The GitHub repository also contains the specialized [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) that runs at boot time to configure your instance's certificate data, control plane endpoint, cluster name, and more\.

Additionally, the GitHub repository contains our Amazon EKS node AWS CloudFormation templates\. These templates make it easier to spin up an instance running the Amazon EKS optimized AMI and register it with a cluster\.

For more information, see the repositories on GitHub at [https://github\.com/awslabs/amazon\-eks\-ami](https://github.com/awslabs/amazon-eks-ami)\.

Amazon EKS optimized Amazon Linux 2 contains an optional bootstrap flag to enable the containerd runtime\. When bootstrapped in Amazon EKS optimized accelerated Amazon Linux AMIs for v1\.21, [AWS Inferentia](http://aws.amazon.com/machine-learning/inferentia/) workloads are not supported\.

## Configuring VT1 for your custom Amazon Linux AMI<a name="vt1"></a>

Custom Amazon Linux AMIs in Amazon EKS can support the VT1 video transcoding instance family for Amazon Linux 2, Ubuntu 18, and Ubuntu 20\. VT1 supports the Xilinx U30 media transcoding cards with accelerated H\.264/AVC and H\.265/HEVC codecs\. To get the benefit of these accelerated instances, you must follow these steps: 

1. Create and launch a base AMI from Amazon Linux 2, Ubuntu 18, or Ubuntu 20\.

1. After the based AMI is launched, Install the [XRT driver](https://xilinx.github.io/video-sdk/) and runtime on the node\.

1. [Create a cluster](https://docs.aws.amazon.com/eks/latest/userguide/create-cluster.html)\.

1. Install the Kubernetes [FPGA plugin](https://github.com/Xilinx/FPGA_as_a_Service/tree/master/k8s-fpga-device-plugin) on your cluster\.

   ```
   kubectl apply -f fpga-device-plugin.yml
   ```

The plugin will now advertise Xilinx U30 devices per node on your Amazon EKS cluster\. You can use the FFMPEG docker image to run example video transcoding workloads on your Amazon EKS cluster\.