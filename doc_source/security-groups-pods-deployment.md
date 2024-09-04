# Configure the Amazon VPC CNI plugin for Kubernetes for security groups for Amazon EKS Pods<a name="security-groups-pods-deployment"></a>

If you use Pods with Amazon EC2 instances, you need to configure the Amazon VPC CNI plugin for Kubernetes for security groups

If you use Fargate Pods only, and don't have any Amazon EC2 nodes in your cluster, see [Use a security group policy for an Amazon EKS Pod](sg-pods-example-deployment.md)\.

1. Check your current Amazon VPC CNI plugin for Kubernetes version with the following command:

   ```
   kubectl describe daemonset aws-node --namespace kube-system | grep amazon-k8s-cni: | cut -d : -f 3
   ```

   An example output is as follows\.

   ```
   v1.7.6
   ```

   If your Amazon VPC CNI plugin for Kubernetes version is earlier than `1.7.7`, then update the plugin to version `1.7.7` or later\. For more information, see [Assign IPs to Pods with the Amazon VPC CNI](managing-vpc-cni.md)

1. Add the [https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSVPCResourceController](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSVPCResourceController) managed IAM policy to the [cluster role](cluster-iam-role.md#create-service-role) that is associated with your Amazon EKS cluster\. The policy allows the role to manage network interfaces, their private IP addresses, and their attachment and detachment to and from network instances\.

   1. Retrieve the name of your cluster IAM role and store it in a variable\. Replace `my-cluster` with the name of your cluster\.

      ```
      cluster_role=$(aws eks describe-cluster --name my-cluster --query cluster.roleArn --output text | cut -d / -f 2)
      ```

   1. Attach the policy to the role\.

      ```
      aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonEKSVPCResourceController --role-name $cluster_role
      ```

1. Enable the Amazon VPC CNI add\-on to manage network interfaces for Pods by setting the `ENABLE_POD_ENI` variable to `true` in the `aws-node` DaemonSet\. Once this setting is set to `true`, for each node in the cluster the add\-on creates a `cninode` custom resource\. The VPC resource controller creates and attaches one special network interface called a *trunk network interface* with the description `aws-k8s-trunk-eni`\.

   ```
   kubectl set env daemonset aws-node -n kube-system ENABLE_POD_ENI=true
   ```
**Note**  
The trunk network interface is included in the maximum number of network interfaces supported by the instance type\. For a list of the maximum number of network interfaces supported by each instance type, see [IP addresses per network interface per instance type](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#AvailableIpPerENI) in the *Amazon EC2 User Guide*\. If your node already has the maximum number of standard network interfaces attached to it then the VPC resource controller will reserve a space\. You will have to scale down your running Pods enough for the controller to detach and delete a standard network interface, create the trunk network interface, and attach it to the instance\.

1. You can see which of your nodes have a `CNINode` custom resource with the following command\. If `No resources found` is returned, then wait several seconds and try again\. The previous step requires restarting the Amazon VPC CNI plugin for Kubernetes Pods, which takes several seconds\.

   ```
   $ kubectl get cninode -A
        NAME FEATURES
        ip-192-168-64-141.us-west-2.compute.internal [{"name":"SecurityGroupsForPods"}]
        ip-192-168-7-203.us-west-2.compute.internal [{"name":"SecurityGroupsForPods"}]
   ```

   If you are using VPC CNI versions older than `1.15`, node labels were used instead of the `CNINode` custom resource\. You can see which of your nodes have the node label`aws-k8s-trunk-eni` set to `true` with the following command\. If `No resources found` is returned, then wait several seconds and try again\. The previous step requires restarting the Amazon VPC CNI plugin for Kubernetes Pods, which takes several seconds\.

   ```
   kubectl get nodes -o wide -l vpc.amazonaws.com/has-trunk-attached=true
   -
   ```

   Once the trunk network interface is created, Pods are assigned secondary IP addresses from the trunk or standard network interfaces\. The trunk interface is automatically deleted if the node is deleted\.

   When you deploy a security group for a Pod in a later step, the VPC resource controller creates a special network interface called a *branch network interface* with a description of `aws-k8s-branch-eni` and associates the security groups to it\. Branch network interfaces are created in addition to the standard and trunk network interfaces attached to the node\.

   If you are using liveness or readiness probes, then you also need to disable *TCP early demux*, so that the `kubelet` can connect to Pods on branch network interfaces using TCP\. To disable *TCP early demux*, run the following command:

   ```
   kubectl patch daemonset aws-node -n kube-system \
     -p '{"spec": {"template": {"spec": {"initContainers": [{"env":[{"name":"DISABLE_TCP_EARLY_DEMUX","value":"true"}],"name":"aws-vpc-cni-init"}]}}}}'
   ```
**Note**  
If you're using `1.11.0` or later of the Amazon VPC CNI plugin for Kubernetes add\-on and set `POD_SECURITY_GROUP_ENFORCING_MODE`=`standard`, as described in the next step, then you don't need to run the previous command\.

1. If your cluster uses `NodeLocal DNSCache`, or you want to use Calico network policy with your Pods that have their own security groups, or you have Kubernetes services of type `NodePort` and `LoadBalancer` using instance targets with an `externalTrafficPolicy` set to `Local` for Pods that you want to assign security groups to, then you must be using version `1.11.0` or later of the Amazon VPC CNI plugin for Kubernetes add\-on, and you must enable the following setting:

   ```
   kubectl set env daemonset aws-node -n kube-system POD_SECURITY_GROUP_ENFORCING_MODE=standard
   ```
**Important**  
Pod security group rules aren't applied to traffic between Pods or between Pods and services, such as `kubelet` or `nodeLocalDNS`, that are on the same node\. Pods using different security groups on the same node can't communicate because they are configured in different subnets, and routing is disabled between these subnets\.
Outbound traffic from Pods to addresses outside of the VPC is network address translated to the IP address of the instance's primary network interface \(unless you've also set `AWS_VPC_K8S_CNI_EXTERNALSNAT=true`\)\. For this traffic, the rules in the security groups for the primary network interface are used, rather than the rules in the Pod's security groups\.
For this setting to apply to existing Pods, you must restart the Pods or the nodes that the Pods are running on\.

1. To see how to use a security group policy for your Pod, see [Use a security group policy for an Amazon EKS Pod](sg-pods-example-deployment.md)\.