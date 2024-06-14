# Logging Amazon EKS API calls with AWS CloudTrail<a name="logging-using-cloudtrail"></a>

Amazon EKS is integrated with AWS CloudTrail\. CloudTrail is a service that provides a record of actions by a user, role, or an AWS service in Amazon EKS\. CloudTrail captures all API calls for Amazon EKS as events\. This includes calls from the Amazon EKS console and from code calls to the Amazon EKS API operations\.

If you create a trail, you can enable continuous delivery of CloudTrail events to an Amazon S3 bucket\. This includes events for Amazon EKS\. If you don't configure a trail, you can still view the most recent events in the CloudTrail console in **Event history**\. Using the information that CloudTrail collects, you can determine several details about a request\. For example, you can determine when the request was made to Amazon EKS, the IP address where the request was made from, and who made the request\. 

To learn more about CloudTrail, see the [AWS CloudTrail User Guide](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/)\.

**Topics**
+ [Amazon EKS information in CloudTrail](service-name-info-in-cloudtrail.md)
+ [Understanding Amazon EKS log file entries](understanding-service-name-entries.md)
+ [Enable Auto Scaling group metrics collection](enable-asg-metrics.md)