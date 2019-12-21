# Pod Execution Role<a name="pod-execution-role"></a>

The Amazon EKS pod execution role is required to run pods on AWS Fargate infrastructure\.

When your cluster creates pods on AWS Fargate infrastructure, the pod needs to make calls to AWS APIs on your behalf, for example, to pull container images from Amazon ECR\. The Amazon EKS pod execution role provides the IAM permissions to do this\.

When you create a Fargate profile, you must specify a pod execution role to use with your pods\. This role is added to the cluster's Kubernetes [Role Based Access Control](https://kubernetes.io/docs/admin/authorization/rbac/) \(RBAC\) for authorization, so that the `kubelet` that is running on the Fargate infrastructure can register with your Amazon EKS cluster\. This is what allows Fargate infrastructure to appear in your cluster as nodes\.

Before you create a Fargate profile, you must create an IAM role with the following IAM policy:
+ `[AmazonEKSFargatePodExecutionRolePolicy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSFargatePodExecutionRolePolicy%24jsonEditor)`

**To create the Amazon EKS pod execution role**

1. Create a file called `trust-relationship.json` and save it with the following text\.

   ```
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "",
         "Effect": "Allow",
         "Principal": {
           "Service": "eks-fargate-pods.amazonaws.com"
         },
         "Action": "sts:AssumeRole"
       }
     ]
   }
   ```

1. Create an IAM role that uses that trust relationship with the following AWS CLI command\.

   ```
   aws iam create-role --role-name AmazonEKSFargatePodExecutionRole --assume-role-policy-document file://trust-relationship.json
   ```

1. Attach the `[AmazonEKSFargatePodExecutionRolePolicy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSFargatePodExecutionRolePolicy%24jsonEditor)` to your new role with the following command\.

   ```
   aws iam attach-role-policy --role-name AmazonEKSFargatePodExecutionRole --policy-arn arn:aws:iam::aws:policy/AmazonEKSFargatePodExecutionRolePolicy
   ```