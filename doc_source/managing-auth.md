# Managing Cluster Authentication<a name="managing-auth"></a>

Amazon EKS uses IAM to provide authentication to your Kubernetes cluster \(through the aws eks get\-token command, available in version 1\.18\.10 or greater of the AWS CLI, or the [AWS IAM Authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator)\), but it still relies on native Kubernetes [Role Based Access Control](https://kubernetes.io/docs/admin/authorization/rbac/) \(RBAC\) for authorization\. This means that IAM is only used for authentication of valid IAM entities\. All permissions for interacting with your Amazon EKS cluster’s Kubernetes API is managed through the native Kubernetes RBAC system\.

![\[Amazon EKS and IAM integration\]](http://docs.aws.amazon.com/eks/latest/userguide/images/eks-iam.png)

**Topics**
+ [Installing `kubectl`](install-kubectl.md)
+ [Installing `aws-iam-authenticator`](install-aws-iam-authenticator.md)
+ [Create a `kubeconfig` for Amazon EKS](create-kubeconfig.md)
+ [Managing Users or IAM Roles for your Cluster](add-user-role.md)