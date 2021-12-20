# Cluster authentication<a name="managing-auth"></a>

Amazon EKS uses IAM to provide authentication to your Kubernetes cluster \(through the  `aws eks get-token`  command, available in version 1\.16\.156 or later of the AWS CLI, or the [AWS IAM Authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator)\), but it still relies on native Kubernetes [Role Based Access Control](https://kubernetes.io/docs/admin/authorization/rbac/) \(RBAC\) for authorization\. This means that IAM is only used for authentication of valid IAM entities\. All permissions for interacting with your Amazon EKS cluster’s Kubernetes API is managed through the native Kubernetes RBAC system\. The following picture shows this relationship\.

![\[Amazon EKS and IAM integration\]](http://docs.aws.amazon.com/eks/latest/userguide/images/eks-iam.png)

**Note**  
Amazon EKS uses the authentication token to make the `sts:GetCallerIdentity` call\. As a result, AWS CloudTrail events with the name `GetCallerIdentity` from the source `sts.amazonaws.com` can have Amazon EKS service IP addresses for their source IP address\.

**Topics**
+ [Enabling IAM user and role access to your cluster](add-user-role.md)
+ [Authenticating users for your cluster from an OpenID Connect identity provider](authenticate-oidc-identity-provider.md)
+ [Create a `kubeconfig` for Amazon EKS](create-kubeconfig.md)
+ [Installing `aws-iam-authenticator`](install-aws-iam-authenticator.md)
+ [Default Amazon EKS Kubernetes roles and users](default-roles-users.md)