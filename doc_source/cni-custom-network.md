# CNI custom networking<a name="cni-custom-network"></a>

By default, when new network interfaces are allocated for pods, [ipamD](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/docs/cni-proposal.md) uses the security groups and subnet of the node's primary network interface\. You might want your pods to use a different security group or subnet, within the same VPC as your control plane security group\. For example:
+ There are a limited number of IP addresses available in a subnet\. This might limit the number of pods that can be created in the cluster\. Using different subnets for pods allows you to increase the number of available IP addresses\.
+ For security reasons, your pods must use different security groups or subnets than the node's primary network interface\.
+ The nodes are configured in public subnets and you want the pods to be placed in private subnets using a NAT Gateway\. For more information, see [External source network address translation \(SNAT\)](external-snat.md)\.

**Note**  
You can configure custom networking for self\-managed node groups or for managed node groups that were created with a [launch template that uses a custom AMI](launch-templates.md#launch-template-custom-ami)\. The procedures in this topic require the [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) version 1\.4\.0 or later\. To check your CNI version, and update if necessary, see [Updating the Amazon VPC CNI self\-managed add\-on](managing-vpc-cni.md#updating-vpc-cni-add-on)\.
Enabling a custom network effectively removes an available network interface \(and all of its available IP addresses for pods\) from each node that uses it\. The primary network interface for the node is not used for pod placement when a custom network is enabled\.
The procedure in this topic instructs the CNI plugin to associate different security groups to secondary network interfaces than are associated to the primary network interface in the instance\. All pods using the secondary network interfaces will still share use of the secondary network interfaces and will all use the same security groups\. If you want to assign different security groups to individual pods, then you can use [Security groups for pods](security-groups-for-pods.md)\. Security groups for pods create additional network interfaces that can each be assigned a unique security group\. Security groups for pods can be used with or without custom networking\.

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
   amazon-k8s-cni:1.9.x-eksbuild.y
   ```

1. If you have version 1\.3 or later of the CNI installed, you can skip to step 6\. Define a new `ENIConfig` custom resource for your cluster\.

   1. Create a file named *`ENIConfig.yaml`* with the following contents:

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

   1. Create a unique file for each network interface configuration\. Each file must include the following contents with a unique value for `name`\. We highly recommend using a value for `name` that matches the Availability Zone of the subnet because this makes deployment of multi\-Availability Zone Auto Scaling groups simpler \(see step 6c below\)\. 

      In this example, a file named `us-west-2a.yaml` is created\. Replace the *<example values>* \(including *`<>`*\) for `name`, `subnet`, and `securityGroups` with your own values\. In this example, we follow best practices and set the value for `name` to the Availability Zone that the subnet is in\. If you don't have a specific security group that you want to attach for your pods, you can leave that value empty for now\. Later, you specify the node security group in the ENIConfig\.

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
Each subnet and security group combination requires its own custom resource\. If you have multiple subnets in the same Availability Zone, use the following command to annotate the nodes in each subnet with the matching config name\.  

        ```
        kubectl annotate node <node-name>.<region>.compute.internal k8s.amazonaws.com/eniConfig=<subnet1ConfigName>
        ```
If you don't specify a valid security group for the VPC, the default security group for the VPC is assigned to secondary ENI's\.

   1. Apply each custom resource file that you created to your cluster with the following command:

      ```
      kubectl apply -f <us-west-2a>.yaml
      ```

   1. \(Optional, but recommended for multi\-Availability Zone node groups\) By default, Kubernetes applies the Availability Zone of a node to the `failure-domain.beta.kubernetes.io/zone` label\. If you named your `ENIConfig` custom resources after each Availability Zone in your VPC, as recommended in step 6a, then you can enable Kubernetes to automatically apply the corresponding `ENIConfig` for the node's Availability Zone with the following command\.

      ```
      kubectl set env daemonset aws-node -n kube-system ENI_CONFIG_LABEL_DEF=failure-domain.beta.kubernetes.io/zone
      ```
**Note**  
Ensure that an annotation with the key `k8s.amazonaws.com/eniConfig` for the `ENI_CONFIG_ANNOTATION_DEF` environment variable doesn't exist in the container spec for the `aws-node` daemonset\. If it exists, it overrides the `ENI_CONFIG_LABEL_DEF` value, and should be removed\. You can check to see if the variable is set with the `kubectl describe daemonset aws-node -n kube-system | grep ENI_CONFIG_ANNOTATION_DEF` command\. If no output is returned, then the variable is not set\.

1. Determine the Amazon EKS recommend number of maximum pods for your nodes\.

   1. Download a script that you can use to calculate the maximum number of pods for each instance type\.

      ```
      curl -o max-pods-calculator.sh https://raw.githubusercontent.com/awslabs/amazon-eks-ami/master/files/max-pods-calculator.sh
      ```

   1. Mark the script as executable on your computer\.

      ```
      chmod +x max-pods-calculator.sh
      ```

   1. Run the script, replacing *`<m5.large>`* \(including *`<>`*\) with the instance type that you plan to deploy and *<1\.9\.*x*\-eksbuild\.*y*>* or later with your Amazon VPC CNI add\-on version\.

      ```
      ./max-pods-calculator.sh --instance-type <m5.large> --cni-version <1.9.x-eksbuild.y> --cni-custom-networking-enabled
      ```

      Output

      ```
      20
      ```

1. Create one of the following types of node groups\. 
   + **Self\-managed** – Deploy the node group using the instructions in [Launching self\-managed Amazon Linux nodes](launch-workers.md)\. Do not specify the subnets that you specified in the `ENIConfig` resources that you deployed\. Specify the following text for the **BootstrapArguments** parameter\.

     ```
     --use-max-pods false --kubelet-extra-args '--max-pods=<20>'
     ```
   + **Managed** – If you use `eksctl`, you can deploy a node group with the following command\. Replace the *<example values>* with your own values\.

     ```
     eksctl create nodegroup \
       --cluster <my-cluster> \
       --region <us-west-2> \
       --name <my-nodegroup> \
       --node-type <m5.large> \
       --managed \
       --max-pods-per-node <20>
     ```

     If you prefer to use a different tool to deploy your managed node group, then you must deploy the node group using a launch template\. In your launch template, specify an Amazon EKS optimized AMI ID, then [deploy the node group using a launch template](launch-templates.md) and provide the following user data\. This user data passes arguments into the `bootstrap.sh` file\. For more information about the bootstrap file, see [bootstrap\.sh](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) on GitHub\.

     ```
     /etc/eks/bootstrap.sh <my-cluster> \
       --kubelet-extra-args '--max-pods=<20>'
     ```
**Note**  
 If you want your nodes to support a significantly higher number of pods, run the script in step 7\.c\. again, adding the `--cni-prefix-delegation-enabled` option to the command\. *110* is returned for an `m5.large` instance type\. If you want your node to support a significantly higher number of pods, see [Increase the amount of available IP addresses for your Amazon EC2 nodes](cni-increase-ip-addresses.md)\.

1. After your node group is created, record the security group that was created for the subnet and apply the security group to the associated `ENIConfig`\. Edit each `ENIConfig` with the following command, replacing *<eniconfig\-name>* with your value:

   ```
   kubectl edit eniconfig.crd.k8s.amazonaws.com/<eniconfig-name>
   ```

   If you followed best practices in step 6, the `eniconfig-name` corresponds to the Availability Zone name\.

   The `spec` section should look like this:

   ```
   spec:
     securityGroups:
     - <sg-0dff222a2d22c2c22>
     subnet: <subnet-022b222c2f22fdf22>
   ```

1. If you had any nodes in your cluster with running Pods before you switched to the custom CNI networking feature, you should cordon and drain the nodes to gracefully shutdown the Pods and then terminate the nodes\. Only new nodes that are registered with the `k8s.amazonaws.com/eniConfig` label use the custom networking feature\.