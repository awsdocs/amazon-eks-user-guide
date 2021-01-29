# Amazon EKS node IAM role<a name="create-node-role"></a>

The Amazon EKS node `kubelet` daemon makes calls to AWS APIs on your behalf\. Nodes receive permissions for these API calls through an IAM instance profile and associated policies\. Before you can launch nodes and register them into a cluster, you must create an IAM role for those nodes to use when they are launched\. This requirement applies to nodes launched with the Amazon EKS optimized AMI provided by Amazon, or with any other node AMIs that you intend to use\. Before you create nodes, you must create an IAM role with the following IAM policies:
+ `[AmazonEKSWorkerNodePolicy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy%24jsonEditor)`
+ `[AmazonEC2ContainerRegistryReadOnly](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly%24jsonEditor)`

## Check for an existing node role<a name="check-worker-node-role"></a>

You can use the following procedure to check and see if your account already has the Amazon EKS node role\.<a name="procedure_check_worker_node_role"></a>

**To check for the `eksNodeRole` in the IAM console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the navigation panel, choose **Roles**\. 

1. Search the list of roles for `eksNodeRole`\. If a role that contains `eksNodeRole` or `NodeInstanceRole` does not exist, then see [Creating the Amazon EKS node IAM role](#create-worker-node-role) to create the role\. If a role that contains `eksNodeRole` or `NodeInstanceRole` does exist, then select the role to view the attached policies\.

1. Choose **Permissions**\.

1. Ensure that the **AmazonEKSWorkerNodePolicy** and **AmazonEC2ContainerRegistryReadOnly** managed policies are attached to the role\. If the policies are attached, your Amazon EKS node role is properly configured\.
**Note**  
If the **AmazonEKS\_CNI\_Policy** policy is attached to the role, we recommend removing it and attaching it to an IAM role that is mapped to the `aws-node` Kubernetes service account instead\. For more information, see [Configuring the VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.

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

## Creating the Amazon EKS node IAM role<a name="create-worker-node-role"></a>

You can create the node IAM role with the AWS Management Console AWS CloudFormation\.<a name="create-node-role-console2"></a>

**To create your Amazon EKS node role in the IAM console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. Choose **Roles**, then **Create role**\.

1. Choose **EC2** from the list of **Common use cases** under** Choose a use case,** then choose **Next: Permissions**\.

1. In the **Filter policies** box, enter `AmazonEKSWorkerNodePolicy`\. Check the box to the left of **AmazonEKSWorkerNodePolicy**\.

1. In the **Filter policies** box, enter `AmazonEC2ContainerRegistryReadOnly`\. Check the box to the left of **AmazonEC2ContainerRegistryReadOnly**\.

1. The **AmazonEKS\_CNI\_Policy** policy must be attached to either this role or to a different role that is mapped to the `aws-node` Kubernetes service account\. We recommend assigning the policy to the role associated to the Kubernetes service account instead of assigning it to this role\. For more information, see [Configuring the VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.

1. Choose **Next: Tags**\.

1. \(Optional\) Add metadata to the role by attaching tags as key–value pairs\. For more information about using tags in IAM, see [Tagging IAM Entities](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html) in the *IAM User Guide*\. 

1. Choose **Next: Review**\.

1. For **Role name**, enter a unique name for your role, such as NodeInstanceRole\. For **Role description**, replace the current text with descriptive text such as Amazon EKS \- Node Group Role, then choose **Create role**\.<a name="create-node-role-cfn"></a>

**To create your Amazon EKS node role using AWS CloudFormation**

1. Open the AWS CloudFormation console at [https://console\.aws\.amazon\.com/cloudformation](https://console.aws.amazon.com/cloudformation/)\.

1. Choose **Create stack** and then choose **With new resources \(standard\)**\.

1. For **Specify template**, select **Amazon S3 URL**\.

1. Paste the URL that corresponds to the Region that your cluster is in into the **Amazon S3 URL** text area and choose **Next** twice:
   + All Regions other than China Regions\.

     ```
     https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-nodegroup-role.yaml
     ```
   + Beijing and Ningxia China Regions\.

     ```
     https://s3.cn-north-1.amazonaws.com.cn/amazon-eks/cloudformation/2020-10-29/amazon-eks-nodegroup-role.yaml
     ```

1. On the **Specify stack details** page, for **Stack name** enter a name such as **eks\-node\-group\-instance\-role** and choose **Next**\.

1. \(Optional\) On the **Configure stack options** page, you can choose to tag your stack resources\. Choose **Next**\.

1. On the **Review** page, check the box in the **Capabilities** section and choose **Create stack**\.

1. When your stack is created, select it in the console and choose **Outputs**\.

1. Record the **NodeInstanceRole** value for the IAM role that was created\. You need this when you create your node group\.

1. \(Optional, but recommended\) One of the IAM policies attached to the role by the AWS CloudFormation template in a previous step is the **AmazonEKS\_CNI\_Policy** managed policy\. The policy must be attached to this role or to a role associated to the Kubernetes `aws-node` service account that is used for the Amazon EKS VPC CNI plugin\. We recommend assigning the policy to the role associated to the Kubernetes service account\. For more information, see [Configuring the VPC CNI plugin to use IAM roles for service accounts](cni-iam-role.md)\.