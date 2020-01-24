# Pod Execution Role<a name="pod-execution-role"></a>

The Amazon EKS pod execution role is required to run pods on AWS Fargate infrastructure\.

When your cluster creates pods on AWS Fargate infrastructure, the pod needs to make calls to AWS APIs on your behalf, for example, to pull container images from Amazon ECR\. The Amazon EKS pod execution role provides the IAM permissions to do this\.

When you create a Fargate profile, you must specify a pod execution role to use with your pods\. This role is added to the cluster's Kubernetes [Role Based Access Control](https://kubernetes.io/docs/admin/authorization/rbac/) \(RBAC\) for authorization, so that the `kubelet` that is running on the Fargate infrastructure can register with your Amazon EKS cluster\. This is what allows Fargate infrastructure to appear in your cluster as nodes\.

Before you create a Fargate profile, you must create an IAM role with the following IAM policy:
+ `[AmazonEKSFargatePodExecutionRolePolicy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSFargatePodExecutionRolePolicy%24jsonEditor)`

## Check for an Existing Pod Execution Role<a name="check-pod-execuiton-role"></a>

You can use the following procedure to check and see if your account already has the Amazon EKS pod execution role\.<a name="procedure_check_worker_node_role"></a>

**To check for the `AmazonEKSFargatePodExecutionRole` in the IAM console**

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the navigation pane, choose **Roles**\. 

1. Search the list of roles for `AmazonEKSFargatePodExecutionRole`\. If the role does not exist, see [Creating the Amazon EKS Pod Execution Role](#create-pod-execution-role) to create the role\. If the role does exist, select the role to view the attached policies\.

1. Choose **Permissions**\.

1. Ensure that the **AmazonEKSFargatePodExecutionRolePolicy** Amazon managed policy is attached to the role\. If the policy is attached, then your Amazon EKS pod execution role is properly configured\.

1. Choose **Trust Relationships**, **Edit Trust Relationship**\.

1. Verify that the trust relationship contains the following policy\. If the trust relationship matches the policy below, choose **Cancel**\. If the trust relationship does not match, copy the policy into the **Policy Document** window and choose **Update Trust Policy**\.

   ```
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "Service": "eks-fargate-pods.amazonaws.com"
         },
         "Action": "sts:AssumeRole"
       }
     ]
   }
   ```

## Creating the Amazon EKS Pod Execution Role<a name="create-pod-execution-role"></a>

You can use the following procedure to create the Amazon EKS pod execution role if you do not already have one for your account\.

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. Choose **Roles**, then **Create role**\.

1. Choose **EKS** from the list of services, **EKS \- Fargate pod** for your use case, and then **Next: Permissions**\.

1. Choose **Next: Tags**\.

1. \(Optional\) Add metadata to the role by attaching tags as key–value pairs\. For more information about using tags in IAM, see [Tagging IAM Entities](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html) in the *IAM User Guide*\. 

1. Choose **Next: Review**\.

1. For **Role name**, enter a unique name for your role, such as `AmazonEKSFargatePodExecutionRole`, then choose **Create role**\.