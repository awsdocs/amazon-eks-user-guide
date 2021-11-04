# Getting started with Amazon EKS – AWS Management Console and AWS CLI<a name="getting-started-console"></a>

This guide helps you to create all of the required resources to get started with Amazon Elastic Kubernetes Service \(Amazon EKS\) using the AWS Management Console and the AWS CLI\. In this guide, you manually create each resource\. At the end of this tutorial, you will have a running Amazon EKS cluster that you can deploy applications to\. 

The procedures in this guide give you complete visibility into how each resource is created and how the resources interact with each other\. If you'd rather have most of the resources created for you automatically, use the `eksctl` CLI to create your cluster and nodes\. For more information, see [Getting started with Amazon EKS – `eksctl`](getting-started-eksctl.md)\.

## Prerequisites<a name="eks-prereqs"></a>

Before starting this tutorial, you must install and configure the following tools and resources that you need to create and manage an Amazon EKS cluster\.
+ **AWS CLI** – A command line tool for working with AWS services, including Amazon EKS\. This guide requires that you use version 2\.2\.37 or later or 1\.20\.40 or later\. For more information, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) in the AWS Command Line Interface User Guide\. After installing the AWS CLI, we recommend that you also configure it\. For more information, see [Quick configuration with `aws configure`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the AWS Command Line Interface User Guide\.
+ **`kubectl`** – A command line tool for working with Kubernetes clusters\. This guide requires that you use version 1\.21 or later\. For more information, see [Installing `kubectl`](install-kubectl.md)\.
+ **Required IAM permissions** – The IAM security principal that you're using must have permissions to work with Amazon EKS IAM roles and service linked roles, AWS CloudFormation, and a VPC and related resources\. For more information, see [Actions, resources, and condition keys for Amazon Elastic Container Service for Kubernetes](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html) and [Using service\-linked roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html) in the IAM User Guide\. You must complete all steps in this guide as the same user\.

## Step 1: Create your Amazon EKS cluster<a name="eks-create-cluster"></a>

Create an Amazon EKS cluster\.

**Important**  
To get started as simply and quickly as possible, this topic includes steps to create a cluster and nodes with default settings\. Before creating a cluster and nodes for production use, we recommend that you familiarize yourself with all settings and deploy a cluster and nodes with the settings that meet your requirements\. For more information, see [Creating an Amazon EKS cluster](create-cluster.md) and [Amazon EKS nodes](eks-compute.md)\.

**To create your cluster**

1. Create an Amazon VPC with public and private subnets that meets Amazon EKS requirements\. You can replace *example values* with your own, but we recommend using the example values in this tutorial\.

   ```
   aws cloudformation create-stack \
     --region us-west-2 \
     --stack-name my-eks-vpc-stack \
     --template-url https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-10-29/amazon-eks-vpc-private-subnets.yaml
   ```

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

   Make sure that the Region selected in the top right of your console is **Oregon** If not, select the drop\-down next to the Region name and select **US West \(Oregon\) us\-west\-2**\. Though you can create a cluster in any [Amazon EKS supported Region](https://docs.aws.amazon.com/general/latest/gr/eks.html), in this tutorial, it's created in **US West \(Oregon\) us\-west\-2**\.

1. Select **Create cluster**\. If you don't see this option, in the **Create EKS cluster** box, enter a name for your cluster, such as `my-cluster`, and select **Next step**\.

1. On the **Configure cluster** page enter a name for your cluster, such as *`my-cluster`* and select ***myAmazonEKSClusterRole*** for **Cluster Service Role**\. Leave the remaining settings at their default values and select **Next**\.

1. On the **Specify networking** page, select ***vpc\-00x0000x000x0x000* \| *my\-eks\-vpc\-stack\-VPC*** from the **VPC** drop down list\. Leave the remaining settings at their default values and select **Next**\.

1. On the **Configure logging** page, select **Next**\.

1. On the **Review and create** page, select **Create**\.

   To the right of the cluster's name, the cluster status is **Creating** for several minutes until the cluster provisioning process completes\. Don't continue to the next step until the status is **Active**\.
**Note**  
You might receive an error that one of the Availability Zones in your request doesn't have sufficient capacity to create an Amazon EKS cluster\. If this happens, the error output contains the Availability Zones that can support a new cluster\. Retry creating your cluster with at least two subnets that are located in the supported Availability Zones for your account\. For more information, see [Insufficient capacity](troubleshooting.md#ICE)\.

## Step 2: Configure your computer to communicate with your cluster<a name="eks-configure-kubectl"></a>

In this section, you create a `kubeconfig` file for your cluster\. The settings in this file enable the `kubectl` CLI to communicate with your cluster\.

**To configure your computer to communicate with your cluster**

1. Create or update a `kubeconfig` file for your cluster\. If necessary, replace *`us-west-2`* with the Region that you created your cluster in\.

   ```
   aws eks update-kubeconfig \
     --region us-west-2 \
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

## Step 3: Create an IAM OpenID Connect \(OIDC\) provider<a name="gs-console-oidc"></a>

Create an IAM OpenID Connect \(OIDC\) provider for your cluster so that Kubernetes service accounts used by workloads can access AWS resources\. You only need to complete this step one time for a cluster\.

1. Select the **Configuration** tab\.

1. In the **Details** section, copy the value for **OpenID Connect provider URL**\.

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the navigation panel, choose **Identity Providers**\. 

1. Choose **Add Provider**\.

1. For **Provider Type**, choose **OpenID Connect**\.

1. For **Provider URL**, paste the OIDC provider URL for your cluster from step two, and then choose **Get thumbprint**\.

1. For **Audience**, enter `sts.amazonaws.com` and choose **Add provider**\.

## Step 4: Create nodes<a name="eks-launch-workers"></a>

You can create a cluster with one of the following node types\. To learn more about each type, see [Amazon EKS nodes](eks-compute.md)\. After your cluster is deployed, you can add other node types\.
+ **Fargate – Linux** – Select this type if you want to run Linux applications on AWS Fargate\.
+ **Managed nodes – Linux** – Select this type if you want to run Amazon Linux applications on Amazon EC2 instances\. Though not covered in this guide, you can also add [Windows self\-managed](launch-windows-workers.md) and [Bottlerocket](launch-node-bottlerocket.md) nodes to your cluster\. A cluster must contain at least one Linux node, even if all your workloads are Windows\. 

Select the tab with the name of the node type that you'd like to create\.

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

1. Choose the cluster to create a Fargate profile for and select the **Configuration** tab, then the **Compute** tab\.

1. Under **Fargate profiles**, choose **Add Fargate profile**\.

1. On the **Configure Fargate profile** page, enter the following information and choose **Next**\.

   1. For **Name**, enter a unique name for your Fargate profile, such as *`my-profile`*\.

   1. For **Pod execution role**, choose the ***myAmazonEKSFargatePodExecutionRole*** role that you created in step one\.

   1. Select the **Subnets** dropdown and unselect any subnet with `Public` in its name\. Only private subnets are supported for pods running on Fargate\.

1. On the **Configure pods selection** page, enter the following information and choose **Next**\.

   1. For **Namespace**, enter `default`\.

1. On the **Review and create** page, review the information for your Fargate profile and choose **Create**\.

------
#### [ Managed nodes – Linux ]

Create a managed node group, specifying the subnets and node IAM role that you created in previous steps\.<a name="launch-managed-node-group-console"></a>

**To create your Amazon EC2 Linux managed node group**

1. Create an IAM role for the Amazon VPC CNI plugin and attach the required Amazon EKS IAM managed policy to it\. The Amazon EKS Amazon VPC CNI plugin is installed on a cluster, by default\. The plugin assigns an IP address from your VPC to each pod\.

   1. Copy the following contents to a file named `cni-role-trust-policy.json`\. Replace `111122223333` with your account ID and replace `XXXXXXXXXX45D83924220DC4815XXXXX` with the value after the last `/` of your [**OpenID Connect provider URL**](#gs-console-oidc)\.

      ```
      {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect": "Allow",
            "Principal": {
              "Federated": "arn:aws:iam::111122223333:oidc-provider/oidc.eks.us-west-2.amazonaws.com/id/XXXXXXXXXX45D83924220DC4815XXXXX"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
              "StringEquals": {
                "oidc.eks.<region-code>.amazonaws.com/id/XXXXXXXXXX45D83924220DC4815XXXXX:sub": "system:serviceaccount:kube-system:aws-node"
              }
            }
          }
        ]
      }
      ```

   1. Create an IAM role for the Amazon VPC CNI plugin\.

      ```
      aws iam create-role \
        --role-name myAmazonEKSCNIRole \
        --assume-role-policy-document file://"cni-role-trust-policy.json"
      ```

   1. Attach the required Amazon EKS managed IAM policy to the role\.

      ```
      aws iam attach-role-policy \
        --policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy \
        --role-name myAmazonEKSCNIRole
      ```

1. Associate the Kubernetes service account used by the VPC CNI plugin to the IAM role\. Replace `111122223333` with your account ID\.

   ```
   aws eks update-addon \
     --region us-west-2 \
     --cluster-name my-cluster \
     --addon-name vpc-cni \
     --service-account-role-arn arn:aws:iam::111122223333:role/myAmazonEKSCNIRole
   ```

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

   1. Attach the required Amazon EKS managed IAM policies to the role\.

      ```
      aws iam attach-role-policy \
        --policy-arn arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy \
        --role-name myAmazonEKSNodeRole
      aws iam attach-role-policy \
        --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly \
        --role-name myAmazonEKSNodeRole
      ```

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the name of the cluster that you created in [Step 1: Create your Amazon EKS cluster](#eks-create-cluster), such as ***my\-cluster***\.

1. Select the **Configuration** tab\.

1. On the **Configuration** tab, select the **Compute** tab, and then choose **Add Node Group**\.

1. On the **Configure node group** page, fill out the parameters accordingly, accept the remaining default values, and then choose **Next**\.
   + **Name** – Enter a unique name for your managed node group, such as `my-nodegroup`\.
   + **Node IAM role name** – Choose ***myAmazonEKSNodeRole***\. In this getting started guide, this role must only be used for this node group and no other node groups\.

1. On the **Set compute and scaling configuration** page, accept the default values and select **Next**\.

1. On the **Specify networking** page, select an existing key pair to use for `SSH key pair` and then choose **Next**\. If you don't have a key pair, you can create one with the following command\. If necessary, change `us-west-2` to the Region that you created your cluster in\. Be sure to save the return output in a file on your local computer\. For more information, see [Creating or importing a key pair](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#prepare-key-pair) in the Amazon EC2 User Guide for Linux Instances\. Though the key isn't required in this guide, you can only specify a key to use when you create the node group\. Specifying the key allows you to SSH to the node once it's created\.

   ```
   aws ec2 create-key-pair --region us-west-2 --key-name myKeyPair
   ```

1. On the **Review and create** page, review your managed node group configuration and choose **Create**\.

1. After several minutes, the **Status** in the **Node Group configuration** section will change from **Creating** to **Active**\. Don't continue to the next step until the status is **Active**\.

------

## Step 5: View resources<a name="gs-view-resources"></a>

You can view your nodes and Kubernetes workloads\.

**To view your nodes**

1. In the left pane, select **Clusters**, and then in the list of **Clusters**, select the name of the cluster that you created, such as ***my\-cluster***\.

1. On the **Overview** tab, you see the list of **Nodes** that were deployed for the cluster\. You can select the name of a node to see more information about it\. For more information about what you see here, see [View nodes](view-nodes.md)\.

1. On the **Workloads** tab of the cluster, you see a list of the workloads that are deployed by default to an Amazon EKS cluster\. You can select the name of a workload to see more information about it\. For more information about what you see here, see [View workloads](view-workloads.md)\.

## Step 6: Delete your cluster and nodes<a name="gs-console-clean-up"></a>

After you've finished with the cluster and nodes that you created for this tutorial, you should clean up by deleting the cluster and nodes\. If you want to do more with this cluster before you clean up, see [Next steps](#gs-console-next-steps)\.

**To delete your cluster and nodes**

1. Delete all node groups and Fargate profiles\.

   1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

   1. In the left navigation, select **Clusters**, and then in the list of clusters, select the name of the cluster that you want to delete\.

   1. Select the **Configuration** tab\. On the **Compute** tab, select:
      + The node group that you created in a previous step and select **Delete**\. Enter the name of the node group, and then select **Delete**\.
      + The **Fargate Profile** that you created in a previous step and select **Delete**\. Enter the name of the profile, and then select **Delete**\.

1. Delete the cluster\.

   1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

   1. Select the cluster to delete and choose **Delete**\.

   1. On the delete cluster confirmation screen, choose **Delete**\.

1. Delete the VPC AWS CloudFormation stack that you created in this guide\.

   1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

   1. Select the VPC stack to delete, and choose **Delete**\.

   1. On the **Delete Stack** confirmation screen, choose **Delete stack**\.

1. Delete the IAM roles that you created\.

   1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

   1. In the left navigation pane, select **Roles**\.

   1. Select the ***myAmazonEKSClusterRole*** from the list\. Select **Delete role**, and then select **Yes, Delete**\. Delete the  ***myAmazonEKSFargatePodExecutionRole*** or  ***myAmazonEKSNodeRole*** role that you created and the ***myAmazonEKSCNIRole*** role, if you created one\.

## Next steps<a name="gs-console-next-steps"></a>

Now that you have a working Amazon EKS cluster with nodes, you are ready to start installing Kubernetes add\-ons and deploying applications to your cluster\. The following documentation topics help you to extend the functionality of your cluster\.
+ The IAM entity \(user or role\) that created the cluster is added to the Kubernetes RBAC authorization table as the administrator \(with `system:masters` permissions\)\. Initially, only that IAM user can make calls to the Kubernetes API server using `kubectl`\. If you want other users to have access to your cluster, then you must add them to the `aws-auth` `ConfigMap`\. For more information, see [Managing users or IAM roles for your cluster](add-user-role.md)\.
+ [Restrict access to IMDS](best-practices-security.md#restrict-ec2-credential-access) – If you plan to assign IAM roles to all of your Kubernetes service accounts so that pods only have the minimum permissions that they need, and no pods in the cluster require access to the Amazon EC2 instance metadata service \(IMDS\) for other reasons, such as retrieving the current Region, then we recommend blocking pod access to IMDS\. For more information, see [IAM roles for service accounts](iam-roles-for-service-accounts.md) and [Restricting access to the IMDS and Amazon EC2 instance profile credentials](best-practices-security.md#restrict-ec2-credential-access)\. 
+ Migrate the default Amazon VPC CNI, CoreDNS, and `kube-proxy` add\-ons to Amazon EKS add\-ons\. For more information, see [Adding the Amazon VPC CNI Amazon EKS add\-on](managing-vpc-cni.md#adding-vpc-cni-eks-add-on), [Adding the CoreDNS Amazon EKS add\-on](managing-coredns.md#adding-coredns-eks-add-on), and [Adding the `kube-proxy` Amazon EKS add\-on](managing-kube-proxy.md#adding-kube-proxy-eks-add-on)\.
+ [Cluster Autoscaler](cluster-autoscaler.md) – Configure the Kubernetes Cluster Autoscaler to automatically adjust the number of nodes in your node groups\.
+ [Deploy a sample application](sample-deployment.md) – Deploy a sample Linux application to test your cluster and Linux nodes\.
+ [Cluster management](eks-managing.md) – Learn how to use important tools for managing your cluster\.