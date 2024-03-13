# Prometheus metrics<a name="prometheus"></a>

[https://prometheus.io/](https://prometheus.io/) is a monitoring and time series database that scrapes endpoints\. It provides the ability to query, aggregate, and store collected data\. You can also use it for alerting and alert aggregation\. This topic explains how to set up Prometheus as either a managed or open source option\. Monitoring Amazon EKS control plane metrics is a common use case\.

Amazon Managed Service for Prometheus is a Prometheus\-compatible monitoring and alerting service that makes it easy to monitor containerized applications and infrastructure at scale\. It is a fully\-managed service that automatically scales the ingestion, storage, querying, and alerting of your metrics\. It also integrates with AWS security services to enable fast and secure access to your data\. You can use the open\-source PromQL query language to query your metrics and alert on them\.

For more information about how to use the Prometheus metrics after you turn them on, see the [https://docs.aws.amazon.com/prometheus/latest/userguide/what-is-Amazon-Managed-Service-Prometheus.html](https://docs.aws.amazon.com/prometheus/latest/userguide/what-is-Amazon-Managed-Service-Prometheus.html)\.

## Turn on Prometheus metrics when creating a cluster<a name="turn-on-prometheus-metrics"></a>

**Important**  
Amazon Managed Service for Prometheus resources are outside of the cluster lifecycle and need to be maintained independent of the cluster\. When you delete your cluster, make sure to also delete any applicable scrapers to stop applicable costs\. For more information, see [Find and delete scrapers](https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-collector-how-to.html#AMP-collector-list-delete) in the *Amazon Managed Service for Prometheus User Guide*\.

When you create a new cluster, you can turn on the option to send metrics to Prometheus\. In the AWS Management Console, this option is in the **Configure observability** step of creating a new cluster\. For more information, see [Creating an Amazon EKS cluster](create-cluster.md)\.

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

## Viewing Prometheus scraper details<a name="viewing-prometheus-scraper-details"></a>

After creating a cluster with the Prometheus metrics option turned on, you can view your Prometheus scraper details\. When viewing your cluster in the AWS Management Console, choose the **Observability ** tab\. A table shows a list of scrapers for the cluster, including information such as the scraper ID, alias, status, and creation date\.

To see more details about the scraper, choose a scraper ID link\. For example, you can view the scraper configuration, Amazon Resource Name \(ARN\), remote write URL, and networking information\. You can use the scraper ID as input to Amazon Managed Service for Prometheus API operations like `DescribeScraper` and `DeleteScraper`\. You can also use the API to create more scrapers\.

For more information on using the Prometheus API, see the [Amazon Managed Service for Prometheus API Reference](https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-APIReference.html)\.

## Deploying Prometheus using Helm<a name="deploy-prometheus"></a>

Alternatively, you can deploy Prometheus into your cluster with Helm V3\. If you already have Helm installed, you can check your version with the `helm version` command\. Helm is a package manager for Kubernetes clusters\. For more information about Helm and how to install it, see [Using Helm with Amazon EKS](helm.md)\.

After you configure Helm for your Amazon EKS cluster, you can use it to deploy Prometheus with the following steps\.

**To deploy Prometheus using Helm**

1. Create a Prometheus namespace\.

   ```
   kubectl create namespace prometheus
   ```

1. Add the `prometheus-community` chart repository\.

   ```
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   ```

1. Deploy Prometheus\.

   ```
   helm upgrade -i prometheus prometheus-community/prometheus \
       --namespace prometheus \
       --set alertmanager.persistentVolume.storageClass="gp2",server.persistentVolume.storageClass="gp2"
   ```
**Note**  
If you get the error `Error: failed to download "stable/prometheus" (hint: running `helm repo update` may help)` when executing this command, run `helm repo update prometheus-community`, and then try running the Step 2 command again\.  
If you get the error `Error: rendered manifests contain a resource that already exists`, run `helm uninstall your-release-name -n namespace`, then try running the Step 3 command again\.

1. Verify that all of the Pods in the `prometheus` namespace are in the `READY` state\.

   ```
   kubectl get pods -n prometheus
   ```

   An example output is as follows\.

   ```
   NAME                                             READY   STATUS    RESTARTS   AGE
   prometheus-alertmanager-59b4c8c744-r7bgp         1/2     Running   0          48s
   prometheus-kube-state-metrics-7cfd87cf99-jkz2f   1/1     Running   0          48s
   prometheus-node-exporter-jcjqz                   1/1     Running   0          48s
   prometheus-node-exporter-jxv2h                   1/1     Running   0          48s
   prometheus-node-exporter-vbdks                   1/1     Running   0          48s
   prometheus-pushgateway-76c444b68c-82tnw          1/1     Running   0          48s
   prometheus-server-775957f748-mmht9               1/2     Running   0          48s
   ```

1. Use `kubectl` to port forward the Prometheus console to your local machine\.

   ```
   kubectl --namespace=prometheus port-forward deploy/prometheus-server 9090
   ```

1. Point a web browser to `http://localhost:9090` to view the Prometheus console\.

1. Choose a metric from the **\- insert metric at cursor** menu, then choose **Execute**\. Choose the **Graph** tab to show the metric over time\. The following image shows `container_memory_usage_bytes` over time\.  
![\[Prometheus metrics\]](http://docs.aws.amazon.com/eks/latest/userguide/images/prometheus-metric.png)

1. From the top navigation bar, choose **Status**, then **Targets**\.  
![\[Prometheus console\]](http://docs.aws.amazon.com/eks/latest/userguide/images/prometheus.png)

   All of the Kubernetes endpoints that are connected to Prometheus using service discovery are displayed\.

## Viewing the control plane raw metrics<a name="view-raw-metrics"></a>

As an alternative to deploying Prometheus, the Kubernetes API server exposes a number of metrics that are represented in a [Prometheus format](https://github.com/prometheus/docs/blob/master/content/docs/instrumenting/exposition_formats.md)\. These metrics are useful for monitoring and analysis\. They are exposed internally through a metrics endpoint that refers to the `/metrics` HTTP API\. Like other endpoints, this endpoint is exposed on the Amazon EKS control plane\. This endpoint is primarily useful for looking at a specific metric\. To analyze metrics over time, we recommend deploying Prometheus\.

To view the raw metrics output, use `kubectl` with the `--raw` flag\. This command allows you to pass any HTTP path and returns the raw response\.

```
kubectl get --raw /metrics
```

An example output is as follows\.

```
[...]
# HELP rest_client_requests_total Number of HTTP requests, partitioned by status code, method, and host.
# TYPE rest_client_requests_total counter
rest_client_requests_total{code="200",host="127.0.0.1:21362",method="POST"} 4994
rest_client_requests_total{code="200",host="127.0.0.1:443",method="DELETE"} 1
rest_client_requests_total{code="200",host="127.0.0.1:443",method="GET"} 1.326086e+06
rest_client_requests_total{code="200",host="127.0.0.1:443",method="PUT"} 862173
rest_client_requests_total{code="404",host="127.0.0.1:443",method="GET"} 2
rest_client_requests_total{code="409",host="127.0.0.1:443",method="POST"} 3
rest_client_requests_total{code="409",host="127.0.0.1:443",method="PUT"} 8
# HELP ssh_tunnel_open_count Counter of ssh tunnel total open attempts
# TYPE ssh_tunnel_open_count counter
ssh_tunnel_open_count 0
# HELP ssh_tunnel_open_fail_count Counter of ssh tunnel failed open attempts
# TYPE ssh_tunnel_open_fail_count counter
ssh_tunnel_open_fail_count 0
```

This raw output returns verbatim what the API server exposes\. The different metrics are listed by line, with each line including a metric name, tags, and a value\.

```
metric_name{"tag"="value"[,...]}
            value
```