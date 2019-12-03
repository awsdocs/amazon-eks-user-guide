# Getting Started with AWS Fargate on Amazon EKS<a name="fargate-getting-started"></a>

This topic helps you to get started running pods on AWS Fargate with your Amazon EKS cluster\.

**Note**  
AWS Fargate with Amazon EKS is currently only available in the following Regions:  


| Region Name | Region | 
| --- | --- | 
| US East \(Ohio\) | us\-east\-2 | 
| US East \(N\. Virginia\) | us\-east\-1 | 
| Asia Pacific \(Tokyo\) | ap\-northeast\-1 | 
| EU \(Ireland\) | eu\-west\-1 | 

## \(Optional\) Create a Cluster<a name="fargate-gs-create-cluster"></a>

Pods running on Fargate are supported on Amazon EKS clusters beginning with Kubernetes version 1\.14 and [platform version](platform-versions.md) `eks.5`\. Existing clusters can update to version 1\.14 to take advantage of this feature\. For more information, see [Updating an Amazon EKS Cluster Kubernetes Version](update-cluster.md)\. Existing 1\.14 clusters will be automatically updated to `eks.5` over time to support this feature\.

If you do not already have an Amazon EKS cluster that supports Fargate, you can create one with the following `eksctl` command\.

**Note**  
The command below creates a cluster with a two\-node [managed node group](managed-node-groups.md) for pods that can't run on Fargate \(such as pods with privileged containers\) or pods that you would prefer to run on Amazon EC2 instances\. If you intend to *only* run pods on Fargate in your cluster, you can remove the `--managed` flag and add the `--without-nodegroup` flag, which creates a cluster with no worker nodes\.

```
eksctl create cluster --name my-cluster --version 1.14 --managed
```

## Ensure that Existing Nodes can Communicate with Fargate Pods<a name="fargate-gs-check-compatibility"></a>

If you are working with a new cluster with no worker nodes, or a cluster with only [managed node groups](managed-node-groups.md), you can skip to the next section\.

If you are working with an existing cluster that already has worker nodes associated with it, you need to make sure that pods on these nodes can communicate freely with pods running on Fargate\. Pods running on Fargate are automatically configured to use the cluster security group for the cluster they is associated with\. You must ensure that any existing worker nodes in your cluster can send and receive traffic to and from the cluster security group\. [Managed Node Groups](managed-node-groups.md) are automatically configured to use the cluster security group as well, so you do not need to modify or check them for this compatibility\.

For existing node groups that were created with `eksctl` or the Amazon EKS\-managed AWS CloudFormation templates, you can add the cluster security group to the nodes manually, or you can modify the node group's Auto Scaling group launch template to attach the cluster security group to the instances\. For more information, see [Changing an Instance's Security Groups](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html#SG_Changing_Group_Membership) in the *Amazon VPC User Guide*\.

You can check for a cluster security group for your cluster in the AWS Management Console under the cluster's **Networking** section, or with the following AWS CLI command:

```
aws eks describe-cluster --name  --query cluster.resourcesVpcConfig.clusterSecurityGroupId
```

## Create a Fargate Pod Execution Role<a name="fargate-sg-pod-execution-role"></a>

When your cluster creates pods on AWS Fargate, the pods need to make calls to AWS APIs on your behalf to do things like pull container images from Amazon ECR\. The Amazon EKS pod execution role provides the IAM permissions to do this\.

When you create a Fargate profile, you must specify a pod execution role to use with your pods\. This role is added to the cluster's Kubernetes [Role Based Access Control](https://kubernetes.io/docs/admin/authorization/rbac/) \(RBAC\) for authorization\. This allows the `kubelet` that is running on the Fargate infrastructure to register with your Amazon EKS cluster so that it can appear in your cluster as a node\. For more information, see [Pod Execution Role](pod-execution-role.md)\.

**To create the Amazon EKS pod execution role**

1. Create a file called `trust-relationship.json` and save it with the following text\.

   ```
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "",
         "Effect": "Allow",
         "Principal": {
           "Service": "eks-fargate-pods.amazonaws.com"
         },
         "Action": "sts:AssumeRole"
       }
     ]
   }
   ```

1. Create an IAM role that uses that trust relationship with the following AWS CLI command\.

   ```
   aws iam create-role --role-name AmazonEKSFargatePodExecutionRole --assume-role-policy-document file://trust-relationship.json
   ```

1. Attach the `[AmazonEKSFargatePodExecutionRolePolicy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSFargatePodExecutionRolePolicy%24jsonEditor)` to your new role with the following command\.

   ```
   aws iam attach-role-policy --role-name AmazonEKSFargatePodExecutionRole --policy-arn arn:aws:iam::aws:policy/AmazonEKSFargatePodExecutionRolePolicy
   ```

## Create a Fargate Profile for your Cluster<a name="fargate-gs-create-profile"></a>

Before you can schedule pods running on Fargate in your cluster, you must define a Fargate profile that specifies which pods should use Fargate when they are launched\. For more information, see [AWS Fargate Profile](fargate-profile.md)\.

**To create a Fargate profile for a cluster**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the cluster to create a Fargate profile for\.

1. Under **Fargate profiles**, choose **Add Fargate profile**\.

1. On the **Configure Fargate profile** page, enter the following information and choose **Next**\.

   1. For **Name**, enter a unique name for your Fargate profile\.

   1. For **Pod execution role**, choose the pod execution role to use with your Fargate profile\. Only IAM roles with the `eks-fargate-pods.amazonaws.com` service principal are shown\. If you do not see any roles listed here, you must create one\. For more information, see [Pod Execution Role](pod-execution-role.md)\.

   1. For **Subnets**, choose the subnets to use for your pods\. By default, all subnets in your cluster's VPC are selected\. Only private subnets are supported for pods running on Fargate; you must deselect any public subnets\.

   1. For **Tags**, you can optionally tag your Fargate profile\. These tags do not propagate to other resources associated with the profile, such as its pods\.

1. On the **Configure pods selection** page, enter the following information and choose **Next**\.

   1. For **Namespace**, enter a namespace to match for pods, such as `kube-system` or `default`\.

   1. \(Optional\) Add Kubernetes labels to the selector that pods in the specified namespace must have to match the selector\. For example, you could add the label `infrastructure: fargate` to the selector so that only pods in the specified namespace that also have the `infrastructure: fargate` Kubernetes label match the selector\.

1. On the **Review and create** page, review the information for your Fargate profile and choose **Create**\.

## \(Optional\) Update CoreDNS<a name="fargate-gs-coredns"></a>

By default, CoreDNS is configured to run on Amazon EC2 infrastructure on Amazon EKS clusters\. If you want to *only* run your pods on Fargate in your cluster, you need to modify the CoreDNS deployment to remove the `eks.amazonaws.com/compute-type : ec2` annotation\. You would also need to create a Fargate profile to target the CoreDNS pods\. The following Fargate profile JSON file does this\.

```
{
    "fargateProfileName": "coredns",
    "clusterName": "dev",
    "podExecutionRoleArn": "arn:aws:iam::111122223333:role/AmazonEKSFargatePodExecutionRole",
    "subnets": [
        "subnet-0b64dd020cdff3864",
        "subnet-00b03756df55e2b87",
        "subnet-0418fcb68ed294abf"
    ],
    "selectors": [
        {
            "namespace": "kube-system",
            "labels": {
                "k8s-app": "kube-dns"
            }
        }
    ]
}
```

You could apply this Fargate profile to your cluster with the following AWS CLI command\. First, create a file called `coredns.json` and paste the JSON file from the previous step into it, replacing the *variable text* with your own cluster values\.

```
aws eks create-fargate-profile --cli-input-json file://coredns.json
```

Then, use the following `kubectl` command to remove the `eks.amazonaws.com/compute-type : ec2` annotation from the CoreDNS pods\.

```
kubectl patch deployment coredns -n kube-system --type json \
-p='[{"op": "remove", "path": "/spec/template/metadata/annotations/eks.amazonaws.com~1compute-type"}]'
```

## Next Steps<a name="fargate-gs-next-steps"></a>
+ You can start migrating your existing applications to run on Fargate with the following workflow\.

  1. [Create a Fargate profile](fargate-profile.md#create-fargate-profile) that matches your application's Kubernetes namespace and Kubernetes labels\.

  1. Delete and re\-create any existing pods so that they are scheduled on Fargate\. For example, the following command triggers a rollout of the `coredns` Deployment\. You can modify the namespace and deployment type to update your specific pods\.

     ```
     kubectl rollout restart -n kube-system deployment coredns
     ```
+ Deploy the [ALB Ingress Controller on Amazon EKS](alb-ingress.md) \(version v1\.1\.4 or later\) to allow Ingress objects for your pods running on Fargate\.
+ Deploy the [Vertical Pod Autoscaler](vertical-pod-autoscaler.md) for your pods running on Fargate to optimize the CPU and memory used for your applications\. Be sure to set the pod update policy to either `Auto` or `Recreate` to ensure correct functionality\.