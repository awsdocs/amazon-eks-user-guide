# Retrieving Amazon EKS optimized Bottlerocket AMI IDs<a name="retrieve-ami-id-bottlerocket"></a>

You can retrieve the Amazon Machine Image \(AMI\) ID for Amazon EKS optimized AMIs by querying the AWS Systems Manager Parameter Store API\. Using this parameter, you don't need to manually look up Amazon EKS optimized AMI IDs\. For more information about the Systems Manager Parameter Store API, see [GetParameter](https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_GetParameter.html)\. The [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) that you use must have the `ssm:GetParameter` IAM permission to retrieve the Amazon EKS optimized AMI metadata\.

You can retrieve the image ID of the latest recommended Amazon EKS optimized Bottlerocket AMI with the following AWS CLI command by using the sub\-parameter `image_id`\. Replace `1.29` with a [supported version](platform-versions.md) and `region-code` with an [Amazon EKS supported Region](https://docs.aws.amazon.com/general/latest/gr/eks.html) for which you want the AMI ID\.

```
aws ssm get-parameter --name /aws/service/bottlerocket/aws-k8s-1.29/x86_64/latest/image_id --region region-code --query "Parameter.Value" --output text
```

An example output is as follows\.

```
ami-1234567890abcdef0
```