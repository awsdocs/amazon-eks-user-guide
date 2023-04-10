# AWS services integrated with Amazon EKS<a name="eks-integrations"></a>

Amazon EKS works with other AWS services to provide additional solutions for your business challenges\. This topic identifies services that either use Amazon EKS to add functionality, or services that Amazon EKS uses to perform tasks\.

**Topics**
+ [Creating Amazon EKS resources with AWS CloudFormation](creating-resources-with-cloudformation.md)
+ [Use AWS App Mesh with Kubernetes](gs-app-mesh.md)
+ [Amazon EKS and AWS Local Zones](local-zones.md)
+ [Deep Learning Containers](deep-learning-containers.md)
+ [Amazon VPC Lattice](#integration-vpc-lattice)

## Amazon VPC Lattice<a name="integration-vpc-lattice"></a>

 Amazon VPC Lattice is a fully managed application networking service built directly into the AWS networking infrastructure that you can use to connect, secure, and monitor your services across multiple accounts and Virtual Private Clouds \(VPCs\)\. With Amazon EKS, you can leverage Amazon VPC Lattice through the use of the AWS Gateway API Controller, an implementation of the Kubernetes [Gateway API](https://gateway-api.sigs.k8s.io/)\. Using Amazon VPC Lattice, you can set up cross\-cluster connectivity with standard Kubernetes semantics in a simple and consistent manner\. To get started using Amazon VPC Lattice with Amazon EKS see the [AWS Gateway API Controller User Guide](https://www.gateway-api-controller.eks.aws.dev/)\.