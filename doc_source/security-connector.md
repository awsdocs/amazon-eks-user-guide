# Amazon EKS Connector considerations<a name="security-connector"></a>

The Amazon EKS Connector is an open source component that runs on your Kubernetes cluster\. This cluster can be located outside of the AWS environment\. This creates additional considerations for security responsibilities\. This configuration can be illustrated by the following diagram\. Orange represents AWS responsibilities, and blue represents customer responsibilities:

![\[EKS Connector Responsibilities\]](http://docs.aws.amazon.com/eks/latest/userguide/images/connector-model.png)

This topic describes the differences in the responsibility model if the connected cluster is outside of AWS\.

## AWS responsibilities<a name="connect-aws-resp"></a>
+ Maintaining, building, and delivering Amazon EKS Connector, which is an [open source component](https://github.com/aws/amazon-eks-connector) that runs on a customer's Kubernetes cluster and communicates with AWS\.
+ Maintaining transport and application layer communication security between the connected Kubernetes cluster and AWS services\.

## Customer responsibilities<a name="connect-cust-resp"></a>
+ Kubernetes cluster specific security, specifically along the following lines:
  + Kubernetes Secrets must be properly encrypted and protected\.
  + Lock down access to the `eks-connector` namespace\.
+ Configuring role\-based access control \(RBAC\) permissions to manage user access from AWS\. For instructions, see [Granting access to a user to view a cluster](https://docs.aws.amazon.com/eks/latest/userguide/connector-grant-access.html)\.
+ Installing and upgrading Amazon EKS Connector\.
+ Maintaining the hardware, software, and infrastructure that supports the connected Kubernetes cluster\.
+ Securing their AWS accounts \(for example, through using [secure root user credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html)\)\.