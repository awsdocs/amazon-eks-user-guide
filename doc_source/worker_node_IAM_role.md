# Amazon EKS worker node IAM role<a name="worker_node_IAM_role"></a>

The Amazon EKS worker node `kubelet` daemon makes calls to AWS APIs on your behalf\. Worker nodes receive permissions for these API calls through an IAM instance profile and associated policies\. Before you can launch worker nodes and register them into a cluster, you must create an IAM role for those worker nodes to use when they are launched\. This requirement applies to worker nodes launched with the Amazon EKS\-optimized AMI provided by Amazon, or with any other worker node AMIs that you intend to use\. Before you create worker nodes, you must create an IAM role with the following IAM policies:
+ `[AmazonEKSWorkerNodePolicy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy%24jsonEditor)`
+ `[AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor)`
+ `[AmazonEC2ContainerRegistryReadOnly](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly%24jsonEditor)`

## Check for an existing worker node role<a name="check-worker-node-role"></a>

You can use the following procedure to check and see if your account already has the Amazon EKS worker node role\.<a name="procedure_check_worker_node_role"></a>

**To check for the `NodeInstanceRole` in the IAM console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the navigation pane, choose **Roles**\. 

1. Search the list of roles for `NodeInstanceRole`\. If a role that contains `NodeInstanceRole` does not exist, then see [Creating the Amazon EKS worker node IAM role](#create-worker-node-role) to create the role\. If a role that contains `NodeInstanceRole` does exist, then select the role to view the attached policies\.

1. Choose **Permissions**\.

1. Ensure that the **AmazonEKSWorkerNodePolicy**, **AmazonEKS\_CNI\_Policy**, and **AmazonEC2ContainerRegistryReadOnly** managed policies are attached to the role\. If the policies are attached, your Amazon EKS worker node role is properly configured\.

1. Choose **Trust Relationships**, **Edit Trust Relationship**\.

1. Verify that the trust relationship contains the following policy\. If the trust relationship matches the policy below, choose **Cancel**\. If the trust relationship does not match, copy the policy into the **Policy Document** window and choose **Update Trust Policy**\.

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

## Creating the Amazon EKS worker node IAM role<a name="create-worker-node-role"></a>

If you created your worker nodes by following the steps in the [Getting started with the AWS Management Console](getting-started-console.md) or [Getting started with `eksctl`](getting-started-eksctl.md) topics, then the worker node role already exists and you don't need to manually create it\. You can use the AWS Management Console or AWS CloudFormation to create the Amazon EKS worker node role if you do not already have one for your account\. Select the name of the tool that you'd like to use to create the role\.

------
#### [ AWS Management Console ]

**To create your Amazon EKS worker node role in the IAM console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. Choose **Roles**, then **Create role**\.

1. Choose **EC2** from the list of services, then **Next: Permissions**\.

1. In the **Filter policies** box, enter **AmazonEKSWorkerNodePolicy**\. Check the box to the left of **AmazonEKSWorkerNodePolicy\.**

1. In the **Filter policies** box, enter **AmazonEKS\_CNI\_Policy**\. Check the box to the left of **AmazonEKS\_CNI\_Policy\.**

1. In the **Filter policies** box, enter **AmazonEC2ContainerRegistryReadOnly**\. Check the box to the left of **AmazonEC2ContainerRegistryReadOnly\.**

1. Choose **Next: Tags**\.

1. \(Optional\) Add metadata to the role by attaching tags as key–value pairs\. For more information about using tags in IAM, see [Tagging IAM Entities](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html) in the *IAM User Guide*\. 

1. Choose **Next: Review**\.

1. For **Role name**, enter a unique name for your role, such as **NodeInstanceRole**\. For **Role description**, replace the current text with descriptive text such as **Amazon EKS \- Node Group Role**, then choose **Create role**\.

------
#### [ AWS CloudFormation ]

**To create your Amazon EKS worker node role using AWS CloudFormation**

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. Choose **Create stack** and then choose **With new resources \(standard\)**\.

1. For **Specify template**, select **Amazon S3 URL**\.

1. Paste the following URL into the **Amazon S3 URL** text area and choose **Next** twice:

   ```
   https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-04-21/amazon-eks-nodegroup-role.yaml
   ```

1. On the **Specify stack details** page, for **Stack name** enter a name such as **eks\-node\-group\-instance\-role** and choose **Next**\.

1. \(Optional\) On the **Configure stack options** page, you can choose to tag your stack resources\. Choose **Next**\.

1. On the **Review** page, check the box in the **Capabilities** section and choose **Create stack**\.

1. When your stack is created, select it in the console and choose **Outputs**\.

1. Record the **NodeInstanceRole** value for the IAM role that was created\. You need this when you create your node group\.

------