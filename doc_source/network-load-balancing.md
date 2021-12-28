# Network load balancing on Amazon EKS<a name="network-load-balancing"></a>

When you create a Kubernetes `Service` of type `LoadBalancer`, an AWS Network Load Balancer \(NLB\) is provisioned that load balances network traffic\. For more information about AWS NLBs, see [What is a Network Load Balancer?](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html)\. For more information about a Kubernetes Service, see [Service](https://kubernetes.io/docs/concepts/services-networking/service/) in the Kubernetes documentation\. NLBs can be used with Pods deployed to Amazon EC2 nodes or to AWS Fargate IP targets\. You can deploy an AWS NLB to a public or private subnet\.

Network traffic is load balanced at L4 of the OSI model\. To load balance application traffic at L7, you deploy a Kubernetes `Ingress`, which provisions an AWS Application Load Balancer \(ALB\)\. For more information, see [Application load balancing on Amazon EKS](alb-ingress.md)\. To learn more about the differences between the two types of load balancing, see [Elastic Load Balancing features](https://docs.aws.amazon.com/elasticloadbalancing/features/) on the AWS website\.

In Amazon EKS, you can load balance network traffic to an NLB \(with *instance* or *IP* targets\) using the AWS Load Balancer Controller\. For more information, see [AWS Load Balancer Controller](https://github.com/kubernetes-sigs/aws-load-balancer-controller) on GitHub\. For more information about NLB target types, see [Target type](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-target-groups.html#target-type) in the User Guide for Network Load Balancers\.

**Important**  
With the `2.2.0` and later releases of the [AWS Load Balancer Controller](aws-load-balancer-controller.md), the legacy [AWS cloud provider load balancer controller](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer) has been phased out, and is only receiving critical bug fixes\. For more information, see [Legacy Cloud Provider](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.3/guide/service/annotations/#legacy-cloud-provider) in the AWS Load Balancer Controller documentation\. When provisioning new NLBs for Services of type `LoadBalancer`, we recommend using the AWS Load Balancer Controller\. If you still need to create a network load balancer with instance targets using the legacy AWS legacy cloud provider load balancer controller, see [Type LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer) in the Kubernetes documentation\.  
The information in this topic is about the AWS Load Balancer Controller, not the legacy AWS Cloud Provider controller\. Service annotations are different when using the AWS Load Balancer Controller than they are when using the legacy controller\. Make sure to review the [annotations](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.3/guide/service/annotations/) for the AWS Load Balancer Controller before deploying Services\.

**Prerequisites**

Before you can load balance network traffic, you must meet the following requirements\.
+ Have the AWS Load Balancer Controller deployed on your cluster\. For more information, see [AWS Load Balancer Controller](aws-load-balancer-controller.md)\. We recommend version 2\.3\.1 or later\.
+ At least one subnet\. If multiple tagged subnets are found in an Availability Zone, the controller chooses the first subnet whose subnet ID comes first lexicographically\.
+ If you're using the AWS Load Balancer Controller version `v2.1.1` or earlier, subnets must be tagged as follows\. If using version 2\.1\.2 or later, this tag is optional\. You might want to tag a subnet if you have multiple clusters running in the same VPC, or multiple AWS services sharing subnets in a VPC, and want more control over where load balancers are provisioned for each cluster\. If you explicitly specify subnet IDs as an annotation on a Service object, then Kubernetes and the AWS Load Balancer Controller use those subnets directly to create the load balancer\. Subnet tagging isn't required if you choose to use this method for provisioning load balancers and you can skip the following private and public subnet tagging requirements\. Replace *`cluster-name`* with your cluster name\.
  + **Key** – `kubernetes.io/cluster/cluster-name`
  + **Value** – `shared` or `owned`
+ Your public and private subnets must meet the following requirements, unless you explicitly specify subnet IDs as an annotation on a Service or Ingress object\. If you provision load balancers by explicitly specifying subnet IDs as an annotation on a Service or Ingress object, then Kubernetes and the AWS Load Balancer Controller use those subnets directly to create the load balancer and the following tags aren't required\.
  + **Private subnets** – Must be tagged in the following format\. This is so that Kubernetes and the AWS Load Balancer Controller know that the subnets can be used for internal load balancers\. If you use `eksctl` or an Amazon EKS AWS AWS CloudFormation template to create your VPC after March 26, 2020, then the subnets are tagged appropriately when they're created\. For more information about the Amazon EKS AWS AWS CloudFormation VPC templates, see [Creating a VPC for your Amazon EKS cluster](creating-a-vpc.md)\.
    + **Key** – `kubernetes.io/role/internal-elb`
    + **Value** – `1`
  + **Public subnets** – Must be tagged in the following format\. This is so that Kubernetes knows to use only those subnets for external load balancers instead of choosing a public subnet in each Availability Zone \(based on the lexicographical order of the subnet IDs\)\. If you use `eksctl` or an Amazon EKS AWS CloudFormation template to create your VPC after March 26, 2020, then the subnets are tagged appropriately when they're created\. For more information about the Amazon EKS AWS CloudFormation VPC templates, see [Creating a VPC for your Amazon EKS cluster](creating-a-vpc.md)\.
    + **Key** – `kubernetes.io/role/elb`
    + **Value** – `1`

  If the subnet role tags aren't explicitly added, the Kubernetes Service controller examines the route table of your cluster VPC subnets to determine if the subnet is private or public\. We recommend that you don't rely on this behavior, and instead explicitly add the private or public role tags\. The AWS Load Balancer Controller doesn't examine route tables, and requires the private and public tags to be present for successful auto discovery\. 

**Considerations**
+ When using the [Amazon EKS VPC CNI plugin](pod-networking.md), the AWS Load Balancer Controller can load balance to IP or instance targets\. When using [Alternate compatible CNI plugins](alternate-cni-plugins.md), the controller can only load balance to instance targets\.
+ The controller provisions NLBs, but not Classic Load Balancers\.
+ The configuration of your load balancer is controlled by annotations that are added to the manifest for your Service\. If you want to add tags to the load balancer when or after it's created, add the following annotation in your Service specification\. For more information, see [AWS Resource Tags](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.3/guide/service/annotations/#aws-resource-tags) in the AWS Load Balancer Controller documentation\.

  ```
  service.beta.kubernetes.io/aws-load-balancer-additional-resource-tags
  ```
+ You can assign [Elastic IP addresses](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html) to the NLB by adding the following annotation\. Replace the *`example-values`* with the `Allocation IDs` of your Elastic IP addresses\. The number of `Allocation IDs` must match the number of subnets that are used for the load balancer\. For more information, see the [AWS Load Balancer Controller](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.3/guide/service/annotations/#eip-allocations) documentation\.

  ```
  service.beta.kubernetes.io/aws-load-balancer-eip-allocations: eipalloc-xxxxxxxxxxxxxxxxx,eipalloc-yyyyyyyyyyyyyyyyy
  ```
+ Amazon EKS adds one inbound rule to the node's security group for client traffic and one rule for each load balancer subnet in the VPC for health checks for each NLB that you create\. Deployment of a Service of type `LoadBalancer` can fail if Amazon EKS attempts to create rules that exceed the quota for the maximum number of rules allowed for a security group\. For more information, see [Security groups](https://docs.aws.amazon.com/vpc/latest/userguide/amazon-vpc-limits.html#vpc-limits-security-groups) in Amazon VPC quotas in the Amazon VPC User Guide\. Consider the following options to minimize the chances of exceeding the maximum number of rules for a security group:
  + Request an increase in your rules per security group quota\. For more information, see [Requesting a quota increase](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html) in the Service Quotas User Guide\.
  + Use IP targets, rather than instance targets\. With IP targets, you can share rules for the same target ports\. You can manually specify load balancer subnets with an annotation\. For more information, see [Annotations](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.3/guide/service/annotations/) on GitHub\.
  + Use an Ingress, instead of a Service of type `LoadBalancer`, to send traffic to your Service\. The AWS Application Load Balancer requires fewer rules than NLBs\. You can share an ALB across multiple Ingresses, while an NLB cannot be shared across services\. For more information, see [Application load balancing on Amazon EKS](alb-ingress.md)\.
  + Deploy your clusters to multiple accounts\.
+ If your Pods run on Windows in an Amazon EKS cluster, a single Service with a load balancer can support up to 64 backend Pods\. Each Pod has its own unique IP address\. This is a limitation of the Windows OS on the Amazon EC2 nodes\.
+ We recommend only creating new NLBs with the AWS Load Balancer Controller\. Attempting to replace existing NLBs created with the legacy `AWS` Cloud Provider controller can result in multiple NLBs that might cause application downtime\.

## Create a network load balancer<a name="network-load-balancer"></a>

**Important**  
Service annotations are different when using the AWS Load Balancer Controller than they are when using the legacy AWS Cloud Provider load balancer controller\. Make sure to review the [annotations](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.3/guide/service/annotations/) for the AWS Load Balancer Controller before deploying Services\.

You can create a network load balancer with IP or instance targets\.

------
#### [ IP targets ]

You can use IP targets with Pods deployed to Amazon EC2 nodes or Fargate\. Your Kubernetes Service must be created as type `LoadBalancer`\. For more information, see [Type LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer) in the Kubernetes documentation\. 

To create a load balancer that uses IP targets, add the following annotation to a Service manifest and deploy your Service\. You can view a [sample Service manifest](#network-load-balancing-service-sample-manifest) with the annotations\.

```
service.beta.kubernetes.io/aws-load-balancer-type: "external"
service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: "ip"
```

NLBs are created with the `internal` `aws-load-balancer-scheme`, by default\. For `internal` NLBs, your Amazon EKS cluster must be configured to use at least one private subnet in your VPC\. Kubernetes examines the route table for your subnets to identify whether they are public or private\. Public subnets have a route directly to the internet using an internet gateway, but private subnets do not\. 

If you want to create an NLB in a public subnet to load balance to Amazon EC2 nodes \(Fargate can only be private\), specify `internet-facing` with the following annotation:

```
service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"
```

**Note**  
The `service.beta.kubernetes.io/aws-load-balancer-type: "nlb-ip"` annotation is still supported for backwards compatibility\. However, we recommend using the previous annotations for new load balancers instead of `service.beta.kubernetes.io/aws-load-balancer-type: "nlb-ip"`\.

**Important**  
Do not edit the annotations after creating your Service\. If you need to modify it, delete the Service object and create it again with the desired value for this annotation\.

------
#### [ Instance targets ]

The legacy AWS Cloud Provider load balancer controller created NLBs with instance targets only\. Version 2\.2\.0 and later of the AWS Load Balancer Controller also creates NLBs with instance targets\. We recommend using it, rather than the legacy controller, to create new NLBs\. You can use NLB instance targets with Pods deployed to Amazon EC2 nodes, but not to Fargate\. To load balance network traffic across Pods deployed to Fargate, you must use IP targets\. 

To deploy an NLB to a private subnet, your Service specification must have the following annotations\. You can view a [sample Service manifest](#network-load-balancing-service-sample-manifest) with the annotations\. The `external` value for `aws-load-balancer-type` is what causes the AWS Load Balancer Controller, rather than the legacy AWS Cloud Provider controller, to create the NLB\.

```
service.beta.kubernetes.io/aws-load-balancer-type: "external"
service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: "instance"
```

NLBs are created with the `internal` `aws-load-balancer-scheme`, by default\. For internal NLBs, your Amazon EKS cluster must be configured to use at least one private subnet in your VPC\. Kubernetes examines the route table for your subnets to identify whether they are public or private\. Public subnets have a route directly to the internet using an internet gateway, but private subnets do not\. 

If you want to create an NLB in a public subnet to load balance to Amazon EC2 nodes, specify `internet-facing` with the following annotation:

```
service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"
```

**Important**  
Do not edit the annotations after creating your Service\. If you need to modify it, delete the Service object and create it again with the desired value for this annotation\.

------

## \(Optional\) Deploy a sample application<a name="load-balancer-sample-application"></a>

**Prerequisites**
+ At least one public or private subnet in your cluster VPC\.
+ Have the AWS Load Balancer Controller deployed on your cluster\. For more information, see [AWS Load Balancer Controller](aws-load-balancer-controller.md)\. We recommend version 2\.3\.1 or later\.

**To deploy a sample application**

1. If you're deploying to Fargate, make sure you have an available private subnet in your VPC and create a Fargate profile\. If you're not deploying to Fargate, skip this step\. You can create the profile by running the following command or in the [AWS Management Console](fargate-profile.md#create-fargate-profile) using the same values for `name` and `namespace` that are in the command\.

   ```
   eksctl create fargateprofile \
       --cluster my-cluster \
       --region region-code \
       --name nlb-sample-app \
       --namespace nlb-sample-app
   ```

1. Deploy a sample application\.

   1. Create a namespace for the application\.

      ```
      kubectl create namespace nlb-sample-app
      ```

   1. Save the following contents to a file named `sample-deployment.yaml` file on your computer\.

      ```
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: nlb-sample-app
        namespace: nlb-sample-app
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
                image: public.ecr.aws/nginx/nginx:1.21
                ports:
                  - name: tcp
                    containerPort: 80
      ```

   1. Apply the manifest to the cluster\.

      ```
      kubectl apply -f sample-deployment.yaml
      ```

1. Create a Service with an internal NLB that load balances to IP targets\. 

   1. <a name="network-load-balancing-service-sample-manifest"></a>Save the following contents to a file named `sample-service.yaml` file on your computer\. If you're deploying to Fargate nodes, remove the `service.beta.kubernetes.io/aws-load-balancer-scheme: internet-facing` line\.

      ```
      apiVersion: v1
      kind: Service
      metadata:
        name: nlb-sample-service
        namespace: nlb-sample-app
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

1. <a name="nlb-sample-app-verify-deployment"></a>Verify that the Service was deployed\.

   ```
   kubectl get svc nlb-sample-service -n nlb-sample-app
   ```

   Output

   ```
   NAME            TYPE           CLUSTER-IP         EXTERNAL-IP                                                                    PORT(S)        AGE
   sample-service  LoadBalancer   10.100.240.137   k8s-nlbsampl-nlbsampl-xxxxxxxxxx-xxxxxxxxxxxxxxxx.elb.us-west-2.amazonaws.com   80:32400/TCP   16h
   ```
**Note**  
The values for *10\.100\.240\.137* and *xxxxxxxxxx*\-*xxxxxxxxxxxxxxxx* will be different than the example output \(they will be unique to your load balancer\) and *us\-west\-2* may be different for you, depending on which Region your cluster is in\. 

1. Open the [Amazon EC2 AWS Management Console](https://console.aws.amazon.com/ec2)\. Select **Target Groups** \(under **Load Balancing**\) in the left panel\. In the **Name** column, select the target group's name where the value in the **Load balancer** column matches a portion of the name in the `EXTERNAL-IP` column of the output in the previous step\. For example, you'd select the target group named `k8s-default-samplese-xxxxxxxxxx` if your output were the same as the output above\. The **Target type** is `IP` because that was specified in the sample Service manifest\.

1. Select the **Target group** and then select the **Targets** tab\. Under **Registered targets**, you should see three IP addresses of the three replicas deployed in a previous step\. Wait until the status of all targets is **healthy** before continuing\. It might take several minutes before all targets are `healthy`\. The targets might be in an `unhealthy` state before changing to a `healthy` state\.

1. Send traffic to the Service replacing *xxxxxxxxxx\-xxxxxxxxxxxxxxxx* and *us\-west\-2* with the values returned in the output for a [previous step](#nlb-sample-app-verify-deployment) for `EXTERNAL-IP`\. If you deployed to a private subnet, then you'll need to view the page from a device within your VPC, such as a bastion host\. For more information, see [Linux Bastion Hosts on AWS](http://aws.amazon.com/quickstart/architecture/linux-bastion/)\.

   ```
   curl k8s-default-samplese-xxxxxxxxxx-xxxxxxxxxxxxxxxx.elb.us-west-2.amazonaws.com
   ```

   The output is as follows\.

   ```
   <!DOCTYPE html>
   <html>
   <head>
   <title>Welcome to nginx!</title>
   ...
   ```

1. When you're finished with the sample Deployment, Service, and Namespace, remove them\.

   ```
   kubectl delete service nlb-sample-service -n nlb-sample-app
   kubectl delete deployment nlb-sample-app -n nlb-sample-app
   kubectl delete namespace nlb-sample-app
   ```
