--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Launching self\-managed Windows nodes<a name="launch-windows-workers"></a>

This topic describes how to launch Auto Scaling groups of Windows nodes that register with your Amazon EKS cluster\. After the nodes join the cluster, you can deploy Kubernetes applications to them\.

**Important**  
Amazon EKS nodes are standard Amazon EC2 instances, and you are billed for them based on normal Amazon EC2 instance prices\. For more information, see [Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/)\.

You can launch self\-managed Windows nodes with `eksctl` or the AWS Management Console\.

eksctl  
This procedure requires that you have installed `eksctl`, and that your `eksctl` version is at least `0.177.0`\. You can check your version with the following command\.

```
eksctl version
```

For instructions on how to install or upgrade `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.NOTE: This procedure only works for clusters that were created with `eksctl`\.

\+

1. \(Optional\) If the **AmazonEKS\_CNI\_Policy** managed IAM policy \(if you have an `IPv4` cluster\) or the `[replaceable]`AmazonEKS\_CNI\_IPv6\_Policy` ` (that you if you have an `IPv6 cluster) is attached to your , we recommend assigning it to an IAM role that you associate to the [noloc]`Kubernetes```aws-node` service account instead\. For more information, see \.

   Create your node group with the following command\. Replace `[replaceable]`region\-code` ` with the AWS Region that your cluster is in. Replace `[replaceable] with your cluster name. The name can contain only alphanumeric characters (case-sensitive) and hyphens. It must start with an alphabetic character and can’t be longer than 100 characters. Replace [replaceable] with a name for your node group. The node group name can’t be longer than 63 characters. It must start with letter or digit, but can also include hyphens and underscores for the remaining characters. For [noloc]`Kubernetes` version 1.24 or later, you can replace [replaceable] with 2022 to use [noloc]`Windows` Server 2022. Replace the rest of the [replaceable] with your own values.` 
**Important**  
To deploy a node group to AWS Outposts, AWS Wavelength, or AWS Local Zone subnets, don’t pass the AWS Outposts, Wavelength, or Local Zone subnets when you create the cluster\. Create the node group with a config file, specifying the AWS Outposts, Wavelength, or Local Zone subnets\. For more information, see [Create a nodegroup from a config file](https://eksctl.io/usage/nodegroups/#creating-a-nodegroup-from-a-config-file) and [Config file schema](https://eksctl.io/usage/schema/) in the `eksctl` documentation\.

   ```
   eksctl create nodegroup \
       --region region-code \
       --cluster my-cluster \
       --name ng-windows \
       --node-type t2.large \
       --nodes 3 \
       --nodes-min 1 \
       --nodes-max 4 \
       --managed=false \
       --node-ami-family WindowsServer2019FullContainer
   ```

    NOTE: **\*** To see the available options for `eksctl` commands, enter the following command\. \+ 

   **\*** To see the available options for `eksctl` commands, enter the following command\. \+ 

    To see the available options for `eksctl` commands, enter the following command\. \+ 

   `eksctl` commands, enter the following command\. \+ 

    commands, enter the following command\. \+ 

   ```
   eksctl command -help
   ```

An example output is as follows\. Several lines are output while the nodes are created\. One of the last lines of output is the following example line\.

\+

```
[✔]  created 1 nodegroup(s) in cluster "`my-cluster`"
```

1. We recommend blocking Pod access to IMDS if the following conditions are true:
   + You plan to assign IAM roles to all of your Kubernetes service accounts so that Pods only have the minimum permissions that they need\.
   + No Pods in the cluster require access to the Amazon EC2 instance metadata service \(IMDS\) for other reasons, such as retrieving the current AWS Region\.

   For more information, see [Restrict access to the instance profile assigned to the worker node](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node)\.  
 AWS Management Console  
\*

1. Wait for your cluster status to show as `ACTIVE`\. If you launch your nodes before the cluster is active, the nodes fail to register with the cluster and you need to relaunch them\.

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/) 

1. Choose **Create stack**\.

1. For **Specify template**, select **Amazon S3 URL**\.

1. Copy the following URL and paste it into **Amazon S3 URL**\.

   ```
   https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2023-02-09/amazon-eks-windows-nodegroup.yaml
   ```

1. Select **Next** twice\.

1. On the **Quick create stack** page, enter the following parameters accordingly:
   +  **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it ` `[replaceable].`  **ClusterName**: Enter the name that you used when you created your Amazon EKS cluster\.

     The following steps show one method to retrieve the applicable group\.

     1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

     1. Choose the name of the cluster\.

     1. Choose the **Networking** tab\.

     1. Use the **Additional security groups** value as a reference when selecting from the **ClusterControlPlaneSecurityGroup** dropdown list\. **NodeGroupName**: Enter a name for your node group\. This name can be used later to identify the Auto Scaling node group that’s created for your nodes\. The node group name can’t be longer than 63 characters\. It must start with letter or digit, but can also include hyphens and underscores for the remaining characters\. **NodeAutoScalingGroupMinSize**: Enter the minimum number of nodes that your node Auto Scaling group can scale in to\. **NodeAutoScalingGroupDesiredCapacity**: Enter the desired number of nodes to scale to when your stack is created\. **NodeAutoScalingGroupMaxSize**: Enter the maximum number of nodes that your node Auto Scaling group can scale out to\. **NodeImageIdSSMParam**: Pre\-populated with the Amazon EC2 Systems Manager parameter of the current recommended Amazon EKS optimized Windows Core AMI ID\. To use the full version of Windows, replace ` Core ` with `Full`\. **NodeImageId**: \(Optional\) If you’re using your own custom AMI \(instead of the Amazon EKS optimized AMI\), enter a node AMI ID for your AWS Region\. If you specify a value for this field, it overrides any values in the **NodeImageIdSSMParam** field\. **NodeVolumeSize**: Specify a root volume size for your nodes, in GiB\. **KeyName**: Enter the name of an Amazon EC2 SSH key pair that you can use to connect using SSH into your nodes with after they launch\. If you don’t already have an Amazon EC2 key pair, you can create one in the AWS Management Console\. For more information, see [https://docs\.aws\.amazon\.com/](https://docs.aws.amazon.com/) AWSEC2/latest/WindowsGuide/ec2\-key\-pairs\.html\[Amazon EC2 key pairs\] in the *Amazon EC2 User Guide for Windows Instances*\.

**Note**  
If you don’t provide a key pair here, the AWS CloudFormation stack fails to be created\. **BootstrapArguments**: Specify any optional arguments to pass to the node bootstrap script, such as extra `kubelet` arguments using `-KubeletExtraArgs`\. **DisableIMDSv1**: By default, each node supports the Instance Metadata Service Version 1 \(IMDSv1\) and IMDSv2\. You can disable IMDSv1\. To prevent future nodes and Pods in the node group from using MDSv1, set **DisableIMDSv1** to **true**\. For more information about IMDS, see [https://docs\.aws\.amazon\.com/](https://docs.aws.amazon.com/) AWSEC2/latest/UserGuide/configuring\-instance\-metadata\-service\.html\[Configuring the instance metadata service\]\.

     IMPORTANT:
     + If any of the subnets are public subnets, then they must have the automatic public IP address assignment setting enabled\. If the setting isn’t enabled for the public subnet, then any nodes that you deploy to that public subnet won’t be assigned a public IP address and won’t be able to communicate with the cluster or other AWS services\. If the subnet was deployed before March 26, 2020 using either of the , or by using `eksctl`, then automatic public IP address assignment is disabled for public subnets\. For information about how to enable public IP address assignment for a subnet, see [Modifying the public IPv4 addressing attribute for your subnet](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#subnet-public-ip)\. If the node is deployed to a private subnet, then it’s able to communicate with the cluster and other AWS services through a NAT gateway\.
     + If you select AWS Outposts, Wavelength, or Local Zone subnets, then the subnets must not have been passed in when you created the cluster\.Acknowledge that the stack might create IAM resources, and then choose **Create stack**\.When your stack has finished creating, select it in the console and choose **Outputs**\.Record the **NodeInstanceRole** for the node group that was created\. You need this when you configure your Amazon EKS Windows nodes\.Check to see if you already have an `aws\-auth``ConfigMap`\.

   ```
   kubectl describe configmap -n kube-system aws-auth
   ```If you are shown an `aws\-auth``ConfigMap`, then update it as needed\.

   1. Open the `ConfigMap` for editing\.

      ```
      kubectl edit -n kube-system configmap/aws-auth
      ```

   1. Add new `mapRoles` entries as needed\. Set the `rolearn` values to the **NodeInstanceRole** values that you recorded in the previous procedures\.

      ```
      [...]
      data:
        mapRoles: |
      - rolearn: ARN of linux instance role (not instance profile)
            username: system:node:{{EC2PrivateDNSName}}
            groups:
              - system:bootstrappers
              - system:nodes
          - rolearn: ARN of windows instance role (not instance profile)
            username: system:node:{{EC2PrivateDNSName}}
            groups:
              - system:bootstrappers
              - system:nodes
              - eks:kube-proxy-windows
      [...]
      ```

   1. Save the file and exit your text editor\.If you received an error stating "`Error from server (NotFound): configmaps "aws-auth" not found`, then apply the stock `ConfigMap`\.

   1. Download the configuration map\.

      ```
      curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/aws-auth-cm-windows.yaml
      ```

   1. In the ` aws-auth-cm-windows.yaml ` file, set the `rolearn` values to the applicable **NodeInstanceRole** values that you recorded in the previous procedures\. You can do this with a text editor, or by replacing the ` example values ` and running the following command:

      ```
      sed -i.bak -e 's|ARN of linux instance role (not instance profile)|my-node-linux-instance-role|' \
          -e 's|ARN of windows instance role (not instance profile)|my-node-windows-instance-role|' aws-auth-cm-windows.yaml
      ```

      IMPORTANT: ** **\* Don’t modify any other lines in this file\. **\* Don’t use the same IAM role for both Windows and Linux nodes\.** Apply the configuration\. This command might take a few minutes to finish\.

      ```
      kubectl apply -f aws-auth-cm-windows.yaml
      ```Watch the status of your nodes and wait for them to reach the `Ready` status\.

   ```
   kubectl get nodes --watch
   ```

   Enter `Ctrl`\+`C` to return to a shell prompt\.

**Note**  
If you receive any authorization or resource type errors, see in the troubleshooting topic\.

If nodes fail to join the cluster, then see in the Troubleshooting guide\. \.\. \(Optional\) If the **AmazonEKS\_CNI\_Policy** managed IAM policy \(if you have an `IPv4` cluster\) or the `[replaceable]`AmazonEKS\_CNI\_IPv6\_Policy` ` (that you if you have an `IPv6 cluster) is attached to your , we recommend assigning it to an IAM role that you associate to the [noloc]`Kubernetes```aws-node` service account instead\. For more information, see \. \.\. We recommend blocking Pod access to IMDS if the following conditions are true:

\+ **\* You plan to assign IAM roles to all of your Kubernetes service accounts so that Pods only have the minimum permissions that they need\. **\* No Pods in the cluster require access to the Amazon EC2 instance metadata service \(IMDS\) for other reasons, such as retrieving the current AWS Region\.

\+

For more information, see [Restrict access to the instance profile assigned to the worker node](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node)\.