# AWS Distro for OpenTelemetry \(ADOT\) prerequisites and considerations<a name="adot-reqts"></a>

Before installing the AWS Distro for OpenTelemetry \(ADOT\) add\-on, you must meet the following prerequisites and considerations\.
+ Connected clusters can't use this add\-on\.
+ Meet the [TLS certificate requirement](#adot-reqtcr) to ensure end\-to\-end encryption\.
+ If installing an add\-on version that is `v0.62.1` or earlier, grant permissions to Amazon EKS add\-ons to install ADOT\.

  ```
  kubectl apply -f https://amazon-eks.s3.amazonaws.com/docs/addons-otel-permissions.yaml
  ```

## TLS certificate requirement<a name="adot-reqtcr"></a>

The ADOT Operator uses [admission webhooks](https://kubernetes.io/docs/reference/access-authn-authz/webhook/) to mutate and validate the Collector Custom Resource \(CR\) requests\. In Kubernetes, the webhook requires a TLS certificate that the API server is configured to trust\. There are multiple ways for you to generate the required TLS certificate\. However, the default method is to install the latest version of the [cert\-manager](https://cert-manager.io/docs/) manually\. The cert\-manager generates a self\-signed certificate\.

### Installing cert\-manager<a name="adot-reqtcrsteps"></a>

**Installing cert\-manager**

1. Install cert\-manager using the following command\. This creates the necessary cert\-manager objects that allow end\-to\-end encryption\. This must be done for each cluster that will have ADOT installed\.

   ```
   kubectl apply -f \
   https://github.com/cert-manager/cert-manager/releases/download/v1.8.2/cert-manager.yaml
   ```

1. Verify that cert\-manager is ready using the following command\.

   ```
   kubectl get pod -w -n cert-manager
   ```

   The example output is as follows\.

   ```
   NAME READY  STATUS RESTARTS  AGE
   cert-manager-5597cff495-mnb2p  1/1  Running  0 12d
   cert-manager-cainjector-bd5f9c764-8jp5g  1/1  Running  0 12d
   cert-manager-webhook-5f57f59fbc-h9st8  1/1  Running  0 12d
   ```