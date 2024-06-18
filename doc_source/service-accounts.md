# Grant Kubernetes workloads access to AWS using Kubernetes Service Accounts<a name="service-accounts"></a>

A Kubernetes service account provides an identity for processes that run in a Pod\. For more information see [Managing Service Accounts](https://kubernetes.io/docs/reference/access-authn-authz/service-accounts-admin) in the Kubernetes documentation\. If your Pod needs access to AWS services, you can map the service account to an AWS Identity and Access Management identity to grant that access\. For more information, see [IAM roles for service accounts](iam-roles-for-service-accounts.md)\.

## Service account tokens<a name="service-account-tokens"></a>

The [https://kubernetes.io/docs/reference/access-authn-authz/service-accounts-admin/#bound-service-account-token-volume](https://kubernetes.io/docs/reference/access-authn-authz/service-accounts-admin/#bound-service-account-token-volume) feature is enabled by default in Kubernetes versions\. This feature improves the security of service account tokens by allowing workloads running on Kubernetes to request JSON web tokens that are audience, time, and key bound\. Service account tokens have an expiration of one hour\. In earlier Kubernetes versions, the tokens didn't have an expiration\. This means that clients that rely on these tokens must refresh the tokens within an hour\. The following [Kubernetes client SDKs](https://kubernetes.io/docs/reference/using-api/client-libraries/) refresh tokens automatically within the required time frame:
+ Go version `0.15.7` and later
+ Python version `12.0.0` and later
+ Java version `9.0.0` and later
+ JavaScript version `0.10.3` and later
+ Ruby `master` branch
+ Haskell version `0.3.0.0`
+ C\# version `7.0.5` and later

If your workload is using an earlier client version, then you must update it\. To enable a smooth migration of clients to the newer time\-bound service account tokens, Kubernetes adds an extended expiry period to the service account token over the default one hour\. For Amazon EKS clusters, the extended expiry period is 90 days\. Your Amazon EKS cluster's Kubernetes API server rejects requests with tokens that are greater than 90 days old\. We recommend that you check your applications and their dependencies to make sure that the Kubernetes client SDKs are the same or later than the versions listed previously\.

When the API server receives requests with tokens that are greater than one hour old, it annotates the API audit log event with `annotations.authentication.k8s.io/stale-token`\. The value of the annotation looks like the following example:

```
subject: system:serviceaccount:common:fluent-bit, seconds after warning threshold: 4185802.
```<a name="identify-pods-using-stale-tokens"></a>

If your cluster has [control plane logging](control-plane-logs.md) enabled, then the annotations are in the audit logs\. You can use the following [CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html) query to identify all the Pods in your Amazon EKS cluster that are using stale tokens:

```
fields @timestamp
| filter @logStream like /kube-apiserver-audit/
| filter @message like /seconds after warning threshold/
| parse @message "subject: *, seconds after warning threshold:*\"" as subject, elapsedtime
```

The `subject` refers to the service account that the Pod used\. The `elapsedtime` indicates the elapsed time \(in seconds\) after reading the latest token\. The requests to the API server are denied when the `elapsedtime` exceeds 90 days \(7,776,000 seconds\)\. You should proactively update your applications' Kubernetes client SDK to use one of the version listed previously that automatically refresh the token\. If the service account token used is close to 90 days and you don't have sufficient time to update your client SDK versions before token expiration, then you can terminate existing Pods and create new ones\. This results in refetching of the service account token, giving you an additional 90 days to update your client version SDKs\.

If the Pod is part of a deployment, the suggested way to terminate Pods while keeping high availability is to perform a roll out with the following command\. Replace `my-deployment` with the name of your deployment\.

```
kubectl rollout restart deployment/my-deployment
```

## Cluster add\-ons<a name="boundserviceaccounttoken-validated-add-on-versions"></a>

The following cluster add\-ons have been updated to use the Kubernetes client SDKs that automatically refetch service account tokens\. We recommend making sure that the listed versions, or later versions, are installed on your cluster\.
+ Amazon VPC CNI plugin for Kubernetes and metrics helper plugins version `1.8.0` and later\. To check your current version or update it, see [Working with the Amazon VPC CNI plugin for Kubernetes Amazon EKS add\-on](managing-vpc-cni.md) and [cni\-metrics\-helper](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/cmd/cni-metrics-helper/README.md)\.
+ CoreDNS version `1.8.4` and later\. To check your current version or update it, see [Working with the CoreDNS Amazon EKS add\-on](managing-coredns.md)\.
+ AWS Load Balancer Controller version `2.0.0` and later\. To check your current version or update it, see [What is the AWS Load Balancer Controller?](aws-load-balancer-controller.md)\.
+ A current `kube-proxy` version\. To check your current version or update it, see [Working with the Kubernetes `kube-proxy` add\-on](managing-kube-proxy.md)\.
+ AWS for Fluent Bit version `2.25.0` or later\. To update your current version, see [Releases](https://github.com/aws/aws-for-fluent-bit/releases) on GitHub\.
+ Fluentd image version [1\.14\.6\-1\.2](https://hub.docker.com/r/fluent/fluentd/tags?page=1&name=v1.14.6-1.2) or later and Fluentd filter plugin for Kubernetes metadata version [2\.11\.1](https://rubygems.org/gems/fluent-plugin-kubernetes_metadata_filter/versions/2.11.1) or later\. 

## Granting AWS Identity and Access Management permissions to workloads on Amazon Elastic Kubernetes Service clusters<a name="service-accounts-iam"></a>

Amazon EKS provides two ways to grant AWS Identity and Access Management permissions to workloads that run in Amazon EKS clusters: *IAM roles for service accounts*, and *EKS Pod Identities*\.

IAM roles for service accounts  
*IAM roles for service accounts \(IRSA\)* configures Kubernetes applications running on AWS with fine\-grained IAM permissions to access various other AWS resources such as Amazon S3 buckets, Amazon DynamoDB tables, and more\. You can run multiple applications together in the same Amazon EKS cluster, and ensure each application has only the minimum set of permissions that it needs\. IRSA was build to support various Kubernetes deployment options supported by AWS such as Amazon EKS, Amazon EKS Anywhere, Red Hat OpenShift Service on AWS, and self managed Kubernetes clusters on Amazon EC2 instances\. Thus, IRSA was build using foundational AWS service like IAM, and did not take any direct dependency on the Amazon EKS service and the EKS API\. For more information, see [IAM roles for service accounts](iam-roles-for-service-accounts.md)\.

EKS Pod Identities  
EKS Pod Identity offers cluster administrators a simplified workflow for authenticating applications to access various other AWS resources such as Amazon S3 buckets, Amazon DynamoDB tables, and more\. EKS Pod Identity is for EKS only, and as a result, it simplifies how cluster administrators can configure Kubernetes applications to obtain IAM permissions\. These permissions can now be easily configured with fewer steps directly through AWS Management Console, EKS API, and AWS CLI, and there isn't any action to take inside the cluster in any Kubernetes objects\. Cluster administrators don't need to switch between the EKS and IAM services, or use privileged IAM operations to configure permissions required by your applications\. IAM roles can now be used across multiple clusters without the need to update the role trust policy when creating new clusters\. IAM credentials supplied by EKS Pod Identity include role session tags, with attributes such as cluster name, namespace, service account name\. Role session tags enable administrators to author a single role that can work across service accounts by allowing access to AWS resources based on matching tags\. For more information, see [EKS Pod Identities](pod-identities.md)\.

### Comparing EKS Pod Identity and IRSA<a name="service-accounts-iam-compare"></a>

At a high level, both EKS Pod Identity and IRSA enables you to grant IAM permissions to applications running on Kubernetes clusters\. But they are fundamentally different in how you configure them, the limits supported, and features enabled\. Below, we compare some of the key facets of both the solutions\.


|  | EKS Pod Identity | IRSA | 
| --- | --- | --- | 
|  Role extensibility  |  You have to setup each role once to establish trust with the newly\-introduced Amazon EKS service principal `pods.eks.amazonaws.com`\. After this one\-time step, you don't need to update the role's trust policy each time that it is used in a new cluster\.  |  You have to update the IAM role's trust policy with the new EKS cluster OIDC provider endpoint each time you want to use the role in a new cluster\.  | 
|  Cluster scalability  |  EKS Pod Identity doesn't require users to setup IAM OIDC provider, so this limit doesn't apply\.  |  Each EKS cluster has an OpenID Connect \(OIDC\) issuer URL associated with it\. To use IRSA, a unique OpenID Connect provider needs to be created for each EKS cluster in IAM\. IAM has a default global limit of 100 OIDC providers for each AWS account\. If you plan to have more than 100 EKS clusters for each AWS account with IRSA, then you will reach the IAM OIDC provider limit\.  | 
|  Role scalability  |  EKS Pod Identity doesn't require users to define trust relationship between IAM role and service account in the trust policy, so this limit doesn't apply\.  |  In IRSA, you define the trust relationship between an IAM role and service account in the role's trust policy\. By default, the length of trust policy size is `2048`\. This means that you can typically define 4 trust relationships in a single trust policy\. While you can get the trust policy length limit increased, you are typically limited to a max of 8 trust relationships within a single trust policy\.  | 
|  Role reusability  |  AWS STS temporary credentials supplied by EKS Pod Identity include role session tags, such as cluster name, namespace, service account name\. Role session tags enable administrators to author a single IAM role that can be used with multiple service accounts, with different effective permission, by allowing access to AWS resources based on tags attached to them\. This is also called attribute\-based access control \(ABAC\)\. For more information, see [Define permissions for EKS Pod Identities to assume roles based on tags](pod-id-abac.md)\.  |  AWS STS session tags are not supported\. You can reuse a role between clusters but every pod receives all of the permissions of the role\.  | 
|  Environments supported  |  EKS Pod Identity is only available on Amazon EKS\.  |  IRSA can be used such as Amazon EKS, Amazon EKS Anywhere, Red Hat OpenShift Service on AWS, and self managed Kubernetes clusters on Amazon EC2 instances\.  | 
|  EKS versions supported  |  EKS Kubernetes versions `1.24` or later\. For the specific platform versions, see [EKS Pod Identity cluster versions](pod-identities.md#pod-id-cluster-versions)\.  |  All of the supported EKS cluster versions\.  | 