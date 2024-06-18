# Application load balancing on Amazon EKS<a name="alb-ingress"></a>

When you create a Kubernetes `ingress`, an AWS Application Load Balancer \(ALB\) is provisioned that load balances application traffic\. To learn more, see [What is an Application Load Balancer?](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html) in the *Application Load Balancers User Guide* and [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) in the Kubernetes documentation\. ALBs can be used with Pods that are deployed to nodes or to AWS Fargate\. You can deploy an ALB to public or private subnets\.

Application traffic is balanced at `L7` of the OSI model\. To load balance network traffic at `L4`, you deploy a Kubernetes `service` of the `LoadBalancer` type\. This type provisions an AWS Network Load Balancer\. For more information, see [Network load balancing on Amazon EKS](network-load-balancing.md)\. To learn more about the differences between the two types of load balancing, see [Elastic Load Balancing features](https://aws.amazon.com/elasticloadbalancing/features/) on the AWS website\. 

**Prerequisites**

Before you can load balance application traffic to an application, you must meet the following requirements\.
+ Have an existing cluster\. If you don't have an existing cluster, see [Getting started with Amazon EKS](getting-started.md)\. If you need to update the version of an existing cluster, see [Updating an Amazon EKS cluster Kubernetes version](update-cluster.md)\.
+ Have the AWS Load Balancer Controller deployed on your cluster\. For more information, see [What is the AWS Load Balancer Controller?](aws-load-balancer-controller.md)\. We recommend version `2.7.2` or later\.
+ At least two subnets in different Availability Zones\. The AWS Load Balancer Controller chooses one subnet from each Availability Zone\. When multiple tagged subnets are found in an Availability Zone, the controller chooses the subnet whose subnet ID comes first lexicographically\. Each subnet must have at least eight available IP addresses\.

  If you're using multiple security groups attached to worker node, exactly one security group must be tagged as follows\. Replace `my-cluster` with your cluster name\.
  + **Key** – `kubernetes.io/cluster/my-cluster`
  + **Value** – `shared` or `owned`
+ If you're using the AWS Load Balancer Controller version `2.1.1` or earlier, subnets must be tagged in the format that follows\. If you're using version `2.1.2` or later, tagging is optional\. However, we recommend that you tag a subnet if any of the following is the case\. You have multiple clusters that are running in the same VPC, or have multiple AWS services that share subnets in a VPC\. Or, you want more control over where load balancers are provisioned for each cluster\. Replace `my-cluster` with your cluster name\.
  + **Key** – `kubernetes.io/cluster/my-cluster`
  + **Value** – `shared` or `owned`
+ Your public and private subnets must meet the following requirements\. This is unless you explicitly specify subnet IDs as an annotation on a service or ingress object\. Assume that you provision load balancers by explicitly specifying subnet IDs as an annotation on a service or ingress object\. In this situation, Kubernetes and the AWS load balancer controller use those subnets directly to create the load balancer and the following tags aren't required\.
  + **Private subnets** – Must be tagged in the following format\. This is so that Kubernetes and the AWS load balancer controller know that the subnets can be used for internal load balancers\. If you use `eksctl` or an Amazon EKS AWS CloudFormation template to create your VPC after March 26, 2020, the subnets are tagged appropriately when created\. For more information about the Amazon EKS AWS CloudFormation VPC templates, see [Creating a VPC for your Amazon EKS cluster](creating-a-vpc.md)\.
    + **Key** – `kubernetes.io/role/internal-elb`
    + **Value** – `1`
  + **Public subnets** – Must be tagged in the following format\. This is so that Kubernetes knows to use only the subnets that were specified for external load balancers\. This way, Kubernetes doesn't choose a public subnet in each Availability Zone \(lexicographically based on their subnet ID\)\. If you use `eksctl` or an Amazon EKS AWS CloudFormation template to create your VPC after March 26, 2020, the subnets are tagged appropriately when created\. For more information about the Amazon EKS AWS CloudFormation VPC templates, see [Creating a VPC for your Amazon EKS cluster](creating-a-vpc.md)\.
    + **Key** – `kubernetes.io/role/elb`
    + **Value** – `1`

  If the subnet role tags aren't explicitly added, the Kubernetes service controller examines the route table of your cluster VPC subnets\. This is to determine if the subnet is private or public\. We recommend that you don't rely on this behavior\. Rather, explicitly add the private or public role tags\. The AWS Load Balancer Controller doesn't examine route tables\. It also requires the private and public tags to be present for successful auto discovery\.

**Considerations**
+ The [AWS Load Balancer Controller](https://github.com/kubernetes-sigs/aws-load-balancer-controller) creates ALBs and the necessary supporting AWS resources whenever a Kubernetes ingress resource is created on the cluster with the `kubernetes.io/ingress.class: alb` annotation\. The ingress resource configures the ALB to route HTTP or HTTPS traffic to different Pods within the cluster\. To ensure that your ingress objects use the AWS Load Balancer Controller, add the following annotation to your Kubernetes ingress specification\. For more information, see [Ingress specification](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.7/guide/ingress/spec/) on GitHub\.

  ```
  annotations:
      kubernetes.io/ingress.class: alb
  ```
**Note**  
If you're load balancing to `IPv6` Pods, add the following annotation to your ingress spec\. You can only load balance over `IPv6` to IP targets, not instance targets\. Without this annotation, load balancing is over `IPv4`\.  

  ```
  alb.ingress.kubernetes.io/ip-address-type: dualstack
  ```
+ The AWS Load Balancer Controller supports the following traffic modes:
  + **Instance** – Registers nodes within your cluster as targets for the ALB\. Traffic reaching the ALB is routed to `NodePort` for your service and then proxied to your Pods\. This is the default traffic mode\. You can also explicitly specify it with the `alb.ingress.kubernetes.io/target-type: instance` annotation\.
**Note**  
Your Kubernetes service must specify the `NodePort` or "LoadBalancer" type to use this traffic mode\.
  + **IP** – Registers Pods as targets for the ALB\. Traffic reaching the ALB is directly routed to Pods for your service\. You must specify the `alb.ingress.kubernetes.io/target-type: ip` annotation to use this traffic mode\. The IP target type is required when target Pods are running on Fargate\.
+ To tag ALBs created by the controller, add the following annotation to the controller: `alb.ingress.kubernetes.io/tags`\. For a list of all available annotations supported by the AWS Load Balancer Controller, see [Ingress annotations](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.7/guide/ingress/annotations/) on GitHub\.
+ Upgrading or downgrading the ALB controller version can introduce breaking changes for features that rely on it\. For more information about the breaking changes that are introduced in each release, see the [ALB controller release notes](https://github.com/kubernetes-sigs/aws-load-balancer-controller/releases) on GitHub\.
<a name="alb-ingress-groups"></a>
**To share an application load balancer across multiple service resources using `IngressGroups`**  
To join an ingress to a group, add the following annotation to a Kubernetes ingress resource specification\. 

```
alb.ingress.kubernetes.io/group.name: my-group
```

The group name must:
+ Be 63 or fewer characters in length\.
+ Consist of lower case letters, numbers, `-`, and `.`
+ Start and end with a letter or number\.

The controller automatically merges ingress rules for all ingresses in the same ingress group\. It supports them with a single ALB\. Most annotations that are defined on an ingress only apply to the paths defined by that ingress\. By default, ingress resources don't belong to any ingress group\.

**Warning**  
**Potential security risk**: Specify an ingress group for an ingress only when all the Kubernetes users that have RBAC permission to create or modify ingress resources are within the same trust boundary\. If you add the annotation with a group name, other Kubernetes users might create or modify their ingresses to belong to the same ingress group\. Doing so can cause undesirable behavior, such as overwriting existing rules with higher priority rules\. 

You can add an order number of your ingress resource\.

```
alb.ingress.kubernetes.io/group.order: '10'
```

The number can be 1\-1000\. The lowest number for all ingresses in the same ingress group is evaluated first\. All ingresses without this annotation are evaluated with a value of zero\. Duplicate rules with a higher number can overwrite rules with a lower number\. By default, the rule order between ingresses within the same ingress group is determined lexicographically based namespace and name\.

**Important**  
Ensure that each ingress in the same ingress group has a unique priority number\. You can't have duplicate order numbers across ingresses\.

## \(Optional\) Deploy a sample application<a name="application-load-balancer-sample-application"></a>

**Prerequisites**
+ At least one public or private subnet in your cluster VPC\.
+ Have the AWS Load Balancer Controller deployed on your cluster\. For more information, see [What is the AWS Load Balancer Controller?](aws-load-balancer-controller.md)\. We recommend version `2.7.2` or later\.

**To deploy a sample application**

You can run the sample application on a cluster that has Amazon EC2 nodes, Fargate Pods, or both\.

1. If you're not deploying to Fargate, skip this step\. If you're deploying to Fargate, create a Fargate profile\. You can create the profile by running the following command or in the [AWS Management Console](fargate-profile.md#create-fargate-profile) using the same values for `name` and `namespace` that are in the command\. Replace the `example values` with your own\.

   ```
   eksctl create fargateprofile \
       --cluster my-cluster \
       --region region-code \
       --name alb-sample-app \
       --namespace game-2048
   ```

1. Deploy the game [2048](https://play2048.co/) as a sample application to verify that the AWS Load Balancer Controller creates an AWS ALB as a result of the ingress object\. Complete the steps for the type of subnet you're deploying to\.

   1. If you're deploying to Pods in a cluster that you created with the `IPv6` family, skip to the next step\.
      + **Public**

        ```
        kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.7.2/docs/examples/2048/2048_full.yaml
        ```
      + **Private**

        1. Download the manifest\.

           ```
           curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.7.2/docs/examples/2048/2048_full.yaml
           ```

        1. Edit the file and find the line that says `alb.ingress.kubernetes.io/scheme: internet-facing`\.

        1. Change `internet-facing` to `internal` and save the file\.

        1. Apply the manifest to your cluster\.

           ```
           kubectl apply -f 2048_full.yaml
           ```

   1. If you're deploying to Pods in a cluster that you created with the [`IPv6` family](cni-ipv6.md), complete the following steps\.

      1. Download the manifest\.

         ```
         curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.7.2/docs/examples/2048/2048_full.yaml
         ```

      1. Open the file in an editor and add the following line to the annotations in the ingress spec\.

         ```
         alb.ingress.kubernetes.io/ip-address-type: dualstack
         ```

      1. If you're load balancing to internal Pods, rather than internet facing Pods, change the line that says `alb.ingress.kubernetes.io/scheme: internet-facing` to `alb.ingress.kubernetes.io/scheme: internal`

      1. Save the file\.

      1. Apply the manifest to your cluster\.

         ```
         kubectl apply -f 2048_full.yaml
         ```

1. After a few minutes, verify that the ingress resource was created with the following command\.

   ```
   kubectl get ingress/ingress-2048 -n game-2048
   ```

   An example output is as follows\.

   ```
   NAME           CLASS    HOSTS   ADDRESS                                                                   PORTS   AGE
   ingress-2048   <none>   *       k8s-game2048-ingress2-xxxxxxxxxx-yyyyyyyyyy.region-code.elb.amazonaws.com   80      2m32s
   ```
**Note**  
If you created the load balancer in a private subnet, the value under `ADDRESS` in the previous output is prefaced with `internal-`\.  
If your ingress wasn't successfully created after several minutes, run the following command to view the AWS Load Balancer Controller logs\. These logs might contain error messages that you can use to diagnose issues with your deployment\.  

   ```
   kubectl logs -f -n kube-system -l app.kubernetes.io/instance=aws-load-balancer-controller
   ```

1. If you deployed to a public subnet, open a browser and navigate to the `ADDRESS` URL from the previous command output to see the sample application\. If you don't see anything, refresh your browser and try again\. If you deployed to a private subnet, then you'll need to view the page from a device within your VPC, such as a bastion host\. For more information, see [Linux Bastion Hosts on AWS](https://aws.amazon.com/quickstart/architecture/linux-bastion/)\.  
![\[2048 sample application\]](http://docs.aws.amazon.com/eks/latest/userguide/images/2048.png)

1. When you finish experimenting with your sample application, delete it by running one of the the following commands\.
   + If you applied the manifest, rather than applying a copy that you downloaded, use the following command\.

     ```
     kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.7.2/docs/examples/2048/2048_full.yaml
     ```
   + If you downloaded and edited the manifest, use the following command\.

     ```
     kubectl delete -f 2048_full.yaml
     ```