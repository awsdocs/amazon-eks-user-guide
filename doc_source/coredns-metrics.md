# CoreDNS metrics<a name="coredns-metrics"></a>

CoreDNS as an EKS add\-on exposes the metrics from CoreDNS on port `9153` in the Prometheus format in the `kube-dns` service\. You can use Prometheus, the Amazon CloudWatch agent, or any other compatible system to scrape \(collect\) these metrics\.

For an example *scrape configuration* that is compatible with both Prometheus and the CloudWatch agent, see [CloudWatch agent configuration for Prometheus](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContainerInsights-Prometheus-Setup-configure.html) in the *Amazon CloudWatch User Guide*\.