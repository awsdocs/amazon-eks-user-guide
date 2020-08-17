# Using Service\-Linked Roles for Amazon EKS<a name="using-service-linked-roles"></a>

Amazon Elastic Kubernetes Service uses AWS Identity and Access Management \(IAM\) [service\-linked roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html#iam-term-service-linked-role)\. A service\-linked role is a unique type of IAM role that is linked directly to Amazon EKS\. Service\-linked roles are predefined by Amazon EKS and include all the permissions that the service requires to call other AWS services on your behalf\. 

**Topics**
+ [Using Roles for Amazon EKS](using-service-linked-roles-eks.md)
+ [Using Roles for Amazon EKS node groups](using-service-linked-roles-eks-nodegroups.md)