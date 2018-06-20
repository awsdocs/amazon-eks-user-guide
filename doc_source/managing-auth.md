# Managing Cluster Authentication<a name="managing-auth"></a>

Amazon EKS uses IAM to provide authentication to your Kubernetes cluster \(through the [Heptio Authenticator](https://github.com/heptio/authenticator)\), but it still relies on native Kubernetes [Role Based Access Control](https://kubernetes.io/docs/admin/authorization/rbac/) \(RBAC\) for authorization\. This means that IAM is only used for authentication of valid IAM entities\. All permissions for interacting with your Amazon EKS cluster’s Kubernetes API is managed through the native Kubernetes RBAC system\.

![\[Amazon EKS and IAM integration\]](http://docs.aws.amazon.com/eks/latest/userguide/images/eks-iam.png)

**Topics**
+ [Configure kubectl for Amazon EKS](configure-kubectl.md)
+ [Create a `kubeconfig` for Amazon EKS](create-kubeconfig.md)
+ [Managing Users or IAM Roles for your Cluster](add-user-role.md)