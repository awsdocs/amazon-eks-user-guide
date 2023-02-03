# Installing or updating the Amazon VPC CNI plugin for Kubernetes metrics helper add\-on<a name="cni-metrics-helper"></a>

The Amazon VPC CNI plugin for Kubernetes metrics helper is a tool that you can use to scrape network interface and IP address information, aggregate metrics at the cluster level, and publish the metrics to Amazon CloudWatch\. To learn more about the metrics helper, see [cni\-metrics\-helper](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/cmd/cni-metrics-helper/README.md) on GitHub\.

When managing an Amazon EKS cluster, you might want to know how many IP addresses have been assigned and how many are available\. The Amazon VPC CNI plugin for Kubernetes metrics helper helps you to:
+ Track these metrics over time
+ Troubleshoot and diagnose issues related to IP assignment and reclamation
+ Provide insights for capacity planning

When a node is provisioned, the Amazon VPC CNI plugin for Kubernetes automatically allocates a pool of secondary IP addresses from the node's subnet to the primary network interface \(`eth0`\)\. This pool of IP addresses is known as the *warm pool*, and its size is determined by the node's instance type\. For example, a `c4.large` instance can support three network interfaces and nine IP addresses per interface\. The number of IP addresses available for a given pod is one less than the maximum \(of ten\) because one of the IP addresses is reserved for the elastic network interface itself\. For more information, see [IP Addresses Per Network Interface Per Instance Type](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#AvailableIpPerENI) in the *Amazon EC2 User Guide for Linux Instances*\.

As the pool of IP addresses is depleted, the plugin automatically attaches another elastic network interface to the instance and allocates another set of secondary IP addresses to that interface\. This process continues until the node can no longer support additional elastic network interfaces\.

The following metrics are collected for your cluster and exported to CloudWatch:
+ The maximum number of network interfaces that the cluster can support
+ The number of network interfaces have been allocated to pods
+ The number of IP addresses currently assigned to pods
+ The total and maximum numbers of IP addresses available
+ The number of ipamD errors

**Prerequisites**
+ An existing AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see [Creating an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ Version `2.9.20` or later or `1.27.63` or later of the AWS CLI installed and configured on your device or AWS CloudShell\. You can check your current version with `aws --version | cut -d / -f2 | cut -d ' ' -f1`\. Package managers such `yum`, `apt-get`, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI\. To install the latest version, see [ Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with `aws configure`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the AWS Command Line Interface User Guide\. The AWS CLI version installed in the AWS CloudShell may also be several versions behind the latest version\. To update it, see [ Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the AWS CloudShell User Guide\.
+ The `kubectl` command line tool is installed on your device or AWS CloudShell\. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster\. For example, if your cluster version is `1.23`, you can use `kubectl` version `1.22`, `1.23`, or `1.24` with it\. To install or upgrade `kubectl`, see [Installing or updating `kubectl`](install-kubectl.md)\.
+ If your cluster is `1.21` or later, make sure that your Amazon VPC CNI plugin for Kubernetes, `kube-proxy`, and CoreDNS add\-ons are at the minimum versions listed in [Service account tokens](service-accounts.md#boundserviceaccounttoken-validated-add-on-versions)\.

## Deploy or update the CNI metrics helper<a name="efs-create-iam-resources"></a>

Create an IAM policy and role and deploy the metrics helper\. If you previously created an IAM role for the add\-on's service account to use you can skip to the [Determine the version of the Amazon VPC CNI plugin for Kubernetes that's installed on your cluster](#cni-metrics-helper-determine-plugin-version) step\.

**To deploy the CNI metrics helper**

1. Create an IAM policy that grants the CNI metrics helper `cloudwatch:PutMetricData` permissions to send metric data to CloudWatch\. 

   1. Run the following command to create a file named `cni-metrics-helper-policy.json`\.

      ```
      cat >cni-metrics-helper-policy.json <<EOF
      {
          "Version": "2012-10-17",
          "Statement": [
              {
                  "Effect": "Allow",
                  "Action": [
                      "cloudwatch:PutMetricData",
                      "ec2:DescribeTags"
                  ],
                  "Resource": "*"
              }
          ]
      }
      EOF
      ```

   1. Create an IAM policy named `AmazonEKSVPCCNIMetricsHelperPolicy`\.

      ```
      aws iam create-policy --policy-name AmazonEKSVPCCNIMetricsHelperPolicy \
          --description "Grants permission to write metrics to CloudWatch" \
          --policy-document file://cni-metrics-helper-policy.json
      ```

1. Retrieve your AWS account ID and store it in a variable\.

   ```
   account_id=$(aws sts get-caller-identity --query Account --output text)
   ```

   Confirm that the variable is set\.

   ```
   echo $account_id
   ```

   The example output is as follows\.

   ```
   111122223333
   ```

1. Create an IAM role and attach the IAM policy to it\. Create a Kubernetes service account\. Annotate the Kubernetes service account with the IAM role ARN and the IAM role with the Kubernetes service account name\. You can create the role using `eksctl` or the AWS CLI\.

------
#### [ eksctl ]

   Run the following command to create the IAM role\. You can replace *AmazonEKSVPCCNIMetricsHelperRole\-my\-cluster* with any name you choose, but we recommend including the name of the cluster that you'll use this role with in the role name\. Replace `my-cluster` with the name of your cluster\. 

   ```
   eksctl create iamserviceaccount \
       --name cni-metrics-helper \
       --namespace kube-system \
       --cluster my-cluster \
       --role-name "AmazonEKSVPCCNIMetricsHelperRole-my-cluster" \
       --attach-policy-arn arn:aws:iam::$account_id:policy/AmazonEKSVPCCNIMetricsHelperPolicy \
       --approve
   ```

------
#### [ AWS CLI ]

   1. Retrieve your cluster's OIDC provider URL and store it in a variable\. Replace `my-cluster` with your cluster name\.

      ```
      oidc_issuer=$(aws eks describe-cluster --name my-cluster --query "cluster.identity.oidc.issuer" --output text | cut -c9-)
      ```

      Confirm that the variable is set\.

      ```
      echo $oidc_issuer
      ```

      The example output is as follows\.

      ```
      oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE
      ```

   1. Create an IAM role, granting the Kubernetes service account the `AssumeRoleWithWebIdentity` action\.

      1. Create a trust policy file named `trust-policy.json`\.

         ```
         cat >trust-policy.json <<EOF
         {
           "Version": "2012-10-17",
           "Statement": [
             {
               "Effect": "Allow",
               "Principal": {
                 "Federated": "arn:aws:iam::$account_id:oidc-provider/$oidc_issuer"
               },
               "Action": "sts:AssumeRoleWithWebIdentity",
               "Condition": {
                 "StringEquals": {
                   "$oidc_issuer:aud": "sts.amazonaws.com",
                   "$oidc_issuer:sub": "system:serviceaccount:kube-system:cni-metrics-helper"
                 }
               }
             }
           ]
         }
         EOF
         ```

      1. Create the role\. You can replace *AmazonEKSVPCCNIMetricsHelperRole\-my\-cluster* with any name you choose, but we recommend including the name of the cluster that you'll use this role with in the role name\.

         ```
         aws iam create-role \
           --role-name AmazonEKSVPCCNIMetricsHelperRole-my-cluster \
           --assume-role-policy-document file://"trust-policy.json"
         ```

   1. Attach the IAM policy to the role\.

      ```
      aws iam attach-role-policy \
        --policy-arn arn:aws:iam::$account_id:policy/AmazonEKSVPCCNIMetricsHelperPolicy \
        --role-name AmazonEKSVPCCNIMetricsHelperRole-my-cluster
      ```

------

1. Verify that the role you created is configured correctly\.

   1. Verify the trust policy for the role\.

      ```
      aws iam get-role --role-name AmazonEKSVPCCNIMetricsHelperRole-my-cluster --query Role.AssumeRolePolicyDocument.Statement[]
      ```

      The example output is as follows\.

      ```
      [
          {
              "Effect": "Allow",
              "Principal": {
                  "Federated": "arn:aws:iam::oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE"
              },
              "Action": "sts:AssumeRoleWithWebIdentity",
              "Condition": {
                  "StringEquals": {
                      "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:sub": "system:serviceaccount:kube-system:cni-metrics-helper",
                      "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:aud": "sts.amazonaws.com"
                  }
              }
          }
      ]
      ```

   1. Verify that your cluster's OIDC provider matches the provider returned in the previous step\.

      ```
      aws eks describe-cluster --name my-cluster --query "cluster.identity.oidc.issuer" --output text | cut -c9-
      ```

      The example output is as follows\.

      ```
      oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE
      ```

1. Determine the version of the Amazon VPC CNI plugin for Kubernetes that's installed on your cluster\.

   ```
   kubectl describe daemonset aws-node -n kube-system | grep amazon-k8s-cni: | cut -d ":" -f3 | cut -d "v" -f2 | cut -d "-" -f1
   ```

   The example output is as follows\.

   ```
   1.11.4
   ```

   In the previous output, `1` is the major version, `11` is the minor version, and `4` is the patch version\.

1. To add the same version of the CNI metrics helper to your cluster \(or to update to the same version\) as your Amazon VPC CNI plugin for Kubernetes, run the following command for the AWS Region that your cluster is in\.
**Important**  
You can only update one minor version at a time\. For example, if your current minor version is `1.10` and you want to update to `1.12`, then you must update to `1.11` first, then update to `1.12`\. You can however, update more than one patch version at a time\. For example, you can update directly from `1.11.2` to `1.11.4`\. If you need to update to a version that is earlier or later than the version listed in the following commands, then see [Releases](https://github.com/aws/amazon-vpc-cni-k8s/releases) on GitHub\. The URL for each version is listed in the `To apply this release:` section of the release note\. Replace the *portion* of the following URLs with the same portion of the URL in the release note\. 

   AWS GovCloud \(US\-East\) \(`us-gov-east-1`\)

   ```
   kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/v1.12.1/config/master/cni-metrics-helper-us-gov-east-1.yaml
   ```

   AWS GovCloud \(US\-West\) \(`us-gov-west-1`\)

   ```
   kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/v1.12.1/config/master/cni-metrics-helper-us-gov-west-1.yaml
   ```

   All other AWS Regions

   1. Download the manifest file\.

      ```
      curl -O https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/v1.12.1/config/master/cni-metrics-helper.yaml
      ```

   1. If your cluster isn't in `us-west-2`, then replace `region-code` in the following command with the AWS Region that your cluster is in and then run the modified command to replace `us-west-2` in the file with your AWS Region\.

      ```
      sed -i.bak -e 's/us-west-2/region-code/' cni-metrics-helper.yaml
      ```

   1. If your cluster isn't in `us-west-2`, then replace `602401143452` in the following command with the account from [Amazon container image registries](add-ons-images.md) for the AWS Region that your cluster is in and then run the modified command to replace `602401143452` in the file\.

      ```
      sed -i.bak -e 's/602401143452/602401143452/' cni-metrics-helper.yaml
      ```

   1. Apply the manifest file to your cluster\.

      ```
      kubectl apply -f cni-metrics-helper.yaml
      ```

1. If you previously configured an IAM role for the add\-on's service account to use you can skip to the [Restart the cni\-metrics\-helper deployment](#cni-metrics-helper-restart) step\.

   Annotate the `cni-metrics-helper` Kubernetes service account created in a previous step with the ARN of the IAM role that you created previously\. Replace `my-cluster` with your cluster name and `AmazonEKSVPCCNIMetricsHelperRole-my-cluster` with the name of the IAM role that you created in a previous step\.

   ```
   kubectl annotate serviceaccount cni-metrics-helper -n kube-system \
       eks.amazonaws.com/role-arn=arn:aws:iam::$account_id:role/AmazonEKSVPCCNIMetricsHelperRole-my-cluster
   ```

1. \(Optional\) Configure the AWS Security Token Service endpoint type used by your Kubernetes service account\. For more information, see [Configuring the AWS Security Token Service endpoint for a service account](configure-sts-endpoint.md)\.

1. Restart the `cni-metrics-helper` deployment\.

   ```
   kubectl rollout restart deployment cni-metrics-helper -n kube-system
   ```

1. Confirm the version of the metrics helper that you deployed\.

   ```
   kubectl describe deployment cni-metrics-helper -n kube-system | grep cni-metrics-helper: | cut -d ":" -f 3
   ```

   The example output is as follows\.

   ```
   v1.12.1
   ```

## Creating a metrics dashboard<a name="create-metrics-dashboard"></a>

After you have deployed the CNI metrics helper, you can view the CNI metrics in the Amazon CloudWatch console\. This topic helps you to create a dashboard for viewing your cluster's CNI metrics\.

**To create a CNI metrics dashboard**

1. Open the CloudWatch console at [https://console\.aws\.amazon\.com/cloudwatch/](https://console.aws.amazon.com/cloudwatch/)\.

1. In the left navigation pane, choose **Metrics** and then select **All metrics**\.

1. Choose the **Graphed metrics** tab\.

1. Choose **Add metrics using browse or query**\.

1. Make sure that under **Metrics**, you've selected the AWS Region for your cluster\.

1. In the Search box, enter **Kubernetes** and then press **Enter**\.

1. Select the metrics that you want to add to the dashboard\.

1. At the upper right of the console, select **Actions**, and then **Add to dashboard**\.

1. In the **Select a dashboard** section, choose **Create new**, enter a name for your dashboard, such as **EKS\-CNI\-metrics**, and then choose **Create**\.

1. In the **Widget type** section, select **Number**\.

1. In the **Customize widget title** section, enter a logical name for your dashboard title, such as **EKS CNI metrics**\.

1. Choose **Add to dashboard** to finish\. Now your CNI metrics are added to a dashboard that you can monitor\. For more information about Amazon CloudWatch Logs metrics, see [Using Amazon CloudWatch metrics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/working_with_metrics.html) in the Amazon CloudWatch User Guide\.  
![\[EKS CNI metrics\]](http://docs.aws.amazon.com/eks/latest/userguide/images/EKS_CNI_metrics.png)