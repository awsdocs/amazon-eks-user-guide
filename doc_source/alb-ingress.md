# ALB Ingress Controller on Amazon EKS<a name="alb-ingress"></a>

The [AWS ALB Ingress Controller for Kubernetes](https://github.com/kubernetes-sigs/aws-alb-ingress-controller) is a controller that triggers the creation of an Application Load Balancer and the necessary supporting AWS resources whenever an Ingress resource is created on the cluster with the `kubernetes.io/ingress.class: alb` annotation\. The Ingress resource uses the ALB to route HTTP or HTTPS traffic to different endpoints within the cluster\. The ALB Ingress Controller is supported for production workloads running on Amazon EKS clusters\.

To ensure that your Ingress objects use the ALB Ingress Controller, add the following annotation to your Ingress specification\. For more information, see [Ingress specification](https://kubernetes-sigs.github.io/aws-alb-ingress-controller/guide/ingress/spec/) in the documentation\.

```
annotations:
    kubernetes.io/ingress.class: alb
```

Your Kubernetes service can be of the following types:
+ NodePort
+ ClusterIP \(with the `alb.ingress.kubernetes.io/target-type: ip` annotation to put the service into IP mode\)
+ LoadBalancer \(this creates two load balancers; one for the service, and one for the ingress\)

For other available annotations supported by the ALB Ingress Controller, see [Ingress annotations](https://kubernetes-sigs.github.io/aws-alb-ingress-controller/guide/ingress/annotation/)\.

This topic show you how to configure the ALB Ingress Controller to work with your Amazon EKS cluster\.

**To deploy the ALB Ingress Controller to an Amazon EKS cluster**

1. Tag the subnets in your VPC that you want to use for your load balancers so that the ALB Ingress Controller knows that it can use them\. For more information, see [Subnet Tagging Requirement](network_reqs.md#vpc-subnet-tagging)\.
   + All subnets in your VPC should be tagged accordingly so that Kubernetes can discover them\.     
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html)
   + Public subnets in your VPC should be tagged accordingly so that Kubernetes knows to use only those subnets for external load balancers\.    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html)
   + Private subnets in your VPC should be tagged accordingly so that Kubernetes knows that it can use them for internal load balancers:    
[\[See the AWS documentation website for more details\]](http://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html)

1. Create an IAM policy called `ALBIngressControllerIAMPolicy` for your worker node instance profile that allows the ALB Ingress Controller to make calls to AWS APIs on your behalf\. Use the following AWS CLI commands to create the IAM policy in your AWS account\. You can view the policy document [on GitHub](https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.2/docs/examples/iam-policy.json)\.

   1. Download the policy document from GitHub\.

      ```
      curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.4/docs/examples/iam-policy.json
      ```

   1. Create the policy\.

      ```
      aws iam create-policy \
      --policy-name ALBIngressControllerIAMPolicy \
      --policy-document file://iam-policy.json
      ```

   Take note of the policy ARN that is returned\.

1. Get the IAM role name for your worker nodes\. Use the following command to print the `aws-auth` configmap\.

   ```
   kubectl -n kube-system describe configmap aws-auth
   ```

   Output:

   ```
   Name:         aws-auth
   Namespace:    kube-system
   Labels:       <none>
   Annotations:  <none>
   
   Data
   ====
   mapRoles:
   ----
   - groups:
     - system:bootstrappers
     - system:nodes
     rolearn: arn:aws:iam::111122223333:role/eksctl-alb-nodegroup-ng-b1f603c5-NodeInstanceRole-GKNS581EASPU
     username: system:node:{{EC2PrivateDNSName}}
   
   Events:  <none>
   ```

   Record the role name for any `rolearn` values that have the `system:nodes` group assigned to them\. In the above example output, the role name is *eksctl\-alb\-nodegroup\-ng\-b1f603c5\-NodeInstanceRole\-GKNS581EASPU*\. You should have one value for each node group in your cluster\.

1. Attach the new `ALBIngressControllerIAMPolicy` IAM policy to each of the worker node IAM roles you identified earlier with the following command, substituting the red text with your own AWS account number and worker node IAM role name\.

   ```
   aws iam attach-role-policy \
   --policy-arn arn:aws:iam::111122223333:policy/ALBIngressControllerIAMPolicy \
   --role-name eksctl-alb-nodegroup-ng-b1f603c5-NodeInstanceRole-GKNS581EASPU
   ```

1. Create a service account, cluster role, and cluster role binding for the ALB Ingress Controller to use with the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.4/docs/examples/rbac-role.yaml
   ```

1. Deploy the ALB Ingress Controller with the following command\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.4/docs/examples/alb-ingress-controller.yaml
   ```
**Note**  
If you are launching the controller on AWS Fargate, then see the [Kubernetes ALB 1\.14 release notes](https://github.com/kubernetes-sigs/aws-alb-ingress-controller/releases/tag/v1.1.4) for additional requirements

1. Open the ALB Ingress Controller deployment manifest for editing with the following command\.

   ```
   kubectl edit deployment.apps/alb-ingress-controller -n kube-system
   ```

1. Add the cluster name, VPC ID, and AWS Region name for your cluster after the `--ingress-class=alb` line and then save and close the file\.

   ```
       spec:
         containers:
         - args:
           - --ingress-class=alb
           - --cluster-name=my_cluster
           - --aws-vpc-id=vpc-03468a8157edca5bd
           - --aws-region=us-west-2
   ```

**To deploy a sample application**

1. Deploy a sample application to verify that the ALB Ingress Controller creates an Application Load Balancer as a result of the Ingress object\. Use the following commands to deploy the game [2048](https://play2048.co/) as a sample application\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.4/docs/examples/2048/2048-namespace.yaml
   kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.4/docs/examples/2048/2048-deployment.yaml
   kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.4/docs/examples/2048/2048-service.yaml
   kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.4/docs/examples/2048/2048-ingress.yaml
   ```

1. After a few minutes, verify that the Ingress resource was created with the following command\.

   ```
   kubectl get ingress/2048-ingress -n 2048-game
   ```

   Output:

   ```
   NAME           HOSTS   ADDRESS                                                                 PORTS   AGE
   2048-ingress   *       example-2048game-2048ingr-6fa0-352729433.us-west-2.elb.amazonaws.com   80      24h
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
   kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.4/docs/examples/2048/2048-ingress.yaml
   kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.4/docs/examples/2048/2048-service.yaml
   kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.4/docs/examples/2048/2048-deployment.yaml
   kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.4/docs/examples/2048/2048-namespace.yaml
   ```