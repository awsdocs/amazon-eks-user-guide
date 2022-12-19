# Amazon EKS add\-ons<a name="eks-add-ons"></a>

An add\-on is software that provides supporting operational capabilities to Kubernetes applications, but is not specific to the application\. This includes software like observability agents or Kubernetes drivers that allow the cluster to interact with underlying AWS resources for networking, compute, and storage\. Add\-on software is typically built and maintained by the Kubernetes community, cloud providers like AWS, or third\-party vendors\. Amazon EKS automatically installs self\-managed add\-ons such as the Amazon VPC CNI plugin for Kubernetes, `kube-proxy`, and CoreDNS for every cluster\. You can change the default configuration of the add\-ons and update them when desired\.

 Amazon EKS add\-ons provide installation and management of a curated set of add\-ons for Amazon EKS clusters\. All Amazon EKS add\-ons include the latest security patches, bug fixes, and are validated by AWS to work with Amazon EKS\. Amazon EKS add\-ons allow you to consistently ensure that your Amazon EKS clusters are secure and stable and reduce the amount of work that you need to do in order to install, configure, and update add\-ons\. If a self\-managed add\-on, such as `kube-proxy` is already running on your cluster and is available as an Amazon EKS add\-on, then you can install the `kube-proxy` Amazon EKS add\-on to start benefiting from the capabilities of Amazon EKS add\-ons\.

You can update specific Amazon EKS managed configuration fields for Amazon EKS add\-ons through the Amazon EKS API\. You can also modify configuration fields not managed by Amazon EKS directly within the Kubernetes cluster once the add\-on starts\. This includes defining specific configuration fields for an add\-on where applicable\. These changes are not overridden by Amazon EKS once they are made\. This is made possible using the Kubernetes server\-side apply feature\. For more information, see [ Kubernetes field management](kubernetes-field-management.md)\.

You can use Amazon EKS add\-ons with any Amazon EKS [node type](eks-compute.md)\.

**Considerations**
+ To configure add\-ons for the cluster your IAM user must have IAM permissions to work with add\-ons\. For more information, see the actions with `Addon` in their name in [Actions defined by Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html#amazonelastickubernetesservice-actions-as-permissions)\.
+ Amazon EKS add\-ons run on the nodes that you provision or configure for your cluster\. Node types include Amazon EC2 instances and Fargate\.
+ You can modify fields that aren't managed by Amazon EKS to customize the installation of an Amazon EKS add\-on\. For more information, see [ Kubernetes field management](kubernetes-field-management.md)\.
+ If you create a cluster with the AWS Management Console, the Amazon EKS `kube-proxy`, Amazon VPC CNI plugin for Kubernetes, and CoreDNS Amazon EKS add\-ons are automatically added to your cluster\. If you use `eksctl` to create your cluster with a `config` file, `eksctl` can also create the cluster with Amazon EKS add\-ons\. If you create your cluster using `eksctl` without a `config` file or with any other tool, the self\-managed `kube-proxy`, Amazon VPC CNI plugin for Kubernetes, and CoreDNS add\-ons are installed, rather than the Amazon EKS add\-ons\. You can either manage them yourself or add the Amazon EKS add\-ons manually after cluster creation\.
+ The `eks:addon-cluster-admin` `ClusterRoleBinding` binds the `cluster-admin` `ClusterRole` to the `eks:addon-manager` identity\. The role has the necessary permissions for the `eks:addon-manager` identity to create Kubernetes namespaces and install add\-ons into namespaces\. If the `eks:addon-cluster-admin` `ClusterRoleBinding` is removed, the Amazon EKS cluster continues to function, however Amazon EKS is no longer able to manage any add\-ons\. All clusters starting with the following platform versions use the new `ClusterRoleBinding`\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/eks-add-ons.html)

You can add, update, or delete Amazon EKS add\-ons using the Amazon EKS API, AWS Management Console, AWS CLI, and `eksctl`\. For more information, see [Managing Amazon EKS add\-ons](managing-add-ons.md)\. You can also create Amazon EKS add\-ons using [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-addon.html)\.

## Available Amazon EKS add\-ons<a name="workloads-add-ons-available-add-ons"></a>

The following Amazon EKS add\-ons are available to create on your cluster\. For information about an add\-on, choose it from the list\.
+ [Amazon VPC CNI plugin for Kubernetes](managing-vpc-cni.md)
+ [CoreDNS](managing-coredns.md) 
+ [`kube-proxy`](managing-kube-proxy.md)
+ [ADOT](opentelemetry.md)
+ [Amazon EBS CSI](managing-ebs-csi.md)

In addition to the previous list of Amazon EKS add\-ons, you can also add a wide selection of operational software Amazon EKS add\-ons from independent software vendors\. The following add\-ons are only available for clusters created after November 27, 2022\. Installation on clusters created before that date might fail\. Choose an add\-on to learn more about it and its installation requirements\.

## Dynatrace<a name="add-on-dynatrace"></a>
+ **Publisher** – Dynatrace
+ **Name** – `dynatrace_dynatrace-operator`
+ **Version** – `v0.8.2-eksbuild.0`
+ **Namespace** – `dynatrace`
+ **Service account name** – A service account isn't used with this add\-on\.
+ **AWS managed IAM policy** – A managed policy isn't used with this add\-on\.
+ **Custom IAM permissions** – Custom permissions aren't used with this add\-on\.
+ **Setup and usage instructions** – See [Kubernetes monitoring](https://www.dynatrace.com/technologies/kubernetes-monitoring/) in the dynatrace documentation\.

## Kpow<a name="add-on-kpow"></a>
+ **Publisher** – Factorhouse
+ **Name** – `factorhouse_kpow`
+ **Version** – `v90.2.3-eksbuild.0`
+ **Namespace** – `factorhouse`
+ **Service account name** – `kpow`
+ **AWS managed IAM policy** – [AWSLicenseManagerConsumptionPolicy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/service-role/AWSLicenseManagerConsumptionPolicy$jsonEditor)
+ **Command to create required IAM role** – The following command requires that you have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one, or to create one, see [Creating an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\. Replace *my\-cluster* with the name of your cluster and *my\-kpow\-role* with the name for your role\. This command requires that you have `eksctl` installed on your device\. If you need to use a different tool to create the role and annotate the Kubernetes service account, see [Configuring a Kubernetes service account to assume an IAM role](associate-service-account-role.md)\.

  ```
  eksctl create iamserviceaccount --name kpow --namespace factorhouse --cluster my-cluster --role-name "my-kpow-role" \
      --role-only --attach-policy-arn arn:aws:iam::aws:policy/service-role/AWSLicenseManagerConsumptionPolicy --approve
  ```
+ **Custom IAM permissions** – Custom permissions aren't used with this add\-on\.
+ **Setup and usage instructions** – See [AWS Marketplace LM](https://docs.kpow.io/installation/aws-marketplace-lm/) in the Kpow documentation\.

## Kubecost<a name="add-on-kubecost"></a>
+ **Publisher** – Kubecost
+ **Name** – `kubecost_kubecost`
+ **Version** – `v1.98.0-eksbuild.1`
+ **Namespace** – `kubecost`
+ **Service account name** – A service account isn't used with this add\-on\.
+ **AWS managed IAM policy** – A managed policy isn't used with this add\-on\.
+ **Custom IAM permissions** – Custom permissions aren't used with this add\-on\.
+ **Setup and usage instructions** – See [Amazon EKS integration](https://guide.kubecost.com/hc/en-us/articles/8428105779095-Amazon-EKS-integration) in the Kubecost documentation\.
+ If your cluster is version `1.23` or later, you must have the [Amazon EBS CSI driver](ebs-csi.md) installed on your cluster\. otherwise you will receive an error\.

## Kyverno Enterprise<a name="add-on-nirmata"></a>
+ **Publisher** – Nirmata
+ **Name** – `nirmata_kyverno`
+ **Version** – `v1.8.1-eksbuild.0`
+ **Namespace** – `kyverno`
+ **Service account name** – `kyverno`
+ **AWS managed IAM policy** – [AWSLicenseManagerConsumptionPolicy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/service-role/AWSLicenseManagerConsumptionPolicy$jsonEditor)
+ **Command to create required IAM role** – The following command requires that you have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one, or to create one, see [Creating an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\. Replace *my\-cluster* with the name of your cluster and *my\-kyverno\-role* with the name for your role\. This command requires that you have `eksctl` installed on your device\. If you need to use a different tool to create the role and annotate the Kubernetes service account, see [Configuring a Kubernetes service account to assume an IAM role](associate-service-account-role.md)\.

  ```
  eksctl create iamserviceaccount --name kyverno --namespace kyverno --cluster my-cluster --role-name "my-kyverno-role" \
      --role-only --attach-policy-arn arn:aws:iam::aws:policy/service-role/AWSLicenseManagerConsumptionPolicy --approve
  ```
+ **Custom IAM permissions** – Custom permissions aren't used with this add\-on\.
+ **Setup and usage instructions** – See [Nirmata Kyverno Enterprise](https://docs.nirmata.io/n4k/) in the Nirmata documenation\.

## Teleport<a name="add-on-teleport"></a>
+ **Publisher** – Teleport
+ **Name** – `teleport_teleport`
+ **Version** – `v10.3.1-eksbuild.0`
+ **Namespace** – `teleport`
+ **Service account name** – A service account isn't used with this add\-on\.
+ **AWS managed IAM policy** – A managed policy isn't used with this add\-on\.
+ **Custom IAM permissions** – Custom permissions aren't used with this add\-on\.
+ **Setup and usage instructions** – See [How Teleport Works](https://goteleport.com/how-it-works/) in the Teleport documentation\.

## Tetrate<a name="add-on-tetrate"></a>
+ **Publisher** – Tetrate
+ **Name** – `tetrate-io_istio-distro`
+ **Version** – `v1.15.3-eksbuild.0`
+ **Namespace** – `istio-system`
+ **Service account name** – A service account isn't used with this add\-on\.
+ **AWS managed IAM policy** – A managed policy isn't used with this add\-on\.
+ **Custom IAM permissions** – Custom permissions aren't used with this add\-on\.
+ **Setup and usage instructions** – See the [Tetrate Istio Distro](https://tetratelabs.io/) web site\.

## Upbound Universal Crossplane<a name="add-on-upbound"></a>
+ **Publisher** – Upbound
+ **Name** – `upbound_universal-crossplane`
+ **Version** – `v1.9.1-eksbuild.0`
+ **Namespace** – `upbound-system`
+ **Service account name** – A service account isn't used with this add\-on\.
+ **AWS managed IAM policy** – A managed policy isn't used with this add\-on\.
+ **Custom IAM permissions** – Custom permissions aren't used with this add\-on\.
+ **Setup and usage instructions** – See [Upbound Universal Crossplane \(UXP\)](https://docs.upbound.io/uxp/) in the Upbound documentation\.