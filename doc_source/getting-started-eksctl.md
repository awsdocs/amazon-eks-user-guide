--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Getting started with Amazon EKS – eksctl<a name="getting-started-eksctl"></a>

This guide helps you to create all of the required resources to get started with Amazon Elastic Kubernetes Service \(Amazon EKS\) using `eksctl`, a simple command line utility for creating and managing Kubernetes clusters on Amazon EKS\. At the end of this tutorial, you will have a running Amazon EKS cluster that you can deploy applications to\.

## Prerequisites<a name="eksctl-prereqs"></a>

Before starting this tutorial, you must install and configure the following tools and resources that you need to create and manage an Amazon EKS cluster\.
+  ** `eksctl` ** – A command line tool for working with EKS clusters that automates many individual tasks\. For more information, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.
+  **Required IAM permissions** – The IAM security principal that you’re using must have permissions to work with Amazon EKS IAM roles, service linked roles, AWS CloudFormation, a VPC, and related resources\. For more information, see [Actions, resources, and condition keys for Amazon Elastic Container Service for Kubernetes](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html) and [Using service\-linked roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html) in the IAM User Guide\. You must complete all steps in this guide as the same user\. To check the current user, run the following command:

  ```
  aws sts get-caller-identity
  ```

## Step 1: Create your Amazon EKS cluster and nodes<a name="create-cluster-gs-eksctl"></a>

**Important**  

Create your Amazon EKS cluster with the following command\. You can replace ` my-cluster ` with your own value\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can’t be longer than 100 characters\. Replace ` region-code ` with any AWS Region that is supported by Amazon EKS\. For a list of AWS Regions, see [Amazon EKS endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/eks.html) in the AWS General Reference guide\.

Fargate – Linux   
\*

```
eksctl create cluster --name my-cluster --region region-code --fargate
```

Managed nodes – Linux   
\*

```
eksctl create cluster --name my-cluster --region region-code
```

Cluster creation takes several minutes\. During creation you’ll see several lines of output\. The last line of output is similar to the following example line\.

```
[...]
[✓]  EKS cluster "my-cluster" in "`region-code`" region is ready
```

 `eksctl` created a `kubectl`config file in `~/.kube` or added the new cluster’s configuration within an existing `config` file in `~/.kube` on your computer\.

After cluster creation is complete, view the AWS CloudFormation stack named `eksctl-my-cluster-cluster` in the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/) to see all of the resources that were created\.

## Step 2: View Kubernetes resources<a name="gs-eksctl-view-resources"></a>

1. View your cluster nodes\.

   ```
   kubectl get nodes -o wide
   ```

   An example output is as follows\.  
Fargate – Linux   
\*\*

```
NAME                                                STATUS   ROLES    AGE     VERSION              INTERNAL-IP   EXTERNAL-IP   OS-IMAGE         KERNEL-VERSION                  CONTAINER-RUNTIME
fargate-ip-192-0-2-0.region-code.compute.internal   Ready    <none>   8m3s    v1.2.3-eks-1234567   192.0.2.0     <none>        Amazon Linux 2   1.23.456-789.012.amzn2.x86_64   containerd://1.2.3
fargate-ip-192-0-2-1.region-code.compute.internal   Ready    <none>   7m30s   v1.2.3-eks-1234567   192-0-2-1     <none>        Amazon Linux 2   1.23.456-789.012.amzn2.x86_64   containerd://1.2.3
```

Managed nodes – Linux   
\*\*

```
NAME                                        STATUS   ROLES    AGE    VERSION              INTERNAL-IP   EXTERNAL-IP   OS-IMAGE         KERNEL-VERSION                  CONTAINER-RUNTIME
ip-192-0-2-0.region-code.compute.internal   Ready    <none>   6m7s   v1.2.3-eks-1234567   192.0.2.0     192.0.2.2     Amazon Linux 2   1.23.456-789.012.amzn2.x86_64   containerd://1.2.3
ip-192-0-2-1.region-code.compute.internal   Ready    <none>   6m4s   v1.2.3-eks-1234567   192.0.2.1     192.0.2.3     Amazon Linux 2   1.23.456-789.012.amzn2.x86_64   containerd://1.2.3
```

\+

1. View the workloads running on your cluster\.

   ```
   kubectl get pods -A -o wide
   ```

   An example output is as follows\.  
Fargate – Linux   
\*\*

```
NAMESPACE     NAME                       READY   STATUS    RESTARTS   AGE   IP          NODE                                                NOMINATED NODE   READINESS GATES
kube-system   coredns-1234567890-abcde   1/1     Running   0          18m   192.0.2.0   fargate-ip-192-0-2-0.region-code.compute.internal   <none>           <none>
kube-system   coredns-1234567890-12345   1/1     Running   0          18m   192.0.2.1   fargate-ip-192-0-2-1.region-code.compute.internal   <none>           <none>
```

Managed nodes – Linux   
\*\*

```
NAMESPACE     NAME                       READY   STATUS    RESTARTS   AGE     IP          NODE                                        NOMINATED NODE   READINESS GATES
kube-system   aws-node-12345             1/1     Running   0          7m43s   192.0.2.1   ip-192-0-2-1.region-code.compute.internal   <none>           <none>
kube-system   aws-node-67890             1/1     Running   0          7m46s   192.0.2.0   ip-192-0-2-0.region-code.compute.internal   <none>           <none>
kube-system   coredns-1234567890-abcde   1/1     Running   0          14m     192.0.2.3   ip-192-0-2-3.region-code.compute.internal   <none>           <none>
kube-system   coredns-1234567890-12345   1/1     Running   0          14m     192.0.2.4   ip-192-0-2-4.region-code.compute.internal   <none>           <none>
kube-system   kube-proxy-12345           1/1     Running   0          7m46s   192.0.2.0   ip-192-0-2-0.region-code.compute.internal   <none>           <none>
kube-system   kube-proxy-67890           1/1     Running   0          7m43s   192.0.2.1   ip-192-0-2-1.region-code.compute.internal   <none>           <none>
```

\+

## Step 3: Delete your cluster and nodes<a name="gs-eksctl-clean-up"></a>

```
eksctl delete cluster --name my-cluster --region region-code
```

## Next steps<a name="gs-eksctl-next-steps"></a>

The following documentation topics help you to extend the functionality of your cluster\.
+ Deploy a to your cluster\.
+ The [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) that created the cluster is the only principal that can make calls to the Kubernetes API server with `kubectl` or the AWS Management Console\. If you want other IAM principals to have access to your cluster, then you need to add them\. For more information, see and \.
+ Before deploying a cluster for production use, we recommend familiarizing yourself with all of the settings for and \. Some settings \(such as enabling SSH access to Amazon EC2 nodes\) must be made when the cluster is created\.
+ To increase security for your cluster, \.