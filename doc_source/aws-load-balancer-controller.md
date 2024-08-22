# Route internet traffic with AWS Load Balancer Controller<a name="aws-load-balancer-controller"></a>

The AWS Load Balancer Controller manages AWS Elastic Load Balancers for a Kubernetes cluster\. You can use the controller to expose your cluster apps to the internet\. The controller provisions AWS load balancers that point to cluster Service or Ingress resources\. In other words, the controller creates a single IP address or DNS name that points to multiple pods in your cluster\. 

![\[\]](http://docs.aws.amazon.com/eks/latest/userguide/images/lbc-overview.svg)

The controller watches for Kubernetes Ingress or Service resources\. In response, it creates the appropriate AWS Elastic Load Balancing resources\. You can configure the specific behavior of the load balancers by applying annotations to the Kubernetes resources\. For example, you can attach AWS security groups to load balancers using annotations\. 

The controller provisions the following resources: 

Kubernetes `Ingress`  
The LBC creates an [AWS Application Load Balancer \(ALB\)](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html) when you create a Kubernetes `Ingress`\. [Review the annotations you can apply to an Ingress resource\. ](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.7/guide/ingress/annotations/)

Kubernetes service of the `LoadBalancer` type  
The LBC creates an [AWS Network Load Balancer \(NLB\) ](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html)when you create a Kubernetes service of type `LoadBalancer`\. [Review the annotations you can apply to a Service resource\.](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.7/guide/service/annotations/)   
In the past, the Kubernetes network load balancer was used for *instance* targets, but the LBC was used for *IP* targets\. With the AWS Load Balancer Controller version `2.3.0` or later, you can create NLBs using either target type\. For more information about NLB target types, see [Target type](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-target-groups.html#target-type) in the User Guide for Network Load Balancers\.

The controller is an [open\-source project](https://github.com/kubernetes-sigs/aws-load-balancer-controller) managed on GitHub\.

Before deploying the controller, we recommend that you review the prerequisites and considerations in [Route application and HTTP traffic with Application Load Balancers](alb-ingress.md) and [Route TCP and UDP traffic with Network Load Balancers](network-load-balancing.md)\. In those topics, you will deploy a sample app that includes an AWS load balancer\. 

## Install the controller<a name="lbc-overview"></a>

You can use one of the following procedures to install the AWS Load Balancer Controller:
+ If you are new to Amazon EKS we recommend that you use Helm for the installation because it simplifies the AWS Load Balancer Controller installation\. For more information, see [Install AWS Load Balancer Controller with Helm](lbc-helm.md)\. 
+ For advanced configurations, such as clusters with restricted network access to public container registries, use Kubernetes Manifests\. For more information, see [Install AWS Load Balancer Controller with manifests](lbc-manifest.md)\.

## Migrate from deprecated controller versions<a name="lbc-deprecated"></a>
+ If you have deprecated versions of the AWS Load Balancer Controller installed, learn how to [Migrate apps from deprecated AWSIngress Controller](lbc-remove.md)\.
+ Deprecated versions cannot be upgraded\. They must be removed and a current version of the AWS Load Balancer Controller installed\. 
+ <a name="lbc-deprecated-list"></a>Deprecated versions include:
  + AWS ALB Ingress Controller for Kubernetes \("Ingress Controller"\), a predecessor to the AWS Load Balancer Controller\.
  + Any `0.1.x` version of the AWS Load Balancer Controller 

## Legacy cloud provider<a name="lbc-legacy"></a>

Kubernetes includes a legacy cloud provider for AWS\. The legacy cloud provider is capable of provisioning AWS load balancers, similar to the AWS Load Balancer Controller\. The legacy cloud provider creates Classic Load Balancers\. If you do not install the AWS Load Balancer Controller, Kubernetes will default to using the legacy cloud provider\. You should install the AWS Load Balancer Controller and avoid using the legacy cloud provider\. 

**Important**  
In versions 2\.5 and newer, the AWS Load Balancer Controller becomes the default controller for Kubernetes *service* resources with the `type: LoadBalancer` and makes an AWS Network Load Balancer \(NLB\) for each service\. It does this by making a mutating webhook for services, which sets the `spec.loadBalancerClass` field to `service.k8s.aws/nlb` for new services of `type: LoadBalancer`\. You can turn off this feature and revert to using the [legacy Cloud Provider](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.7/guide/service/annotations/#legacy-cloud-provider) as the default controller, by setting the helm chart value `enableServiceMutatorWebhook` to `false`\. The cluster won't provision new Classic Load Balancers for your services unless you turn off this feature\. Existing Classic Load Balancers will continue to work\.