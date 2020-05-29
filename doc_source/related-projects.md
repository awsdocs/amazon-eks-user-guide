# Related projects<a name="related-projects"></a>

These open source projects extend the functionality of Kubernetes clusters running on AWS, including clusters managed by Amazon EKS\.

## Management tools<a name="related-management-tools"></a>

Related management tools for Amazon EKS and Kubernetes clusters\.

### eksctl<a name="related-eksctl"></a>

`eksctl` is a simple CLI tool for creating clusters on Amazon EKS\.
+ Project URL: [https://eksctl\.io/](https://eksctl.io/)
+ Project documentation: [https://eksctl\.io/](https://eksctl.io/)
+ AWS open source blog: [eksctl: Amazon EKS cluster with one command](http://aws.amazon.com/blogs/opensource/eksctl-eks-cluster-one-command/)

### AWS service operator<a name="related-aws-service-operator"></a>

AWS Service Operator allows you to create AWS resources using `kubectl`\.
+ Project URL: [https://github\.com/aws/aws\-service\-operator\-k8s](https://github.com/aws/aws-service-operator-k8s)
+ Project documentation: [https://github\.com/aws/aws\-service\-operator\-k8s/blob/master/README\.md](https://github.com/aws/aws-service-operator-k8s/blob/master/README.md)
+ AWS open source blog: [AWS service operator for Kubernetes now available](http://aws.amazon.com/blogs/opensource/aws-service-operator-kubernetes-available/)

## Networking<a name="related-networking"></a>

Related networking projects for Amazon EKS and Kubernetes clusters\.

### Amazon VPC CNI plugin for Kubernetes<a name="related-vpc-cni-k8s"></a>

Amazon EKS supports native VPC networking via the Amazon VPC CNI plugin for Kubernetes\. Using this CNI plugin allows Kubernetes pods to have the same IP address inside the pod as they do on the VPC network\. For more information, see [Pod networking \(CNI\)](pod-networking.md) and [CNI configuration variables](cni-env-vars.md)\.
+ Project URL: [https://github\.com/aws/amazon\-vpc\-cni\-k8s](https://github.com/aws/amazon-vpc-cni-k8s)
+ Project documentation: [https://github\.com/aws/amazon\-vpc\-cni\-k8s/blob/master/README\.md](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/README.md)

### AWS Application Load Balancer \(ALB\) ingress controller for Kubernetes<a name="related-alb-ingress-controller"></a>

The AWS ALB Ingress Controller satisfies Kubernetes ingress resources by provisioning Application Load Balancers\.
+ Project URL: [https://github\.com/kubernetes\-sigs/aws\-alb\-ingress\-controller](https://github.com/kubernetes-sigs/aws-alb-ingress-controller)
+ Project documentation: [https://github\.com/kubernetes\-sigs/aws\-alb\-ingress\-controller/tree/master/docs](https://github.com/kubernetes-sigs/aws-alb-ingress-controller/tree/master/docs)
+ AWS open source blog: [Kubernetes ingress with AWS ALB ingress controller](http://aws.amazon.com/blogs/opensource/kubernetes-ingress-aws-alb-ingress-controller/)

### ExternalDNS<a name="related-externaldns"></a>

ExternalDNS synchronizes exposed Kubernetes services and ingresses with DNS providers including Amazon Route 53 and AWS Service Discovery\.
+ Project URL: [https://github\.com/kubernetes\-incubator/external\-dns](https://github.com/kubernetes-incubator/external-dns)
+ Project documentation: [https://github\.com/kubernetes\-incubator/external\-dns/blob/master/docs/tutorials/aws\.md](https://github.com/kubernetes-incubator/external-dns/blob/master/docs/tutorials/aws.md)

## Security<a name="related-security"></a>

Related security projects for Amazon EKS and Kubernetes clusters\.

### AWS IAM authenticator<a name="related-authenticator"></a>

A tool to use AWS IAM credentials to authenticate to a Kubernetes cluster if you're not using the AWS CLI version 1\.16\.156 or higher\. For more information, see [Installing `aws-iam-authenticator`](install-aws-iam-authenticator.md)\.
+ Project URL: [https://github\.com/kubernetes\-sigs/aws\-iam\-authenticator](https://github.com/kubernetes-sigs/aws-iam-authenticator)
+ Project documentation: [https://github\.com/kubernetes\-sigs/aws\-iam\-authenticator/blob/master/README\.md](https://github.com/kubernetes-sigs/aws-iam-authenticator/blob/master/README.md)
+ AWS open source blog: [Deploying the AWS IAM authenticator to kops](http://aws.amazon.com/blogs/opensource/deploying-heptio-authenticator-kops/)

## Machine learning<a name="related-machine-learning"></a>

Related machine learning projects for Amazon EKS and Kubernetes clusters\.

### Kubeflow<a name="related-kubeflow"></a>

A machine learning toolkit for Kubernetes\.
+ Project URL: [https://www\.kubeflow\.org/](https://www.kubeflow.org/)
+ Project documentation: [https://www\.kubeflow\.org/docs/](https://www.kubeflow.org/docs/)
+ AWS open source blog: [Kubeflow on Amazon EKS](http://aws.amazon.com/blogs/opensource/kubeflow-amazon-eks/)

## Auto Scaling<a name="related-auto-scaling"></a>

Related auto scaling projects for Amazon EKS and Kubernetes clusters\.

### Cluster autoscaler<a name="related-cluster-autoscaler"></a>

Cluster Autoscaler is a tool that automatically adjusts the size of the Kubernetes cluster based on CPU and memory pressure\.
+ Project URL: [https://github\.com/kubernetes/autoscaler/tree/master/cluster\-autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler)
+ Project documentation: [https://github\.com/kubernetes/autoscaler/blob/master/cluster\-autoscaler/cloudprovider/aws/README\.md](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/cloudprovider/aws/README.md)
+ Amazon EKS workshop: [https://eksworkshop\.com/scaling/deploy\_ca/](https://eksworkshop.com/scaling/deploy_ca/)

### Escalator<a name="related-escalator"></a>

Escalator is a batch or job optimized horizontal autoscaler for Kubernetes\.
+ Project URL: [https://github\.com/atlassian/escalator](https://github.com/atlassian/escalator)
+ Project documentation: [https://github\.com/atlassian/escalator/blob/master/docs/README\.md](https://github.com/atlassian/escalator/blob/master/docs/README.md)

## Monitoring<a name="related-monitoring"></a>

Related monitoring projects for Amazon EKS and Kubernetes clusters\.

### Prometheus<a name="related-prometheus"></a>

Prometheus is an open\-source systems monitoring and alerting toolkit\.
+ Project URL: [https://prometheus\.io/](https://prometheus.io/)
+ Project documentation: [https://prometheus\.io/docs/introduction/overview/](https://prometheus.io/docs/introduction/overview/)
+ Amazon EKS workshop: [https://eksworkshop\.com/intermediate/240\_monitoring/](https://eksworkshop.com/intermediate/240_monitoring/)

## Continuous integration / continuous deployment<a name="related-cicd"></a>

Related CI/CD projects for Amazon EKS and Kubernetes clusters\.

### Jenkins X<a name="related-jenkinsx"></a>

CI/CD solution for modern cloud applications on Amazon EKS and Kubernetes clusters\.
+ Project URL: [https://jenkins\-x\.io/](https://jenkins-x.io/)
+ Project documentation: [https://jenkins\-x\.io/docs/](https://jenkins-x.io/docs/)