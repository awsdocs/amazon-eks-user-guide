# Related projects<a name="related-projects"></a>

These open\-source projects extend the functionality of Kubernetes clusters running on or outside of AWS, including clusters managed by Amazon EKS\.

## Management tools<a name="related-management-tools"></a>

Related management tools for Amazon EKS and Kubernetes clusters\.

### eksctl<a name="related-eksctl"></a>

`eksctl` is a simple CLI tool for creating clusters on Amazon EKS\.
+ [Project URL](https://eksctl.io/)
+ [Project documentation](https://eksctl.io/)
+ AWS open source blog: [eksctl: Amazon EKS cluster with one command](https://aws.amazon.com/blogs/opensource/eksctl-eks-cluster-one-command/)

### AWS controllers for Kubernetes<a name="related-aws-controllers"></a>

With AWS Controllers for Kubernetes, you can create and manage AWS resources directly from your Kubernetes cluster\.
+  [Project URL](https://github.com/aws-controllers-k8s/)
+ AWS open source blog: [AWS service operator for Kubernetes now available](https://aws.amazon.com/blogs/opensource/aws-service-operator-kubernetes-available/)

### Flux CD<a name="related-flux-cd"></a>

Flux is a tool that you can use to manage your cluster configuration using Git\. It uses an operator in the cluster to trigger deployments inside of Kubernetes\. For more information about operators, see [OperatorHub\.io](https://operatorhub.io/) on GitHub\.
+ [Project URL](https://fluxcd.io/)
+ [Project documentation](https://docs.fluxcd.io/)

### CDK for Kubernetes<a name="related-cdk"></a>

With the CDK for Kubernetes \(cdk8s\), you can define Kubernetes apps and components using familiar programming languages\. cdk8s apps synthesize into standard Kubernetes manifests, which can be applied to any Kubernetes cluster\.
+ [ Project URL](https://cdk8s.io/)
+ [Project documentation](https://cdk8s.io/docs/latest/)
+ AWS containers blog: [Introducing cdk8s\+: Intent\-driven APIs for Kubernetes objects](https://aws.amazon.com/blogs/containers/introducing-cdk8s-intent-driven-apis-for-kubernetes-objects/)

## Networking<a name="related-networking"></a>

Related networking projects for Amazon EKS and Kubernetes clusters\.

### Amazon VPC CNI plugin for Kubernetes<a name="related-vpc-cni-k8s"></a>

Amazon EKS supports native VPC networking through the Amazon VPC CNI plugin for Kubernetes\. The plugin assigns an IP address from your VPC to each Pod\.
+ [Project URL](https://github.com/aws/amazon-vpc-cni-k8s)
+ [Project documentation](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/README.md)

### AWS Load Balancer Controller for Kubernetes<a name="related-alb-ingress-controller"></a>

The AWS Load Balancer Controller helps manage AWS Elastic Load Balancers for a Kubernetes cluster\. It satisfies Kubernetes Ingress resources by provisioning AWS Application Load Balancers\. It satisfies Kubernetes service resources by provisioning AWS Network Load Balancers\.
+ [Project URL](https://github.com/kubernetes-sigs/aws-load-balancer-controller)
+ [Project documentation](https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/)

### ExternalDNS<a name="related-externaldns"></a>

ExternalDNS synchronizes exposed Kubernetes services and ingresses with DNS providers including Amazon Route 53 and AWS Service Discovery\.
+ [Project URL](https://github.com/kubernetes-incubator/external-dns)
+ [Project documentation](https://github.com/kubernetes-incubator/external-dns/blob/master/docs/tutorials/aws.md)

## Machine learning<a name="related-machine-learning"></a>

Related machine learning projects for Amazon EKS and Kubernetes clusters\.

### Kubeflow<a name="related-kubeflow"></a>

A machine learning toolkit for Kubernetes\.
+ [Project URL](https://www.kubeflow.org/)
+ [Project documentation](https://www.kubeflow.org/docs/)
+ AWS open source blog: [Kubeflow on Amazon EKS](https://aws.amazon.com/blogs/opensource/kubeflow-amazon-eks/)

## Auto Scaling<a name="related-auto-scaling"></a>

Related auto scaling projects for Amazon EKS and Kubernetes clusters\.

### Cluster autoscaler<a name="related-cluster-autoscaler"></a>

Cluster Autoscaler is a tool that automatically adjusts the size of the Kubernetes cluster based on CPU and memory pressure\.
+ [Project URL](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler)
+ [Project documentation](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/cloudprovider/aws/README.md)
+ Amazon EKS workshop: [https://www\.eksworkshop\.com/](https://www.eksworkshop.com/)

### Escalator<a name="related-escalator"></a>

Escalator is a batch or job optimized horizontal autoscaler for Kubernetes\.
+ [Project URL](https://github.com/atlassian/escalator)
+ [Project documentation](https://github.com/atlassian/escalator/blob/master/docs/README.md)

## Monitoring<a name="related-monitoring"></a>

Related monitoring projects for Amazon EKS and Kubernetes clusters\.

### Prometheus<a name="related-prometheus"></a>

Prometheus is an open\-source systems monitoring and alerting toolkit\.
+ [Project URL](https://prometheus.io/)
+ [Project documentation](https://prometheus.io/docs/introduction/overview/)
+ Amazon EKS workshop: [https://eksworkshop\.com/intermediate/240\_monitoring/](https://eksworkshop.com/intermediate/240_monitoring/)

## Continuous integration / continuous deployment<a name="related-cicd"></a>

Related CI/CD projects for Amazon EKS and Kubernetes clusters\.

### Jenkins X<a name="related-jenkinsx"></a>

CI/CD solution for modern cloud applications on Amazon EKS and Kubernetes clusters\.
+ [Project URL](https://jenkins-x.io/)
+ [Project documentation](https://jenkins-x.io/docs/)