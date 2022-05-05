# Deploy the AWS Distro for OpenTelemetry \(ADOT\) Collector for X\-Ray<a name="configure-xray"></a>

You can deploy the AWS Distro for OpenTelemetry \(ADOT\) Collector to send traces to X\-Ray by applying a YAML configuration file\. We have included an example YAML file called `collector-config-xray.yaml`:


|  | 
| --- |
| <pre><br />apiVersion: opentelemetry.io/v1alpha1<br />kind: OpenTelemetryCollector<br />metadata:<br />  name: my-collector-xray<br />spec:<br />  mode: deployment <br />  serviceAccount: adot-demo<br />  config: |<br />    receivers:<br />      otlp:<br />        protocols:<br />          grpc:<br />            endpoint: 0.0.0.0:4317<br />          http:<br />            endpoint: 0.0.0.0:4318<br />    processors:<br />    exporters:<br />      awsxray:<br />        region: <AWS_REGION><br />    service:<br />      pipelines:<br />        traces:<br />          receivers: [otlp]<br />          processors: []<br />          exporters: [awsxray]<br /></pre>  | 

1. Apply the YAML file using the command:

   ```
   kubectl apply -f collector-config-xray.yaml
   ```

1. \(Optional\) Verify trace data is being sent to X\-Ray by opening the [X\-Ray console](https://console.aws.amazon.com/xray/home) and select `Traces` from the left menu\. Your trace data should be present\.