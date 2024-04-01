# `IPv6` addresses for clusters, Pods, and services<a name="cni-ipv6"></a>

By default, Kubernetes assigns `IPv4` addresses to your Pods and services\. Instead of assigning `IPv4` addresses to your Pods and services, you can configure your cluster to assign `IPv6` addresses to them\. Amazon EKS doesn't support dual\-stacked Pods or services, even though Kubernetes does in version `1.23` and later\. As a result, you can't assign both `IPv4` and `IPv6` addresses to your Pods and services\. 

You select which IP family you want to use for your cluster when you create it\. You can't change the family after you create the cluster\.

## Considerations for using the `IPv6` family for your cluster<a name="ipv6-considerations"></a>
+ You must create a new cluster and specify that you want to use the `IPv6` family for that cluster\. You can't enable the `IPv6` family for a cluster that you updated from a previous version\. For instructions on how to create a new cluster, see [Creating an Amazon EKS cluster](create-cluster.md)\.
+ The version of the Amazon VPC CNI add\-on that you deploy to your cluster must be version `1.10.1` or later\. This version or later is deployed by default\. After you deploy the add\-on, you can't downgrade your Amazon VPC CNI add\-on to a version lower than `1.10.1` without first removing all nodes in all node groups in your cluster\.
+ Windows Pods and services aren't supported\.
+ If you use Amazon EC2 nodes, you must configure the Amazon VPC CNI add\-on with IP prefix delegation and `IPv6`\. If you choose the `IPv6` family when creating your cluster, the `1.10.1` version of the add\-on defaults to this configuration\. This is the case for both a self\-managed or Amazon EKS add\-on\. For more information about IP prefix delegation, see [Increase the amount of available IP addresses for your Amazon EC2 nodes](cni-increase-ip-addresses.md)\.
+ When you create a cluster, the VPC and subnets that you specify must have an `IPv6` CIDR block that's assigned to the VPC and subnets that you specify\. They must also have an `IPv4` CIDR block assigned to them\. This is because, even if you only want to use `IPv6`, a VPC still requires an `IPv4` CIDR block to function\. For more information, see [Associate an `IPv6` CIDR block with your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html#vpc-associate-ipv6-cidr) in the Amazon VPC User Guide\.
+ When you create your cluster and nodes, you must specify subnets that are configured to auto\-assign `IPv6` addresses\. Otherwise, you can't deploy your cluster and nodes\. By default, this configuration is disabled\. For more information, see [Modify the `IPv6` addressing attribute for your subnet](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#subnet-ipv6) in the Amazon VPC User Guide\.
+ The route tables that are assigned to your subnets must have routes for `IPv6` addresses\. For more information, see [Migrate to `IPv6`](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-migrate-ipv6.html) in the Amazon VPC User Guide\.
+ Your security groups must allow `IPv6` addresses\. For more information, see [Migrate to `IPv6`](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-migrate-ipv6.html) in the Amazon VPC User Guide\.
+ You can only use `IPv6` with AWS Nitro\-based Amazon EC2 or Fargate nodes\.
+ You can't use `IPv6` with [Security groups for Pods](security-groups-for-pods.md) with Amazon EC2 nodes\. However, you can use it with Fargate nodes\. If you need separate security groups for individual Pods, continue using the `IPv4` family with Amazon EC2 nodes, or use Fargate nodes instead\.
+ If you previously used [custom networking](cni-custom-network.md) to help alleviate IP address exhaustion, you can use `IPv6` instead\. You can't use custom networking with `IPv6`\. If you use custom networking for network isolation, then you might need to continue to use custom networking and the `IPv4` family for your clusters\.
+ You can't use `IPv6` with [AWS Outposts](eks-outposts.md)\.
+ Pods and services are only assigned an `IPv6` address\. They aren't assigned an `IPv4` address\. Because Pods are able to communicate to `IPv4` endpoints through NAT on the instance itself, [DNS64 and NAT64](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html#nat-gateway-nat64-dns64) aren't needed\. If the traffic needs a public IP address, the traffic is then source network address translated to a public IP\.
+ The source `IPv6` address of a Pod isn't source network address translated to the `IPv6` address of the node when communicating outside of the VPC\. It is routed using an internet gateway or egress\-only internet gateway\.
+ All nodes are assigned an `IPv4` and `IPv6` address\.
+ The [Amazon FSx for Lustre CSI driver](fsx-csi.md) is not supported\.
+ You can use version `2.3.1` or later of the AWS Load Balancer Controller to load balance [application](alb-ingress.md) or [network](network-load-balancing.md) traffic to `IPv6` Pods in IP mode, but not instance mode\. For more information, see [What is the AWS Load Balancer Controller?](aws-load-balancer-controller.md)\.
+ You must attach an `IPv6` IAM policy to your node IAM or CNI IAM role\. Between the two, we recommend that you attach it to a CNI IAM role\. For more information, see [Create IAM policy for clusters that use the `IPv6` family](cni-iam-role.md#cni-iam-role-create-ipv6-policy) and [Step 1: Create the Amazon VPC CNI plugin for Kubernetes IAM role](cni-iam-role.md#cni-iam-role-create-role)\.
+ Each Fargate Pod receives an `IPv6` address from the CIDR that's specified for the subnet that it's deployed in\. The underlying hardware unit that runs Fargate Pods gets a unique `IPv4` and `IPv6` address from the CIDRs that are assigned to the subnet that the hardware unit is deployed in\.
+ We recommend that you perform a thorough evaluation of your applications, Amazon EKS add\-ons, and AWS services that you integrate with before deploying `IPv6` clusters\. This is to ensure that everything works as expected with `IPv6`\.
+ Use of the Amazon EC2 [Instance Metadata Service](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html) `IPv6` endpoint is not supported with Amazon EKS\.
+ When creating a self\-managed node group in a cluster that uses the `IPv6` family, user\-data must include the following `BootstrapArguments` for the [https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) file that runs at node start up\. Replace *your\-cidr* with the `IPv6` CIDR range of your cluster's VPC\.

  ```
  --ip-family ipv6 --service-ipv6-cidr your-cidr
  ```

  If you don't know the `IPv6` `CIDR` range for your cluster, you can see it with the following command \(requires the AWS CLI version `2.4.9` or later\)\.

  ```
  aws eks describe-cluster --name my-cluster --query cluster.kubernetesNetworkConfig.serviceIpv6Cidr --output text
  ```

## Deploy an `IPv6` cluster and managed Amazon Linux nodes<a name="deploy-ipv6-cluster"></a>

In this tutorial, you deploy an `IPv6` Amazon VPC, an Amazon EKS cluster with the `IPv6` family, and a managed node group with Amazon EC2 Amazon Linux nodes\. You can't deploy Amazon EC2 Windows nodes in an `IPv6` cluster\. You can also deploy Fargate nodes to your cluster, though those instructions aren't provided in this topic for simplicity\. 

Before creating a cluster for production use, we recommend that you familiarize yourself with all settings and deploy a cluster with the settings that meet your requirements\. For more information, see [Creating an Amazon EKS cluster](create-cluster.md), [Managed node groups](managed-node-groups.md) and the [considerations](#ipv6-considerations) for this topic\. You can only enable some settings when creating your cluster\.

**Prerequisites**

Before starting this tutorial, you must install and configure the following tools and resources that you need to create and manage an Amazon EKS cluster\.
+ The `kubectl` command line tool is installed on your device or AWS CloudShell\. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster\. For example, if your cluster version is `1.28`, you can use `kubectl` version `1.27`, `1.28`, or `1.29` with it\. To install or upgrade `kubectl`, see [Installing or updating `kubectl`](install-kubectl.md)\.
+ The IAM security principal that you're using must have permissions to work with Amazon EKS IAM roles, service linked roles, AWS CloudFormation, a VPC, and related resources\. For more information, see [Actions, resources, and condition keys for Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html) and [Using service\-linked roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html) in the IAM User Guide\.

Procedures are provided to create the resources with either `eksctl` or the AWS CLI\. You can also deploy the resources using the AWS Management Console, but those instructions aren't provided in this topic for simplicity\.

------
#### [ eksctl ]

**Prerequisite**  
`eksctl` version `0.175.0` or later installed on your computer\. To install or update to it, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.

**To deploy an `IPv6` cluster with `eksctl`**

1. Create the `ipv6-cluster.yaml` file\. Copy the command that follows to your device\. Make the following modifications to the command as needed and then run the modified command:
   + Replace `my-cluster` with a name for your cluster\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can't be longer than 100 characters\.
   + Replace `region-code` with any AWS Region that is supported by Amazon EKS\. For a list of AWS Regions, see [Amazon EKS endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/eks.html) in the AWS General Reference guide\.
   + The value for `version` with the version of your cluster\. For more information, see [supported Amazon EKS Kubernetes version](kubernetes-versions.md)\.
   + Replace `my-nodegroup` with a name for your node group\. The node group name can't be longer than 63 characters\. It must start with letter or digit, but can also include hyphens and underscores for the remaining characters\.
   + Replace `t3.medium` with any [AWS Nitro System instance type](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html#ec2-nitro-instances)\.

   ```
   cat >ipv6-cluster.yaml <<EOF
   ---
   apiVersion: eksctl.io/v1alpha5
   kind: ClusterConfig
   
   metadata:
     name: my-cluster
     region: region-code
     version: "X.XX"
   
   kubernetesNetworkConfig:
     ipFamily: IPv6
   
   addons:
     - name: vpc-cni
       version: latest
     - name: coredns
       version: latest
     - name: kube-proxy
       version: latest
   
   iam:
     withOIDC: true
   
   managedNodeGroups:
     - name: my-nodegroup
       instanceType: t3.medium
   EOF
   ```

1. Create your cluster\.

   ```
   eksctl create cluster -f ipv6-cluster.yaml
   ```

   Cluster creation takes several minutes\. Don't proceed until you see the last line of output, which looks similar to the following output\.

   ```
   [...]
   [✓]  EKS cluster "my-cluster" in "region-code" region is ready
   ```

1. Confirm that default Pods are assigned `IPv6` addresses\.

   ```
   kubectl get pods -n kube-system -o wide
   ```

   An example output is as follows\.

   ```
   NAME                       READY   STATUS    RESTARTS   AGE     IP                                       NODE                                            NOMINATED NODE   READINESS GATES
   aws-node-rslts             1/1     Running   1          5m36s   2600:1f13:b66:8200:11a5:ade0:c590:6ac8   ip-192-168-34-75.region-code.compute.internal   <none>           <none>
   aws-node-t74jh             1/1     Running   0          5m32s   2600:1f13:b66:8203:4516:2080:8ced:1ca9   ip-192-168-253-70.region-code.compute.internal  <none>           <none>
   coredns-85d5b4454c-cw7w2   1/1     Running   0          56m     2600:1f13:b66:8203:34e5::                ip-192-168-253-70.region-code.compute.internal  <none>           <none>
   coredns-85d5b4454c-tx6n8   1/1     Running   0          56m     2600:1f13:b66:8203:34e5::1               ip-192-168-253-70.region-code.compute.internal  <none>           <none>
   kube-proxy-btpbk           1/1     Running   0          5m36s   2600:1f13:b66:8200:11a5:ade0:c590:6ac8   ip-192-168-34-75.region-code.compute.internal   <none>           <none>
   kube-proxy-jjk2g           1/1     Running   0          5m33s   2600:1f13:b66:8203:4516:2080:8ced:1ca9   ip-192-168-253-70.region-code.compute.internal  <none>           <none>
   ```

1. Confirm that default services are assigned `IPv6` addresses\.

   ```
   kubectl get services -n kube-system -o wide
   ```

   An example output is as follows\.

   ```
   NAME       TYPE        CLUSTER-IP          EXTERNAL-IP   PORT(S)         AGE   SELECTOR
   kube-dns   ClusterIP   fd30:3087:b6c2::a   <none>        53/UDP,53/TCP   57m   k8s-app=kube-dns
   ```

1. \(Optional\) [Deploy a sample application](sample-deployment.md) or deploy the [AWS Load Balancer Controller](aws-load-balancer-controller.md) and a sample application to load balance [application](alb-ingress.md) or [network](network-load-balancing.md) traffic to `IPv6` Pods\.

1. After you've finished with the cluster and nodes that you created for this tutorial, you should clean up the resources that you created with the following command\.

   ```
   eksctl delete cluster my-cluster
   ```

------
#### [ AWS CLI ]

**Prerequisite**  
Version `2.12.3` or later or version `1.27.160` or later of the AWS Command Line Interface \(AWS CLI\) installed and configured on your device or AWS CloudShell\. To check your current version, use `aws --version | cut -d / -f2 | cut -d ' ' -f1`\. Package managers such `yum`, `apt-get`, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI\. To install the latest version, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with aws configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the *AWS Command Line Interface User Guide*\. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version\. To update it, see [Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the *AWS CloudShell User Guide*\. If you use the AWS CloudShell, you may need to [install version `2.12.3` or later or `1.27.160` or later of the AWS CLI](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software), because the default AWS CLI version installed in the AWS CloudShell may be an earlier version\.

**Important**  
You must complete all steps in this procedure as the same user\. To check the current user, run the following command:  

  ```
  aws sts get-caller-identity
  ```
You must complete all steps in this procedure in the same shell\. Several steps use variables set in previous steps\. Steps that use variables won't function properly if the variable values are set in a different shell\. If you use the [AWS CloudShell](https://docs.aws.amazon.com/cloudshell/latest/userguide/welcome.html) to complete the following procedure, remember that if you don't interact with it using your keyboard or pointer for approximately 20–30 minutes, your shell session ends\. Running processes do not count as interactions\.
The instructions are written for the Bash shell, and may need adjusting in other shells\.

**To create your cluster with the AWS CLI**

Replace all `example values` in the steps of this procedure with your own values\.

1. Run the following commands to set some variables used in later steps\. Replace `region-code` with the AWS Region that you want to deploy your resources in\. The value can be any AWS Region that is supported by Amazon EKS\. For a list of AWS Regions, see [Amazon EKS endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/eks.html) in the AWS General Reference guide\. Replace `my-cluster` with a name for your cluster\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can't be longer than 100 characters\. Replace `my-nodegroup` with a name for your node group\. The node group name can't be longer than 63 characters\. It must start with letter or digit, but can also include hyphens and underscores for the remaining characters\. Replace `111122223333` with your account ID\.

   ```
   export region_code=region-code
   export cluster_name=my-cluster
   export nodegroup_name=my-nodegroup
   export account_id=111122223333
   ```

1. Create an Amazon VPC with public and private subnets that meets Amazon EKS and `IPv6` requirements\.

   1. Run the following command to set a variable for your AWS CloudFormation stack name\. You can replace `my-eks-ipv6-vpc` with any name you choose\.

      ```
      export vpc_stack_name=my-eks-ipv6-vpc
      ```

   1. Create an `IPv6` VPC using an AWS CloudFormation template\.

      ```
      aws cloudformation create-stack --region $region_code --stack-name $vpc_stack_name \
        --template-url https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-ipv6-vpc-public-private-subnets.yaml
      ```

      The stack takes a few minutes to create\. Run the following command\. Don't continue to the next step until the output of the command is `CREATE_COMPLETE`\.

      ```
      aws cloudformation describe-stacks --region $region_code --stack-name $vpc_stack_name --query Stacks[].StackStatus --output text
      ```

   1. Retrieve the IDs of the public subnets that were created\.

      ```
      aws cloudformation describe-stacks --region $region_code --stack-name $vpc_stack_name \
          --query='Stacks[].Outputs[?OutputKey==`SubnetsPublic`].OutputValue' --output text
      ```

      An example output is as follows\.

      ```
      subnet-0a1a56c486EXAMPLE,subnet-099e6ca77aEXAMPLE
      ```

   1. Enable the auto\-assign `IPv6` address option for the public subnets that were created\.

      ```
      aws ec2 modify-subnet-attribute --region $region_code --subnet-id subnet-0a1a56c486EXAMPLE --assign-ipv6-address-on-creation
      aws ec2 modify-subnet-attribute --region $region_code --subnet-id subnet-099e6ca77aEXAMPLE --assign-ipv6-address-on-creation
      ```

   1.  Retrieve the names of the subnets and security groups created by the template from the deployed AWS CloudFormation stack and store them in variables for use in a later step\.

      ```
      security_groups=$(aws cloudformation describe-stacks --region $region_code --stack-name $vpc_stack_name \
          --query='Stacks[].Outputs[?OutputKey==`SecurityGroups`].OutputValue' --output text)
      
      public_subnets=$(aws cloudformation describe-stacks --region $region_code --stack-name $vpc_stack_name \
          --query='Stacks[].Outputs[?OutputKey==`SubnetsPublic`].OutputValue' --output text)
      
      private_subnets=$(aws cloudformation describe-stacks --region $region_code --stack-name $vpc_stack_name \
          --query='Stacks[].Outputs[?OutputKey==`SubnetsPrivate`].OutputValue' --output text)
      
      subnets=${public_subnets},${private_subnets}
      ```

1. Create a cluster IAM role and attach the required Amazon EKS IAM managed policy to it\. Kubernetes clusters managed by Amazon EKS make calls to other AWS services on your behalf to manage the resources that you use with the service\.

   1. Run the following command to create the `eks-cluster-role-trust-policy.json` file\.

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

   1. Run the following command to set a variable for your role name\. You can replace `myAmazonEKSClusterRole` with any name you choose\.

      ```
      export cluster_role_name=myAmazonEKSClusterRole
      ```

   1. Create the role\.

      ```
      aws iam create-role --role-name $cluster_role_name --assume-role-policy-document file://"eks-cluster-role-trust-policy.json"
      ```

   1. Retrieve the ARN of the IAM role and store it in a variable for a later step\.

      ```
      cluster_iam_role=$(aws iam get-role --role-name $cluster_role_name --query="Role.Arn" --output text)
      ```

   1. Attach the required Amazon EKS managed IAM policy to the role\.

      ```
      aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy --role-name $cluster_role_name
      ```

1. Create your cluster\.

   ```
   aws eks create-cluster --region $region_code --name $cluster_name --kubernetes-version 1.XX \
      --role-arn $cluster_iam_role --resources-vpc-config subnetIds=$subnets,securityGroupIds=$security_groups \
      --kubernetes-network-config ipFamily=ipv6
   ```

   1. 
**Note**  
You might receive an error that one of the Availability Zones in your request doesn't have sufficient capacity to create an Amazon EKS cluster\. If this happens, the error output contains the Availability Zones that can support a new cluster\. Retry creating your cluster with at least two subnets that are located in the supported Availability Zones for your account\. For more information, see [Insufficient capacity](troubleshooting.md#ICE)\.

     The cluster takes several minutes to create\. Run the following command\. Don't continue to the next step until the output from the command is `ACTIVE`\.

     ```
     aws eks describe-cluster --region $region_code --name $cluster_name --query cluster.status
     ```

1. Create or update a `kubeconfig` file for your cluster so that you can communicate with your cluster\.

   ```
   aws eks update-kubeconfig --region $region_code --name $cluster_name
   ```

   By default, the `config` file is created in `~/.kube` or the new cluster's configuration is added to an existing `config` file in `~/.kube`\.

1. Create a node IAM role\.

   1. Run the following command to create the `vpc-cni-ipv6-policy.json` file\.

      ```
      cat >vpc-cni-ipv6-policy <<EOF
      {
          "Version": "2012-10-17",
          "Statement": [
              {
                  "Effect": "Allow",
                  "Action": [
                      "ec2:AssignIpv6Addresses",
                      "ec2:DescribeInstances",
                      "ec2:DescribeTags",
                      "ec2:DescribeNetworkInterfaces",
                      "ec2:DescribeInstanceTypes"
                  ],
                  "Resource": "*"
              },
              {
                  "Effect": "Allow",
                  "Action": [
                      "ec2:CreateTags"
                  ],
                  "Resource": [
                      "arn:aws:ec2:*:*:network-interface/*"
                  ]
              }
          ]
      }
      EOF
      ```

   1. Create the IAM policy\.

      ```
      aws iam create-policy --policy-name AmazonEKS_CNI_IPv6_Policy --policy-document file://vpc-cni-ipv6-policy.json
      ```

   1. Run the following command to create the `node-role-trust-relationship.json` file\.

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

   1. Run the following command to set a variable for your role name\. You can replace `AmazonEKSNodeRole` with any name you choose\.

      ```
      export node_role_name=AmazonEKSNodeRole
      ```

   1. Create the IAM role\.

      ```
      aws iam create-role --role-name $node_role_name --assume-role-policy-document file://"node-role-trust-relationship.json"
      ```

   1. Attach the IAM policy to the IAM role\.

      ```
      aws iam attach-role-policy --policy-arn arn:aws:iam::$account_id:policy/AmazonEKS_CNI_IPv6_Policy \
          --role-name $node_role_name
      ```
**Important**  
For simplicity in this tutorial, the policy is attached to this IAM role\. In a production cluster however, we recommend attaching the policy to a separate IAM role\. For more information, see [Configuring the Amazon VPC CNI plugin for Kubernetes to use IAM roles for service accounts \(IRSA\)](cni-iam-role.md)\.

   1. Attach two required IAM managed policies to the IAM role\.

      ```
      aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy \
        --role-name $node_role_name
      aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly \
        --role-name $node_role_name
      ```

   1. Retrieve the ARN of the IAM role and store it in a variable for a later step\.

      ```
      node_iam_role=$(aws iam get-role --role-name $node_role_name --query="Role.Arn" --output text)
      ```

1. Create a managed node group\.

   1. View the IDs of the subnets that you created in a previous step\.

      ```
      echo $subnets
      ```

      An example output is as follows\.

      ```
      subnet-0a1a56c486EXAMPLE,subnet-099e6ca77aEXAMPLE,subnet-0377963d69EXAMPLE,subnet-0c05f819d5EXAMPLE
      ```

   1. Create the node group\. Replace `0a1a56c486EXAMPLE`, `099e6ca77aEXAMPLE`, `0377963d69EXAMPLE`, and `0c05f819d5EXAMPLE` with the values returned in the output of the previous step\. Be sure to remove the commas between subnet IDs from the previous output in the following command\. You can replace `t3.medium` with any [AWS Nitro System instance type](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html#ec2-nitro-instances)\.

      ```
      aws eks create-nodegroup --region $region_code --cluster-name $cluster_name --nodegroup-name $nodegroup_name \
          --subnets subnet-0a1a56c486EXAMPLE subnet-099e6ca77aEXAMPLE subnet-0377963d69EXAMPLE subnet-0c05f819d5EXAMPLE \
          --instance-types t3.medium --node-role $node_iam_role
      ```

      The node group takes a few minutes to create\. Run the following command\. Don't proceed to the next step until the output returned is `ACTIVE`\.

      ```
      aws eks describe-nodegroup --region $region_code --cluster-name $cluster_name --nodegroup-name $nodegroup_name \
          --query nodegroup.status --output text
      ```

1. Confirm that the default Pods are assigned `IPv6` addresses in the `IP` column\.

   ```
   kubectl get pods -n kube-system -o wide
   ```

   An example output is as follows\.

   ```
   NAME                       READY   STATUS    RESTARTS   AGE     IP                                       NODE                                            NOMINATED NODE   READINESS GATES
   aws-node-rslts             1/1     Running   1          5m36s   2600:1f13:b66:8200:11a5:ade0:c590:6ac8   ip-192-168-34-75.region-code.compute.internal   <none>           <none>
   aws-node-t74jh             1/1     Running   0          5m32s   2600:1f13:b66:8203:4516:2080:8ced:1ca9   ip-192-168-253-70.region-code.compute.internal  <none>           <none>
   coredns-85d5b4454c-cw7w2   1/1     Running   0          56m     2600:1f13:b66:8203:34e5::                ip-192-168-253-70.region-code.compute.internal  <none>           <none>
   coredns-85d5b4454c-tx6n8   1/1     Running   0          56m     2600:1f13:b66:8203:34e5::1               ip-192-168-253-70.region-code.compute.internal  <none>           <none>
   kube-proxy-btpbk           1/1     Running   0          5m36s   2600:1f13:b66:8200:11a5:ade0:c590:6ac8   ip-192-168-34-75.region-code.compute.internal   <none>           <none>
   kube-proxy-jjk2g           1/1     Running   0          5m33s   2600:1f13:b66:8203:4516:2080:8ced:1ca9   ip-192-168-253-70.region-code.compute.internal  <none>           <none>
   ```

1. Confirm that the default services are assigned `IPv6` addresses in the `IP` column\.

   ```
   kubectl get services -n kube-system -o wide
   ```

   An example output is as follows\.

   ```
   NAME       TYPE        CLUSTER-IP          EXTERNAL-IP   PORT(S)         AGE   SELECTOR
   kube-dns   ClusterIP   fd30:3087:b6c2::a   <none>        53/UDP,53/TCP   57m   k8s-app=kube-dns
   ```

1. \(Optional\) [Deploy a sample application](sample-deployment.md) or deploy the [AWS Load Balancer Controller](aws-load-balancer-controller.md) and a sample application to load balance [application](alb-ingress.md) or [network](network-load-balancing.md) traffic to `IPv6` Pods\.

1. After you've finished with the cluster and nodes that you created for this tutorial, you should clean up the resources that you created with the following commands\. Make sure that you're not using any of the resources outside of this tutorial before deleting them\.

   1. If you're completing this step in a different shell than you completed the previous steps in, set the values of all the variables used in previous steps, replacing the `example values` with the values you specified when you completed the previous steps\. If you're completing this step in the same shell that you completed the previous steps in, skip to the next step\.

      ```
      export region_code=region-code
      export vpc_stack_name=my-eks-ipv6-vpc
      export cluster_name=my-cluster
      export nodegroup_name=my-nodegroup
      export account_id=111122223333
      export node_role_name=AmazonEKSNodeRole
      export cluster_role_name=myAmazonEKSClusterRole
      ```

   1. Delete your node group\.

      ```
      aws eks delete-nodegroup --region $region_code --cluster-name $cluster_name --nodegroup-name $nodegroup_name
      ```

      Deletion takes a few minutes\. Run the following command\. Don't proceed to the next step if any output is returned\.

      ```
      aws eks list-nodegroups --region $region_code --cluster-name $cluster_name --query nodegroups --output text
      ```

   1. Delete the cluster\.

      ```
      aws eks delete-cluster --region $region_code --name $cluster_name
      ```

      The cluster takes a few minutes to delete\. Before continuing make sure that the cluster is deleted with the following command\.

      ```
      aws eks describe-cluster --region $region_code --name $cluster_name
      ```

      Don't proceed to the next step until your output is similar to the following output\.

      ```
      An error occurred (ResourceNotFoundException) when calling the DescribeCluster operation: No cluster found for name: my-cluster.
      ```

   1. Delete the IAM resources that you created\. Replace `AmazonEKS_CNI_IPv6_Policy` with the name you chose, if you chose a different name than the one used in previous steps\.

      ```
      aws iam detach-role-policy --role-name $cluster_role_name --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy
      aws iam detach-role-policy --role-name $node_role_name --policy-arn arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy
      aws iam detach-role-policy --role-name $node_role_name --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly
      aws iam detach-role-policy --role-name $node_role_name --policy-arn arn:aws:iam::$account_id:policy/AmazonEKS_CNI_IPv6_Policy
      aws iam delete-policy --policy-arn arn:aws:iam::$account_id:policy/AmazonEKS_CNI_IPv6_Policy
      aws iam delete-role --role-name $cluster_role_name
      aws iam delete-role --role-name $node_role_name
      ```

   1. Delete the AWS CloudFormation stack that created the VPC\.

      ```
      aws cloudformation delete-stack --region $region_code --stack-name $vpc_stack_name
      ```

------