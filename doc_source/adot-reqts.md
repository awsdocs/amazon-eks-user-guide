# AWS Distro for OpenTelemetry \(ADOT\) prerequisites and considerations<a name="adot-reqts"></a>

Before installing the AWS Distro for OpenTelemetry \(ADOT\) add\-on, you must meet the following prerequisites and considerations\.
+ [Connected clusters](eks-connector.md) can't use this add\-on\.
+ Meet the TLS certificate requirement to ensure end\-to\-end encryption\. The ADOT Operator uses [admission webhooks](https://kubernetes.io/docs/reference/access-authn-authz/webhook/) to mutate and validate the Collector Custom Resource \(CR\) requests\. In Kubernetes, the webhook requires a TLS certificate that the API server is configured to trust\. There are multiple ways for you to generate the required TLS certificate\. However, the default method is to install the latest version of the [https://cert-manager.io/docs/](https://cert-manager.io/docs/) manually\. The `cert-manager` generates a self\-signed certificate\. For more information on installing `cert-manager`, see [`kubectl` apply](https://cert-manager.io/docs/installation/kubectl/#steps) in the `cert-manager` Documentation\.
+ If installing an add\-on version that is `v0.62.1` or earlier, grant permissions to Amazon EKS add\-ons to install ADOT\.

  ```
  kubectl apply -f https://amazon-eks.s3.amazonaws.com/docs/addons-otel-permissions.yaml
  ```