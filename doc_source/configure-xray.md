# Deploy the AWS Distro for OpenTelemetry \(ADOT\) Collector for X\-Ray<a name="configure-xray"></a>

You can deploy the AWS Distro for OpenTelemetry \(ADOT\) Collector to send traces to X\-Ray by applying a YAML configuration file\. This procedure downloads an example YAML file that you can apply to your cluster\.

1. Download the `collector-config-xray.yaml` file to your computer\. You can also [view the file](https://github.com/aws-observability/aws-otel-community/blob/master/sample-configs/operator/collector-config-xray.yaml) on GitHub\.

   ```
   curl -o collector-config-xray.yaml https://raw.githubusercontent.com/aws-observability/aws-otel-community/master/sample-configs/operator/collector-config-xray.yaml
   ```

1. In `collector-config-xray.yaml`, replace the following with your own values:
   + `mode: deployment`
   + `serviceAccount: adot-collector`
   + `region: "<YOUR_AWS_REGION>"`

1. Apply the YAML file to your cluster to deploy the ADOT Collector:

   ```
   kubectl apply -f collector-config-xray.yaml 
   ```

1. 

   ```
   apiVersion: opentelemetry.io/v1alpha1
   kind: OpenTelemetryCollector
   metadata:
     name: my-collector-xray
   spec:
     mode: deployment 
     serviceAccount: adot-collector
     config: |
       receivers:
         otlp:
           protocols:
             grpc:
               endpoint: 0.0.0.0:4317
             http:
               endpoint: 0.0.0.0:4318
       processors:
       exporters:
         awsxray:
           region: region-code
       service:
         pipelines:
           traces:
             receivers: [otlp]
             processors: []
             exporters: [awsxray]
   ```

1. \(Optional\) Verify trace data is being sent to X\-Ray by opening the [X\-Ray console](https://console.aws.amazon.com/xray/home) and select `Traces` from the left menu\. Your trace data should be present\.