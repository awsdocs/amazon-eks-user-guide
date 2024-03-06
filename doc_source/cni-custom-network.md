# Custom networking for pods<a name="cni-custom-network"></a>

By default, when the Amazon VPC CNI plugin for Kubernetes creates secondary [elastic network interfaces](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html) \(network interfaces\) for your Amazon EC2 node, it creates them in the same subnet as the node's primary network interface\. It also associates the same security groups to the secondary network interface that are associated to the primary network interface\. For one or more of the following reasons, you might want the plugin to create secondary network interfaces in a different subnet or want to associate different security groups to the secondary network interfaces, or both: 
+ There's a limited number of `IPv4` addresses that are available in the subnet that the primary network interface is in\. This might limit the number of Pods that you can create in the subnet\. By using a different subnet for secondary network interfaces, you can increase the number of available `IPv4` addresses available for Pods\.
+ For security reasons, your Pods might need to use a different subnet or security groups than the node's primary network interface\.
+ The nodes are configured in public subnets, and you want to place the Pods in private subnets\. The route table associated to a public subnet includes a route to an internet gateway\. The route table associated to a private subnet doesn't include a route to an internet gateway\.

**Considerations**
+ With custom networking enabled, no IP addresses assigned to the primary network interface are assigned to Pods\. Only IP addresses from secondary network interfaces are assigned to `Pods`\.
+ If your cluster uses the `IPv6` family, you can't use custom networking\.
+ If you plan to use custom networking only to help alleviate `IPv4` address exhaustion, you can create a cluster using the `IPv6` family instead\. For more information, see [`IPv6` addresses for clusters, Pods, and services](cni-ipv6.md)\.
+ Even though Pods deployed to subnets specified for secondary network interfaces can use different subnet and security groups than the node's primary network interface, the subnets and security groups must be in the same VPC as the node\.

**Prerequisites**
+ Familiarity with how the Amazon VPC CNI plugin for Kubernetes creates secondary network interfaces and assigns IP addresses to Pods\. For more information, see [ENI Allocation](https://github.com/aws/amazon-vpc-cni-k8s#eni-allocation) on GitHub\.
+ Version `2.12.3` or later or version `1.27.160` or later of the AWS Command Line Interface \(AWS CLI\) installed and configured on your device or AWS CloudShell\. To check your current version, use `aws --version | cut -d / -f2 | cut -d ' ' -f1`\. Package managers such `yum`, `apt-get`, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI\. To install the latest version, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with aws configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the *AWS Command Line Interface User Guide*\. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version\. To update it, see [Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the *AWS CloudShell User Guide*\.
+ The `kubectl` command line tool is installed on your device or AWS CloudShell\. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster\. For example, if your cluster version is `1.28`, you can use `kubectl` version `1.27`, `1.28`, or `1.29` with it\. To install or upgrade `kubectl`, see [Installing or updating `kubectl`](install-kubectl.md)\.
+ We recommend that you complete the steps in this topic in a Bash shell\. If you aren't using a Bash shell, some script commands such as line continuation characters and the way variables are set and used require adjustment for your shell\. Additionally, the quoting and escaping rules for your shell might be different\. For more information, see [Using quotation marks with strings in the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-parameters-quoting-strings.html) in the AWS Command Line Interface User Guide\.

For this tutorial, we recommend using the `example values`, except where it's noted to replace them\. You can replace any `example value` when completing the steps for a production cluster\. We recommend completing all steps in the same terminal\. This is because variables are set and used throughout the steps and won't exist in different terminals\.

The commands in this topic are formatted using the conventions listed in [Using the AWS CLI examples](https://docs.aws.amazon.com/cli/latest/userguide/welcome-examples.html)\. If you're running commands from the command line against resources that are in a different AWS Region than the default AWS Region defined in the AWS CLI [profile](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-profiles) that you're using, then you need to add **\-\-region *region\-code*** to the commands\.

When you want to deploy custom networking to your production cluster, skip to [Step 2: Configure your VPC](#custom-networking-configure-vpc)\.

## Step 1: Create a test VPC and cluster<a name="custom-networking-create-cluster"></a>

**To create a cluster**

The following procedures help you create a test VPC and cluster and configure custom networking for that cluster\. We don't recommend using the test cluster for production workloads because several unrelated features that you might use on your production cluster aren't covered in this topic\. For more information, see [Creating an Amazon EKS cluster](create-cluster.md)\.

1. Define a few variables to use in the remaining steps\.

   ```
   export cluster_name=my-custom-networking-cluster
   account_id=$(aws sts get-caller-identity --query Account --output text)
   ```

1. Create a VPC\.

   1. Create a VPC using an Amazon EKS AWS CloudFormation template\.

      ```
      aws cloudformation create-stack --stack-name my-eks-custom-networking-vpc \
        --template-url https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-vpc-private-subnets.yaml \
        --parameters ParameterKey=VpcBlock,ParameterValue=192.168.0.0/24 \
        ParameterKey=PrivateSubnet01Block,ParameterValue=192.168.0.64/27 \
        ParameterKey=PrivateSubnet02Block,ParameterValue=192.168.0.96/27 \
        ParameterKey=PublicSubnet01Block,ParameterValue=192.168.0.0/27 \
        ParameterKey=PublicSubnet02Block,ParameterValue=192.168.0.32/27
      ```

      The AWS CloudFormation stack takes a few minutes to create\. To check on the stack's deployment status, run the following command\.

      ```
      aws cloudformation describe-stacks --stack-name my-eks-custom-networking-vpc --query Stacks\[\].StackStatus  --output text
      ```

      Don't continue to the next step until the output of the command is `CREATE_COMPLETE`\.

   1. Define variables with the values of the private subnet IDs created by the template\.

      ```
      subnet_id_1=$(aws cloudformation describe-stack-resources --stack-name my-eks-custom-networking-vpc \
          --query "StackResources[?LogicalResourceId=='PrivateSubnet01'].PhysicalResourceId" --output text)
      subnet_id_2=$(aws cloudformation describe-stack-resources --stack-name my-eks-custom-networking-vpc \
          --query "StackResources[?LogicalResourceId=='PrivateSubnet02'].PhysicalResourceId" --output text)
      ```

   1. Define variables with the Availability Zones of the subnets retrieved in the previous step\.

      ```
      az_1=$(aws ec2 describe-subnets --subnet-ids $subnet_id_1 --query 'Subnets[*].AvailabilityZone' --output text)
      az_2=$(aws ec2 describe-subnets --subnet-ids $subnet_id_2 --query 'Subnets[*].AvailabilityZone' --output text)
      ```

1. Create a cluster IAM role\.

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

   1. Create the Amazon EKS cluster IAM role\. If necessary, preface `eks-cluster-role-trust-policy.json` with the path on your computer that you wrote the file to in the previous step\. The command associates the trust policy that you created in the previous step to the role\. To create an IAM role, the [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) that is creating the role must be assigned the `iam:CreateRole` action \(permission\)\.

      ```
      aws iam create-role --role-name myCustomNetworkingAmazonEKSClusterRole --assume-role-policy-document file://"eks-cluster-role-trust-policy.json"
      ```

   1. Attach the Amazon EKS managed policy named [https://console.aws.amazon.com/arn:aws:iam::aws:policy/AmazonEKSClusterPolicy](https://console.aws.amazon.com/arn:aws:iam::aws:policy/AmazonEKSClusterPolicy) to the role\. To attach an IAM policy to an [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html), the principal that is attaching the policy must be assigned one of the following IAM actions \(permissions\): `iam:AttachUserPolicy` or `iam:AttachRolePolicy`\.

      ```
      aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy --role-name myCustomNetworkingAmazonEKSClusterRole
      ```

1. Create an Amazon EKS cluster and configure your device to communicate with it\.

   1. Create a cluster\.

      ```
      aws eks create-cluster --name my-custom-networking-cluster \
         --role-arn arn:aws:iam::$account_id:role/myCustomNetworkingAmazonEKSClusterRole \
         --resources-vpc-config subnetIds=$subnet_id_1","$subnet_id_2
      ```
**Note**  
You might receive an error that one of the Availability Zones in your request doesn't have sufficient capacity to create an Amazon EKS cluster\. If this happens, the error output contains the Availability Zones that can support a new cluster\. Retry creating your cluster with at least two subnets that are located in the supported Availability Zones for your account\. For more information, see [Insufficient capacity](troubleshooting.md#ICE)\.

   1. The cluster takes several minutes to create\. To check on the cluster's deployment status, run the following command\.

      ```
      aws eks describe-cluster --name my-custom-networking-cluster --query cluster.status
      ```

      Don't continue to the next step until the output of the command is `"ACTIVE"`\.

   1. Configure `kubectl` to communicate with your cluster\.

      ```
      aws eks update-kubeconfig --name my-custom-networking-cluster
      ```

## Step 2: Configure your VPC<a name="custom-networking-configure-vpc"></a>

This tutorial requires the VPC created in [Step 1: Create a test VPC and cluster](#custom-networking-create-cluster)\. For a production cluster, adjust the steps accordingly for your VPC by replacing all of the `example values` with your own\.

1. Confirm that your currently\-installed Amazon VPC CNI plugin for Kubernetes is the latest version\. To determine the latest version for the Amazon EKS add\-on type and update your version to it, see [Updating an add\-on](managing-add-ons.md#updating-an-add-on)\. To determine the latest version for the self\-managed add\-on type and update your version to it, see [Working with the Amazon VPC CNI plugin for Kubernetes Amazon EKS add\-on](managing-vpc-cni.md)\.

1. Retrieve the ID of your cluster VPC and store it in a variable for use in later steps\. For a production cluster, replace *`my-custom-networking-cluster`* with the name of your cluster\.

   ```
   vpc_id=$(aws eks describe-cluster --name my-custom-networking-cluster --query "cluster.resourcesVpcConfig.vpcId" --output text)
   ```

1. Associate an additional Classless Inter\-Domain Routing \(CIDR\) block with your cluster's VPC\. The CIDR block can't overlap with any existing associated CIDR blocks\.

   1. View the current CIDR blocks associated to your VPC\.

      ```
      aws ec2 describe-vpcs --vpc-ids $vpc_id \
          --query 'Vpcs[*].CidrBlockAssociationSet[*].{CIDRBlock: CidrBlock, State: CidrBlockState.State}' --out table
      ```

      An example output is as follows\.

      ```
      ----------------------------------
      |          DescribeVpcs          |
      +-----------------+--------------+
      |    CIDRBlock    |    State     |
      +-----------------+--------------+
      |  192.168.0.0/24 |  associated  |
      +-----------------+--------------+
      ```

   1. Associate an additional CIDR block to your VPC\. For more information, see [Associate additional `IPv4` CIDR blocks with your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html#add-ipv4-cidr) in the Amazon VPC User Guide\.

      ```
      aws ec2 associate-vpc-cidr-block --vpc-id $vpc_id --cidr-block 192.168.1.0/24
      ```

   1. Confirm that the new block is associated\.

      ```
      aws ec2 describe-vpcs --vpc-ids $vpc_id --query 'Vpcs[*].CidrBlockAssociationSet[*].{CIDRBlock: CidrBlock, State: CidrBlockState.State}' --out table
      ```

      An example output is as follows\.

      ```
      ----------------------------------
      |          DescribeVpcs          |
      +-----------------+--------------+
      |    CIDRBlock    |    State     |
      +-----------------+--------------+
      |  192.168.0.0/24 |  associated  |
      |  192.168.1.0/24 |  associated  |
      +-----------------+--------------+
      ```

   Don't proceed to the next step until your new CIDR block's `State` is `associated`\.

1. Create as many subnets as you want to use in each Availability Zone that your existing subnets are in\. Specify a CIDR block that's within the CIDR block that you associated with your VPC in a previous step\. 

   1. Create new subnets\. The subnets must be created in a different VPC CIDR block than your existing subnets are in, but in the same Availability Zones as your existing subnets\. In this example, one subnet is created in the new CIDR block in each Availability Zone that the current private subnets exist in\. The IDs of the subnets created are stored in variables for use in later steps\. The `Name` values match the values assigned to the subnets created using the Amazon EKS VPC template in a previous step\. Names aren't required\. You can use different names\. 

      ```
      new_subnet_id_1=$(aws ec2 create-subnet --vpc-id $vpc_id --availability-zone $az_1 --cidr-block 192.168.1.0/27 \
          --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=my-eks-custom-networking-vpc-PrivateSubnet01},{Key=kubernetes.io/role/internal-elb,Value=1}]' \
          --query Subnet.SubnetId --output text)
      new_subnet_id_2=$(aws ec2 create-subnet --vpc-id $vpc_id --availability-zone $az_2 --cidr-block 192.168.1.32/27 \
          --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=my-eks-custom-networking-vpc-PrivateSubnet02},{Key=kubernetes.io/role/internal-elb,Value=1}]' \
          --query Subnet.SubnetId --output text)
      ```
**Important**  
By default, your new subnets are implicitly associated with your VPC's [main route table](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html#RouteTables)\. This route table allows communication between all the resources that are deployed in the VPC\. However, it doesn't allow communication with resources that have IP addresses that are outside the CIDR blocks that are associated with your VPC\. You can associate your own route table to your subnets to change this behavior\. For more information, see [Subnet route tables](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html#subnet-route-tables) in the Amazon VPC User Guide\.

   1. View the current subnets in your VPC\.

      ```
      aws ec2 describe-subnets --filters "Name=vpc-id,Values=$vpc_id" \
          --query 'Subnets[*].{SubnetId: SubnetId,AvailabilityZone: AvailabilityZone,CidrBlock: CidrBlock}' \
          --output table
      ```

      An example output is as follows\.

      ```
      ----------------------------------------------------------------------
      |                           DescribeSubnets                          |
      +------------------+--------------------+----------------------------+
      | AvailabilityZone |     CidrBlock      |         SubnetId           |
      +------------------+--------------------+----------------------------+
      |  us-west-2d      |  192.168.0.0/27    |     subnet-example1        |
      |  us-west-2a      |  192.168.0.32/27   |     subnet-example2        |
      |  us-west-2a      |  192.168.0.64/27   |     subnet-example3        |
      |  us-west-2d      |  192.168.0.96/27   |     subnet-example4        |
      |  us-west-2a      |  192.168.1.0/27    |     subnet-example5        |
      |  us-west-2d      |  192.168.1.32/27   |     subnet-example6        |
      +------------------+--------------------+----------------------------+
      ```

      You can see the subnets in the `192.168.1.0` CIDR block that you created are in the same Availability Zones as the subnets in the `192.168.0.0` CIDR block\.

## Step 3: Configure Kubernetes resources<a name="custom-networking-configure-kubernetes"></a>

**To configure Kubernetes resources**

1. Set the `AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG` environment variable to `true` in the `aws-node` `DaemonSet`\.

   ```
   kubectl set env daemonset aws-node -n kube-system AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG=true
   ```

1. Retrieve the ID of your [cluster security group](sec-group-reqs.md) and store it in a variable for use in the next step\. Amazon EKS automatically creates this security group when you create your cluster\.

   ```
   cluster_security_group_id=$(aws eks describe-cluster --name $cluster_name --query cluster.resourcesVpcConfig.clusterSecurityGroupId --output text)
   ```

1. Create an `ENIConfig` custom resource for each subnet that you want to deploy Pods in\.

   1. Create a unique file for each network interface configuration\.

      

      The following commands create separate `ENIConfig` files for the two subnets that were created in a previous step\. The value for `name` must be unique\. The name is the same as the Availability Zone that the subnet is in\. The cluster security group is assigned to the `ENIConfig`\.

      ```
      cat >$az_1.yaml <<EOF
      apiVersion: crd.k8s.amazonaws.com/v1alpha1
      kind: ENIConfig
      metadata: 
        name: $az_1
      spec: 
        securityGroups: 
          - $cluster_security_group_id
        subnet: $new_subnet_id_1
      EOF
      ```

      ```
      cat >$az_2.yaml <<EOF
      apiVersion: crd.k8s.amazonaws.com/v1alpha1
      kind: ENIConfig
      metadata: 
        name: $az_2
      spec: 
        securityGroups: 
          - $cluster_security_group_id
        subnet: $new_subnet_id_2
      EOF
      ```

      For a production cluster, you can make the following changes to the previous commands:
      + Replace *`$cluster_security_group_id`* with the ID of an existing [security group](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html) that you want to use for each `ENIConfig`\.
      + We recommend naming your `ENIConfigs` the same as the Availability Zone that you'll use the `ENIConfig` for, whenever possible\. You might need to use different names for your `ENIConfigs` than the names of the Availability Zones for a variety of reasons\. For example, if you have more than two subnets in the same Availability Zone and want to use them both with custom networking, then you need multiple `ENIConfigs` for the same Availability Zone\. Since each `ENIConfig` requires a unique name, you can't name more than one of your `ENIConfigs` using the Availability Zone name\.

        If your `ENIConfig` names aren't all the same as Availability Zone names, then replace `$az_1` and `$az_2` with your own names in the previous commands and [annotate your nodes with the `ENIConfig`](#custom-networking-annotate-eniconfig) later in this tutorial\.
**Note**  
If you don't specify a valid security group for use with a production cluster and you're using:  
version `1.8.0` or later of the Amazon VPC CNI plugin for Kubernetes, then the security groups associated with the node's primary elastic network interface are used\.
a version of the Amazon VPC CNI plugin for Kubernetes that's earlier than `1.8.0`, then the default security group for the VPC is assigned to secondary network interfaces\.
**Important**  
`AWS_VPC_K8S_CNI_EXTERNALSNAT=false` is a default setting in the configuration for the Amazon VPC CNI plugin for Kubernetes\. If you're using the default setting, then traffic that is destined for IP addresses that aren't within one of the CIDR blocks associated with your VPC use the security groups and subnets of your node's primary network interface\. The subnets and security groups defined in your `ENIConfigs` that are used to create secondary network interfaces aren't used for this traffic\. For more information about this setting, see [SNAT for Pods](external-snat.md)\.
If you also use security groups for Pods, the security group that's specified in a `SecurityGroupPolicy` is used instead of the security group that's specified in the `ENIConfigs`\. For more information, see [Security groups for Pods](security-groups-for-pods.md)\.

   1. Apply each custom resource file that you created to your cluster with the following commands\.

      ```
      kubectl apply -f $az_1.yaml
      kubectl apply -f $az_2.yaml
      ```

1. Confirm that your `ENIConfigs` were created\.

   ```
   kubectl get ENIConfigs
   ```

   An example output is as follows\.

   ```
   NAME         AGE
   us-west-2a   117s
   us-west-2d   105s
   ```

1. If you're enabling custom networking on a production cluster and named your `ENIConfigs` something other than the Availability Zone that you're using them for, then skip to the [next step](#custom-networking-deploy-nodes) to deploy Amazon EC2 nodes\.

   Enable Kubernetes to automatically apply the `ENIConfig` for an Availability Zone to any new Amazon EC2 nodes created in your cluster\.

   1. For the test cluster in this tutorial, skip to the [next step](#custom-networking-automatically-apply-eniconfig)\.

      For a production cluster, check to see if an annotation with the key `k8s.amazonaws.com/eniConfig` for the `[ENI\_CONFIG\_ANNOTATION\_DEF](https://github.com/aws/amazon-vpc-cni-k8s#eni_config_annotation_def)` environment variable exists in the container spec for the `aws-node` `DaemonSet`\.

      ```
      kubectl describe daemonset aws-node -n kube-system | grep ENI_CONFIG_ANNOTATION_DEF
      ```

      If output is returned, the annotation exists\. If no output is returned, then the variable is not set\. For a production cluster, you can use either this setting or the setting in the following step\. If you use this setting, it overrides the setting in the following step\. In this tutorial, the setting in the next step is used\.

   1. Update your `aws-node` `DaemonSet` to automatically apply the `ENIConfig` for an Availability Zone to any new Amazon EC2 nodes created in your cluster\.

      ```
      kubectl set env daemonset aws-node -n kube-system ENI_CONFIG_LABEL_DEF=topology.kubernetes.io/zone
      ```

## Step 4: Deploy Amazon EC2 nodes<a name="custom-networking-deploy-nodes"></a>

**To deploy Amazon EC2 nodes**

1. Create a node IAM role\.

   1. Run the following command to create an IAM trust policy JSON file\.

      ```
      cat >node-role-trust-relationship.json <<EOF
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

   1. Run the following command to set a variable for your role name\. You can replace `myCustomNetworkingAmazonEKSNodeRole` with any name you choose\.

      ```
      export node_role_name=myCustomNetworkingAmazonEKSNodeRole
      ```

   1. Create the IAM role and store its returned Amazon Resource Name \(ARN\) in a variable for use in a later step\.

      ```
      node_role_arn=$(aws iam create-role --role-name $node_role_name --assume-role-policy-document file://"node-role-trust-relationship.json" \
          --query Role.Arn --output text)
      ```

   1. Attach three required IAM managed policies to the IAM role\.

      ```
      aws iam attach-role-policy \
        --policy-arn arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy \
        --role-name $node_role_name
      aws iam attach-role-policy \
        --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly \
        --role-name $node_role_name
      aws iam attach-role-policy \
          --policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy \
          --role-name $node_role_name
      ```
**Important**  
For simplicity in this tutorial, the [https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKS_CNI_Policy.html](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKS_CNI_Policy.html) policy is attached to the node IAM role\. In a production cluster however, we recommend attaching the policy to a separate IAM role that is used only with the Amazon VPC CNI plugin for Kubernetes\. For more information, see [Configuring the Amazon VPC CNI plugin for Kubernetes to use IAM roles for service accounts \(IRSA\)](cni-iam-role.md)\.

1. Create one of the following types of node groups\. To determine the instance type that you want to deploy, see [Choosing an Amazon EC2 instance type](choosing-instance-type.md)\. For this tutorial, complete the **Managed**, **Without a launch template or with a launch template without an AMI ID specified** option\. If you're going to use the node group for production workloads, then we recommend that you familiarize yourself with all of the [managed](create-managed-node-group.md) and [self\-managed](worker.md) node group options before deploying the node group\.
   + **Managed** – Deploy your node group using one of the following options:
     + **Without a launch template or with a launch template without an AMI ID specified** – Run the following command\. For this tutorial, use the `example values`\. For a production node group, replace all `example values` with your own\. The node group name can't be longer than 63 characters\. It must start with letter or digit, but can also include hyphens and underscores for the remaining characters\.

       ```
       aws eks create-nodegroup --cluster-name $cluster_name --nodegroup-name my-nodegroup \
           --subnets $subnet_id_1 $subnet_id_2 --instance-types t3.medium --node-role $node_role_arn
       ```
     + **With a launch template with a specified AMI ID**

       1. Determine the Amazon EKS recommended number of maximum Pods for your nodes\. Follow the instructions in [Amazon EKS recommended maximum Pods for each Amazon EC2 instance type](choosing-instance-type.md#determine-max-pods), adding **`--cni-custom-networking-enabled`** to step 3 in that topic\. Note the output for use in the next step\.

       1. In your launch template, specify an Amazon EKS optimized AMI ID, or a custom AMI built off the Amazon EKS optimized AMI, then [deploy the node group using a launch template](launch-templates.md) and provide the following user data in the launch template\. This user data passes arguments into the `bootstrap.sh` file\. For more information about the bootstrap file, see [bootstrap\.sh](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) on GitHub\. You can replace `20` with either the value from the previous step \(recommended\) or your own value\.

          ```
          /etc/eks/bootstrap.sh my-cluster --use-max-pods false --kubelet-extra-args '--max-pods=20'
          ```

          If you've created a custom AMI that is not built off the Amazon EKS optimized AMI, then you need to custom create the configuration yourself\. 
   + **Self\-managed**

     1. Determine the Amazon EKS recommended number of maximum Pods for your nodes\. Follow the instructions in [Amazon EKS recommended maximum Pods for each Amazon EC2 instance type](choosing-instance-type.md#determine-max-pods), adding **`--cni-custom-networking-enabled`** to step 3 in that topic\. Note the output for use in the next step\.

     1. Deploy the node group using the instructions in [Launching self\-managed Amazon Linux nodes](launch-workers.md)\. Specify the following text for the **BootstrapArguments** parameter\. You can replace `20` with either the value from the previous step \(recommended\) or your own value\.

        ```
        --use-max-pods false --kubelet-extra-args '--max-pods=20'
        ```
**Note**  
If you want nodes in a production cluster to support a significantly higher number of Pods, run the script in [Amazon EKS recommended maximum Pods for each Amazon EC2 instance type](choosing-instance-type.md#determine-max-pods) again\. Also, add the `--cni-prefix-delegation-enabled` option to the command\. For example, `110` is returned for an `m5.large` instance type\. For instructions on how to enable this capability, see [Increase the amount of available IP addresses for your Amazon EC2 nodes](cni-increase-ip-addresses.md)\. You can use this capability with custom networking\.

   Node group creation takes several minutes\. You can check the status of the creation of a managed node group with the following command\.

   ```
   aws eks describe-nodegroup --cluster-name $cluster_name --nodegroup-name my-nodegroup --query nodegroup.status --output text
   ```

   Don't continue to the next step until the output returned is `ACTIVE`\.

1. For the tutorial, you can skip this step\.

   For a production cluster, if you didn't name your `ENIConfigs` the same as the Availability Zone that you're using them for, then you must annotate your nodes with the `ENIConfig` name that should be used with the node\. This step isn't necessary if you only have one subnet in each Availability Zone and you named your `ENIConfigs` with the same names as your Availability Zones\. This is because the Amazon VPC CNI plugin for Kubernetes automatically associates the correct `ENIConfig` with the node for you when you enabled it to do so in a [previous step](#custom-networking-automatically-apply-eniconfig)\. 

   1. Get the list of nodes in your cluster\.

      ```
      kubectl get nodes
      ```

      An example output is as follows\.

      ```
      NAME                                          STATUS   ROLES    AGE     VERSION
      ip-192-168-0-126.us-west-2.compute.internal   Ready    <none>   8m49s   v1.22.9-eks-810597c
      ip-192-168-0-92.us-west-2.compute.internal    Ready    <none>   8m34s   v1.22.9-eks-810597c
      ```

   1. Determine which Availability Zone each node is in\. Run the following command for each node that was returned in the previous step\.

      ```
      aws ec2 describe-instances --filters Name=network-interface.private-dns-name,Values=ip-192-168-0-126.us-west-2.compute.internal \
      --query 'Reservations[].Instances[].{AvailabilityZone: Placement.AvailabilityZone, SubnetId: SubnetId}'
      ```

      An example output is as follows\.

      ```
      [
          {
              "AvailabilityZone": "us-west-2d",
              "SubnetId": "subnet-Example5"
          }
      ]
      ```

   1. Annotate each node with the `ENIConfig` that you created for the subnet ID and Availability Zone\. You can only annotate a node with one `ENIConfig`, though multiple nodes can be annotated with the same `ENIConfig`\. Replace the `example values` with your own\.

      ```
      kubectl annotate node ip-192-168-0-126.us-west-2.compute.internal k8s.amazonaws.com/eniConfig=EniConfigName1
      kubectl annotate node ip-192-168-0-92.us-west-2.compute.internal k8s.amazonaws.com/eniConfig=EniConfigName2
      ```

1. If you had nodes in a production cluster with running Pods before you switched to using the custom networking feature, complete the following tasks:

   1. Make sure that you have available nodes that are using the custom networking feature\.

   1. Cordon and drain the nodes to gracefully shut down the Pods\. For more information, see [Safely Drain a Node](https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/) in the Kubernetes documentation\.

   1. Terminate the nodes\. If the nodes are in an existing managed node group, you can delete the node group\. Copy the command that follows to your device\. Make the following modifications to the command as needed and then run the modified command:
      + Replace `my-cluster` with the name for your cluster\.
      + Replace `my-nodegroup` with the name for your node group\.

      ```
      aws eks delete-nodegroup --cluster-name my-cluster --nodegroup-name my-nodegroup
      ```

    Only new nodes that are registered with the `k8s.amazonaws.com/eniConfig` label use the custom networking feature\.

1. Confirm that Pods are assigned an IP address from a CIDR block that's associated to one of the subnets that you created in a previous step\.

   ```
   kubectl get pods -A -o wide
   ```

   An example output is as follows\.

   ```
   NAMESPACE     NAME                       READY   STATUS    RESTARTS   AGE     IP              NODE                                          NOMINATED NODE   READINESS GATES
   kube-system   aws-node-2rkn4             1/1     Running   0          7m19s   192.168.0.92    ip-192-168-0-92.us-west-2.compute.internal    <none>           <none>
   kube-system   aws-node-k96wp             1/1     Running   0          7m15s   192.168.0.126   ip-192-168-0-126.us-west-2.compute.internal   <none>           <none>
   kube-system   coredns-657694c6f4-smcgr   1/1     Running   0          56m     192.168.1.23    ip-192-168-0-92.us-west-2.compute.internal    <none>           <none>
   kube-system   coredns-657694c6f4-stwv9   1/1     Running   0          56m     192.168.1.28    ip-192-168-0-92.us-west-2.compute.internal    <none>           <none>
   kube-system   kube-proxy-jgshq           1/1     Running   0          7m19s   192.168.0.92    ip-192-168-0-92.us-west-2.compute.internal    <none>           <none>
   kube-system   kube-proxy-wx9vk           1/1     Running   0          7m15s   192.168.0.126   ip-192-168-0-126.us-west-2.compute.internal   <none>           <none>
   ```

   You can see that the `coredns` `Pods` are assigned IP addresses from the `192.168.1.0` CIDR block that you added to your VPC\. Without custom networking, they would have been assigned addresses from the `192.168.0.0` CIDR block, because it was the only CIDR block originally associated with the VPC\.

   If a Pod's `spec` contains `hostNetwork=true`, it's assigned the primary IP address of the node\. It isn't assigned an address from the subnets that you added\. By default, this value is set to `false`\. This value is set to `true` for the `kube-proxy` and Amazon VPC CNI plugin for Kubernetes \(`aws-node`\) Pods that run on your cluster\. This is why the `kube-proxy` and the plugin's `aws-node` Pods aren't assigned `192.168.1.x` addresses in the previous output\. For more information about a Pod's `hostNetwork` setting, see [PodSpec v1 core](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.29/#podspec-v1-core) in the Kubernetes API reference\.

## Step 5: Delete tutorial resources<a name="custom-network-delete-resources"></a>

After you complete the tutorial, we recommend that you delete the resources that you created\. You can then adjust the steps to enable custom networking for a production cluster\.

**To delete the tutorial resources**

1. If the node group that you created was just for testing, then delete it\.

   ```
   aws eks delete-nodegroup --cluster-name $cluster_name --nodegroup-name my-nodegroup
   ```

   Even after the AWS CLI output says that the cluster is deleted, the delete process might not actually be complete\. The delete process takes a few minutes\. Confirm that it's complete by running the following command\.

   ```
   aws eks describe-nodegroup --cluster-name $cluster_name --nodegroup-name my-nodegroup --query nodegroup.status --output text
   ```

   Don't continue until the returned output is similar to the following output\.

   ```
   An error occurred (ResourceNotFoundException) when calling the DescribeNodegroup operation: No node group found for name: my-nodegroup.
   ```

1. If the node group that you created was just for testing, then delete the node IAM role\.

   1. Detach the policies from the role\.

      ```
      aws iam detach-role-policy --role-name myCustomNetworkingAmazonEKSNodeRole --policy-arn arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy
      aws iam detach-role-policy --role-name myCustomNetworkingAmazonEKSNodeRole --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly
      aws iam detach-role-policy --role-name myCustomNetworkingAmazonEKSNodeRole --policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy
      ```

   1. Delete the role\.

      ```
      aws iam delete-role --role-name myCustomNetworkingAmazonEKSNodeRole
      ```

1. Delete the cluster\.

   ```
   aws eks delete-cluster --name $cluster_name
   ```

   Confirm the cluster is deleted with the following command\.

   ```
   aws eks describe-cluster --name $cluster_name --query cluster.status --output text
   ```

   When output similar to the following is returned, the cluster is successfully deleted\.

   ```
   An error occurred (ResourceNotFoundException) when calling the DescribeCluster operation: No cluster found for name: my-cluster.
   ```

1. Delete the cluster IAM role\.

   1. Detach the policies from the role\.

      ```
      aws iam detach-role-policy --role-name myCustomNetworkingAmazonEKSClusterRole --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy
      ```

   1. Delete the role\.

      ```
      aws iam delete-role --role-name myCustomNetworkingAmazonEKSClusterRole
      ```

1. Delete the subnets that you created in a previous step\.

   ```
   aws ec2 delete-subnet --subnet-id $new_subnet_id_1
   aws ec2 delete-subnet --subnet-id $new_subnet_id_2
   ```

1. Delete the VPC that you created\.

   ```
   aws cloudformation delete-stack --stack-name my-eks-custom-networking-vpc
   ```