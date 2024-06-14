# Manage access<a name="cluster-auth"></a>

Learn how to manage access to your Amazon EKS cluster\. Using Amazon EKS requires knowledge of how both Kubernetes and AWS Identity and Access Management \(AWS IAM\) handle access control\. 

**This section includes:**

**[Grant access to Kubernetes APIs ](grant-k8s-access.md)— **Learn how to enable applications or users to authenticate to the Kubernetes API\. You can use access entries, the aws\-auth ConfigMap, or an external OIDC provider\. 

**[Creating or updating a `kubeconfig` file for an Amazon EKS cluster](create-kubeconfig.md) — **Learn how to configure kubectl to communicate with your Amazon EKS cluster\. Use the AWS CLI to create a kubeconfig file\. 

**[Grant Kubernetes workloads access to AWS using Kubernetes Service Accounts](service-accounts.md) —** Learn how to associate a Kubernetes service account with AWS IAM Roles\. You can use Pod Identity or IAM Roles for Service Accounts \(IRSA\)\. 

**Common Tasks:**
+ Grant developers access to the Kubernetes API\. View Kubernetes resources in the AWS Management Console\. 
  + Solution: [Use Access Entries](access-entries.md) to associate Kubernetes RBAC permissions with AWS IAM Users or Roles\.
+ Configure kubectl to talk to an Amazon EKS cluster using AWS Credentials\. 
  + Solution: Use the AWS CLI to[ create a kubeconfig file](create-kubeconfig.md)\. 
+ Use an external identity provider, such as Ping Identity, to authenticate users to the Kubernetes API\.
  + Solution: [Link an external OIDC provider](authenticate-oidc-identity-provider.md)\.
+ Grant workloads on your Kubernetes cluster the ability to call AWS APIs\. 
  + Solution: [Use Pod Identity](pod-identities.md) to associate an AWS IAM Role to a Kubernetes Service Account\. 

**Background: **
+ [Learn how Kubernetes Service Accounts work\. ](https://kubernetes.io/docs/concepts/security/service-accounts/)
+ [Review the Kubernetes Role Based Access Control \(RBAC\) Model](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) 
+ For more information about managing access to AWS resources, see the [AWS IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/intro-structure.html)\. Alternatively, take a free[ introductory training on using AWS IAM](https://explore.skillbuilder.aws/learn/course/external/view/elearning/120/introduction-to-aws-identity-and-access-management-iam)\. 

