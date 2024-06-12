# Amazon EKS troubleshooting<a name="troubleshooting"></a>

This chapter covers some common errors that you may see while using Amazon EKS and how to work around them\. If you need to troubleshoot specific Amazon EKS areas, see the separate [Troubleshooting IAM](security_iam_troubleshoot.md), [Troubleshooting issues in Amazon EKS Connector](troubleshooting-connector.md), and [Troubleshooting for ADOT using EKS Add\-Ons](https://aws-otel.github.io/docs/getting-started/adot-eks-add-on/troubleshooting) topics\.

For other troubleshooting information, see [Knowledge Center content about Amazon Elastic Kubernetes Service](https://repost.aws/tags/knowledge-center/TA4IvCeWI1TE66q4jEj4Z9zg/amazon-elastic-kubernetes-service) on *AWS re:Post*\.

## Insufficient capacity<a name="ICE"></a>

If you receive the following error while attempting to create an Amazon EKS cluster, then one of the Availability Zones you specified doesn't have sufficient capacity to support a cluster\.

`Cannot create cluster 'example-cluster' because region-1d, the targeted Availability Zone, does not currently have sufficient capacity to support the cluster. Retry and choose from these Availability Zones: region-1a, region-1b, region-1c`

Retry creating your cluster with subnets in your cluster VPC that are hosted in the Availability Zones returned by this error message\.

There are Availability Zones that a cluster can't reside in\. Compare the Availability Zones that your subnets are in with the list of Availability Zones in the [Subnet requirements and considerations](network_reqs.md#network-requirements-subnets)\.

## Nodes fail to join cluster<a name="worker-node-fail"></a>

There are a few common reasons that prevent nodes from joining the cluster:
+ If the nodes are managed nodes, Amazon EKS adds entries to the `aws-auth` `ConfigMap` when you create the node group\. If the entry was removed or modified, then you need to re\-add it\. For more information, enter **eksctl create iamidentitymapping \-\-help** in your terminal\. You can view your current `aws-auth` `ConfigMap` entries by replacing *my\-cluster* in the following command with the name of your cluster and then running the modified command: **eksctl get iamidentitymapping \-\-cluster *my\-cluster***\. The ARN of the role that you specify can't include a [path](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-friendly-names) other than `/`\. For example, if the name of your role is `development/apps/my-role`, you'd need to change it to `my-role` when specifying the ARN for the role\. Make sure that you specify the node IAM role ARN \(not the instance profile ARN\)\.

  If the nodes are self\-managed, and you haven't created [access entries](access-entries.md) for the ARN of the node's IAM role, then run the same commands listed for managed nodes\. If you have created an access entry for the ARN for your node IAM role, then it might not be configured properly in the access entry\. Make sure that the node IAM role ARN \(not the instance profile ARN\) is specified as the principal ARN in your `aws-auth` `ConfigMap` entry or access entry\. For more information about access entries, see [Manage access entries](access-entries.md)\.
+ The **ClusterName** in your node AWS CloudFormation template doesn't exactly match the name of the cluster you want your nodes to join\. Passing an incorrect value to this field results in an incorrect configuration of the node's `/var/lib/kubelet/kubeconfig` file, and the nodes will not join the cluster\.
+ The node is not tagged as being *owned* by the cluster\. Your nodes must have the following tag applied to them, where `my-cluster` is replaced with the name of your cluster\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/troubleshooting.html)
+ The nodes may not be able to access the cluster using a public IP address\. Ensure that nodes deployed in public subnets are assigned a public IP address\. If not, you can associate an Elastic IP address to a node after it's launched\. For more information, see [Associating an Elastic IP address with a running instance or network interface](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html#using-instance-addressing-eips-associating)\. If the public subnet is not set to automatically assign public IP addresses to instances deployed to it, then we recommend enabling that setting\. For more information, see [Modifying the public `IPv4` addressing attribute for your subnet](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#subnet-public-ip)\. If the node is deployed to a private subnet, then the subnet must have a route to a NAT gateway that has a public IP address assigned to it\.
+ The AWS STS endpoint for the AWS Region that you're deploying the nodes to is not enabled for your account\. To enable the region, see [Activating and deactivating AWS STS in an AWS Region](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_enable-regions.html#sts-regions-activate-deactivate)\.
+ The node doesn't have a private DNS entry, resulting in the `kubelet` log containing a `node "" not found` error\. Ensure that the VPC where the node is created has values set for `domain-name` and `domain-name-servers` as `Options` in a `DHCP options set`\. The default values are `domain-name:<region>.compute.internal` and `domain-name-servers:AmazonProvidedDNS`\. For more information, see [DHCP options sets](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_DHCP_Options.html#AmazonDNS) in the *Amazon VPC User Guide*\.
+ If the nodes in the managed node group do not connect to the cluster within 15 minutes, a health issue of “NodeCreationFailure” will be emitted and the console status will be set to `Create failed`\. For Windows AMIs that have slow launch times, this issue can be resolved using [fast launch](https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/win-ami-config-fast-launch.html)\.

To identify and troubleshoot common causes that prevent worker nodes from joining a cluster, you can use the `AWSSupport-TroubleshootEKSWorkerNode` runbook\. For more information, see `[AWSSupport\-TroubleshootEKSWorkerNode](https://docs.aws.amazon.com/systems-manager-automation-runbooks/latest/userguide/automation-awssupport-troubleshooteksworkernode.html)` in the *AWS Systems Manager Automation runbook reference*\.

## Unauthorized or access denied \(`kubectl`\)<a name="unauthorized"></a>

If you receive one of the following errors while running `kubectl` commands, then you don't have `kubectl` configured properly for Amazon EKS or the credentials for the IAM principal \(role or user\) that you're using don't map to a Kubernetes username that has sufficient permissions to Kubernetes objects on your Amazon EKS cluster\.
+ `could not get token: AccessDenied: Access denied`
+ `error: You must be logged in to the server (Unauthorized)`
+ `error: the server doesn't have a resource type "svc"`

This could be due to one of the following reasons:
+ The cluster was created with credentials for one IAM principal and `kubectl` is configured to use credentials for a different IAM principal\. To resolve this, update your `kube config` file to use the credentials that created the cluster\. For more information, see [Creating or updating a `kubeconfig` file for an Amazon EKS cluster](create-kubeconfig.md)\.
+ If your cluster meets the minimum platform requirements in the prerequisites section of [Manage access entries](access-entries.md), an access entry doesn't exist with your IAM principal\. If it exists, it doesn't have the necessary Kubernetes group names defined for it, or doesn't have the proper access policy associated to it\. For more information, see [Manage access entries](access-entries.md)\.
+ If your cluster doesn't meet the minimum platform requirements in [Manage access entries](access-entries.md), an entry with your IAM principal doesn't exist in the `aws-auth` `ConfigMap`\. If it exists, it's not mapped to Kubernetes group names that are bound to a Kubernetes `Role` or `ClusterRole` with the necessary permissions\. For more information about Kubernetes role\-based authorization \(RBAC\) objects, see [Using RBAC authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) in the Kubernetes documentation\. You can view your current `aws-auth` `ConfigMap` entries by replacing *my\-cluster* in the following command with the name of your cluster and then running the modified command: **eksctl get iamidentitymapping \-\-cluster *my\-cluster***\. If an entry for with the ARN of your IAM principal isn't in the `ConfigMap`, enter **eksctl create iamidentitymapping \-\-help** in your terminal to learn how to create one\. 

If you install and configure the AWS CLI, you can configure the IAM credentials that you use\. For more information, see [Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) in the *AWS Command Line Interface User Guide*\. You can also configure `kubectl` to use an IAM role, if you assume an IAM role to access Kubernetes objects on your cluster\. For more information, see [Creating or updating a `kubeconfig` file for an Amazon EKS cluster](create-kubeconfig.md)\.

## `hostname doesn't match`<a name="python-version"></a>

Your system's Python version must be `2.7.9` or later\. Otherwise, you receive `hostname doesn't match` errors with AWS CLI calls to Amazon EKS\. For more information, see [What are "hostname doesn't match" errors?](https://requests.readthedocs.io/en/latest/community/faq.html#what-are-hostname-doesn-t-match-errors) in the *Python Requests Frequently Asked Questions*\.

## `getsockopt: no route to host`<a name="troubleshoot-docker-cidr"></a>

Docker runs in the `172.17.0.0/16` CIDR range in Amazon EKS clusters\. We recommend that your cluster's VPC subnets do not overlap this range\. Otherwise, you will receive the following error:

```
Error: : error upgrading connection: error dialing backend: dial tcp 172.17.<nn>.<nn>:10250: getsockopt: no route to host
```

## `Instances failed to join the Kubernetes cluster`<a name="instances-failed-to-join"></a>

If you receive the error `Instances failed to join the Kubernetes cluster` in the AWS Management Console, ensure that either the cluster's private endpoint access is enabled, or that you have correctly configured CIDR blocks for public endpoint access\. For more information, see [Amazon EKS cluster endpoint access control](cluster-endpoint.md)\.

## Managed node group error codes<a name="troubleshoot-managed-node-groups"></a>

If your managed node group encounters a hardware health issue, Amazon EKS returns an error code to help you to diagnose the issue\. These health checks don't detect software issues because they are based on [Amazon EC2 health checks](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring-system-instance-status-check.html)\. The following list describes the error codes\.

**AccessDenied**  
Amazon EKS or one or more of your managed nodes is failing to authenticate or authorize with your Kubernetes cluster API server\. For more information about resolving a common cause, see [Fixing a common cause of `AccessDenied` errors for managed node groups](#access-denied-managed-node-groups)\. Private Windows AMIs can also cause this error code alongside the `Not authorized for images` error message\. For more information, see [`Not authorized for images`](#not-authorized-for-images)\.

**AmiIdNotFound**  
We couldn't find the AMI ID associated with your launch template\. Make sure that the AMI exists and is shared with your account\.

**AutoScalingGroupNotFound**  
We couldn't find the Auto Scaling group associated with the managed node group\. You may be able to recreate an Auto Scaling group with the same settings to recover\.

**ClusterUnreachable**  
Amazon EKS or one or more of your managed nodes is unable to communicate with your Kubernetes cluster API server\. This can happen if there are network disruptions or if API servers are timing out processing requests\.

**Ec2SecurityGroupNotFound**  
We couldn't find the cluster security group for the cluster\. You must recreate your cluster\.

**Ec2SecurityGroupDeletionFailure**  
We could not delete the remote access security group for your managed node group\. Remove any dependencies from the security group\.

**Ec2LaunchTemplateNotFound**  
We couldn't find the Amazon EC2 launch template for your managed node group\. You must recreate your node group to recover\.

**Ec2LaunchTemplateVersionMismatch**  
The Amazon EC2 launch template version for your managed node group doesn't match the version that Amazon EKS created\. You may be able to revert to the version that Amazon EKS created to recover\.

**IamInstanceProfileNotFound**  
We couldn't find the IAM instance profile for your managed node group\. You may be able to recreate an instance profile with the same settings to recover\.

**IamNodeRoleNotFound**  
We couldn't find the IAM role for your managed node group\. You may be able to recreate an IAM role with the same settings to recover\.

**AsgInstanceLaunchFailures**  
Your Auto Scaling group is experiencing failures while attempting to launch instances\.

**NodeCreationFailure**  
Your launched instances are unable to register with your Amazon EKS cluster\. Common causes of this failure are insufficient [node IAM role](create-node-role.md) permissions or lack of outbound internet access for the nodes\. Your nodes must meet either of the following requirements:  
+ Able to access the internet using a public IP address\. The security group associated to the subnet the node is in must allow the communication\. For more information, see [Subnet requirements and considerations](network_reqs.md#network-requirements-subnets) and [Amazon EKS security group requirements and considerations](sec-group-reqs.md)\.
+ Your nodes and VPC must meet the requirements in [Private cluster requirements](private-clusters.md)\. 

**InstanceLimitExceeded**  
Your AWS account is unable to launch any more instances of the specified instance type\. You may be able to request an Amazon EC2 instance limit increase to recover\.

**InsufficientFreeAddresses**  
One or more of the subnets associated with your managed node group doesn't have enough available IP addresses for new nodes\.

**InternalFailure**  
These errors are usually caused by an Amazon EKS server\-side issue\.

### Fixing a common cause of `AccessDenied` errors for managed node groups<a name="access-denied-managed-node-groups"></a>

The most common cause of `AccessDenied` errors when performing operations on managed node groups is missing the `eks:node-manager` `ClusterRole` or `ClusterRoleBinding`\. Amazon EKS sets up these resources in your cluster as part of onboarding with managed node groups, and these are required for managing the node groups\.

The `ClusterRole` may change over time, but it should look similar to the following example:

```
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: eks:node-manager
rules:
- apiGroups:
  - ''
  resources:
  - pods
  verbs:
  - get
  - list
  - watch
  - delete
- apiGroups:
  - ''
  resources:
  - nodes
  verbs:
  - get
  - list
  - watch
  - patch
- apiGroups:
  - ''
  resources:
  - pods/eviction
  verbs:
  - create
```

The `ClusterRoleBinding` may change over time, but it should look similar to the following example:

```
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: eks:node-manager
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: eks:node-manager
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: eks:node-manager
```

Verify that the `eks:node-manager` `ClusterRole` exists\.

```
kubectl describe clusterrole eks:node-manager
```

If present, compare the output to the previous `ClusterRole` example\.

Verify that the `eks:node-manager` `ClusterRoleBinding` exists\.

```
kubectl describe clusterrolebinding eks:node-manager
```

If present, compare the output to the previous `ClusterRoleBinding` example\.

If you've identified a missing or broken `ClusterRole` or `ClusterRoleBinding` as the cause of an `AcessDenied` error while requesting managed node group operations, you can restore them\. Save the following contents to a file named `eks-node-manager-role.yaml`\.

```
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: eks:node-manager
rules:
- apiGroups:
  - ''
  resources:
  - pods
  verbs:
  - get
  - list
  - watch
  - delete
- apiGroups:
  - ''
  resources:
  - nodes
  verbs:
  - get
  - list
  - watch
  - patch
- apiGroups:
  - ''
  resources:
  - pods/eviction
  verbs:
  - create
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: eks:node-manager
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: eks:node-manager
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: eks:node-manager
```

Apply the file\.

```
kubectl apply -f eks-node-manager-role.yaml
```

Retry the node group operation to see if that resolved your issue\.

## `Not authorized for images`<a name="not-authorized-for-images"></a>

One potential cause of a `Not authorized for images` error message is using a private Amazon EKS Windows AMI to launch Windows managed node groups\. After releasing new Windows AMIs, AWS makes AMIs that are older than 4 months private, which makes them no longer accessible\. If your managed node group is using a private Windows AMI, consider [updating your Windows managed node group](update-managed-node-group.md)\. While we can’t guarantee that we can provide access to AMIs that have been made private, you can request access by filing a ticket with AWS Support\. For more information, see [Patches, security updates, and AMI IDs](https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/aws-windows-ami.html#ami-patches-security-ID) in the *Amazon EC2 User Guide for Windows Instances*\.

## Node is in `NotReady` state<a name="not-ready"></a>

If your node enters a `NotReady` status, this likely indicates that the node is unhealthy and unavailable to schedule new Pods\. This can occur for various reasons, such as the node lacking sufficient resources for CPU, memory, or available disk space\.

For Amazon EKS optimized Windows AMIs, there’s no reservation for compute resources specified by default in the `kubelet` configuration\. To help prevent resource issues, you can reserve compute resources for system processes by providing the `kubelet` with configuration values for [https://kubernetes.io/docs/tasks/administer-cluster/reserve-compute-resources/#kube-reserved](https://kubernetes.io/docs/tasks/administer-cluster/reserve-compute-resources/#kube-reserved) and/or [https://kubernetes.io/docs/tasks/administer-cluster/reserve-compute-resources/#system-reserved](https://kubernetes.io/docs/tasks/administer-cluster/reserve-compute-resources/#system-reserved)\. You do this using the `-KubeletExtraArgs` command\-line parameter in the bootstrap script\. For more information, see [Reserve Compute Resources for System Daemons](https://kubernetes.io/docs/tasks/administer-cluster/reserve-compute-resources/) in the Kubernetes documentation and [Bootstrap script configuration parameters](eks-optimized-windows-ami.md#bootstrap-script-configuration-parameters) in this user guide\.

## CNI log collection tool<a name="troubleshoot-cni"></a>

The Amazon VPC CNI plugin for Kubernetes has its own troubleshooting script that is available on nodes at `/opt/cni/bin/aws-cni-support.sh`\. You can use the script to collect diagnostic logs for support cases and general troubleshooting\.

Use the following command to run the script on your node:

```
sudo bash /opt/cni/bin/aws-cni-support.sh
```

**Note**  
If the script is not present at that location, then the CNI container failed to run\. You can manually download and run the script with the following command:  

```
curl -O https://raw.githubusercontent.com/awslabs/amazon-eks-ami/master/log-collector-script/linux/eks-log-collector.sh
sudo bash eks-log-collector.sh
```

The script collects the following diagnostic information\. The CNI version that you have deployed can be earlier than the script version\.

```
      This is version 0.6.1. New versions can be found at https://github.com/awslabs/amazon-eks-ami

Trying to collect common operating system logs... 
Trying to collect kernel logs... 
Trying to collect mount points and volume information... 
Trying to collect SELinux status... 
Trying to collect iptables information... 
Trying to collect installed packages... 
Trying to collect active system services... 
Trying to collect Docker daemon information... 
Trying to collect kubelet information... 
Trying to collect L-IPAMD information... 
Trying to collect sysctls information... 
Trying to collect networking information... 
Trying to collect CNI configuration information... 
Trying to collect running Docker containers and gather container data... 
Trying to collect Docker daemon logs... 
Trying to archive gathered information... 

	Done... your bundled logs are located in /var/log/eks_i-0717c9d54b6cfaa19_2020-03-24_0103-UTC_0.6.1.tar.gz
```

The diagnostic information is collected and stored at:

```
/var/log/eks_i-0717c9d54b6cfaa19_2020-03-24_0103-UTC_0.6.1.tar.gz
```

## Container runtime network not ready<a name="troubleshoot-container-runtime-network"></a>

You may receive a `Container runtime network not ready` error and authorization errors similar to the following:

```
4191 kubelet.go:2130] Container runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady message:docker: network plugin is not ready: cni config uninitialized
4191 reflector.go:205] k8s.io/kubernetes/pkg/kubelet/kubelet.go:452: Failed to list *v1.Service: Unauthorized
4191 kubelet_node_status.go:106] Unable to register node "ip-10-40-175-122.ec2.internal" with API server: Unauthorized
4191 reflector.go:205] k8s.io/kubernetes/pkg/kubelet/kubelet.go:452: Failed to list *v1.Service: Unauthorized
```

This can happen due to one of the following reasons:

1. You either don't have an `aws-auth` `ConfigMap` on your cluster or it doesn't include entries for the IAM role that you configured your nodes with\.

   This `ConfigMap` entry is necessary if your nodes meet one of the following criteria:
   + Managed nodes in a cluster with any Kubernetes or platform version\.
   + Self\-managed nodes in a cluster that is earlier than one of the platform versions listed in the prerequisites section of the [Manage access entries](access-entries.md) topic\.

   To resolve the issue, view the existing entries in your `ConfigMap` by replacing *my\-cluster* in the following command with the name of your cluster and then running the modified command: **eksctl get iamidentitymapping \-\-cluster *my\-cluster***\. If you receive an error message from the command, it might be because your cluster doesn't have an `aws-auth` `ConfigMap`\. The following command adds an entry to the `ConfigMap`\. If the `ConfigMap` doesn't exist, the command also creates it\. Replace *111122223333* with the AWS account ID for the IAM role and *myAmazonEKSNodeRole* with the name of your node's role\.

   ```
   eksctl create iamidentitymapping --cluster my-cluster \
       --arn arn:aws:iam::111122223333:role/myAmazonEKSNodeRole --group system:bootstrappers,system:nodes \
       --username system:node:{{EC2PrivateDNSName}}
   ```

   The ARN of the role that you specify can't include a [path](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-friendly-names) other than `/`\. For example, if the name of your role is `development/apps/my-role`, you'd need to change it to `my-role` when specifying the ARN of the role\. Make sure that you specify the node IAM role ARN \(not the instance profile ARN\)\.

1. Your self\-managed nodes are in a cluster with a platform version at the minimum version listed in the prerequisites in the [Manage access entries](access-entries.md) topic, but an entry isn't listed in the `aws-auth` `ConfigMap` \(see previous item\) for the node's IAM role or an access entry doesn't exist for the role\. To resolve the issue, view your existing access entries by replacing *my\-cluster* in the following command with the name of your cluster and then running the modified command: **aws eks list\-access\-entries \-\-cluster\-name *my\-cluster***\. The following command adds an access entry for the node's IAM role\. Replace *111122223333* with the AWS account ID for the IAM role and *myAmazonEKSNodeRole* with the name of your node's role\. If you have a Windows node, replace *EC2\_Linux* with **EC2\_Windows**\. Make sure that you specify the node IAM role ARN \(not the instance profile ARN\)\.

   ```
   aws eks create-access-entry --cluster-name my-cluster --principal-arn arn:aws:iam::111122223333:role/myAmazonEKSNodeRole --type EC2_Linux
   ```

## TLS handshake timeout<a name="troubleshoot-tls-handshake-timeout"></a>

When a node is unable to establish a connection to the public API server endpoint, you may see an error similar to the following error\.

```
server.go:233] failed to run Kubelet: could not init cloud provider "aws": error finding instance i-1111f2222f333e44c: "error listing AWS instances: \"RequestError: send request failed\\ncaused by: Post  net/http: TLS handshake timeout\""
```

The `kubelet` process will continually respawn and test the API server endpoint\. The error can also occur temporarily during any procedure that performs a rolling update of the cluster in the control plane, such as a configuration change or version update\.

To resolve the issue, check the route table and security groups to ensure that traffic from the nodes can reach the public endpoint\.

## InvalidClientTokenId<a name="default-region-env-variable"></a>

If you're using IAM roles for service accounts for a Pod or `DaemonSet` deployed to a cluster in a China AWS Region, and haven't set the `AWS_DEFAULT_REGION` environment variable in the spec, the Pod or `DaemonSet` may receive the following error: 

```
An error occurred (InvalidClientTokenId) when calling the GetCallerIdentity operation: The security token included in the request is invalid
```

To resolve the issue, you need to add the `AWS_DEFAULT_REGION` environment variable to your Pod or `DaemonSet` spec, as shown in the following example Pod spec\.

```
apiVersion: v1
kind: Pod
metadata:
  name: envar-demo
  labels:
    purpose: demonstrate-envars
spec:
  containers:
  - name: envar-demo-container
    image: gcr.io/google-samples/node-hello:1.0
    env:
    - name: AWS_DEFAULT_REGION
      value: "region-code"
```

## VPC admission webhook certificate expiration<a name="troubleshoot-vpc-admission-webhook-certificate-expiration"></a>

If the certificate used to sign the VPC admission webhook expires, the status for new Windows Pod deployments stays at `ContainerCreating`\. 

To resolve the issue if you have legacy Windows support on your data plane, see [Renewing the VPC admission webhook certificate](windows-support.md#windows-certificate)\. If your cluster and platform version are later than a version listed in the [Windows support prerequisites](windows-support.md#windows-support-prerequisites), then we recommend that you remove legacy Windows support on your data plane and enable it for your control plane\. Once you do, you don't need to manage the webhook certificate\. For more information, see [Enabling Windows support for your Amazon EKS cluster](windows-support.md)\.

## Node groups must match Kubernetes version before upgrading control plane<a name="troubleshoot-node-grups-must-match-kubernetes-version"></a>

Before you upgrade a control plane to a new Kubernetes version, the minor version of the managed and Fargate nodes in your cluster must be the same as the version of your control plane's current version\. The Amazon EKS `update-cluster-version` API rejects requests until you upgrade all Amazon EKS managed nodes to the current cluster version\. Amazon EKS provides APIs to upgrade managed nodes\. For information on upgrading a managed node group's Kubernetes version, see [Updating a managed node group](update-managed-node-group.md)\. To upgrade the version of a Fargate node, delete the pod that's represented by the node and redeploy the pod after you upgrade your control plane\. For more information, see [Updating an Amazon EKS cluster Kubernetes version](update-cluster.md)\.

## When launching many nodes, there are `Too Many Requests` errors<a name="too-many-requests"></a>

If you launch many nodes simultaneously, you may see an error message in the [Amazon EC2 user data](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html#user-data-shell-scripts) execution logs that says `Too Many Requests`\. This can occur because the control plane is being overloaded with `describeCluster` calls\. The overloading results in throttling, nodes failing to run the bootstrap script, and nodes failing to join the cluster altogether\.

Make sure that `--apiserver-endpoint`, `--b64-cluster-ca`, and `--dns-cluster-ip` arguments are being passed to the node's bootstrap script\. When including these arguments, there's no need for the bootstrap script to make a `describeCluster` call, which helps prevent the control plane from being overloaded\. For more information, see [Provide user data to pass arguments to the `bootstrap.sh` file included with an Amazon EKS optimized Linux/Bottlerocket AMI](launch-templates.md#mng-specify-eks-ami)\.

## HTTP 401 unauthorized error response on Kubernetes API server requests<a name="troubleshooting-boundservicetoken"></a>

You see these errors if a Pod's service account token has expired on a cluster\.

Your Amazon EKS cluster's Kubernetes API server rejects requests with tokens older than 90 days\. In previous Kubernetes versions, tokens did not have an expiration\. This means that clients that rely on these tokens must refresh them within an hour\. To prevent the Kubernetes API server from rejecting your request due to an invalid token, the [Kubernetes client SDK](https://kubernetes.io/docs/reference/using-api/client-libraries/) version used by your workload must be the same, or later than the following versions:
+ Go version `0.15.7` and later
+ Python version `12.0.0` and later
+ Java version `9.0.0` and later
+ JavaScript version `0.10.3` and later
+ Ruby `master` branch
+ Haskell version `0.3.0.0`
+ C\# version `7.0.5` and later

You can identify all existing Pods in your cluster that are using stale tokens\. For more information, see [Kubernetes service accounts](service-accounts.md#identify-pods-using-stale-tokens)\.

## Amazon EKS platform version is more than two versions behind the current platform version<a name="troubleshooting-platform-version"></a>

This can happen when Amazon EKS isn't able to automatically update your cluster's [platform version](platform-versions.md)\. Though there are many causes for this, some of the common causes follow\. If any of these problems apply to your cluster, it may still function, its platform version just won't be updated by Amazon EKS\.

**Problem**  
The [cluster IAM role](service_IAM_role.md) was deleted – This role was specified when the cluster was created\. You can see which role was specified with the following command\. Replace *my\-cluster* with the name of your cluster\.

```
aws eks describe-cluster --name my-cluster --query cluster.roleArn --output text | cut -d / -f 2
```

An example output is as follows\.

```
eksClusterRole
```

**Solution**  
Create a new [cluster IAM role](service_IAM_role.md) with the same name\.

**Problem**  
A subnet specified during cluster creation was deleted – The subnets to use with the cluster were specified during cluster creation\. You can see which subnets were specified with the following command\. Replace *my\-cluster* with the name of your cluster\.

```
aws eks describe-cluster --name my-cluster --query cluster.resourcesVpcConfig.subnetIds
```

An example output is as follows\.

```
[
"subnet-EXAMPLE1",
"subnet-EXAMPLE2"
]
```

**Solution**  
Confirm whether the subnet IDs exist in your account\.

```
vpc_id=$(aws eks describe-cluster --name my-cluster --query cluster.resourcesVpcConfig.vpcId --output text)
aws ec2 describe-subnets --filters "Name=vpc-id,Values=$vpc_id" --query "Subnets[*].SubnetId"
```

An example output is as follows\.

```
[
"subnet-EXAMPLE3",
"subnet-EXAMPLE4"
]
```

If the subnet IDs returned in the output don't match the subnet IDs that were specified when the cluster was created, then if you want Amazon EKS to update the cluster, you need to change the subnets used by the cluster\. This is because if you specified more than two subnets when you created your cluster, Amazon EKS randomly selects subnets that you specified to create new elastic network interfaces in\. These network interfaces enable the control plane to communicate with your nodes\. Amazon EKS won't update the cluster if the subnet it selects doesn't exist\. You have no control over which of the subnets that you specified at cluster creation that Amazon EKS chooses to create a new network interface in\.

When you initiate a Kubernetes version update for your cluster, the update can fail for the same reason\. 

**Problem**  
A security group specified during cluster creation was deleted – If you specified security groups during cluster creation, you can see their IDs with the following command\. Replace *my\-cluster* with the name of your cluster\.

```
aws eks describe-cluster --name my-cluster --query cluster.resourcesVpcConfig.securityGroupIds
```

An example output is as follows\.

```
[
    "sg-EXAMPLE1"
]
```

If `[]` is returned, then no security groups were specified when the cluster was created and a missing security group isn't the problem\. If security groups are returned, then confirm that the security groups exist in your account\.

**Solution**  
Confirm whether these security groups exist in your account\.

```
vpc_id=$(aws eks describe-cluster --name my-cluster --query cluster.resourcesVpcConfig.vpcId --output text)
aws ec2 describe-security-groups --filters "Name=vpc-id,Values=$vpc_id" --query "SecurityGroups[*].GroupId"
```

An example output is as follows\.

```
[
"sg-EXAMPLE2"
]
```

If the security group IDs returned in the output don't match the security group IDs that were specified when the cluster was created, then if you want Amazon EKS to update the cluster, you need to change the security groups used by the cluster\. Amazon EKS won't update a cluster if the security group IDs specified at cluster creation don't exist\.

When you initiate a Kubernetes version update for your cluster, the update can fail for the same reason\. 

**Other reasons that Amazon EKS doesn't update the platform version of your cluster**
+ You don't have at least six \(though we recommend 16\) available IP addresses in each of the subnets that you specified when you created your cluster\. If you don't have enough available IP addresses in the subnet, you either need to free up IP addresses in the subnet or you need to change the subnets used by the cluster to use subnets with enough available IP addresses\.
+ You enabled [secrets encryption](enable-kms.md) when you created your cluster and the AWS KMS key that you specified has been deleted\. If you want Amazon EKS to update the cluster, you need to create a new cluster

## Cluster health FAQs and error codes with resolution paths<a name="cluster-health-status"></a>

Amazon EKS detects issues with your EKS clusters and the cluster infrastructure and stores it in the *cluster health*\. You can detect, troubleshoot, and address cluster issues more rapidly with the aid of cluster health information\. This enables you to create application environments that are more secure and up\-to\-date\. Additionally, it may be impossible for you to upgrade to newer versions of Kubernetes or for Amazon EKS to install security updates on a degraded cluster as a result of issues with the necessary infrastructure or cluster configuration\. Amazon EKS can take 3 hours to detect issues or detect that an issue is resolved\.

The health of an Amazon EKS cluster is a shared responsibility between Amazon EKS and its users\. You are responsible for the prerequisite infrastructure of IAM roles and Amazon VPC subnets, as well as other necessary infrastructure, that must be provided in advance\. Amazon EKS detects changes in the configuration of this infrastructure and the cluster\.

To access your health of your cluster in the Amazon EKS console, look for a section called **Health Issues** in the **Overview** tab of the Amazon EKS cluster detail page\. This data will be also be available by calling the `DescribeCluster` action in the EKS API, for example from within the AWS Command Line Interface\.

**Why should I use this feature?**  
You will get increased visibility into the health of your Amazon EKS cluster, quickly diagnose and fix any issues, without needing to spend time debugging or opening AWS support cases\. For example: you accidentally deleted a subnet for the Amazon EKS cluster, Amazon EKS won’t be able to create cross account network interfaces and Kubernetes AWS CLI commands such as `kubectl` exec or `kubectl` logs\. These will fail with the error: `Error from server: error dialing backend: remote error: tls: internal error.` Now you will see an Amazon EKS health issue that says: `subnet-da60e280 was deleted: could not create network interface`\.

**How does this feature relate or work with other AWS services?**  
IAM roles and Amazon VPC subnets are two examples of prerequisite infrastructure that cluster health detects issues with\. This feature will return detailed information if those resources are not configured properly\.

**Does a cluster with health issues incur charges?**  
Yes, every Amazon EKS cluster is billed at the standard Amazon EKS pricing\. The *cluster health* feature is available at no additional charge\.

**Does this feature work with Amazon EKS clusters on AWS Outposts?**  
Yes, cluster issues are detected for EKS clusters in the AWS Cloud including *extended clusters* on AWS Outposts and *local clusters* on AWS Outposts\. Cluster health doesn't detect issues with Amazon EKS Anywhere or Amazon EKS Distro \(EKS\-D\)\.

**Can I get notified when new issues are detected?**  
No, you need to check the Amazon EKS Console or call the EKS `DescribeCluster` API\.

**Does the console give me warnings for health issues?**  
Yes, any cluster with health issues will include a banner at the top of the console\.

The first two columns are what are needed for API response values\. The third field of the [Health ClusterIssue](https://docs.aws.amazon.com/eks/latest/APIReference/API_ClusterIssue.html) object is resourceIds, the return of which is dependent on the issue type\.


| Code | Message | ResourceIds | Cluster Recoverable? | 
| --- | --- | --- | --- | 
|  SUBNET\_NOT\_FOUND  |  We couldn't find one or more subnets currently associated with your cluster\. Call Amazon EKS update\-cluster\-config API to update subnets\.  | Subnet Ids | Yes | 
| SECURITY\_GROUP\_NOT\_FOUND | We couldn't find one or more security groups currently associated with your cluster\. Call Amazon EKS update\-cluster\-config API to update security groups | Security group Ids | Yes | 
| IP\_NOT\_AVAILABLE | One or more of the subnets associated with your cluster does not have enough available IP addresses for Amazon EKS to perform cluster management operations\. Free up addresses in the subnet\(s\), or associate different subnets to your cluster using the Amazon EKS update\-cluster\-config API\. | Subnet Ids | Yes | 
| VPC\_NOT\_FOUND | We couldn't find the VPC associated with your cluster\. You must delete and recreate your cluster\. | VPC id | No | 
| ASSUME\_ROLE\_ACCESS\_DENIED | Your cluster is not using the Amazon EKS service\-linked\-role\. We couldn't assume the role associated with your cluster to perform required Amazon EKS management operations\. Check the role exists and has the required trust policy\. | The cluster IAM role | Yes | 
|  PERMISSION\_ACCESS\_DENIED  |  Your cluster is not using the Amazon EKS service\-linked\-role\. The role associated with your cluster does not grant sufficient permissions for Amazon EKS to perform required management operations\. Check the policies attached to the cluster role and if any separate deny policies are applied\. | The cluster IAM role | Yes | 
|  ASSUME\_ROLE\_ACCESS\_DENIED\_USING\_SLR  |  We couldn't assume the Amazon EKS cluster management service\-linked\-role\. Check the role exists and has the required trust policy\.  |  The Amazon EKS service\-linked\-role  | Yes | 
|  PERMISSION\_ACCESS\_DENIED\_USING\_SLR  |  The Amazon EKS cluster management service\-linked\-role does not grant sufficient permissions for Amazon EKS to perform required management operations\. Check the policies attached to the cluster role and if any separate deny policies are applied\.  |  The Amazon EKS service\-linked\-role  | Yes | 
|  OPT\_IN\_REQUIRED  |  Your account doesn't have an Amazon EC2 service subscription\. Update your account subscriptions in your account settings page\.  | N/A | Yes | 
|  STS\_REGIONAL\_ENDPOINT\_DISABLED  |  The STS regional endpoint is disabled\. Enable the endpoint for Amazon EKS to perform required cluster management operations\.  | N/A | Yes | 
|  KMS\_KEY\_DISABLED  |  The AWS KMS Key associated with your cluster is disabled\. Re\-enable the key to recover your cluster\.  |  The KMS Key Arn  | Yes | 
|  KMS\_KEY\_NOT\_FOUND  |  We couldn't find the AWS KMS key associated with your cluster\. You must delete and recreate the cluster\.  |  The KMS Key ARN  | No | 
|  KMS\_GRANT\_REVOKED  |  Grants for the AWS KMS Key associated with your cluster are revoked\. You must delete and recreate the cluster\.  |  The KMS Key Arn  | No | 