# Amazon EKS add\-on support for ADOT Operator<a name="opentelemetry"></a>

Amazon EKS supports using the AWS Management Console, AWS CLI and Amazon EKS API to install and manage the [AWS Distro for OpenTelemetry \(ADOT\)](https://aws-otel.github.io/) Operator\. This enables a simplified experience for instrumenting your applications running on Amazon EKS to send metric and trace data to multiple monitoring service options like [Amazon CloudWatch](https://console.aws.amazon.com/cloudwatch), [https://console.aws.amazon.com/prometheus](https://console.aws.amazon.com/prometheus), and [X\-Ray](https://console.aws.amazon.com/xray)\. This topic describes how to get started using ADOT for applications running on your Amazon EKS cluster\.
+ [Prerequisites](adot-reqts.md)
+ [Creating an IAM role](adot-iam.md)
+ [Installing the add\-on](adot-manage.md#adot-install)
+ [Deploying the ADOT Collector](deploy-collector.md) for your preferred monitoring option
+ [Deploying the ADOT Collector using advanced configuration](deploy-collector-advanced-configuration.md)
+ [Deploying a sample application](sample-app.md) to generate OTLP data

Before installing ADOT, make sure that you have read and understand the [prerequisites and considerations](adot-reqts.md)\.