# Walkthrough: Updating the VPC CNI plugin to use IAM roles for service accounts<a name="iam-roles-for-service-accounts-cni-walkthrough"></a>

The [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) is the networking plugin for pod networking in Amazon EKS clusters\. The CNI plugin is responsible for allocating VPC IP addresses to Kubernetes nodes and configuring the necessary networking for pods on each node\. The plugin requires IAM permissions, provided by the AWS managed policy `[AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor)`, to make calls to AWS APIs on your behalf\. By default, this policy is attached to your node IAM role\. However, using this method, all pods on the nodes have the same permissions as the CNI plugin\. You can use the IAM roles for service accounts feature to provide the `[AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor)` permissions, and then remove the policy from the node IAM role\.

For ease of use, this topic uses `eksctl` to configure IAM roles for service accounts\. However, if you would rather use the AWS Management Console, the AWS CLI, or one of the AWS SDKs, the same basic concepts apply, but you will have to modify the steps to use the procedures in [Enabling IAM roles for service accounts on your cluster](enable-iam-roles-for-service-accounts.md)\.

**To configure the CNI plugin to use IAM roles for service accounts**

1. Check your `eksctl` version with the following command\. This procedure assumes that you have installed `eksctl` and that your `eksctl` version is at least `0.31.0-rc.0`\. 

   ```
   eksctl version
   ```

    For more information about installing or upgrading `eksctl`, see [Installing or upgrading `eksctl`](eksctl.md#installing-eksctl)\.

1. If your cluster isn't in a China Region, or your cluster runs at least Kubernetes `1.18` \(in any region\), skip this step\. Describe one of the pods and verify that the `AWS_DEFAULT_REGION` environment variable exists\.

   ```
   kubectl exec -n kube-system aws-node-<9rgzw> env | grep AWS
   ```

   Output:

   ```
   ...
   AWS_DEFAULT_REGION=<region-code>
   ```

   If the variable does not exist, you need to use the following command to add the variable to each of your pods that uses IAM roles for service accounts\.

   ```
   kubectl set env daemonset aws-node -n kube-system AWS_DEFAULT_REGION=<region-code>
   ```

1. Check the version of your cluster's Amazon VPC CNI Plugin for Kubernetes\. Use the following command to print your cluster's CNI version\.

   ```
   kubectl describe daemonset aws-node --namespace kube-system | grep Image | cut -d "/" -f 2
   ```

   Output:

   ```
   amazon-k8s-cni:<1.6.3>
   ```

   If your CNI version is earlier than 1\.7\.5, complete the following steps to create a service account and then upgrade your CNI version to the latest version:

   1. Create an OIDC identity provider for your cluster with the following command\. Substitute the cluster name with your own value\.

      ```
      eksctl utils associate-iam-oidc-provider --cluster <cluster_name> --approve
      ```

   1. Create a Kubernetes service account with the following command\. Replace `<cluster_name>` \(including `<>`\) with your own value\. This command deploys an AWS CloudFormation stack that creates an IAM role, attaches the `AmazonEKS_CNI_Policy` AWS managed policy to it, and binds the IAM role to the service account\. 

      ```
      eksctl create iamserviceaccount \
          --name aws-node \
          --namespace kube-system \
          --cluster <cluster_name> \
          --attach-policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy \
          --approve \
          --override-existing-serviceaccounts
      ```

   1. Upgrade your CNI version to the latest version by completing the instructions in the option that corresponds to the Region that your cluster is in\.
      + All Regions other than Beijing and Ningxia China

        Upgrade your CNI version to the latest version\. The manifest specifies the `aws-node` service account that you created in the previous step\.

        ```
        kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.7/config/v1.7/aws-k8s-cni.yaml
        ```
      + Beijing and Ningxia China

        1. Download the latest version of the CNI manifest with the following command\.

           ```
           curl -o aws-k8s-cni-cn.yaml https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/master/config/v1.7/aws-k8s-cni-cn.yaml
           ```

        1. If your cluster is version 1\.17 or earlier, edit the `aws-k8s-cni-cn.yaml` file\. In the following portion of the file, add the `AWS_DEFAULT_REGION` environment variable\.

           ```
           env:
             - name: AWS_VPC_K8S_CNI_LOGLEVEL
               value: DEBUG
             - name: AWS_VPC_K8S_CNI_VETHPREFIX
               value: eni
             - name: AWS_VPC_ENI_MTU
               value: "9001"
             - name: AWS_DEFAULT_REGION
               value: <region-code>
           ```

        1. Upgrade your CNI version to the latest version\. The manifest specifies the `aws-node` service account that your created in a previous step\.

           ```
           kubectl apply -f aws-k8s-cni-cn.yaml
           ```

1. Watch the roll out, and wait for the `DESIRED` count of the deployment to match the `UP-TO-DATE` count\. Press **Ctrl \+ c** to exit\. 

   ```
   kubectl get -n kube-system daemonset.apps/aws-node --watch
   ```

1. List the pods in the `aws-node` DaemonSet\.

   ```
   kubectl get pods -n kube-system  -l k8s-app=aws-node
   ```

   Output:

   ```
   NAME             READY   STATUS        RESTARTS   AGE
   aws-node-mp88b   1/1     Running       0          17m
   aws-node-n4tcd   1/1     Running       0          20s
   aws-node-qt9dl   1/1     Running       0          17m
   ```

1. Check the version of your cluster's Amazon VPC CNI Plugin for Kubernetes again, confirming that the version is 1\.7\.5\. 

   ```
   kubectl describe daemonset aws-node --namespace kube-system | grep Image | cut -d "/" -f 2
   ```

   Output:

   ```
   amazon-k8s-cni:<1.7.5>
   ```

1. Describe one of the pods and verify that the `AWS_WEB_IDENTITY_TOKEN_FILE` and `AWS_ROLE_ARN` environment variables exist\.

   ```
   kubectl exec -n kube-system aws-node-<9rgzw> env | grep AWS
   ```

   Output:

   ```
   AWS_VPC_K8S_CNI_LOGLEVEL=DEBUG
   AWS_ROLE_ARN=arn:aws:iam::<111122223333>:role/eksctl-prod-addon-iamserviceaccount-kube-sys-Role1-<V66K5I6JLDGK>
   AWS_WEB_IDENTITY_TOKEN_FILE=/var/run/secrets/eks.amazonaws.com/serviceaccount/token
   ```

   The IAM role was created by `eksctl` when you created the Kubernetes service account in a previous step\.

1. Remove the `[AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor)` policy from your node IAM role\.

   1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

   1. In the left navigation, choose **Roles**, and then search for your node instance role\.

   1. Choose the **Permissions** tab for your node instance role and then choose the **X** to the right of the `[AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor)`\.

   1. Choose **Detach** to finish\.

Now your CNI plug\-in pods are getting their IAM permissions from their own role\. The pods also have access to the permissions assigned to the [Amazon EKS node IAM role](create-node-role.md), unless you block access to IMDS\. For more information, see [Restricting access to the IMDS and Amazon EC2 instance profile credentials](best-practices-security.md#restrict-ec2-credential-access)\.