# Deploy the AWS Distro for OpenTelemetry Collector<a name="deploy-collector"></a>

Once the [AWS Distro for OpenTelemetry \(ADOT\) Operator is installed](adot-manage.md#adot-install) and running, you can deploy the ADOT Collector into your Amazon EKS cluster\. The ADOT Collector can be deployed in one of four modes: `Deployment`, `DaemonSet`, `StatefulSet`, and `Sidecar` and can be deployed for visibility by an individual service\. For more information on these modes, see the ADOT Collector [Deploy the ADOT Collector](https://aws-otel.github.io/docs/getting-started/adot-eks-add-on/installation#deploy-the-adot-collector) on GitHub\.

You can deploy the ADOT Collector by applying a YAML file to your cluster\. You should have already installed the [ADOT Operator](adot-manage.md#adot-install)\. You can [Create an IAM role](adot-iam.md) with your Amazon EKS service account using [IRSA](iam-roles-for-service-accounts.md)\. By doing this, your service account can provide AWS permissions to the containers you run in any pod that uses that service account\.

We provide ADOT Collector examples for the following services \(in deployment modes\):
+ [Prometheus](deploy-deployment.md)
+ [Amazon CloudWatch](configure-cw.md)
+ [X\-Ray](configure-xray.md)