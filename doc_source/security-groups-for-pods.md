# Security groups for pods<a name="security-groups-for-pods"></a>

Security groups for pods integrate Amazon EC2 security groups with Kubernetes pods\. You can use Amazon EC2 security groups to define rules that allow inbound and outbound network traffic to and from pods that you deploy to nodes running on many Amazon EC2 instance types\. For a detailed explanation of this capability, see the [Introducing security groups for pods](http://aws.amazon.com/blogs/containers/introducing-security-groups-for-pods/) blog post\.

## Considerations<a name="security-groups-pods-considerations"></a>

Before deploying security groups for pods, consider the following limits and conditions:
+ Your Amazon EKS cluster must be running Kubernetes version 1\.17 and Amazon EKS platform version `eks.3` or later\. You can't use security groups for pods on Kubernetes clusters that you deployed to Amazon EC2\.
+ Traffic flow to and from pods with associated security groups are not subjected to [Calico network policy](calico.md) enforcement and are limited to Amazon EC2 security group enforcement only\. Community effort is underway to remove this limitation\. 
+ Security groups for pods can't be used with pods deployed to Fargate\.
+ Security groups for pods can't be used with Windows nodes\.
+ Security groups for pods are supported by most [Nitro\-based](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html#ec2-nitro-instances) Amazon EC2 instance families, including the `m5`, `c5`, `r5`, `p3`, `m6g`, `cg6`, and `r6g` instance families\. The `t3` instance family is not supported\. For a complete list of supported instances, see [Amazon EC2 supported instances and branch network interfaces](#supported-instance-types)\. Your nodes must be one of the supported instance types\.
+ Source NAT is disabled for outbound traffic from pods with assigned security groups so that outbound security group rules are applied\. To access the internet, pods with assigned security groups must be launched on nodes that are deployed in a private subnet configured with a NAT gateway or instance\. Pods with assigned security groups deployed to public subnets are not able to access the internet\.
+ Kubernetes services of type `NodePort` and `LoadBalancer` using instance targets with an `externalTrafficPolicy` set to `Local` are not supported with pods that you assign security groups to\. For more information about using a load balancer with instance targets, see [Load balancer – Instance targets](load-balancing.md#load-balancer-instance)\.
+ If you're also using pod security policies to restrict access to pod mutation, then the `eks-vpc-resource-controller` and `vpc-resource-controller` Kubernetes service accounts must be specified in the Kubernetes `ClusterRoleBinding` for the the `Role` that your `psp` is assigned to\. If you're using the [default Amazon EKS `psp`, `Role`, and `ClusterRoleBinding`](pod-security-policy.md#default-psp), this is the `eks:podsecuritypolicy:authenticated` `ClusterRoleBinding`\. For example, you would add the service accounts to the `subjects:` section, as shown in the following example:

  ```
  ...
  subjects:
    - kind: Group
      apiGroup: rbac.authorization.k8s.io
      name: system:authenticated
    - kind: ServiceAccount
      name: vpc-resource-controller
    - kind: ServiceAccount
      name: eks-vpc-resource-controller
  ```
+ If you're using [custom networking](cni-custom-network.md) and security groups for pods together, the security group specified by security groups for pods is used instead of the security group specified in the `ENIconfig`\.

## Deploy security groups for pods<a name="security-groups-pods-deployment"></a>

**To deploy security groups for pods**

1. Check your current CNI plug\-in version with the following command\.

   ```
   kubectl describe daemonset aws-node --namespace kube-system | grep Image | cut -d "/" -f 2
   ```

   The output is similar to the following output\.

   ```
   amazon-k8s-cni:<1.7.1>
   ```

   If your CNI plug\-in version is earlier than 1\.7\.1, then upgrade your CNI plug\-in to version 1\.7\.1 or later\. For more information, see [Amazon VPC CNI plugin for Kubernetes upgrades](cni-upgrades.md)\.

1. Add the `AmazonEKSVPCResourceController` managed policy to the [cluster role](service_IAM_role.md#create-service-role) that is associated with your Amazon EKS cluster\. The [policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSVPCResourceController$jsonEditor) allows the role to manage network interfaces, their private IP addresses, and their attachment and detachment to and from instances\. The following command adds the policy to a cluster role named `<eksClusterRole>`\.

   ```
   aws iam attach-role-policy \
       --policy-arn arn:aws:iam::aws:policy/AmazonEKSVPCResourceController \
       --role-name <eksClusterRole>
   ```

1. Enable the CNI plug\-in to manage network interfaces for pods by setting the `ENABLE_POD_ENI` variable to `true` in the `aws-node` DaemonSet\. Once this setting is set to `true`, for each node in the cluster the plug\-in adds a label with the value `vpc.amazonaws.com/has-trunk-attached=true`\. The VPC resource controller creates and attaches one special network interface called a *trunk network interface* with the description `aws-k8s-trunk-eni`\.

   ```
   kubectl set env daemonset aws-node -n kube-system ENABLE_POD_ENI=true
   ```
**Note**  
The trunk network interface is included in the maximum number of network interfaces supported by the instance type\. For a list of the maximum number of interfaces supported by each instance type, see [IP addresses per network interface per instance type](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#AvailableIpPerENI) in the *Amazon EC2 User Guide for Linux Instances*\. If your node already has the maximum number of standard network interfaces attached to it then the VPC resource controller will reserve a space\. You will have to scale down your running pods enough for the controller to detach and delete a standard network interface, create the trunk network interface, and attach it to the instance\.

   You can see which of your nodes have `aws-k8s-trunk-eni` set to `true` with the following command\.

   ```
   kubectl get nodes -o wide -l vpc.amazonaws.com/has-trunk-attached=true
   ```

   Once the trunk network interface is created, pods can be assigned secondary IP addresses from the trunk or standard network interfaces\. The trunk interface is automatically deleted if the node is deleted\. 

   When you deploy a security group for a pod in a later step, the VPC resource controller creates a special network interface called a *branch network interface* with a description of `aws-k8s-branch-eni` and associates the security groups to it\. Branch network interfaces are created in addition to the standard and trunk network interfaces attached to the node\. If are you using liveness or readiness probes, you also need to disable TCP early demux, so that the `kubelet` can connect to pods on branch network interfaces via TCP\. To disable TCP early demux, run the following command:

   ```
   kubectl edit ds aws-node -n kube-system
   ```

   Under the `initContainers` section, change the value of `DISABLE_TCP_EARLY_DEMUX` from `false` to `true`, and save the file\.

1. Create a namespace to deploy resources to\.

   ```
   kubectl create namespace <my-namespace>
   ```

1. Deploy an Amazon EKS `SecurityGroupPolicy` to your cluster\.

   1. Save the following example security policy to a file named <my\-security\-group\-policy\.yaml>\. You can replace `podSelector` with `serviceAccountSelector` if you'd rather select pods based on service account labels\. You must specify one selector or the other\. An empty `podSelector` \(example: `podSelector: {}`\) selects all pods in the namespace\. An empty `serviceAccountSelector` selects all service accounts in the namespace\. You must specify 1\-5 security group IDs for `groupIds`\. If you specify more than one ID, then the combination of all the rules in all the security groups are effective for the selected pods\.

      ```
      apiVersion: vpcresources.k8s.aws/v1beta1
      kind: SecurityGroupPolicy
      metadata:
        name: <my-security-group-policy>
        namespace: <my-namespace>
      spec:
        <podSelector>: 
          matchLabels:
            <role>: <my-role>
        securityGroups:
          groupIds:
            - <sg-abc123>
      ```
**Important**  
The security groups that you specify in the policy must exist\. If they don't exist, then, when you deploy a pod that matches the selector, your pod remains stuck in the creation process\. If you describe the pod, you'll see an error message similar to the following one: `An error occurred (InvalidSecurityGroupID.NotFound) when calling the CreateNetworkInterface operation: The securityGroup ID '<sg-abc123>' does not exist`\.
The security group must allow inbound communication from the cluster security group \(for `kubelet`\) over any ports you've configured probes for\.
The security group must allow outbound communication to the cluster security group \(for CoreDNS\) over TCP and UDP port 53\. The cluster security group must also allow inbound TCP and UDP port 53 communication from all security groups associated to pods\.

   1. Deploy the policy\.

      ```
      kubectl apply -f <my-security-group-policy.yaml>
      ```

1. Deploy a sample application with a label that matches the `<my-role>` value for `<podSelector>` that you specified in the previous step\.

   1. Save the following contents to a file\.

      ```
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: <my-deployment>
        namespace: <my-namespace>
        labels:
          app: <my-app>
      spec:
        replicas: <1>
        selector:
          matchLabels:
            app: <my-app>
        template:
          metadata:
            labels:
              app: <my-app>
              role: <my-role>
          spec:
            containers:
            - name: <my-container>
              image: <my-image>
              ports:
              - containerPort: <80>
      ```

   1. Deploy the application with the following command\. When you deploy the application, the CNI plug\-in matches the `role` label and the security groups that you specified in the previous step are applied to the pod\.

      ```
      kubectl apply -f <file-name-you-used-in-previous-step.yaml>
      ```
**Note**  
If your pod is stuck in the `Waiting` state and you see `Insufficient permissions: Unable to create Elastic Network Interface.` when you describe the pod, confirm that you added the IAM policy to the IAM cluster role in a previous step\.
If your pod is stuck in the `Pending` state, confirm that your node instance type is listed in [Amazon EC2 supported instances and branch network interfaces](#supported-instance-types) and that that the maximum number of branch network interfaces supported by the instance type multiplied times the number of nodes in your node group hasn't already been met\. For example, an `m5.large` instance supports nine branch network interfaces\. If your node group has five nodes, then a maximum of 45 branch network interfaces can be created for the node group\. The 46th pod that you attempt to deploy will sit in `Pending` state until another pod that has associated security groups is deleted\.

      If you run `kubectl describe pod <my-deployment-xxxxxxxxxx-xxxxx> -n <my-namespace>` and see a message similar to the following message, then it can be safely ignored\. This message might appear when the CNI plug\-in tries to set up host networking and fails while the network interface is being created\. The CNI plug\-in logs this event until the network interface is created\.

      ```
      Failed to create pod sandbox: rpc error: code = Unknown desc = failed to set up sandbox container "<e24268322e55c8185721f52df6493684f6c2c3bf4fd59c9c121fd4cdc894579f>" network for pod "<my-deployment-59f5f68b58-c89wx>": networkPlugin
      cni failed to set up pod "<my-deployment-59f5f68b58-c89wx_my-namespace>" network: add cmd: failed to assign an IP address to container
      ```

      You cannot exceed the maximum number of pods that can be run on the instance type\. For a list of the maximum number of pods that you can run on each instance type, see [eni\-max\-pods\.txt](https://github.com/awslabs/amazon-eks-ami/blob/master/files/eni-max-pods.txt) on GitHub\. When you delete a pod that has associated security groups, or delete the node that the pod is running on, the VPC resource controller deletes the branch network interface\. If you delete a cluster with pods using pods for security groups, then the controller does not delete the branch network interfaces, so you'll need to delete them yourself\.

## Amazon EC2 supported instances and branch network interfaces<a name="supported-instance-types"></a>

The following table lists the number of branch network interfaces that you can use with each supported Amazon EC2 instance type\.


| Instance type | Branch network interfaces | 
| --- | --- | 
| a1\.medium | 10 | 
| a1\.large | 9 | 
| a1\.xlarge | 18 | 
| a1\.2xlarge | 38 | 
| a1\.4xlarge | 54 | 
| a1\.metal | 54 | 
| c5\.large | 9 | 
| c5\.xlarge | 18 | 
| c5\.2xlarge | 38 | 
| c5\.4xlarge | 54 | 
| c5\.9xlarge | 54 | 
| c5\.12xlarge | 54 | 
| c5\.18xlarge | 107 | 
| c5\.24xlarge | 107 | 
| c5\.metal | 107 | 
| c5a\.large | 9 | 
| c5a\.xlarge | 18 | 
| c5a\.2xlarge | 38 | 
| c5a\.4xlarge | 54 | 
| c5a\.8xlarge | 54 | 
| c5a\.12xlarge | 54 | 
| c5a\.16xlarge | 107 | 
| c5a\.24xlarge | 107 | 
| c5d\.large | 9 | 
| c5d\.xlarge | 18 | 
| c5d\.2xlarge | 38 | 
| c5d\.4xlarge | 54 | 
| c5d\.9xlarge | 54 | 
| c5d\.12xlarge | 54 | 
| c5d\.18xlarge | 107 | 
| c5d\.24xlarge | 107 | 
| c5d\.metal | 107 | 
| c5n\.large | 9 | 
| c5n\.xlarge | 18 | 
| c5n\.2xlarge | 38 | 
| c5n\.4xlarge | 54 | 
| c5n\.9xlarge | 54 | 
| c5n\.18xlarge | 107 | 
| c5n\.metal | 107 | 
| c6g\.medium | 4 | 
| c6g\.large | 9 | 
| c6g\.xlarge | 18 | 
| c6g\.2xlarge | 38 | 
| c6g\.4xlarge | 54 | 
| c6g\.8xlarge | 54 | 
| c6g\.12xlarge | 54 | 
| c6g\.16xlarge | 107 | 
| c6g\.metal | 107 | 
| g4dn\.xlarge | 39 | 
| g4dn\.2xlarge | 39 | 
| g4dn\.4xlarge | 59 | 
| g4dn\.8xlarge | 58 | 
| g4dn\.12xlarge | 54 | 
| g4dn\.16xlarge | 118 | 
| g4dn\.metal | 107 | 
| i3en\.large | 5 | 
| i3en\.xlarge | 12 | 
| i3en\.2xlarge | 28 | 
| i3en\.3xlarge | 38 | 
| i3en\.6xlarge | 54 | 
| i3en\.12xlarge | 114 | 
| i3en\.24xlarge | 107 | 
| i3en\.metal | 107 | 
| inf1\.xlarge | 38 | 
| inf1\.2xlarge | 38 | 
| inf1\.6xlarge | 54 | 
| inf1\.24xlarge | 107 | 
| m5\.large | 9 | 
| m5\.xlarge | 18 | 
| m5\.2xlarge | 38 | 
| m5\.4xlarge | 54 | 
| m5\.8xlarge | 54 | 
| m5\.12xlarge | 54 | 
| m5\.16xlarge | 107 | 
| m5\.24xlarge | 107 | 
| m5\.metal | 107 | 
| m5a\.large | 9 | 
| m5a\.xlarge | 18 | 
| m5a\.2xlarge | 38 | 
| m5a\.4xlarge | 54 | 
| m5a\.8xlarge | 54 | 
| m5a\.12xlarge | 54 | 
| m5a\.16xlarge | 107 | 
| m5a\.24xlarge | 107 | 
| m5ad\.large | 9 | 
| m5ad\.xlarge | 18 | 
| m5ad\.2xlarge | 38 | 
| m5ad\.4xlarge | 54 | 
| m5ad\.8xlarge | 54 | 
| m5ad\.12xlarge | 54 | 
| m5ad\.16xlarge | 107 | 
| m5ad\.24xlarge | 107 | 
| m5d\.large | 9 | 
| m5d\.xlarge | 18 | 
| m5d\.2xlarge | 38 | 
| m5d\.4xlarge | 54 | 
| m5d\.8xlarge | 54 | 
| m5d\.12xlarge | 54 | 
| m5d\.16xlarge | 107 | 
| m5d\.24xlarge | 107 | 
| m5d\.metal | 107 | 
| m5dn\.large | 9 | 
| m5dn\.xlarge | 18 | 
| m5dn\.2xlarge | 38 | 
| m5dn\.4xlarge | 54 | 
| m5dn\.8xlarge | 54 | 
| m5dn\.12xlarge | 54 | 
| m5dn\.16xlarge | 107 | 
| m5dn\.24xlarge | 107 | 
| m5n\.large | 9 | 
| m5n\.xlarge | 18 | 
| m5n\.2xlarge | 38 | 
| m5n\.4xlarge | 54 | 
| m5n\.8xlarge | 54 | 
| m5n\.12xlarge | 54 | 
| m5n\.16xlarge | 107 | 
| m5n\.24xlarge | 107 | 
| m6g\.medium | 4 | 
| m6g\.large | 9 | 
| m6g\.xlarge | 18 | 
| m6g\.2xlarge | 38 | 
| m6g\.4xlarge | 54 | 
| m6g\.8xlarge | 54 | 
| m6g\.12xlarge | 54 | 
| m6g\.16xlarge | 107 | 
| m6g\.metal | 107 | 
| p3\.2xlarge | 38 | 
| p3\.8xlarge | 54 | 
| p3\.16xlarge | 114 | 
| p3dn\.24xlarge | 107 | 
| r5\.large | 9 | 
| r5\.xlarge | 18 | 
| r5\.2xlarge | 38 | 
| r5\.4xlarge | 54 | 
| r5\.8xlarge | 54 | 
| r5\.12xlarge | 54 | 
| r5\.16xlarge | 107 | 
| r5\.24xlarge | 107 | 
| r5\.metal | 107 | 
| r5a\.large | 9 | 
| r5a\.xlarge | 18 | 
| r5a\.2xlarge | 38 | 
| r5a\.4xlarge | 54 | 
| r5a\.8xlarge | 54 | 
| r5a\.12xlarge | 54 | 
| r5a\.16xlarge | 107 | 
| r5a\.24xlarge | 107 | 
| r5ad\.large | 9 | 
| r5ad\.xlarge | 18 | 
| r5ad\.2xlarge | 38 | 
| r5ad\.4xlarge | 54 | 
| r5ad\.8xlarge | 54 | 
| r5ad\.12xlarge | 54 | 
| r5ad\.16xlarge | 107 | 
| r5ad\.24xlarge | 107 | 
| r5d\.large | 9 | 
| r5d\.xlarge | 18 | 
| r5d\.2xlarge | 38 | 
| r5d\.4xlarge | 54 | 
| r5d\.8xlarge | 54 | 
| r5d\.12xlarge | 54 | 
| r5d\.16xlarge | 107 | 
| r5d\.24xlarge | 107 | 
| r5d\.metal | 107 | 
| r5dn\.large | 9 | 
| r5dn\.xlarge | 18 | 
| r5dn\.2xlarge | 38 | 
| r5dn\.4xlarge | 54 | 
| r5dn\.8xlarge | 54 | 
| r5dn\.12xlarge | 54 | 
| r5dn\.16xlarge | 107 | 
| r5dn\.24xlarge | 107 | 
| r5n\.large | 9 | 
| r5n\.xlarge | 18 | 
| r5n\.2xlarge | 38 | 
| r5n\.4xlarge | 54 | 
| r5n\.8xlarge | 54 | 
| r5n\.12xlarge | 54 | 
| r5n\.16xlarge | 107 | 
| r5n\.24xlarge | 107 | 
| r6g\.medium | 4 | 
| r6g\.large | 9 | 
| r6g\.xlarge | 18 | 
| r6g\.2xlarge | 38 | 
| r6g\.4xlarge | 54 | 
| r6g\.8xlarge | 54 | 
| r6g\.12xlarge | 54 | 
| r6g\.16xlarge | 107 | 
| z1d\.large | 13 | 
| z1d\.xlarge | 28 | 
| z1d\.2xlarge | 58 | 
| z1d\.3xlarge | 54 | 
| z1d\.6xlarge | 54 | 
| z1d\.12xlarge | 107 | 
| z1d\.metal | 107 | 