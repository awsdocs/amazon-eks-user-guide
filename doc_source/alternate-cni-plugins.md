# Alternate compatible CNI plugins<a name="alternate-cni-plugins"></a>

Amazon EKS only officially supports the [Amazon VPC CNI plugin for Kubernetes](pod-networking.md)\. Amazon EKS runs upstream Kubernetes and is certified Kubernetes however, so you can install alternate CNI plugins to Amazon EC2 nodes in your cluster\. Your cluster will fail to install an alternate CNI plugin to Fargate nodes, if you have them in your cluster\. The [Amazon VPC CNI plugin for Kubernetes](pod-networking.md) is already on your Fargate nodes, but it's the only plugin that you can use with Fargate nodes\. If you plan to use an alternate CNI plugin in production, then we strongly recommend that you either obtain commercial support, or have the in\-house expertise to troubleshoot and contribute fixes to the open source CNI plugin project\.

Amazon EKS maintains relationships with a network of partners that offer support for alternate compatible CNI plugins\. See the following partners' documentation for details on supported Kubernetes versions and qualifications and testing performed\.


| Partner | Product | Documentation | 
| --- | --- | --- | 
| Tigera | [Calico](https://www.tigera.io/partners/aws/) | [Installation instructions](https://docs.projectcalico.org/getting-started/kubernetes/managed-public-cloud/eks) | 
| Isovalent | [Cilium](https://cilium.io/contact-us-eks/) | [Installation instructions](https://docs.cilium.io/en/v1.9/gettingstarted/k8s-install-eks/) | 
| Weaveworks | [Weave Net](https://www.weave.works/contact/) | [Installation instructions](https://www.weave.works/docs/net/latest/kubernetes/kube-addon/#-installing-on-eks) | 
| VMware | [Antrea](https://antrea.io/) | [Installation instructions](https://antrea.io/docs/main/docs/eks-installation) | 

Amazon EKS aims to give you a wide selection of options to cover all use cases\. If you develop a commercially supported Kubernetes CNI plugin that is not listed here, then please contact our partner team at [aws\-container\-partners@amazon\.com](mailto:aws-container-partners@amazon.com) for more information\.