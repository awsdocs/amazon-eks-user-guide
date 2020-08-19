# ALB Ingress Controller on Amazon EKS<a name="alb-ingress"></a>

The [AWS ALB Ingress Controller for Kubernetes](https://github.com/kubernetes-sigs/aws-alb-ingress-controller) is a controller that triggers the creation of an Application Load Balancer \(ALB\) and the necessary supporting AWS resources whenever an Ingress resource is created on the cluster with the `kubernetes.io/ingress.class: alb` annotation\. The Ingress resource configures the ALB to route HTTP or HTTPS traffic to different pods within the cluster\. The ALB Ingress Controller is supported for production workloads running on Amazon EKS clusters\.

To ensure that your ingress objects use the ALB Ingress Controller, add the following annotation to your Ingress specification\. For more information, see [Ingress specification](https://kubernetes-sigs.github.io/aws-alb-ingress-controller/guide/ingress/spec/) in the documentation\.

```
annotations:
    kubernetes.io/ingress.class: alb
```

The ALB Ingress controller supports the following traffic modes:
+ **Instance** – Registers nodes within your cluster as targets for the ALB\. Traffic reaching the ALB is routed to `NodePort` for your service and then proxied to your pods\. This is the default traffic mode\. You can also explicitly specify it with the `alb.ingress.kubernetes.io/target-type: instance` annotation\.
**Note**  
Your Kubernetes service must specify the `NodePort` type to use this traffic mode\.
+ **IP** – Registers pods as targets for the ALB\. Traffic reaching the ALB is directly routed to pods for your service\. You must specify the `alb.ingress.kubernetes.io/target-type: ip` annotation to use this traffic mode\.

For other available annotations supported by the ALB Ingress Controller, see [Ingress annotations](https://kubernetes-sigs.github.io/aws-alb-ingress-controller/guide/ingress/annotation/)\.

This topic shows you how to configure the ALB Ingress Controller to work with your Amazon EKS cluster\.

**Important**  
You cannot use the ALB Ingress Controller with [Private clusters](private-clusters.md)\.

**To deploy the ALB Ingress Controller to an Amazon EKS cluster**

1. Tag the subnets in your VPC that you want to use for your load balancers so that the ALB Ingress Controller knows that it can use them\. For more information, see [Subnet tagging requirement](network_reqs.md#vpc-subnet-tagging)\. If you deployed your cluster with `eksctl`, then the tags are already applied\.
   + All subnets in your VPC should be tagged accordingly so that Kubernetes can discover them\.     
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html)
   + Public subnets in your VPC should be tagged accordingly so that Kubernetes knows to use only those subnets for external load balancers\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html)
   + Private subnets must be tagged in the following way so that Kubernetes knows it can use the subnets for internal load balancers\. If you use an Amazon EKS AWS CloudFormation template to create your VPC after 03/26/2020, then the subnets created by the template are tagged when they're created\. For more information about the Amazon EKS AWS CloudFormation VPC templates, see [Creating a VPC for your Amazon EKS cluster](create-public-private-vpc.md)\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html)

1. Create an IAM OIDC provider and associate it with your cluster\. If you don't have `eksctl` version 0\.26\.0\-rc\.1 or later installed, complete the instructions in [Installing or upgrading `eksctl`](eksctl.md#installing-eksctl) to install or upgrade it\. You can check your installed version with `eksctl version`\.

   ```
   eksctl utils associate-iam-oidc-provider \
       --region region-code \
       --cluster prod \
       --approve
   ```

1. Download an IAM policy for the ALB Ingress Controller pod that allows it to make calls to AWS APIs on your behalf\. You can view the [policy document](https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.8/docs/examples/iam-policy.json) on GitHub\.

   ```
   curl -o iam-policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.8/docs/examples/iam-policy.json
   ```

1. Create an IAM policy called `ALBIngressControllerIAMPolicy` using the policy downloaded in the previous step\. 

   ```
   aws iam create-policy \
       --policy-name ALBIngressControllerIAMPolicy \
       --policy-document file://iam-policy.json
   ```

   Take note of the policy ARN that is returned\.

1. Create a Kubernetes service account named `alb-ingress-controller` in the `kube-system` namespace, a cluster role, and a cluster role binding for the ALB Ingress Controller to use with the following command\. If you don't have `kubectl` installed, complete the instructions in [Installing `kubectl`](install-kubectl.md) to install it\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.8/docs/examples/rbac-role.yaml
   ```

1. Create an IAM role for the ALB Ingress Controller and attach the role to the service account created in the previous step\. If you didn't create your cluster with `eksctl`, then use the instructions on the AWS Management Console or AWS CLI tabs\.

------
#### [ eksctl ]

   The command that follows only works for clusters that were created with `eksctl`\. 

   ```
   eksctl create iamserviceaccount \
       --region region-code \
       --name alb-ingress-controller \
       --namespace kube-system \
       --cluster prod \
       --attach-policy-arn arn:aws:iam::111122223333:policy/ALBIngressControllerIAMPolicy \
       --override-existing-serviceaccounts \
       --approve
   ```

------
#### [ AWS Management Console ]

   1. Using the instructions on the AWS Management Console tab in [Create an IAM role](create-service-account-iam-policy-and-role.md#create-service-account-iam-role), create an IAM role named `eks-alb-ingress-controller` and attach the `ALBIngressControllerIAMPolicy` IAM policy that you created in a previous step to it\. Note the Amazon Resource Name \(ARN\) of the role, once you've created it\.

   1. Annotate the Kubernetes service account with the ARN of the role that you created with the following command\.

      ```
      kubectl annotate serviceaccount -n kube-system alb-ingress-controller \
      eks.amazonaws.com/role-arn=arn:aws:iam::111122223333:role/eks-alb-ingress-controller
      ```

------
#### [ AWS CLI ]

   1. Using the instructions on the AWS CLI tab in [Create an IAM role](create-service-account-iam-policy-and-role.md#create-service-account-iam-role), create an IAM role named `eks-alb-ingress-controller` and attach the `ALBIngressControllerIAMPolicy` IAM policy that you created in a previous step to it\. Note the Amazon Resource Name \(ARN\) of the role, once you've created it\.

   1. Annotate the Kubernetes service account with the ARN of the role that you created with the following command\.

      ```
      kubectl annotate serviceaccount -n kube-system alb-ingress-controller \
      eks.amazonaws.com/role-arn=arn:aws:iam::111122223333:role/eks-alb-ingress-controller
      ```

------

1. Deploy the ALB Ingress Controller with the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.8/docs/examples/alb-ingress-controller.yaml
   ```

1. Open the ALB Ingress Controller deployment manifest for editing with the following command\.

   ```
   kubectl edit deployment.apps/alb-ingress-controller -n kube-system
   ```

1. Add a line for the cluster name after the `--ingress-class=alb` line\. If you're running the ALB Ingress Controller on Fargate, then you must also add the lines for the VPC ID, and AWS Region name of your cluster\. Once you've added the appropriate lines, save and close the file\.

   ```
       spec:
         containers:
         - args:
           - --ingress-class=alb
           - --cluster-name=prod
           - --aws-vpc-id=vpc-03468a8157edca5bd
           - --aws-region=region-code
   ```

1. Confirm that the ALB Ingress Controller is running with the following command\.

   ```
   kubectl get pods -n kube-system
   ```

   Expected output:

   ```
   NAME                                      READY   STATUS    RESTARTS   AGE
   alb-ingress-controller-55b5bbcb5b-bc8q9   1/1     Running   0          56s
   ```

**To deploy a sample application**

1. Deploy the game [2048](https://play2048.co/) as a sample application to verify that the ALB Ingress Controller creates an Application Load Balancer as a result of the Ingress object\. You can run the sample application on a cluster that has Amazon EC2 nodes only, one or more Fargate pods, or a combination of the two\. If your cluster has Amazon EC2 nodes and no Fargate pods, then select the **Amazon EC2 nodes only** tab\. If your cluster has any existing Fargate pods, or you want to deploy the application to new Fargate pods, then select the **Fargate** tab\. For more information about Fargate pods, see [Getting started with AWS Fargate using Amazon EKS](fargate-getting-started.md) \.

------
#### [ Amazon EC2 nodes only ]

   Deploy the application with the following commands\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.8/docs/examples/2048/2048-namespace.yaml
   kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.8/docs/examples/2048/2048-deployment.yaml
   kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.8/docs/examples/2048/2048-service.yaml
   kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.8/docs/examples/2048/2048-ingress.yaml
   ```

------
#### [ Fargate ]

   Ensure that the cluster that you want to use Fargate in is in the list of [supported Regions](fargate.md)\.

   1. Create a Fargate profile that includes the sample application's namespace with the following command\. Replace the *example\-values* with your own values\.
**Note**  
The command that follows only works for clusters that were created with `eksctl`\. If you didn't create your cluster with `eksctl`, then you can create the profile with the the [AWS Management Console](fargate-profile.md#create-fargate-profile), using the same values for `name` and `namespace` that are in the command below\.

      ```
      eksctl create fargateprofile --cluster prod --region region-code --name alb-sample-app --namespace 2048-game
      ```

   1. Download and apply the manifest files to create the Kubernetes namespace, deployment, and service with the following commands\.

      ```
      kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.8/docs/examples/2048/2048-namespace.yaml
      kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.8/docs/examples/2048/2048-deployment.yaml
      kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.8/docs/examples/2048/2048-service.yaml
      ```

   1. Download the ingress manifest file with the following command\.

      ```
      curl -o 2048-ingress.yaml https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.8/docs/examples/2048/2048-ingress.yaml
      ```

   1. Edit the `2048-ingress.yaml` file\. Under the existing `alb.ingress.kubernetes.io/scheme: internet-facing` line , add the line `alb.ingress.kubernetes.io/target-type: ip`\.

   1. Apply the ingress manifest file with the following command\.

      ```
      kubectl apply -f 2048-ingress.yaml
      ```

------

1. After a few minutes, verify that the Ingress resource was created with the following command\.

   ```
   kubectl get ingress/2048-ingress -n 2048-game
   ```

   Output:

   ```
   NAME           HOSTS   ADDRESS                                                                 PORTS      AGE
   2048-ingress   *       example-2048game-2048ingr-6fa0-352729433.region-code.elb.amazonaws.com   80      24h
   ```
**Note**  
If your Ingress has not been created after several minutes, run the following command to view the Ingress controller logs\. These logs may contain error messages that can help you diagnose any issues with your deployment\.  

   ```
   kubectl logs -n kube-system   deployment.apps/alb-ingress-controller
   ```

1. Open a browser and navigate to the `ADDRESS` URL from the previous command output to see the sample application\.  
![\[2048 sample application\]](http://docs.aws.amazon.com/eks/latest/userguide/images/2048.png)

1. When you finish experimenting with your sample application, delete it with the following commands\.

   ```
   kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.8/docs/examples/2048/2048-ingress.yaml
   kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.8/docs/examples/2048/2048-service.yaml
   kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.8/docs/examples/2048/2048-deployment.yaml
   kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.8/docs/examples/2048/2048-namespace.yaml
   ```