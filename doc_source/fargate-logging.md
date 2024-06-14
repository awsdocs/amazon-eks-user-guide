--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Fargate logging<a name="fargate-logging"></a>

**Important**  
 AWS Fargate with Amazon EKS isn’t available in AWS GovCloud \(US\-East\) and AWS GovCloud \(US\-West\)\.

Amazon EKS on Fargate offers a built\-in log router based on Fluent Bit\. This means that you don’t explicitly run a Fluent Bit container as a sidecar, but Amazon runs it for you\. All that you have to do is configure the log router\. The configuration happens through a dedicated `ConfigMap` that must meet the following criteria:
+ Named `aws-logging` 
+ Created in a dedicated namespace called `aws-observability` 
+ Can’t exceed 5300 characters\.

Once you’ve created the `ConfigMap`, Amazon EKS on Fargate automatically detects it and configures the log router with it\. Fargate uses a version of AWS for Fluent Bit, an upstream compliant distribution of Fluent Bit managed by AWS\. For more information, see [AWS for Fluent Bit](https://github.com/aws/aws-for-fluent-bit) on GitHub\.

The log router allows you to use the breadth of services at AWS for log analytics and storage\. You can stream logs from Fargate directly to Amazon CloudWatch, Amazon OpenSearch Service\. You can also stream logs to destinations such as [Amazon S3](https://aws.amazon.com/s3/), [Amazon Kinesis Data Streams](https://aws.amazon.com/kinesis/data-streams/), and partner tools through [Amazon Data Firehose](https://aws.amazon.com/kinesis/data-firehose/)\.

## Kubernetes filter support<a name="fargate-logging-kubernetes-filter"></a>

This feature requires the following minimum Kubernetes version and platform level, or later\.

The Fluent Bit Kubernetes filter allows you to add Kubernetes metadata to your log files\. For more information about the filter, see [Kubernetes](https://docs.fluentbit.io/manual/pipeline/filters/kubernetes) in the Fluent Bit documentation\. You can apply a filter using the API server endpoint\.

```
filters.conf: |
    [FILTER]
        Name             kubernetes
        Match            kube.*
        Merge_Log           On
        Buffer_Size         0
        Kube_Meta_Cache_TTL 300s
```

**Important**  
 `Kube_URL`, `Kube_CA_File`, `Kube_Token_Command`, and `Kube_Token_File` are service owned configuration parameters and must not be specified\. Amazon EKS Fargate populates these values\.
 `Kube_Meta_Cache_TTL` is the time Fluent Bit waits until it communicates with the API server for the latest metadata\. If `Kube_Meta_Cache_TTL` isn’t specified, Amazon EKS Fargate appends a default value of 30 minutes to lessen the load on the API server\.

### To ship Fluent Bit process logs to your account<a name="ship-fluent-bit-process-logs"></a>

You can optionally ship Fluent Bit process logs to Amazon CloudWatch using the following `ConfigMap`\. Shipping Fluent Bit process logs to CloudWatch requires additional log ingestion and storage costs\. Replace `[replaceable]`region\-code```` with the AWS Region that your cluster is in\.

```
kind: ConfigMap
apiVersion: v1
metadata:
  name: aws-logging
  namespace: aws-observability
  labels:
data:
  # Configuration files: server, input, filters and output
  # ======================================================
  flb_log_cw: "true"  # Ships Fluent Bit process logs to CloudWatch.

  output.conf: |
    [OUTPUT]
        Name cloudwatch
        Match kube.*
        region region-code
        log_group_name fluent-bit-cloudwatch
        log_stream_prefix from-fluent-bit-
        auto_create_group true
```

The logs are in the AWS Region that the cluster resides in under CloudWatch\. The log group name is ` my-cluster-fluent-bit-logs` and the Fluent Bit logstream name is `fluent-bit-[replaceable]`podname`-[replaceable]`pod\-namespace````\.

**Note**  
The process logs are shipped only when the Fluent Bit process successfully starts\. If there is a failure while starting Fluent Bit, the process logs are missed\. You can only ship process logs to CloudWatch\.
To debug shipping process logs to your account, you can apply the previous `ConfigMap` to get the process logs\. Fluent Bit failing to start is usually due to your `ConfigMap` not being parsed or accepted by Fluent Bit while starting\.

### To stop shipping Fluent Bit process logs<a name="stop-fluent-bit-process-logs"></a>

Shipping Fluent Bit process logs to CloudWatch requires additional log ingestion and storage costs\. To exclude process logs in an existing `ConfigMap` setup, do the following steps\.

1. Locate the CloudWatch log group automatically created for your Amazon EKS cluster’s Fluent Bit process logs after enabling Fargate logging\. It follows the format `{cluster_name}-fluent-bit-logs`\.

1. Delete the existing CloudWatch log streams created for each Pod’s process logs in the CloudWatch log group\.

1. Edit the `ConfigMap` and set `flb_log_cw: "false"`\.

1. Restart any existing Pods in the cluster\.

## Test application<a name="fargate-logging-test-application"></a>

1. Deploy a sample Pod\.

   1. Save the following contents to a file named ` sample-app.yaml` on your computer\.

      ```
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: sample-app
        namespace: same-namespace-as-your-fargate-profile
      spec:
        replicas: 3
        selector:
          matchLabels:
            app: nginx
        template:
          metadata:
            labels:
              app: nginx
          spec:
            containers:
              - name: nginx
                image: nginx:latest
                ports:
                  - name: http
                    containerPort: 80
      ```

   1. Apply the manifest to the cluster\.

      ```
      kubectl apply -f sample-app.yaml
      ```

1. View the NGINX logs using the destination\(s\) that you configured in the `ConfigMap`\.

## Size considerations<a name="fargate-logging-size-considerations"></a>

We suggest that you plan for up to 50 MB of memory for the log router\. If you expect your application to generate logs at very high throughput then you should plan for up to 100 MB\.

## Troubleshooting<a name="fargate-logging-troubleshooting"></a>

To confirm whether the logging feature is enabled or disabled for some reason, such as an invalid `ConfigMap`, and why it’s invalid, check your Pod events with ` `kubectl describe pod [replaceable] ``\. The output might include Pod events that clarify whether logging is enabled or not, such as the following example output\.

```
[...]
Annotations:          CapacityProvisioned: 0.25vCPU 0.5GB
                      Logging: LoggingDisabled: LOGGING_CONFIGMAP_NOT_FOUND
                      kubernetes.io/psp: eks.privileged
[...]
Events:
  Type     Reason           Age        From                                                           Message
  ⁂⁂⁂⁂     ⁂⁂⁂⁂⁂⁂           ⁂⁂⁂⁂       ⁂⁂⁂⁂                                                           ⁂⁂⁂⁂⁂⁂-
  Warning  LoggingDisabled  <unknown>  fargate-scheduler                                              Disabled logging because aws-logging configmap was not found. configmap "aws-logging" not found
```

The Pod events are ephemeral with a time period depending on the settings\. You can also view a Pod’s annotations using ` `kubectl describe pod [replaceable] ``\. In the Pod annotation, there is information about whether the logging feature is enabled or disabled and the reason\.