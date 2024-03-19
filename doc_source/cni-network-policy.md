# Configure your cluster for Kubernetes network policies<a name="cni-network-policy"></a>

By default, there are no restrictions in Kubernetes for IP addresses, ports, or connections between any Pods in your cluster or between your Pods and resources in any other network\. You can use Kubernetes *network policy* to restrict network traffic to and from your Pods\. For more information, see [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) in the Kubernetes documentation\.

If you have version `1.13` or earlier of the Amazon VPC CNI plugin for Kubernetes on your cluster, you need to implement a third party solution to apply Kubernetes network policies to your cluster\. Version `1.14` or later of the plugin can implement network policies, so you don't need to use a third party solution\. In this topic, you learn how to configure your cluster to use Kubernetes network policy on your cluster without using a third party add\-on\.

Network policies in the Amazon VPC CNI plugin for Kubernetes are supported in the following configurations\.
+ Amazon EKS clusters of version `1.25` and later\.
+ Version 1\.14 or later of the Amazon VPC CNI plugin for Kubernetes on your cluster\.
+ Cluster configured for `IPv4` or `IPv6` addresses\.
+ You can use network policies with [security groups for Pods](security-groups-for-pods.md)\. With network policies, you can control all in\-cluster communication\. With security groups for Pods, you can control access to AWS services from applications within a Pod\.
+ You can use network policies with *custom networking* and *prefix delegation*\.

## Considerations<a name="cni-network-policy-considerations"></a>
+ When applying Amazon VPC CNI plugin for Kubernetes network policies to your cluster with the Amazon VPC CNI plugin for Kubernetes , you can apply the policies to Amazon EC2 Linux nodes only\. You can't apply the policies to Fargate or Windows nodes\.
+ If your cluster is currently using a third party solution to manage Kubernetes network policies, you can use those same policies with the Amazon VPC CNI plugin for Kubernetes\. However you must remove your existing solution so that it isn't managing the same policies\.
+ You can apply multiple network policies to the same Pod\. When two or more policies that select the same Pod are configured, all policies are applied to the Pod\.
+ The maximum number of unique combinations of ports for each protocol in each `ingress:` or `egress:` selector in a network policy is 24\.
+ For any of your Kubernetes services, the service port must be the same as the container port\. If you're using named ports, use the same name in the service spec too\.
+ 

**Policy enforcement at Pod startup**  
The Amazon VPC CNI plugin for Kubernetes configures network policies for pods in parallel with the pod provisioning\. Until all of the policies are configured for the new pod, containers in the new pod will start with a *default allow policy*\. This is called *standard mode*\. A default allow policy means that all ingress and egress traffic is allowed to and from the new pods\.

  You can change this default network policy by setting the environment variable `NETWORK_POLICY_ENFORCING_MODE` to `strict` in the `aws-node` container of the VPC CNI `DaemonSet`\.

  ```
  env:
    - name: NETWORK_POLICY_ENFORCING_MODE
      value: "strict"
  ```

  With the `NETWORK_POLICY_ENFORCING_MODE` variable set to `strict`, pods that use the VPC CNI start with a *default deny policy*, then policies are configured\. This is called *strict mode*\. In strict mode, you must have a network policy for every endpoint that your pods need to access in your cluster\. Note that this requirement applies to the CoreDNS pods\. The default deny policy isn’t configured for pods with Host networking\.
+ The network policy feature creates and requires a `PolicyEndpoint` Custom Resource Definition \(CRD\) called `policyendpoints.networking.k8s.aws`\. `PolicyEndpoint` objects of the Custom Resource are managed by Amazon EKS\. You shouldn't modify or delete these resources\.
+ If you run pods that use the instance role IAM credentials or connect to the EC2 IMDS, be careful to check for network policies that would block access to the EC2 IMDS\. You may need to add a network policy to allow access to EC2 IMDS\. For more information, see [Instance metadata and user data](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html) in the Amazon EC2 User Guide for Linux Instances\.

  Pods that use *IAM roles for service accounts* don't access EC2 IMDS\.
+ The Amazon VPC CNI plugin for Kubernetes doesn't apply network policies to additional network interfaces for each pod, only the primary interface for each pod \(`eth0`\)\. This affects the following architectures:
  + `IPv6` pods with the `ENABLE_V4_EGRESS` variable set to `true`\. This variable enables the `IPv4` egress feature to connect the IPv6 pods to `IPv4` endpoints such as those outside the cluster\. The `IPv4` egress feature works by creating an additional network interface with a local loopback IPv4 address\.
  + When using chained network plugins such as Multus\. Because these plugins add network interfaces to each pod, network policies aren't applied to the chained network plugins\.
+ The network policy feature uses port `8162` on the node for metrics by default\. Also, the feature used port `8163` for health probes\. If you run another application on the nodes or inside pods that needs to use these ports, the app fails to run\. In VPC CNI version `v1.14.1` or later, you can change these ports port in the following places:

------
#### [ AWS Management Console ]

  1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

  1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to configure the Amazon VPC CNI add\-on for\.

  1. Choose the **Add\-ons** tab\.

  1. Select the box in the top right of the add\-on box and then choose **Edit**\.

  1. On the **Configure *name of addon*** page:

     1. Select a `v1.14.0-eksbuild.3` or later version in the **Version** dropdown list\.

     1. Expand the **Optional configuration settings**\.

     1. Enter the JSON key `"enableNetworkPolicy":` and value `"true"` in **Configuration values**\. The resulting text must be a valid JSON object\. If this key and value are the only data in the text box, surround the key and value with curly braces `{}`\.

        The following example has network policy feature enabled, the network policy logs enabled, the network policy logs sent to Amazon CloudWatch Logs, and the metrics and health probes are set to the default port numbers:

     ```
     {
         "enableNetworkPolicy": "true",
         "nodeAgent": {
             "enablePolicyEventLogs": "true",
             "enableCloudWatchLogs": "true",
             "healthProbeBindAddr": "8163",
             "metricsBindAddr": "8162"
         }
     }
     ```

------
#### [ Helm ]

  If you have installed the Amazon VPC CNI plugin for Kubernetes through `helm`, you can update the configuration to change the ports\.
  + Run the following command to change the ports\. Set the port number in the value for either key `nodeAgent.metricsBindAddr` or key `nodeAgent.healthProbeBindAddr`, respectively\.

    ```
    helm upgrade --set nodeAgent.metricsBindAddr=8162 --set nodeAgent.healthProbeBindAddr=8163 aws-vpc-cni --namespace kube-system eks/aws-vpc-cni
    ```

------
#### [ kubectl ]

  1. Open the `aws-node` `DaemonSet` in your editor\.

     ```
     kubectl edit daemonset -n kube-system aws-node
     ```

  1. Replace the port numbers in the following command arguments in the `args:` in the `aws-network-policy-agent` container in the VPC CNI `aws-node` daemonset manifest\.

     ```
         - args:
                 - --metrics-bind-addr=:8162
                 - --health-probe-bind-addr=:8163
     ```

------

## Prerequisites<a name="cni-network-policy-prereqs"></a>
+ 

**Minimum cluster version**  
An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\. The cluster must be Kubernetes version `1.25` or later\. The cluster must be running one of the Kubernetes versions and platform versions listed in the following table\. Note that any Kubernetes and platform versions later than those listed are also supported\. You can check your current Kubernetes version by replacing *my\-cluster* in the following command with the name of your cluster and then running the modified command:

  ```
  aws eks describe-cluster
                --name my-cluster --query cluster.version --output
                text
  ```    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/cni-network-policy.html)
+ 

**Minimum VPC CNI version**  
Version `1.14` or later of the Amazon VPC CNI plugin for Kubernetes on your cluster\. You can see which version that you currently have with the following command\.

  ```
  kubectl describe daemonset aws-node --namespace kube-system | grep amazon-k8s-cni: | cut -d : -f 3
  ```

  If your version is earlier than `1.14`, see [Updating the Amazon EKS add\-on](managing-vpc-cni.md#vpc-add-on-update) to upgrade to version `1.14` or later\.
+ 

**Minimum Linux kernel version**  
Your nodes must have Linux kernel version `5.10` or later\. You can check your kernel version with `uname -r`\. If you're using the latest versions of the Amazon EKS optimized Amazon Linux, Amazon EKS optimized accelerated Amazon Linux AMIs, and Bottlerocket AMIs, they already have the required kernel version\.

  The Amazon EKS optimized accelerated Amazon Linux AMI version `v20231116` or later have kernel version `5.10`\.

## To configure your cluster to use Kubernetes network policies<a name="cni-network-policy-setup"></a>

1. 

**Mount the BPF filesystem**
**Note**  
If your cluster is version `1.27` or later, you can skip this step as all Amazon EKS optimized Amazon Linux and Bottlerocket AMIs for `1.27` or later have this feature already\.  
For all other cluster versions, if you upgrade the Amazon EKS optimized Amazon Linux to version `v20230703` or later or you upgrade the Bottlerocket AMI to version `v1.0.2` or later, you can skip this step\.

   1. Mount the Berkeley Packet Filter \(BPF\) file system on each of your nodes\.

      ```
      sudo mount -t bpf bpffs /sys/fs/bpf
      ```

   1. Then, add the same command to your user data in your launch template for your Amazon EC2 Auto Scaling Groups\.

1. 

**Enable network policy in the VPC CNI**

   1. See which type of the add\-on is installed on your cluster\. Depending on the tool that you created your cluster with, you might not currently have the Amazon EKS add\-on type installed on your cluster\. Replace *my\-cluster* with the name of your cluster\.

      ```
      aws eks describe-addon --cluster-name my-cluster --addon-name vpc-cni --query addon.addonVersion --output text
      ```

      If a version number is returned, you have the Amazon EKS type of the add\-on installed on your cluster and don't need to complete the remaining steps in this procedure\. If an error is returned, you don't have the Amazon EKS type of the add\-on installed on your cluster\.

   1. 
      + Amazon EKS add\-on

------
#### [ AWS Management Console ]

        1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

        1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to configure the Amazon VPC CNI add\-on for\.

        1. Choose the **Add\-ons** tab\.

        1. Select the box in the top right of the add\-on box and then choose **Edit**\.

        1. On the **Configure *name of addon*** page:

           1. Select a `v1.14.0-eksbuild.3` or later version in the **Version** dropdown list\.

           1. Expand the **Optional configuration settings**\.

           1. Enter the JSON key `"enableNetworkPolicy":` and value `"true"` in **Configuration values**\. The resulting text must be a valid JSON object\. If this key and value are the only data in the text box, surround the key and value with curly braces `{}`\. The following example shows network policy is enabled:

              ```
              { "enableNetworkPolicy": "true" }
              ```

              The following screenshot shows an example of this scenario\.  
![\[AWS Management Console showing the VPC CNI add-on with network policy in the optional configuration.\]](http://docs.aws.amazon.com/eks/latest/userguide/images/console-cni-config-network-policy.png)

------
#### [ AWS CLI ]
        + Run the following AWS CLI command\. Replace `my-cluster` with the name of your cluster and the IAM role ARN with the role that you are using\.

          ```
          aws eks update-addon --cluster-name my-cluster --addon-name vpc-cni --addon-version v1.14.0-eksbuild.3 \
              --service-account-role-arn arn:aws:iam::123456789012:role/AmazonEKSVPCCNIRole \
              --resolve-conflicts PRESERVE --configuration-values '{"enableNetworkPolicy": "true"}'
          ```

------
      + Self\-managed add\-on

------
#### [ Helm ]

        If you have installed the Amazon VPC CNI plugin for Kubernetes through `helm`, you can update the configuration to enable network policy\.
        + Run the following command to enable network policy\.

          ```
          helm upgrade --set enableNetworkPolicy=true aws-vpc-cni --namespace kube-system eks/aws-vpc-cni
          ```

------
#### [ kubectl ]

        1. Open the `amazon-vpc-cni` `ConfigMap` in your editor\.

           ```
           kubectl edit configmap -n kube-system amazon-vpc-cni -o yaml
           ```

        1. Add the following line to the `data` in the `ConfigMap`\.

           ```
           enable-network-policy-controller: "true"
           ```

           Once you've added the line, your `ConfigMap` should look like the following example\.

           ```
           apiVersion: v1
            kind: ConfigMap
            metadata:
             name: amazon-vpc-cni
             namespace: kube-system
            data:
             enable-network-policy-controller: "true"
           ```

        1. Open the `aws-node` `DaemonSet` in your editor\.

           ```
           kubectl edit daemonset -n kube-system aws-node
           ```

        1. Replace the `false` with `true` in the command argument `--enable-network-policy=false` in the `args:` in the `aws-network-policy-agent` container in the VPC CNI `aws-node` daemonset manifest\.

           ```
                - args:
                   - --enable-network-policy=true
           ```

------

1. Confirm that the `aws-node` pods are running on your cluster\.

   ```
   kubectl get pods -n kube-system | grep 'aws-node\|amazon'
   ```

   An example output is as follows\.

   ```
   aws-node-gmqp7                                          2/2     Running   1 (24h ago)   24h
   aws-node-prnsh                                          2/2     Running   1 (24h ago)   24h
   ```

   If network policy is enabled, there are 2 containers in the `aws-node` pods\. In previous versions and if network policy is disabled, there is only a single container in the `aws-node` pods\.

   You can now deploy Kubernetes network policies to your cluster\. For more information, see [Kubernetes network policies](#network-policies-implement-policies)\.

## Stars demo of network policy<a name="network-policy-stars-demo"></a>

This demo creates a front\-end, back\-end, and client service on your Amazon EKS cluster\. The demo also creates a management graphical user interface that shows the available ingress and egress paths between each service\. We recommend that you complete the demo on a cluster that you don't run production workloads on\. 

Before you create any network policies, all services can communicate bidirectionally\. After you apply the network policies, you can see that the client can only communicate with the front\-end service, and the back\-end only accepts traffic from the front\-end\.

**To run the Stars policy demo**

1. Apply the front\-end, back\-end, client, and management user interface services:

   ```
   kubectl apply -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/create_resources.files/namespace.yaml
   kubectl apply -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/create_resources.files/management-ui.yaml
   kubectl apply -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/create_resources.files/backend.yaml
   kubectl apply -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/create_resources.files/frontend.yaml
   kubectl apply -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/create_resources.files/client.yaml
   ```

1. View all Pods on the cluster\.

   ```
   kubectl get pods -A
   ```

   An example output is as follows\.

   In your output, you should see pods in the namespaces shown in the following output\. The *NAMES* of your pods and the number of pods in the `READY` column are different than those in the following output\. Don't continue until you see pods with similar names and they all have `Running` in the `STATUS` column\.

   ```
   NAMESPACE         NAME                                       READY   STATUS    RESTARTS   AGE
   [...]
   client            client-xlffc                               1/1     Running   0          5m19s
   [...]
   management-ui     management-ui-qrb2g                        1/1     Running   0          5m24s
   stars             backend-sz87q                              1/1     Running   0          5m23s
   stars             frontend-cscnf                             1/1     Running   0          5m21s
   [...]
   ```

1. To connect to the management user interface, connect to the `EXTERNAL-IP` of the service running on your cluster:

   ```
   kubectl get service/management-ui -n management-ui
   ```

1. Open the a browser to the location from the previous step\. You should see the management user interface\. The **C** node is the client service, the **F** node is the front\-end service, and the **B** node is the back\-end service\. Each node has full communication access to all other nodes, as indicated by the bold, colored lines\.  
![\[Open network policy\]](http://docs.aws.amazon.com/eks/latest/userguide/images/stars-default.png)

1. Apply the following network policy in both the `stars` and `client` namespaces to isolate the services from each other:

   ```
   kind: NetworkPolicy
   apiVersion: networking.k8s.io/v1
   metadata:
     name: default-deny
   spec:
     podSelector:
       matchLabels: {}
   ```

   You can use the following commands to apply the policy to both namespaces:

   ```
   kubectl apply -n stars -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/apply_network_policies.files/default-deny.yaml
   kubectl apply -n client -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/apply_network_policies.files/default-deny.yaml
   ```

1. Refresh your browser\. You see that the management user interface can no longer reach any of the nodes, so they don't show up in the user interface\.

1. Apply the following different network policies to allow the management user interface to access the services\. Apply this policy to allow the UI:

   ```
   kind: NetworkPolicy
   apiVersion: networking.k8s.io/v1
   metadata:
     namespace: stars
     name: allow-ui 
   spec:
     podSelector:
       matchLabels: {}
     ingress:
       - from:
           - namespaceSelector:
               matchLabels:
                 role: management-ui
   ```

   Apply this policy to allow the client:

   ```
   kind: NetworkPolicy
   apiVersion: networking.k8s.io/v1
   metadata:
     namespace: client 
     name: allow-ui 
   spec:
     podSelector:
       matchLabels: {}
     ingress:
       - from:
           - namespaceSelector:
               matchLabels:
                 role: management-ui
   ```

   You can use the following commands to apply both policies:

   ```
   kubectl apply -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/apply_network_policies.files/allow-ui.yaml
   kubectl apply -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/apply_network_policies.files/allow-ui-client.yaml
   ```

1. Refresh your browser\. You see that the management user interface can reach the nodes again, but the nodes cannot communicate with each other\.  
![\[UI access network policy\]](http://docs.aws.amazon.com/eks/latest/userguide/images/stars-no-traffic.png)

1. Apply the following network policy to allow traffic from the front\-end service to the back\-end service:

   ```
   kind: NetworkPolicy
   apiVersion: networking.k8s.io/v1
   metadata:
     namespace: stars
     name: backend-policy
   spec:
     podSelector:
       matchLabels:
         role: backend
     ingress:
       - from:
           - podSelector:
               matchLabels:
                 role: frontend
         ports:
           - protocol: TCP
             port: 6379
   ```

1. Refresh your browser\. You see that the front\-end can communicate with the back\-end\.  
![\[Front-end to back-end policy\]](http://docs.aws.amazon.com/eks/latest/userguide/images/stars-front-end-back-end.png)

1. Apply the following network policy to allow traffic from the client to the front\-end service:

   ```
   kind: NetworkPolicy
   apiVersion: networking.k8s.io/v1
   metadata:
     namespace: stars
     name: frontend-policy
   spec:
     podSelector:
       matchLabels:
         role: frontend 
     ingress:
       - from:
           - namespaceSelector:
               matchLabels:
                 role: client
         ports:
           - protocol: TCP
             port: 80
   ```

1. Refresh your browser\. You see that the client can communicate to the front\-end service\. The front\-end service can still communicate to the back\-end service\.  
![\[Final network policy\]](http://docs.aws.amazon.com/eks/latest/userguide/images/stars-final.png)

1. \(Optional\) When you are done with the demo, you can delete its resources\.

   ```
   kubectl delete -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/create_resources.files/client.yaml
   kubectl delete -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/create_resources.files/frontend.yaml
   kubectl delete -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/create_resources.files/backend.yaml
   kubectl delete -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/create_resources.files/management-ui.yaml
   kubectl delete -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/create_resources.files/namespace.yaml
   ```

   Even after deleting the resources, there can still be network policy endpoints on the nodes that might interfere in unexpected ways with networking in your cluster\. The only sure way to remove these rules is to reboot the nodes or terminate all of the nodes and recycle them\. To terminate all nodes, either set the Auto Scaling Group desired count to 0, then back up to the desired number, or just terminate the nodes\.

## Troubleshooting network policies<a name="network-policies-troubleshooting"></a>

You can troubleshoot and investigate network connections that use network policies by reading the [Network policy logs](#network-policies-troubleshooting-flowlogs) and by running tools from the [eBPF SDK](#network-policies-ebpf-sdk)\.

### Network policy logs<a name="network-policies-troubleshooting-flowlogs"></a>

Whether connections are allowed or denied by a network policies is logged in *flow logs*\. The network policy logs on each node include the flow logs for every pod that has a network policy\. Network policy logs are stored at `/var/log/aws-routed-eni/network-policy-agent.log`\. The following example is from a `network-policy-agent.log` file:

```
{"level":"info","timestamp":"2023-05-30T16:05:32.573Z","logger":"ebpf-client","msg":"Flow Info: ","Src
IP":"192.168.87.155","Src Port":38971,"Dest IP":"64.6.160","Dest
Port":53,"Proto":"UDP","Verdict":"ACCEPT"}
```

Network policy logs are disabled by default\. To enable the network policy logs, follow these steps:

**Note**  
Network policy logs require an additional 1 vCPU for the `aws-network-policy-agent` container in the VPC CNI `aws-node` daemonset manifest\.

#### Amazon EKS add\-on<a name="cni-network-policy-flowlogs-addon"></a>

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

![\[AWS Management Console showing the VPC CNI add-on with network policy and CloudWatch Logs in the optional configuration.\]](http://docs.aws.amazon.com/eks/latest/userguide/images/console-cni-config-network-policy-logs.png)

------
#### [ AWS CLI ]
+ Run the following AWS CLI command\. Replace `my-cluster` with the name of your cluster and replace the IAM role ARN with the role that you are using\.

  ```
  aws eks update-addon --cluster-name my-cluster --addon-name vpc-cni --addon-version v1.14.0-eksbuild.3 \
      --service-account-role-arn arn:aws:iam::123456789012:role/AmazonEKSVPCCNIRole \
      --resolve-conflicts PRESERVE --configuration-values '{"nodeAgent": {"enablePolicyEventLogs": "true"}}'
  ```

------

#### Self\-managed add\-on<a name="cni-network-policy-flowlogs-selfmanaged"></a>

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

### Send network policy logs to Amazon CloudWatch Logs<a name="network-policies-cloudwatchlogs"></a>

You can monitor the network policy logs using services such as Amazon CloudWatch Logs\. You can use the following methods to send the network policy logs to CloudWatch Logs\.

For EKS clusters, the policy logs will be located under `/aws/eks/cluster-name/cluster/` and for self\-managed K8S clusters, the logs will be placed under `/aws/k8s-cluster/cluster`/\.

#### Send network policy logs with Amazon VPC CNI plugin for Kubernetes<a name="network-policies-cwl-agent"></a>

If you enable network policy, a second container is add to the `aws-node` pods for a *node agent*\. This node agent can send the network policy logs to CloudWatch Logs\.

**Note**  
Only the network policy logs are sent by the node agent\. Other logs made by the VPC CNI aren't included\.

##### Prerequisites<a name="cni-network-policy-cwl-agent-prereqs"></a>
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

##### Amazon EKS add\-on<a name="cni-network-policy-cwl-agent-addon"></a>

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

![\[AWS Management Console showing the VPC CNI add-on with network policy and CloudWatch Logs in the optional configuration.\]](http://docs.aws.amazon.com/eks/latest/userguide/images/console-cni-config-network-policy-logs-cwl.png)

------
#### [ AWS CLI ]
+ Run the following AWS CLI command\. Replace `my-cluster` with the name of your cluster and replace the IAM role ARN with the role that you are using\.

  ```
  aws eks update-addon --cluster-name my-cluster --addon-name vpc-cni --addon-version v1.14.0-eksbuild.3 \
      --service-account-role-arn arn:aws:iam::123456789012:role/AmazonEKSVPCCNIRole \
      --resolve-conflicts PRESERVE --configuration-values '{"nodeAgent": {"enablePolicyEventLogs": "true", "enableCloudWatchLogs": "true"}}'
  ```

------

##### Self\-managed add\-on<a name="cni-network-policy-cwl-agent-selfmanaged"></a>

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

#### Send network policy logs with a Fluent Bit daemonset<a name="network-policies-cwl-fluentbit"></a>

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

### Included eBPF SDK<a name="network-policies-ebpf-sdk"></a>

The Amazon VPC CNI plugin for Kubernetes installs eBPF SDK collection of tools on the nodes\. You can use the eBPF SDK tools to identify issues with network policies\. For example, the following command lists the programs that are running on the node\.

```
sudo /opt/cni/bin/aws-eks-na-cli ebpf progs
```

To run this command, you can use any method to connect to the node\.

## Kubernetes network policies<a name="network-policies-implement-policies"></a>

To implement Kubernetes network policies you create Kubernetes `NetworkPolicy` objects and deploy them to your cluster\. `NetworkPolicy` objects are scoped to a namespace\. You implement policies to allow or deny traffic between Pods based on label selectors, namespaces, and IP address ranges\. For more information about creating `NetworkPolicy` objects, see [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/#networkpolicy-resource) in the Kubernetes documentation\.

Enforcement of Kubernetes `NetworkPolicy` objects is implemented using the Extended Berkeley Packet Filter \(eBPF\)\. Relative to `iptables` based implementations, it offers lower latency and performance characteristics, including reduced CPU utilization and avoiding sequential lookups\. Additionally, eBPF probes provide access to context rich data that helps debug complex kernel level issues and improve observability\. Amazon EKS supports an eBPF\-based exporter that leverages the probes to log policy results on each node and export the data to external log collectors to aid in debugging\. For more information, see the [eBPF documentation](https://ebpf.io/what-is-ebpf/#what-is-ebpf)\.