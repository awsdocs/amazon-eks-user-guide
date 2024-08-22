# Amazon VPC CNI plugin for Kubernetes<a name="add-ons-vpc-cni"></a>

The Amazon VPC CNI plugin for Kubernetes Amazon EKS add\-on is a Kubernetes container network interface \(CNI\) plugin that provides native VPC networking for your cluster\. The self\-managed or managed type of this add\-on is installed on each Amazon EC2 node, by default\. For more information, see [Kubernetes container network interface \(CNI\) plugin](https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)\.

The Amazon EKS add\-on name is `vpc-cni`\.

## Required IAM permissions<a name="add-ons-vpc-cni-iam-permissions"></a>

This add\-on uses the [IAM roles for service accounts](iam-roles-for-service-accounts.md#iam-roles-for-service-accounts.title) capability of Amazon EKS\. If your cluster uses the `IPv4` family, the permissions in the [AmazonEKS\_CNI\_Policy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKS_CNI_Policy.html) are required\. If your cluster uses the `IPv6` family, you must [create an IAM policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html) with the permissions in [IPv6 mode](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/docs/iam-policy.md#ipv6-mode)\. You can create an IAM role, attach one of the policies to it, and annotate the Kubernetes service account used by the add\-on with the following command\. 

Replace `my-cluster` with the name of your cluster and `AmazonEKSVPCCNIRole` with the name for your role\. If your cluster uses the `IPv6` family, then replace `AmazonEKS_CNI_Policy` with the name of the policy that you created\. This command requires that you have [https://eksctl.io](https://eksctl.io) installed on your device\. If you need to use a different tool to create the role, attach the policy to it, and annotate the Kubernetes service account, see [Assign IAM roles to Kubernetes service accounts](associate-service-account-role.md)\.

```
eksctl create iamserviceaccount --name aws-node --namespace kube-system --cluster my-cluster --role-name AmazonEKSVPCCNIRole \
    --role-only --attach-policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy --approve
```

## Update information<a name="add-ons-vpc-cni-update-information"></a>

You can only update one minor version at a time\. For example, if your current version is `1.28.x-eksbuild.y` and you want to update to `1.30.x-eksbuild.y`, then you must update your current version to `1.29.x-eksbuild.y` and then update it again to `1.30.x-eksbuild.y`\. For more information about updating the add\-on, see [Updating the Amazon VPC CNI plugin for Kubernetes Amazon EKS add\-on](vpc-add-on-update.md)\.