# Amazon EKS add\-on support for ADOT Operator<a name="opentelemetry"></a>

Amazon EKS supports using the AWS Management Console, AWS CLI and Amazon EKS API to install and manage the [AWS; Distro for OpenTelemetry \(ADOT\)](https://aws-otel.github.io/) Operator\. This enables a simplified experience for instrumenting your applications running on Amazon EKS to send metrics and traces to multiple monitoring services like [Amazon CloudWatch](https://console.aws.amazon.com/cloudwatch), [Prometheus](https://console.aws.amazon.com/prometheus);, and [X\-Ray](https://console.aws.amazon.com/xray)\. This topic describes how to get started using ADOT for applications running on your Amazon EKS cluster, including:
+ [Prerequisites](adot-reqts.md)
+ [Creating an IAM role](adot-iam.md)
+ [Installing the add\-on](adot-manage.md#adot-install)
+ [Deploying the ADOT Collector](deploy-collector.md) for your preferred service
+ [Deploying a sample application](sample-app.md) to generate OTLP data

## ADOT considerations<a name="adot-considerations"></a>

Before you use ADOT, review the following considerations and prerequisites:
+ The ADOT Operator does not yet support ARM64 architecture\.
+ Connected clusters cannot use this add\-on\.