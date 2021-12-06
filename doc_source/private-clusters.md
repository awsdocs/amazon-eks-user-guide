# Private clusters<a name="private-clusters"></a>

This topic describes how to deploy an Amazon EKS private cluster without outbound internet access\. If you're not familiar with Amazon EKS networking, see [De\-mystifying cluster networking for Amazon EKS worker nodes](http://aws.amazon.com/blogs/containers/de-mystifying-cluster-networking-for-amazon-eks-worker-nodes/)\.

## Requirements<a name="private-cluster-requirements"></a>

The following requirements must be met to run Amazon EKS in a private cluster without outbound internet access\.
+ A container image must be in or copied to Amazon Elastic Container Registry \(Amazon ECR\) or to a registry inside the VPC to be pulled\. For more information, see [Creating local copies of container images](#container-images)\.
+ Endpoint private access is required for nodes to register with the cluster endpoint\. Endpoint public access is optional\. For more information, see [Amazon EKS cluster endpoint access control](cluster-endpoint.md)\.
+ You may need to include the VPC endpoints found at [VPC endpoints for private clusters](#vpc-endpoints-private-clusters)\.
+ For Linux and Windows nodes, you must include bootstrap arguments when launching self\-managed nodes\. This text bypasses the Amazon EKS introspection and doesn't require access to the Amazon EKS API from within the VPC\. Replace *<api\-server\-endpoint>* and *<certificate\-authority>* with the values from your Amazon EKS cluster\.
  + For Linux nodes:

    ```
    --apiserver-endpoint <api-server-endpoint> --b64-cluster-ca <certificate-authority>
    ```

    For additional arguments, see the [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) on GitHub\.
  + For Windows nodes:

    ```
    -APIServerEndpoint <api-server-endpoint> -Base64ClusterCA <certificate-authority>
    ```

    For additional arguments, see [Amazon EKS optimized Windows AMI](eks-custom-ami-windows.md)\.
+ The `aws-auth` ConfigMap must be created from within the VPC\. For more information about create the `aws-auth` ConfigMap, see [Managing users or IAM roles for your cluster](add-user-role.md)\.

## Considerations<a name="private-cluster-considerations"></a>

Here are some things to consider when running Amazon EKS in a private cluster without outbound internet access\.
+ AWS X\-Ray is supported with private clusters, but you must use an AWS X\-Ray VPC endpoint\. For more information, see [VPC endpoints for private clusters](#vpc-endpoints-private-clusters)\.
+ Amazon CloudWatch Logs is supported with private clusters, but you must use an Amazon CloudWatch Logs VPC endpoint\. For more information, see [VPC endpoints for private clusters](#vpc-endpoints-private-clusters)\.
+ Self\-managed and managed [nodes](worker.md) are supported\. The instances for nodes must have access to the VPC endpoints\. If you create a managed node group, the VPC endpoint security group must allow the CIDR for the subnets, or you must add the created node security group to the VPC endpoint security group\.
+ [IAM roles for service accounts](iam-roles-for-service-accounts.md) is supported\. You must include the STS VPC endpoint\. For more information, see [VPC endpoints for private clusters](#vpc-endpoints-private-clusters)\.
+ The [Amazon EBS CSI driver](ebs-csi.md) is supported\. Before deploying, the [kustomization\.yaml](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/deploy/kubernetes/overlays/stable/kustomization.yaml) file must be changed to set the container images to use the same Region as the Amazon EKS cluster\.
+ The [Amazon EFS CSI driver](efs-csi.md) is supported\. Before deploying, the [kustomization\.yaml](https://github.com/kubernetes-sigs/aws-efs-csi-driver/blob/master/deploy/kubernetes/overlays/stable/kustomization.yaml) file must be changed to set the container images to use the same Region as the Amazon EKS cluster\.
+ The [Amazon FSx for Lustre CSI driver](fsx-csi.md) isn't supported\.
+ [AWS Fargate](fargate.md) is supported with private clusters\. You can use the AWS Load Balancer Controller to deploy AWS Application Load Balancers \(ALBs\) and Network Load Balancers with\. The controller supports network load balancers with IP targets, which are required for use with Fargate\. For more information, see [Application load balancing on Amazon EKS](alb-ingress.md) and [Create a network load balancer](network-load-balancing.md#network-load-balancer)\.
+ [AWS Load Balancer Controller](aws-load-balancer-controller.md) is supported\. However, while installing, you should use [command line flags](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.2/deploy/configurations/#controller-command-line-flags) to set `enable-shield`, `enable-waf`, and `enable-wafv2` to false\. In addition, [certificate discovery](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.1/guide/ingress/cert_discovery/#discover-via-ingress-rule-host)) with hostnames from the Ingress objects isn't supported\. This is because the controller needs to reach ACM, which doesn't have a VPC endpoint\.
+ [App Mesh](https://docs.aws.amazon.com/app-mesh/latest/userguide/what-is-app-mesh.html) is supported with private clusters when you use the App Mesh Envoy VPC endpoint\. For more information, see [VPC endpoints for private clusters](#vpc-endpoints-private-clusters)\.
  + The App Mesh sidecar injector for Kubernetes is supported\. For more information, see [App Mesh sidecar injector](https://github.com/aws/aws-app-mesh-inject) on GitHub\.
  + The App Mesh controller for Kubernetes isn't supported\. For more information, see [App Mesh controller](https://github.com/aws/aws-app-mesh-controller-for-k8s) on GitHub\.
  + [Cluster Autoscaler](autoscaling.md#cluster-autoscaler) is supported\. When deploying Cluster Autoscaler pods, make sure that the command line includes `--aws-use-static-instance-list=true`\. For more information, see [Use Static Instance List](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/cloudprovider/aws/README.md#use-static-instance-list) on GitHub\. The worker node VPC must also include the STS VPC endpoint and autoscaling VPC endpoint\. For more information, see [VPC endpoints for private clusters](#vpc-endpoints-private-clusters)\.

## Creating local copies of container images<a name="container-images"></a>

Because a private cluster has no outbound internet access, container images can't be pulled from external sources such as Docker Hub\. Instead, container images must be copied locally to Amazon ECR or to an alternative registry accessible in the VPC\. A container image can be copied to Amazon ECR from outside the private VPC\. The private cluster accesses the Amazon ECR repository using the Amazon ECR VPC endpoints\. You must have Docker and the AWS CLI installed on the workstation that you use to create the local copy\.

**To create a local copy of a container image**

1. Create an Amazon ECR repository\. For more information, see [Creating a repository](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html)\.

1. Pull the container image from the external registry using `docker pull`\.

1. Tag your image with the Amazon ECR registry, repository, and the optional image tag name combination using `docker tag`\.

1. Authenticate to the registry\. For more information, see [Registry authentication](https://docs.aws.amazon.com/AmazonECR/latest/userguide/Registries.html#registry_auth)\.

1. [Push the image to Amazon ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html) using `docker push`\. 
**Note**  
 Make sure to update your resource configuration to use the new image location\.

   The following example pulls the [amazon/aws\-node\-termination\-handler](https://hub.docker.com/r/amazon/aws-node-termination-handler) image, using tag `v1.3.1-linux-amd64`, from Docker Hub and creates a local copy in Amazon ECR\.

   ```
   aws ecr create-repository --repository-name amazon/aws-node-termination-handler
   docker pull amazon/aws-node-termination-handler:v1.3.1-linux-amd64
   docker tag amazon/aws-node-termination-handler <111122223333>.dkr.ecr.<region-code>.amazonaws.com/amazon/aws-node-termination-handler:v1.3.1-linux-amd64
   aws ecr get-login-password --region <region-code> | docker login --username AWS --password-stdin <111122223333>.dkr.ecr.<region-code>.amazonaws.com
   docker push <111122223333>.dkr.ecr.<region-code>.amazonaws.com/amazon/aws-node-termination-handler:v1.3.1-linux-amd64
   ```

## VPC endpoints for private clusters<a name="vpc-endpoints-private-clusters"></a>

The following [VPC endpoints](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-endpoints.html) might be required\.
+ `com.amazonaws.<region>.ec2`
+ `com.amazonaws.<region>.ecr.api`
+ `com.amazonaws.<region>.ecr.dkr`
+ `com.amazonaws.<region>.s3` – For pulling container images
+ `com.amazonaws.<region>.logs` – For CloudWatch Logs
+ `com.amazonaws.<region>.sts` – If using Cluster Autoscaler or IAM roles for service accounts
+ `com.amazonaws.<region>.elasticloadbalancing` – If using Application Load Balancers
+ `com.amazonaws.<region>.autoscaling` – If using Cluster Autoscaler
+ `com.amazonaws.<region>.appmesh-envoy-management` – If using App Mesh
+ `com.amazonaws.<region>.xray` – If using AWS X\-Ray