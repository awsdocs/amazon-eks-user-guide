# Amazon EKS add\-ons<a name="eks-add-ons"></a>

An add\-on is software that provides supporting operational capabilities to Kubernetes applications, but is not specific to the application\. This includes software like observability agents or Kubernetes drivers that allow the cluster to interact with underlying AWS resources for networking, compute, and storage\. Add\-on software is typically built and maintained by the Kubernetes community, cloud providers like AWS, or third\-party vendors\. Amazon EKS automatically installs self\-managed add\-ons such as the Amazon VPC CNI plugin for Kubernetes, `kube-proxy`, and CoreDNS for every cluster\. You can change the default configuration of the add\-ons and update them when desired\.

 Amazon EKS add\-ons provide installation and management of a curated set of add\-ons for Amazon EKS clusters\. All Amazon EKS add\-ons include the latest security patches, bug fixes, and are validated by AWS to work with Amazon EKS\. Amazon EKS add\-ons allow you to consistently ensure that your Amazon EKS clusters are secure and stable and reduce the amount of work that you need to do in order to install, configure, and update add\-ons\. If a self\-managed add\-on, such as `kube-proxy` is already running on your cluster and is available as an Amazon EKS add\-on, then you can install the `kube-proxy` Amazon EKS add\-on to start benefiting from the capabilities of Amazon EKS add\-ons\.

You can update specific Amazon EKS managed configuration fields for Amazon EKS add\-ons through the Amazon EKS API\. You can also modify configuration fields not managed by Amazon EKS directly within the Kubernetes cluster once the add\-on starts\. This includes defining specific configuration fields for an add\-on where applicable\. These changes are not overridden by Amazon EKS once they are made\. This is made possible using the Kubernetes server\-side apply feature\. For more information, see [ Kubernetes field management](kubernetes-field-management.md)\.

You can use Amazon EKS add\-ons with any Amazon EKS [node type](eks-compute.md)\.

**Considerations**
+ To configure add\-ons for the cluster your [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) must have IAM permissions to work with add\-ons\. For more information, see the actions with `Addon` in their name in [Actions defined by Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html#amazonelastickubernetesservice-actions-as-permissions)\.
+ Amazon EKS add\-ons run on the nodes that you provision or configure for your cluster\. Node types include Amazon EC2 instances and Fargate\.
+ You can modify fields that aren't managed by Amazon EKS to customize the installation of an Amazon EKS add\-on\. For more information, see [ Kubernetes field management](kubernetes-field-management.md)\.
+ If you create a cluster with the AWS Management Console, the Amazon EKS `kube-proxy`, Amazon VPC CNI plugin for Kubernetes, and CoreDNS Amazon EKS add\-ons are automatically added to your cluster\. If you use `eksctl` to create your cluster with a `config` file, `eksctl` can also create the cluster with Amazon EKS add\-ons\. If you create your cluster using `eksctl` without a `config` file or with any other tool, the self\-managed `kube-proxy`, Amazon VPC CNI plugin for Kubernetes, and CoreDNS add\-ons are installed, rather than the Amazon EKS add\-ons\. You can either manage them yourself or add the Amazon EKS add\-ons manually after cluster creation\.
+ The `eks:addon-cluster-admin` `ClusterRoleBinding` binds the `cluster-admin` `ClusterRole` to the `eks:addon-manager` Kubernetes identity\. The role has the necessary permissions for the `eks:addon-manager` identity to create Kubernetes namespaces and install add\-ons into namespaces\. If the `eks:addon-cluster-admin` `ClusterRoleBinding` is removed, the Amazon EKS cluster continues to function, however Amazon EKS is no longer able to manage any add\-ons\. All clusters starting with the following platform versions use the new `ClusterRoleBinding`\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/eks-add-ons.html)

You can add, update, or delete Amazon EKS add\-ons using the Amazon EKS API, AWS Management Console, AWS CLI, and `eksctl`\. For more information, see [Managing Amazon EKS add\-ons](managing-add-ons.md)\. You can also create Amazon EKS add\-ons using [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-addon.html)\.

## Available Amazon EKS add\-ons from Amazon EKS<a name="workloads-add-ons-available-eks"></a>

The following Amazon EKS add\-ons are available to create on your cluster\. You can always view the most current list of available add\-ons using `eksctl`, the AWS Management Console, or the AWS CLI\. To see all available add\-ons or to install an add\-on, see [Creating an add\-on](managing-add-ons.md#creating-an-add-on)\. If an add\-on requires IAM permissions, then you must have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one, or to create one, see [Creating an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\. You can [update](managing-add-ons.md#updating-an-add-on) or [delete](managing-add-ons.md#removing-an-add-on) an add\-on once you've installed it\. 

Choose an add\-on to learn more about it and its installation requirements\.

### Amazon VPC CNI plugin for Kubernetes<a name="add-ons-vpc-cni"></a>
+ **Name** – `vpc-cni`
+ **Description** – A [Kubernetes container network interface \(CNI\) plugin](https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/) that provides native VPC networking for your cluster\. The self\-managed or managed type of this add\-on is installed on each Amazon EC2 node, by default\.
+ **Required IAM permissions** – This add\-on utilizes the [IAM roles for service accounts](iam-roles-for-service-accounts.md) capability of Amazon EKS\. If your cluster uses the `IPv4` family, the permissions in the [AmazonEKS\_CNI\_Policy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKS_CNI_Policy.html) are required\. If your cluster uses the `IPv6` family, you must [create an IAM policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html) with the permissions in [IPv6 mode](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/docs/iam-policy.md#ipv6-mode)\. You can create an IAM role, attach one of the policies to it, and annotate the Kubernetes service account used by the add\-on with the following command\. 

  Replace *my\-cluster* with the name of your cluster and *AmazonEKSVPCCNIRole* with the name for your role\. If your cluster uses the `IPv6` family, then replace *AmazonEKS\_CNI\_Policy* with the name of the policy that you created\. This command requires that you have `eksctl` installed on your device\. If you need to use a different tool to create the role, attach the policy to it, and annotate the Kubernetes service account, see [Configuring a Kubernetes service account to assume an IAM role](associate-service-account-role.md)\.

  ```
  eksctl create iamserviceaccount --name aws-node --namespace kube-system --cluster my-cluster --role-name "AmazonEKSVPCCNIRole" \
      --role-only --attach-policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy --approve
  ```
+ **Additional information** – To learn more about the add\-on's configurable settings, see [aws\-vpc\-cni\-k8s](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/README.md) on GitHub\. To learn more about the plug\-in, see [Proposal: CNI plugin for Kubernetes networking over AWS VPC](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/docs/cni-proposal.md)\. For more information about creating the add\-on, see [Creating the Amazon EKS add\-on](managing-vpc-cni.md#vpc-add-on-create)\.
+ **Update information** – You can only update one minor version at a time\. For example, if your current version is `1.24.x-eksbuild.y` and you want to update to `1.26.x-eksbuild.y`, then you must update your current version to `1.25.x-eksbuild.y` and then update it again to `1.26.x-eksbuild.y`\. For more information about updating the add\-on, see [Updating the Amazon EKS add\-on](managing-vpc-cni.md#vpc-add-on-update)\.

### CoreDNS<a name="add-ons-coredns"></a>
+ **Name** – `coredns`
+ **Description** – A flexible, extensible DNS server that can serve as the Kubernetes cluster DNS\. The self\-managed or managed type of this add\-on was installed, by default, when you created your cluster\. When you launch an Amazon EKS cluster with at least one node, two replicas of the CoreDNS image are deployed by default, regardless of the number of nodes deployed in your cluster\. The CoreDNS Pods provide name resolution for all Pods in the cluster\. You can deploy the CoreDNS Pods to Fargate nodes if your cluster includes an [AWS Fargate profile](fargate-profile.md) with a namespace that matches the namespace for the CoreDNS `deployment`\.
+ **Required IAM permissions** – This add\-on doesn't require any permissions\.
+ **Additional information** – To learn more about CoreDNS, see [Using CoreDNS for Service Discovery](https://kubernetes.io/docs/tasks/administer-cluster/coredns/) and [Customizing DNS Service](https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/) in the Kubernetes documentation\.

### `Kube-proxy`<a name="add-ons-kube-proxy"></a>
+ **Name** – `kube-proxy`
+ **Description** – Maintains network rules on each Amazon EC2 node\. It enables network communication to your Pods\. The self\-managed or managed type of this add\-on is installed on each Amazon EC2 node in your cluster, by default\.
+ **Required IAM permissions** – This add\-on doesn't require any permissions\.
+ **Additional information** – To learn more about `kube-proxy`, see [https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/) in the Kubernetes documentation\.
+ **Update information** – Before updating your current version, consider the following requirements:
  + `Kube-proxy` on an Amazon EKS cluster has the same [compatibility and skew policy as Kubernetes](https://kubernetes.io/releases/version-skew-policy/#kube-proxy)\.
  + `Kube-proxy` must be the same minor version as `kubelet` on your Amazon EC2 nodes\. 
  + `Kube-proxy` can't be later than the minor version of your cluster's control plane\.
  + The `kube-proxy` version on your Amazon EC2 nodes can't be more than two minor versions earlier than your control plane\. For example, if your control plane is running Kubernetes 1\.26, then the `kube-proxy` minor version can't be earlier than 1\.24\.
  + If you recently updated your cluster to a new Kubernetes minor version, then update your Amazon EC2 nodes to the same minor version *before* updating `kube-proxy` to the same minor version as your nodes\.

### Amazon EBS CSI driver<a name="add-ons-aws-ebs-csi-driver"></a>
+ **Name** – `aws-ebs-csi-driver`
+ **Description** – A Kubernetes Container Storage Interface \(CSI\) plugin that provides Amazon EBS storage for your cluster\.
+ **Required IAM permissions** – This add\-on utilizes the [IAM roles for service accounts](iam-roles-for-service-accounts.md) capability of Amazon EKS\. You must [create an IAM policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html) with the permissions in the [example policy](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/docs/example-iam-policy.json) from GitHub\. You can create an IAM role, attach one of the policies to it, and annotate the Kubernetes service account used by the add\-on with the following command\. Replace *my\-cluster* with the name of your cluster, *AmazonEKS\_EBS\_CSI\_DriverRole* with the name for your role, and *AmazonEBSCSIDriverPolicy* with the name of the policy that you created\. This command requires that you have `eksctl` installed on your device\. If you need to use a different tool to create the role, attach the policy to it, and annotate the Kubernetes service account, see [Configuring a Kubernetes service account to assume an IAM role](associate-service-account-role.md)\.

  ```
  eksctl create iamserviceaccount --name ebs-csi-controller-sa --namespace kube-system --cluster my-cluster \
      --role-name "AmazonEKS_EBS_CSI_DriverRole" --role-only --attach-policy-arn arn:aws:iam::aws:policy/AmazonEBSCSIDriverPolicy --approve
  ```
+ **Additional information** – To learn more about the driver, see [Amazon EBS CSI driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/README.md) on GitHub\. You can deploy [examples](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/tree/master/examples/kubernetes) for testing purposes from GitHub\.

### ADOT<a name="add-ons-adot"></a>
+ **Name** – `adot`
+ **Description** – The [AWS Distro for OpenTelemetry](https://aws-otel.github.io/) \(ADOT\) is a secure, production\-ready, AWS supported distribution of the OpenTelemetry project\. 
**Prerequisites** - This add/-on requires [cert-manager](https://cert-manager.io/) deployed on the cluster as a [pre-requisite](**url**https://docs.aws.amazon.com/eks/latest/userguide/adot-reqts.html). Thus this add-on will not work if deployed directly using the [Terraform eks module](terraform-aws-modules/eks/aws) `cluster_addons` property. 
+ **Required IAM permissions** – This add\-on utilizes the [IAM roles for service accounts](iam-roles-for-service-accounts.md) capability of Amazon EKS\. The permissions in the [AmazonPrometheusRemoteWriteAccess](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonPrometheusRemoteWriteAccess.html), [AWSXrayWriteOnlyAccess](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AWSXrayWriteOnlyAccess), and [CloudWatchAgentServerPolicy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy) AWS managed policies\. You can create an IAM role, attach the managed policies to it, and annotate the Kubernetes service account used by the add\-on with the following command\. Replace *my\-cluster* with the name of your cluster and *AmazonEKS\_ADOT\_Collector\_Role* with the name for your role\. This command requires that you have `eksctl` installed on your device\. If you need to use a different tool to create the role, attach the policy to it, and annotate the Kubernetes service account, see [Configuring a Kubernetes service account to assume an IAM role](associate-service-account-role.md)\.

  ```
  eksctl create iamserviceaccount --name adot-collector --namespace default --cluster my-cluster --role-name "AmazonEKS_ADOT_Collector_Role" \
      --attach-policy-arn arn:aws:iam::aws:policy/AmazonPrometheusRemoteWriteAccess \
      --attach-policy-arn arn:aws:iam::aws:policy/AWSXrayWriteOnlyAccess \
      --attach-policy-arn arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy --approve
  ```
+ **Additional information** – For more information, see [Getting Started with AWS Distro for OpenTelemetry using EKS Add\-Ons](https://aws-otel.github.io/docs/getting-started/adot-eks-add-on) in the AWS Distro for OpenTelemetry documentation\.

### Amazon GuardDuty agent<a name="add-ons-guard-duty"></a>
**Note**  
 Amazon GuardDuty isn't available in the Asia Pacific \(Melbourne\) Region\.
+ **Name** – `aws-guardduty-agent`
+ **Description** – Amazon GuardDuty is a security monitoring service that analyzes and processes [foundational data sources](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_data-sources.html) including AWS CloudTrail management events and Amazon VPC flow logs\. Amazon GuardDuty also processes [features](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty-features-activation-model.html), such as Kubernetes audit logs and runtime monitoring\.
+ **Required IAM permissions** – This add\-on doesn't require any permissions\.
+ **Additional information** – For more information, see [Amazon EKS Protection in Amazon GuardDuty](https://docs.aws.amazon.com/guardduty/latest/ug/kubernetes-protection.html)\.
  + To detect potential security threats in your Amazon EKS clusters, enable Amazon GuardDuty runtime monitoring and deploy the GuardDuty security agent to your Amazon EKS clusters\.
  + GuardDuty doesn't support ARM64 nodes at this time\. 

## Additional Amazon EKS add\-ons from independent software vendors<a name="workloads-add-ons-available-vendors"></a>

In addition to the previous list of Amazon EKS add\-ons, you can also add a wide selection of operational software Amazon EKS add\-ons from independent software vendors\. Choose an add\-on to learn more about it and its installation requirements\.

### Dynatrace<a name="add-on-dynatrace"></a>
+ **Publisher** – Dynatrace
+ **Name** – `dynatrace_dynatrace-operator`
+ **Version** – `v0.8.2-eksbuild.0`
+ **Namespace** – `dynatrace`
+ **Service account name** – A service account isn't used with this add\-on\.
+ **AWS managed IAM policy** – A managed policy isn't used with this add\-on\.
+ **Custom IAM permissions** – Custom permissions aren't used with this add\-on\.
+ **Setup and usage instructions** – See [Kubernetes monitoring](https://www.dynatrace.com/technologies/kubernetes-monitoring/) in the dynatrace documentation\.

### Kpow<a name="add-on-kpow"></a>
+ **Publisher** – Factorhouse
+ **Name** – `factorhouse_kpow`
+ **Version** – `v90.2.3-eksbuild.0`
+ **Namespace** – `factorhouse`
+ **Service account name** – `kpow`
+ **AWS managed IAM policy** – [AWSLicenseManagerConsumptionPolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AWSLicenseManagerConsumptionPolicy.html)
+ **Command to create required IAM role** – The following command requires that you have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one, or to create one, see [Creating an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\. Replace *my\-cluster* with the name of your cluster and *my\-kpow\-role* with the name for your role\. This command requires that you have `eksctl` installed on your device\. If you need to use a different tool to create the role and annotate the Kubernetes service account, see [Configuring a Kubernetes service account to assume an IAM role](associate-service-account-role.md)\.

  ```
  eksctl create iamserviceaccount --name kpow --namespace factorhouse --cluster my-cluster --role-name "my-kpow-role" \
      --role-only --attach-policy-arn arn:aws:iam::aws:policy/service-role/AWSLicenseManagerConsumptionPolicy --approve
  ```
+ **Custom IAM permissions** – Custom permissions aren't used with this add\-on\.
+ **Setup and usage instructions** – See [AWS Marketplace LM](https://docs.kpow.io/installation/aws-marketplace-lm/) in the Kpow documentation\.

### Kubecost<a name="add-on-kubecost"></a>
+ **Publisher** – Kubecost
+ **Name** – `kubecost_kubecost`
+ **Version** – `v1.98.0-eksbuild.1`
+ **Namespace** – `kubecost`
+ **Service account name** – A service account isn't used with this add\-on\.
+ **AWS managed IAM policy** – A managed policy isn't used with this add\-on\.
+ **Custom IAM permissions** – Custom permissions aren't used with this add\-on\.
+ **Setup and usage instructions** – See [Amazon EKS integration](https://guide.kubecost.com/hc/en-us/articles/8428105779095-Amazon-EKS-integration) in the Kubecost documentation\.
+ If your cluster is version `1.23` or later, you must have the [Amazon EBS CSI driver](ebs-csi.md) installed on your cluster\. otherwise you will receive an error\.

### Kyverno Enterprise<a name="add-on-nirmata"></a>
+ **Publisher** – Nirmata
+ **Name** – `nirmata_kyverno`
+ **Version** – `v1.8.1-eksbuild.0`
+ **Namespace** – `kyverno`
+ **Service account name** – `kyverno`
+ **AWS managed IAM policy** – [AWSLicenseManagerConsumptionPolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AWSLicenseManagerConsumptionPolicy.html)
+ **Command to create required IAM role** – The following command requires that you have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one, or to create one, see [Creating an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\. Replace *my\-cluster* with the name of your cluster and *my\-kyverno\-role* with the name for your role\. This command requires that you have `eksctl` installed on your device\. If you need to use a different tool to create the role and annotate the Kubernetes service account, see [Configuring a Kubernetes service account to assume an IAM role](associate-service-account-role.md)\.

  ```
  eksctl create iamserviceaccount --name kyverno --namespace kyverno --cluster my-cluster --role-name "my-kyverno-role" \
      --role-only --attach-policy-arn arn:aws:iam::aws:policy/service-role/AWSLicenseManagerConsumptionPolicy --approve
  ```
+ **Custom IAM permissions** – Custom permissions aren't used with this add\-on\.
+ **Setup and usage instructions** – See [Nirmata Kyverno Enterprise](https://docs.nirmata.io/n4k/) in the Nirmata documenation\.

### Teleport<a name="add-on-teleport"></a>
+ **Publisher** – Teleport
+ **Name** – `teleport_teleport`
+ **Version** – `v10.3.1-eksbuild.0`
+ **Namespace** – `teleport`
+ **Service account name** – A service account isn't used with this add\-on\.
+ **AWS managed IAM policy** – A managed policy isn't used with this add\-on\.
+ **Custom IAM permissions** – Custom permissions aren't used with this add\-on\.
+ **Setup and usage instructions** – See [How Teleport Works](https://goteleport.com/how-it-works/) in the Teleport documentation\.

### Tetrate<a name="add-on-tetrate"></a>
+ **Publisher** – Tetrate
+ **Name** – `tetrate-io_istio-distro`
+ **Version** – `v1.15.3-eksbuild.0`
+ **Namespace** – `istio-system`
+ **Service account name** – A service account isn't used with this add\-on\.
+ **AWS managed IAM policy** – A managed policy isn't used with this add\-on\.
+ **Custom IAM permissions** – Custom permissions aren't used with this add\-on\.
+ **Setup and usage instructions** – See the [Tetrate Istio Distro](https://tetratelabs.io/) web site\.

### Upbound Universal Crossplane<a name="add-on-upbound"></a>
+ **Publisher** – Upbound
+ **Name** – `upbound_universal-crossplane`
+ **Version** – `v1.9.1-eksbuild.0`
+ **Namespace** – `upbound-system`
+ **Service account name** – A service account isn't used with this add\-on\.
+ **AWS managed IAM policy** – A managed policy isn't used with this add\-on\.
+ **Custom IAM permissions** – Custom permissions aren't used with this add\-on\.
+ **Setup and usage instructions** – See [Upbound Universal Crossplane \(UXP\)](https://docs.upbound.io/uxp/) in the Upbound documentation\.
