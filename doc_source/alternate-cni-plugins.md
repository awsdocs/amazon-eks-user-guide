# Alternate compatible CNI plugins<a name="alternate-cni-plugins"></a>

The [https://github.com/aws/amazon-vpc-cni-plugins](https://github.com/aws/amazon-vpc-cni-plugins) is the only CNI plugin supported by Amazon EKS\. Amazon EKS runs upstream Kubernetes, so you can install alternate compatible CNI plugins to Amazon EC2 nodes in your cluster\. If you have Fargate nodes in your cluster, the Amazon VPC CNI plugin for Kubernetes is already on your Fargate nodes\. It's the only CNI plugin you can use with Fargate nodes\. An attempt to install an alternate CNI plugin on Fargate nodes fails\.

If you plan to use an alternate CNI plugin on Amazon EC2 nodes, we recommend that you obtain commercial support for the plugin or have the in\-house expertise to troubleshoot and contribute fixes to the CNI plugin project\. 

Amazon EKS maintains relationships with a network of partners that offer support for alternate compatible CNI plugins\. For details about the versions, qualifications, and testing performed, see the following partner documentation\.


| Partner | Product | Documentation | 
| --- | --- | --- | 
| Tigera | [Calico](https://www.tigera.io/partners/aws/) | [Installation instructions](https://docs.projectcalico.org/getting-started/kubernetes/managed-public-cloud/eks) | 
| Isovalent | [Cilium](https://cilium.io) | [Installation instructions](https://docs.cilium.io/en/stable/gettingstarted/k8s-install-default/) | 
| Juniper | [Cloud\-Native Contrail Networking \(CN2\)](https://www.juniper.net/us/en/products/sdn-and-orchestration/contrail/cloud-native-contrail-networking.html) | [Installation instructions](https://www.juniper.net/documentation/us/en/software/cn-cloud-native23.2/cn-cloud-native-eks-install-and-lcm/index.html) | 
| VMware | [Antrea](https://antrea.io/) | [Installation instructions](https://antrea.io/docs/main/docs/eks-installation) | 

Amazon EKS aims to give you a wide selection of options to cover all use cases\. If you develop a commercially supported Kubernetes CNI plugin not listed here, contact our partner team at [aws\-container\-partners@amazon\.com](mailto:aws-container-partners@amazon.com) for more information\.