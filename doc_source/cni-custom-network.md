# CNI Custom Networking<a name="cni-custom-network"></a>

By default, when new network interfaces are allocated for pods, [ipamD](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/docs/cni-proposal.md) uses the worker node's primary elastic network interface's security groups and subnet\. However, there are use cases where your pod network interfaces should use a different security group or subnet, within the same VPC as your control plane security group\. For example:
+ There are a limited number of IP addresses available in a subnet\. This limits the number of pods can be created in the cluster\. Using different subnets for pod groups allows you to increase the number of available IP addresses\.
+ For security reasons, your pods must use different security groups or subnets than the node's primary network interface\.
+ The worker nodes are configured in public subnets and you want the pods to be placed in private subnets using a NAT Gateway\. For more information, see [External Source Network Address Translation \(SNAT\)](external-snat.md)\.

**Note**  
The use cases discussed in this topic require [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) version 1\.4\.0 or later\. To check your CNI version, and upgrade if necessary, see [Amazon VPC CNI Plugin for Kubernetes Upgrades](cni-upgrades.md)\.

Enabling this feature effectively removes an available elastic network interface \(and all of its available IP addresses for pods\) from each worker node that uses it\. The primary network interface for the worker node is not used for pod placement when this feature is enabled\. You should choose larger instance types with more available elastic network interfaces if you choose to enable this feature\.

Once you enable custom network and apply ENIConfig in different subnet or VPC CIDR, please note that the primary elastic network interface cannot be used to provide Pod IP addresses. If you are using [Amazon EKS-Optimized Linux AMI](https://docs.aws.amazon.com/en_us/eks/latest/userguide/eks-optimized-ami.html), it is necessary to reduce the max number of Pods that can be scheduled on Node as defined in the [eni-max-pods.txt](https://github.com/awslabs/amazon-eks-ami/blob/master/files/eni-max-pods.txt) config file and restart kubelet. This change will let kubelet running on worker node apply new `--max-pods` configuration. For more information, see [kubelet reference](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/) in the *Kuberentes documentation*.

The following formula explains how to get the number of Pods that can be scheduled on your worker node after you apply the configuration:

```
maxPods = (number of interfaces - 1) * (max IPv4 address per interface - 1) + 2
```

For example: If you are using m5.large instance type, it supports 3 network interfaces, 10 IPv4 addresses per interface, so you will have 20 available IP addresses that can be used on this m5.large worker node:

```
maxPods = (3 - 1) * (10 - 1) + 2 = 20
```

To view a table that lists the maximum number of network interfaces per instance type, see [Elastic Network Interfaces - IP Addresses Per Network Interface Per Instance Type](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html) in the *Amazon EC2 User Guide*

Note: If you expect to enable custom networking feature in your EKS cluster and you are using Amazon EKS-optimized AMI, you can set up the parameter `--use-max-pods` as **false** and add the number of maxPods by applying `--kubelet-extra-args` argument in [bootstrapping script(bootstrap.sh)](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) to make your worker nodes can support this function. If you use the Amazon EKS\-provided AWS CloudFormation templates to create your worker node groups, it is same by adding following option to the **BootstrapArguments** field in the AWS CloudFormation console when launching unmanaged nodegroup:

```
--use-max-pods false --kubelet-extra-args '--max-pods=<NUMBER_OF_PODS>'
```

**To configure CNI custom networking**

1. Associate a secondary CIDR block to your cluster's VPC\. For more information, see [Associating a Secondary IPv4 CIDR Block with Your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html#add-ipv4-cidr) in the *Amazon VPC User Guide*\.

1. Create a subnet in your VPC for each Availability Zone, using your secondary CIDR block\. Your custom subnets must be from a different VPC CIDR block than the subnet that your worker nodes were launched into\. For more information, see [Creating a Subnet in Your VPC ](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html#AddaSubnet) in the *Amazon VPC User Guide*\.

1. Set the `AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG=true` environment variable to `true` in the `aws-node` DaemonSet:

   ```
   kubectl set env daemonset aws-node -n kube-system AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG=true
   ```

1. Define a new `ENIConfig` custom resource for your cluster\.

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

   1. Create a unique file for each elastic network interface configuration to use with the following information\. Replacing the subnet and security group IDs with your own values\. If you don't have a specific security group that you want to attach for your pods, you can leave that value empty for now\. Later, you will specify the worker node security group in the `ENIConfig`\.

      For this example, the file is called `custom-pod-netconfig.yaml`\.
**Note**  
Each subnet and security group combination requires its own custom resource\.

      ```
      apiVersion: crd.k8s.amazonaws.com/v1alpha1
      kind: ENIConfig
      metadata: 
        name: custom-pod-netconfig
      spec: 
        securityGroups: 
          - sg-0dff363a7d37c3c61
        subnet: subnet-017b472c2f79fdf96
      ```

   1. Apply each custom resource file that you created earlier to your cluster with the following command:

      ```
      kubectl apply -f custom-pod-netconfig.yaml
      ```

1. Create a new worker node group for each `ENIConfig` that you configured, and limit the Auto Scaling group to the same Availability Zone as the `ENIConfig`\. 

   Follow the steps in [Launching Amazon EKS Linux Worker Nodes](launch-workers.md) to create each new worker node group\. When you create each group, apply the `k8s.amazonaws.com/eniConfig` label to the node group, and set the value to the name of the `ENIConfig` to use for that worker node group\.
   + If you use `eksctl` to create your worker node groups, add the following flag to your `create cluster` command:

     ```
     --node-labels k8s.amazonaws.com/eniConfig=custom-pod-netconfig
     ```
   + If you use the Amazon EKS\-provided AWS CloudFormation templates to create your worker node groups, add the following option to the **BootstrapArguments** field in the AWS CloudFormation console: 

     ```
     --kubelet-extra-args '--node-labels=k8s.amazonaws.com/eniConfig=custom-pod-netconfig'
     ```

1. After your worker node groups are created, record the security group that was created for each worker node group and apply it to its associated `ENIConfig`\. Edit each `ENIConfig` with the following command, replacing the red text with your value\):

   ```
   kubectl edit eniconfig.crd.k8s.amazonaws.com/custom-pod-netconfig
   ```

   The `spec` section should look like this:

   ```
   spec:
     securityGroups:
     - sg-08052d900a2c7fb0a
     subnet: subnet-017b472c2f79fdf96
   ```

1. If you have any worker nodes in your cluster that had pods placed on them before you completed this procedure, you should terminate them\. Only new nodes that are registered with the `k8s.amazonaws.com/eniConfig` label will use the new custom networking feature\.

**To automatically apply an ENIConfig to a node based on its Availability Zone**
+ By default, Kubernetes applies the availability zone of a node to the `failure-domain.beta.kubernetes.io/zone` label\. You can name your `ENIConfig` custom resources after each Availability Zone in your VPC, and then specify this label as the value of the `ENI_CONFIG_LABEL_DEF` environment variable in the `aws-node` container spec for your worker nodes\.

  ```
  ...
      spec:
        containers:
        - env:
          - name: AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG
            value: "true"
          - name: ENI_CONFIG_LABEL_DEF
            value: failure-domain.beta.kubernetes.io/zone
          - name: AWS_VPC_K8S_CNI_LOGLEVEL
            value: DEBUG
          - name: MY_NODE_NAME
  ...
  ```

  For example, if `subnet-0c4678ec01ce68b24` is in the `us-east-1a` Availability Zone, you could use the following `ENIConfig` for that Availability Zone by naming it `us-east-1a`:

  ```
  apiVersion: crd.k8s.amazonaws.com/v1alpha1
  kind: ENIConfig
  metadata:
   name: us-east-1a
  spec:
    securityGroups:
    - sg-08052d900a2c7fb0a
    subnet: subnet-0c4678ec01ce68b24
  ```
