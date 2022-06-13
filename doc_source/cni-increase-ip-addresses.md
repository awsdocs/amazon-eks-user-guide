# Increase the amount of available IP addresses for your Amazon EC2 nodes<a name="cni-increase-ip-addresses"></a>

By default, the number of IP addresses available to assign to pods is based on the number of IP addresses assigned to Elastic network interfaces, and the number of network interfaces attached to your Amazon EC2 node\. You can configure version `1.9.0` or later of the Amazon VPC CNI add\-on to assign /28 IPv4 address prefixes\. With 1\.10\.1 or later of the add\-on, you can still assign /28 IPv4 address prefixes, but if your cluster is version 1\.21 or later, and you've [configured it for IPv6](cni-ipv6.md), you can assign /80 IPv6 address prefixes instead\. 

When configured for prefix assignment, the CNI add\-on can assign significantly more IP addresses to a network interface than it can when you assign individual IP addresses\. The node can then assign significantly more available IP addresses to pods\. For more information about the Amazon EC2 capability that enables the add\-on to do this, see [Assigning prefixes to Amazon EC2 network interfaces](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-prefix-eni.html) in the Amazon EC2 User Guide for Linux Instances\. 

Without enabling this capability, the add\-on must make more Amazon EC2 application programming interface \(API\) calls to configure the network interfaces and IP addresses necessary for pod connectivity\. The frequency of these API calls combined with a high number of network interfaces in each VPC can lead to longer pod and instance launch times as clusters grow to larger sizes\. This results in scaling delays to meet the demand of large and spiky workloads, and adds cost and management overhead because you need to provision additional clusters and VPCs to meet scaling requirements\. See the [Kubernetes scalability thresholds](https://github.com/kubernetes/community/blob/master/sig-scalability/configs-and-limits/thresholds.md) for more information\.

**Considerations**
+ AWS Nitro\-based nodes use this capability\. Instances that aren't Nitro\-based continue to allocate individual secondary IP addresses, but have a significantly lower number of IP addresses to assign to pods than Nitro\-based instances\.
+ Once you configure the add\-on to assign prefixes to network interfaces, you can't downgrade your Amazon VPC CNI add\-on to a version lower than `1.9.0` \(or 1\.10\.1\) without removing all nodes in all node groups in your cluster\.
+ Your VPC must have enough available contiguous `/28` IPv4 address blocks to support this capability\.
+ Each instance type supports a maximum number of pods\. If your managed node group consists of multiple instance types, the smallest number of maximum pods for an instance in the cluster is applied to all nodes in the cluster\.
+ If you have an existing managed node group, the next AMI or launch template update of your node group results in new worker nodes coming up with the new IP address prefix assignment\-enabled `max-pod` value\.

**Prerequisites**
+ An existing cluster\. To deploy one, see [Creating an Amazon EKS cluster](create-cluster.md)\. 
+ Version `1.9.0` or later \(for version 1\.20 or earlier clusters or 1\.21 or later clusters configured for IPv4\) or 1\.10\.1 or later \(for version 1\.21 or later clusters configured for IPv6\) of the Amazon VPC CNI add\-on deployed to your cluster\.

**To increase the amount of available IP addresses for your Amazon EC2 nodes**

1. Confirm that your currently\-installed Amazon VPC CNI version is 1\.9\.0 or 1\.10\.1 or later\.

   ```
   kubectl describe daemonset aws-node --namespace kube-system | grep Image | cut -d "/" -f 2
   ```

   The example output is as follows\.

   ```
   amazon-k8s-cni:v1.10.1-eksbuild.1
   ```

   If your version is earlier than 1\.9\.0, then you must update it\. For more information, see the updating sections of [Managing the Amazon VPC CNI add\-on](managing-vpc-cni.md)\.

1. Enable the parameter to assign prefixes to network interfaces for the Amazon VPC CNI `DaemonSet`\. When you deploy a 1\.21 or later cluster, version 1\.10\.1 or later of the VPC CNI add\-on is deployed with it\. If you created the cluster with the IPv6 family, this setting was set to `true` by default\. If you created the cluster with the IPv4 family, this setting was set to `false` by default\.

   ```
   kubectl set env daemonset aws-node -n kube-system ENABLE_PREFIX_DELEGATION=true
   ```
**Important**  
Even if your subnet has free IP addresses, if the subnet does not have any contiguous `/28` blocks available, you will see the following error in the VPC CNI logs:   

   ```
   "failed to allocate a private IP/Prefix address: InsufficientCidrBlocks: The specified subnet does not have enough free cidr blocks to satisfy the request"
   ```
This can happen due to fragmentation of existing secondary IP addresses spread out across a subnet\. To resolve this error, either create a new subnet and launch pods there, or use an Amazon EC2 subnet CIDR reservation to reserve space within a subnet for use with prefix assignment\. For more information, see [Subnet CIDR reservations](https://docs.aws.amazon.com/vpc/latest/userguide/subnet-cidr-reservation.html) in the Amazon VPC User Guide\.

1. If you plan to deploy a managed node group without a launch template, or with a launch template that you haven't specified an AMI ID in, and you're using a version of the VPC add\-on at or later than the versions listed in the prerequisites, then skip to the next step\. Managed node groups automatically calculates the maximum number of pods for you\.

   If you're deploying a self\-managed node group or a managed node group with a launch template that you have specified an AMI ID in, then you must determine the Amazon EKS recommend number of maximum pods for your nodes\. Follow the instructions in [Amazon EKS recommended maximum pods for each Amazon EC2 instance type](choosing-instance-type.md#determine-max-pods), adding **`--cni-prefix-delegation-enabled`** to step 3\. Note the output for use in a later step\.
**Important**  
Managed node groups enforces a maximum number on the value of `maxPods`\. For instances with less than 30 vCPUs the maximum number is 110 and for all other instances the maximum number is 250\. This maximum number is applied whether prefix delegation is enabled or not\. 

1. If you're using a 1\.21 or later cluster configured for IPv6, skip to the next step\.

   Specify the parameters in one of the following options\. To determine which option is right for you and what value to provide for it, see [`WARM_PREFIX_TARGET`, `WARM_IP_TARGET`, and `MINIMUM_IP_TARGET`](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/docs/prefix-and-ip-target.md) on GitHub\.

   You can replace the *example values* with a value greater than zero\.
   + `WARM_PREFIX_TARGET` 

     ```
     kubectl set env ds aws-node -n kube-system WARM_PREFIX_TARGET=1
     ```
   + `WARM_IP_TARGET` or `MINIMUM_IP_TARGET` – If either value is set, it overrides any value set for `WARM_PREFIX_TARGET`\.

     ```
     kubectl set env ds aws-node -n kube-system WARM_IP_TARGET=5
     ```

     ```
     kubectl set env ds aws-node -n kube-system MINIMUM_IP_TARGET=2
     ```

1. Create one of the following types of node groups with at least one Amazon EC2 Nitro Amazon Linux 2 instance type\. For a list of Nitro instance types, see [Instances built on the Nitro System](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html#ec2-nitro-instances) in the Amazon EC2 User Guide for Linux Instances\. This capability is not supported on Windows\. For the options that include *110*, replace it with either the value from step 3 \(recommended\), or your own value\. 
   + **Self\-managed** – Deploy the node group using the instructions in [Launching self\-managed Amazon Linux nodes](launch-workers.md)\. Specify the following text for the **BootstrapArguments** parameter\.

     ```
     --use-max-pods false --kubelet-extra-args '--max-pods=110'
     ```

     If you're using `eksctl` to create the node group, you can use the following command\.

     ```
     eksctl create nodegroup --cluster my-cluster --managed=false --max-pods-per-node 110
     ```
   + **Managed** – Deploy your node group using one of the following options:
     + **Without a launch template or with a launch template without an AMI ID specified** – Complete the procedure in [Creating a managed node group](create-managed-node-group.md)\. Managed node groups automatically calculates the Amazon EKS recommended `max-pods` value for you\.
     + **With a launch template with a specified AMI ID** – In your launch template, specify an Amazon EKS optimized AMI ID, or a custom AMI built off the Amazon EKS optimized AMI, then [deploy the node group using a launch template](launch-templates.md) and provide the following user data in the launch template\. This user data passes arguments into the `bootstrap.sh` file\. For more information about the bootstrap file, see [bootstrap\.sh](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) on GitHub\.

       ```
       /etc/eks/bootstrap.sh my-cluster \
         --use-max-pods false \
         --kubelet-extra-args '--max-pods=110'
       ```

       If you're using `eksctl` to create the node group, you can use the following command\.

       ```
       eksctl create nodegroup --cluster my-cluster --max-pods-per-node 110
       ```

       If you've created a custom AMI that is not built off the Amazon EKS optimized AMI, then you need to custom create the configuration yourself\.
**Note**  
If you also want to assign IP addresses to pods from a different subnet than the instance's, then you need to enable the capability in this step\. For more information, see [Tutorial: Custom networking](cni-custom-network.md)\.

1. Once your nodes are deployed, view the nodes in your cluster\.

   ```
   kubectl get nodes
   ```

   The example output is as follows\.

   ```
   NAME                                           STATUS     ROLES    AGE   VERSION
   ip-192-168-22-103.region-code.compute.internal   Ready      <none>   19m   v1.20.4-eks-6b7464
   ip-192-168-97-94.region-code.compute.internal    Ready      <none>   19m   v1.20.4-eks-6b7464
   ```

1. Describe one of the nodes to determine the `max-pods` for the node\.

   ```
   kubectl describe node node-name ip-192-168-22-103.region-code.compute.internal
   ```

   The example output is as follows\.

   ```
   ...
   Allocatable:
     attachable-volumes-aws-ebs:  25
     cpu:                         1930m
     ephemeral-storage:           76224326324
     hugepages-1Gi:               0
     hugepages-2Mi:               0
     memory:                      7244720Ki
     pods:                        110
   ...
   ```

   In the previous output, `110` is the maximum number of pods that Kubernetes will deploy to the node\.