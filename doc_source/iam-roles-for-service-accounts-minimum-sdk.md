# Using a supported AWS SDK<a name="iam-roles-for-service-accounts-minimum-sdk"></a>

The containers in your pods must use an AWS SDK version that supports assuming an IAM role via an OIDC web identity token file\. AWS SDKs that are included in Linux distribution package managers may not be new enough to support this feature\. Be sure to use at least the minimum SDK versions listed below:
+ Java \(Version 2\) — [2\.10\.11](https://github.com/aws/aws-sdk-java-v2/releases/tag/2.10.11)
+ Java — [1\.11\.704](https://github.com/aws/aws-sdk-java/releases/tag/1.11.704)
+ Go — [1\.23\.13](https://github.com/aws/aws-sdk-go/releases/tag/v1.23.13)
+ Python \(Boto3\) — [1\.9\.220](https://github.com/boto/boto3/releases/tag/1.9.220)
+ Python \(botocore\) — [1\.12\.200](https://github.com/boto/botocore/releases/tag/1.12.200)
+ AWS CLI — [1\.16\.232](https://github.com/aws/aws-cli/releases/tag/1.16.232)
+ Node — [2\.521\.0](https://github.com/aws/aws-sdk-js/releases/tag/v2.521.0)
+ Ruby — [2\.11\.345](https://github.com/aws/aws-sdk-ruby/releases/tag/v2.11.345)
+ C\+\+ — [1\.7\.174](https://github.com/aws/aws-sdk-cpp/releases/tag/1.7.174)
+ \.NET — [3\.3\.659\.1](https://github.com/aws/aws-sdk-net/releases/tag/3.3.659.1)
+ PHP — [3\.110\.7](https://github.com/aws/aws-sdk-php/releases/tag/3.110.7)

Many popular Kubernetes add\-ons, such as the [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler) and the [ AWS Load Balancer Controller  The AWS Load Balancer Controller manages AWS Elastic Load Balancers for a Kubernetes cluster\. The controller provisions:   An AWS Application Load Balancer \(ALB\) when you create a Kubernetes `Ingress`\.   An AWS Network Load Balancer \(NLB\) when you create a Kubernetes `Service` of type `LoadBalancer` using IP targets on 1\.18 or later Amazon EKS clusters\. If you're load balancing network traffic to instance targets, then you use the in\-tree Kubernetes load balancer controller and don't need to install this controller\. For more information about NLB target types, see [Target type](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-target-groups.html#target-type) in the User Guide for Network Load Balancers\.    The controller was formerly named the *AWS ALB Ingress Controller*\. It is an [open source project](https://github.com/kubernetes-sigs/aws-load-balancer-controller) managed on GitHub\. This topic helps you install the controller using default options\. You can view the full [documentation](https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/) for the controller on GitHub\. Before deploying the controller we recommend that you review the prequisites and considerations in [Application load balancing on Amazon EKS](alb-ingress.md) and [Network load balancing on Amazon EKS](load-balancing.md)\. Those topics also include steps to deploy a sample application that require the controller to provision AWS resources\.  Prerequisite An existing cluster\. If you don't have an existing cluster, see [Getting started with Amazon EKS](getting-started.md)\.  To deploy the AWS Load Balancer Controller to an Amazon EKS cluster In the following steps, replace the `<example values>` \(including `<>`\) with your own values\.  Determine whether you have an existing IAM OIDC provider for your cluster\.View your cluster's OIDC provider URL\. 

   ```
   aws eks describe-cluster --name <cluster_name> --query "cluster.identity.oidc.issuer" --output text
   ``` Example output: 

   ```
   https://oidc.eks.us-west-2.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E
   ``` List the IAM OIDC providers in your account\. Replace `<EXAMPLED539D4633E53DE1B716D3041E>` \(including `<>`\) with the value returned from the previous command\. 

   ```
   aws iam list-open-id-connect-providers | grep <EXAMPLED539D4633E53DE1B716D3041E>
   ``` Example output 

   ```
   "Arn": "arn:aws:iam::111122223333:oidc-provider/oidc.eks.us-west-2.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E"
   ``` If output is returned from the previous command, then you already have a provider for your cluster\. If no output is returned, then you must create an IAM OIDC provider\. To create an IAM OIDC provider, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.   Download an IAM policy for the AWS Load Balancer Controller that allows it to make calls to AWS APIs on your behalf\. You can view the [policy document](https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2_ga/docs/install/iam_policy.json) on GitHub\. Use the command that corresponds to the Region that your cluster is in\.   All Regions other than China Regions\. 

     ```
     curl -o iam_policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.1.0/docs/install/iam_policy.json
     ```   Beijing and Ningxia China Regions\. 

     ```
     curl -o iam_policy_cn.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.1.0/docs/install/iam_policy_cn.json
     ```     Create an IAM policy using the policy downloaded in the previous step\. Change `iam_policy.json` to `iam_policy_cn.json` in the following command, if you downloaded that file instead\. 

   ```
   aws iam create-policy \
       --policy-name <AWSLoadBalancerControllerIAMPolicy> \
       --policy-document file://iam_policy.json
   ``` Take note of the policy ARN that is returned\.   Create an IAM role and annotate the Kubernetes service account named `aws-load-balancer-controller` in the `kube-system` namespace for the AWS Load Balancer Controller using one of the following options\.   **Using eksctl** Use the following command: 

     ```
       eksctl create iamserviceaccount \
       --cluster=<my-cluster> \
       --namespace=kube-system \
       --name=aws-load-balancer-controller \
       --attach-policy-arn=arn:aws:iam::<AWS_ACCOUNT_ID>:policy/<AWSLoadBalancerControllerIAMPolicy> \
       --override-existing-serviceaccounts \
       --approve
     ```    **Using the AWS Management Console and `kubectl`** Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.  In the navigation panel, choose **Roles**, **Create Role**\.   In the **Select type of trusted entity** section, choose **Web identity**\.   In the **Choose a web identity provider** section:   For **Identity provider**, choose the URL for your cluster\.   For **Audience**, choose `sts.amazonaws.com`\.     Choose **Next: Permissions**\.   In the **Attach Policy** section, select the `AWSLoadBalancerControllerIAMPolicy` policy that you created in step 3 to use for your service account\.  Choose **Next: Tags**\.  On the **Add tags \(optional\)** screen, you can add tags for the account\. Choose **Next: Review**\.   For **Role Name**, enter a name for your role, such as `AmazonEKSLoadBalancerConrollerRole`, and then choose **Create Role**\.   After the role is created, choose the role in the console to open it for editing\.   Choose the **Trust relationships** tab, and then choose **Edit trust relationship**\. Change the line that looks similar to the following: 

        ```
        "oidc.eks.us-west-2.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E:aud": "sts.amazonaws.com"
        ``` To look like the following, changing the `<example values>` \(including `<>`\) to your own: 

        ```
        "oidc.eks.<region-code>.amazonaws.com/id/<EXAMPLED539D4633E53DE1B716D3041E>:sub": "system:serviceaccount:kube-system:aws-load-balancer-controller"
        ```   Choose **Update Trust Policy** to finish\.  Note the ARN of the role for use in a later step\.  Save the following contents to a file named `aws-load-balancer-controller-service-account.yaml` 

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
              eks.amazonaws.com/role-arn: arn:aws:iam::<AWS_ACCOUNT_ID>:role/AmazonEKSLoadBalancerConrollerRole
        ```   Create the service account on your cluster\. 

        ```
        kubectl apply -f aws-load-balancer-controller-service-account.yaml
        ```       If you currently have the AWS ALB Ingress Controller for Kubernetes installed, uninstall it\. The AWS Load Balancer Controller replaces the functionality of the AWS ALB Ingress Controller for Kubernetes\.   Check to see if the controller is currently installed\. 

      ```
      kubectl get deployment -n kube-system alb-ingress-controller
      ``` Output \(if it is installed\)\. Skip to step 5b\. 

      ```
      NAME                   READY UP-TO-DATE AVAILABLE AGE
      alb-ingress-controller 1/1   1          1         122d
      ``` Output \(if it isn't installed\)\. If it isn't installed, skip to step 6\. 

      ```
      Error from server (NotFound): deployments.apps "alb-ingress-controller" not found
      ```   If the controller is installed, enter the following commands to remove it\. 

      ```
      kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.8/docs/examples/alb-ingress-controller.yaml
      kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.8/docs/examples/rbac-role.yaml
      ```   If you removed the AWS ALB Ingress Controller for Kubernetes, add the following IAM policy to the IAM role created in step 4\. The policy allows the AWS Load Balancer Controller access to the resources that were created by the ALB Ingress Controller for Kubernetes\.   Download the IAM policy\. You can also [view the policy](https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy_v1_to_v2_additional.json)\. 

         ```
         curl -o iam_policy_v1_to_v2_additional.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.1.0/docs/install/iam_policy_v1_to_v2_additional.json
         ```   Create the IAM policy and note the ARN returned\. 

         ```
         aws iam create-policy \
           --policy-name <AWSLoadBalancerControllerAdditionalIAMPolicy> \
           --policy-document file://iam_policy_v1_to_v2_additional.json
         ```   Attach the IAM policy to the IAM role that you created in step 4\. Replace `<your-role-name>` \(including `<>`\) with the name of the role\. If you created the role using `eksctl`, then to find the role name that was created, open the [AWS CloudFormation console](https://console.aws.amazon.com//cloudformation) and select the **eksctl\-<your\-cluster\-name>\-addon\-iamserviceaccount\-kube\-system\-aws\-load\-balancer\-controller** stack\. Select the **Resources** tab\. The role name is in the **Physical ID** column\. If you used the AWS Management Console to create the role, then the role name is whatever you named it, such as `AmazonEKSLoadBalancerConrollerRole`\. 

         ```
         aws iam attach-role-policy \
           --role-name eksctl-<your-role name>\
           --policy-arn arn:aws:iam::111122223333:policy/AWSLoadBalancerControllerAdditionalIAMPolicy
         ```       Install the AWS Load Balancer Controller using one of the following methods:   With Helm   Install the `TargetGroupBinding` custom resource definitions\. 

        ```
        kubectl apply -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller//crds?ref=master"
        ```   Add the `eks-charts` repository\. 

        ```
        helm repo add eks https://aws.github.io/eks-charts
        ```   Install the AWS Load Balancer Controller using the command that corresponds to the Region that your cluster is in\.  If you are deploying the controller to Amazon EC2 nodes that you have [restricted access to the Amazon EC2 instance metadata service \(IMDS\)](best-practices-security.md#restrict-ec2-credential-access) from, or if you are deploying to Fargate, then you need to add the following flags to the command that you run:   `--set region=<region-code>`   `--set vpcId=<vpc-xxxxxxxx>`      All Regions other than China Regions\. 

          ```
          helm upgrade -i aws-load-balancer-controller eks/aws-load-balancer-controller \
            --set clusterName=<cluster-name> \
            --set serviceAccount.create=false \
            --set serviceAccount.name=aws-load-balancer-controller \
            -n kube-system
          ```   Beijing and Ningxia China Regions\. 

          ```
          helm upgrade -i aws-load-balancer-controller eks/aws-load-balancer-controller \
            --set clusterName=<cluster-name> \
            --set serviceAccount.create=false \
            --set serviceAccount.name=aws-load-balancer-controller \
            --set image.repository=918309763551.dkr.ecr.cn-north-1.amazonaws.com.cn/amazon/aws-load-balancer-controller \
            -n kube-system
          ```    The deployed chart does not receive security updates automatically\. You need to manually upgrade to a newer chart when it becomes available\.      With a Kubernetes manifest   Install `cert-manager` to inject certificate configuration into the webhooks\.   Install on Kubernetes `1.16` or later\. 

          ```
          kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/v1.0.2/cert-manager.yaml
          ```   Install on Kubernetes `1.15`\. 

          ```
           kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/v1.0.2/cert-manager-legacy.yaml
          ```     Install the controller\.    Download the controller specification\. For more information about the controller, see the [documentation](https://kubernetes-sigs.github.io/aws-load-balancer-controller/) on GitHub\. 

           ```
           curl -o v2_1_0_full.yaml https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.1.0/docs/install/v2_1_0_full.yaml
           ```   Edit the saved yaml file\. It is recommended that you delete the `ServiceAccount` section from the yaml specification\. Doing so will preserve the service account that you created in step 4 if you delete the controller\. In the `Deployment` `spec` section set the `--cluster-name` value to your Amazon EKS cluster name\.    Apply the file\. 

           ```
           kubectl apply -f v2_1_0_full.yaml
           ```         Verify that the controller is installed\. 

   ```
   kubectl get deployment -n kube-system aws-load-balancer-controller
   ``` Output 

   ```
   NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
   aws-load-balancer-controller   1/1     1            1           84s
   ```   Before using the controller to provision AWS resources, your cluster must meet specific requirements\. For more information, see [Application load balancing on Amazon EKS](alb-ingress.md) and [Network load balancing on Amazon EKS](load-balancing.md)\.   ](aws-load-balancer-controller.md) support IAM roles for service accounts\. The [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) also supports IAM roles for service accounts\.

To ensure that you are using a supported SDK, follow the installation instructions for your preferred SDK at [Tools for Amazon Web Services](https://aws.amazon.com/tools/) when you build your containers\. 