# Launching self\-managed Amazon Linux nodes on an Outpost<a name="eks-outposts-self-managed-nodes"></a>

This topic describes how you can launch Auto Scaling groups of Amazon Linux nodes on an Outpost that register with your Amazon EKS cluster\. The cluster can be on the AWS Cloud or on an Outpost\.

**Prerequisites**
+ An existing Outpost\. For more information, see [What is AWS Outposts](https://docs.aws.amazon.com/outposts/latest/userguide/what-is-outposts.html)\.
+ An existing Amazon EKS cluster\. To deploy a cluster on the AWS Cloud, see [Creating an Amazon EKS cluster](create-cluster.md)\. To deploy a cluster on an Outpost, see [Local clusters for Amazon EKS on AWS Outposts](eks-outposts-local-cluster-overview.md)\.
+ Suppose that you're creating your nodes in a cluster on the AWS Cloud and you have subnets in the AWS Region where you have AWS Outposts, AWS Wavelength, or AWS Local Zones enabled\. Then, those subnets must not have been passed in when you created your cluster\. If you're creating your nodes in a cluster on an Outpost, you must have passed in an Outpost subnet when creating your cluster\.
+ \(Recommended for clusters on the AWS Cloud\) The Amazon VPC CNI plugin for Kubernetes add\-on configured with its own IAM role that has the necessary IAM policy attached to it\. For more information, see [Configuring the Amazon VPC CNI plugin for Kubernetes to use IAM roles for service accounts \(IRSA\)](cni-iam-role.md)\. Local clusters do not support IAM roles for service accounts\. 

You can create a self\-managed Amazon Linux node group with `eksctl` or the AWS Management Console \(with an AWS CloudFormation template\)\. You can also use [Terraform](https://registry.terraform.io/modules/terraform-aws-modules/eks/aws/latest)\.

------
#### [ eksctl ]

**Prerequisite**  
Version `0.175.0` or later of the `eksctl` command line tool installed on your device or AWS CloudShell\. To install or update `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.

**To launch self\-managed Linux nodes using `eksctl`**

1. If your cluster is on the AWS Cloud and the **AmazonEKS\_CNI\_Policy** managed IAM policy is attached to your [Amazon EKS node IAM role](create-node-role.md), we recommend assigning it to an IAM role that you associate to the Kubernetes `aws-node` service account instead\. For more information, see [Configuring the Amazon VPC CNI plugin for Kubernetes to use IAM roles for service accounts \(IRSA\)](cni-iam-role.md)\. If your cluster in on your Outpost, the policy must be attached to your node role\.

1. The following command creates a node group in an existing cluster\. The cluster must have been created using `eksctl`\. Replace `al-nodes` with a name for your node group\. The node group name can't be longer than 63 characters\. It must start with letter or digit, but can also include hyphens and underscores for the remaining characters\. Replace `my-cluster` with the name of your cluster\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can't be longer than 100 characters\. If your cluster exists on an Outpost, replace `id` with the ID of an Outpost subnet\. If your cluster exists on the AWS Cloud, replace `id` with the ID of a subnet that you didn't specify when you created your cluster\. Replace `instance-type` with an instance type supported by your Outpost\. Replace the remaining `example values` with your own values\. The nodes are created with the same Kubernetes version as the control plane, by default\. 

   Replace `instance-type` with an instance type available on your Outpost\.

   Replace `my-key` with the name of your Amazon EC2 key pair or public key\. This key is used to SSH into your nodes after they launch\. If you don't already have an Amazon EC2 key pair, you can create one in the AWS Management Console\. For more information, see [Amazon EC2 key pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) in the *Amazon EC2 User Guide for Linux Instances*\.

   Create your node group with the following command\.

   ```
   eksctl create nodegroup --cluster my-cluster --name al-nodes --node-type instance-type \
       --nodes 3 --nodes-min 1 --nodes-max 4 --managed=false --node-volume-type gp2 --subnet-ids subnet-id
   ```

   If your cluster is deployed on the AWS Cloud:
   + The node group that you deploy can assign `IPv4` addresses to Pods from a different CIDR block than that of the instance\. For more information, see [Custom networking for pods](cni-custom-network.md)\.
   + The node group that you deploy doesn't require outbound internet access\. For more information, see [Private cluster requirements](private-clusters.md)\.

   For a complete list of all available options and defaults, see [AWS Outposts Support](https://eksctl.io/usage/outposts/) in the `eksctl` documentation\.

   If nodes fail to join the cluster, then see [Nodes fail to join cluster](troubleshooting.md#worker-node-fail) in [Amazon EKS troubleshooting](troubleshooting.md) and [Can't join nodes to a cluster](eks-outposts-troubleshooting.md#outposts-troubleshooting-unable-to-join-nodes-to-a-cluster) in [Troubleshooting local clusters for Amazon EKS on AWS Outposts](eks-outposts-troubleshooting.md)\.

   An example output is as follows\. Several lines are output while the nodes are created\. One of the last lines of output is the following example line\.

   ```
   [✔]  created 1 nodegroup(s) in cluster "my-cluster"
   ```

1. \(Optional\) Deploy a [sample application](sample-deployment.md) to test your cluster and Linux nodes\.

------
#### [ AWS Management Console ]

**Step 1: To launch self\-managed Amazon Linux nodes using the AWS Management Console**

1. Download the latest version of the AWS CloudFormation template\.

   ```
   curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2022-12-23/amazon-eks-nodegroup.yaml
   ```

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. Choose **Create stack** and then select **With new resources \(standard\)**\.

1. For **Specify template**, select **Upload a template file** and then select **Choose file**\. Select the `amazon-eks-nodegroup.yaml` file that you downloaded in a previous step and then select **Next**\.

1. On the **Specify stack details** page, enter the following parameters accordingly, and then choose **Next**:
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it **`al-nodes`**\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can't be longer than 100 characters\.
   + **ClusterName**: Enter the name of your cluster\. If this name doesn't match your cluster name, your nodes can't join the cluster\.
   + **ClusterControlPlaneSecurityGroup**: Choose the **SecurityGroups** value from the AWS CloudFormation output that you generated when you created your [VPC](creating-a-vpc.md)\.

     The following steps show one operation to retrieve the applicable group\.

     1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

     1. Choose the name of the cluster\.

     1. Choose the **Networking** tab\.

     1. Use the **Additional security groups** value as a reference when selecting from the **ClusterControlPlaneSecurityGroup** dropdown list\.
   + **NodeGroupName**: Enter a name for your node group\. This name can be used later to identify the Auto Scaling node group that's created for your nodes\.
   + **NodeAutoScalingGroupMinSize**: Enter the minimum number of nodes that your node Auto Scaling group can scale in to\.
   + **NodeAutoScalingGroupDesiredCapacity**: Enter the desired number of nodes to scale to when your stack is created\.
   + **NodeAutoScalingGroupMaxSize**: Enter the maximum number of nodes that your node Auto Scaling group can scale out to\.
   + **NodeInstanceType**: Choose an instance type for your nodes\. If your cluster is running on the AWS Cloud, then for more information, see [Choosing an Amazon EC2 instance type](choosing-instance-type.md)\. If your cluster is running on an Outpost, then you can only select an instance type that is available on your Outpost\.
   + **NodeImageIdSSMParam**: Pre\-populated with the Amazon EC2 Systems Manager parameter of a recent Amazon EKS optimized AMI for a variable Kubernetes version\. To use a different Kubernetes minor version supported with Amazon EKS, replace `1.XX` with a different [supported version](kubernetes-versions.md)\. We recommend specifying the same Kubernetes version as your cluster\.

     To use the Amazon EKS optimized accelerated AMI, replace `amazon-linux-2` with **amazon\-linux\-2\-gpu**\. To use the Amazon EKS optimized Arm AMI, replace `amazon-linux-2` with **amazon\-linux\-2\-arm64**\.
**Note**  
The Amazon EKS node AMI is based on Amazon Linux\. You can track security or privacy events for Amazon Linux 2 at the [Amazon Linux Security Center](https://alas.aws.amazon.com/alas2.html) or subscribe to the associated [RSS feed](https://alas.aws.amazon.com/AL2/alas.rss)\. Security and privacy events include an overview of the issue, what packages are affected, and how to update your instances to correct the issue\.
   + **NodeImageId**: \(Optional\) If you're using your own custom AMI \(instead of the Amazon EKS optimized AMI\), enter a node AMI ID for your AWS Region\. If you specify a value here, it overrides any values in the **NodeImageIdSSMParam** field\. 
   + **NodeVolumeSize**: Specify a root volume size for your nodes, in GiB\.
   + **NodeVolumeType**: Specify a root volume type for your nodes\.
   + **KeyName**: Enter the name of an Amazon EC2 SSH key pair that you can use to connect using SSH into your nodes with after they launch\. If you don't already have an Amazon EC2 key pair, you can create one in the AWS Management Console\. For more information, see [Amazon EC2 key pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) in the *Amazon EC2 User Guide for Linux Instances*\.
**Note**  
If you don't provide a key pair here, the AWS CloudFormation stack creation fails\.
   + **BootstrapArguments**: There are several optional arguments that you can pass to your nodes\. For more information, view the [bootstrap script usage information](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) on GitHub\. If you're adding nodes to a cluster that doesn't have an ingress and egress internet connection \(also known as private clusters\), then you must provide the following bootstrap arguments \(as a single line\)\.

     ```
     --b64-cluster-ca ${CLUSTER_CA} --apiserver-endpoint https://${APISERVER_ENDPOINT} --enable-local-outpost true --cluster-id ${CLUSTER_ID}
     ```
   + **DisableIMDSv1**: By default, each node supports the Instance Metadata Service Version 1 \(IMDSv1\) and IMDSv2\. You can disable IMDSv1\. To prevent future nodes and Pods in the node group from using IMDSv1, set **DisableIMDSv1** to **true**\. For more information about IMDS, see [Configuring the instance metadata service](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html)\. For more information about restricting access to it on your nodes, see [Restrict access to the instance profile assigned to the worker node](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node)\.
   + **VpcId**: Enter the ID for the [VPC](creating-a-vpc.md) that you created\. Before choosing a VPC, review [VPC requirements and considerations](eks-outposts-vpc-subnet-requirements.md#outposts-vpc-requirements)\.
   + **Subnets**: If your cluster is on an Outpost, then choose at least one private subnet in your VPC\. Before choosing subnets, review [Subnet requirements and considerations](eks-outposts-vpc-subnet-requirements.md#outposts-subnet-requirements)\. You can see which subnets are private by opening each subnet link from the **Networking** tab of your cluster\.

1. Select your desired choices on the **Configure stack options** page, and then choose **Next**\.

1. Select the check box to the left of **I acknowledge that AWS CloudFormation might create IAM resources\.**, and then choose **Create stack**\.

1. When your stack has finished creating, select it in the console and choose **Outputs**\.

1. Record the **NodeInstanceRole** for the node group that was created\. You need this when you configure your Amazon EKS nodes\.

**Step 2: To enable nodes to join your cluster**

1. Check to see if you already have an `aws-auth` `ConfigMap`\.

   ```
   kubectl describe configmap -n kube-system aws-auth
   ```

1. If you are shown an `aws-auth` `ConfigMap`, then update it as needed\.

   1. Open the `ConfigMap` for editing\.

      ```
      kubectl edit -n kube-system configmap/aws-auth
      ```

   1. Add a new `mapRoles` entry as needed\. Set the `rolearn` value to the **NodeInstanceRole** value that you recorded in the previous procedure\.

      ```
      [...]
      data:
        mapRoles: |
          - rolearn: <ARN of instance role (not instance profile)>
            username: system:node:{{EC2PrivateDNSName}}
            groups:
              - system:bootstrappers
              - system:nodes
      [...]
      ```

   1. Save the file and exit your text editor\.

1. If you received an error stating "`Error from server (NotFound): configmaps "aws-auth" not found`, then apply the stock `ConfigMap`\.

   1. Download the configuration map\.

      ```
      curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/aws-auth-cm.yaml
      ```

   1. In the `aws-auth-cm.yaml` file, set the `rolearn` to the **NodeInstanceRole** value that you recorded in the previous procedure\. You can do this with a text editor, or by replacing `my-node-instance-role` and running the following command:

      ```
      sed -i.bak -e 's|<ARN of instance role (not instance profile)>|my-node-instance-role|' aws-auth-cm.yaml
      ```

   1. Apply the configuration\. This command may take a few minutes to finish\.

      ```
      kubectl apply -f aws-auth-cm.yaml
      ```

1. Watch the status of your nodes and wait for them to reach the `Ready` status\.

   ```
   kubectl get nodes --watch
   ```

   Enter `Ctrl`\+`C` to return to a shell prompt\.
**Note**  
If you receive any authorization or resource type errors, see [Unauthorized or access denied \(`kubectl`\)](troubleshooting.md#unauthorized) in the troubleshooting topic\.

   If nodes fail to join the cluster, then see [Nodes fail to join cluster](troubleshooting.md#worker-node-fail) in [Amazon EKS troubleshooting](troubleshooting.md) and [Can't join nodes to a cluster](eks-outposts-troubleshooting.md#outposts-troubleshooting-unable-to-join-nodes-to-a-cluster) in [Troubleshooting local clusters for Amazon EKS on AWS Outposts](eks-outposts-troubleshooting.md)\.

1. Install the Amazon EBS CSI driver\. For more information, see [Installation](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/docs/install.md) on GitHub\. In the **Set up driver permission** section, make sure to follow the instruction for the **Using IAM instance profile** option\. You must use the `gp2` storage class\. The `gp3` storage class isn't supported\.

   To create a `gp2` storage class on your cluster, complete the following steps\.

   1. Run the following command to create the `gp2-storage-class.yaml` file\.

      ```
      cat >gp2-storage-class.yaml <<EOF
      apiVersion: storage.k8s.io/v1
      kind: StorageClass
      metadata:
        annotations:
          storageclass.kubernetes.io/is-default-class: "true"
        name: ebs-sc
      provisioner: ebs.csi.aws.com
      volumeBindingMode: WaitForFirstConsumer
      parameters:
        type: gp2
        encrypted: "true"
      allowVolumeExpansion: true
      EOF
      ```

   1. Apply the manifest to your cluster\.

      ```
      kubectl apply -f gp2-storage-class.yaml
      ```

1. \(GPU nodes only\) If you chose a GPU instance type and the Amazon EKS optimized accelerated AMI, you must apply the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) as a DaemonSet on your cluster\. Replace `vX.X.X` with your desired [NVIDIA/k8s\-device\-plugin](https://github.com/NVIDIA/k8s-device-plugin/releases) version before running the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/vX.X.X/nvidia-device-plugin.yml
   ```

**Step 3: Additional actions**

1. \(Optional\) Deploy a [sample application](sample-deployment.md) to test your cluster and Linux nodes\.

1. If your cluster is deployed on an Outpost, then skip this step\. If your cluster is deployed on the AWS Cloud, the following information is optional\. If the **AmazonEKS\_CNI\_Policy** managed IAM policy is attached to your [Amazon EKS node IAM role](create-node-role.md), we recommend assigning it to an IAM role that you associate to the Kubernetes `aws-node` service account instead\. For more information, see [Configuring the Amazon VPC CNI plugin for Kubernetes to use IAM roles for service accounts \(IRSA\)](cni-iam-role.md)\.

------