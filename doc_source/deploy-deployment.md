# Deploy the AWS Distro for OpenTelemetry Collector for Amazon Managed Service for Prometheus in deployment mode<a name="deploy-deployment"></a>

The following procedure uses an example YAML file with `deployment` as the `mode` value\. This is the default mode and deploys the ADOT Collector similarly to a standalone application\. This configuration receives OTLP metrics from the sample application and Amazon Managed Service for Prometheus metrics scraped from Pods on the cluster\. You can change the `mode` to `Daemonset`, `StatefulSet`, and `Sidecar` depending on your deployment strategy\. For a `Daemonset` deployment, see [Advanced Collector Configuration for Amazon Managed Prometheus](https://aws-otel.github.io/docs/getting-started/adot-eks-add-on/config-advanced) in the ADOT documentation or [click here](https://github.com/aws-observability/aws-otel-community/blob/master/sample-configs/operator/collector-config-advanced.yaml) to download the DaemonSet example\.

Make sure that you have satisfied the prerequisites and completed the procedure in [Install the AWS Distro for OpenTelemetry \(ADOT\) Operator](adot-manage.md#adot-install)\. 

1. Download the `collector-config-amp.yaml` file to your computer\. You can also [view the file](https://github.com/aws-observability/aws-otel-community/blob/master/sample-configs/operator/collector-config-amp.yaml) on GitHub\.

   ```
   curl -O https://raw.githubusercontent.com/aws-observability/aws-otel-community/master/sample-configs/operator/collector-config-amp.yaml
   ```

1. In `collector-config-amp.yaml`, replace the following with your own values:
   + `mode: deployment` \(for more information, see [Deploy the ADOT Collector](https://aws-otel.github.io/docs/getting-started/adot-eks-add-on/installation#deploy-the-adot-collector) on GitHub\)
   + `serviceAccount: adot-collector`
   + `endpoint: "<YOUR_REMOTE_WRITE_ENDPOINT>"`
   + `region: "<YOUR_AWS_REGION>"`
   + `name: adot-collector`

1. Apply the YAML file to your cluster to deploy the ADOT Collector:

   ```
   kubectl apply -f collector-config-amp.yaml
   ```