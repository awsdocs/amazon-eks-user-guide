# CNI Custom Networking<a name="cni-custom-network"></a>

By default, when new network interfaces are allocated for pods, [ipamD](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/docs/cni-proposal.md) uses the worker node's primary elastic network interface's security groups and subnet\. However, there are use cases where your pod network interfaces should use a different security group or subnet, within the same VPC as your control plane security group\.

**Note**  
The use cases discussed in this document require [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) version 1\.4\.0 or later\. To check your CNI version, and upgrade if necessary, see [Amazon VPC CNI Plugin for Kubernetes Upgrades](cni-upgrades.md)\.
+ There are a limited number of IP addresses available in a subnet\. This limits the number of pods can be created in the cluster\. Using different subnets for pod groups allows you to increase the number of available IP addresses\.
+ For security reasons, your pods must use different security groups or subnets than the node's primary network interface\.
+ The worker nodes are configured in public subnets and you wish for your pods to be placed in private subnets using a NAT Gateway\. In this situation, please also read about [External Source Network Address Translation](external-snat.md)\.

**To configure CNI custom networking**

1. Edit the `aws-node` configmap:

   ```
   kubectl edit daemonset -n kube-system aws-node
   ```

1. Add the `AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG` environment variable to the node container spec and set it to `true`:

   ```
   ...
       spec:
         containers:
         - env:
           - name: AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG
             value: "true"
           - name: AWS_VPC_K8S_CNI_LOGLEVEL
             value: DEBUG
           - name: MY_NODE_NAME
   ...
   ```

1. Save the file and exit your text editor\.

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

1. Create an `ENIConfig` custom resource for each subnet for pods to reside\.

   1. Create a unique file for each elastic network interface configuration to use with the following information\. Replacing the subnet and security group IDs with your own values\. For this example, the file is called `group1-pod-netconfig.yaml`\.
**Note**  
Each subnet and security group combination requires its own custom resource definition\.

      ```
      apiVersion: crd.k8s.amazonaws.com/v1alpha1
      kind: ENIConfig
      metadata:
       name: group1-pod-netconfig
      spec:
       subnet: subnet-0c4678ec01ce68b24
       securityGroups:
       - sg-066c7927a794cf7e7
       - sg-08f5f22cfb70d8405
       - sg-0bb293fc16f5c2058
      ```

   1. Apply each custom resource file that you created earlier to your cluster with the following command:

      ```
      kubectl apply -f group1-pod-netconfig.yaml
      ```

**Applying an ENIConfig to a node**

For each node in your cluster you can specify an `ENIConfig` by applying an annotation or a label. By default the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) will look at the annotation or label with the key _k8s.amazonaws.com/eniConfig_. Worker nodes can only utilise a single `ENIConfig` value at a time\. The subnet in the `ENIConfig` must belong to the same Availability Zone in which the worker node resides\. If both a label and an annotation are specified, the plugin will use the value specified in the annotation. If neither a label or an annotation are specified, the plugin will use the `ENIConfig` named `default`\.

**Note**
Prior to the release of [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) version 1\.4\.0 only annotations were supported for specifying the `ENIConfig` and it was not possible to change the annotation key from the default _k8s.amazonaws.com/eniConfig_. Further note that an `ENIConfig` was not supported in versions prior to 1\.2\.1. To check your CNI version, and upgrade if necessary, see [Amazon VPC CNI Plugin for Kubernetes Upgrades](cni-upgrades.md)\.

To apply an annotation to an instance:

```
kubectl annotate node <nodename>.<region>.compute.internal k8s.amazonaws.com/eniConfig=group1-pod-netconfig
```

To apply a label to an instance:

```
kubectl annotate label <nodename>.<region>.compute.internal k8s.amazonaws.com/eniConfig=group1-pod-netconfig

```

Because Labels can be applied to nodes on startup you can use this to your advantage to ensure that nodes are started with the desired label. For example, using the [**bootstrap.sh**](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) script.

```
/etc/eks/bootstrap.sh mycluster --kubelet-extra-args "--node-labels k8s.amazonaws.com/eniConfig=group1-pod-netconfig"
```

For more information on bootstraping containers please refer to the [*Launching Amazon EKS Worker Nodes*](launch-workers.md) page.

To change the annotation or label key that the plugin will check you can use the `ENI_CONFIG_ANNOTATION_DEF` and `ENI_CONFIG_LABEL_DEF` environment variables applied to the pod. For example, inside the node container spec:

```
...
    spec:
      containers:
      - env:
        - name: AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG
          value: "true"
        - name: ENI_CONFIG_ANNOTATION_DEF
          value: my_custom_annotation
        - name: ENI_CONFIG_LABEL_DEF
          value: my_custom_label
        - name: AWS_VPC_K8S_CNI_LOGLEVEL
          value: DEBUG
        - name: MY_NODE_NAME
...
```

Because by default Kubernetes will put the availability zone of a node in the _failure-domain.beta.kubernetes.io/zone_ label you can use this label in your `ENI_CONFIG_LABEL_DEF` and name your `ENIConfig` custom resources after each Availability Zone in your VPC by specifying this in the node container spec:

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

For example, on the assumption that `subnet-0c4678ec01ce68b24` is in the **us-east-1a** availability zone, you could use the following `ENIConfig` for the **us-east-1a** availability zone:

```
apiVersion: crd.k8s.amazonaws.com/v1alpha1
kind: ENIConfig
metadata:
 name: us-east-1a
spec:
 subnet: subnet-0c4678ec01ce68b24
 securityGroups:
 - sg-066c7927a794cf7e7
 - sg-08f5f22cfb70d8405
 - sg-0bb293fc16f5c2058
 ```
