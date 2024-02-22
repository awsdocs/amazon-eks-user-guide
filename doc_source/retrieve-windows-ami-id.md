# Retrieving Amazon EKS optimized Windows AMI IDs<a name="retrieve-windows-ami-id"></a>

You can programmatically retrieve the Amazon Machine Image \(AMI\) ID for Amazon EKS optimized AMIs by querying the AWS Systems Manager Parameter Store API\. This parameter eliminates the need for you to manually look up Amazon EKS optimized AMI IDs\. For more information about the Systems Manager Parameter Store API, see [GetParameter](https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_GetParameter.html)\. The [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) that you use must have the `ssm:GetParameter` IAM permission to retrieve the Amazon EKS optimized AMI metadata\.

You can retrieve the image ID of the latest recommended Amazon EKS optimized Windows AMI with the following command by using the sub\-parameter `image_id`\. You can replace `1.29` with any supported Amazon EKS version and can replace `region-code` with an [Amazon EKS supported Region](https://docs.aws.amazon.com/general/latest/gr/eks.html) for which you want the AMI ID\. Replace `Core` with `Full` to see the Windows Server full AMI ID\. For Kubernetes version `1.24` or later, you can replace `2019` with `2022` to see the Windows Server 2022 AMI ID\.

```
aws ssm get-parameter --name /aws/service/ami-windows-latest/Windows_Server-2019-English-Core-EKS_Optimized-1.29/image_id --region region-code --query "Parameter.Value" --output text
```

An example output is as follows\.

```
ami-1234567890abcdef0
```