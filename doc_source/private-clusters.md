# Private cluster requirements<a name="private-clusters"></a>

This topic describes how to deploy an Amazon EKS cluster that doesn't have outbound internet access\. If you're not familiar with Amazon EKS networking, see [De\-mystifying cluster networking for Amazon EKS worker nodes](http://aws.amazon.com/blogs/containers/de-mystifying-cluster-networking-for-amazon-eks-worker-nodes/)\. If your cluster doesn't have outbound internet access, then it must meet the following requirements:
+ Your cluster must pull images from a container registry that's in your VPC\. You can create an Amazon Elastic Container Registry in your VPC and copy container images to it for your nodes to pull from\. For more information, see [Copy a container image from one repository to another repository](copy-image-to-repository.md)\.
+ Your cluster must have endpoint private access enabled\. This is required for nodes to register with the cluster endpoint\. Endpoint public access is optional\. For more information, see [Amazon EKS cluster endpoint access control](cluster-endpoint.md)\.
+ Self\-managed Linux and Windows nodes must include the following bootstrap arguments before they're launched\. These arguments bypass Amazon EKS introspection and don't require access to the Amazon EKS API from within the VPC\.

  1. Determine the value of your cluster's endpoint with the following command\. Replace *my\-cluster* with the name of your cluster\.

     ```
     aws eks describe-cluster --name my-cluster --query cluster.endpoint --output text
     ```

     The example output is as follows\.

     ```
     https://EXAMPLE108C897D9B2F1B21D5EXAMPLE.sk1.region-code.eks.amazonaws.com
     ```

  1. Determine the value of your cluster's certificate authority with the following command\. Replace *my\-cluster* with the name of your cluster\.

     ```
     aws eks describe-cluster --name my-cluster --query cluster.certificateAuthority --output text
     ```

     The returned output is a long string\.

  1. Replace `cluster-endpoint` and `certificate-authority` in the following commands with the values returned in the output from the previous commands\. For more information about specifying bootstrap arguments when launching self\-managed nodes, see [Launching self\-managed Amazon Linux nodes](launch-workers.md) and [Launching self\-managed Windows nodes](launch-windows-workers.md)\.
  + For Linux nodes:

    ```
    --apiserver-endpoint cluster-endpoint --b64-cluster-ca certificate-authority
    ```

    For additional arguments, see the [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) on GitHub\.
  + For Windows nodes:

    ```
    -APIServerEndpoint cluster-endpoint -Base64ClusterCA certificate-authority
    ```

    If you're using custom service CIDR, then you need to specify it using the `-ServiceCIDR` parameter\. For additional arguments, see [Amazon EKS optimized Windows AMI](eks-custom-ami-windows.md)\.
+ Your cluster's `aws-auth` `ConfigMap` must be created from within your VPC\. For more information about create the `aws-auth` `ConfigMap`, see [Enabling IAM user and role access to your cluster](add-user-role.md)\.
+ Pods configured with [IAM roles for service accounts](iam-roles-for-service-accounts.md) acquire credentials from an AWS Security Token Service \(AWS STS\) API call\. If there is no outbound internet access, you must create and use an AWS STS VPC endpoint in your VPC\. Most AWS `v1` SDKs use the global AWS STS endpoint by default \(`sts.amazonaws.com`\), which doesn't use the AWS STS VPC endpoint\. To use the AWS STS VPC endpoint, you might need to configure your SDK to use the regional AWS STS endpoint \(`sts.region-code.amazonaws.com`\)\. For more information, see [Configuring the AWS Security Token Service endpoint for a service account](configure-sts-endpoint.md)\.

## <a name="private-cluster-considerations"></a>
+ Your cluster's VPC subnets must have a VPC interface endpoint for any AWS services that your pods need access to\. For more information, see [Access an AWS service using an interface VPC endpoint](https://docs.aws.amazon.com/vpc/latest/privatelink/create-interface-endpoint.html)\. Some commonly\-used services and endpoints are listed in the following table\. For a complete list of endpoints, see [AWS services that integrate with AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/aws-services-privatelink-support.html) in the [AWS PrivateLink Guide](https://docs.aws.amazon.com/vpc/latest/privatelink/)\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/private-clusters.html)

**Considerations**
+ Any self\-managed nodes must be deployed to subnets that have the VPC interface endpoints that you require\. If you create a managed node group, the VPC interface endpoint security group must allow the CIDR for the subnets, or you must add the created node security group to the VPC interface endpoint security group\.
+ If your pods use Amazon EFS volumes, then before deploying the [Amazon EFS CSI driver](efs-csi.md), the driver's [kustomization\.yaml](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/deploy/kubernetes/overlays/stable/kustomization.yaml) file must be changed to set the container images to use the same AWS Region as the Amazon EKS cluster\.
+ You can use the [AWS Load Balancer Controller](aws-load-balancer-controller.md) to deploy AWS Application Load Balancers \(ALB\) and Network Load Balancers to your private cluster\. When deploying it, you should use [command line flags](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.4/deploy/configurations/#controller-command-line-flags) to set `enable-shield`, `enable-waf`, and `enable-wafv2` to false\. [Certificate discovery](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.4/guide/ingress/cert_discovery/#discover-via-ingress-rule-host) with hostnames from Ingress objects isn't supported\. This is because the controller needs to reach AWS Certificate Manager, which doesn't have a VPC interface endpoint\.

  The controller supports network load balancers with IP targets, which are required for use with Fargate\. For more information, see [Application load balancing on Amazon EKS](alb-ingress.md) and [Create a network load balancer](network-load-balancing.md#network-load-balancer)\.
+ The [Amazon FSx for Lustre CSI driver](fsx-csi.md) isn't supported\.
+ Some container software products use API calls that access the AWS Marketplace Metering Service to monitor usage\. Private clusters do not allow these calls, so you can't use these container types in private clusters\.