# Choosing an Amazon EC2 instance type<a name="choosing-instance-type"></a>

Each Amazon EC2 instance type offers different compute, memory, storage, and network capabilities, and is grouped in an instance family based on these capabilities\.

Consider the following criteria before choosing an instance type for a node group\.
+ **Number of instances in a node group** – In general, fewer, larger instances are better, especially if you have a lot of Daemonsets\. Each instance requires API calls to the API server, so the more instances you have, the more load on the API server\.
+ **Operating system** – Review the supported instance types for [Linux](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html), [Windows](https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/instance-types.html), and [Bottlerocket](http://aws.amazon.com/bottlerocket/faqs/)\. Before creating Windows instances, review [Windows support](windows-support.md)\.
+ **Hardware architecture** – Do you need x86 or Arm? You can only deploy Linux on Arm\. Before deploying Arm instances, review [Amazon EKS optimized Arm Amazon Linux AMIs](eks-optimized-ami.md#arm-ami)\. Do you need instances built on the Nitro System \([Linux](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html#ec2-nitro-instances) or [Windows](https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/instance-types.html#ec2-nitro-instances)\) or that have [Accelerated](https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/accelerated-computing-instances.html) capabilities? Amazon EKS only supports Linux on accelerated instances\. 
+ **Maximum number of pods** – Since each pod is assigned its own IP address, the number of IP addresses for an instance are a factor in determining the number of pods that can run on an instance\. [AWS Nitro System](http://aws.amazon.com/ec2/nitro/) instance types optionally support significantly more IP addresses than non Nitro System instance types\. Not all IP addresses assigned for an instance are available to pods however\. To determine how many pods an instance type supports, see [Amazon EKS recommended maximum pods for each Amazon EC2 instance type](#determine-max-pods)\. 
+ **Version of the Amazon VPC CNI add\-on that you're running** – The latest version of the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) supports [these instance types](https://github.com/aws/amazon-vpc-cni-k8s/blob/release-1.9/pkg/awsutils/vpc_ip_resource_limit.go)\. You may need to update your Amazon VPC CNI add\-on version to take advantage of the latest supported instance types\. For more information, see [Updating the Amazon VPC CNI self\-managed add\-on](managing-vpc-cni.md#updating-vpc-cni-add-on)\. The latest version supports the latest features for use with Amazon EKS\. Earlier versions don't support all features\. You can view features supported by different versions in the [Changelog](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/CHANGELOG.md) on GitHub\.
+ **Region that you're creating your nodes in** – Not all instance types are available in all Regions\.
+ **Whether you're using [security groups for pods](security-groups-for-pods.md)** – If you are, only specific instance types are supported\. For more information, see [Amazon EC2 supported instances and branch network interfaces](security-groups-for-pods.md#supported-instance-types)\.

## Amazon EKS recommended maximum pods for each Amazon EC2 instance type<a name="determine-max-pods"></a>

Amazon EKS provides a script that you can download and run to determine the Amazon EKS recommended maximum number of pods to run on each instance type\. The script uses hardware attributes of each instance, and configuration options, to determine the max pods number\. You can use the number returned in these steps to enable capabilities such as [assigning IP addresses to pods from a different subnet than the instance's](cni-custom-network.md) and [significantly increasing the number of IP addresses for your instance](cni-increase-ip-addresses.md)\.

1. Download a script that you can use to calculate the maximum number of pods for each instance type\.

   ```
   curl -o max-pods-calculator.sh https://raw.githubusercontent.com/awslabs/amazon-eks-ami/master/files/max-pods-calculator.sh
   ```

1. Mark the script as executable on your computer\.

   ```
   chmod +x max-pods-calculator.sh
   ```

1. Run the script, replacing *`<m5.large>`* \(including *`<>`*\) with the instance type that you plan to deploy and *<1\.9\.0\-eksbuild\.1>* with your Amazon VPC CNI add\-on version\. To determine your add\-on version, see the update procedures in [Managing the Amazon VPC CNI add\-on](managing-vpc-cni.md)\.

   ```
   ./max-pods-calculator.sh --instance-type <m5.large> --cni-version <1.9.0-eksbuild.1>
   ```

   Output

   ```
   29
   ```

   You can add the following options to the script to see the maximum pods supported when using optional capabilities\.
   +  `--cni-custom-networking-enabled` – Use this option when you want to assign IP addresses from a different subnet than your instance's\. For more information, see [CNI custom networking](cni-custom-network.md)\. Adding this option to the previous script with the same example values yields `20`\.
   + `--cni-prefix-delegation-enabled` – Use this option when you want to assign significantly more IP addresses to each elastic network interface\. This capability requires an Amazon Linux instance that run on the Nitro System and version 1\.9\.0 or later of the Amazon VPC CNI add\-on\. For more information, see [Increase the amount of available IP addresses for your Amazon EC2 nodes](cni-increase-ip-addresses.md)\. Adding this option to the previous script with the same example values yields `110`\.

You can also run the script with the `--help` option to see all available options\.