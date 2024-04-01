# Launching self\-managed Bottlerocket nodes<a name="launch-node-bottlerocket"></a>

**Note**  
Managed node groups might offer some advantages for your use case\. For more information, see [Managed node groups](managed-node-groups.md)\.

This topic describes how to launch Auto Scaling groups of [Bottlerocket](https://aws.amazon.com/bottlerocket/) nodes that register with your Amazon EKS cluster\. Bottlerocket is a Linux\-based open\-source operating system from AWS that you can use for running containers on virtual machines or bare metal hosts\. After the nodes join the cluster, you can deploy Kubernetes applications to them\. For more information about Bottlerocket, see [Using a Bottlerocket AMI with Amazon EKS](https://github.com/bottlerocket-os/bottlerocket/blob/develop/QUICKSTART-EKS.md) on GitHub and [Custom AMI support](https://eksctl.io/usage/custom-ami-support/) in the `eksctl` documentation\.

For information about in\-place upgrades, see [Bottlerocket Update Operator](https://github.com/bottlerocket-os/bottlerocket-update-operator) on GitHub\.

**Important**  
Amazon EKS nodes are standard Amazon EC2 instances, and you are billed for them based on normal Amazon EC2 instance prices\. For more information, see [Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/)\.
You can launch Bottlerocket nodes in Amazon EKS extended clusters on AWS Outposts, but you can't launch them in local clusters on AWS Outposts\. For more information, see [Amazon EKS on AWS Outposts](eks-outposts.md)\.
You can deploy to Amazon EC2 instances with `x86` or Arm processors\. However, you can't deploy to instances that have Inferentia chips\.
Bottlerocket is compatible with AWS CloudFormation\. However, there is no official CloudFormation template that can be copied to deploy Bottlerocket nodes for Amazon EKS\.
Bottlerocket images don't come with an SSH server or a shell\. You can use out\-of\-band access methods to allow SSH enabling the admin container and to pass some bootstrapping configuration steps with user data\. For more information, see these sections in the [bottlerocket README\.md](https://github.com/bottlerocket-os/bottlerocket) on GitHub:  
[Exploration](https://github.com/bottlerocket-os/bottlerocket#exploration)
[Admin container](https://github.com/bottlerocket-os/bottlerocket#admin-container)
[Kubernetes settings](https://github.com/bottlerocket-os/bottlerocket#kubernetes-settings)

**To launch Bottlerocket nodes using `eksctl`**

This procedure requires `eksctl` version `0.175.0` or later\. You can check your version with the following command:

```
eksctl version
```

For instructions on how to install or upgrade `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.
**Note**  
This procedure only works for clusters that were created with `eksctl`\.

1. Copy the following contents to your device\. Replace `my-cluster` with the name of your cluster\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can't be longer than 100 characters\. Replace `ng-bottlerocket` with a name for your node group\. The node group name can't be longer than 63 characters\. It must start with letter or digit, but can also include hyphens and underscores for the remaining characters\. To deploy on Arm instances, replace `m5.large` with an Arm instance type\. Replace `my-ec2-keypair-name` with the name of an Amazon EC2 SSH key pair that you can use to connect using SSH into your nodes with after they launch\. If you don't already have an Amazon EC2 key pair, you can create one in the AWS Management Console\. For more information, see [Amazon EC2 key pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) in the *Amazon EC2 User Guide for Linux Instances*\. Replace all remaining *`example values`* with your own values\. Once you've made the replacements, run the modified command to create the `bottlerocket.yaml` file\.

   If specifying an Arm Amazon EC2 instance type, then review the considerations in [Amazon EKS optimized Arm Amazon Linux AMIs](eks-optimized-ami.md#arm-ami) before deploying\. For instructions on how to deploy using a custom AMI, see [Building Bottlerocket](https://github.com/bottlerocket-os/bottlerocket/blob/develop/BUILDING.md) on GitHub and [Custom AMI support](https://eksctl.io/usage/custom-ami-support/) in the `eksctl` documentation\. To deploy a managed node group, deploy a custom AMI using a launch template\. For more information, see [Customizing managed nodes with launch templates](launch-templates.md)\.
**Important**  
To deploy a node group to AWS Outposts, AWS Wavelength, or AWS Local Zone subnets, don't pass AWS Outposts, AWS Wavelength, or AWS Local Zone subnets when you create the cluster\. You must specify the subnets in the following example\. For more information see [Create a nodegroup from a config file](https://eksctl.io/usage/nodegroups/#creating-a-nodegroup-from-a-config-file) and [Config file schema](https://eksctl.io/usage/schema/) in the `eksctl` documentation\. Replace `region-code` with the AWS Region that your cluster is in\.

   ```
   cat >bottlerocket.yaml <<EOF
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
     - name: ng-bottlerocket
       instanceType: m5.large
       desiredCapacity: 3
       amiFamily: Bottlerocket
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

1. Deploy your nodes with the following command\.

   ```
   eksctl create nodegroup --config-file=bottlerocket.yaml
   ```

   An example output is as follows\.

   Several lines are output while the nodes are created\. One of the last lines of output is the following example line\.

   ```
   [✔]  created 1 nodegroup(s) in cluster "my-cluster"
   ```

1. \(Optional\) Create a Kubernetes [persistent volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) on a Bottlerocket node using the [Amazon EBS CSI Plugin](https://github.com/kubernetes-sigs/aws-ebs-csi-driver)\. The default Amazon EBS driver relies on file system tools that aren't included with Bottlerocket\. For more information about creating a storage class using the driver, see [Amazon EBS CSI driver](ebs-csi.md)\.

1. \(Optional\) By default, `kube-proxy` sets the `nf_conntrack_max` kernel parameter to a default value that may differ from what Bottlerocket originally sets at boot\. To keep Bottlerocket's [default setting](https://github.com/bottlerocket-os/bottlerocket/blob/develop/packages/release/release-sysctl.conf), edit the `kube-proxy` configuration with the following command\.

   ```
   kubectl edit -n kube-system daemonset kube-proxy
   ```

   Add `--conntrack-max-per-core` and `--conntrack-min` to the `kube-proxy` arguments that are in the following example\. A setting of `0` implies no change\.

   ```
         containers:
         - command:
           - kube-proxy
           - --v=2
           - --config=/var/lib/kube-proxy-config/config
           - --conntrack-max-per-core=0
           - --conntrack-min=0
   ```

1. \(Optional\) Deploy a [sample application](sample-deployment.md) to test your Bottlerocket nodes\.

1. We recommend blocking Pod access to IMDS if the following conditions are true:
   + You plan to assign IAM roles to all of your Kubernetes service accounts so that Pods only have the minimum permissions that they need\.
   + No Pods in the cluster require access to the Amazon EC2 instance metadata service \(IMDS\) for other reasons, such as retrieving the current AWS Region\.

   For more information, see [Restrict access to the instance profile assigned to the worker node](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node)\.