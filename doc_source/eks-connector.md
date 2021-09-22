# Amazon EKS Connector<a name="eks-connector"></a>


|  | 
| --- |
| The Amazon EKS Connector is in preview release for Amazon EKS and is subject to change\. | 

The Amazon EKS Connector allows you to register and connect any conformant Kubernetes cluster to AWS and visualize it in the Amazon EKS console\. Once connected, you can see your cluster's status, configuration, and workloads in the Amazon EKS console\. Amazon EKS displays connected clusters in Amazon EKS console for workload visualization only and does not manage them\. The Amazon EKS Connector connects the following types of Kubernetes clusters to Amazon EKS\.


+ On\-premise Kubernetes clusters
+ Self\-managed clusters running on Amazon EC2
+ Managed clusters from other cloud providers

## Amazon EKS Connector considerations<a name="connect-cluster-reqts"></a>

Consider the following when using Amazon EKS Connector\.
+ You must have administrative privileges to the Kubernetes cluster prior to registering the cluster to Amazon EKS\.
+ The Amazon EKS Connector must run on Linux 64\-bit \(x86\) worker nodes\. ARM worker nodes are not supported\.
+ You must have worker nodes in your Kubernetes cluster that have outbound access to the `ssm.` and `ssmmessages.` Systems Manager endpoints\. For more information, see [Systems Manager endpoints](https://docs.aws.amazon.com/general/latest/gr/ssm.html) in the *AWS General Reference*\.
+ You can connect up to 10 clusters per Region\.
+ Only the Amazon EKS `RegisterCluster`, `ListClusters`, `DescribeCluster`, and `DeregisterCluster` APIs are supported for external Kubernetes clusters\.
+ Tags are not supported for connected clusters\.

## Required IAM roles for Amazon EKS Connector<a name="connector-iam-permissions"></a>

Using the Amazon EKS Connector requires the following 2 IAM roles, which you will have to create\.

To enable cluster view permission for another user, then follow [Granting access to a user to view a cluster](connector-grant-access.md)\.

### Creating the Amazon EKS Connector service\-linked IAM role<a name="con-slr"></a>

The Amazon EKS Connector service\-linked IAM role allows Amazon EKS to connect to external Kubernetes clusters\. For more information, see [Amazon EKS Connector role](using-service-linked-roles-eks-connector.md)\. You can create the role with this command:

```
aws iam create-service-linked-role --aws-service-name eks-connector.amazonaws.com
```

### Creating the Amazon EKS Connector agent IAM role<a name="create-con-agent-role"></a>

The IAM role for the Amazon EKS Connector agent\. You can create the role with the following steps\.

**To create the Amazon EKS Connector agent IAM role**

1. Create a file named `eks-connector-agent-trust-policy.json` that contains the following JSON to use for the IAM role\.

   ```
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Sid": "SSMAccess",
               "Effect": "Allow",
               "Principal": {
                   "Service": [
                       "ssm.amazonaws.com"
                   ]
               },
               "Action": "sts:AssumeRole"
           }
       ]
   }
   ```

1. Create a file named `eks-connector-agent-policy.json` that contains the following JSON to use for the IAM role\.

   ```
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Sid": "SsmControlChannel",
               "Effect": "Allow",
               "Action": [
                   "ssmmessages:CreateControlChannel"
               ],
               "Resource": "arn:aws:eks:*:*:cluster/*"
           },
           {
               "Sid": "ssmDataplaneOperations",
               "Effect": "Allow",
               "Action": [
                   "ssmmessages:CreateDataChannel",
                   "ssmmessages:OpenDataChannel",
                   "ssmmessages:OpenControlChannel"
               ],
               "Resource": "*"
           }
       ]
   }
   ```

1. Create the Amazon EKS Connector agent role using the trust policy and policy you created in the previous steps\.

   ```
   aws iam create-role \
        --role-name AmazonEKSConnectorAgentRole \
        --assume-role-policy-document file://eks-connector-agent-trust-policy.json
   ```

1. Attach the policy to your Amazon EKS Connector agent role\.

   ```
   aws iam put-role-policy \
        --role-name AmazonEKSConnectorAgentRole \
        --policy-name AmazonEKSConnectorAgentPolicy \
        --policy-document file://eks-connector-agent-policy.json
   ```