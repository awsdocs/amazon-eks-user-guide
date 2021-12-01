# Configuring the Amazon VPC CNI plugin to use IAM roles for service accounts<a name="cni-iam-role"></a>

The [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-k8s) is the networking plugin for pod networking in Amazon EKS clusters\. The plugin is responsible for allocating VPC IP addresses to Kubernetes nodes and configuring the necessary networking for pods on each node\. The plugin:
+ Requires IAM permissions, provided by the AWS managed policy `[AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor)`, to make calls to AWS APIs on your behalf\. You can attach this policy to the [Amazon EKS node IAM role](create-node-role.md), or to a separate IAM role\. We recommend that you assign it to a separate role, as detailed in this topic\.
+ Creates and is configured to use a service account named `aws-node` when it's deployed\. The service account is bound to a Kubernetes `clusterrole` named `aws-node`, which is assigned the required Kubernetes permissions\.

**Note**  
Regardless of whether you configure the VPC CNI plugin to use IAM roles for service accounts, the pods also have access to the permissions assigned to the [Amazon EKS node IAM role](create-node-role.md), unless you block access to IMDS\. For more information, see [Restrict access to the instance profile assigned to the worker node](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node)\.

You can use `eksctl` or the AWS Management Console to create your CNI plugin IAM role\.

------
#### [ eksctl ]

1. Create an IAM role and attach the `AmazonEKS_CNI_Policy` managed IAM policy with the following command\. Replace *`cluster_name`* with your own value\. This command creates an IAM OIDC provider for your cluster if it doesn't already exist\. It then deploys an AWS CloudFormation stack that creates an IAM role, attaches the `AmazonEKS_CNI_Policy` AWS managed policy to it, and annotates the existing `aws-node` service account with the ARN of the IAM role\. 

   ```
   eksctl create iamserviceaccount \
       --name aws-node \
       --namespace kube-system \
       --cluster cluster_name \
       --attach-policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy \
       --approve \
       --override-existing-serviceaccounts
   ```

1. Describe one of the pods and verify that the `AWS_WEB_IDENTITY_TOKEN_FILE` and `AWS_ROLE_ARN` environment variables exist\.

   ```
   kubectl exec -n kube-system aws-node-9rgzw -c aws-node -- env | grep AWS
   ```

   Output:

   ```
   ...
   AWS_WEB_IDENTITY_TOKEN_FILE=/var/run/secrets/eks.amazonaws.com/serviceaccount/token
   ...
   AWS_ROLE_ARN=arn:arn:aws::111122223333:role/eksctl-prod-addon-iamserviceaccount-kube-sys-Role1-V66K5I6JLDGK
   
   ...
   ```

------
#### [ AWS Management Console ]

**Prerequisite**  
You must have an existing IAM OIDC provider for your cluster\. To determine whether you already do or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.<a name="configure-cni-iam-console-create-iam-account"></a>

**To create your CNI plugin IAM role with the AWS Management Console**

1. In the navigation panel, choose **Roles**, **Create Role**\.

1. In the **Select type of trusted entity** section, choose **Web identity**\.

1. In the **Choose a web identity provider** section:

   1. For **Identity provider**, choose the URL for your cluster\.

   1. For **Audience**, choose `sts.amazonaws.com`\.

1. Choose **Next: Permissions**\.

1. In the **Attach Policy** section, select the `[AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor)` policy to use for your service account\.

1. Choose **Next: Tags**\.

1. On the **Add tags \(optional\)** screen, you can add tags for the account\. Choose **Next: Review**\.

1. For **Role Name**, enter a name for your role, such as *`AmazonEKSCNIRole`*, and then choose **Create Role**\.

1. After the role is created, choose the role in the console to open it for editing\.

1. Choose the **Trust relationships** tab, and then choose **Edit trust relationship**\.

1. Find the line that looks similar to the following:

   ```
   "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E:aud": "sts.amazonaws.com"
   ```

   Change the line to look like the following line\. Replace *`EXAMPLED539D4633E53DE1B716D3041E`* wih your cluster's OIDC provider ID, replace *region\-code* with the Region code that your cluster is in, and be sure to change `aud` \(from the previous output\) to `sub` in the following string\.

   ```
   "oidc.eks.<region-code>.amazonaws.com/id/<EXAMPLED539D4633E53DE1B716D3041E>:sub": "system:serviceaccount:kube-system:aws-node"
   ```

1. Choose **Update Trust Policy** to finish\.<a name="configure-cni-iam-console-patch-service-account"></a>

**To annotate the `aws-node` Kubernetes service account with the IAM role**

1. If you're using the Amazon EKS add\-on with a 1\.18 or later Amazon EKS cluster, see [Updating the Amazon VPC CNI Amazon EKS add\-on](managing-vpc-cni.md#updating-vpc-cni-eks-add-on), instead of completing this procedure\. If you're not using the Amazon VPC CNI Amazon EKS add\-on, then use the following command to annotate the `aws-node` service account with the ARN of the IAM role that you created previously\. Replace the `example values` with your own values\.

   ```
   kubectl annotate serviceaccount \
       -n kube-system aws-node \
       eks.amazonaws.com/role-arn=arn:aws:iam::AWS_ACCOUNT_ID:role/AmazonEKSCNIRole
   ```

1. Delete and re\-create any existing pods that are associated with the service account to apply the credential environment variables\. The mutating web hook does not apply them to pods that are already running\. The following command deletes the existing the `aws-node` DaemonSet pods and deploys them with the service account annotation\.

   ```
   kubectl delete pods -n kube-system -l k8s-app=aws-node
   ```

1. Confirm that the pods all restarted\.

   ```
   kubectl get pods -n kube-system  -l k8s-app=aws-node
   ```

1. Describe one of the pods and verify that the `AWS_WEB_IDENTITY_TOKEN_FILE` and `AWS_ROLE_ARN` environment variables exist\.

   ```
   kubectl exec -n kube-system aws-node-9rgzw -c aws-node -- env | grep AWS
   ```

   Output:

   ```
   ...
   AWS_WEB_IDENTITY_TOKEN_FILE=/var/run/secrets/eks.amazonaws.com/serviceaccount/token
   ...
   AWS_ROLE_ARN=arn:arn:aws::111122223333:role/eksctl-prod-addon-iamserviceaccount-kube-sys-Role1-V66K5I6JLDGK
   
   ...
   ```

------

## Remove the CNI policy from the node IAM role<a name="remove-cni-policy-node-iam-role"></a>

If your [Amazon EKS node IAM role](create-node-role.md) currently has the `AmazonEKS_CNI_Policy` IAM policy attached to it, and you've created a separate IAM role, attached the policy to it instead, and assigned it to the `aws-node` Kubernetes service account, then we recommend that you remove the policy from your node role\.

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

1. In the left navigation, choose **Roles**, and then search for your node instance role\.

1. Choose the **Permissions** tab for your node instance role and then choose the **X** to the right of the `[AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor)`\.

1. Choose **Detach** to finish\.