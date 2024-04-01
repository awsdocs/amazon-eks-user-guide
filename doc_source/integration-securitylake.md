# Using Amazon Security Lake with Amazon EKS<a name="integration-securitylake"></a>

Amazon Security Lake is a fully managed security data lake service that allows you to centralize security data from various sources, including Amazon EKS\. By integrating Amazon EKS with Security Lake, you can gain deeper insights into the activities performed on your Kubernetes resources and enhance the security posture of your Amazon EKS clusters\.

**Note**  
For more information about using Security Lake with Amazon EKS and setting up data sources, refer to the [Amazon Security Lake documentation](https://docs.aws.amazon.com/security-lake/latest/userguide/internal-sources.html#eks-eudit-logs)\.

## Benefits of using Security Lake with Amazon Amazon EKS<a name="sl-benefits"></a>

**Centralized security data** — Security Lake automatically collects and centralizes security data from your Amazon EKS clusters, along with data from other AWS services, SaaS providers, on\-premises sources, and third\-party sources\. This provides a comprehensive view of your security posture across your entire organization\.

**Standardized data format** — Security Lake converts the collected data into the [Open Cybersecurity Schema Framework \(OCSF\) format](https://docs.aws.amazon.com/security-lake/latest/userguide/open-cybersecurity-schema-framework.html), which is a standard open\-source schema\. This normalization enables easier analysis and integration with other security tools and services\.

**Improved threat detection** — By analyzing the centralized security data, including Amazon EKS control plane logs, you can detect potentially suspicious activities within your Amazon EKS clusters more effectively\. This helps in identifying and responding to security incidents promptly\.

**Simplified data management** — Security Lake manages the lifecycle of your security data with customizable retention and replication settings\. This simplifies data management tasks and ensures that you retain the necessary data for compliance and auditing purposes\.

## Enabling Security Lake for Amazon EKS<a name="sl-enable"></a>

**To start using Security Lake with Amazon EKS, follow these steps:**

1. Enable Amazon EKS control plane logging for your EKS clusters\. Refer to [Enabling and disabling control plane logs](control-plane-logs.md#enabling-control-plane-log-export) for detailed instructions\.

1. [Add Amazon EKS Audit Logs as a source in Security Lake\.](https://docs.aws.amazon.com/security-lake/latest/userguide/internal-sources.html#add-internal-sources) Security Lake will then start collecting in\-depth information about the activities performed on the Kubernetes resources running in your EKS clusters\.

1. [Configure retention and replication settings](https://docs.aws.amazon.com/security-lake/latest/userguide/lifecycle-management.html) for your security data in Security Lake based on your requirements\.

1. Use the normalized OCSF data stored in Security Lake for incident response, security analytics, and integration with other AWS services or third\-party tools\. For example, you can [Generate security insights from Amazon Security Lake data using Amazon OpenSearch Ingestion](https://aws.amazon.com/blogs/big-data/generate-security-insights-from-amazon-security-lake-data-using-amazon-opensearch-ingestion/)\.

## Analyzing EKS Logs in Security Lake<a name="sl-format"></a>

Security Lake normalizes EKS log events to the OCSF format, making it easier to analyze and correlate the data with other security events\. You can use various tools and services, such as Amazon Athena, Amazon QuickSight, or third\-party security analytics tools, to query and visualize the normalized data\.

For more information about the OCSF mapping for EKS log events, refer to the [mapping reference](https://github.com/ocsf/examples/tree/main/mappings/markdown/AWS/v1.1.0/EKS Audit Logs) in the OCSF GitHub repository\.