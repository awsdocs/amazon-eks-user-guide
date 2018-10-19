# External Source Network Address Translation \(SNAT\)<a name="external-snat"></a>

By default, the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) configures pods with source network address translation \(SNAT\) enabled\. This sets the return address for a packet to the primary public IP of the instance and allows for communication with the internet\. In this default configuration, when you use an internet gateway and a public address, the return packet is routed to the correct Amazon EC2 instance\.

![\[SNAT enabled\]](http://docs.aws.amazon.com/eks/latest/userguide/images/SNAT-enabled.jpg)

However, SNAT can cause issues if traffic from another private IP space \(for example, [VPC peering](https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html), [Transit VPC](https://docs.aws.amazon.com/aws-technical-content/latest/aws-vpc-connectivity-options/transit-vpc.html), or [Direct Connect](https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html)\) attempts to communicate directly to a pod that is not attached to the primary elastic network interface of the Amazon EC2 instance\. To specify that NAT be handled by an external device \(such as a NAT gateway, and not on the instance itself\), you can disable SNAT on the instance by setting the `AWS_VPC_K8S_CNI_EXTERNALSNAT` environment variable to `true`\. Disable SNAT to allow inbound communication to your pods from external VPNs, direct connections, and external VPCs, and your pods do not need to access the internet directly via an internet gateway\.

**Note**  
SNAT is required for nodes that reside in a public subnet\. To use external SNAT, your nodes must reside in a private subnet and connect to the internet through a NAT gateway or another external NAT device\.

![\[SNAT disabled\]](http://docs.aws.amazon.com/eks/latest/userguide/images/SNAT-disabled.jpg)

**To disable SNAT on your worker nodes**

1. Edit the `aws-node` configmap:

   ```
   kubectl edit daemonset -n kube-system aws-node
   ```

1. Add the `AWS_VPC_K8S_CNI_EXTERNALSNAT` environment variable to the node container spec and set it to `true`:

   ```
   ...
       spec:
         containers:
         - env:
           - name: AWS_VPC_K8S_CNI_EXTERNALSNAT
             value: "true"
           - name: AWS_VPC_K8S_CNI_LOGLEVEL
             value: DEBUG
           - name: MY_NODE_NAME
   ...
   ```

1. Save the file and exit your text editor\.