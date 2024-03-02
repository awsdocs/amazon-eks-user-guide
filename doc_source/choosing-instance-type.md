# Choosing an Amazon EC2 instance type<a name="choosing-instance-type"></a>

Amazon EC2 provides a wide selection of instance types for worker nodes\. Each instance type offers different compute, memory, storage, and network capabilities\. Each instance is also grouped in an instance family based on these capabilities\. For a list, see [Available instance types](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html#AvailableInstanceTypes) in the *Amazon EC2 User Guide for Linux Instances* and [Available instance types](https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/instance-types.html#AvailableInstanceTypes) in the *Amazon EC2 User Guide for Windows Instances*\. Amazon EKS releases several variations of Amazon EC2 AMIs to enable support\. To make sure that the instance type you select is compatible with Amazon EKS, consider the following criteria\.
+ All Amazon EKS AMIs don't currently support the `g5g` and `mac` families\.
+ Arm and non\-accelerated Amazon EKS AMIs don't support the `g3`, `g4`, `inf`, and `p` families\.
+ Accelerated Amazon EKS AMIs don't support the `a`, `c`, `hpc`, `m`, and `t` families\.
+ For Arm\-based instances, Amazon Linux 2023 \(AL2023\) only supports instance types that use Graviton2 or later processors\. AL2023 doesn't support `A1` instances\.

When choosing between instance types that are supported by Amazon EKS, consider the following capabilities of each type\.

**Number of instances in a node group**  
In general, fewer, larger instances are better, especially if you have a lot of Daemonsets\. Each instance requires API calls to the API server, so the more instances you have, the more load on the API server\.

**Operating system**  
Review the supported instance types for [Linux](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html), [Windows](https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/instance-types.html), and [Bottlerocket](https://aws.amazon.com/bottlerocket/faqs/)\. Before creating Windows instances, review [Enabling Windows support for your Amazon EKS cluster](windows-support.md)\.

**Hardware architecture**  
Do you need x86 or Arm? You can only deploy Linux on Arm\. Before deploying Arm instances, review [Amazon EKS optimized Arm Amazon Linux AMIs](eks-optimized-ami.md#arm-ami)\. Do you need instances built on the Nitro System \([Linux](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html#ec2-nitro-instances) or [Windows](https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/instance-types.html#ec2-nitro-instances)\) or that have [Accelerated](https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/accelerated-computing-instances.html) capabilities? If you need accelerated capabilities, you can only use Linux with Amazon EKS\.

**Maximum number of Pods**  
Since each Pod is assigned its own IP address, the number of IP addresses supported by an instance type is a factor in determining the number of Pods that can run on the instance\. To manually determine how many Pods an instance type supports, see [Amazon EKS recommended maximum Pods for each Amazon EC2 instance type](#determine-max-pods)\.  
If you're using an Amazon EKS optimized Amazon Linux 2 AMI that's `v20220406` or newer, you can use a new instance type without upgrading to the latest AMI\. For these AMIs, the AMI auto\-calculates the necessary `max-pods` value if it isn't listed in the `[eni\-max\-pods\.txt](https://github.com/awslabs/amazon-eks-ami/blob/master/files/eni-max-pods.txt)` file\. Instance types that are currently in preview may not be supported by Amazon EKS by default\. Values for `max-pods` for such types still need to be added to `eni-max-pods.txt` in our AMI\.
[AWS Nitro System](https://aws.amazon.com/ec2/nitro/) instance types optionally support significantly more IP addresses than non\-Nitro System instance types\. However, not all IP addresses assigned for an instance are available to Pods\. To assign a significantly larger number of IP addresses to your instances, you must have version `1.9.0` or later of the Amazon VPC CNI add\-on installed in your cluster and configured appropriately\. For more information, see [Increase the amount of available IP addresses for your Amazon EC2 nodes](cni-increase-ip-addresses.md)\. To assign the largest number of IP addresses to your instances, you must have version `1.10.1` or later of the Amazon VPC CNI add\-on installed in your cluster and deploy the cluster with the `IPv6` family\.

**IP family**  
You can use any supported instance type when using the `IPv4` family for a cluster, which allows your cluster to assign private `IPv4` addresses to your Pods and Services\. But if you want to use the `IPv6` family for your cluster, then you must use [AWS Nitro System](https://aws.amazon.com/ec2/nitro/) instance types or bare metal instance types\. Only `IPv4` is supported for Windows instances\. Your cluster must be running version `1.10.1` or later of the Amazon VPC CNI add\-on\. For more information about using `IPv6`, see [`IPv6` addresses for clusters, Pods, and services](cni-ipv6.md)\. 

**Version of the Amazon VPC CNI add\-on that you're running**  
The latest version of the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) supports [these instance types](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/pkg/vpc/vpc_ip_resource_limit.go)\. You may need to update your Amazon VPC CNI add\-on version to take advantage of the latest supported instance types\. For more information, see [Working with the Amazon VPC CNI plugin for Kubernetes Amazon EKS add\-on](managing-vpc-cni.md)\. The latest version supports the latest features for use with Amazon EKS\. Earlier versions don't support all features\. You can view features supported by different versions in the [Changelog](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/CHANGELOG.md) on GitHub\.

**AWS Region that you're creating your nodes in**  
Not all instance types are available in all AWS Regions\.

**Whether you're using security groups for Pods**  
If you're using security groups for Pods, only specific instance types are supported\. For more information, see [Security groups for Pods](security-groups-for-pods.md)\.

## Amazon EKS recommended maximum Pods for each Amazon EC2 instance type<a name="determine-max-pods"></a>

Since each Pod is assigned its own IP address, the number of IP addresses supported by an instance type is a factor in determining the number of Pods that can run on the instance\. Amazon EKS provides a script that you can download and run to determine the Amazon EKS recommended maximum number of Pods to run on each instance type\. The script uses hardware attributes of each instance, and configuration options, to determine the maximum Pods number\. You can use the number returned in these steps to enable capabilities such as [assigning IP addresses to Pods from a different subnet than the instance's](cni-custom-network.md) and [significantly increasing the number of IP addresses for your instance](cni-increase-ip-addresses.md)\. If you're using a managed node group with multiple instance types, use a value that would work for all instance types\.

1. Download a script that you can use to calculate the maximum number of Pods for each instance type\.

   ```
   curl -O https://raw.githubusercontent.com/awslabs/amazon-eks-ami/master/files/max-pods-calculator.sh
   ```

1. Mark the script as executable on your computer\.

   ```
   chmod +x max-pods-calculator.sh
   ```

1. Run the script, replacing *`m5.large`* with the instance type that you plan to deploy and `1.9.0-eksbuild.1` with your Amazon VPC CNI add\-on version\. To determine your add\-on version, see the update procedures in [Working with the Amazon VPC CNI plugin for Kubernetes Amazon EKS add\-on](managing-vpc-cni.md)\.

   ```
   ./max-pods-calculator.sh --instance-type m5.large --cni-version 1.9.0-eksbuild.1
   ```

   An example output is as follows\.

   ```
   29
   ```

   You can add the following options to the script to see the maximum Pods supported when using optional capabilities\.
   +  `--cni-custom-networking-enabled` – Use this option when you want to assign IP addresses from a different subnet than your instance's\. For more information, see [Custom networking for pods](cni-custom-network.md)\. Adding this option to the previous script with the same example values yields `20`\.
   + `--cni-prefix-delegation-enabled` – Use this option when you want to assign significantly more IP addresses to each elastic network interface\. This capability requires an Amazon Linux instance that run on the Nitro System and version `1.9.0` or later of the Amazon VPC CNI add\-on\. For more information, see [Increase the amount of available IP addresses for your Amazon EC2 nodes](cni-increase-ip-addresses.md)\. Adding this option to the previous script with the same example values yields `110`\.

You can also run the script with the `--help` option to see all available options\.

**Note**  
The max Pods calculator script limits the return value to `110` based on [Kubernetes scalability thresholds](https://github.com/kubernetes/community/blob/master/sig-scalability/configs-and-limits/thresholds.md) and recommended settings\. If your instance type has greater than 30 vCPUs, this limit jumps to `250`, a number based on internal Amazon EKS scalability team testing\. For more information, see the [Amazon VPC CNI plugin increases pods per node limits](https://aws.amazon.com/blogs/containers/amazon-vpc-cni-increases-pods-per-node-limits/) blog post\.