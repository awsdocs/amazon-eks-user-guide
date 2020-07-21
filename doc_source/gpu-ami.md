# Amazon EKS\-optimized accelerated Amazon Linux 2 AMIs<a name="gpu-ami"></a>

The Amazon EKS\-optimized accelerated AMI is built on top of the standard Amazon EKS\-optimized Linux AMI, and is configured to serve as an optional image for Amazon EKS nodes to support GPU and [Inferentia](http://aws.amazon.com/machine-learning/inferentia/) based workloads\.

In addition to the standard Amazon EKS\-optimized AMI configuration, the accelerated AMI includes the following:
+ NVIDIA drivers
+ The `nvidia-container-runtime` \(as the default runtime\)
+ AWS Neuron container runtime

The AMI IDs for the latest Amazon EKS\-optimized accelerated AMI are shown in the following table\. You can also retrieve the IDs with an AWS Systems Manager parameter using different tools\. For more information, see [Retrieving Amazon EKS\-optimized Amazon Linux 2 AMI IDs](retrieve-ami-id.md)\.  

**Note**  
The Amazon EKS\-optimized accelerated AMI only supports GPU and Inferentia based instance types\. Be sure to specify these instance types in your node AWS CloudFormation template\. By using the Amazon EKS\-optimized accelerated AMI, you agree to [NVIDIA's end user license agreement \(EULA\)](https://www.nvidia.com/en-us/about-nvidia/eula-agreement/)\. 
The Amazon EKS\-optimized accelerated AMI was previously referred to as the *Amazon EKS\-optimized AMI with GPU support*\. 
Previous versions of the Amazon EKS\-optimized accelerated AMI installed the nvidia\-docker repository\. The repository is no longer included in Amazon EKS AMI version `v20200529` and later\. 

------
#### [ Kubernetes version 1\.17\.7 ]


| Region | Amazon EKS\-optimized accelerated Amazon Linux 2 AMI | 
| --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.17%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-east-2) | 
| US East \(N\. Virginia\) \(us\-east\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.17%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-east-1) | 
| US West \(Oregon\) \(us\-west\-2\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.17%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-west-2) | 
| Asia Pacific \(Hong Kong\) \(ap\-east\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.17%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-east-1) | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.17%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-south-1) | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.17%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-northeast-1) | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.17%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-northeast-2) | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.17%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-southeast-1) | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.17%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-southeast-2) | 
| Canada \(Central\) \(ca\-central\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.17%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ca-central-1) | 
| China \(Beijing\) \(cn\-north\-1\) | [View AMI ID](https://console.amazonaws.cn/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.17%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=cn-north-1) | 
| China \(Ningxia\) \(cn\-northwest\-1\) | [View AMI ID](https://console.amazonaws.cn/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.17%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=cn-northwest-1) | 
| Europe \(Frankfurt\) \(eu\-central\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.17%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-central-1) | 
| Europe \(Ireland\) \(eu\-west\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.17%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-west-1) | 
| Europe \(London\) \(eu\-west\-2\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.17%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-west-2) | 
| Europe \(Paris\) \(eu\-west\-3\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.17%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-west-3) | 
| Europe \(Stockholm\) \(eu\-north\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.17%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-north-1) | 
| Middle East \(Bahrain\) \(me\-south\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.17%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=me-south-1) | 
| South America \(São Paulo\) \(sa\-east\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.17%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=sa-east-1) | 
| AWS GovCloud \(US\-East\) \(us\-gov\-east\-1\) | [View AMI ID](https://console.amazonaws-us-gov.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.17%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-gov-east-1) | 
| AWS GovCloud \(US\-West\) \(us\-gov\-west\-1\) | [View AMI ID](https://console.amazonaws-us-gov.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.17%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-gov-west-1) | 

------
#### [ Kubernetes version 1\.16\.12 ]


| Region | Amazon EKS\-optimized accelerated Amazon Linux 2 AMI | 
| --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.16%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-east-2) | 
| US East \(N\. Virginia\) \(us\-east\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.16%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-east-1) | 
| US West \(Oregon\) \(us\-west\-2\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.16%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-west-2) | 
| Asia Pacific \(Hong Kong\) \(ap\-east\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.16%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-east-1) | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.16%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-south-1) | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.16%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-northeast-1) | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.16%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-northeast-2) | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.16%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-southeast-1) | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.16%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-southeast-2) | 
| Canada \(Central\) \(ca\-central\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.16%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ca-central-1) | 
| China \(Beijing\) \(cn\-north\-1\) | [View AMI ID](https://console.amazonaws.cn/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.16%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=cn-north-1) | 
| China \(Ningxia\) \(cn\-northwest\-1\) | [View AMI ID](https://console.amazonaws.cn/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.16%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=cn-northwest-1) | 
| Europe \(Frankfurt\) \(eu\-central\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.16%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-central-1) | 
| Europe \(Ireland\) \(eu\-west\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.16%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-west-1) | 
| Europe \(London\) \(eu\-west\-2\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.16%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-west-2) | 
| Europe \(Paris\) \(eu\-west\-3\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.16%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-west-3) | 
| Europe \(Stockholm\) \(eu\-north\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.16%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-north-1) | 
| Middle East \(Bahrain\) \(me\-south\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.16%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=me-south-1) | 
| South America \(São Paulo\) \(sa\-east\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.16%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=sa-east-1) | 
| AWS GovCloud \(US\-East\) \(us\-gov\-east\-1\) | [View AMI ID](https://console.amazonaws-us-gov.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.16%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-gov-east-1) | 
| AWS GovCloud \(US\-West\) \(us\-gov\-west\-1\) | [View AMI ID](https://console.amazonaws-us-gov.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.16%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-gov-west-1) | 

------
#### [ Kubernetes version 1\.15\.11 ]


| Region | Amazon EKS\-optimized accelerated Amazon Linux 2 AMI | 
| --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.15%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-east-2) | 
| US East \(N\. Virginia\) \(us\-east\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.15%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-east-1) | 
| US West \(Oregon\) \(us\-west\-2\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.15%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-west-2) | 
| Asia Pacific \(Hong Kong\) \(ap\-east\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.15%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-east-1) | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.15%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-south-1) | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.15%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-northeast-1) | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.15%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-northeast-2) | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.15%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-southeast-1) | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.15%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-southeast-2) | 
| Canada \(Central\) \(ca\-central\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.15%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ca-central-1) | 
| China \(Beijing\) \(cn\-north\-1\) | [View AMI ID](https://console.amazonaws.cn/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.15%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=cn-north-1) | 
| China \(Ningxia\) \(cn\-northwest\-1\) | [View AMI ID](https://console.amazonaws.cn/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.15%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=cn-northwest-1) | 
| Europe \(Frankfurt\) \(eu\-central\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.15%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-central-1) | 
| Europe \(Ireland\) \(eu\-west\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.15%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-west-1) | 
| Europe \(London\) \(eu\-west\-2\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.15%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-west-2) | 
| Europe \(Paris\) \(eu\-west\-3\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.15%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-west-3) | 
| Europe \(Stockholm\) \(eu\-north\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.15%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-north-1) | 
| Middle East \(Bahrain\) \(me\-south\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.15%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=me-south-1) | 
| South America \(São Paulo\) \(sa\-east\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.15%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=sa-east-1) | 
| AWS GovCloud \(US\-East\) \(us\-gov\-east\-1\) | [View AMI ID](https://console.amazonaws-us-gov.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.15%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-gov-east-1) | 
| AWS GovCloud \(US\-West\) \(us\-gov\-west\-1\) | [View AMI ID](https://console.amazonaws-us-gov.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.15%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-gov-west-1) | 

------
#### [ Kubernetes version 1\.14\.9 ]


| Region | Amazon EKS\-optimized accelerated Amazon Linux 2 AMI | 
| --- | --- | 
| US East \(Ohio\) \(us\-east\-2\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-east-2) | 
| US East \(N\. Virginia\) \(us\-east\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-east-1) | 
| US West \(Oregon\) \(us\-west\-2\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-west-2) | 
| Asia Pacific \(Hong Kong\) \(ap\-east\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-east-1) | 
| Asia Pacific \(Mumbai\) \(ap\-south\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-south-1) | 
| Asia Pacific \(Tokyo\) \(ap\-northeast\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-northeast-1) | 
| Asia Pacific \(Seoul\) \(ap\-northeast\-2\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-northeast-2) | 
| Asia Pacific \(Singapore\) \(ap\-southeast\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-southeast-1) | 
| Asia Pacific \(Sydney\) \(ap\-southeast\-2\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ap-southeast-2) | 
| Canada \(Central\) \(ca\-central\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=ca-central-1) | 
| China \(Beijing\) \(cn\-north\-1\) | [View AMI ID](https://console.amazonaws.cn/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=cn-north-1) | 
| China \(Ningxia\) \(cn\-northwest\-1\) | [View AMI ID](https://console.amazonaws.cn/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=cn-northwest-1) | 
| Europe \(Frankfurt\) \(eu\-central\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-central-1) | 
| Europe \(Ireland\) \(eu\-west\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-west-1) | 
| Europe \(London\) \(eu\-west\-2\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-west-2) | 
| Europe \(Paris\) \(eu\-west\-3\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-west-3) | 
| Europe \(Stockholm\) \(eu\-north\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=eu-north-1) | 
| Middle East \(Bahrain\) \(me\-south\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=me-south-1) | 
| South America \(São Paulo\) \(sa\-east\-1\) | [View AMI ID](https://console.aws.amazon.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=sa-east-1) | 
| AWS GovCloud \(US\-East\) \(us\-gov\-east\-1\) | [View AMI ID](https://console.amazonaws-us-gov.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-gov-east-1) | 
| AWS GovCloud \(US\-West\) \(us\-gov\-west\-1\) | [View AMI ID](https://console.amazonaws-us-gov.com/systems-manager/parameters/%252Faws%252Fservice%252Feks%252Foptimized-ami%252F1.14%252Famazon-linux-2-gpu%252Frecommended%252Fimage_id/description?region=us-gov-west-1) | 

------

**Important**  
These AMIs require the latest AWS CloudFormation node template\. You can't use these AMIs with a previous version of the node template; they will fail to join your cluster\. Be sure to upgrade any existing AWS CloudFormation node stacks with the latest template \(URL shown below\) before you attempt to use these AMIs\.  

```
https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-06-10/amazon-eks-nodegroup.yaml
```

The AWS CloudFormation node template launches your nodes with Amazon EC2 user data that triggers a specialized [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh)\. This script allows your nodes to discover and connect to your cluster's control plane automatically\. For more information, see [Launching self\-managed Amazon Linux 2 Linux nodes](launch-workers.md)\.

## Enabling GPU based workloads<a name="enabling-gpu-workloads"></a>

The following section describes how to run a workload on a GPU based instance with the Amazon EKS\-optimized accelerated AMI\. For more information about using Inferentia based workloads, see [Inferentia support](inferentia-support.md)\.

After your GPU nodes join your cluster, you must apply the [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin) as a DaemonSet on your cluster with the following command\.

```
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/1.0.0-beta6/nvidia-device-plugin.yml
```

You can verify that your nodes have allocatable GPUs with the following command:

```
kubectl get nodes "-o=custom-columns=NAME:.metadata.name,GPU:.status.allocatable.nvidia\.com/gpu"
```

## Example GPU manifest<a name="example-gpu-manifest"></a>

This section provides an example pod manifest for you to test that your GPU nodes are configured properly\.

**Example Get `nvidia-smi` output**  
This example pod manifest launches a Cuda container that runs `nvidia-smi` on a node\. Create a file called `nvidia-smi.yaml`, copy and paste the following manifest into it, and save the file\.  

```
apiVersion: v1
kind: Pod
metadata:
  name: nvidia-smi
spec:
  restartPolicy: OnFailure
  containers:
  - name: nvidia-smi
    image: nvidia/cuda:9.2-devel
    args:
    - "nvidia-smi"
    resources:
      limits:
        nvidia.com/gpu: 1
```
Apply the manifest with the following command:  

```
kubectl apply -f nvidia-smi.yaml
```
After the pod has finished running, view its logs with the following command:  

```
kubectl logs nvidia-smi
```
Output:  

```
Mon Aug  6 20:23:31 2018
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 396.26                 Driver Version: 396.26                    |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  Tesla V100-SXM2...  On   | 00000000:00:1C.0 Off |                    0 |
| N/A   46C    P0    47W / 300W |      0MiB / 16160MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
```