# `Kube-proxy`<a name="add-ons-kube-proxy"></a>

The `Kube-proxy` Amazon EKS add\-on maintains network rules on each Amazon EC2 node\. It enables network communication to your Pods\. The self\-managed or managed type of this add\-on is installed on each Amazon EC2 node in your cluster, by default\.

The Amazon EKS add\-on name is `kube-proxy`\.

## Required IAM permissions<a name="add-ons-kube-proxy-iam-permissions"></a>

This add\-on doesn't require any permissions\.

## Update information<a name="add-ons-kube-proxy-update-information"></a>

Before updating your current version, consider the following requirements:
+ `Kube-proxy` on an Amazon EKS cluster has the same [compatibility and skew policy as Kubernetes](https://kubernetes.io/releases/version-skew-policy/#kube-proxy)\.

## Additional information<a name="add-ons-kube-proxy-information"></a>

To learn more about `kube-proxy`, see [https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/) in the Kubernetes documentation\.