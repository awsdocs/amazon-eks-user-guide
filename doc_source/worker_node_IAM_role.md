# Amazon EKS Worker Node IAM Role<a name="worker_node_IAM_role"></a>

The Amazon EKS worker node `kubelet` daemon makes calls to AWS APIs on your behalf\. Worker nodes receive permissions for these API calls through an IAM instance profile and associated policies\. Before you can launch worker nodes and register them into a cluster, you must create an IAM role for those worker nodes to use when they are launched\. This requirement applies to worker nodes launched with the Amazon EKS\-optimized AMI provided by Amazon, or with any other worker node AMIs that you intend to use\. Before you create worker nodes, you must create an IAM role with the following IAM policies:
+ `[AmazonEKSWorkerNodePolicy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy%24jsonEditor)`
+ `[AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor)`
+ `[AmazonEC2ContainerRegistryReadOnly](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly%24jsonEditor)`

## Check for an Existing Worker Node Role<a name="check-worker-node-role"></a>

You can use the following procedure to check and see if your account already has the Amazon EKS worker node role\.<a name="procedure_check_worker_node_role"></a>

**To check for the `NodeInstanceRole` in the IAM console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the navigation pane, choose **Roles**\. 

1. Search the list of roles for `NodeInstanceRole`\. If the role does not exist, see [Creating the Amazon EKS Worker Node IAM Role](#create-worker-node-role) to create the role\. If the role does exist, select the role to view the attached policies\.

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

## Creating the Amazon EKS Worker Node IAM Role<a name="create-worker-node-role"></a>

If you created your worker nodes by following the steps in the [Getting Started with the AWS Management Console](getting-started-console.md) or [Getting Started with `eksctl`](getting-started-eksctl.md) topics, then the worker node role account already exists and you don't need to manually create it\. You can use the following procedure to create the Amazon EKS worker node role if you do not already have one for your account\.

**To create your Amazon EKS worker node IAM role**

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. Choose **Create stack** and then choose **With new resources \(standard\)**\.

1. For **Specify template**, select **Amazon S3 URL**\.

1. Paste the following URL into the **Amazon S3 URL** text area and choose **Next**:

   ```
   https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-11-15/amazon-eks-nodegroup-role.yaml
   ```

1. On the **Specify stack details** page, fill out the parameters accordingly, and then choose **Next**\.
   + **Stack name**: Choose a stack name for your AWS CloudFormation stack\. For example, you can call it **eks\-node\-group\-instance\-role**\.

1. \(Optional\) On the **Configure stack options** page, you can choose to tag your stack resources\. Choose **Next**\.

1. On the **Review** page, check the box in the **Capabilities** section and choose **Create stack**\.

1. When your stack is created, select it in the console and choose **Outputs**\.

1. Record the **NodeInstanceRole** value for the IAM role that was created\. You need this when you create your node group\.