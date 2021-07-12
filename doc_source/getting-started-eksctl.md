# Getting started with Amazon EKS – `eksctl`<a name="getting-started-eksctl"></a>

This guide helps you to create all of the required resources to get started with Amazon Elastic Kubernetes Service \(Amazon EKS\) using `eksctl`, a simple command line utility for creating and managing Kubernetes clusters on Amazon EKS\. At the end of this tutorial, you will have a running Amazon EKS cluster that you can deploy applications to\. 

The procedures in this guide create several resources for you automatically that you have to create manually when you create your cluster using the AWS Management Console\. If you'd rather manually create most of the resources to better understand how they interact with each other, then use the AWS Management Console to create your cluster and compute\. For more information, see [Getting started with Amazon EKS – AWS Management Console and AWS CLI](getting-started-console.md)\.

## Prerequisites<a name="eksctl-prereqs"></a>

Before starting this tutorial, you must install and configure the following tools and resources that you need to create and manage an Amazon EKS cluster\.
+ **`kubectl`** – A command line tool for working with Kubernetes clusters\. This guide requires that you use version 1\.20 or later\. For more information, see [Installing `kubectl`](install-kubectl.md)\.
+ **`eksctl`** – A command line tool for working with EKS clusters that automates many individual tasks\. This guide requires that you use version 0\.56\.0 or later\. For more information, see [The `eksctl` command line utility](eksctl.md)\.
+ **Required IAM permissions** – The IAM security principal that you're using must have permissions to work with Amazon EKS IAM roles and service linked roles, AWS CloudFormation, and a VPC and related resources\. For more information, see [Actions, resources, and condition keys for Amazon Elastic Container Service for Kubernetes](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html) and [Using service\-linked roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html) in the IAM User Guide\. You must complete all steps in this guide as the same user\.

## Step 1: Create your Amazon EKS cluster and nodes<a name="create-cluster-gs-eksctl"></a>

Create your cluster and nodes\.

**Important**  
To get started as simply and quickly as possible, this topic includes steps to create a cluster and nodes with default settings\. Before creating a cluster and nodes for production use, we recommend that you familiarize yourself with all settings and deploy a cluster and nodes with the settings that meet your requirements\. For more information, see [Creating an Amazon EKS cluster](create-cluster.md) and [Amazon EKS nodes](eks-compute.md)\.

You can create a cluster with one of the following node types\. To learn more about each type, see [Amazon EKS nodes](eks-compute.md)\. After your cluster is deployed, you can add other node types\.
+ **Managed nodes – Linux** – Select this type of node if you want to run Amazon Linux applications on Amazon EC2 instances\. Though not covered in this guide, you can also add [Windows self\-managed](launch-windows-workers.md) and [Bottlerocket](launch-node-bottlerocket.md) nodes to your cluster\. A cluster must contain at least one Linux node, even if all your workloads are Windows\. 

Select the tab with the name of the node type that you'd like to create a cluster with\.

------
#### [ Managed nodes – Linux ]

**To create your cluster with Amazon EC2 Linux managed nodes**  
Create your cluster and Linux managed node group\. Replace `my-cluster` with your own value\. 

Replace `<your-key>` \(including *`<>`*\) with the name of an existing key pair\. If you don't have a key pair, you can create one with the following command\. If necessary, change `us-west-2` to the Region that you create your cluster in\. Be sure to save the return output in a file on your local computer\. For more information, see [Creating or importing a key pair](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#prepare-key-pair) in the Amazon EC2 User Guide for Linux Instances\. Though the key isn't required in this guide, you can only specify a key to use when you create the node group\. Specifying the key allows you to SSH to nodes once they're created\. To run the command, you need to have the AWS CLI version 2\.2\.5 or later or 1\.19\.75 or later\. For more information, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) in the AWS Command Line Interface User Guide\.

```
aws ec2 create-key-pair --region us-west-2 --key-name myKeyPair
```

Create your cluster and nodes with the following command\. Replace the *example values* \(including *<>*\) with your own\. Though you can create a cluster in any [Amazon EKS supported Region](https://docs.aws.amazon.com/general/latest/gr/eks.html), in this tutorial, it's created in **US West \(Oregon\) us\-west\-2**\.

```
eksctl create cluster \
--name my-cluster \
--region us-west-2 \
--with-oidc \
--ssh-access \
--ssh-public-key <your-key> \
--managed
```

The previous command creates a cluster with nodes using primarily default Amazon EKS settings\. To see all resources created, view the stack named `eksctl-<my-cluster>-cluster` in the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\. For a list of all settings and options, enter `eksctl create cluster -h`\. For documentation of all settings and options, see [Creating and Managing Clusters](https://eksctl.io/usage/creating-and-managing-clusters/) in the `eksctl` documentation\.

**Output**

You'll see several lines of output as the cluster and nodes are created\. Cluster and node creation takes several minutes\. The last line of output is similar to the following example line\.

```
...
[✓]  EKS cluster "my-cluster" in "us-west-2" region is ready
```

`eksctl` created a `kubectl` `config` file in `~/.kube` or added the new cluster's configuration within an existing `config` file in `~/.kube`\.

------

## Step 2: View resources<a name="gs-eksctl-view-resources"></a>

1. View your cluster nodes\.

   ```
   kubectl get nodes -o wide
   ```

   **Amazon EC2 node output**

   ```
   NAME                                           STATUS   ROLES    AGE    VERSION              INTERNAL-IP      EXTERNAL-IP     OS-IMAGE         KERNEL-VERSION                  CONTAINER-RUNTIME
   ip-192-168-12-49.us-west-2.compute.internal    Ready    <none>   6m7s   v1.18.9-eks-d1db3c   192.168.12.49    52.35.116.65    Amazon Linux 2   4.14.209-160.335.amzn2.x86_64   docker://19.3.6
   ip-192-168-72-129.us-west-2.compute.internal   Ready    <none>   6m4s   v1.18.9-eks-d1db3c   192.168.72.129   44.242.140.21   Amazon Linux 2   4.14.209-160.335.amzn2.x86_64   docker://19.3.6
   ```

   **Fargate node output**

   ```
   NAME                                                    STATUS   ROLES    AGE     VERSION              INTERNAL-IP       EXTERNAL-IP   OS-IMAGE         KERNEL-VERSION                  CONTAINER-RUNTIME
   fargate-ip-192-168-141-147.us-west-2.compute.internal   Ready    <none>   8m3s    v1.18.8-eks-7c9bda   192.168.141.147   <none>        Amazon Linux 2   4.14.209-160.335.amzn2.x86_64   containerd://1.3.2
   fargate-ip-192-168-164-53.us-west-2.compute.internal    Ready    <none>   7m30s   v1.18.8-eks-7c9bda   192.168.164.53    <none>        Amazon Linux 2   4.14.209-160.335.amzn2.x86_64   containerd://1.3.2
   ```

   For more information about what you see here, see [View nodes](view-nodes.md)\.

1. View the workloads running on your cluster\.

   ```
   kubectl get pods --all-namespaces -o wide
   ```

   **Amazon EC2 output**

   ```
   NAMESPACE     NAME                       READY   STATUS    RESTARTS   AGE     IP               NODE                                           NOMINATED NODE   READINESS GATES
   kube-system   aws-node-6ctpm             1/1     Running   0          7m43s   192.168.72.129   ip-192-168-72-129.us-west-2.compute.internal   <none>           <none>
   kube-system   aws-node-cbntg             1/1     Running   0          7m46s   192.168.12.49    ip-192-168-12-49.us-west-2.compute.internal    <none>           <none>
   kube-system   coredns-559b5db75d-26t47   1/1     Running   0          14m     192.168.78.81    ip-192-168-72-129.us-west-2.compute.internal   <none>           <none>
   kube-system   coredns-559b5db75d-9rvnk   1/1     Running   0          14m     192.168.29.248   ip-192-168-12-49.us-west-2.compute.internal    <none>           <none>
   kube-system   kube-proxy-l8pbd           1/1     Running   0          7m46s   192.168.12.49    ip-192-168-12-49.us-west-2.compute.internal    <none>           <none>
   kube-system   kube-proxy-zh85h           1/1     Running   0          7m43s   192.168.72.129   ip-192-168-72-129.us-west-2.compute.internal   <none>           <none>
   ```

   **Fargate output**

   ```
   NAMESPACE     NAME                       READY   STATUS    RESTARTS   AGE   IP                NODE                                                    NOMINATED NODE   READINESS GATES
   kube-system   coredns-69dfb8f894-9z95l   1/1     Running   0          18m   192.168.164.53    fargate-ip-192-168-164-53.us-west-2.compute.internal    <none>           <none>
   kube-system   coredns-69dfb8f894-c8v66   1/1     Running   0          18m   192.168.141.147   fargate-ip-192-168-141-147.us-west-2.compute.internal   <none>           <none>
   ```

   For more information about what you see here, see [View workloads](view-workloads.md)\.

## Step 3: Delete your cluster and nodes<a name="gs-eksctl-clean-up"></a>

After you've finished with the cluster and nodes that you created for this tutorial, you should clean up by deleting the cluster and nodes\. If you want to do more with this cluster before you clean up, see [Next steps](#gs-eksctl-next-steps)\.

Delete your cluster and nodes\.

```
eksctl delete cluster --name my-cluster --region us-west-2
```

## Next steps<a name="gs-eksctl-next-steps"></a>

Now that you have a working Amazon EKS cluster with nodes, you are ready to start installing Kubernetes add\-ons and deploying applications to your cluster\. The following documentation topics help you to extend the functionality of your cluster\.
+ The IAM entity \(user or role\) that created the cluster is added to the Kubernetes RBAC authorization table as the administrator \(with `system:masters` permissions\)\. Initially, only that IAM user can make calls to the Kubernetes API server using `kubectl`\. If you want other users to have access to your cluster, then you must add them to the `aws-auth` `ConfigMap`\. For more information, see [Managing users or IAM roles for your cluster](add-user-role.md)\.
+ [Restrict access to IMDS](best-practices-security.md#restrict-ec2-credential-access) – If you plan to assign IAM roles to all of your Kubernetes service accounts so that pods only have the minimum permissions that they need, and no pods in the cluster require access to the Amazon EC2 instance metadata service \(IMDS\) for other reasons, such as retrieving the current Region, then we recommend blocking pod access to IMDS\. For more information, see [IAM roles for service accounts](iam-roles-for-service-accounts.md) and [Restricting access to the IMDS and Amazon EC2 instance profile credentials](best-practices-security.md#restrict-ec2-credential-access)\. 
+ Migrate the default Amazon VPC CNI, CoreDNS, and `kube-proxy` add\-ons to Amazon EKS add\-ons\.For more information, see [Adding the Amazon VPC CNI Amazon EKS add\-on](managing-vpc-cni.md#adding-vpc-cni-eks-add-on), [Adding the CoreDNS Amazon EKS add\-on](managing-coredns.md#adding-coredns-eks-add-on), and [Adding the `kube-proxy` Amazon EKS add\-on](managing-kube-proxy.md#adding-kube-proxy-eks-add-on)\.
+ [Cluster Autoscaler](cluster-autoscaler.md) – Configure the Kubernetes Cluster Autoscaler to automatically adjust the number of nodes in your node groups\.
+ [Deploy a sample Linux workload](sample-deployment.md) – Deploy a sample Linux application to test your cluster and Linux nodes\.
+ [Cluster management](eks-managing.md) – Learn how to use important tools for managing your cluster\.