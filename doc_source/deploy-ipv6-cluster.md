# Deploying an Amazon EKS `IPv6` cluster and managed Amazon Linux nodes<a name="deploy-ipv6-cluster"></a>

In this tutorial, you deploy an `IPv6` Amazon VPC, an Amazon EKS cluster with the `IPv6` family, and a managed node group with Amazon EC2 Amazon Linux nodes\. You can't deploy Amazon EC2 Windows nodes in an `IPv6` cluster\. You can also deploy Fargate nodes to your cluster, though those instructions aren't provided in this topic for simplicity\. 

Complete the following before you start the tutorial:

Install and configure the following tools and resources that you need to create and manage an Amazon EKS cluster\.
+ We recommend that you familiarize yourself with all settings and deploy a cluster with the settings that meet your requirements\. For more information, see [Create an Amazon EKS cluster](create-cluster.md), [Simplify node lifecycle with managed node groups](managed-node-groups.md) and the [considerations](cni-ipv6.md#ipv6-considerations) for this topic\. You can only enable some settings when creating your cluster\.
+ The `kubectl` command line tool is installed on your device or AWS CloudShell\. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster\. For example, if your cluster version is `1.30`, you can use `kubectl` version `1.29`, `1.30`, or `1.31` with it\. To install or upgrade `kubectl`, see [Set up `kubectl` and `eksctl`](install-kubectl.md)\.
+ The IAM security principal that you're using must have permissions to work with Amazon EKS IAM roles, service linked roles, AWS CloudFormation, a VPC, and related resources\. For more information, see [Actions, resources, and condition keys for Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html) and [Using service\-linked roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html) in the IAM User Guide\.
+ If you use the eksctl, install version `0.191.0` or later on your computer\. To install or update to it, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.

## Procedure<a name="deploy-ipv6-cluster-procedure"></a>

You can use the eksctl or CLI to deploy an `IPv6` cluster\.

------
#### [ eksctl ]

1. Create the `ipv6-cluster.yaml` file\. Copy the command that follows to your device\. Make the following modifications to the command as needed and then run the modified command:
   + Replace `my-cluster` with a name for your cluster\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphanumeric character and can't be longer than 100 characters\. The name must be unique within the AWS Region and AWS account that you're creating the cluster in\.
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

1. Run the following commands to set some variables used in later steps\. Replace `region-code` with the AWS Region that you want to deploy your resources in\. The value can be any AWS Region that is supported by Amazon EKS\. For a list of AWS Regions, see [Amazon EKS endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/eks.html) in the AWS General Reference guide\. Replace `my-cluster` with a name for your cluster\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphanumeric character and can't be longer than 100 characters\. The name must be unique within the AWS Region and AWS account that you're creating the cluster in\. Replace `my-nodegroup` with a name for your node group\. The node group name can't be longer than 63 characters\. It must start with letter or digit, but can also include hyphens and underscores for the remaining characters\. Replace `111122223333` with your account ID\.

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
      CLUSTER_IAM_ROLE=$(aws iam get-role --role-name $cluster_role_name --query="Role.Arn" --output text)
      ```

   1. Attach the required Amazon EKS managed IAM policy to the role\.

      ```
      aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy --role-name $cluster_role_name
      ```

1. Create your cluster\.

   ```
   aws eks create-cluster --region $region_code --name $cluster_name --kubernetes-version 1.XX \
      --role-arn $CLUSTER_IAM_ROLE --resources-vpc-config subnetIds=$subnets,securityGroupIds=$security_groups \
      --kubernetes-network-config ipFamily=ipv6
   ```

   1. 
**Note**  
You might receive an error that one of the Availability Zones in your request doesn't have sufficient capacity to create an Amazon EKS cluster\. If this happens, the error output contains the Availability Zones that can support a new cluster\. Retry creating your cluster with at least two subnets that are located in the supported Availability Zones for your account\. For more information, see [Insufficient capacity](troubleshooting.md#ice)\.

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
For simplicity in this tutorial, the policy is attached to this IAM role\. In a production cluster however, we recommend attaching the policy to a separate IAM role\. For more information, see [Configure Amazon VPC CNI plugin to use IRSA](cni-iam-role.md)\.

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