# Security groups for Pods<a name="security-groups-for-pods"></a>

Security groups for Pods integrate Amazon EC2 security groups with Kubernetes Pods\. You can use Amazon EC2 security groups to define rules that allow inbound and outbound network traffic to and from Pods that you deploy to nodes running on many Amazon EC2 instance types and Fargate\. For a detailed explanation of this capability, see the [Introducing security groups for Pods](https://aws.amazon.com/blogs/containers/introducing-security-groups-for-pods/) blog post\.

## Considerations<a name="sg-pods-considerations"></a>
+ Before deploying security groups for Pods, consider the following limitations and conditions:
+ Security groups for Pods can't be used with Windows nodes\.
+ Security groups for Pods can be used with clusters configured for the `IPv6` family that contain Amazon EC2 nodes by using version 1\.16\.0 or later of the Amazon VPC CNI plugin\. You can use security groups for Pods with clusters configure `IPv6` family that contain only Fargate nodes by using version 1\.7\.7 or later of the Amazon VPC CNI plugin\. For more information, see [`IPv6` addresses for clusters, Pods, and services](cni-ipv6.md)
+ Security groups for Pods are supported by most [Nitro\-based](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html#ec2-nitro-instances) Amazon EC2 instance families, though not by all generations of a family\. For example, the `m5`, `c5`, `r5`, `p3`, `m6g`, `c6g`, and `r6g` instance family and generations are supported\. No instance types in the `t` family are supported\. For a complete list of supported instance types, see the [limits\.go](https://github.com/aws/amazon-vpc-resource-controller-k8s/blob/release-1.1.4/pkg/aws/vpc/limits.go) file on Github\. Your nodes must be one of the listed instance types that have `IsTrunkingCompatible: true` in that file\.
+ If you're also using Pod security policies to restrict access to Pod mutation, then the `eks:vpc-resource-controller` Kubernetes user must be specified in the Kubernetes `ClusterRoleBinding` for the `role` that your `psp` is assigned to\. If you're using the default Amazon EKS `psp`, `role`, and `ClusterRoleBinding`, this is the `eks:podsecuritypolicy:authenticated` `ClusterRoleBinding`\. For example, you add the user to the `subjects:` section, as shown in the following example:

  ```
  [...]
  subjects:
    - kind: Group
      apiGroup: rbac.authorization.k8s.io
      name: system:authenticated
    - apiGroup: rbac.authorization.k8s.io
      kind: User
      name: eks:vpc-resource-controller
    - kind: ServiceAccount
      name: eks-vpc-resource-controller
  ```
+ If you're using custom networking and security groups for Pods together, the security group specified by security groups for Pods is used instead of the security group specified in the `ENIConfig`\.
+ If you're using version `1.10.2` or earlier of the Amazon VPC CNI plugin and you include the `terminationGracePeriodSeconds` setting in your Pod spec, the value for the setting can't be zero\.  
+ If you're using version `1.10` or earlier of the Amazon VPC CNI plugin, or version `1.11` with `POD_SECURITY_GROUP_ENFORCING_MODE`=`strict`, which is the default setting, then Kubernetes services of type `NodePort` and `LoadBalancer` using instance targets with an `externalTrafficPolicy` set to `Local` aren't supported with Pods that you assign security groups to\. For more information about using a load balancer with instance targets, see [Network load balancing on Amazon EKS](network-load-balancing.md)
+ If you're using version `1.10` or earlier of the Amazon VPC CNI plugin or version `1.11` with `POD_SECURITY_GROUP_ENFORCING_MODE`=`strict`, which is the default setting, source NAT is disabled for outbound traffic from Pods with assigned security groups so that outbound security group rules are applied\. To access the internet, Pods with assigned security groups must be launched on nodes that are deployed in a private subnet configured with a NAT gateway or instance\. Pods with assigned security groups deployed to public subnets are not able to access the internet\.

  If you're using version `1.11` or later of the plugin with `POD_SECURITY_GROUP_ENFORCING_MODE`=`standard`, then Pod traffic destined for outside of the VPC is translated to the IP address of the instance's primary network interface\. For this traffic, the rules in the security groups for the primary network interface are used, rather than the rules in the Pod's security groups\. 
+ To use Calico network policy with Pods that have associated security groups, you must use version `1.11.0` or later of the Amazon VPC CNI plugin and set `POD_SECURITY_GROUP_ENFORCING_MODE`=`standard`\. Otherwise, traffic flow to and from Pods with associated security groups are not subjected to Calico network policy enforcement and are limited to Amazon EC2 security group enforcement only\. To update your Amazon VPC CNI version, see [Working with the Amazon VPC CNI plugin for Kubernetes Amazon EKS add\-on](managing-vpc-cni.md)
+ Pods running on Amazon EC2 nodes that use security groups in clusters that use [Nodelocal DNSCache](https://kubernetes.io/docs/tasks/administer-cluster/nodelocaldns/) are only supported with version `1.11.0` or later of the Amazon VPC CNI plugin and with `POD_SECURITY_GROUP_ENFORCING_MODE`=`standard`\. To update your Amazon VPC CNI plugin version, see [Working with the Amazon VPC CNI plugin for Kubernetes Amazon EKS add\-on](managing-vpc-cni.md)
+ Security groups for Pods might lead to higher Pod startup latency for Pods with high churn\. This is due to rate limiting in the resource controller\.

## Configure the Amazon VPC CNI plugin for Kubernetes for security groups for Pods<a name="security-groups-pods-deployment"></a>

**To deploy security groups for Pods**

If you're using security groups for Fargate Pods only, and don't have any Amazon EC2 nodes in your cluster, skip to [Deploy an example application](#sg-pods-example-deployment)\.

1. Check your current Amazon VPC CNI plugin for Kubernetes version with the following command:

   ```
   kubectl describe daemonset aws-node --namespace kube-system | grep amazon-k8s-cni: | cut -d : -f 3
   ```

   An example output is as follows\.

   ```
   v1.7.6
   ```

   If your Amazon VPC CNI plugin for Kubernetes version is earlier than `1.7.7`, then update the plugin to version `1.7.7` or later\. For more information, see [Working with the Amazon VPC CNI plugin for Kubernetes Amazon EKS add\-on](managing-vpc-cni.md)

1. Add the [https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSVPCResourceController](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSVPCResourceController) managed IAM policy to the [cluster role](service_IAM_role.md#create-service-role) that is associated with your Amazon EKS cluster\. The policy allows the role to manage network interfaces, their private IP addresses, and their attachment and detachment to and from network instances\.

   1. Retrieve the name of your cluster IAM role and store it in a variable\. Replace `my-cluster` with the name of your cluster\.

      ```
      cluster_role=$(aws eks describe-cluster --name my-cluster --query cluster.roleArn --output text | cut -d / -f 2)
      ```

   1. Attach the policy to the role\.

      ```
      aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonEKSVPCResourceController --role-name $cluster_role
      ```

1. Enable the Amazon VPC CNI add\-on to manage network interfaces for Pods by setting the `ENABLE_POD_ENI` variable to `true` in the `aws-node` DaemonSet\. Once this setting is set to `true`, for each node in the cluster the add\-on creates a cninode custom resource\. The VPC resource controller creates and attaches one special network interface called a *trunk network interface* with the description `aws-k8s-trunk-eni`\.

   ```
   kubectl set env daemonset aws-node -n kube-system ENABLE_POD_ENI=true
   ```
**Note**  
The trunk network interface is included in the maximum number of network interfaces supported by the instance type\. For a list of the maximum number of network interfaces supported by each instance type, see [IP addresses per network interface per instance type](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#AvailableIpPerENI) in the *Amazon EC2 User Guide for Linux Instances*\. If your node already has the maximum number of standard network interfaces attached to it then the VPC resource controller will reserve a space\. You will have to scale down your running Pods enough for the controller to detach and delete a standard network interface, create the trunk network interface, and attach it to the instance\.

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

   If you are using liveness or readiness probes, then you also need to disable TCP early demux, so that the `kubelet` can connect to Pods on branch network interfaces using TCP\. To disable TCP early demux, run the following command:

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

## Deploy an example application<a name="sg-pods-example-deployment"></a>

To use security groups for Pods, you must have an existing security group and [Deploy an Amazon EKS `SecurityGroupPolicy`](#deploy-securitygrouppolicy) to your cluster, as described in the following procedure\. The following steps show you how to use the security group policy for a Pod\. Unless otherwise noted, complete all steps from the same terminal because variables are used in the following steps that don't persist across terminals\.

**To deploy an example Pod with a security group**

1. Create a Kubernetes namespace to deploy resources to\. You can replace *my\-namespace* with the name of a namespace that you want to use\.

   ```
   kubectl create namespace my-namespace
   ```

1. Deploy an Amazon EKS `SecurityGroupPolicy` to your cluster\.

   1. Copy the following contents to your device\. You can replace *podSelector* with **serviceAccountSelector** if you'd rather select Pods based on service account labels\. You must specify one selector or the other\. An empty `podSelector` \(example: `podSelector: {}`\) selects all Pods in the namespace\. You can change *my\-role* to the name of your role\. An empty `serviceAccountSelector` selects all service accounts in the namespace\. You can replace *my\-security\-group\-policy* with a name for your `SecurityGroupPolicy` and *my\-namespace* with the namespace that you want to create the `SecurityGroupPolicy` in\. 

      You must replace *my\_pod\_security\_group\_id* with the ID of an existing security group\. If you don't have an existing security group, then you must create one\. For more information, see [Amazon EC2 security groups for Linux instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html) in the [Amazon EC2 User Guide for Linux Instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/)\. You can specify 1\-5 security group IDs\. If you specify more than one ID, then the combination of all the rules in all the security groups are effective for the selected Pods\.

      ```
      cat >my-security-group-policy.yaml <<EOF
      apiVersion: vpcresources.k8s.aws/v1beta1
      kind: SecurityGroupPolicy
      metadata:
        name: my-security-group-policy
        namespace: my-namespace
      spec:
        podSelector: 
          matchLabels:
            role: my-role
        securityGroups:
          groupIds:
            - my_pod_security_group_id
      EOF
      ```
**Important**  
The security group or groups that you specify for your Pods must meet the following criteria:  
They must exist\. If they don't exist, then, when you deploy a Pod that matches the selector, your Pod remains stuck in the creation process\. If you describe the Pod, you'll see an error message similar to the following one: `An error occurred (InvalidSecurityGroupID.NotFound) when calling the CreateNetworkInterface operation: The securityGroup ID 'sg-05b1d815d1EXAMPLE' does not exist`\.
They must allow inbound communication from the security group applied to your nodes \(for `kubelet`\) over any ports that you've configured probes for\.
They must allow outbound communication over `TCP` and `UDP` ports 53 to a security group assigned to the Pods \(or nodes that the Pods run on\) running CoreDNS\. The security group for your CoreDNS Pods must allow inbound `TCP` and `UDP` port 53 traffic from the security group that you specify\.
They must have necessary inbound and outbound rules to communicate with other Pods that they need to communicate with\.
They must have rules that allow the Pods to communicate with the Kubernetes control plane if you're using the security group with Fargate\. The easiest way to do this is to specify the cluster security group as one of the security groups\.
Security group policies only apply to newly scheduled Pods\. They do not affect running Pods\.

   1. Deploy the policy\.

      ```
      kubectl apply -f my-security-group-policy.yaml
      ```

1. Deploy a sample application with a label that matches the `my-role` value for `podSelector` that you specified in a previous step\.

   1. Copy the following contents to your device\. Replace the *example values* with your own and then run the modified command\. If you replace *my\-role*, make sure that it's the same as the value you specified for the selector in a previous step\.

      ```
      cat >sample-application.yaml <<EOF
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: my-deployment
        namespace: my-namespace
        labels:
          app: my-app
      spec:
        replicas: 4
        selector:
          matchLabels:
            app: my-app
        template:
          metadata:
            labels:
              app: my-app
              role: my-role
          spec:
            terminationGracePeriodSeconds: 120
            containers:
            - name: nginx
              image: public.ecr.aws/nginx/nginx:1.23
              ports:
              - containerPort: 80
      ---
      apiVersion: v1
      kind: Service
      metadata:
        name: my-app
        namespace: my-namespace
        labels:
          app: my-app
      spec:
        selector:
          app: my-app
        ports:
          - protocol: TCP
            port: 80
            targetPort: 80
      EOF
      ```

   1. Deploy the application with the following command\. When you deploy the application, the Amazon VPC CNI plugin for Kubernetes matches the `role` label and the security groups that you specified in the previous step are applied to the Pod\.

      ```
      kubectl apply -f sample-application.yaml
      ```

1. View the Pods deployed with the sample application\. For the remainder of this topic, this terminal is referred to as `TerminalA`\.

   ```
   kubectl get pods -n my-namespace -o wide
   ```

   An example output is as follows\.

   ```
   NAME                             READY   STATUS    RESTARTS   AGE     IP               NODE                                            NOMINATED NODE   READINESS GATES
   my-deployment-5df6f7687b-4fbjm   1/1     Running   0          7m51s   192.168.53.48    ip-192-168-33-28.region-code.compute.internal   <none>           <none>
   my-deployment-5df6f7687b-j9fl4   1/1     Running   0          7m51s   192.168.70.145   ip-192-168-92-33.region-code.compute.internal   <none>           <none>
   my-deployment-5df6f7687b-rjxcz   1/1     Running   0          7m51s   192.168.73.207   ip-192-168-92-33.region-code.compute.internal   <none>           <none>
   my-deployment-5df6f7687b-zmb42   1/1     Running   0          7m51s   192.168.63.27    ip-192-168-33-28.region-code.compute.internal   <none>           <none>
   ```
**Note**  
If any Pods are stuck in the `Waiting` state, then run `kubectl describe pod my-deployment-xxxxxxxxxx-xxxxx -n my-namespace`\. If you see `Insufficient permissions: Unable to create Elastic Network Interface.`, confirm that you added the IAM policy to the IAM cluster role in a previous step\.
If any Pods are stuck in the `Pending` state, confirm that your node instance type is listed in [https://github.com/aws/amazon-vpc-resource-controller-k8s/blob/master/pkg/aws/vpc/limits.go](https://github.com/aws/amazon-vpc-resource-controller-k8s/blob/master/pkg/aws/vpc/limits.go) and that the product of the maximum number of branch network interfaces supported by the instance type multiplied times the number of nodes in your node group hasn't already been met\. For example, an `m5.large` instance supports nine branch network interfaces\. If your node group has five nodes, then a maximum of 45 branch network interfaces can be created for the node group\. The 46th Pod that you attempt to deploy will sit in `Pending` state until another Pod that has associated security groups is deleted\.

   If you run `kubectl describe pod my-deployment-xxxxxxxxxx-xxxxx -n my-namespace` and see a message similar to the following message, then it can be safely ignored\. This message might appear when the Amazon VPC CNI plugin for Kubernetes tries to set up host networking and fails while the network interface is being created\. The plugin logs this event until the network interface is created\.

   ```
   Failed to create Pod sandbox: rpc error: code = Unknown desc = failed to set up sandbox container "e24268322e55c8185721f52df6493684f6c2c3bf4fd59c9c121fd4cdc894579f" network for Pod "my-deployment-5df6f7687b-4fbjm": networkPlugin
   cni failed to set up Pod "my-deployment-5df6f7687b-4fbjm-c89wx_my-namespace" network: add cmd: failed to assign an IP address to container
   ```

   You can't exceed the maximum number of Pods that can be run on the instance type\. For a list of the maximum number of Pods that you can run on each instance type, see [eni\-max\-pods\.txt](https://github.com/awslabs/amazon-eks-ami/blob/master/files/eni-max-pods.txt) on GitHub\. When you delete a Pod that has associated security groups, or delete the node that the Pod is running on, the VPC resource controller deletes the branch network interface\. If you delete a cluster with Pods using Pods for security groups, then the controller doesn't delete the branch network interfaces, so you'll need to delete them yourself\. For information about how to delete network interfaces, see [Delete a network interface](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#delete_eni) in the Amazon EC2 User Guide for Linux Instances\.

1. In a separate terminal, shell into one of the Pods\. For the remainder of this topic, this terminal is referred to as `TerminalB`\. Replace **5df6f7687b*\-*4fbjm** with the ID of one of the Pods returned in your output from the previous step\.

   ```
   kubectl exec -it -n my-namespace my-deployment-5df6f7687b-4fbjm -- /bin/bash
   ```

1. From the shell in `TerminalB`, confirm that the sample application works\.

   ```
   curl my-app
   ```

   An example output is as follows\.

   ```
   <!DOCTYPE html>
   <html>
   <head>
   <title>Welcome to nginx!</title>
   [...]
   ```

   You received the output because all Pods running the application are associated with the security group that you created\. That group contains a rule that allows all traffic between all Pods that the security group is associated to\. DNS traffic is allowed outbound from that security group to the cluster security group, which is associated with your nodes\. The nodes are running the CoreDNS Pods, which your Pods did a name lookup to\.

1. From `TerminalA`, remove the security group rules that allow DNS communication to the cluster security group from your security group\. If you didn't add the DNS rules to the cluster security group in a previous step, then replace `$my_cluster_security_group_id` with the ID of the security group that you created the rules in\.

   ```
   aws ec2 revoke-security-group-ingress --group-id $my_cluster_security_group_id --security-group-rule-ids $my_tcp_rule_id
   aws ec2 revoke-security-group-ingress --group-id $my_cluster_security_group_id --security-group-rule-ids $my_udp_rule_id
   ```

1. From `TerminalB`, attempt to access the application again\.

   ```
   curl my-app
   ```

   An example output is as follows\.

   ```
   curl: (6) Could not resolve host: my-app
   ```

   The attempt fails because the Pod is no longer able to access the CoreDNS Pods, which have the cluster security group associated to them\. The cluster security group no longer has the security group rules that allow DNS communication from the security group associated to your Pod\.

   If you attempt to access the application using the IP addresses returned for one of the Pods in a previous step, you still receive a response because all ports are allowed between Pods that have the security group associated to them and a name lookup isn't required\.

1. Once you've finished experimenting, you can remove the sample security group policy, application, and security group that you created\. Run the following commands from `TerminalA`\.

   ```
   kubectl delete namespace my-namespace
   aws ec2 revoke-security-group-ingress --group-id $my_pod_security_group_id --security-group-rule-ids $my_inbound_self_rule_id
   wait
   sleep 45s 
   aws ec2 delete-security-group --group-id $my_pod_security_group_id
   ```