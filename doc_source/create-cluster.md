# Creating an Amazon EKS Cluster<a name="create-cluster"></a>

This topic walks you through creating an Amazon EKS cluster\.

If this is your first time creating an Amazon EKS cluster, we recommend that you follow one of our [Getting Started with Amazon EKS](getting-started.md) guides instead\. They provide complete end\-to\-end walkthroughs for creating an Amazon EKS cluster with worker nodes\.

**Important**  
When an Amazon EKS cluster is created, the IAM entity \(user or role\) that creates the cluster is added to the Kubernetes RBAC authorization table as the administrator \(with `system:master` permissions\. Initially, only that IAM user can make calls to the Kubernetes API server using kubectl\. For more information, see [Managing Users or IAM Roles for your Cluster](add-user-role.md)\. If you use the console to create the cluster, you must ensure that the same IAM user credentials are in the AWS SDK credential chain when you are running kubectl commands on your cluster\.  
If you install and configure the AWS CLI, you can configure the IAM credentials for your user\. If the AWS CLI is configured properly for your user, then `eksctl` and the [AWS IAM Authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator) can find those credentials as well\. For more information, see [Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) in the *AWS Command Line Interface User Guide*\.

Choose the tab below that corresponds to your desired cluster creation method:

------
#### [ eksctl ]

**To create your cluster with `eksctl`**

1. Choose a tab below that matches your workload requirements\. If you want to create a cluster that only runs pods on AWS Fargate, choose **AWS Fargate\-only cluster**\. If you only intend to run Linux workloads on your cluster, choose **Cluster with Linux\-only workloads**\. If you want to run Linux and Windows workloads on your cluster, choose **Cluster with Linux and Windows workloads**\.

------
#### [ AWS Fargate\-only cluster ]

   This procedure assumes that you have installed `eksctl`, and that your `eksctl` version is at least `0.15.0-rc.2`\. You can check your version with the following command:

   ```
   eksctl version
   ```

    For more information on installing or upgrading `eksctl`, see [Installing or Upgrading `eksctl`](eksctl.md#installing-eksctl)\.

   Create your Amazon EKS cluster with Fargate support with the following command\. Replace the example *values* with your own values\. For `--region`, specify a [supported region](fargate.md)\.

   ```
   eksctl create cluster \
   --name prod \
   --region region-code \
   --fargate
   ```

   Your new Amazon EKS cluster is created without a worker node group\. However, `eksctl` creates a pod execution role, a Fargate profile for the `default` and `kube-system` namespaces, and it patches the `coredns` deployment so that it can run on Fargate\. For more information see [AWS Fargate](fargate.md)\.

------
#### [ Cluster with Linux\-only workloads ]

   This procedure assumes that you have installed `eksctl`, and that your `eksctl` version is at least `0.15.0-rc.2`\. You can check your version with the following command:

   ```
   eksctl version
   ```

    For more information on installing or upgrading `eksctl`, see [Installing or Upgrading `eksctl`](eksctl.md#installing-eksctl)\.

   Create your Amazon EKS cluster and Linux worker nodes with the following command\. Replace the example *values* with your own values\.

**Important**  
Kubernetes version 1\.12 is now deprecated on Amazon EKS\. On **May 11th, 2020**, Kubernetes version 1\.12 will no longer be supported on Amazon EKS\. On this date, you will no longer be able to create new 1\.12 clusters, and all existing Amazon EKS clusters running Kubernetes version 1\.12 will eventually be automatically updated to version 1\.13\. We recommend that you update any 1\.12 clusters to version 1\.13 or later in order to avoid service interruption\. For more information, see [Amazon EKS Version Deprecation](kubernetes-versions.md#version-deprecation)\.  
Kubernetes API versions available through Amazon EKS are officially supported by AWS, until we remove the ability to create clusters using that version\. This is true even if upstream Kubernetes is no longer supporting a version available on Amazon EKS\. We backport security fixes that are applicable to the Kubernetes versions supported on Amazon EKS\. Existing clusters are always supported, and Amazon EKS will automatically update your cluster to a supported version if you have not done so manually by the version end of life date\.

   ```
   eksctl create cluster \
   --name prod \
   --region region-code \
   --nodegroup-name standard-workers \
   --node-type t3.medium \
   --nodes 3 \
   --nodes-min 1 \
   --nodes-max 4 \
   --ssh-access \
   --ssh-public-key my-public-key.pub \
   --managed
   ```

**Note**  
The `--managed` option for Amazon EKS [Managed Node Groups](managed-node-groups.md) is currently only supported on Kubernetes 1\.14 and later clusters\. We recommend that you use the latest version of Kubernetes that is available in Amazon EKS to take advantage of the latest features\. If you choose to use an earlier Kubernetes version, you must remove the `--managed` option\.  
For more information on the available options for eksctl create cluster, see the project [README on GitHub](https://github.com/weaveworks/eksctl/blob/master/README.md) or view the help page with the following command\.  

     ```
     eksctl create cluster --help
     ```
Though `--ssh-public-key` is optional, we highly recommend that you specify it when you create your node group with a cluster\. This option enables SSH access to the nodes in your managed node group\. Enabling SSH access allows you to connect to your instances and gather diagnostic information if there are issues\. You cannot enable remote access after the node group is created\. For more information, about keys, see [Amazon EC2 Key Pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) in the Amazon EC2 User Guide for Linux Instances\.

   Output:

   You'll see several lines of output as the cluster and worker nodes are created\. The last line of output is similar to the following example line\.

   ```
   [✓]  EKS cluster "prod" in "region-code" region is ready
   ```

------
#### [ Cluster with Linux and Windows workloads ]

   This procedure assumes that you have installed `eksctl`, and that your `eksctl` version is at least `0.15.0-rc.2`\. You can check your version with the following command:

   ```
   eksctl version
   ```

   For more information on installing or upgrading `eksctl`, see [Installing or Upgrading `eksctl`](eksctl.md#installing-eksctl)\.

   Familiarize yourself with the Windows support [considerations](windows-support.md#considerations), which include supported values for `instanceType` in the example text below\. Replace the example *values* with your own values\. Save the text below to a file named `cluster-spec.yaml`\. The configuration file is used to create a cluster and both Linux and Windows worker node groups\. Even if you only want to run Windows workloads in your cluster, all Amazon EKS clusters must contain at least one Linux worker node\. We recommend that you create at least two worker nodes in each node group for availability purposes\. The minimum required Kubernetes version for Windows workloads is 1\.14\.

   ```
   ---
   apiVersion: eksctl.io/v1alpha5
   kind: ClusterConfig
   
   metadata:
     name: windows-prod
     region: region-code
   managedNodeGroups:
     - name: linux-ng
       instanceType: t2.large
       minSize: 2
   
   nodeGroups:
     - name: windows-ng
       instanceType: m5.large
       minSize: 2
       volumeSize: 100
       amiFamily: WindowsServer2019FullContainer
   ```

   Create your Amazon EKS cluster and Windows and Linux worker nodes with the following command\.

   ```
   eksctl create cluster -f cluster-spec.yaml --install-vpc-controllers
   ```

**Note**  
The `managedNodeGroups` option for Amazon EKS [Managed Node Groups](managed-node-groups.md) is currently only supported on Kubernetes 1\.14 and later clusters\. We recommend that you use the latest version of Kubernetes that is available in Amazon EKS to take advantage of the latest features\. If you choose to use an earlier Kubernetes version, you must remove the `--managed` option\.  
For more information on the available options for eksctl create cluster, see the project [README on GitHub](https://github.com/weaveworks/eksctl/blob/master/README.md) or view the help page with the following command\.  

   ```
   eksctl create cluster --help
   ```

   Output:

   You'll see several lines of output as the cluster and worker nodes are created\. The last line of output is similar to the following example line\.

   ```
   [✓]  EKS cluster "windows-prod" in "region-code" region is ready
   ```

------

1. Cluster provisioning usually takes between 10 and 15 minutes\. When your cluster is ready, test that your `kubectl` configuration is correct\.

   ```
   kubectl get svc
   ```
**Note**  
If you receive the error `"aws-iam-authenticator": executable file not found in $PATH`, your kubectl isn't configured for Amazon EKS\. For more information, see [Installing `aws-iam-authenticator`](install-aws-iam-authenticator.md)\.  
If you receive any other authorization or resource type errors, see [Unauthorized or Access Denied \(`kubectl`\)](troubleshooting.md#unauthorized) in the troubleshooting section\.

   Output:

   ```
   NAME             TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
   svc/kubernetes   ClusterIP   10.100.0.1   <none>        443/TCP   1m
   ```

1. \(Linux GPU workers only\) If you chose a GPU instance type and the Amazon EKS\-optimized AMI with GPU support, you must apply the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) as a DaemonSet on your cluster with the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/1.0.0-beta/nvidia-device-plugin.yml
   ```

------
#### [ AWS Management Console ]

**To create your cluster with the console**

This procedure has the following prerequisites:
+ You have created a VPC and a dedicated security group that meet the requirements for an Amazon EKS cluster\. For more information, see [Cluster VPC Considerations](network_reqs.md) and [Amazon EKS Security Group Considerations](sec-group-reqs.md)\. The [Getting Started with the AWS Management Console](getting-started-console.md) guide creates a VPC that meets the requirements, or you can also follow [Creating a VPC for Your Amazon EKS Cluster](create-public-private-vpc.md) to create one\.
+ You have created an Amazon EKS service role to apply to your cluster\. The [Getting Started with Amazon EKS](getting-started.md) guide creates a service role for you, or you can also follow [Amazon EKS IAM Roles](security_iam_service-with-iam.md#security_iam_service-with-iam-roles) to create one manually\.

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose **Create cluster**\.
**Note**  
If your IAM user doesn't have administrative privileges, you must explicitly add permissions for that user to call the Amazon EKS API operations\. For more information, see [Amazon EKS Identity\-Based Policy Examples](security_iam_id-based-policy-examples.md)\.

1. On the **Create cluster** page, fill in the following fields and then choose **Create**:
   + **Cluster name** – A unique name for your cluster\.
   + **Kubernetes version** – The version of Kubernetes to use for your cluster\. Unless you require a specific Kubernetes version for your application, we recommend that you use the latest version available in Amazon EKS\.
**Important**  
Kubernetes version 1\.12 is now deprecated on Amazon EKS\. On **May 11th, 2020**, Kubernetes version 1\.12 will no longer be supported on Amazon EKS\. On this date, you will no longer be able to create new 1\.12 clusters, and all existing Amazon EKS clusters running Kubernetes version 1\.12 will eventually be automatically updated to version 1\.13\. We recommend that you update any 1\.12 clusters to version 1\.13 or later in order to avoid service interruption\. For more information, see [Amazon EKS Version Deprecation](kubernetes-versions.md#version-deprecation)\.  
Kubernetes API versions available through Amazon EKS are officially supported by AWS, until we remove the ability to create clusters using that version\. This is true even if upstream Kubernetes is no longer supporting a version available on Amazon EKS\. We backport security fixes that are applicable to the Kubernetes versions supported on Amazon EKS\. Existing clusters are always supported, and Amazon EKS will automatically update your cluster to a supported version if you have not done so manually by the version end of life date\.
   + **Role name** – Choose the Amazon EKS service role to allow Amazon EKS and the Kubernetes control plane to manage AWS resources on your behalf\. For more information, see [Amazon EKS IAM Roles](security_iam_service-with-iam.md#security_iam_service-with-iam-roles)\.
   + **VPC** – The VPC to use for your cluster\.
   + **Subnets** – The subnets within the preceding VPC to use for your cluster\. By default, the available subnets in the VPC are preselected\. Specify all subnets that will host resources for your cluster \(such as private subnets for worker nodes and public subnets for load balancers\)\. Your subnets must meet the requirements for an Amazon EKS cluster\. For more information, see [Cluster VPC Considerations](network_reqs.md)\.
   + **Security Groups**: The **SecurityGroups** value from the AWS CloudFormation output that you generated with [Create your Amazon EKS Cluster VPC](getting-started-console.md#vpc-create)\. This security group has **ControlPlaneSecurityGroup** in the drop\-down name\.
**Important**  
The worker node AWS CloudFormation template modifies the security group that you specify here, so **Amazon EKS strongly recommends that you use a dedicated security group for each cluster control plane \(one per cluster\)**\. If this security group is shared with other resources, you might block or disrupt connections to those resources\.
   + **Endpoint private access** – Choose whether to enable or disable private access for your cluster's Kubernetes API server endpoint\. If you enable private access, Kubernetes API requests that originate from within your cluster's VPC use the private VPC endpoint\. For more information, see [Amazon EKS Cluster Endpoint Access Control](cluster-endpoint.md)\.
   + **Endpoint public access** – Choose whether to enable or disable public access for your cluster's Kubernetes API server endpoint\. If you disable public access, your cluster's Kubernetes API server can receive only requests from within the cluster VPC\. For more information, see [Amazon EKS Cluster Endpoint Access Control](cluster-endpoint.md)\.
   + **Secrets encryption** – Choose whether to enable or disable envelope encryption of Kubernetes secrets using AWS Key Management Service \(AWS KMS\)\. If you enable envelope encryption, the Kubernetes secrets are encrypted using the customer master key \(CMK\) that you select\. The CMK must be symmetric, created in the same region as the cluster, and if the CMK was created in a different account, the user must have access to the CMK\. For more information, see [Allowing Users in Other Accounts to Use a CMK](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html) in the *AWS Key Management Service Developer Guide*\. Kubernetes secrets encryption with an AWS KMS CMK requires Kubernetes version 1\.13 or later\.
   + **Logging** – For each individual log type, choose whether the log type should be **Enabled** or **Disabled**\. By default, each log type is **Disabled**\. For more information, see [Amazon EKS Control Plane Logging](control-plane-logs.md)\.
   + **Tags** – \(Optional\) Add any tags to your cluster\. For more information, see [Tagging Your Amazon EKS Resources](eks-using-tags.md)\.
**Note**  
You might receive an error that one of the Availability Zones in your request doesn't have sufficient capacity to create an Amazon EKS cluster\. If this happens, the error output contains the Availability Zones that can support a new cluster\. Retry creating your cluster with at least two subnets that are located in the supported Availability Zones for your account\. For more information, see [Insufficient Capacity](troubleshooting.md#ICE)\.

1. On the **Clusters** page, choose the name of your new cluster to view the cluster information\.

1. The **Status** field shows **CREATING** until the cluster provisioning process completes\. When your cluster provisioning is complete \(usually between 10 and 15 minutes\), note the **API server endpoint** and **Certificate authority** values\. These are used in your kubectl configuration\.

1. Now that you have created your cluster, follow the procedures in [Installing `aws-iam-authenticator`](install-aws-iam-authenticator.md) and [Create a `kubeconfig` for Amazon EKS](create-kubeconfig.md) to enable communication with your new cluster\.

1. \(Optional\) If you want to run pods on AWS Fargate in your cluster, see [Getting Started with AWS Fargate on Amazon EKS](fargate-getting-started.md)\.

1. After you enable communication, follow the procedures in [Launching Amazon EKS Linux Worker Nodes](launch-workers.md) to add Linux worker nodes to your cluster to support your workloads\.

1. \(Optional\) After you add Linux worker nodes to your cluster, follow the procedures in [Windows Support](windows-support.md) to add Windows support to your cluster and to add Windows worker nodes\. All Amazon EKS clusters must contain at least one Linux worker node, even if you only want to run Windows workloads in your cluster\.

------
#### [ AWS CLI ]

**To create your cluster with the AWS CLI**

This procedure has the following prerequisites:
+ You have created a VPC and a dedicated security group that meets the requirements for an Amazon EKS cluster\. For more information, see [Cluster VPC Considerations](network_reqs.md) and [Amazon EKS Security Group Considerations](sec-group-reqs.md)\. The [Getting Started with the AWS Management Console](getting-started-console.md) guide creates a VPC that meets the requirements, or you can also follow [Creating a VPC for Your Amazon EKS Cluster](create-public-private-vpc.md) to create one\.
+ You have created an Amazon EKS service role to apply to your cluster\. The [Getting Started with Amazon EKS](getting-started.md) guide creates a service role for you, or you can also follow [Amazon EKS IAM Roles](security_iam_service-with-iam.md#security_iam_service-with-iam-roles) to create one manually\.

1. Create your cluster with the following command\. Substitute your cluster name, the Amazon Resource Name \(ARN\) of your Amazon EKS service role that you created in [Create your Amazon EKS Service Role](getting-started-console.md#role-create), and the subnet and security group IDs for the VPC that you created in [Create your Amazon EKS Cluster VPC](getting-started-console.md#vpc-create)\.
**Important**  
Kubernetes version 1\.12 is now deprecated on Amazon EKS\. On **May 11th, 2020**, Kubernetes version 1\.12 will no longer be supported on Amazon EKS\. On this date, you will no longer be able to create new 1\.12 clusters, and all existing Amazon EKS clusters running Kubernetes version 1\.12 will eventually be automatically updated to version 1\.13\. We recommend that you update any 1\.12 clusters to version 1\.13 or later in order to avoid service interruption\. For more information, see [Amazon EKS Version Deprecation](kubernetes-versions.md#version-deprecation)\.  
Kubernetes API versions available through Amazon EKS are officially supported by AWS, until we remove the ability to create clusters using that version\. This is true even if upstream Kubernetes is no longer supporting a version available on Amazon EKS\. We backport security fixes that are applicable to the Kubernetes versions supported on Amazon EKS\. Existing clusters are always supported, and Amazon EKS will automatically update your cluster to a supported version if you have not done so manually by the version end of life date\.

   ```
   aws eks --region region-code create-cluster \
      --name devel --kubernetes-version 1.15 \
      --role-arn \
         arn:aws:iam::111122223333:role/eks-service-role-AWSServiceRoleForAmazonEKS-EXAMPLEBKZRQR \
      --resources-vpc-config \
         subnetIds=subnet-a9189fe2,subnet-50432629,securityGroupIds=sg-f5c54184
   ```
**Important**  
If you receive a syntax error similar to the following, you might be using a preview version of the AWS CLI for Amazon EKS\. The syntax for many Amazon EKS commands has changed since the public service launch\. Update your AWS CLI version to the latest available and delete the custom service model directory at `~/.aws/models/eks`\.  

   ```
   aws: error: argument --cluster-name is required
   ```
**Note**  
If your IAM user doesn't have administrative privileges, you must explicitly add permissions for that user to call the Amazon EKS API operations\. For more information, see [Amazon EKS Identity\-Based Policy Examples](security_iam_id-based-policy-examples.md)\.

   Output:

   ```
   {
       "cluster": {
           "name": "devel",
           "arn": "arn:aws:eks:region-code:111122223333:cluster/devel",
           "createdAt": 1527785885.159,
           "version": "1.15",
           "roleArn": "arn:aws:iam::111122223333:role/eks-service-role-AWSServiceRoleForAmazonEKS-AFNL4H8HB71F",
           "resourcesVpcConfig": {
               "subnetIds": [
                   "subnet-a9189fe2",
                   "subnet-50432629"
               ],
               "securityGroupIds": [
                   "sg-f5c54184"
               ],
               "vpcId": "vpc-a54041dc",
               "endpointPublicAccess": true,
               "endpointPrivateAccess": false
           },
           "status": "CREATING",
           "certificateAuthority": {}
       }
   }
   ```
**Note**  
You might receive an error that one of the Availability Zones in your request doesn't have sufficient capacity to create an Amazon EKS cluster\. If this happens, the error output contains the Availability Zones that can support a new cluster\. Retry creating your cluster with at least two subnets that are located in the supported Availability Zones for your account\. For more information, see [Insufficient Capacity](troubleshooting.md#ICE)\.

   To encrypt the Kubernetes secrets with a customer master key \(CMK\) from AWS Key Management Service \(AWS KMS\), first create a CMK using the [create\-key](https://docs.aws.amazon.com/goto/aws-cli/kms-2014-11-01/CreateKey) operation\.

   ```
   MY_KEY_ARN=$(aws kms create-key --query KeyMetadata.Arn —output text)
   ```

   Add the `--encryption-config` parameter to the `aws eks create-cluster` command\. Encryption of Kubernetes secrets can only be enabled when the cluster is created\.

   ```
   --encryption-config '[{"resources":["secrets"],"provider":{"keyArn":"$MY_KEY_ARN"}}]'
   ```

   The `keyArn` member can contain either the alias or ARN of your CMK\. The CMK must be symmetric, created in the same region as the cluster, and if the CMK was created in a different account, the user must have access to the CMK\. For more information, see [Allowing Users in Other Accounts to Use a CMK](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html) in the *AWS Key Management Service Developer Guide*\. Kubernetes secrets encryption with an AWS KMS CMK requires Kubernetes version 1\.13 or later\.

1. Cluster provisioning usually takes between 10 and 15 minutes\. You can query the status of your cluster with the following command\. When your cluster status is `ACTIVE`, you can proceed\.

   ```
   aws eks --region region-code describe-cluster --name devel --query "cluster.status"
   ```

1. When your cluster provisioning is complete, retrieve the `endpoint` and `certificateAuthority.data` values with the following commands\. You must add these values to your kubectl configuration so that you can communicate with your cluster\.

   1. Retrieve the `endpoint`\.

      ```
      aws eks --region region-code describe-cluster --name devel  --query "cluster.endpoint" --output text
      ```

   1. Retrieve the `certificateAuthority.data`\.

      ```
      aws eks --region region-code describe-cluster --name devel  --query "cluster.certificateAuthority.data" --output text
      ```

1. Now that you have created your cluster, follow the procedures in [Installing `aws-iam-authenticator`](install-aws-iam-authenticator.md) and [Create a `kubeconfig` for Amazon EKS](create-kubeconfig.md) to enable communication with your new cluster\.

1. \(Optional\) If you want to run pods on AWS Fargate in your cluster, see [Getting Started with AWS Fargate on Amazon EKS](fargate-getting-started.md)\.

1. After you enable communication, follow the procedures in [Launching Amazon EKS Linux Worker Nodes](launch-workers.md) to add worker nodes to your cluster to support your workloads\.

1. \(Optional\) After you add Linux worker nodes to your cluster, follow the procedures in [Windows Support](windows-support.md) to add Windows support to your cluster and to add Windows worker nodes\. All Amazon EKS clusters must contain at least one Linux worker node, even if you only want to run Windows workloads in your cluster\.

------