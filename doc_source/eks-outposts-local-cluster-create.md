# Creating a local cluster on an Outpost<a name="eks-outposts-local-cluster-create"></a>

This topic provides an overview of what to consider when running a local cluster on an Outpost\. The topic also provides instructions for how to deploy a local cluster on an Outpost\.

**Considerations**
**Important**  
These considerations aren't replicated in related Amazon EKS documentation\. If other Amazon EKS documentation topics conflict with the considerations here, follow the considerations here\.
These considerations are subject to change and might change frequently\. So, we recommend that you regularly review this topic\.
Many of the considerations are different than the considerations for creating a cluster on the AWS Cloud\.
+ Local clusters support Outpost racks only\. A single local cluster can run across multiple physical Outpost racks that comprise a single logical Outpost\. A single local cluster can't run across multiple logical Outposts\. Each logical Outpost has a single Outpost ARN\.
+ Local clusters run and manage the Kubernetes control plane in your account on the Outpost\. You can't run workloads on the Kubernetes control plane instances or modify the Kubernetes control plane components\. These nodes are managed by the Amazon EKS service\. Changes to the Kubernetes control plane don't persist through automatic Amazon EKS management actions, such as patching\.
+ Local clusters support self\-managed add\-ons and self\-managed Amazon Linux node groups\. The [Amazon VPC CNI plugin for Kubernetes](managing-vpc-cni.md), [`kube-proxy`](managing-kube-proxy.md), and [CoreDNS](managing-coredns.md) add\-ons are automatically installed on local clusters\. 
+ Local clusters require the use of Amazon EBS on Outposts\. Your Outpost must have Amazon EBS available for the Kubernetes control plane storage\.
+ Local clusters use Amazon EBS on Outposts\. Your Outpost must have Amazon EBS available for the Kubernetes control plane storage\. Outposts support Amazon EBS `gp2` volumes only\.
+ Amazon EBS backed Kubernetes `PersistentVolumes` are supported using the Amazon EBS CSI driver\.

**Prerequisites**
+ Familiarity with the [Outposts deployment options](eks-outposts.md#outposts-overview-comparing-deployment-options), [Capacity considerations](eks-outposts-capacity-considerations.md), and [Amazon EKS local cluster VPC and subnet requirements and considerations](eks-outposts-vpc-subnet-requirements.md)\.
+ An existing Outpost\. For more information, see [What is AWS Outposts](https://docs.aws.amazon.com/outposts/latest/userguide/what-is-outposts.html)\.
+ The `kubectl` command line tool is installed on your computer or AWS CloudShell\. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster\. For example, if your cluster version is `1.28`, you can use `kubectl` version `1.27`, `1.28`, or `1.29` with it\. To install or upgrade `kubectl`, see [Installing or updating `kubectl`](install-kubectl.md)\.
+ Version `2.12.3` or later or version `1.27.160` or later of the AWS Command Line Interface \(AWS CLI\) installed and configured on your device or AWS CloudShell\. To check your current version, use `aws --version | cut -d / -f2 | cut -d ' ' -f1`\. Package managers such `yum`, `apt-get`, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI\. To install the latest version, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with aws configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the *AWS Command Line Interface User Guide*\. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version\. To update it, see [Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the *AWS CloudShell User Guide*\.
+ An IAM principal \(user or role\) with permissions to `create` and `describe` an Amazon EKS cluster\. For more information, see [Create a local Kubernetes cluster on an Outpost](security_iam_id-based-policy-examples.md#policy-create-local-cluster) and [List or describe all clusters](security_iam_id-based-policy-examples.md#policy_example2)\.

When a local Amazon EKS cluster is created, the [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) that creates the cluster is permanently added\. The principal is specifically added to the Kubernetes RBAC authorization table as the administrator\. This entity has `system:masters` permissions\. The identity of this entity isn't visible in your cluster configuration\. So, it's important to note the entity that created the cluster and make sure that you never delete it\. Initially, only the principal that created the server can make calls to the Kubernetes API server using `kubectl`\. If you use the console to create the cluster, make sure that the same IAM credentials are in the AWS SDK credential chain when you run `kubectl` commands on your cluster\. After your cluster is created, you can grant other IAM principals access to your cluster\.

**To create a local Amazon EKS local cluster**

You can create a local cluster with `eksctl`, the AWS Management Console, the [AWS CLI](https://docs.aws.amazon.com/cli/latest/reference/eks/create-cluster.html), the [Amazon EKS API](https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html), the [AWS SDKs](https://aws.amazon.com/developer/tools/), [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-outpostconfig.html) or [Terraform](https://registry.terraform.io/modules/terraform-aws-modules/eks/aws/latest)\.

1. Create a local cluster\.

------
#### [ eksctl ]

**Prerequisite**  
Version `0.175.0` or later of the `eksctl` command line tool installed on your device or AWS CloudShell\. To install or update `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\. 

**To create your cluster with `eksctl`**

   1. Copy the contents that follow to your device\. Replace the following values and then run the modified command to create the `outpost-control-plane.yaml` file:
      + Replace `region-code` with the [supported AWS Region](eks-outposts-local-cluster-overview.md#outposts-control-plane-supported-regions) that you want to create your cluster in\.
      + Replace `my-cluster` with a name for your cluster\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can't be longer than 100 characters\. The name must be unique within the AWS Region and AWS account that you're creating the cluster in\.
      + Replace `vpc-ExampleID1` and `subnet-ExampleID1` with the IDs of your existing VPC and subnet\. The VPC and subnet must meet the requirements in [Amazon EKS local cluster VPC and subnet requirements and considerations](eks-outposts-vpc-subnet-requirements.md)\.
      + Replace `uniqueid` with the ID of your Outpost\.
      + Replace `m5.large` with an instance type available on your Outpost\. Before choosing an instance type, see [Capacity considerations](eks-outposts-capacity-considerations.md)\. Three control plane instances are deployed\. You can't change this number\.

      ```
      cat >outpost-control-plane.yaml <<EOF
      apiVersion: eksctl.io/v1alpha5
      kind: ClusterConfig
      
      metadata:
        name: my-cluster
        region: region-code
        version: "1.24"
      
      vpc:
        clusterEndpoints:
          privateAccess: true
        id: "vpc-vpc-ExampleID1"
        subnets:
          private:
            outpost-subnet-1:
              id: "subnet-subnet-ExampleID1"
      
      outpost:
        controlPlaneOutpostARN: arn:aws:outposts:region-code:111122223333:outpost/op-uniqueid
        controlPlaneInstanceType: m5.large
      EOF
      ```

      For a complete list of all available options and defaults, see [AWS Outposts Support](https://eksctl.io/usage/outposts/) and [Config file schema](https://eksctl.io/usage/schema/) in the `eksctl` documentation\.

   1. Create the cluster using the configuration file that you created in the previous step\. `eksctl` creates a VPC and one subnet on your Outpost to deploy the cluster in\.

      ```
      eksctl create cluster -f outpost-control-plane.yaml
      ```

      Cluster provisioning takes several minutes\. While the cluster is being created, several lines of output appear\. The last line of output is similar to the following example line\.

      ```
      [✓]  EKS cluster "my-cluster" in "region-code" region is ready
      ```

**Tip**  
To see the most options that you can specify when creating a cluster with `eksctl`, use the **eksctl create cluster \-\-help** command\. To see all the available options, you can use a `config` file\. For more information, see [Using config files](https://eksctl.io/usage/creating-and-managing-clusters/#using-config-files) and the [config file schema](https://eksctl.io/usage/schema/) in the `eksctl` documentation\. You can find [config file examples](https://github.com/weaveworks/eksctl/tree/master/examples) on GitHub\.

   `Eksctl` automatically created an [access entry](access-entries.md) for the IAM principal \(user or role\) that created the cluster and granted the IAM principal administrator permissions to Kubernetes objects on the cluster\. If you don't want the cluster creator to have administrator access to Kubernetes objects on the cluster, add the following text to the previous configuration file: **bootstrapClusterCreatorAdminPermissions: false** \(at the same level as `metadata`, `vpc`, and `outpost`\)\. If you added the option, then after cluster creation, you need to create an access entry for at least one IAM principal, or no IAM principals will have access to Kubernetes objects on the cluster\.

------
#### [ AWS Management Console ]

**Prerequisite**  
An existing VPC and subnet that meet Amazon EKS requirements\. For more information, see [Amazon EKS local cluster VPC and subnet requirements and considerations](eks-outposts-vpc-subnet-requirements.md)\.

**To create your cluster with the AWS Management Console**

   1. If you already have a local cluster IAM role, or you're going to create your cluster with `eksctl`, then you can skip this step\. By default, `eksctl` creates a role for you\.

      1. Run the following command to create an IAM trust policy JSON file\. 

         ```
         cat >eks-local-cluster-role-trust-policy.json <<EOF
         {
           "Version": "2012-10-17",
           "Statement": [
             {
               "Effect": "Allow",
               "Principal": {
                 "Service": "ec2.amazonaws.com"
               },
               "Action": "sts:AssumeRole"
             }
           ]
         }
         EOF
         ```

      1. Create the Amazon EKS cluster IAM role\. To create an IAM role, the [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) that is creating the role must be assigned the `iam:CreateRole` action \(permission\)\.

         ```
         aws iam create-role --role-name myAmazonEKSLocalClusterRole --assume-role-policy-document file://"eks-local-cluster-role-trust-policy.json"
         ```

      1. Attach the Amazon EKS managed policy named [https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSLocalOutpostClusterPolicy.html](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSLocalOutpostClusterPolicy.html) to the role\. To attach an IAM policy to an [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html), the principal that is attaching the policy must be assigned one of the following IAM actions \(permissions\): `iam:AttachUserPolicy` or `iam:AttachRolePolicy`\.

         ```
         aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonEKSLocalOutpostClusterPolicy --role-name myAmazonEKSLocalClusterRole
         ```

   1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

   1. At the top of the console screen, make sure that you have selected a [supported AWS Region](eks-outposts-local-cluster-overview.md#outposts-control-plane-supported-regions)\.

   1. Choose **Add cluster** and then choose **Create**\.

   1. On the **Configure cluster** page, enter or select values for the following fields:
      + **Kubernetes control plane location** – Choose AWS Outposts\.
      + **Outpost ID** – Choose the ID of the Outpost that you want to create your control plane on\.
      + **Instance type** – Select an instance type\. Only the instance types available in your Outpost are displayed\. In the dropdown list, each instance type describes how many nodes the instance type is recommended for\. Before choosing an instance type, see [Capacity considerations](eks-outposts-capacity-considerations.md)\. All replicas are deployed using the same instance type\. You can't change the instance type after your cluster is created\. Three control plane instances are deployed\. You can't change this number\.
      + **Name** – A name for your cluster\. It must be unique in your AWS account\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can't be longer than 100 characters\. The name must be unique within the AWS Region and AWS account that you're creating the cluster in\.
      + **Kubernetes version** – Choose the Kubernetes version that you want to use for your cluster\. We recommend selecting the latest version, unless you need to use an earlier version\.
      + **Cluster service role** – Choose the Amazon EKS cluster IAM role that you created in a previous step to allow the Kubernetes control plane to manage AWS resources\.
      + **Kubernetes cluster administrator access** – If you want the IAM principal \(role or user\) that's creating the cluster to have administrator access to the Kubernetes objects on the cluster, accept the default \(allow\)\. Amazon EKS creates an access entry for the IAM principal and grants cluster administrator permissions to the access entry\. For more information about access entries, see [Manage access entries](access-entries.md)\.

        If you want a different IAM principal than the principal creating the cluster to have administrator access to Kubernetes cluster objects, choose the disallow option\. After cluster creation, any IAM principal that has IAM permissions to create access entries can add an access entries for any IAM principals that need access to Kubernetes cluster objects\. For more information about the required IAM permissions, see [Actions defined by Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html#amazonelastickubernetesservice-actions-as-permissions) in the Service Authorization Reference\. If you choose the disallow option and don't create any access entries, then no IAM principals will have access to the Kubernetes objects on the cluster\. 
      + **Tags** – \(Optional\) Add any tags to your cluster\. For more information, see [Tagging your Amazon EKS resources](eks-using-tags.md)\.

      When you're done with this page, choose **Next**\.

   1. On the **Specify networking** page, select values for the following fields:
      + **VPC** – Choose an existing VPC\. The VPC must have a sufficient number of IP addresses available for the cluster, any nodes, and other Kubernetes resources that you want to create\. Your VPC must meet the requirements in [VPC requirements and considerations](eks-outposts-vpc-subnet-requirements.md#outposts-vpc-requirements)\.
      + **Subnets** – By default, all available subnets in the VPC specified in the previous field are preselected\. The subnets that you choose must meet the requirements in [Subnet requirements and considerations](eks-outposts-vpc-subnet-requirements.md#outposts-subnet-requirements)\.

        **Security groups** – \(Optional\) Specify one or more security groups that you want Amazon EKS to associate to the network interfaces that it creates\. Amazon EKS automatically creates a security group that enables communication between your cluster and your VPC\. Amazon EKS associates this security group, and any that you choose, to the network interfaces that it creates\. For more information about the cluster security group that Amazon EKS creates, see [Amazon EKS security group requirements and considerations](sec-group-reqs.md)\. You can modify the rules in the cluster security group that Amazon EKS creates\. If you choose to add your own security groups, you can't change the ones that you choose after cluster creation\. For on\-premises hosts to communicate with the cluster endpoint, you must allow inbound traffic from the cluster security group\. For clusters that don't have an ingress and egress internet connection \(also knows as private clusters\), you must do one of the following:
        + Add the security group associated with required VPC endpoints\. For more information about the required endpoints, see [interface VPC endpoints](eks-outposts-vpc-subnet-requirements.md#vpc-subnet-requirements-vpc-endpoints) in [Subnet access to AWS services](eks-outposts-vpc-subnet-requirements.md#subnet-access-to-services)\.
        + Modify the security group that Amazon EKS created to allow traffic from the security group associated with the VPC endpoints\. 

      When you're done with this page, choose **Next**\.

   1. On the **Configure observability** page, you can optionally choose which **Metrics** and **Control plane logging** options that you want to turn on\. By default, each log type is turned off\.
      + For more information on the Prometheus metrics option, see [Turn on Prometheus metrics when creating a cluster](prometheus.md#turn-on-prometheus-metrics)\.
      + For more information on the **Control plane logging** options, see [Amazon EKS control plane logging](control-plane-logs.md)\.

      When you're done with this page, choose **Next**\.

   1. On the **Review and create** page, review the information that you entered or selected on the previous pages\. If you need to make changes, choose **Edit**\. When you're satisfied, choose **Create**\. The **Status** field shows **CREATING** while the cluster is provisioned\.

      Cluster provisioning takes several minutes\.

------

1. After your cluster is created, you can view the Amazon EC2 control plane instances that were created\.

   ```
   aws ec2 describe-instances --query 'Reservations[*].Instances[*].{Name:Tags[?Key==`Name`]|[0].Value}' | grep my-cluster-control-plane
   ```

   An example output is as follows\.

   ```
   "Name": "my-cluster-control-plane-id1"
   "Name": "my-cluster-control-plane-id2"
   "Name": "my-cluster-control-plane-id3"
   ```

   Each instance is tainted with `node-role.eks-local.amazonaws.com/control-plane` so that no workloads are ever scheduled on the control plane instances\. For more information about taints, see [Taints and Tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/) in the Kubernetes documentation\. Amazon EKS continuously monitors the state of local clusters\. We perform automatic management actions, such as security patches and repairing unhealthy instances\. When local clusters are disconnected from the cloud, we complete actions to ensure that the cluster is repaired to a healthy state upon reconnect\.

1. If you created your cluster using `eksctl`, then you can skip this step\. `eksctl` completes this step for you\. Enable `kubectl` to communicate with your cluster by adding a new context to the `kubectl` `config` file\. For instructions on how to create and update the file, see [Creating or updating a `kubeconfig` file for an Amazon EKS cluster](create-kubeconfig.md)\.

   ```
   aws eks update-kubeconfig --region region-code --name my-cluster
   ```

   An example output is as follows\.

   ```
   Added new context arn:aws:eks:region-code:111122223333:cluster/my-cluster to /home/username/.kube/config
   ```

1. To connect to your local cluster's Kubernetes API server, have access to the local gateway for the subnet, or connect from within the VPC\. For more information about connecting an Outpost rack to your on\-premises network, see [How local gateways for racks work](https://docs.aws.amazon.com/outposts/latest/userguide/how-racks-work.html) in the AWS Outposts User Guide\. If you use Direct VPC Routing and the Outpost subnet has a route to your local gateway, the private IP addresses of the Kubernetes control plane instances are automatically broadcasted over your local network\. The local cluster's Kubernetes API server endpoint is hosted in Amazon Route 53 \(Route 53\)\. The API service endpoint can be resolved by public DNS servers to the Kubernetes API servers' private IP addresses\. 

   Local clusters' Kubernetes control plane instances are configured with static elastic network interfaces with fixed private IP addresses that don't change throughout the cluster lifecycle\. Machines that interact with the Kubernetes API server might not have connectivity to Route 53 during network disconnects\. If this is the case, we recommend configuring `/etc/hosts` with the static private IP addresses for continued operations\. We also recommend setting up local DNS servers and connecting them to your Outpost\. For more information, see the [AWS Outposts documentation](https://docs.aws.amazon.com/outposts/latest/userguide/how-outposts-works.html#dns)\. Run the following command to confirm that communication's established with your cluster\.

   ```
   kubectl get svc
   ```

   An example output is as follows\.

   ```
   NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
   kubernetes   ClusterIP   10.100.0.1   <none>        443/TCP   28h
   ```

1. \(Optional\) Test authentication to your local cluster when it's in a disconnected state from the AWS Cloud\. For instructions, see [Preparing for network disconnects](eks-outposts-network-disconnects.md)\.

## Internal resources<a name="outposts-control-plan-internal-resources"></a>

Amazon EKS creates the following resources on your cluster\. The resources are for Amazon EKS internal use\. For proper functioning of your cluster, don't edit or modify these resources\.
+ The following [mirror Pods](https://kubernetes.io/docs/reference/glossary/?all=true#term-mirror-pod):
  + `aws-iam-authenticator-node-hostname`
  + `eks-certificates-controller-node-hostname`
  + `etcd-node-hostname`
  + `kube-apiserver-node-hostname`
  + `kube-controller-manager-node-hostname`
  + `kube-scheduler-node-hostname`
+ The following self\-managed add\-ons:
  + `kube-system/coredns`
  + `kube-system/``kube-proxy` \(not created until you add your first node\)
  + `kube-system/aws-node` \(not created until you add your first node\)\. Local clusters use the Amazon VPC CNI plugin for Kubernetes plugin for cluster networking\. Do not change the configuration for control plane instances \(Pods named `aws-node-controlplane-*`\)\. There are configuration variables that you can use to change the default value for when the plugin creates new network interfaces\. For more information, see the [documentation](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/README.md) on GitHub\.
+ The following services:
  + `default/kubernetes`
  + `kube-system/kube-dns`
+ A `PodSecurityPolicy` named `eks.system`
+ A `ClusterRole` named `eks:system:podsecuritypolicy`
+ A `ClusterRoleBinding` named `eks:system`
+ A default [PodSecurityPolicy](pod-security-policy.md#default-psp)
+ In addition to the [cluster security group](sec-group-reqs.md), Amazon EKS creates a security group in your AWS account that's named `eks-local-internal-do-not-use-or-edit-cluster-name-uniqueid`\. This security group allows traffic to flow freely between Kubernetes components running on the control plane instances\.

Recommended next steps:
+ [Grant the IAM principal that created the cluster the required permissions to view Kubernetes resources in the AWS Management Console](view-kubernetes-resources.md#view-kubernetes-resources-permissions)
+ [Grant IAM entities access to your cluster](grant-k8s-access.md)\. If you want the entities to view Kubernetes resources in the Amazon EKS console, grant the [Required permissions](view-kubernetes-resources.md#view-kubernetes-resources-permissions) to the entities\.
+ [Configure logging for your cluster](control-plane-logs.md)
+ Familiarize yourself with what happens during [network disconnects](eks-outposts-network-disconnects.md)\.
+ [Add nodes to your cluster](eks-outposts-self-managed-nodes.md)
+ Consider setting up a backup plan for your `etcd`\. Amazon EKS doesn't support automated backup and restore of `etcd` for local clusters\. For more information, see [Backing up an `etcd` cluster](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#backing-up-an-etcd-cluster) in the Kubernetes documentation\. The two main options are using `etcdctl` to automate taking snapshots or using Amazon EBS storage volume backup\.