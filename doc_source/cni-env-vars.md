# CNI Configuration Variables<a name="cni-env-vars"></a>

The Amazon VPC CNI plugin for Kubernetes supports a number of configuration options, which are set through environment variables\. The following environment variables are available, and all of them are optional\. 

`AWS_VPC_CNI_NODE_PORT_SUPPORT`  
Type: Boolean  
Default: `true`  
Specifies whether `NodePort` services are enabled on a worker node's primary network interface\. This requires additional `iptables` rules and that the kernel's reverse path filter on the primary interface is set to `loose`\.

`AWS_VPC_K8S_CNI_EXTERNALSNAT`  
Type: Boolean  
Default: `false`  
Specifies whether an external NAT gateway should be used to provide SNAT of secondary ENI IP addresses\. If set to `true`, the SNAT `iptables` rule and off\-VPC IP rule are not applied, and these rules are removed if they have already been applied\.  
Disable SNAT if you need to allow inbound communication to your pods from external VPNs, direct connections, and external VPCs, and your pods do not need to access the Internet directly via an Internet Gateway\. However, your nodes must be running in a private subnet and connected to the internet through an AWS NAT Gateway or another external NAT device\.  
For more information, see [External Source Network Address Translation \(SNAT\)](external-snat.md)\.

`AWS_VPC_K8S_CNI_RANDOMIZESNAT`
Type: String  
Default: `hashrandom`  
Valid Values: `hashrandom`, `prng`, `none`  
Specifies whether the SNAT `iptables` rule should randomize the outgoing ports for connections\. This should be used when
`AWS_VPC_K8S_CNI_EXTERNALSNAT=false`. When enabled (`hashrandom`) the `--random` flag will be added to the SNAT `iptables`
rule\. To use pseudo random number generation rather than hash based (i.e. `--random-fully`) use `prng` for the environment
variable. For old versions of `iptables` that do not support `--random-fully` this option will fall back to `--random`.
Disable (`none`) this functionality if you rely on sequential port allocation for outgoing connections.

*Note*: Any options other than `none` will cause outbound connections to be assigned a source port that's not necessarily part of the ephemeral port range set at the OS level (/proc/sys/net/ipv4/ip_local_port_range). This is relevant for any customers that might have NACLs restricting traffic based on the port range found in ip_local_port_range

`AWS_VPC_K8S_CNI_EXCLUDE_SNAT_CIDRS` (Since v1.6.0)  
Type: String   
Default: empty   
Specify a comma separated list of IPv4 CIDRs to exclude from SNAT. For every item in the list an `iptables` rule and off\-VPC
IP rule will be applied. If an item is not a valid ipv4 range it will be skipped. This should be used when `AWS_VPC_K8S_CNI_EXTERNALSNAT=false`.

`MAX_ENI`  
Type: Integer  
Default: None  
Specifies the maximum number of ENIs that will be attached to the node. When `MAX_ENI` is unset or 0 (or lower), the setting
is not used, and the maximum number of ENIs is always equal to the maximum number for the instance type in question. Even when
`MAX_ENI` is a positive number, it is limited by the maximum number for the instance type.

`WARM_ENI_TARGET`  
Type: Integer  
Default: `1`  
Specifies the number of free elastic network interfaces \(and all of their available IP addresses\) that the `ipamD` daemon should attempt to keep available for pod assignment on the node\. By default, `ipamD` attempts to keep 1 elastic network interface and all of its IP addresses available for pod assignment\.  
The number of IP addresses per network interface varies by instance type\. For more information, see [IP Addresses Per Network Interface Per Instance Type](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#AvailableIpPerENI) in the *Amazon EC2 User Guide for Linux Instances*\. 
For example, an `m4.4xlarge` launches with 1 network interface and 30 IP addresses\. If 5 pods are placed on the node and 5 free IP addresses are removed from the IP address warm pool, then `ipamD` attempts to allocate more interfaces until `WARM_ENI_TARGET` free interfaces are available on the node\.  
If `WARM_IP_TARGET` is set, then this environment variable is ignored and the `WARM_IP_TARGET` behavior is used instead\.

`WARM_IP_TARGET`  
Type: Integer  
Default: None  
Specifies the number of free IP addresses that the `ipamD` daemon should attempt to keep available for pod assignment on the node\. For example, if `WARM_IP_TARGET` is set to 10, then `ipamD` attempts to keep 10 free IP addresses available at all times\. If the elastic network interfaces on the node are unable to provide these free addresses, `ipamD` attempts to allocate more interfaces until `WARM_IP_TARGET` free IP addresses are available\.  
This environment variable overrides `WARM_ENI_TARGET` behavior\.

`MINIMUM_IP_TARGET` (Since v1.6.0)  
Type: Integer  
Default: None  
Specifies the number of total IP addresses that the `ipamD` daemon should attempt to allocate for pod assignment on the node.
`MINIMUM_IP_TARGET` behaves identically to `WARM_IP_TARGET` except that instead of setting a target number of free IP
addresses to keep available at all times, it sets a target number for a floor on how many total IP addresses are allocated.

`MINIMUM_IP_TARGET` is for pre-scaling, `WARM_IP_TARGET` is for dynamic scaling. For example, suppose a cluster has an
expected pod density of approximately 30 pods per node. If `WARM_IP_TARGET` is set to 30 to ensure there are enough IPs
allocated up front by the CNI, then 30 pods are deployed to the node, the CNI will allocate an additional 30 IPs, for
a total of 60, accelerating IP exhaustion in the relevant subnets. If instead `MINIMUM_IP_TARGET` is set to 30 and
`WARM_IP_TARGET` to 2, after the 30 pods are deployed the CNI would allocate an additional 2 IPs. This still provides
elasticity, but uses roughly half as many IPs as using WARM_IP_TARGET alone (32 IPs vs 60 IPs).

This also improves reliability of the EKS cluster by reducing the number of calls necessary to allocate or deallocate
private IPs, which may be throttled, especially at scaling-related times.

`AWS_VPC_ENI_MTU` (Since v1.6.0)  
Type: Integer  
Default: 9001  
Used to configure the MTU size for attached ENIs. The valid range is from `576` to `9001`.

`AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG`  
Type: Boolean  
Default: `false`  
Specifies that your pods may use subnets and security groups \(within the same VPC as your control plane resources\) that are independent of your cluster's `resourcesVpcConfig`\. By default, pods share the same subnet and security groups as the worker node's primary interface\. Setting this variable to `true` causes `ipamD` to use the security groups and subnets in a worker node's `ENIConfig` for elastic network interface allocation\. You must create an `ENIConfig` custom resource definition for each subnet that your pods will reside in, and then annotate each worker node to use a specific `ENIConfig` \(multiple worker nodes can be annotated with the same `ENIConfig`\)\. Worker nodes can only be annotated with a single `ENIConfig` at a time, and the subnet in the `ENIConfig` must belong to the same Availability Zone that the worker node resides in\. For more information, see [CNI Custom Networking](cni-custom-network.md)\.

`ENI_CONFIG_ANNOTATION_DEF`  
Type: String  
Default: `k8s.amazonaws.com/eniConfig`  
Specifies node annotation key name. This should be used when `AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG=true`. Annotation value
will be used to set `ENIConfig` name. Note that annotations take precedence over labels.

`ENI_CONFIG_LABEL_DEF`
Type: String
Default: `k8s.amazonaws.com/eniConfig`
Specifies node label key name\. This should be used when `AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG=true`. Label value will be used
to set `ENIConfig` name\. Note that annotations will take precedence over labels. To use labels ensure annotation with key
`k8s.amazonaws.com/eniConfig` or defined key (in `ENI_CONFIG_ANNOTATION_DEF`) is not set on the node.
To select an `ENIConfig` based upon availability zone set this to `failure-domain.beta.kubernetes.io/zone` and create an
`ENIConfig` custom resource for each availability zone (e.g. `us-east-1a`).
