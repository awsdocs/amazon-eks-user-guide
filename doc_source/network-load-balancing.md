# Network load balancing on Amazon EKS<a name="network-load-balancing"></a>

Network traffic is load balanced at `L4` of the OSI model\. To load balance application traffic at `L7`, you deploy a Kubernetes `ingress`, which provisions an AWS Application Load Balancer\. For more information, see [Application load balancing on Amazon EKS](alb-ingress.md)\. To learn more about the differences between the two types of load balancing, see [Elastic Load Balancing features](https://aws.amazon.com/elasticloadbalancing/features/) on the AWS website\. 

When you create a Kubernetes `Service` of type `LoadBalancer`, the AWS cloud provider load balancer controller creates AWS [Classic Load Balancers](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/introduction.html) by default, but can also create AWS [Network Load Balancers](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html)\. This controller is only receiving critical bug fixes in the future\. For more information about using the AWS cloud provider load balancer , see [AWS cloud provider load balancer controller](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer) in the Kubernetes documentation\. Its use is not covered in this topic\.

We recommend that you use version `2.7.2` or later of the [AWS Load Balancer Controller](aws-load-balancer-controller.md) instead of the AWS cloud provider load balancer controller\. The AWS Load Balancer Controller creates AWS Network Load Balancers, but doesn't create AWS Classic Load Balancers\. The remainder of this topic is about using the AWS Load Balancer Controller\.

An AWS Network Load Balancer can load balance network traffic to Pods deployed to Amazon EC2 IP and instance [targets](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-target-groups.html#target-type) or to AWS Fargate IP targets\. For more information, see [AWS Load Balancer Controller](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.7/guide/targetgroupbinding/targetgroupbinding/#targettype) on GitHub\.

**Prerequisites**

Before you can load balance network traffic using the AWS Load Balancer Controller, you must meet the following requirements\.
+ Have an existing cluster\. If you don't have an existing cluster, see [Getting started with Amazon EKS](getting-started.md)\. If you need to update the version of an existing cluster, see [Updating an Amazon EKS cluster Kubernetes version](update-cluster.md)\.
+ Have the AWS Load Balancer Controller deployed on your cluster\. For more information, see [What is the AWS Load Balancer Controller?](aws-load-balancer-controller.md)\. We recommend version `2.7.2` or later\.
+ At least one subnet\. If multiple tagged subnets are found in an Availability Zone, the controller chooses the first subnet whose subnet ID comes first lexicographically\. The subnet must have at least eight available IP addresses\.
+ If you're using the AWS Load Balancer Controller version `2.1.1` or earlier, subnets must be tagged as follows\. If using version `2.1.2` or later, this tag is optional\. You might want to tag a subnet if you have multiple clusters running in the same VPC, or multiple AWS services sharing subnets in a VPC, and want more control over where load balancers are provisioned for each cluster\. If you explicitly specify subnet IDs as an annotation on a service object, then Kubernetes and the AWS Load Balancer Controller use those subnets directly to create the load balancer\. Subnet tagging isn't required if you choose to use this method for provisioning load balancers and you can skip the following private and public subnet tagging requirements\. Replace `my-cluster` with your cluster name\.
  + **Key** – `kubernetes.io/cluster/my-cluster`
  + **Value** – `shared` or `owned`
+ Your public and private subnets must meet the following requirements, unless you explicitly specify subnet IDs as an annotation on a service or ingress object\. If you provision load balancers by explicitly specifying subnet IDs as an annotation on a service or ingress object, then Kubernetes and the AWS Load Balancer Controller use those subnets directly to create the load balancer and the following tags aren't required\.
  + **Private subnets** – Must be tagged in the following format\. This is so that Kubernetes and the AWS Load Balancer Controller know that the subnets can be used for internal load balancers\. If you use `eksctl` or an Amazon EKS AWS AWS CloudFormation template to create your VPC after March 26, 2020, then the subnets are tagged appropriately when they're created\. For more information about the Amazon EKS AWS AWS CloudFormation VPC templates, see [Creating a VPC for your Amazon EKS cluster](creating-a-vpc.md)\.
    + **Key** – `kubernetes.io/role/internal-elb`
    + **Value** – `1`
  + **Public subnets** – Must be tagged in the following format\. This is so that Kubernetes knows to use only those subnets for external load balancers instead of choosing a public subnet in each Availability Zone \(based on the lexicographical order of the subnet IDs\)\. If you use `eksctl` or an Amazon EKS AWS CloudFormation template to create your VPC after March 26, 2020, then the subnets are tagged appropriately when they're created\. For more information about the Amazon EKS AWS CloudFormation VPC templates, see [Creating a VPC for your Amazon EKS cluster](creating-a-vpc.md)\.
    + **Key** – `kubernetes.io/role/elb`
    + **Value** – `1`

  If the subnet role tags aren't explicitly added, the Kubernetes service controller examines the route table of your cluster VPC subnets to determine if the subnet is private or public\. We recommend that you don't rely on this behavior, and instead explicitly add the private or public role tags\. The AWS Load Balancer Controller doesn't examine route tables, and requires the private and public tags to be present for successful auto discovery\. 

**Considerations**
+ The configuration of your load balancer is controlled by annotations that are added to the manifest for your service\. Service annotations are different when using the AWS Load Balancer Controller than they are when using the AWS cloud provider load balancer controller\. Make sure to review the [annotations](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.7/guide/service/annotations/) for the AWS Load Balancer Controller before deploying services\.
+ When using the [Amazon VPC CNI plugin for Kubernetes](managing-vpc-cni.md), the AWS Load Balancer Controller can load balance to Amazon EC2 IP or instance targets and Fargate IP targets\. When using [Alternate compatible CNI plugins](alternate-cni-plugins.md), the controller can only load balance to instance targets\. For more information about Network Load Balancer target types, see [Target type](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-target-groups.html#target-type) in the User Guide for Network Load Balancers
+ If you want to add tags to the load balancer when or after it's created, add the following annotation in your service specification\. For more information, see [AWS Resource Tags](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.7/guide/service/annotations/#aws-resource-tags) in the AWS Load Balancer Controller documentation\.

  ```
  service.beta.kubernetes.io/aws-load-balancer-additional-resource-tags
  ```
+ You can assign [Elastic IP addresses](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html) to the Network Load Balancer by adding the following annotation\. Replace the *`example values`* with the `Allocation IDs` of your Elastic IP addresses\. The number of `Allocation IDs` must match the number of subnets that are used for the load balancer\. For more information, see the [https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.7/guide/service/annotations/#eip-allocations](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.7/guide/service/annotations/#eip-allocations) documentation\.

  ```
  service.beta.kubernetes.io/aws-load-balancer-eip-allocations: eipalloc-xxxxxxxxxxxxxxxxx,eipalloc-yyyyyyyyyyyyyyyyy
  ```
+ Amazon EKS adds one inbound rule to the node's security group for client traffic and one rule for each load balancer subnet in the VPC for health checks for each Network Load Balancer that you create\. Deployment of a service of type `LoadBalancer` can fail if Amazon EKS attempts to create rules that exceed the quota for the maximum number of rules allowed for a security group\. For more information, see [Security groups](https://docs.aws.amazon.com/vpc/latest/userguide/amazon-vpc-limits.html#vpc-limits-security-groups) in Amazon VPC quotas in the Amazon VPC User Guide\. Consider the following options to minimize the chances of exceeding the maximum number of rules for a security group:
  + Request an increase in your rules per security group quota\. For more information, see [Requesting a quota increase](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html) in the Service Quotas User Guide\.
  + Use IP targets, rather than instance targets\. With IP targets, you can share rules for the same target ports\. You can manually specify load balancer subnets with an annotation\. For more information, see [Annotations](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.7/guide/service/annotations/) on GitHub\.
  + Use an ingress, instead of a service of type `LoadBalancer`, to send traffic to your service\. The AWS Application Load Balancer requires fewer rules than Network Load Balancers\. You can share an ALB across multiple ingresses\. For more information, see [Application load balancing on Amazon EKS](alb-ingress.md)\. You can't share a Network Load Balancer across multiple services\.
  + Deploy your clusters to multiple accounts\.
+ If your Pods run on Windows in an Amazon EKS cluster, a single service with a load balancer can support up to 1024 back\-end Pods\. Each Pod has its own unique IP address\.
+ We recommend only creating new Network Load Balancers with the AWS Load Balancer Controller\. Attempting to replace existing Network Load Balancers created with the AWS cloud provider load balancer controller can result in multiple Network Load Balancers that might cause application downtime\.

## Create a network load balancer<a name="network-load-balancer"></a>

You can create a network load balancer with IP or instance targets\.

------
#### [ IP targets ]

You can use IP targets with Pods deployed to Amazon EC2 nodes or Fargate\. Your Kubernetes service must be created as type `LoadBalancer`\. For more information, see [Type LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer) in the Kubernetes documentation\. 

To create a load balancer that uses IP targets, add the following annotations to a service manifest and deploy your service\. The `external` value for `aws-load-balancer-type` is what causes the AWS Load Balancer Controller, rather than the AWS cloud provider load balancer controller, to create the Network Load Balancer\. You can view a [sample service manifest](#network-load-balancing-service-sample-manifest) with the annotations\.

```
service.beta.kubernetes.io/aws-load-balancer-type: "external"
service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: "ip"
```

**Note**  
If you're load balancing to `IPv6` Pods, add the following annotation\. You can only load balance over `IPv6` to IP targets, not instance targets\. Without this annotation, load balancing is over `IPv4`\.  

```
service.beta.kubernetes.io/aws-load-balancer-ip-address-type: dualstack
```

Network Load Balancers are created with the `internal` `aws-load-balancer-scheme`, by default\. You can launch Network Load Balancers in any subnet in your cluster's VPC, including subnets that weren't specified when you created your cluster\.

Kubernetes examines the route table for your subnets to identify whether they are public or private\. Public subnets have a route directly to the internet using an internet gateway, but private subnets do not\. 

If you want to create a Network Load Balancer in a public subnet to load balance to Amazon EC2 nodes \(Fargate can only be private\), specify `internet-facing` with the following annotation:

```
service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"
```

**Note**  
The `service.beta.kubernetes.io/aws-load-balancer-type: "nlb-ip"` annotation is still supported for backwards compatibility\. However, we recommend using the previous annotations for new load balancers instead of `service.beta.kubernetes.io/aws-load-balancer-type: "nlb-ip"`\.

**Important**  
Do not edit the annotations after creating your service\. If you need to modify it, delete the service object and create it again with the desired value for this annotation\.

------
#### [ Instance targets ]

The AWS cloud provider load balancer controller creates Network Load Balancers with instance targets only\. Version `2.2.0` and later of the AWS Load Balancer Controller also creates Network Load Balancers with instance targets\. We recommend using it, rather than the AWS cloud provider load balancer controller, to create new Network Load Balancers\. You can use Network Load Balancer instance targets with Pods deployed to Amazon EC2 nodes, but not to Fargate\. To load balance network traffic across Pods deployed to Fargate, you must use IP targets\. 

To deploy a Network Load Balancer to a private subnet, your service specification must have the following annotations\. You can view a [sample service manifest](#network-load-balancing-service-sample-manifest) with the annotations\. The `external` value for `aws-load-balancer-type` is what causes the AWS Load Balancer Controller, rather than the AWS cloud provider load balancer controller, to create the Network Load Balancer\.

```
service.beta.kubernetes.io/aws-load-balancer-type: "external"
service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: "instance"
```

Network Load Balancers are created with the `internal` `aws-load-balancer-scheme`, by default\. For internal Network Load Balancers, your Amazon EKS cluster must be configured to use at least one private subnet in your VPC\. Kubernetes examines the route table for your subnets to identify whether they are public or private\. Public subnets have a route directly to the internet using an internet gateway, but private subnets do not\. 

If you want to create an Network Load Balancer in a public subnet to load balance to Amazon EC2 nodes, specify `internet-facing` with the following annotation:

```
service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"
```

**Important**  
Do not edit the annotations after creating your service\. If you need to modify it, delete the service object and create it again with the desired value for this annotation\.

------

## \(Optional\) Deploy a sample application<a name="load-balancer-sample-application"></a>

**Prerequisites**
+ At least one public or private subnet in your cluster VPC\.
+ Have the AWS Load Balancer Controller deployed on your cluster\. For more information, see [What is the AWS Load Balancer Controller?](aws-load-balancer-controller.md)\. We recommend version `2.7.2` or later\.

**To deploy a sample application**

1. If you're deploying to Fargate, make sure you have an available private subnet in your VPC and create a Fargate profile\. If you're not deploying to Fargate, skip this step\. You can create the profile by running the following command or in the [AWS Management Console](fargate-profile.md#create-fargate-profile) using the same values for `name` and `namespace` that are in the command\. Replace the `example values` with your own\.

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
                image: public.ecr.aws/nginx/nginx:1.23
                ports:
                  - name: tcp
                    containerPort: 80
      ```

   1. Apply the manifest to the cluster\.

      ```
      kubectl apply -f sample-deployment.yaml
      ```

1. Create a service with an internet\-facing Network Load Balancer that load balances to IP targets\. 

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

1. <a name="nlb-sample-app-verify-deployment"></a>Verify that the service was deployed\.

   ```
   kubectl get svc nlb-sample-service -n nlb-sample-app
   ```

   An example output is as follows\.

   ```
   NAME            TYPE           CLUSTER-IP         EXTERNAL-IP                                                                    PORT(S)        AGE
   sample-service  LoadBalancer   10.100.240.137   k8s-nlbsampl-nlbsampl-xxxxxxxxxx-xxxxxxxxxxxxxxxx.elb.region-code.amazonaws.com  80:32400/TCP   16h
   ```
**Note**  
The values for `10.100.240.137` and `xxxxxxxxxx`\-*xxxxxxxxxxxxxxxx* will be different than the example output \(they will be unique to your load balancer\) and *us\-west\-2* may be different for you, depending on which AWS Region that your cluster is in\. 

1. Open the [Amazon EC2 AWS Management Console](https://console.aws.amazon.com/ec2)\. Select **Target Groups** \(under **Load Balancing**\) in the left navigation pane\. In the **Name** column, select the target group's name where the value in the **Load balancer** column matches a portion of the name in the `EXTERNAL-IP` column of the output in the previous step\. For example, you'd select the target group named `k8s-default-samplese-xxxxxxxxxx` if your output were the same as the previous output\. The **Target type** is `IP` because that was specified in the sample service manifest\.

1. Select the **Target group** and then select the **Targets** tab\. Under **Registered targets**, you should see three IP addresses of the three replicas deployed in a previous step\. Wait until the status of all targets is **healthy** before continuing\. It might take several minutes before all targets are `healthy`\. The targets might be in an `unhealthy` state before changing to a `healthy` state\.

1. Send traffic to the service replacing `xxxxxxxxxx-xxxxxxxxxxxxxxxx` and `us-west-2` with the values returned in the output for a [previous step](#nlb-sample-app-verify-deployment) for `EXTERNAL-IP`\. If you deployed to a private subnet, then you'll need to view the page from a device within your VPC, such as a bastion host\. For more information, see [Linux Bastion Hosts on AWS](https://aws.amazon.com/quickstart/architecture/linux-bastion/)\.

   ```
   curl k8s-default-samplese-xxxxxxxxxx-xxxxxxxxxxxxxxxx.elb.region-code.amazonaws.com
   ```

   An example output is as follows\.

   ```
   <!DOCTYPE html>
   <html>
   <head>
   <title>Welcome to nginx!</title>
   [...]
   ```

1. When you're finished with the sample deployment, service, and namespace, remove them\.

   ```
   kubectl delete namespace nlb-sample-app
   ```