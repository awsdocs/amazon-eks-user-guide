# Amazon EBS CSI driver<a name="add-ons-aws-ebs-csi-driver"></a>

The Amazon EBS CSI driver Amazon EKS add\-on is a Kubernetes Container Storage Interface \(CSI\) plugin that provides Amazon EBS storage for your cluster\.

The Amazon EKS add\-on name is `aws-ebs-csi-driver`\.

## Required IAM permissions<a name="add-ons-aws-ebs-csi-driver-iam-permissions"></a>

This add\-on utilizes the [IAM roles for service accounts](iam-roles-for-service-accounts.md#iam-roles-for-service-accounts.title) capability of Amazon EKS\. The permissions in the [https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEBSCSIDriverPolicy.html](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEBSCSIDriverPolicy.html) AWS managed policy are required\. You can create an IAM role and attach the managed policy to it with the following command\. Replace `my-cluster` with the name of your cluster and `AmazonEKS_EBS_CSI_DriverRole` with the name for your role\. This command requires that you have [https://eksctl.io](https://eksctl.io) installed on your device\. If you need to use a different tool or you need to use a custom [KMS key](https://aws.amazon.com/kms/) for encryption, see [Create an Amazon EBS CSI driver IAM role](csi-iam-role.md)\.

```
eksctl create iamserviceaccount \
    --name ebs-csi-controller-sa \
    --namespace kube-system \
    --cluster my-cluster \
    --role-name AmazonEKS_EBS_CSI_DriverRole \
    --role-only \
    --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy \
    --approve
```

## Additional information<a name="add-ons-aws-ebs-csi-driver-information"></a>

To learn more about the add\-on, see [Use Amazon EBS storage](ebs-csi.md)\.