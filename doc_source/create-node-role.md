--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Amazon EKS node IAM role<a name="create-node-role"></a>

The Amazon EKS node `kubelet` daemon makes calls to AWS APIs on your behalf\. Nodes receive permissions for these API calls through an IAM instance profile and associated policies\. Before you can launch nodes and register them into a cluster, you must create an IAM role for those nodes to use when they are launched\. This requirement applies to nodes launched with the Amazon EKS optimized AMI provided by Amazon, or with any other node AMIs that you intend to use\. Additionally, this requirement applies to both managed node groups and self\-managed nodes\.

**Note**  
You can’t use the same role that is used to create any clusters\.

Before you create nodes, you must create an IAM role with the following permissions:
+ Permissions for the `kubelet` to describe Amazon EC2 resources in the VPC, such as provided by the ` [AmazonEKSWorkerNodePolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSWorkerNodePolicy.html) ` policy\. This policy also provides the permissions for the Amazon EKS Pod Identity Agent\.
+ Permissions for the `kubelet` to use container images from Amazon Elastic Container Registry \(Amazon ECR\), such as provided by the ` [AmazonEC2ContainerRegistryReadOnly](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEC2ContainerRegistryReadOnly.html) ` policy\. The permissions to use container images from Amazon Elastic Container Registry \(Amazon ECR\) are required because the built\-in add\-ons for networking run pods that use container images from Amazon ECR\.

**Note**  
Prior to October 3, 2023, ` [AmazonEKSWorkerNodePolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEKSWorkerNodePolicy.html) ` and ` [AmazonEC2ContainerRegistryReadOnly](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEC2ContainerRegistryReadOnly.html) ` were required on the IAM role for each managed node group\.

## Check for an existing node role<a name="check-worker-node-role"></a>

You can use the following procedure to check and see if your account already has the Amazon EKS node role\.

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the left navigation pane, choose **Roles**\.

1. Choose **Permissions**\.

1. Ensure that the **AmazonEKSWorkerNodePolicy** and **AmazonEC2ContainerRegistryReadOnly** managed policies are attached to the role or a custom policy is attached with the minimal permissions\.

1. Choose **Trust relationships**, and then choose **Edit trust policy**\.

1. Verify that the trust relationship contains the following policy\. If the trust relationship matches the following policy, choose **Cancel**\. If the trust relationship doesn’t match, copy the policy into the **Edit trust policy** window and choose **Update policy**\.

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

You can create the node IAM role with the AWS Management Console or the AWS CLI\.

 AWS Management Console  

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the left navigation pane, choose **Roles**\.

1. On the **Roles** page, choose **Create role**\.

1. On the **Select trusted entity** page, do the following:

   1. In the **Trusted entity type** section, choose ** AWS service**\.

   1. Under **Use case**, choose **EC2**\.

   1. Choose **Next**\.

1. On the **Add permissions** page, attach a custom policy or do the following:

   1. In the **Filter policies** box, enter `AmazonEKSWorkerNodePolicy`\.

   1. Select the check box to the left of **AmazonEKSWorkerNodePolicy** in the search results\.

   1. Choose **Clear filters**\.

   1. In the **Filter policies** box, enter `AmazonEC2ContainerRegistryReadOnly`\.

   1. Select the check box to the left of **AmazonEC2ContainerRegistryReadOnly** in the search results\.

   1. Choose **Next**\.

1. On the **Name, review, and create** page, do the following:

   1. For **Role name**, enter a unique name for your role, such as `AmazonEKSNodeRole`\.

   1. For **Description**, replace the current text with descriptive text such as `Amazon EKS - Node role`\.

   1. Under **Add tags \(Optional\)**, add metadata to the role by attaching tags as key\-value pairs\. For more information about using tags in IAM, see [Tagging IAM resources](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html) in the *IAM User Guide*\.

   1. Choose **Create role**\.

 AWS CLI  

1. Run the following command to create the `node-role-trust-relationship.json` file\.

   ```
   //⁂cat >node-role-trust-relationship.json <<EOF
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

1. Create the IAM role\.

   ```
   aws iam create-role \
     --role-name AmazonEKSNodeRole \
   //⁂  --assume-role-policy-document file://"node-role-trust-relationship.json"
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
        //⁂aws iam create-policy --policy-name AmazonEKS_CNI_IPv6_Policy --policy-document file://vpc-cni-ipv6-policy.json
        ```

     1. Attach the IAM policy to the IAM role\. Replace ` 111122223333 ` with your account ID\.

        ```
        aws iam attach-role-policy \
          --policy-arn arn:aws:iam::111122223333:policy/AmazonEKS_CNI_IPv6_Policy \
          --role-name AmazonEKSNodeRole
        ```