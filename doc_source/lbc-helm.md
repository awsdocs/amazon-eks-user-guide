# Install the AWS Load Balancer Controller using Helm<a name="lbc-helm"></a>

This topic describes how to install the AWS Load Balancer Controller using Helm, a package manager for Kubernetes, and `eksctl`\. The controller is installed with default options\. For more information about the controller, including details on configuring it with annotations, see the [AWS Load Balancer Controller Documentation](https://kubernetes-sigs.github.io/aws-load-balancer-controller/) on GitHub\. 

In the following steps, replace the `example values` with your own values\.

## Prerequisites<a name="lbc-prereqs"></a>

Before starting this tutorial, you must install and configure the following tools and resources that you need to create and manage an Amazon EKS cluster\. <a name="lbc-prereqs.itemizedlist"></a>
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\.
+ An existing AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ Make sure that your Amazon VPC CNI plugin for Kubernetes, `kube-proxy`, and CoreDNS add\-ons are at the minimum versions listed in [Service account tokens](service-accounts.md#boundserviceaccounttoken-validated-add-on-versions)\.
+ Familiarity with AWS Elastic Load Balancing\. For more information, see the [Elastic Load Balancing User Guide](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/)\.
+ Familiarity with Kubernetes [service](https://kubernetes.io/docs/concepts/services-networking/service/) and [ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) resources\.
+  [Helm](https://helm.sh/docs/helm/helm_install/) installed locally\. 

## Step 1: Create IAM Role using `eksctl`<a name="lbc-helm-iam"></a>

**Note**  
You only need to create an IAM Role for the AWS Load Balancer Controller one per AWS account\. Check if `AmazonEKSLoadBalancerControllerRole` exists in the [IAM Console](https://console.aws.amazon.com/iam)\. If this role exists, skip to [Step 2: Install AWS Load Balancer Controller](#lbc-helm-install)\.<a name="lbc-iam.step1"></a>

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
If you view the policy in the AWS Management Console, the console shows warnings for the **ELB** service, but not for the **ELB v2** service\. This happens because some of the actions in the policy exist for **ELB v2**, but not for **ELB**\. You can ignore the warnings for **ELB**\.<a name="lbc-iam.eksctl"></a>

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

## Step 2: Install AWS Load Balancer Controller<a name="lbc-helm-install"></a>

**Install AWS Load Balancer Controller using [Helm V3](https://helm.sh/)**

1. Add the `eks-charts` Helm chart repository\. AWS maintains [this repository](https://github.com/aws/eks-charts) on GitHub\.

   ```
   $ helm repo add eks https://aws.github.io/eks-charts
   ```

1. Update your local repo to make sure that you have the most recent charts\.

   ```
   $ helm repo update eks
   ```

1. Install the AWS Load Balancer Controller\. 

   Replace `my-cluster` with the name of your cluster\. In the following command, `aws-load-balancer-controller` is the Kubernetes service account that you created in a previous step\.

   For more information about configuring the helm chart, see [https://github.com/aws/eks-charts/blob/master/stable/aws-load-balancer-controller/values.yaml](https://github.com/aws/eks-charts/blob/master/stable/aws-load-balancer-controller/values.yaml) on GitHub\.

   ```
   $ helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
     -n kube-system \
     --set clusterName=my-cluster \
     --set serviceAccount.create=false \
     --set serviceAccount.name=aws-load-balancer-controller
   ```

   1. If you're deploying the controller to Amazon EC2 nodes that have [restricted access to the Amazon EC2 instance metadata service \(IMDS\)](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node), or if you're deploying to Fargate, then add the following flags to the `helm` command that follows:
      + `--set region=region-code`
      + `--set vpcId=vpc-xxxxxxxx`

   1. To view the available versions of the Helm Chart and Load Balancer Controller, use the following command:

      ```
      helm search repo eks/aws-load-balancer-controller --versions
      ```
**Important**  
The deployed chart doesn't receive security updates automatically\. You need to manually upgrade to a newer chart when it becomes available\. When upgrading, change `install` to `upgrade` in the previous command\.  
The `helm install` command automatically installs the custom resource definitions \(CRDs\) for the controller\. The `helm upgrade` command does not\. If you use `helm upgrade,` you must manually install the CRDs\. Run the following command to install the CRDs:  

   ```
   wget https://raw.githubusercontent.com/aws/eks-charts/master/stable/aws-load-balancer-controller/crds/crds.yaml 
   kubectl apply -f crds.yaml
   ```

## Step 3: Verify that the controller is installed<a name="lbc-helm-verify"></a><a name="lbc-verify-procedure"></a>

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