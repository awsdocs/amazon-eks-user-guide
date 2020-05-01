# Arm support<a name="arm-support"></a>

This topic describes how to create an Amazon EKS cluster and add worker nodes running on Amazon EC2 A1 instances to Amazon EKS clusters\. Amazon EC2 A1 instances deliver significant cost savings for scale\-out and Arm\-based applications such as web servers, containerized microservices, caching fleets, and distributed data stores\.

**Note**  
These instructions and the assets that they reference are offered as a beta feature that is administered by AWS\. Use of these instructions and assets is governed as a beta under the [AWS service terms](https://aws.amazon.com/service-terms/)\. While in beta, Amazon EKS does not support using Amazon EC2 A1 instances for production Kubernetes workloads\. Submit comments or questions in a [GitHub issue](https://github.com/aws/containers-roadmap/issues/264)\.

## Considerations<a name="arm-considerations"></a>
+ Worker nodes can be any [A1 instance](https://aws.amazon.com/ec2/instance-types/a1/) type, but all worker nodes must be an A1 instance type\.
+ Worker nodes must be deployed with Kubernetes version 1\.13 or 1\.14\.
+ To use A1 instance worker nodes, you must setup a new Amazon EKS cluster\. You cannot add worker nodes to a cluster that has existing worker nodes\.

## Prerequisites<a name="arm-prerequisites"></a>
+ Have `eksctl` installed on your computer\. If you don't have it installed, see [Install `eksctl`](getting-started-eksctl.md#install-eksctl) for installation instructions\.
+ Have `kubectl` and the AWS IAM authenticator installed on your computer\. If you don't have them installed, see [Installing `kubectl`](install-kubectl.md) for installation instructions\.

## Create a cluster<a name="create-cluster-no-workers"></a>

1. Run the following command to create an Amazon EKS cluster with no worker nodes\. If you want to create a cluster running Kubernetes version 1\.13, then replace *`1.14`* with `1.13` in your command\. You can replace *`region-code`* with any [Region that Amazon EKS is available in](https://docs.aws.amazon.com/general/latest/gr/eks.html)\.

   ```
   eksctl create cluster \
   --name a1-preview \
   --version 1.14 \
   --region region-code \
   --without-nodegroup
   ```

   Launching an Amazon EKS cluster using `eksctl` creates an AWS CloudFormation stack\. The launch process for this stack typically takes 10 to 15 minutes\. You can monitor the progress in the Amazon EKS console\.

1. When the cluster creation completes, open the [AWS CloudFormation console](https://us-west-2.console.aws.amazon.com/cloudformation/home)\. You will see a stack named `eksctl-a1-preview-cluster`\. Select this stack\. Select the **Resources** tab\. Record the values of the IDs for the `ControlPlaneSecurityGroup` and `VPC` resources\.

1. Confirm that the cluster is running with the `kubectl get svc` command\. The command returns output similar to the following example output\.

   ```
   NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
   kubernetes   ClusterIP   10.100.0.1       <none>        443/TCP   20m
   ```

## Enable Arm support<a name="enable-arm-support"></a>

To support having only A1 nodes in an Amazon EKS cluster, you need to update some of the Kubernetes components\. Complete the following steps to update CoreDNS and `kube-proxy`, and install the Amazon VPC ARM64 CNI Plugin for Kubernetes\.

1. Update the CoreDNS image ID using the command that corresponds to the version of the cluster that you installed in a previous step\.

   **Kubernetes 1\.14**

   ```
   kubectl apply -f https://raw.githubusercontent.com/aws/containers-roadmap/master/preview-programs/eks-arm-preview/dns-arm-1.14.yaml
   ```

   **Kubernetes 1\.13**

   ```
   kubectl apply -f https://raw.githubusercontent.com/aws/containers-roadmap/master/preview-programs/eks-arm-preview/dns-arm-1.13.yaml
   ```

1. Update the `kube-proxy` image ID using the command that corresponds to the version of the cluster that you installed in a previous step\.

   **Kubernetes 1\.14**

   ```
   kubectl apply -f https://raw.githubusercontent.com/aws/containers-roadmap/master/preview-programs/eks-arm-preview/kube-proxy-arm-1.14.yaml
   ```

   **Kubernetes 1\.13**

   ```
   kubectl apply -f https://raw.githubusercontent.com/aws/containers-roadmap/master/preview-programs/eks-arm-preview/kube-proxy-arm-1.13.yaml
   ```

1. Deploy the Amazon VPC ARM64 CNI Plugin for Kubernetes\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/aws/containers-roadmap/master/preview-programs/eks-arm-preview/aws-k8s-cni-arm64.yaml
   ```

## Launch worker nodes<a name="launch-arm-worker-nodes"></a>

1. Open the [AWS CloudFormation console](https://console.aws.amazon.com/cloudformation)\. Ensure that you are in the AWS Region that you created your Amazon EKS cluster in\.

1. Choose **Create stack**, and then choose **With new resources \(standard\)\.**

1. For **Specify template**, select **Amazon S3 URL**, enter the following URL into the **Amazon S3 URL** box, and then choose **Next** twice\.

   ```
   https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-04-21/amazon-eks-arm-nodegroup.yaml
   ```

1. On the **Specify stack details** page, fill out the following parameters accordingly:
   + **Stack name** – Choose a stack name for your AWS CloudFormation stack\. For example, you can name it ***a1\-preview*\-worker\-nodes**\.
   + **KubernetesVersion** – Select the version of Kubernetes that you chose when launching your Amazon EKS cluster\.
   + **ClusterName** – Enter the name that you used when you created your Amazon EKS cluster\.
**Important**  
This name must exactly match the name you used in [Step 1: Create your Amazon EKS cluster](getting-started-console.md#eks-create-cluster); otherwise, your worker nodes cannot join the cluster\.
   + **ClusterControlPlaneSecurityGroup** – Choose the `ControlPlaneSecurityGroup` ID value from the AWS CloudFormation output that you generated with [Create a cluster](#create-cluster-no-workers)\.
   + **NodeGroupName** – Enter a name for your node group\. This name can be used later to identify the Auto Scaling node group that is created for your worker nodes\.
   + **NodeAutoScalingGroupMinSize** – Enter the minimum number of nodes that your worker node Auto Scaling group can scale in to\.
   + **NodeAutoScalingGroupDesiredCapacity** – Enter the desired number of nodes to scale to when your stack is created\.
   + **NodeAutoScalingGroupMaxSize** – Enter the maximum number of nodes that your worker node Auto Scaling group can scale out to\.
   + **NodeInstanceType** – Choose one of the A1 instance types for your worker nodes, such as `a1.large`\.
   + **NodeVolumeSize** – Specify a root volume size for your worker nodes, in GiB\.
   + **KeyName** – Enter the name of an Amazon EC2 SSH key pair that you can use to connect using SSH into your worker nodes with after they launch\. If you don't already have an Amazon EC2 key pair, you can create one in the AWS Management Console\. For more information, see [Amazon EC2 key pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) in the *Amazon EC2 User Guide for Linux Instances*\.
**Note**  
If you do not provide a key pair here, the AWS CloudFormation stack creation fails\.
   + **BootstrapArguments** – Arguments to pass to the bootstrap script\. For details, see [https://github\.com/awslabs/amazon\-eks\-ami/blob/master/files/bootstrap\.sh](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh)\.
   + **VpcId** – Enter the ID for the VPC that you created in [Create a cluster](#create-cluster-no-workers)\.
   + **Subnets** – Choose the subnets that you created in [Create a cluster](#create-cluster-no-workers)\.
**Important**  
If any of the subnets are public subnets, then they must have the automatic public IP address assignment setting enabled\. If the setting is not enabled for the public subnet, then any worker nodes that you deploy to that public subnet will not be assigned a public IP address and will not be able to communicate with the cluster or other AWS services\. If the subnet was deployed before 03/26/2020 using either of the [Amazon EKS AWS CloudFormation VPC templates](create-public-private-vpc.md), or by using `eksctl`, then automatic public IP address assignment is disabled for public subnets\. For information about how to enable public IP address assignment for a subnet, see [ Modifying the Public IPv4 Addressing Attribute for Your Subnet](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#subnet-public-ip)\. If the worker node is deployed to a private subnet, then it is able to communicate with the cluster and other AWS services through a NAT gateway\.
   + **NodeImageAMI113** – The Amazon EC2 Systems Manager parameter for the 1\.13 AMI image ID\. This value is ignored if you selected `1.14` for `KubernetesVersion`\.
   + **NodeImageAMI114** – The Amazon EC2 Systems Manager parameter for the 1\.14 AMI image ID\. This value is ignored if you selected `1.13` for `KubernetesVersion`\.

1. Choose **Next** and then choose **Next** again\.

1. Acknowledge that the stack might create IAM resources, and then choose **Create stack**\.

1. When your stack has finished creating, select it in the console and choose **Outputs**\.

1. Record the **NodeInstanceRole** for the node group that was created\. You need this when you configure your Amazon EKS worker nodes\.

## Join worker nodes to a cluster<a name="join-arm-cluster"></a>

1. Download, edit, and apply the AWS IAM Authenticator configuration map\.

   1. Use the following command to download the configuration map:

      ```
      wget https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2019-11-15/aws-auth-cm.yaml
      ```

   1. Open the file with your favorite text editor\. Replace the *<ARN of instance role \(not instance profile\)>* snippet with the **NodeInstanceRole** value that you recorded in the previous procedure, and save the file\.
**Important**  
Do not modify any other lines in this file\.

      ```
      apiVersion: v1
      kind: ConfigMap
      metadata:
        name: aws-auth
        namespace: kube-system
      data:
        mapRoles: |
          - rolearn: <ARN of instance role (not instance profile)>
            username: system:node:{{EC2PrivateDNSName}}
            groups:
              - system:bootstrappers
              - system:nodes
      ```

   1. Apply the configuration\. This command may take a few minutes to finish\.

      ```
      kubectl apply -f aws-auth-cm.yaml
      ```
**Note**  
If you receive the error `"aws-iam-authenticator": executable file not found in $PATH`, your kubectl isn't configured for Amazon EKS\. For more information, see [Installing `aws-iam-authenticator`](install-aws-iam-authenticator.md)\.  
If you receive any other authorization or resource type errors, see [Unauthorized or access denied \(`kubectl`\)](troubleshooting.md#unauthorized) in the troubleshooting section\.

1. Watch the status of your nodes and wait for them to reach the `Ready` status\.

   ```
   kubectl get nodes --watch
   ```

## \(Optional\) Deploy an application<a name="launch-arm-application"></a>

To confirm that you can deploy and run an application on the worker nodes, complete the following steps\.

1. Deploy the CNI metrics helper with the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/aws/containers-roadmap/master/preview-programs/eks-arm-preview/cni-metrics-helper-arm64.yaml
   ```

   The output returned is similar to the following example output\.

   ```
   clusterrole.rbac.authorization.k8s.io/cni-metrics-helper created
   serviceaccount/cni-metrics-helper created
   clusterrolebinding.rbac.authorization.k8s.io/cni-metrics-helper created
   deployment.extensions/cni-metrics-helper created
   ```

1. Confirm that the CNI metrics helper is running with the following command\.

   ```
   kubectl -n kube-system get pods -o wide
   ```

   The pod is running if you see the `cni-metrics-helper` pod returned in the output\.