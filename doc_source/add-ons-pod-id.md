# EKS Pod Identity Agent<a name="add-ons-pod-id"></a>

The Amazon EKS Pod Identity Agent Amazon EKS add\-on provides the ability to manage credentials for your applications, similar to the way that EC2 instance profiles provide credentials to EC2 instances\.

The Amazon EKS add\-on name is `eks-pod-identity-agent`\.

## Required IAM permissions<a name="add-ons-pod-id-iam-permissions"></a>

This add\-on users permissions from the [Amazon EKS node IAM role](create-node-role.md)\.

## Update information<a name="add-ons-pod-id-update-information"></a>

You can only update one minor version at a time\. For example, if your current version is `1.28.x-eksbuild.y` and you want to update to `1.30.x-eksbuild.y`, then you must update your current version to `1.29.x-eksbuild.y` and then update it again to `1.30.x-eksbuild.y`\. For more information about updating the add\-on, see [Updating the Amazon VPC CNI plugin for Kubernetes Amazon EKS add\-on](vpc-add-on-update.md)\.