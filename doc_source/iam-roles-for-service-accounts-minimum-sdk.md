# Using a supported AWS SDK<a name="iam-roles-for-service-accounts-minimum-sdk"></a>

When using [IAM roles for service accounts](iam-roles-for-service-accounts.md), the containers in your Pods must use an AWS SDK version that supports assuming an IAM role through an OpenID Connect web identity token file\. Make sure that you're using the following versions, or later, for your AWS SDK:
+ Java \(Version 2\) – [2\.10\.11](https://github.com/aws/aws-sdk-java-v2/releases/tag/2.10.11)
+ Java – [1\.11\.704](https://github.com/aws/aws-sdk-java/releases/tag/1.11.704)
+ Go – [1\.23\.13](https://github.com/aws/aws-sdk-go/releases/tag/v1.23.13)
+ Python \(Boto3\) – [1\.9\.220](https://github.com/boto/boto3/releases/tag/1.9.220)
+ Python \(botocore\) – [1\.12\.200](https://github.com/boto/botocore/releases/tag/1.12.200)
+ AWS CLI – [1\.16\.232](https://github.com/aws/aws-cli/releases/tag/1.16.232)
+ Node – [2\.525\.0](https://github.com/aws/aws-sdk-js/releases/tag/v2.525.0) and [3\.27\.0](https://github.com/aws/aws-sdk-js-v3/releases/tag/v3.27.0)
+ Ruby – [3\.58\.0](https://github.com/aws/aws-sdk-ruby/blob/version-3/gems/aws-sdk-core/CHANGELOG.md#3580-2019-07-01)
+ C\+\+ – [1\.7\.174](https://github.com/aws/aws-sdk-cpp/releases/tag/1.7.174)
+ \.NET – [3\.3\.659\.1](https://github.com/aws/aws-sdk-net/releases/tag/3.3.659.1) – You must also include `AWSSDK.SecurityToken`\.
+ PHP – [3\.110\.7](https://github.com/aws/aws-sdk-php/releases/tag/3.110.7)

Many popular Kubernetes add\-ons, such as the [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler), the [Installing the AWS Load Balancer Controller add\-on](aws-load-balancer-controller.md), and the [Amazon VPC CNI plugin for Kubernetes](cni-iam-role.md) support IAM roles for service accounts\.

To ensure that you're using a supported SDK, follow the installation instructions for your preferred SDK at [Tools to Build on AWS](https://aws.amazon.com/tools/) when you build your containers\. 