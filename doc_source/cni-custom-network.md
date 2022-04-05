# CNI custom networking<a name="cni-custom-network"></a>

By default, when new network interfaces are allocated for pods, [ipamD](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/docs/cni-proposal.md) uses the security groups and subnet of the node's primary network interface\. You might want your pods to use a different security group or subnet, within the same VPC as your control plane security group\. For example:
+ There are a limited number of IP addresses available in a subnet\. This might limit the number of pods that can be created in the cluster\. Using different subnets for pods allows you to increase the number of available IP addresses\.
+ For security reasons, your pods must use different security groups or subnets than the node's primary network interface\.
+ The nodes are configured in public subnets and you want the pods to be placed in private subnets using a NAT Gateway\. For more information, see [External source network address translation \(SNAT\)](external-snat.md)\.

**Considerations**
+ The procedures in this topic require the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) version 1\.6\.3\-eksbuild\.1 or later\.
+ Enabling a custom network effectively removes an available network interface \(and all of its available IP addresses for pods\) from each node that uses it\. The primary network interface for the node is not used for pod placement when a custom network is enabled\.
+ The procedure in this topic instructs the Amazon VPC CNI plugin to associate different security groups to secondary network interfaces than are associated to the primary network interface in the instance\. All pods using the secondary network interfaces still share use of the secondary network interfaces and all use the same security groups\.

  If you want to assign different security groups to individual pods, then you can use [Security groups for pods](security-groups-for-pods.md)\. Security groups for pods create additional network interfaces that can each be assigned a unique security group\. Security groups for pods can be used with or without custom networking\.
+ You can't use custom networking if you created your cluster to use the IPv6 family\. If you plan to use custom networking to help alleviate IP address exhaustion, you can use IPv6 instead\. For more information, see [Assigning IPv6 addresses to pods and services](cni-ipv6.md)\.

**To configure CNI custom networking**

1. Confirm that your currently\-installed Amazon VPC CNI plugin version is 1\.6\.3\-eksbuild\.1 or later\.

   ```
   kubectl describe daemonset aws-node \
       --namespace kube-system | grep Image | cut -d "/" -f 2
   ```

   Output:

   ```
   amazon-k8s-cni:1.6.3-eksbuild.1
   ```

   If your version is earlier than 1\.6\.3\-eksbuild\.1, then you must update it\. For more information, see the updating sections of [Managing the Amazon VPC CNI add\-on](managing-vpc-cni.md)\.

1. Associate a secondary CIDR block to your cluster's VPC\. For more information, see [Associating a Secondary IPv4 CIDR Block with Your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html#add-ipv4-cidr) in the *Amazon VPC User Guide*\.

1. Create a subnet in your VPC for each Availability Zone, using your secondary CIDR block\. Your custom subnets must be from a different VPC CIDR block than the subnet that your nodes were launched into\. For more information, see [Creating a subnet in your VPC ](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html#AddaSubnet) in the *Amazon VPC User Guide*\.

1. Set the `AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG` environment variable to `true` in the `aws-node` DaemonSet:

   ```
   kubectl set env daemonset aws-node \
       -n kube-system AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG=true
   ```

1. Create an `ENIConfig` custom resource for each subnet that you want to schedule pods in\.

   1. Create a unique file for each network interface configuration\. Each file must include the following contents with a unique value for `name`\. We highly recommend using a value for `name` that matches the Availability Zone of the subnet because this makes deployment of multi\-Availability Zone Auto Scaling groups simpler \(see step 5c below\)\. 

      In this example, a file named `us-west-2a.yaml` is created\. Replace the *example values* with your own values\. In this example, we follow best practices and set the value for `name` to the Availability Zone that the subnet is in\. If you don't have a specific security group that you want to attach for your pods, you can leave that value empty for now\. Later, you specify the node security group in the ENIConfig\.

      ```
      apiVersion: crd.k8s.amazonaws.com/v1alpha1
      kind: ENIConfig
      metadata: 
        name: us-west-2a
      spec: 
        securityGroups: 
          - sg-0dff111a1d11c1c11
        subnet: subnet-011b111c1f11fdf11
      ```
**Note**  
Each subnet and security group combination requires its own custom resource\. If you have multiple subnets in the same Availability Zone, use the following command to annotate the nodes in each subnet with the matching config name\.  

        ```
        kubectl annotate node \
           node-name.region-code.compute.internal \
            k8s.amazonaws.com/eniConfig=subnet1ConfigName
        ```
If you don't specify a valid security group for the VPC, and you're using version 1\.8\.0 or later of the VPC CNI plugin, then the security groups associated with the node's primary elastic network interface are used\. If you're using a version of the plugin that is earlier than 1\.8\.0, then the default security group for the VPC is assigned to secondary elastic network interfaces\.
If you specified a security group, ensure that the recommended or minimum required security group settings for the cluster, control plane and node security groups are met\. For more information, see [Amazon EKS security group considerations](sec-group-reqs.md)\.

   1. Apply each custom resource file that you created to your cluster with the following command:

      ```
      kubectl apply -f us-west-2a.yaml
      ```

   1. \(Optional, but recommended for multi\-Availability Zone node groups\) By default, Kubernetes applies the Availability Zone of a node to the `topology.kubernetes.io/zone` label\. If you named your `ENIConfig` custom resources after each Availability Zone in your VPC, as recommended in step 5a, then you can enable Kubernetes to automatically apply the corresponding `ENIConfig` for the node's Availability Zone with the following command\.

      ```
      kubectl set env daemonset aws-node \
          -n kube-system ENI_CONFIG_LABEL_DEF=topology.kubernetes.io/zone
      ```
**Note**  
Ensure that an annotation with the key `k8s.amazonaws.com/eniConfig` for the `ENI_CONFIG_ANNOTATION_DEF` environment variable doesn't exist in the container spec for the `aws-node` daemonset\. If it exists, it overrides the `ENI_CONFIG_LABEL_DEF` value, and should be removed\. You can check to see if the variable is set with the **kubectl describe daemonset aws\-node \-n kube\-system \| grep ENI\_CONFIG\_ANNOTATION\_DEF** command\. If no output is returned, then the variable is not set\.

1. If you plan to deploy a managed node group without a launch template, or with a launch template that you haven't specified an AMI ID in, then skip to step 7 and use the **Managed, Without a launch template or with a launch template without an AMI ID specified** option\. Managed node groups automatically calculates the maximum pods value for you\.

   If you're deploying a self\-managed node group or a managed node group with a launch template that you have specified an AMI ID in, then you must determine the Amazon EKS recommend number of maximum pods for your nodes\. Follow the instructions in [Amazon EKS recommended maximum pods for each Amazon EC2 instance type](choosing-instance-type.md#determine-max-pods), adding **`--cni-custom-networking-enabled`** to step 3\. Note the output for use in a later step\.

1. Create one of the following types of node groups\. For additional instance selection criteria, see [Choosing an Amazon EC2 instance type](choosing-instance-type.md)\. For the options that include *20*, replace it with either the value from the previous step \(recommended\) or your own value\. 
   + **Self\-managed** – Deploy the node group using the instructions in [Launching self\-managed Amazon Linux nodes](launch-workers.md)\. Don't specify the subnets that you specified in the `ENIConfig` resources that you deployed\. Specify the following text for the **BootstrapArguments** parameter\.

     ```
     --use-max-pods false --kubelet-extra-args '--max-pods=20'
     ```
   + **Managed** – Deploy your node group using one of the following options:
     + **Without a launch template or with a launch template without an AMI ID specified** – Complete the procedure in [Creating a managed node group](create-managed-node-group.md)\. Managed node groups automatically calculates the Amazon EKS recommended `max-pods` value for you\.
     + **With a launch template with a specified AMI ID** – In your launch template, specify an Amazon EKS optimized AMI ID, or a custom AMI built off the Amazon EKS optimized AMI, then [deploy the node group using a launch template](launch-templates.md) and provide the following user data in the launch template\. This user data passes arguments into the `bootstrap.sh` file\. For more information about the bootstrap file, see [bootstrap\.sh](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) on GitHub\.

       ```
       /etc/eks/bootstrap.sh my-cluster \
           --use-max-pods false \
           --kubelet-extra-args '--max-pods=20'
       ```

       If you've created a custom AMI that is not built off the Amazon EKS optimized AMI, then you need to custom create the configuration yourself\.
**Note**  
If you want your nodes to support a significantly higher number of pods, run the script in [Amazon EKS recommended maximum pods for each Amazon EC2 instance type](choosing-instance-type.md#determine-max-pods) again, adding the `--cni-prefix-delegation-enabled` option to the command\. For example, *110* is returned for an `m5.large` instance type\. To enable this capability, see [Increase the amount of available IP addresses for your Amazon EC2 nodes](cni-increase-ip-addresses.md)\. You can use this   
capability with custom networking\.

1. After your node group is created, record the security group that was created for the subnet and apply the security group to the associated `ENIConfig`\. Edit each `ENIConfig` with the following command, replacing *eniconfig\-name* with your value:

   ```
   kubectl edit eniconfig.crd.k8s.amazonaws.com/eniconfig-name
   ```

   If you followed best practices in step 5, the `eniconfig-name` corresponds to the Availability Zone name\.

   The `spec` section should look like the following example spec:

   ```
   spec:
     securityGroups:
     - sg-0dff222a2d22c2c22
     subnet: subnet-022b222c2f22fdf22
   ```
**Note**  
If you use the security group that was created, ensure that the recommended or minimum required security group settings for the cluster, control plane and node security groups are met\. For more information, see [Amazon EKS security group considerations](sec-group-reqs.md)\.

1. If you had any nodes in your cluster with running pods before you switched to the custom CNI networking feature, you should cordon and drain the nodes to gracefully shutdown the pods and then terminate the nodes\. Only new nodes that are registered with the `k8s.amazonaws.com/eniConfig` label use the custom networking feature\.