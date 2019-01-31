# Amazon EKS Shared Responsibility Model<a name="shared-responsibilty"></a>

Security and compliance is a shared responsibility between AWS and the customer\. This shared model helps relieve your operational burden as AWS operates, manages, and controls the components from the host operating system and virtualization layer down to the physical security of the facilities in which the service operates\. For more information, see the official AWS [Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/) detail page\.

AWS is responsible for protecting the infrastructure that runs all services offered in the AWS Cloud\. This infrastructure is composed of the hardware, software, networking, and facilities that run AWS Cloud services\. For Amazon EKS, AWS is responsible for the Kubernetes control plane, which includes the control plane nodes and `etcd` database\. 

You assume responsibility and management of the following:
+ The security configuration of the data plane, including the configuration of the security groups that allow traffic to pass from the Amazon EKS control plane into the customer VPC
+ The configuration of the worker nodes and the containers themselves
+ The worker node guest operating system \(including updates and security patches\)
+ Other associated application software:
  + Setting up and managing network controls, such as firewall rules
  + Managing platform\-level identity and access management, either with or in addition to IAM

For more information about using AWS IAM with Amazon EKS, see [Amazon EKS IAM Policies, Roles, and Permissions](IAM_policies.md)\.

For more information about managing native Kubernetes [Role Based Access Control](https://kubernetes.io/docs/admin/authorization/rbac/) \(RBAC\) with Amazon EKS clusters, see [Managing Cluster Authentication](managing-auth.md)\.

Amazon EKS is integrated with AWS CloudTrail, a service that provides a record of actions taken by a user, role, or an AWS service in Amazon EKS\. CloudTrail captures all API calls for Amazon EKS as events\. For more information, see [Logging Amazon EKS API Calls with AWS CloudTrail](logging-using-cloudtrail.md)\.