# Kubernetes service accounts<a name="service-accounts"></a>

A Kubernetes service account provides an identity for processes that run in a pod\. For more information see [Managing Service Accounts](https://kubernetes.io/docs/reference/access-authn-authz/service-accounts-admin) in the Kubernetes documentation\. If your pod needs access to AWS services, you can map the service account to an AWS Identity and Access Management identity to grant that access\. For more information, see [IAM roles for service accounts](iam-roles-for-service-accounts.md)\.

## Service account tokens<a name="service-account-tokens"></a>

The [https://kubernetes.io/docs/reference/access-authn-authz/service-accounts-admin/#bound-service-account-token-volume](https://kubernetes.io/docs/reference/access-authn-authz/service-accounts-admin/#bound-service-account-token-volume) feature is enabled by default in Kubernetes version `1.21` and later\. This feature improves the security of service account tokens by allowing workloads running on Kubernetes to request JSON web tokens that are audience, time, and key bound\. Service account tokens have an expiration of one hour\. In earlier Kubernetes versions, the tokens didn't have an expiration\. This means that clients that rely on these tokens must refresh the tokens within an hour\. The following [Kubernetes client SDKs](https://kubernetes.io/docs/reference/using-api/client-libraries/) refresh tokens automatically within the required time frame:
+ Go version `0.15.7` and later
+ Python version `12.0.0` and later
+ Java version `9.0.0` and later
+ JavaScript version `0.10.3` and later
+ Ruby `master` branch
+ Haskell version `0.3.0.0`
+ C\# version `7.0.5` and later

If your workload is using an older client version, then you must update it\. To enable a smooth migration of clients to the newer time\-bound service account tokens, Kubernetes version `1.21` and later adds an extended expiry period to the service account token over the default one hour\. For Amazon EKS clusters, the extended expiry period is 90 days\. Your Amazon EKS cluster's Kubernetes API server rejects requests with tokens older than 90 days\. We recommend that you check your applications and their dependencies to make sure that the Kubernetes client SDKs are the same or later than the versions listed previously\.

When the API server receives requests with tokens that are older than one hour, it annotates the API audit log event with `annotations.authentication.k8s.io/stale-token`\. The value of the annotation looks like the following example:

```
subject: system:serviceaccount:common:fluent-bit, seconds after warning threshold: 4185802.
```<a name="identify-pods-using-stale-tokens"></a>

If your cluster has [control plane logging](control-plane-logs.md) enabled, then the annotations are in the audit logs\. You can use the following [CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html) query to identify all the pods in your Amazon EKS cluster that are using stale tokens:

```
fields @timestamp
| filter @logStream like /kube-apiserver-audit/
| filter @message like /seconds after warning threshold/
| parse @message "subject: *, seconds after warning threshold:*\"" as subject, elapsedtime
```

The `subject` refers to the service account that the pod used\. The `elapsedtime` indicates the elapsed time \(in seconds\) after reading the latest token\. The requests to the API server are denied when the `elapsedtime` exceeds 90 days\. You should proactively update your applications' Kubernetes client SDK to use one of the version listed previously that automatically refresh the token\. If the service account token used is close to 90 days and you don't have sufficient time to update your client SDK versions before token expiration, then you can terminate existing pods and create new ones\. This results in refetching of the service account token, giving you an additional 90 days to update your client version SDKs\.

If the pod is part of a deployment, the suggested way to terminate pods while keeping high availability is to perform a roll out with the following command\. Replace `my-deployment` with the name of your deployment\.

```
kubectl rollout restart deployment/my-deployment
```

## Cluster add\-ons<a name="boundserviceaccounttoken-validated-add-on-versions"></a>

The following cluster add\-ons have been updated to use the Kubernetes client SDKs that automatically refetch service account tokens\. We recommend making sure that the listed versions, or later versions, are installed on your `1.21` or later cluster\.
+ Amazon VPC CNI and CNI metrics helper plugins version `1.8.0` and later\. To check your current version or update it, see [Updating the Amazon VPC CNI plugin for Kubernetes add\-on](managing-vpc-cni.md) and [Installing the Amazon VPC CNI plugin for Kubernetes metrics helper add\-on](cni-metrics-helper.md)\.
+ CoreDNS version `1.8.4` and later\. To check your current version or update it, see [Updating the CoreDNS add\-on](managing-coredns.md)\.
+ AWS Load Balancer Controller version `2.0.0` and later\. To check your current version or update it, see [Installing the AWS Load Balancer Controller add\-on](aws-load-balancer-controller.md)\.
+ `kube-proxy` version `1.21.2-eksbuild.2` and later\. To check your current version or update it, see [Updating the `kube-proxy` add\-on](managing-kube-proxy.md)\.
+ AWS for Fluent Bit version `2.25.0` or later\. To update your current version, see [Releases](https://github.com/aws/aws-for-fluent-bit/releases) on GitHub\.
+ Fluentd image version [1\.14\.6\-1\.2](https://hub.docker.com/r/fluent/fluentd/tags?page=1&name=v1.14.6-1.2) or later and Fluentd filter plugin for Kubernetes metadata version [2\.11\.1](https://rubygems.org/gems/fluent-plugin-kubernetes_metadata_filter/versions/2.11.1) or later\. 