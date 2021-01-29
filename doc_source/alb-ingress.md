# Application load balancing on Amazon EKS<a name="alb-ingress"></a>

When you create a Kubernetes `Ingress`, an AWS Application Load Balancer is provisioned that load balances application traffic\. To learn more, see [What is an Application Load Balancer?](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html) in the *Application Load Balancers User Guide* and [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) in the Kubernetes documentation\. ALBs can be used with pods deployed to nodes or to AWS Fargate\. You can deploy an ALB to public or private subnets\.

Application traffic is balanced at L7 of the OSI model\. To load balance network traffic at L4, you deploy a Kubernetes `Service` of type `LoadBalancer`, which provisions an AWS Network Load Balancer\. For more information, see [Network load balancing on Amazon EKS](load-balancing.md)\. To learn more about the differences between the two types of load balancing, see [Elastic Load Balancing features](https://aws.amazon.com/elasticloadbalancing/features/) on the AWS web site\. 

**Prerequisites**

Before you can load balance application traffic to an application, you must meet the following requirements\.
+ Have an existing cluster\. If you don't have an existing cluster, see [Getting started with Amazon EKS](getting-started.md)\. If you need to update the version of an existing cluster, see [Updating a cluster](update-cluster.md)\.
+ The AWS Load Balancer Controller provisioned on your cluster\. For more information, see [AWS Load Balancer Controller](aws-load-balancer-controller.md)\.
+ Public subnets must be tagged as follows so that Kubernetes knows to use only those subnets for external load balancers instead of choosing a public subnet in each Availability Zone \(in lexicographical order by subnet ID\)\. If you use `eksctl` or an Amazon EKS AWS CloudFormation template to create your VPC after March 26, 2020, then the subnets are tagged appropriately when they're created\. For more information about the Amazon EKS AWS CloudFormation VPC templates, see [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md)\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html)
+ Private subnets must be tagged as follows so that Kubernetes knows it can use the subnets for internal load balancers\. If you use `eksctl` or an Amazon EKS AWS CloudFormation template to create your VPC after March 26, 2020, then the subnets are tagged appropriately when they're created\. For more information about the Amazon EKS AWS CloudFormation VPC templates, see [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md)\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html)

**Considerations**
+ The [AWS Load Balancer Controller](https://github.com/kubernetes-sigs/aws-load-balancer-controller) creates ALBs and the necessary supporting AWS resources whenever a Kubernetes Ingress resource is created on the cluster with the `kubernetes.io/ingress.class: alb` annotation\. The Ingress resource configures the ALB to route HTTP or HTTPS traffic to different pods within the cluster\. To ensure that your Ingress objects use the AWS Load Balancer Controller, add the following annotation to your Kubernetes Ingress specification\. For more information, see [Ingress specification](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.1/guide/ingress/spec/) on GitHub\.

  ```
  annotations:
      kubernetes.io/ingress.class: alb
  ```
+ The AWS Load Balancer Controller supports the following traffic modes:
  + **Instance** – Registers nodes within your cluster as targets for the ALB\. Traffic reaching the ALB is routed to `NodePort` for your service and then proxied to your pods\. This is the default traffic mode\. You can also explicitly specify it with the `alb.ingress.kubernetes.io/target-type: instance` annotation\.
**Note**  
Your Kubernetes service must specify the `NodePort` type to use this traffic mode\.
  + **IP** – Registers pods as targets for the ALB\. Traffic reaching the ALB is directly routed to pods for your service\. You must specify the `alb.ingress.kubernetes.io/target-type: ip` annotation to use this traffic mode\. The IP target type is required when target pods are running on Fargate\.
+ To tag ALBs created by the controller, add the following annotation to the controller: `alb.ingress.kubernetes.io/tags`\. For a list of all available annotations supported by the AWS Load Balancer Controller, see [Ingress annotations](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.1/guide/ingress/annotations/) on GitHub\.
<a name="alb-ingress-groups"></a>
**To share an application load balancer across multiple ingress resources using `IngressGroups`**  
To join an Ingress to an Ingress group, add the following annotation to a Kubernetes Ingress resource specification\. 

```
alb.ingress.kubernetes.io/group.name: <my-group>
```

The group name must be:
+ 63 characters or less in length\.
+ Consist of lower case alphanumeric characters, `-`, and `.`, and must start and end with an alphanumeric character\.

The controller will automatically merge ingress rules for all Ingresses in the same Ingress group and support them with a single ALB\. Most annotations defined on an Ingress only apply to the paths defined by that Ingress\. By default, Ingress resources don't belong to any Ingress group\.

**Warning**  
**Potential security risk**: You should only specify an Ingress group for an Ingress when all Kubernetes users with RBAC permission to create or modify Ingress resources are within the same trust boundary\. If you add the annotation with a group name, other Kubernetes users may create or modify their Ingresses to belong to the same Ingress group\. Doing so can cause undesirable behavior, such as overwriting existing rules with higher priority rules\. 

You can add an order number of your Ingress resource\.

```
alb.ingress.kubernetes.io/group.order: <'10'>
```

The number can be between 1\-1000\. The lowest number for all Ingresses in the same Ingress group is evaluated first\. All Ingresses without this annotation are evaluated with a value of zero\. Duplicate rules with a higher number can overwrite rules with a lower number\. By default, the rule order between Ingresses within the same Ingress group are determined by the lexical order of an Ingress’ namespace and name\.

**Important**  
Ensure that each Ingress in the same Ingress group has a unique priority number\. You can't have duplicate order numbers across Ingresses\.

**To deploy a sample application**

You can run the sample application on a cluster that has Amazon EC2 nodes only, Fargate pods, or both\.

1. If you're deploying to Fargate, create a Fargate profile\. If you're not deploying to Fargate skip this step\. The command that follows only works for clusters that were created with `eksctl`\. If you didn't create your cluster with `eksctl`, then you can create the profile with the the [AWS Management Console](fargate-profile.md#create-fargate-profile), using the same values for `name` and `namespace` that are in the command below\.

   ```
   eksctl create fargateprofile --cluster <my-cluster> --region <region-code> --name <alb-sample-app> --namespace game-2048
   ```

1. Deploy the game [2048](https://play2048.co/) as a sample application to verify that the AWS Load Balancer Controller creates an AWS ALB as a result of the Ingress object\. 

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.1.0/docs/examples/2048/2048_full.yaml
   ```

1. After a few minutes, verify that the Ingress resource was created with the following command\.

   ```
   kubectl get ingress/ingress-2048 -n game-2048
   ```

   Output:

   ```
   NAME           CLASS    HOSTS   ADDRESS                                                                   PORTS   AGE
   ingress-2048   <none>   *       k8s-game2048-ingress2-xxxxxxxxxx-yyyyyyyyyy.us-west-2.elb.amazonaws.com   80      2m32s
   ```
**Note**  
If your Ingress has not been created after several minutes, run the following command to view the Load Balancer Controller logs\. These logs may contain error messages that can help you diagnose any issues with your deployment\.  

   ```
   kubectl logs -n kube-system   deployment.apps/aws-load-balancer-controller
   ```

1. Open a browser and navigate to the `ADDRESS` URL from the previous command output to see the sample application\. If you don't see anything, wait a few minutes and refresh your browser\.  
![\[2048 sample application\]](http://docs.aws.amazon.com/eks/latest/userguide/images/2048.png)

1. When you finish experimenting with your sample application, delete it with the following commands\.

   ```
   kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.1.0/docs/examples/2048/2048_full.yaml
   ```