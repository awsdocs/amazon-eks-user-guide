# Configuring the Amazon VPC CNI plugin to use IAM roles for service accounts<a name="cni-iam-role"></a>

The [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) is the networking plugin for pod networking in Amazon EKS clusters\. The plugin is responsible for allocating VPC IP addresses to Kubernetes nodes and configuring the necessary networking for pods on each node\. The plugin:
+ Requires IAM permissions\. If you're going to use IPv4 for your cluster, the permissions are provided by the `[AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor)` AWS managed policy\. If you're going to use [IPv6](cni-ipv6.md) for your cluster, then you'll create a custom IAM policy in the following procedure\. You can attach the policy to the [Amazon EKS node IAM role](create-node-role.md), or to a separate IAM role\. We recommend that you assign it to a separate role, as detailed in this topic\.
+ Creates and is configured to use a service account named `aws-node` when it's deployed\. The service account is bound to a Kubernetes `clusterrole` named `aws-node`, which is assigned the required Kubernetes permissions\.

**Note**  
Regardless of whether you configure the Amazon VPC CNI plugin to use IAM roles for service accounts, the pods also have access to the permissions assigned to the [Amazon EKS node IAM role](create-node-role.md), unless you block access to IMDS\. For more information, see [Restrict access to the instance profile assigned to the worker node](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node)\.

**Prerequisites**
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\.
+ An existing AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.

## Step 1: \(Optional\) Create IAM policy for IPv6<a name="cni-iam-role-create-ipv6-policy"></a>

If you created a 1\.21 or later cluster that uses the IPv6 family and the cluster has version 1\.10\.1 or later of the VPC CNI add\-on configured, then you need to create an IAM policy that you can assign to an IAM role in a later step\. If you have an existing 1\.21 or later cluster that you didn't configure with the IPv6 family when you created it, then to use IPv6, you must create a new cluster\. For more information about using IPv6 with your cluster, see [Assigning IPv6 addresses to pods and services](cni-ipv6.md)\.

1. Copy the following text and save it to a file named `vpc-cni-ipv6-policy.json`\.

   ```
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
   ```

1. Create the IAM policy\.

   ```
   aws iam create-policy \
       --policy-name AmazonEKS_CNI_IPv6_Policy \
       --policy-document file://vpc-cni-ipv6-policy.json
   ```

## Step 2: Create the Amazon VPC CNI plugin IAM role<a name="cni-iam-role-create-role"></a>

If you're using IPv4 for your cluster, you'll attach the `AmazonEKS_CNI_Policy` managed IAM policy to the role\. If you're using IPv6 for your cluster, you'll attach the [*AmazonEKS\_CNI\_IPv6\_Policy*](#cni-iam-role-create-ipv6-policy)\.

You can use `eksctl` or the AWS Management Console to create your CNI plugin IAM role\.

------
#### [ eksctl ]

1. Create an IAM role and attach the IAM policy to the role with the following command\.  Replace *`my-cluster`* with your own value\. This command creates and deploys an AWS CloudFormation stack that creates an IAM role, attaches the policy that you specify to it, and annotates the existing `aws-node` service account with the ARN of the IAM role that is created\.

   ```
   eksctl create iamserviceaccount \
       --name aws-node \
       --namespace kube-system \
       --cluster my-cluster \
       --attach-policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy \
       --approve \
       --override-existing-serviceaccounts
   ```

1. \(Optional\) Add an annotation to your service account to use the AWS Security Token Service AWS Regional endpoint, rather than the global endpoint\. For more information see [Associate an IAM role to a service account](specify-service-account-role.md#sts-regional-endpoint)\.

1. View your running Amazon VPC CNI pods\.

   ```
   kubectl get pods -n kube-system  -l k8s-app=aws-node
   ```

1. Describe one of the pods and verify that the `AWS_WEB_IDENTITY_TOKEN_FILE` and `AWS_ROLE_ARN` environment variables exist\. Replace *9rgzw* with the name of one of your pods returned in the output of the previous step\.

   ```
   kubectl exec -n kube-system aws-node-9rgzw -c aws-node -- env | grep AWS
   ```

   Output:

   ```
   ...
   AWS_WEB_IDENTITY_TOKEN_FILE=/var/run/secrets/eks.amazonaws.com/serviceaccount/token
   ...
   AWS_ROLE_ARN=arn:arn:aws::111122223333:role/eksctl-prod-addon-iamserviceaccount-kube-sys-Role1-V66K5I6JLDGK
   
   ...
   ```

   If you added the annotation to your service account to use the AWS Security Token Service AWS Regional endpoint, rather than the global endpoint, then verify that the following line is also returned in the previous output\.

   ```
   AWS_STS_REGIONAL_ENDPOINTS=regional
   ```

------
#### [ AWS Management Console ]

**Prerequisite**  
An existing AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.<a name="configure-cni-iam-console-create-iam-account"></a>

**To create your CNI plugin IAM role with the AWS Management Console**

1. In the left navigation pane, choose **Roles**\. Then choose **Create role**\.

1. In the **Trusted entity type** section, choose **Web identity**\.

1. In the **Web identity** section:

   1. For **Identity provider**, choose the URL for your cluster\.

   1. For **Audience**, choose `sts.amazonaws.com`\.

1. Choose **Next**\.

1. In the **Filter policies** box, enter `[AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor)` or *AmazonEKS\_CNI\_IPv6\_Policy* and then select the check box to the left of the policy name returned in the search\.

1. Choose **Next**\.

1. For **Role name**, enter a unique name for your role, such as **AmazonEKSCNIRole**\.

1. For **Description**, enter descriptive text such as **Amazon EKS \- CNI role**\.

1. Choose **Create role**\.

1. After the role is created, choose the role in the console to open it for editing\.

1. Choose the **Trust relationships** tab, and then choose **Edit trust policy**\.

1. Find the line that looks similar to the following:

   ```
   "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E:aud": "sts.amazonaws.com"
   ```

   Change the line to look like the following line\. Replace *`EXAMPLED539D4633E53DE1B716D3041E`* with your cluster's OIDC provider ID, replace *region\-code* with the AWS Region code that your cluster is in, and be sure to change `aud` \(from the previous output\) to `sub` in the following string\.

   ```
   "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E:sub": "system:serviceaccount:kube-system:aws-node"
   ```

1. Choose **Update policy** to finish\.<a name="configure-cni-iam-console-patch-service-account"></a>

**To annotate the `aws-node` Kubernetes service account with the IAM role**

1. If you're using the Amazon EKS add\-on with a 1\.18 or later Amazon EKS cluster, see [Updating the Amazon VPC CNI Amazon EKS add\-on](managing-vpc-cni.md#updating-vpc-cni-eks-add-on), instead of completing this procedure\. If you're not using the Amazon VPC CNI Amazon EKS add\-on, then use the following command to annotate the `aws-node` service account with the ARN of the IAM role that you created previously\. Replace the `example values` with your own values\.

   ```
   kubectl annotate serviceaccount \
       -n kube-system aws-node \
       eks.amazonaws.com/role-arn=arn:aws:iam::AWS_ACCOUNT_ID:role/AmazonEKSCNIRole
   ```

1. \(Optional\) Add an additional annotation to your service account to use the AWS Security Token Service AWS Regional endpoint, rather than the global endpoint\. For more information see [Associate an IAM role to a service account](specify-service-account-role.md#sts-regional-endpoint)\.

1. Delete and re\-create any existing pods that are associated with the service account to apply the credential environment variables\. The mutating web hook does not apply them to pods that are already running\. The following command deletes the existing the `aws-node` DaemonSet pods and deploys them with the service account annotation\.

   ```
   kubectl delete pods -n kube-system -l k8s-app=aws-node
   ```

1. Confirm that the pods all restarted\.

   ```
   kubectl get pods -n kube-system  -l k8s-app=aws-node
   ```

1. Describe one of the pods and verify that the `AWS_WEB_IDENTITY_TOKEN_FILE` and `AWS_ROLE_ARN` environment variables exist\. Replace *9rgzw* with the name of one of your pods returned in the output of the previous step\.

   ```
   kubectl exec -n kube-system aws-node-9rgzw -c aws-node -- env | grep AWS
   ```

   Output:

   ```
   ...
   AWS_WEB_IDENTITY_TOKEN_FILE=/var/run/secrets/eks.amazonaws.com/serviceaccount/token
   ...
   AWS_ROLE_ARN=arn:arn:aws::111122223333:role/eksctl-prod-addon-iamserviceaccount-kube-sys-Role1-V66K5I6JLDGK
   
   ...
   ```

   If you added the annotation to your service account to use the AWS Security Token Service AWS Regional endpoint, rather than the global endpoint, then verify that the following line is also returned in the previous output\.

   ```
   AWS_STS_REGIONAL_ENDPOINTS=regional
   ```

------

## Remove the CNI policy from the node IAM role<a name="remove-cni-policy-node-iam-role"></a>

If your [Amazon EKS node IAM role](create-node-role.md) currently has the `AmazonEKS_CNI_Policy` IAM policy or an [IPv6 policy](#cni-iam-role-create-ipv6-policy) attached to it, and you've created a separate IAM role, attached the policy to it instead, and assigned it to the `aws-node` Kubernetes service account, then we recommend that you remove the policy from your node role\.

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the left navigation pane, choose **Roles**, and then search for your node instance role\.

1. Choose the **Permissions** tab for your node instance role and then choose the **X** to the right of the `[AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor)` or *AmazonEKS\_CNI\_IPv6\_Policy*\.

1. Choose **Detach** to finish\.