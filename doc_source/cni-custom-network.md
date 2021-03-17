# CNI custom networking<a name="cni-custom-network"></a>

By default, when new network interfaces are allocated for pods, [ipamD](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/docs/cni-proposal.md) uses the node's primary network interface's security groups and subnet\. You might want your pods to use a different security group or subnet, within the same VPC as your control plane security group\. For example:
+ There are a limited number of IP addresses available in a subnet\. This might limit the number of pods that can be created in the cluster\. Using different subnets for pods allows you to increase the number of available IP addresses\.
+ For security reasons, your pods must use different security groups or subnets than the node's primary network interface\.
+ The nodes are configured in public subnets and you want the pods to be placed in private subnets using a NAT Gateway\. For more information, see [External source network address translation \(SNAT\)](external-snat.md)\.

**Note**  
You can configure custom networking for self\-managed node groups or for managed node groups that were created with a [launch template that uses a custom AMI](launch-templates.md#launch-template-custom-ami)\. The procedures in this topic require the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) version 1\.4\.0 or later\. To check your CNI version, and upgrade if necessary, see [Amazon VPC CNI plugin for Kubernetes upgrades](cni-upgrades.md)\.
Enabling a custom network effectively removes an available network interface \(and all of its available IP addresses for pods\) from each node that uses it\. The primary network interface for the node is not used for pod placement when a custom network is enabled\.
The procedure in this topic instructs the CNI plugin to associate different security groups to secondary network interfaces than are associated to the primary network interface in the instance\. All pods using the secondary network interfaces will still share use of the secondary network interfaces and will all use the same security groups\. If you want to assign different security groups to individual pods, then you can use [Security groups for pods](security-groups-for-pods.md)\. Security groups for pods create additional network interfaces that can each be assigned a unique security group\. security groups for pods can be used with or without custom networking\.

**To configure CNI custom networking**

1. Associate a secondary CIDR block to your cluster's VPC\. For more information, see [Associating a Secondary IPv4 CIDR Block with Your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html#add-ipv4-cidr) in the *Amazon VPC User Guide*\.

1. Create a subnet in your VPC for each Availability Zone, using your secondary CIDR block\. Your custom subnets must be from a different VPC CIDR block than the subnet that your nodes were launched into\. For more information, see [Creating a subnet in your VPC ](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html#AddaSubnet) in the *Amazon VPC User Guide*\.

1. Set the `AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG` environment variable to `true` in the `aws-node` DaemonSet:

   ```
   kubectl set env daemonset aws-node -n kube-system AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG=true
   ```

1. View the currently\-installed CNI version\.

   ```
   kubectl describe daemonset aws-node --namespace kube-system | grep Image | cut -d "/" -f 2
   ```

   Output:

   ```
   amazon-k8s-cni:1.7.5
   ```

1. If you have version 1\.3 or later of the CNI installed, you can skip to step 6\. Define a new `ENIConfig` custom resource for your cluster\.

   1. Create a file called `ENIConfig.yaml` and paste the following content into it:

      ```
      apiVersion: apiextensions.k8s.io/v1beta1
      kind: CustomResourceDefinition
      metadata:
        name: eniconfigs.crd.k8s.amazonaws.com
      spec:
        scope: Cluster
        group: crd.k8s.amazonaws.com
        version: v1alpha1
        names:
          plural: eniconfigs
          singular: eniconfig
          kind: ENIConfig
      ```

   1. Apply the file to your cluster with the following command:

      ```
      kubectl apply -f ENIConfig.yaml
      ```

1. Create an `ENIConfig` custom resource for each subnet that you want to schedule pods in\.

   1. Create a unique file for each network interface configuration\. Each file must include the following contents with a unique value for `name`\. We highly recommend using a value for `name` that matches the Availability Zone of the subnet because this makes deployment of multi\-AZ Auto Scaling groups simpler \(see step 6c below\)\. 

      In this example, a file named `us-west-2a.yaml` is created\. Replace the <example values> for `name`, `subnet`, and `securityGroups` with your own values\. In this example, we follow best practices and set the value for `name` to the Availability Zone that the subnet is in\. If you don't have a specific security group that you want to attach for your pods, you can leave that value empty for now\. Later, you will specify the node security group in the ENIConfig\.

      ```
      apiVersion: crd.k8s.amazonaws.com/v1alpha1
      kind: ENIConfig
      metadata: 
        name: <us-west-2a>
      spec: 
        securityGroups: 
          - <sg-0dff111a1d11c1c11>
        subnet: <subnet-011b111c1f11fdf11>
      ```
**Note**  
- Each subnet and security group combination requires its own custom resource\. If you have multiple subnets in the same Availability Zone, use the following command to annotate the nodes in each subnet with the matching config name\.  

      ```
      kubectl annotate node <node-name>.<region>.compute.internal k8s.amazonaws.com/eniConfig=<subnet1ConfigName>
      ```

- Ensure that `spec.securityGroups` property exists with Security Group Id from same VPC for ENIConfig CustomResourceDefinition manifest. If not exists, aws-cni will assign Default Security Group from VPC to Secondary ENI's of the worker node.

   1. Apply each custom resource file that you created to your cluster with the following command:

      ```
      kubectl apply -f <us-west-2a>.yaml
      ```

   2. \(Optional, but recommended for multi\-Availability Zone node groups\) By default, Kubernetes applies the Availability Zone of a node to the `failure-domain.beta.kubernetes.io/zone` label\. If you named your ENIConfig custom resources after each Availability Zone in your VPC, as recommended in step 6a, then you can enable Kubernetes to automatically apply the corresponding ENIConfig for the node's Availability Zone with the following command\.

      ```
      kubectl set env daemonset aws-node -n kube-system ENI_CONFIG_LABEL_DEF=failure-domain.beta.kubernetes.io/zone
      ```
**Note**  
Ensure that an annotation with the key `k8s.amazonaws.com/eniConfig` for the `ENI_CONFIG_ANNOTATION_DEF` environment variable doesn't exist in the container spec for the `aws-node` daemonset\. If it exists, it overrides the `ENI_CONFIG_LABEL_DEF` value, and should be removed\. You can check to see if the variable is set with the `kubectl describe daemonset aws-node -n kube-system | grep ENI_CONFIG_ANNOTATION_DEF` command\. If no output is returned, then the variable is not set\.

1. Create a new self\-managed node group\. For managed node groups, use a custom AMI with a [launch template](launch-templates.md#launch-template-custom-ami)\.

   1. Determine the maximum number of pods that can be scheduled on each node using the following formula\. 

      ```
      maxPods = (number of interfaces - 1) * (max IPv4 addresses per interface - 1) + 2
      ```

      For example, the `m5.large` instance type supports three network interfaces and ten IPv4 addresses for each interface\. Inserting the values into the formula, the instance can support up to 20 pods, as shown in the following calculation\.

      ```
      maxPods = (3 - 1) * (10 - 1) + 2 = 20
      ```

      For more information about the maximum number of network interfaces for each instance type, see [IP addresses per network interface per instance type](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#AvailableIpPerENI) in the *Amazon EC2 User Guide for Linux Instances*\.

   1. Follow the steps for **Self\-managed nodes** in [Launching self\-managed Amazon Linux nodes](launch-workers.md) to create a new self\-managed node group\. After you've opened the AWS CloudFormation template, enter values as described in the instructions\. Specify the subnets that you specified in the `ENIConfig` resources that you deployed\. For the **BootstrapArguments** field, enter the following value\.

      ```
      --use-max-pods false --kubelet-extra-args '--max-pods=<20>'
      ```

1. After your node group is created, record the security group that was created for subnet and apply the security group to the associated `ENIConfig`\. Edit each `ENIConfig` with the following command, replacing <eniconfig\-name> with your value:

   ```
   kubectl edit eniconfig.crd.k8s.amazonaws.com/<eniconfig-name>
   ```

   If you followed best practices from steps 6a and 6c, the `eniconfig-name` corresponds to the Availability Zone name\.

   The `spec` section should look like this:

   ```
   spec:
     securityGroups:
     - <sg-0dff222a2d22c2c22>
     subnet: <subnet-022b222c2f22fdf22>
   ```

1. If you have any nodes in your cluster that had pods placed on them before you completed this procedure, you should terminate them\. Only new nodes that are registered with the `k8s.amazonaws.com/eniConfig` label use the new custom networking feature\.