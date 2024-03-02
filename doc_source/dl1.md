# Configuring DL1 for your custom Amazon Linux 2 AMI<a name="dl1"></a>

Custom Amazon Linux 2 \(AL2\) AMIs in Amazon EKS can support deep learning workloads at scale through additional configuration and Kubernetes add\-ons\. This document describes the components required to set up a generic Kubernetes solution for an on\-premise setup or as a baseline in a larger cloud configuration\. To support this function, you will have to perform the following steps in your custom environment:
+ SynapaseAI® Software drivers loaded on the system – These are included in the [AMIs available on Github](https://github.com/aws-samples/aws-habana-baseami-pipeline)\.

  The Habana device plugin \-\- A Daemonset that allows you to automatically enable the registration of Habana devices in your Kubernetes cluster and track device health\.
+ Helm 3\.x
+ [Helm chart to install MPI Operator](https://docs.habana.ai/en/latest/Gaudi_Kubernetes/Gaudi_Kubernetes.html#habana-mpi-operator-and-helm-chart-for-kubernetes)\.
+ MPI Operator

1. Create and launch a base AMI from AL2, Ubuntu 18, or Ubuntu 20\.

1. Follow [these instructions](https://docs.habana.ai/en/latest/Gaudi_Kubernetes/Gaudi_Kubernetes.html) to set up the environment for DL1\.