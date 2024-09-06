# Additional Amazon EKS add\-ons from independent software vendors<a name="workloads-add-ons-available-vendors"></a>

In addition to the previous list of Amazon EKS add\-ons, you can also add a wide selection of operational software Amazon EKS add\-ons from independent software vendors\. Choose an add\-on to learn more about it and its installation requirements\.

[![AWS Videos](http://img.youtube.com/vi/https://www.youtube.com/embed/IIPj119mspc/0.jpg)](http://www.youtube.com/watch?v=https://www.youtube.com/embed/IIPj119mspc)

## Accuknox<a name="add-on-accuknox"></a>

The add\-on name is `accuknox_kubearmor` and the namespace is `kubearmor`\. Accuknox publishes the add\-on\.

For information about the add\-on, see [Getting Started with KubeArmor](https://docs.kubearmor.io/kubearmor/quick-links/deployment_guide) in the KubeArmor documentation\.

### Service account name<a name="add-on-accuknox-service-account-name"></a>

A service account isn't used with this add\-on\.

### AWS managed IAM policy<a name="add-on-accuknox-managed-policy"></a>

A managed policy isn't used with this add\-on\.

### Custom IAM permissions<a name="add-on-accuknox-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## Akuity<a name="add-on-akuity"></a>

The add\-on name is `akuity_agent` and the namespace is `akuity`\. Akuity publishes the add\-on\.

For information about how the add\-on, see [Installing the Akuity Agent on Amazon EKS with the Akuity EKS add\-on](https://docs.akuity.io/tutorials/eks-addon-agent-install/) in the Akuity Platform documentation\.

### Service account name<a name="add-on-akuity-service-account-name"></a>

A service account isn't used with this add\-on\.

### AWS managed IAM policy<a name="add-on-akuity-managed-policy"></a>

A managed policy isn't used with this add\-on\.

### Custom IAM permissions<a name="add-on-akuity-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## Calyptia<a name="add-on-calyptia"></a>

The add\-on name is `calyptia_fluent-bit` and the namespace is `calytia-fluentbit`\. Calyptia publishes the add\-on\.

For information about the add\-on, see [Getting Started with Calyptia Core Agent](https://docs.akuity.io/tutorials/eks-addon-agent-install/) on the Calyptia documentation website\.

### Service account name<a name="add-on-calyptia-service-account-name"></a>

The service account name is `clyptia-fluentbit`\.

### AWS managed IAM policy<a name="add-on-calyptia-managed-policy"></a>

This add\-on uses the `AWSMarketplaceMeteringRegisterUsage` managed policy\. For more information, see [AWSMarketplaceMeteringRegisterUsage](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AWSMarketplaceMeteringRegisterUsage.html) in the AWS Managed Policy Reference Guide\.

### Command to create required IAM role<a name="add-on-calyptia-custom-permissions"></a>

The following command requires that you have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\. Replace `my-cluster` with the name of your cluster and `my-calyptia-role` with the name for your role\. This command requires that you have [https://eksctl.io](https://eksctl.io) installed on your device\. If you need to use a different tool to create the role and annotate the Kubernetes service account, see [Assign IAM roles to Kubernetes service accounts](associate-service-account-role.md)\.

```
eksctl create iamserviceaccount --name service-account-name  --namespace calyptia-fluentbit --cluster my-cluster --role-name my-calyptia-role \
    --role-only --attach-policy-arn arn:aws:iam::aws:policy/AWSMarketplaceMeteringRegisterUsage --approve
```

## Cisco Observability Collector<a name="add-on-cisco-collector"></a>

The add\-on name is `cisco_cisco-cloud-observability-collectors` and the namespace is `appdynamics`\. Cisco pubishes the add\-on\.

For information about the add\-on, see [Use the Cisco Cloud Observability AWS Marketplace Add\-Ons](https://docs.appdynamics.com/observability/cisco-cloud-observability/en/kubernetes-and-app-service-monitoring/install-kubernetes-and-app-service-monitoring-with-amazon-elastic-kubernetes-service/use-the-cisco-cloud-observability-aws-marketplace-add-ons) in the Cisco AppDynamics documentation\.

### Service account name<a name="add-on-cisco-collector-service-account-name"></a>

A service account isn't used with this add\-on\.

### AWS managed IAM policy<a name="add-on-cisco-collector-managed-policy"></a>

A managed policy isn't used with this add\-on\.

### Custom IAM permissions<a name="add-on-cisco-collector-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## Cisco Observability Operator<a name="add-on-cisco-operator"></a>

The add\-on name is `cisco_cisco-cloud-observability-operators` and the namespace is `appdynamics`\. Cisco publishes the add\-on\.

For information about the add\-on, see [Use the Cisco Cloud Observability AWS Marketplace Add\-Ons](https://docs.appdynamics.com/observability/cisco-cloud-observability/en/kubernetes-and-app-service-monitoring/install-kubernetes-and-app-service-monitoring-with-amazon-elastic-kubernetes-service/use-the-cisco-cloud-observability-aws-marketplace-add-ons) in the Cisco AppDynamics documentation\.

### Service account name<a name="add-on-cisco-operator-service-account-name"></a>

A service account isn't used with this add\-on\.

### AWS managed IAM policy<a name="add-on-cisco-operator-managed-policy"></a>

A managed policy isn't used with this add\-on\.

### Custom IAM permissions<a name="add-on-cisco-operator-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## CLOUDSOFT<a name="add-on-cloudsoft"></a>

The add\-on name is `cloudsoft_cloudsoft-amp` and the namespace is `cloudsoft-amp`\. CLOUDSOFT publishes the add\-on\.

For information about the add\-on, see [Amazon EKS ADDON](https://docs.cloudsoft.io/operations/configuration/aws-eks-addon.html) in the CLOUDSOFT documentation\.

### Service account name<a name="add-on-cloudsoft-service-account-name"></a>

A service account isn't used with this add\-on\.

### AWS managed IAM policy<a name="add-on-cloudsoft-managed-policy"></a>

A managed policy isn't used with this add\-on\.

### Custom IAM permissions<a name="add-on-cloudsoft-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## Cribl<a name="add-on-cribl"></a>

The add\-on name is `cribl_cribledge` and the namespace is `cribledge`\. Cribl publishes the add\-on\.

For information about the add\-on, see [Installing the Cribl Amazon EKS Add\-on for Edge](https://docs.cribl.io/edge/usecase-edge-aws-eks/) in the Cribl documentation

### Service account name<a name="add-on-cribl-service-account-name"></a>

A service account isn't used with this add\-on\.

### AWS managed IAM policy<a name="add-on-cribl-managed-policy"></a>

A managed policy isn't used with this add\-on\.

### Custom IAM permissions<a name="add-on-cribl-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## Dynatrace<a name="add-on-dynatrace"></a>

The add\-on name is `dynatrace_dynatrace-operator` and the namespace is `dynatrace`\. Dynatrace publishes the add\-on\.

For information about the add\-on, see [Kubernetes monitoring](https://www.dynatrace.com/technologies/kubernetes-monitoring/) in the dynatrace documentation\.

### Service account name<a name="add-on-dynatrace-service-account-name"></a>

A service account isn't used with this add\-on\.

### AWS managed IAM policy<a name="add-on-dynatrace-managed-policy"></a>

A managed policy isn't used with this add\-on\.

### Custom IAM permissions<a name="add-on-dynatrace-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## Datree<a name="add-on-datree-pro"></a>

The add\-on name is `datree_engine-pro` and the namespace is `datree`\. Datree publishes the add\-on\.

For information about the add\-on, see [Amazon EKS\-intergration](https://hub.datree.io/integrations/eks-integration) in the Datree documentation\.

### Service account name<a name="add-on-datree-pro-service-account-name"></a>

The service account name is datree\-webhook\-server\-awsmp\.

### AWS managed IAM policy<a name="add-on-datree-pro-managed-policy"></a>

The managed policy is AWSLicenseManagerConsumptionPolicy\. For more information, see [AWSLicenseManagerConsumptionPolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AWSLicenseManagerConsumptionPolicy.html) in the AWS Managed Policy Reference Guide\.\.

### Command to create required IAM role<a name="add-on-datree-pro-iam-command"></a>

The following command requires that you have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\. Replace `my-cluster` with the name of your cluster and `my-datree-role` with the name for your role\. This command requires that you have [https://eksctl.io](https://eksctl.io) installed on your device\. If you need to use a different tool to create the role and annotate the Kubernetes service account, see [Assign IAM roles to Kubernetes service accounts](associate-service-account-role.md)\.

```
eksctl create iamserviceaccount --name datree-webhook-server-awsmp --namespace datree --cluster my-cluster --role-name my-datree-role \
    --role-only --attach-policy-arn arn:aws:iam::aws:policy/service-role/AWSLicenseManagerConsumptionPolicy --approve
```

### Custom permissions<a name="add-on-datree-pro-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## Datadog<a name="add-on-datadog"></a>

The add\-on name is `datadog_operator` and the namespace is `datadog-agent`\. Datadog publishes the add\-on\.

For information about the add\-on, see [Installing the Datadog Agent on Amazon EKS with the Datadog Operator Add\-on](https://docs.datadoghq.com/containers/guide/operator-eks-addon/?tab=console) in the Datadog documentation\.

### Service account name<a name="add-on-datadog-service-account-name"></a>

A service account isn't used with this add\-on\.

### AWS managed IAM policy<a name="add-on-datadog-managed-policy"></a>

A managed policy isn't used with this add\-on\.

### Custom IAM permissions<a name="add-on-datadog-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## Groundcover<a name="add-on-groundcover"></a>

The add\-on name is `groundcover_agent` and the namespace is `groundcover`\. groundcover publishes the add\-on\.

For information about the add\-on, see [Installing the groundcover Amazon EKS Add\-on](https://docs.groundcover.com/docs/~/changes/VhDDAl1gy1VIO3RIcgxD/configuration/customization-guide/customize-deployment/eks-add-on) in the groundcover documentation\.

### Service account name<a name="add-on-groundcover-service-account-name"></a>

A service account isn't used with this add\-on\.

### AWS managed IAM policy<a name="add-on-groundcover-managed-policy"></a>

A managed policy isn't used with this add\-on\.

### Custom IAM permissions<a name="add-on-groundcover-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## Grafana Labs<a name="add-on-grafana"></a>

The add\-on name is `grafana-labs_kubernetes-monitoring` and the namespace is `monitoring`\. Grafana Labs publishes the add\-on\.

For information about the add\-on, see [Configure Kubernetes Monitoring as an Add\-on with Amazon EKS](https://grafana.com/docs/grafana-cloud/monitor-infrastructure/kubernetes-monitoring/configuration/config-aws-eks/) in the Grafana Labs documentation\.

### Service account name<a name="add-on-grafana-service-account-name"></a>

A service account isn't used with this add\-on\.

### AWS managed IAM policy<a name="add-on-grafana-managed-policy"></a>

A managed policy isn't used with this add\-on\.

### Custom IAM permissions<a name="add-on-grafana-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## Guance<a name="add-on-guance"></a>
+ **Publisher** – GUANCE
+ **Name** – `guance_datakit`
+ **Namespace** – `datakit`
+ **Service account name** – A service account isn't used with this add\-on\.
+ **AWS managed IAM policy** – A managed policy isn't used with this add\-on\.
+ **Custom IAM permissions** – Custom permissions aren't used with this add\-on\.
+ **Setup and usage instructions** – See [Using Amazon EKS add\-on](https://docs.guance.com/en/datakit/datakit-eks-deploy/#add-on-install) in the Guance documentation\.

## HA Proxy<a name="add-on-ha-proxy"></a>

The name is `haproxy-technologies_kubernetes-ingress-ee` and the namespace is `haproxy-controller`\. HA Proxy publishes the add\-on\.

For information about the add\-on, see [Amazon EKS\-intergration](https://hub.datree.io/integrations/eks-integration) in the Datree documentation\.

### Service account name<a name="add-on-ha-proxy-service-account-name"></a>

The service account name is `customer defined`\.

### AWS managed IAM policy<a name="add-on-ha-proxy-managed-policy"></a>

The managed policy is AWSLicenseManagerConsumptionPolicy\. For more information, see [AWSLicenseManagerConsumptionPolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AWSLicenseManagerConsumptionPolicy.html) in the AWS Managed Policy Reference Guide\.\.

### Command to create required IAM role<a name="add-on-ha-proxy-iam-command"></a>

The following command requires that you have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\. Replace `my-cluster` with the name of your cluster and `my-haproxy-role` with the name for your role\. This command requires that you have [https://eksctl.io](https://eksctl.io) installed on your device\. If you need to use a different tool to create the role and annotate the Kubernetes service account, see [Assign IAM roles to Kubernetes service accounts](associate-service-account-role.md)\.

```
eksctl create iamserviceaccount --name service-account-name  --namespace haproxy-controller --cluster my-cluster --role-name my-haproxy-role \
    --role-only --attach-policy-arn arn:aws:iam::aws:policy/service-role/AWSLicenseManagerConsumptionPolicy --approve
```

### Custom permissions<a name="add-on-ha-proxy-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## Kpow<a name="add-on-kpow"></a>

The add\-on name is `factorhouse_kpow` and the namespace is `factorhouse`\. Factorhouse publishes the add\-on\.

For information about the add\-on, see [AWS Marketplace LM](https://docs.kpow.io/installation/aws-marketplace-lm/) in the Kpow documentation\.

### Service account name<a name="add-on-kpow-service-account-name"></a>

The service account name is `kpow`\.

### AWS managed IAM policy<a name="add-on-kpow-managed-policy"></a>

The managed policy is AWSLicenseManagerConsumptionPolicy\. For more information, see [AWSLicenseManagerConsumptionPolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AWSLicenseManagerConsumptionPolicy.html) in the AWS Managed Policy Reference Guide\.\.

### Command to create required IAM role<a name="add-on-kpow-iam-command"></a>

The following command requires that you have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\. Replace `my-cluster` with the name of your cluster and `my-kpow-role` with the name for your role\. This command requires that you have [https://eksctl.io](https://eksctl.io) installed on your device\. If you need to use a different tool to create the role and annotate the Kubernetes service account, see [Assign IAM roles to Kubernetes service accounts](associate-service-account-role.md)\.

```
eksctl create iamserviceaccount --name kpow --namespace factorhouse --cluster my-cluster --role-name my-kpow-role \
    --role-only --attach-policy-arn arn:aws:iam::aws:policy/service-role/AWSLicenseManagerConsumptionPolicy --approve
```

### Custom permissions<a name="add-on-kpow-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## Kubecost<a name="add-on-kubecost"></a>

The add\-on name is `kubecost_kubecost` and the namespace is `kubecost`\. Kubecost publishes the add\-on\.

For information about the add\-on, see[AWS Cloud Billing Integration](https://docs.kubecost.com/install-and-configure/install/cloud-integration/aws-cloud-integrations) in the Kubecost documentation\.

If your cluster is version `1.23` or later, you must have the [Store Kubernetes volumes with Amazon EBS](ebs-csi.md) installed on your cluster\. otherwise you will receive an error\.

### Service account name<a name="add-on-kubecost-service-account-name"></a>

A service account isn't used with this add\-on\.

### AWS managed IAM policy<a name="add-on-kubecost-managed-policy"></a>

A managed policy isn't used with this add\-on\.

### Custom IAM permissions<a name="add-on-kubecost-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## Kasten<a name="add-on-kasten"></a>

 The add\-on name is `kasten_k10` and the namespace is `kasten-io`\. Kasten by Veeam publishes the add\-on\.

For information about the add\-on, see [Installing K10 on AWS using Amazon EKS Add\-on](https://docs.kasten.io/latest/install/aws-eks-addon/aws-eks-addon.html) in the Kasten documentation\.

 If your Amazon EKS cluster is version Kubernetes `1.23` or later, you must have the Amazon EBS CSI driver installed on your cluster with a default `StorageClass`\.

### Service account name<a name="add-on-kasten-service-account-name"></a>

The service account name is `k10-k10`\.

### AWS managed IAM policy<a name="add-on-kasten-managed-policy"></a>

The managed policy is AWSLicenseManagerConsumptionPolicy\. For more information, see [AWSLicenseManagerConsumptionPolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AWSLicenseManagerConsumptionPolicy.html) in the AWS Managed Policy Reference Guide\.\.

### Command to create required IAM role<a name="add-on-kasten-iam-command"></a>

The following command requires that you have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\. Replace `my-cluster` with the name of your cluster and `my-kasten-role` with the name for your role\. This command requires that you have [https://eksctl.io](https://eksctl.io) installed on your device\. If you need to use a different tool to create the role and annotate the Kubernetes service account, see [Assign IAM roles to Kubernetes service accounts](associate-service-account-role.md)\.

```
eksctl create iamserviceaccount --name k10-k10 --namespace kasten-io --cluster my-cluster --role-name my-kasten-role \
    --role-only --attach-policy-arn arn:aws:iam::aws:policy/service-role/AWSLicenseManagerConsumptionPolicy --approve
```

### Custom permissions<a name="add-on-kasten-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## Kong<a name="add-on-kong"></a>

The add\-on name is `kong_konnect-ri` and the namespace is `kong`\. Kong publishes the add\-on\.

For information about the add\-on, see [Installing the Kong Gateway EKS Add\-on](https://kong.github.io/aws-marketplace-addon-kong-gateway/) in the Kong documentation\.

If your cluster is version `1.23` or later, you must have the [Store Kubernetes volumes with Amazon EBS](ebs-csi.md) installed on your cluster\. otherwise you will receive an error\.

### Service account name<a name="add-on-kong-service-account-name"></a>

A service account isn't used with this add\-on\.

### AWS managed IAM policy<a name="add-on-kong-managed-policy"></a>

A managed policy isn't used with this add\-on\.

### Custom IAM permissions<a name="add-on-kong-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## LeakSignal<a name="add-on-leaksignal"></a>

The add\-on name is `leaksignal_leakagent` and the namespace is `leakagent`\. LeakSignal publishes the add\-on\.

For information about the add\-on, see [Install the LeakAgent add\-on](https://www.leaksignal.com/docs/LeakAgent/Deployment/AWS%20EKS%20Addon/) in the LeakSignal documentation

If your cluster is version `1.23` or later, you must have the [Store Kubernetes volumes with Amazon EBS](ebs-csi.md) installed on your cluster\. otherwise you will receive an error\.

### Service account name<a name="add-on-leaksignal-service-account-name"></a>

A service account isn't used with this add\-on\.

### AWS managed IAM policy<a name="add-on-leaksignal-managed-policy"></a>

A managed policy isn't used with this add\-on\.

### Custom IAM permissions<a name="add-on-leaksignal-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## NetApp<a name="add-on-netapp"></a>

The add\-on name is `netapp_trident-operator` and the namespace is `trident`\. NetApp publishes the add\-on\.

For information about the add\-on, see [Configure the Astra Trident EKS add\-on](https://docs.netapp.com/us-en/trident/trident-use/trident-aws-addon.html) in the NetApp documentation\.

### Service account name<a name="add-on-netapp-service-account-name"></a>

A service account isn't used with this add\-on\.

### AWS managed IAM policy<a name="add-on-netapp-managed-policy"></a>

A managed policy isn't used with this add\-on\.

### Custom IAM permissions<a name="add-on-netapp-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## New Relic<a name="add-on-new-relic"></a>

The add\-on name is `new-relic_kubernetes-operator` and the namespace is `newrelic`\. New Relic publishes the add\-on\.

For information about the add\-on, see[Installing the New Relic Add\-on for EKS](https://docs.newrelic.com/docs/infrastructure/amazon-integrations/connect/eks-add-on) in the New Relic documentation\.

### Service account name<a name="add-on-new-relic-service-account-name"></a>

A service account isn't used with this add\-on\.

### AWS managed IAM policy<a name="add-on-new-relic-managed-policy"></a>

A managed policy isn't used with this add\-on\.

### Custom IAM permissions<a name="add-on-new-relic-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## Rafay<a name="add-on-rafay"></a>

The add\-on name is `rafay-systems_rafay-operator`and the namespace is `rafay-system`\. Rafay publishes the add\-on\.

For information about the add\-on, see [Installing the Rafay Amazon EKS Add\-on](https://docs.rafay.co/clusters/import/eksaddon/) in the Rafay documentation\.

### Service account name<a name="add-on-rafay-service-account-name"></a>

A service account isn't used with this add\-on\.

### AWS managed IAM policy<a name="add-on-rafay-managed-policy"></a>

A managed policy isn't used with this add\-on\.

### Custom IAM permissions<a name="add-on-rafay-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## Rad Security<a name="add-on-rad"></a>
+ **Publisher** – RAD SECURITY
+ **Name** – `rad-security_rad-security`
+ **Namespace** – `ksoc`
+ **Service account name** – A service account isn't used with this add\-on\.
+ **AWS managed IAM policy** – A managed policy isn't used with this add\-on\.
+ **Custom IAM permissions** – Custom permissions aren't used with this add\-on\.
+ **Setup and usage instructions** – See [Installing Rad Through The AWS Marketplace](https://docs.rad.security/docs/installing-ksoc-in-the-aws-marketplace) in the Rad Security documentation\.

## SolarWinds<a name="add-on-solarwinds"></a>
+ **Publisher** – SOLARWINDS
+ **Name** – `solarwinds_swo-k8s-collector-addon`
+ **Namespace** – `solarwinds`
+ **Service account name** – A service account isn't used with this add\-on\.
+ **AWS managed IAM policy** – A managed policy isn't used with this add\-on\.
+ **Custom IAM permissions** – Custom permissions aren't used with this add\-on\.
+ **Setup and usage instructions** – See [Monitor an Amazon EKS cluster](https://documentation.solarwinds.com/en/success_center/observability/content/configure/configure-kubernetes.htm#MonitorAmazonEKS) in the SolarWinds documentation\.

## Solo<a name="add-on-solo"></a>

The add\-on name is `solo-io_istio-distro` and the namespace is `istio-system`\. Solo publishes the add\-on\.

For information about the add\-on, see [Installing Istio](https://docs.solo.io/gloo-mesh-enterprise/main/setup/install/eks_addon/) in the Solo\.io documentation\.\.

### Service account name<a name="add-on-solo-service-account-name"></a>

A service account isn't used with this add\-on\.

### AWS managed IAM policy<a name="add-on-solo-managed-policy"></a>

A managed policy isn't used with this add\-on\.

### Custom IAM permissions<a name="add-on-solo-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## Snyk<a name="add-on-snyk"></a>
+ **Publisher** – SNYK
+ **Name** – `snyk_runtime-sensor`
+ **Namespace** – `snyk_runtime-sensor`
+ **Service account name** – A service account isn't used with this add\-on\.
+ **AWS managed IAM policy** – A managed policy isn't used with this add\-on\.
+ **Custom IAM permissions** – Custom permissions aren't used with this add\-on\.
+ **Setup and usage instructions** – See [Snyk runtime sensor](https://docs.snyk.io/integrate-with-snyk/snyk-runtime-sensor) in the Snyk user docs\.

## Stormforge<a name="add-on-stormforge"></a>

The add\-on name is `stormforge_optimize-Live` and the namespace is `stormforge-system`\. Stormforge publishes the add\-on\.

For information about the add\-on, see [Installing the StormForge Agent](https://docs.stormforge.io/optimize-live/getting-started/install-v2/) in the StormForge documentation\.

### Service account name<a name="add-on-stormforge-service-account-name"></a>

A service account isn't used with this add\-on\.

### AWS managed IAM policy<a name="add-on-stormforge-managed-policy"></a>

A managed policy isn't used with this add\-on\.

### Custom IAM permissions<a name="add-on-stormforge-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## Splunk<a name="add-on-splunk"></a>

The add\-on name is `splunk_splunk-otel-collector-chart` and the namespace is `splunk-monitoring`\. Splunk publishes the add\-on\.

For information about the add\-on, see [Install the Splunk add\-on for Amazon EKS](https://docs.splunk.com/observability/en/gdi/opentelemetry/install-k8s-addon-eks.html) in the Splunk documentation\.

### Service account name<a name="add-on-splunk-service-account-name"></a>

A service account isn't used with this add\-on\.

### AWS managed IAM policy<a name="add-on-splunk-managed-policy"></a>

A managed policy isn't used with this add\-on\.

### Custom IAM permissions<a name="add-on-splunk-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## Teleport<a name="add-on-teleport"></a>

The add\-on name is `teleport_teleport` and the namespace is `teleport`\. Teleport publishes the add\-on\.

For information about the add\-on, see [How Teleport Works](https://goteleport.com/how-it-works/) in the Teleport documentation\.

### Service account name<a name="add-on-teleport-service-account-name"></a>

A service account isn't used with this add\-on\.

### AWS managed IAM policy<a name="add-on-teleport-managed-policy"></a>

A managed policy isn't used with this add\-on\.

### Custom IAM permissions<a name="add-on-teleport-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## Tetrate<a name="add-on-tetrate"></a>

The add\-on name is `tetrate-io_istio-distro` and the namespace is `istio-system`\. Tetrate Io publishes the add\-on\.

For information about the add\-on, see the [Tetrate Istio Distro](https://tetratelabs.io/) website\.

### Service account name<a name="add-on-tetrate-service-account-name"></a>

A service account isn't used with this add\-on\.

### AWS managed IAM policy<a name="add-on-tetrate-managed-policy"></a>

A managed policy isn't used with this add\-on\.

### Custom IAM permissions<a name="add-on-tetrate-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## Upbound Universal Crossplane<a name="add-on-upbound"></a>

The add\-on name is `upbound_universal-crossplane` and the namespace is `upbound-system`\. Upbound publishes the add\-on\.

For information about the add\-on, see [Upbound Universal Crossplane \(UXP\)](https://docs.upbound.io/uxp/) in the Upbound documentation\.

### Service account name<a name="add-on-upbound-service-account-name"></a>

A service account isn't used with this add\-on\.

### AWS managed IAM policy<a name="add-on-upbound-managed-policy"></a>

A managed policy isn't used with this add\-on\.

### Custom IAM permissions<a name="add-on-upbound-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.

## Upwind<a name="add-on-upwind"></a>

The add\-on name is `upwind` and the namespace is `upwind`\. Upwind publishes the add\-on\.

For information about the add\-on, see [Upwind documentation](https://docs.upwind.io/install-sensor/kubernetes/install?installation-method=amazon-eks-addon)\.

### Service account name<a name="add-on-upwind-service-account-name"></a>

A service account isn't used with this add\-on\.

### AWS managed IAM policy<a name="add-on-upwind-managed-policy"></a>

A managed policy isn't used with this add\-on\.

### Custom IAM permissions<a name="add-on-upwind-custom-permissions"></a>

Custom permissions aren't used with this add\-on\.