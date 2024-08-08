# CoreDNS<a name="add-ons-coredns"></a>

The CoreDNS Amazon EKS add\-on is a flexible, extensible DNS server that can serve as the Kubernetes cluster DNS\. The self\-managed or managed type of this add\-on was installed, by default, when you created your cluster\. When you launch an Amazon EKS cluster with at least one node, two replicas of the CoreDNS image are deployed by default, regardless of the number of nodes deployed in your cluster\. The CoreDNS Pods provide name resolution for all Pods in the cluster\. You can deploy the CoreDNS Pods to Fargate nodes if your cluster includes an [Define which Pods use AWS Fargate when launched](fargate-profile.md) with a namespace that matches the namespace for the CoreDNS `deployment`\.

The Amazon EKS add\-on name is `coredns`\.

## Required IAM permissions<a name="add-ons-coredns-iam-permissions"></a>

This add\-on doesn't require any permissions\.

## Additional information<a name="add-ons-coredns-information"></a>

To learn more about CoreDNS, see [Using CoreDNS for Service Discovery](https://kubernetes.io/docs/tasks/administer-cluster/coredns/) and [Customizing DNS Service](https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/) in the Kubernetes documentation\.