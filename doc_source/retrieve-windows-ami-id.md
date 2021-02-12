# Retrieving Amazon EKS optimized Windows AMI IDs<a name="retrieve-windows-ami-id"></a>

You can programmatically retrieve the Amazon Machine Image \(AMI\) ID for Amazon EKS optimized AMIs by querying the AWS Systems Manager Parameter Store API\. This parameter eliminates the need for you to manually look up Amazon EKS optimized AMI IDs\. For more information about the Systems Manager Parameter Store API, see [GetParameter](https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_GetParameter.html)\. Your user account must have the `ssm:GetParameter` IAM permission to retrieve the Amazon EKS optimized AMI metadata\.

You can retrieve the AMI ID with the AWS CLI or the AWS Management Console\.
+ **AWS CLI** – You can retrieve the image ID of the latest recommended Amazon EKS optimized Windows AMI with the following command by using the sub\-parameter `image_id`\. You can replace *`<1.18>`* \(including `<>`\) with any supported Amazon EKS version and can replace *`<region-code>`* with an [Amazon EKS supported Region](https://docs.aws.amazon.com/general/latest/gr/eks.html) for which you want the AMI ID\. Replace *`<Core>`* with `Full` to see the Windows Server full AMI ID\. You can also replace *`<2019>`* with `2004` for the `Core` version only\.

  ```
  aws ssm get-parameter --name /aws/service/ami-windows-latest/Windows_Server-<2019>-English-<Core>-EKS_Optimized-<1.18>/image_id --region <region-code> --query "Parameter.Value" --output text
  ```

  Example output:

  ```
  ami-<ami-00a053f1635fffea0>
  ```
+ **AWS Management Console** – You can query for the recommended Amazon EKS optimized AMI ID using a URL\. The URL opens the Amazon EC2 Systems Manager console with the value of the ID for the parameter\. In the following URL, you can replace *<1\.18>* \(including *`<>`*\) with any supported Amazon EKS version and can replace *`<region-code>`* with an [Amazon EKS supported Region](https://docs.aws.amazon.com/general/latest/gr/eks.html) for which you want the AMI ID\. Replace *`<Core>`* with `Full` to see the Windows Server full AMI ID\. You can also replace *`<2019>`* with `2004` for the `Core` version only\.

  ```
  https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Fami-windows-latest%252FWindows_Server-<2019>-English-<Core>-EKS_Optimized-<1.18>%252Fimage_id/description?region=<region-code>
  ```