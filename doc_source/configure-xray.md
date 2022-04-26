# Deploy the AWS Distro for OpenTelemetry \(ADOT\) Collector for X\-Ray<a name="configure-xray"></a>

You can deploy the AWS Distro for OpenTelemetry \(ADOT\) Collector to send traces to X\-Ray by applying a YAML configuration file\. We have included an example YAML file called `collector-config-xray.yaml`:

```
apiVersion: opentelemetry.io/v1alpha1
kind: OpenTelemetryCollector
metadata:
  name: my-collector
spec:
  mode: deployment # This configuration is omittable.
  serviceAccount: adot-collector
  config: |
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
    processors:

    exporters:
      awsxray:
        region: <AWS_REGION>

    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: []
          exporters: [awsxray]
```

1. Apply the YAML file with the command:

   ```
   kubectl apply -f collector-config-xray.yaml
   ```

1. \(Optional\) Verify trace data is being sent to X\-Ray by opening the [X\-Ray console](https://console.aws.amazon.com/xray/home) and select `Traces` from the left menu\. Your trace data should be present\.