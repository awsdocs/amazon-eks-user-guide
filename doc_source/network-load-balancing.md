# Network load balancing on Amazon EKS<a name="network-load-balancing"></a>

When you create a Kubernetes `Service` of type `LoadBalancer`, an AWS Network Load Balancer \(NLB\) is provisioned that load balances network traffic\. For more information about NLBs, see [What is a Network Load Balancer?](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html)\. For more information about a Kubernetes Service, see [Service](https://kubernetes.io/docs/concepts/services-networking/service/) in the Kubernetes documentation\. NLBs can be used with pods deployed to Amazon EC2 nodes or to AWS Fargate IP targets\. You can deploy an AWS load balancer to a public or private subnet\.

Network traffic is load balanced at L4 of the OSI model\. To load balance application traffic at L7, you deploy a Kubernetes `Ingress`, which provisions an AWS Application Load Balancer\. For more information, see [Application load balancing on Amazon EKS](alb-ingress.md)\. To learn more about the differences between the two types of load balancing, see [Elastic Load Balancing features](https://docs.aws.amazon.com/elasticloadbalancing/features/) on the AWS website\.

In Amazon EKS, you can load balance network traffic to an NLB \(*instance* or *IP* target\)\. For more information about NLB target types, see [Target type](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-target-groups.html#target-type) in the User Guide for Network Load Balancers\. For more information, see [AWS load balancer controller](https://github.com/kubernetes-sigs/aws-alb-ingress-controller) on GitHub\.

**Important**  
With the `2.2.0` release of the [AWS Load Balancer Controller](aws-load-balancer-controller.md), the [Kubernetes in\-tree service load balancer controller](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer) is deprecated, and is only receiving critical bug fixes\. When provisioning new network load balancers for Services of type `LoadBalancer`, we recommend using the AWS Load Balancer Controller\. The information in this topic assumes that you're using the AWS Load Balancer Controller, not the Kubernetes in\-tree controller\.

**Prerequisites**

Before you can load balance network traffic to an application, you must meet the following requirements\.
+ At least one subnet\. In the case of multiple tagged subnets found in an Availability Zone, the controller chooses the first subnet in lexicographical order by the subnet IDs\.
+ If you're using the AWS Load Balancer controller version `v2.1.1` or earlier, subnets must be tagged as follows\. If using version 2\.1\.2 or later, this tag is optional\. You might want to tag a subnet if you have multiple clusters running in the same VPC, or multiple AWS services sharing subnets in a VPC, and want more control over where load balancers are provisioned per cluster\. If you explicitly specify subnet IDs as an annotation on a Service object, then Kubernetes and the AWS Load Balancer Controller use those subnets directly to create the load balancer\. Subnet tagging is not required if you choose to use this method for provisioning load balancers and you can skip the following private and public subnet tagging requirements\. Replace *`cluster-name`* with your cluster name\.
  + **Key** – `kubernetes.io/cluster/cluster-name`
  + **Value** – `shared` or `owned`
+ Your public and private subnets must meet the following requirements, unless you explicitly specify subnet IDs as an annotation on a Service or Ingress object\. If you provision load balancers by explicitly specifying subnet IDs as an annotation on a Service or Ingress object, then Kubernetes and the AWS Load Balancer Controller use those subnets directly to create the load balancer and the following tags are not required\.
  + **Private subnets** – Must be tagged as follows so that Kubernetes and the AWS Load Balancer Controller know that the subnets can be used for internal load balancers\. If you use `eksctl` or an Amazon EKS AWS AWS CloudFormation template to create your VPC after March 26, 2020, then the subnets are tagged appropriately when they're created\. For more information about the Amazon EKS AWS AWS CloudFormation VPC templates, see [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md)\.
    + **Key** – `kubernetes.io/role/internal-elb`
    + **Value** – `1`
  + **Public subnets** – Must be tagged as follows so that Kubernetes knows to use only those subnets for external load balancers instead of choosing a public subnet in each Availability Zone \(in lexicographical order by subnet ID\)\. If you use `eksctl` or an Amazon EKS AWS CloudFormation template to create your VPC after March 26, 2020, then the subnets are tagged appropriately when they're created\. For more information about the Amazon EKS AWS CloudFormation VPC templates, see [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md)\.
    + **Key** – `kubernetes.io/role/elb`
    + **Value** – `1`

  If the subnet role tags are not explicitly added, the Kubernetes service controller examines the route table of your cluster VPC subnets to determine if the subnet is private or public\. We recommend that you do not rely on this behavior, and instead explicitly add the private or public role tags\. The AWS Load Balancer Controller does not examine route tables, and requires the private and public tags to be present for successful auto discovery\. 

**Considerations**
+ You can only use NLB *IP* targets with the [Amazon EKS VPC CNI plugin](pod-networking.md)\. You can use NLB *instance* targets with the Amazon EKS VPC CNI plugin or [alternate compatible CNI plugins](alternate-cni-plugins.md)\.
+ The controller provisions NLBs, but not Classic Load Balancers\.
+ The configuration of your load balancer is controlled by annotations that are added to the manifest for your service\. If you want to add tags to the load balancer when, or after, it's created, add the following annotation in your service specification\. For more information, see [Other ELB annotations](https://kubernetes.io/docs/concepts/services-networking/service/#other-elb-annotations) in the Kubernetes documentation\.

  ```
  service.beta.kubernetes.io/aws-load-balancer-additional-resource-tags
  ```
+ You can assign [Elastic IP addresses](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html) to the Network Load Balancer by adding the following annotation\. Replace the *`example-values`* with the Allocation IDs of your Elastic IP addresses\. The number of Allocation IDs must match the number of subnets used for the load balancer\.

  ```
  service.beta.kubernetes.io/aws-load-balancer-eip-allocations: eipalloc-xxxxxxxxxxxxxxxxx,eipalloc-yyyyyyyyyyyyyyyyy
  ```
+ For each NLB that you create Amazon EKS adds one inbound rule to the node's security group for client traffic and one rule for each load balancer subnet in the VPC for health checks\. Deployment of a service of type `LoadBalancer` can fail if Amazon EKS attempts to create rules that exceed the quota for the maximum number of rules allowed for a security group\. For more information, see [Security groups](https://docs.aws.amazon.com/vpc/latest/userguide/amazon-vpc-limits.html#vpc-limits-security-groups) in Amazon VPC quotas in the Amazon VPC User Guide\. Consider the following options to minimize the chances of exceeding the maximum number of rules for a security group\.
  + Request an increase in your rules per security group quota\. For more information, see [Requesting a quota increase](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html) in the Service Quotas User Guide\.
  + Use [Create a network load balancer](#network-load-balancer), rather than instance targets\. With IP targets, rules can potentially be shared for the same target ports\. Load balancer subnets can be manually specified with an annotation\. For more information, see [Annotations](https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/guide/service/annotations/#subnets) on GitHub\.
  + Use an Ingress, instead of a Service of type `LoadBalancer` to send traffic to your service\. The AWS Application Load Balancer \(ALB\) requires fewer rules than NLBs\. An ALB can also be shared across multiple Ingresses\. For more information, see [Application load balancing on Amazon EKS](alb-ingress.md)\.
  + Deploy your clusters to multiple accounts\.
+ If your pods run on Windows, In an Amazon EKS cluster, a single service with a load balancer can support up to 64 backend pods\. Each pod has its own unique IP address\. This is a limitation of the Windows OS on the Amazon EC2 nodes\.
+ We recommend only creating new NLBs with the AWS Load Balancer Controller\. Attempting to replace existing NLBs created with the Kubernetes in\-tree load\-balancer controller can result in multiple NLBs that might cause application downtime\.

## Create a network load balancer<a name="network-load-balancer"></a>

You can create a network load balancer with IP or instance targets\. Select the tab with the name of the type of targets you want to load balance to\.

------
#### [ IP targets ]

You can use IP targets with pods deployed to Amazon EC2 nodes or Fargate\. Your Kubernetes service must be created as type `LoadBalancer`\. For more information, see [Type LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer) in the Kubernetes documentation\.

To create a load balancer that uses IP targets, add the following annotation to a service manifest and deploy your service\. You can view a [sample service manifest](#network-load-balancing-service-sample-manifest) with the annotations\.

```
service.beta.kubernetes.io/aws-load-balancer-type: "external"
service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: "ip"
```

NLBs are created as internal, by default\. For internal NLBs, your Amazon EKS cluster must be configured to use at least one private subnet in your VPC\. Kubernetes examines the route table for your subnets to identify whether they are public or private\. Public subnets have a route directly to the internet using an internet gateway, but private subnets do not\. 

If you want to create an internet\-facing NLB, add the following annotation:

```
service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"
```

**Note**  
The `service.beta.kubernetes.io/aws-load-balancer-type: "nlb-ip"` annotation is still supported for backwards compatibility, but we recommend using the previous annotations for new load balancers instead of `service.beta.kubernetes.io/aws-load-balancer-type: "nlb-ip"`\.

**Important**  
Do not edit the annotations after creating your service\. If you need to modify it, delete the service object and create it again with the desired value for this annotation\.

------
#### [ Instance targets ]

In the past, the Kubernetes in\-tree controller created NLBs with instance targets\. Version 2\.2\.0 or later of the AWS Load Balancer Controller creates NLBs with instance targets\. We recommend using it, rather than the Kubernetes in\-tree controller, to create new NLBs\. You can use NLB instance targets with pods deployed to Amazon EC2 nodes, but not to Fargate\. To load balance network traffic across pods deployed to Fargate, you must use IP targets\. 

To deploy a load balancer to a private subnet, your service specification must have the following annotations\. You can view a [sample service manifest](#network-load-balancing-service-sample-manifest) with the annotations\.

```
service.beta.kubernetes.io/aws-load-balancer-type: "external"
service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: "instance"
```

NLBs are created as internal, by default\. For internal NLBs, your Amazon EKS cluster must be configured to use at least one private subnet in your VPC\. Kubernetes examines the route table for your subnets to identify whether they are public or private\. Public subnets have a route directly to the internet using an internet gateway, but private subnets do not\. 

If you want to create an internet\-facing NLB, add the following annotation:

```
service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"
```

**Important**  
Do not edit the annotations after creating your service\. If you need to modify it, delete the service object and create it again with the desired value for this annotation\.

------

## Deploy a sample application<a name="load-balancer-sample-application"></a>

**To deploy a sample application**

1. Deploy a sample application\.

   1. Save the following contents to a file named *`sample-deployment.yaml`* file on your computer\.

      ```
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: sample-app
      spec:
        replicas: 3
        selector:
          matchLabels:
            app: nginx
        template:
          metadata:
            labels:
              app: nginx
          spec:
            containers:
              - name: nginx
                image: public.ecr.aws/nginx/nginx:1.19.6
                ports:
                  - name: http
                    containerPort: 80
      ```

   1. Apply the manifest to the cluster\.

      ```
      kubectl apply -f sample-deployment.yaml
      ```

1. Create a service with an internal NLB that load balances to IP targets\.

   1. <a name="network-load-balancing-service-sample-manifest"></a>Save the following contents to a file named *`sample-service.yaml`* file on your computer\.

      ```
      apiVersion: v1
      kind: Service
      metadata:
        name: sample-service
        annotations:
          service.beta.kubernetes.io/aws-load-balancer-type: external
          service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: ip
          service.beta.kubernetes.io/aws-load-balancer-scheme: internet-facing
      spec:
        ports:
          - port: 80
            targetPort: 80
            protocol: TCP
        type: LoadBalancer
        selector:
          app: nginx
      ```

   1. Apply the manifest to the cluster\.

      ```
      kubectl apply -f sample-service.yaml
      ```

1. Verify that the service was deployed\.

   ```
   kubectl get svc sample-service
   ```

   Output

   ```
   NAME            TYPE           CLUSTER-IP         EXTERNAL-IP                                                                    PORT(S)        AGE
   sample-service  LoadBalancer   10.100.240.137   k8s-default-samplese-xxxxxxxxxx-xxxxxxxxxxxxxxxx.elb.us-west-2.amazonaws.com   80:32400/TCP   16h
   ```

1. Open the [Amazon EC2 AWS Management Console](https://console.aws.amazon.com/ec2)\. Select **Target Groups** \(under **Load Balancing**\) in the left panel\. In the **Name** column, select the target group's name where the value in the **Load balancer** column matches the name in the `EXTERNAL-IP` column of the output in the previous step\. For example, you'd select the target group named r `k8s-default-samplese-xxxxxxxxxx` if your output were the same as the output above\. The **Target type** is `IP` because that was specified in the sample service deployment manifest\.

1. Select the **Target group** and then select the **Targets** tab\. Under **Registered targets**, you should see three IP addresses of the three replicas deployed in a previous step\. Wait until the status of all targets is** healthy** before continuing\. It may take several minutes before all targets are `healthy`\. The targets may have an `unhealthy` state before changing to `healthy`\.

1. Send traffic to the service replacing *xxxxxxxxxx\-xxxxxxxxxxxxxxxx* with the value returned in a previous step for the `EXTERNAL-IP` and *us\-west\-2* with the Region that your cluster is in\.

   ```
   curl k8s-default-samplese-xxxxxxxxxx-xxxxxxxxxxxxxxxx.elb.us-west-2.amazonaws.com
   ```

   Output

   ```
   <!DOCTYPE html>
   <html>
   <head>
   <title>Welcome to nginx!</title>
   ...
   ```

1. When you're finished with the sample deployment and service, remove them\.

   ```
   kubectl delete service sample-service
   kubectl delete deployment sample-app
   ```