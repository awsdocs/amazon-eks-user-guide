# Retrieving Amazon EKS\-Optimized AMI IDs<a name="retrieve-ami-id"></a>

You can programmatically retrieve the Amazon Machine Image \(AMI\) ID for Amazon EKS\-optimized AMIs by querying the AWS Systems Manager Parameter Store API\. This parameter eliminates the need for you to manually look up Amazon EKS\-optimized AMI IDs\. For more information about the Systems Manager Parameter Store API, see [GetParameter](https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_GetParameter.html)\. Your user account must have the `ssm:GetParameter` IAM permission to retrieve the Amazon EKS\-optimized AMI metadata\.

Select the name of the tool that you want to retrieve the AMI ID with\.

------
#### [ AWS CLI ]

You can retrieve the image ID of the latest recommended Amazon EKS\-optimized Amazon Linux AMI with the following command by using the sub\-parameter `image_id`\. Replace *1\.14* with a [supported version](platform-versions.md) and *us\-west\-2* with an [Amazon EKS\-supported Region](https://docs.aws.amazon.com/general/latest/gr/rande.html#eks_region) for which you want the AMI ID\. Replace *amazon\-linux\-2* with `amazon-linux-2-gpu` to see the AMI with GPU ID\.

```
aws ssm get-parameter --name /aws/service/eks/optimized-ami/1.14/amazon-linux-2/recommended/image_id --region us-west-2 --query "Parameter.Value" --output text
```

Example output:

```
ami-abcd1234efgh5678i
```

------
#### [ AWS Management Console ]

You can query for the recommended Amazon EKS\-optimized AMI ID using a URL\. The URL opens the Amazon EC2 Systems Manager console with the value of the ID for the parameter\. In the following URL, replace *1\.14* with a [supported version](platform-versions.md) and *us\-west\-2* with an [Amazon EKS\-supported Region](https://docs.aws.amazon.com/general/latest/gr/rande.html#eks_region) for which you want the AMI ID\. Replace *amazon\-linux\-2* with `amazon-linux-2-gpu` to see the AMI with GPU ID\.

```
https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2%252Frecommended%252Fimage_id/description?region=us-west-2
```

------
#### [ AWS CloudFormation ]

You can launch the AWS CloudFormation console with the Amazon EKS worker node template's `NodeImageIdSSMParam` field pre\-populated with the Amazon EC2 Systems Manager parameter value for the Amazon EKS recommended AMI ID \. In the following link, replace *1\.14* with a [supported version](platform-versions.md) and *us\-west\-2* in the *?region=us\-west\-2\#* part of the URL with the [Amazon EKS supported Region](https://docs.aws.amazon.com/general/latest/gr/rande.html#eks_region) for which you want the AMI ID\. Replace *amazon\-linux\-2* with `amazon-linux-2-gpu` if you want to use an AMI with GPU\. Open an internet browser and enter the modified link for the pre\-populated template\.

```
[https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/create/review?templateURL=https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-11-15/amazon-eks-nodegroup.yaml&param_NodeImageIdSSMParam=/aws/service/eks/optimized-ami/1.14/amazon-linux-2/recommended/image_id](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/create/review?templateURL=https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-11-15/amazon-eks-nodegroup.yaml&param_NodeImageIdSSMParam=/aws/service/eks/optimized-ami/1.14/amazon-linux-2/recommended/image_id)
```

If you want to specify your own custom AMI ID, enter the ID in the `NodeImageId` field of the template instead of using the SSM parameter\. The value overrides the value that is specified for the `NodeImageIdSSMParam` field\.

------