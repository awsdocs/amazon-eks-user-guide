# Available Amazon EKS add\-ons from AWS<a name="workloads-add-ons-available-eks"></a>

The following Amazon EKS add\-ons are available to create on your cluster\. You can view the most current list of available add\-ons using `eksctl`, the AWS Management Console, or the AWS CLI\. To see all available add\-ons or to install an add\-on, see [Creating an Amazon EKS add\-on](creating-an-add-on.md)\. If an add\-on requires IAM permissions, then you must have an IAM OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\. You can [update](updating-an-add-on.md) or [delete](removing-an-add-on.md) an add\-on after you've installed it\. 

You can use any of the following Amazon EKS add\-ons\.


| Description | Learn more | 
| --- | --- | 
|  Provide native VPC networking for your cluster  |  [Amazon VPC CNI plugin for Kubernetes](add-ons-vpc-cni.md)  | 
|  A flexible, extensible DNS server that can serve as the Kubernetes cluster DNS  |  [CoreDNS](add-ons-coredns.md)  | 
| Maintain network rules on each Amazon EC2 node |  [`Kube-proxy`](add-ons-kube-proxy.md)  | 
| Provide Amazon EBS storage for your cluster |  [Amazon EBS CSI driver](add-ons-aws-ebs-csi-driver.md)  | 
| Provide Amazon EFS storage for your cluster |  [Amazon EFS CSI driver](add-ons-aws-efs-csi-driver.md)  | 
| Provide Amazon S3 storage for your cluster |  [Mountpoint for Amazon S3 CSI Driver](mountpoint-for-s3-add-on.md)  | 
| Enable the use of snapshot functionality in compatible CSI drivers, such as the Amazon EBS CSI driver |  [CSI snapshot controller](addons-csi-snapshot-controller.md)  | 
| Secure, production\-ready, AWS supported distribution of the OpenTelemetry project |  [AWS Distro for OpenTelemetry](add-ons-adot.md)  | 
| Security monitoring service that analyzes and processes foundational data sources including AWS CloudTrail management events and Amazon VPC flow logs\. Amazon GuardDuty also processes features, such as Kubernetes audit logs and runtime monitoring |  [Amazon GuardDuty agent](add-ons-guard-duty.md)  | 
| Monitoring and observability service provided by AWS\. This add\-on installs the CloudWatch Agent and enables both CloudWatch Application Signals and CloudWatch Container Insights with enhanced observability for Amazon EKS |  [Amazon CloudWatch Observability agent](amazon-cloudwatch-observability.md)  | 
| Ability to manage credentials for your applications, similar to the way that EC2 instance profiles provide credentials to EC2 instances |  [EKS Pod Identity Agent](add-ons-pod-id.md)  | 