--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Creating a managed node group<a name="create-managed-node-group"></a>

This topic describes how you can launch Amazon EKS managed node groups of nodes that register with your Amazon EKS cluster\. After the nodes join the cluster, you can deploy Kubernetes applications to them\.

**Important**  
Amazon EKS nodes are standard Amazon EC2 instances\. You’re billed based on the normal Amazon EC2 prices\. For more information, see [Amazon EC2 Pricing](https://aws.amazon.com/ec2/pricing/)\.
+ An existing Amazon EKS cluster\. To deploy one, see \.
+ An existing IAM role for the nodes to use\. To create one, see \. If this role doesn’t have either of the policies for the VPC CNI, the separate role that follows is required for the VPC CNI pods\.
+ \(Optional, but recommended\) The Amazon VPC CNI plugin for  Kubernetes add\-on configured with its own IAM role that has the necessary IAM policy attached to it\. For more information, see \.
+ Familiarity with the considerations listed in \. Depending on the instance type you choose, there may be additional prerequisites for your cluster and VPC\.

You can create a managed node group with `eksctl` or the AWS Management Console\.

eksctl  
This procedure requires `eksctl` version `0.177.0` or later\. You can check your version with the following command:

```
eksctl version
```

For instructions on how to install or upgrade `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.

1. Create a managed node group with or without using a custom launch template\. Manually specifying a launch template allows for greater customization of a node group\. For example, it can allow deploying a custom AMI or providing arguments to the `boostrap.sh` script in an Amazon EKS optimized AMI\. For a complete list of every available option and default, enter the following command\.

   ```
   eksctl create nodegroup --help
   ```

   In the following command, replace ` my-cluster ` with the name of your cluster and replace ` my-mng ` with the name of your node group\. The node group name can’t be longer than 63 characters\. It must start with letter or digit, but can also include hyphens and underscores for the remaining characters\.
**Important**  
If you don’t use a custom launch template when first creating a managed node group, don’t use one at a later time for the node group\. If you didn’t specify a custom launch template, the system auto\-generates a launch template that we don’t recommend that you modify manually\. Manually modifying this auto\-generated launch template might cause errors\.

   \+  
Without a launch template  

Replace ` ami-family ` with an allowed keyword\. For more information, see [Setting the node AMI Family](https://eksctl.io/usage/custom-ami-support/#setting-the-node-ami-family) in the `eksctl` documentation\. Replace ` my-key ` with the name of your Amazon EC2 key pair or public key\. This key is used to SSH into your nodes after they launch\.

\+ NOTE: For Windows, this command doesn’t enable SSH\. Instead, it associates your Amazon EC2 key pair with the instance and allows you to RDP into the instance\.

\+

\+

If you don’t already have an Amazon EC2 key pair, you can create one in the AWS Management Console\. For Linux information, see [https://docs\.aws\.amazon\.com/](https://docs.aws.amazon.com/) AWSEC2/latest/UserGuide/ec2\-key\-pairs\.html\[Amazon EC2 key pairs and Linux instances\] in the *Amazon EC2 User Guide for Linux Instances*\. For Windows information, see [https://docs\.aws\.amazon\.com/](https://docs.aws.amazon.com/) AWSEC2/latest/WindowsGuide/ec2\-key\-pairs\.html\[Amazon EC2 key pairs and Windows instances\] in the *Amazon EC2 User Guide for Windows Instances*\.

\+

We recommend blocking Pod access to IMDS if the following conditions are true:

\+ ** **\* You plan to assign IAM roles to all of your Kubernetes service accounts so that Pods only have the minimum permissions that they need\. **\* No Pods in the cluster require access to the Amazon EC2 instance metadata service \(IMDS\) for other reasons, such as retrieving the current AWS Region\.** 

\+

For more information, see [Restrict access to the instance profile assigned to the worker node](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node)\.

\+

If you want to block Pod access to IMDS, then add the ` --disable-pod-imds option to the following command.` 

\+

```
eksctl create nodegroup \
  --cluster my-cluster \
  --region region-code \
  --name my-mng \
  --node-ami-family ami-family \
  --node-type m5.large \
  --nodes 3 \
  --nodes-min 2 \
  --nodes-max 4 \
  --ssh-access \
  --ssh-public-key my-key
```

\+

\+

With a launch template  
We recommend blocking Pod access to IMDS if the following conditions are true:  
+ You plan to assign IAM roles to all of your Kubernetes service accounts so that Pods only have the minimum permissions that they need\.
+ No Pods in the cluster require access to the Amazon EC2 instance metadata service \(IMDS\) for other reasons, such as retrieving the current AWS Region\.
For more information, see [Restrict access to the instance profile assigned to the worker node](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node)\.  
\+  
If you want to block Pod access to IMDS, then specify the necessary settings in the launch template\.  
\+  

1. Copy the following contents to your device\. Replace the ` example values ` and then run the modified command to create the `eks-nodegroup.yaml` file\. Several settings that you specify when deploying without a launch template are moved into the launch template\. If you don’t specify a `version`, the template’s default version is used\.

   ```
   //⁂cat >eks-nodegroup.yaml <<EOF
   apiVersion: eksctl.io/v1alpha5
   kind: ClusterConfig
   metadata:
     name: my-cluster
     region: region-code
   managedNodeGroups:
   - name: my-mng
     launchTemplate:
       id: lt-id
       version: "1"
   EOF
   ```

1. Deploy the nodegroup with the following command\.

   ```
   eksctl create nodegroup --config-file eks-nodegroup.yaml
   ```  
 AWS Management Console  

   1. Wait for your cluster status to show as `ACTIVE`\. You can’t create a managed node group for a cluster that isn’t already `ACTIVE`\.

   1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

   1. Choose the name of the cluster that you want to create a managed node group in\.

   1. Select the **Compute** tab\.

   1. Choose **Add node group**\.

   1. On the **Configure node group** page, fill out the parameters accordingly, and then choose **Next**\.
      +  **Name** – Enter a unique name for your managed node group\. The node group name can’t be longer than 63 characters\. It must start with letter or digit, but can also include hyphens and underscores for the remaining characters\.

        IMPORTANT:
        + You can’t use the same role that is used to create any clusters\.

\+

\+
+  ** Kubernetes labels** – \(Optional\) You can choose to apply Kubernetes labels to the nodes in your managed node group\.

  1. On the **Set compute and scaling configuration** page, fill out the parameters accordingly, and then choose **Next**\.

     The console displays a set of commonly used instance types\. If you need to create a managed node group with an instance type that’s not displayed, then use `eksctl`, the AWS CLI, AWS CloudFormation, or an SDK to create the node group\. If you specified a launch template on the previous page, then you can’t select a value because the instance type must be specified in the launch template\. The value from the launch template is displayed\. If you selected **Spot** for **Capacity type**, then we recommend specifying multiple instance types to enhance availability\.
+  **Disk size** – Enter the disk size \(in GiB\) to use for your node’s root volume\.

  If you specified a launch template on the previous page, then you can’t select a value because it must be specified in the launch template\.
+  **Desired size** – Specify the current number of nodes that the managed node group should maintain at launch\.
+  **Minimum size** – Specify the minimum number of nodes that the managed node group can scale in to\.
+  **Maximum size** – Specify the maximum number of nodes that the managed node group can scale out to\.
+  **Node group update configuration** – \(Optional\) You can select the number or percentage of nodes to be updated in parallel\. These nodes will be unavailable during the update\. For **Maximum unavailable**, select one of the following options and specify a **Value**:
  +  **Number** – Select and specify the number of nodes in your node group that can be updated in parallel\.
  +  **Percentage** – Select and specify the percentage of nodes in your node group that can be updated in parallel\. This is useful if you have a large number of nodes in your node group\.

    1. On the **Specify networking** page, fill out the parameters accordingly, and then choose **Next**\.
+  **Subnets** – Choose the subnets to launch your managed nodes into\.
**Important**  
If you are running a stateful application across multiple Availability Zones that is backed by Amazon EBS volumes and using the Kubernetes , you should configure multiple node groups, each scoped to a single Availability Zone\. In addition, you should enable the `--balance-similar-node-groups` feature\.

  IMPORTANT: **\***\* If you use a launch template and specify multiple network interfaces, Amazon EC2 won’t auto\-assign a public `IPv4` address, even if `MapPublicIpOnLaunch` is set to `true`\. For nodes to join the cluster in this scenario, you must either enable the cluster’s private API server endpoint, or launch nodes in a private subnet with outbound internet access provided through an alternative method, such as a NAT Gateway\. For more information, see [https://docs\.aws\.amazon\.com/](https://docs.aws.amazon.com/) AWSEC2/latest/UserGuide/using\-instance\-addressing\.html\[Amazon EC2 instance IP addressing\] in the *Amazon EC2 User Guide for Linux Instances*\.
+  **Configure SSH access to nodes** \(Optional\)\. Enabling SSH allows you to connect to your instances and gather diagnostic information if there are issues\. We highly recommend enabling remote access when you create a node group\. You can’t enable remote access after the node group is created\.
**Note**  
For Windows, this command doesn’t enable SSH\. Instead, it associates your Amazon EC2 key pair with the instance and allows you to RDP into the instance\.
+ For **SSH key pair** \(Optional\), choose an Amazon EC2 SSH key to use\. For Linux information, see [https://docs\.aws\.amazon\.com/](https://docs.aws.amazon.com/) AWSEC2/latest/UserGuide/ec2\-key\-pairs\.html\[Amazon EC2 key pairs and Linux instances\] in the *Amazon EC2 User Guide for Linux Instances*\. For Windows information, see [https://docs\.aws\.amazon\.com/](https://docs.aws.amazon.com/) AWSEC2/latest/WindowsGuide/ec2\-key\-pairs\.html\[Amazon EC2 key pairs and Windows instances\] in the *Amazon EC2 User Guide for Windows Instances*\. If you chose to use a launch template, then you can’t select one\. When an Amazon EC2 SSH key is provided for node groups using Bottlerocket AMIs, the administrative container is also enabled\. For more information, see [Admin container](https://github.com/bottlerocket-os/bottlerocket#admin-container) on GitHub\.
+ For **Allow SSH remote access from**, if you want to limit access to specific instances, then select the security groups that are associated to those instances\. If you don’t select specific security groups, then SSH access is allowed from anywhere on the internet \(`0.0.0.0/0`\)\.

  1. On the **Review and create** page, review your managed node group configuration and choose **Create**\.

     If nodes fail to join the cluster, then see in the Troubleshooting guide\.

  1. Watch the status of your nodes and wait for them to reach the `Ready` status\.

     ```
     kubectl get nodes --watch
     ```

  1. \(GPU nodes only\) If you chose a GPU instance type and the Amazon EKS optimized accelerated AMI, then you must apply the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) as a DaemonSet on your cluster\. Replace ` vX.X.X ` with your desired [NVIDIA/k8s\-device\-plugin](https://github.com/NVIDIA/k8s-device-plugin/releases) version before running the following command\.

     ```
     kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/vX.X.X/nvidia-device-plugin.yml
     ```

Now that you have a working Amazon EKS cluster with nodes, you’re ready to start installing Kubernetes add\-ons and deploying applications to your cluster\. The following documentation topics help you to extend the functionality of your cluster\.
+ The [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) that created the cluster is the only principal that can make calls to the Kubernetes API server with `kubectl` or the AWS Management Console\. If you want other IAM principals to have access to your cluster, then you need to add them\. For more information, see and \.
+ We recommend blocking Pod access to IMDS if the following conditions are true:
  + You plan to assign IAM roles to all of your Kubernetes service accounts so that Pods only have the minimum permissions that they need\.
  + No Pods in the cluster require access to the Amazon EC2 instance metadata service \(IMDS\) for other reasons, such as retrieving the current AWS Region\.

  For more information, see [Restrict access to the instance profile assigned to the worker node](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node)\.
+ – Configure the Kubernetes Cluster Autoscaler to automatically adjust the number of nodes in your node groups\.
+ Deploy a to your cluster\.
+ – Learn how to use important tools for managing your cluster\.