# Network load balancing on Amazon EKS<a name="load-balancing"></a>

You can load balance network traffic across pods using the AWS Network Load Balancer \(NLB\) or Classic Load Balancer \(CLB\)\. To learn more about the differences between the two types, see [Elastic Load Balancing features](https://aws.amazon.com/elasticloadbalancing/features/) on the AWS web site\. You can deploy an AWS load balancer to a public or private subnet\.

Network traffic is load balanced at L4 of the OSI model\. To load balance application traffic at L7, see [Application load balancing on Amazon EKS](alb-ingress.md)\. To learn more about the differences between the two types of load balancing, see [Elastic Load Balancing features](https://aws.amazon.com/elasticloadbalancing/features/) on the AWS web site\.

In Amazon EKS, you can load balance network traffic to an NLB \(*instance* or *IP* targets\) or a CLB \(*instance* target only\)\. For more information about NLB target types, see [Target type](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-target-groups.html#target-type) in the User Guide for Network Load Balancers\. When you load balance network traffic to instance targets, the Kubernetes in\-tree load balancing controller creates the NLB or CLB\. To load balance network traffic to IP target types, the AWS Load Balancer Controller creates an NLB\. For more information, see [AWS Load Balancer Controller](https://github.com/kubernetes-sigs/aws-load-balancer-controller) on GitHub\. The in\-tree load balancing controller is included in Kubernetes\. To use the AWS Load Balancer Controller, you must deploy it to a 1\.15 or later cluster\.

**Prerequisites**

Before you can load balance network traffic to an application, you must meet the following requirements\.
+ Have an existing cluster\. If you don't have an existing cluster, see [Getting started with Amazon EKS](getting-started.md)\.
+ Public subnets must be tagged as follows so that Kubernetes knows to use only those subnets for external load balancers instead of choosing a public subnet in each Availability Zone \(in lexicographical order by subnet ID\)\. If you use `eksctl` or an Amazon EKS AWS CloudFormation template to create your VPC after March 26, 2020, then the subnets are tagged appropriately when they're created\. For more information about the Amazon EKS AWS CloudFormation VPC templates, see [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md)\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/load-balancing.html)
+ Private subnets must be tagged as follows so that Kubernetes knows it can use the subnets for internal load balancers\. If you use `eksctl` or an Amazon EKS AWS CloudFormation template to create your VPC after March 26, 2020, then the subnets are tagged appropriately when they're created\. For more information about the Amazon EKS AWS CloudFormation VPC templates, see [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md)\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/load-balancing.html)

**Considerations**
+ Use of the UDP protocol is supported with the load balancer on Amazon EKS version 1\.15 and later with the following minimum or later platform versions\. For more information, see [Amazon EKS platform versions](platform-versions.md)\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/load-balancing.html)
+ You can only use NLB *IP* targets with the [Amazon EKS VPC CNI plugin](pod-networking.md)\. You can use NLB *instance* targets with the Amazon EKS VPC CNI plugin, or [alternate compatible CNI plugins](alternate-cni-plugins.md)\.
+ You can only use *IP* targets with NLB\. You can't use IP targets with CLBs\.
+ You can only use NLB *IP* targets with clusters running at least Amazon EKS version 1\.18\. To upgrade your current version, see [Updating a Cluster](update-cluster.md)\.
+ The configuration of your load balancer is controlled by annotations that are added to the manifest for your service\. If you want to add tags to the load balancer when \(or after\) it's created, add the following annotation in your service specification\. For more information, see [Other ELB annotations](https://kubernetes.io/docs/concepts/services-networking/service/#other-elb-annotations) in the Kubernetes documentation\.

  ```
  service.beta.kubernetes.io/aws-load-balancer-additional-resource-tags
  ```
+ If you're using Amazon EKS 1\.16 or later, you can assign [elastic IP addresses](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html) to the Network Load Balancer by adding the following annotation\. Replace the `<example-values>` \(including `<>`\) with the Allocation IDs of your elastic IP addresses\. The number of Allocation IDs must match the number of subnets used for the load balancer\.

  ```
  service.beta.kubernetes.io/aws-load-balancer-eip-allocations: eipalloc-<xxxxxxxxxxxxxxxxx>,eipalloc-<yyyyyyyyyyyyyyyyy>
  ```

## Load balancer – Instance targets<a name="load-balancer-instance"></a>

NLB or CLBs with instance targets are created by the Kubernetes in\-tree load balancing controller\. The in\-tree controller is included with Kubernetes, so you don't need to deploy it to your cluster\. You can use NLB instance targets with pods deployed to nodes, but not to Fargate\. To load balance network traffic across pods deployed to Fargate, you must use [IP targets](#load-balancer-ip)\. By default, external \(public\) Classic Load Balancers are created when you deploy a Kubernetes service of type `LoadBalancer`\. To deploy a Network Load Balancer instead, apply the following annotation to your service:

```
service.beta.kubernetes.io/aws-load-balancer-type: nlb
```

**Important**  
Do not edit this annotation after creating your service\. If you need to modify it, delete the service object and create it again with the desired value for this annotation\.

To deploy a load balancer to a private subnet, your service specification must have the following annotation:

```
service.beta.kubernetes.io/aws-load-balancer-internal: "true"
```

For internal load balancers, your Amazon EKS cluster must be configured to use at least one private subnet in your VPC\. Kubernetes examines the route table for your subnets to identify whether they are public or private\. Public subnets have a route directly to the internet using an internet gateway, but private subnets do not\. 

For an example service manifest that specifies a load balancer, see [Type LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer) in the Kubernetes documentation\. For more information about using Network Load Balancer with Kubernetes, see [Network Load Balancer support on AWS](https://kubernetes.io/docs/concepts/services-networking/service/#aws-nlb-support) in the Kubernetes documentation\.

## Load balancer – IP targets<a name="load-balancer-ip"></a>

NLBs with IP targets are created by the AWS Load Balancer Controller \(you cannot use CLBs with instance targets\)\. To use the controller, you must deploy it to your cluster\. You can use NLB IP targets with pods deployed to Amazon EC2 nodes or Fargate\. For more information about the controller, see [AWS Load Balancer Controller](https://github.com/kubernetes-sigs/aws-load-balancer-controller) on GitHub\. The controller creates and manages the NLB\. Your Kubernetes service must be created as type `LoadBalancer`\. For more information, see [Type LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer) in the Kubernetes documentation\.

To create a load balancer that uses IP targets, add the following annotation to a service manifest and deploy your service\. 

```
service.beta.kubernetes.io/aws-load-balancer-type: "nlb-ip"
```

**Important**  
Do not edit this annotation after creating your service\. If you need to modify it, delete the service object and create it again with the desired value for this annotation\. You can only use NLB *IP* targets with clusters running at least Amazon EKS version 1\.18\. To upgrade your current version, see [Updating a Cluster](update-cluster.md)\.<a name="deploy-lb-controller"></a>

**To deploy the AWS Load Balancer Controller to an Amazon EKS cluster**

1. Create an IAM OIDC provider and associate it with your cluster\. Replace the `<example values>` \(including `<>`\) with your own\.

   ```
   eksctl utils associate-iam-oidc-provider \
       --region <region-code> \
       --cluster <my-cluster> \
       --approve
   ```

1. Download an IAM policy for the AWS Load Balancer Controller that allows it to make calls to AWS APIs on your behalf\. You can view the [policy document](https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.1.0/docs/install/iam_policy.json) on GitHub\. Use the command that corresponds to the Region that your cluster is in\.
   + All Regions other than China Regions\.

     ```
     curl -o iam-policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.1.0/docs/install/iam_policy.json
     ```
   + Beijing and Ningxia China Regions\.

     ```
     curl -o iam-policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.1.0/docs/install/iam_policy_cn.json
     ```

1. Create an IAM policy using the policy downloaded in the previous step\. 

   ```
   aws iam create-policy \
       --policy-name <AWSLoadBalancerControllerIAMPolicy> \
       --policy-document file://iam-policy.json
   ```

   Take note of the policy ARN that is returned\.

1. Create an IAM role and Kubernetes service account named `aws-load-balancer-controller` in the `kube-system` namespace, a cluster role, and a cluster role binding for the load balancer controller to use with the following command\.

   ```
   eksctl create iamserviceaccount \
     --cluster=<my-cluster> \
     --namespace=kube-system \
     --name=aws-load-balancer-controller \
     --attach-policy-arn=arn:aws:iam::<AWS_ACCOUNT_ID>:policy/<AWSLoadBalancerControllerIAMPolicy> \
     --override-existing-serviceaccounts \
     --approve
   ```

1. If you currently have the AWS ALB Ingress Controller for Kubernetes installed, uninstall it\. The AWS Load Balancer Controller replaces the functionality of the AWS ALB Ingress Controller for Kubernetes\.

   1. Check to see if the controller is currently installed\.

      ```
      kubectl get deployment -n kube-system alb-ingress-controller
      ```

      Output \(if it is installed\)\. Skip to step 5\.2\.

      ```
      NAME                   READY UP-TO-DATE AVAILABLE AGE
      alb-ingress-controller 1/1   1          1         122d
      ```

      Output \(if it isn't installed\)\. If it isn't installed, skip to step 6\.

      ```
      Error from server (NotFound): deployments.apps "alb-ingress-controller" not found
      ```

   1. If the controller is installed, enter the following commands to remove it\.

      ```
      kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.8/docs/examples/alb-ingress-controller.yaml
      kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.8/docs/examples/rbac-role.yaml
      ```

   1. If you removed the AWS ALB Ingress Controller for Kubernetes, add the following IAM policy to the IAM account created in step 4\. The policy allows the AWS load balancer access to the resources that were created by the ALB Ingress Controller for Kubernetes\.

      1. Download the IAM policy\. You can also [view the policy](https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.1.0/docs/install/iam_policy_v1_to_v2_additional.json)\.

         ```
         curl -o iam_policy_v1_to_v2_additional.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.1.0/docs/install/iam_policy_v1_to_v2_additional.json
         ```

      1. Create the IAM policy and note the ARN returned\.

         ```
         aws iam create-policy \
           --policy-name <AWSLoadBalancerControllerAdditionalIAMPolicy> \
           --policy-document file://iam_policy_v1_to_v2_additional.json
         ```

      1. Open the [AWS CloudFormation console](https://console.aws.amazon.com//cloudformation) and select the **eksctl\-<your\-cluster\-name>\-addon\-iamserviceaccount\-kube\-system\-aws\-load\-balancer\-controller** stack that was deployed in step 4 by `eksctl`\. Select the **Resources** tab, and then select the link in the **Physical ID** column\. Note the value for** Role ARN** for use in the next step\.

      1. Attach the IAM policy to the IAM role\.

         ```
         aws iam attach-role-policy \
           --role-name eksctl-<your-cluster-name>-addon-iamserviceaccount-kube-sys-Role1-<1DZ86GS3UBRGN>\
           --policy-arn arn:aws:iam::111122223333:policy/AWSLoadBalancerControllerAdditionalIAMPolicy
         ```

1. Install the AWS Load Balancer Controller using Helm\. If you'd prefer to install the controller manually, then skip to the next step\.

   1. Install the `TargetGroupBinding` custom resource definitions\.

      ```
      kubectl apply -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller//crds?ref=master"
      ```

   1. Add the `eks-charts` repository\.

      ```
      helm repo add eks https://aws.github.io/eks-charts
      ```

   1. Install the AWS Load Balancer Controller using the command that corresponds to the Region that your cluster is in\.
      + All Regions other than China Regions\.

        ```
        helm upgrade -i aws-load-balancer-controller eks/aws-load-balancer-controller \
          --set clusterName=<cluster-name> \
          --set serviceAccount.create=false \
          --set serviceAccount.name=aws-load-balancer-controller \
          -n kube-system
        ```
      + Beijing and Ningxia China Regions\.

        ```
        helm upgrade -i aws-load-balancer-controller eks/aws-load-balancer-controller \
          --set clusterName=<cluster-name> \
          --set serviceAccount.create=false \
          --set serviceAccount.name=aws-load-balancer-controller \
          --set image.repository=918309763551.dkr.ecr.cn-north-1.amazonaws.com.cn/amazon/aws-load-balancer-controller \
          -n kube-system
        ```
**Important**  
The deployed chart does not receive security updates automatically\. You need to manually upgrade to a newer chart when it becomes available\.

1. Install the controller manually\. If you already installed the controller using the previous step, then don't complete this step\.

   1. Install `cert-manager` to inject certificate configuration into the webhooks\.
      + Install on Kubernetes `1.16` or later\.

        ```
        kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/v1.0.2/cert-manager.yaml
        ```
      + Install on Kubernetes `1.15` or earlier\.

        ```
         kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/v1.0.2/cert-manager-legacy.yaml
        ```

   1. Install the controller\. 

      1. Download the controller specification\. For more information about the controller, see the [documentation](https://kubernetes-sigs.github.io/aws-load-balancer-controller/) on GitHub\.

         ```
         curl -o v2_1_0_full.yaml https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.1.0/docs/install/v2_1_0_full.yaml
         ```

      1. Edit the saved yaml file\. In the `Deployment` `spec` section set the `--cluster-name` value to your Amazon EKS cluster name\. It is recommended that you delete the `ServiceAccount` from the yaml specification\. Doing so will preserve the `eksctl`\-created iamserviceaccount if you delete the installation\.

      1. Apply the file\.

         ```
         kubectl apply -f v2_1_0_full.yaml
         ```

1. Verify that the controller is installed\.

   ```
   kubectl get deployment -n kube-system aws-load-balancer-controller
   ```

   Output

   ```
   NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
   aws-load-balancer-controller   1/1     1            1           84s
   ```

**\(Optional\) To deploy a sample application**

1. Deploy a sample application\.

   1. Save the following contents to a `yaml` file on your computer\.

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
                image: public.ecr.aws/z9d2n7e1/nginx:1.19.5
                ports:
                  - name: http
                    containerPort: 80
      ```

   1. Apply the manifest to the cluster\.

      ```
      kubectl apply -f <file-name-you-specified>.yaml
      ```

1. Create a service of type `LoadBalancer` with an annotation to create an NLB with IP targets\.

   1. Save the following contents to a `yaml` file on your computer\.

      ```
      apiVersion: v1
      kind: Service
      metadata:
        name: sample-service
        annotations:
          service.beta.kubernetes.io/aws-load-balancer-type: nlb-ip
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
      kubectl apply -f <file-name-you-specified>.yaml
      ```

1. Verify that the service was deployed\.

   ```
   kubectl get svc sample-service
   ```

   Output

   ```
   NAME            TYPE           CLUSTER-IP       EXTERNAL-IP                                                                    PORT(S)        AGE
   sample-service  LoadBalancer   10.100.240.137   k8s-default-samplese-xxxxxxxxxx-xxxxxxxxxxxxxxxx.elb.us-west-2.amazonaws.com   80:32400/TCP   16h
   ```

1. Open the [Amazon EC2 AWS Management Console](https://console.aws.amazon.com/ec2)\. Select **Target Groups** \(under **Load Balancing**\) in the left panel\. Find the **Target group** that was created in a previous step\. The name in the **Load balancer** column will be a part of the name returned in the previous step\. For example, `k8s-default-nlbipsvc-xxxxxxxxxx`\. The **Target type** is `IP`\.

1. Select the **Target group** to view its details\. Under **Registered targets**, you should see three IP addresses of the three replicas deployed in a previous step\. Wait until all the status of all targets is** healthy** before continuing\. It may take several minutes before all targets are `healthy`\. The targets may have an `unhealthy` state before changing to `healthy`\.

1. Send traffic to the service replacing the example value with the value returned in a previous step for the `EXTERNAL-IP`\.

   ```
   curl <k8s-default-samplese-xxxxxxxxxx-xxxxxxxxxxxxxxxx.elb.us-west-2.amazonaws.com>
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