# Alternate compatible CNI plugins<a name="alternate-cni-plugins"></a>

Amazon EKS only officially supports the [Amazon VPC CNI plugin](pod-networking.md)\. Amazon EKS runs upstream Kubernetes and is certified Kubernetes conformant however, so alternate CNI plugins will work with Amazon EKS clusters\. If you plan to use an alternate CNI plugin in production, then we strongly recommend that you either obtain commercial support, or have the in\-house expertise to troubleshoot and contribute fixes to the open source CNI plugin project\.

Amazon EKS maintains relationships with a network of partners that offer support for alternate compatible CNI plugins\. Refer to the following partners' documentation for details on supported Kubernetes versions and qualifications and testing performed\.


| Partner | Product | Documentation | 
| --- | --- | --- | 
| Tigera | [ Calico](https://www.tigera.io/partners/aws/) | [Installation instructions](https://docs.projectcalico.org/getting-started/kubernetes/managed-public-cloud/eks) | 
| Isovalent | [Cilium](https://cilium.io/contact-us-eks/) | [Installation instructions](https://docs.cilium.io/en/v1.7/gettingstarted/k8s-install-eks/) | 
| Weaveworks | [Weave Net](https://www.weave.works/contact/) | [Installation instructions](https://www.weave.works/docs/net/latest/kubernetes/kube-addon/#-installing-on-eks) | 
| VMware | [Antrea](https://antrea.io/) | [Installation instructions](https://antrea.io/docs/v0.9.3/eks-installation/) | 

Amazon EKS aims to give you a wide selection of options to cover all use cases\. If you develop a commercially supported Kubernetes CNI plugin that is not listed here, then please contact our partner team at [aws\-container\-partners@amazon\.com](mailto:aws-container-partners@amazon.com) for more information\.