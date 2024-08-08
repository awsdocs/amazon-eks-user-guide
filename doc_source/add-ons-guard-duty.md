# Amazon GuardDuty agent<a name="add-ons-guard-duty"></a>

The Amazon GuardDuty agent Amazon EKS add\-on is a security monitoring service that analyzes and processes [foundational data sources](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_data-sources.html) including AWS CloudTrail management events and Amazon VPC flow logs\. Amazon GuardDuty also processes [features](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty-features-activation-model.html), such as Kubernetes audit logs and runtime monitoring\.

The Amazon EKS add\-on name is `aws-guardduty-agent`\.

## Required IAM permissions<a name="add-ons-guard-duty-iam-permissions"></a>

This add\-on doesn't require any permissions\.

## Additional information<a name="add-ons-guard-duty-information"></a>

For more information, see [Runtime Monitoring for Amazon EKS clusters in Amazon GuardDuty](https://docs.aws.amazon.com/guardduty/latest/ug/how-runtime-monitoring-works-eks.html)\.
+ To detect potential security threats in your Amazon EKS clusters, enable Amazon GuardDuty runtime monitoring and deploy the GuardDuty security agent to your Amazon EKS clusters\.