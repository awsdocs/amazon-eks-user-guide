# Amazon EKS networking add\-ons<a name="eks-networking-add-ons"></a>

Several networking add\-ons are available for your Amazon EKS cluster\.

## Built\-in add\-ons<a name="eks-networking-add-ons-built-in"></a>

**Note**  
If you create clusters in any way except by using the console, each cluster comes with the self\-managed versions of the built\-in add\-ons\. The self\-managed versions can't be managed from the AWS Management Console, AWS Command Line Interface, or SDKs\. You manage the configuration and upgrades of self\-managed add\-ons\.  
We recommend adding the Amazon EKS type of the add\-on to your cluster instead of using the self\-managed type of the add\-on\. If you create clusters in the console, the Amazon EKS type of these add\-ons is installed\.

**Amazon VPC CNI plugin for Kubernetes**  
This CNI add\-on creates elastic network interfaces and attaches them to your Amazon EC2 nodes\. The add\-on also assigns a private `IPv4` or `IPv6` address from your VPC to each Pod and service\. This add\-on is installed, by default, on your cluster\. For more information, see [Working with the Amazon VPC CNI plugin for Kubernetes Amazon EKS add\-on](managing-vpc-cni.md)\.

**CoreDNS**  
CoreDNS is a flexible, extensible DNS server that can serve as the Kubernetes cluster DNS\. CoreDNS provides name resolution for all Pods in the cluster\. This add\-on is installed, by default, on your cluster\. For more information, see [Working with the CoreDNS Amazon EKS add\-on](managing-coredns.md)\.

**`kube-proxy`**  
This add\-on maintains network rules on your Amazon EC2 nodes and enables network communication to your Pods\. This add\-on is installed, by default, on your cluster\. For more information, see [Working with the Kubernetes `kube-proxy` add\-on](managing-kube-proxy.md)\.

## Optional AWS networking add\-ons<a name="eks-networking-add-ons-optional"></a>

**AWS Load Balancer Controller**  
When you deploy Kubernetes service objects of type `loadbalancer`, the controller creates AWS Network Load Balancers \. When you create Kubernetes ingress objects, the controller creates AWS Application Load Balancers\. We recommend using this controller to provision Network Load Balancers, rather than using the [legacy Cloud Provider](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.7/guide/service/annotations/#legacy-cloud-provider) controller built\-in to Kubernetes\. For more information, see the [https://kubernetes-sigs.github.io/aws-load-balancer-controller](https://kubernetes-sigs.github.io/aws-load-balancer-controller) documentation\.

**AWS Gateway API Controller**  
This controller lets you connect services across multiple Kubernetes clusters using the [Kubernetes gateway API](https://gateway-api.sigs.k8s.io/)\. The controller connects Kubernetes services running on Amazon EC2 instances, containers, and serverless functions by using the [Amazon VPC Lattice](https://docs.aws.amazon.com/vpc-lattice/latest/ug/what-is-vpc-service-network.html) service\. For more information, see the [AWS Gateway API Controller](https://www.gateway-api-controller.eks.aws.dev/) documentation\.

For more information about add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\.