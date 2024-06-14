--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Creating a local cluster on an Outpost<a name="eks-outposts-local-cluster-create"></a>

This topic provides an overview of what to consider when running a local cluster on an Outpost\. The topic also provides instructions for how to deploy a local cluster on an Outpost\.

IMPORTANT: ** These considerations aren’t replicated in related Amazon EKS documentation\. If other Amazon EKS documentation topics conflict with the considerations here, follow the considerations here\. ** These considerations are subject to change and might change frequently\. So, we recommend that you regularly review this topic\. \*\* Many of the considerations are different than the considerations for creating a cluster on the AWS Cloud\.

\+
+ Local clusters support Outpost racks only\. A single local cluster can run across multiple physical Outpost racks that comprise a single logical Outpost\. A single local cluster can’t run across multiple logical Outposts\. Each logical Outpost has a single Outpost ARN\.
+ Local clusters run and manage the Kubernetes control plane in your account on the Outpost\. You can’t run workloads on the Kubernetes control plane instances or modify the Kubernetes control plane components\. These nodes are managed by the Amazon EKS service\. Changes to the Kubernetes control plane don’t persist through automatic Amazon EKS management actions, such as patching\.
+ Local clusters require the use of Amazon EBS on Outposts\. Your Outpost must have Amazon EBS available for the Kubernetes control plane storage\.
+ Local clusters use Amazon EBS on Outposts\. Your Outpost must have Amazon EBS available for the Kubernetes control plane storage\. Outposts support Amazon EBS `gp2` volumes only\.
+ Amazon EBS backed Kubernetes `PersistentVolumes` are supported using the Amazon EBS CSI driver\.
+ An existing Outpost\. For more information, see [What is AWS Outposts](https://docs.aws.amazon.com/outposts/latest/userguide/what-is-outposts.html)\.
+ Version `2.12.3` or later or version `1.27.160` or later of the AWS Command Line Interface \(AWS CLI\) installed and configured on your device or AWS CloudShell\. To check your current version, use ` `aws --version | cut -d / -f2 | cut -d ' ' -f1 are often several versions behind the latest version of the AWS CLI. To install the latest version, see [Installing](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with aws configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the AWS Command Line Interface User Guide. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version. To update it, see [Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the AWS CloudShell User Guide.` 

When a local Amazon EKS cluster is created, the [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) that creates the cluster is permanently added\. The principal is specifically added to the Kubernetes RBAC authorization table as the administrator\. This entity has `system:masters` permissions\. The identity of this entity isn’t visible in your cluster configuration\. So, it’s important to note the entity that created the cluster and make sure that you never delete it\. Initially, only the principal that created the server can make calls to the Kubernetes API server using `kubectl`\. If you use the console to create the cluster, make sure that the same IAM credentials are in the AWS SDK credential chain when you run `kubectl` commands on your cluster\. After your cluster is created, you can grant other IAM principals access to your cluster\.

You can create a local cluster with `eksctl`, the AWS Management Console, the [AWS CLI](https://docs.aws.amazon.com/cli/latest/reference/eks/create-cluster.html), the [Amazon EKS API](https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html), the [AWS SDKs](https://aws.amazon.com/developer/tools/), [https://docs\.aws\.amazon\.com/](https://docs.aws.amazon.com/) AWSCloudFormation/latest/UserGuide/aws\-properties\-eks\-cluster\-outpostconfig\.html\[AWS CloudFormation\] or [Terraform](https://registry.terraform.io/modules/terraform-aws-modules/eks/aws/latest)\.

1. Create a local cluster\.  
eksctl  
\*\* \.Prerequisite Version `0.177.0` or later of the `eksctl` command line tool installed on your device or AWS CloudShell\. To install or update `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.  

   1. Copy the contents that follow to your device\. Replace the following values and then run the modified command to create the `outpost-control-plane.yaml` file:
      + Replace ` my-cluster ` with a name for your cluster\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can’t be longer than 100 characters\. The name must be unique within the AWS Region and AWS account that you’re creating the cluster in\.
      + Replace ` uniqueid ` with the ID of your Outpost\.

        ```
        //⁂cat >outpost-control-plane.yaml <<EOF
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
      [✓]  EKS cluster "`my-cluster`" in "`region-code`" region is ready
      ```
**Tip**  
To see the most options that you can specify when creating a cluster with `eksctl`, use the `eksctl create cluster --help` command\. To see all the available options, you can use a `config` file\. For more information, see [Using config files](https://eksctl.io/usage/creating-and-managing-clusters/#using-config-files) and the [config file schema](https://eksctl.io/usage/schema/) in the `eksctl` documentation\. You can find [config file examples](https://github.com/weaveworks/eksctl/tree/master/examples) on GitHub\.

 AWS Management Console  
\*\* \.Prerequisite  

1. If you already have a local cluster IAM role, or you’re going to create your cluster with `eksctl`, then you can skip this step\. By default, `eksctl` creates a role for you\.

   1. Run the following command to create an IAM trust policy JSON file\.

      ```
      //⁂cat >eks-local-cluster-role-trust-policy.json <<EOF
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
      //⁂aws iam create-role --role-name myAmazonEKSLocalClusterRole --assume-role-policy-document file://"eks-local-cluster-role-trust-policy.json"
      ```

   1. Attach the Amazon EKS managed policy named [AmazonEKSLocalOutpostClusterPolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSLocalOutpostClusterPolicy.html) to the role\. To attach an IAM policy to an [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html), the principal that is attaching the policy must be assigned one of the following IAM actions \(permissions\): `iam:AttachUserPolicy` or `iam:AttachRolePolicy`\.

      ```
      aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonEKSLocalOutpostClusterPolicy --role-name myAmazonEKSLocalClusterRole
      ```

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose **Add cluster** and then choose **Create**\.

1. On the **Configure cluster** page, enter or select values for the following fields:
   +  ** Kubernetes control plane location** – Choose AWS Outposts\.
   +  **Outpost ID** – Choose the ID of the Outpost that you want to create your control plane on\.
   +  **Name** – A name for your cluster\. It must be unique in your AWS account\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can’t be longer than 100 characters\. The name must be unique within the AWS Region and AWS account that you’re creating the cluster in\.
   +  ** Kubernetes version** – Choose the Kubernetes version that you want to use for your cluster\. We recommend selecting the latest version, unless you need to use an earlier version\.
   +  **Cluster service role** – Choose the Amazon EKS cluster IAM role that you created in a previous step to allow the Kubernetes control plane to manage AWS resources\.

     If you want a different IAM principal than the principal creating the cluster to have administrator access to Kubernetes cluster objects, choose the disallow option\. After cluster creation, any IAM principal that has IAM permissions to create access entries can add an access entries for any IAM principals that need access to Kubernetes cluster objects\. For more information about the required IAM permissions, see [Actions defined by Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html#amazonelastickubernetesservice-actions-as-permissions) in the Service Authorization Reference\. If you choose the disallow option and don’t create any access entries, then no IAM principals will have access to the Kubernetes objects on the cluster\.

   When you’re done with this page, choose **Next**\.

1. On the **Specify networking** page, select values for the following fields:
   + Modify the security group that Amazon EKS created to allow traffic from the security group associated with the VPC endpoints\.

   When you’re done with this page, choose **Next**\.

1. On the **Configure observability** page, you can optionally choose which **Metrics** and **Control plane logging** options that you want to turn on\. By default, each log type is turned off\.
When you’re done with this page, choose **Next**\.  

1. On the **Review and create** page, review the information that you entered or selected on the previous pages\. If you need to make changes, choose **Edit**\. When you’re satisfied, choose **Create**\. The **Status** field shows **CREATING** while the cluster is provisioned\.

   Cluster provisioning takes several minutes\. \. After your cluster is created, you can view the Amazon EC2 control plane instances that were created\.

   \+

   ```
   aws ec2 describe-instances --query 'Reservations[*].Instances[*].{Name:Tags[?Key==`Name`]|[0].Value}' | grep my-cluster-control-plane
   ```

   \+

   An example output is as follows\.

   \+

   ```
   "Name": "`my-cluster`-control-plane-`id1`"
   "Name": "`my-cluster`-control-plane-`id2`"
   "Name": "`my-cluster`-control-plane-`id3`"
   ```

   \+

   Each instance is tainted with `node-role.eks-local.amazonaws.com/control-plane` so that no workloads are ever scheduled on the control plane instances\. For more information about taints, see [Taints and Tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/) in the Kubernetes documentation\. Amazon EKS continuously monitors the state of local clusters\. We perform automatic management actions, such as security patches and repairing unhealthy instances\. When local clusters are disconnected from the cloud, we complete actions to ensure that the cluster is repaired to a healthy state upon reconnect\.

   \+

   ```
   aws eks update-kubeconfig --region region-code --name my-cluster
   ```

   \+

   An example output is as follows\.

   \+

   ```
   Added new context arn:aws:eks::`111122223333`:cluster/`my-cluster`to`/home/username/`.kube/config
   ```

   1. To connect to your local cluster’s Kubernetes API server, have access to the local gateway for the subnet, or connect from within the VPC\. For more information about connecting an Outpost rack to your on\-premises network, see [How local gateways for racks work](https://docs.aws.amazon.com/outposts/latest/userguide/how-racks-work.html) in the AWS Outposts User Guide\. If you use Direct VPC Routing and the Outpost subnet has a route to your local gateway, the private IP addresses of the Kubernetes control plane instances are automatically broadcasted over your local network\. The local cluster’s Kubernetes API server endpoint is hosted in Amazon Route 53 \(Route 53\)\. The API service endpoint can be resolved by public DNS servers to the Kubernetes API servers' private IP addresses\.

      Local clusters' Kubernetes control plane instances are configured with static elastic network interfaces with fixed private IP addresses that don’t change throughout the cluster lifecycle\. Machines that interact with the Kubernetes API server might not have connectivity to Route 53 during network disconnects\. If this is the case, we recommend configuring `/etc/hosts` with the static private IP addresses for continued operations\. We also recommend setting up local DNS servers and connecting them to your Outpost\. For more information, see the [AWS Outposts documentation](https://docs.aws.amazon.com/outposts/latest/userguide/how-outposts-works.html#dns)\. Run the following command to confirm that communication’s established with your cluster\.

      ```
      kubectl get svc
      ```

      An example output is as follows\.

      ```
      NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
      kubernetes   ClusterIP   10.100.0.1   <none>        443/TCP   28h
      ```

## Internal resources<a name="outposts-control-plan-internal-resources"></a>

Amazon EKS creates the following resources on your cluster\. The resources are for Amazon EKS internal use\. For proper functioning of your cluster, don’t edit or modify these resources\.
+ The following [mirror Pods](https://kubernetes.io/docs/reference/glossary/?all=true#term-mirror-pod):
  +  `aws-iam-authenticator-node-hostname ` 
  +  `eks-certificates-controller-node-hostname ` 
  +  `etcd-node-hostname ` 
  +  `kube-apiserver-node-hostname ` 
  +  `kube-controller-manager-node-hostname ` 
  +  `kube-scheduler-node-hostname ` 
+ The following self\-managed add\-ons:
  +  `kube-system/coredns` 
  +  `kube-system/` `kube-proxy` \(not created until you add your first node\)
  +  `kube-system/aws-node` \(not created until you add your first node\)\. Local clusters use the Amazon VPC CNI plugin for  Kubernetes plugin for cluster networking\. Do not change the configuration for control plane instances \(Pods named `aws-node-controlplane-*`\)\. There are configuration variables that you can use to change the default value for when the plugin creates new network interfaces\. For more information, see the [documentation](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/README.md) on GitHub\.
+ The following services:
  +  `default/kubernetes` 
  +  `kube-system/kube-dns` 
+ A `PodSecurityPolicy` named `eks.system` 
+ A `ClusterRole` named `eks:system:podsecuritypolicy` 
+ A `ClusterRoleBinding` named `eks:system` 

Recommended next steps:
+ Consider setting up a backup plan for your `etcd`\. Amazon EKS doesn’t support automated backup and restore of `etcd` for local clusters\. For more information, see [Backing up an etcd cluster](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#backing-up-an-etcd-cluster) in the Kubernetes documentation\. The two main options are using `etcdctl` to automate taking snapshots or using Amazon EBS storage volume backup\.