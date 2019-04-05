# Amazon EKS User Guide

-----
*****Copyright &copy; 2019 Amazon Web Services, Inc. and/or its affiliates. All rights reserved.*****

-----
Amazon's trademarks and trade dress may not be used in 
     connection with any product or service that is not Amazon's, 
     in any manner that is likely to cause confusion among customers, 
     or in any manner that disparages or discredits Amazon. All other 
     trademarks not owned by Amazon are the property of their respective
     owners, who may or may not be affiliated with, connected to, or 
     sponsored by Amazon.

-----
## Contents
+ [What Is Amazon EKS?](what-is-eks.md)
+ [Getting Started with Amazon EKS](getting-started.md)
+ [Amazon EKS Clusters](clusters.md)
   + [Creating an Amazon EKS Cluster](create-cluster.md)
   + [Updating an Amazon EKS Cluster Kubernetes Version](update-cluster.md)
   + [Amazon EKS Cluster Endpoint Access Control](cluster-endpoint.md)
   + [Amazon EKS Control Plane Logging](control-plane-logs.md)
   + [Deleting a Cluster](delete-cluster.md)
   + [Platform Versions](platform-versions.md)
+ [Worker Nodes](worker.md)
   + [Amazon EKS-Optimized AMI](eks-optimized-ami.md)
      + [Amazon EKS-Optimized AMI with GPU Support](gpu-ami.md)
   + [Amazon EKS Partner AMIs](eks-partner-amis.md)
   + [Launching Amazon EKS Worker Nodes](launch-workers.md)
   + [Worker Node Updates](update-workers.md)
      + [Migrating to a New Worker Node Group](migrate-stack.md)
      + [Updating an Existing Worker Node Group](update-stack.md)
+ [Storage Classes](storage-classes.md)
+ [Load Balancing](load-balancing.md)
+ [Amazon EKS Networking](eks-networking.md)
   + [Cluster VPC Considerations](network_reqs.md)
   + [Cluster Security Group Considerations](sec-group-reqs.md)
   + [Pod Networking](pod-networking.md)
   + [CNI Configuration Variables](cni-env-vars.md)
   + [Installing CoreDNS](coredns.md)
   + [External Source Network Address Translation (SNAT)](external-snat.md)
   + [CNI Custom Networking](cni-custom-network.md)
   + [Amazon VPC CNI Plugin for Kubernetes Upgrades](cni-upgrades.md)
   + [Installing Calico on Amazon EKS](calico.md)
+ [Managing Cluster Authentication](managing-auth.md)
   + [Installing kubectl](install-kubectl.md)
   + [Installing aws-iam-authenticator](install-aws-iam-authenticator.md)
   + [Create a kubeconfig for Amazon EKS](create-kubeconfig.md)
   + [Managing Users or IAM Roles for your Cluster](add-user-role.md)
+ [Amazon EKS Service Limits](service_limits.md)
+ [Amazon EKS IAM Policies, Roles, and Permissions](IAM_policies.md)
   + [Policy Structure](iam-policy-structure.md)
   + [Creating Amazon EKS IAM Policies](EKS_IAM_user_policies.md)
   + [Amazon EKS Service IAM Role](service_IAM_role.md)
+ [Installing the Kubernetes Metrics Server](metrics-server.md)
+ [Control Plane Metrics with Prometheus](prometheus.md)
+ [Using Helm with Amazon EKS](helm.md)
+ [Tutorial: Deploy the Kubernetes Web UI (Dashboard)](dashboard-tutorial.md)
+ [Getting Started with AWS App Mesh and Kubernetes](mesh-gs-k8s.md)
+ [Deep Learning Containers](deep-learning-containers.md)
+ [Tutorial: Creating a VPC with Public and Private Subnets for Your Amazon EKS Cluster](create-public-private-vpc.md)
+ [Logging Amazon EKS API Calls with AWS CloudTrail](logging-using-cloudtrail.md)
+ [Related Projects](related-projects.md)
+ [Amazon EKS Shared Responsibility Model](shared-responsibilty.md)
+ [Amazon EKS Troubleshooting](troubleshooting.md)
+ [Document History for Amazon EKS](doc-history.md)
+ [AWS Glossary](glossary.md)