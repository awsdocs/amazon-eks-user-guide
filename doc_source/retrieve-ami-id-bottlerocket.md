# Retrieve recommended Bottlerocket AMI IDs<a name="retrieve-ami-id-bottlerocket"></a>

You can retrieve the Amazon Machine Image \(AMI\) ID for Amazon EKS optimized AMIs by querying the AWS Systems Manager Parameter Store API\. Using this parameter, you don't need to manually look up Amazon EKS optimized AMI IDs\. For more information about the Systems Manager Parameter Store API, see [GetParameter](https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_GetParameter.html)\. The [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) that you use must have the `ssm:GetParameter` IAM permission to retrieve the Amazon EKS optimized AMI metadata\.

You can retrieve the image ID of the latest recommended Amazon EKS optimized Bottlerocket AMI with the following AWS CLI command, which uses the sub\-parameter `image_id`\. Make the following modifications to the command as needed and then run the modified command:
+ Replace `kubernetes-version` with a supported [Amazon EKS version](platform-versions.md)\.
+ Replace `-flavor` with one of the following options\.
  + Remove `-flavor` for variants without a GPU\.
  + Use `-nvidia` for GPU\-enabled variants\.
+ Replace `architecture` with one of the following options\.
  + Use `x86_64` for `x86` based instances\.
  + Use `arm64` for ARM instances\.
+ Replace `region-code` with an [Amazon EKS supported AWS Region](https://docs.aws.amazon.com/general/latest/gr/eks.html) for which you want the AMI ID\.

```
aws ssm get-parameter --name /aws/service/bottlerocket/aws-k8s-kubernetes-version-flavor/architecture/latest/image_id \
    --region region-code --query "Parameter.Value" --output text
```

Here's an example command after placeholder replacements have been made\.

```
aws ssm get-parameter --name /aws/service/bottlerocket/aws-k8s-1.30/x86_64/latest/image_id \
    --region us-west-2 --query "Parameter.Value" --output text
```

An example output is as follows\.

```
ami-1234567890abcdef0
```