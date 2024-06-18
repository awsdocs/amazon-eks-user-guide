# Security in Amazon EKS<a name="security"></a>

Cloud security at AWS is the highest priority\. As an AWS customer, you benefit from a data center and network architecture that is built to meet the requirements of the most security\-sensitive organizations\.

Security is a shared responsibility between AWS and you\. The [shared responsibility model](https://aws.amazon.com/compliance/shared-responsibility-model/) describes this as security *of* the cloud and security *in* the cloud:
+ **Security of the cloud** – AWS is responsible for protecting the infrastructure that runs AWS services in the AWS Cloud\. For Amazon EKS, AWS is responsible for the Kubernetes control plane, which includes the control plane nodes and `etcd` database\. Third\-party auditors regularly test and verify the effectiveness of our security as part of the [AWS compliance programs](https://aws.amazon.com/compliance/programs/)\. To learn about the compliance programs that apply to Amazon EKS, see [AWS Services in Scope by Compliance Program](https://aws.amazon.com/compliance/services-in-scope/)\.
+ **Security in the cloud** – Your responsibility includes the following areas\.
  + The security configuration of the data plane, including the configuration of the security groups that allow traffic to pass from the Amazon EKS control plane into the customer VPC
  + The configuration of the nodes and the containers themselves
  + The node's operating system \(including updates and security patches\)
  + Other associated application software:
    + Setting up and managing network controls, such as firewall rules
    + Managing platform\-level identity and access management, either with or in addition to IAM
  + The sensitivity of your data, your company's requirements, and applicable laws and regulations

This documentation helps you understand how to apply the shared responsibility model when using Amazon EKS\. The following topics show you how to configure Amazon EKS to meet your security and compliance objectives\. You also learn how to use other AWS services that help you to monitor and secure your Amazon EKS resources\.

**Note**  
Linux containers are made up of control groups \(cgroups\) and namespaces that help limit what a container can access, but all containers share the same Linux kernel as the host Amazon EC2 instance\. Running a container as the root user \(UID 0\) or granting a container access to host resources or namespaces such as the host network or host PID namespace are strongly discouraged, because doing so reduces the effectiveness of the isolation that containers provide\.

**Topics**
+ [Certificate signing](cert-signing.md)
+ [Identity and access management for Amazon EKS](security-iam.md)
+ [Compliance validation for Amazon Elastic Kubernetes Service](compliance.md)
+ [Resilience in Amazon EKS](disaster-recovery-resiliency.md)
+ [Infrastructure security in Amazon EKS](infrastructure-security.md)
+ [Configuration and vulnerability analysis in Amazon EKS](configuration-vulnerability-analysis.md)
+ [Security best practices for Amazon EKS](security-best-practices.md)
+ [Pod security policy](pod-security-policy.md)
+ [Pod security policy \(PSP\) removal FAQ](pod-security-policy-removal-faq.md)
+ [Using AWS Secrets Manager secrets with Kubernetes](manage-secrets.md)
+ [Amazon EKS Connector considerations](security-connector.md)