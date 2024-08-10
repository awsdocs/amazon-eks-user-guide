# View control plane raw metrics in Prometheus format<a name="view-raw-metrics"></a>

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