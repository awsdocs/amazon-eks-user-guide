# Getting started with Amazon EKS – AWS Management Console and AWS CLI<a name="getting-started-console"></a>

This guide helps you to create all of the required resources to get started with Amazon Elastic Kubernetes Service \(Amazon EKS\) using the AWS Management Console and the AWS CLI\. In this guide, you manually create each resource\. At the end of this tutorial, you will have a running Amazon EKS cluster that you can deploy applications to\. 

The procedures in this guide give you complete visibility into how each resource is created and how the resources interact with each other\. If you'd rather have most of the resources created for you automatically, use the `eksctl` CLI to create your cluster and nodes\. For more information, see [Getting started with Amazon EKS – `eksctl`](getting-started-eksctl.md)\.

## Prerequisites<a name="eks-prereqs"></a>

Before starting this tutorial, you must install and configure the following tools and resources that you need to create and manage an Amazon EKS cluster\.
+ **AWS CLI** – A command line tool for working with AWS services, including Amazon EKS\. This guide requires that you use version 2\.4\.9 or later or 1\.22\.30 or later\. For more information, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) in the AWS Command Line Interface User Guide\. After installing the AWS CLI, we recommend that you also configure it\. For more information, see [Quick configuration with `aws configure`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the AWS Command Line Interface User Guide\.
+ **`kubectl`** – A command line tool for working with Kubernetes clusters\. This guide requires that you use version 1\.21 or later\. For more information, see [Installing `kubectl`](install-kubectl.md)\.
+ **Required IAM permissions** – The IAM security principal that you're using must have permissions to work with Amazon EKS IAM roles and service linked roles, AWS CloudFormation, and a VPC and related resources\. For more information, see [Actions, resources, and condition keys for Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html) and [Using service\-linked roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html) in the IAM User Guide\. You must complete all steps in this guide as the same user\.

## Step 1: Create your Amazon EKS cluster<a name="eks-create-cluster"></a>

**Important**  
To get started as simply and quickly as possible, this topic includes steps to create a cluster with default settings\. Before creating a cluster for production use, we recommend that you familiarize yourself with all settings and deploy a cluster with the settings that meet your requirements\. For more information, see [Creating an Amazon EKS cluster](create-cluster.md)\. Some settings can only be enabled when creating your cluster\.

**To create your cluster**

1. Create an Amazon VPC with public and private subnets that meets Amazon EKS requirements\. Replace *region\-code* with any AWS Region that is supported by Amazon EKS\. For a list of AWS Regions, see [Amazon EKS endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/eks.html) in the AWS General Reference guide\. You can replace *my\-eks\-vpc\-stack* with any name you choose\.

   ```
   aws cloudformation create-stack \
     --region region-code \
     --stack-name my-eks-vpc-stack \
     --template-url https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-10-29/amazon-eks-vpc-private-subnets.yaml
   ```
**Tip**  
For a list of all the resources the previous command creates, open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\. Choose the *my\-eks\-vpc\-stack* stack and then choose the **Resources** tab\.

1. Create a cluster IAM role and attach the required Amazon EKS IAM managed policy to it\. Kubernetes clusters managed by Amazon EKS make calls to other AWS services on your behalf to manage the resources that you use with the service\.

   1. Copy the following contents to a file named `cluster-role-trust-policy.json`\.

      ```
      {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect": "Allow",
            "Principal": {
              "Service": "eks.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
          }
        ]
      }
      ```

   1. Create the role\.

      ```
      aws iam create-role \
        --role-name myAmazonEKSClusterRole \
        --assume-role-policy-document file://"cluster-role-trust-policy.json"
      ```

   1. Attach the required Amazon EKS managed IAM policy to the role\.

      ```
      aws iam attach-role-policy \
        --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy \
        --role-name myAmazonEKSClusterRole
      ```

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

   Make sure that the AWS Region shown in the top right of your console is the AWS Region that you want to create your cluster in\. If it's not, choose the dropdown next to the AWS Region name and choose the AWS Region that you want to use\.

1. Choose **Add cluster** and then choose **Create**\. If you don't see this option, then choose **Clusters** in the left panel first\.

1. On the **Configure cluster** page, do the following:

   1. Enter a **Name** for your cluster, such as **my\-cluster**\.

   1. For **Cluster Service Role**, choose *myAmazonEKSClusterRole*\.

   1. Leave the remaining settings at their default values and choose **Next**\.

1. On the **Specify networking** page, do the following:

   1. Choose the ID of the VPC that you created in a previous step from the **VPC** dropdown list\. It is something like *vpc\-00x0000x000x0x000* \| *my\-eks\-vpc\-stack\-VPC*\.

   1. Leave the remaining settings at their default values and choose **Next**\.

1. On the **Configure logging** page, choose **Next**\.

1. On the **Review and create** page, choose **Create**\.

   To the right of the cluster's name, the cluster status is **Creating** for several minutes until the cluster provisioning process completes\. Don't continue to the next step until the status is **Active**\.
**Note**  
You might receive an error that one of the Availability Zones in your request doesn't have sufficient capacity to create an Amazon EKS cluster\. If this happens, the error output contains the Availability Zones that can support a new cluster\. Retry creating your cluster with at least two subnets that are located in the supported Availability Zones for your account\. For more information, see [Insufficient capacity](troubleshooting.md#ICE)\.

## Step 2: Configure your computer to communicate with your cluster<a name="eks-configure-kubectl"></a>

In this section, you create a `kubeconfig` file for your cluster\. The settings in this file enable the `kubectl` CLI to communicate with your cluster\.

**To configure your computer to communicate with your cluster**

1. Create or update a `kubeconfig` file for your cluster\. Replace *region\-code* with the AWS Region that you created your cluster in and *my\-cluster* with the name of your cluster\.

   ```
   aws eks update-kubeconfig \
     --region region-code \
     --name my-cluster
   ```

   By default, the `config` file is created in `~/.kube` or the new cluster's configuration is added to an existing `config` file in `~/.kube`\.

1. Test your configuration\.

   ```
   kubectl get svc
   ```
**Note**  
If you receive any authorization or resource type errors, see [Unauthorized or access denied \(`kubectl`\)](troubleshooting.md#unauthorized) in the troubleshooting section\.

   **Output**

   ```
   NAME             TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
   svc/kubernetes   ClusterIP   10.100.0.1   <none>        443/TCP   1m
   ```

## Step 3: Create nodes<a name="eks-launch-workers"></a>

**Important**  
To get started as simply and quickly as possible, this topic includes steps to create nodes with default settings\. Before creating nodes for production use, we recommend that you familiarize yourself with all settings and deploy nodes with the settings that meet your requirements\. For more information, see [Amazon EKS nodes](eks-compute.md)\. Some settings can only be enabled when creating your nodes\.

You can create a cluster with one of the following node types\. To learn more about each type, see [Amazon EKS nodes](eks-compute.md)\. After your cluster is deployed, you can add other node types\.
+ **Fargate – Linux** – Choose this type of node if you want to run Linux applications on [AWS Fargate](https://docs.aws.amazon.com/AmazonECS/latest/userguide/what-is-fargate.html)\. Fargate is a serverless compute engine that lets you deploy Kubernetes pods without managing Amazon EC2 instances\.
+ **Managed nodes – Linux** – Choose this type of node if you want to run Amazon Linux applications on Amazon EC2 instances\. Though not covered in this guide, you can also add [Windows self\-managed](launch-windows-workers.md) and [Bottlerocket](launch-node-bottlerocket.md) nodes to your cluster\.

------
#### [ Fargate – Linux ]

Create a Fargate profile\. When Kubernetes pods are deployed with criteria that matches the criteria defined in the profile, the pods are deployed to Fargate\.

**To create a Fargate profile**

1. Create an IAM role and attach the required Amazon EKS IAM managed policy to it\. When your cluster creates pods on Fargate infrastructure, the components running on the Fargate infrastructure need to make calls to AWS APIs on your behalf to do things like pull container images from Amazon ECR or route logs to other AWS services\. The Amazon EKS pod execution role provides the IAM permissions to do this\. 

   1. Copy the following contents to a file named `pod-execution-role-trust-policy.json`\.

      ```
      {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect": "Allow",
            "Principal": {
              "Service": "eks-fargate-pods.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
          }
        ]
      }
      ```

   1. Create a pod execution IAM role\.

      ```
      aws iam create-role \
        --role-name myAmazonEKSFargatePodExecutionRole \
        --assume-role-policy-document file://"pod-execution-role-trust-policy.json"
      ```

   1. Attach the required Amazon EKS managed IAM policy to the role\.

      ```
      aws iam attach-role-policy \
        --policy-arn arn:aws:iam::aws:policy/AmazonEKSFargatePodExecutionRolePolicy \
        --role-name myAmazonEKSFargatePodExecutionRole
      ```

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. On the **Clusters** page, choose the *my\-cluster* cluster\.

1. On the ***my\-cluster*** page, do the following:

   1. Choose the **Configuration** tab\.

   1. Choose the **Compute** tab\.

   1. Under **Fargate Profiles**, choose **Add Fargate Profile**\.

1. On the **Configure Fargate Profile** page, do the following:

   1. For **Name**, enter a unique name for your Fargate profile, such as ***my\-profile***\.

   1. For **Pod execution role**, choose the *myAmazonEKSFargatePodExecutionRole* role that you created in a previous step\.

   1. Choose the **Subnets** dropdown and deselect any subnet with `Public` in its name\. Only private subnets are supported for pods that are running on Fargate\.

   1. Choose **Next**\.

1. On the **Configure pod selection** page, do the following:

   1. For **Namespace**, enter **default**\.

   1. Choose **Next**\.

1. On the **Review and create** page, review the information for your Fargate profile and choose **Create**\.

1. After a few minutes, the **Status** in the **Fargate Profile configuration** section will change from **Creating** to **Active**\. Don't continue to the next step until the status is **Active**\.

1. If you plan to deploy all pods to Fargate \(none to Amazon EC2 nodes\), do the following to create another Fargate profile and run the default name resolver \(CoreDNS\) on Fargate\.
**Note**  
If you don't do this, you won't have any nodes at this time\.

   1. On the **Fargate Profile** page, choose *my\-cluster*\.

   1. Under **Fargate profiles**, choose **Add Fargate Profile**\.

   1. For **Name**, enter ***CoreDNS***\.

   1. For **Pod execution role**, choose the *myAmazonEKSFargatePodExecutionRole* role that you created in a previous step\.

   1. Choose the **Subnets** dropdown and deselect any subnet with `Public` in its name\. Only private subnets are supported for pods running on Fargate\.

   1. Choose **Next**\.

   1. For **Namespace**, enter **kube\-system**\.

   1. Choose **Match labels**, and then choose **Add label**\.

   1. Enter **k8s\-app** for **Key** and **kube\-dns** for value\. This is necessary for the default name resolver \(CoreDNS\) to deploy to Fargate\.

   1. Choose **Next**\.

   1. On the **Review and create** page, review the information for your Fargate profile and choose **Create**\.

   1. Run the following command to remove the default `eks.amazonaws.com/compute-type : ec2` annotation from the CoreDNS pods\. 

      ```
      kubectl patch deployment coredns \
          -n kube-system \
          --type json \
          -p='[{"op": "remove", "path": "/spec/template/metadata/annotations/eks.amazonaws.com~1compute-type"}]'
      ```
**Note**  
The system creates and deploys two nodes based on the Fargate profile label you added\. You won't see anything listed in **Node Groups** because they aren't applicable for Fargate nodes, but you will see the new nodes listed in the **Overview** tab\.

------
#### [ Managed nodes – Linux ]

Create a managed node group, specifying the subnets and node IAM role that you created in previous steps\.<a name="launch-managed-node-group-console"></a>

**To create your Amazon EC2 Linux managed node group**

1. Create a node IAM role and attach the required Amazon EKS IAM managed policy to it\. The Amazon EKS node `kubelet` daemon makes calls to AWS APIs on your behalf\. Nodes receive permissions for these API calls through an IAM instance profile and associated policies\.

   1. Copy the following contents to a file named `node-role-trust-policy.json`\.

      ```
      {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect": "Allow",
            "Principal": {
              "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
          }
        ]
      }
      ```

   1. Create the node IAM role\.

      ```
      aws iam create-role \
        --role-name myAmazonEKSNodeRole \
        --assume-role-policy-document file://"node-role-trust-policy.json"
      ```

   1. Attach the required managed IAM policies to the role\.

      ```
      aws iam attach-role-policy \
        --policy-arn arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy \
        --role-name myAmazonEKSNodeRole
      aws iam attach-role-policy \
        --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly \
        --role-name myAmazonEKSNodeRole
      aws iam attach-role-policy \
        --policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy \
        --role-name myAmazonEKSNodeRole
      ```

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the name of the cluster that you created in [Step 1: Create your Amazon EKS cluster](#eks-create-cluster), such as *my\-cluster*\.

1. On the ***my\-cluster*** page, do the following:

   1. Choose the **Configuration** tab\.

   1. Choose the **Compute** tab\.

   1. Choose **Add Node Group**\.

1. On the **Configure Node Group** page, do the following:

   1. For **Name**, enter a unique name for your managed node group, such as ***my\-nodegroup***\.

   1. For **Node IAM role name**, choose *myAmazonEKSNodeRole* role that you created in a previous step\. We recommend that each node group use its own unique IAM role\.

   1. Choose **Next**\.

1. On the **Set compute and scaling configuration** page, accept the default values and choose **Next**\.

1. On the **Specify networking** page, accept the default values and choose **Next**\. 

1. On the **Review and create** page, review your managed node group configuration and choose **Create**\.

1. After several minutes, the **Status** in the **Node Group configuration** section will change from **Creating** to **Active**\. Don't continue to the next step until the status is **Active**\.

------

## Step 4: View resources<a name="gs-view-resources"></a>

You can view your nodes and Kubernetes workloads\.

**To view your nodes and workloads**

1. In the left panel, choose **Clusters**, and then in the list of **Clusters**, choose the name of the cluster that you created, such as *my\-cluster*\.

1. On the ***my\-cluster*** page, do the following:

   1. On the **Overview** tab, you see the list of **Nodes** that were deployed for the cluster\. You can choose the name of a node to see more information about it\. For more information about what you see here, see [View nodes](view-nodes.md)\.

   1. On the **Workloads** tab of the cluster, you see a list of the workloads that are deployed by default to an Amazon EKS cluster\. You can choose the name of a workload to see more information about it\. For more information about what you see here, see [View workloads](view-workloads.md)\. If you created Fargate nodes, only **coredns** has a status\.

## Step 5: Delete resources<a name="gs-console-clean-up"></a>

After you've finished with the cluster and nodes that you created for this tutorial, you should delete the resources that you created\. If you want to do more with this cluster before you delete the resources, see [Next steps](#gs-console-next-steps)\.

**To delete the resources that you created in this guide**

1. Delete any node groups or Fargate profiles that you created\.

   1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

   1. In the left navigation, choose **Clusters**\. In the list of clusters, choose *my\-cluster*\.

   1. Choose the **Configuration** tab, and then choose the **Compute** tab\.

   1. If you created a node group, choose the *my\-nodegroup* node group and then choose **Delete**\. Enter ***my\-nodegroup***, and then choose **Delete**\.

   1. For each Fargate profile that you created, choose it and then choose **Delete**\. Enter the name of the profile, and then choose **Delete**\.
**Note**  
When deleting a second Fargate profile, you may need to wait for the first one to finish deleting\.

   1. Don't continue until the node group or Fargate profiles are deleted\.

1. Delete the cluster\.

   1. In the left navigation, choose **Clusters**\. In the list of clusters, choose *my\-cluster*\.

   1. Choose **Delete cluster**\.

   1. Enter ***my\-cluster*** and then choose **Delete**\. Don't continue until the cluster is deleted\.

1. Delete the VPC AWS CloudFormation stack that you created\.

   1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

   1. Choose the *my\-eks\-vpc\-stack* stack, and then choose **Delete**\.

   1. In the **Delete *my\-eks\-vpc\-stack*** confirmation dialog box, choose **Delete stack**\.

1. Delete the IAM roles that you created\.

   1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

   1. In the left navigation panel, choose **Roles**\.

   1. Select each role you created from the list \(*myAmazonEKSClusterRole*, as well as *myAmazonEKSFargatePodExecutionRole* or *myAmazonEKSNodeRole*\)\. Choose **Delete**, enter the requested confirmation text, then choose **Delete**\.

## Next steps<a name="gs-console-next-steps"></a>

The following documentation topics help you to extend the functionality of your cluster\.
+ The IAM entity \(user or role\) that created the cluster is the only IAM user that can make calls to the Kubernetes API server using `kubectl`\. If you want other users to have access to your cluster, see [Enabling IAM user and role access to your cluster](add-user-role.md)\.
+ Deploy a [sample application](sample-deployment.md) to your cluster\.
+ Before deploying a cluster for production use, we recommend familiarizing yourself with all of the settings for [clusters](create-cluster.md) and [nodes](eks-compute.md)\. Some settings \(such as enabling SSH access to Amazon EC2 nodes\) must be made when the cluster is created\.
+ To increase security for your cluster, [configure the Amazon VPC Container Networking Interface plugin to use IAM roles for service accounts](cni-iam-role.md)\.