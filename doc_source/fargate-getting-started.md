# Getting started with AWS Fargate using Amazon EKS<a name="fargate-getting-started"></a>

This topic describes how to get started running pods on AWS Fargate with your Amazon EKS cluster\.

If you restrict access to the public endpoint of your cluster using CIDR blocks, we recommend that you also enable private endpoint access\. This way, Fargate pods can communicate with the cluster\. Without the private endpoint enabled, the CIDR blocks that you specify for public access must include the outbound sources from your VPC\. For more information, see [Amazon EKS cluster endpoint access control](cluster-endpoint.md)\. 

**Prerequisite**  
An existing cluster\. AWS Fargate with Amazon EKS is available in all Amazon EKS Regions except AWS GovCloud \(US\-East\) and AWS GovCloud \(US\-West\)\. If you don't already have an Amazon EKS cluster, see [Getting started with Amazon EKS](getting-started.md)\.

## Ensure that existing nodes can communicate with Fargate pods<a name="fargate-gs-check-compatibility"></a>

If you're working with a new cluster with no nodes, or a cluster with only [managed node groups](managed-node-groups.md), you can skip to [Create a Fargate pod execution role](#fargate-sg-pod-execution-role)\.

Assume that you're working with an existing cluster that already has nodes that are associated with it\. Make sure that pods on these nodes can communicate freely with the pods that are running on Fargate\. Pods that are running on Fargate are automatically configured to use the cluster security group for the cluster that they're associated with\. Ensure that any existing nodes in your cluster can send and receive traffic to and from the cluster security group\. [Managed node groups](managed-node-groups.md) are automatically configured to use the cluster security group as well, so you don't need to modify or check them for this compatibility\.

For existing node groups that were created with `eksctl` or the Amazon EKS managed AWS CloudFormation templates, you can add the cluster security group to the nodes manually\. Or, alternatively, you can modify the Auto Scaling group launch template for the node group to attach the cluster security group to the instances\. For more information, see [Changing an instance's security groups](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html#SG_Changing_Group_Membership) in the *Amazon VPC User Guide*\.

You can check for a security group for your cluster in the AWS Management Console under the **Networking** section for the cluster\. Or, you can do this using the following AWS CLI command\. When using this command, replace `my-cluster` with the name of your cluster\.

```
aws eks describe-cluster --name my-cluster --query cluster.resourcesVpcConfig.clusterSecurityGroupId
```

## Create a Fargate pod execution role<a name="fargate-sg-pod-execution-role"></a>

When your cluster creates pods on AWS Fargate, the components that run on the Fargate infrastructure must make calls to AWS APIs on your behalf\. The Amazon EKS pod execution role provides the IAM permissions to do this\. To create an AWS Fargate pod execution role, see [Amazon EKS pod execution IAM role](pod-execution-role.md)\.

**Note**  
If you created your cluster with `eksctl` using the `--fargate` option, your cluster already has a pod execution role that you can find in the IAM console with the pattern `eksctl-my-cluster-FargatePodExecutionRole-ABCDEFGHIJKL`\. Similarly, if you use `eksctl` to create your Fargate profiles, `eksctl` creates your pod execution role if one isn't already created\.

## Create a Fargate profile for your cluster<a name="fargate-gs-create-profile"></a>

Before you can schedule pods that are running on Fargate in your cluster, you must define a Fargate profile that specifies which pods use Fargate when they're launched\. For more information, see [AWS Fargate profile](fargate-profile.md)\.

**Note**  
If you created your cluster with `eksctl` using the `--fargate` option, then a Fargate profile is already created for your cluster with selectors for all pods in the `kube-system` and `default` namespaces\. Use the following procedure to create Fargate profiles for any other namespaces you would like to use with Fargate\.

You can create a Fargate profile using `eksctl` or the AWS Management Console\.

------
#### [ eksctl ]

This procedure requires `eksctl` version `0.132.0` or later\. You can check your version with the following command:

```
eksctl version
```

For instructions on how to install or upgrade `eksctl`, see [Installing or updating `eksctl`](eksctl.md)\.

**To create a Fargate profile with `eksctl`**  
Create your Fargate profile with the following `eksctl` command, replacing every `example value` with your own values\. You're required to specify a namespace\. However, the `--labels` option isn't required\.

```
eksctl create fargateprofile \
    --cluster my-cluster \
    --name my-fargate-profile \
    --namespace my-kubernetes-namespace \
    --labels key=value
```

You can use certain wildcards for `my-kubernetes-namespace` and `key=value` labels\. For more information, see [Fargate profile wildcards](fargate-profile.md#fargate-profile-wildcards)\.

------
#### [ AWS Management Console ]

**To create a Fargate profile for a cluster with the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the cluster to create a Fargate profile for\.

1. Choose the **Compute** tab\.

1. Under **Fargate profiles**, choose **Add Fargate profile**\.

1. On the **Configure Fargate profile** page, do the following:

   1. For **Name**, enter a name for your Fargate profile\. The name must be unique\.

   1. For **Pod execution role**, choose the pod execution role to use with your Fargate profile\. Only the IAM roles with the `eks-fargate-pods.amazonaws.com` service principal are shown\. If you don't see any roles listed, you must create one\. For more information, see [Amazon EKS pod execution IAM role](pod-execution-role.md)\.

   1. Choose the **Subnets** dropdown and deselect any subnet with `Public` in its name\. Only private subnets are supported for pods that are running on Fargate\.

   1. For **Tags**, you can optionally tag your Fargate profile\. These tags don't propagate to other resources that are associated with the profile such as pods\.

   1. Choose **Next**\.

1. On the **Configure pod selection** page, do the following:

   1. For **Namespace**, enter a namespace to match for pods\.
      + You can use specific namespaces to match, such as `kube-system` or `default`\.
      + You can use certain wildcards \(for example, `prod-*`\) to match multiple namespaces \(for example, `prod-deployment` and `prod-test`\)\. For more information, see [Fargate profile wildcards](fargate-profile.md#fargate-profile-wildcards)\.

   1. \(Optional\) Add Kubernetes labels to the selector\. Specifically add them to the one that the pods in the specified namespace need to match\.
      + You can add the label `infrastructure: fargate` to the selector so that only pods in the specified namespace that also have the `infrastructure: fargate` Kubernetes label match the selector\.
      + You can use certain wildcards \(for example, `key?: value?`\) to match multiple namespaces \(for example, `keya: valuea` and `keyb: valueb`\)\. For more information, see [Fargate profile wildcards](fargate-profile.md#fargate-profile-wildcards)\.

   1. Choose **Next**\.

1. On the **Review and create** page, review the information for your Fargate profile and choose **Create**\.

------

## Update CoreDNS<a name="fargate-gs-coredns"></a>

By default, CoreDNS is configured to run on Amazon EC2 infrastructure on Amazon EKS clusters\. If you want to *only* run your pods on Fargate in your cluster, complete the following steps\.

**Note**  
If you created your cluster with `eksctl` using the `--fargate` option, then you can skip to [Next steps](#fargate-gs-next-steps)\.

1. Create a Fargate profile for CoreDNS with the following command\. Replace `my-cluster` with your cluster name, `111122223333` with your account ID, `AmazonEKSFargatePodExecutionRole` with the name of your pod execution role, and `0000000000000001`, `0000000000000002`, and `0000000000000003` with the IDs of your private subnets\. If you don't have a pod execution role, you must [create one](#fargate-sg-pod-execution-role) first\. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-West\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:`\.
**Important**  
The role ARN can't include a path\. The format of the role ARN must be `arn:aws:iam::111122223333:role/role-name`\. For more information, see [aws\-auth `ConfigMap` does not grant access to the cluster](security_iam_troubleshoot.md#security-iam-troubleshoot-ConfigMap)\.

   ```
   aws eks create-fargate-profile \
       --fargate-profile-name coredns \
       --cluster-name my-cluster \
       --pod-execution-role-arn arn:aws:iam::111122223333:role/AmazonEKSFargatePodExecutionRole \
       --selectors namespace=kube-system,labels={k8s-app=kube-dns} \
       --subnets subnet-0000000000000001 subnet-0000000000000002 subnet-0000000000000003
   ```

1. Run the following command to remove the `eks.amazonaws.com/compute-type : ec2` annotation from the CoreDNS pods\.

   ```
   kubectl patch deployment coredns \
       -n kube-system \
       --type json \
       -p='[{"op": "remove", "path": "/spec/template/metadata/annotations/eks.amazonaws.com~1compute-type"}]'
   ```

## Next steps<a name="fargate-gs-next-steps"></a>
+ You can start migrating your existing applications to run on Fargate with the following workflow\.

  1. [Create a Fargate profile](fargate-profile.md#create-fargate-profile) that matches your application's Kubernetes namespace and Kubernetes labels\.

  1. Delete and re\-create any existing pods so that they're scheduled on Fargate\. For example, the following command triggers a rollout of the `coredns` deployment\. You can modify the namespace and deployment type to update your specific pods\.

     ```
     kubectl rollout restart -n kube-system deployment coredns
     ```
+ Deploy the [Application load balancing on Amazon EKS](alb-ingress.md) to allow Ingress objects for your pods running on Fargate\.
+ You can use the [Vertical Pod Autoscaler](vertical-pod-autoscaler.md) to set the initial correct size of CPU and memory for your Fargate pods, and then use the [Horizontal Pod Autoscaler](horizontal-pod-autoscaler.md) to scale those pods\. If you want the Vertical Pod Autoscaler to automatically re\-deploy pods to Fargate with higher CPU and memory combinations, set the Vertical Pod Autoscaler's mode to either `Auto` or `Recreate`\. This is to ensure correct functionality\. For more information, see the [Vertical Pod Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler#quick-start) documentation on GitHub\.
+ You can set up the [AWS Distro for OpenTelemetry](http://aws.amazon.com/otel) \(ADOT\) collector for application monitoring by following [these instructions](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Container-Insights-EKS-otel.html)\.