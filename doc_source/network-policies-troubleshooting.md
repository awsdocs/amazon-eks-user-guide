# Troubleshooting Kubernetes network policies For Amazon EKS<a name="network-policies-troubleshooting"></a>

You can troubleshoot and investigate network connections that use network policies by reading the [Network policy logs](#network-policies-troubleshooting-flowlogs) and by running tools from the [eBPF SDK](#network-policies-ebpf-sdk)\.

## Network policy logs<a name="network-policies-troubleshooting-flowlogs"></a>

Whether connections are allowed or denied by a network policies is logged in *flow logs*\. The network policy logs on each node include the flow logs for every pod that has a network policy\. Network policy logs are stored at `/var/log/aws-routed-eni/network-policy-agent.log`\. The following example is from a `network-policy-agent.log` file:

```
{"level":"info","timestamp":"2023-05-30T16:05:32.573Z","logger":"ebpf-client","msg":"Flow Info: ","Src
IP":"192.168.87.155","Src Port":38971,"Dest IP":"64.6.160","Dest
Port":53,"Proto":"UDP","Verdict":"ACCEPT"}
```

Network policy logs are disabled by default\. To enable the network policy logs, follow these steps:

**Note**  
Network policy logs require an additional 1 vCPU for the `aws-network-policy-agent` container in the VPC CNI `aws-node` daemonset manifest\.

### Amazon EKS add\-on<a name="cni-network-policy-flowlogs-addon"></a>

------
#### [ AWS Management Console ]

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to configure the Amazon VPC CNI add\-on for\.

1. Choose the **Add\-ons** tab\.

1. Select the box in the top right of the add\-on box and then choose **Edit**\.

1. On the **Configure *name of addon*** page:

   1. Select a `v1.14.0-eksbuild.3` or later version in the **Version** dropdown list\.

   1. Expand the **Optional configuration settings**\.

   1. Enter the top\-level JSON key `"nodeAgent":` and value is an object with a key `"enablePolicyEventLogs":` and value of `"true"` in **Configuration values**\. The resulting text must be a valid JSON object\. The following example shows network policy and the network policy logs are enabled, and the network policy logs are sent to CloudWatch Logs:

      ```
      {
          "enableNetworkPolicy": "true",
          "nodeAgent": {
              "enablePolicyEventLogs": "true"
          }
      }
      ```

The following screenshot shows an example of this scenario\.

![\[\]](http://docs.aws.amazon.com/eks/latest/userguide/images/console-cni-config-network-policy-logs.png)

------
#### [ AWS CLI ]
+ Run the following AWS CLI command\. Replace `my-cluster` with the name of your cluster and replace the IAM role ARN with the role that you are using\.

  ```
  aws eks update-addon --cluster-name my-cluster --addon-name vpc-cni --addon-version v1.14.0-eksbuild.3 \
      --service-account-role-arn arn:aws:iam::123456789012:role/AmazonEKSVPCCNIRole \
      --resolve-conflicts PRESERVE --configuration-values '{"nodeAgent": {"enablePolicyEventLogs": "true"}}'
  ```

------

### Self\-managed add\-on<a name="cni-network-policy-flowlogs-selfmanaged"></a>

------
#### [ Helm ]

If you have installed the Amazon VPC CNI plugin for Kubernetes through `helm`, you can update the configuration to write the network policy logs\.
+ Run the following command to enable network policy\.

  ```
  helm upgrade --set nodeAgent.enablePolicyEventLogs=true aws-vpc-cni --namespace kube-system eks/aws-vpc-cni
  ```

------
#### [ kubectl ]

If you have installed the Amazon VPC CNI plugin for Kubernetes through `kubectl`, you can update the configuration to write the network policy logs\.

1. Open the `aws-node` `DaemonSet` in your editor\.

   ```
   kubectl edit daemonset -n kube-system aws-node
   ```

1. Replace the `false` with `true` in the command argument `--enable-policy-event-logs=false` in the `args:` in the `aws-network-policy-agent` container in the VPC CNI `aws-node` daemonset manifest\.

   ```
        - args:
           - --enable-policy-event-logs=true
   ```

------

## Send network policy logs to Amazon CloudWatch Logs<a name="network-policies-cloudwatchlogs"></a>

You can monitor the network policy logs using services such as Amazon CloudWatch Logs\. You can use the following methods to send the network policy logs to CloudWatch Logs\.

For EKS clusters, the policy logs will be located under `/aws/eks/cluster-name/cluster/` and for self\-managed K8S clusters, the logs will be placed under `/aws/k8s-cluster/cluster`/\.

### Send network policy logs with Amazon VPC CNI plugin for Kubernetes<a name="network-policies-cwl-agent"></a>

If you enable network policy, a second container is add to the `aws-node` pods for a *node agent*\. This node agent can send the network policy logs to CloudWatch Logs\.

**Note**  
Only the network policy logs are sent by the node agent\. Other logs made by the VPC CNI aren't included\.

#### Prerequisites<a name="cni-network-policy-cwl-agent-prereqs"></a>
+ Add the following permissions as a stanza or separate policy to the IAM role that you are using for the VPC CNI\.

  ```
  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Sid": "VisualEditor0",
              "Effect": "Allow",
              "Action": [
                  "logs:DescribeLogGroups",
                  "logs:CreateLogGroup",
                  "logs:CreateLogStream",
                  "logs:PutLogEvents"
              ],
              "Resource": "*"
          }
      ]
  }
  ```

#### Amazon EKS add\-on<a name="cni-network-policy-cwl-agent-addon"></a>

------
#### [ AWS Management Console ]

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to configure the Amazon VPC CNI add\-on for\.

1. Choose the **Add\-ons** tab\.

1. Select the box in the top right of the add\-on box and then choose **Edit**\.

1. On the **Configure *name of addon*** page:

   1. Select a `v1.14.0-eksbuild.3` or later version in the **Version** dropdown list\.

   1. Expand the **Optional configuration settings**\.

   1. Enter the top\-level JSON key `"nodeAgent":` and value is an object with a key `"enableCloudWatchLogs":` and value of `"true"` in **Configuration values**\. The resulting text must be a valid JSON object\. The following example shows network policy and the network policy logs are enabled, and the logs are sent to CloudWatch Logs:

      ```
      {
          "enableNetworkPolicy": "true",
          "nodeAgent": {
              "enablePolicyEventLogs": "true",
              "enableCloudWatchLogs": "true",
          }
      }
      ```

The following screenshot shows an example of this scenario\.

![\[\]](http://docs.aws.amazon.com/eks/latest/userguide/images/console-cni-config-network-policy-logs-cwl.png)

------
#### [ AWS CLI ]
+ Run the following AWS CLI command\. Replace `my-cluster` with the name of your cluster and replace the IAM role ARN with the role that you are using\.

  ```
  aws eks update-addon --cluster-name my-cluster --addon-name vpc-cni --addon-version v1.14.0-eksbuild.3 \
      --service-account-role-arn arn:aws:iam::123456789012:role/AmazonEKSVPCCNIRole \
      --resolve-conflicts PRESERVE --configuration-values '{"nodeAgent": {"enablePolicyEventLogs": "true", "enableCloudWatchLogs": "true"}}'
  ```

------

#### Self\-managed add\-on<a name="cni-network-policy-cwl-agent-selfmanaged"></a>

------
#### [ Helm ]

If you have installed the Amazon VPC CNI plugin for Kubernetes through `helm`, you can update the configuration to send network policy logs to CloudWatch Logs\.
+ Run the following command to enable network policy logs and send them to CloudWatch Logs\.

  ```
  helm upgrade --set nodeAgent.enablePolicyEventLogs=true --set nodeAgent.enableCloudWatchLogs=true aws-vpc-cni --namespace kube-system eks/aws-vpc-cni
  ```

------
#### [ kubectl ]

1. Open the `aws-node` `DaemonSet` in your editor\.

   ```
   kubectl edit daemonset -n kube-system aws-node
   ```

1. Replace the `false` with `true` in two command arguments `--enable-policy-event-logs=false` and `--enable-cloudwatch-logs=false` in the `args:` in the `aws-network-policy-agent` container in the VPC CNI `aws-node` daemonset manifest\.

   ```
        - args:
           - --enable-policy-event-logs=true
           - --enable-cloudwatch-logs=true
   ```

------

### Send network policy logs with a Fluent Bit daemonset<a name="network-policies-cwl-fluentbit"></a>

If you are using Fluent Bit in a daemonset to send logs from your nodes, you can add configuration to include the network policy logs from network policies\. You can use the following example configuration:

```
    [INPUT]
        Name              tail
        Tag               eksnp.*
        Path              /var/log/aws-routed-eni/network-policy-agent*.log
        Parser            json
        DB                /var/log/aws-routed-eni/flb_npagent.db
        Mem_Buf_Limit     5MB
        Skip_Long_Lines   On
        Refresh_Interval  10
```

## Included eBPF SDK<a name="network-policies-ebpf-sdk"></a>

The Amazon VPC CNI plugin for Kubernetes installs eBPF SDK collection of tools on the nodes\. You can use the eBPF SDK tools to identify issues with network policies\. For example, the following command lists the programs that are running on the node\.

```
sudo /opt/cni/bin/aws-eks-na-cli ebpf progs
```

To run this command, you can use any method to connect to the node\.