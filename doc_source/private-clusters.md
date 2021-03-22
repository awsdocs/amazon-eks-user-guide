# Private clusters<a name="private-clusters"></a>

This topic describes how to deploy a private cluster without outbound internet access\. If you're not familiar with Amazon EKS networking, see [De\-mystifying cluster networking for Amazon EKS worker nodes](http://aws.amazon.com/blogs/containers/de-mystifying-cluster-networking-for-amazon-eks-worker-nodes/)\.

## Requirements<a name="private-cluster-requirements"></a>

The following requirements must be met to run Amazon EKS in a private cluster without outbound internet access\.
+ A container image must be in or copied to Amazon Elastic Container Registry \(Amazon ECR\) or to a registry inside the VPC to be pulled\. For more information, see [Creating local copies of container images](#container-images)\.
+ Endpoint private access is required for nodes to register with the cluster endpoint\. Endpoint public access is optional\. For more information, see [Amazon EKS cluster endpoint access control](cluster-endpoint.md)\.
+ You may need to include the VPC endpoints found at [VPC endpoints for private clusters](#vpc-endpoints-private-clusters)\.
+ You must include the following text to the bootstrap arguments when launching self\-managed nodes\. This text bypasses the Amazon EKS introspection and does not require access to the Amazon EKS API from within the VPC\. Replace <cluster\-endpoint> and <cluster\-certificate\-authority> with the values from your Amazon EKS cluster\.

  ```
  --apiserver-endpoint <cluster-endpoint> --b64-cluster-ca <cluster-certificate-authority>
  ```
+ The `aws-auth` ConfigMap must be created from within the VPC\. For more information about create the `aws-auth` ConfigMap, see [Managing users or IAM roles for your cluster](add-user-role.md)\.

## Considerations<a name="private-cluster-considerations"></a>

Here are some things to consider when running Amazon EKS in a private cluster without outbound internet access\.
+ AWS X\-Ray is not supported with private clusters\.
+ Amazon CloudWatch Logs is supported with private clusters, but you must use an Amazon CloudWatch Logs VPC endpoint\. For more information, see [VPC endpoints for private clusters](#vpc-endpoints-private-clusters)\.
+ Self\-managed and managed [nodes](worker.md) are supported\. The instances for nodes must have access to the VPC endpoints\. If you create a managed node group, the VPC endpoint security group must allow the CIDR for the subnets, or you must add the created node security group to the VPC endpoint security group\.
+ [IAM roles for service accounts](iam-roles-for-service-accounts.md) is supported\. You must include the STS VPC endpoint\. For more information, see [VPC endpoints for private clusters](#vpc-endpoints-private-clusters)\.
+ The [Amazon EBS CSI driver](ebs-csi.md) is supported\. Before deploying, the [kustomization\.yaml](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/deploy/kubernetes/overlays/stable/kustomization.yaml) file must be changed to set the container images to use the same Region as the Amazon EKS cluster\.
+ The [Amazon EFS CSI driver](efs-csi.md) is supported\. Before deploying, the [kustomization\.yaml](https://github.com/kubernetes-sigs/aws-efs-csi-driver/blob/master/deploy/kubernetes/overlays/stable/kustomization.yaml) file must be changed to set the container images to use the same Region as the Amazon EKS cluster\.
+ The [Amazon FSx for Lustre CSI driver](fsx-csi.md) is not supported\.
+ [AWS Fargate](fargate.md) is supported with private clusters\. You must include the STS VPC endpoint\. For more information, see [VPC endpoints for private clusters](#vpc-endpoints-private-clusters)\. You can use the AWS load balancer controller to deploy AWS Application Load Balancers and Network Load Balancers with\. The controller supports network load balancers with IP targets, which are required for use with Fargate\. For more information, see [Application load balancing on Amazon EKS](alb-ingress.md) and [Load balancer – IP targets](load-balancing.md#load-balancer-ip)\.
+ [App Mesh](https://docs.aws.amazon.com/app-mesh/latest/userguide/what-is-app-mesh.html) is supported with private clusters when you use the App Mesh Envoy VPC endpoint\. For more information, see [VPC endpoints for private clusters](#vpc-endpoints-private-clusters)\.
  + The App Mesh sidecar injector for Kubernetes is supported\. For more information, see [App Mesh sidecar injector](https://github.com/aws/aws-app-mesh-inject) on GitHub\.
  + The App Mesh controller for Kubernetes is not supported\. For more information, see [App Mesh controller](https://github.com/aws/aws-app-mesh-controller-for-k8s) on GitHub\.

## Creating local copies of container images<a name="container-images"></a>

Because a private cluster has no outbound internet access, container images cannot be pulled from external sources such as Docker Hub\. Instead, container images must be copied locally to Amazon ECR or to an alternative registry accessible in the VPC\. A container image can be copied to Amazon ECR from outside the private VPC\. The private cluster accesses the Amazon ECR repository using the Amazon ECR VPC endpoints\. You must have Docker and the AWS CLI installed on the workstation that you use to create the local copy\.

**To create a local copy of a container image**

1. Create an Amazon ECR repository\. For more information, see [Creating a repository](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html)\.

1. Pull the container image from the external registry using `docker pull`\.

1. Tag your image with the Amazon ECR registry, repository, and optional image tag name combination using `docker tag`\.

1. Authenticate to the registry\. For more information, see [Registry authentication](https://docs.aws.amazon.com/AmazonECR/latest/userguide/Registries.html#registry_auth)\.

1. [Push the image to Amazon ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html) using `docker push`\. 
**Note**  
 Be sure to update your resource configuration to use the new image location\.

   The following example pulls the [amazon/aws\-node\-termination\-handler](https://hub.docker.com/r/amazon/aws-node-termination-handler) image, using tag `v1.3.1-linux-amd64`, from Docker Hub and creates a local copy in Amazon ECR\.

   ```
   aws ecr create-repository --repository-name amazon/aws-node-termination-handler
   docker pull amazon/aws-node-termination-handler:v1.3.1-linux-amd64
   docker tag amazon/aws-node-termination-handler <111122223333>.dkr.ecr.<region-code>.amazonaws.com/amazon/aws-node-termination-handler:v1.3.1-linux-amd64
   aws ecr get-login-password --region <region-code> | docker login --username AWS --password-stdin <111122223333>.dkr.ecr.<region-code>.amazonaws.com
   docker push <111122223333>.dkr.ecr.<region-code>.amazonaws.com/amazon/aws-node-termination-handler:v1.3.1-linux-amd64
   ```

## VPC endpoints for private clusters<a name="vpc-endpoints-private-clusters"></a>

The following [VPC endpoints](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-endpoints.html) may be required\.
+ `com.amazonaws.<region>.ec2`
+ `com.amazonaws.<region>.ecr.api`
+ `com.amazonaws.<region>.ecr.dkr`
+ `com.amazonaws.<region>.s3` – For pulling container images
+ `com.amazonaws.<region>.logs` – For CloudWatch Logs
+ `com.amazonaws.<region>.sts` – If using AWS Fargate or IAM roles for service accounts
+ `com.amazonaws.<region>.elasticloadbalancing` – If using Application Load Balancers
+ `com.amazonaws.<region>.autoscaling` – If using Cluster Autoscaler
+ `com.amazonaws.<region>.appmesh-envoy-management` – If using App Mesh

## STS endpoints for IAM Roles for Service Accounts<a name="irsa-regional-endpoint"></a>

Pods configured with [IAM roles for service accounts](iam-roles-for-service-accounts.md) acquire credentials from an STS API call\. If there is no outbound internet access, you must create and use an [STS VPC endpoint](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_sts_vpce.html#id_credentials_sts_vpce_create) in your VPC\.

Note that most AWS v1 SDKs will use the global STS endpoint by default (`sts.amazonaws.com`), which will not use the STS VPC endpoint\. To use the STS VPC endpoint, you may need to configure the SDK to use the regional STS endpoint (`sts.<region-code>.amazonaws.com`)\. You can do this by setting the `AWS_STS_REGIONAL_ENDPOINTS` environment variable with a value of `regional`, along with the AWS region\.

For example, in a pod spec:

```yaml
...
  containers:
    - env:
      - name: AWS_REGION
        value: <region-code>
      - name: AWS_STS_REGIONAL_ENDPOINTS
        value: regional
      ...
```

Replace `<region-code>` with the Region that your cluster is in (`us-west-2` for example)\.
