# Amazon EKS add\-ons<a name="eks-add-ons"></a>

Amazon EKS add\-ons provide installation and management of a curated list of Kubernetes operational software for EKS clusters\. All Amazon EKS add\-ons include the latest security patches, bug fixes, and are validated by AWS to work with Amazon EKS\. Amazon EKS add\-ons allow you to consistently ensure that your Amazon EKS clusters are secure and stable and reduce the amount of work that you need to do in order to start and manage production\-ready Kubernetes clusters on AWS\.

Amazon EKS add\-ons can be used with any 1\.18 or later Amazon EKS cluster\. The cluster can include self\-managed and custom nodes, Amazon EKS managed node groups, and Fargate\.

An add\-on is software that provides supporting operational capabilities to Kubernetes applications, but is not specific to the application\. This includes software like observability agents or Kubernetes drivers that allow the cluster to interact with underlying AWS resources for networking, compute, and storage\. Add\-on software is typically built and maintained by the Kubernetes community, cloud providers like AWS, or third\-party vendors\.

You can update specific Amazon EKS managed configuration fields through the Amazon EKS API\. You can also modify configuration fields not managed by Amazon EKS directly within the Kubernetes cluster once the add\-on starts\. This includes defining specific configuration fields for an add\-on where applicable\. These changes are not overridden by Amazon EKS once they are made\. This is made possible using the Kubernetes server side apply feature\. For more information, see [Add-on configuration](add-ons-configuration.md)\.

**Considerations**  
+ To configure add\-ons for the cluster your IAM user must have administrative privileges within the cluster\. For more information, see [Cluster authentication](managing-auth.md)\.
+ Amazon EKS add\-ons are only available with Amazon EKS clusters running Kubernetes version 1\.18 and later\.
+ Amazon EKS add\-ons run on the nodes that you provision or configure for your cluster\. Node types include Amazon EC2 instances and Fargate\.
+ You can modify fields that are not managed by Amazon EKS to customize the installation of an add-on. For more information, see [Add-on configuration](add-ons-configuration.md)\.

You can add, update, or delete Amazon EKS add\-ons using the Amazon EKS API, AWS Management Console, and AWS CLI\. For detailed steps when using the AWS Management Console and AWS CLI, see the topics for the following add\-ons:
+ [Amazon VPC CNI](managing-vpc-cni.md)
+ [CoreDNS](managing-coredns.md)
+ [kube\-proxy](managing-kube-proxy.md)

You can also create Amazon EKS add\-ons using [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-addon.html)\.
