# Mountpoint for Amazon S3 CSI Driver<a name="mountpoint-for-s3-add-on"></a>

The Mountpoint for Amazon S3 CSI Driver Amazon EKS add\-on is a Kubernetes Container Storage Interface \(CSI\) plugin that provides Amazon S3 storage for your cluster\.

The Amazon EKS add\-on name is `aws-mountpoint-s3-csi-driver`\.

## Required IAM permissions<a name="add-ons-mountpoint-for-s3-add-on-iam-permissions"></a>

This add\-on uses the [IAM roles for service accounts](iam-roles-for-service-accounts.md#iam-roles-for-service-accounts.title) capability of Amazon EKS\. The IAM role that is created will require a policy that gives access to S3\. Follow the [Mountpoint IAM permissions recommendations](https://github.com/awslabs/mountpoint-s3/blob/main/doc/CONFIGURATION.md#iam-permissions) when creating the policy\. Alternatively, you may use the AWS managed policy [https://console.aws.amazon.com/iam/home?#/policies/arn:aws:iam::aws:policy/AmazonS3FullAccess$jsonEditor](https://console.aws.amazon.com/iam/home?#/policies/arn:aws:iam::aws:policy/AmazonS3FullAccess$jsonEditor), but this managed policy grants more permissions than are needed for Mountpoint\. 

You can create an IAM role and attach your policy to it with the following commands\. Replace *my\-cluster* with the name of your cluster, **region\-code** with the correct AWS Region code, *AmazonEKS\_S3\_CSI\_DriverRole* with the name for your role, and *AmazonEKS\_S3\_CSI\_DriverRole\_ARN* with the role ARN\. These commands require that you have [https://eksctl.io](https://eksctl.io) installed on your device\. For instructions on using the IAM console or AWS CLI, see [Create an IAM role](s3-csi.md#s3-create-iam-role)\.

```
CLUSTER_NAME=my-cluster
REGION=region-code
ROLE_NAME=AmazonEKS_S3_CSI_DriverRole
POLICY_ARN=AmazonEKS_S3_CSI_DriverRole_ARN
eksctl create iamserviceaccount \
    --name s3-csi-driver-sa \
    --namespace kube-system \
    --cluster $CLUSTER_NAME \
    --attach-policy-arn $POLICY_ARN \
    --approve \
    --role-name $ROLE_NAME \
    --region $REGION \
    --role-only
```

## Additional information<a name="add-ons-mountpoint-for-s3-add-on-information"></a>

To learn more about the add\-on, see [Access Amazon S3 objects with Mountpoint for Amazon S3 CSI driver](s3-csi.md)\.