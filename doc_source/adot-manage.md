# Manage the AWS Distro for OpenTelemetry Operator<a name="adot-manage"></a>

The AWS Distro for OpenTelemetry \(ADOT\) Operator is available as an Amazon EKS add\-on\. After installing the ADOT Operator, you can configure the ADOT Collector to specify the deployment type and the service that will receive your application metric or trace data\. This topic describes how to manage the ADOT add\-on\.
+ [Install the AWS Distro for OpenTelemetry \(ADOT\) Operator](#adot-install)
+ [Update the AWS Distro for OpenTelemetry \(ADOT\) Operator](#adot-update)
+ [Remove the AWS Distro for OpenTelemetry \(ADOT\) Operator](#adot-remove)

To install the ADOT Collector, see [Deploy the AWS Distro for OpenTelemetry Collector](deploy-collector.md)\.

## Install the AWS Distro for OpenTelemetry \(ADOT\) Operator<a name="adot-install"></a>

Installing the ADOT add\-on includes the ADOT Operator, which in turn deploys the ADOT Collector\. The ADOT Operator is a custom controller which introduces a new object type called the `OpenTelemetryCollector` through [CustomResourceDefinition \(CRD\)](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)\. When the ADOT Operator detects the presence of the `OpenTelemetryCollector` resource, then it installs the ADOT Collector\.

**Prerequisites**
+ You have met the [ADOT prerequisites](adot-reqts.md)\.
+ [kubectl is installed](https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html)\.
+ Update your `kubeconfig` if necessary using the following command\.

  ```
  aws eks update-kubeconfig --name cluster_name --region AWS_REGION
  ```
+ [eksctl is installed](https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html)\.
+ [AWS CLI version 2 is installed](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)\.
+ An existing Amazon EKS cluster\.
+ An existing Amazon EKS service IAM role\. If you don't have the role, you can follow [Create an IAM role](adot-iam.md) to create one\.

------
#### [ AWS Management Console ]

Install the ADOT Amazon EKS add\-on to your Amazon EKS cluster using the following steps:

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left pane, select **Clusters**, and then select the name of your cluster on the **Clusters** page\.

1. Choose the **Add\-ons** tab\.

1. Click **Add new** and select **AWS Distro for OpenTelemetry** from the drop\-down list\.

1. The default version will be selected in the **Version** drop\-down\. Click **Override existing configuration for this add\-on on the cluster** if a service account is already created in the cluster without an IAM Role\.

1. Click **Add**\.

------
#### [ AWS CLI ]

1. Install the ADOT Amazon EKS add\-on to your Amazon EKS cluster using the command:

   ```
   aws eks create-addon --addon-name adot --cluster-name your-cluster
   ```

   The example output is as follows\.

   ```
   {
   
    "addon": {
    "addonName": "adot",
    "clusterName": "adot",
    "status": "CREATING",
    "addonVersion": "v0.45.0-eksbuild.1",
    "health": {
    "issues": []
    },
    "addonArn": "arn:aws:eks:region:111122223333:addon/adot/adot/c0bfbc67-ae88-d472-53e4-e88c79f7be7c",
    "createdAt": "2022-03-11T03:48:50.212000-08:00",
    "modifiedAt": "2022-03-11T03:48:50.234000-08 (tel:5023400008):00",
    "tags": {}
    }
   }
   ```

   The `status` field value will be `CREATING` until complete\.

1. Verify that ADOT is installed and running using the command:

   ```
   aws eks describe-addon --addon-name adot --cluster-name your-cluster
   ```

   The example output is as follows\.

   ```
   {
    "addon": {
    "addonName": "adot",
   "clusterName": "your-cluster",
    "status": "ACTIVE",
    "addonVersion": "v0.45.0-eksbuild.1",
    "health": {
    "issues": []
    },
    "addonArn": "arn:aws:eks:us-west-2:111122223333:addon/adot/adot/9ebe61e2-824d-14c2-408e-c491a7cc5fb8",
    "createdAt": "2021-10-27T15:00:41.536000-07:00",
    "modifiedAt": "2021-10-27T15:01:24.104000-07:00",
    "tags": {}
       }
   }
   ```

   The `status` value is now `ACTIVE` as creation is complete\.

------

## Update the AWS Distro for OpenTelemetry \(ADOT\) Operator<a name="adot-update"></a>

Amazon EKS does not automatically update ADOT on your cluster\. You must initiate the update and then Amazon EKS updates the Amazon EKS add\-on for you\. 

**To update the ADOT Amazon EKS add\-on using the AWS CLI**

1. Check the current version of your ADOT add\-on\. Replace *my\-cluster* with your cluster name\.

   ```
   aws eks describe-addon \
       --cluster-name my-cluster \
       --addon-name adot \
       --query "addon.addonVersion" \
       --output text
   ```

   The example output is as follows\.

   ```
   1.7.0
   ```

1. Determine the ADOT versions are available that are supported by your cluster's version\.

   ```
   aws eks describe-addon-versions \
       --addon-name adot \
       --kubernetes-version 1.19 \
       --query "addons[].addonVersions[].[addonVersion, compatibilities[].defaultVersion]" \
       --output text
   ```

   The example output is as follows\.

   ```
   1.8.0
   True
   1.7.0
   False
   ```

   The version with `True` underneath is the default version deployed with new clusters\. Later versions can be returned and updated, if necessary\.

1. To update the ADOT version, use the following command and replace the `addon-version` value with the desired version\.

   ```
   aws eks update-addon \
       --cluster-name my-cluster \
       --addon-name adot \
       --addon-version 1.8.0 \
       --resolve-conflicts OVERWRITE
   ```

**Note**  
The `--resolve-conflicts OVERWRITE` option will resolve any conflicts with Amazon EKS add\-on settings by overwriting your settings\. Ensure that your settings don't require management\. Without this option, conflicts must be resolved manually\. hen updating For more information, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

## Remove the AWS Distro for OpenTelemetry \(ADOT\) Operator<a name="adot-remove"></a>
+  You must delete the ADOT Collector resource separately from the ADOT Collector\. In this command, specify the YAML file that you used to deploy the ADOT Collector:

  ```
  kubectl delete -f collector-config.yaml
  ```
+ You can remove the ADOT Operator through either the AWS CLI or `eksctl`\. If you remove the ADOT Operator, you must follow the [installation instructions](#adot-install) again to reinstall:

  CLI

  ```
  aws eks delete-addon --addon-name adot --cluster-name your-cluster
  ```

  `eksctl`

  ```
  eksctl delete addon --cluster your-cluster --name adot
  ```