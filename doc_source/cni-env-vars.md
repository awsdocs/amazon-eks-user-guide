# CNI Configuration Variables<a name="cni-env-vars"></a>

The Amazon VPC CNI plugin for Kubernetes supports a number of configuration options, which are set through environment variables\. The following environment variables are available, and all of them are optional\. 

`AWS_VPC_CNI_NODE_PORT_SUPPORT`  
Type: Boolean  
Default: `true`  
Specifies whether `NodePort` services are enabled on a worker node's primary network interface\. This requires additional `iptables` rules and that the kernel's reverse path filter on the primary interface is set to `loose`\.

`AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG`  
Type: Boolean  
Default: `false`  
Specifies that your pods may use subnets and security groups \(within the same VPC as your control plane resources\) that are independent of your cluster's `resourcesVpcConfig`\. By default, pods share the same subnet and security groups as the worker node's primary interface\. Setting this variable to `true` causes `ipamD` to use the security groups and subnets in a worker node's `ENIConfig` for elastic network interface allocation\. You must create an `ENIConfig` custom resource definition for each subnet that your pods will reside in, and then annotate each worker node to use a specific `ENIConfig` \(multiple worker nodes can be annotated with the same `ENIConfig`\)\. Worker nodes can only be annotated with a single `ENIConfig` at a time, and the subnet in the `ENIConfig` must belong to the same Availability Zone that the worker node resides in\. For more information, see [CNI Custom Networking](cni-custom-network.md)\.

`AWS_VPC_K8S_CNI_EXTERNALSNAT`  
Type: Boolean  
Default: `false`  
Specifies whether an external NAT gateway should be used to provide SNAT of secondary ENI IP addresses\. If set to `true`, the SNAT `iptables` rule and off\-VPC IP rule are not applied, and these rules are removed if they have already been applied\.  
Disable SNAT if you need to allow inbound communication to your pods from external VPNs, direct connections, and external VPCs, and your pods do not need to access the Internet directly via an Internet Gateway\. However, your nodes must be running in a private subnet and connected to the internet through an AWS NAT Gateway or another external NAT device\.  
For more information, see [External Source Network Address Translation \(SNAT\)](external-snat.md)\.

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