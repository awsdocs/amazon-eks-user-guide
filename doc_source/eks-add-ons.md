--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Amazon EKS add\-ons<a name="eks-add-ons"></a>

An add\-on is software that provides supporting operational capabilities to Kubernetes applications, but is not specific to the application\. This includes software like observability agents or Kubernetes drivers that allow the cluster to interact with underlying AWS resources for networking, compute, and storage\. Add\-on software is typically built and maintained by the Kubernetes community, cloud providers like AWS, or third\-party vendors\. Amazon EKS automatically installs self\-managed add\-ons such as the Amazon VPC CNI plugin for  Kubernetes, `kube-proxy`, and CoreDNS for every cluster\. You can change the default configuration of the add\-ons and update them when desired\.

Amazon EKS add\-ons provide installation and management of a curated set of add\-ons for Amazon EKS clusters\. All Amazon EKS add\-ons include the latest security patches, bug fixes, and are validated by AWS to work with Amazon EKS\. Amazon EKS add\-ons allow you to consistently ensure that your Amazon EKS clusters are secure and stable and reduce the amount of work that you need to do in order to install, configure, and update add\-ons\. If a self\-managed add\-on, such as `kube-proxy` is already running on your cluster and is available as an Amazon EKS add\-on, then you can install the `kube-proxy` Amazon EKS add\-on to start benefiting from the capabilities of Amazon EKS add\-ons\.
+ To configure add\-ons for the cluster your [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) must have IAM permissions to work with add\-ons\. For more information, see the actions with `Addon` in their name in [Actions defined by Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html#amazonelastickubernetesservice-actions-as-permissions)\.
+ Amazon EKS add\-ons run on the nodes that you provision or configure for your cluster\. Node types include Amazon EC2 instances and Fargate\.
+ If you create a cluster with the AWS Management Console, the Amazon EKS `kube-proxy`, Amazon VPC CNI plugin for  Kubernetes, and CoreDNS Amazon EKS add\-ons are automatically added to your cluster\. If you use `eksctl` to create your cluster with a `config` file, `eksctl` can also create the cluster with Amazon EKS add\-ons\. If you create your cluster using `eksctl` without a `config` file or with any other tool, the self\-managed `kube-proxy`, Amazon VPC CNI plugin for  Kubernetes, and CoreDNS add\-ons are installed, rather than the Amazon EKS add\-ons\. You can either manage them yourself or add the Amazon EKS add\-ons manually after cluster creation\.
+ The `eks:addon-cluster-admin`ClusterRoleBinding binds the `cluster-admin`ClusterRole to the `eks:addon-manager` Kubernetes identity\. The role has the necessary permissions for the `eks:addon-manager` identity to create Kubernetes namespaces and install add\-ons into namespaces\. If the `eks:addon\-cluster\-admin``ClusterRoleBinding` is removed, the Amazon EKS cluster will continue to function, however Amazon EKS is no longer able to manage any add\-ons\. All clusters starting with the following platform versions use the new `ClusterRoleBinding`\.

## Available Amazon EKS add\-ons from Amazon EKS<a name="workloads-add-ons-available-eks"></a>

Choose an add\-on to learn more about it and its installation requirements\.

### Amazon VPC CNI plugin for Kubernetes<a name="add-ons-vpc-cni"></a>
+  **Name** – `vpc-cni` 
+  **Description** – A [Kubernetes container network interface \(CNI\) plugin](https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/) that provides native VPC networking for your cluster\. The self\-managed or managed type of this add\-on is installed on each Amazon EC2 node, by default\.

  ```
  eksctl create iamserviceaccount --name aws-node --namespace kube-system --cluster my-cluster --role-name AmazonEKSVPCCNIRole \
      --role-only --attach-policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy --approve
  ```

### CoreDNS<a name="add-ons-coredns"></a>
+  **Name** – `coredns` 
+  **Required IAM permissions** – This add\-on doesn’t require any permissions\.
+  **Additional information** – To learn more about CoreDNS, see [Using CoreDNS for Service Discovery](https://kubernetes.io/docs/tasks/administer-cluster/coredns/) and [Customizing DNS Service](https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/) in the Kubernetes documentation\.

### `Kube-proxy`<a name="add-ons-kube-proxy"></a>
+  **Name** – `kube-proxy` 
+  **Description** – Maintains network rules on each Amazon EC2 node\. It enables network communication to your Pods\. The self\-managed or managed type of this add\-on is installed on each Amazon EC2 node in your cluster, by default\.
+  **Required IAM permissions** – This add\-on doesn’t require any permissions\.
+  **Additional information** – To learn more about `kube-proxy`, see [kube\-proxy](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/) in the Kubernetes documentation\.
+  **Update information** – Before updating your current version, consider the following requirements:
  +  `Kube-proxy` on an Amazon EKS cluster has the same [compatibility and skew policy as Kubernetes](https://kubernetes.io/releases/version-skew-policy/#kube-proxy)\.
  +  `Kube-proxy` must be the same minor version as `kubelet` on your Amazon EC2 nodes\.
  +  `Kube-proxy` can’t be later than the minor version of your cluster’s control plane\.
  + The `kube-proxy` version on your Amazon EC2 nodes can’t be more than two minor versions earlier than your control plane\. For example, if your control plane is running Kubernetes 1\.29, then the `kube-proxy` minor version can’t be earlier than 1\.27\.
  + If you recently updated your cluster to a new Kubernetes minor version, then update your Amazon EC2 nodes to the same minor version *before* updating `kube-proxy` to the same minor version as your nodes\.

### Amazon EBS CSI driver<a name="add-ons-aws-ebs-csi-driver"></a>
+  **Name** – `aws-ebs-csi-driver` 
+  **Description** – A Kubernetes Container Storage Interface \(CSI\) plugin that provides Amazon EBS storage for your cluster\.

  ```
  eksctl create iamserviceaccount \
      --name ebs-csi-controller-sa \
      --namespace kube-system \
      --cluster my-cluster \
      --role-name AmazonEKS_EBS_CSI_DriverRole \
      --role-only \
      --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy \
      --approve
  ```

### Amazon EFS CSI driver<a name="add-ons-aws-efs-csi-driver"></a>
+  **Name** – `aws-efs-csi-driver` 
+  **Description** – A Kubernetes Container Storage Interface \(CSI\) plugin that provides Amazon EFS storage for your cluster\.

  ```
  export cluster_name=my-cluster
  export role_name=AmazonEKS_EFS_CSI_DriverRole
  eksctl create iamserviceaccount \
      --name efs-csi-controller-sa \
      --namespace kube-system \
      --cluster $cluster_name \
      --role-name $role_name \
      --role-only \
      --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEFSCSIDriverPolicy \
      --approve
  TRUST_POLICY=$(aws iam get-role --role-name $role_name --query 'Role.AssumeRolePolicyDocument' | \
      sed -e 's/efs-csi-controller-sa/efs-csi-*/' -e 's/StringEquals/StringLike/')
  aws iam update-assume-role-policy --role-name $role_name --policy-document "$TRUST_POLICY"
  ```

### Mountpoint for Amazon S3 CSI Driver<a name="mountpoint-for-s3-add-on"></a>
+  **Name** – `aws-mountpoint-s3-csi-driver` 
+  **Description** – A Kubernetes Container Storage Interface \(CSI\) plugin that provides Amazon S3 storage for your cluster\.

  ```
  CLUSTER_NAME=my-cluster
  REGION=region-code
  ROLE_NAME=AmazonEKS_S3_CSI_DriverRole
  POLICY_ARN=AmazonEKS_S3_CSI_DriverRole_ARN
  eksctl create iamserviceaccount \
      --name s3-csi-driver-sa \
      --namespace kube-system \
      --cluster $CLUSTER_NAME \
      --attach-policy-arn $POLICY_ARN \
      --approve \
      --role-name $ROLE_NAME \
      --region $REGION \
      --role-only
  ```

### CSI snapshot controller<a name="addons-csi-snapshot-controller"></a>
+  **Name** – `snapshot-controller` 
+  **Description** – The Container Storage Interface \(CSI\) snapshot controller enables the use of snapshot functionality in compatible CSI drivers, such as the Amazon EBS CSI driver\.
+  **Required IAM permissions** – This add\-on doesn’t require any permissions\.

### AWS Distro for OpenTelemetry<a name="add-ons-adot"></a>
+  **Name** – `adot` 
+  **Description** – The [AWS Distro for OpenTelemetry](https://aws-otel.github.io/) \(ADOT\) is a secure, production\-ready, AWS supported distribution of the OpenTelemetry project\.
+  **Required IAM permissions** – This add\-on only requires IAM permissions if you’re using one of the preconfigured custom resources that can be opted into through advanced configuration\.
+  **Additional information** – For more information, see [Getting Started with AWS Distro for OpenTelemetry using EKS Add\-Ons](https://aws-otel.github.io/docs/getting-started/adot-eks-add-on) in the AWS Distro for OpenTelemetry documentation\.

  ADOT requires that `cert-manager` is deployed on the cluster as a prerequisite, otherwise this add\-on won’t work if deployed directly using the [https://registry\.terraform\.io/modules/terraform\-aws\-modules/eks/aws/latest](https://registry.terraform.io/modules/terraform-aws-modules/eks/aws/latest) `cluster_addons` property\. For more requirements, see [Requirements for Getting Started with AWS Distro for OpenTelemetry using EKS Add\-Ons](https://aws-otel.github.io/docs/getting-started/adot-eks-add-on/requirements) in the AWS Distro for OpenTelemetry documentation\.

### Amazon GuardDuty agent<a name="add-ons-guard-duty"></a>
+  **Name** – `aws-guardduty-agent` 
+  **Description** – Amazon GuardDuty is a security monitoring service that analyzes and processes [foundational data sources](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_data-sources.html) including AWS CloudTrail management events and Amazon VPC flow logs\. Amazon GuardDuty also processes [features](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty-features-activation-model.html), such as Kubernetes audit logs and runtime monitoring\.
+  **Required IAM permissions** – This add\-on doesn’t require any permissions\.
+  **Additional information** – For more information, see [Runtime Monitoring for Amazon EKS clusters in Amazon GuardDuty](https://docs.aws.amazon.com/guardduty/latest/ug/how-runtime-monitoring-works-eks.html)\.
  + To detect potential security threats in your Amazon EKS clusters, enable Amazon GuardDuty runtime monitoring and deploy the GuardDuty security agent to your Amazon EKS clusters\.<a name="amazon-cloudwatch-observability"></a>

1. Amazon CloudWatch Observability agent

**Example**  
+  **Name** – `amazon-cloudwatch-observability` 
+  **Description** [Amazon CloudWatch Agent](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent.html) is the monitoring and observability service provided by AWS\. This add\-on installs the CloudWatch Agent and enables both CloudWatch Application Signals and CloudWatch Container Insights with enhanced observability for Amazon EKS\.

  ```
  eksctl create iamserviceaccount \
      --name cloudwatch-agent \
      --namespace amazon-cloudwatch \
      --cluster my-cluster \
      --role-name AmazonEKS_Observability_Role \
      --role-only \
      --attach-policy-arn arn:aws:iam::aws:policy/{aws}XrayWriteOnlyAccess \
      --attach-policy-arn arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy \
      --approve
  ```
+  **Additional information** – For more information, see [Install the CloudWatch agent](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/install-CloudWatch-Observability-EKS-addon.html)\.

### Amazon EKS Pod Identity Agent<a name="add-ons-pod-id"></a>
+  **Name** – `eks-pod-identity-agent` 
+  **Description** – Amazon EKS Pod Identity provide the ability to manage credentials for your applications, similar to the way that Amazon EC2 instance profiles provide credentials to EC2 instances\.

## Additional Amazon EKS add\-ons from independent software vendors<a name="workloads-add-ons-available-vendors"></a>

In addition to the previous list of Amazon EKS add\-ons, you can also add a wide selection of operational software Amazon EKS add\-ons from independent software vendors\. Choose an add\-on to learn more about it and its installation requirements\.

### Accuknox<a name="add-on-accuknox"></a>
+  **Publisher** – Accuknox 
+  **Name** – `accuknox_kubearmor` 
+  **Namespace** – `kubearmor` 
+  **Service account name** – A service account isn’t used with this add\-on\.
+  ** AWS managed IAM policy** – A managed policy isn’t used with this add\-on\.
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See [Getting Started with KubeArmor](https://docs.kubearmor.io/kubearmor/quick-links/deployment_guide) in the KubeArmor documentation\.

### Akuity<a name="add-on-akuity"></a>
+  **Publisher** – Akuity 
+  **Name** – `akuity_agent` 
+  **Namespace** – `akuity` 
+  **Service account name** – A service account isn’t used with this add\-on\.
+  ** AWS managed IAM policy** – A managed policy isn’t used with this add\-on\.
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See [Installing the Akuity Agent on Amazon EKS with the Akuity EKS add\-on](https://docs.akuity.io/tutorials/eks-addon-agent-install/) in the Akuity Platform documentation\.

### Calyptia<a name="add-on-calyptia"></a>
+  **Publisher** – Calyptia 
+  **Name** – `calyptia_fluent-bit` 
+  **Namespace** – `calytia-fluentbit` 
+  **Service account name** – `clyptia-fluentbit` 
+  ** AWS managed IAM policy** – [https://docs\.aws\.amazon\.com/aws\-managed\-policy/latest/reference/](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/) AWSMarketplaceMeteringRegisterUsage\.html\[AWSMarketplaceMeteringRegisterUsage\]\.

  ```
  eksctl create iamserviceaccount --name service-account-name  --namespace calyptia-fluentbit --cluster my-cluster --role-name my-calyptia-role \
      --role-only --attach-policy-arn arn:aws:iam::aws:policy/{aws}MarketplaceMeteringRegisterUsage --approve
  ```
+  **Setup and usage instructions** – See [Calyptia for Fluent Bit](https://docs.calyptia.com/calyptia-for-fluent-bit/installation/eks-add-on) in the Calyptia documentation\.

### Cisco Observability Collector<a name="add-on-cisco-collector"></a>
+  **Publisher** – Cisco 
+  **Name** – `cisco_cisco-cloud-observability-collectors` 
+  **Namespace** – `appdynamics` 
+  **Service account name** – A service account isn’t used with this add\-on\.
+  ** AWS managed IAM policy** – A managed policy isn’t used with this add\-on\.
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See [Use the Cisco Cloud Observability AWS Marketplace Add\-Ons](https://docs.appdynamics.com/observability/cisco-cloud-observability/en/kubernetes-and-app-service-monitoring/install-kubernetes-and-app-service-monitoring-with-amazon-elastic-kubernetes-service/use-the-cisco-cloud-observability-aws-marketplace-add-ons) in the Cisco AppDynamics documentation\.

### Cisco Observability Operator<a name="add-on-cisco-operator"></a>
+  **Publisher** – Cisco 
+  **Name** – `cisco_cisco-cloud-observability-operators` 
+  **Namespace** – `appdynamics` 
+  **Service account name** – A service account isn’t used with this add\-on\.
+  ** AWS managed IAM policy** – A managed policy isn’t used with this add\-on\.
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See [Use the Cisco Cloud Observability AWS Marketplace Add\-Ons](https://docs.appdynamics.com/observability/cisco-cloud-observability/en/kubernetes-and-app-service-monitoring/install-kubernetes-and-app-service-monitoring-with-amazon-elastic-kubernetes-service/use-the-cisco-cloud-observability-aws-marketplace-add-ons) in the Cisco AppDynamics documentation\.

### CLOUDSOFT<a name="add-on-cloudsoft"></a>
+  **Publisher** – CLOUDSOFT 
+  **Name** – `cloudsoft_cloudsoft-amp` 
+  **Namespace** – `cloudsoft-amp` 
+  **Service account name** – A service account isn’t used with this add\-on\.
+  ** AWS managed IAM policy** – A managed policy isn’t used with this add\-on\.
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See [Amazon EKS ADDON](https://docs.cloudsoft.io/operations/configuration/aws-eks-addon.html) in the CLOUDSOFT documentation\.

### Cribl<a name="add-on-cribl"></a>
+  **Publisher** – Cribl 
+  **Name** – `cribl_cribledge` 
+  **Namespace** – `cribledge` 
+  **Service account name** – A service account isn’t used with this add\-on\.
+  ** AWS managed IAM policy** – A managed policy isn’t used with this add\-on\.
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See [Installing the Cribl Amazon EKS Add\-on for Edge](https://docs.cribl.io/edge/usecase-edge-aws-eks/) in the Cribl documentation\.

### Dynatrace<a name="add-on-dynatrace"></a>
+  **Publisher** – Dynatrace 
+  **Name** – `dynatrace_dynatrace-operator` 
+  **Namespace** – `dynatrace` 
+  **Service account name** – A service account isn’t used with this add\-on\.
+  ** AWS managed IAM policy** – A managed policy isn’t used with this add\-on\.
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See [Kubernetes monitoring](https://www.dynatrace.com/technologies/kubernetes-monitoring/) in the dynatrace documentation\.

### Datree<a name="add-on-datree-pro"></a>
+  **Publisher** – Datree 
+  **Name** – `datree_engine-pro` 
+  **Namespace** – `datree` 
+  **Service account name** – datree\-webhook\-server\-awsmp
+  ** AWS managed IAM policy** – [https://docs\.aws\.amazon\.com/aws\-managed\-policy/latest/reference/](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/) AWSLicenseManagerConsumptionPolicy\.html\[AWSLicenseManagerConsumptionPolicy\]\.

  ```
  eksctl create iamserviceaccount --name datree-webhook-server-awsmp --namespace datree --cluster my-cluster --role-name my-datree-role \
      --role-only --attach-policy-arn arn:aws:iam::aws:policy/service-role/{aws}LicenseManagerConsumptionPolicy --approve
  ```
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See [Amazon EKS\-intergration](https://hub.datree.io/integrations/eks-integration) in the Datree documentation\.

### Datadog<a name="add-on-datadog"></a>
+  **Publisher** – Datadog 
+  **Name** – `datadog_operator` 
+  **Namespace** – `datadog-agent` 
+  **Service account name** – A service account isn’t used with this add\-on\.
+  ** AWS managed IAM policy** – A managed policy isn’t used with this add\-on\.
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See [Installing the Datadog Agent on Amazon EKS with the Datadog Operator Add\-on](https://docs.datadoghq.com/containers/guide/operator-eks-addon/?tab=console) in the Datadog documentation\.

### Groundcover<a name="add-on-groundcover"></a>
+  **Publisher** – groundcover 
+  **Name** – `groundcover_agent` 
+  **Namespace** – `groundcover` 
+  **Service account name** – A service account isn’t used with this add\-on\.
+  ** AWS managed IAM policy** – A managed policy isn’t used with this add\-on\.
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See [Installing the groundcover Amazon EKS Add\-on](https://docs.groundcover.com/docs/~/changes/VhDDAl1gy1VIO3RIcgxD/configuration/customization-guide/customize-deployment/eks-add-on) in the groundcover documentation\.

### Grafana Labs<a name="add-on-grafana"></a>
+  **Publisher** – Grafana Labs 
+  **Name** – `grafana-labs_kubernetes-monitoring` 
+  **Namespace** – `monitoring` 
+  **Service account name** – A service account isn’t used with this add\-on\.
+  ** AWS managed IAM policy** – A managed policy isn’t used with this add\-on\.
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See [Configure Kubernetes Monitoring as an Add\-on with Amazon EKS](https://grafana.com/docs/grafana-cloud/monitor-infrastructure/kubernetes-monitoring/configuration/config-aws-eks/) in the Grafana Labs documentation\.

### HA Proxy<a name="add-on-ha-proxy"></a>
+  **Publisher** – HA Proxy 
+  **Name** – `haproxy-technologies_kubernetes-ingress-ee` 
+  **Namespace** – `haproxy-controller` 
+  **Service account name** – `customer defined` 
+  ** AWS managed IAM policy** – [https://docs\.aws\.amazon\.com/aws\-managed\-policy/latest/reference/](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/) AWSLicenseManagerConsumptionPolicy\.html\[AWSLicenseManagerConsumptionPolicy\]\.

  ```
  eksctl create iamserviceaccount --name service-account-name  --namespace haproxy-controller --cluster my-cluster --role-name my-haproxy-role \
      --role-only --attach-policy-arn arn:aws:iam::aws:policy/service-role/{aws}LicenseManagerConsumptionPolicy --approve
  ```
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See [Install HAProxy Enterprise Kubernetes Ingress Controller on Amazon EKS from AWS](https://www.haproxy.com/documentation/kubernetes/1.8/enterprise/install/aws/install-using-marketplace/#create-the-required-iam-role) in the HAProxy documentation\.

### Kpow<a name="add-on-kpow"></a>
+  **Publisher** – Factorhouse 
+  **Name** – `factorhouse_kpow` 
+  **Namespace** – `factorhouse` 
+  **Service account name** – `kpow` 
+  ** AWS managed IAM policy** – [https://docs\.aws\.amazon\.com/aws\-managed\-policy/latest/reference/](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/) AWSLicenseManagerConsumptionPolicy\.html\[AWSLicenseManagerConsumptionPolicy\]

  ```
  eksctl create iamserviceaccount --name kpow --namespace factorhouse --cluster my-cluster --role-name my-kpow-role \
      --role-only --attach-policy-arn arn:aws:iam::aws:policy/service-role/{aws}LicenseManagerConsumptionPolicy --approve
  ```
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See [AWS Marketplace LM](https://docs.kpow.io/installation/aws-marketplace-lm/) in the Kpow documentation\.

### Kubecost<a name="add-on-kubecost"></a>
+  **Publisher** – Kubecost 
+  **Name** – `kubecost_kubecost` 
+  **Namespace** – `kubecost` 
+  **Service account name** – A service account isn’t used with this add\-on\.
+  ** AWS managed IAM policy** – A managed policy isn’t used with this add\-on\.
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See [AWS Cloud Billing Integration](https://docs.kubecost.com/install-and-configure/install/cloud-integration/aws-cloud-integrations) in the Kubecost documentation\.
+ If your cluster is version `1.23` or later, you must have the installed on your cluster\. otherwise you will receive an error\.

### Kasten<a name="add-on-kasten"></a>
+  **Publisher** – Kasten by Veeam 
+  **Name** – `kasten_k10` 
+  **Namespace** – `kasten-io` 
+  **Service account name** – `k10-k10` 
+  ** AWS managed IAM policy** – [https://docs\.aws\.amazon\.com/aws\-managed\-policy/latest/reference/](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/) AWSLicenseManagerConsumptionPolicy\.html\[AWSLicenseManagerConsumptionPolicy\]\.

  ```
  eksctl create iamserviceaccount --name k10-k10 --namespace kasten-io --cluster my-cluster --role-name my-kasten-role \
      --role-only --attach-policy-arn arn:aws:iam::aws:policy/service-role/{aws}LicenseManagerConsumptionPolicy --approve
  ```
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See [Installing K10 on AWS using Amazon EKS Add\-on](https://docs.kasten.io/latest/install/aws-eks-addon/aws-eks-addon.html) in the Kasten documentation\.
+  **Additional information** – If your Amazon EKS cluster is version Kubernetes `1.23` or later, you must have the Amazon EBS CSI driver installed on your cluster with a default `StorageClass`\.

### Kong<a name="add-on-kong"></a>
+  **Publisher** – Kong 
+  **Name** – `kong_konnect-ri` 
+  **Namespace** – `kong` 
+  **Service account name** – A service account isn’t used with this add\-on\.
+  ** AWS managed IAM policy** – A managed policy isn’t used with this add\-on\.
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See [Installing the Kong Gateway EKS Add\-on](https://kong.github.io/aws-marketplace-addon-kong-gateway/) in the Kong documentation\.

### LeakSignal<a name="add-on-leaksignal"></a>
+  **Publisher** – LeakSignal 
+  **Name** – `leaksignal_leakagent` 
+  **Namespace** – `leakagent` 
+  **Service account name** – A service account isn’t used with this add\-on\.
+  ** AWS managed IAM policy** – A managed policy isn’t used with this add\-on\.
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See [https://www\.leaksignal\.com/docs/LeakAgent/Deployment/](https://www.leaksignal.com/docs/LeakAgent/Deployment/) AWS%20EKS%20Addon/\[Install the LeakAgent add\-on\] in the LeakSignal documentation\.

### NetApp<a name="add-on-netapp"></a>
+  **Publisher** – NetApp 
+  **Name** – `netapp_trident-operator` 
+  **Namespace** – `trident` 
+  **Service account name** – A service account isn’t used with this add\-on\.
+  ** AWS managed IAM policy** – A managed policy isn’t used with this add\-on\.
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See [Configure the Astra Trident EKS add\-on](https://docs.netapp.com/us-en/trident/trident-use/trident-aws-addon.html) in the NetApp documentation\.

### New Relic<a name="add-on-new-relic"></a>
+  **Publisher** – New Relic 
+  **Name** – `new-relic_kubernetes-operator` 
+  **Namespace** – `newrelic` 
+  **Service account name** – A service account isn’t used with this add\-on\.
+  ** AWS managed IAM policy** – A managed policy isn’t used with this add\-on\.
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See [Installing the New Relic Add\-on for EKS](https://docs.newrelic.com/docs/infrastructure/amazon-integrations/connect/eks-add-on) in the New Relic documentation\.

### Rafay<a name="add-on-rafay"></a>
+  **Publisher** – Rafay 
+  **Name** – `rafay-systems_rafay-operator` 
+  **Namespace** – `rafay-system` 
+  **Service account name** – A service account isn’t used with this add\-on\.
+  ** AWS managed IAM policy** – A managed policy isn’t used with this add\-on\.
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See [Installing the Rafay Amazon EKS Add\-on](https://docs.rafay.co/clusters/import/eksaddon/) in the Rafay documentation\.

### Solo\.io<a name="add-on-solo"></a>
+  **Publisher** – Solo\.io 
+  **Name** – `solo-io_istio-distro` 
+  **Namespace** – `istio-system` 
+  **Service account name** – A service account isn’t used with this add\-on\.
+  ** AWS managed IAM policy** – A managed policy isn’t used with this add\-on\.
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See [Installing Istio](https://docs.solo.io/gloo-mesh-enterprise/main/setup/install/eks_addon/) in the Solo\.io documentation\.

### Stormforge<a name="add-on-stormforge"></a>
+  **Publisher** – Stormforge 
+  **Name** – `stormforge_optimize-Live` 
+  **Namespace** – `stormforge-system` 
+  **Service account name** – A service account isn’t used with this add\-on\.
+  ** AWS managed IAM policy** – A managed policy isn’t used with this add\-on\.
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See [Installing the StormForge Agent](https://docs.stormforge.io/optimize-live/getting-started/install-v2/) in the StormForge documentation\.

### Splunk<a name="add-on-splunk"></a>
+  **Publisher** – Splunk 
+  **Name** – `splunk_splunk-otel-collector-chart` 
+  **Namespace** – `splunk-monitoring` 
+  **Service account name** – A service account isn’t used with this add\-on\.
+  ** AWS managed IAM policy** – A managed policy isn’t used with this add\-on\.
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See [Install the Splunk add\-on for Amazon EKS](https://docs.splunk.com/observability/en/gdi/opentelemetry/install-k8s-addon-eks.html) in the Splunk documentation\.

### Teleport<a name="add-on-teleport"></a>
+  **Publisher** – Teleport 
+  **Name** – `teleport_teleport` 
+  **Namespace** – `teleport` 
+  **Service account name** – A service account isn’t used with this add\-on\.
+  ** AWS managed IAM policy** – A managed policy isn’t used with this add\-on\.
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See [How Teleport Works](https://goteleport.com/how-it-works/) in the Teleport documentation\.

### Tetrate<a name="add-on-tetrate"></a>
+  **Publisher** – Tetrate Io
+  **Name** – `tetrate-io_istio-distro` 
+  **Namespace** – `istio-system` 
+  **Service account name** – A service account isn’t used with this add\-on\.
+  ** AWS managed IAM policy** – A managed policy isn’t used with this add\-on\.
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See the [Tetrate Istio Distro](https://tetratelabs.io/) web site\.

### Upbound Universal Crossplane<a name="add-on-upbound"></a>
+  **Publisher** – Upbound 
+  **Name** – `upbound_universal-crossplane` 
+  **Namespace** – `upbound-system` 
+  **Service account name** – A service account isn’t used with this add\-on\.
+  ** AWS managed IAM policy** – A managed policy isn’t used with this add\-on\.
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See [Upbound Universal Crossplane \(UXP\)](https://docs.upbound.io/uxp/) in the Upbound documentation\.

### Upwind<a name="add-on-upwind"></a>
+  **Publisher** – Upwind 
+  **Name** – `upwind` 
+  **Namespace** – `upwind` 
+  **Service account name** – A service account isn’t used with this add\-on\.
+  ** AWS managed IAM policy** – A managed policy isn’t used with this add\-on\.
+  **Custom IAM permissions** – Custom permissions aren’t used with this add\-on\.
+  **Setup and usage instructions** – See the installation steps in the [Upwind documentation](https://docs.upwind.io/install-sensor/kubernetes/install?installation-method=amazon-eks-addon)\.