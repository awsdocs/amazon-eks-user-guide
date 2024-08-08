# Retrieve recommended Microsoft Windows AMI IDs<a name="retrieve-windows-ami-id"></a>

You can programmatically retrieve the Amazon Machine Image \(AMI\) ID for Amazon EKS optimized AMIs by querying the AWS Systems Manager Parameter Store API\. This parameter eliminates the need for you to manually look up Amazon EKS optimized AMI IDs\. For more information about the Systems Manager Parameter Store API, see [GetParameter](https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_GetParameter.html)\. The [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) that you use must have the `ssm:GetParameter` IAM permission to retrieve the Amazon EKS optimized AMI metadata\.

You can retrieve the image ID of the latest recommended Amazon EKS optimized Windows AMI with the following command, which uses the sub\-parameter `image_id`\. Make the following modifications to the command as needed and then run the modified command:
+ Replace `release` with one of the following options\.
  + Use `2022` for Windows Server 2022, but only if you're using Kubernetes version `1.24` or later\.
  + Use `2019` for Windows Server 2019\.
+ Replace `installation-option` with one of the following options\. For more information, see [What is the Server Core installation option in Windows Server](https://learn.microsoft.com/en-us/windows-server/administration/server-core/what-is-server-core)\.
  + Use `Core` for a minimal installation with a smaller attack surface\.
  + Use `Full` to include the Windows desktop experience\.
+ Replace `kubernetes-version` with a supported [Amazon EKS version](platform-versions.md)\.
+ Replace `region-code` with an [Amazon EKS supported AWS Region](https://docs.aws.amazon.com/general/latest/gr/eks.html) for which you want the AMI ID\.

```
aws ssm get-parameter --name /aws/service/ami-windows-latest/Windows_Server-release-English-installation-option-EKS_Optimized-kubernetes-version/image_id \
    --region region-code --query "Parameter.Value" --output text
```

Here's an example command after placeholder replacements have been made\.

```
aws ssm get-parameter --name /aws/service/ami-windows-latest/Windows_Server-2022-English-Core-EKS_Optimized-1.30/image_id \
    --region us-west-2 --query "Parameter.Value" --output text
```

An example output is as follows\.

```
ami-1234567890abcdef0
```