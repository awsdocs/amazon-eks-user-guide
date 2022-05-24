# Deploy the AWS Distro for OpenTelemetry Collector for Amazon Managed Service for Prometheus in deployment mode<a name="deploy-deployment"></a>

The following is an example YAML file with `deployment` as the `mode` value\. This is the default mode and deploys the ADOT Collector similarly to a standalone application\. This configuration receives OTLP metrics from the sample application and Amazon Managed Service for Prometheus metrics scraped from pods on the cluster\. You can change the `mode` to Daemonset, StatefulSet, and Sidecar depending on your deployment strategy\. For a `daemonset` deployment, see [the github page](https://aws-otel.github.io/docs/getting-started/adot-eks-add-on/config-advanced) or [click here](https://github.com/aws-observability/aws-otel-community/blob/master/sample-configs/collector-config-advanced.yaml) to download the daemonset example\. 

1. Copy the following text to a YAML file\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/deploy-deployment.html)

1. After you configured the YAML file, apply it to your cluster to deploy the ADOT Collector:

   ```
   kubectl apply -f deployment.yaml 
   ```