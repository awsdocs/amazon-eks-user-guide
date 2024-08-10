# Monitor your cluster metrics with Prometheus<a name="prometheus"></a>

[https://prometheus.io/](https://prometheus.io/) is a monitoring and time series database that scrapes endpoints\. It provides the ability to query, aggregate, and store collected data\. You can also use it for alerting and alert aggregation\. This topic explains how to set up Prometheus as either a managed or open source option\. Monitoring Amazon EKS control plane metrics is a common use case\.

Amazon Managed Service for Prometheus is a Prometheus\-compatible monitoring and alerting service that makes it easy to monitor containerized applications and infrastructure at scale\. It is a fully\-managed service that automatically scales the ingestion, storage, querying, and alerting of your metrics\. It also integrates with AWS security services to enable fast and secure access to your data\. You can use the open\-source PromQL query language to query your metrics and alert on them\. Also, you can use alert manager in Amazon Managed Service for Prometheus to set up alerting rules for critical alerts\. You can then send these critical alerts as notifications to an Amazon SNS topic\.

For more information about how to use the Prometheus metrics after you turn them on, see the [https://docs.aws.amazon.com/prometheus/latest/userguide/what-is-Amazon-Managed-Service-Prometheus.html](https://docs.aws.amazon.com/prometheus/latest/userguide/what-is-Amazon-Managed-Service-Prometheus.html)\.

There are several different options for using Prometheus with Amazon EKS:
+ You can turn on Prometheus metrics when first creating an Amazon EKS cluster, which is covered by this topic\.
+ If you already have an existing Amazon EKS cluster, you can create your own Prometheus scraper\. For more information, see [https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-collector-how-to.html#AMP-collector-create](https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-collector-how-to.html#AMP-collector-create)\.
+ You can deploy Prometheus using Helm\. For more information, see [Deploy Prometheus using Helm](deploy-prometheus.md)\.
+ You can view control plane raw metrics in Prometheus format\. For more information, see [View control plane raw metrics in Prometheus format](view-raw-metrics.md)\.

## Step 1: Turn on Prometheus metrics when creating a cluster<a name="turn-on-prometheus-metrics"></a>

**Important**  
Amazon Managed Service for Prometheus resources are outside of the cluster lifecycle and need to be maintained independent of the cluster\. When you delete your cluster, make sure to also delete any applicable scrapers to stop applicable costs\. For more information, see [Find and delete scrapers](https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-collector-how-to.html#AMP-collector-list-delete) in the *Amazon Managed Service for Prometheus User Guide*\.

When you create a new cluster, you can turn on the option to send metrics to Prometheus\. In the AWS Management Console, this option is in the **Configure observability** step of creating a new cluster\. For more information, see [Create an Amazon EKS cluster](create-cluster.md)\.

Prometheus discovers and collects metrics from your cluster through a pull\-based model called scraping\. Scrapers are set up to gather data from your cluster infrastructure and containerized applications\. 

When you turn on the option to send Prometheus metrics, Amazon Managed Service for Prometheus provides a fully managed agentless scraper\. Use the following **Advanced configuration** options to customize the default scraper as needed\.

Scraper alias  
\(Optional\) Enter a unique alias for the scraper\.

Destination  
Choose an Amazon Managed Service for Prometheus workspace\. A workspace is a logical space dedicated to the storage and querying of Prometheus metrics\. With this workspace, you will be able to view Prometheus metrics across the accounts that have access to it\. The **Create new workspace** option tells Amazon EKS to create a workspace on your behalf using the **Workspace alias** you provide\. With the **Select existing workspace** option, you can select an existing workspace from a dropdown list\. For more information about workspaces, see [Managing workspaces](https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-manage-ingest-query.html) in the *Amazon Managed Service for Prometheus User Guide*\.

Service access  
This section summarizes the permissions you grant when sending Prometheus metrics:  
+ Allow Amazon Managed Service for Prometheus to describe the scraped Amazon EKS cluster
+ Allow remote writing to the Amazon Managed Prometheus workspace
If the `AmazonManagedScraperRole` already exists, the scraper uses it\. Choose the `AmazonManagedScraperRole` link to see the **Permission details**\. If the `AmazonManagedScraperRole` doesn’t exist already, choose the **View permission** details link to see the specific permissions you are granting by sending Prometheus metrics\.

Subnets  
View the subnets that the scraper will inherit\. If you need to change them, go back to the create cluster **Specify networking** step\.

Security groups  
View the security groups that the scraper will inherit\. If you need to change them, go back to the create cluster **Specify networking** step\.

Scraper configuration  
Modify the scraper configuration in YAML format as needed\. To do so, use the form or upload a replacement YAML file\. For more information, see [Scraper configuration](https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-collector-how-to.html#AMP-collector-configuration) in the *Amazon Managed Service for Prometheus User Guide*\.

Amazon Managed Service for Prometheus refers to the agentless scraper that is created alongside the cluster as an AWS managed collector\. For more information about AWS managed collectors, see [AWS managed collectors](https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-collector.html) in the *Amazon Managed Service for Prometheus User Guide*\.

**Important**  
You must set up your `aws-auth` `ConfigMap` to give the scraper in\-cluster permissions\. For more information, see [Configuring your Amazon EKS cluster](https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-collector-how-to.html#AMP-collector-eks-setup) in the *Amazon Managed Service for Prometheus User Guide*\.

## Step 2: View Prometheus scraper details<a name="viewing-prometheus-scraper-details"></a>

After creating a cluster with the Prometheus metrics option turned on, you can view your Prometheus scraper details\. When viewing your cluster in the AWS Management Console, choose the **Observability ** tab\. A table shows a list of scrapers for the cluster, including information such as the scraper ID, alias, status, and creation date\.

To see more details about the scraper, choose a scraper ID link\. For example, you can view the scraper configuration, Amazon Resource Name \(ARN\), remote write URL, and networking information\. You can use the scraper ID as input to Amazon Managed Service for Prometheus API operations like `DescribeScraper` and `DeleteScraper`\. You can also use the API to create more scrapers\.

For more information on using the Prometheus API, see the [Amazon Managed Service for Prometheus API Reference](https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-APIReference.html)\.