--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Private cluster requirements<a name="private-clusters"></a>

If you’re not familiar with Amazon EKS networking, see [De\-mystifying cluster networking for Amazon EKS worker nodes](https://aws.amazon.com/blogs/containers/de-mystifying-cluster-networking-for-amazon-eks-worker-nodes/)\. If your cluster doesn’t have outbound internet access, then it must meet the following requirements:
+ Self\-managed Linux and Windows nodes must include the following bootstrap arguments before they’re launched\. These arguments bypass Amazon EKS introspection and don’t require access to the Amazon EKS API from within the VPC\.

  1. Determine the value of your cluster’s endpoint with the following command\. Replace *my\-cluster* with the name of your cluster\.

     ```
     aws eks describe-cluster --name my-cluster --query cluster.endpoint --output text
     ```

     An example output is as follows\.

     ```
     https://`EXAMPLE108C897D9B2F1B21D5EXAMPLE`.`sk1`.`region-code`.eks.
     ```

  1. Determine the value of your cluster’s certificate authority with the following command\. Replace *my\-cluster* with the name of your cluster\.

     ```
     aws eks describe-cluster --name my-cluster --query cluster.certificateAuthority --output text
     ```

     The returned output is a long string\.
     + For Linux nodes:

       ```
       --apiserver-endpoint cluster-endpoint --b64-cluster-ca certificate-authority
       ```

       For additional arguments, see the [bootstrap script](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) on GitHub\.
     + For Windows nodes:
**Note**  
If you’re using custom service CIDR, then you need to specify it using the `-ServiceCIDR` parameter\. Otherwise, the DNS resolution for Pods in the cluster will fail\.

       ```
       -APIServerEndpoint cluster-endpoint -Base64ClusterCA certificate-authority
       ```
+ Your cluster’s `aws-auth`ConfigMap must be created from within your VPC. For more information about creating and adding entries to the `aws-auth`ConfigMap, enter `eksctl create iamidentitymapping --help` in your terminal\. If the `ConfigMap` doesn’t exist on your server, `eksctl` will create it when you use the command to add an identity mapping\.

## Unknown Title\!<a name="private-cluster-considerations"></a>
+ Your cluster’s VPC subnets must have a VPC interface endpoint for any AWS services that your Pods need access to\. For more information, see [Access an AWS service using an interface VPC endpoint](https://docs.aws.amazon.com/vpc/latest/privatelink/create-interface-endpoint.html)\. Some commonly\-used services and endpoints are listed in the following table\. For a complete list of endpoints, see [AWS services that integrate with AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/aws-services-privatelink-support.html) in the [AWS PrivateLink Guide](https://docs.aws.amazon.com/vpc/latest/privatelink/)\.
+ Any self\-managed nodes must be deployed to subnets that have the VPC interface endpoints that you require\. If you create a managed node group, the VPC interface endpoint security group must allow the CIDR for the subnets, or you must add the created node security group to the VPC interface endpoint security group\.
+ Some container software products use API calls that access the AWS Marketplace Metering Service to monitor usage\. Private clusters do not allow these calls, so you can’t use these container types in private clusters\.