# Retrieving Amazon EKS optimized Amazon Linux AMI IDs<a name="retrieve-ami-id"></a>

You can programmatically retrieve the Amazon Machine Image \(AMI\) ID for Amazon EKS optimized AMIs by querying the AWS Systems Manager Parameter Store API\. This parameter eliminates the need for you to manually look up Amazon EKS optimized AMI IDs\. For more information about the Systems Manager Parameter Store API, see [GetParameter](https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_GetParameter.html)\.

**To retrieve an AMI ID for Amazon EKS optimized AMIs using the AWS CLI**

1. Determine the region your node instance will be deployed in, such as `us-east-1`\.

1. Determine the type of AMI you need\. For information about the types of Amazon EC2 instances, see [Instance Types](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html)\.
   + `amazon-linux-2` is for Amazon Linux 2 \(AL2\) `x86` based instances\.
   + `amazon-linux-2-arm64` is for AL2 ARM instances, such as [AWS Graviton](https://aws.amazon.com/ec2/graviton/) based instances\.
   + `amazon-linux-2-gpu` is for AL2 [GPU accelerated instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/accelerated-computing-instances.html#gpu-instances)\.
   + `amazon-linux-2023/x86_64/standard` is for Amazon Linux 2023 \(AL2023\) `x86` based instances\.
   + `amazon-linux-2023/arm64/standard` is for AL2023 ARM instances\.

1. Determine the Kubernetes version of the cluster your node will be attached to, such as 1\.29\.

1. Run the following AWS CLI command to retrieve the appropriate AMI ID\. Replace the AWS Region, Kubernetes version, and platform as appropriate\. You must be logged into the AWS CLI using an [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) that has the `ssm:GetParameter` IAM permission to retrieve the Amazon EKS optimized AMI metadata\.

   ```
   aws ssm get-parameter --name /aws/service/eks/optimized-ami/1.29/amazon-linux-2/recommended/image_id \
                   --region region-code --query "Parameter.Value" --output text
   ```

   An example output is as follows\.

   ```
   ami-1234567890abcdef0
   ```