# Retrieve recommended Amazon Linux AMI IDs<a name="retrieve-ami-id"></a>

You can programmatically retrieve the Amazon Machine Image \(AMI\) ID for Amazon EKS optimized AMIs by querying the AWS Systems Manager Parameter Store API\. This parameter eliminates the need for you to manually look up Amazon EKS optimized AMI IDs\. For more information about the Systems Manager Parameter Store API, see [GetParameter](https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_GetParameter.html)\. The [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html#iam-term-principal) that you use must have the `ssm:GetParameter` IAM permission to retrieve the Amazon EKS optimized AMI metadata\.

You can retrieve the image ID of the latest recommended Amazon EKS optimized Amazon Linux AMI with the following command, which uses the sub\-parameter `image_id`\. Make the following modifications to the command as needed and then run the modified command:
+ Replace `kubernetes-version` with a supported [Amazon EKS version](platform-versions.md)\.
+ Replace `ami-type` with one of the following options\. For information about the types of Amazon EC2 instances, see [Amazon EC2 instance types](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html)\.
  + Use `amazon-linux-2023/x86_64/standard` for Amazon Linux 2023 \(AL2023\) `x86` based instances\.
  + Use `amazon-linux-2023/arm64/standard` for AL2023 ARM instances\.
  + Use `amazon-linux-2` for Amazon Linux 2 \(AL2\) `x86` based instances\.
  + Use `amazon-linux-2-arm64` for AL2 ARM instances, such as [AWS Graviton](https://aws.amazon.com/ec2/graviton/) based instances\.
  + Use `amazon-linux-2-gpu` for AL2 [hardware accelerated](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/accelerated-computing-instances.html) `x86` based instances for NVIDIA GPU, [Inferentia](https://aws.amazon.com/machine-learning/inferentia/), and [Trainium](https://aws.amazon.com/machine-learning/trainium/) based workloads\.
+ Replace `region-code` with an [Amazon EKS supported AWS Region](https://docs.aws.amazon.com/general/latest/gr/eks.html) for which you want the AMI ID\.

```
aws ssm get-parameter --name /aws/service/eks/optimized-ami/kubernetes-version/ami-type/recommended/image_id \
    --region region-code --query "Parameter.Value" --output text
```

Here's an example command after placeholder replacements have been made\.

```
aws ssm get-parameter --name /aws/service/eks/optimized-ami/1.30/amazon-linux-2023/x86_64/standard/recommended/image_id \
    --region us-west-2 --query "Parameter.Value" --output text
```

An example output is as follows\.

```
ami-1234567890abcdef0
```