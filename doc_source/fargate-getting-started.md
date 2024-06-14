--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Getting started with AWS Fargate using Amazon EKS<a name="fargate-getting-started"></a>

**Important**  
 AWS Fargate with Amazon EKS isn’t available in AWS GovCloud \(US\-East\) and AWS GovCloud \(US\-West\)\.

This topic describes how to get started running Pods on AWS Fargate with your Amazon EKS cluster\.

## Ensure that existing nodes can communicate with Fargate Pods<a name="fargate-gs-check-compatibility"></a>

**Prerequisite**  
For existing node groups that were created with `eksctl` or the Amazon EKS managed AWS CloudFormation templates, you can add the cluster security group to the nodes manually\. Or, alternatively, you can modify the Auto Scaling group launch template for the node group to attach the cluster security group to the instances\. For more information, see [Changing an instance’s security groups](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html#SG_Changing_Group_Membership) in the *Amazon VPC User Guide*\.

You can check for a security group for your cluster in the AWS Management Console under the **Networking** section for the cluster\. Or, you can do this using the following AWS CLI command\. When using this command, replace ` my-cluster ` with the name of your cluster\.

```
aws eks describe-cluster --name my-cluster --query cluster.resourcesVpcConfig.clusterSecurityGroupId
```

## Create a Fargate Pod execution role<a name="fargate-sg-pod-execution-role"></a>

**Note**  
If you created your cluster with `eksctl` using the `--fargate` option, your cluster already has a Pod execution role that you can find in the IAM console with the pattern `eksctl-[replaceable]`my\-cluster`-FargatePodExecutionRole-[replaceable]`ABCDEFGHIJKL` `. Similarly, if you use `eksctl to create your Fargate profiles, eksctl creates your [noloc]`Pod`` execution role if one isn’t already created\.

## Create a Fargate profile for your cluster<a name="fargate-gs-create-profile"></a>

**Note**  
If you created your cluster with `eksctl` using the `--fargate` option, then a Fargate profile is already created for your cluster with selectors for all Pods in the `kube-system` and `default` namespaces\. Use the following procedure to create Fargate profiles for any other namespaces you would like to use with Fargate\.

You can create a Fargate profile using `eksctl` or the AWS Management Console\.

eksctl  
+ This procedure requires `eksctl` version `0.177.0` or later\. You can check your version with the following command:

  ```
  eksctl version
  ```

  For instructions on how to install or upgrade `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.

**To create a Fargate profile with `eksctl`**  
Create your Fargate profile with the following `eksctl` command, replacing every ` example value ` with your own values\. You’re required to specify a namespace\. However, the `--labels` option isn’t required\.

  ```
  eksctl create fargateprofile \
      --cluster my-cluster \
      --name my-fargate-profile \
      --namespace my-kubernetes-namespace \
      --labels key=value
  ```

 AWS Management Console  

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the cluster to create a Fargate profile for\.

1. Choose the **Compute** tab\.

1. Under **Fargate profiles**, choose **Add Fargate profile**\.

1. On the **Configure Fargate profile** page, do the following:

   1. For **Name**, enter a name for your Fargate profile\. The name must be unique\.

   1. Modify the selected **Subnets** as needed\.
**Note**  
Only private subnets are supported for Pods that are running on Fargate\.

   1. For **Tags**, you can optionally tag your Fargate profile\. These tags don’t propagate to other resources that are associated with the profile such as Pods\.

   1. Choose **Next**\.

1. On the **Configure Pod selection** page, do the following:

   1. For **Namespace**, enter a namespace to match for Pods\.
      + You can use specific namespaces to match, such as ` kube-system or `default. ` 
      + \(Optional\) Add Kubernetes labels to the selector\. Specifically add them to the one that the Pods in the specified namespace need to match\.
        + You can add the label ` infrastructure: fargate to the selector so that only Pods in the specified namespace that also have the infrastructure: fargate Kubernetes label match the selector.` Choose **Next**\.

1. On the **Review and create** page, review the information for your Fargate profile and choose **Create**\.

## Update CoreDNS<a name="fargate-gs-coredns"></a>

By default, CoreDNS is configured to run on Amazon EC2 infrastructure on Amazon EKS clusters\. If you want to *only* run your Pods on Fargate in your cluster, complete the following steps\.

**Note**  

\+ IMPORTANT: The role ARN can’t include a [path](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-friendly-names) other than `/`\. For example, if the name of your role is `development/apps/my-role`, you need to change it to `my-role` when specifying the ARN for the role\. The format of the role ARN must be `arn:aws:iam::[replaceable]`111122223333`:role/[replaceable]`role\-name````\.

\+

```
aws eks create-fargate-profile \
    --fargate-profile-name coredns \
    --cluster-name my-cluster \
    --pod-execution-role-arn arn:aws:iam::111122223333:role/AmazonEKSFargatePodExecutionRole \
    --selectors namespace=kube-system,labels={k8s-app=kube-dns} \
    --subnets subnet-0000000000000001 subnet-0000000000000002 subnet-0000000000000003
```

1. Run the following command to remove the `eks.amazonaws.com/compute-type : ec2` annotation from the CoreDNS Pods\.

   ```
   kubectl patch deployment coredns \
       -n kube-system \
       --type json \
       -p='[{"op": "remove", "path": "/spec/template/metadata/annotations/eks.amazonaws.com~1compute-type"}]'
   ```

## Next steps<a name="fargate-gs-next-steps"></a>
+ You can start migrating your existing applications to run on Fargate with the following workflow\.

  1. Delete and re\-create any existing Pods so that they’re scheduled on Fargate\. For example, the following command triggers a rollout of the `coredns` deployment\. You can modify the namespace and deployment type to update your specific Pods\.

     ```
     kubectl rollout restart -n kube-system deployment coredns
     ```
+ You can set up the [AWS Distro for OpenTelemetry](https://aws.amazon.com/otel) \(ADOT\) collector for application monitoring by following [these instructions](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Container-Insights-EKS-otel.html)\.