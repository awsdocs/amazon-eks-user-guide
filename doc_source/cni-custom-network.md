# CNI Custom Networking<a name="cni-custom-network"></a>

By default, when new network interfaces are allocated for pods, [ipamD](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/docs/cni-proposal.md) uses the worker node's primary elastic network interface's security groups and subnet\. However, there are use cases where your pod network interfaces should use a different security group or subnet, within the same VPC as your control plane security group\.

**Note**  
This feature requires [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) version 1\.2\.1 or later\. To check your CNI version, and upgrade if necessary, see [Amazon VPC CNI Plugin for Kubernetes Upgrades](cni-upgrades.md)\.
+ There are a limited number of IP addresses available in a subnet\. This limits the number of pods can be created in the cluster\. Using different subnets for pod groups allows you to increase the number of available IP addresses\.
+ For security reasons, your pods must use different security groups or subnets than the node's primary network interface\.

**To configure CNI custom networking**

1. Edit the `aws-node` daemonset:

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

1. Create an `ENIConfig` custom resource definition for each subnet in which your pods reside\.

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

   1. Apply each custom resource definition file that you created earlier to your cluster with the following command:

      ```
      kubectl apply -f group1-pod-netconfig.yaml
      ```

1. For each node in your cluster, annotate the node with the custom network configuration to use\. Worker nodes can only be annotated with a single `ENIConfig` value at a time\. The subnet in the `ENIConfig` must belong to the same Availability Zone in which the worker node resides\.

   ```
   kubectl annotate node <nodename>.<region>.compute.internal k8s.amazonaws.com/eniConfig=group1-pod-netconfig
   ```