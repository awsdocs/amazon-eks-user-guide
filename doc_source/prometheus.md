# Control plane metrics with Prometheus<a name="prometheus"></a>

The Kubernetes API server exposes a number of metrics that are useful for monitoring and analysis\. These metrics are exposed internally through a metrics endpoint that refers to the `/metrics` HTTP API\. Like other endpoints, this endpoint is exposed on the Amazon EKS control plane\. This topic explains some of the ways you can use this endpoint to view and analyze what your cluster is doing\.

## Viewing the raw metrics<a name="view-raw-metrics"></a>

To view the raw metrics output, use `kubectl` with the `--raw` flag\. This command allows you to pass any HTTP path and returns the raw response\.

```
kubectl get --raw /metrics
```

Example output:

```
...
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

This raw output returns verbatim what the API server exposes\. These metrics are represented in a [Prometheus format](https://github.com/prometheus/docs/blob/master/content/docs/instrumenting/exposition_formats.md)\. This format allows the API server to expose different metrics broken down by line\. Each line includes a metric name, tags, and a value\.

```
<metric_name>{"<tag>"="<value>"[<,...>]} <value>
```

While this endpoint is useful if you are looking for a specific metric, you typically want to analyze these metrics over time\. To do this, you can deploy [Prometheus](https://prometheus.io/) into your cluster\. Prometheus is a monitoring and time series database that scrapes exposed endpoints and aggregates data, allowing you to filter, graph, and query the results\.

## Deploying Prometheus<a name="deploy-prometheus"></a>

This topic helps you deploy Prometheus into your cluster with Helm V3\. If you already have Helm installed, you can check your version with the `helm version` command\. Helm is a package manager for Kubernetes clusters\. For more information about Helm and how to install it, see [Using Helm with Amazon EKS](helm.md)\.

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
If you get the error `Error: failed to download "stable/prometheus" (hint: running `helm repo update` may help)` when executing this command, run `helm repo update`, and then try running the Step 3 command again\.  
If you get the error `Error: rendered manifests contain a resource that already exists`, run `helm uninstall your-release-name -n namespace`, then try running the Step 3 command again\.

1. Verify that all of the pods in the `prometheus` namespace are in the `READY` state\.

   ```
   kubectl get pods -n prometheus
   ```

   Output:

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

1. Point a web browser to [localhost:9090](localhost:9090) to view the Prometheus console\.

1. Choose a metric from the **\- insert metric at cursor** menu, then choose **Execute**\. Choose the **Graph** tab to show the metric over time\. The following image shows `container_memory_usage_bytes` over time\.  
![\[Prometheus metrics\]](http://docs.aws.amazon.com/eks/latest/userguide/images/prometheus-metric.png)

1. From the top navigation bar, choose **Status**, then **Targets**\.  
![\[Prometheus console\]](http://docs.aws.amazon.com/eks/latest/userguide/images/prometheus.png)

   All of the Kubernetes endpoints that are connected to Prometheus using service discovery are displayed\.