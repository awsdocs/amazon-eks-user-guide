# Application load balancing on Amazon EKS<a name="alb-ingress"></a>

You can load balance application traffic across pods using the AWS Application Load Balancer \(ALB\)\. To learn more, see [What is an Application Load Balancer?](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html) in the *Application Load Balancers User Guide*\. You can share an ALB across multiple applications in your Kubernetes cluster using Ingress groups\. In the past, you needed to use a separate ALB for each application\. The controller automatically provisions AWS ALBs in response to Kubernetes Ingress objects\. ALBs can be used with pods deployed to nodes or to AWS Fargate\. You can deploy an ALB to public or private subnets\.

Application traffic is balanced at L7 of the OSI model\. To load balance network traffic at L4, see [Network load balancing on Amazon EKS](load-balancing.md)\. To learn more about the differences between the two types of load balancing, see [Elastic Load Balancing features](https://aws.amazon.com/elasticloadbalancing/features/) on the AWS web site\. 

**Prerequisites**

Before you can load balance application traffic to an application, you must meet the following requirements\.
+ Have an existing 1\.15 or later cluster\. If you don't have an existing cluster, see [Getting started with Amazon EKS](getting-started.md)\.
+ Public subnets must be tagged as follows so that Kubernetes knows to use only those subnets for external load balancers instead of choosing a public subnet in each Availability Zone \(in lexicographical order by subnet ID\)\. If you use `eksctl` or an Amazon EKS AWS CloudFormation template to create your VPC after March 26, 2020, then the subnets are tagged appropriately when they're created\. For more information about the Amazon EKS AWS CloudFormation VPC templates, see [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md)\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html)
+ Private subnets must be tagged as follows so that Kubernetes knows it can use the subnets for internal load balancers\. If you use `eksctl` or an Amazon EKS AWS CloudFormation template to create your VPC after March 26, 2020, then the subnets are tagged appropriately when they're created\. For more information about the Amazon EKS AWS CloudFormation VPC templates, see [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md)\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html)

The [AWS load balancer controller](https://github.com/kubernetes-sigs/aws-load-balancer-controller) \(formerly named *AWS ALB Ingress Controller*\) creates ALBs and the necessary supporting AWS resources whenever a Kubernetes Ingress resource is created on the cluster with the `kubernetes.io/ingress.class: alb` annotation\. The Ingress resource configures the ALB to route HTTP or HTTPS traffic to different pods within the cluster\. To ensure that your Ingress objects use the AWS load balancer controller, add the following annotation to your Kubernetes Ingress specification\. For more information, see [Ingress specification](https://kubernetes-sigs.github.io/aws-load-balancer-controller/guide/ingress/spec/) on GitHub\.

```
annotations:
    kubernetes.io/ingress.class: alb
```

The AWS load balancer controller supports the following traffic modes:
+ **Instance** – Registers nodes within your cluster as targets for the ALB\. Traffic reaching the ALB is routed to `NodePort` for your service and then proxied to your pods\. This is the default traffic mode\. You can also explicitly specify it with the `alb.ingress.kubernetes.io/target-type: instance` annotation\.
**Note**  
Your Kubernetes service must specify the `NodePort` type to use this traffic mode\.
+ **IP** – Registers pods as targets for the ALB\. Traffic reaching the ALB is directly routed to pods for your service\. You must specify the `alb.ingress.kubernetes.io/target-type: ip` annotation to use this traffic mode\.

To tag ALBs created by the controller, add the following annotation to the controller: `alb.ingress.kubernetes.io/tags`\. For a list of all available annotations supported by the AWS load balancer controller, see [Ingress annotations](https://kubernetes-sigs.github.io/aws-load-balancer-controller/guide/ingress/annotations/) on GitHub\.

This topic shows you how to configure the AWS load balancer controller to work with your Amazon EKS cluster\.<a name="deploy-lb-controller2"></a>

**To deploy the AWS load balancer controller to an Amazon EKS cluster**

1. Create an IAM OIDC provider and associate it with your cluster\. Replace the `<example values>` \(including `<>`\) with your own\.

   ```
   eksctl utils associate-iam-oidc-provider \
       --region <region-code> \
       --cluster <my-cluster> \
       --approve
   ```

1. Download an IAM policy for the AWS load balancer controller that allows it to make calls to AWS APIs on your behalf\. You can view the [policy document](https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2_ga/docs/install/iam_policy.json) on GitHub\. Use the command that corresponds to the Region that your cluster is in\.
   + All Regions other than China Regions\.

     ```
     curl -o iam-policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy.json
     ```
   + Beijing and Ningxia China Regions\.

     ```
     curl -o iam-policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy_cn.json
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

1. If you currently have the AWS ALB Ingress Controller for Kubernetes installed, uninstall it\. The AWS load balancer controller replaces the functionality of the AWS ALB Ingress Controller for Kubernetes\.

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

      1. Download the IAM policy\. You can also [view the policy](https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy_v1_to_v2_additional.json)\.

         ```
         curl -o iam_policy_v1_to_v2_additional.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy_v1_to_v2_additional.json
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
           --policy-arn= arn:aws:iam::111122223333:policy/AWSLoadBalancerControllerAdditionalIAMPolicy
         ```

1. Install the AWS load balancer controller using Helm\. If you'd prefer to install the controller manually, then skip to the next step\.

   1. Install the `TargetGroupBinding` custom resource definitions\.

      ```
      kubectl apply -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller//crds?ref=master"
      ```

   1. Add the `eks-charts` repository\.

      ```
      helm repo add eks https://aws.github.io/eks-charts
      ```

   1. Install the AWS load balancer controller using the command that corresponds to the Region that your cluster is in\.
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

      1. Download the controller specification\. For more information about the controller, see the [documentation](https://github.com/kubernetes-sigs/aws-alb-ingress-controller/) on GitHub\.

         ```
         curl -o v2_0_0_full.yaml https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/v2_0_0_full.yaml
         ```

      1. Edit the saved yaml file\. In the `Deployment` `spec` section set the `--cluster-name` value to your Amazon EKS cluster name\. It is recommended that you delete the `ServiceAccount` from the yaml specification\. Doing so will preserve the `eksctl`\-created iamserviceaccount if you delete the installation\.

      1. Apply the file\.

         ```
         kubectl apply -f v2_0_0_full.yaml
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
<a name="alb-ingress-groups"></a>
**To share an ALB across multiple ingress resources using `IngressGroups`**  
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

1. If you're not deploying to Fargate, skip this step\. Create a Fargate profile\. The command that follows only works for clusters that were created with `eksctl`\. If you didn't create your cluster with `eksctl`, then you can create the profile with the the [AWS Management Console](fargate-profile.md#create-fargate-profile), using the same values for `name` and `namespace` that are in the command below\.

   ```
   eksctl create fargateprofile --cluster <my-cluster> --region <region-code> --name <alb-sample-app> --namespace game-2048
   ```

1. Deploy the game [2048](https://play2048.co/) as a sample application to verify that the AWS load balancer controller creates an AWS ALB as a result of the Ingress object\. 

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/examples/2048/2048_full.yaml
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
If your Ingress has not been created after several minutes, run the following command to view the load balancer controller logs\. These logs may contain error messages that can help you diagnose any issues with your deployment\.  

   ```
   kubectl logs -n kube-system   deployment.apps/aws-load-balancer-controller
   ```

1. Open a browser and navigate to the `ADDRESS` URL from the previous command output to see the sample application\.  
![\[2048 sample application\]](http://docs.aws.amazon.com/eks/latest/userguide/images/2048.png)

1. When you finish experimenting with your sample application, delete it with the following commands\.

   ```
   kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/examples/2048/2048_full.yaml
   ```