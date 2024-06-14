# Authenticate users for your cluster from an OpenID Connect identity provider<a name="authenticate-oidc-identity-provider"></a>

Amazon EKS supports using OpenID Connect \(OIDC\) identity providers as a method to authenticate users to your cluster\. OIDC identity providers can be used with, or as an alternative to AWS Identity and Access Management \(IAM\)\. For more information about using IAM, see [Grant access to Kubernetes APIs ](grant-k8s-access.md)\. After configuring authentication to your cluster, you can create Kubernetes `roles` and `clusterroles` to assign permissions to the roles, and then bind the roles to the identities using Kubernetes `rolebindings` and `clusterrolebindings`\. For more information, see [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) in the Kubernetes documentation\.

**Considerations**
+ You can associate one OIDC identity provider to your cluster\.
+ Kubernetes doesn't provide an OIDC identity provider\. You can use an existing public OIDC identity provider, or you can run your own identity provider\. For a list of certified providers, see [OpenID Certification](https://openid.net/certification/) on the OpenID site\.
+ The issuer URL of the OIDC identity provider must be publicly accessible, so that Amazon EKS can discover the signing keys\. Amazon EKS doesn't support OIDC identity providers with self\-signed certificates\.
+ You can't disable IAM authentication to your cluster, because it's still required for joining nodes to a cluster\.
+ An Amazon EKS cluster must still be created by an AWS [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html), rather than an OIDC identity provider user\. This is because the cluster creator interacts with the Amazon EKS APIs, rather than the Kubernetes APIs\.
+ OIDC identity provider\-authenticated users are listed in the cluster's audit log if CloudWatch logs are turned on for the control plane\. For more information, see [Enabling and disabling control plane logs](control-plane-logs.md#enabling-control-plane-log-export)\.
+ You can't sign in to the AWS Management Console with an account from an OIDC provider\. You can only [view Kubernetes resources](view-kubernetes-resources.md) in the console by signing into the AWS Management Console with an AWS Identity and Access Management account\.

## Associate an OIDC identity provider<a name="associate-oidc-identity-provider"></a>

Before you can associate an OIDC identity provider with your cluster, you need the following information from your provider:<a name="oidc-identity-provider-required-properties"></a>

**Issuer URL**  
The URL of the OIDC identity provider that allows the API server to discover public signing keys for verifying tokens\. The URL must begin with `https://` and should correspond to the `iss` claim in the provider's OIDC ID tokens\. In accordance with the OIDC standard, path components are allowed but query parameters are not\. Typically the URL consists of only a host name, like `https://server.example.org` or `https://example.com`\. This URL should point to the level below `.well-known/openid-configuration` and must be publicly accessible over the internet\.

**Client ID \(also known as *audience*\)**  
The ID for the client application that makes authentication requests to the OIDC identity provider\.

You can associate an identity provider using `eksctl` or the AWS Management Console\.

------
#### [ eksctl ]

**To associate an OIDC identity provider to your cluster using `eksctl`**

1. Create a file named *`associate-identity-provider.yaml`* with the following contents\. Replace the *`example values`* with your own\. The values in the `identityProviders` section are obtained from your OIDC identity provider\. Values are only required for the `name`, `type`, `issuerUrl`, and `clientId` settings under `identityProviders`\.

   ```
   ---
   apiVersion: eksctl.io/v1alpha5
   kind: ClusterConfig
   
   metadata:
     name: my-cluster
     region: your-region-code
   
   identityProviders:
     - name: my-provider
       type: oidc
       issuerUrl: https://example.com
       clientId: kubernetes
       usernameClaim: email
       usernamePrefix: my-username-prefix
       groupsClaim: my-claim
       groupsPrefix: my-groups-prefix
       requiredClaims:
         string: string
       tags:
         env: dev
   ```
**Important**  
Don't specify `system:`, or any portion of that string, for `groupsPrefix` or `usernamePrefix`\.

1. Create the provider\.

   ```
   eksctl associate identityprovider -f associate-identity-provider.yaml
   ```

1. To use `kubectl` to work with your cluster and OIDC identity provider, see [Using `kubectl`](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#using-kubectl) in the Kubernetes documentation\.

------
#### [ AWS Management Console ]

**To associate an OIDC identity provider to your cluster using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Select your cluster, and then select the **Access** tab\.

1. In the **OIDC Identity Providers** section, select** Associate Identity Provider**\.

1. On the **Associate OIDC Identity Provider** page, enter or select the following options, and then select **Associate**\.
   + For **Name**, enter a unique name for the provider\.
   + For **Issuer URL**, enter the URL for your provider\. This URL must be accessible over the internet\.
   + For **Client ID**, enter the OIDC identity provider's client ID \(also known as **audience**\)\.
   + For **Username claim**, enter the claim to use as the username\.
   + For **Groups claim**, enter the claim to use as the user's group\.
   + \(Optional\) Select **Advanced options**, enter or select the following information\.
     + **Username prefix** – Enter a prefix to prepend to username claims\. The prefix is prepended to username claims to prevent clashes with existing names\. If you do not provide a value, and the username is a value other than `email`, the prefix defaults to the value for **Issuer URL**\. You can use the value` -` to disable all prefixing\. Don't specify `system:` or any portion of that string\.
     + **Groups prefix** – Enter a prefix to prepend to groups claims\. The prefix is prepended to group claims to prevent clashes with existing names \(such as` system: groups`\)\. For example, the value `oidc:` creates group names like `oidc:engineering` and `oidc:infra`\. Don't specify `system:` or any portion of that string\.\.
     + **Required claims** – Select **Add claim** and enter one or more key value pairs that describe required claims in the client ID token\. The paris describe required claims in the ID Token\. If set, each claim is verified to be present in the ID token with a matching value\.

1. To use `kubectl` to work with your cluster and OIDC identity provider, see [Using `kubectl`](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#using-kubectl) in the Kubernetes documentation\.

------

## Disassociate an OIDC identity provider from your cluster<a name="disassociate-oidc-identity-provider"></a>

If you disassociate an OIDC identity provider from your cluster, users included in the provider can no longer access the cluster\. However, you can still access the cluster with [IAM principals](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html)\.

**To disassociate an OIDC identity provider from your cluster using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the **OIDC Identity Providers** section, select **Disassociate**, enter the identity provider name, and then select `Disassociate`\.

## Example IAM policy<a name="oidc-identity-provider-iam-policy"></a>

If you want to prevent an OIDC identity provider from being associated with a cluster, create and associate the following IAM policy to the IAM accounts of your Amazon EKS administrators\. For more information, see [Creating IAM policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html) and [Adding IAM identity permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html#add-policies-console) in the IAM User Guide and [Actions, resources, and condition keys for Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelasticcontainerserviceforkubernetes.html) in the Service Authorization Reference\.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "denyOIDC",
            "Effect": "Deny",
            "Action": [
                "eks:AssociateIdentityProviderConfig"
            ],
            "Resource": "arn:aws:eks:us-west-2.amazonaws.com:111122223333:cluster/*"

        },
        {
            "Sid": "eksAdmin",
            "Effect": "Allow",
            "Action": [
                "eks:*"
            ],
            "Resource": "*"
        }
    ]
}
```

The following example policy allows OIDC identity provider association if the `clientID` is `kubernetes` and the `issuerUrl` is `https://cognito-idp.us-west-2amazonaws.com/*`\.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowCognitoOnly",
            "Effect": "Deny",
            "Action": "eks:AssociateIdentityProviderConfig",
            "Resource": "arn:aws:eks:us-west-2:111122223333:cluster/my-instance",
            "Condition": {
                "StringNotLikeIfExists": {
                    "eks:issuerUrl": "https://cognito-idp.us-west-2.amazonaws.com/*"
                }
            }
        },
        {
            "Sid": "DenyOtherClients",
            "Effect": "Deny",
            "Action": "eks:AssociateIdentityProviderConfig",
            "Resource": "arn:aws:eks:us-west-2:111122223333:cluster/my-instance",
            "Condition": {
                "StringNotEquals": {
                    "eks:clientId": "kubernetes"
                }
            }
        },
        {
            "Sid": "AllowOthers",
            "Effect": "Allow",
            "Action": "eks:*",
            "Resource": "*"
        }
    ]
}
```

## Partner validated OIDC identity providers<a name="partner-validated-identity-providers"></a>

Amazon EKS maintains relationships with a network of partners that offer support for compatible OIDC identity providers\. Refer to the following partners' documentation for details on how to integrate the identity provider with Amazon EKS\.


|  Partner  |  Product  |  Documentation  | 
| --- | --- | --- | 
|  PingIdentity  |  [PingOne for Enterprise](https://docs.pingidentity.com/r/en-us/pingoneforenterprise/p14e_landing)  |  [Installation instructions](https://docs.pingidentity.com/r/en-us/solution-guides/htg_config_oidc_authn_aws_eks_custers)  | 

Amazon EKS aims to give you a wide selection of options to cover all use cases\. If you develop a commercially supported OIDC compatible identity provider that is not listed here, then contact our partner team at [aws\-container\-partners@amazon\.com](mailto:aws-container-partners@amazon.com) for more information\.