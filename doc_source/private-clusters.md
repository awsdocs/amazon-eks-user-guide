# Private clusters<a name="private-clusters"></a>

This chapter discusses running Amazon EKS in a private cluster without outbound internet access, commonly referred to as "air-gapped".

## Private cluster considerations<a name="private-cluster-considerations"></a>

Here's some things to consider when running Amazon EKS in a private cluster without outbound internet access\.
+ Any container image that is not in Amazon ECR or a registry inside the VPC will need to be copied to Amazon ECR or a registry inside the VPC in order to be pulled\. See [Creating local copies of container images](#creating-local-copies-of-container-images)\.
+ **Endpoint private access** is required in order for the worker nodes to register with the cluster endpoint\. **Endpoint public access** is optional\.
+ You must bypass the EKS cluster introspection by providing the cluster certificate authority and cluster API endpoint to the worker nodes\.
+ You must include the VPC endpoints found at [VPC endpoints for private clusters](#vpc-endpoints-for-private-clusters)\.
+ Managed node groups is not supported with private clusters\.
+ eksctl is not supported with private clusters\.
+ AWS X-Ray is not supported with private clusters\.
+ CloudWatch Logs is supported with private clusters\. You must include the CloudWatch Logs VPC endpoint\.
+ For deploying worker nodes, [Self-managed nodes](launch-workers#self-managed-nodes) and [Amazon EKS managed node groups](launch-workers#amazon-eks-managed-node-groups) are supported\.
  + The instances for worker nodes must have access to the VPC endpoints\. If you are creating a managed node group, the VPC endpoint security group must allow the CIDR for the subnets or you must add the created worker node security group to the VPC endpoint security group\.
+ You need to include the following to the bootstrap arguments when launching worker nodes\. This will bypass the EKS introspection and does not require access to the EKS API from within the VPC\. Substitute the *{CLUSTER_ENDPOINT}* and *{CLUSTER_CERTIFICATE_AUTHORITY}* for the values from your EKS cluster\.

   ```
   --apiserver-endpoint {CLUSTER_ENDPOINT} --b64-cluster-ca {CLUSTER_CERTIFICATE_AUTHORITY}
   ```

+ [IAM roles for service accounts](iam-roles-for-service-accounts) is supported\. You must include the STS VPC endpoint\.
+ The [Amazon EBS CSI driver](ebs-csi) is supported\. When deploying, the [kustomization.yaml](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/deploy/kubernetes/overlays/stable/kustomization.yaml) file must be changed to set the container images to use the same region as the EKS cluster\.
+ The [Amazon EFS CSI driver](efs-csi) is supported\. When deploying, the [kustomization.yaml](https://github.com/kubernetes-sigs/aws-efs-csi-driver/blob/master/deploy/kubernetes/overlays/stable/kustomization.yaml) file must be changed to set the container images to use the same region as the EKS cluster\.
+ The [Amazon FSx for Lustre CSI driver](fsx-csi) is not supported\.
+ The `aws-auth` ConfigMap must be created from within the VPC\.
+ The [ALB Ingress Controller on Amazon EKS](alb-ingress) does not work in private clusters\.
+ [AWS Fargate](fargate) is supported with private clusters. You must include the STS VPC endpoint\.
   + You must use a third-party ingress controller with AWS Fargate, since the ALB Ingress Controller on Amazon EKS does not work in private clusters and Classic Load Balancers and Network Load Balancers are not supported on pods running on Fargate\.
+ Autoscaling requires the Autoscaling VPC endpoint\.
+ [App Mesh](appmesh-getting-started) is supported with private clusters when using the App Mesh Envoy VPC endpoint\.
  + The App Mesh sidecar injector for Kubernetes is supported\.
  + The App Mesh controller for Kubernetes is not supported\.

## Creating local copies of container images<a name="creating-local-copies-of-container-images"></a>

Since a private cluster has no outbound internet access, container images cannot be pulled from external sources, such as Docker Hub. Instead, container images must be copied locally to Amazon ECR, or alternatively a registry running in the VPC.

A container image can be copied to Amazon ECR from outside the private VPC. The private cluster will access the ECR repository using the ECR VPC endpoints. You must have Docker and the AWS CLI installed on the workstation used to create the local copy.

**To create a local copy of a container image** *{SOURCE_IMAGE}*

1. [Create a repository](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html)\.

1. Pull the container image from the external registry using **docker pull**\.

1. Tag your image with the Amazon ECR registry, repository, and optional image tag name combination using **docker tag**\.

1. [Authenticate to the registry](https://docs.aws.amazon.com/AmazonECR/latest/userguide/Registries.html#registry_auth)\.

1. [Push the image to Amazon ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html)\ using **docker push**.

**Note**
Be sure to update your resource configuration to use the new image location.

The following example pulls the [amazon/aws-node-termination-handler](https://hub.docker.com/r/amazon/aws-node-termination-handler) image (using tag **v1.3.1-linux-amd64**) from Docker Hub and creates a local copy in Amazon ECR.

```
aws ecr create-repository --repository-name amazon/aws-node-termination-handler
docker pull amazon/aws-node-termination-handler:v1.3.1-linux-amd64
docker tag amazon/aws-node-termination-handler *aws_account_id*.dkr.ecr.*region*.amazonaws.com/amazon/aws-node-termination-handler:v1.3.1-linux-amd64
aws ecr get-login-password --region *REGION* | docker login --username AWS --password-stdin *aws_account_id*.dkr.ecr.*region*.amazonaws.com
docker push *aws_account_id*.dkr.ecr.*region*.amazonaws.com/amazon/aws-node-termination-handler:v1.3.1-linux-amd64
```

## VPC endpoints for private clusters<a name="vpc-endpoints-for-private-clusters"></a>

The following [VPC endpoints](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-endpoints.html) may be required.

+ **com.amazonaws.REGION.ec2**
+ **com.amazonaws.REGION.ecr.api**
+ **com.amazonaws.REGION.ecr.dkr**
+ **com.amazonaws.REGION.s3** for pulling container images
+ **com.amazonaws.REGION.logs**
+ **com.amazonaws.REGION.sts** if using AWS Fargate or IAM Roles for Service Accounts
+ **com.amazonaws.REGION.elasticloadbalancing** if using Application Load Balancers
+ **com.amazonaws.REGION.autoscaling** if using Cluster Autoscaler
+ **com.amazonaws.REGION.appmesh-envoy-management** if using App Mesh
