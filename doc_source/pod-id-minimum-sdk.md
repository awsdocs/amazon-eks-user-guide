# Using a supported AWS SDK<a name="pod-id-minimum-sdk"></a>

**Important**  
An earlier version of the documentation was incorrect\. The AWS SDK for Java v1 doesn't support EKS Pod Identity\.

When using [EKS Pod Identities](pod-identities.md), the containers in your Pods must use an AWS SDK version that supports assuming an IAM role from the EKS Pod Identity Agent\. Make sure that you're using the following versions, or later, for your AWS SDK:
+ Java \(Version 2\) – [2\.21\.30](https://github.com/aws/aws-sdk-java-v2/releases/tag/2.21.30)
+ Go v1 – [v1\.47\.11](https://github.com/aws/aws-sdk-go/releases/tag/v1.47.11)
+ Go v2 – [release\-2023\-11\-14](https://github.com/aws/aws-sdk-go-v2/releases/tag/release-2023-11-14)
+ Python \(Boto3\) – [1\.34\.41](https://github.com/boto/boto3/releases/tag/1.34.41)
+ Python \(botocore\) – [1\.32\.0](https://github.com/boto/botocore/releases/tag/1.32.0)
+ AWS CLI – [1\.30\.0](https://github.com/aws/aws-cli/releases/tag/1.30.0)

  AWS CLI – [2\.15\.0](https://github.com/aws/aws-cli/releases/tag/2.15.0)
+ JavaScript v2 – [2\.1550\.0](https://github.com/aws/aws-sdk-js/releases/tag/v2.1550.0)
+ JavaScript v3 – [3\.458\.0](https://github.com/aws/aws-sdk-js-v3/releases/tag/v3.458.0)
+ Ruby – [3\.188\.0](https://github.com/aws/aws-sdk-ruby/blob/version-3/gems/aws-sdk-core/CHANGELOG.md#31880-2023-11-22)
+ C\+\+ – [1\.11\.263](https://github.com/aws/aws-sdk-cpp/releases/tag/1.11.263)
+ \.NET – [3\.7\.734\.0](https://github.com/aws/aws-sdk-net/releases/tag/3.7.734.0) –
+ PHP – [3\.287\.1](https://github.com/aws/aws-sdk-php/releases/tag/3.287.1)

To ensure that you're using a supported SDK, follow the installation instructions for your preferred SDK at [Tools to Build on AWS](https://aws.amazon.com/tools/) when you build your containers\.

## Using EKS Pod Identity credentials<a name="pod-id-using-creds"></a>

To use the credentials from a EKS Pod Identity association, your code can use any AWS SDK to create a client for an AWS service with an SDK, and by default the SDK searches in a chain of locations for AWS Identity and Access Management credentials to use\. The EKS Pod Identity credentials will be used if you don't specify a credential provider when you create the client or otherwise initialized the SDK\.

This works because EKS Pod Identities have been added to the *Container credential provider* which is searched in a step in the default credential chain\. If your workloads currently use credentials that are earlier in the chain of credentials, those credentials will continue to be used even if you configure an EKS Pod Identity association for the same workload\.

For more information about how EKS Pod Identities work, see [How EKS Pod Identity works](pod-id-how-it-works.md)\.