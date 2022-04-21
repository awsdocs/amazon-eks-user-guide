# Deploy ADOT Collector for Amazon CloudWatch data<a name="configure-cw"></a>

The AWS Distro for OpenTelemetry \(ADOT\) Collector can be deployed to receive OTLP metrics for export to Amazon CloudWatch\. We have included an example YAML file that you can apply to your cluster for use with the [sample application](sample-app.md)\. For a more detailed example, see [the github page](https://aws-otel.github.io/docs/getting-started/adot-eks-add-on/config-advanced)\. Replace the `region` value with your own\.

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
      awsemf:
        region: <AWS_REGION>

    service:
      pipelines:
        metrics:
          receivers: [otlp]
          processors: []
          exporters: [awsemf]
```

1. Create a YAML file\. In this example, it is named `collector-config-cloudwatch.yaml`\.

1. Apply the YAML file with the command:

   ```
   kubectl apply -f collector-config-cloudwatch.yaml
   ```

1. \(Optional\) Verify the metrics data is being sent to Amazon CloudWatch by opening the [Amazon CloudWatch console](https://console.aws.amazon.com/cloudwatch/home) and open the **Metrics** menu on the left\. Select **All metrics** and click the **AOCDockerDemo/AOCDockerDemoService** box under **custom namespaces**\. You can view any metrics data by selecting any grouping\.