--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Launching self\-managed Ubuntu nodes<a name="launch-node-ubuntu"></a>

**Note**  

This topic describes how to launch Auto Scaling groups of [Ubuntu on Amazon Elastic Kubernetes Service \(EKS\)](https://cloud-images.ubuntu.com/aws-eks/) or [Ubuntu Pro on Amazon Elastic Kubernetes Service \(EKS\)](https://ubuntu.com/blog/ubuntu-pro-for-eks-is-now-generally-available) nodes that register with your Amazon EKS cluster\. Ubuntu and Ubuntu Pro for EKS are based on the official Ubuntu Minimal LTS, include the custom AWS kernel that is jointly developed with AWS, and have been built specifically for EKS\. Ubuntu Pro adds additional security coverage by supporting EKS extended support periods, kernel livepatch, FIPS compliance and the ability to run unlimited Pro containers\.

After the nodes join the cluster, you can deploy containerized applications to them\. For more information, visit the documentation for [Ubuntu on AWS](https://documentation.ubuntu.com/aws/en/latest/) and [Custom AMI support](https://eksctl.io/usage/custom-ami-support/) in the `eksctl` documentation\.

**Important**  
Amazon EKS nodes are standard Amazon EC2 instances, and you are billed for them based on normal Amazon EC2 instance prices\. For more information, see [Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/)\.
You can deploy to Amazon EC2 instances with `x86` or Arm processors\. However, instances that have Inferentia chips might need to install the [Neuron SDK](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/) first\.

This procedure requires `eksctl` version `0.177.0` or later\. You can check your version with the following command:

```
eksctl version
```

For instructions on how to install or upgrade `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.NOTE: This procedure only works for clusters that were created with `eksctl`\.

\+

1. Copy the following contents to your device\. Replace `my-cluster` with the name of your cluster\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can’t be longer than 100 characters\. Replace `ng-ubuntu` with a name for your node group\. The node group name can’t be longer than 63 characters\. It must start with letter or digit, but can also include hyphens and underscores for the remaining characters\. To deploy on Arm instances, replace `m5.large` with an Arm instance type\. Replace `my-ec2-keypair-name` with the name of an Amazon EC2 SSH key pair that you can use to connect using SSH into your nodes with after they launch\. If you don’t already have an Amazon EC2 key pair, you can create one in the AWS Management Console\. For more information, see [https://docs\.aws\.amazon\.com/](https://docs.aws.amazon.com/) AWSEC2/latest/UserGuide/ec2\-key\-pairs\.html\[Amazon EC2 key pairs\] in the Amazon EC2 User Guide for Linux Instances\. Replace all remaining * `example values` with your own values\. Once you’ve made the replacements, run the modified command to create the `ubuntu.yaml` file\.* 
**Important**  
To deploy a node group to AWS Outposts, AWS Wavelength, or AWS Local Zone subnets, don’t pass AWS Outposts, AWS Wavelength, or AWS Local Zone subnets when you create the cluster\. You must specify the subnets in the following example\. For more information see [Create a nodegroup from a config file](https://eksctl.io/usage/nodegroups/#creating-a-nodegroup-from-a-config-file) and [Config file schema](https://eksctl.io/usage/schema/) in the `eksctl` documentation\. Replace `[replaceable]`region\-code```` with the AWS Region that your cluster is in\.

   ```
   //⁂cat ubuntu.yaml EOF
   ---
   apiVersion: eksctl.io/v1alpha5
   kind: ClusterConfig
   
   metadata:
     name: my-cluster
     region: region-code
     version: '1.29'
   
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

    To create an Ubuntu Pro node group, just change the `amiFamily` value to `UbuntuPro2204`\. 

   Ubuntu Pro node group, just change the `amiFamily` value to `UbuntuPro2204`\. 

    node group, just change the `amiFamily` value to `UbuntuPro2204`\. 

   `amiFamily` value to `UbuntuPro2204`\. 

    value to `UbuntuPro2204`\. 

   `UbuntuPro2204`\. 

   \. Deploy your nodes with the following command\.

   ```
   eksctl create nodegroup --config-file=ubuntu.yaml
   ```

   An example output is as follows\.

   Several lines are output while the nodes are created\. One of the last lines of output is the following example line\.

   ```
   [✔]  created 1 nodegroup(s) in cluster "`my-cluster`"
   ```We recommend blocking Pod access to IMDS if the following conditions are true:
   + You plan to assign IAM roles to all of your Kubernetes service accounts so that Pods only have the minimum permissions that they need\.
   + No Pods in the cluster require access to the Amazon EC2 instance metadata service \(IMDS\) for other reasons, such as retrieving the current AWS Region\.

   For more information, see [Restrict access to the instance profile assigned to the worker node](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node)\.