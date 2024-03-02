# Amazon EKS ended support for `Dockershim`<a name="dockershim-deprecation"></a>

Kubernetes no longer supports `Dockershim`\. The Kubernetes team removed the runtime in Kubernetes version `1.24`\. For more information, see [Kubernetes is Moving on From Dockershim: Commitments and Next Steps](https://kubernetes.io/blog/2022/01/07/kubernetes-is-moving-on-from-dockershim/) on the *Kubernetes Blog*\.

Amazon EKS also ended support for `Dockershim` starting with the Kubernetes version `1.24` release\. Amazon EKS AMIs that are officially published have `containerd` as the only runtime starting with version `1.24`\. This topic covers some details, but more information is available in [All you need to know about moving to containerd on Amazon EKS](https://aws.amazon.com/blogs/containers/all-you-need-to-know-about-moving-to-containerd-on-amazon-eks/)\.

There's a `kubectl` plugin that you can use to see which of your Kubernetes workloads mount the Docker socket volume\. For more information, see [Detector for Docker Socket \(DDS\)](https://github.com/aws-containers/kubectl-detector-for-docker-socket) on GitHub\. Amazon EKS AMIs that run Kubernetes versions that are earlier than `1.24` use Docker as the default runtime\. However, these Amazon EKS AMIs have a bootstrap flag option that you can use to test out your workloads on any supported cluster using `containerd`\. For more information, see [Test migration from Docker to `containerd`](eks-optimized-ami.md#containerd-bootstrap)\.

We will continue to publish AMIs for existing Kubernetes versions until the end of their support date\. For more information, see [Amazon EKS Kubernetes release calendar](kubernetes-versions.md#kubernetes-release-calendar)\. If you require more time to test your workloads on `containerd`, use a supported version before `1.24`\. But, when you want to upgrade official Amazon EKS AMIs to version `1.24` or later, make sure to validate that your workloads run on `containerd`\.

The `containerd` runtime provides more reliable performance and security\. `containerd` is the runtime that's being standardized on across Amazon EKS\. Fargate and Bottlerocket already use `containerd` only\. `containerd` helps to minimize the number of Amazon EKS AMI releases that are required to address `Dockershim` [Common Vulnerabilities and Exposures](https://cve.mitre.org/) \(CVEs\)\. Because `Dockershim` already uses `containerd` internally, you might not need to make any changes\. However, there are some situations where changes might or must be required:
+ You must make changes to applications that mount the Docker socket\. For example, container images that are built with a container are impacted\. Many monitoring tools also mount the Docker socket\. You might need to wait for updates or re\-deploy workloads for runtime monitoring\.
+ You might need to make changes for applications that are reliant on specific Docker settings\. For example, the `HTTPS_PROXY` protocol is no longer supported\. You must update applications that use this protocol\. For more information, see [https://docs.docker.com/engine/reference/commandline/dockerd/](https://docs.docker.com/engine/reference/commandline/dockerd/) in the *Docker Docs*\.
+ If you use the Amazon ECR credential helper to pull images, you must switch to the `kubelet` image credential provider\. For more information, see [Configure a `kubelet` image credential provider](https://kubernetes.io/docs/tasks/kubelet-credential-provider/kubelet-credential-provider/) in the Kubernetes documentation\.
+ Because Amazon EKS `1.24` no longer supports Docker, some flags that the [Amazon EKS bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) previously supported are no longer supported\. Before moving to Amazon EKS `1.24` or later, you must remove any reference to flags that are now unsupported:
  + `--container-runtime dockerd` \(`containerd` is the only supported value\)
  + `--enable-docker-bridge`
  + `--docker-config-json`
+ If you already have Fluentd configured for Container Insights, then you must migrate Fluentd to Fluent Bit before changing to `containerd`\. The Fluentd parsers are configured to only parse log messages in JSON format\. Unlike `dockerd`, the `containerd` container runtime has log messages that aren't in JSON format\. If you don't migrate to Fluent Bit, some of the configured Fluentd's parsers will generate a massive amount of errors inside the Fluentd container\. For more information on migrating, see [Set up Fluent Bit as a DaemonSet to send logs to CloudWatch Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Container-Insights-setup-logs-FluentBit.html)\.
+ If you use a custom AMI and you are upgrading to Amazon EKS `1.24`, then you must make sure that IP forwarding is enabled for your worker nodes\. This setting wasn't needed with Docker but is required for `containerd`\. It is needed to troubleshoot Pod\-to\-Pod, Pod\-to\-external, or Pod\-to\-apiserver network connectivity\.

  To verify this setting on a worker node, run either of the following commands:
  + `sysctl net.ipv4.ip_forward`
  + `cat /proc/sys/net/ipv4/ip_forward`

  If the output is `0`, then run either of the following commands to activate the `net.ipv4.ip_forward` kernel variable:
  + `sysctl -w net.ipv4.ip_forward=1`
  + `echo 1 > /proc/sys/net/ipv4/ip_forward`

  For the setting's activation on Amazon EKS AMIs in the `containerd` runtime, see `[install\-worker\.sh](https://github.com/awslabs/amazon-eks-ami/blob/master/scripts/install-worker.sh)` on GitHub\.

   