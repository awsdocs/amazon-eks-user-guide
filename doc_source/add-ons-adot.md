# AWS Distro for OpenTelemetry<a name="add-ons-adot"></a>

ThAWS Distro for OpenTelemetry Amazon EKS add\-on is a secure, production\-ready, AWS supported distribution of the OpenTelemetry project\. For more information, see [AWS Distro for OpenTelemetry](https://aws-otel.github.io/) on GitHub\.

The Amazon EKS add\-on name is `adot`\.

## Required IAM permissions<a name="add-ons-adot-iam-permissions"></a>

This add\-on only requires IAM permissions if you’re using one of the preconfigured custom resources that can be opted into through advanced configuration\.

## Additional information<a name="add-ons-adot-information"></a>

For more information, see [Getting Started with AWS Distro for OpenTelemetry using EKS Add\-Ons](https://aws-otel.github.io/docs/getting-started/adot-eks-add-on) in the AWS Distro for OpenTelemetry documentation\.

ADOT requires that `cert-manager` is deployed on the cluster as a prerequisite, otherwise this add\-on won't work if deployed directly using the [Amazon EKS Terraform](https://registry.terraform.io/modules/terraform-aws-modules/eks/aws/latest) `cluster_addons` property\. For more requirements, see [Requirements for Getting Started with AWS Distro for OpenTelemetry using EKS Add\-Ons](https://aws-otel.github.io/docs/getting-started/adot-eks-add-on/requirements) in the AWS Distro for OpenTelemetry documentation\.