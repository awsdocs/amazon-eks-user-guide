# CNI configuration variables<a name="cni-env-vars"></a>

The Amazon VPC CNI plugin for Kubernetes supports a number of configuration options, which are set through environment variables\. The following environment variables are available, and all of them are optional\. 

**`AWS_VPC_CNI_NODE_PORT_SUPPORT`**  
**Type** – Boolean  
**Default** – `true`  
Specifies whether `NodePort` services are enabled on a worker node's primary network interface\. This requires additional `iptables` rules and that the kernel's reverse path filter on the primary interface is set to `loose`\.

**`AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG`**  
**Type** – Boolean  
**Default** – `false`  
Specifies that your pods may use subnets and security groups, within the same VPC as your control plane resources, that are independent of your cluster's `resourcesVpcConfig`\. By default, pods share the same subnet and security groups as the worker node's primary interface\. Setting this variable to `true` causes `ipamD` to use the security groups and subnets in a worker node's `ENIConfig` for elastic network interface allocation\. You must create an `ENIConfig` custom resource definition for each subnet that your pods will reside in, and then annotate each worker node to use a specific `ENIConfig` \(multiple worker nodes can be annotated with the same `ENIConfig`\)\. Worker nodes can only be annotated with a single `ENIConfig` at a time, and the subnet in the `ENIConfig` must belong to the same Availability Zone that the worker node resides in\. For more information, see [CNI custom networking](cni-custom-network.md)\.

**`ENI_CONFIG_ANNOTATION_DEF`**  
**Type** – String  
**Default** – `k8s.amazonaws.com/eniConfig`  
Specifies a node annotation key name\. This should be used when `AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG=true`\. The annotation value will be used to set `ENIConfig` name\. Annotations take precedence over labels\.

**`ENI_CONFIG_LABEL_DEF`**  
**Type** – String  
**Default** – `k8s.amazonaws.com/eniConfig`  
Specifies a node label key name\. This should be used when `AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG=true`\. The label value will be used to set `ENIConfig` name\. Annotations will take precedence over labels\. To use labels, ensure that an annotation with the key `k8s.amazonaws.com/eniConfig` is defined and that a value for the annotation key `ENI_CONFIG_ANNOTATION_DEF` is not set on the node\. To select an `ENIConfig` based upon Availability Zone, set this to `failure-domain.beta.kubernetes.io/zone` and create an `ENIConfig` custom resource for each Availability Zone, such as `us-east-1a`\. For more information, see [CNI custom networking](cni-custom-network.md)\.

**`AWS_VPC_K8S_CNI_EXTERNALSNAT`**  
**Type** – Boolean  
**Default** – `false`  
Specifies whether an external NAT gateway should be used to provide SNAT of secondary ENI IP addresses\. If set to `true`, the SNAT `iptables` rule and off\-VPC IP rule are not applied, and these rules are removed if they have already been applied\.  
Disable SNAT if you need to allow inbound communication to your pods from external VPNs, direct connections, and external VPCs, and your pods do not need to access the internet directly via an Internet Gateway\. Your nodes must be running in a private subnet and connected to the internet through an AWS NAT Gateway or another external NAT device\.  
For more information, see [External source network address translation \(SNAT\)](external-snat.md)\.

**`AWS_VPC_K8S_CNI_RANDOMIZESNAT`**  
**Type** – String  
**Default** – `hashrandom`  
**Valid values** – `hashrandom`, `prng`, `none`  
Specifies whether the SNAT `iptables` rule should randomize the outgoing ports for connections\. This should be used when `AWS_VPC_K8S_CNI_EXTERNALSNAT=false`\. When enabled \(`hashrandom`\) the `--random` flag will be added to the SNAT `iptables` rule\. To use a pseudo random number generation, rather than hash\-based \(`--random-fully`\), use `prng` for the environment variable\. For old versions of `iptables` that do not support `--random-fully`, this option will fall back to `--random`\. Disable \(`none`\) this functionality if you rely on sequential port allocation for outgoing connections\.   
Any options other than `none` will cause outbound connections to be assigned a source port that's not necessarily part of the ephemeral port range set at the OS level \(`/proc/sys/net/ipv4/ip_local_port_range`\)\. This is relevant if you have NACLs restricting traffic based on the port range found in `ip_local_port_range`\.

**`WARM_ENI_TARGET`**  
**Type** – Integer  
**Default** – `1`  
Specifies the number of free elastic network interfaces \(and all of their available IP addresses\) that the `ipamD` daemon should attempt to keep available for pod assignment on the node\. By default, `ipamD` attempts to keep one elastic network interface and all of its IP addresses available for pod assignment\.  
The number of IP addresses per network interface varies by instance type\. For more information, see [IP addresses per network interface per instance type](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#AvailableIpPerENI) in the *Amazon EC2 User Guide for Linux Instances*\. 
For example, an `m4.4xlarge` launches with one network interface and 30 IP addresses\. If five pods are placed on the node and five free IP addresses are removed from the IP address warm pool, then `ipamD` attempts to allocate more interfaces until `WARM_ENI_TARGET` free interfaces are available on the node\.  
If `WARM_IP_TARGET` is set, then this environment variable is ignored and the `WARM_IP_TARGET` behavior is used instead\.

**`WARM_IP_TARGET`**  
**Type** – Integer  
**Default** – None  
Specifies the number of free IP addresses that the `ipamD` daemon should attempt to keep available for pod assignment on the node\. For example, if `WARM_IP_TARGET` is set to 10, then `ipamD` attempts to keep 10 free IP addresses available at all times\. If the elastic network interfaces on the node are unable to provide these free addresses, `ipamD` attempts to allocate more interfaces until `WARM_IP_TARGET` free IP addresses are available\.  
This environment variable overrides `WARM_ENI_TARGET` behavior\.

**`MAX_ENI`**  
**Type** – Integer  
**Default** – None  
Specifies the maximum number of ENIs that will be attached to the node\. When `MAX_ENI` is unset or less than or equal to `0`, the setting is not used, and the maximum number of ENIs is always equal to the maximum number for the instance type in question\. Even when `MAX_ENI` is a positive number, it is limited by the maximum number for the instance type\.

**`AWS_VPC_K8S_CNI_LOGLEVEL`**  
**Type** – String  
**Default** – DEBUG  
**Valid values** – `trace`, `debug`, `info`, `warn`, `error`, `critical`, or `off` \(not case sensitive\)  
Specifies the loglevel for `ipamd`\.

**`AWS_VPC_K8S_CNI_LOG_FILE`**  
**Type** – String  
**Default** – Unset  
Valid values: `stdout` or a file path  
Specifies where to write the logging output of `ipamd`\. You can specify `stdout` or override the default file, such as `/var/log/aws-routed-eni/ipamd.log`\.

**`AWS_VPC_K8S_PLUGIN_LOG_FILE`**  
**Type** – String  
**Default** – Unset  
**Valid values** – `stdout` or a file path\.  
Specifies where to write the logging output for the `aws-cni` plugin\. You can specify `stdout` or override the default file, such as `/var/log/aws-routed-eni/plugin.log`\.

**`AWS_VPC_K8S_PLUGIN_LOG_LEVEL`**  
**Type** – String  
**Valid values** – `trace`, `debug`, `info`, `warn`, `error`, `critical`, or `off` \(not case sensitive\)  
Specifies the log level for the `aws-cni` plugin\.

**`INTROSPECTION_BIND_ADDRESS`**  
**Type** – String  
**Default** – `127.0.0.1:61679`  
Specifies the bind address for the introspection endpoint\. A Unix domain socket can be specified with the `unix:` prefix before the socket path\.

**`DISABLE_INTROSPECTION`**  
**Type** – Boolean  
**Default** – false  
Specifies whether introspection endpoints are disabled on a worker node\. Setting this to `true` will reduce the debugging information you can get from the node when running the `aws-cni-support.sh` script\.

**`DISABLE_METRICS`**  
**Type** – Boolean  
**Default** – false  
Specifies whether the Prometheus metrics endpoint is disabled or not for `ipamd`\. By default metrics are published on `:61678/metrics`\.

**`AWS_VPC_K8S_CNI_VETHPREFIX`**  
**Type** – String  
**Default** – `eni`  
Specifies the `veth` prefix used to generate the host\-side `veth` device name for the CNI\. The prefix can be a maximum of four characters long\.

**`CLUSTER_NAME`**  
**Type** – String  
**Default** – `""`  
Specifies the cluster name to tag allocated ENIs with\.  

**ENI tags related to allocation**

This plugin interacts with the following tags on ENIs:
+ `cluster.k8s.amazonaws.com/name`
+ `node.k8s.amazonaws.com/instance_id`
+ `node.k8s.amazonaws.com/no_manage`
**Cluster name tag**  
The tag `cluster.k8s.amazonaws.com/name` will be set to the cluster name of the `aws-node` daemonset which created the ENI\.
**Instance ID tag**  
The tag `node.k8s.amazonaws.com/instance_id` will be set to the instance ID of the `aws-node` instance that allocated this ENI\.
**No manage tag**  
The `node.k8s.amazonaws.com/no_manage` tag is read by the `aws-node` daemonset to determine whether an ENI attached to the machine should not be configured or used for private IP addresses\. This tag is not set by the CNI plugin itself, but rather may be set by a user to indicate that an ENI is intended for host networking pods, or for some other process unrelated to Kubernetes\.
Attaching an ENI with the `no_manage` tag will result in an incorrect value for the `kubelet`'s `--max-pods` configuration option\. Consider also updating the `MAX_ENI` and `--max-pods` configuration options on this plugin and the `kubelet`, respectively, if you are using of this tag\.

**Notes**  
The `L-IPAMD` \(`aws-node` daemonSet\) running on every worker node requires access to the Kubernetes API server\. If it can not reach the Kubernetes API server, `ipamD` will exit and the CNI will not be able to get any IP addresses for pods\. To confirm whether `L-IPAMD` has access to the Kubernetes API server\.  

```
kubectl get svc kubernetes
```
Output  

```
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.0.0.1   <none>        443/TCP   29d
```
SSH into a worker node to check whether the worker node can reach the API server\.  

```
telnet 10.0.0.1 443
```
Output  

```
Trying 10.0.0.1...
Connected to 10.0.0.1.
Escape character is '^]'.
```
If you receive the last line of output, then the Kubernetes API server is reachable\.