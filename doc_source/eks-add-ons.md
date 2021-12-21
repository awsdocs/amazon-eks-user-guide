# Amazon EKS add\-ons<a name="eks-add-ons"></a>

An add\-on is software that provides supporting operational capabilities to Kubernetes applications, but is not specific to the application\. This includes software like observability agents or Kubernetes drivers that allow the cluster to interact with underlying AWS resources for networking, compute, and storage\. Add\-on software is typically built and maintained by the Kubernetes community, cloud providers like AWS, or third\-party vendors\. Amazon EKS automatically installs self\-managed add\-ons such as the Amazon VPC CNI, `kube-proxy`, and CoreDNS for every cluster\. You can change the default configuration of the add\-ons and update them when desired\.

 Amazon EKS add\-ons provide installation and management of a curated set of add\-ons for Amazon EKS clusters\. All Amazon EKS add\-ons include the latest security patches, bug fixes, and are validated by AWS to work with Amazon EKS\. Amazon EKS add\-ons allow you to consistently ensure that your Amazon EKS clusters are secure and stable and reduce the amount of work that you need to do in order to install, configure, and update add\-ons\. If a self\-managed add\-on, such as `kube-proxy` is already running on your cluster and is available as an Amazon EKS add\-on, then you can install the `kube-proxy` Amazon EKS add\-on to start benefiting from the capabilities of Amazon EKS add\-ons\.

You can update specific Amazon EKS managed configuration fields for Amazon EKS add\-ons through the Amazon EKS API\. You can also modify configuration fields not managed by Amazon EKS directly within the Kubernetes cluster once the add\-on starts\. This includes defining specific configuration fields for an add\-on where applicable\. These changes are not overridden by Amazon EKS once they are made\. This is made possible using the Kubernetes server\-side apply feature\. For more information, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.

Amazon EKS add\-ons can be used with any 1\.18 or later Amazon EKS cluster\. The cluster can include self\-managed and Amazon EKS managed node groups, and Fargate\.

**Considerations**
+ To configure add\-ons for the cluster your IAM user must have IAM permissions to work with add\-ons\. For more information, see the actions with `Addon` in their name in [Actions defined by Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html#amazonelastickubernetesservice-actions-as-permissions)\.
+ Amazon EKS add\-ons are only available with Amazon EKS clusters running Kubernetes version 1\.18 and later\.
+ Amazon EKS add\-ons run on the nodes that you provision or configure for your cluster\. Node types include Amazon EC2 instances and Fargate\.
+ You can modify fields that aren't managed by Amazon EKS to customize the installation of an Amazon EKS add\-on\. For more information, see [Amazon EKS add\-on configuration](add-ons-configuration.md)\.
+ If you create a cluster with the AWS Management Console, the Amazon EKS `kube-proxy`, Amazon VPC CNI, and CoreDNS Amazon EKS add\-ons are automatically added to your cluster\. If you use eksctl to create your cluster with a `config` file, `eksctl` can also create the cluster with Amazon EKS add\-ons\. If you create your cluster using `eksctl` without a `config` file or with any other tool, the self\-managed `kube-proxy`, Amazon VPC CNI, and CoreDNS add\-ons are installed, rather than the Amazon EKS add\-ons\. You can either manage them yourself or add the Amazon EKS add\-ons manually after cluster creation\.

You can add, update, or delete Amazon EKS add\-ons using the Amazon EKS API, AWS Management Console, AWS CLI, and `eksctl`\. For detailed steps when using the AWS Management Console, AWS CLI, and `eksctl`, see the topics for the following add\-ons:
+ [Amazon VPC CNI](managing-vpc-cni.md)
+ [CoreDNS](managing-coredns.md) 
+ [kube\-proxy](managing-kube-proxy.md)
+ [Amazon EBS CSI](managing-ebs-csi.md)

You can also create Amazon EKS add\-ons using [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-addon.html)\.