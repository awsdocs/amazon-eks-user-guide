# Fargate logging<a name="fargate-logging"></a>

Amazon EKS on Fargate offers a built\-in log router based on Fluent Bit. This means you do not explicitly run a Fluent Bit container as a sidecar, but Amazon runs it for you and all you have to do is to configure the log router. The configuration happens via a dedicated `ConfigMap` that: 1. MUST be called `aws-logging`, and 2. MUST be placed in a dedicated namespace called `aws-observability`. Once you've created said `ConfigMap`, EKS on Fargate will automatically detect it and configure the log router with it. Fargate uses a version of AWS for Fluent Bit, an upstream compliant distribution of Fluent Bit managed by AWS\. For more information, see [AWS for Fluent Bit](https://github.com/aws/aws-for-fluent-bit) on GitHub\. 

The log router allows you to use the breadth of services at AWS for log analytics and storage\. You can stream logs from Fargate directly to Amazon CloudWatch, Amazon Elasticsearch Service, and Amazon Kinesis Data Firehose destinations such as Amazon S3, Amazon Kinesis Data Streams, and partner tools\. 

**Prerequisites**  
An existing Fargate profile that specifies an existing Kubernetes namespace that you deploy Fargate pods to\. For more information, see [Create a Fargate profile for your cluster](fargate-getting-started.md#fargate-gs-create-profile)\.

**Log router configuration**  

As a preparation, you have to first create the dedicated namespace `aws-observability` that will host the `ConfigMap` named `aws-logging`:

1. Save the following contents to a file named `aws-observability-namespace.yaml` on your computer\.

      ```
      kind: Namespace
      apiVersion: v1
      metadata:
        name: aws-observability
        labels:
          aws-observability: enabled
      ```

1. Create the namespace\.

      ```
      kubectl apply -f aws-observability-namespace.yaml
      ```

To configure the log router, apply a `ConfigMap` to your Amazon EKS cluster with a `Fluent Conf` data value that defines where container logs are shipped to\. `Fluent Conf` is Fluent Bit, which is a fast and lightweight log processor configuration language that is used to route container logs to a log destination of your choice\. For more information, see [Configuration File](https://docs.fluentbit.io/manual/administration/configuring-fluent-bit/configuration-file) in the Fluent Bit documentation\.

NOTE: While in a typical `Fluent Conf` the main sections included are `Service`, `Input`, `Filter`, and `Output`\ the Fargate log router ONLY accepts the `Filter`, `Output`, and `Parser` sections and manages the `Service` and `Input` itself\. In other words: if you do provide any other section than `Filter`, `Output`, and `Parser` those are rejected\. 


When creating the `ConfigMap` you should take the following rules into account that Fargate uses to validate the `Filter`, `Output`, and `Parser` fields:

1. `[FILTER]`, `[OUTPUT],` and `[PARSER]` are supposed to be specified under each corresponding key : `filters.conf`, `output.conf`, and `parsers.conf`\. For example, `[FILTER]` must be under `filters.conf`\. You can have one or more `[FILTER]`s under `filters.conf`\. The same is true for `[OUTPUT]` and `[PARSER]` sections\. For example, by specifying multiple `[OUTPUT]` sections, you can route your logs to different destinations at the same time.

1. Fargate validates the required keys for each section\. `Name` and `match` are required for each `[FILTER]` and `[OUTPUT]`\. `Name` and `format` are required for each `[PARSER]`\. The keys are case\-insensitive\. 

1. Environment variables such as `${ENV_VAR}` are not allowed in the `configmap`\. 

1. The indentation has to be the same for either directive or key\-value pair within each `filters.conf`, `output.conf`, and `parsers.conf`\. Key\-value pairs have to be indented more than directives\. 

1. Fargate validates against the following supported filters: `grep`, `parser`, `record_modifier`, `rewrite_tag`, `throttle`, `nest`, and `modify`\.

1. Fargate validates against the following supported output: `es`, `firehose`, `kinesis_firehose`, `cloudwatch`, `cloudwatch_logs`, and `kinesis`\. 

1. At least one supported `Output` plugin has to be provided in the `ConfigMap` to enable logging\. `Filter` and `Parser` are not required to enable logging\.

For more information about `Fluent Conf` see [Configuration File](https://docs.fluentbit.io/manual/administration/configuring-fluent-bit/configuration-file) in the Fluent Bit documentation\. You can also run Fluent Bit on Amazon EC2 using the desired configuration to troubleshoot any issues that arise from validation\

**To send logs to Amazon CloudWatch**

In the following steps, replace the `<example values>` with your own values\.

You have two output options when using CloudWatch:
      + [https://docs.fluentbit.io/manual/v/1.5/pipeline/outputs/cloudwatch](https://docs.fluentbit.io/manual/v/1.5/pipeline/outputs/cloudwatch) – An output plugin written in C\.
      + [https://github.com/aws/amazon-cloudwatch-logs-for-fluent-bit](https://github.com/aws/amazon-cloudwatch-logs-for-fluent-bit) – An output plugin written in Golang\.

The following example shows you how to use the `cloudwatch_logs` plugin to send logs to CloudWatch\.

      1. Save the following contents to a file named `aws-logging-cloudwatch-configmap.yaml`\.

         ```
         kind: ConfigMap
         apiVersion: v1
         metadata:
           name: aws-logging
           namespace: aws-observability
           labels:
         data:
           output.conf: |
             [OUTPUT]
                 Name cloudwatch_logs
                 Match   *
                 region us-east-1
                 log_group_name example-cloudwatch
                 log_stream_prefix from-fluent-bit-
                 auto_create_group On
         ```

      1. Apply the manifest to your cluster\.

         ```
         kubectl apply -f aws-logging-cloudwatch-configmap.yaml
         ```

      1. Download the CloudWatch IAM policy to your computer\. You can also [view the policy](https://raw.githubusercontent.com/aws-samples/amazon-eks-fluent-logging-examples/mainline/examples/fargate/cloudwatchlogs/permissions.json) on GitHub\.

         ```
         curl -o permissions.json https://raw.githubusercontent.com/aws-samples/amazon-eks-fluent-logging-examples/mainline/examples/fargate/cloudwatchlogs/permissions.json
         ```

**To send logs to Amazon Elasticsearch Service**

If you want to send logs to Amazon Elasticsearch Service, use the [es](https://docs.fluentbit.io/manual/v/1.5/pipeline/outputs/elasticsearch) output, which is a plugin written in C\. The following example shows you how to use the plugin to send logs to Elasticsearch\.

      1. Save the following contents to a file named `aws-logging-elasticsearch-configmap.yaml`\.

         ```
         kind: ConfigMap
         apiVersion: v1
         metadata:
           name: aws-logging
           namespace: aws-observability
           labels:
         data:
           output.conf: |
             [OUTPUT]
               Name  es
               Match *
               Host  search-example-gjxdcilagiprbglqn42jsty66y.eu-west-1.es.amazonaws.com
               Port  443
               Index example
               Type  example_type
               AWS_Auth On
               AWS_Region eu-west-1
               tls   On
         ```

      1. Apply the manifest to your cluster\.

         ```
         kubectl apply -f aws-logging-elasticsearch-configmap.yaml
         ```

      1. Download the Elasticsearch IAM policy to your computer\. You can also [view the policy](https://raw.githubusercontent.com/aws-samples/amazon-eks-fluent-logging-examples/mainline/examples/fargate/amazon-elasticsearch/permissions.json) on GitHub\.

         ```
         curl -o permissions.json https://raw.githubusercontent.com/aws-samples/amazon-eks-fluent-logging-examples/mainline/examples/fargate/amazon-elasticsearch/permissions.json
         ```

NOTE: Make sure that Kibana's access control is configured properly, that is: the `all_access role` in Kibana needs to have the Fargate pod execution role
as well as the IRSA role mapped. Equally, the same mapping must be done for the `security_manager` role. You can add above mappings via "Menu -> Security -> Roles" and then select the respective roles. There is also a [Support article](https://aws.amazon.com/tr/premiumsupport/knowledge-center/es-troubleshoot-cloudwatch-logs/) that has some background on the topic.

**To send logs to Amazon Kinesis Data Firehose**

You have two output options when using Kinesis Data Firehose:
      + [https://docs.fluentbit.io/manual/pipeline/outputs/firehose](https://docs.fluentbit.io/manual/pipeline/outputs/firehose) – An output plugin written in C\.
      + [https://github.com/aws/amazon-kinesis-firehose-for-fluent-bit](https://github.com/aws/amazon-kinesis-firehose-for-fluent-bit) – An output plugin written in Golang\.

The following example shows you how to use the `kinesis_firehose` plugin to send logs to Kinesis Data Firehose\.

      1. Save the following contents to a file named `aws-logging-firehose-configmap.yaml`\.

         ```
         kind: ConfigMap
         apiVersion: v1
         metadata:
           name: aws-logging
           namespace: aws-observability
           labels:
         data:
           output.conf: |
             [OUTPUT]
              Name  kinesis_firehose
              Match *
              region <us-east-1>
              delivery_stream my-stream-firehose
         ```

      1. Apply the manifest to your cluster\.

         ```
         kubectl apply -f aws-logging-firehose-configmap.yaml
         ```

      1. Download the Kinesis Data Firehose IAM policy to your computer\. You can also [view the policy](https://raw.githubusercontent.com/aws-samples/amazon-eks-fluent-logging-examples/mainline/examples/fargate/kinesis-firehose/permissions.json) on GitHub\.

         ```
         curl -o permissions.json https://raw.githubusercontent.com/aws-samples/amazon-eks-fluent-logging-examples/mainline/examples/fargate/kinesis-firehose/permissions.json
         ```

**Configure permissions**

1. Create an IAM policy using one or more of the permissions created for a specific destination such as CloudWatch or AES\.

   ```
   aws iam create-policy --policy-name <eks-fargate-logging-policy> --policy-document file://permissions.json
   ```

1. Attach the IAM policy to the pod execution role specified for your Fargate profile\. Replace `<111122223333>` with your account ID\.

   ```
   aws iam attach-role-policy \
     --policy-arn arn:aws:iam::<111122223333>:policy/<eks-fargate-logging-policy> \
     --role-name <your-pod-execution-role>
   ```

**Test setup**

To test the log routing you can deploy a sample pod as described in the following\.

   1. Save the following contents to a `yaml` file on your computer\.

      ```
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: sample-app
        namespace: <same-namespace-as-your-fargate-profile>
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
      kubectl apply -f <name-of-file-from-previous-step>.yaml
      ```

   1. View the NGINX logs using the destination(s) that you configured in the `ConfigMap`.
   

**Size considerations**  
We suggest that you plan for up to 50 MB of memory for your logs\. If you expect your application to generate logs at very high throughput then you should plan for up to 100 MB\.

**Troubleshooting**  
To confirm whether the logging feature is enabled or disabled for some reason, such as an invalid `ConfigMap`, and why it is invalid, check your pod events with `kubectl describe pod <pod_name>`\. The output might include pod events that clarify whether logging is enabled or not, such as the following example output\.

```
...
Annotations:          CapacityProvisioned: 0.25vCPU 0.5GB
                      Logging: LoggingDisabled: LOGGING_CONFIGMAP_NOT_FOUND
                      kubernetes.io/psp: eks.privileged
...
Events:
  Type     Reason           Age        From                                                           Message
  ----     ------           ----       ----                                                           -------
  Warning  LoggingDisabled  <unknown>  fargate-scheduler                                              Disabled logging because aws-logging configmap was not found. configmap "aws-logging" not found
```

The pod events are ephemeral with a time period depending on the settings\. You can also view a pod's annotations using `kubectl describe pod <pod-name>`\. In the pod annotation, there is information about whether the logging feature is enabled or disabled and the reason\.

 
