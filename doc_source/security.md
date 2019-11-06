# Security in Amazon EKS<a name="security"></a>

Cloud security at AWS is the highest priority\. As an AWS customer, you benefit from a data center and network architecture that is built to meet the requirements of the most security\-sensitive organizations\.

Security is a shared responsibility between AWS and you\. The [shared responsibility model](http://aws.amazon.com/compliance/shared-responsibility-model/) describes this as security *of* the cloud and security *in* the cloud:
+ **Security of the cloud** – AWS is responsible for protecting the infrastructure that runs AWS services in the AWS Cloud\. For Amazon EKS, AWS is responsible for the Kubernetes control plane, which includes the control plane nodes and `etcd` database\. Third\-party auditors regularly test and verify the effectiveness of our security as part of the [AWS compliance programs](http://aws.amazon.com/compliance/programs/)\. To learn about the compliance programs that apply to Amazon EKS, see [AWS Services in Scope by Compliance Program](http://aws.amazon.com/compliance/services-in-scope/)\.
+ **Security in the cloud** – Your responsibility includes the following areas\.
  + The security configuration of the data plane, including the configuration of the security groups that allow traffic to pass from the Amazon EKS control plane into the customer VPC
  + The configuration of the worker nodes and the containers themselves
  + The worker node guest operating system \(including updates and security patches\)
  + Other associated application software:
    + Setting up and managing network controls, such as firewall rules
    + Managing platform\-level identity and access management, either with or in addition to IAM
  + The sensitivity of your data, your company’s requirements, and applicable laws and regulations 

This documentation helps you understand how to apply the shared responsibility model when using Amazon EKS\. The following topics show you how to configure Amazon EKS to meet your security and compliance objectives\. You also learn how to use other AWS services that help you to monitor and secure your Amazon EKS resources\. 

**Topics**
+ [Identity and Access Management for Amazon EKS](security-iam.md)
+ [Logging and Monitoring in Amazon EKS](logging-monitoring.md)
+ [Compliance Validation for Amazon EKS](compliance.md)
+ [Resilience in Amazon EKS](disaster-recovery-resiliency.md)
+ [Infrastructure Security in Amazon EKS](infrastructure-security.md)
+ [Configuration and Vulnerability Analysis in Amazon EKS](configuration-vulnerability-analysis.md)
+ [Pod Security Policy](pod-security-policy.md)