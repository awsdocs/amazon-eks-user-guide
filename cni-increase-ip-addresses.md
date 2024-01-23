# Increase the amount of available IP addresses for your Amazon EC2 nodes<a name="cni-increase-ip-addresses"></a>

Each Amazon EC2 instance supports a maximum number of elastic network interfaces and a maximum number of IP addresses that can be assigned to each network interface\. Each node requires one IP address for each network interface\. All other available IP addresses can be assigned to `Pods`\. Each `Pod` requires its own IP address\. As a result, you might have nodes that have available compute and memory resources, but can't accommodate additional `Pods` because the node has run out of IP addresses to assign to `Pods`\.

In this topic, you learn how to significantly increase the number of IP addresses that nodes can assign to `Pods` by assigning IP prefixes, rather than assigning individual secondary IP addresses to your nodes\. Each prefix includes several IP addresses\. If you don't configure your cluster for IP prefix assignment, your cluster must make more Amazon EC2 application programming interface \(API\) calls to configure network interfaces and IP addresses necessary for Pod connectivity\. As clusters grow to larger sizes, the frequency of these API calls can lead to longer Pod and instance launch times\. This results in scaling delays to meet the demand of large and spiky workloads, and adds cost and management overhead because you need to provision additional clusters and VPCs to meet scaling requirements\. For more information, see [Kubernetes Scalability thresholds](https://github.com/kubernetes/community/blob/master/sig-scalability/configs-and-limits/thresholds.md) on GitHub\.

**Considerations**
+ Each Amazon EC2 instance type supports a maximum number of Pods\. If your managed node group consists of multiple instance types, the smallest number of maximum Pods for an instance in the cluster is applied to all nodes in the cluster\.
+ By default, the maximum number of `Pods` that you can run on a node is 110, but you can change that number\. If you change the number and have an existing managed node group, the next AMI or launch template update of your node group results in new nodes coming up with the changed value\.
+ When transitioning from assigning IP addresses to assigning IP prefixes, we recommend that you create new node groups to increase the number of available IP addresses, rather than doing a rolling replacement of existing nodes\. Running Pods on a node that has both IP addresses and prefixes assigned can lead to inconsistency in the advertised IP address capacity, impacting the future workloads on the node\. For the recommended way of performing the transition, see [Replace all nodes during migration from Secondary IP mode to Prefix Delegation mode or vice versa](https://github.com/aws/aws-eks-best-practices/blob/master/content/networking/prefix-mode/index_windows.md#replace-all-nodes-during-migration-from-secondary-ip-mode-to-prefix-delegation-mode-or-vice-versa) in the Amazon EKS best practices guide\.
+ For clusters with Linux nodes only\.
  + Once you configure the add\-on to assign prefixes to network interfaces, you can't downgrade your Amazon VPC CNI plugin for Kubernetes add\-on to a version lower than `1.9.0` \(or `1.10.1`\) without removing all nodes in all node groups in your cluster\.
  + If you're also using security groups for Pods, with `POD_SECURITY_GROUP_ENFORCING_MODE`=`standard` and `AWS_VPC_K8S_CNI_EXTERNALSNAT`=`false`, when your Pods communicate with endpoints outside of your VPC, the node's security groups are used, rather than any security groups you've assigned to your Pods\. 

    If you're also using [security groups for Pods](security-groups-for-pods.md), with `POD_SECURITY_GROUP_ENFORCING_MODE`=`strict`, when your `Pods` communicate with endpoints outside of your VPC, the `Pod's` security groups are used\.

**Prerequisites**
+ An existing cluster\. To deploy one, see [Creating an Amazon EKS cluster](create-cluster.md)\. 
+ The subnets that your Amazon EKS nodes are in must have sufficient contiguous `/28` \(for `IPv4` clusters\) or `/80` \(for `IPv6` clusters\) Classless Inter\-Domain Routing \(CIDR\) blocks\. You can only have Linux nodes in an `IPv6` cluster\. Using IP prefixes can fail if IP addresses are scattered throughout the subnet CIDR\. We recommend that following:
  + Using a subnet CIDR reservation so that even if any IP addresses within the reserved range are still in use, upon their release, the IP addresses aren't reassigned\. This ensures that prefixes are available for allocation without segmentation\.
  + Use new subnets that are specifically used for running the workloads that IP prefixes are assigned to\. Both Windows and Linux workloads can run in the same subnet when assigning IP prefixes\.
+ To assign IP prefixes to your nodes, your nodes must be AWS Nitro\-based\. Instances that aren't Nitro\-based continue to allocate individual secondary IP addresses, but have a significantly lower number of IP addresses to assign to Pods than Nitro\-based instances do\.
+ **For clusters with Linux nodes only** – If your cluster is configured for the `IPv4` family, you must have version `1.9.0` or later of the Amazon VPC CNI plugin for Kubernetes add\-on installed\. You can check your current version with the following command\.

  ```
  kubectl describe daemonset aws-node --namespace kube-system | grep Image | cut -d "/" -f 2
  ```

  If your cluster is configured for the `IPv6` family, you must have version `1.10.1` of the add\-on installed\. If your plugin version is earlier than the required versions, you must update it\. For more information, see the updating sections of [Working with the Amazon VPC CNI plugin for Kubernetes Amazon EKS add\-on](managing-vpc-cni.md)\.
+ **For clusters with Windows nodes only**
  + Your cluster and its platform version must be at, or later than the versions in the following table\. To upgrade your cluster version, see [Updating an Amazon EKS cluster Kubernetes version](update-cluster.md)\. If your cluster isn't at the minimum platform version, then you can't assign IP prefixes to your nodes until Amazon EKS has updated your platform version\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/cni-increase-ip-addresses.html)

    You can check your current Kubernetes and platform version by replacing `my-cluster` in the following command with the name of your cluster and then running the modified command: **aws eks describe\-cluster \-\-name *my\-cluster* \-\-query 'cluster\.\{"Kubernetes Version": version, "Platform Version": platformVersion\}'**\.
  + Windows support enabled for your cluster\. For more information, see [Enabling Windows support for your Amazon EKS cluster](windows-support.md)\.

**To increase the amount of available IP addresses for your Amazon EC2 nodes**

1. Configure your cluster to assign IP address prefixes to nodes\. Complete the procedure on the tab that matches your node's operating system\.

------
#### [ Linux ]

   1. Enable the parameter to assign prefixes to network interfaces for the Amazon VPC CNI `DaemonSet`\. When you deploy a `1.21` or later cluster, version `1.10.1` or later of the Amazon VPC CNI plugin for Kubernetes add\-on is deployed with it\. If you created the cluster with the `IPv6` family, this setting was set to `true` by default\. If you created the cluster with the `IPv4` family, this setting was set to `false` by default\.

      ```
      kubectl set env daemonset aws-node -n kube-system ENABLE_PREFIX_DELEGATION=true
      ```
**Important**  
Even if your subnet has available IP addresses, if the subnet does not have any contiguous `/28` blocks available, you will see the following error in the Amazon VPC CNI plugin for Kubernetes logs\.  

      ```
      InsufficientCidrBlocks: The specified subnet does not have enough free cidr blocks to satisfy the request
      ```
This can happen due to fragmentation of existing secondary IP addresses spread out across a subnet\. To resolve this error, either create a new subnet and launch Pods there, or use an Amazon EC2 subnet CIDR reservation to reserve space within a subnet for use with prefix assignment\. For more information, see [Subnet CIDR reservations](https://docs.aws.amazon.com/vpc/latest/userguide/subnet-cidr-reservation.html) in the Amazon VPC User Guide\.

   1. If you plan to deploy a managed node group without a launch template, or with a launch template that you haven't specified an AMI ID in, and you're using a version of the Amazon VPC CNI plugin for Kubernetes at or later than the versions listed in the prerequisites, then skip to the next step\. Managed node groups automatically calculates the maximum number of Pods for you\.

      If you're deploying a self\-managed node group or a managed node group with a launch template that you have specified an AMI ID in, then you must determine the Amazon EKS recommend number of maximum Pods for your nodes\. Follow the instructions in [Amazon EKS recommended maximum Pods for each Amazon EC2 instance type](choosing-instance-type.md#determine-max-pods), adding **`--cni-prefix-delegation-enabled`** to step 3\. Note the output for use in a later step\.
**Important**  
Managed node groups enforces a maximum number on the value of `maxPods`\. For instances with less than 30 vCPUs the maximum number is 110 and for all other instances the maximum number is 250\. This maximum number is applied whether prefix delegation is enabled or not\. 

   1. If you're using a `1.21` or later cluster configured for `IPv6`, skip to the next step\.

      Specify the parameters in one of the following options\. To determine which option is right for you and what value to provide for it, see [`WARM_PREFIX_TARGET`, `WARM_IP_TARGET`, and `MINIMUM_IP_TARGET`](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/docs/prefix-and-ip-target.md) on GitHub\.

      You can replace the `example values` with a value greater than zero\.
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

   1. Create one of the following types of node groups with at least one Amazon EC2 Nitro Amazon Linux 2 instance type\. For a list of Nitro instance types, see [Instances built on the Nitro System](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html#ec2-nitro-instances) in the Amazon EC2 User Guide for Linux Instances\. This capability is not supported on Windows\. For the options that include `110`, replace it with either the value from step 3 \(recommended\), or your own value\. 
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
If you also want to assign IP addresses to Pods from a different subnet than the instance's, then you need to enable the capability in this step\. For more information, see [Custom networking for pods](cni-custom-network.md)\.

------
#### [ Windows ]

   1. Enable assignment of IP prefixes\.

      1. Open the `amazon-vpc-cni` `ConfigMap` for editing\.

         ```
         kubectl edit configmap -n kube-system amazon-vpc-cni -o yaml
         ```

      1. Add the following line to the `data` section\.

         ```
           enable-windows-prefix-delegation: "true"
         ```

      1. Save the file and close the editor\.

      1. Confirm that the line was added to the `ConfigMap`\.

         ```
         kubectl get configmap -n kube-system amazon-vpc-cni -o "jsonpath={.data.enable-windows-prefix-delegation}"
         ```

         If the returned output isn't `true`, then there might have been an error\. Try completing the step again\.
**Important**  
Even if your subnet has available IP addresses, if the subnet does not have any contiguous `/28` blocks available, you will see the following error in the node events\.   

         ```
         "failed to allocate a private IP/Prefix address: InsufficientCidrBlocks: The specified subnet does not have enough free cidr blocks to satisfy the request"
         ```
This can happen due to fragmentation of existing secondary IP addresses spread out across a subnet\. To resolve this error, either create a new subnet and launch Pods there, or use an Amazon EC2 subnet CIDR reservation to reserve space within a subnet for use with prefix assignment\. For more information, see [Subnet CIDR reservations](https://docs.aws.amazon.com/vpc/latest/userguide/subnet-cidr-reservation.html) in the Amazon VPC User Guide\.

   1. \(Optional\) Specify additional configuration for controlling the pre\-scaling and dynamic scaling behavior for your cluster\. For more information, see [Configuration options with Prefix Delegation mode on Windows](https://github.com/aws/amazon-vpc-resource-controller-k8s/blob/master/docs/windows/prefix_delegation_config_options.md) on GitHub\.

      1. Open the `amazon-vpc-cni` `ConfigMap` for editing\. 

         ```
         kubectl edit configmap -n kube-system amazon-vpc-cni -o yaml
         ```

      1. Replace the `example values` with a value greater than zero and add the entries that you require to the `data` section of the `ConfigMap`\. If you set a value for either `warm-ip-target` or `minimum-ip-target`, the value overrides any value set for `warm-prefix-target`\.

         ```
           warm-prefix-target: "1" 
           warm-ip-target: "5"
           minimum-ip-target: "2"
         ```

      1. Save the file and close the editor\.

   1. Create Windows node groups with at least one Amazon EC2 Nitro instance type\. For a list of Nitro instance types, see [Instances built on the Nitro System](https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/instance-types.html#ec2-nitro-instances) in the Amazon Amazon EC2 User Guide for Windows Instances\. By default, the maximum number of Pods that you can deploy to a node is 110\. If you want to increase or decrease that number, specify the following in the user data for the bootstrap configuration\. Replace `max-pods-quantity` with your max pods value\.

      ```
      -KubeletExtraArgs '--max-pods=max-pods-quantity'
      ```

      If you're deploying managed node groups, this configuration needs to be added in the launch template\. For more information, see [Customizing managed nodes with launch templates](launch-templates.md)\. For more information about the configuration parameters for Windows bootstrap script, see [Bootstrap script configuration parameters](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters)\.

------

1. Once your nodes are deployed, view the nodes in your cluster\.

   ```
   kubectl get nodes
   ```

   An example output is as follows\.

   ```
   NAME                                             STATUS     ROLES    AGE   VERSION
   ip-192-168-22-103.region-code.compute.internal   Ready      <none>   19m   v1.XX.X-eks-6b7464
   ip-192-168-97-94.region-code.compute.internal    Ready      <none>   19m   v1.XX.X-eks-6b7464
   ```

1. Describe one of the nodes to determine the value of `max-pods` for the node and the number of available IP addresses\. Replace `192.168.30.193` with the `IPv4` address in the name of one of your nodes returned in the previous output\. 

   ```
   kubectl describe node ip-192-168-30-193.region-code.compute.internal | grep 'pods\|PrivateIPv4Address'
   ```

   An example output is as follows\.

   ```
   pods:                                  110
   vpc.amazonaws.com/PrivateIPv4Address:  144
   ```

   In the previous output, `110` is the maximum number of Pods that Kubernetes will deploy to the node, even though *144* IP addresses are available\.