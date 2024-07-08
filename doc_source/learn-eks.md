# Learn Amazon EKS by example<a name="learn-eks"></a>

## Overview<a name="overview"></a>

This Amazon EKS User Guide contains general\-purpose procedures to create your first EKS cluster from the [command line](getting-started-eksctl.md) or [AWS Management Console](getting-started-console.md) and a solid reference for all major Amazon EKS components\. However, as an Amazon EKS cluster administrator or developer, you can gain a deeper understanding of Amazon EKS by following learning paths that exist in sites outside of this guide\. These sites can help you:
+ **Set up specific types of clusters**\. Specific cluster types can be based on your workload types or security requirements\. For example, you may want to tune a cluster to run batch, machine learning, or compute\-intensive workloads\.
+ **Enhance your clusters**\. You can add advanced features to your cluster to provide things like observability,flexible storage, autoscaling, or specialized cluster networking\. 
+ **Automate updates**\. Using features like GitOps, you can set up to provision cluster infrastructure and workloads automatically, based on changes that occur to those components in your Git repositories\.
+ **Use advanced cluster setup tools**\. While `eksctl` provides a quick way to create a cluster, there are other tools that can make it easier to configure and upgrade more complex clusters\. These include tools like [Terraform ](https://www.terraform.io/) and [CloudFormation](https://aws.amazon.com/cloudformation/)\.

To start out on your Amazon EKS learning path, I recommend that you visit some of the sites described on this page\. If you run into problems along the way, there are also resources to help you get through them\. For example, the [Re:post Knowledge Center](https://repost.aws/search/content?globalSearch=EKS) lets you search the support database for Amazon EKS\-related support issues\. Also the [Amazon EKS Best Practices Guide](https://aws.github.io/aws-eks-best-practices/) offers tips on the best ways to set up your production\-grade clusters\.

## Amazon EKS Workshop<a name="eks-workshop"></a>

Starting with a basic understanding of Kubernetes and containers, the [Amazon EKS workshop](https://www.eksworkshop.com/) is a learning platform for walking a cluster administrator through important features of Amazon EKS\. Here are ways you can engage with the Amazon EKS workshop:
+ **Amazon EKS Basics**: Watch the video on the [Introduction](https://www.eksworkshop.com/docs/introduction) page to learn about how Amazon EKS implements Kubernetes features on the AWS cloud\. If you need an even more basic understanding of Kubernetes, watch the [What is Kubernetes](https://www.youtube.com/watch?v=a2gfpZE8vXY) video\.
+ **Amazon EKS Setup**: If you have an AWS account, the [Setup](https://www.eksworkshop.com/docs/introduction/setup/) section helps you set up a CloudShell environment to you for creating a cluster\. It offers a choice of [eksctl](https://www.eksworkshop.com/docs/introduction/setup/your-account/using-eksctl) \(a simple cluster creation command line\) and [Terraform](https://www.eksworkshop.com/docs/introduction/setup/your-account/using-terraform) \(a more infrastructure\-as\-code approach to creating a cluster\) for creating your Amazon EKS cluster\.
+ **Amazon EKS Getting started**: Try out a simple web store from the [Sample application](https://www.eksworkshop.com/docs/introduction/getting-started/about) section\. You can use this throughout the other exercises\. In this section, you can also learn about [packaging container images](https://www.eksworkshop.com/docs/introduction/getting-started/packaging-application) and how microservices are managed using Kubernetes Pods, Deployments, Services, StatefulSets and Namespaces\. Then use Kustomize to deploy changes to Kubernetes manifests\.
+ **Amazon EKS Fundamentals**: Using AWS features such as the [AWS Load Balancer Controller](https://www.eksworkshop.com/docs/fundamentals/exposing/aws-lb-controller), the workshop shows you how to expose your applications to the outside world\. For storage, the workshop showcases how to use [Amazon EBS](https://www.eksworkshop.com/docs/fundamentals/storage/ebs/) for block storage, [Amazon EFS](https://www.eksworkshop.com/docs/fundamentals/storage/efs/) for filesystem storage, and Amazon FSx for NetApp ONTAP to manage ONTAP file systems in AWS\. For node management, the workshop helps you set up [Managed Node Groups](https://www.eksworkshop.com/docs/fundamentals/managed-node-groups/)\.
+ **Amazon EKS advanced features**: More advanced features offered through the Amazon EKS workshop include labs for setting up:
  + Autoscaling: This includes node autoscaling \(with [Cluster Autoscaler](https://www.eksworkshop.com/docs/autoscaling/compute/cluster-autoscaler/) or [Karpenter](https://www.eksworkshop.com/docs/autoscaling/compute/karpenter/)\) and workload autoscaling \(with [Horizontal Pod Autoscaler](https://www.eksworkshop.com/docs/autoscaling/workloads/horizontal-pod-autoscaler/) and [Cluster Proportional Autoscaler](https://www.eksworkshop.com/docs/autoscaling/workloads/cluster-proportional-autoscaler/)\)\.
  + Observability: Learn about [Logging](https://www.eksworkshop.com/docs/observability/logging/), [OpenSearch](https://www.eksworkshop.com/docs/observability/opensearch/), [Container Insights on Amazon EKS](https://www.eksworkshop.com/docs/observability/container-insights/), and [Cost Visibility with Kubecost](https://www.eksworkshop.com/docs/observability/kubecost/) in a set of [Observability labs](https://www.eksworkshop.com/docs/observability/)\.
  + Security: This set of [Security labs](https://www.eksworkshop.com/docs/security/) let you explore [Secrets Management](https://www.eksworkshop.com/docs/security/secrets-management/), [Amazon GuardDuty](https://www.eksworkshop.com/docs/security/guardduty/), [Pod Security Standards](https://www.eksworkshop.com/docs/security/pod-security-standards/), and [Kyverno policy management](https://www.eksworkshop.com/docs/security/kyverno/)\.
  + Networking: Learn networking features for Amazon EKS from [Networking](https://www.eksworkshop.com/docs/networking/) labs that include [Amazon VPC CNI](https://www.eksworkshop.com/docs/networking/vpc-cni/) \(supporting network plugins\) and [Amazon VPC Lattice](https://www.eksworkshop.com/docs/networking/vpc-lattice/) \(for configuring clusters across VC and user accounts\)\.
  + Automation: Labs on [Automation](https://www.eksworkshop.com/docs/automation/) step you through [GitOps](https://www.eksworkshop.com/docs/automation/gitops/) methods of managing your clusters and projects like [AWS Controllers for Kubernetes](https://www.eksworkshop.com/docs/automation/controlplanes/ack/) and [Crossplane](https://www.eksworkshop.com/docs/automation/controlplanes/crossplane/) for managing Amazon EKS control planes\.

## Amazon EKS hands\-on cluster setup tutorials<a name="eks-hands-on-cluster-setup-tutorials"></a>

A set of [Amazon EKS Cluster Setup tutorials](https://community.aws/tags/eks-cluster-setup) on the AWS Community site can help you create special\-purpose Amazon EKS clusters and enhance those clusters in various ways\. The tutorials are divided into three different types:

*Building clusters*

These tutorials help you build clusters that can be used for special purposes\. These special purposes include the ability to run:
+ [https://community.aws/tutorials/navigating-amazon-eks/eks-cluster-ipv6-globally-scalable](https://community.aws/tutorials/navigating-amazon-eks/eks-cluster-ipv6-globally-scalable)
+ [https://community.aws/tutorials/navigating-amazon-eks/eks-cluster-batch-processing](https://community.aws/tutorials/navigating-amazon-eks/eks-cluster-batch-processing)
+ [https://community.aws/tutorials/navigating-amazon-eks/eks-cluster-high-traffic](https://community.aws/tutorials/navigating-amazon-eks/eks-cluster-high-traffic)
+ [https://community.aws/tutorials/navigating-amazon-eks/eks-karpenter-fargate](https://community.aws/tutorials/navigating-amazon-eks/eks-karpenter-fargate)
+ [https://community.aws/tutorials/navigating-amazon-eks/eks-cluster-financial-workload](https://community.aws/tutorials/navigating-amazon-eks/eks-cluster-financial-workload)
+ [https://community.aws/tutorials/navigating-amazon-eks/eks-cluster-windows-fargate](https://community.aws/tutorials/navigating-amazon-eks/eks-cluster-windows-fargate)

*Enhancing clusters*

Once you have an existing cluster, you can extend and enhance that cluster in ways that allow it to run specialized workloads and otherwise enhance the clusters\. These tutorials include ways to:
+ [https://community.aws/tutorials/navigating-amazon-eks/eks-with-efs-add-on/](https://community.aws/tutorials/navigating-amazon-eks/eks-with-efs-add-on/)
+ [https://community.aws/tutorials/navigating-amazon-eks/eks-dynamic-db-storage-ebs-csi](https://community.aws/tutorials/navigating-amazon-eks/eks-dynamic-db-storage-ebs-csi)
+ [https://community.aws/tutorials/navigating-amazon-eks/eks-cluster-load-balancer-ipv4](https://community.aws/tutorials/navigating-amazon-eks/eks-cluster-load-balancer-ipv4)
+ [https://community.aws/tutorials/navigating-amazon-eks/eks-cluster-load-balancer-ipv6](https://community.aws/tutorials/navigating-amazon-eks/eks-cluster-load-balancer-ipv6)

*Optimizing AWS services*

Using these tutorials, you can better integrate your clusters with AWS services\. These tutorials include those that help you:
+ [https://community.aws/tutorials/navigating-amazon-eks/automating-dns-records-for-microservices-using-externaldns/](https://community.aws/tutorials/navigating-amazon-eks/automating-dns-records-for-microservices-using-externaldns/)
+ [https://community.aws/tutorials/navigating-amazon-eks/eks-monitor-containerized-applications](https://community.aws/tutorials/navigating-amazon-eks/eks-monitor-containerized-applications)
+ [https://community.aws/tutorials/navigating-amazon-eks/managing-high-volume-batch-sqs-eks](https://community.aws/tutorials/navigating-amazon-eks/managing-high-volume-batch-sqs-eks)
+ [https://community.aws/tutorials/navigating-amazon-eks/eks-integrate-secrets-manager](https://community.aws/tutorials/navigating-amazon-eks/eks-integrate-secrets-manager)
+ [https://community.aws/tutorials/navigating-amazon-eks/eks-fargate-mtls-nginx-controller](https://community.aws/tutorials/navigating-amazon-eks/eks-fargate-mtls-nginx-controller)

## Amazon EKS Samples<a name="eks-samples"></a>

The [Amazon Amazon EKS Samples](https://github.com/aws-samples/aws-eks-se-samples) repository stores manifests to use with Amazon EKS\. These manifests give you the opportunity to try out different kinds of applications in Amazon EKS or create specific types of Amazon EKS clusters\. Samples include manifests to:
+ [https://github.com/aws-samples/aws-eks-se-samples/tree/main/examples/eksctl/how-to-eks-fargate](https://github.com/aws-samples/aws-eks-se-samples/tree/main/examples/eksctl/how-to-eks-fargate)
+ [https://github.com/aws-samples/aws-eks-se-samples/blob/main/examples/eksctl/how-to-existing-iamrole/existing-role.yaml](https://github.com/aws-samples/aws-eks-se-samples/blob/main/examples/eksctl/how-to-existing-iamrole/existing-role.yaml)
+ [https://github.com/aws-samples/aws-eks-se-samples/tree/main/examples/eksctl/how-to-ubuntu-nodegroups](https://github.com/aws-samples/aws-eks-se-samples/tree/main/examples/eksctl/how-to-ubuntu-nodegroups)
+ [https://github.com/aws-samples/aws-eks-se-samples/tree/main/examples/kubernetes/how-to-backup-restore-ebs-pvc](https://github.com/aws-samples/aws-eks-se-samples/tree/main/examples/kubernetes/how-to-backup-restore-ebs-pvc)
+ [https://github.com/aws-samples/aws-eks-se-samples/tree/main/examples/kubernetes/how-to-dr-multi-account](https://github.com/aws-samples/aws-eks-se-samples/tree/main/examples/kubernetes/how-to-dr-multi-account)
+ [https://github.com/aws-samples/aws-eks-se-samples/tree/main/examples/kubernetes/how-to-enable-proxy-procotcol-clb](https://github.com/aws-samples/aws-eks-se-samples/tree/main/examples/kubernetes/how-to-enable-proxy-procotcol-clb)
+ [https://github.com/aws-samples/aws-eks-se-samples/tree/main/examples/kubernetes/how-to-logging-eks-fargate-opensearch](https://github.com/aws-samples/aws-eks-se-samples/tree/main/examples/kubernetes/how-to-logging-eks-fargate-opensearch)
+ [https://github.com/aws-samples/aws-eks-se-samples/tree/main/examples/kubernetes/how-to-python-sdk-containers](https://github.com/aws-samples/aws-eks-se-samples/tree/main/examples/kubernetes/how-to-python-sdk-containers)
+ [https://github.com/aws-samples/aws-eks-se-samples/tree/main/examples/kubernetes/how-to-setup-nfs-csi-eks](https://github.com/aws-samples/aws-eks-se-samples/tree/main/examples/kubernetes/how-to-setup-nfs-csi-eks)
+ [https://github.com/aws-samples/aws-eks-se-samples/tree/main/examples/kubernetes/how-to-snapshot-restore-resize-sts](https://github.com/aws-samples/aws-eks-se-samples/tree/main/examples/kubernetes/how-to-snapshot-restore-resize-sts)
+ [https://github.com/aws-samples/aws-eks-se-samples/tree/main/examples/kubernetes/how-to-topology-awareness-hints](https://github.com/aws-samples/aws-eks-se-samples/tree/main/examples/kubernetes/how-to-topology-awareness-hints)

Keep in mind that these samples are for learning and testing purposes only and are not intended to be used in production\.

## AWS Tutorials<a name="aws-tutorials"></a>

The [AWS Tutorials](https://aws.amazon.com/tutorials) site publishes a few Amazon EKS tutorials, but also offers a search tool to find other tutorials published on AWS sites \(such as the AWS Community site\)\. Amazon EKS tutorials published directly on this site include:
+ [https://aws.amazon.com/tutorials/deploy-webapp-eks/](https://aws.amazon.com/tutorials/deploy-webapp-eks/)
+ [https://aws.amazon.com/tutorials/amazon-eks-with-spot-instances/](https://aws.amazon.com/tutorials/amazon-eks-with-spot-instances/)
+ [https://aws.amazon.com/tutorials/cost-optimize-jenkins/](https://aws.amazon.com/tutorials/cost-optimize-jenkins/)

## Developers Workshop<a name="developers-workshop"></a>

If you are a software developer, looking to create or refactor applications to run on Amazon EKS, the [Amazon EKS Developers workshop ](http://developers.eksworkshop.com)is a good place to start\. The workshop not only helps you build containerized applications, but also helps you deploy those containers to a container registry \([ECR](https://aws.amazon.com/ecr/)\) and from there to an Amazon EKS cluster\.

Start with the [Amazon EKS Python Workshop](https://developers.eksworkshop.com/docs/introduction/python/about-workshop) to go through the process of refactoring a python application, then set up your development environment to prepare for deploying the application\. Step through sections on Containers, Kubernetes, and Amazon EKS to prepare to run your containerized applications in those environments\.

## Terraform Workshop<a name="terraform-workshop"></a>

While `eksctl` is a simple tool for creating a cluster, for more complex infrastructure\-as\-code types of Amazon EKS deployments, [Terraform](https://www.terraform.io/) is a popular Amazon EKS cluster creation and management tool\. The [Terraform Amazon EKS Workshop](https://catalog.us-east-1.prod.workshops.aws/workshops/afee4679-89af-408b-8108-44f5b1065cc7/en-US) teaches how to use Terraform to build an AWS VPC, create Amazon EKS clusters, and add optional enhancements to your cluster\. In particular, there is a section for creating a [private Amazon EKS cluster](https://catalog.us-east-1.prod.workshops.aws/workshops/afee4679-89af-408b-8108-44f5b1065cc7/en-US/500-eks-terraform-workshop)

## AWS Amazon EKS Training<a name="aws-eks-training"></a>

AWS offers formal training for learning about Amazon EKS\. A three\-day training course entitled [Running Containers on Amazon Elastic Kubernetes Service](https://aws.amazon.com/training/classroom/running-containers-on-amazon-elastic-kubernetes-service-amazon-eks/) teaches:
+ Kubernetes and Amazon EKS fundamentals
+ How to build Amazon EKS clusters
+ Securing Amazon EKS with AWS IAM and Kubernetes RBAC authorization
+ GitOps automation tools
+ Monitoring tools
+ Techniques for improving cost, efficiency, and resiliency