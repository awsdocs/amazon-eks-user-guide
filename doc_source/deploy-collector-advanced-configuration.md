# Deploy the AWS Distro for OpenTelemetry Collector using advanced configuration<a name="deploy-collector-advanced-configuration"></a>

Amazon EKS add\-ons provides the ability to configure add\-ons during installation time\. With this functionality, an ADOT Collector can also be deployed during an installation, provided that add\-on version `v0.62.1-eksbuild.1` or higher is being used\.

For an example list of configurable values Amazon EKS add\-ons provides for ADOT for Collector deployment, see [EKS add\-ons Advanced Configuration for ADOT: Collector Deployment](https://aws-otel.github.io/docs/getting-started/adot-eks-add-on/add-on-configuration-collector-deployment)\.

An example of how to use Amazon EKS add\-ons to install ADOT with a Collector deployment to Amazon Managed [https://prometheus.io/](https://prometheus.io/) can be seen in the steps that follow\. Make sure that you have satisfied the prerequisites and completed the procedure in [Install the AWS Distro for OpenTelemetry \(ADOT\) Operator](adot-manage.md#adot-install)\. 

1. Create `configuration-values.json` with the following contents\. Replace *`example values`* with your own\.

   ```
   {
     "collector": {
       "serviceAccount": {
         "create": false,
         "name": "your-irsa-account-name"
       },
       "amp": {
         "enabled": true,
         "remoteWriteEndpoint": "https://aps-workspaces.region-code.amazonaws.com/workspaces/ws-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/api/v1/remote_write"
       }
     }
   }
   ```

1. Run the following command\. Replace *`example values`* with your own\.

   ```
   aws eks create-addon \
       --cluster-name my-cluster \
       --addon-name adot \
       --addon-version add-on-version \
       --configuration-values file://configuration-values.json
   ```

Note that the collector may take 2 to 3 minutes to create and show up in your cluster\.