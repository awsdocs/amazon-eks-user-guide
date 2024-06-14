--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Choosing an Amazon EC2 instance type<a name="choosing-instance-type"></a>

Amazon EC2 provides a wide selection of instance types for worker nodes\. Each instance type offers different compute, memory, storage, and network capabilities\. Each instance is also grouped in an instance family based on these capabilities\. For a list, see \{https\-\-\-docs\-aws\-amazon\-com\-AWSEC2\-latest\-UserGuide\-instance\-types\-html\-AvailableInstanceTypes\}\[Available instance types\] in the *Amazon EC2 User Guide for Linux Instances* and \{https\-\-\-docs\-aws\-amazon\-com\-AWSEC2\-latest\-WindowsGuide\-instance\-types\-html\-AvailableInstanceTypes\}\[Available instance types\] in the *Amazon EC2 User Guide for Windows Instances*\. Amazon EKS releases several variations of Amazon EC2 AMIs to enable support\. To make sure that the instance type you select is compatible with Amazon EKS, consider the following criteria\.
+ All Amazon EKS AMIs don’t currently support the `g5g` and `mac` families\.
+  Arm and non\-accelerated Amazon EKS AMIs don’t support the `g3`, `g4`, `inf`, and `p` families\.
+ Accelerated Amazon EKS AMIs don’t support the `a`, `c`, `hpc`, `m`, and `t` families\.
+ For Arm\-based instances, Amazon Linux 2023 \(AL2023\) only supports instance types that use Graviton2 or later processors\. AL2023 doesn’t support `A1` instances\.

When choosing between instance types that are supported by Amazon EKS, consider the following capabilities of each type\.

Number of instances in a node group  
+ In general, fewer, larger instances are better, especially if you have a lot of Daemonsets\. Each instance requires API calls to the API server, so the more instances you have, the more load on the API server\.

Operating systemHardware architectureMaximum number of Pods   
\+`NOTE: If you’re using an Amazon EKS optimized Amazon Linux 2 AMI that’s `v20220406` or newer, you can use a new instance type without upgrading to the latest AMI\. For these AMIs, the AMI auto\-calculates the necessary `max-pods` value if it isn’t listed in the ` [eni\-max\-pods\.txt](https://github.com/awslabs/amazon-eks-ami/blob/main/templates/shared/runtime/eni-max-pods.txt) ` file\. Instance types that are currently in preview may not be supported by Amazon EKS by default\. Values for max\-pods` for such types still need to be added to `eni-max-pods.txt` in our AMI\.

IP familyVersion of the Amazon VPC CNI add\-on that you’re running AWS Region that you’re creating your nodes in  
+ Not all instance types are available in all AWS Regions\.

Whether you’re using security groups for Pods   

## Amazon EKS recommended maximum Pods for each Amazon EC2 instance type<a name="determine-max-pods"></a>

1. Download a script that you can use to calculate the maximum number of Pods for each instance type\.

   ```
   curl -O https://raw.githubusercontent.com/awslabs/amazon-eks-ami/master/templates/al2/runtime/max-pods-calculator.sh
   ```

1. Mark the script as executable on your computer\.

   ```
   chmod +x max-pods-calculator.sh
   ```

   ```
   ./max-pods-calculator.sh --instance-type m5.large --cni-version 1.9.0-eksbuild.1
   ```

   An example output is as follows\.

   ```
   `29`
   ```

   You can add the following options to the script to see the maximum Pods supported when using optional capabilities\.

You can also run the script with the `--help` option to see all available options\.

**Note**  