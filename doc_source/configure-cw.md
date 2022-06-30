# Deploy the AWS Distro for OpenTelemetry Collector for CloudWatch<a name="configure-cw"></a>

The AWS Distro for OpenTelemetry \(ADOT\) Collector can be deployed to receive OTLP metrics for export to Amazon CloudWatch\. This procedure downloads an example YAML file that you can apply to your cluster\.

1. Download the `collector-config-cloudwatch.yaml` file to your computer\. You can also [view the file](https://github.com/aws-observability/aws-otel-community/blob/master/sample-configs/operator/collector-config-cloudwatch.yaml) on GitHub\.

   ```
   curl -o collector-config-cloudwatch.yaml https://raw.githubusercontent.com/aws-observability/aws-otel-community/master/sample-configs/operator/collector-config-cloudwatch.yaml
   ```

1. In `collector-config-cloudwatch.yaml`, replace the following with your own values:
   + `mode: deployment`
   + `serviceAccount: adot-collector`
   + `value: <YOUR_EKS_CLUSTER_NAME>`
   + `region: "<YOUR_AWS_REGION>"`
   + `name: adot-collector`

1. Apply the YAML file to your cluster to deploy the ADOT Collector:

   ```
   kubectl apply -f collector-config-cloudwatch.yaml 
   ```

1. \(Optional\) Verify the metrics data is being sent to Amazon CloudWatch by opening the [Amazon CloudWatch console](https://console.aws.amazon.com/cloudwatch/home) and open the **Metrics** menu on the left\. Select **All metrics** and click the **AOCDockerDemo/AOCDockerDemoService** box under **custom namespaces**\. You can view any metrics data by selecting any grouping\.