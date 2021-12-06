# Launch template support<a name="launch-templates"></a>

Managed node groups are always deployed with an Amazon EC2 Auto Scaling Group launch template\. If you don't specify your own launch template to use when creating a managed node group, the Amazon EKS API creates a launch template with default values in your account\. Creating your own launch template and a managed node group from that template provides you with greater flexibility when deploying managed nodes than the default launch template\. For the highest level of customization, you can deploy managed nodes using your own launch template and a custom AMI\. If you don't use your own launch template, one will be created automatically\. We don't recommend that you modify auto\-generated launch templates\. So, make sure to specify a custom one when first creating a managed node group if you want that ability\.

After you deployed a managed node group with your own launch template, update it with a different version of the same launch template\. When you update your node group to a different version of your launch template, all nodes in the group are recycled to match the new configuration of the specified launch template version\. Existing node groups that don't use a custom launch template can't be updated directly\. Rather, you must create a new node group with a custom launch template to do so\.

## Launch template configuration basics<a name="launch-template-basics"></a>

You can create an Amazon EC2 Auto Scaling launch template with the AWS Management Console, AWS CLI, or an AWS SDK\. For more information, see [Creating a Launch Template for an Auto Scaling Group](https://docs.aws.amazon.com/autoscaling/ec2/userguide/create-launch-template.html) in the *Amazon EC2 Auto Scaling User Guide*\. Some of the settings in a launch template are similar to the settings used for managed node configuration\. When deploying or updating a node group with a launch template, some settings must be specified in either the node group configuration or the launch template\. Don't specify both places\. If a setting exists where it shouldn't, then operations such as creating or updating a node group fail\. 

The following table lists the settings that are prohibited in a launch template\. It also lists similar settings, if any are available, are required in the managed node group configuration\. The listed settings are the settings that appear in the console\. They might have similar but different names in the AWS CLI and SDK\.


| Launch template – Prohibited | Amazon EKS node group configuration | 
| --- | --- | 
| IAM instance profile under Advanced details | Node IAM Role under Node Group configuration on the Configure Node Group page | 
| Subnet under Network interfaces \(Add network interface\) | Subnets under Node Group network configuration on the Specify networking page | 
| Shutdown behavior and Stop \- Hibernate behavior under Advanced details\. Retain default Don't include in launch template setting in launch template for both settings\. | No equivalent\. Amazon EKS must control the instance lifecycle, not the Auto Scaling group\. | 

The following table lists the prohibited settings in a managed node group configuration\. It also lists similar settings, if any are available, which are required in a launch template\. The listed settings are the settings that appear in the console\. They might have similar names in the AWS CLI and SDK\.


| Amazon EKS node group configuration – Prohibited |  Launch template | 
| --- | --- | 
|  \(Only if you specified a custom AMI in a launch template\) **AMI type** under **Node Group compute configuration** on **Set compute and scaling configuration** page – Console displays **Specified in launch template** and the AMI ID that was specified\. If an AMI type wasn't specified in the launch template, you can select an AMI in the node group configuration\.  |  **AMI** under ****Launch template contents**** – You must specify an ID if you have either of the following requirements: [\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/launch-templates.html)  | 
| Disk size under Node Group compute configuration on Set compute and scaling configuration page – Console displays Specified in launch template\. | Size under Storage \(Volumes\) \(Add new volume\)\. You must specify this in the launch template\. | 
| SSH key pair under Node Group configuration on the Specify Networking page – The console displays the key that was specified in the launch template or displays Not specified in launch template\. | Key pair name under Key pair \(login\)\. | 
| You can't specify source security groups that are allowed remote access when using a launch template\. | Security groups under Network settings for the instance or Security groups under Network interfaces \(Add network interface\), but not both\. For more information, see [Using custom security groups](#launch-template-security-groups)\. | 

**Note**  
If you deploy a node group using a launch template, specify zero or one **Instance type** under **Launch template contents** in a launch template\. Alternatively, you can specify 0–20 instance types for **Instance types** on the **Set compute and scaling configuration** page in the console\. Or, you can do so using other tools that use the Amazon EKS API\. If you specify an instance type in a launch template, and use that launch template to deploy your node group, then you can't specify any instance types in the console or using other tools that use the Amazon EKS API\. If you don't specify an instance type in a launch template, in the console, or using other tools that use the Amazon EKS API, the `t3.medium` instance type is used\. If your node group is using the Spot capacity type, then we recommend specifying multiple instance types using the console\. For more information, see [Managed node group capacity types](managed-node-groups.md#managed-node-group-capacity-types)\. 
If any containers that you deploy to the node group use the Instance Metadata Service Version 2, make sure to set the **Metadata response hop limit** to `2` in your launch template\. For more information, see [Instance metadata and user data](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html) in the *Amazon EC2 User Guide for Linux Instances*\. If you deploy a managed node group without using a custom launch template, this value is automatically set for the node group in the default launch template\.

## Tagging Amazon EC2 instances<a name="launch-template-tagging"></a>

You can use the `TagSpecification` parameter of a launch template to specify which tags to apply to Amazon EC2 instances in your node group\. The IAM entity calling the `CreateNodegroup` or `UpdateNodegroupVersion` APIs must have permissions for `ec2:RunInstances` and `ec2:CreateTags`, and the tags must be added to the launch template\.

## Using custom security groups<a name="launch-template-security-groups"></a>

You can use a launch template to specify custom Amazon EC2 [security groups](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html) to apply to instances in your node group\. This can be either in the instance level security groups parameter or as part of the network interface configuration parameters\. However, you can't create a launch template that specifies both instance level and network interface security groups\. Consider the following conditions that apply to using custom security groups with managed node groups:
+ Amazon EKS only allows launch templates with a single network interface specification\.
+ By default, Amazon EKS applies the [cluster security group](sec-group-reqs.md#cluster-sg) to the instances in your node group to facilitate communication between nodes and the control plane\. If you specify custom security groups in the launch template using either option mentioned earlier, Amazon EKS doesn't add the cluster security group\. So, you must ensure that the inbound and outbound rules of your security groups enable communication with the endpoint of your cluster\. If your security group rules are incorrect, the worker nodes can't join the cluster\. For more information about security group rules, see [Amazon EKS security group considerations](sec-group-reqs.md)\.
+ If you need SSH access to the instances in your node group, include a security group that allows that access\.

## Amazon EC2 user data<a name="launch-template-user-data"></a>

The launch template includes a section for custom user data\. You can specify configuration settings for your node group in this section without manually creating individual custom AMIs\. For more information about the settings available for Bottlerocket, see [Using user data](https://github.com/bottlerocket-os/bottlerocket#using-user-data) on GitHub\.

You can supply Amazon EC2 user data in your launch template using `cloud-init` when launching your instances\. For more information, see the [cloud\-init](https://cloudinit.readthedocs.io/en/latest/index.html) documentation\. Your user data can be used to perform common configuration operations\. This includes the following operations:
+ [Including users or groups](https://cloudinit.readthedocs.io/en/latest/topics/examples.html#including-users-and-groups)
+ [Installing packages](https://cloudinit.readthedocs.io/en/latest/topics/examples.html#install-arbitrary-packages)

Amazon EC2 user data in launch templates that are used with managed node groups must be in the [MIME multi\-part archive](https://cloudinit.readthedocs.io/en/latest/topics/format.html#mime-multi-part-archive) format for Amazon Linux AMIs and TOML format for Bottlerocket AMIs\. This is because your user data is merged with Amazon EKS user data required for nodes to join the cluster\. Don't specify any commands in your user data that starts or modifies `kubelet`\. This is performed as part of the user data merged by Amazon EKS\. Certain `kubelet` parameters, such as setting labels on nodes, can be configured directly through the managed node groups API\.

**Note**  
For more information about advanced `kubelet` customization, including manually starting it or passing in custom configuration parameters, see [Specifying an AMI](#launch-template-custom-ami)\. If a custom AMI ID is specified in a launch template, Amazon EKS doesn't merge user data\.

The following details provide more information about the user data section for Amazon Linux or Bottlerocket\.

------
#### [ Amazon Linux user data ]

You can combine multiple user data blocks together into a single MIME multi\-part file\. For example, you can combine a cloud boothook that configures the Docker daemon with a user data shell script that installs a custom package\. A MIME multi\-part file consists of the following components:
+ The content type and part boundary declaration – `Content-Type: multipart/mixed; boundary="==BOUNDARY=="`
+ The MIME version declaration – `MIME-Version: 1.0`
+ One or more user data blocks, which contain the following components:
  + The opening boundary, which signals the beginning of a user data block – `--==BOUNDARY==`
  + The content type declaration for the block: `Content-Type: text/cloud-config; charset="us-ascii"`\. For more information about content types, see the [cloud\-init](https://cloudinit.readthedocs.io/en/latest/topics/format.html) documentation\.
  + The content of the user data \(for example, a list of shell commands or `cloud-init` directives\)\.
  + The closing boundary, which signals the end of the MIME multi\-part file: `--==BOUNDARY==--`

  The following is an example of a MIME multi\-part file that you can use to create your own\.

  ```
  MIME-Version: 1.0
  Content-Type: multipart/mixed; boundary="==MYBOUNDARY=="
  
  --==MYBOUNDARY==
  Content-Type: text/x-shellscript; charset="us-ascii"
  
  #!/bin/bash
  echo "Running custom user data script"
  
  --==MYBOUNDARY==--
  ```

------
#### [ Bottlerocket user data ]

Bottlerocket structures user data in the TOML format\. You can provide user data to be merged with the user data provided by Amazon EKS\. For example, you can provide additional `kubelet` settings\.

```
[settings.kubernetes.system-reserved]
cpu = "10m"
memory = "100Mi"
ephemeral-storage= "1Gi"
```

For more information about the supported settings, see [Bottlerocket documentation](https://github.com/bottlerocket-os/bottlerocket)\. You can configure node labels and taints in your user data\. However, we recommend that you configure these within your node group instead\. Amazon EKS applies these configurations when you do so\.

When user data is merged, formatting isn't preserved, but the content remains the same\. The configuration that you provide in your user data overrides any settings that are configured by Amazon EKS\. So, if you set `settings.kubernetes.max-pods` or `settings.kubernetes.cluster-dns-ip`, values in your user data are applied to the nodes\.

Amazon EKS doesn't support all valid TOML\. The following is a list of known unsupported formats:
+ Quotes within quoted keys: `'quoted "value"' = "value"`
+ Escaped quotes in values: `str = "I'm a string. \"You can quote me\""`
+ Mixed floats and integers: `numbers = [ 0.1, 0.2, 0.5, 1, 2, 5 ]`
+ Mixed types in arrays: `contributors = ["foo@example.com", { name = "Baz", email = "baz@example.com" }]`
+ Bracketed headers with quoted keys: `[foo."bar.baz"]`

------

## Specifying an AMI<a name="launch-template-custom-ami"></a>

If you have either of the following requirements, then specify an AMI ID in the `imageId` field of your launch template\. Select the requirement you have for additional information\.

### Provide user data to pass arguments to the `bootstrap.sh` file included with an Amazon EKS optimized AMI<a name="mng-specify-eks-ami"></a>

You can pass the arguments to the `bootstrap.sh` by using `eksctl` without specifying a launch template\. Or you can do so by specifying the information in the user data section of a launch template\.

------
#### [ Eksctl without specifying a launch template ]

Create a file named `my-nodegroup.yaml` with the following contents\. This example creates a node group that provides an additional `kubelet` argument to set a custom `max pods` value using the `bootstrap.sh` script included with the Amazon EKS optimized AMI\. For more information, see the [https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) file on GitHub\.

Replace every `<example value>` \(including `<>`\) with your own values\.

```
---
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: <my-cluster-name>
  region: <us-west-2>

managedNodeGroups:
  - name: <my-nodegroup
    ami: <ami-0e6af48ea232fbdb1>
    instanceType: <m5.large>
    privateNetworking: true
    disableIMDSv1: true
    labels: { <x86-al2-specified-mng> }
    overrideBootstrapCommand: |
      #!/bin/bash
      /etc/eks/bootstrap.sh <my-cluster-name> \
        --kubelet-extra-args <'--max-pods=40'> \
        --b64-cluster-ca <certificateAuthority> \
        --apiserver-endpoint <endpoint> \
        --dns-cluster-ip <serivceIpv4Cidr>.10 \
        --use-max-pods false
```

The only required argument in the previous example is the cluster name \(`my-cluster-name`\)\. However, by setting the values for `--apiserver-endpoint`, `--b64-cluster-ca`, and `--dns-cluster-ip`, there's no need for the `bootstrap` script to make a `describeCluster` call\. This is useful in private cluster setups or clusters where you're scaling in and out nodes frequently\.

You can find the values for your cluster to specify the values for the optional arguments with the following command\.

```
aws eks describe-cluster --name <my-cluster-name>
```

The example values for the optional arguments are the name of the properties returned in the output from the command\. The value for `--dns-cluster-ip` is your service CIDR with `.10` at the end\. For example, if the returned value for s`erviceIpv4Cidr` is `10.100.0.0/16`, then your value is `10.100.0.10`\. 

For every available `eksctl` `config` file option, see [Config file schema](https://eksctl.io/usage/schema/) in the `eksctl` documentation\. `Eksctl` still creates a launch template for you and populates its user data with the data that you provide in the `config` file\.

Create your node group with the following command\.

```
eksctl create nodegroup --config-file=my-nodegroup.yaml
```

------
#### [ User data in a launch template ]

Specify the following information in the user data section of your launch template\. Replace every `<example value>` \(including `<>`\) with your own values\. This example creates a node group that provides an additional `kubelet` argument to set a custom `max pods` value using the `bootstrap.sh` script included with the Amazon EKS optimized AMI\. For more information, see the [https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) file on GitHub\.

```
#!/bin/bash
/etc/eks/bootstrap.sh <my-cluster-name> \
--kubelet-extra-args <'--max-pods=40'> \
--b64-cluster-ca <certificateAuthority> \
--apiserver-endpoint <endpoint> 
--dns-cluster-ip <serivceIpv4Cidr>.10
--use-max-pods false
```

The only required argument in the previous example is the cluster name \(`<my-cluster-name>`\)\. However, by setting the values for `--apiserver-endpoint`, `--b64-cluster-ca`, and `--dns-cluster-ip`, there's no need for the `bootstrap` script to make a `describeCluster` call\. This is useful in private cluster setups or clusters where you're scaling in and out nodes frequently\.

You can find the values for your cluster to specify the values for the optional arguments with the following command\.

```
aws eks describe-cluster --name <my-cluster-name>
```

The example values for the optional arguments are the name of the properties returned in the output from the command\. The value for `--dns-cluster-ip` is your service CIDR with `.10` at the end\. For example, if the returned value for s`erviceIpv4Cidr` is `10.100.0.0/16`, then your value is `10.100.0.10`\. 

------

### Run a custom AMI due to specific security, compliance, or internal policy requirements<a name="mng-specify-custom-ami"></a>

For more information, see [Amazon Machine Images \(AMI\)](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html) in the *Amazon EC2 User Guide for Linux Instances*\. The Amazon EKS AMI build specification contains resources and configuration scripts for building a custom Amazon EKS AMI based on Amazon Linux 2\. For more information, see [Amazon EKS AMI Build Specification](https://github.com/awslabs/amazon-eks-ami/) on GitHub\. To build custom AMIs installed with other operating systems, see [Amazon EKS Sample Custom AMIs](https://github.com/aws-samples/amazon-eks-custom-amis) on GitHub\.

**Important**  
When specifying an AMI, Amazon EKS doesn't merge any user data\. Rather, you're responsible for supplying the required `bootstrap` commands for nodes to join the cluster\. If your nodes fail to join the cluster, the Amazon EKS `CreateNodegroup` and `UpdateNodegroupVersion` actions also fail\.

**The following are the limits and conditions involved with specifying an AMI ID with managed node groups:**
+ You must create a new node group to switch between specifying an AMI ID in a launch template and not specifying an AMI ID\.
+ You aren't notified in the console when a newer AMI version is available\. To update your node group to a newer AMI version, you need to create a new version of your launch template with an updated AMI ID\. Then, you need to update the node group with the new launch template version\. 
+ The following fields can't be set in the API if you specify an AMI ID: 
  + `amiType`
  + `releaseVersion`
  + `version`
+ You can't specify a Windows AMI ID because Windows can't be used in managed node groups\.