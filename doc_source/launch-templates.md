# Launch template support<a name="launch-templates"></a>

You can deploy a managed node group using an Amazon EC2 launch template\. Launch templates have the benefit of providing you with a greater level of flexibility and customization when deploying managed nodes\. For the highest level of customization, you can deploy managed nodes using a launch template and a custom AMI\.

After you've deployed a managed node group with a launch template, you can then update it with a different version of the same launch template\. When you update your node group to a different version of your launch template, all of the nodes in the group are recycled to match the new configuration of the specified launch template version\. Existing node groups that do not use launch templates cannot be updated directly\. Rather, you must create a new node group with a launch template to do so\.

## Launch template configuration basics<a name="launch-template-basics"></a>

You can create an Amazon EC2 Auto Scaling launch template with the AWS Management Console, AWS CLI, or an AWS SDK\. For more information, see [Creating a Launch Template for an Auto Scaling Group](https://docs.aws.amazon.com/autoscaling/ec2/userguide/create-launch-template.html) in the Amazon EC2 User Guide\. Some of the settings in a launch template are similar to the settings used for managed node configuration\. When deploying or updating a node group with a launch template, some settings must be specified in the node group configuration or the launch template, but not both\. If a setting exists where it shouldn't, then operations such as creating or updating a node group fail\. 

The following table lists the settings that are prohibited in a launch template and which similar settings \(if any\) are required in the managed node group configuration\. The listed settings are the settings that appear in the console\. They might have similar but different names in the AWS CLI and SDK\.


| Launch template – Prohibited | Amazon EKS node group configuration | 
| --- | --- | 
| IAM instance profile under Advanced details | Node IAM Role under Node Group configuration on the Configure Node Group page | 
| Subnet under Network interfaces \(Add network interface\) | Subnets under Node Group network configuration on the Specify networking page | 
| Request Spot Instances under Advanced details, Purchasing options | No equivalent is available because Spot Instances are not supported in node groups\. | 
| Shutdown behavior and Stop \- Hibernate behavior under Advanced details\. Retain default Don't include in launch template setting in launch template for both settings\. | No equivalent\. Amazon EKS must control the instance lifecycle, not the Auto Scaling group\. | 

The following table lists the settings that are prohibited in a managed node group configuration and which similar settings \(if any\) are required in a launch template\. The listed settings are the settings that appear in the console\. They might have similar names in the AWS CLI and SDK\.


| Amazon EKS node group configuration – Prohibited |  Launch template | 
| --- | --- | 
|  \(Only if you specified a custom AMI in a launch template\) **AMI type** under **Node Group compute configuration** on **Set compute and scaling configuration** page – Console displays **Specified in launch template** and the AMI ID that was specified\. If an AMI type was not specified in the launch template, then you can select an AMI in the node group configuration\.  |  AMI under Launch template contents – You must specify if you are using a custom AMI\. If you specify an AMI that doesn't meet the requirements listed in [Using a custom AMI](#launch-template-custom-ami), the node group deployment will fail\. | 
| Instance type on Set compute and scaling configuration page – Console displays Specified in launch template and the instance type that was specified\. | Instance type under Launch template contents – You must specify this setting in a launch template version to be able to select the version when creating the node group\. | 
| Disk size under Node Group compute configuration on Set compute and scaling configuration page – Console displays Specified in launch template\. | Size under Storage \(Volumes\) \(Add new volume\)\. You must specify this in the launch template\. | 
| SSH key pair under Node Group configuration on the Specify Networking page – The console displays the key that was specified in the launch template or displays Not specified in launch template\. | Key pair name under Key pair \(login\)\. | 
| You can't specify source security groups that are allowed remote access when using a launch template\. | Security groups under Network settings for the instance or Security groups under Network interfaces \(Add network interface\), but not both\. For more information, see [Using custom security groups](#launch-template-security-groups)\. | 

**Note**  
If any containers that you deploy to the node group use the Instance Metadata Service Version 2, then make sure to set the **Metadata response hop limit** to `2` in your launch template\. For more information, see [Instance metadata and user data](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html) in the Amazon EC2 User Guide\. If you deploy a managed node group without using a launch template, this value is automatically set for the node group\.

## Tagging Amazon EC2 instances<a name="launch-template-tagging"></a>

You can use the `TagSpecification` parameter of a launch template to specify which tags to apply to Amazon EC2 instances in your node group\. The IAM entity calling the `CreateNodegroup` or `UpdateNodegroupVersion` APIs must have permissions for `ec2:RunInstances` and `ec2:CreateTags`, and the tags must be added to the launch template\.

## Using custom security groups<a name="launch-template-security-groups"></a>

You can use a launch template to specify custom Amazon EC2 [security groups](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html) to apply to instances in your node group\. This can be either in the instance level security groups parameter or as part of the network interface configuration parameters\. However, you can't create a launch template that specifies both instance level and network interface security groups\. Consider the following conditions that apply to using custom security groups with managed node groups:
+ Amazon EKS only allows launch templates with a single network interface specification\.
+ By default, Amazon EKS applies the [cluster security group](https://docs.aws.amazon.com/eks/latest/userguide/sec-group-reqs.html#cluster-sg) to the instances in your node group to facilitate communication between nodes and the control plane\. If you specify custom security groups in the launch template using either option mentioned earlier, Amazon EKS doesn't add the cluster security group\. Therefore, you must ensure that the inbound and outbound rules of your security groups enable communication with your cluster’s endpoint\. Incorrect security group rules result in worker nodes being unable to join the cluster\. To learn about the security group rules that you should need to apply, see [Amazon EKS security group considerations](sec-group-reqs.md)\.
+ If you need SSH access to the instances in your node group, be sure to include a security group that allows that access\.

## Amazon EC2 user data<a name="launch-template-user-data"></a>

You can supply Amazon EC2 user data in your launch template using `cloud-init` when launching your instances\. For more information, see the [cloud\-init](https://cloudinit.readthedocs.io/en/latest/index.html) documentation\. Your user data can be used to perform common configuration operations\. This includes the following operations:
+ [Including users or groups](https://cloudinit.readthedocs.io/en/latest/topics/examples.html#including-users-and-groups)
+ [Installing packages](https://cloudinit.readthedocs.io/en/latest/topics/examples.html#install-arbitrary-packages)

Amazon EC2 user data in launch templates that are used with managed node groups must be in the [MIME multi\-part archive](https://cloudinit.readthedocs.io/en/latest/topics/format.html#mime-multi-part-archive) format\. This is because your user data is merged with Amazon EKS user data required for nodes to join the cluster\. 

**Note**  
Amazon EKS doesn't merge user data when a custom AMI is used\. For more information, see [Using a custom AMI](#launch-template-custom-ami)\.

You can combine multiple user data blocks together into a single MIME multi\-part file\. For example, you can combine a cloud boothook that configures the Docker daemon with a user data shell script that installs a custom package\. A MIME multi\-part file consists of the following components:
+ The content type and part boundary declaration – `Content-Type: multipart/mixed; boundary="==BOUNDARY=="`
+ The MIME version declaration – `MIME-Version: 1.0`
+ One or more user data blocks, which contain the following components:
  + The opening boundary, which signals the beginning of a user data block – `--==BOUNDARY==`
  + The content type declaration for the block: `Content-Type: text/cloud-config; charset="us-ascii"`\. For more information about content types, see the [cloud\-init](https://cloudinit.readthedocs.io/en/latest/topics/format.html) documentation\.
  + The content of the user data, for example, a list of shell commands or `cloud-init` directives\.
  + The closing boundary, which signals the end of the MIME multi\-part file: `--==BOUNDARY==--`

  The following is an example of a MIME multi\-part file that you can use to create your own\.

  ```
  MIME-Version: 1.0
  Content-Type: multipart/mixed; boundary="==MYBOUNDARY=="
  
  --==MYBOUNDARY==
  Content-Type: text/x-shellscript; charset="us-ascii"
  
  #!/bin/bash
  echo "Running custom user data script"
  
  --==MYBOUNDARY==--\
  ```

## Using a custom AMI<a name="launch-template-custom-ami"></a>

If your organization needs to run a custom AMI due to specific security, compliance, or internal policy requirements, you can deploy such AMIs to managed node groups by using a launch template\. For more information, see [Amazon Machine Images \(AMI\)](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html) in the Amazon EC2 User Guide for Linux Instances\. The Amazon EKS AMI build specification contains resources and configuration scripts for building a custom Amazon EKS AMI based on Amazon Linux 2\. For more information, see [Amazon EKS AMI Build Specification](https://github.com/awslabs/amazon-eks-ami/) on GitHub\. To build custom AMIs installed with other operating systems, see [Amazon EKS Sample Custom AMIs](https://github.com/aws-samples/amazon-eks-custom-amis) on GitHub\.

**Note**  
When using a custom AMI, Amazon EKS doesn't merge any user data\. Rather, you are responsible for supplying the required bootstrap commands for nodes to join the cluster\. If your nodes fail to join the cluster, the Amazon EKS `CreateNodegroup` and `UpdateNodegroupVersion` actions also fail\.

To use a custom AMI with managed node groups, specify an AMI ID in the `imageId` field of the launch template\. To update your node group to a newer version of a custom AMI, create a new version of the launch template with an updated AMI ID, and update the node group with the new launch template version\.

**Limitations of using custom AMIs with managed node groups**
+ You must create a new node group to switch between using custom AMIs and Amazon EKS optimized AMIs\.
+ The following fields can't be set in the API if you're using a custom AMI
  + `amiType`
  + `releaseVersion`
  + `version`