# Amazon container image registries<a name="add-ons-images"></a>

When you deploy add\-ons such as the [Installing the AWS Load Balancer Controller add\-on](aws-load-balancer-controller.md), the [Amazon VPC CNI](managing-vpc-cni.md#updating-vpc-cni-add-on), [`kube-proxy`](managing-kube-proxy.md#updating-kube-proxy-add-on), or [storage drivers](storage.md) to your cluster, your nodes might pull the container image from an Amazon EKS Amazon ECR private repository\. The image's registry, repository, and tag are specified in a manifest or Helm `values.yaml` file referenced in the topics for each add\-on that you deploy\.

Amazon EKS replicates the images to a repository in each Amazon EKS supported AWS Region\. Your nodes can pull the container image over the internet from any of the following registries\. Alternatively, your nodes can pull the image over Amazon's network if you created an [interface VPC endpoint for Amazon ECR \(AWS PrivateLink\)](https://docs.aws.amazon.com/AmazonECR/latest/userguide/vpc-endpoints.html) in your VPC\. The registries require authentication with an AWS IAM account\. Your nodes authenticate using the [Amazon EKS node IAM role](create-node-role.md), which has the permissions in the [AmazonEC2ContainerRegistryReadOnly](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly%24jsonEditor) managed IAM policy associated to it\.


| AWS Region | Registry | 
| --- | --- | 
| af\-south\-1 | 877085696533\.dkr\.ecr\.af\-south\-1\.amazonaws\.com | 
| ap\-east\-1 | 800184023465\.dkr\.ecr\.ap\-east\-1\.amazonaws\.com | 
| ap\-northeast\-1 | 602401143452\.dkr\.ecr\.ap\-northeast\-1\.amazonaws\.com | 
| ap\-northeast\-2 | 602401143452\.dkr\.ecr\.ap\-northeast\-2\.amazonaws\.com | 
| ap\-northeast\-3 | 602401143452\.dkr\.ecr\.ap\-northeast\-3\.amazonaws\.com | 
| ap\-south\-1 | 602401143452\.dkr\.ecr\.ap\-south\-1\.amazonaws\.com | 
| ap\-southeast\-1 | 602401143452\.dkr\.ecr\.ap\-southeast\-1\.amazonaws\.com | 
| ap\-southeast\-2 | 602401143452\.dkr\.ecr\.ap\-southeast\-2\.amazonaws\.com | 
| ap\-southeast\-3 | 296578399912\.dkr\.ecr\.ap\-southeast\-3\.amazonaws\.com | 
| ca\-central\-1 | 602401143452\.dkr\.ecr\.ca\-central\-1\.amazonaws\.com | 
| cn\-north\-1 | 918309763551\.dkr\.ecr\.cn\-north\-1\.amazonaws\.com | 
| cn\-northwest\-1 | 961992271922\.dkr\.ecr\.cn\-northwest\-1\.amazonaws\.com | 
| eu\-central\-1 | 602401143452\.dkr\.ecr\.eu\-central\-1\.amazonaws\.com | 
| eu\-north\-1 | 602401143452\.dkr\.ecr\.eu\-north\-1\.amazonaws\.com | 
| eu\-south\-1 | 590381155156\.dkr\.ecr\.eu\-south\-1\.amazonaws\.com | 
| eu\-west\-1 | 602401143452\.dkr\.ecr\.eu\-west\-1\.amazonaws\.com | 
| eu\-west\-2 | 602401143452\.dkr\.ecr\.eu\-west\-2\.amazonaws\.com | 
| eu\-west\-3 | 602401143452\.dkr\.ecr\.eu\-west\-3\.amazonaws\.com | 
| me\-south\-1 | 558608220178\.dkr\.ecr\.me\-south\-1\.amazonaws\.com | 
| sa\-east\-1 | 602401143452\.dkr\.ecr\.sa\-east\-1\.amazonaws\.com | 
| us\-east\-1 | 602401143452\.dkr\.ecr\.us\-east\-1\.amazonaws\.com | 
| us\-east\-2 | 602401143452\.dkr\.ecr\.us\-east\-2\.amazonaws\.com | 
| us\-gov\-east\-1 | 151742754352\.dkr\.ecr\.us\-gov\-east\-1\.amazonaws\.com | 
| us\-gov\-west\-1 | 013241004608\.dkr\.ecr\.us\-gov\-west\-1\.amazonaws\.com | 
| us\-west\-1 | 602401143452\.dkr\.ecr\.us\-west\-1\.amazonaws\.com | 
| us\-west\-2 | 602401143452\.dkr\.ecr\.us\-west\-2\.amazonaws\.com | 