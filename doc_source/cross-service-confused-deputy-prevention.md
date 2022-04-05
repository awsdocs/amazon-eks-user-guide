# Cross\-service confused deputy prevention<a name="cross-service-confused-deputy-prevention"></a>

The confused deputy problem is a security issue where an entity that doesn't have permission to perform an action can coerce a more\-privileged entity to perform the action\. In AWS, cross\-service impersonation can result in the confused deputy problem\. Cross\-service impersonation can occur when one service \(the *calling service*\) calls another service \(the *called service*\)\. The calling service can be manipulated to use its permissions to act on another customer's resources in a way it shouldn't otherwise have permission to access\. To prevent this, AWS provides tools that help you protect your data for all services with service principals that have been given access to resources in your account\. 

We recommend using the [https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html#condition-keys-sourcearn](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html#condition-keys-sourcearn) or [https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html#condition-keys-sourceaccount](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html#condition-keys-sourceaccount) global condition context keys in resource policies to limit the permissions that Amazon Elastic Kubernetes Service gives another service to the resource\. Use `aws:SourceArn` if you want only one resource to be associated with the cross\-service access\. Use `aws:SourceAccount` if you want to allow any resource in that account to be associated with the cross\-service use\.

The most effective way to protect against the confused deputy problem is to use the `aws:SourceArn` global condition context key with the full ARN of the resource\. If you don't know the full ARN of the resource or if you are specifying multiple resources, use the `aws:SourceArn` global context condition key with wild card characters \(`*`\) for the unknown portions of the ARN\. For example, `arn:aws:eks:*:123456789012:*`\. 

The following example shows how you can use the `aws:SourceArn` global condition context key in Amazon EKS to prevent the confused deputy problem\. This example is for the trust policy of the [Amazon EKS cluster IAM role](service_IAM_role.md)\. Replace *region\-code* with the AWS Region that your cluster is in, *123456789012* with your account ID, and *cluster\-name* with your cluster's name\. If you want to use the same role for clusters in all AWS Regions in your account, replace *region\-code* with **\***\. If you want to use the same role for all clusters in your account, replace *cluster\-name* with **\***\.

```
{
  "Version": "2012-10-17",
  "Statement": {
    "Effect": "Allow",
    "Principal": {
      "Service": "eks.amazonaws.com"
    },
    "Action": "sts:AssumeRole",
    "Condition": {
      "ArnLike": {
        "aws:SourceArn": "arn:aws:eks:region-code:123456789012:cluster/cluster-name"
      }
    }
  }
}
```

See [Amazon EKS pod execution IAM role](pod-execution-role.md) for an example of a trust policy for that role\.