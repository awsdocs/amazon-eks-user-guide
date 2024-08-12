# Disassociate an OIDC identity provider from your cluster<a name="disassociate-oidc-identity-provider"></a>

If you disassociate an OIDC identity provider from your cluster, users included in the provider can no longer access the cluster\. However, you can still access the cluster with [IAM principals](https://docs.aws.amazon.com/IAM/latest/UserGuide/intro-structure.html)\.

**To disassociate an OIDC identity provider from your cluster using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the **OIDC Identity Providers** section, select **Disassociate**, enter the identity provider name, and then select `Disassociate`\.