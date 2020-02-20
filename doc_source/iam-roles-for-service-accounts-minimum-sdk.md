# Using a Supported AWS SDK<a name="iam-roles-for-service-accounts-minimum-sdk"></a>

The containers in your pods must use an AWS SDK version that supports assuming an IAM role via an OIDC web identity token file\. AWS SDKs that are included in Linux distribution package managers may not be new enough to support this feature\. Be sure to use at least the minimum SDK versions listed below:
+ Java \(Version 2\) — [2\.10\.11](https://github.com/aws/aws-sdk-java-v2/releases/tag/2.10.11)
+ Java — [1\.11\.625](https://github.com/aws/aws-sdk-java/releases/tag/1.11.625)
+ Go — [1\.23\.13](https://github.com/aws/aws-sdk-go/releases/tag/v1.23.13)
+ Python \(Boto3\) — [1\.9\.220](https://github.com/boto/boto3/releases/tag/1.9.220)
+ Python \(botocore\) — [1\.12\.200](https://github.com/boto/botocore/releases/tag/1.12.200)
+ AWS CLI — [1\.16\.232](https://github.com/aws/aws-cli/releases/tag/1.16.232)
+ Node — [2\.521\.0](https://github.com/aws/aws-sdk-js/releases/tag/v2.521.0)
+ Ruby — [2\.11\.345](https://github.com/aws/aws-sdk-ruby/releases/tag/v2.11.345)
+ C\+\+ — [1\.7\.174](https://github.com/aws/aws-sdk-cpp/releases/tag/1.7.174)
+ PHP — [3\.110\.7](https://github.com/aws/aws-sdk-php/releases/tag/3.110.7)
+ .NET — [3\.3\.652\.1](https://github.com/aws/aws-sdk-net/releases/tag/3.3.652.1)

Many popular Kubernetes add\-ons, such as the [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler) and the [ALB Ingress Controller](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/cloudprovider/aws/CA_with_AWS_IAM_OIDC.md) support IAM roles for service accounts\. The [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) has been updated with a supported version of the AWS SDK for Go, and you can use the IAM roles for service accounts feature to provide the required permissions for the CNI to work\.

To ensure that you are using a supported SDK, follow the installation instructions for your preferred SDK at [Tools for Amazon Web Services](https://aws.amazon.com/tools/) when you build your containers\. 