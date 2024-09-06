# Available Amazon EKS add\-ons from AWS<a name="workloads-add-ons-available-eks"></a>

The following Amazon EKS add\-ons are available to create on your cluster\. You can view the most current list of available add\-ons using `eksctl`, the AWS Management Console, or the AWS CLI\. To see all available add\-ons or to install an add\-on, see [Creating an Amazon EKS add\-on](creating-an-add-on.md)\. If an add\-on requires IAM permissions, then you must have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\. You can [update](updating-an-add-on.md) or [delete](removing-an-add-on.md) an add\-on after you've installed it\. 

You can use any of the following Amazon EKS add\-ons\.


| Description | Learn more | 
| --- | --- | 
|  Provide native VPC networking for your cluster  |  [Amazon VPC CNI plugin for Kubernetes](#add-ons-vpc-cni)  | 
|  A flexible, extensible DNS server that can serve as the Kubernetes cluster DNS  |  [CoreDNS](#add-ons-coredns)  | 
| Maintain network rules on each Amazon EC2 node |  [`Kube-proxy`](#add-ons-kube-proxy)  | 
| Provide Amazon EBS storage for your cluster |  [Amazon EBS CSI driver](#add-ons-aws-ebs-csi-driver)  | 
| Provide Amazon EFS storage for your cluster |  [Amazon EFS CSI driver](#add-ons-aws-efs-csi-driver)  | 
| Provide Amazon S3 storage for your cluster |  [Mountpoint for Amazon S3 CSI Driver](#mountpoint-for-s3-add-on)  | 
| Enable the use of snapshot functionality in compatible CSI drivers, such as the Amazon EBS CSI driver |  [CSI snapshot controller](#addons-csi-snapshot-controller)  | 
| Secure, production\-ready, AWS supported distribution of the OpenTelemetry project |  [AWS Distro for OpenTelemetry](#add-ons-adot)  | 
| Security monitoring service that analyzes and processes foundational data sources including AWS CloudTrail management events and Amazon VPC flow logs\. Amazon GuardDuty also processes features, such as Kubernetes audit logs and runtime monitoring |  [Amazon GuardDuty agent](#add-ons-guard-duty)  | 
| Monitoring and observability service provided by AWS\. This add\-on installs the CloudWatch Agent and enables both CloudWatch Application Signals and CloudWatch Container Insights with enhanced observability for Amazon EKS |  [Amazon CloudWatch Observability agent](#amazon-cloudwatch-observability)  | 
| Ability to manage credentials for your applications, similar to the way that EC2 instance profiles provide credentials to EC2 instances |  [EKS Pod Identity Agent](#add-ons-pod-id)  | 

## Amazon VPC CNI plugin for Kubernetes<a name="add-ons-vpc-cni"></a>

The Amazon VPC CNI plugin for Kubernetes Amazon EKS add\-on is a Kubernetes container network interface \(CNI\) plugin that provides native VPC networking for your cluster\. The self\-managed or managed type of this add\-on is installed on each Amazon EC2 node, by default\. For more information, see [Kubernetes container network interface \(CNI\) plugin](https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)\.

The Amazon EKS add\-on name is `vpc-cni`\.

### Required IAM permissions<a name="add-ons-vpc-cni-iam-permissions"></a>

This add\-on uses the [IAM roles for service accounts](iam-roles-for-service-accounts.md#iam-roles-for-service-accounts.title) capability of Amazon EKS\. If your cluster uses the `IPv4` family, the permissions in the [AmazonEKS\_CNI\_Policy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKS_CNI_Policy.html) are required\. If your cluster uses the `IPv6` family, you must [create an IAM policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html) with the permissions in [IPv6 mode](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/docs/iam-policy.md#ipv6-mode)\. You can create an IAM role, attach one of the policies to it, and annotate the Kubernetes service account used by the add\-on with the following command\. 

Replace `my-cluster` with the name of your cluster and `AmazonEKSVPCCNIRole` with the name for your role\. If your cluster uses the `IPv6` family, then replace `AmazonEKS_CNI_Policy` with the name of the policy that you created\. This command requires that you have [https://eksctl.io](https://eksctl.io) installed on your device\. If you need to use a different tool to create the role, attach the policy to it, and annotate the Kubernetes service account, see [Assign IAM roles to Kubernetes service accounts](associate-service-account-role.md)\.

```
eksctl create iamserviceaccount --name aws-node --namespace kube-system --cluster my-cluster --role-name AmazonEKSVPCCNIRole \
    --role-only --attach-policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy --approve
```

### Update information<a name="add-ons-vpc-cni-update-information"></a>

You can only update one minor version at a time\. For example, if your current version is `1.28.x-eksbuild.y` and you want to update to `1.30.x-eksbuild.y`, then you must update your current version to `1.29.x-eksbuild.y` and then update it again to `1.30.x-eksbuild.y`\. For more information about updating the add\-on, see [Updating the Amazon VPC CNI plugin for Kubernetes Amazon EKS add\-on](vpc-add-on-update.md)\.

## CoreDNS<a name="add-ons-coredns"></a>

The CoreDNS Amazon EKS add\-on is a flexible, extensible DNS server that can serve as the Kubernetes cluster DNS\. The self\-managed or managed type of this add\-on was installed, by default, when you created your cluster\. When you launch an Amazon EKS cluster with at least one node, two replicas of the CoreDNS image are deployed by default, regardless of the number of nodes deployed in your cluster\. The CoreDNS Pods provide name resolution for all Pods in the cluster\. You can deploy the CoreDNS Pods to Fargate nodes if your cluster includes an [Define which Pods use AWS Fargate when launched](fargate-profile.md) with a namespace that matches the namespace for the CoreDNS `deployment`\.

The Amazon EKS add\-on name is `coredns`\.

### Required IAM permissions<a name="add-ons-coredns-iam-permissions"></a>

This add\-on doesn't require any permissions\.

### Additional information<a name="add-ons-coredns-information"></a>

To learn more about CoreDNS, see [Using CoreDNS for Service Discovery](https://kubernetes.io/docs/tasks/administer-cluster/coredns/) and [Customizing DNS Service](https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/) in the Kubernetes documentation\.

## `Kube-proxy`<a name="add-ons-kube-proxy"></a>

The `Kube-proxy` Amazon EKS add\-on maintains network rules on each Amazon EC2 node\. It enables network communication to your Pods\. The self\-managed or managed type of this add\-on is installed on each Amazon EC2 node in your cluster, by default\.

The Amazon EKS add\-on name is `kube-proxy`\.

### Required IAM permissions<a name="add-ons-kube-proxy-iam-permissions"></a>

This add\-on doesn't require any permissions\.

### Update information<a name="add-ons-kube-proxy-update-information"></a>

Before updating your current version, consider the following requirements:
+ `Kube-proxy` on an Amazon EKS cluster has the same [compatibility and skew policy as Kubernetes](https://kubernetes.io/releases/version-skew-policy/#kube-proxy)\.

### Additional information<a name="add-ons-kube-proxy-information"></a>

To learn more about `kube-proxy`, see [https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/) in the Kubernetes documentation\.

## Amazon EBS CSI driver<a name="add-ons-aws-ebs-csi-driver"></a>

The Amazon EBS CSI driver Amazon EKS add\-on is a Kubernetes Container Storage Interface \(CSI\) plugin that provides Amazon EBS storage for your cluster\.

The Amazon EKS add\-on name is `aws-ebs-csi-driver`\.

### Required IAM permissions<a name="add-ons-aws-ebs-csi-driver-iam-permissions"></a>

This add\-on utilizes the [IAM roles for service accounts](iam-roles-for-service-accounts.md#iam-roles-for-service-accounts.title) capability of Amazon EKS\. The permissions in the [https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEBSCSIDriverPolicy.html](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEBSCSIDriverPolicy.html) AWS managed policy are required\. You can create an IAM role and attach the managed policy to it with the following command\. Replace `my-cluster` with the name of your cluster and `AmazonEKS_EBS_CSI_DriverRole` with the name for your role\. This command requires that you have [https://eksctl.io](https://eksctl.io) installed on your device\. If you need to use a different tool or you need to use a custom [KMS key](https://aws.amazon.com/kms/) for encryption, see [Step 1: Create an IAM role](ebs-csi.md#csi-iam-role)\.

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

### Additional information<a name="add-ons-aws-ebs-csi-driver-information"></a>

To learn more about the add\-on, see [Store Kubernetes volumes with Amazon EBS](ebs-csi.md)\.

## Amazon EFS CSI driver<a name="add-ons-aws-efs-csi-driver"></a>

The Amazon EFS CSI driver Amazon EKS add\-on is a Kubernetes Container Storage Interface \(CSI\) plugin that provides Amazon EFS storage for your cluster\.

The Amazon EKS add\-on name is `aws-efs-csi-driver`\.

### Required IAM permissions<a name="add-ons-aws-efs-csi-driver-iam-permissions"></a>

**Required IAM permissions** – This add\-on utilizes the [IAM roles for service accounts](iam-roles-for-service-accounts.md#iam-roles-for-service-accounts.title) capability of Amazon EKS\. The permissions in the [https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEFSCSIDriverPolicy.html](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEFSCSIDriverPolicy.html) AWS managed policy are required\. You can create an IAM role and attach the managed policy to it with the following commands\. Replace `my-cluster` with the name of your cluster and `AmazonEKS_EFS_CSI_DriverRole` with the name for your role\. These commands require that you have [https://eksctl.io](https://eksctl.io) installed on your device\. If you need to use a different tool, see [Step 1: Create an IAM role](efs-csi.md#efs-create-iam-resources)\.

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

### Additional information<a name="add-ons-aws-efs-csi-driver-information"></a>

To learn more about the add\-on, see [Store an elastic file system with Amazon EFS](efs-csi.md)\.

## Mountpoint for Amazon S3 CSI Driver<a name="mountpoint-for-s3-add-on"></a>

The Mountpoint for Amazon S3 CSI Driver Amazon EKS add\-on is a Kubernetes Container Storage Interface \(CSI\) plugin that provides Amazon S3 storage for your cluster\.

The Amazon EKS add\-on name is `aws-mountpoint-s3-csi-driver`\.

### Required IAM permissions<a name="add-ons-mountpoint-for-s3-add-on-iam-permissions"></a>

This add\-on uses the [IAM roles for service accounts](iam-roles-for-service-accounts.md#iam-roles-for-service-accounts.title) capability of Amazon EKS\. The IAM role that is created will require a policy that gives access to S3\. Follow the [Mountpoint IAM permissions recommendations](https://github.com/awslabs/mountpoint-s3/blob/main/doc/CONFIGURATION.md#iam-permissions) when creating the policy\. Alternatively, you may use the AWS managed policy [https://console.aws.amazon.com/iam/home?#/policies/arn:aws:iam::aws:policy/AmazonS3FullAccess$jsonEditor](https://console.aws.amazon.com/iam/home?#/policies/arn:aws:iam::aws:policy/AmazonS3FullAccess$jsonEditor), but this managed policy grants more permissions than are needed for Mountpoint\. 

You can create an IAM role and attach your policy to it with the following commands\. Replace *my\-cluster* with the name of your cluster, **region\-code** with the correct AWS Region code, *AmazonEKS\_S3\_CSI\_DriverRole* with the name for your role, and *AmazonEKS\_S3\_CSI\_DriverRole\_ARN* with the role ARN\. These commands require that you have [https://eksctl.io](https://eksctl.io) installed on your device\. For instructions on using the IAM console or AWS CLI, see [Create an IAM role](s3-csi.md#s3-create-iam-role)\.

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

### Additional information<a name="add-ons-mountpoint-for-s3-add-on-information"></a>

To learn more about the add\-on, see [Access Amazon S3 objects with Mountpoint for Amazon S3 CSI driver](s3-csi.md)\.

## CSI snapshot controller<a name="addons-csi-snapshot-controller"></a>

The Container Storage Interface \(CSI\) snapshot controller enables the use of snapshot functionality in compatible CSI drivers, such as the Amazon EBS CSI driver\.

The Amazon EKS add\-on name is `snapshot-controller`\.

### Required IAM permissions<a name="add-ons-csi-snapshot-controller-iam-permissions"></a>

 This add\-on doesn't require any permissions\.

### Additional information<a name="add-ons-csi-snapshot-controller-information"></a>

To learn more about the add\-on, see [Enable snapshot functionality for CSI volumes](csi-snapshot-controller.md)\.

## AWS Distro for OpenTelemetry<a name="add-ons-adot"></a>

The AWS Distro for OpenTelemetry Amazon EKS add\-on is a secure, production\-ready, AWS supported distribution of the OpenTelemetry project\. For more information, see [AWS Distro for OpenTelemetry](https://aws-otel.github.io/) on GitHub\.

The Amazon EKS add\-on name is `adot`\.

### Required IAM permissions<a name="add-ons-adot-iam-permissions"></a>

This add\-on only requires IAM permissions if you're using one of the preconfigured custom resources that can be opted into through advanced configuration\.

### Additional information<a name="add-ons-adot-information"></a>

For more information, see [Getting Started with AWS Distro for OpenTelemetry using EKS Add\-Ons](https://aws-otel.github.io/docs/getting-started/adot-eks-add-on) in the AWS Distro for OpenTelemetry documentation\.

ADOT requires that `cert-manager` is deployed on the cluster as a prerequisite, otherwise this add\-on won't work if deployed directly using the [Amazon EKS Terraform](https://registry.terraform.io/modules/terraform-aws-modules/eks/aws/latest) `cluster_addons` property\. For more requirements, see [Requirements for Getting Started with AWS Distro for OpenTelemetry using EKS Add\-Ons](https://aws-otel.github.io/docs/getting-started/adot-eks-add-on/requirements) in the AWS Distro for OpenTelemetry documentation\.

## Amazon GuardDuty agent<a name="add-ons-guard-duty"></a>

The Amazon GuardDuty agent Amazon EKS add\-on is a security monitoring service that analyzes and processes [foundational data sources](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_data-sources.html) including AWS CloudTrail management events and Amazon VPC flow logs\. Amazon GuardDuty also processes [features](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty-features-activation-model.html), such as Kubernetes audit logs and runtime monitoring\.

The Amazon EKS add\-on name is `aws-guardduty-agent`\.

### Required IAM permissions<a name="add-ons-guard-duty-iam-permissions"></a>

This add\-on doesn't require any permissions\.

### Additional information<a name="add-ons-guard-duty-information"></a>

For more information, see [Runtime Monitoring for Amazon EKS clusters in Amazon GuardDuty](https://docs.aws.amazon.com/guardduty/latest/ug/how-runtime-monitoring-works-eks.html)\.
+ To detect potential security threats in your Amazon EKS clusters, enable Amazon GuardDuty runtime monitoring and deploy the GuardDuty security agent to your Amazon EKS clusters\.

## Amazon CloudWatch Observability agent<a name="amazon-cloudwatch-observability"></a>

The Amazon CloudWatch Observability agent Amazon EKS add\-on the monitoring and observability service provided by AWS\. This add\-on installs the CloudWatch Agent and enables both CloudWatch Application Signals and CloudWatch Container Insights with enhanced observability for Amazon EKS\. For more information, see [Amazon CloudWatch Agent](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent.html)\.

The Amazon EKS add\-on name is `amazon-cloudwatch-observability`\.

### Required IAM permissions<a name="amazon-cloudwatch-observability-iam-permissions"></a>

This add\-on uses the [IAM roles for service accounts](iam-roles-for-service-accounts.md#iam-roles-for-service-accounts.title) capability of Amazon EKS\. The permissions in the [AWSXrayWriteOnlyAccess](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AWSXrayWriteOnlyAccess) and [CloudWatchAgentServerPolicy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy) AWS managed policies are required\. You can create an IAM role, attach the managed policies to it, and annotate the Kubernetes service account used by the add\-on with the following command\. Replace `my-cluster` with the name of your cluster and `AmazonEKS_Observability_role` with the name for your role\. This command requires that you have [https://eksctl.io](https://eksctl.io) installed on your device\. If you need to use a different tool to create the role, attach the policy to it, and annotate the Kubernetes service account, see [Assign IAM roles to Kubernetes service accounts](associate-service-account-role.md)\.

```
eksctl create iamserviceaccount \
    --name cloudwatch-agent \
    --namespace amazon-cloudwatch \
    --cluster my-cluster \
    --role-name AmazonEKS_Observability_Role \
    --role-only \
    --attach-policy-arn arn:aws:iam::aws:policy/AWSXrayWriteOnlyAccess \
    --attach-policy-arn arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy \
    --approve
```

### Additional information<a name="amazon-cloudwatch-observability-information"></a>

For more information, see [Install the CloudWatch agent](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/install-CloudWatch-Observability-EKS-addon.html)\.

## EKS Pod Identity Agent<a name="add-ons-pod-id"></a>

The Amazon EKS Pod Identity Agent Amazon EKS add\-on provides the ability to manage credentials for your applications, similar to the way that EC2 instance profiles provide credentials to EC2 instances\.

The Amazon EKS add\-on name is `eks-pod-identity-agent`\.

### Required IAM permissions<a name="add-ons-pod-id-iam-permissions"></a>

This add\-on users permissions from the [Amazon EKS node IAM role](create-node-role.md)\.

### Update information<a name="add-ons-pod-id-update-information"></a>

You can only update one minor version at a time\. For example, if your current version is `1.28.x-eksbuild.y` and you want to update to `1.30.x-eksbuild.y`, then you must update your current version to `1.29.x-eksbuild.y` and then update it again to `1.30.x-eksbuild.y`\. For more information about updating the add\-on, see [Updating the Amazon VPC CNI plugin for Kubernetes Amazon EKS add\-on](vpc-add-on-update.md)\.