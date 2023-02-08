# Deploy a sample application to test the AWS Distro for OpenTelemetry Collector<a name="sample-app"></a>

The sample application will generate and send OTLP data to any of the services that you have configured through the AWS Distro for OpenTelemetry [\(ADOT\) Collector deployment](deploy-collector.md)\. This step is optional if you already have an application running inside your cluster that can produce data\. Consult your application's documentation to ensure that data is sent to the correct endpoints\.

The sample application and traffic generator were largely taken from an example in the [ADOT Collector repository](https://github.com/aws-observability/aws-otel-collector/blob/main/examples/docker/docker-compose.yaml)\. A `docker-compose.yaml` file was translated to Kubernetes resources using the [Kompose tool](https://kompose.io/)\.

To apply the traffic generator and sample application, do the following steps\.

1. Download the `traffic-generator.yaml` file to your computer\. You can also [view the file](https://github.com/aws-observability/aws-otel-community/blob/master/sample-configs/traffic-generator.yaml) on GitHub\.

   ```
   curl -O https://raw.githubusercontent.com/aws-observability/aws-otel-community/master/sample-configs/traffic-generator.yaml
   ```

1. In `traffic-generator.yaml`, make sure that the second `kind` value reflects your mode\. For more information, see the ADOT Collector [installation instructions](https://aws-otel.github.io/docs/getting-started/operator#step-2-install-adot-collector-as-kubernetes-custom-resource-to-your-eks-cluster) on GitHub\.

   ```
   kind: Deployment
   ```

   `traffic-generator.yaml` makes `http` calls to the Kubernetes service `sample-app:4567`\. This allows the traffic generator to interact with the sample application on port `4567`\. `sample-app` resolves to the IP address of the `sample-app` pod\.

1. Apply `traffic-generator.yaml` to your cluster\.

   ```
   kubectl apply -f traffic-generator.yaml
   ```

1. Download the `sample-app.yaml` file to your computer\. You can also [view the file](https://github.com/aws-observability/aws-otel-community/blob/master/sample-configs/sample-app.yaml) on GitHub\.

   ```
   curl -O https://raw.githubusercontent.com/aws-observability/aws-otel-community/master/sample-configs/sample-app.yaml
   ```

1. In `sample-app.yaml`, replace the following with your own AWS Region:

   ```
   value: "<YOUR_AWS_REGION>"
   ```

   The following actions are defined by `sample-app.yaml`:
   + The Service resource configures `port: 4567` to allow HTTP requests for the traffic generator\.
   + The Deployment resource configures some environment variables:
     + The `LISTEN_ADDRESS` is configured to `0.0.0.0:4567` for HTTP requests from the traffic generator\.
     + The `OTEL_EXPORTER_OTLP_ENDPOINT` has a value of `http://my-collector-collector:4317`\. `my-collector-collector` is the name of the Kubernetes service that allows the sample application to interact with the ADOT Collector on port `4317`\. In the ADOT Collector configuration, the ADOT Collector receives metrics and traces from an endpoint: `0.0.0.0:4317`\. 

1. In `sample-app.yaml`, update the `value` for `OTEL_EXPORTER_OTLP_ENDPOINT` if it doesn't match your collector service name\.

   For example, X\-Ray requires replacing `http://my-collector-collector:4317` with `http://my-collector-xray-collector:4317`\.

1. Apply `sample-app.yaml` to your cluster\.

   ```
   kubectl apply -f sample-app.yaml
   ```