# CNI metrics helper<a name="cni-metrics-helper"></a>

The CNI metrics helper is a tool that you can use to scrape network interface and IP address information, aggregate metrics at the cluster level, and publish the metrics to Amazon CloudWatch\. To learn more about the metrics helper, see [cni\-metrics\-helper](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/cmd/cni-metrics-helper/README.md) on GitHub\.

When managing an Amazon EKS cluster, you may want to know how many IP addresses have been assigned and how many are available\. The CNI metrics helper helps you to:
+ Track these metrics over time
+ Troubleshoot and diagnose issues related to IP assignment and reclamation
+ Provide insights for capacity planning

When a node is provisioned, the CNI plugin automatically allocates a pool of secondary IP addresses from the node’s subnet to the primary network interface \(`eth0`\)\. This pool of IP addresses is known as the *warm pool*, and its size is determined by the node’s instance type\. For example, a `c4.large` instance can support three network interfaces and nine IP addresses per interface\. The number of IP addresses available for a given pod is one less than the maximum \(of ten\) because one of the IP addresses is reserved for the elastic network interface itself\. For more information, see [IP Addresses Per Network Interface Per Instance Type](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#AvailableIpPerENI) in the *Amazon EC2 User Guide for Linux Instances*\.

As the pool of IP addresses is depleted, the plugin automatically attaches another elastic network interface to the instance and allocates another set of secondary IP addresses to that interface\. This process continues until the node can no longer support additional elastic network interfaces\.

The following metrics are collected for your cluster and exported to CloudWatch:
+ The maximum number of network interfaces that the cluster can support
+ The number of network interfaces have been allocated to pods
+ The number of IP addresses currently assigned to pods
+ The total and maximum numbers of IP addresses available
+ The number of ipamD errors

**Prerequisites**
+ An existing AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ Version 2\.3\.7 or later or 1\.22\.8 or later of the AWS CLI installed and configured on your computer or AWS CloudShell\. For more information, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with `aws configure`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config)in the AWS Command Line Interface User Guide\. 
+ The `kubectl` command line tool installed on your computer or AWS CloudShell\. The version must be the same, or up to two versions later than your cluster version\. To install or upgrade `kubectl`, see [Installing `kubectl`](install-kubectl.md)\.

## Deploy the CNI metrics helper<a name="efs-create-iam-resources"></a>

Create an IAM policy and role and deploy the metrics helper\.

**To deploy the CNI metrics helper**

1. Create an IAM policy that grants the CNI metrics helper `cloudwatch:PutMetricData` permissions to send metric data to CloudWatch\. 

   1. Copy the following contents to a file named `cni-metrics-helper-policy.json`\.

      ```
      {
          "Version": "2012-10-17",
          "Statement": [
              {
                  "Effect": "Allow",
                  "Action": [
                      "cloudwatch:PutMetricData"
                  ],
                  "Resource": "*"
              }
          ]
      }
      ```

   1. Create an IAM policy named `AmazonEKSVPCCNIMetricsHelperPolicy`\.

      ```
      aws iam create-policy --policy-name AmazonEKSVPCCNIMetricsHelperPolicy \
          --description "Grants permission to write metrics to CloudWatch" \
          --policy-document file://cni-metrics-helper-policy.json
      ```

1. Create an IAM role and attach the IAM policy to it\. Create a Kubernetes service account\. Annotate the Kubernetes service account with the IAM role ARN and the IAM role with the Kubernetes service account name\. You can create the role using `eksctl` or the AWS CLI\.

------
#### [ eksctl ]

   Run the following command to create the IAM role\. If you don't have an IAM OIDC provider for your cluster, the command also creates the IAM OIDC provider\. Replace `my-cluster` with your cluster name, `111122223333` with your account ID, and `region-code` with the Region that your cluster is in\. 

   ```
   eksctl create iamserviceaccount \
       --name cni-metrics-helper \
       --namespace kube-system \
       --cluster my-cluster \
       --attach-policy-arn arn:aws:iam::111122223333:policy/AmazonEKSVPCCNIMetricsHelperPolicy \
       --approve \
       --override-existing-serviceaccounts \
       --region region-code
   ```

------
#### [ AWS CLI ]

   1. Determine your cluster's OIDC provider URL\. Replace `my-cluster` with your cluster name\. If the output from the command is `None`, review the **Prerequisites**\.

      ```
      aws eks describe-cluster --name my-cluster --query "cluster.identity.oidc.issuer" --output text
      ```

      Output

      ```
      https://oidc.eks.region-code.amazonaws.com/id/oidc-id
      ```

   1. Create the IAM role, granting the Kubernetes service account the `AssumeRoleWithWebIdentity` action\.

      1. Copy the following contents to a file named `trust-policy.json`\. Replace `111122223333` with your account ID\. Replace `oidc-id` and `region-code` with the values returned in the previous step\.

         ```
         {
           "Version": "2012-10-17",
           "Statement": [
             {
               "Effect": "Allow",
               "Principal": {
                 "Federated": "arn:aws:iam::111122223333:oidc-provider/oidc.eks.region-code.amazonaws.com/id/oidc-id"
               },
               "Action": "sts:AssumeRoleWithWebIdentity",
               "Condition": {
                 "StringEquals": {
                   "oidc.eks.region-code.amazonaws.com/id/oidc-id:sub": "system:serviceaccount:kube-system:cni-metrics-helper"
                 }
               }
             }
           ]
         }
         ```

      1. Create the role\.

         ```
         aws iam create-role \
           --role-name AmazonEKSVPCCNIMetricsHelperRole \
           --assume-role-policy-document file://"trust-policy.json"
         ```

   1. Attach the IAM policy to the role\. Replace `111122223333` with your account ID\.

      ```
      aws iam attach-role-policy \
        --policy-arn arn:aws:iam::111122223333:policy/AmazonEKSVPCCNIMetricsHelperPolicy \
        --role-name AmazonEKSVPCCNIMetricsHelperRole
      ```

------

1. Apply the CNI metrics helper manifest to your cluster\.

   ```
   kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/master/config/master/cni-metrics-helper.yaml
   ```

   The previous command assumes that you are using the latest version of the Amazon VPC CNI add\-on\. To use a specific version, replace the URL with the following URL\. Replace *1\.9* with the version of the CNI add\-on that you're using\.

   ```
   https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.9/config/v1.9/cni-metrics-helper.yaml
   ```

1. Annotate the `cni-metrics-helper` Kubernetes service account created in the previous step with the ARN of the IAM role that you created previously\. Use the command that matches the tool that you used to create the role in a previous step\. Replace `111122223333` with your account ID\.
   + If you used `eksctl` to create the role, use this command\.

     ```
     kubectl annotate serviceaccount cni-metrics-helper \
         -n kube-system \
         eks.amazonaws.com/role-arn=arn:aws:iam::111122223333:role/eksctl-my-cluster-addon-iamserviceaccount-kube-sy-Role1-1J7XB63IN3L6T
     ```
   + If you used AWS CLI to create the role, use this command\.

     ```
     kubectl annotate serviceaccount cni-metrics-helper \
         -n kube-system \
         eks.amazonaws.com/role-arn=arn:aws:iam::111122223333:role/AmazonEKSVPCCNIMetricsHelperRole
     ```

1. Restart the `cni-metrics-helper` deployment\.

   ```
   kubectl rollout restart \
       deployment cni-metrics-helper \
       -n kube-system
   ```

## Creating a metrics dashboard<a name="create-metrics-dashboard"></a>

After you have deployed the CNI metrics helper, you can view the CNI metrics in the CloudWatch console\. This topic helps you to create a dashboard for viewing your cluster's CNI metrics\.

**To create a CNI metrics dashboard**

1. Open the CloudWatch console at [https://console\.aws\.amazon\.com/cloudwatch/](https://console.aws.amazon.com/cloudwatch/)\.

1. In the left navigation, select **Metrics** and then select **All metrics**\.

1. Under **Custom Namespaces**, select **Kubernetes**\.

1. Select **CLUSTER\_ID**\.

1. On the **Metrics** tab, select the metrics you want to add to the dashboard\.

1. At the top right of the console, select **Actions**, and then **Add to dashboard**\.

1. In the **Select a dashboard** section, select **Create new**, enter a name for your dashboard, such as **EKS\-CNI\-metrics**, and then select **Create**\.

1. In the **Widget type** section, select **Number**\.

1. In the **Customize widget title** section, enter a logical name for your dashboard title, such as **EKS CNI metrics**\.

1. Select **Add to dashboard** to finish\. Now your CNI metrics are added to a dashboard that you can monitor, as shown below\.  
![\[EKS CNI metrics\]](http://docs.aws.amazon.com/eks/latest/userguide/images/EKS_CNI_metrics.png)