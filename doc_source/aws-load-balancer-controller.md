# AWS Load Balancer Controller<a name="aws-load-balancer-controller"></a>

The AWS Load Balancer Controller manages AWS Elastic Load Balancers for a Kubernetes cluster\. The controller provisions the following resources\.
+ An AWS Application Load Balancer \(ALB\) when you create a Kubernetes `Ingress`\.
+ An AWS Network Load Balancer \(NLB\) when you create a Kubernetes `Service` of type `LoadBalancer`\. In the past, the Kubernetes in\-tree load balancer was used for *instance* targets, but the AWS Load balancer Controller was used for *IP* targets\. With the AWS Load Balancer Controller version 2\.3\.0 or later, you can create Network Load Balancers using either target type\. For more information about NLB target types, see [Target type](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-target-groups.html#target-type) in the User Guide for Network Load Balancers\.

The controller was formerly named the *AWS ALB Ingress Controller*\. It's an [open\-source project](https://github.com/kubernetes-sigs/aws-load-balancer-controller) managed on GitHub\. This topic describes how to install the controller using default options\. You can view the full [documentation](https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/) for the controller on GitHub\. Before deploying the controller, we recommend that you review the prerequisites and considerations in [Application load balancing on Amazon EKS](alb-ingress.md) and [Network load balancing on Amazon EKS](network-load-balancing.md)\. Those topics also include steps on how to deploy a sample application that require the controller to provision AWS resources\.

**Prerequisites**
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\.
+ An existing AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.<a name="deploy-lb-controller"></a>

**To deploy the AWS Load Balancer Controller to an Amazon EKS cluster**

In the following steps, replace the `example values` with your own values\.

1. <a name="lbc-download-iam-policy"></a>Download an IAM policy for the AWS Load Balancer Controller that allows it to make calls to AWS APIs on your behalf\. You can view the [policy document](https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.3.1/docs/install/iam_policy.json) on GitHub\.

   ```
   curl -o iam_policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.3.1/docs/install/iam_policy.json
   ```

1. <a name="lbc-create-policy"></a>Create an IAM policy using the policy downloaded in the previous step\.

   ```
   aws iam create-policy \
       --policy-name AWSLoadBalancerControllerIAMPolicy \
       --policy-document file://iam_policy.json
   ```
**Note**  
If you view the policy in the AWS Management Console, you may see warnings for ELB\. These can be safely ignored because some of the actions only exist for ELB v2\. You do not see warnings for ELB v2\.

1. <a name="lbc-create-role"></a>Create an IAM role and annotate the Kubernetes service account that's named `aws-load-balancer-controller` in the `kube-system` namespace for the AWS Load Balancer Controller using `eksctl` or the AWS Management Console and `kubectl`\.

------
#### [ eksctl ]

   Replace *my\_cluster* with the name of your cluster and *111122223333* with your account ID and then run the command\.

   ```
   eksctl create iamserviceaccount \
     --cluster=my_cluster \
     --namespace=kube-system \
     --name=aws-load-balancer-controller \
     --attach-policy-arn=arn:aws:iam::111122223333:policy/AWSLoadBalancerControllerIAMPolicy \
     --override-existing-serviceaccounts \
     --approve
   ```

------
#### [ AWS Management Console and kubectl ]

   **Using the AWS Management Console and `kubectl`**

   1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

   1. In the navigation panel, choose **Roles**, **Create Role**\.

   1. In the **Select type of trusted entity** section, choose **Web identity**\.

   1. In the **Choose a web identity provider** section:

      1. For **Identity provider**, choose the URL for your cluster\. If you don't see a URL, confirm that you met the prerequisites for this topic\.

      1. For **Audience**, choose `sts.amazonaws.com`\.

   1. Choose **Next: Permissions**\.

   1. In the **Attach Policy** section, select the *`AWSLoadBalancerControllerIAMPolicy`* policy that you created in a [previous step](#lbc-create-policy) to use for your service account\.

   1. Choose **Next: Tags**\.

   1. On the **Add tags \(optional\)** screen, you can add tags for the account\. Choose **Next: Review**\.

   1. For **Role Name**, enter a name for your role, such as *`AmazonEKSLoadBalancerControllerRole`*, and then choose **Create Role**\.

   1. After the role is created, choose the role in the console to open it for editing\.

   1. Choose the **Trust relationships** tab, and then choose **Edit trust relationship**\.

   1. Find the line that looks similar to the following line:

      ```
      "oidc.eks.us-west-2.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E:aud": "sts.amazonaws.com"
      ```

      Change the line to look like the following line\. Replace *`EXAMPLED539D4633E53DE1B716D3041E`* with your cluster's OIDC provider ID and if necessary, replace *region\-code* with the Region code that your cluster is in\. Change `aud` to **`sub`** and replace *sts\.amazonaws\.com* with the value in the following text\.

      ```
      "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E:sub": "system:serviceaccount:kube-system:aws-load-balancer-controller"
      ```

   1. Choose **Update Trust Policy** to finish\.

   1. Note the ARN of the role for use in a later step\.

   1. Save the following contents to a file that's named *`aws-load-balancer-controller-service-account.yaml`*, replacing *111122223333* with your account ID\.

      ```
      apiVersion: v1
      kind: ServiceAccount
      metadata:
        labels:
          app.kubernetes.io/component: controller
          app.kubernetes.io/name: aws-load-balancer-controller
        name: aws-load-balancer-controller
        namespace: kube-system
        annotations:
            eks.amazonaws.com/role-arn: arn:aws:iam::111122223333:role/AmazonEKSLoadBalancerControllerRole
      ```

   1. Create the service account on your cluster\.

      ```
      kubectl apply -f aws-load-balancer-controller-service-account.yaml
      ```

------

1. <a name="lbc-4"></a>If you currently have the AWS ALB Ingress Controller for Kubernetes installed, uninstall it\. The AWS Load Balancer Controller replaces the functionality of the AWS ALB Ingress Controller for Kubernetes\.

   1. Check to see if the controller is currently installed\.

      ```
      kubectl get deployment -n kube-system alb-ingress-controller
      ```

      This is the output if the controller isn't installed\. Skip to the [install controller](#lbc-install-controller) step\.

      ```
      Error from server (NotFound): deployments.apps "alb-ingress-controller" not found
      ```

      This is the output if the controller is installed\.

      ```
      NAME                   READY UP-TO-DATE AVAILABLE AGE
      alb-ingress-controller 1/1   1          1         122d
      ```

   1. Enter the following commands to remove the controller\.

      ```
      kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.8/docs/examples/alb-ingress-controller.yaml
      kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.8/docs/examples/rbac-role.yaml
      ```

   1. Add the following IAM policy to the IAM role created in a [previous step](#lbc-create-role)\. The policy allows the AWS Load Balancer Controller access to the resources that were created by the ALB Ingress Controller for Kubernetes\.

      1. Download the IAM policy\. You can also [view the policy](https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy_v1_to_v2_additional.json)\.

         ```
         curl -o iam_policy_v1_to_v2_additional.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.3.1/docs/install/iam_policy_v1_to_v2_additional.json
         ```

      1. Create the IAM policy and note the ARN that is returned\.

         ```
         aws iam create-policy \
           --policy-name AWSLoadBalancerControllerAdditionalIAMPolicy \
           --policy-document file://iam_policy_v1_to_v2_additional.json
         ```

      1. Attach the IAM policy to the IAM role that you created in a [previous step](#lbc-create-role)\. Replace `your-role-name` with the name of the role\. If you created the role using `eksctl`, then to find the role name that was created, open the [AWS CloudFormation console](https://console.aws.amazon.com/cloudformation) and select the **eksctl\-*your\-cluster\-name*\-addon\-iamserviceaccount\-kube\-system\-aws\-load\-balancer\-controller** stack\. Select the **Resources** tab\. The role name is in the **Physical ID** column\. If you used the AWS Management Console to create the role, then the role name is whatever you named it, such as `AmazonEKSLoadBalancerControllerRole`\.

         ```
         aws iam attach-role-policy \
           --role-name your-role name \
           --policy-arn arn:aws:iam::111122223333:policy/AWSLoadBalancerControllerAdditionalIAMPolicy
         ```

1. <a name="lbc-install-controller"></a>Install the AWS Load Balancer Controller using Helm V3 or later or by applying a Kubernetes manifest\. If you want to deploy the controller on Fargate, use the Helm chart\. It doesn't depend on `cert-manager`\.

------
#### [ Helm V3 or later ]

   1. Add the `eks-charts` repository\.

      ```
      helm repo add eks https://aws.github.io/eks-charts
      ```

   1. Update your local repo to make sure that you have the most recent charts\.

      ```
      helm repo update
      ```

   1. Install the AWS Load Balancer Controller\. If you're deploying the controller to Amazon EC2 nodes that have [restricted access to the Amazon EC2 instance metadata service \(IMDS\)](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node), or if you're deploying to Fargate, then add the following flags to the following command:
      + `--set region=region-code`
      + `--set vpcId=vpc-xxxxxxxx`

      If you're deploying to any Region other than `us-west-2`, then add the following flag to the following command, replacing *`account`* and `region-code` with the values for your region listed in [Amazon EKS add\-on container image addresses](add-ons-images.md)\.

      `--set image.repository=account.dkr.ecr.region-code.amazonaws.com/amazon/aws-load-balancer-controller`

      ```
      helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
        -n kube-system \
        --set clusterName=cluster-name \
        --set serviceAccount.create=false \
        --set serviceAccount.name=aws-load-balancer-controller
      ```
**Important**  
The deployed chart doesn't receive security updates automatically\. You need to manually upgrade to a newer chart when it becomes available\. When upgrading, change `install` to `upgrade` in the previous command, but run the following command to install the `TargetGroupBinding` custom resource definitions before running the previous command\.  

      ```
      kubectl apply -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller/crds?ref=master"
      ```

------
#### [ Kubernetes manifest ]

   1. Install `cert-manager` to inject certificate configuration into the webhooks\.

      ```
      kubectl apply \
          --validate=false \
          -f https://github.com/jetstack/cert-manager/releases/download/v1.5.4/cert-manager.yaml
      ```

   1. Install the controller\. 

      1. Download the controller specification\. For more information about the controller, see the [documentation](https://kubernetes-sigs.github.io/aws-load-balancer-controller/) on GitHub\.

         ```
         curl -Lo v2_3_1_full.yaml https://github.com/kubernetes-sigs/aws-load-balancer-controller/releases/download/v2.3.1/v2_3_1_full.yaml
         ```

      1. Make the following edits to the `v2_3_1_full.yaml` file:
         + Delete the `ServiceAccount` section of the file\. Deleting this section prevents the annotation with the IAM role from being overwritten when the controller is deployed and preserves the service account that you created in step 3 if you delete the controller\.
         + Replace `your-cluster-name` in the `Deployment` `spec` section of the file with the name of your cluster\.

           ```
           ...
           spec:
                 containers:
                   - args:
                       - --cluster-name=your-cluster-name
           ...
           ```
         + If you're deploying the controller to Amazon EC2 nodes that have [restricted access to the Amazon EC2 instance metadata service \(IMDS\)](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node), or if you're deploying to Fargate, then add the **following parameters** under `- args:`\.

           ```
           ...
           spec:
                 containers:
                   - args:
                       - --cluster-name=your-cluster-name
                       - --ingress-class=alb
                       - --aws-vpc-id=vpc-xxxxxxxx
                       - --aws-region=region-code
           ...
           ```

      1. Apply the file\.

         ```
         kubectl apply -f v2_3_1_full.yaml
         ```

------

1. Verify that the controller is installed\.

   ```
   kubectl get deployment -n kube-system aws-load-balancer-controller
   ```

   Output

   ```
   NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
   aws-load-balancer-controller   2/2     2            2           84s
   ```

   You receive the previous output if you deployed using Helm\. If you deployed using the Kubernetes manifest, you only have one replica\.

1. Before using the controller to provision AWS resources, your cluster must meet specific requirements\. For more information, see [Application load balancing on Amazon EKS](alb-ingress.md) and [Network load balancing on Amazon EKS](network-load-balancing.md)\.