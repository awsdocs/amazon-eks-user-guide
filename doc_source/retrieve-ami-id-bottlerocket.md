# Retrieving Amazon EKS optimized Bottlerocket AMI IDs<a name="retrieve-ami-id-bottlerocket"></a>

You can retrieve the Amazon Machine Image \(AMI\) ID for Amazon EKS optimized AMIs by querying the AWS Systems Manager Parameter Store API\. Using this parameter, you don't need to manually look up Amazon EKS optimized AMI IDs\. For more information about the Systems Manager Parameter Store API, see [GetParameter](https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_GetParameter.html)\. Your user account must have the `ssm:GetParameter` IAM permission to retrieve the Amazon EKS optimized AMI metadata\.

You can retrieve the AMI ID with the AWS CLI or the AWS Management Console\.
+ **AWS CLI** – You can retrieve the image ID of the latest recommended Amazon EKS optimized Bottlerocket AMI with the following AWS CLI command by using the sub\-parameter `image_id`\. Replace *<1\.21>* with a [supported version](platform-versions.md) and *<region\-code>* with an [Amazon EKS supported Region](https://docs.aws.amazon.com/general/latest/gr/eks.html) for which you want the AMI ID\.

  ```
  aws ssm get-parameter --name /aws/service/bottlerocket/aws-k8s-<1.21>/x86_64/latest/image_id --region <region-code> --query "Parameter.Value" --output text
  ```

  The following is an example output\.

  ```
  ami-<068ed1c8e99b4810c>
  ```
+ **AWS Management Console** – You can query for the recommended Amazon EKS optimized AMI ID using a URL in the AWS Management Console\. The URL opens the Amazon EC2 Systems Manager console with the value of the ID for the parameter\. In the following URL, replace *<1\.21>* with a [supported version](platform-versions.md) and *<region\-code>* with an [Amazon EKS supported Region](https://docs.aws.amazon.com/general/latest/gr/eks.html) for which you want the AMI ID\.

  ```
  https://console.aws.amazon.com/systems-manager/parameters/aws/service/bottlerocket/aws-k8s-<1.21>/x86_64/latest/image_id/description?region=<region-code>
  ```