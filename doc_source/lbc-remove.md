# Migrate from Deprecated Controller<a name="lbc-remove"></a>

This topic describes how to migrate from deprecated controller versions\. More specifically, it describes how to remove deprecated versions of the AWS Load Balancer Controller\. 
+ Deprecated versions cannot be upgraded\. They must be removed and a current version of the LBC installed\. 
+ <a name="lbc-deprecated-list"></a>Deprecated versions include:
  + AWS ALB Ingress Controller for Kubernetes \("Ingress Controller"\), a predecessor to the AWS Load Balancer Controller\.
  + Any `0.1.x` version of the AWS Load Balancer Controller 

## Remove Deprecated Controller Version<a name="lbc-remove-desc"></a>

**Note**  
You may have installed the deprecated version using Helm or manually with Kubernetes manifests\. Complete the procedure using the tool that you originally installed it with\.

**Remove Ingress Controller using Helm**

1. If you installed the `incubator/aws-alb-ingress-controller` Helm chart, uninstall it\.

   ```
   $ helm delete aws-alb-ingress-controller -n kube-system
   ```

1. If you have version `0.1.x` of the `eks-charts/aws-load-balancer-controller` chart installed, uninstall it\. The upgrade from `0.1.x` to version `1.0.0` doesn't work due to incompatibility with the webhook API version\. 

   ```
   $ helm delete aws-load-balancer-controller -n kube-system
   ```

**Remove Ingress Controller using Kubernetes manifest**

1. Check to see if the controller is currently installed\.

   ```
   $ kubectl get deployment -n kube-system alb-ingress-controller
   ```

   This is the output if the controller isn't installed\. 

   Error from server \(NotFound\): deployments\.apps "alb\-ingress\-controller" not found

   This is the output if the controller is installed\.

   ```
   NAME                   READY UP-TO-DATE AVAILABLE AGE
   alb-ingress-controller 1/1   1          1         122d
   ```

1. Enter the following commands to remove the controller\.

   ```
   $ kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.8/docs/examples/alb-ingress-controller.yaml
   kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.8/docs/examples/rbac-role.yaml
   ```

## Migrate to AWS Load Balancer Controller<a name="lbc-migrate"></a>

To migrate from the ALB Ingress Controller for Kubernetes to the AWS Load Balancer Controller, you need to:

1. Remove the ALB Ingress Controller \(see above\)\.

1. [Install the AWS Load Balancer Controller\.](aws-load-balancer-controller.md#lbc-overview) 

1. Add an additional policy to the IAM Role used by the LBC\. This policy permits the LBC to manage resources created by the ALB Ingress Controller for Kubernetes\.

**Add Migration Policy to AWS Load Balancer Controller IAM role\.**

1. Download the IAM policy\. This policy permits the LBC to manage resources created by the ALB Ingress Controller for Kubernetes\. You can also [view the policy](https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy_v1_to_v2_additional.json)\.

   ```
   $ curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.7.2/docs/install/iam_policy_v1_to_v2_additional.json
   ```

1. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-West\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:`\.\.

   ```
   $ sed -i.bak -e 's|arn:aws:|arn:aws-us-gov:|' iam_policy_v1_to_v2_additional.json
   ```

1. Create the IAM policy and note the ARN that is returned\.

   ```
   $ aws iam create-policy \
     --policy-name AWSLoadBalancerControllerAdditionalIAMPolicy \
     --policy-document file://iam_policy_v1_to_v2_additional.json
   ```

1. Attach the IAM policy to the IAM role used by the LBC\. Replace `your-role-name` with the name of the role, such as `AmazonEKSLoadBalancerControllerRole`\. 

   If you created the role using `eksctl`, then to find the role name that was created, open the [AWS CloudFormation console](https://console.aws.amazon.com/cloudformation) and select the **eksctl\-*my\-cluster*\-addon\-iamserviceaccount\-kube\-system\-aws\-load\-balancer\-controller** stack\. Select the **Resources** tab\. The role name is in the **Physical ID** column\. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-West\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:`\.

   ```
   $ aws iam attach-role-policy \
     --role-name your-role-name \
     --policy-arn arn:aws:iam::111122223333:policy/AWSLoadBalancerControllerAdditionalIAMPolicy
   ```