# Configuring the Amazon VPC CNI plugin for Kubernetes to use IAM roles for service accounts \(IRSA\)<a name="cni-iam-role"></a>

The [https://github.com/aws/amazon-vpc-cni-k8s](https://github.com/aws/amazon-vpc-cni-k8s) is the networking plugin for Pod networking in Amazon EKS clusters\. The plugin is responsible for allocating VPC IP addresses to Kubernetes nodes and configuring the necessary networking for Pods on each node\. The plugin:
+ Requires AWS Identity and Access Management \(IAM\) permissions\. If your cluster uses the IPv4 family, the permissions are specified in the `[AmazonEKS\_CNI\_Policy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKS_CNI_Policy.html)` AWS managed policy\. If your cluster uses the IPv6 family, then the permissions must be added to an [IAM policy that you create](#cni-iam-role-create-ipv6-policy)\. You can attach the policy to the [Amazon EKS node IAM role](create-node-role.md), or to a separate IAM role\. We recommend that you assign it to a separate role, as detailed in this topic\.
+ Creates and is configured to use a Kubernetes service account named `aws-node` when it's deployed\. The service account is bound to a Kubernetes `clusterrole` named `aws-node`, which is assigned the required Kubernetes permissions\.

**Note**  
The Pods for the Amazon VPC CNI plugin for Kubernetes have access to the permissions assigned to the [Amazon EKS node IAM role](create-node-role.md), unless you block access to IMDS\. For more information, see [Restrict access to the instance profile assigned to the worker node](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node)\.

**Prerequisites**
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\.
+ An existing AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.

## Step 1: Create the Amazon VPC CNI plugin for Kubernetes IAM role<a name="cni-iam-role-create-role"></a>

**To create the IAM role**

1. Determine the IP family of your cluster\.

   ```
   aws eks describe-cluster --name my-cluster | grep ipFamily
   ```

   An example output is as follows\.

   ```
   "ipFamily": "ipv4"
   ```

   The output may return `ipv6` instead\.

1. Create the IAM role\. You can use `eksctl` or `kubectl` and the AWS CLI to create your IAM role\.

------
#### [ eksctl ]

   Create an IAM role and attach the IAM policy to the role with the command that matches the IP family of your cluster\. The command creates and deploys an AWS CloudFormation stack that creates an IAM role, attaches the policy that you specify to it, and annotates the existing `aws-node` Kubernetes service account with the ARN of the IAM role that is created\.
   + `IPv4`

     Replace *`my-cluster`* with your own value\.

     ```
     eksctl create iamserviceaccount \
         --name aws-node \
         --namespace kube-system \
         --cluster my-cluster \
         --role-name AmazonEKSVPCCNIRole \
         --attach-policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy \
         --override-existing-serviceaccounts \
         --approve
     ```
   + `IPv6`

     Replace *`my-cluster`* with your own value\. Replace `111122223333` with your account ID and replace `AmazonEKS_CNI_IPv6_Policy` with the name of your `IPv6` policy\. If you don't have an `IPv6` policy, see [Create IAM policy for clusters that use the `IPv6` family](#cni-iam-role-create-ipv6-policy) to create one\. To use `IPv6` with your cluster, it must meet several requirements\. For more information, see [`IPv6` addresses for clusters, Pods, and services](cni-ipv6.md)\.

     ```
     eksctl create iamserviceaccount \
         --name aws-node \
         --namespace kube-system \
         --cluster my-cluster \    
         --role-name AmazonEKSVPCCNIRole \
         --attach-policy-arn arn:aws:iam::111122223333:policy/AmazonEKS_CNI_IPv6_Policy \
         --override-existing-serviceaccounts \
         --approve
     ```

------
#### [ kubectl and the AWS CLI ]

   1. View your cluster's OIDC provider URL\.

      ```
      aws eks describe-cluster --name my-cluster --query "cluster.identity.oidc.issuer" --output text
      ```

      An example output is as follows\.

      ```
      https://oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE
      ```

      If no output is returned, then you must [create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.

   1. Copy the following contents to a file named `vpc-cni-trust-policy.json`\. Replace `111122223333` with your account ID and `EXAMPLED539D4633E53DE1B71EXAMPLE` with the output returned in the previous step\. Replace `region-code` with the AWS Region that your cluster is in\.

      ```
      {
          "Version": "2012-10-17",
          "Statement": [
              {
                  "Effect": "Allow",
                  "Principal": {
                      "Federated": "arn:aws:iam::111122223333:oidc-provider/oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE"
                  },
                  "Action": "sts:AssumeRoleWithWebIdentity",
                  "Condition": {
                      "StringEquals": {
                          "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:aud": "sts.amazonaws.com",
                          "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:sub": "system:serviceaccount:kube-system:aws-node"
                      }
                  }
              }
          ]
      }
      ```

   1. Create the role\. You can replace *`AmazonEKSVPCCNIRole`* with any name that you choose\.

      ```
      aws iam create-role \
        --role-name AmazonEKSVPCCNIRole \
        --assume-role-policy-document file://"vpc-cni-trust-policy.json"
      ```

   1. Attach the required IAM policy to the role\. Run the command that matches the IP family of your cluster\.
      + `IPv4`

        ```
        aws iam attach-role-policy \
          --policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy \
          --role-name AmazonEKSVPCCNIRole
        ```
      + `IPv6`

        Replace `111122223333` with your account ID and `AmazonEKS_CNI_IPv6_Policy` with the name of your `IPv6` policy\. If you don't have an `IPv6` policy, see [Create IAM policy for clusters that use the `IPv6` family](#cni-iam-role-create-ipv6-policy) to create one\. To use `IPv6` with your cluster, it must meet several requirements\. For more information, see [`IPv6` addresses for clusters, Pods, and services](cni-ipv6.md)\.

        ```
        aws iam attach-role-policy \
          --policy-arn arn:aws:iam::111122223333:policy/AmazonEKS_CNI_IPv6_Policy \
          --role-name AmazonEKSVPCCNIRole
        ```

   1. Run the following command to annotate the `aws-node` service account with the ARN of the IAM role that you created previously\. Replace the `example values` with your own values\.

      ```
      kubectl annotate serviceaccount \
          -n kube-system aws-node \
          eks.amazonaws.com/role-arn=arn:aws:iam::111122223333:role/AmazonEKSVPCCNIRole
      ```

------

1. \(Optional\) Configure the AWS Security Token Service endpoint type used by your Kubernetes service account\. For more information, see [Configure the AWS Security Token Service endpoint for a service account](configure-sts-endpoint.md)\.

## Step 2: Re\-deploy Amazon VPC CNI plugin for KubernetesPods<a name="cni-iam-role-redeploy-pods"></a>

1. Delete and re\-create any existing Pods that are associated with the service account to apply the credential environment variables\. The annotation is not applied to Pods that are currently running without the annotation\. The following command deletes the existing `aws-node` DaemonSet Pods and deploys them with the service account annotation\.

   ```
   kubectl delete Pods -n kube-system -l k8s-app=aws-node
   ```

1. Confirm that the Pods all restarted\.

   ```
   kubectl get pods -n kube-system -l k8s-app=aws-node
   ```

1. Describe one of the Pods and verify that the `AWS_WEB_IDENTITY_TOKEN_FILE` and `AWS_ROLE_ARN` environment variables exist\. Replace *cpjw7* with the name of one of your Pods returned in the output of the previous step\.

   ```
   kubectl describe pod -n kube-system aws-node-cpjw7 | grep 'AWS_ROLE_ARN:\|AWS_WEB_IDENTITY_TOKEN_FILE:'
   ```

   An example output is as follows\.

   ```
   AWS_ROLE_ARN:                 arn:aws:iam::111122223333:role/AmazonEKSVPCCNIRole
         AWS_WEB_IDENTITY_TOKEN_FILE:  /var/run/secrets/eks.amazonaws.com/serviceaccount/token
         AWS_ROLE_ARN:                           arn:aws:iam::111122223333:role/AmazonEKSVPCCNIRole
         AWS_WEB_IDENTITY_TOKEN_FILE:            /var/run/secrets/eks.amazonaws.com/serviceaccount/token
   ```

   Two sets of duplicate results are returned because the Pod contains two containers\. Both containers have the same values\.

   If your Pod is using the AWS Regional endpoint, then the following line is also returned in the previous output\.

   ```
   AWS_STS_REGIONAL_ENDPOINTS=regional
   ```

## Step 3: Remove the CNI policy from the node IAM role<a name="remove-cni-policy-node-iam-role"></a>

If your [Amazon EKS node IAM role](create-node-role.md) currently has the `AmazonEKS_CNI_Policy` IAM \(`IPv4`\) policy or an [`IPv6` policy](#cni-iam-role-create-ipv6-policy) attached to it, and you've created a separate IAM role, attached the policy to it instead, and assigned it to the `aws-node` Kubernetes service account, then we recommend that you remove the policy from your node role with the the AWS CLI command that matches the IP family of your cluster\. Replace `AmazonEKSNodeRole` with the name of your node role\.
+ `IPv4`

  ```
  aws iam detach-role-policy --role-name AmazonEKSNodeRole --policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy
  ```
+ `IPv6`

  Replace `111122223333` with your account ID and `AmazonEKS_CNI_IPv6_Policy` with the name of your `IPv6` policy\.

  ```
  aws iam detach-role-policy --role-name AmazonEKSNodeRole --policy-arn arn:aws:iam::111122223333:policy/AmazonEKS_CNI_IPv6_Policy
  ```

## Create IAM policy for clusters that use the `IPv6` family<a name="cni-iam-role-create-ipv6-policy"></a>

If you created a cluster that uses the `IPv6` family and the cluster has version `1.10.1` or later of the Amazon VPC CNI plugin for Kubernetes add\-on configured, then you need to create an IAM policy that you can assign to an IAM role\. If you have an existing cluster that you didn't configure with the `IPv6` family when you created it, then to use `IPv6`, you must create a new cluster\. For more information about using `IPv6` with your cluster, see [`IPv6` addresses for clusters, Pods, and services](cni-ipv6.md)\.

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
   aws iam create-policy --policy-name AmazonEKS_CNI_IPv6_Policy --policy-document file://vpc-cni-ipv6-policy.json
   ```