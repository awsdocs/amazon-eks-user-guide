# Installing the AWS Load Balancer Controller add\-on<a name="aws-load-balancer-controller"></a>

The AWS Load Balancer Controller manages AWS Elastic Load Balancers for a Kubernetes cluster\. The controller provisions the following resources:
+ An AWS Application Load Balancer \(ALB\) when you create a Kubernetes `Ingress`\.
+ An AWS Network Load Balancer \(NLB\) when you create a Kubernetes service of type `LoadBalancer`\. In the past, the Kubernetes network load balancer was used for *instance* targets, but the AWS Load balancer Controller was used for *IP* targets\. With the AWS Load Balancer Controller version `2.3.0` or later, you can create NLBs using either target type\. For more information about NLB target types, see [Target type](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-target-groups.html#target-type) in the User Guide for Network Load Balancers\.

The AWS Load Balancer Controller controller was formerly named the *AWS ALB Ingress Controller*\. It's an [open\-source project](https://github.com/kubernetes-sigs/aws-load-balancer-controller) managed on GitHub\. This topic describes how to install the controller using default options\. You can view the full [documentation](https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/) for the controller on GitHub\. Before deploying the controller, we recommend that you review the prerequisites and considerations in [Application load balancing on Amazon EKS](alb-ingress.md) and [Network load balancing on Amazon EKS](network-load-balancing.md)\. Those topics also include steps on how to deploy a sample application that require the AWS Load Balancer Controller to provision AWS Application Load Balancers and Network Load Balancers\.

**Prerequisites**
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\.
+ An existing AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see [Creating an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ If your cluster is `1.21` or later, make sure that your Amazon VPC CNI plugin for Kubernetes, `kube-proxy`, and CoreDNS add\-ons are at the minimum versions listed in [Service account tokens](service-accounts.md#boundserviceaccounttoken-validated-add-on-versions)\.

**To deploy the AWS Load Balancer Controller to an Amazon EKS cluster**

In the following steps, replace the `example values` with your own values\.

1. Create an IAM policy\.

   1. Download an IAM policy for the AWS Load Balancer Controller that allows it to make calls to AWS APIs on your behalf\.
      + AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-West\) AWS Regions

        ```
        curl -o iam_policy_us-gov.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.4.3/docs/install/iam_policy_us-gov.json
        ```
      + All other AWS Regions

        ```
        curl -o iam_policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.4.3/docs/install/iam_policy.json
        ```

   1. Create an IAM policy using the policy downloaded in the previous step\. If you downloaded `iam_policy_us-gov.json`, change `iam_policy.json` to `iam_policy_us-gov.json` before running the command\.

      ```
      aws iam create-policy \
          --policy-name AWSLoadBalancerControllerIAMPolicy \
          --policy-document file://iam_policy.json
      ```
**Note**  
If you view the policy in the AWS Management Console, you may see warnings for **ELB**\. These can be safely ignored because some of the actions only exist for ELB v2\. You do not see warnings for ELB v2\.

1. Create an IAM role\. Create a Kubernetes service account named `aws-load-balancer-controller` in the `kube-system` namespace for the AWS Load Balancer Controller and annotate the Kubernetes service account with the name of the IAM role\.

   You can use `eksctl` or the AWS CLI and `kubectl` to create the IAM role and Kubernetes service account\.

------
#### [ eksctl ]

   Replace `my-cluster` with the name of your cluster, `111122223333` with your account ID, and then run the command\. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-West\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:`\.

   ```
   eksctl create iamserviceaccount \
     --cluster=my-cluster \
     --namespace=kube-system \
     --name=aws-load-balancer-controller \
     --role-name "AmazonEKSLoadBalancerControllerRole" \
     --attach-policy-arn=arn:aws:iam::111122223333:policy/AWSLoadBalancerControllerIAMPolicy \
     --approve
   ```

------
#### [ AWS CLI and kubectl ]

   **Using the AWS CLI and `kubectl`**

   1. View your cluster's OIDC provider URL\.

      ```
      aws eks describe-cluster --name my-cluster --query "cluster.identity.oidc.issuer" --output text
      ```

      The example output is as follows\.

      ```
      oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE
      ```

      If no output is returned, then you must [create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.

   1. Copy the following contents to your device\. Replace `111122223333` with your account ID\. Replace `region-code` with the AWS Region that your cluster is in\.\. Replace `EXAMPLED539D4633E53DE1B71EXAMPLE` with the output returned in the previous step\. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-West\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:`\. After replacing the text, run the modified command to create the `load-balancer-role-trust-policy.json` file\.

      ```
      cat >load-balancer-role-trust-policy.json <<EOF
      {
          "Version": "2012-10-17",
          "Statement": [
              {
                  "Effect": "Allow",
                  "Principal": {
                      "Federated": "arn:aws:iam::111122223333:oidc-provider/oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE"
                  },
                  "Action": "sts:AssumeRoleWithWebIdentity",
                  "Condition": {
                      "StringEquals": {
                          "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:aud": "sts.amazonaws.com",
                          "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:sub": "system:serviceaccount:kube-system:aws-load-balancer-controller"
                      }
                  }
              }
          ]
      }
      EOF
      ```

   1. Create the IAM role\.

      ```
      aws iam create-role \
        --role-name AmazonEKSLoadBalancerControllerRole \
        --assume-role-policy-document file://"load-balancer-role-trust-policy.json"
      ```

   1. Attach the required Amazon EKS managed IAM policy to the IAM role\. Replace `111122223333` with your account ID\.

      ```
      aws iam attach-role-policy \
        --policy-arn arn:aws:iam::111122223333:policy/AWSLoadBalancerControllerIAMPolicy \
        --role-name AmazonEKSLoadBalancerControllerRole
      ```

   1. Copy the following contents to your device\. Replace `111122223333` with your account ID\. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-West\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:`\. After replacing the text, run the modified command to create the `aws-load-balancer-controller-service-account.yaml` file\.

      ```
      cat >aws-load-balancer-controller-service-account.yaml <<EOF
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
      EOF
      ```

   1. Create the Kubernetes service account on your cluster\. The Kubernetes service account named `aws-load-balancer-controller` is annotated with the IAM role that you created named `AmazonEKSLoadBalancerControllerRole`\.

      ```
      kubectl apply -f aws-load-balancer-controller-service-account.yaml
      ```

------

1. \(Optional\) Configure the AWS Security Token Service endpoint type used by your Kubernetes service account\. For more information, see [Configuring the AWS Security Token Service endpoint for a service account](configure-sts-endpoint.md)\.

1. If you don't currently have the AWS ALB Ingress Controller for Kubernetes installed, or don't currently have the `0.1.x` version of the AWS Load Balancer Controller installed with Helm, then skip to the next step\.

   Uninstall the AWS ALB Ingress Controller or `0.1.x` version of the AWS Load Balancer Controller \(only if installed with Helm\)\. Complete the procedure using the tool that you originally installed it with\. The AWS Load Balancer Controller replaces the functionality of the AWS ALB Ingress Controller for Kubernetes\.

------
#### [ Helm ]

   1. If you installed the `incubator/aws-alb-ingress-controller` Helm chart, uninstall it\.

      ```
      helm delete aws-alb-ingress-controller -n kube-system
      ```

   1. If you have version `0.1.x` of the `eks-charts/aws-load-balancer-controller` chart installed, uninstall it\. The upgrade from `0.1.x` to version `1.0.0` doesn't work due to incompatibility with the webhook API version\. 

      ```
      helm delete aws-load-balancer-controller -n kube-system
      ```

------
#### [ Kubernetes manifest ]

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
         curl -o iam_policy_v1_to_v2_additional.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.4.3/docs/install/iam_policy_v1_to_v2_additional.json
         ```

      1. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-West\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:`\.\.

         ```
         sed -i.bak -e 's|arn:aws:|arn:aws-us-gov:|' iam_policy_v1_to_v2_additional.json
         ```

      1. Create the IAM policy and note the ARN that is returned\.

         ```
         aws iam create-policy \
           --policy-name AWSLoadBalancerControllerAdditionalIAMPolicy \
           --policy-document file://iam_policy_v1_to_v2_additional.json
         ```

      1. Attach the IAM policy to the IAM role that you created in a [previous step](#lbc-create-role)\. Replace `your-role-name` with the name of the role\. If you created the role using `eksctl`, then to find the role name that was created, open the [AWS CloudFormation console](https://console.aws.amazon.com/cloudformation) and select the **eksctl\-*my\-cluster*\-addon\-iamserviceaccount\-kube\-system\-aws\-load\-balancer\-controller** stack\. Select the **Resources** tab\. The role name is in the **Physical ID** column\. If you used the AWS Management Console to create the role, then the role name is whatever you named it, such as `AmazonEKSLoadBalancerControllerRole`\. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-West\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:`\.

         ```
         aws iam attach-role-policy \
           --role-name your-role-name \
           --policy-arn arn:aws:iam::111122223333:policy/AWSLoadBalancerControllerAdditionalIAMPolicy
         ```

------

1. Install the AWS Load Balancer Controller using [Helm V3](helm.md) or later or by applying a Kubernetes manifest\. If you want to deploy the controller on Fargate, use the Helm procedure because it doesn't depend on `cert-manager`\.

------
#### [ Helm ]

   1. Add the `eks-charts` repository\.

      ```
      helm repo add eks https://aws.github.io/eks-charts
      ```

   1. Update your local repo to make sure that you have the most recent charts\.

      ```
      helm repo update
      ```

   1. If your nodes don't have access to Amazon EKS Amazon ECR image repositories, then you need to pull the following container image and push it to a repository that your nodes have access to\. For more information on how to pull, tag, and push an image to your own repository, see [Copy a container image from one repository to another repository](copy-image-to-repository.md)\. Replace *`602401143452`* and `region-code` with the values for your AWS Region listed in [Amazon container image registries](add-ons-images.md)\.

      ```
      602401143452.dkr.ecr.region-code.amazonaws.com/amazon/aws-load-balancer-controller:v2.4.3
      ```

   1. Install the AWS Load Balancer Controller\. If you're deploying the controller to Amazon EC2 nodes that have [restricted access to the Amazon EC2 instance metadata service \(IMDS\)](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node), or if you're deploying to Fargate, then add the following flags to the `helm` command that follows:
      + `--set region=region-code`
      + `--set vpcId=vpc-xxxxxxxx`

      If you're deploying to any AWS Region other than `us-west-2`, then add the following flag to the `helm` command, replacing *`602401143452`* and `region-code` with the values for your AWS Region listed in [Amazon container image registries](add-ons-images.md)\. If you pulled the image and pushed it to your own repository, then replace the full registry and repository with your own\.

      ```
      --set image.repository=602401143452.dkr.ecr.region-code.amazonaws.com/amazon/aws-load-balancer-controller
      ```

      Replace `my-cluster` with your own\. In the following command, `aws-load-balancer-controller` is the Kubernetes service account that you created in a previous step\.

      ```
      helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
        -n kube-system \
        --set clusterName=my-cluster \
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

   1. Install `cert-manager` using one of the following methods to inject certificate configuration into the webhooks\.
      + If your nodes have access to the `quay.io` container registry, install `cert-manager` to inject certificate configuration into the webhooks\. 

        ```
        kubectl apply \
            --validate=false \
            -f https://github.com/jetstack/cert-manager/releases/download/v1.5.4/cert-manager.yaml
        ```
      + If your nodes don't have access to the `quay.io` container registry, then complete the following tasks:

        1. Download the manifest\.

           ```
           curl -Lo cert-manager.yaml https://github.com/jetstack/cert-manager/releases/download/v1.5.4/cert-manager.yaml
           ```

        1. Pull the following images and push them to a repository that your nodes have access to\. For more information on how to pull, tag, and push the images to your own repository, see [Copy a container image from one repository to another repository](copy-image-to-repository.md)\.

           ```
           quay.io/jetstack/cert-manager-cainjector:v1.5.4
           quay.io/jetstack/cert-manager-controller:v1.5.4
           quay.io/jetstack/cert-manager-webhook:v1.5.4
           ```

        1. Replace `quay.io` in the manifest for the three images with your own registry name\. The following command assumes that your private repository's name is the same as the source repository\. Replace **111122223333*\.dkr\.ecr\.*region\-code*\.amazonaws\.com* with your private registry\.

           ```
           sed -i.bak -e 's|quay.io|111122223333.dkr.ecr.region-code.amazonaws.com|' ./cert-manager.yaml
           ```

        1. Apply the manifest\.

           ```
           kubectl apply \
               --validate=false \
               -f ./cert-manager.yaml
           ```

   1. Install the controller\. 

      1. Download the controller specification\. For more information about the controller, see the [documentation](https://kubernetes-sigs.github.io/aws-load-balancer-controller/) on GitHub\.

         ```
         curl -Lo v2_4_3_full.yaml https://github.com/kubernetes-sigs/aws-load-balancer-controller/releases/download/v2.4.3/v2_4_3_full.yaml
         ```

      1. Make the following edits to the file\.
         + If you downloaded the `v2_4_3_full.yaml` file, run the following command to remove the `ServiceAccount` section in the manifest\. If you don't remove this section, the required annotation that you made to the service account in a previous step is overwritten\. Removing this section also preserves the service account that you created in a previous step if you delete the controller\.

           ```
           sed -i.bak -e '480,488d' ./v2_4_3_full.yaml
           ```

           If you downloaded a different file version, then open the file in an editor and remove the following lines\. 

           ```
           apiVersion: v1
           kind: ServiceAccount
           metadata:
             labels:
               app.kubernetes.io/component: controller
               app.kubernetes.io/name: aws-load-balancer-controller
             name: aws-load-balancer-controller
             namespace: kube-system
           ---
           ```
         + Replace `your-cluster-name` in the `Deployment` `spec` section of the file with the name of your cluster by replacing `my-cluster` with the name of your cluster\.

           ```
           sed -i.bak -e 's|your-cluster-name|my-cluster|' ./v2_4_3_full.yaml
           ```
         + If your nodes don't have access to the Amazon EKS Amazon ECR image repositories, then you need to pull the following image and push it to a repository that your nodes have access to\. For more information on how to pull, tag, and push an image to your own repository, see [Copy a container image from one repository to another repository](copy-image-to-repository.md)\.

           ```
           amazon/aws-alb-ingress-controller:v2.4.3
           ```

           Add your registry's name to the manifest\. The following command assumes that your private repository's name is the same as the source repository and adds your private registry's name to the file\. In the source file there is no registry specified because Kubernetes pulls from `docker.io`, by default\. Replace **111122223333*\.dkr\.ecr\.*region\-code*\.amazonaws\.com* with your registry\. This line assumes that you named your private repository the same as the source repository\. If not, change the `amazon/aws-alb-ingress-controller` text after your private registry name to your repository name\.

           ```
           sed -i.bak -e 's|amazon/aws-alb-ingress-controller|111122223333.dkr.ecr.region-code.amazonaws.com/amazon/aws-alb-ingress-controller|' ./v2_4_3_full.yaml
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
         kubectl apply -f v2_4_3_full.yaml
         ```

      1. Apply the `IngressClass` and `IngressClassParams` manifest to your cluster\.

         ```
         curl -Lo v2_4_3_ingclass.yaml https://github.com/kubernetes-sigs/aws-load-balancer-controller/releases/download/v2.4.3/v2_4_3_ingclass.yaml
         ```

      1. Apply the manifest to your cluster\.

         ```
         kubectl apply -f v2_4_3_ingclass.yaml
         ```

------

1. Verify that the controller is installed\.

   ```
   kubectl get deployment -n kube-system aws-load-balancer-controller
   ```

   The example output is as follows\.

   ```
   NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
   aws-load-balancer-controller   2/2     2            2           84s
   ```

   You receive the previous output if you deployed using Helm\. If you deployed using the Kubernetes manifest, you only have one replica\.

1. Before using the controller to provision AWS resources, your cluster must meet specific requirements\. For more information, see [Application load balancing on Amazon EKS](alb-ingress.md) and [Network load balancing on Amazon EKS](network-load-balancing.md)\.