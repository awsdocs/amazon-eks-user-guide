# Deploy the AWS Distro for OpenTelemetry \(ADOT\) Collector using EKS add\-ons Advanced Configuration<a name="deploy-collector-advanced-configuration"></a>

EKS add\-ons provides the ability to configure add\-ons during installation time\. With this functionality, an ADOT Collector can also be deployed during an installation, provided that add\-on version `v0.62.1-eksbuild.1` or higher is being used\.

For more information on Collector configuration, see the [Collector configuration](deploy-collector.md) page of the guide\. An example list of configurable values EKS add\-ons provides for ADOT for Collector deployment can be found [here](https://aws-otel.github.io/docs/getting-started/adot-eks-add-on/add-on-configuration-collector-deployment)\.

## Deploy the ADOT Collector using EKS add\-ons Advanced Configuration

An example of how to use EKS add\-ons to install ADOT, with a Collector deployment to Amazon Managed Prometheus using a pre\-existing service account for IRSA, can be seen in the command below

```
aws eks create-addon \
    --cluster-name <YOUR-EKS-CLUSTER-NAME> \
    --addon-name adot \
    --addon-version v0.62.1-eksbuild.1 \
    --configuration-values file://configuration-values.json
```

```json
// configuration-values.json
{
  "collector": {
    "serviceAccount": {
      "create": false,
      "name": "<YOUR-SERVICE-ACCOUNT-NAME>"
    },
    "amp": {
      "enabled": true,
      "remoteWriteEndpoint": "https://aps-workspaces.us-west-2.amazonaws.com/workspaces/ws-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/api/v1/remote_write"
    }
  }
}
```

Note that collector may take 2\-3 minutes to create and show up in your cluster\.
