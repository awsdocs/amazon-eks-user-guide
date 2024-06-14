# Grant access to Kubernetes APIs<a name="grant-k8s-access"></a>

Your cluster has an Kubernetes API endpoint\. Kubectl uses this API\. You can authenticate to this API using two types of identities: 
+ **An AWS Identity and Access Management \(IAM\) *principal* \(role or user\)** – This type requires authentication to IAM\. Users can sign in to AWS as an [IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html) user or with a [federated identity](https://aws.amazon.com/identity/federation/) by using credentials provided through an identity source\. Users can only sign in with a federated identity if your administrator previously set up identity federation using IAM roles\. When users access AWS by using federation, they're indirectly [assuming a role](https://docs.aws.amazon.com/IAM/latest/UserGuide/when-to-use-iam.html#security_iam_authentication-iamrole)\. When users use this type of identity, you:
  + Can assign them Kubernetes permissions so that they can work with Kubernetes objects on your cluster\. For more information about how to assign permissions to your IAM principals so that they're able to access Kubernetes objects on your cluster, see [Manage access entries](access-entries.md)\.
  + Can assign them IAM permissions so that they can work with your Amazon EKS cluster and its resources using the Amazon EKS API, AWS CLI, AWS CloudFormation, AWS Management Console, or `eksctl`\. For more information, see [Actions defined by Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html#amazonelastickubernetesservice-actions-as-permissions) in the Service Authorization Reference\.
  + Nodes join your cluster by assuming an IAM role\. The ability to access your cluster using IAM principals is provided by the [AWS IAM Authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator#readme), which runs on the Amazon EKS control plane\. 
+ **A user in your own OpenID Connect \(OIDC\) provider** – This type requires authentication to your [https://openid.net/connect/](https://openid.net/connect/) provider\. For more information about setting up your own OIDC provider with your Amazon EKS cluster, see [Authenticate users for your cluster from an OpenID Connect identity provider](authenticate-oidc-identity-provider.md)\. When users use this type of identity, you:
  + Can assign them Kubernetes permissions so that they can work with Kubernetes objects on your cluster\.
  + Can't assign them IAM permissions so that they can work with your Amazon EKS cluster and its resources using the Amazon EKS API, AWS CLI, AWS CloudFormation, AWS Management Console, or `eksctl`\.

You can use both types of identities with your cluster\. The IAM authentication method cannot be disabled\. The OIDC authentication method is optional\.

## Associate IAM Identities with Kubernetes Permissions<a name="authentication-modes"></a>

The [AWS IAM Authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator#readme) is installed on your cluster's control plane\. It enables [AWS Identity and Access Management](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html) \(IAM\) principals \(roles and users\) that you allow to access Kubernetes resources on your cluster\. You can allow IAM principals to access Kubernetes objects on your cluster using one of the following methods:
+ **Creating access entries** – If your cluster is at or later than the platform version listed in the [Prerequisites](access-entries.md#access-entries-prerequisites) section for your cluster's Kubernetes version, we recommend that you use this option\.

  Use *access entries* to manage the Kubernetes permissions of IAM principals from outside the cluster\. You can add and manage access to the cluster by using the EKS API, AWS Command Line Interface, AWS SDKs, AWS CloudFormation, and AWS Management Console\. This means you can manage users with the same tools that you created the cluster with\.

  To get started, follow [Setting up access entries](access-entries.md#setting-up-access-entries), then [Migrating existing `aws-auth ConfigMap` entries to access entries](migrating-access-entries.md)\.
+ **Adding entries to the `aws-auth` `ConfigMap`** – If your cluster's platform version is earlier than the version listed in the [Prerequisites](access-entries.md#access-entries-prerequisites) section, then you must use this option\. If your cluster's platform version is at or later than the platform version listed in the [Prerequisites](access-entries.md#access-entries-prerequisites) section for your cluster's Kubernetes version, and you've added entries to the `ConfigMap`, then we recommend that you migrate those entries to access entries\. You can't migrate entries that Amazon EKS added to the `ConfigMap` however, such as entries for IAM roles used with managed node groups or Fargate profiles\. For more information, see [Grant access to Kubernetes APIs ](#grant-k8s-access)\.
  + If you have to use the `aws-auth` `ConfigMap` option, you can add entries to the `ConfigMap` using the **eksctl create iamidentitymapping** command\. For more information, see [Manage IAM users and roles](https://eksctl.io/usage/iam-identity-mappings/) in the `eksctl` documentation\.

## Set Cluster Authentication Mode<a name="set-cam"></a>

Each cluster has an *authentication mode*\. The authentication mode determines which methods you can use to allow IAM principals to access Kubernetes objects on your cluster\. There are three authentication modes\.

**Important**  
Once the access entry method is enabled, it cannot be disabled\.   
If the `ConfigMap` method is not enabled during cluster creation, it cannot be enabled later\. All clusters created before the introduction of access entries have the `ConfigMap` method enabled\. 

The `aws-auth` `ConfigMap` inside the cluster  
This is the original authentication mode for Amazon EKS clusters\. The IAM principal that created the cluster is the initial user that can access the cluster by using `kubectl`\. The initial user must add other users to the list in the `aws-auth` `ConfigMap` and assign permissions that affect the other users within the cluster\. These other users can't manage or remove the initial user, as there isn't an entry in the `ConfigMap` to manage\.

Both the `ConfigMap` and access entries  
With this authentication mode, you can use both methods to add IAM principals to the cluster\. Note that each method stores separate entries; for example, if you add an access entry from the AWS CLI, the `aws-auth` `ConfigMap` is not updated\.

Access entries only  
With this authentication mode, you can use the EKS API, AWS Command Line Interface, AWS SDKs, AWS CloudFormation, and AWS Management Console to manage access to the cluster for IAM principals\.  
Each access entry has a *type* and you can use the combination of an *access scope* to limit the principal to a specific namespace and an *access policy* to set preconfigured reusable permissions policies\. Alternatively, you can use the STANDARD type and Kubernetes RBAC groups to assign custom permissions\.


| Authentication mode | Methods | 
| --- | --- | 
| ConfigMap only \(CONFIG\_MAP\) | aws\-auth ConfigMap | 
| EKS API and ConfigMap \(API\_AND\_CONFIG\_MAP\) | access entries in the EKS API, AWS Command Line Interface, AWS SDKs, AWS CloudFormation, and AWS Management Console and aws\-auth ConfigMap | 
| EKS API only \(API\) | access entries in the EKS API, AWS Command Line Interface, AWS SDKs, AWS CloudFormation, and AWS Management Console | 