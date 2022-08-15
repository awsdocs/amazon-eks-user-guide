# Creating an Amazon EKS cluster<a name="create-cluster"></a>

This topic provides an overview of the available options and describes what to consider when you create an Amazon EKS cluster\. If this is your first time creating an Amazon EKS cluster, we recommend that you follow one of our [Getting started with Amazon EKS](getting-started.md) guides\. These guides help you to create a simple, default cluster without expanding into all of the available options\.

**Prerequisites**
+ An existing VPC and subnets that meet [Amazon EKS requirements](network_reqs.md)\. Before you deploy a cluster for production use, we recommend that you have a thorough understanding of the VPC and subnet requirements\. If you don't have a VPC and subnets, you can create them using an [Amazon EKS provided AWS CloudFormation template](creating-a-vpc.md)\.
+ The `kubectl` command line tool is installed on your computer or AWS CloudShell\. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster\. For example, if your cluster version is `1.22`, you can use `kubectl` version `1.21`,`1.22`, or `1.23` with it\. To install or upgrade `kubectl`, see [Installing or updating `kubectl`](install-kubectl.md)\.
+ Version `2.7.21` or later or `1.25.46` or later of the AWS CLI installed and configured on your computer or AWS CloudShell\. For more information, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with `aws configure`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the AWS Command Line Interface User Guide\.
+ An IAM user or role with permissions to `create` and `describe` an Amazon EKS cluster\. For more information, see [Create a Kubernetes cluster](security_iam_id-based-policy-examples.md#policy-create-cluster) and [List or describe all clusters](security_iam_id-based-policy-examples.md#policy_example2)\.

When an Amazon EKS cluster is created, the IAM entity \(user or role\) that creates the cluster is permanently added to the Kubernetes RBAC authorization table as the administrator\. This entity has `system:masters` permissions\. The identity of this entity isn't visible in your cluster configuration\. So, it's important to note the entity that created the cluster and make sure that you never delete it\. Initially, only the IAM entity that created the server can make calls to the Kubernetes API server using `kubectl`\. If you use the console to create the cluster, you must ensure that the same IAM credentials are in the AWS SDK credential chain when you run `kubectl` commands on your cluster\. After your cluster is created, you can grant other IAM entities access to your cluster\.

**To create an Amazon EKS cluster**

1. If you already have a cluster IAM role, or you're going to create your cluster with `eksctl`, then you can skip this step\. By default, `eksctl` creates a role for you\.<a name="create-cluster-iam-role-cli"></a>

**To create an Amazon EKS cluster IAM role**

   1. Run the following command to create an IAM trust policy JSON file\. 

      ```
      cat >eks-cluster-role-trust-policy.json <<EOF
      {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect": "Allow",
            "Principal": {
              "Service": "eks.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
          }
        ]
      }
      EOF
      ```

   1. Create the Amazon EKS cluster IAM role\. If necessary, preface *eks\-cluster\-role\-trust\-policy\.json* with the path on your computer that you wrote the file to in the previous step\. The command associates the trust policy that you created in the previous step to the role\. To create an IAM role, the IAM entity \(user or role\) that is creating the role must be assigned the following IAM action \(permission\): `iam:CreateRole`\.

      ```
      aws iam create-role --role-name myAmazonEKSClusterRole --assume-role-policy-document file://"eks-cluster-role-trust-policy.json"
      ```

   1. Attach the Amazon EKS managed policy named [https://console.aws.amazon.com/arn:aws:iam::aws:policy/AmazonEKSClusterPolicy](https://console.aws.amazon.com/arn:aws:iam::aws:policy/AmazonEKSClusterPolicy) to the role\. To attach an IAM policy to an IAM entity \(user or role\), the IAM entity that is attaching the policy must be assigned one of the following IAM actions \(permissions\): `iam:AttachUserPolicy` or `iam:AttachRolePolicy`\.

      ```
      aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy --role-name myAmazonEKSClusterRole
      ```

1. Create an Amazon EKS cluster\. 

    You can create a cluster by using `eksctl`, the AWS Management Console, or the AWS CLI\.

------
#### [ eksctl ]

**Prerequisite**  
Version `0.108.0` or later of the `eksctl` command line tool installed on your computer or AWS CloudShell\. To install or update `eksctl`, see [Installing or updating `eksctl`](eksctl.md)\.

**To create your cluster**  
Create an Amazon EKS `IPv4` cluster with the Amazon EKS latest Kubernetes version in your default AWS Region\. Before running command, make the following replacements:
   + Replace `region-code` with the AWS Region that you want to create your cluster in\.
   + Replace `my-cluster` with a name for your cluster\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can't be longer than 100 characters\. The name must be unique within the AWS Region and AWS account that you're creating the cluster in\.
   + Replace *1\.23* with any [Amazon EKS supported version](kubernetes-versions.md)\. To deploy a 1\.23 cluster with `eksctl`, you need to use `eksctl` version `0.109.0-rc.0` or later\. To install this version, follow the instructions for your operating system in [Installing or updating `eksctl`](eksctl.md)\. You need to use the instructions in the note for the last step, replacing the version in the note with this version\.
   + Change the values for `vpc-private-subnets` to meet your requirements\. You can also add additional IDs\. You must specify at least two subnet IDs\. If you'd rather specify public subnets, you can change `--vpc-private-subnets` to `--vpc-public-subnets`\. Public subnets have an associated route table with a route to an internet gateway, but private subnets don't have an associated route table\. We recommend using private subnets whenever possible\.

     The subnets that you choose must meet the [Amazon EKS subnet requirements](network_reqs.md#network-requirements-subnets)\. Before selecting subnets, we recommend that you're familiar with all of the [Amazon EKS VPC and subnet requirements and considerations](network_reqs.md)\. You can't change which subnets you want to use after cluster creation\. 

   ```
   eksctl create cluster --name my-cluster --region region-code --version 1.23 --vpc-private-subnets subnet-ExampleID1,subnet-ExampleID2 --without-nodegroup
   ```

   Cluster provisioning takes several minutes\. While the cluster is being created, several lines of output appear\. The last line of output is similar to the following example line\.

   ```
   [✓]  EKS cluster "my-cluster" in "region-code" region is ready
   ```

**Tip**  
To see the most options that you can specify when creating a cluster with `eksctl`, use the **eksctl create cluster \-\-help** command\. To see all the available options, you can use a `config` file\. For more information, see [Using config files](https://eksctl.io/usage/creating-and-managing-clusters/#using-config-files) and the [config file schema](https://eksctl.io/usage/schema/) in the `eksctl` documentation\. You can find [config file examples](https://github.com/weaveworks/eksctl/tree/master/examples) on GitHub\.

**Optional settings**

   The following are optional settings that, if required, must be added to the previous command\. You can only enable these options when you create the cluster, not after\. If you need to specify these options, you must create the cluster with an [`eksctl` config file](https://eksctl.io/usage/creating-and-managing-clusters/#using-config-files) and specify the settings, rather than using the previous command\. 
   + If you want to specify one or more security groups that Amazon EKS assigns to the network interfaces that it creates, specify the [https://eksctl.io/usage/schema/#vpc-securityGroup](https://eksctl.io/usage/schema/#vpc-securityGroup) option\.

     Whether you choose any security groups or not, Amazon EKS creates a security group that enables communication between your cluster and your VPC\. Amazon EKS associates this security group, and any that you choose, to the network interfaces that it creates\. For more information about the cluster security group that Amazon EKS creates, see [Amazon EKS security group requirements and considerations](sec-group-reqs.md)\. You can modify the rules in the cluster security group that Amazon EKS creates\. If you choose to add your own security groups, you can't change the ones that you choose after cluster creation\.
   + If you want to specify which `IPv4` Classless Inter\-domain Routing \(CIDR\) block Kubernetes assigns service IP addresses from, specify the [https://eksctl.io/usage/schema/#kubernetesNetworkConfig-serviceIPv4CIDR](https://eksctl.io/usage/schema/#kubernetesNetworkConfig-serviceIPv4CIDR) option\. 

     Specifying your own range can help prevent conflicts between Kubernetes services and other networks peered or connected to your VPC\. Enter a range in CIDR notation\. For example: `10.2.0.0/16`\.

     The CIDR block must meet the following requirements:
     + Be within one of the following ranges: `10.0.0.0/8`, `172.16.0.0/12`, or `192.168.0.0/16`\.
     + Have a minimum size of `/24` and a maximum size of `/12`\.
     + Not overlap with the range of the VPC for your Amazon EKS resources\.

     You can only specify this option when using the `IPv4` address family and only at cluster creation\. If you don't specify this, then Kubernetes assigns service IP addresses from either the `10.100.0.0/16` or `172.20.0.0/16` CIDR blocks\.
   + If you're creating cluster that's version `1.21` or later and want the cluster to assign `IPv6` addresses to pods and services instead of `IPv4` addresses, specify the [https://eksctl.io/usage/schema/#kubernetesNetworkConfig-ipFamily](https://eksctl.io/usage/schema/#kubernetesNetworkConfig-ipFamily) option\.

     Kubernetes assigns `IPv4` addresses to pods and services, by default\. Before deciding to use the `IPv6` family, make sure that you're familiar with all of the considerations and requirements in the [VPC requirements and considerations](network_reqs.md#network-requirements-vpc), [Subnet requirements and considerations](network_reqs.md#network-requirements-subnets), [Amazon EKS security group requirements and considerations](sec-group-reqs.md), and [Tutorial: Assigning `IPv6` addresses to pods and services](cni-ipv6.md) topics\. If you choose the `IPv6` family, you can't specify an address range for Kubernetes to assign `IPv6` service addresses from like you can for the `IPv4` family\. Kubernetes assigns service addresses from the unique local address range \(`fc00::/7`\)\.

------
#### [ AWS Management Console ]

**To create your cluster**

   1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

   1. Choose **Add cluster** and then choose **Create**\.

   1. On the **Configure cluster** page, enter the following fields:
      + **Name** – A name for your cluster\. It must be unique in your AWS account\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can't be longer than 100 characters\. The name must be unique within the AWS Region and AWS account that you're creating the cluster in\.
      + **Kubernetes version** – The version of Kubernetes to use for your cluster\. 
      + **Cluster service role** – Choose the Amazon EKS cluster IAM role that you created to allow the Kubernetes control plane to manage AWS resources on your behalf\.
      + **Secrets encryption** – \(Optional\) Choose to enable secrets encryption of Kubernetes secrets using a KMS key\. You can also enable this after you create your cluster\. Before you enable this capability, make sure that you're familiar with the information in [Enabling secret encryption on an existing cluster](enable-kms.md)\.
      + **Tags** – \(Optional\) Add any tags to your cluster\. For more information, see [Tagging your Amazon EKS resources](eks-using-tags.md)\.

   1. Select **Next**\.

   1. On the **Specify networking** page, select values for the following fields:
      + **VPC** – Choose an existing VPC that meets [Amazon EKS VPC requirements](network_reqs.md#network-requirements-vpc) to create your cluster in\. Before choosing a VPC, we recommend that you're familiar with all of the requirements and considerations in [Amazon EKS VPC and subnet requirements and considerations](network_reqs.md)\. You can't change which VPC you want to use after cluster creation\. If no VPCs are listed, then you need to create one first\. For more information, see [Creating a VPC for your Amazon EKS cluster](creating-a-vpc.md)\.
      + **Subnets** – By default, all available subnets in the VPC specified in the previous field are preselected\. You must select at least two\.

        The subnets that you choose must meet the [Amazon EKS subnet requirements](network_reqs.md#network-requirements-subnets)\. Before selecting subnets, we recommend that you're familiar with all of the [Amazon EKS VPC and subnet requirements and considerations](network_reqs.md)\. You can't change which subnets you want to use after cluster creation\. 

        **Security groups** – \(Optional\) Specify one or more security groups that you want Amazon EKS to associate to the network interfaces that it creates\.

        Whether you choose any security groups or not, Amazon EKS creates a security group that enables communication between your cluster and your VPC\. Amazon EKS associates this security group, and any that you choose, to the network interfaces that it creates\. For more information about the cluster security group that Amazon EKS creates, see [Amazon EKS security group requirements and considerations](sec-group-reqs.md)\. You can modify the rules in the cluster security group that Amazon EKS creates\. If you choose to add your own security groups, you can't change the ones that you choose after cluster creation\.
      + **Choose cluster IP address family** – If the version you chose for your cluster is `1.20` or earlier, only the **IPv4** option is available\. If you chose `1.21` or later, then **IPv4** and **IPv6** are available\.

        Kubernetes assigns `IPv4` addresses to pods and services, by default\. Before deciding to use the `IPv6` family, make sure that you're familiar with all of the considerations and requirements in the [VPC requirements and considerations](network_reqs.md#network-requirements-vpc), [Subnet requirements and considerations](network_reqs.md#network-requirements-subnets), [Amazon EKS security group requirements and considerations](sec-group-reqs.md), and [Tutorial: Assigning `IPv6` addresses to pods and services](cni-ipv6.md) topics\. If you choose the `IPv6` family, you can't specify an address range for Kubernetes to assign `IPv6` service addresses from like you can for the `IPv4` family\. Kubernetes assigns service addresses from the unique local address range \(`fc00::/7`\)\.
      + \(Optional\) Choose **Configure Kubernetes Service IP address range** and specify a **Service `IPv4` range**\.

        Specifying your own range can help prevent conflicts between Kubernetes services and other networks peered or connected to your VPC\. Enter a range in CIDR notation\. For example: `10.2.0.0/16`\.

        The CIDR block must meet the following requirements:
        + Be within one of the following ranges: `10.0.0.0/8`, `172.16.0.0/12`, or `192.168.0.0/16`\.
        + Have a minimum size of `/24` and a maximum size of `/12`\.
        + Not overlap with the range of the VPC for your Amazon EKS resources\.

        You can only specify this option when using the `IPv4` address family and only at cluster creation\. If you don't specify this, then Kubernetes assigns service IP addresses from either the `10.100.0.0/16` or `172.20.0.0/16` CIDR blocks\.
      + For **Cluster endpoint access**, select an option\. After your cluster is created, you can change this option\. Before selecting a non\-default option, make sure to familiarize yourself with the options and their implications\. For more information, see [Amazon EKS cluster endpoint access control](cluster-endpoint.md)\.

   1. You can accept the defaults in the **Networking add\-ons** section to install the default version of the [Amazon VPC CNI plugin for Kubernetes](pod-networking.md), [CoreDNS](managing-coredns.md), and [`kube-proxy`](managing-kube-proxy.md) Amazon EKS add\-ons\. Or, alternatively, you can select a different version\. If you don't require the functionality of any of the add\-ons, you can remove them once your cluster is created\. If you need to manage Amazon EKS managed settings for any of these add\-ons yourself, remove Amazon EKS management of the add\-on after your cluster is created\. For more information, see [Amazon EKS add\-ons](eks-add-ons.md)\.

   1. Select **Next**\.

   1. On the **Configure logging** page, you can optionally choose which log types that you want to enable\. By default, each log type is **Disabled**\. Before selecting a different option, familiarize yourself with the information in [Amazon EKS control plane logging](control-plane-logs.md)\. After you create the cluster, you can change this option\.

   1. Select **Next**\.

   1. On the **Review and create** page, review the information that you entered or selected on the previous pages\. If you need to make changes, choose **Edit**\. When you're satisfied, choose **Create**\. The **Status** field shows **CREATING** while the cluster is provisioned\.
**Note**  
You might receive an error that one of the Availability Zones in your request doesn't have sufficient capacity to create an Amazon EKS cluster\. If this happens, the error output contains the Availability Zones that can support a new cluster\. Retry creating your cluster with at least two subnets that are located in the supported Availability Zones for your account\. For more information, see [Insufficient capacity](troubleshooting.md#ICE)\.

      Cluster provisioning takes several minutes\.

------
#### [ AWS CLI ]

**To create your cluster**

   1. Create your cluster with the command that follows\. Before running the command, make the following replacements:
      + Replace `region-code` with the AWS Region that you want to create your cluster in\.
      + Replace `my-cluster` with a name for your cluster\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can't be longer than 100 characters\. The name must be unique within the AWS Region and AWS account that you're creating the cluster in\.
      + Replace `1.23` with any [Amazon EKS supported version](kubernetes-versions.md)\. 
      + Replace `111122223333` with your account ID and `myAmazonEKSClusterRole` with the name of your cluster IAM role\.
      + Replace the values for `subnetIds` with your own\. You can also add additional IDs\. You must specify at least two subnet IDs\.

        The subnets that you choose must meet the [Amazon EKS subnet requirements](network_reqs.md#network-requirements-subnets)\. Before selecting subnets, we recommend that you're familiar with all of the [Amazon EKS VPC and subnet requirements and considerations](network_reqs.md)\. You can't change which subnets you want to use after cluster creation\. 
      + If you don't want to specify a security group ID, remove `,securityGroupIds=sg-ExampleID1` from the command\. If you want to specify one or more security group IDs, replace the values for `securityGroupIds` with your own\. You can also add additional IDs\.

        Whether you choose any security groups or not, Amazon EKS creates a security group that enables communication between your cluster and your VPC\. Amazon EKS associates this security group, and any that you choose, to the network interfaces that it creates\. For more information about the cluster security group that Amazon EKS creates, see [Amazon EKS security group requirements and considerations](sec-group-reqs.md)\. You can modify the rules in the cluster security group that Amazon EKS creates\. If you choose to add your own security groups, you can't change the ones that you choose after cluster creation\.

      ```
      aws eks create-cluster --region region-code --name my-cluster --kubernetes-version 1.23 \
         --role-arn arn:aws:iam::111122223333:role/myAmazonEKSClusterRole \
         --resources-vpc-config subnetIds=subnet-ExampleID1,subnet-ExampleID2,securityGroupIds=sg-ExampleID1
      ```
**Note**  
You might receive an error that one of the Availability Zones in your request doesn't have sufficient capacity to create an Amazon EKS cluster\. If this happens, the error output contains the Availability Zones that can support a new cluster\. Retry creating your cluster with at least two subnets that are located in the supported Availability Zones for your account\. For more information, see [Insufficient capacity](troubleshooting.md#ICE)\.

**Optional settings**

      The following are optional settings that, if required, must be added to the previous command\. You can only enable these options when you create the cluster, not after\.
      + If you want to specify which `IPv4` Classless Inter\-domain Routing \(CIDR\) block Kubernetes assigns service IP addresses from, you must specify it by adding the **`--kubernetes-network-config serviceIpv4Cidr=CIDR block`** to the following command\.

        Specifying your own range can help prevent conflicts between Kubernetes services and other networks peered or connected to your VPC\. Enter a range in CIDR notation\. For example: `10.2.0.0/16`\.

        The CIDR block must meet the following requirements:
        + Be within one of the following ranges: `10.0.0.0/8`, `172.16.0.0/12`, or `192.168.0.0/16`\.
        + Have a minimum size of `/24` and a maximum size of `/12`\.
        + Not overlap with the range of the VPC for your Amazon EKS resources\.

        You can only specify this option when using the `IPv4` address family and only at cluster creation\. If you don't specify this, then Kubernetes assigns service IP addresses from either the `10.100.0.0/16` or `172.20.0.0/16` CIDR blocks\.
      + If you're creating a cluster of version `1.21` or later and want the cluster to assign `IPv6` addresses to pods and services instead of `IPv4` addresses, add **`--kubernetes-network-config ipFamily=ipv6`** to the following command\.

        Kubernetes assigns `IPv4` addresses to pods and services, by default\. Before deciding to use the `IPv6` family, make sure that you're familiar with all of the considerations and requirements in the [VPC requirements and considerations](network_reqs.md#network-requirements-vpc), [Subnet requirements and considerations](network_reqs.md#network-requirements-subnets), [Amazon EKS security group requirements and considerations](sec-group-reqs.md), and [Tutorial: Assigning `IPv6` addresses to pods and services](cni-ipv6.md) topics\. If you choose the `IPv6` family, you can't specify an address range for Kubernetes to assign `IPv6` service addresses from like you can for the `IPv4` family\. Kubernetes assigns service addresses from the unique local address range \(`fc00::/7`\)\.

   1. It takes several minutes to provision the cluster\. You can query the status of your cluster with the following command\. 

      ```
      aws eks describe-cluster \
          --region region-code \
          --name my-cluster \
          --query "cluster.status"
      ```

      Don't proceed to the next step until the output returned is `ACTIVE`\.

------

1. If you created your cluster using `eksctl`, then you can skip this step\. This is because `eksctl` already completed this step for you\. Enable `kubectl` to communicate with your cluster by adding a new context to the `kubectl` `config` file\. For more information about how to create and update the file, see [Create a `kubeconfig` for Amazon EKS](create-kubeconfig.md)\.

   ```
   aws eks update-kubeconfig --region region-code --name my-cluster
   ```

   The example output is as follows\.

   ```
   Added new context arn:aws:eks:region-code:111122223333:cluster/my-cluster to /home/username/.kube/config
   ```

1. Confirm communication with your cluster by running the following command\.

   ```
   kubectl get svc
   ```

   The example output is as follows\.

   ```
   NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
   kubernetes   ClusterIP   10.100.0.1   <none>        443/TCP   28h
   ```

1. \(Recommended\) To use some Amazon EKS add\-ons, or to enable individual Kubernetes workloads to have specific AWS Identity and Access Management \(IAM\) permissions, create an IAM OpenID Connect \(OIDC\) provider for your cluster\. For instructions on how to create an IAM OIDC provider for your cluster, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\. You only need to create an IAM OIDC provider for your cluster once\. To learn more about Amazon EKS add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\. To learn more about assigning specific IAM permissions to your workloads, see [IAM roles for service accounts technical overview](iam-roles-for-service-accounts-technical-overview.md)\. 

1. \(Recommended\) Configure your cluster for the Amazon VPC CNI plugin for Kubernetes plugin before deploying Amazon EC2 nodes to your cluster\. By default, the plugin was installed with your cluster\. When you add Amazon EC2 nodes to your cluster, the plugin is automatically deployed to each Amazon EC2 node that you add\. The plugin requires you to attach one of the following IAM policies to an IAM role:
   + **[https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy$jsonEditor](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy$jsonEditor) managed IAM policy** – If your cluster uses the `IPv4` family
   + **An [IAM policy that you create](cni-iam-role.md#cni-iam-role-create-ipv6-policy)** – If your cluster uses the `IPv6` family

   The IAM role that you attach the policy to can be the node IAM role, or a dedicated role used only for the plugin\. We recommend attaching the policy to this role\. For more information about creating the role, see [Configuring the Amazon VPC CNI plugin for Kubernetes to use IAM roles for service accounts](cni-iam-role.md) or [Amazon EKS node IAM role](create-node-role.md)\.

1. If you deployed your cluster using the AWS Management Console, you can skip this step\. The AWS Management Console deploys the Amazon VPC CNI plugin for Kubernetes, CoreDNS, and `kube-proxy` Amazon EKS add\-ons, by default\.

   \(Optional\) If you deploy your cluster using either `eksctl` or the AWS CLI, then the Amazon VPC CNI plugin for Kubernetes, CoreDNS, and `kube-proxy` self\-managed add\-ons are deployed\. You can migrate the Amazon VPC CNI plugin for Kubernetes, CoreDNS, and `kube-proxy` self\-managed add\-ons that are deployed with your cluster to Amazon EKS add\-ons\. For more information, see [Amazon EKS add\-ons](eks-add-ons.md)\.

Recommended next steps:
+ [Grant the IAM entity that created the cluster the required permissions to view Kubernetes resources in the AWS Management Console](view-kubernetes-resources.md#view-kubernetes-resources-permissions)
+ [Grant IAM entities access to your cluster](add-user-role.md)\. If you want the entities to view Kubernetes resources in the Amazon EKS console, grant the [Required permissions](view-kubernetes-resources.md#view-kubernetes-resources-permissions) to the entities\.
+ [Enable the private endpoint for your cluster](cluster-endpoint.md) if you want nodes and users to access your cluster from within your VPC\.
+ [Enable secrets encryption for your cluster](enable-kms.md)
+ [Configure logging for your cluster](control-plane-logs.md)
+ [Add nodes to your cluster](eks-compute.md)