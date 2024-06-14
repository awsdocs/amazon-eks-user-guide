# Install the AWS Load Balancer Controller add\-on using Kubernetes Manifests<a name="lbc-manifest"></a>

This topic describes how to install the controller by downloading and applying Kubernetes manifests\. You can view the full [documentation](https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/) for the controller on GitHub\. 

In the following steps, replace the `example values` with your own values\.

## Prerequisites<a name="lbc-prereqs"></a>

Before starting this tutorial, you must install and configure the following tools and resources that you need to create and manage an Amazon EKS cluster\.<a name="lbc-prereqs.itemizedlist"></a>
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\.
+ An existing AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ Make sure that your Amazon VPC CNI plugin for Kubernetes, `kube-proxy`, and CoreDNS add\-ons are at the minimum versions listed in [Service account tokens](service-accounts.md#boundserviceaccounttoken-validated-add-on-versions)\.
+ Familiarity with AWS Elastic Load Balancing\. For more information, see the [Elastic Load Balancing User Guide](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/)\.
+ Familiarity with Kubernetes [service](https://kubernetes.io/docs/concepts/services-networking/service/) and [ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) resources\.

## Step 1: Configure IAM<a name="lbc-iam"></a>

**Note**  
You only need to create an IAM Role for the AWS Load Balancer Controller one per AWS account\. Check if `AmazonEKSLoadBalancerControllerRole` exists in the [IAM Console](https://console.aws.amazon.com/iam)\. If this role exists, skip to [Step 2: Install `cert-manager`](#lbc-cert)\.<a name="lbc-iam.step1"></a>

**Create an IAM policy\.**

1. Download an IAM policy for the AWS Load Balancer Controller that allows it to make calls to AWS APIs on your behalf\. 

------
#### [ AWS ]

   ```
   $ curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.7.2/docs/install/iam_policy.json
   ```

------
#### [ AWS GovCloud \(US\) ]

   ```
   $ curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.7.2/docs/install/iam_policy_us-gov.json
   ```

   ```
   $ mv iam_policy_us-gov.json iam_policy.json
   ```

------

1. Create an IAM policy using the policy downloaded in the previous step\. 

   ```
   $ aws iam create-policy \
       --policy-name AWSLoadBalancerControllerIAMPolicy \
       --policy-document file://iam_policy.json
   ```
**Note**  
If you view the policy in the AWS Management Console, the console shows warnings for the **ELB** service, but not for the **ELB v2** service\. This happens because some of the actions in the policy exist for **ELB v2**, but not for **ELB**\. You can ignore the warnings for **ELB**\.

------
#### [ eksctl ]<a name="lbc-iam.eksctl"></a>

**Create IAM Role using `eksctl`**
+ Replace `my-cluster` with the name of your cluster, `111122223333` with your account ID, and then run the command\. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-West\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:`\.

  ```
  $ eksctl create iamserviceaccount \
    --cluster=my-cluster \
    --namespace=kube-system \
    --name=aws-load-balancer-controller \
    --role-name AmazonEKSLoadBalancerControllerRole \
    --attach-policy-arn=arn:aws:iam::111122223333:policy/AWSLoadBalancerControllerIAMPolicy \
    --approve
  ```

------
#### [ AWS CLI and kubectl ]

**Create IAM Role using the AWS CLI and `kubectl`**

1. Retrieve your cluster's OIDC provider ID and store it in a variable\.

   ```
   oidc_id=$(aws eks describe-cluster --name my-cluster --query "cluster.identity.oidc.issuer" --output text | cut -d '/' -f 5)
   ```

1. Determine whether an IAM OIDC provider with your cluster's ID is already in your account\. You need OIDC configured for both the cluster and IAM\.

   ```
   aws iam list-open-id-connect-providers | grep $oidc_id | cut -d "/" -f4
   ```

   If output is returned, then you already have an IAM OIDC provider for your cluster\. If no output is returned, then you must create an IAM OIDC provider for your cluster\. For more information, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.

1. Copy the following contents to your device\. Replace `111122223333` with your account ID\. Replace `region-code` with the AWS Region that your cluster is in\. Replace `EXAMPLED539D4633E53DE1B71EXAMPLE` with the output returned in the previous step\. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-West\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:`\. After replacing the text, run the modified command to create the `load-balancer-role-trust-policy.json` file\.

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
   $ kubectl apply -f aws-load-balancer-controller-service-account.yaml
   ```

------

## Step 2: Install `cert-manager`<a name="lbc-cert"></a>

Install `cert-manager` using one of the following methods to inject certificate configuration into the webhooks\. For more information, see [Getting Started](https://cert-manager.io/docs/installation/#getting-started) on the *`cert-manager` Documentation*\.

We recommend using the `quay.io` container registry to install `cert-manager`\. If your nodes do not have access to the `quay.io` container registry, Install `cert-manager` using Amazon ECR \(see below\)\.

------
#### [ Quay\.io ]

**Install `cert-manager` using Quay\.io**
+ If your nodes have access to the `quay.io` container registry, install `cert-manager` to inject certificate configuration into the webhooks\. 

  ```
  $ kubectl apply \
      --validate=false \
      -f https://github.com/jetstack/cert-manager/releases/download/v1.13.5/cert-manager.yaml
  ```

------
#### [ Amazon ECR ]

**Install `cert-manager` using Amazon ECR**

1. Install `cert-manager` using one of the following methods to inject certificate configuration into the webhooks\. For more information, see [Getting Started](https://cert-manager.io/docs/installation/#getting-started) on the *`cert-manager` Documentation*\.

1. Download the manifest\.

   ```
   curl -Lo cert-manager.yaml https://github.com/jetstack/cert-manager/releases/download/v1.13.5/cert-manager.yaml
   ```

1. Pull the following images and push them to a repository that your nodes have access to\. For more information on how to pull, tag, and push the images to your own repository, see [Copy a container image from one repository to another repository](copy-image-to-repository.md)\.

   ```
   quay.io/jetstack/cert-manager-cainjector:v1.13.5
   quay.io/jetstack/cert-manager-controller:v1.13.5
   quay.io/jetstack/cert-manager-webhook:v1.13.5
   ```

1. Replace `quay.io` in the manifest for the three images with your own registry name\. The following command assumes that your private repository's name is the same as the source repository\. Replace `111122223333.dkr.ecr.region-code.amazonaws.com` with your private registry\.

   ```
   $ sed -i.bak -e 's|quay.io|111122223333.dkr.ecr.region-code.amazonaws.com|' ./cert-manager.yaml
   ```

1. Apply the manifest\.

   ```
   $ kubectl apply \
       --validate=false \
       -f ./cert-manager.yaml
   ```

------

## Step 3: Install AWS Load Balancer Controller<a name="lbc-install"></a>

**Install AWS Load Balancer Controller using a Kubernetes manifest**

1. Download the controller specification\. For more information about the controller, see the [documentation](https://kubernetes-sigs.github.io/aws-load-balancer-controller/) on GitHub\.

   ```
   curl -Lo v2_7_2_full.yaml https://github.com/kubernetes-sigs/aws-load-balancer-controller/releases/download/v2.7.2/v2_7_2_full.yaml
   ```

1. Make the following edits to the file\.

   1. If you downloaded the `v2_7_2_full.yaml` file, run the following command to remove the `ServiceAccount` section in the manifest\. If you don't remove this section, the required annotation that you made to the service account in a previous step is overwritten\. Removing this section also preserves the service account that you created in a previous step if you delete the controller\.

      ```
      $ sed -i.bak -e '596,604d' ./v2_7_2_full.yaml
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

   1. Replace `your-cluster-name` in the `Deployment` `spec` section of the file with the name of your cluster by replacing `my-cluster` with the name of your cluster\.

      ```
      $ sed -i.bak -e 's|your-cluster-name|my-cluster|' ./v2_7_2_full.yaml
      ```

   1. If your nodes don't have access to the Amazon EKS Amazon ECR image repositories, then you need to pull the following image and push it to a repository that your nodes have access to\. For more information on how to pull, tag, and push an image to your own repository, see [Copy a container image from one repository to another repository](copy-image-to-repository.md)\.

      ```
      public.ecr.aws/eks/aws-load-balancer-controller:v2.7.2
      ```

      Add your registry's name to the manifest\. The following command assumes that your private repository's name is the same as the source repository and adds your private registry's name to the file\. Replace `111122223333.dkr.ecr.region-code.amazonaws.com` with your registry\. This line assumes that you named your private repository the same as the source repository\. If not, change the `eks/aws-load-balancer-controller` text after your private registry name to your repository name\.

      ```
      $ sed -i.bak -e 's|public.ecr.aws/eks/aws-load-balancer-controller|111122223333.dkr.ecr.region-code.amazonaws.com/eks/aws-load-balancer-controller|' ./v2_7_2_full.yaml
      ```

   1. \(Required only for Fargate or Restricted IMDS\) 

      If you're deploying the controller to Amazon EC2 nodes that have [restricted access to the Amazon EC2 instance metadata service \(IMDS\)](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node), or if you're deploying to Fargate, then add the **following parameters** under `- args:`\.

      ```
      [...]
      spec:
            containers:
              - args:
                  - --cluster-name=your-cluster-name
                  - --ingress-class=alb
                  - --aws-vpc-id=vpc-xxxxxxxx
                  - --aws-region=region-code
                  
                  
      [...]
      ```

1. Apply the file\.

   ```
   $ kubectl apply -f v2_7_2_full.yaml
   ```

1. Download the `IngressClass` and `IngressClassParams` manifest to your cluster\.

   ```
   $ curl -Lo v2_7_2_ingclass.yaml https://github.com/kubernetes-sigs/aws-load-balancer-controller/releases/download/v2.7.2/v2_7_2_ingclass.yaml
   ```

1. Apply the manifest to your cluster\.

   ```
   $ kubectl apply -f v2_7_2_ingclass.yaml
   ```

## Step 4: Verify that the controller is installed<a name="lbc-verify"></a><a name="lbc-verify-procedure"></a>

1. Verify that the controller is installed\.

   ```
   $ kubectl get deployment -n kube-system aws-load-balancer-controller
   ```

   An example output is as follows\.

   ```
   NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
   aws-load-balancer-controller   2/2     2            2           84s
   ```

   You receive the previous output if you deployed using Helm\. If you deployed using the Kubernetes manifest, you only have one replica\.

1. Before using the controller to provision AWS resources, your cluster must meet specific requirements\. For more information, see [Application load balancing on Amazon EKS](alb-ingress.md) and [Network load balancing on Amazon EKS](network-load-balancing.md)\.