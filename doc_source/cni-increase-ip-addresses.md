# Increase the amount of available IP addresses for your Amazon EC2 nodes<a name="cni-increase-ip-addresses"></a>

By default, the number of IP addresses available to assign to pods is based on the number of IP addresses assigned to Elastic network interfaces, and the number of network interfaces attached to your Amazon EC2 node\. You can configure version `1.9.0` or later of the Amazon VPC CNI add\-on to assign `/28` \(16 IP addresses\) IP address prefixes, instead of assigning individual IP addresses to network interfaces\. The node can then assign significantly more available IP addresses to pods\. For more information about the Amazon EC2 capability that enables the add\-on to do this, see [Assigning prefixes to Amazon EC2 network interfaces](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-prefix-eni.html) in the Amazon EC2 User Guide for Linux Instances\. 

Without enabling this capability, the add\-on must make more Amazon EC2 application programming interface \(API\) calls to configure the network interfaces and IP addresses necessary for pod connectivity\. The frequency of these API calls combined with a high number of network interfaces in each VPC can lead to longer pod and instance launch times as clusters grow to larger sizes\. This results in scaling delays to meet the demand of large and spiky workloads, and adds cost and management overhead because you need to provision additional clusters and VPCs to meet scaling requirements\.

**Considerations**
+ AWS Nitro\-based nodes use this capability\. Instances that aren't Nitro\-based continue to allocate individual secondary IP addresses, but have a significantly lower number of IP addresses to assign to pods than Nitro\-based instances\.
+ Once you configure the add\-on to assign prefixes to network interfaces, you can't downgrade your Amazon VPC CNI add\-on to a version lower than `1.9.0` without removing all nodes in all node groups in your cluster\.
+ Make sure that your VPC has enough available IP addresses to support this capability, because the addresses are allocated from your VPC's address space\.

**Prerequisites**
+ An existing cluster\. If you don't have a cluster, you can create one using one of the [Getting started with Amazon EKS](getting-started.md) guides\.
+ Version `1.9.0` or later of the Amazon VPC CNI add\-on added to your cluster\. To add or update the add\-on on your cluster, see [Managing the Amazon VPC CNI add\-on](managing-vpc-cni.md)\.

**To configure CNI prefix delegation**

1. Enable the parameter to assign prefixes to network interfaces for the Amazon VPC CNI Daemonset\.

   ```
   kubectl set env daemonset aws-node -n kube-system ENABLE_PREFIX_DELEGATION=true
   ```

1. Determine the Amazon EKS recommend number of maximum pods for your nodes\.

   1. Download a script that you can use to calculate the maximum number of pods for each instance type\.

      ```
      curl -o max-pods-calculator.sh https://github.com/awslabs/amazon-eks-ami/blob/master/files/max-pods-calculator.sh
      ```

   1. Mark the script as executable on your computer\.

      ```
      chmod +x max-pods-calculator.sh
      ```

   1. In the remaining steps, replace all *<example values>* \(including *<>*\) with your own values\. Replace *`<m5.large>`* with the instance type that you plan to deploy and *<1\.9\.*x*\-eksbuild\.*y*>* or later with your Amazon VPC CNI add\-on version\.

      ```
      ./max-pods-calculator.sh --instance-type <m5.large> --cni-version <1.9.x-eksbuild.y> --cni-prefix-delegation-enabled
      ```

      Output

      ```
      110
      ```
**Note**  
`110` is the maximum number of pods recommended by Amazon EKS for a `m5.large` instance\. If the `ENABLE_PREFIX_DELEGATION` parameter is not enabled, the recommended maximum pods is `29`\.

1. Specify the parameters in one of the following options\. To determine which option is right for you and what value to provide for it, see [`WARM_PREFIX_TARGET`, `WARM_IP_TARGET`, and `MINIMUM_IP_TARGET`](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/docs/prefix-and-ip-target.md) on GitHub\.

   You can replace the *<example values>* with a value greater than zero\.
   + `WARM_PREFIX_TARGET` 

     ```
     kubectl set env ds aws-node -n kube-system WARM_PREFIX_TARGET=<1>
     ```
   + `WARM_IP_TARGET` – If this value is set, it overrides any value set for `WARM_PREFIX_TARGET`\. If using this option, you must specify both of the following parameters\.

     ```
     kubectl set env ds aws-node -n kube-system WARM_IP_TARGET=<5>
     ```

     `MINIMUM_IP_TARGET` – If this value is set, it overrides any value set for `WARM_PREFIX_TARGET`\.

     ```
     kubectl set env ds aws-node -n kube-system MINIMUM_IP_TARGET=<2>
     ```

1. Create one of the following types of node groups with at least one Amazon EC2 Nitro Amazon Linux 2 instance type\. For a list of Nitro instance types, see [Instances built on the Nitro System](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html#ec2-nitro-instances) in the Amazon EC2 User Guide for Linux Instances\. This capability is not supported on Windows\. Replace *<110>* \(including *`<>`*\) with either the value from step 2 \(recommended\), or your own value\. 
   + **Self\-managed** – Deploy the node group using the instructions in [Launching self\-managed Amazon Linux nodes](launch-workers.md)\. Specify the following text for the **BootstrapArguments** parameter\.

     ```
     --use-max-pods false --kubelet-extra-args '--max-pods=<110>'
     ```
   + **Managed** – If you use eksctl, you can deploy a node group with the following command\.

     ```
     eksctl create nodegroup \
       --cluster <my-cluster> \
       --region <us-west-2> \
       --name <my-nodegroup> \
       --node-type <m5.large> \
       --managed \
       --max-pods-per-node <110>
     ```

     If you prefer to use a different tool to deploy your managed node group, then you must deploy the node group using a launch template\. In your launch template, specify an Amazon EKS optimized AMI ID, then [deploy the node group using a launch template](launch-templates.md) and provide the following user data\. This user data passes arguments into the `bootstrap.sh` file\. For more information about the bootstrap file, see [bootstrap\.sh](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) on GitHub\.

     ```
     /etc/eks/bootstrap.sh <my-cluster> \
       --kubelet-extra-args '--max-pods=<110>'
     ```
**Note**  
 If you also want to use custom networking, you need to enable it in this step\. For more information about custom networking, see [CNI custom networking](cni-custom-network.md)\.

1. Once your nodes are deployed, view the nodes in your cluster\.

   ```
   kubectl get nodes
   ```

   Output

   ```
   NAME                                           STATUS     ROLES    AGE   VERSION
   ip-192-168-22-103.us-west-2.compute.internal   Ready      <none>   19m   v1.20.4-eks-6b7464
   ip-192-168-97-94.us-west-2.compute.internal    Ready      <none>   19m   v1.20.4-eks-6b7464
   ```

1. Describe one of the nodes to determine the max pods for the node\.

   ```
   kubectl describe node node-name ip-192-168-22-103.us-west-2.compute.internal
   ```

   Output

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