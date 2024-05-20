# Launching self\-managed Ubuntu nodes<a name="launch-node-ubuntu"></a>

This topic describes how to launch Auto Scaling groups of [Ubuntu for EKS](https://cloud-images.ubuntu.com/docs/aws/eks/) or [Ubuntu Pro for EKS](https://ubuntu.com/blog/ubuntu-pro-for-eks-is-now-generally-available) nodes that register with your Amazon EKS cluster\. Ubuntu and Ubuntu Pro for EKS are based on the official Ubuntu Minimal LTS, include the custom Ubuntu-AWS optimized kernel, and have been built specifically for the EKS service\. Ubuntu Pro adds additional security coverage by supporting EKS extended support periods, kernel livepatch, FIPS compliance and the ability to run unlimited Pro containers\.

After the nodes join the cluster, you can deploy containerized applications to them\. For more information about Ubuntu eks, visit the [technical documentation](https://documentation.canonical.com/aws) and [Custom AMI support](https://eksctl.io/usage/custom-ami-support/) in the `eksctl` documentation\.


**Important**  
- Amazon EKS nodes are standard Amazon EC2 instances, and you are billed for them based on normal Amazon EC2 instance prices\. For more information, see [Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/)\.
- You can launch Ubuntu nodes in Amazon EKS extended clusters on AWS Outposts, but you can't launch them in local clusters on AWS Outposts\. For more information, see [Amazon EKS on AWS Outposts](eks-outposts.md)\.
- You can deploy to Amazon EC2 instances with `x86` or Arm processors\. However, instances that have Inferentia chips may need to install the [Neuron SDK](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/) first.
- Ubuntu for EKS is compatible with AWS CloudFormation\. However, there is no official CloudFormation template that can be copied to deploy Ubuntu nodes for Amazon EKS\.

**To launch Ubuntu for EKS or Ubuntu Pro for EKS nodes using `eksctl`**

This procedure requires `eksctl` version `0.177.0` or later\. You can check your version with the following command:

```
eksctl version
```

For instructions on how to install or upgrade `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.
**Note**  
This procedure only works for clusters that were created with `eksctl`\.

1. Copy the following contents to your device\. Replace `my-cluster` with the name of your cluster\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can't be longer than 100 characters\. Replace `ng-ubuntu` with a name for your node group\. The node group name can't be longer than 63 characters\. It must start with letter or digit, but can also include hyphens and underscores for the remaining characters\. To deploy on Arm instances, replace `m5.large` with an Arm instance type\. Replace `my-ec2-keypair-name` with the name of an Amazon EC2 SSH key pair that you can use to connect using SSH into your nodes with after they launch\. If you don't already have an Amazon EC2 key pair, you can create one in the AWS Management Console\. For more information, see [Amazon EC2 key pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) in the *Amazon EC2 User Guide for Linux Instances*\. Replace all remaining *`example values`* with your own values\. Once you've made the replacements, run the modified command to create the `ubuntu.yaml` file\.

**Important**  
To deploy a node group to AWS Outposts, AWS Wavelength, or AWS Local Zone subnets, don't pass AWS Outposts, AWS Wavelength, or AWS Local Zone subnets when you create the cluster\. You must specify the subnets in the following example\. For more information see [Create a nodegroup from a config file](https://eksctl.io/usage/nodegroups/#creating-a-nodegroup-from-a-config-file) and [Config file schema](https://eksctl.io/usage/schema/) in the `eksctl` documentation\. Replace `region-code` with the AWS Region that your cluster is in\.

   ```
   cat >ubuntu.yaml <<EOF
   ---
   apiVersion: eksctl.io/v1alpha5
   kind: ClusterConfig
   
   metadata:
     name: my-cluster
     region: region-code
     version: '1.30'
   
   iam:
     withOIDC: true
   
   nodeGroups:
     - name: ng-ubuntu
       instanceType: m5.large
       desiredCapacity: 3
       amiFamily: Ubuntu22.04
       ami: auto-ssm
       iam:
          attachPolicyARNs:
             - arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy
             - arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly
             - arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
             - arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy
       ssh:
           allow: true
           publicKeyName: my-ec2-keypair-name
   EOF
   ```

For launching an Ubuntu Pro cluster, just change the `amiFamily` value to  `UbuntuPro2204`

1. Deploy your nodes with the following command\.

   ```
   eksctl create nodegroup --config-file=ubuntu.yaml
   ```

   An example output is as follows\.

   Several lines are output while the nodes are created\. One of the last lines of output is the following example line\.

   ```
   [✔]  created 1 nodegroup(s) in cluster "my-cluster"
   ```

1. \(Optional\) Deploy a [sample application](sample-deployment.md) to test your Ubuntu nodes\.
