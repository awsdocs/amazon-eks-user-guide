# Private clusters<a name="private-clusters"></a>

This topic describes how to deploy an Amazon EKS private cluster without outbound internet access\. If you're not familiar with Amazon EKS networking, see [De\-mystifying cluster networking for Amazon EKS worker nodes](http://aws.amazon.com/blogs/containers/de-mystifying-cluster-networking-for-amazon-eks-worker-nodes/)\.

## Requirements<a name="private-cluster-requirements"></a>

The following requirements must be met to run Amazon EKS in a private cluster without outbound internet access\.
+ A container image must be in or copied to Amazon Elastic Container Registry \(Amazon ECR\) or to a registry inside the VPC to be pulled\. For more information, see [Creating local copies of container images](#container-images)\.
+ Endpoint private access is required for nodes to register with the cluster endpoint\. Endpoint public access is optional\. For more information, see [Amazon EKS cluster endpoint access control](cluster-endpoint.md)\.
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
+ The `aws-auth` ConfigMap must be created from within the VPC\. For more information about create the `aws-auth` ConfigMap, see [Enabling IAM user and role access to your cluster](add-user-role.md)\.

## Considerations<a name="private-cluster-considerations"></a>

Here are some things to consider when running Amazon EKS in a private cluster without outbound internet access\.
+ Many AWS services support private clusters, but you must use a VPC endpoint\. For more information, see [VPC endpoints](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-endpoints.html)\. Some commonly\-used services and endpoints include:
  + [AWS X\-Ray](https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html) – `com.amazonaws.<region>.xray` – 
  + [Amazon CloudWatch Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html) – `com.amazonaws.<region>.logs`
  + [IAM roles for service accounts](iam-roles-for-service-accounts.md) – `com.amazonaws.<region>.sts`
  + [App Mesh](https://docs.aws.amazon.com/app-mesh/latest/userguide/what-is-app-mesh.html) – `com.amazonaws.<region>.appmesh-envoy-management` 
    + The App Mesh sidecar injector for Kubernetes is supported\. For more information, see [App Mesh sidecar injector](https://github.com/aws/aws-app-mesh-inject) on GitHub\.
    + The App Mesh controller for Kubernetes isn't supported\. For more information, see [App Mesh controller](https://github.com/aws/aws-app-mesh-controller-for-k8s) on GitHub\.
    + [Cluster Autoscaler](autoscaling.md#cluster-autoscaler) is supported\. When deploying Cluster Autoscaler pods, make sure that the command line includes `--aws-use-static-instance-list=true`\. For more information, see [Use Static Instance List](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/cloudprovider/aws/README.md#use-static-instance-list) on GitHub\. The worker node VPC must also include the STS VPC endpoint and autoscaling VPC endpoint\.
+ Before deploying the [Amazon EFS CSI driver](efs-csi.md) or [Amazon EFS CSI driver](efs-csi.md) , the [kustomization\.yaml](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/deploy/kubernetes/overlays/stable/kustomization.yaml) file must be changed to set the container images to use the same Region as the Amazon EKS cluster\.
+ Self\-managed and managed [nodes](worker.md) are supported\. The instances for nodes must have access to the VPC endpoints\. If you create a managed node group, the VPC endpoint security group must allow the CIDR for the subnets, or you must add the created node security group to the VPC endpoint security group\.
+ The [Amazon FSx for Lustre CSI driver](fsx-csi.md) isn't supported\.
+ [AWS Fargate](fargate.md) is supported with private clusters\. You can use the AWS Load Balancer Controller to deploy AWS Application Load Balancers \(ALBs\) and Network Load Balancers with\. The controller supports network load balancers with IP targets, which are required for use with Fargate\. For more information, see [Application load balancing on Amazon EKS](alb-ingress.md) and [Create a network load balancer](network-load-balancing.md#network-load-balancer)\.
+ [AWS Load Balancer Controller](aws-load-balancer-controller.md) is supported\. However, while installing, you should use [command line flags](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.2/deploy/configurations/#controller-command-line-flags) to set `enable-shield`, `enable-waf`, and `enable-wafv2` to false\. In addition, [certificate discovery](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.1/guide/ingress/cert_discovery/#discover-via-ingress-rule-host)) with hostnames from the Ingress objects isn't supported\. This is because the controller needs to reach ACM, which doesn't have a VPC endpoint\.

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

## AWS STS endpoints for IAM roles for service accounts<a name="sts-endpoints"></a>

Pods configured with [IAM roles for service accounts](iam-roles-for-service-accounts.md) acquire credentials from an AWS Security Token Service \(AWS STS\) API call\. If there is no outbound internet access, you must create and use an AWS STS [VPC endpoint](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_sts_vpce.html#id_credentials_sts_vpce_create) in your VPC\. Most AWS v1 SDKs use the global AWS STS endpoint by default \(`sts.amazonaws.com`\), which doesn't use the AWS STS VPC endpoint\. To use the AWS STS VPC endpoint, you may need to configure the SDK to use the regional AWS STS endpoint \(`sts.region-code.amazonaws.com`\)\. You can do this by setting the `AWS_STS_REGIONAL_ENDPOINTS` environment variable with a value of `regional`, along with the AWS Region\.

For example, in a pod spec:

```
            ...
            containers:
            - env:
            - name: '
            value: region-code
                - name: AWS_STS_REGIONAL_ENDPOINTS
                value: regional
                ...
                ```
```

Replace `region-code` with the Region that your cluster is in \(`us-west-2` for example\)\.