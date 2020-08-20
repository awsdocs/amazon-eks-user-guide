# Amazon EKS troubleshooting<a name="troubleshooting"></a>

This chapter covers some common errors that you may see while using Amazon EKS and how to work around them\.

## Insufficient capacity<a name="ICE"></a>

If you receive the following error while attempting to create an Amazon EKS cluster, then one of the Availability Zones you specified does not have sufficient capacity to support a cluster\.

`Cannot create cluster 'example-cluster' because region-1d, the targeted Availability Zone, does not currently have sufficient capacity to support the cluster. Retry and choose from these Availability Zones: region-1a, region-1b, region-1c`

Retry creating your cluster with subnets in your cluster VPC that are hosted in the Availability Zones returned by this error message\.

## Nodes fail to join cluster<a name="worker-node-fail"></a>

There are a few common reasons that prevent nodes from joining the cluster:
+ The `aws-auth-cm.yaml` file does not have the correct IAM role ARN for your nodes\. Ensure that the node IAM role ARN \(not the instance profile ARN\) is specified in your `aws-auth-cm.yaml` file\. For more information, see [Launching self\-managed Amazon Linux nodes](launch-workers.md)\.
+ The **ClusterName** in your node AWS CloudFormation template does not exactly match the name of the cluster you want your nodes to join\. Passing an incorrect value to this field results in an incorrect configuration of the node's `/var/lib/kubelet/kubeconfig` file, and the nodes will not join the cluster\.
+ The node is not tagged as being *owned* by the cluster\. Your nodes must have the following tag applied to them, where `<cluster_name>` is replaced with the name of your cluster\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/troubleshooting.html)
+ The nodes may not be able to access the cluster using a public IP address\. Ensure that nodes deployed in public subnets are assigned a public IP address\. If not, you can associate an elastic IP address to a node after it's launched\. For more information, see [Associating an elastic IP address with a running instance or network interface](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html#using-instance-addressing-eips-associating)\. If the public subnet is not set to automatically assign public IP addresses to instances deployed to it, then we recommend enabling that setting\. For more information, see [Modifying the public IPv4 addressing attribute for your subnet](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#subnet-public-ip)\. If the node is deployed to a private subnet, then the subnet must have a route to a NAT gateway that has a public IP address assigned to it\.
+ The STS endpoint for the Region that you're deploying the nodes to is not enabled for your account\. To enable the region, see [Activating and deactivating AWS STS in an AWS Region](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_enable-regions.html#sts-regions-activate-deactivate)\.

## Unauthorized or access denied \(`kubectl`\)<a name="unauthorized"></a>

If you receive one of the following errors while running kubectl commands, then your kubectl is not configured properly for Amazon EKS or the IAM user or role credentials that you are using do not map to a Kubernetes RBAC user with sufficient permissions in your Amazon EKS cluster\.
+ `could not get token: AccessDenied: Access denied`
+ `error: You must be logged in to the server (Unauthorized)`
+ `error: the server doesn't have a resource type "svc"`

This could be because the cluster was created with one set of AWS credentials \(from an IAM user or role\), and kubectl is using a different set of credentials\.

When an Amazon EKS cluster is created, the IAM entity \(user or role\) that creates the cluster is added to the Kubernetes RBAC authorization table as the administrator \(with `system:masters` permissions\)\. Initially, only that IAM user can make calls to the Kubernetes API server using kubectl\. For more information, see [Managing users or IAM roles for your cluster](add-user-role.md)\.  If you use the console to create the cluster, you must ensure that the same IAM user credentials are in the AWS SDK credential chain when you are running kubectl commands on your cluster\.

If you install and configure the AWS CLI, you can configure the IAM credentials for your user\.  For more information, see [Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) in the *AWS Command Line Interface User Guide*\.

If you assumed a role to create the Amazon EKS cluster, you must ensure that kubectl is configured to assume the same role\. Use the following command to update your kubeconfig file to use an IAM role\. For more information, see [Create a `kubeconfig` for Amazon EKS](create-kubeconfig.md)\.

```
aws --region region-code eks update-kubeconfig --name cluster_name --role-arn arn:aws:iam::aws_account_id:role/role_name
```

To map an IAM user to a Kubernetes RBAC user, see [Managing users or IAM roles for your cluster](add-user-role.md) or watch a [video](https://www.youtube.com/watch?time_continue=3&v=97n9vWV3VcU) about how to map a user\.

## `aws-iam-authenticator` Not found<a name="no-auth-provider"></a>

If you receive the error `"aws-iam-authenticator": executable file not found in $PATH`, then your kubectl is not configured for Amazon EKS\. For more information, see [Installing `aws-iam-authenticator`](install-aws-iam-authenticator.md)\.

**Note**  
The `aws-iam-authenticator` is not required if you have the AWS CLI version 1\.16\.156 or higher installed\.

## `hostname doesn't match`<a name="python-version"></a>

Your system's Python version must be 2\.7\.9 or later\. Otherwise, you receive `hostname doesn't match` errors with AWS CLI calls to Amazon EKS\. For more information, see [What are "hostname doesn't match" errors?](https://requests.readthedocs.io/en/master/community/faq/#what-are-hostname-doesn-t-match-errors) in the Python Requests FAQ\.

## `getsockopt: no route to host`<a name="troubleshoot-docker-cidr"></a>

Docker runs in the `172.17.0.0/16` CIDR range in Amazon EKS clusters\. We recommend that your cluster's VPC subnets do not overlap this range\. Otherwise, you will receive the following error:

```
Error: : error upgrading connection: error dialing backend: dial tcp 172.17.nn.nn:10250: getsockopt: no route to host
```

## Managed node group errors<a name="troubleshoot-managed-node-groups"></a>

If you receive the error "Instances failed to join the kubernetes cluster" in the AWS Management Console, ensure that either the cluster's private endpoint access is enabled, or that you have correctly configured CIDR blocks for public endpoint access\. For more information, see [Amazon EKS cluster endpoint access control](cluster-endpoint.md)\.

If your managed node group encounters a health issue, Amazon EKS returns an error message to help you to diagnose the issue\. The following error messages and their associated descriptions are shown below\.
+ **AutoScalingGroupNotFound**: We couldn't find the Auto Scaling group associated with the managed node group\. You may be able to recreate an Auto Scaling group with the same settings to recover\.
+ **Ec2SecurityGroupNotFound**: We couldn't find the cluster security group for the cluster\. You must recreate your cluster\.
+ **Ec2SecurityGroupDeletionFailure**: We could not delete the remote access security group for your managed node group\. Remove any dependencies from the security group\.
+ **Ec2LaunchTemplateNotFound**: We couldn't find the Amazon EC2 launch template for your managed node group\. You may be able to recreate a launch template with the same settings to recover\.
+ **Ec2LaunchTemplateVersionMismatch**: The Amazon EC2 launch template version for your managed node group does not match the version that Amazon EKS created\. You may be able to revert to the version that Amazon EKS created to recover\.
+ **IamInstanceProfileNotFound**: We couldn't find the IAM instance profile for your managed node group\. You may be able to recreate an instance profile with the same settings to recover\.
+ **IamNodeRoleNotFound**: We couldn't find the IAM role for your managed node group\. You may be able to recreate an IAM role with the same settings to recover\.
+ **AsgInstanceLaunchFailures**: Your Auto Scaling group is experiencing failures while attempting to launch instances\.
+ **NodeCreationFailure**: Your launched instances are unable to register with your Amazon EKS cluster\. Common causes of this failure are insufficient [node IAM role](worker_node_IAM_role.md) permissions or lack of outbound internet access for the nodes\. Your nodes must be able to access the internet using a public IP address to function properly\. For more information, see [VPC IP addressing](network_reqs.md#vpc-cidr)\. Your nodes must also have ports open to the internet\. For more information, see [Amazon EKS security group considerations](sec-group-reqs.md)\.
+ **InstanceLimitExceeded**: Your AWS account is unable to launch any more instances of the specified instance type\. You may be able to request an Amazon EC2 instance limit increase to recover\.
+ **InsufficientFreeAddresses**: One or more of the subnets associated with your managed node group does not have enough available IP addresses for new nodes\.
+ **AccessDenied**: Amazon EKS or one or more of your managed nodes is unable to communicate with your cluster API server\. For more information about resolving this error, see [Fixing `AccessDenied` errors for managed node groups](#access-denied-managed-node-groups)\.
+ **InternalFailure**: These errors are usually caused by an Amazon EKS server\-side issue\.

### Fixing `AccessDenied` errors for managed node groups<a name="access-denied-managed-node-groups"></a>

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

## CNI log collection tool<a name="troubleshoot-cni"></a>

The Amazon VPC CNI plugin for Kubernetes has its own troubleshooting script \(which is available on nodes at `/opt/cni/bin/aws-cni-support.sh`\) that you can use to collect diagnostic logs for support cases and general troubleshooting\.

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

The diagnostic information is collected and stored at ``

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

The errors are most likely related to the AWS IAM Authenticator configuration map not being applied to the nodes\. The configuration map provides the `system:bootstrappers` and `system:nodes` Kubernetes RBAC permissions for nodes to register to the cluster\. For more information, see **To enable nodes to join your cluster** on the **Self\-managed nodes** tab of [Launching self\-managed Amazon Linux nodes](launch-workers.md)\. Ensure that you specify the **Role ARN** of the instance role in the configuration map, not the **Instance Profile ARN**\.

The authenticator does not recognize a **Role ARN** if it includes a [path](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-friendly-names) other than `/`, such as the following example:

```
arn:aws:iam::111122223333:role/development/apps/prod-iam-role-NodeInstanceRole-621LVEXAMPLE
```

When specifying a **Role ARN** in the configuration map that includes a path other than `/`, you must drop the path\. The ARN above would be specified as the following:

```
arn:aws:iam::111122223333:role/prod-iam-role-NodeInstanceRole-621LVEXAMPLE
```

## TLS handshake timeout<a name="troubleshoot-tls-handshake-timeout"></a>

When a node is unable to establish a connection to the public API server endpoint, you may an error similar to the following error\.

```
server.go:233] failed to run Kubelet: could not init cloud provider "aws": error finding instance i-1111f2222f333e44c: "error listing AWS instances: \"RequestError: send request failed\\ncaused by: Post  net/http: TLS handshake timeout\""
```

The `kubelet` process will continually respawn and test the API server endpoint\. The error can also occur temporarily during any procedure that performs a rolling update of the cluster in the control plane, such as a configuration change or version update\.

To resolve the issue, check the route table and security groups to ensure that traffic from the nodes can reach the public endpoint\.