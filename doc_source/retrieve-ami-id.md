# Retrieving Amazon EKS\-Optimized AMI IDs<a name="retrieve-ami-id"></a>

You can programmatically retrieve the Amazon Machine Image \(AMI\) ID for Amazon EKS\-optimized AMIs by querying the AWS Systems Manager Parameter Store API\. This parameter eliminates the need for you to manually look up Amazon EKS\-optimized AMI IDs\. For more information about the Systems Manager Parameter Store API, see [GetParameter](https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_GetParameter.html)\. Your user account must have the `ssm:GetParameter` IAM permission to retrieve the Amazon EKS\-optimized AMI metadata\.

Select the name of the tool that you want to retrieve the AMI ID with\.

------
#### [ AWS CLI ]

You can retrieve the image ID of the latest recommended Amazon EKS\-optimized Amazon Linux AMI with the following command by using the sub\-parameter `image_id`\. Replace *1\.15* with a [supported version](platform-versions.md) and *region\-code* with an [Amazon EKS\-supported Region](https://docs.aws.amazon.com/general/latest/gr/rande.html#eks_region) for which you want the AMI ID\. Replace *amazon\-linux\-2* with `amazon-linux-2-gpu` to see the AMI with GPU ID\.

```
aws ssm get-parameter --name /aws/service/eks/optimized-ami/1.15/amazon-linux-2/recommended/image_id --region region-code --query "Parameter.Value" --output text
```

Example output:

```
ami-abcd1234efgh5678i
```

------
#### [ AWS Management Console ]

You can query for the recommended Amazon EKS\-optimized AMI ID using a URL\. The URL opens the Amazon EC2 Systems Manager console with the value of the ID for the parameter\. In the following URL, replace *1\.15* with a [supported version](platform-versions.md) and *region\-code* with an [Amazon EKS\-supported Region](https://docs.aws.amazon.com/general/latest/gr/rande.html#eks_region) for which you want the AMI ID\. Replace *amazon\-linux\-2* with `amazon-linux-2-gpu` to see the AMI with GPU ID\.

```
https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.15%252Famazon-linux-2%252Frecommended%252Fimage_id/description?region=region-code
```

------