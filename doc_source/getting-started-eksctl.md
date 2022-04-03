# Getting started with Amazon EKS – `eksctl`<a name="getting-started-eksctl"></a>

This guide helps you to create all of the required resources to get started with Amazon Elastic Kubernetes Service \(Amazon EKS\) using `eksctl`, a simple command line utility for creating and managing Kubernetes clusters on Amazon EKS\. At the end of this tutorial, you will have a running Amazon EKS cluster that you can deploy applications to\. 

The procedures in this guide create several resources for you automatically that you have to create manually when you create your cluster using the AWS Management Console\. If you'd rather manually create most of the resources to better understand how they interact with each other, then use the AWS Management Console to create your cluster and compute\. For more information, see [Getting started with Amazon EKS – AWS Management Console and AWS CLI](getting-started-console.md)\.

## Prerequisites<a name="eksctl-prereqs"></a>

Before starting this tutorial, you must install and configure the following tools and resources that you need to create and manage an Amazon EKS cluster\.
+ **`kubectl`** – A command line tool for working with Kubernetes clusters\. This guide requires that you use version 1\.21 or later\. For more information, see [Installing `kubectl`](install-kubectl.md)\.
+ **`eksctl`** – A command line tool for working with EKS clusters that automates many individual tasks\. This guide requires that you use version 0\.89\.0 or later\. For more information, see [Installing `eksctl`](eksctl.md)\.
+ **Required IAM permissions** – The IAM security principal that you're using must have permissions to work with Amazon EKS IAM roles and service linked roles, AWS CloudFormation, and a VPC and related resources\. For more information, see [Actions, resources, and condition keys for Amazon Elastic Container Service for Kubernetes](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html) and [Using service\-linked roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html) in the IAM User Guide\. You must complete all steps in this guide as the same user\.

## (Optional) Step 1: Create an IAM Role to own your EKS Cluster
The IAM security principal that you use to create your EKS Cluster permanently has full access to the Kubernetes API. We recommend creating a dedicated IAM role associated with the cluster, to contain these special permissions. This role may also be used to recover the cluster if other authentication mechanisms fail.

1. Create IAM Role 

This guide uses the `AdministratorAccess` managed policy. Creating a cluster requires wide ranging permissions. For more information, see [Minimum IAM Policies](https://eksctl.io/usage/minimum-iam-policies/).

------
#### [ CloudFormation ]

1. Create a role with sufficient permissions, and define a trust relationship for assuming the role. 

   1. Copy the following contents to a file named `ClusterCreateRoleStack.yaml`.

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Resources:
  ClusterCreateRole:
    Type: 'AWS::IAM::Role'
    Properties:
      RoleName: "ClusterCreate"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              AWS:
                - arn:aws:iam::<your-account-id>:root
            Action:
              - 'sts:AssumeRole'
      Path: /
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AdministratorAccess
```

   1. Create the CloudFormation stack for the role\.

```
aws cloudformation create-stack \
  --stack-name ClusterCreateRoleStack \
  --template-body file://$(pwd)/ClusterCreateRoleStack.yaml \
  --capabilities CAPABILITY_NAMED_IAM
```

------
#### [ Terraform ]

This example uses the [official AWS Terraform provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs).

1. Create a role with sufficient permissions, and define a trust relationship for assuming the role. 

   1. Copy the following contents to a file named `ClusterCreateRoleStack.tf` in an empty directory.

```terraform
resource "aws_iam_role" "ClusterCreate" {
  name = "ClusterCreate"

  path = "/"
  managed_policy_arns = [ "arn:aws:iam::aws:policy/AdministratorAccess" ]


  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          AWS = "arn:aws:iam::185309785115:root"
        }
      },
    ]
  })

}
```

   1. In the new directory, apply the terraform document.

```
terraform apply
```

------
#### [ AWS Console ]

1. Open the Amazon IAM console at [https://console.aws.amazon.com/iamv2/](https://console.aws.amazon.com/iamv2/)\.

1. Choose **Roles** under *Access Management* in the left sidebar, and then choose **Create Role**\. 

1. On the **Select trusted entity** page, do the following:

   1. Select **AWS account** as the *Trusted Entity*.

   1. For the AWS account, choose **This account**)\.

   1. Leave the remaining settings at their default values and choose **Next**\.

1. On the **Add permissions** page, do the following:

   1. Select the **AdministratorAccess** policy.

   1. Leave the remaining settings at their default values and choose **Next**\.

1. On the **Name, review, and create** page, add a name such as "ClusterCreate",  choose **Create Role**\.

------

1. Create profile for role with AWS CLI

Create a AWS CLI profile for the new role. The `source_profile` may be default, or another profile with AWS credentials. 

Open the AWS CLI config file:

```
vi ~/.aws/config
```

Insert the new profile:

```
[profile ClusterCreate]
role_arn = arn:aws:iam::<your-account-id>:role/ClusterCreate
source_profile = <default-profile>
```

1. Configure AWS CLI to use role 

```
export AWS_PROFILE=ClusterCreate
```

Now, `eksctl` will use this dedicated IAM role to create the cluster.


## Step 2: Create your Amazon EKS cluster and nodes<a name="create-cluster-gs-eksctl"></a>

**Important**  
To get started as simply and quickly as possible, this topic includes steps to create a cluster and nodes with default settings\. Before creating a cluster and nodes for production use, we recommend that you familiarize yourself with all settings and deploy a cluster and nodes with the settings that meet your requirements\. For more information, see [Creating an Amazon EKS cluster](create-cluster.md) and [Amazon EKS nodes](eks-compute.md)\. Some settings can only be enabled when creating your cluster and nodes\.

You can create a cluster with one of the following node types\. To learn more about each type, see [Amazon EKS nodes](eks-compute.md)\. After your cluster is deployed, you can add other node types\.
+ **Fargate – Linux** – Select this type of node if you want to run Linux applications on [AWS Fargate](https://docs.aws.amazon.com/AmazonECS/latest/userguide/what-is-fargate.html)\. Fargate is a serverless compute engine that lets you deploy Kubernetes pods without managing Amazon EC2 instances\.
+ **Managed nodes – Linux** – Select this type of node if you want to run Amazon Linux applications on Amazon EC2 instances\. Though not covered in this guide, you can also add [Windows self\-managed](launch-windows-workers.md) and [Bottlerocket](launch-node-bottlerocket.md) nodes to your cluster\.

Create your Amazon EKS cluster with the following command\. You can replace `my-cluster` with your own value\. The cluster name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can't be longer than 128 characters\. Replace *region\-code* with any AWS Region that is supported by Amazon EKS\. For a list of AWS Regions, see [Amazon EKS endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/eks.html) in the AWS General Reference guide\.

------
#### [ Fargate – Linux ]

```
eksctl create cluster --name my-cluster --region region-code --fargate
```

------
#### [ Managed nodes – Linux ]

```
eksctl create cluster --name my-cluster --region region-code
```

------

**Output**

Cluster creation takes several minutes\. During creation you'll see several lines of output\. The last line of output is similar to the following example line\.

```
...
[✓]  EKS cluster "my-cluster" in "region-code" region is ready
```

`eksctl` created a `kubectl` `config` file in `~/.kube` or added the new cluster's configuration within an existing `config` file in `~/.kube` on your computer\.

After cluster creation is complete, view the AWS CloudFormation stack named `eksctl-my-cluster-cluster` in the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/) to see all of the resources that were created\.

## Step 3: View Kubernetes resources<a name="gs-eksctl-view-resources"></a>

1. View your cluster nodes\.

   ```
   kubectl get nodes -o wide
   ```

   Example output:

------
#### [ Fargate – Linux ]

   ```
   NAME                                                    STATUS   ROLES    AGE     VERSION              INTERNAL-IP       EXTERNAL-IP   OS-IMAGE         KERNEL-VERSION                  CONTAINER-RUNTIME
   fargate-ip-192-168-141-147.region-code.compute.internal Ready    <none>   8m3s    v1.21.5-eks-7c9bda   192.168.141.147   <none>        Amazon Linux 2   5.4.156-83.273.amzn2.x86_64   containerd://1.3.2
   fargate-ip-192-168-164-53.region-code.compute.internal  Ready    <none>   7m30s   v1.21.5-eks-7c9bda   192.168.164.53    <none>        Amazon Linux 2   5.4.156-83.273.amzn2.x86_64   containerd://1.3.2
   ```

------
#### [ Managed nodes – Linux ]

   ```
   NAME                                            STATUS   ROLES    AGE    VERSION              INTERNAL-IP      EXTERNAL-IP     OS-IMAGE         KERNEL-VERSION                  CONTAINER-RUNTIME
   ip-192-168-12-49.region-code.compute.internal   Ready    <none>   6m7s   v1.21.5-eks-d1db3c   192.168.12.49    52.35.116.65    Amazon Linux 2   5.4.156-83.273.amzn2.x86_64   docker://20.10.7
   ip-192-168-72-129.region-code.compute.internal  Ready    <none>   6m4s   v1.21.5-eks-d1db3c   192.168.72.129   44.242.140.21   Amazon Linux 2   5.4.156-83.273.amzn2.x86_64   docker://20.10.7
   ```

------

   For more information about what you see in the output, see [View nodes](view-nodes.md)\.

1. View the workloads running on your cluster\.

   ```
   kubectl get pods --all-namespaces -o wide
   ```

   Example output:

------
#### [ Fargate – Linux ]

   ```
   NAMESPACE     NAME                       READY   STATUS    RESTARTS   AGE   IP                NODE                                                      NOMINATED NODE   READINESS GATES
   kube-system   coredns-69dfb8f894-9z95l   1/1     Running   0          18m   192.168.164.53    fargate-ip-192-168-164-53.region-code.compute.internal    <none>           <none>
   kube-system   coredns-69dfb8f894-c8v66   1/1     Running   0          18m   192.168.141.147   fargate-ip-192-168-141-147.region-code.compute.internal   <none>           <none>
   ```

------
#### [ Managed nodes – Linux ]

   ```
   NAMESPACE     NAME                       READY   STATUS    RESTARTS   AGE     IP               NODE                                             NOMINATED NODE   READINESS GATES
   kube-system   aws-node-6ctpm             1/1     Running   0          7m43s   192.168.72.129   ip-192-168-72-129.region-code.compute.internal   <none>           <none>
   kube-system   aws-node-cbntg             1/1     Running   0          7m46s   192.168.12.49    ip-192-168-12-49.region-code.compute.internal    <none>           <none>
   kube-system   coredns-559b5db75d-26t47   1/1     Running   0          14m     192.168.78.81    ip-192-168-72-129.region-code.compute.internal   <none>           <none>
   kube-system   coredns-559b5db75d-9rvnk   1/1     Running   0          14m     192.168.29.248   ip-192-168-12-49.region-code.compute.internal    <none>           <none>
   kube-system   kube-proxy-l8pbd           1/1     Running   0          7m46s   192.168.12.49    ip-192-168-12-49.region-code.compute.internal    <none>           <none>
   kube-system   kube-proxy-zh85h           1/1     Running   0          7m43s   192.168.72.129   ip-192-168-72-129.region-code.compute.internal   <none>           <none>
   ```

------

   For more information about what you see in the output, see [View workloads](view-workloads.md)\.

## Step 4: Delete your cluster and nodes<a name="gs-eksctl-clean-up"></a>

After you've finished with the cluster and nodes that you created for this tutorial, you should clean up by deleting the cluster and nodes with the following command\. If you want to do more with this cluster before you clean up, see [Next steps](#gs-eksctl-next-steps)\.

```
eksctl delete cluster --name my-cluster --region region-code
```

## Next steps<a name="gs-eksctl-next-steps"></a>

The following documentation topics help you to extend the functionality of your cluster\.
+ Deploy a [sample application](sample-deployment.md) to your cluster\.
+ The IAM entity \(user or role\) that created the cluster is the only IAM user that can make calls to the Kubernetes API server using `kubectl`\. If you want other users to have access to your cluster, see [Enabling IAM user and role access to your cluster](add-user-role.md)\.
+ Before deploying a cluster for production use, we recommend familiarizing yourself with all of the settings for [clusters](create-cluster.md) and [nodes](eks-compute.md)\. Some settings \(such as enabling SSH access to Amazon EC2 nodes\) must be made when the cluster is created\.
+ To increase security for your cluster, [configure the Amazon VPC Container Networking Interface plugin to use IAM roles for service accounts](cni-iam-role.md)\.
