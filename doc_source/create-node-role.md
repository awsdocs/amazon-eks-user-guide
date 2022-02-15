# Amazon EKS node IAM role<a name="create-node-role"></a>

The Amazon EKS node `kubelet` daemon makes calls to AWS APIs on your behalf\. Nodes receive permissions for these API calls through an IAM instance profile and associated policies\. Before you can launch nodes and register them into a cluster, you must create an IAM role for those nodes to use when they are launched\. This requirement applies to nodes launched with the Amazon EKS optimized AMI provided by Amazon, or with any other node AMIs that you intend to use\. Before you create nodes, you must create an IAM role with the following IAM policies:
+ `[AmazonEKSWorkerNodePolicy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy%24jsonEditor)`
+ `[AmazonEC2ContainerRegistryReadOnly](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly%24jsonEditor)`
+ Either the `[AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor)` managed policy \(if you created your cluster with the IPv4 family\) or an [IPv6 policy that you create](cni-iam-role.md#cni-iam-role-create-ipv6-policy) \(if you created your cluster with the IPv6 family\)\. Rather than attaching the policy to this role however, we recommend that you attach the policy to a separate role used specifically for the Amazon VPC CNI add\-on\. For more information about creating a separate role for the Amazon VPC CNI add\-on, see [Configuring the Amazon VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.

**Note**  
The Amazon EC2 node groups must have a different IAM role than the Fargate profile\. For more information, see [Amazon EKS pod execution IAM role](pod-execution-role.md)\.

## Check for an existing node role<a name="check-worker-node-role"></a>

You can use the following procedure to check and see if your account already has the Amazon EKS node role\.<a name="procedure_check_worker_node_role"></a>

**To check for the `eksNodeRole` in the IAM console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the navigation panel, choose **Roles**\. 

1. Search the list of roles for `eksNodeRole`, `AmazonEKSNodeRole`, or `NodeInstanceRole`\. If a role with one of those names doesn't exist, then see [Creating the Amazon EKS node IAM role](#create-worker-node-role) to create the role\. If a role that contains `eksNodeRole`, `AmazonEKSNodeRole`, or `NodeInstanceRole` does exist, then select the role to view the attached policies\.

1. Choose **Permissions**\.

1. Ensure that the **AmazonEKSWorkerNodePolicy** and **AmazonEC2ContainerRegistryReadOnly** managed policies are attached to the role\. If the policies are attached, your Amazon EKS node role is properly configured\.
**Note**  
If the **AmazonEKS\_CNI\_Policy** policy is attached to the role, we recommend removing it and attaching it to an IAM role that is mapped to the `aws-node` Kubernetes service account instead\. For more information, see [Configuring the Amazon VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.

1. Choose **Trust Relationships**, **Edit Trust Relationship**\.

1. Verify that the trust relationship contains the following policy\. If the trust relationship matches the policy below, choose **Cancel**\. If the trust relationship doesn't match, copy the policy into the **Policy Document** window and choose **Update Trust Policy**\.

   ```
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
   ```

## Creating the Amazon EKS node IAM role<a name="create-worker-node-role"></a>

You can create the node IAM role with the AWS Management Console or the AWS CLI\. Select the tab with the name of the tool that you want to create the role with\.

------
#### [ AWS Management Console ]<a name="create-node-role-console"></a>

**To create your Amazon EKS node role in the IAM console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. Choose **Roles**, then **Create role**\.

1. Choose **EC2** from the list of **Common use cases** under **Choose a use case**\.

1. Choose **Next: Permissions**\.

1. In the **Filter policies** box, enter **AmazonEKSWorkerNodePolicy**\.

1. Check the box to the left of **AmazonEKSWorkerNodePolicy**\.

1. In the **Filter policies** box, enter **AmazonEC2ContainerRegistryReadOnly**\.

1. Check the box to the left of **AmazonEC2ContainerRegistryReadOnly**\.

1. Either the **AmazonEKS\_CNI\_Policy** managed policy, or an [IPv6 policy](cni-iam-role.md#cni-iam-role-create-ipv6-policy) that you create must be attached to either this role or to a different role that's mapped to the `aws-node` Kubernetes service account\. We recommend assigning the policy to the role associated to the Kubernetes service account instead of assigning it to this role\. For more information, see [Configuring the Amazon VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.

1. Choose **Next: Tags**\.

1. \(Optional\) Add metadata to the role by attaching tags as key–value pairs\. For more information about using tags in IAM, see [Tagging IAM Entities](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html) in the *IAM User Guide*\. 

1. Choose **Next: Review**\.

1. For **Role name**, enter a unique name for your role, such as **AmazonEKSNodeRole**\.

1. For **Role description**, replace the current text with descriptive text such as **Amazon EKS \- Node role**\.

1. Choose **Create role**\.

------
#### [ AWS CLI ]

1. Save the following contents to a file named *node\-role\-trust\-relationship\.json*\.

   ```
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
   ```

1. Create the IAM role\.

   ```
   aws iam create-role \
     --role-name AmazonEKSNodeRole \
     --assume-role-policy-document file://"node-role-trust-relationship.json"
   ```

1. Attach two required IAM managed policies to the IAM role\.

   ```
   aws iam attach-role-policy \
     --policy-arn arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy \
     --role-name AmazonEKSNodeRole
   aws iam attach-role-policy \
     --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly \
     --role-name AmazonEKSNodeRole
   ```

1. Attach one of the following IAM policies to the IAM role depending on which IP family you created your cluster with\. The policy must be attached to this role or to a role associated to the Kubernetes `aws-node` service account that's used for the Amazon EKS VPC CNI plugin\. We recommend assigning the policy to the role associated to the Kubernetes service account\. To assign the policy to the role associated to the Kubernetes service account, see [Configuring the Amazon VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.
   + IPv4

     ```
     aws iam attach-role-policy \
       --policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy \
       --role-name AmazonEKSNodeRole
     ```
   + IPv6

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

     1. Attach the IAM policy to the IAM role\. Replace *111122223333* with your account ID\.

        ```
        aws iam attach-role-policy \
          --policy-arn arn:aws:iam::111122223333:policy/AmazonEKS_CNI_IPv6_Policy \
          --role-name AmazonEKSNodeRole
        ```

------