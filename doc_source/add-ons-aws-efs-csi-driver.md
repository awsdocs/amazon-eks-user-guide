# Amazon EFS CSI driver<a name="add-ons-aws-efs-csi-driver"></a>

The Amazon EFS CSI driver Amazon EKS add\-on is a Kubernetes Container Storage Interface \(CSI\) plugin that provides Amazon EFS storage for your cluster\.

The Amazon EKS add\-on name is `aws-efs-csi-driver`\.

## Required IAM permissions<a name="add-ons-aws-efs-csi-driver-iam-permissions"></a>

**Required IAM permissions** – This add\-on utilizes the [IAM roles for service accounts](iam-roles-for-service-accounts.md#iam-roles-for-service-accounts.title) capability of Amazon EKS\. The permissions in the [https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEFSCSIDriverPolicy.html](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEFSCSIDriverPolicy.html) AWS managed policy are required\. You can create an IAM role and attach the managed policy to it with the following commands\. Replace `my-cluster` with the name of your cluster and `AmazonEKS_EFS_CSI_DriverRole` with the name for your role\. These commands require that you have [https://eksctl.io](https://eksctl.io) installed on your device\. If you need to use a different tool, see [Create an IAM role](efs-csi.md#efs-create-iam-resources)\.

```
export cluster_name=my-cluster
export role_name=AmazonEKS_EFS_CSI_DriverRole
eksctl create iamserviceaccount \
    --name efs-csi-controller-sa \
    --namespace kube-system \
    --cluster $cluster_name \
    --role-name $role_name \
    --role-only \
    --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEFSCSIDriverPolicy \
    --approve
TRUST_POLICY=$(aws iam get-role --role-name $role_name --query 'Role.AssumeRolePolicyDocument' | \
    sed -e 's/efs-csi-controller-sa/efs-csi-*/' -e 's/StringEquals/StringLike/')
aws iam update-assume-role-policy --role-name $role_name --policy-document "$TRUST_POLICY"
```

## Additional information<a name="add-ons-aws-efs-csi-driver-information"></a>

To learn more about the add\-on, see [Use Amazon EFS storage](efs-csi.md)\.