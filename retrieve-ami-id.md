# Retrieving Amazon EKS optimized Amazon Linux AMI IDs<a name="retrieve-ami-id"></a>

You can programmatically retrieve the Amazon Machine Image \(AMI\) ID for Amazon EKS optimized AMIs by querying the AWS Systems Manager Parameter Store API\. This parameter eliminates the need for you to manually look up Amazon EKS optimized AMI IDs\. For more information about the Systems Manager Parameter Store API, see [GetParameter](https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_GetParameter.html)\.

**To retrieve an AMI ID for Amazon EKS optimized AMIs using the AWS CLI**

1. Determine the region your node instance will be deployed in, such as `us-east-1`\.

1. Determine the type of AMI you need\. For information about the types of Amazon EC2 instances, see [Instance Types](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html)\.
   + `amazon-linux-2` is the most common value, for x86 based instances\.
   + `amazon-linux-2-arm64` is for ARM instances, such as [AWS Graviton](http://aws.amazon.com/ec2/graviton/) based instances\.
   + `amazon-linux-2-gpu` is for [GPU accelerated instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/accelerated-computing-instances.html#gpu-instances)\.

1. Determine the Kubernetes version of the cluster your node will be attached to, such as 1\.28\.

1. Run the following AWS CLI command to retrieve the appropriate AMI ID\. Replace the AWS Region, Kubernetes version, and platform as appropriate\. You must be logged into the AWS CLI using an [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) that has the `ssm:GetParameter` IAM permission to retrieve the Amazon EKS optimized AMI metadata\.

   ```
   aws ssm get-parameter --name /aws/service/eks/optimized-ami/1.28/amazon-linux-2/recommended/image_id \
                   --region region-code --query "Parameter.Value" --output text
   ```

   An example output is as follows\.

   ```
   ami-1234567890abcdef0
   ```