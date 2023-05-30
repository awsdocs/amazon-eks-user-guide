# Manage the AWS Distro for OpenTelemetry Operator<a name="adot-manage"></a>

The AWS Distro for OpenTelemetry \(ADOT\) Operator is available as an Amazon EKS add\-on\. After installing the ADOT Operator, you can configure the ADOT Collector to specify the deployment type and the service that will receive your application metric or trace data\. This topic describes how to manage the ADOT add\-on\.
+ [Install the AWS Distro for OpenTelemetry \(ADOT\) Operator](#adot-install)
+ [Update the AWS Distro for OpenTelemetry \(ADOT\) Operator](#adot-update)
+ [Remove the AWS Distro for OpenTelemetry \(ADOT\) Operator](#adot-remove)

To install the ADOT Collector, see [Deploy the AWS Distro for OpenTelemetry Collector](deploy-collector.md)\. Alternatively, with the advanced configuration feature of Amazon EKS add\-ons, you can install the ADOT Collector during add\-on creation or add\-on updates\. For more information, see [Deploy the AWS Distro for OpenTelemetry Collector using advanced configuration](deploy-collector-advanced-configuration.md)\.

## Install the AWS Distro for OpenTelemetry \(ADOT\) Operator<a name="adot-install"></a>

Installing the ADOT add\-on includes the ADOT Operator, which in turn deploys the ADOT Collector\. The ADOT Operator is a custom controller which introduces a new object type called the `OpenTelemetryCollector` through [CustomResourceDefinition \(CRD\)](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)\. When the ADOT Operator detects the presence of the `OpenTelemetryCollector` resource, then it installs the ADOT Collector\.

**Prerequisites**
+ You have met the [ADOT prerequisites](adot-reqts.md)\.
+ [kubectl is installed](install-kubectl.md)\.
+ Update your `kubeconfig` if necessary using the following command\.

  ```
  aws eks update-kubeconfig --name my-cluster --region region-code
  ```
+ [eksctl is installed](eksctl.md)\.
+ Version `2.11.3` or later or `1.27.93` or later of the AWS CLI installed and configured on your device or AWS CloudShell\. You can check your current version with `aws --version | cut -d / -f2 | cut -d ' ' -f1`\. Package managers such `yum`, `apt-get`, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI\. To install the latest version, see [ Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with `aws configure`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the AWS Command Line Interface User Guide\. The AWS CLI version installed in the AWS CloudShell may also be several versions behind the latest version\. To update it, see [ Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the AWS CloudShell User Guide\.
+ An existing Amazon EKS cluster\.
+ An existing Amazon EKS service IAM role\. If you don't have the role, you can follow [Create an IAM role](adot-iam.md) to create one\.

------
#### [ AWS Management Console ]

Install the ADOT Amazon EKS add\-on to your Amazon EKS cluster using the following steps:

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left pane, select **Clusters**, and then select the name of your cluster on the **Clusters** page\.

1. Choose the **Add\-ons** tab\.

1. Click **Add new** and select **AWS Distro for OpenTelemetry** from the drop\-down list\.

1. The default version will be selected in the **Version** drop\-down\. If deploying an ADOT Collector, make sure that the version is `v0.62.1-eksbuild.1` or greater\.

1. If a service account is already created in the cluster without an IAM role, select **Override existing configuration for this add\-on on the cluster**\.

1. \(Optional\) If deploying an ADOT Collector, provide the configuration values that match your use case for Collector deployment\. Do this under the **Optional configuration settings** drop\-down in the **Configuration values** field\. The **Add\-on configuration schema** provides the available options for your configuration values\.

1. Click **Add**\.

------
#### [ AWS CLI ]

1. Install the ADOT Amazon EKS add\-on to your Amazon EKS cluster\. Optionally, the `--configuration-values` flag can be added to deploy an ADOT Collector during add\-on installation\. You may also configure other available values with this flag\.

   ```
   aws eks create-addon --addon-name adot --cluster-name my-cluster --configuration-values my-configuration-values
   ```

   The `status` field value will be `CREATING` until complete\.

1. Verify that ADOT is installed and running\.

   ```
   aws eks describe-addon --addon-name adot --cluster-name my-cluster
   ```

   You'll see `"status": "ACTIVE"` when creation is complete\.

------

## Update the AWS Distro for OpenTelemetry \(ADOT\) Operator<a name="adot-update"></a>

Amazon EKS does not automatically update ADOT on your cluster\. You must initiate the update and then Amazon EKS updates the Amazon EKS add\-on for you\. 

**To update the ADOT Amazon EKS add\-on using the AWS CLI**

1. Check the current version of your ADOT add\-on\. Replace `my-cluster` with your cluster name\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name adot --query "addon.addonVersion" --output text
   ```

1. Determine the ADOT versions are available that are supported by your cluster's version\.

   ```
   aws eks describe-addon-versions --addon-name adot --kubernetes-version 1.23 \
       --query "addons[].addonVersions[].[addonVersion, compatibilities[].defaultVersion]" --output text
   ```

   The example output is as follows\.

   ```
   v0.58.0-eksbuild.1
   True
   v0.56.0-eksbuild.2
   False
   ```

   The version with `True` underneath is the default version deployed when the add\-on is created\. The version deployed when the add\-on is created might not be the latest available version\. In the previous output, the latest version is deployed when the add\-on is created\.

1. Update the ADOT version\. Replace `my-cluster` with the name of your cluster and `v0.58.0-eksbuild.1` with the desired version\. Optionally, the `--configuration-values` flag can be added to deploy an ADOT Collector during add\-on installation\. You may also configure other available values with this flag\.

   ```
   aws eks update-addon --cluster-name my-cluster --addon-name adot --addon-version v0.58.0-eksbuild.1 --resolve-conflicts PRESERVE --configuration-values my-configuration-values
   ```

   The *PRESERVE* option preserves any custom settings that you've set for the add\-on\. For more information about other options for this setting, see [update\-addon](https://docs.aws.amazon.com/cli/latest/reference/eks/update-addon.html) in the Amazon EKS Command Line Reference\. For more information about Amazon EKS add\-on configuration management, see [ Kubernetes field management](kubernetes-field-management.md)\.

## Remove the AWS Distro for OpenTelemetry \(ADOT\) Operator<a name="adot-remove"></a>
+ You must delete the ADOT Collector resource separately from the ADOT Collector\. In this command, specify the YAML file that you used to [deploy the ADOT Collector](deploy-collector.md):

  ```
  kubectl delete -f collector-config-(amp|cloudwatch|xray|advanced).yaml
  ```
+ You can remove the ADOT Operator through either the AWS CLI or `eksctl`\. If you remove the ADOT Operator, you must follow the [installation instructions](#adot-install) again to reinstall:

  CLI

  ```
  aws eks delete-addon --addon-name adot --cluster-name my-cluster
  ```

  `eksctl`

  ```
  eksctl delete addon --cluster my-cluster --name adot
  ```