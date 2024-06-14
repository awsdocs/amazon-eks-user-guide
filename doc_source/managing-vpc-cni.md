--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Working with the Amazon VPC CNI plugin for Kubernetes Amazon EKS add\-on<a name="managing-vpc-cni"></a>

The Amazon VPC CNI plugin for  Kubernetes add\-on is deployed on each Amazon EC2 node in your Amazon EKS cluster\. The add\-on creates [https://docs\.aws\.amazon\.com/](https://docs.aws.amazon.com/) AWSEC2/latest/UserGuide/using\-eni\.html\[elastic network interfaces\] and attaches them to your Amazon EC2 nodes\. The add\-on also assigns a private `IPv4`or `IPv6` address from your VPC to each Pod and service\.

The following table lists the latest available version of the Amazon EKS add\-on type for each Kubernetes version\. 

**Important**  

**Important**  
To upgrade to VPC CNI v1\.12\.0 or later, you must upgrade to VPC CNI v1\.7\.0 first\. We recommend that you update one minor version at a time\.  
====   
An existing Amazon EKS cluster\. To deploy one, see \.
An existing AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see \.
IMPORTANT: Amazon VPC CNI plugin for  Kubernetes versions `v1.16.0` to `v1.16.1` removed compatibility with Kubernetes versions `1.23` and earlier\. VPC CNI version `v1.16.2` restores compatibility with Kubernetes versions `1.23` and earlier and CNI spec `v0.4.0`\.
 Amazon VPC CNI plugin for  Kubernetes versions `v1.16.0` to `v1.16.1` implement CNI specification version `v1.0.0`\. CNI spec `v1.0.0` is supported on EKS clusters that run the Kubernetes versions `v1.24` or later\. VPC CNI version `v1.16.0` to `v1.16.1` and CNI spec `v1.0.0` aren’t supported on Kubernetes version `v1.23` or earlier\. For more information about `v1.0.0` of the CNI spec, see [Container Network Interface \(CNI\) Specification](https://github.com/containernetworking/cni/blob/spec-v1.0.0/SPEC.md) on  
Versions are specified as `major-version.minor-version.patch-version-eksbuild.build-number`\. \* \.Check version compatibility for each feature Some features of each release of the Amazon VPC CNI plugin for  Kubernetes require certian Kubernetes versions\. When using different Amazon EKS features, if a specific version of the add\-on is required, then it’s noted in the feature documentation\. Unless you have a specific reason for running an earlier version, we recommend running the latest version\.
<a name="vpc-add-on-create"></a>=== Creating the Amazon EKS add\-on  
Create the Amazon EKS type of the add\-on\.  
See which version of the add\-on is installed on your cluster\.  

   ```
   kubectl describe daemonset aws-node --namespace kube-system | grep amazon-k8s-cni: | cut -d : -f 3
   ```
An example output is as follows\.  

   ```
   `v1.16.4-eksbuild.2`
   ```
See which type of the add\-on is installed on your cluster\. Depending on the tool that you created your cluster with, you might not currently have the Amazon EKS add\-on type installed on your cluster\. Replace *my\-cluster* with the name of your cluster\.  

   ```
   $ aws eks describe-addon --cluster-name my-cluster --addon-name vpc-cni --query addon.addonVersion --output text
   ```
If a version number is returned, you have the Amazon EKS type of the add\-on installed on your cluster and don’t need to complete the remaining steps in this procedure\. If an error is returned, you don’t have the Amazon EKS type of the add\-on installed on your cluster\. Complete the remaining steps of this procedure to install it\.
Save the configuration of your currently installed add\-on\.  

   ```
   kubectl get daemonset aws-node -n kube-system -o yaml > aws-k8s-cni-old.yaml
   ```
Replace ` my-cluster ` with the name of your cluster\.  

     ```
     aws eks create-addon --cluster-name my-cluster --addon-name vpc-cni --addon-version v1.18.1-eksbuild.3 \
         --service-account-role-arn arn:aws:iam::111122223333:role/AmazonEKSVPCCNIRole
     ```
If you’ve applied custom settings to your current add\-on that conflict with the default settings of the Amazon EKS add\-on, creation might fail\. If creation fails, you receive an error that can help you resolve the issue\. Alternatively, you can add `--resolve-conflicts OVERWRITE` to the previous command\. This allows the add\-on to overwrite any existing custom settings\. Once you’ve created the add\-on, you can update it with your custom settings\.
Confirm that the latest version of the add\-on for your cluster’s Kubernetes version was added to your cluster\. Replace ` my-cluster ` with the name of your cluster\.  

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name vpc-cni --query addon.addonVersion --output text
   ```
It might take several seconds for add\-on creation to complete\.  
An example output is as follows\.  

   ```
   `v1.18.1-eksbuild.3`
   ```
\(Optional\) Install the `cni-metrics-helper` to your cluster\. It scrapes elastic network interface and IP address information, aggregates it at a cluster level, and publishes the metrics to Amazon CloudWatch\. For more information, see [cni\-metrics\-helper](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/cmd/cni-metrics-helper/README.md) on GitHub\.
<a name="vpc-add-on-update"></a>=== Updating the Amazon EKS add\-on  
See which version of the add\-on is installed on your cluster\. Replace ` my-cluster ` with your cluster name\.  

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name vpc-cni --query "addon.addonVersion" --output text
   ```
An example output is as follows\.  

   ```
   `v1.16.4-eksbuild.2`
   ```
Save the configuration of your currently installed add\-on\.  

   ```
   kubectl get daemonset aws-node -n kube-system -o yaml > aws-k8s-cni-old.yaml
   ```
Replace ` my-cluster ` with the name of your cluster\.
The `--resolve-conflicts` *PRESERVE* option preserves existing configuration values for the add\-on\. If you’ve set custom values for add\-on settings, and you don’t use this option, Amazon EKS overwrites your values with its default values\. If you use this option, then we recommend testing any field and value changes on a non\-production cluster before updating the add\-on on your production cluster\. If you change this value to `OVERWRITE`, all settings are changed to Amazon EKS default values\. If you’ve set custom values for any settings, they might be overwritten with Amazon EKS default values\. If you change this value to `none`, Amazon EKS doesn’t change the value of any settings, but the update might fail\. If the update fails, you receive an error message to help you resolve the conflict\.
If you’re not updating a configuration setting, remove `--configuration-values '{"env":{"AWS_VPC_K8S_CNI_EXTERNALSNAT":"true"}}'` from the command\. If you’re updating a configuration setting, replace *"env":\{"AWS\_VPC\_K8S\_CNI\_EXTERNALSNAT":"true"\}* with the setting that you want to set\. In this example, the ` AWS_VPC_K8S_CNI_EXTERNALSNAT` environment variable is set to `true`\. The value that you specify must be valid for the configuration schema\. If you don’t know the configuration schema, run `aws eks describe-addon-configuration --addon-name vpc-cni --addon-version [replaceable]`v1\.18\.1\-eksbuild\.3` `, replacing [replaceable]. For an explanation of each setting, see [CNI Configuration Variables](https://github.com/aws/amazon-vpc-cni-k8s#cni-configuration-variables) on GitHub.`   

     ```
     aws eks update-addon --cluster-name my-cluster --addon-name vpc-cni --addon-version v1.18.1-eksbuild.3 \
         --service-account-role-arn arn:aws:iam::111122223333:role/AmazonEKSVPCCNIRole \
         --resolve-conflicts PRESERVE --configuration-values '{"env":{"{aws}_VPC_K8S_CNI_EXTERNALSNAT":"true"}}'
     ```
 It might take several seconds for the update to complete\. 
Confirm that the add\-on version was updated\. Replace ` my-cluster ` with the name of your cluster\.  

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name vpc-cni
   ```
It might take several seconds for the update to complete\.  
An example output is as follows\.  

   ```
   {
       "addon": {
           "addonName": "vpc-cni",
           "clusterName": "my-cluster",
           "status": "ACTIVE",
           "addonVersion": "v1.18.1-eksbuild.3",
           "health": {
               "issues": []
           },
           "addonArn": "arn:aws:eks:region:111122223333:addon/my-cluster/vpc-cni/74c33d2f-b4dc-8718-56e7-9fdfa65d14a9",
           "createdAt": "2023-04-12T18:25:19.319000+00:00",
           "modifiedAt": "2023-04-12T18:40:28.683000+00:00",
           "serviceAccountRoleArn": "arn:aws:iam::111122223333:role/AmazonEKSVPCCNIRole",
           "tags": {},
           "configurationValues": "{\"env\":{\"{aws}_VPC_K8S_CNI_EXTERNALSNAT\":\"true\"}}"
       }
   }
   ```
<a name="vpc-add-on-self-managed-update"></a>=== Updating the self\-managed add\-on

We recommend adding the Amazon EKS type of the add\-on to your cluster instead of using the self\-managed type of the add\-on\. If you’re not familiar with the difference between the types, see \. For more information about adding an Amazon EKS add\-on to your cluster, see \. If you’re unable to use the Amazon EKS add\-on, we encourage you to submit an issue about why you can’t to the [Containers roadmap GitHub repository](https://github.com/aws/containers-roadmap/issues)\.

**Example**  

1. Confirm that you don’t have the Amazon EKS type of the add\-on installed on your cluster\. Replace *my\-cluster* with the name of your cluster\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name vpc-cni --query addon.addonVersion --output text
   ```

1. See which version of the container image is currently installed on your cluster\.

   ```
   kubectl describe daemonset aws-node --namespace kube-system | grep amazon-k8s-cni: | cut -d : -f 3
   ```

   An example output is as follows\.

   ```
   `v1.16.4-eksbuild.2`
   ```

   Your output might not include the build number\.

1. Backup your current settings so you can configure the same settings once you’ve updated your version\.

   ```
   kubectl get daemonset aws-node -n kube-system -o yaml > aws-k8s-cni-old.yaml
   //⁂----``. To review the available versions and familiarize yourself with the changes in the version that you want to update to, see [path]``https://github.com/aws/amazon-vpc-cni-k8s/releases[releases]`` on  [noloc]GitHub``. Note that we recommend updating to the same  ``major``.``minor``.``patch`` version listed in the <<vpc-cni-latest-available-version,latest available versions table>>, even if later versions are available on GitHub.. The build versions listed in the table aren't specified in the self-managed versions listed on GitHub. Update your version by completing the tasks in one of the following options:
   +
   ** If you don't have any custom settings for the add-on, then run the command under the `To apply this release:` heading on GitHub for the https://github.com/aws/amazon-vpc-cni-k8s/releases[release] that you're updating to.
   ** If you have custom settings, download the manifest file with the following command. Change [replaceable]``https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/v1.18.1/config/master/aws-k8s-cni.yaml`` to the URL for the release on GitHub that you're updating to.
   +
   [source,bash]
   ```

   curl \-O [https://raw\.githubusercontent\.com/aws/amazon\-vpc\-cni\-k8s/v1\.18\.1/config/master/aws\-k8s\-cni\.yaml](https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/v1.18.1/config/master/aws-k8s-cni.yaml) 

```
+

//⁂If necessary, modify the manifest with the custom settings from the backup you made in a previous step and then apply the modified manifest to your cluster. If your nodes don't have access to the private Amazon EKS Amazon ECR repositories that the images are pulled from (see the lines that start with  `image:` in the manifest), then you'll have to download the images, copy them to your own repository, and modify the manifest to pull the images from your repository. For more information, see <<copy-image-to-repository,Copy a container image from one repository to another repository>>.
+
```

```
. Confirm that the new version is now installed on your cluster.
+
[source,bash]
```
kubectl describe daemonset aws\-node \-\-namespace kube\-system \| grep amazon\-k8s\-cni: \| cut \-d : \-f 3  

```
+

An example output is as follows.
+
```
 `v1.18.1`   

```
. (Optional) Install the `cni-metrics-helper` to your cluster. It scrapes elastic network interface and IP address information, aggregates it at a cluster level, and publishes the metrics to Amazon CloudWatch. For more information, see https://github.com/aws/amazon-vpc-cni-k8s/blob/master/cmd/cni-metrics-helper/README.md[cni-metrics-helper] on GitHub.


[.topic]
[[cni-iam-role,cni-iam-role.title]]
=== Configuring the  [noloc]``Amazon VPC CNI plugin for ``[noloc]``Kubernetes`` to use IAM roles for service accounts (IRSA)

[abstract]
--
Learn how to configure the [noloc]``Amazon VPC CNI plugin for ``[noloc]``Kubernetes`` to use an IAM account with its  [noloc]``Kubernetes`` service account.
--

The  https://github.com/aws/amazon-vpc-cni-k8s[Amazon VPC CNI plugin for Kubernetes] is the networking plugin for [noloc]``Pod`` networking in Amazon EKS clusters. The plugin is responsible for allocating VPC IP addresses to  [noloc]``Kubernetes`` nodes and configuring the necessary networking for  [noloc]``Pods`` on each node. The plugin:


//⁂* Requires {aws} Identity and Access Management (IAM) permissions. If your cluster uses the `IPv4` family, the permissions are specified in the [path]``{https---docs-aws-amazon-com-aws-managed-policy-latest-reference-AmazonEKS-CNI-Policy-html}[AmazonEKS_CNI_Policy]`` {aws} managed policy.If your cluster uses the `IPv6` family, then the permissions must be added to an <<cni-iam-role-create-ipv6-policy,IAM policy that you create>>. You can attach the policy to the  <<create-node-role,Amazon EKS node IAM role>>, or to a separate IAM role. We recommend that you assign it to a separate role, as detailed in this topic.
* Creates and is configured to use a [noloc]``Kubernetes`` service account named  `aws-node` when it's deployed. The service account is bound to a [noloc]``Kubernetes````clusterrole`` named ``aws-node``, which is assigned the required [noloc]``Kubernetes`` permissions.


[NOTE]
```

**Example**  
+ An existing Amazon EKS cluster\. To deploy one, see \.
+ An existing AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see \.
<a name="cni-iam-role-create-role"></a>==== Step 1: Create the Amazon VPC CNI plugin for  Kubernetes IAM role \. Determine the IP family of your cluster\.  
\+  

```
aws eks describe-cluster --name my-cluster | grep ipFamily
```
\+  
An example output is as follows\.  
\+  

```
"ipFamily": "ipv`4`"
```
\+  
The output may return `ipv6` instead\. \. Create the IAM role\. You can use `eksctl` or `kubectl` and the AWS CLI to create your IAM role\.  
\+    
eksctl  
+ Create an IAM role and attach the IAM policy to the role with the command that matches the IP family of your cluster\. The command creates and deploys an AWS CloudFormation stack that creates an IAM role, attaches the policy that you specify to it, and annotates the existing `aws-node` Kubernetes service account with the ARN of the IAM role that is created\.
  +  `IPv4` 

    Replace * `my-cluster` with your own value\.* 

    ```
    eksctl create iamserviceaccount \
        --name aws-node \
        --namespace kube-system \
        --cluster my-cluster \
        --role-name AmazonEKSVPCCNIRole \
        --attach-policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy \
        --override-existing-serviceaccounts \
        --approve
    ```
  +  `IPv6` 

    ```
    eksctl create iamserviceaccount \
        --name aws-node \
        --namespace kube-system \
        --cluster my-cluster \
        --role-name AmazonEKSVPCCNIRole \
        --attach-policy-arn arn:aws:iam::111122223333:policy/AmazonEKS_CNI_IPv6_Policy \
        --override-existing-serviceaccounts \
        --approve
    ```  
kubectl and the AWS CLI  

1. View your cluster’s OIDC provider URL\.

   ```
   aws eks describe-cluster --name my-cluster --query "cluster.identity.oidc.issuer" --output text
   ```

   An example output is as follows\.

   ```
   https://oidc.eks../id/`EXAMPLED539D4633E53DE1B71EXAMPLE`
   ```

1. Copy the following contents to a file named `[replaceable]`vpc\-cni\-trust\-policy\.json` `. Replace `[replaceable] with your account ID and [replaceable] with the output returned in the previous step. Replace ` *region\-code*`` with the AWS Region that your cluster is in\.

   ```
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
                       "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:sub": "system:serviceaccount:kube-system:aws-node"
                   }
               }
           }
       ]
   }
   ```

1. Create the role\. You can replace * `AmazonEKSVPCCNIRole` with any name that you choose\.* 

   ```
   aws iam create-role \
     --role-name AmazonEKSVPCCNIRole \
   //⁂  --assume-role-policy-document file://"vpc-cni-trust-policy.json"
   ```Attach the required IAM policy to the role\. Run the command that matches the IP family of your cluster\.
   +  `IPv4` 

     ```
     aws iam attach-role-policy \
       --policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy \
       --role-name AmazonEKSVPCCNIRole
     ```
   +  `IPv6` 

     ```
     aws iam attach-role-policy \
       --policy-arn arn:aws:iam::111122223333:policy/AmazonEKS_CNI_IPv6_Policy \
       --role-name AmazonEKSVPCCNIRole
     ```Run the following command to annotate the `aws-node` service account with the ARN of the IAM role that you created previously\. Replace the ` example values ` with your own values\.

   ```
   kubectl annotate serviceaccount \
       -n kube-system aws-node \
       eks.amazonaws.com/role-arn=arn:aws:iam::111122223333:role/AmazonEKSVPCCNIRole
   ```

   1. \(Optional\) Configure the AWS Security Token Service endpoint type used by your Kubernetes service account\. For more information, see \.
<a name="cni-iam-role-redeploy-pods"></a>==== Step 2: Re\-deploy Amazon VPC CNI plugin for  Kubernetes Pods \. Delete and re\-create any existing Pods that are associated with the service account to apply the credential environment variables\. The annotation is not applied to Pods that are currently running without the annotation\. The following command deletes the existing `aws-node` DaemonSet Pods and deploys them with the service account annotation\.  
\+  

```
kubectl delete Pods -n kube-system -l k8s-app=aws-node
```

1. Confirm that the Pods all restarted\.

   ```
   kubectl get pods -n kube-system -l k8s-app=aws-node
   ```

1. Describe one of the Pods and verify that the ` AWS_WEB_IDENTITY_TOKEN_FILE` and ` AWS_ROLE_ARN` environment variables exist\. Replace *cpjw7* with the name of one of your Pods returned in the output of the previous step\.

   ```
   kubectl describe pod -n kube-system aws-node-cpjw7 | grep '{aws}_ROLE_ARN:\|{aws}_WEB_IDENTITY_TOKEN_FILE:'
   ```

   An example output is as follows\.

   ```
   {aws}_ROLE_ARN:                 arn:aws:iam::`111122223333`:role/`AmazonEKSVPCCNIRole`{aws}_WEB_IDENTITY_TOKEN_FILE:  /var/run/secrets/eks.amazonaws.com/serviceaccount/token
         {aws}_ROLE_ARN:                           arn:aws:iam::`111122223333`:role/`AmazonEKSVPCCNIRole`{aws}_WEB_IDENTITY_TOKEN_FILE:            /var/run/secrets/eks.amazonaws.com/serviceaccount/token
   ```

   Two sets of duplicate results are returned because the Pod contains two containers\. Both containers have the same values\.

   If your Pod is using the AWS Regional endpoint, then the following line is also returned in the previous output\.

   ```
   {aws}_STS_REGIONAL_ENDPOINTS=regional
   ```
<a name="remove-cni-policy-node-iam-role"></a>==== Step 3: Remove the CNI policy from the node IAM role  
+  `IPv4` 

  ```
  aws iam detach-role-policy --role-name AmazonEKSNodeRole --policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy
  ```
+  `IPv6` 

  Replace ` 111122223333 ` with your account ID and ` AmazonEKS_CNI_IPv6_Policy ` with the name of your `IPv6` policy\.

  ```
  aws iam detach-role-policy --role-name AmazonEKSNodeRole --policy-arn arn:aws:iam::111122223333:policy/AmazonEKS_CNI_IPv6_Policy
  ```
<a name="cni-iam-role-create-ipv6-policy"></a>==== Create IAM policy for clusters that use the `IPv6` family  

1. Copy the following text and save it to a file named `vpc-cni-ipv6-policy.json`\.

   ```
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": [
                   "ec2:AssignIpv6Addresses",
                   "ec2:DescribeInstances",
                   "ec2:DescribeTags",
                   "ec2:DescribeNetworkInterfaces",
                   "ec2:DescribeInstanceTypes"
               ],
               "Resource": "*"
           },
           {
               "Effect": "Allow",
               "Action": [
                   "ec2:CreateTags"
               ],
               "Resource": [
                   "arn:aws:ec2:*:*:network-interface/*"
               ]
           }
       ]
   }
   ```

1. Create the IAM policy\.

   ```
   //⁂aws iam create-policy --policy-name AmazonEKS_CNI_IPv6_Policy --policy-document file://vpc-cni-ipv6-policy.json
   ```
<a name="pod-networking-use-cases"></a>=== Choosing Pod networking use cases  
Learn about the different use cases for Amazon EKS Pod networking and which use cases can be used together\.  
The Amazon VPC CNI plugin for  Kubernetes provides networking for Pods\. The following table helps you understand which networking use cases you can use together and the capabilities and Amazon VPC CNI plugin for  Kubernetes settings that you can use with different Amazon EKS node types\. All information in the table applies to Linux `IPv4` nodes only\.  

```
                        interface
//⁂| IP prefixes
                            assigned to network interface
//⁂| Security groups
                        for Pods
//⁂|
```
Node  
Pod \(If you’ve set `POD_SECURITY_GROUP_ENFORCING_MODE`=`standard` and ` AWS_VPC_K8S_CNI_EXTERNALSNAT`=`false`, traffic destined for endpoints outside the VPC use the node’s security groups, not the Pod’s security groups\)  
Compatible  
Only with version `1.14.0` or later of the Amazon VPC CNI plugin
+ You can’t use `IPv6` with custom networking\.
+  `IPv6` addresses are not translated, so SNAT doesn’t apply\.
+ Traffic flow to and from Pods with associated security groups are not subjected to Calico network policy enforcement and are limited to Amazon VPC security group enforcement only\.
+ If you use Calico network policy enforcement, we recommend that you set the environment variable `ANNOTATE_POD_IP` to `true` to avoid a known issue with Kubernetes\. To use this feature, you must add `patch` permission for pods to the `aws-node` ClusterRole\. Note that adding patch permissions to the `aws-node` DaemonSet increases the security scope for the plugin\. For more information, see [ANNOTATE\_POD\_IP](https://github.com/aws/amazon-vpc-cni-k8s/?tab=readme-ov-file#annotate_pod_ip-v193) in the VPC CNI repo on GitHub\.
+ IP prefixes and IP addresses are associated with standard Amazon EC2 elastic network interfaces\. Pods requiring specific security groups are assigned the primary IP address of a branch network interface\. You can mix Pods getting IP addresses, or IP addresses from IP prefixes with Pods getting branch network interfaces on the same node\.

**Example**  
**Windows nodes**  
==== `IPv6` addresses for clusters, Pods, and services 
Learn how to deploy an Amazon EKS cluster that assigns `IPv6` addresses to Pods and services\.  
By default, Kubernetes assigns `IPv4` addresses to your Pods and services\. Instead of assigning `IPv4` addresses to your Pods and services, you can configure your cluster to assign `IPv6` addresses to them\. Amazon EKS doesn’t support dual\-stacked Pods or services, even though Kubernetes does in version `1.23` and later\. As a result, you can’t assign both `IPv4` and `IPv6` addresses to your Pods and services\.  
You select which IP family you want to use for your cluster when you create it\. You can’t change the family after you create the cluster\.  
<a name="ipv6-considerations"></a>===== Considerations for using the `IPv6` family for your cluster  
+ The version of the Amazon VPC CNI add\-on that you deploy to your cluster must be version `1.10.1` or later\. This version or later is deployed by default\. After you deploy the add\-on, you can’t downgrade your Amazon VPC CNI add\-on to a version lower than `1.10.1` without first removing all nodes in all node groups in your cluster\.
+  Windows Pods and services aren’t supported\.
+ When you create a cluster, the VPC and subnets that you specify must have an `IPv6` CIDR block that’s assigned to the VPC and subnets that you specify\. They must also have an `IPv4` CIDR block assigned to them\. This is because, even if you only want to use `IPv6`, a VPC still requires an `IPv4` CIDR block to function\. For more information, see [Associate an IPv6 CIDR block with your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html#vpc-associate-ipv6-cidr) in the Amazon VPC User Guide\.
+ When you create your cluster and nodes, you must specify subnets that are configured to auto\-assign `IPv6` addresses\. Otherwise, you can’t deploy your cluster and nodes\. By default, this configuration is disabled\. For more information, see [Modify the IPv6 addressing attribute for your subnet](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#subnet-ipv6) in the Amazon VPC User Guide\.
+ The route tables that are assigned to your subnets must have routes for `IPv6` addresses\. For more information, see [Migrate to IPv6](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-migrate-ipv6.html) in the Amazon VPC User Guide\.
+ Your security groups must allow `IPv6` addresses\. For more information, see [Migrate to IPv6](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-migrate-ipv6.html) in the Amazon VPC User Guide\.
+ You can only use `IPv6` with AWS Nitro\-based Amazon EC2 or Fargate nodes\.
+  Pods and services are only assigned an `IPv6` address\. They aren’t assigned an `IPv4` address\. Because Pods are able to communicate to `IPv4` endpoints through NAT on the instance itself, [DNS64 and NAT64](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html#nat-gateway-nat64-dns64) aren’t needed\. If the traffic needs a public IP address, the traffic is then source network address translated to a public IP\.
+ The source `IPv6` address of a Pod isn’t source network address translated to the `IPv6` address of the node when communicating outside of the VPC\. It is routed using an internet gateway or egress\-only internet gateway\.
+ All nodes are assigned an `IPv4` and `IPv6` address\.
+ Each Fargate Pod receives an `IPv6` address from the CIDR that’s specified for the subnet that it’s deployed in\. The underlying hardware unit that runs Fargate Pods gets a unique `IPv4` and `IPv6` address from the CIDRs that are assigned to the subnet that the hardware unit is deployed in\.
+ We recommend that you perform a thorough evaluation of your applications, Amazon EKS add\-ons, and AWS services that you integrate with before deploying `IPv6` clusters\. This is to ensure that everything works as expected with `IPv6`\.
+ Use of the Amazon EC2 [https://docs\.aws\.amazon\.com/](https://docs.aws.amazon.com/) AWSEC2/latest/UserGuide/configuring\-instance\-metadata\-service\.html`IPv6` endpoint is not supported with Amazon EKS\.
+ When creating a self\-managed node group in a cluster that uses the `IPv6` family, user\-data must include the following `BootstrapArguments` for the [bootstrap\.sh](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh) file that runs at node start up\. Replace *your\-cidr* with the `IPv6` CIDR range of your cluster’s VPC\.

  ```
  --ip-family ipv6 --service-ipv6-cidr your-cidr
  ```

  If you don’t know the `IPv6`CIDR range for your cluster, you can see it with the following command (requires the AWS CLI version `2.4.9` or later\)\.

  ```
  aws eks describe-cluster --name my-cluster --query cluster.kubernetesNetworkConfig.serviceIpv6Cidr --output text
  ```
<a name="deploy-ipv6-cluster"></a>===== Deploy an `IPv6` cluster and managed Amazon Linux nodes  
In this tutorial, you deploy an `IPv6` Amazon VPC, an Amazon EKS cluster with the `IPv6` family, and a managed node group with Amazon EC2 Amazon Linux nodes\. You can’t deploy Amazon EC2 Windows nodes in an `IPv6` cluster\. You can also deploy Fargate nodes to your cluster, though those instructions aren’t provided in this topic for simplicity\.  
Before starting this tutorial, you must install and configure the following tools and resources that you need to create and manage an Amazon EKS cluster\.  
+ The `kubectl` command line tool is installed on your device or AWS CloudShell\. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster\. For example, if your cluster version is `1.28`, you can use `kubectl` version `1.27`, `1.28`, or `1.29` with it\. To install or upgrade `kubectl`, see \.
+ The IAM security principal that you’re using must have permissions to work with Amazon EKS IAM roles, service linked roles, AWS CloudFormation, a VPC, and related resources\. For more information, see [Actions, resources, and condition keys for Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html) and [Using service\-linked roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html) in the IAM User Guide\.
Procedures are provided to create the resources with either `eksctl` or the AWS CLI\. You can also deploy the resources using the AWS Management Console, but those instructions aren’t provided in this topic for simplicity\.    
 eksctl   
\* \.Prerequisite `eksctl` version `0.177.0` or later installed on your computer\. To install or update to it, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.  

1. Create the `ipv6-cluster.yaml` file\. Copy the command that follows to your device\. Make the following modifications to the command as needed and then run the modified command:
   + Replace ` my-cluster ` with a name for your cluster\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can’t be longer than 100 characters\.
   + Replace ` region-code ` with any AWS Region that is supported by Amazon EKS\. For a list of AWS Regions, see [Amazon EKS endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/eks.html) in the AWS General Reference guide\.
   + Replace ` my-nodegroup ` with a name for your node group\. The node group name can’t be longer than 63 characters\. It must start with letter or digit, but can also include hyphens and underscores for the remaining characters\.
   + Replace ` t3.medium ` with any \{https\-\-\-docs\-aws\-amazon\-com\-AWSEC2\-latest\-UserGuide\-instance\-types\-html\-ec2\-nitro\-instances\}\[AWS Nitro System instance type\]\.

     ```
     //⁂cat >ipv6-cluster.yaml <<EOF
     ---
     apiVersion: eksctl.io/v1alpha5
     kind: ClusterConfig
     
     metadata:
       name: my-cluster
       region: region-code
       version: "X.XX"
     
     kubernetesNetworkConfig:
       ipFamily: IPv6
     
     addons:
       - name: vpc-cni
         version: latest
       - name: coredns
         version: latest
       - name: kube-proxy
         version: latest
     
     iam:
       withOIDC: true
     
     managedNodeGroups:
       - name: my-nodegroup
         instanceType: t3.medium
     EOF
     ```

1. Create your cluster\.

   ```
   eksctl create cluster -f ipv6-cluster.yaml
   ```

   Cluster creation takes several minutes\. Don’t proceed until you see the last line of output, which looks similar to the following output\.

   ```
   [...]
   [✓]  EKS cluster "`my-cluster`" in "" region is ready
   ```

1. Confirm that default Pods are assigned `IPv6` addresses\.

   ```
   kubectl get pods -n kube-system -o wide
   ```

   An example output is as follows\.

   ```
   NAME                       READY   STATUS    RESTARTS   AGE     IP                                       NODE                                            NOMINATED NODE   READINESS GATES
   aws-node-rslts             1/1     Running   1          5m36s   2600:1f13:b66:8200:11a5:ade0:c590:6ac8   ip-192-168-34-75.region-code.compute.internal   <none>           <none>
   aws-node-t74jh             1/1     Running   0          5m32s   2600:1f13:b66:8203:4516:2080:8ced:1ca9   ip-192-168-253-70.region-code.compute.internal  <none>           <none>
   coredns-85d5b4454c-cw7w2   1/1     Running   0          56m     2600:1f13:b66:8203:34e5::                ip-192-168-253-70.region-code.compute.internal  <none>           <none>
   coredns-85d5b4454c-tx6n8   1/1     Running   0          56m     2600:1f13:b66:8203:34e5::1               ip-192-168-253-70.region-code.compute.internal  <none>           <none>
   kube-proxy-btpbk           1/1     Running   0          5m36s   2600:1f13:b66:8200:11a5:ade0:c590:6ac8   ip-192-168-34-75.region-code.compute.internal   <none>           <none>
   kube-proxy-jjk2g           1/1     Running   0          5m33s   2600:1f13:b66:8203:4516:2080:8ced:1ca9   ip-192-168-253-70.region-code.compute.internal  <none>           <none>
   ```

1. Confirm that default services are assigned `IPv6` addresses\.

   ```
   kubectl get services -n kube-system -o wide
   ```

   An example output is as follows\.

   ```
   NAME       TYPE        CLUSTER-IP          EXTERNAL-IP   PORT(S)         AGE   SELECTOR
   kube-dns   ClusterIP   fd30:3087:b6c2::a   <none>        53/UDP,53/TCP   57m   k8s-app=kube-dns
   ```

1. After you’ve finished with the cluster and nodes that you created for this tutorial, you should clean up the resources that you created with the following command\.

   ```
   eksctl delete cluster my-cluster
   ```  
 AWS CLI  
\* \.Prerequisite Version `2.12.3` or later or version `1.27.160` or later of the AWS Command Line Interface \(AWS CLI\) installed and configured on your device or AWS CloudShell\. To check your current version, use ` `aws --version | cut -d / -f2 | cut -d ' ' -f1 are often several versions behind the latest version of the AWS CLI. To install the latest version, see [Installing](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with aws configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the AWS Command Line Interface User Guide. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version. To update it, see [Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the AWS CloudShell User Guide. If you use the AWS CloudShell, you may need to [install version 2\.12\.3 or later or 1\.27\.160 or later of the AWS CLI](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software), because the default AWS CLI version installed in the AWS CloudShell may be an earlier version.`   
IMPORTANT: \*\* You must complete all steps in this procedure as the same user\. To check the current user, run the following command:  
\+  

```
aws sts get-caller-identity
```
+ You must complete all steps in this procedure in the same shell\. Several steps use variables set in previous steps\. Steps that use variables won’t function properly if the variable values are set in a different shell\. If you use the [AWS CloudShell](https://docs.aws.amazon.com/cloudshell/latest/userguide/welcome.html) to complete the following procedure, remember that if you don’t interact with it using your keyboard or pointer for approximately 20–30 minutes, your shell session ends\. Running processes do not count as interactions\.
+ The instructions are written for the Bash shell, and may need adjusting in other shells\.
Replace all ` example values ` in the steps of this procedure with your own values\.  

1. Run the following commands to set some variables used in later steps\. Replace ` region-code ` with the AWS Region that you want to deploy your resources in\. The value can be any AWS Region that is supported by Amazon EKS\. For a list of AWS Regions, see [Amazon EKS endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/eks.html) in the AWS General Reference guide\. Replace ` my-cluster ` with a name for your cluster\. The name can contain only alphanumeric characters \(case\-sensitive\) and hyphens\. It must start with an alphabetic character and can’t be longer than 100 characters\. Replace ` my-nodegroup ` with a name for your node group\. The node group name can’t be longer than 63 characters\. It must start with letter or digit, but can also include hyphens and underscores for the remaining characters\. Replace ` 111122223333 ` with your account ID\.

   ```
   export region_code=region-code
   export cluster_name=my-cluster
   export nodegroup_name=my-nodegroup
   export account_id=111122223333
   ```

1. Create an Amazon VPC with public and private subnets that meets Amazon EKS and `IPv6` requirements\.

   1. Run the following command to set a variable for your AWS CloudFormation stack name\. You can replace ` my-eks-ipv6-vpc ` with any name you choose\.

      ```
      export vpc_stack_name=my-eks-ipv6-vpc
      ```

   1. Create an `IPv6` VPC using an AWS CloudFormation template\.

      ```
      aws cloudformation create-stack --region $region_code --stack-name $vpc_stack_name \
        --template-url https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-ipv6-vpc-public-private-subnets.yaml
      ```

      The stack takes a few minutes to create\. Run the following command\. Don’t continue to the next step until the output of the command is `CREATE_COMPLETE`\.

      ```
      aws cloudformation describe-stacks --region $region_code --stack-name $vpc_stack_name --query Stacks[].StackStatus --output text
      ```

   1. Retrieve the IDs of the public subnets that were created\.

      ```
      aws cloudformation describe-stacks --region $region_code --stack-name $vpc_stack_name \
          --query='Stacks[].Outputs[?OutputKey==`SubnetsPublic`].OutputValue' --output text
      ```

      An example output is as follows\.

      ```
      subnet-`0a1a56c486EXAMPLE`,subnet-`099e6ca77aEXAMPLE`
      ```

   1. Enable the auto\-assign `IPv6` address option for the public subnets that were created\.

      ```
      aws ec2 modify-subnet-attribute --region $region_code --subnet-id subnet-0a1a56c486EXAMPLE --assign-ipv6-address-on-creation
      aws ec2 modify-subnet-attribute --region $region_code --subnet-id subnet-099e6ca77aEXAMPLE --assign-ipv6-address-on-creation
      ```

   1. Retrieve the names of the subnets and security groups created by the template from the deployed AWS CloudFormation stack and store them in variables for use in a later step\.

      ```
      security_groups=$(aws cloudformation describe-stacks --region $region_code --stack-name $vpc_stack_name \
          --query='Stacks[].Outputs[?OutputKey==`SecurityGroups`].OutputValue' --output text)
      
      public_subnets=$(aws cloudformation describe-stacks --region $region_code --stack-name $vpc_stack_name \
          --query='Stacks[].Outputs[?OutputKey==`SubnetsPublic`].OutputValue' --output text)
      
      private_subnets=$(aws cloudformation describe-stacks --region $region_code --stack-name $vpc_stack_name \
          --query='Stacks[].Outputs[?OutputKey==`SubnetsPrivate`].OutputValue' --output text)
      
      subnets=${public_subnets},${private_subnets}
      ```

1. Create a cluster IAM role and attach the required Amazon EKS IAM managed policy to it\. Kubernetes clusters managed by Amazon EKS make calls to other AWS services on your behalf to manage the resources that you use with the service\.

   1. Run the following command to create the `eks-cluster-role-trust-policy.json` file\.

      ```
      //⁂cat >eks-cluster-role-trust-policy.json <<EOF
      {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect": "Allow",
            "Principal": {
              "Service": "eks.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
          }
        ]
      }
      EOF
      ```

   1. Run the following command to set a variable for your role name\. You can replace ` myAmazonEKSClusterRole ` with any name you choose\.

      ```
      export cluster_role_name=myAmazonEKSClusterRole
      ```

   1. Create the role\.

      ```
      //⁂aws iam create-role --role-name $cluster_role_name --assume-role-policy-document file://"eks-cluster-role-trust-policy.json"
      ```

   1. Retrieve the ARN of the IAM role and store it in a variable for a later step\.

      ```
      cluster_iam_role=$(aws iam get-role --role-name $cluster_role_name --query="Role.Arn" --output text)
      ```

   1. Attach the required Amazon EKS managed IAM policy to the role\.

      ```
      aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy --role-name $cluster_role_name
      ```

1. Create your cluster\.

   ```
   aws eks create-cluster --region $region_code --name $cluster_name --kubernetes-version 1.XX \
      --role-arn $cluster_iam_role --resources-vpc-config subnetIds=$subnets,securityGroupIds=$security_groups \
      --kubernetes-network-config ipFamily=ipv6
   ```

   1. NOTE: You might receive an error that one of the Availability Zones in your request doesn’t have sufficient capacity to create an Amazon EKS cluster\. If this happens, the error output contains the Availability Zones that can support a new cluster\. Retry creating your cluster with at least two subnets that are located in the supported Availability Zones for your account\. For more information, see \.
The cluster takes several minutes to create\. Run the following command\. Don’t continue to the next step until the output from the command is `ACTIVE`\.  
\+  

```
aws eks describe-cluster --region $region_code --name $cluster_name --query cluster.status
```

1. Create or update a `kubeconfig` file for your cluster so that you can communicate with your cluster\.

   ```
   aws eks update-kubeconfig --region $region_code --name $cluster_name
   ```

   By default, the `config` file is created in `~/.kube` or the new cluster’s configuration is added to an existing `config` file in `~/.kube`\.

1. Create a node IAM role\.

   1. Run the following command to create the `vpc-cni-ipv6-policy.json` file\.

      ```
      //⁂cat >vpc-cni-ipv6-policy <<EOF
      {
          "Version": "2012-10-17",
          "Statement": [
              {
                  "Effect": "Allow",
                  "Action": [
                      "ec2:AssignIpv6Addresses",
                      "ec2:DescribeInstances",
                      "ec2:DescribeTags",
                      "ec2:DescribeNetworkInterfaces",
                      "ec2:DescribeInstanceTypes"
                  ],
                  "Resource": "*"
              },
              {
                  "Effect": "Allow",
                  "Action": [
                      "ec2:CreateTags"
                  ],
                  "Resource": [
                      "arn:aws:ec2:*:*:network-interface/*"
                  ]
              }
          ]
      }
      EOF
      ```

   1. Create the IAM policy\.

      ```
      //⁂aws iam create-policy --policy-name AmazonEKS_CNI_IPv6_Policy --policy-document file://vpc-cni-ipv6-policy.json
      ```

   1. Run the following command to create the `node-role-trust-relationship.json` file\.

      ```
      //⁂cat >node-role-trust-relationship.json <<EOF
      {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect": "Allow",
            "Principal": {
              "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
          }
        ]
      }
      EOF
      ```

   1. Run the following command to set a variable for your role name\. You can replace ` AmazonEKSNodeRole ` with any name you choose\.

      ```
      export node_role_name=AmazonEKSNodeRole
      ```

   1. Create the IAM role\.

      ```
      //⁂aws iam create-role --role-name $node_role_name --assume-role-policy-document file://"node-role-trust-relationship.json"
      ```

   1. Attach the IAM policy to the IAM role\.

      ```
      aws iam attach-role-policy --policy-arn arn:aws:iam::$account_id:policy/AmazonEKS_CNI_IPv6_Policy \
          --role-name $node_role_name
      ```

   1. Attach two required IAM managed policies to the IAM role\.

      ```
      aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy \
        --role-name $node_role_name
      aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly \
        --role-name $node_role_name
      ```

   1. Retrieve the ARN of the IAM role and store it in a variable for a later step\.

      ```
      node_iam_role=$(aws iam get-role --role-name $node_role_name --query="Role.Arn" --output text)
      ```

1. Create a managed node group\.

   1. View the IDs of the subnets that you created in a previous step\.

      ```
      echo $subnets
      ```

      An example output is as follows\.

      ```
      subnet-`0a1a56c486EXAMPLE`,subnet-`099e6ca77aEXAMPLE`,subnet-`0377963d69EXAMPLE`,subnet-`0c05f819d5EXAMPLE`
      ```

   1. Create the node group\. Replace `[replaceable]`0a1a56c486EXAMPLE` `, with the values returned in the output of the previous step. Be sure to remove the commas between subnet IDs from the previous output in the following command. You can replace [replaceable] with any {https---docs-aws-amazon-com-AWSEC2-latest-UserGuide-instance-types-html-ec2-nitro-instances}[AWS Nitro System instance type].` 

      ```
      aws eks create-nodegroup --region $region_code --cluster-name $cluster_name --nodegroup-name $nodegroup_name \
          --subnets subnet-0a1a56c486EXAMPLE subnet-099e6ca77aEXAMPLE subnet-0377963d69EXAMPLE subnet-0c05f819d5EXAMPLE \
          --instance-types t3.medium --node-role $node_iam_role
      ```

       The node group takes a few minutes to create\. Run the following command\. Don’t proceed to the next step until the output returned is `ACTIVE`\. 

      `ACTIVE`\. 

      \. 

      ```
      aws eks describe-nodegroup --region $region_code --cluster-name $cluster_name --nodegroup-name $nodegroup_name \
          --query nodegroup.status --output text
      ```

1. Confirm that the default Pods are assigned `IPv6` addresses in the `IP` column\.

   ```
   kubectl get pods -n kube-system -o wide
   ```

   An example output is as follows\.

   ```
   NAME                       READY   STATUS    RESTARTS   AGE     IP                                       NODE                                            NOMINATED NODE   READINESS GATES
   aws-node-rslts             1/1     Running   1          5m36s   2600:1f13:b66:8200:11a5:ade0:c590:6ac8   ip-192-168-34-75.region-code.compute.internal   <none>           <none>
   aws-node-t74jh             1/1     Running   0          5m32s   2600:1f13:b66:8203:4516:2080:8ced:1ca9   ip-192-168-253-70.region-code.compute.internal  <none>           <none>
   coredns-85d5b4454c-cw7w2   1/1     Running   0          56m     2600:1f13:b66:8203:34e5::                ip-192-168-253-70.region-code.compute.internal  <none>           <none>
   coredns-85d5b4454c-tx6n8   1/1     Running   0          56m     2600:1f13:b66:8203:34e5::1               ip-192-168-253-70.region-code.compute.internal  <none>           <none>
   kube-proxy-btpbk           1/1     Running   0          5m36s   2600:1f13:b66:8200:11a5:ade0:c590:6ac8   ip-192-168-34-75.region-code.compute.internal   <none>           <none>
   kube-proxy-jjk2g           1/1     Running   0          5m33s   2600:1f13:b66:8203:4516:2080:8ced:1ca9   ip-192-168-253-70.region-code.compute.internal  <none>           <none>
   ```

1. Confirm that the default services are assigned `IPv6` addresses in the `IP` column\.

   ```
   kubectl get services -n kube-system -o wide
   ```

   An example output is as follows\.

   ```
   NAME       TYPE        CLUSTER-IP          EXTERNAL-IP   PORT(S)         AGE   SELECTOR
   kube-dns   ClusterIP   fd30:3087:b6c2::a   <none>        53/UDP,53/TCP   57m   k8s-app=kube-dns
   ```

1. After you’ve finished with the cluster and nodes that you created for this tutorial, you should clean up the resources that you created with the following commands\. Make sure that you’re not using any of the resources outside of this tutorial before deleting them\.

   1. If you’re completing this step in a different shell than you completed the previous steps in, set the values of all the variables used in previous steps, replacing the ` example values ` with the values you specified when you completed the previous steps\. If you’re completing this step in the same shell that you completed the previous steps in, skip to the next step\.

      ```
      export region_code=region-code
      export vpc_stack_name=my-eks-ipv6-vpc
      export cluster_name=my-cluster
      export nodegroup_name=my-nodegroup
      export account_id=111122223333
      export node_role_name=AmazonEKSNodeRole
      export cluster_role_name=myAmazonEKSClusterRole
      ```

   1. Delete your node group\.

      ```
      aws eks delete-nodegroup --region $region_code --cluster-name $cluster_name --nodegroup-name $nodegroup_name
      ```

      Deletion takes a few minutes\. Run the following command\. Don’t proceed to the next step if any output is returned\.

      ```
      aws eks list-nodegroups --region $region_code --cluster-name $cluster_name --query nodegroups --output text
      ```

   1. Delete the cluster\.

      ```
      aws eks delete-cluster --region $region_code --name $cluster_name
      ```

      The cluster takes a few minutes to delete\. Before continuing make sure that the cluster is deleted with the following command\.

      ```
      aws eks describe-cluster --region $region_code --name $cluster_name
      ```

      Don’t proceed to the next step until your output is similar to the following output\.

      ```
      An error occurred (ResourceNotFoundException) when calling the DescribeCluster operation: No cluster found for name:`my-cluster`.
      ```

   1. Delete the IAM resources that you created\. Replace ` AmazonEKS_CNI_IPv6_Policy ` with the name you chose, if you chose a different name than the one used in previous steps\.

      ```
      aws iam detach-role-policy --role-name $cluster_role_name --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy
      aws iam detach-role-policy --role-name $node_role_name --policy-arn arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy
      aws iam detach-role-policy --role-name $node_role_name --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly
      aws iam detach-role-policy --role-name $node_role_name --policy-arn arn:aws:iam::$account_id:policy/AmazonEKS_CNI_IPv6_Policy
      aws iam delete-policy --policy-arn arn:aws:iam::$account_id:policy/AmazonEKS_CNI_IPv6_Policy
      aws iam delete-role --role-name $cluster_role_name
      aws iam delete-role --role-name $node_role_name
      ```

   1. Delete the AWS CloudFormation stack that created the VPC\.

      ```
      aws cloudformation delete-stack --region $region_code --stack-name $vpc_stack_name
      ```
<a name="external-snat"></a>==== SNAT for Pods   
Learn how to control source network address translation \(SNAT\) for `IPv4` addresses assigned to Pods on your Amazon EC2 nodes\.

For Windows nodes, there are additional details to consider\. By default, the [VPC CNI plugin for Windows](https://github.com/aws/amazon-vpc-cni-plugins/tree/master/plugins/vpc-bridge) is defined with a networking configuration in which the traffic to a destination within the same VPC is excluded for SNAT\. This means that internal VPC communication has SNAT disabled and the IP address allocated to a Pod is routable inside the VPC\. But traffic to a destination outside of the VPC has the source Pod IP SNAT’ed to the instance ENI’s primary IP address\. This default configuration for Windows ensures that the pod can access networks outside of your VPC in the same way as the host instance\.

**Example**  
Due to this behavior:  
+ Your Pods can communicate with internet resources only if the node that they’re running on has a \{https\-\-\-docs\-aws\-amazon\-com\-AWSEC2\-latest\-UserGuide\-using\-instance\-addressing\-html\-concepts\-public\-addresses\}\[public\] or [elastic](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-eips.html) IP address assigned to it and is in a [public subnet](https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html#subnet-basics)\. A public subnet’s associated [route table](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html) has a route to an internet gateway\. We recommend deploying nodes to private subnets, whenever possible\.
+ For versions of the plugin earlier than `1.8.0`, resources that are in networks or VPCs that are connected to your cluster VPC using [VPC peering](https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html), a [transit VPC](https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/transit-vpc-option.html), or [AWS Direct Connect](https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html) can’t initiate communication to your Pods behind secondary elastic network interfaces\. Your Pods can initiate communication to those resources and receive responses from them, though\.
If either of the following statements are true in your environment, then change the default configuration with the command that follows\.  
+ You have resources in networks or VPCs that are connected to your cluster VPC using [VPC peering](https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html), a [transit VPC](https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/transit-vpc-option.html), or [AWS Direct Connect](https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html) that need to initiate communication with your Pods using an `IPv4` address and your plugin version is earlier than `1.8.0`\.
+ Your Pods are in a [private subnet](https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html#subnet-basics) and need to communicate outbound to the internet\. The subnet has a route to a [NAT gateway](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)\.

```
kubectl set env daemonset -n kube-system aws-node {aws}_VPC_K8S_CNI_EXTERNALSNAT=true
```

**Example**  
  ^\*^If a Pod’s spec contains `hostNetwork=true` \(default is `false`\), then its IP address isn’t translated to a different address\. This is the case for the `kube-proxy` and Amazon VPC CNI plugin for  Kubernetes Pods that run on your cluster, by default\. For these Pods, the IP address is the same as the node’s primary IP address, so the Pod’s IP address isn’t translated\. For more information about a Pod’s `hostNetwork` setting, see [PodSpec v1 core](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.29/#podspec-v1-core) in the Kubernetes API reference\.  
<a name="cni-network-policy"></a>==== Configure your cluster for Kubernetes network policies  
Learn how to deploy Kubernetes network policies on your Amazon EKS cluster\.  
By default, there are no restrictions in Kubernetes for IP addresses, ports, or connections between any Pods in your cluster or between your Pods and resources in any other network\. You can use Kubernetes *network policy* to restrict network traffic to and from your Pods\. For more information, see [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) in the Kubernetes documentation\.  
If you have version `1.13` or earlier of the Amazon VPC CNI plugin for  Kubernetes on your cluster, you need to implement a third party solution to apply Kubernetes network policies to your cluster\. Version `1.14` or later of the plugin can implement network policies, so you don’t need to use a third party solution\. In this topic, you learn how to configure your cluster to use Kubernetes network policy on your cluster without using a third party add\-on\.  
Network policies in the Amazon VPC CNI plugin for  Kubernetes are supported in the following configurations\.  
+ Amazon EKS clusters of version `1.25` and later\.
+ Version 1\.14 or later of the Amazon VPC CNI plugin for  Kubernetes on your cluster\.
+ Cluster configured for `IPv4` or `IPv6` addresses\.
+ You can use network policies with *custom networking* and *prefix delegation*\.
<a name="cni-network-policy-considerations"></a>===== Considerations  
+ When applying Amazon VPC CNI plugin for  Kubernetes network policies to your cluster with the Amazon VPC CNI plugin for  Kubernetes , you can apply the policies to Amazon EC2 Linux nodes only\. You can’t apply the policies to Fargate or Windows nodes\.
+ If your cluster is currently using a third party solution to manage Kubernetes network policies, you can use those same policies with the Amazon VPC CNI plugin for  Kubernetes\. However you must remove your existing solution so that it isn’t managing the same policies\.
+ You can apply multiple network policies to the same Pod\. When two or more policies that select the same Pod are configured, all policies are applied to the Pod\.
+ The maximum number of unique combinations of ports for each protocol in each `ingress:` or `egress:` selector in a network policy is 24\.
+ For any of your Kubernetes services, the service port must be the same as the container port\. If you’re using named ports, use the same name in the service spec too\. \* \.Policy enforcement at Pod startup The Amazon VPC CNI plugin for  Kubernetes configures network policies for pods in parallel with the pod provisioning\. Until all of the policies are configured for the new pod, containers in the new pod will start with a *default allow policy*\. This is called *standard mode*\. A default allow policy means that all ingress and egress traffic is allowed to and from the new pods\.

  You can change this default network policy by setting the environment variable `NETWORK_POLICY_ENFORCING_MODE` to `strict` in the `aws-node` container of the VPC CNI `DaemonSet`\.

  ```
  env:
    - name: NETWORK_POLICY_ENFORCING_MODE
      value: "strict"
  ```

  With the `NETWORK_POLICY_ENFORCING_MODE` variable set to `strict`, pods that use the VPC CNI start with a *default deny policy*, then policies are configured\. This is called *strict mode*\. In strict mode, you must have a network policy for every endpoint that your pods need to access in your cluster\. Note that this requirement applies to the CoreDNS pods\. The default deny policy isn’t configured for pods with Host networking\.
+ The network policy feature creates and requires a `PolicyEndpoint` Custom Resource Definition \(CRD\) called `policyendpoints.networking.k8s.aws`\. `PolicyEndpoint` objects of the Custom Resource are managed by Amazon EKS\. You shouldn’t modify or delete these resources\.
+ If you run pods that use the instance role IAM credentials or connect to the EC2 IMDS, be careful to check for network policies that would block access to the EC2 IMDS\. You may need to add a network policy to allow access to EC2 IMDS\. For more information, see [https://docs\.aws\.amazon\.com/](https://docs.aws.amazon.com/) AWSEC2/latest/UserGuide/ec2\-instance\-metadata\.html\[Instance metadata and user data\] in the Amazon EC2 User Guide for Linux Instances\.

  Pods that use *IAM roles for service accounts* don’t access EC2 IMDS\.
+ The Amazon VPC CNI plugin for  Kubernetes doesn’t apply network policies to additional network interfaces for each pod, only the primary interface for each pod \(`eth0`\)\. This affects the following architectures:
  +  `IPv6` pods with the `ENABLE_V4_EGRESS` variable set to `true`\. This variable enables the `IPv4` egress feature to connect the IPv6 pods to `IPv4` endpoints such as those outside the cluster\. The `IPv4` egress feature works by creating an additional network interface with a local loopback IPv4 address\.
  + When using chained network plugins such as Multus\. Because these plugins add network interfaces to each pod, network policies aren’t applied to the chained network plugins\.
+ The network policy feature uses port `8162` on the node for metrics by default\. Also, the feature used port `8163` for health probes\. If you run another application on the nodes or inside pods that needs to use these ports, the app fails to run\. In VPC CNI version `v1.14.1` or later, you can change these ports port in the following places:  
 AWS Management Console  

  1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

  1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to configure the Amazon VPC CNI add\-on for\.

  1. Choose the **Add\-ons** tab\.

  1. Select the box in the top right of the add\-on box and then choose **Edit**\.

  1. On the **Configure *name of addon* ** page:

     1. Select a `v1.14.0-eksbuild.3` or later version in the **Version** dropdown list\.

     1. Expand the **Optional configuration settings**\.

     1. Enter the JSON key `"enableNetworkPolicy":` and value `"true"` in **Configuration values**\. The resulting text must be a valid JSON object\. If this key and value are the only data in the text box, surround the key and value with curly braces `{}`\.

        The following example has network policy feature enabled, the network policy logs enabled, the network policy logs sent to Amazon CloudWatch Logs, and the metrics and health probes are set to the default port numbers:

        ```
        {
            "enableNetworkPolicy": "true",
            "nodeAgent": {
                "enablePolicyEventLogs": "true",
                "enableCloudWatchLogs": "true",
                "healthProbeBindAddr": "8163",
                "metricsBindAddr": "8162"
            }
        }
        ```  
Helm  
If you have installed the Amazon VPC CNI plugin for  Kubernetes through `helm`, you can update the configuration to change the ports\.  

  1. Run the following command to change the ports\. Set the port number in the value for either key `nodeAgent.metricsBindAddr` or key `nodeAgent.healthProbeBindAddr`, respectively\.

     ```
     helm upgrade --set nodeAgent.metricsBindAddr=8162 --set nodeAgent.healthProbeBindAddr=8163 aws-vpc-cni --namespace kube-system eks/aws-vpc-cni
     ```  
 kubectl   

  1. Open the `aws\-node``DaemonSet` in your editor\.

     ```
     kubectl edit daemonset -n kube-system aws-node
     ```

  1. Replace the port numbers in the following command arguments in the `args:` in the `aws-network-policy-agent` container in the VPC CNI `aws-node` daemonset manifest\.

     ```
         - args:
                 - --metrics-bind-addr=:8162
                 - --health-probe-bind-addr=:8163
     ```
<a name="cni-network-policy-prereqs"></a>===== Prerequisites  
\* \.Minimum cluster version An existing Amazon EKS cluster\. To deploy one, see \. The cluster must be Kubernetes version `1.25` or later\. The cluster must be running one of the Kubernetes versions and platform versions listed in the following table\. Note that any Kubernetes and platform versions later than those listed are also supported\. You can check your current Kubernetes version by replacing *my\-cluster* in the following command with the name of your cluster and then running the modified command:  
\+  

```
aws eks describe-cluster
              --name my-cluster --query cluster.version --output
              text
```
\+  
 `1.27.4`   
 `eks.5`   
 `1.26.7`   
 `eks.6`   
 `1.25.12`   
 `eks.7` \* \.Minimum VPC CNI version Version `1.14` or later of the Amazon VPC CNI plugin for  Kubernetes on your cluster\. You can see which version that you currently have with the following command\.  
\+  

```
kubectl describe daemonset aws-node --namespace kube-system | grep amazon-k8s-cni: | cut -d : -f 3
```
\+  
\* \.Minimum Linux kernel version Your nodes must have Linux kernel version `5.10` or later\. You can check your kernel version with `uname -r`\. If you’re using the latest versions of the Amazon EKS optimized Amazon Linux, Amazon EKS optimized accelerated Amazon Linux AMIs, and Bottlerocket AMIs, they already have the required kernel version\.  
\+  
The Amazon EKS optimized accelerated Amazon Linux AMI version `v20231116` or later have kernel version `5.10`\.  
<a name="cni-network-policy-setup"></a>===== To configure your cluster to use Kubernetes network policies \.  
\+ NOTE: If your cluster is version `1.27` or later, you can skip this step as all Amazon EKS optimized Amazon Linux and Bottlerocket AMIs for `1.27` or later have this feature already\.  
For all other cluster versions, if you upgrade the Amazon EKS optimized Amazon Linux to version `v20230703` or later or you upgrade the Bottlerocket AMI to version `v1.0.2` or later, you can skip this step\.  
\+  
\+ \.\. Mount the Berkeley Packet Filter \(BPF\) file system on each of your nodes\.  
\+  

```
sudo mount -t bpf bpffs /sys/fs/bpf
```

1. Then, add the same command to your user data in your launch template for your Amazon EC2 Auto Scaling Groups\. \.

1. See which type of the add\-on is installed on your cluster\. Depending on the tool that you created your cluster with, you might not currently have the Amazon EKS add\-on type installed on your cluster\. Replace *my\-cluster* with the name of your cluster\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name vpc-cni --query addon.addonVersion --output text
   ```

   If a version number is returned, you have the Amazon EKS type of the add\-on installed on your cluster and don’t need to complete the remaining steps in this procedure\. If an error is returned, you don’t have the Amazon EKS type of the add\-on installed on your cluster\. a\. Amazon EKS add\-on

   \+  
 AWS Management Console:  

   1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

   1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to configure the Amazon VPC CNI add\-on for\.

   1. Choose the **Add\-ons** tab\.

   1. Select the box in the top right of the add\-on box and then choose **Edit**\.

   1. On the **Configure *name of addon* ** page:

      1. Select a `v1.14.0-eksbuild.3` or later version in the **Version** dropdown list\.

      1. Expand the **Optional configuration settings**\.

      1. Enter the JSON key `"enableNetworkPolicy":` and value `"true"` in **Configuration values**\. The resulting text must be a valid JSON object\. If this key and value are the only data in the text box, surround the key and value with curly braces `{}`\. The following example shows network policy is enabled:

         ```
         { "enableNetworkPolicy": "true" }
         ```

         The following screenshot shows an example of this scenario\.  
![\[<shared id="AWS"/> Management Console showing the VPC CNI add-on with network policy in the optional configuration.\]](http://docs.aws.amazon.com/eks/latest/userguide/images/console-cni-config-network-policy.png)  
 AWS CLI:  

   1. Run the following AWS CLI command\. Replace `my-cluster` with the name of your cluster and the IAM role ARN with the role that you are using\.

      ```
      aws eks update-addon --cluster-name my-cluster --addon-name vpc-cni --addon-version v1.14.0-eksbuild.3 \
          --service-account-role-arn arn:aws:iam::123456789012:role/AmazonEKSVPCCNIRole \
          --resolve-conflicts PRESERVE --configuration-values '{"enableNetworkPolicy": "true"}'
      ```

      1. Self\-managed add\-on  
Helm:  
If you have installed the Amazon VPC CNI plugin for  Kubernetes through `helm`, you can update the configuration to enable network policy\.

   1. Run the following command to enable network policy\.

      ```
      helm upgrade --set enableNetworkPolicy=true aws-vpc-cni --namespace kube-system eks/aws-vpc-cni
      ```  
 kubectl:  

   1. Open the `amazon\-vpc\-cni``ConfigMap` in your editor\.

      ```
      kubectl edit configmap -n kube-system amazon-vpc-cni -o yaml
      ```

   1. Add the following line to the `data` in the `ConfigMap`\.

      ```
      enable-network-policy-controller: "true"
      ```

      Once you’ve added the line, your `ConfigMap` should look like the following example\.

      ```
      apiVersion: v1
       kind: ConfigMap
       metadata:
        name: amazon-vpc-cni
        namespace: kube-system
       data:
        enable-network-policy-controller: "true"
      ```

   1. Open the `aws\-node``DaemonSet` in your editor\.

      ```
      kubectl edit daemonset -n kube-system aws-node
      ```

   1. Replace the `false` with `true` in the command argument `--enable-network-policy=false` in the `args:` in the `aws-network-policy-agent` container in the VPC CNI `aws-node` daemonset manifest\.

      ```
           - args:
              - --enable-network-policy=true
      ```

      1. Confirm that the `aws-node` pods are running on your cluster\.

         ```
         kubectl get pods -n kube-system | grep 'aws-node\|amazon'
         ```

         An example output is as follows\.

         ```
         aws-node-`gmqp7`2/2     Running   1 (24h ago)   24h
         aws-node-`prnsh`2/2     Running   1 (24h ago)   24h
         ```

         If network policy is enabled, there are 2 containers in the `aws-node` pods\. In previous versions and if network policy is disabled, there is only a single container in the `aws-node` pods\.
<a name="network-policy-stars-demo"></a>===== Stars demo of network policy  
This demo creates a front\-end, back\-end, and client service on your Amazon EKS cluster\. The demo also creates a management graphical user interface that shows the available ingress and egress paths between each service\. We recommend that you complete the demo on a cluster that you don’t run production workloads on\.  
Before you create any network policies, all services can communicate bidirectionally\. After you apply the network policies, you can see that the client can only communicate with the front\-end service, and the back\-end only accepts traffic from the front\-end\.  

1. Apply the front\-end, back\-end, client, and management user interface services:

   ```
   kubectl apply -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/create_resources.files/namespace.yaml
   kubectl apply -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/create_resources.files/management-ui.yaml
   kubectl apply -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/create_resources.files/backend.yaml
   kubectl apply -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/create_resources.files/frontend.yaml
   kubectl apply -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/create_resources.files/client.yaml
   ```

1. View all Pods on the cluster\.

   ```
   kubectl get pods -A
   ```

   An example output is as follows\.

   In your output, you should see pods in the namespaces shown in the following output\. The *NAMES* of your pods and the number of pods in the `READY` column are different than those in the following output\. Don’t continue until you see pods with similar names and they all have `Running` in the `STATUS` column\.

   ```
   NAMESPACE         NAME                                       READY   STATUS    RESTARTS   AGE
   [...]
   client            client-xlffc                               1/1     Running   0          5m19s
   [...]
   management-ui     management-ui-qrb2g                        1/1     Running   0          5m24s
   stars             backend-sz87q                              1/1     Running   0          5m23s
   stars             frontend-cscnf                             1/1     Running   0          5m21s
   [...]
   ```

1. To connect to the management user interface, connect to the `EXTERNAL-IP` of the service running on your cluster:

   ```
   kubectl get service/management-ui -n management-ui
   ```

1. Open the a browser to the location from the previous step\. You should see the management user interface\. The **C** node is the client service, the **F** node is the front\-end service, and the **B** node is the back\-end service\. Each node has full communication access to all other nodes, as indicated by the bold, colored lines\.  
![\[Open network policy\]](http://docs.aws.amazon.com/eks/latest/userguide/images/stars-default.png)

1. Apply the following network policy in both the `stars` and `client` namespaces to isolate the services from each other:

   ```
   kind: NetworkPolicy
   apiVersion: networking.k8s.io/v1
   metadata:
     name: default-deny
   spec:
     podSelector:
       matchLabels: {}
   ```

   You can use the following commands to apply the policy to both namespaces:

   ```
   kubectl apply -n stars -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/apply_network_policies.files/default-deny.yaml
   kubectl apply -n client -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/apply_network_policies.files/default-deny.yaml
   ```

1. Refresh your browser\. You see that the management user interface can no longer reach any of the nodes, so they don’t show up in the user interface\.

1. Apply the following different network policies to allow the management user interface to access the services\. Apply this policy to allow the UI:

   ```
   kind: NetworkPolicy
   apiVersion: networking.k8s.io/v1
   metadata:
     namespace: stars
     name: allow-ui
   spec:
     podSelector:
       matchLabels: {}
     ingress:
       - from:
           - namespaceSelector:
               matchLabels:
                 role: management-ui
   ```

   Apply this policy to allow the client:

   ```
   kind: NetworkPolicy
   apiVersion: networking.k8s.io/v1
   metadata:
     namespace: client
     name: allow-ui
   spec:
     podSelector:
       matchLabels: {}
     ingress:
       - from:
           - namespaceSelector:
               matchLabels:
                 role: management-ui
   ```

   You can use the following commands to apply both policies:

   ```
   kubectl apply -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/apply_network_policies.files/allow-ui.yaml
   kubectl apply -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/apply_network_policies.files/allow-ui-client.yaml
   ```

1. Refresh your browser\. You see that the management user interface can reach the nodes again, but the nodes cannot communicate with each other\.  
![\[UI access network policy\]](http://docs.aws.amazon.com/eks/latest/userguide/images/stars-no-traffic.png)

1. Apply the following network policy to allow traffic from the front\-end service to the back\-end service:

   ```
   kind: NetworkPolicy
   apiVersion: networking.k8s.io/v1
   metadata:
     namespace: stars
     name: backend-policy
   spec:
     podSelector:
       matchLabels:
         role: backend
     ingress:
       - from:
           - podSelector:
               matchLabels:
                 role: frontend
         ports:
           - protocol: TCP
             port: 6379
   ```

1. Refresh your browser\. You see that the front\-end can communicate with the back\-end\.  
![\[Front-end to back-end policy\]](http://docs.aws.amazon.com/eks/latest/userguide/images/stars-front-end-back-end.png)

1. Apply the following network policy to allow traffic from the client to the front\-end service:

   ```
   kind: NetworkPolicy
   apiVersion: networking.k8s.io/v1
   metadata:
     namespace: stars
     name: frontend-policy
   spec:
     podSelector:
       matchLabels:
         role: frontend
     ingress:
       - from:
           - namespaceSelector:
               matchLabels:
                 role: client
         ports:
           - protocol: TCP
             port: 80
   ```

1. Refresh your browser\. You see that the client can communicate to the front\-end service\. The front\-end service can still communicate to the back\-end service\.  
![\[Final network policy\]](http://docs.aws.amazon.com/eks/latest/userguide/images/stars-final.png)

1. \(Optional\) When you are done with the demo, you can delete its resources\.

   ```
   kubectl delete -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/create_resources.files/client.yaml
   kubectl delete -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/create_resources.files/frontend.yaml
   kubectl delete -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/create_resources.files/backend.yaml
   kubectl delete -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/create_resources.files/management-ui.yaml
   kubectl delete -f https://eksworkshop.com/beginner/120_network-policies/calico/stars_policy_demo/create_resources.files/namespace.yaml
   ```

   Even after deleting the resources, there can still be network policy endpoints on the nodes that might interfere in unexpected ways with networking in your cluster\. The only sure way to remove these rules is to reboot the nodes or terminate all of the nodes and recycle them\. To terminate all nodes, either set the Auto Scaling Group desired count to 0, then back up to the desired number, or just terminate the nodes\.
<a name="network-policies-troubleshooting"></a>===== Troubleshooting network policies  
<a name="network-policies-troubleshooting-flowlogs"></a>====== Network policy logs  
Whether connections are allowed or denied by a network policies is logged in *flow logs*\. The network policy logs on each node include the flow logs for every pod that has a network policy\. Network policy logs are stored at `/var/log/aws-routed-eni/network-policy-agent.log`\. The following example is from a `network-policy-agent.log` file:  

```
{"level":"info","timestamp":"2023-05-30T16:05:32.573Z","logger":"ebpf-client","msg":"Flow Info: ","Src
IP":"192.168.87.155","Src Port":38971,"Dest IP":"64.6.160","Dest
Port":53,"Proto":"UDP","Verdict":"ACCEPT"}
```
Network policy logs are disabled by default\. To enable the network policy logs, follow these steps:

Network policy logs require an additional 1 vCPU for the `aws-network-policy-agent` container in the VPC CNI `aws-node` daemonset manifest\.

**Example**  
<a name="cni-network-policy-flowlogs-addon"></a>======= Amazon EKS add\-on    
 AWS Management Console  
\*  

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to configure the Amazon VPC CNI add\-on for\.

1. Choose the **Add\-ons** tab\.

1. Select the box in the top right of the add\-on box and then choose **Edit**\.

1. On the **Configure *name of addon* ** page:

   1. Select a `v1.14.0-eksbuild.3` or later version in the **Version** dropdown list\.

   1. Expand the **Optional configuration settings**\.

   1. Enter the top\-level JSON key `"nodeAgent":` and value is an object with a key `"enablePolicyEventLogs":` and value of `"true"` in **Configuration values**\. The resulting text must be a valid JSON object\. The following example shows network policy and the network policy logs are enabled, and the network policy logs are sent to CloudWatch Logs:

      ```
      {
          "enableNetworkPolicy": "true",
          "nodeAgent": {
              "enablePolicyEventLogs": "true"
          }
      }
      ```
The following screenshot shows an example of this scenario\.  
\+ image::images/console\-cni\-config\-network\-policy\-logs\.png\[AWS Management Console showing the VPC CNI add\-on with network policy and CloudWatch Logs in the optional configuration\.,scaledwidth=80%\]  
 AWS CLI  

1. Run the following AWS CLI command\. Replace `my-cluster` with the name of your cluster and replace the IAM role ARN with the role that you are using\.

   ```
   aws eks update-addon --cluster-name my-cluster --addon-name vpc-cni --addon-version v1.14.0-eksbuild.3 \
       --service-account-role-arn arn:aws:iam::123456789012:role/AmazonEKSVPCCNIRole \
       --resolve-conflicts PRESERVE --configuration-values '{"nodeAgent": {"enablePolicyEventLogs": "true"}}'
   ```
<a name="cni-network-policy-flowlogs-selfmanaged"></a>======= Self\-managed add\-on    
Helm  
If you have installed the Amazon VPC CNI plugin for  Kubernetes through `helm`, you can update the configuration to write the network policy logs\.  

1. Run the following command to enable network policy\.

   ```
   helm upgrade --set nodeAgent.enablePolicyEventLogs=true aws-vpc-cni --namespace kube-system eks/aws-vpc-cni
   ```  
 kubectl   
If you have installed the Amazon VPC CNI plugin for  Kubernetes through `kubectl`, you can update the configuration to write the network policy logs\.  

1. Open the `aws\-node``DaemonSet` in your editor\.

   ```
   kubectl edit daemonset -n kube-system aws-node
   ```

1. Replace the `false` with `true` in the command argument `--enable-policy-event-logs=false` in the `args:` in the `aws-network-policy-agent` container in the VPC CNI `aws-node` daemonset manifest\.

   ```
        - args:
           - --enable-policy-event-logs=true
   ```
<a name="network-policies-cloudwatchlogs"></a>====== Send network policy logs to Amazon CloudWatch Logs  
You can monitor the network policy logs using services such as Amazon CloudWatch Logs\. You can use the following methods to send the network policy logs to CloudWatch Logs\.  
For EKS clusters, the policy logs will be located under `/aws/eks/cluster-name/cluster/` and for self\-managed K8S clusters, the logs will be placed under `/aws/k8s-cluster/cluster`/\.  
<a name="network-policies-cwl-agent"></a>======= Send network policy logs with Amazon VPC CNI plugin for  Kubernetes   
If you enable network policy, a second container is add to the `aws-node` pods for a *node agent*\. This node agent can send the network policy logs to CloudWatch Logs\.

Only the network policy logs are sent by the node agent\. Other logs made by the VPC CNI aren’t included\.

**Example**  
<a name="cni-network-policy-cwl-agent-prereqs"></a>======== Prerequisites  
+ Add the following permissions as a stanza or separate policy to the IAM role that you are using for the VPC CNI\.

  ```
  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Sid": "VisualEditor0",
              "Effect": "Allow",
              "Action": [
                  "logs:DescribeLogGroups",
                  "logs:CreateLogGroup",
                  "logs:CreateLogStream",
                  "logs:PutLogEvents"
              ],
              "Resource": "*"
          }
      ]
  }
  ```
<a name="cni-network-policy-cwl-agent-addon"></a>======== Amazon EKS add\-on    
 AWS Management Console  
\*  

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to configure the Amazon VPC CNI add\-on for\.

1. Choose the **Add\-ons** tab\.

1. Select the box in the top right of the add\-on box and then choose **Edit**\.

1. On the **Configure *name of addon* ** page:

   1. Select a `v1.14.0-eksbuild.3` or later version in the **Version** dropdown list\.

   1. Expand the **Optional configuration settings**\.

   1. Enter the top\-level JSON key `"nodeAgent":` and value is an object with a key `"enableCloudWatchLogs":` and value of `"true"` in **Configuration values**\. The resulting text must be a valid JSON object\. The following example shows network policy and the network policy logs are enabled, and the logs are sent to CloudWatch Logs:

      ```
      {
          "enableNetworkPolicy": "true",
          "nodeAgent": {
              "enablePolicyEventLogs": "true",
              "enableCloudWatchLogs": "true",
          }
      }
      ```
The following screenshot shows an example of this scenario\.  
\+ image::images/console\-cni\-config\-network\-policy\-logs\-cwl\.png\[AWS Management Console showing the VPC CNI add\-on with network policy and CloudWatch Logs in the optional configuration\.,scaledwidth=80%\]  
 AWS CLI  

1. Run the following AWS CLI command\. Replace `my-cluster` with the name of your cluster and replace the IAM role ARN with the role that you are using\.

   ```
   aws eks update-addon --cluster-name my-cluster --addon-name vpc-cni --addon-version v1.14.0-eksbuild.3 \
       --service-account-role-arn arn:aws:iam::123456789012:role/AmazonEKSVPCCNIRole \
       --resolve-conflicts PRESERVE --configuration-values '{"nodeAgent": {"enablePolicyEventLogs": "true", "enableCloudWatchLogs": "true"}}'
   ```
<a name="cni-network-policy-cwl-agent-selfmanaged"></a>======== Self\-managed add\-on    
Helm  
If you have installed the Amazon VPC CNI plugin for  Kubernetes through `helm`, you can update the configuration to send network policy logs to CloudWatch Logs\.  

1. Run the following command to enable network policy logs and send them to CloudWatch Logs\.

   ```
   helm upgrade --set nodeAgent.enablePolicyEventLogs=true --set nodeAgent.enableCloudWatchLogs=true aws-vpc-cni --namespace kube-system eks/aws-vpc-cni
   ```  
 kubectl   

1. Open the `aws\-node``DaemonSet` in your editor\.

   ```
   kubectl edit daemonset -n kube-system aws-node
   ```

1. Replace the `false` with `true` in two command arguments `--enable-policy-event-logs=false` and `--enable-cloudwatch-logs=false` in the `args:` in the `aws-network-policy-agent` container in the VPC CNI `aws-node` daemonset manifest\.

   ```
        - args:
           - --enable-policy-event-logs=true
           - --enable-cloudwatch-logs=true
   ```
<a name="network-policies-cwl-fluentbit"></a>======= Send network policy logs with a Fluent Bit daemonset  
If you are using Fluent Bit in a daemonset to send logs from your nodes, you can add configuration to include the network policy logs from network policies\. You can use the following example configuration:  

```
    [INPUT]
        Name              tail
        Tag               eksnp.*
        Path              /var/log/aws-routed-eni/network-policy-agent*.log
        Parser            json
        DB                /var/log/aws-routed-eni/flb_npagent.db
        Mem_Buf_Limit     5MB
        Skip_Long_Lines   On
        Refresh_Interval  10
```
<a name="network-policies-ebpf-sdk"></a>====== Included eBPF SDK  
The Amazon VPC CNI plugin for  Kubernetes installs eBPF SDK collection of tools on the nodes\. You can use the eBPF SDK tools to identify issues with network policies\. For example, the following command lists the programs that are running on the node\.  

```
sudo /opt/cni/bin/aws-eks-na-cli ebpf progs
```
To run this command, you can use any method to connect to the node\.  
<a name="network-policies-implement-policies"></a>===== Kubernetes network policies  
To implement Kubernetes network policies you create Kubernetes `NetworkPolicy` objects and deploy them to your cluster\. `NetworkPolicy` objects are scoped to a namespace\. You implement policies to allow or deny traffic between Pods based on label selectors, namespaces, and IP address ranges\. For more information about creating `NetworkPolicy` objects, see [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/#networkpolicy-resource) in the Kubernetes documentation\.  
Enforcement of Kubernetes `NetworkPolicy` objects is implemented using the Extended Berkeley Packet Filter \(\[noloc\]eBPF`)`\. Relative to `iptables` based implementations, it offers lower latency and performance characteristics, including reduced CPU utilization and avoiding sequential lookups\. Additionally, eBPF probes provide access to context rich data that helps debug complex kernel level issues and improve observability\. Amazon EKS supports an eBPF\-based exporter that leverages the probes to log policy results on each node and export the data to external log collectors to aid in debugging\. For more information, see the [eBPF documentation](https://ebpf.io/what-is-ebpf/#what-is-ebpf)\.  
<a name="cni-custom-network"></a>==== Custom networking for pods  
Learn how your Pods can use different security groups and subnets than the primary \{https\-\-\-docs\-aws\-amazon\-com\-AWSEC2\-latest\-UserGuide\-using\-eni\-html\-eni\-basics\}\[elastic network interface\] of the Amazon EC2 node that they run on\.  
By default, when the Amazon VPC CNI plugin for  Kubernetes creates secondary [https://docs\.aws\.amazon\.com/](https://docs.aws.amazon.com/) AWSEC2/latest/UserGuide/using\-eni\.html\[elastic network interfaces\] \(network interfaces\) for your Amazon EC2 node, it creates them in the same subnet as the node’s primary network interface\. It also associates the same security groups to the secondary network interface that are associated to the primary network interface\. For one or more of the following reasons, you might want the plugin to create secondary network interfaces in a different subnet or want to associate different security groups to the secondary network interfaces, or both:  
+ There’s a limited number of `IPv4` addresses that are available in the subnet that the primary network interface is in\. This might limit the number of Pods that you can create in the subnet\. By using a different subnet for secondary network interfaces, you can increase the number of available `IPv4` addresses available for Pods\.
+ For security reasons, your Pods might need to use a different subnet or security groups than the node’s primary network interface\.
+ The nodes are configured in public subnets, and you want to place the Pods in private subnets\. The route table associated to a public subnet includes a route to an internet gateway\. The route table associated to a private subnet doesn’t include a route to an internet gateway\.
+ With custom networking enabled, no IP addresses assigned to the primary network interface are assigned to Pods\. Only IP addresses from secondary network interfaces are assigned to `[noloc]`Pods````\.
+ If your cluster uses the `IPv6` family, you can’t use custom networking\.
+ Even though Pods deployed to subnets specified for secondary network interfaces can use different subnet and security groups than the node’s primary network interface, the subnets and security groups must be in the same VPC as the node\.
+ Familiarity with how the Amazon VPC CNI plugin for  Kubernetes creates secondary network interfaces and assigns IP addresses to Pods\. For more information, see [ENI Allocation](https://github.com/aws/amazon-vpc-cni-k8s#eni-allocation) on GitHub\.
+ Version `2.12.3` or later or version `1.27.160` or later of the AWS Command Line Interface \(AWS CLI\) installed and configured on your device or AWS CloudShell\. To check your current version, use ` `aws --version | cut -d / -f2 | cut -d ' ' -f1 are often several versions behind the latest version of the AWS CLI. To install the latest version, see [Installing](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with aws configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the AWS Command Line Interface User Guide. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version. To update it, see [Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the AWS CloudShell User Guide.` 
+ The `kubectl` command line tool is installed on your device or AWS CloudShell\. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster\. For example, if your cluster version is `1.28`, you can use `kubectl` version `1.27`, `1.28`, or `1.29` with it\. To install or upgrade `kubectl`, see \.
+ We recommend that you complete the steps in this topic in a Bash shell\. If you aren’t using a Bash shell, some script commands such as line continuation characters and the way variables are set and used require adjustment for your shell\. Additionally, the quoting and escaping rules for your shell might be different\. For more information, see [Using quotation marks with strings in the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-parameters-quoting-strings.html) in the AWS Command Line Interface User Guide\.
For this tutorial, we recommend using the `[replaceable]`example values` `, except where it’s noted to replace them. You can replace any `[replaceable] when completing the steps for a production cluster. We recommend completing all steps in the same terminal. This is because variables are set and used throughout the steps and won’t exist in different terminals.`   
The commands in this topic are formatted using the conventions listed in [Using the AWS CLI examples](https://docs.aws.amazon.com/cli/latest/userguide/welcome-examples.html)\. If you’re running commands from the command line against resources that are in a different AWS Region than the default AWS Region defined in the AWS CLI [profile](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-profiles) that you’re using, then you need to add `--region region-code ` to the commands\.  
<a name="custom-networking-create-cluster"></a>===== Step 1: Create a test VPC and cluster  

1. Define a few variables to use in the remaining steps\.

   ```
   export cluster_name=my-custom-networking-cluster
   account_id=$(aws sts get-caller-identity --query Account --output text)
   ```

1. Create a VPC\.

   1. Create a VPC using an Amazon EKS AWS CloudFormation template\.

      ```
      aws cloudformation create-stack --stack-name my-eks-custom-networking-vpc \
        --template-url https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-vpc-private-subnets.yaml \
        --parameters ParameterKey=VpcBlock,ParameterValue=192.168.0.0/24 \
        ParameterKey=PrivateSubnet01Block,ParameterValue=192.168.0.64/27 \
        ParameterKey=PrivateSubnet02Block,ParameterValue=192.168.0.96/27 \
        ParameterKey=PublicSubnet01Block,ParameterValue=192.168.0.0/27 \
        ParameterKey=PublicSubnet02Block,ParameterValue=192.168.0.32/27
      ```

      The AWS CloudFormation stack takes a few minutes to create\. To check on the stack’s deployment status, run the following command\.

      ```
      aws cloudformation describe-stacks --stack-name my-eks-custom-networking-vpc --query Stacks\[\].StackStatus  --output text
      ```

      Don’t continue to the next step until the output of the command is `CREATE_COMPLETE`\.

   1. Define variables with the values of the private subnet IDs created by the template\.

      ```
      subnet_id_1=$(aws cloudformation describe-stack-resources --stack-name my-eks-custom-networking-vpc \
          --query "StackResources[?LogicalResourceId=='PrivateSubnet01'].PhysicalResourceId" --output text)
      subnet_id_2=$(aws cloudformation describe-stack-resources --stack-name my-eks-custom-networking-vpc \
          --query "StackResources[?LogicalResourceId=='PrivateSubnet02'].PhysicalResourceId" --output text)
      ```

   1. Define variables with the Availability Zones of the subnets retrieved in the previous step\.

      ```
      az_1=$(aws ec2 describe-subnets --subnet-ids $subnet_id_1 --query 'Subnets[*].AvailabilityZone' --output text)
      az_2=$(aws ec2 describe-subnets --subnet-ids $subnet_id_2 --query 'Subnets[*].AvailabilityZone' --output text)
      ```

1. Create a cluster IAM role\.

   1. Run the following command to create an IAM trust policy JSON file\.

      ```
      //⁂cat >eks-cluster-role-trust-policy.json <<EOF
      {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect": "Allow",
            "Principal": {
              "Service": "eks.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
          }
        ]
      }
      EOF
      ```

   1. Create the Amazon EKS cluster IAM role\. If necessary, preface `eks-cluster-role-trust-policy.json` with the path on your computer that you wrote the file to in the previous step\. The command associates the trust policy that you created in the previous step to the role\. To create an IAM role, the [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) that is creating the role must be assigned the `iam:CreateRole` action \(permission\)\.

      ```
      //⁂aws iam create-role --role-name myCustomNetworkingAmazonEKSClusterRole --assume-role-policy-document file://"eks-cluster-role-trust-policy.json"
      ```

   1. Attach the Amazon EKS managed policy named [AmazonEKSClusterPolicy](https://console.aws.amazon.com/arn:aws:iam::aws:policy/AmazonEKSClusterPolicy) to the role\. To attach an IAM policy to an [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html), the principal that is attaching the policy must be assigned one of the following IAM actions \(permissions\): `iam:AttachUserPolicy` or `iam:AttachRolePolicy`\.

      ```
      aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy --role-name myCustomNetworkingAmazonEKSClusterRole
      ```

1. Create an Amazon EKS cluster and configure your device to communicate with it\.

   1. Create a cluster\.

      ```
      aws eks create-cluster --name my-custom-networking-cluster \
         --role-arn arn:aws:iam::$account_id:role/myCustomNetworkingAmazonEKSClusterRole \
         --resources-vpc-config subnetIds=$subnet_id_1","$subnet_id_2
      ```
**Note**  
You might receive an error that one of the Availability Zones in your request doesn’t have sufficient capacity to create an Amazon EKS cluster\. If this happens, the error output contains the Availability Zones that can support a new cluster\. Retry creating your cluster with at least two subnets that are located in the supported Availability Zones for your account\. For more information, see \.

   1. The cluster takes several minutes to create\. To check on the cluster’s deployment status, run the following command\.

      ```
      aws eks describe-cluster --name my-custom-networking-cluster --query cluster.status
      ```

      Don’t continue to the next step until the output of the command is `"ACTIVE"`\.

   1. Configure `kubectl` to communicate with your cluster\.

      ```
      aws eks update-kubeconfig --name my-custom-networking-cluster
      ```
<a name="custom-networking-configure-vpc"></a>===== Step 2: Configure your VPC  

1. Retrieve the ID of your cluster VPC and store it in a variable for use in later steps\. For a production cluster, replace * `my-custom-networking-cluster` with the name of your cluster\.* 

   ```
   vpc_id=$(aws eks describe-cluster --name my-custom-networking-cluster --query "cluster.resourcesVpcConfig.vpcId" --output text)
   ```Associate an additional Classless Inter\-Domain Routing \(CIDR\) block with your cluster’s VPC\. The CIDR block can’t overlap with any existing associated CIDR blocks\.

   1. View the current CIDR blocks associated to your VPC\.

      ```
      aws ec2 describe-vpcs --vpc-ids $vpc_id \
          --query 'Vpcs[*].CidrBlockAssociationSet[*].{CIDRBlock: CidrBlock, State: CidrBlockState.State}' --out table
      ```

      An example output is as follows\.

      ```
      ----------------------------------
      //⁂|          DescribeVpcs          |
      +-----------------+--------------+
      //⁂|    CIDRBlock    |    State     |
      +-----------------+--------------+
      //⁂|`192.168.0.0/24`|  associated  |
      +-----------------+--------------+
      ```

   1. Associate an additional CIDR block to your VPC\. For more information, see [Associate additional IPv4 CIDR blocks with your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html#add-ipv4-cidr) in the Amazon VPC User Guide\.

      ```
      aws ec2 associate-vpc-cidr-block --vpc-id $vpc_id --cidr-block 192.168.1.0/24
      ```

   1. Confirm that the new block is associated\.

      ```
      aws ec2 describe-vpcs --vpc-ids $vpc_id --query 'Vpcs[*].CidrBlockAssociationSet[*].{CIDRBlock: CidrBlock, State: CidrBlockState.State}' --out table
      ```

      An example output is as follows\.

      ```
      ----------------------------------
      //⁂|          DescribeVpcs          |
      +-----------------+--------------+
      //⁂|    CIDRBlock    |    State     |
      +-----------------+--------------+
      //⁂|`192.168.0.0/24`|  associated  |
      //⁂|`192.168.1.0/24`|  associated  |
      +-----------------+--------------+
      ```

   Don’t proceed to the next step until your new CIDR block’s `State` is `associated`\.Create as many subnets as you want to use in each Availability Zone that your existing subnets are in\. Specify a CIDR block that’s within the CIDR block that you associated with your VPC in a previous step\.

   1. Create new subnets\. The subnets must be created in a different VPC CIDR block than your existing subnets are in, but in the same Availability Zones as your existing subnets\. In this example, one subnet is created in the new CIDR block in each Availability Zone that the current private subnets exist in\. The IDs of the subnets created are stored in variables for use in later steps\. The `Name` values match the values assigned to the subnets created using the Amazon EKS VPC template in a previous step\. Names aren’t required\. You can use different names\.

      ```
      new_subnet_id_1=$(aws ec2 create-subnet --vpc-id $vpc_id --availability-zone $az_1 --cidr-block 192.168.1.0/27 \
          --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=my-eks-custom-networking-vpc-PrivateSubnet01},{Key=kubernetes.io/role/internal-elb,Value=1}]' \
          --query Subnet.SubnetId --output text)
      new_subnet_id_2=$(aws ec2 create-subnet --vpc-id $vpc_id --availability-zone $az_2 --cidr-block 192.168.1.32/27 \
          --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=my-eks-custom-networking-vpc-PrivateSubnet02},{Key=kubernetes.io/role/internal-elb,Value=1}]' \
          --query Subnet.SubnetId --output text)
      ```
**Important**  
By default, your new subnets are implicitly associated with your VPC’s [main route table](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html#RouteTables)\. This route table allows communication between all the resources that are deployed in the VPC\. However, it doesn’t allow communication with resources that have IP addresses that are outside the CIDR blocks that are associated with your VPC\. You can associate your own route table to your subnets to change this behavior\. For more information, see [Subnet route tables](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html#subnet-route-tables) in the Amazon VPC User Guide\.

   1. View the current subnets in your VPC\.

      ```
      aws ec2 describe-subnets --filters "Name=vpc-id,Values=$vpc_id" \
          --query 'Subnets[*].{SubnetId: SubnetId,AvailabilityZone: AvailabilityZone,CidrBlock: CidrBlock}' \
          --output table
      ```

      An example output is as follows\.

      ```
      ----------------------------------------------------------------------
      //⁂|                           DescribeSubnets                          |
      +------------------+--------------------+----------------------------+
      //⁂| AvailabilityZone |     CidrBlock      |         SubnetId           |
      +------------------+--------------------+----------------------------+
      //⁂|`d`|`192.168.0.0/27`|     subnet-`example1`|
      //⁂|`a`|`192.168.0.32/27`|     subnet-`example2`|
      //⁂|`a`|`192.168.0.64/27`|     subnet-`example3`|
      //⁂|`d`|`192.168.0.96/27`|     subnet-`example4`|
      //⁂|`a`|`192.168.1.0/27`|     subnet-`example5`|
      //⁂|`d`|`192.168.1.32/27`|     subnet-`example6`|
      +------------------+--------------------+----------------------------+
      ```

      You can see the subnets in the `192.168.1.0` CIDR block that you created are in the same Availability Zones as the subnets in the `192.168.0.0` CIDR block\.
<a name="custom-networking-configure-kubernetes"></a>===== Step 3: Configure Kubernetes resources \. Set the ` AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG` environment variable to `true` in the `aws-node `\[noloc\]DaemonSet````\.  
\+  

```
kubectl set env daemonset aws-node -n kube-system {aws}_VPC_K8S_CNI_CUSTOM_NETWORK_CFG=true
```
\+  

```
cluster_security_group_id=$(aws eks describe-cluster --name $cluster_name --query cluster.resourcesVpcConfig.clusterSecurityGroupId --output text)
```

1. Create an `ENIConfig` custom resource for each subnet that you want to deploy Pods in\.

   1.  Create a unique file for each network interface configuration\.

      The following commands create separate `ENIConfig` files for the two subnets that were created in a previous step\. The value for `name` must be unique\. The name is the same as the Availability Zone that the subnet is in\. The cluster security group is assigned to the `ENIConfig`\.

      ```
      //⁂cat >$az_1.yaml <<EOF
      apiVersion: crd.k8s.amazonaws.com/v1alpha1
      kind: ENIConfig
      metadata:
        name: $az_1
      spec:
        securityGroups:
          - $cluster_security_group_id
        subnet: $new_subnet_id_1
      EOF
      ```

```
//⁂cat >$az_2.yaml <<EOF
apiVersion: crd.k8s.amazonaws.com/v1alpha1
kind: ENIConfig
metadata:
  name: $az_2
spec:
  securityGroups:
    - $cluster_security_group_id
  subnet: $new_subnet_id_2
EOF
```
\+  
For a production cluster, you can make the following changes to the previous commands:  
\+ **\* Replace * `$cluster_security_group_id` with the ID of an existing [https://docs\.aws\.amazon\.com/](https://docs.aws.amazon.com/) AWSEC2/latest/UserGuide/ec2\-security\-groups\.html\[security group\] that you want to use for each `ENIConfig`\. * **\* We recommend naming your `ENIConfigs` the same as the Availability Zone that you’ll use the `ENIConfig` for, whenever possible\. You might need to use different names for your `ENIConfigs` than the names of the Availability Zones for a variety of reasons\. For example, if you have more than two subnets in the same Availability Zone and want to use them both with custom networking, then you need multiple `ENIConfigs` for the same Availability Zone\. Since each `ENIConfig` requires a unique name, you can’t name more than one of your `ENIConfigs` using the Availability Zone name\.  
\+  
\+ NOTE: If you don’t specify a valid security group for use with a production cluster and you’re using:  
+ version `1.8.0` or later of the Amazon VPC CNI plugin for  Kubernetes, then the security groups associated with the node’s primary elastic network interface are used\.
+ a version of the Amazon VPC CNI plugin for  Kubernetes that’s earlier than `1.8.0`, then the default security group for the VPC is assigned to secondary network interfaces\.

  IMPORTANT:

  1. Apply each custom resource file that you created to your cluster with the following commands\.

     ```
     kubectl apply -f $az_1.yaml
     kubectl apply -f $az_2.yaml
     ```

     1. Confirm that your `ENIConfigs` were created\.

        ```
        kubectl get ENIConfigs
        ```

        An example output is as follows\.

        ```
        NAME         AGE
        us-west-2a   117s
        us-west-2d   105s
        ```

        Enable Kubernetes to automatically apply the `ENIConfig` for an Availability Zone to any new Amazon EC2 nodes created in your cluster\.

        For a production cluster, check to see if an annotation with the key `k8s.amazonaws.com/eniConfig` for the ` [ENI\_CONFIG\_ANNOTATION\_DEF](https://github.com/aws/amazon-vpc-cni-k8s#eni_config_annotation_def) ` environment variable exists in the container spec for the `aws-node `\[noloc\]

     ```
     kubectl describe daemonset aws-node -n kube-system | grep ENI_CONFIG_ANNOTATION_DEF
     ```

     If output is returned, the annotation exists\. If no output is returned, then the variable is not set\. For a production cluster, you can use either this setting or the setting in the following step\. If you use this setting, it overrides the setting in the following step\. In this tutorial, the setting in the next step is used\.

  1.  Update your `aws-node `\[noloc\]

  ```
  kubectl set env daemonset aws-node -n kube-system ENI_CONFIG_LABEL_DEF=topology.kubernetes.io/zone
  ```
<a name="custom-networking-deploy-nodes"></a>===== Step 4: Deploy Amazon EC2 nodes \. Create a node IAM role\.  
\+ \.\. Run the following command to create an IAM trust policy JSON file\.  
\+  

```
//⁂cat >node-role-trust-relationship.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
```

1. Run the following command to set a variable for your role name\. You can replace ` myCustomNetworkingAmazonEKSNodeRole ` with any name you choose\.

   ```
   //⁂⁂⁂DENY LIST ERROR: [AWSDevDocsChecklist] 40-character IAM secret key⁂⁂⁂
   //⁂export node_role_name=myCustomNetworkingAmazonEKSNodeRol⁂⁂⁂⁂⁂
   ```

1. Create the IAM role and store its returned Amazon Resource Name \(ARN\) in a variable for use in a later step\.

   ```
   //⁂node_role_arn=$(aws iam create-role --role-name $node_role_name --assume-role-policy-document file://"node-role-trust-relationship.json" \
       --query Role.Arn --output text)
   ```

1. Attach three required IAM managed policies to the IAM role\.

   ```
   aws iam attach-role-policy \
     --policy-arn arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy \
     --role-name $node_role_name
   aws iam attach-role-policy \
     --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly \
     --role-name $node_role_name
   aws iam attach-role-policy \
       --policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy \
       --role-name $node_role_name
   ```
   +  **Managed** – Deploy your node group using one of the following options:
     + **Without a launch template or with a launch template without an AMI ID specified** – Run the following command\. For this tutorial, use the `[replaceable]`example values` `. For a production node group, replace all `[replaceable] with your own. The node group name can’t be longer than 63 characters. It must start with letter or digit, but can also include hyphens and underscores for the remaining characters.` 

       ```
       aws eks create-nodegroup --cluster-name $cluster_name --nodegroup-name my-nodegroup \
           --subnets $subnet_id_1 $subnet_id_2 --instance-types t3.medium --node-role $node_role_arn
       ``` **With a launch template with a specified AMI ID** 

       ```
       /etc/eks/bootstrap.sh my-cluster --use-max-pods false --kubelet-extra-args '--max-pods=20'
       ```

       If you’ve created a custom AMI that is not built off the Amazon EKS optimized AMI, then you need to custom create the configuration yourself\. **Self\-managed** 

     ```
     --use-max-pods false --kubelet-extra-args '--max-pods=20'
     ```
Node group creation takes several minutes\. You can check the status of the creation of a managed node group with the following command\.  
\+  

```
aws eks describe-nodegroup --cluster-name $cluster_name --nodegroup-name my-nodegroup --query nodegroup.status --output text
```
\+  
Don’t continue to the next step until the output returned is `ACTIVE`\. \. For the tutorial, you can skip this step\.  
\+  
\+ \.\. Get the list of nodes in your cluster\.  
\+  

```
kubectl get nodes
```
\+  
An example output is as follows\.  
\+  

```
NAME                                          STATUS   ROLES    AGE     VERSION
ip-192-168-0-126.us-west-2.compute.internal   Ready    <none>   8m49s   v1.22.9-eks-810597c
ip-192-168-0-92.us-west-2.compute.internal    Ready    <none>   8m34s   v1.22.9-eks-810597c
```

1. Determine which Availability Zone each node is in\. Run the following command for each node that was returned in the previous step\.

   ```
   aws ec2 describe-instances --filters Name=network-interface.private-dns-name,Values=ip-192-168-0-126.us-west-2.compute.internal \
   --query 'Reservations[].Instances[].{AvailabilityZone: Placement.AvailabilityZone, SubnetId: SubnetId}'
   ```

   An example output is as follows\.

   ```
   [
       {
           "AvailabilityZone": "us-west-2d",
           "SubnetId": "subnet-Example5"
       }
   ]
   ```

1. Annotate each node with the `ENIConfig` that you created for the subnet ID and Availability Zone\. You can only annotate a node with one `ENIConfig`, though multiple nodes can be annotated with the same `ENIConfig`\. Replace the ` example values ` with your own\.

   ```
   kubectl annotate node ip-192-168-0-126.us-west-2.compute.internal k8s.amazonaws.com/eniConfig=EniConfigName1
   kubectl annotate node ip-192-168-0-92.us-west-2.compute.internal k8s.amazonaws.com/eniConfig=EniConfigName2
   ```

   1.  If you had nodes in a production cluster with running Pods before you switched to using the custom networking feature, complete the following tasks:

1. Make sure that you have available nodes that are using the custom networking feature\.

1. Cordon and drain the nodes to gracefully shut down the Pods\. For more information, see [Safely Drain a Node](https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/) in the Kubernetes documentation\.

1. Terminate the nodes\. If the nodes are in an existing managed node group, you can delete the node group\. Copy the command that follows to your device\. Make the following modifications to the command as needed and then run the modified command:
   + Replace ` my-cluster ` with the name for your cluster\.
   + Replace ` my-nodegroup ` with the name for your node group\.

     ```
     aws eks delete-nodegroup --cluster-name my-cluster --nodegroup-name my-nodegroup
     ```

   Only new nodes that are registered with the `k8s.amazonaws.com/eniConfig` label use the custom networking feature\.

   1. Confirm that Pods are assigned an IP address from a CIDR block that’s associated to one of the subnets that you created in a previous step\.

      ```
      kubectl get pods -A -o wide
      ```

      An example output is as follows\.

      ```
      NAMESPACE     NAME                       READY   STATUS    RESTARTS   AGE     IP              NODE                                          NOMINATED NODE   READINESS GATES
      kube-system   aws-node-2rkn4             1/1     Running   0          7m19s   192.168.0.92    ip-192-168-0-92.us-west-2.compute.internal    <none>           <none>
      kube-system   aws-node-k96wp             1/1     Running   0          7m15s   192.168.0.126   ip-192-168-0-126.us-west-2.compute.internal   <none>           <none>
      kube-system   coredns-657694c6f4-smcgr   1/1     Running   0          56m     192.168.1.23    ip-192-168-0-92.us-west-2.compute.internal    <none>           <none>
      kube-system   coredns-657694c6f4-stwv9   1/1     Running   0          56m     192.168.1.28    ip-192-168-0-92.us-west-2.compute.internal    <none>           <none>
      kube-system   kube-proxy-jgshq           1/1     Running   0          7m19s   192.168.0.92    ip-192-168-0-92.us-west-2.compute.internal    <none>           <none>
      kube-system   kube-proxy-wx9vk           1/1     Running   0          7m15s   192.168.0.126   ip-192-168-0-126.us-west-2.compute.internal   <none>           <none>
      ```

      You can see that the `coredns `\[noloc\]

   If a Pod’s `spec` contains `hostNetwork=true`, it’s assigned the primary IP address of the node\. It isn’t assigned an address from the subnets that you added\. By default, this value is set to `false`\. This value is set to `true` for the `kube-proxy` and Amazon VPC CNI plugin for  Kubernetes \(`aws-node`\) Pods that run on your cluster\. This is why the `kube-proxy` and the plugin’s `aws-node` Pods aren’t assigned `192.168.1.x ` addresses in the previous output\. For more information about a Pod’s `hostNetwork` setting, see [PodSpec v1 core](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.29/#podspec-v1-core) in the Kubernetes API reference\.
<a name="custom-network-delete-resources"></a>===== Step 5: Delete tutorial resources  
After you complete the tutorial, we recommend that you delete the resources that you created\. You can then adjust the steps to enable custom networking for a production cluster\.  

1. If the node group that you created was just for testing, then delete it\.

   ```
   aws eks delete-nodegroup --cluster-name $cluster_name --nodegroup-name my-nodegroup
   ```

   Even after the AWS CLI output says that the cluster is deleted, the delete process might not actually be complete\. The delete process takes a few minutes\. Confirm that it’s complete by running the following command\.

   ```
   aws eks describe-nodegroup --cluster-name $cluster_name --nodegroup-name my-nodegroup --query nodegroup.status --output text
   ```

   Don’t continue until the returned output is similar to the following output\.

   ```
   An error occurred (ResourceNotFoundException) when calling the DescribeNodegroup operation: No node group found for name: my-nodegroup.
   ```

1. If the node group that you created was just for testing, then delete the node IAM role\.

   1. Detach the policies from the role\.

      ```
      aws iam detach-role-policy --role-name myCustomNetworkingAmazonEKSNodeRole --policy-arn arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy
      aws iam detach-role-policy --role-name myCustomNetworkingAmazonEKSNodeRole --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly
      aws iam detach-role-policy --role-name myCustomNetworkingAmazonEKSNodeRole --policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy
      ```

   1. Delete the role\.

      ```
      aws iam delete-role --role-name myCustomNetworkingAmazonEKSNodeRole
      ```

1. Delete the cluster\.

   ```
   aws eks delete-cluster --name $cluster_name
   ```

   Confirm the cluster is deleted with the following command\.

   ```
   aws eks describe-cluster --name $cluster_name --query cluster.status --output text
   ```

   When output similar to the following is returned, the cluster is successfully deleted\.

   ```
   An error occurred (ResourceNotFoundException) when calling the DescribeCluster operation: No cluster found for name: my-cluster.
   ```

1. Delete the cluster IAM role\.

   1. Detach the policies from the role\.

      ```
      aws iam detach-role-policy --role-name myCustomNetworkingAmazonEKSClusterRole --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy
      ```

   1. Delete the role\.

      ```
      aws iam delete-role --role-name myCustomNetworkingAmazonEKSClusterRole
      ```

1. Delete the subnets that you created in a previous step\.

   ```
   aws ec2 delete-subnet --subnet-id $new_subnet_id_1
   aws ec2 delete-subnet --subnet-id $new_subnet_id_2
   ```

1. Delete the VPC that you created\.

   ```
   aws cloudformation delete-stack --stack-name my-eks-custom-networking-vpc
   ```
<a name="cni-increase-ip-addresses"></a>==== Increase the amount of available IP addresses for your Amazon EC2 nodes  
Learn how to significantly increase the number of IP addresses that you can assign to Pods on each Amazon EC2 node in your cluster\.  
Each Amazon EC2 instance supports a maximum number of elastic network interfaces and a maximum number of IP addresses that can be assigned to each network interface\. Each node requires one IP address for each network interface\. All other available IP addresses can be assigned to `Pods`\. Each `Pod` requires its own IP address\. As a result, you might have nodes that have available compute and memory resources, but can’t accommodate additional `Pods` because the node has run out of IP addresses to assign to `Pods`\.  
+ Each Amazon EC2 instance type supports a maximum number of Pods\. If your managed node group consists of multiple instance types, the smallest number of maximum Pods for an instance in the cluster is applied to all nodes in the cluster\.
+ By default, the maximum number of `Pods` that you can run on a node is 110, but you can change that number\. If you change the number and have an existing managed node group, the next AMI or launch template update of your node group results in new nodes coming up with the changed value\.
+ When transitioning from assigning IP addresses to assigning IP prefixes, we recommend that you create new node groups to increase the number of available IP addresses, rather than doing a rolling replacement of existing nodes\. Running Pods on a node that has both IP addresses and prefixes assigned can lead to inconsistency in the advertised IP address capacity, impacting the future workloads on the node\. For the recommended way of performing the transition, see [Replace all nodes during migration from Secondary IP mode to Prefix Delegation mode or vice versa](https://github.com/aws/aws-eks-best-practices/blob/master/content/networking/prefix-mode/index_windows.md#replace-all-nodes-during-migration-from-secondary-ip-mode-to-prefix-delegation-mode-or-vice-versa) in the Amazon EKS best practices guide\.
+ For clusters with Linux nodes only\.
  + Once you configure the add\-on to assign prefixes to network interfaces, you can’t downgrade your Amazon VPC CNI plugin for  Kubernetes add\-on to a version lower than `1.9.0` \(or `1.10.1`\) without removing all nodes in all node groups in your cluster\.
  + If you’re also using security groups for Pods, with `POD_SECURITY_GROUP_ENFORCING_MODE`=`standard` and ` AWS_VPC_K8S_CNI_EXTERNALSNAT`=`false`, when your Pods communicate with endpoints outside of your VPC, the node’s security groups are used, rather than any security groups you’ve assigned to your Pods\.
+ The subnets that your Amazon EKS nodes are in must have sufficient contiguous `/28` \(for `IPv4` clusters\) or `/80` \(for `IPv6` clusters\) Classless Inter\-Domain Routing \(CIDR\) blocks\. You can only have Linux nodes in an `IPv6` cluster\. Using IP prefixes can fail if IP addresses are scattered throughout the subnet CIDR\. We recommend that following:
  + Using a subnet CIDR reservation so that even if any IP addresses within the reserved range are still in use, upon their release, the IP addresses aren’t reassigned\. This ensures that prefixes are available for allocation without segmentation\.
  + Use new subnets that are specifically used for running the workloads that IP prefixes are assigned to\. Both Windows and Linux workloads can run in the same subnet when assigning IP prefixes\.
+ To assign IP prefixes to your nodes, your nodes must be AWS Nitro\-based\. Instances that aren’t Nitro\-based continue to allocate individual secondary IP addresses, but have a significantly lower number of IP addresses to assign to Pods than Nitro\-based instances do\.
+  **For clusters with Linux nodes only** – If your cluster is configured for the `IPv4` family, you must have version `1.9.0` or later of the Amazon VPC CNI plugin for  Kubernetes add\-on installed\. You can check your current version with the following command\.

  ```
  kubectl describe daemonset aws-node --namespace kube-system | grep Image | cut -d "/" -f 2
  ```
+  **For clusters with Windows nodes only** 
\+  
You can check your current Kubernetes and platform version by replacing ` my-cluster ` in the following command with the name of your cluster and then running the modified command: `aws eks describe-cluster --name [replaceable]`my\-cluster` --query 'cluster.{"Kubernetes Version": version, "Platform Version": platformVersion}'`\. \. Configure your cluster to assign IP address prefixes to nodes\. Complete the procedure on the tab that matches your node’s operating system\.  
\+    
 Linux   

1. Enable the parameter to assign prefixes to network interfaces for the Amazon VPC CNI `[noloc]`DaemonSet` `. When you deploy a `1.21 or later cluster, version 1.10.1 or later of the [noloc]`Amazon VPC CNI plugin for `[noloc]`Kubernetes`` add\-on is deployed with it\. If you created the cluster with the `IPv6` family, this setting was set to `true` by default\. If you created the cluster with the `IPv4` family, this setting was set to `false` by default\.

   ```
   kubectl set env daemonset aws-node -n kube-system ENABLE_PREFIX_DELEGATION=true
   ```
**Important**  
Even if your subnet has available IP addresses, if the subnet does not have any contiguous `/28` blocks available, you will see the following error in the Amazon VPC CNI plugin for  Kubernetes logs\.

```
InsufficientCidrBlocks: The specified subnet does not have enough free cidr blocks to satisfy the request
```
This can happen due to fragmentation of existing secondary IP addresses spread out across a subnet\. To resolve this error, either create a new subnet and launch Pods there, or use an Amazon EC2 subnet CIDR reservation to reserve space within a subnet for use with prefix assignment\. For more information, see [Subnet CIDR reservations](https://docs.aws.amazon.com/vpc/latest/userguide/subnet-cidr-reservation.html) in the Amazon VPC User Guide\. …​ If you plan to deploy a managed node group without a launch template, or with a launch template that you haven’t specified an AMI ID in, and you’re using a version of the Amazon VPC CNI plugin for  Kubernetes at or later than the versions listed in the prerequisites, then skip to the next step\. Managed node groups automatically calculates the maximum number of Pods for you\.  
\+  
\+ IMPORTANT: Managed node groups enforces a maximum number on the value of `maxPods`\. For instances with less than 30 vCPUs the maximum number is 110 and for all other instances the maximum number is 250\. This maximum number is applied whether prefix delegation is enabled or not\. …​ If you’re using a `1.21` or later cluster configured for `IPv6`, skip to the next step\.  
\+  
Specify the parameters in one of the following options\. To determine which option is right for you and what value to provide for it, see [WARM\_PREFIX\_TARGET, WARM\_IP\_TARGET, and MINIMUM\_IP\_TARGET](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/docs/prefix-and-ip-target.md) on GitHub\.  
\+  
You can replace the ` example values ` with a value greater than zero\.  
\+ **\***\* `WARM_PREFIX_TARGET`   
\+  

```
kubectl set env ds aws-node -n kube-system WARM_PREFIX_TARGET=1
```
+  `WARM_IP_TARGET` or `MINIMUM_IP_TARGET` – If either value is set, it overrides any value set for `WARM_PREFIX_TARGET`\.

  ```
  kubectl set env ds aws-node -n kube-system WARM_IP_TARGET=5
  ```

```
kubectl set env ds aws-node -n kube-system MINIMUM_IP_TARGET=2
```

1. Create one of the following types of node groups with at least one Amazon EC2 Nitro Amazon Linux 2 instance type\. For a list of Nitro instance types, see \{https\-\-\-docs\-aws\-amazon\-com\-AWSEC2\-latest\-UserGuide\-instance\-types\-html\-ec2\-nitro\-instances\}\[Instances built on the Nitro System\] in the Amazon EC2 User Guide for Linux Instances\. This capability is not supported on Windows\. For the options that include `[replaceable]`110````, replace it with either the value from step 3 \(recommended\), or your own value\.

   ```
   --use-max-pods false --kubelet-extra-args '--max-pods=110'
   ```

   If you’re using `eksctl` to create the node group, you can use the following command\.

   ```
   eksctl create nodegroup --cluster my-cluster --managed=false --max-pods-per-node 110
   ```
   +  **Managed** – Deploy your node group using one of the following options:

     ```
     /etc/eks/bootstrap.sh my-cluster \
       --use-max-pods false \
       --kubelet-extra-args '--max-pods=110'
     ```

     If you’re using `eksctl` to create the node group, you can use the following command\.

     ```
     eksctl create nodegroup --cluster my-cluster --max-pods-per-node 110
     ```

     If you’ve created a custom AMI that is not built off the Amazon EKS optimized AMI, then you need to custom create the configuration yourself\.  
 Windows   

1. Enable assignment of IP prefixes\.

   1. Open the `amazon\-vpc\-cni``ConfigMap` for editing\.

      ```
      kubectl edit configmap -n kube-system amazon-vpc-cni -o yaml
      ```

   1. Add the following line to the `data` section\.

      ```
        enable-windows-prefix-delegation: "true"
      ```

   1. Save the file and close the editor\.

   1. Confirm that the line was added to the `ConfigMap`\.

      ```
      kubectl get configmap -n kube-system amazon-vpc-cni -o "jsonpath={.data.enable-windows-prefix-delegation}"
      ```

      If the returned output isn’t `true`, then there might have been an error\. Try completing the step again\.
**Important**  
Even if your subnet has available IP addresses, if the subnet does not have any contiguous `/28` blocks available, you will see the following error in the node events\.

```
"failed to allocate a private IP/Prefix address: InsufficientCidrBlocks: The specified subnet does not have enough free cidr blocks to satisfy the request"
```
This can happen due to fragmentation of existing secondary IP addresses spread out across a subnet\. To resolve this error, either create a new subnet and launch Pods there, or use an Amazon EC2 subnet CIDR reservation to reserve space within a subnet for use with prefix assignment\. For more information, see [Subnet CIDR reservations](https://docs.aws.amazon.com/vpc/latest/userguide/subnet-cidr-reservation.html) in the Amazon VPC User Guide\. …​ \(Optional\) Specify additional configuration for controlling the pre\-scaling and dynamic scaling behavior for your cluster\. For more information, see [Configuration options with Prefix Delegation mode on Windows](https://github.com/aws/amazon-vpc-resource-controller-k8s/blob/master/docs/windows/prefix_delegation_config_options.md) on GitHub\.  
\+ …​\. Open the `amazon\-vpc\-cni``ConfigMap` for editing\.  
\+  

```
kubectl edit configmap -n kube-system amazon-vpc-cni -o yaml
```

1. Replace the ` example values ` with a value greater than zero and add the entries that you require to the `data` section of the `ConfigMap`\. If you set a value for either `warm-ip-target` or `minimum-ip-target`, the value overrides any value set for `warm-prefix-target`\.

   ```
     warm-prefix-target: "1"
     warm-ip-target: "5"
     minimum-ip-target: "2"
   ```

1. Save the file and close the editor\.

   1. Create Windows node groups with at least one Amazon EC2 Nitro instance type\. For a list of Nitro instance types, see \{https\-\-\-docs\-aws\-amazon\-com\-AWSEC2\-latest\-WindowsGuide\-instance\-types\-html\-ec2\-nitro\-instances\}\[Instances built on the Nitro System\] in the Amazon Amazon EC2 User Guide for Windows Instances\. By default, the maximum number of Pods that you can deploy to a node is 110\. If you want to increase or decrease that number, specify the following in the user data for the bootstrap configuration\. Replace ` max-pods-quantity ` with your max pods value\.

      ```
      -KubeletExtraArgs '--max-pods=max-pods-quantity'
      ```

      1. Once your nodes are deployed, view the nodes in your cluster\.

         ```
         kubectl get nodes
         ```

         An example output is as follows\.

         ```
         NAME                                             STATUS     ROLES    AGE   VERSION
         ip-192-168-22-103.region-code.compute.internal   Ready      <none>   19m   v1.XX.X-eks-6b7464
         ip-192-168-97-94.region-code.compute.internal    Ready      <none>   19m   v1.XX.X-eks-6b7464
         ```

      1. Describe one of the nodes to determine the value of `max-pods` for the node and the number of available IP addresses\. Replace ` 192.168.30.193 ` with the `IPv4` address in the name of one of your nodes returned in the previous output\.

         ```
         kubectl describe node ip-192-168-30-193.region-code.compute.internal | grep 'pods\|PrivateIPv4Address'
         ```

         An example output is as follows\.

         ```
         pods:`110`vpc.amazonaws.com/PrivateIPv4Address:`144`
         ```

         In the previous output, `110` is the maximum number of Pods that Kubernetes will deploy to the node, even though *144* IP addresses are available\.
<a name="security-groups-for-pods"></a>==== Security groups for Pods   
Learn about how to assign unique security groups to individual Pods\.  
Security groups for Pods integrate Amazon EC2 security groups with Kubernetes Pods\. You can use Amazon EC2 security groups to define rules that allow inbound and outbound network traffic to and from Pods that you deploy to nodes running on many Amazon EC2 instance types and Fargate\. For a detailed explanation of this capability, see the [Introducing security groups for Pods](https://aws.amazon.com/blogs/containers/introducing-security-groups-for-pods/) blog post\.  
<a name="sg-pods-considerations"></a>===== Considerations  
+ Before deploying security groups for Pods, consider the following limitations and conditions:
+ Security groups for Pods can’t be used with Windows nodes\.
+ Security groups for Pods are supported by most \{https\-\-\-docs\-aws\-amazon\-com\-AWSEC2\-latest\-UserGuide\-instance\-types\-html\-ec2\-nitro\-instances\}\[Nitro\-based\] Amazon EC2 instance families, though not by all generations of a family\. For example, the `m5`, `c5`, `r5`, `m6g`, `c6g`, and `r6g` instance family and generations are supported\. No instance types in the `t` family are supported\. For a complete list of supported instance types, see the [limits\.go](https://github.com/aws/amazon-vpc-resource-controller-k8s/blob/v1.5.0/pkg/aws/vpc/limits.go) file on Github\. Your nodes must be one of the listed instance types that have `IsTrunkingCompatible: true` in that file\.
+ If you’re also using Pod security policies to restrict access to Pod mutation, then the `eks:vpc-resource-controller` Kubernetes user must be specified in the Kubernetes `ClusterRoleBinding` for the `role` that your `psp` is assigned to\. If you’re using the default Amazon EKS `psp`, `role`, and `ClusterRoleBinding`, this is the `eks:podsecuritypolicy:authenticated`ClusterRoleBinding. For example, you add the user to the `subjects:` section, as shown in the following example:

  ```
  [...]
  subjects:
    - kind: Group
      apiGroup: rbac.authorization.k8s.io
      name: system:authenticated
    - apiGroup: rbac.authorization.k8s.io
      kind: User
      name: eks:vpc-resource-controller
    - kind: ServiceAccount
      name: eks-vpc-resource-controller
  ```
+ If you’re using custom networking and security groups for Pods together, the security group specified by security groups for Pods is used instead of the security group specified in the `ENIConfig`\.
+ If you’re using version `1.10.2` or earlier of the Amazon VPC CNI plugin and you include the `terminationGracePeriodSeconds` setting in your Pod spec, the value for the setting can’t be zero\.
+ If you’re using version `1.10` or earlier of the Amazon VPC CNI plugin or version `1.11` with `POD_SECURITY_GROUP_ENFORCING_MODE`=`strict`, which is the default setting, source NAT is disabled for outbound traffic from Pods with assigned security groups so that outbound security group rules are applied\. To access the internet, Pods with assigned security groups must be launched on nodes that are deployed in a private subnet configured with a NAT gateway or instance\. Pods with assigned security groups deployed to public subnets are not able to access the internet\.

  If you’re using version `1.11` or later of the plugin with `POD_SECURITY_GROUP_ENFORCING_MODE`=`standard`, then Pod traffic destined for outside of the VPC is translated to the IP address of the instance’s primary network interface\. For this traffic, the rules in the security groups for the primary network interface are used, rather than the rules in the Pod’s security groups\.
+ Security groups for Pods might lead to higher Pod startup latency for Pods with high churn\. This is due to rate limiting in the resource controller\.
<a name="security-groups-pods-deployment"></a>===== Configure the Amazon VPC CNI plugin for  Kubernetes for security groups for Pods   

1. Check your current Amazon VPC CNI plugin for  Kubernetes version with the following command:

   ```
   kubectl describe daemonset aws-node --namespace kube-system | grep amazon-k8s-cni: | cut -d : -f 3
   ```

   An example output is as follows\.

   ```
   `v1.7.6`
   ```

   1. Retrieve the name of your cluster IAM role and store it in a variable\. Replace ` my-cluster ` with the name of your cluster\.

      ```
      cluster_role=$(aws eks describe-cluster --name my-cluster --query cluster.roleArn --output text | cut -d / -f 2)
      ```

   1. Attach the policy to the role\.

      ```
      aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonEKSVPCResourceController --role-name $cluster_role
      ```

1. Enable the Amazon VPC CNI add\-on to manage network interfaces for Pods by setting the `ENABLE_POD_ENI` variable to `true` in the `aws-node` DaemonSet\. Once this setting is set to `true`, for each node in the cluster the add\-on creates a cninode custom resource\. The VPC resource controller creates and attaches one special network interface called a *trunk network interface* with the description `aws-k8s-trunk-eni`\.

   ```
   kubectl set env daemonset aws-node -n kube-system ENABLE_POD_ENI=true
   ```
**Note**  
The trunk network interface is included in the maximum number of network interfaces supported by the instance type\. For a list of the maximum number of network interfaces supported by each instance type, see \{https\-\-\-docs\-aws\-amazon\-com\-AWSEC2\-latest\-UserGuide\-using\-eni\-html\-AvailableIpPerENI\}\[IP addresses per network interface per instance type\] in the *Amazon EC2 User Guide for Linux Instances*\. If your node already has the maximum number of standard network interfaces attached to it then the VPC resource controller will reserve a space\. You will have to scale down your running Pods enough for the controller to detach and delete a standard network interface, create the trunk network interface, and attach it to the instance\.

1. You can see which of your nodes have a `CNINode` custom resource with the following command\. If `No resources found` is returned, then wait several seconds and try again\. The previous step requires restarting the Amazon VPC CNI plugin for  Kubernetes Pods, which takes several seconds\.

   ```
   $ kubectl get cninode -A
        NAME FEATURES
        ip-192-168-64-141.us-west-2.compute.internal [{"name":"SecurityGroupsForPods"}]
        ip-192-168-7-203.us-west-2.compute.internal [{"name":"SecurityGroupsForPods"}]
   ```

   If you are using VPC CNI versions older than `1.15`, node labels were used instead of the `CNINode` custom resource\. You can see which of your nodes have the node label`aws-k8s-trunk-eni` set to `true` with the following command\. If `No resources found` is returned, then wait several seconds and try again\. The previous step requires restarting the Amazon VPC CNI plugin for  Kubernetes Pods, which takes several seconds\.

   ```
   kubectl get nodes -o wide -l vpc.amazonaws.com/has-trunk-attached=true
   -
   ```

   Once the trunk network interface is created, Pods are assigned secondary IP addresses from the trunk or standard network interfaces\. The trunk interface is automatically deleted if the node is deleted\.

   When you deploy a security group for a Pod in a later step, the VPC resource controller creates a special network interface called a *branch network interface* with a description of `aws-k8s-branch-eni` and associates the security groups to it\. Branch network interfaces are created in addition to the standard and trunk network interfaces attached to the node\.

   If you are using liveness or readiness probes, then you also need to disable TCP early demux, so that the `kubelet` can connect to Pods on branch network interfaces using TCP\. To disable TCP early demux, run the following command:

   ```
   kubectl patch daemonset aws-node -n kube-system \
     -p '{"spec": {"template": {"spec": {"initContainers": [{"env":[{"name":"DISABLE_TCP_EARLY_DEMUX","value":"true"}],"name":"aws-vpc-cni-init"}]}}}}'
   ```
**Note**  
If you’re using `1.11.0` or later of the Amazon VPC CNI plugin for  Kubernetes add\-on and set `POD_SECURITY_GROUP_ENFORCING_MODE`=`standard`, as described in the next step, then you don’t need to run the previous command\.

1. If your cluster uses `NodeLocal DNSCache`, or you want to use Calico network policy with your Pods that have their own security groups, or you have Kubernetes services of type `NodePort` and `LoadBalancer` using instance targets with an `externalTrafficPolicy` set to `Local` for Pods that you want to assign security groups to, then you must be using version `1.11.0` or later of the Amazon VPC CNI plugin for  Kubernetes add\-on, and you must enable the following setting:

   ```
   kubectl set env daemonset aws-node -n kube-system POD_SECURITY_GROUP_ENFORCING_MODE=standard
   ```

   IMPORTANT: ** Pod security group rules aren’t applied to traffic between Pods or between Pods and services, such as `kubelet` or `nodeLocalDNS`, that are on the same node\. Pods using different security groups on the same node can’t communicate because they are configured in different subnets, and routing is disabled between these subnets\. ** Outbound traffic from Pods to addresses outside of the VPC is network address translated to the IP address of the instance’s primary network interface \(unless you’ve also set ` AWS_VPC_K8S_CNI_EXTERNALSNAT=true`\)\. For this traffic, the rules in the security groups for the primary network interface are used, rather than the rules in the Pod’s security groups\. \*\* For this setting to apply to existing Pods, you must restart the Pods or the nodes that the Pods are running on\.
<a name="sg-pods-example-deployment"></a>===== Deploy an example application  

1. Create a Kubernetes namespace to deploy resources to\. You can replace *my\-namespace* with the name of a namespace that you want to use\.

   ```
   kubectl create namespace my-namespace
   ```

1.  Deploy an Amazon EKS `SecurityGroupPolicy` to your cluster\.

   1. Copy the following contents to your device\. You can replace *podSelector* with `serviceAccountSelector` if you’d rather select Pods based on service account labels\. You must specify one selector or the other\. An empty `podSelector` \(example: `podSelector: {}`\) selects all Pods in the namespace\. You can change *my\-role* to the name of your role\. An empty `serviceAccountSelector` selects all service accounts in the namespace\. You can replace *my\-security\-group\-policy* with a name for your `SecurityGroupPolicy` and *my\-namespace* with the namespace that you want to create the `SecurityGroupPolicy` in\.

      You must replace *my\_pod\_security\_group\_id* with the ID of an existing security group\. If you don’t have an existing security group, then you must create one\. For more information, see [https://docs\.aws\.amazon\.com/](https://docs.aws.amazon.com/) AWSEC2/latest/UserGuide/ec2\-security\-groups\.html\[Amazon EC2 security groups for Linux instances\] in the [https://docs\.aws\.amazon\.com/](https://docs.aws.amazon.com/) AWSEC2/latest/UserGuide/\[Amazon EC2 User Guide for Linux Instances\]\. You can specify 1\-5 security group IDs\. If you specify more than one ID, then the combination of all the rules in all the security groups are effective for the selected Pods\.

      ```
      //⁂cat >my-security-group-policy.yaml <<EOF
      apiVersion: vpcresources.k8s.aws/v1beta1
      kind: SecurityGroupPolicy
      metadata:
        name: my-security-group-policy
        namespace: my-namespace
      spec:
        podSelector:
          matchLabels:
            role: my-role
        securityGroups:
          groupIds:
            - my_pod_security_group_id
      EOF
      ```

      IMPORTANT:
The security group or groups that you specify for your Pods must meet the following criteria:  
+ They must exist\. If they don’t exist, then, when you deploy a Pod that matches the selector, your Pod remains stuck in the creation process\. If you describe the Pod, you’ll see an error message similar to the following one: `An error occurred (InvalidSecurityGroupID.NotFound) when calling the CreateNetworkInterface operation: The securityGroup ID '[replaceable]`sg\-05b1d815d1EXAMPLE`' does not exist`\.
+ They must allow inbound communication from the security group applied to your nodes \(for `kubelet`\) over any ports that you’ve configured probes for\.
+ They must allow outbound communication over `TCP` and `UDP` ports 53 to a security group assigned to the Pods \(or nodes that the Pods run on\) running CoreDNS\. The security group for your CoreDNS Pods must allow inbound `TCP` and `UDP` port 53 traffic from the security group that you specify\.
+ They must have necessary inbound and outbound rules to communicate with other Pods that they need to communicate with\.
+ They must have rules that allow the Pods to communicate with the Kubernetes control plane if you’re using the security group with Fargate\. The easiest way to do this is to specify the cluster security group as one of the security groups\.
Security group policies only apply to newly scheduled Pods\. They do not affect running Pods\. \.\. Deploy the policy\.  
\+  

```
kubectl apply -f my-security-group-policy.yaml
```

1. Deploy a sample application with a label that matches the ` my-role ` value for ` podSelector ` that you specified in a previous step\.

   1. Copy the following contents to your device\. Replace the *example values* with your own and then run the modified command\. If you replace *my\-role*, make sure that it’s the same as the value you specified for the selector in a previous step\.

      ```
      //⁂cat >sample-application.yaml <<EOF
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: my-deployment
        namespace: my-namespace
        labels:
          app: my-app
      spec:
        replicas: 4
        selector:
          matchLabels:
            app: my-app
        template:
          metadata:
            labels:
              app: my-app
              role: my-role
          spec:
            terminationGracePeriodSeconds: 120
            containers:
            - name: nginx
              image: public.ecr.aws/nginx/nginx:1.23
              ports:
              - containerPort: 80
      ---
      apiVersion: v1
      kind: Service
      metadata:
        name: my-app
        namespace: my-namespace
        labels:
          app: my-app
      spec:
        selector:
          app: my-app
        ports:
          - protocol: TCP
            port: 80
            targetPort: 80
      EOF
      ```

   1. Deploy the application with the following command\. When you deploy the application, the Amazon VPC CNI plugin for  Kubernetes matches the `role` label and the security groups that you specified in the previous step are applied to the Pod\.

      ```
      kubectl apply -f sample-application.yaml
      ```

1. View the Pods deployed with the sample application\. For the remainder of this topic, this terminal is referred to as `TerminalA`\.

   ```
   kubectl get pods -n my-namespace -o wide
   ```

   An example output is as follows\.

   ```
   NAME                             READY   STATUS    RESTARTS   AGE     IP               NODE                                            NOMINATED NODE   READINESS GATES
   my-deployment-5df6f7687b-4fbjm   1/1     Running   0          7m51s   192.168.53.48    ip-192-168-33-28.region-code.compute.internal   <none>           <none>
   my-deployment-5df6f7687b-j9fl4   1/1     Running   0          7m51s   192.168.70.145   ip-192-168-92-33.region-code.compute.internal   <none>           <none>
   my-deployment-5df6f7687b-rjxcz   1/1     Running   0          7m51s   192.168.73.207   ip-192-168-92-33.region-code.compute.internal   <none>           <none>
   my-deployment-5df6f7687b-zmb42   1/1     Running   0          7m51s   192.168.63.27    ip-192-168-33-28.region-code.compute.internal   <none>           <none>
   ```

   NOTE: ** If any Pods are stuck in the `Waiting` state, then run `kubectl describe pod ` *my\-deployment\-xxxxxxxxxx\-xxxxx* ` -n [replaceable]`my\-namespace` `. If you see state, confirm that your node instance type is listed in [limits\.go](https://github.com/aws/amazon-vpc-resource-controller-k8s/blob/master/pkg/aws/vpc/limits.go) and that the product of the maximum number of branch network interfaces supported by the instance type multiplied times the number of nodes in your node group hasn’t already been met. For example, an m5.large instance supports nine branch network interfaces. If your node group has five nodes, then a maximum of 45 branch network interfaces can be created for the node group. The 46th [noloc]`Pod` that you attempt to deploy will sit in Pending state until another [noloc]`Pod`` that has associated security groups is deleted\.** 
If you run `kubectl describe pod [replaceable]my-deployment-xxxxxxxxxx-xxxxx -n [replaceable]my-namespace ` and see a message similar to the following message, then it can be safely ignored\. This message might appear when the Amazon VPC CNI plugin for  Kubernetes tries to set up host networking and fails while the network interface is being created\. The plugin logs this event until the network interface is created\.  
\+  

```
Failed to createsandbox: rpc error: code = Unknown desc = failed to set up sandbox container "`e24268322e55c8185721f52df6493684f6c2c3bf4fd59c9c121fd4cdc894579f`" network for"`my-deployment-5df6f7687b`-`4fbjm`": networkPlugin
cni failed to set up"`my-deployment-5df6f7687b-4fbjm-c89wx_my-namespace`" network: add cmd: failed to assign an IP address to container
```
\+  
You can’t exceed the maximum number of Pods that can be run on the instance type\. For a list of the maximum number of Pods that you can run on each instance type, see [eni\-max\-pods\.txt](https://github.com/awslabs/amazon-eks-ami/blob/main/templates/shared/runtime/eni-max-pods.txt) on GitHub\. When you delete a Pod that has associated security groups, or delete the node that the Pod is running on, the VPC resource controller deletes the branch network interface\. If you delete a cluster with Pods using Pods for security groups, then the controller doesn’t delete the branch network interfaces, so you’ll need to delete them yourself\. For information about how to delete network interfaces, see \{https\-\-\-docs\-aws\-amazon\-com\-AWSEC2\-latest\-UserGuide\-using\-eni\-html\-delete\-eni\}\[Delete a network interface\] in the Amazon EC2 User Guide for Linux Instances\. \. In a separate terminal, shell into one of the Pods\. For the remainder of this topic, this terminal is referred to as `TerminalB`\. Replace *\[replaceable\]*5df6f7687b`-[replaceable]`4fbjm` ` with the ID of one of the [noloc] returned in your output from the previous step.`   
\+  

```
kubectl exec -it -n my-namespace my-deployment-5df6f7687b-4fbjm -- /bin/bash
```

1. From the shell in `TerminalB`, confirm that the sample application works\.

   ```
   curl my-app
   ```

   An example output is as follows\.

   ```
   <!DOCTYPE html>
   <html>
   <head>
   <title>Welcome to nginx!</title>
   [...]
   ```

   You received the output because all Pods running the application are associated with the security group that you created\. That group contains a rule that allows all traffic between all Pods that the security group is associated to\. DNS traffic is allowed outbound from that security group to the cluster security group, which is associated with your nodes\. The nodes are running the CoreDNS Pods, which your Pods did a name lookup to\.

1. From `TerminalA`, remove the security group rules that allow DNS communication to the cluster security group from your security group\. If you didn’t add the DNS rules to the cluster security group in a previous step, then replace ` $my_cluster_security_group_id ` with the ID of the security group that you created the rules in\.

   ```
   aws ec2 revoke-security-group-ingress --group-id $my_cluster_security_group_id --security-group-rule-ids $my_tcp_rule_id
   aws ec2 revoke-security-group-ingress --group-id $my_cluster_security_group_id --security-group-rule-ids $my_udp_rule_id
   ```

1. From `TerminalB`, attempt to access the application again\.

   ```
   curl my-app
   ```

   An example output is as follows\.

   ```
   curl: (6) Could not resolve host: my-app
   ```

   The attempt fails because the Pod is no longer able to access the CoreDNS Pods, which have the cluster security group associated to them\. The cluster security group no longer has the security group rules that allow DNS communication from the security group associated to your Pod\.

   If you attempt to access the application using the IP addresses returned for one of the Pods in a previous step, you still receive a response because all ports are allowed between Pods that have the security group associated to them and a name lookup isn’t required\.

1. Once you’ve finished experimenting, you can remove the sample security group policy, application, and security group that you created\. Run the following commands from `TerminalA`\.

   ```
   kubectl delete namespace my-namespace
   aws ec2 revoke-security-group-ingress --group-id $my_pod_security_group_id --security-group-rule-ids $my_inbound_self_rule_id
   wait
   sleep 45s
   aws ec2 delete-security-group --group-id $my_pod_security_group_id
   ```
<a name="pod-multiple-network-interfaces"></a>==== Multiple network interfaces for Pods   
Learn how to use multiple network interfaces with a Pod using Multus\.  
Multus CNI is a container network interface \(CNI\) plugin for Amazon EKS that enables attaching multiple network interfaces to a Pod\. For more information, see the [Multus\-CNI](https://github.com/k8snetworkplumbingwg/multus-cni) documentation on GitHub\.  
In Amazon EKS, each Pod has one network interface assigned by the Amazon VPC CNI plugin\. With Multus, you can create a multi\-homed Pod that has multiple interfaces\. This is accomplished by Multus acting as a "meta\-plugin"; a CNI plugin that can call multiple other CNI plugins\. AWS support for Multus comes configured with the Amazon VPC CNI plugin as the default delegate plugin\.  
+ Amazon EKS won’t be building and publishing single root I/O virtualization \(SR\-IOV\) and Data Plane Development Kit \(DPDK\) CNI plugins\. However, you can achieve packet acceleration by connecting directly to Amazon EC2 Elastic Network Adapters \(ENA\) through Multus managed host\-device and `ipvlan` plugins\.
+ Amazon EKS is supporting Multus, which provides a generic process that enables simple chaining of additional CNI plugins\. Multus and the process of chaining is supported, but AWS won’t provide support for all compatible CNI plugins that can be chained, or issues that may arise in those CNI plugins that are unrelated to the chaining configuration\.
+ Amazon EKS is providing support and life cycle management for the Multus plugin, but isn’t responsible for any IP address or additional management associated with the additional network interfaces\. The IP address and management of the default network interface utilizing the Amazon VPC CNI plugin remains unchanged\.
+ Only the Amazon VPC CNI plugin is officially supported as the default delegate plugin\. You need to modify the published Multus installation manifest to reconfigure the default delegate plugin to an alternate CNI if you choose not to use the Amazon VPC CNI plugin for primary networking\.
+ Multus is only supported when using the Amazon VPC CNI as the primary CNI\. We do not support the Amazon VPC CNI when used for higher order interfaces, secondary or otherwise\.
+ To prevent the Amazon VPC CNI plugin from trying to manage additional network interfaces assigned to Pods, add the following tag to the network interface:

   **key**: `node.k8s.amazonaws.com/no_manage` 

   **value**: `true` 
+ Multus is compatible with network policies, but the policy has to be enriched to include ports and IP addresses that may be part of additional network interfaces attached to Pods\.
For an implementation walk through, see the [Multus Setup Guide](https://github.com/aws-samples/eks-install-guide-for-multus/blob/main/README.md) on GitHub\.  
<a name="alternate-cni-plugins"></a>=== Alternate compatible CNI plugins  
The [Amazon VPC CNI plugin for Kubernetes](https://github.com/aws/amazon-vpc-cni-plugins) is the only CNI plugin supported by Amazon EKS\. Amazon EKS runs upstream Kubernetes, so you can install alternate compatible CNI plugins to Amazon EC2 nodes in your cluster\. If you have Fargate nodes in your cluster, the Amazon VPC CNI plugin for  Kubernetes is already on your Fargate nodes\. It’s the only CNI plugin you can use with Fargate nodes\. An attempt to install an alternate CNI plugin on Fargate nodes fails\.  
If you plan to use an alternate CNI plugin on Amazon EC2 nodes, we recommend that you obtain commercial support for the plugin or have the in\-house expertise to troubleshoot and contribute fixes to the CNI plugin project\.  
Amazon EKS maintains relationships with a network of partners that offer support for alternate compatible CNI plugins\. For details about the versions, qualifications, and testing performed, see the following partner documentation\.  
Tigera  
 [Calico](https://www.tigera.io/partners/aws/)   
 [Installation instructions](https://docs.projectcalico.org/getting-started/kubernetes/managed-public-cloud/eks)   
 [Cilium](https://cilium.io)   
 [Installation instructions](https://docs.cilium.io/en/stable/gettingstarted/k8s-install-default/)   
 [Cloud\-Native Contrail Networking \(CN2\)](https://www.juniper.net/us/en/products/sdn-and-orchestration/contrail/cloud-native-contrail-networking.html)   
 [Installation instructions](https://www.juniper.net/documentation/us/en/software/cn-cloud-native23.2/cn-cloud-native-eks-install-and-lcm/index.html)   
VMware  
 [Antrea](https://antrea.io/)   
 [Installation instructions](https://antrea.io/docs/main/docs/eks-installation)   
Amazon EKS aims to give you a wide selection of options to cover all use cases\.  
<a name="alternate-network-policy-plugins"></a>==== Alternate compatible network policy plugins  
 [Calico](https://www.tigera.io/project-calico) is a widely adopted solution for container networking and security\. Using Calico on EKS provides a fully compliant network policy enforcement for your EKS clusters\. Additionally, you can opt to use Calico's networking, which conserve IP addresses from your underlying VPC\. [Calico Cloud](https://www.tigera.io/tigera-products/calico-cloud/) enhances the features of Calico Open Source, providing advanced security and observability capabilities\.  
<a name="aws-load-balancer-controller"></a>== What is the  AWS Load Balancer Controller?  
Learn how to install the  AWS Load Balancer Controller add\-on to your cluster\.  
The  AWS Load Balancer Controller manages AWS Elastic Load Balancers for a Kubernetes cluster\. You can use the controller to expose your cluster apps to the internet\. The controller provisions AWS load balancers that point to cluster Service or Ingress resources\. In other words, the controller creates a single IP address or DNS name that points to multiple pods in your cluster\.  
The controller watches for Kubernetes Ingress or Service resources\. In response, it creates the appropriate AWS Elastic Load Balancing resources\. You can configure the specific behavior of the load balancers by applying annotations to the Kubernetes resources\. For example, you can attach AWS security groups to load balancers using annotations\.  
The controller provisions the following resources:    
 Kubernetes `Ingress`   
+ The LBC creates an [AWS Application Load Balancer \(ALB\)](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html) when you create a Kubernetes `Ingress`\. [Review the annotations you can apply to an Ingress resource\.](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.7/guide/ingress/annotations/)   
 Kubernetes service of the `LoadBalancer` type  
+ The LBC creates an [AWS Network Load Balancer \(NLB\)](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html)when you create a Kubernetes service of type `LoadBalancer`\. [Review the annotations you can apply to a Service resource\.](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.7/guide/service/annotations/) 

  In the past, the Kubernetes network load balancer was used for *instance* targets, but the LBC was used for *IP* targets\. With the  AWS Load Balancer Controller version `2.3.0` or later, you can create NLBs using either target type\. For more information about NLB target types, see [Target type](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-target-groups.html#target-type) in the User Guide for Network Load Balancers\.
The controller is an [open\-source project](https://github.com/kubernetes-sigs/aws-load-balancer-controller) managed on GitHub\.  
<a name="lbc-overview"></a>=== Install the Controller 🚀   
<a name="lbc-deprecated"></a>=== Migrate from Deprecated Controller Versions  
+ Deprecated versions cannot be upgraded\. They must be removed and a current version of the  AWS Load Balancer Controller installed\.
+ Deprecated versions include:
  +  AWS ALB Ingress Controller for Kubernetes \("Ingress Controller"\), a predecessor to the  AWS Load Balancer Controller\.
  + Any `0.1.x ` version of the  AWS Load Balancer Controller 
<a name="lbc-legacy"></a>=== Legacy Cloud Provider  
 Kubernetes includes a legacy cloud provider for AWS\. The legacy cloud provider is capable of provisioning AWS load balancers, similar to the  AWS Load Balancer Controller\. The legacy cloud provider creates Classic Load Balancers\. If you do not install the  AWS Load Balancer Controller, Kubernetes will default to using the legacy cloud provider\. You should install the  AWS Load Balancer Controller and avoid using the legacy cloud provider\.

In versions 2\.5 and newer, the  AWS Load Balancer Controller becomes the default controller for Kubernetes *service* resources with the `type: LoadBalancer` and makes an AWS Network Load Balancer \(NLB\) for each service\. It does this by making a mutating webhook for services, which sets the `spec.loadBalancerClass` field to `service.k8s.aws/nlb` for new services of `type: LoadBalancer`\. You can turn off this feature and revert to using the [legacy Cloud Provider](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.7/guide/service/annotations/#legacy-cloud-provider) as the default controller, by setting the helm chart value `enableServiceMutatorWebhook` to `false`\. The cluster won’t provision new Classic Load Balancers for your services unless you turn off this feature\. Existing Classic Load Balancers will continue to work\.

**Example**  
<a name="lbc-helm"></a>=== Install the  AWS Load Balancer Controller using Helm  
Learn how to install the  AWS Load Balancer Controller add\-on to your cluster\.  
This topic describes how to install the  AWS Load Balancer Controller using Helm, a package manager for Kubernetes, and `eksctl`\. The controller is installed with default options\. For more information about the controller, including details on configuring it with annotations, see the [AWS Load Balancer Controller Documentation](https://kubernetes-sigs.github.io/aws-load-balancer-controller/) on GitHub\.  
In the following steps, replace the ` example values ` with your own values\.  
<a name="lbc-prereqs"></a>==== Prerequisites  
Before starting this tutorial, you must install and configure the following tools and resources that you need to create and manage an Amazon EKS cluster\.  
+ An existing Amazon EKS cluster\. To deploy one, see \.
+ An existing AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see \.
+ Familiarity with AWS Elastic Load Balancing\. For more information, see the [Elastic Load Balancing User Guide](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/)\.
+ Familiarity with Kubernetes [service](https://kubernetes.io/docs/concepts/services-networking/service/) and [ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) resources\.
+  [Helm](https://helm.sh/docs/helm/helm_install/) installed locally\.
<a name="lbc-helm-iam"></a>==== Step 1: Create IAM Role using `eksctl` 

**Example**  

1. Download an IAM policy for the  AWS Load Balancer Controller that allows it to make calls to AWS APIs on your behalf\.  
 AWS   
\*\*

```
$ curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.7.2/docs/install/iam_policy.json
```  
 AWS GovCloud \(US\)  
\*\*

```
$ curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.7.2/docs/install/iam_policy_us-gov.json
```

```
$ mv iam_policy_us-gov.json iam_policy.json
```

1. Create an IAM policy using the policy downloaded in the previous step\.

   ```
   $ aws iam create-policy \
       --policy-name {aws}LoadBalancerControllerIAMPolicy \
   //⁂    --policy-document file://iam_policy.json
   ```
**Note**  
If you view the policy in the AWS Management Console, the console shows warnings for the **ELB** service, but not for the **ELB v2** service\. This happens because some of the actions in the policy exist for **ELB v2**, but not for **ELB**\. You can ignore the warnings for **ELB**\.

1. Replace ` my-cluster ` with the name of your cluster, ` 111122223333 ` with your account ID, and then run the command\. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-West\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:`\.

   ```
   $ eksctl create iamserviceaccount \
     --cluster=my-cluster \
     --namespace=kube-system \
     --name=aws-load-balancer-controller \
     --role-name AmazonEKSLoadBalancerControllerRole \
     --attach-policy-arn=arn:aws:iam::111122223333:policy/{aws}LoadBalancerControllerIAMPolicy \
     --approve
   ```
<a name="lbc-helm-install"></a>==== Step 2: Install  AWS Load Balancer Controller \. Add the `eks-charts` Helm chart repository\. AWS maintains [this repository](https://github.com/aws/eks-charts) on GitHub\.  
\+  

```
$ helm repo add eks https://aws.github.io/eks-charts
```

1. Update your local repo to make sure that you have the most recent charts\.

   ```
   $ helm repo update eks
   ```

1. Install the  AWS Load Balancer Controller\.

   Replace ` my-cluster ` with the name of your cluster\. In the following command, `aws-load-balancer-controller` is the Kubernetes service account that you created in a previous step\.

   For more information about configuring the helm chart, see [values\.yaml](https://github.com/aws/eks-charts/blob/master/stable/aws-load-balancer-controller/values.yaml) on GitHub\.

   ```
   $ helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
     -n kube-system \
     --set clusterName=my-cluster \
     --set serviceAccount.create=false \
     --set serviceAccount.name=aws-load-balancer-controller
   ```

   1. If you’re deploying the controller to Amazon EC2 nodes that have [restricted access to the Amazon EC2 instance metadata service \(IMDS\)](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node), or if you’re deploying to Fargate, then add the following flags to the `helm` command that follows:
      +  ` --set region=[replaceable] ` 
      +  ` --set vpcId=[replaceable] ` 

   1. To view the available versions of the Helm Chart and Load Balancer Controller, use the following command:

      ```
      helm search repo eks/aws-load-balancer-controller --versions
      ```
**Important**  
The deployed chart doesn’t receive security updates automatically\. You need to manually upgrade to a newer chart when it becomes available\. When upgrading, change ` install ` to ` upgrade in the previous command.` 
The `helm install` command automatically installs the custom resource definitions \(CRDs\) for the controller\. The `helm upgrade` command does not\. If you use `helm upgrade,` you must manually install the CRDs\. Run the following command to install the CRDs:  

```
wget https://raw.githubusercontent.com/aws/eks-charts/master/stable/aws-load-balancer-controller/crds/crds.yaml
kubectl apply -f crds.yaml
```
<a name="lbc-helm-verify"></a>==== Step 3: Verify that the controller is installed \. Verify that the controller is installed\.  
\+  

```
$ kubectl get deployment -n kube-system aws-load-balancer-controller
```
\+  
An example output is as follows\.  
\+  

```
NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
aws-load-balancer-controller   2/2     2            2           84s
```
\+  
You receive the previous output if you deployed using Helm\. If you deployed using the Kubernetes manifest, you only have one replica\.  
<a name="lbc-manifest"></a>=== Install the  AWS Load Balancer Controller add\-on using Kubernetes Manifests  
Learn how to install the  AWS Load Balancer Controller add\-on to your cluster\.  
This topic describes how to install the controller by downloading and applying Kubernetes manifests\. You can view the full [documentation](https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/) for the controller on GitHub\.  
In the following steps, replace the ` example values ` with your own values\.  
<a name="lbc-prereqs"></a>==== Prerequisites  
Before starting this tutorial, you must install and configure the following tools and resources that you need to create and manage an Amazon EKS cluster\.  
+ An existing Amazon EKS cluster\. To deploy one, see \.
+ An existing AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see \.
+ Familiarity with AWS Elastic Load Balancing\. For more information, see the [Elastic Load Balancing User Guide](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/)\.
+ Familiarity with Kubernetes [service](https://kubernetes.io/docs/concepts/services-networking/service/) and [ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) resources\.
<a name="lbc-iam"></a>==== Step 1: Configure IAM

**Example**  

1. Download an IAM policy for the  AWS Load Balancer Controller that allows it to make calls to AWS APIs on your behalf\.  
 AWS   
\*\*

```
$ curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.7.2/docs/install/iam_policy.json
```  
 AWS GovCloud \(US\)  
\*\*

```
$ curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.7.2/docs/install/iam_policy_us-gov.json
```

```
$ mv iam_policy_us-gov.json iam_policy.json
```

1. Create an IAM policy using the policy downloaded in the previous step\.

   ```
   $ aws iam create-policy \
       --policy-name {aws}LoadBalancerControllerIAMPolicy \
   //⁂    --policy-document file://iam_policy.json
   ```
**Note**  
If you view the policy in the AWS Management Console, the console shows warnings for the **ELB** service, but not for the **ELB v2** service\. This happens because some of the actions in the policy exist for **ELB v2**, but not for **ELB**\. You can ignore the warnings for **ELB**\.  
eksctl  

   1. Replace ` my-cluster ` with the name of your cluster, ` 111122223333 ` with your account ID, and then run the command\. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-West\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:`\.

      ```
      $ eksctl create iamserviceaccount \
        --cluster=my-cluster \
        --namespace=kube-system \
        --name=aws-load-balancer-controller \
        --role-name AmazonEKSLoadBalancerControllerRole \
        --attach-policy-arn=arn:aws:iam::111122223333:policy/{aws}LoadBalancerControllerIAMPolicy \
        --approve
      ```  
 AWS CLI and kubectl  

   1. Retrieve your cluster’s OIDC provider ID and store it in a variable\.

      ```
      oidc_id=$(aws eks describe-cluster --name my-cluster --query "cluster.identity.oidc.issuer" --output text | cut -d '/' -f 5)
      ```

   1. Determine whether an IAM OIDC provider with your cluster’s ID is already in your account\. You need OIDC configured for both the cluster and IAM\.

      ```
      aws iam list-open-id-connect-providers | grep $oidc_id | cut -d "/" -f4
      ```

   1. Copy the following contents to your device\. Replace ` 111122223333 ` with your account ID\. Replace `[replaceable]`region\-code` ` with the AWS Region that your cluster is in. Replace `[replaceable] with the output returned in the previous step. If your cluster is in the AWS GovCloud (US-East) or AWS GovCloud (US-West) AWS Regions, then replace arn:aws: with `arn:aws\-us\-gov:`. After replacing the text, run the modified command to create the [path]`load\-balancer\-role\-trust\-policy\.json`` file\.

      ```
      //⁂cat >load-balancer-role-trust-policy.json <<EOF
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
      //⁂  --assume-role-policy-document file://"load-balancer-role-trust-policy.json"
      ```

   1. Attach the required Amazon EKS managed IAM policy to the IAM role\. Replace ` 111122223333 ` with your account ID\.

      ```
      aws iam attach-role-policy \
        --policy-arn arn:aws:iam::111122223333:policy/{aws}LoadBalancerControllerIAMPolicy \
        --role-name AmazonEKSLoadBalancerControllerRole
      ```

   1. Copy the following contents to your device\. Replace ` 111122223333 ` with your account ID\. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-West\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:`\. After replacing the text, run the modified command to create the `aws-load-balancer-controller-service-account.yaml` file\.

      ```
      //⁂cat >aws-load-balancer-controller-service-account.yaml <<EOF
      apiVersion: v1
      kind: ServiceAccount
      metadata:
        labels:
          app.kubernetes.io/component: controller
          app.kubernetes.io/name: aws-load-balancer-controller
        name: aws-load-balancer-controller
        namespace: kube-system
        annotations:
      //⁂⁂⁂DENY LIST ERROR: [AWSDevDocsChecklist] 40-character IAM secret key⁂⁂⁂
      //⁂    eks.amazonaws.com/role-arn: arn:aws:iam::111122223333:role/AmazonEKSLoadBalancerControllerRole
      EOF
      ```

   1. Create the Kubernetes service account on your cluster\. The Kubernetes service account named `aws-load-balancer-controller` is annotated with the IAM role that you created named `[replaceable]`AmazonEKSLoadBalancerControllerRole````\.

      ```
      $ kubectl apply -f aws-load-balancer-controller-service-account.yaml
      ```
<a name="lbc-cert"></a>==== Step 2: Install `cert-manager`   
Install `cert-manager` using one of the following methods to inject certificate configuration into the webhooks\. For more information, see [Getting Started](https://cert-manager.io/docs/installation/#getting-started) on the * `` *cert\-manager**\.  
We recommend using the `quay.io` container registry to install `cert-manager`\. If your nodes do not have access to the `quay.io` container registry, Install `cert-manager` using Amazon ECR \(see below\)\.    
 Quay\.io   

1. If your nodes have access to the `quay.io` container registry, install `cert-manager` to inject certificate configuration into the webhooks\.

   ```
   $ kubectl apply \
       --validate=false \
       -f https://github.com/jetstack/cert-manager/releases/download/v1.13.5/cert-manager.yaml
   ```  
Amazon ECR  

1. Install `cert-manager` using one of the following methods to inject certificate configuration into the webhooks\. For more information, see [Getting Started](https://cert-manager.io/docs/installation/#getting-started) on the * `` *cert\-manager**\.

1. Download the manifest\.

   ```
   curl -Lo cert-manager.yaml https://github.com/jetstack/cert-manager/releases/download/v1.13.5/cert-manager.yaml
   ```

   ```
   quay.io/jetstack/cert-manager-cainjector:v1.13.5
   quay.io/jetstack/cert-manager-controller:v1.13.5
   quay.io/jetstack/cert-manager-webhook:v1.13.5
   ```

1. Replace `quay.io` in the manifest for the three images with your own registry name\. The following command assumes that your private repository’s name is the same as the source repository\. Replace ` 111122223333.dkr.ecr.[replaceable]region-code.amazonaws.com ` with your private registry\.

   ```
   $ sed -i.bak -e 's|quay.io|111122223333.dkr.ecr.region-code.amazonaws.com|' ./cert-manager.yaml
   ```

1. Apply the manifest\.

   ```
   $ kubectl apply \
       --validate=false \
       -f ./cert-manager.yaml
   ```
<a name="lbc-install"></a>==== Step 3: Install  AWS Load Balancer Controller \. Download the controller specification\. For more information about the controller, see the [documentation](https://kubernetes-sigs.github.io/aws-load-balancer-controller/) on GitHub\.  
\+  

```
curl -Lo v2_7_2_full.yaml https://github.com/kubernetes-sigs/aws-load-balancer-controller/releases/download/v2.7.2/v2_7_2_full.yaml
```

1. Make the following edits to the file\.

   1. If you downloaded the `v2_7_2_full.yaml` file, run the following command to remove the `ServiceAccount` section in the manifest\. If you don’t remove this section, the required annotation that you made to the service account in a previous step is overwritten\. Removing this section also preserves the service account that you created in a previous step if you delete the controller\.

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

   1. Replace `your-cluster-name` in the `Deployment`spec section of the file with the name of your cluster by replacing `my-cluster ` with the name of your cluster\.

      ```
      $ sed -i.bak -e 's|your-cluster-name|my-cluster|' ./v2_7_2_full.yaml
      ```

      ```
      public.ecr.aws/eks/aws-load-balancer-controller:v2.7.2
      ```

      Add your registry’s name to the manifest\. The following command assumes that your private repository’s name is the same as the source repository and adds your private registry’s name to the file\. Replace ` 111122223333.dkr.ecr.[replaceable]region-code.amazonaws.com ` with your registry\. This line assumes that you named your private repository the same as the source repository\. If not, change the `eks/aws-load-balancer-controller` text after your private registry name to your repository name\.

      ```
      $ sed -i.bak -e 's|public.ecr.aws/eks/aws-load-balancer-controller|111122223333.dkr.ecr.region-code.amazonaws.com/eks/aws-load-balancer-controller|' ./v2_7_2_full.yaml
      ```

   1. \(Required only for Fargate or Restricted IMDS\)

      If you’re deploying the controller to Amazon EC2 nodes that have [restricted access to the Amazon EC2 instance metadata service \(IMDS\)](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#restrict-access-to-the-instance-profile-assigned-to-the-worker-node), or if you’re deploying to Fargate, then add the `following parameters` under `- args:`\.

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
<a name="lbc-verify"></a>==== Step 4: Verify that the controller is installed \. Verify that the controller is installed\.  
\+  

```
$ kubectl get deployment -n kube-system aws-load-balancer-controller
```
\+  
An example output is as follows\.  
\+  

```
NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
aws-load-balancer-controller   2/2     2            2           84s
```
\+  
You receive the previous output if you deployed using Helm\. If you deployed using the Kubernetes manifest, you only have one replica\.  
<a name="lbc-remove"></a>=== Migrate from Deprecated Controller  
Learn how to remove the deprecated ALB Ingress Controller\.  
This topic describes how to migrate from deprecated controller versions\. More specifically, it describes how to remove deprecated versions of the  AWS Load Balancer Controller\.  
+ Deprecated versions cannot be upgraded\. They must be removed and a current version of the LBC installed\.
+ Deprecated versions include:
  +  AWS ALB Ingress Controller for Kubernetes \("Ingress Controller"\), a predecessor to the  AWS Load Balancer Controller\.
  + Any `0.1.x ` version of the  AWS Load Balancer Controller 
<a name="lbc-remove-desc"></a>==== Remove Deprecated Controller Version

You may have installed the deprecated version using Helm or manually with Kubernetes manifests\. Complete the procedure using the tool that you originally installed it with\.

**Example**  

1. If you installed the `incubator/aws-alb-ingress-controller` Helm chart, uninstall it\.

   ```
   $ helm delete aws-alb-ingress-controller -n kube-system
   ```

1. If you have version `0.1.x ` of the `eks-charts/aws-load-balancer-controller` chart installed, uninstall it\. The upgrade from `0.1.x ` to version `1.0.0` doesn’t work due to incompatibility with the webhook API version\.

   ```
   $ helm delete aws-load-balancer-controller -n kube-system
   ```

1. Check to see if the controller is currently installed\.

   ```
   $ kubectl get deployment -n kube-system alb-ingress-controller
   ```

   This is the output if the controller isn’t installed\.

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
<a name="lbc-migrate"></a>==== Migrate to  AWS Load Balancer Controller   
To migrate from the ALB Ingress Controller for Kubernetes to the  AWS Load Balancer Controller, you need to:  

1. Remove the ALB Ingress Controller \(see above\)\.

1. Add an additional policy to the IAM Role used by the LBC\. This policy permits the LBC to manage resources created by the ALB Ingress Controller for Kubernetes\.

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
     --policy-name {aws}LoadBalancerControllerAdditionalIAMPolicy \
   //⁂  --policy-document file://iam_policy_v1_to_v2_additional.json
   ```

1. Attach the IAM policy to the IAM role used by the LBC\. Replace ` your-role-name ` with the name of the role, such as `AmazonEKSLoadBalancerControllerRole`\.

   If you created the role using `eksctl`, then to find the role name that was created, open the [AWS CloudFormation console](https://console.aws.amazon.com/cloudformation) and select the **eksctl\-*my\-cluster*\-addon\-iamserviceaccount\-kube\-system\-aws\-load\-balancer\-controller** stack\. Select the **Resources** tab\. The role name is in the **Physical ID** column\. If your cluster is in the AWS GovCloud \(US\-East\) or AWS GovCloud \(US\-West\) AWS Regions, then replace `arn:aws:` with `arn:aws-us-gov:`\.

   ```
   $ aws iam attach-role-policy \
     --role-name your-role-name \
     --policy-arn arn:aws:iam::111122223333:policy/{aws}LoadBalancerControllerAdditionalIAMPolicy
   ```
<a name="managing-coredns"></a>== Working with the CoreDNS Amazon EKS add\-on  
Learn about the CoreDNS self\-managed add\-on and how to create and update it on your cluster\.  
The following table lists the latest version of the Amazon EKS add\-on type for each Kubernetes version\. 

**Example**  
<a name="coredns-upgrade"></a>=== Important CoreDNS upgrade considerations  
+ To improve the stability and availability of the CoreDNS Deployment, versions `v1.9.3-eksbuild.6` and later and `v1.10.1-eksbuild.3` are deployed with a `PodDisruptionBudget`\. If you’ve deployed an existing `PodDisruptionBudget`, your upgrade to these versions might fail\. If the upgrade fails, completing one of the following tasks should resolve the issue:
  + When doing the upgrade of the Amazon EKS add\-on, choose to override the existing settings as your conflict resolution option\. If you’ve made other custom settings to the Deployment, make sure to back up your settings before upgrading so that you can reapply your other custom settings after the upgrade\.
  + Remove your existing `PodDisruptionBudget` and try the upgrade again\.
+ In EKS add\-on versions `v1.9.3-eksbuild.3` and later and `v1.10.1-eksbuild.6` and later, the CoreDNS Deployment sets the `readinessProbe` to use the `/ready` endpoint\. This endpoint is enabled in the `Corefile` configuration file for CoreDNS\.

  If you use a custom `Corefile`, you must add the `ready` plugin to the config, so that the `/ready` endpoint is active in CoreDNS for the probe to use\.
+ In EKS add\-on versions `v1.9.3-eksbuild.7` and later and `v1.10.1-eksbuild.4` and later, you can change the `PodDisruptionBudget`\. You can edit the add\-on and change these settings in the **Optional configuration settings** using the fields in the following example\. This example shows the default `PodDisruptionBudget`\.

  ```
  {
      "podDisruptionBudget": {
          "enabled": true,
          "maxUnavailable": 1
          }
  }
  ```

  You can set `maxUnavailable` or `minAvailable`, but you can’t set both in a single `PodDisruptionBudget`\. For more information about `PodDisruptionBudgets`, see [Specifying a PodDisruptionBudget](https://kubernetes.io/docs/tasks/run-application/configure-pdb/#specifying-a-poddisruptionbudget) in the * Kubernetes documentation*\.

  Note that if you set `enabled` to `false`, the `PodDisruptionBudget` isn’t removed\. After you set this field to `false`, you must delete the `PodDisruptionBudget` object\. Similarly, if you edit the add\-on to use an older version of the add\-on \(downgrade the add\-on\) after upgrading to a version with a `PodDisruptionBudget`, the `PodDisruptionBudget` isn’t removed\. To delete the `PodDisruptionBudget`, you can run the following command:

  ```
  kubectl delete poddisruptionbudget coredns -n kube-system
  ```
+ In EKS add\-on versions `v1.10.1-eksbuild.5` and later, change the default toleration from `node-role.kubernetes.io/master:NoSchedule` to `node-role.kubernetes.io/control-plane:NoSchedule` to comply with KEP 2067\. For more information about KEP 2067, see [KEP\-2067: Rename the kubeadm "master" label and taint](https://github.com/kubernetes/enhancements/tree/master/keps/sig-cluster-lifecycle/kubeadm/2067-rename-master-label-taint#renaming-the-node-rolekubernetesiomaster-node-taint) in the *Kubernetes Enhancement Proposals \(KEPs\)* on GitHub\.

  In EKS add\-on versions `v1.8.7-eksbuild.8` and later and `v1.9.3-eksbuild.9` and later, both tolerations are set to be compatible with every Kubernetes version\.
+ In EKS add\-on versions `v1.9.3-eksbuild.11` and `v1.10.1-eksbuild.7` and later, the CoreDNS Deployment sets a default value for `topologySpreadConstraints`\. The default value ensures that the CoreDNS Pods are spread across the Availability Zones if there are nodes in multiple Availability Zones available\. You can set a custom value that will be used instead of the default value\. The default value follows:

  ```
  topologySpreadConstraints:
    - maxSkew: 1
      topologyKey: topology.kubernetes.io/zone
      whenUnsatisfiable: ScheduleAnyway
      labelSelector:
        matchLabels:
          k8s-app: kube-dns
  ```
<a name="coredns-upgrade-1.11"></a>==== CoreDNS v`1.11` upgrade considerations  
+ In EKS add\-on versions `v1.11.1-eksbuild.4` and later, the container image is based on a [minimal base image](https://gallery.ecr.aws/eks-distro-build-tooling/eks-distro-minimal-base) maintained by Amazon EKS Distro, which contains minimal packages and doesn’t have shells\. For more information, see [Amazon EKS Distro](https://distro.eks.amazonaws.com/)\. The usage and troubleshooting of the CoreDNS image remains the same\.
<a name="coredns-add-on-create"></a>=== Creating the Amazon EKS add\-on  
Create the Amazon EKS type of the add\-on\. Check  
+ An existing Amazon EKS cluster\. To deploy one, see \.

  1. See which version of the add\-on is installed on your cluster\.

     ```
     kubectl describe deployment coredns --namespace kube-system | grep coredns: | cut -d : -f 3
     ```

     An example output is as follows\.

     ```
     `v1.10.1-eksbuild.11`
     ```

  1. See which type of the add\-on is installed on your cluster\. Depending on the tool that you created your cluster with, you might not currently have the Amazon EKS add\-on type installed on your cluster\. Replace *my\-cluster* with the name of your cluster\.

     ```
     aws eks describe-addon --cluster-name my-cluster --addon-name coredns --query addon.addonVersion --output text
     ```

     If a version number is returned, you have the Amazon EKS type of the add\-on installed on your cluster and don’t need to complete the remaining steps in this procedure\. If an error is returned, you don’t have the Amazon EKS type of the add\-on installed on your cluster\. Complete the remaining steps of this procedure to install it\.

  1. Save the configuration of your currently installed add\-on\.

     ```
     kubectl get deployment coredns -n kube-system -o yaml > aws-k8s-coredns-old.yaml
     ```
     + Replace ` my-cluster ` with the name of your cluster\.

       ```
       aws eks create-addon --cluster-name my-cluster --addon-name coredns --addon-version v1.11.1-eksbuild.9
       ```

       If you’ve applied custom settings to your current add\-on that conflict with the default settings of the Amazon EKS add\-on, creation might fail\. If creation fails, you receive an error that can help you resolve the issue\. Alternatively, you can add `--resolve-conflicts OVERWRITE` to the previous command\. This allows the add\-on to overwrite any existing custom settings\. Once you’ve created the add\-on, you can update it with your custom settings\.

  1. Confirm that the latest version of the add\-on for your cluster’s Kubernetes version was added to your cluster\. Replace ` my-cluster ` with the name of your cluster\.

     ```
     aws eks describe-addon --cluster-name my-cluster --addon-name coredns --query addon.addonVersion --output text
     ```

     It might take several seconds for add\-on creation to complete\.

     An example output is as follows\.

     ```
     v1.11.1-eksbuild.9
     ```
<a name="coredns-add-on-update"></a>=== Updating the Amazon EKS add\-on  

1. See which version of the add\-on is installed on your cluster\. Replace ` my-cluster ` with your cluster name\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name coredns --query "addon.addonVersion" --output text
   ```

   An example output is as follows\.

   ```
   `v1.10.1-eksbuild.11`
   ```

1. Save the configuration of your currently installed add\-on\.

   ```
   kubectl get deployment coredns -n kube-system -o yaml > aws-k8s-coredns-old.yaml
   ```
   + Replace ` my-cluster ` with the name of your cluster\.
   + The `--resolve-conflicts` *PRESERVE* option preserves existing configuration values for the add\-on\. If you’ve set custom values for add\-on settings, and you don’t use this option, Amazon EKS overwrites your values with its default values\. If you use this option, then we recommend testing any field and value changes on a non\-production cluster before updating the add\-on on your production cluster\. If you change this value to `OVERWRITE`, all settings are changed to Amazon EKS default values\. If you’ve set custom values for any settings, they might be overwritten with Amazon EKS default values\. If you change this value to `none`, Amazon EKS doesn’t change the value of any settings, but the update might fail\. If the update fails, you receive an error message to help you resolve the conflict\.
   + If you’re not updating a configuration setting, remove `--configuration-values '{"replicaCount":3}'` from the command\. If you’re updating a configuration setting, replace *"replicaCount":3* with the setting that you want to set\. In this example, the number of replicas of CoreDNS is set to `3`\. The value that you specify must be valid for the configuration schema\. If you don’t know the configuration schema, run `aws eks describe-addon-configuration --addon-name coredns --addon-version [replaceable]`v1\.11\.1\-eksbuild\.9` `, replacing [replaceable] documentation.` 

     ```
     aws eks update-addon --cluster-name my-cluster --addon-name coredns --addon-version v1.11.1-eksbuild.9 \
         --resolve-conflicts PRESERVE --configuration-values '{"replicaCount":3}'
     ```

      It might take several seconds for the update to complete\. Confirm that the add\-on version was updated\. Replace ` my-cluster ` with the name of your cluster\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name coredns
   ```

   It might take several seconds for the update to complete\.

   An example output is as follows\.

   ```
   {
       "addon": {
           "addonName": "coredns",
           "clusterName": "my-cluster",
           "status": "ACTIVE",
           "addonVersion": "v1.11.1-eksbuild.9",
           "health": {
               "issues": []
           },
           "addonArn": "arn:aws:eks:region:111122223333:addon/my-cluster/coredns/d2c34f06-1111-2222-1eb0-24f64ce37fa4",
           "createdAt": "2023-03-01T16:41:32.442000+00:00",
           "modifiedAt": "2023-03-01T18:16:54.332000+00:00",
           "tags": {},
           "configurationValues": "{\"replicaCount\":3}"
       }
   }
   ```
<a name="coredns-add-on-self-managed-update"></a>=== Updating the self\-managed add\-on

We recommend adding the Amazon EKS type of the add\-on to your cluster instead of using the self\-managed type of the add\-on\. If you’re not familiar with the difference between the types, see \. For more information about adding an Amazon EKS add\-on to your cluster, see \. If you’re unable to use the Amazon EKS add\-on, we encourage you to submit an issue about why you can’t to the [Containers roadmap GitHub repository](https://github.com/aws/containers-roadmap/issues)\.

**Example**  

1. Confirm that you have the self\-managed type of the add\-on installed on your cluster\. Replace *my\-cluster* with the name of your cluster\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name coredns --query addon.addonVersion --output text
   ```

1. See which version of the container image is currently installed on your cluster\.

   ```
   kubectl describe deployment coredns -n kube-system | grep Image | cut -d ":" -f 3
   ```

   An example output is as follows\.

   ```
   `v1.8.7-eksbuild.2`
   ```

   1. Open the configmap with the following command\.

      ```
      kubectl edit configmap coredns -n kube-system
      ```

   1. Replace `proxy` in the following line with `forward`\. Save the file and exit the editor\.

      ```
      proxy . /etc/resolv.conf
      ```

1. If you originally deployed your cluster on Kubernetes `1.17` or earlier, then you may need to remove a discontinued line from your CoreDNS manifest\.
**Important**  
You must complete this step before updating to CoreDNS version `1.7.0`, but it’s recommended that you complete this step even if you’re updating to an earlier version\.

   \+ \.\. Check to see if your CoreDNS manifest has the line\.

   \+

```
kubectl get configmap coredns -n kube-system -o jsonpath='{$.data.Corefile}' | grep upstream
```
\+  
If no output is returned, your manifest doesn’t have the line and you can skip to the next step to update CoreDNS\. If output is returned, then you need to remove the line\. \.\. Edit the `ConfigMap` with the following command, removing the line in the file that has the word `upstream` in it\. Do not change anything else in the file\. Once the line is removed, save the changes\.  
\+  

```
kubectl edit configmap coredns -n kube-system -o yaml
```

1. Retrieve your current CoreDNS image version:

   ```
   kubectl describe deployment coredns -n kube-system | grep Image
   ```

   An example output is as follows\.

   \-\-\-\-\.dkr\.ecr\.\./eks/coredns:`v1\.8\.7\-eksbuild\.2`

```
. If you're updating to [noloc]``CoreDNS````1.8.3`` or later, then you need to add the `endpointslices` permission to the `system:coredns`[noloc]``Kubernetes````clusterrole``.
+
[source,bash]
```
kubectl edit clusterrole system:coredns \-n kube\-system  

```
+

Add the following lines under the existing permissions lines in the  `rules` section of the file.
+
[source,yaml]
```
+ apiGroups:
+ discovery\.k8s\.io resources:
+ endpointslices verbs:
+ list
+ watch

```
//⁂. Update the [noloc]``CoreDNS`` add-on by replacing  `[replaceable]``602401143452``` and `[replaceable]``region-code``` with the values from the output returned in a previous step. Replace  [replaceable]```v1.11.1-eksbuild.9``` with the [noloc]``CoreDNS`` version listed in the  <<coredns-versions,latest versions table>> for your [noloc]``Kubernetes`` version.
+
[source,bash]
```
kubectl set image deployment\.apps/coredns \-n kube\-system coredns=602401143452\.dkr\.ecr\.region\-code\.amazonaws\.com/eks/coredns:v1\.11\.1\-eksbuild\.9  

```
+

An example output is as follows.
+
```
deployment\.apps/coredns image updated  

```
. Check the container image version again to confirm that it was updated to the version that you specified in the previous step.
+
[source,bash]
```
kubectl describe deployment coredns \-n kube\-system \| grep Image \| cut \-d ":" \-f 3  

```
+

An example output is as follows.
+
```
 `v1.11.1-eksbuild.9`   

```
[.topic]
[[coredns-autoscaling,coredns-autoscaling.title]]
=== Autoscaling  [noloc]``CoreDNS``

When you launch an Amazon EKS cluster with at least one node, a  [noloc]``Deployment`` of two replicas of the  [noloc]``CoreDNS`` image are deployed by default, regardless of the number of nodes deployed in your cluster. The  [noloc]``CoreDNS`` Pods provide name resolution for all Pods in the cluster. Applications use name resolution to connect to pods and services in the cluster as well as connecting to services outside the cluster. As the number of requests for name resolution (queries) from pods increase, the  [noloc]``CoreDNS`` pods can get overwhelmed and slow down, and reject requests that the pods can`'t handle.

To handle the increased load on the [noloc]``CoreDNS`` pods, consider an autoscaling system for  [noloc]``CoreDNS``. Amazon EKS can manage the autoscaling of the  [noloc]``CoreDNS`` Deployment in the EKS Add-on version of  [noloc]``CoreDNS``. This  [noloc]``CoreDNS`` autoscaler continuously monitors the cluster state, including the number of nodes and CPU cores. Based on that information, the controller will dynamically adapt the number of replicas of the  [noloc]``CoreDNS`` deployment in an EKS cluster. This feature works for  [noloc]``CoreDNS````v1.9`` and EKS release version `1.25` and later. For more information about which versions are compatible with [noloc]``CoreDNS`` Autoscaling, see the following section.

We recommend using this feature in conjunction with other https://aws.github.io/aws-eks-best-practices/cluster-autoscaling/[EKS Cluster Autoscaling best practices] to improve overall application availability and cluster scalability.

[[coredns-autoscaling-prereqs,coredns-autoscaling-prereqs.title]]
==== Prerequisites

For Amazon EKS to scale your  [noloc]``CoreDNS`` deployment, there are three prerequisites:



* You must be using the _EKS Add-on_ version of [noloc]``CoreDNS``.
* Your cluster must be running at least the minimum cluster versions and platform versions.
* Your cluster must be running at least the minimum version of the EKS Add-on of [noloc]``CoreDNS``.


[[coredns-autoscaling-cluster-version,coredns-autoscaling-cluster-version.title]]
===== Minimum cluster version

Autoscaling of  [noloc]``CoreDNS`` is done by a new component in the cluster control plane, managed by Amazon EKS. Because of this, you must upgrade your cluster to an EKS release that supports the minimum platform version that has the new component.

A new Amazon EKS cluster. To deploy one, see . The cluster must be [noloc]``Kubernetes`` version  `1.25` or later. The cluster must be running one of the [noloc]``Kubernetes`` versions and platform versions listed in the following table or a later version. Note that any  [noloc]``Kubernetes`` and platform versions later than those listed are also supported. You can check your current  [noloc]``Kubernetes`` version by replacing  [replaceable]``my-cluster`` in the following command with the name of your cluster and then running the modified command:

[source,bash]
```
aws eks describe\-cluster \-\-name my\-cluster \-\-query cluster\.version \-\-output text  

```
//⁂[cols="1,1", frame="all", options="header"]
//⁂|===
//⁂| Kubernetes version
//⁂| Platform version


//⁂|

`1.29.3`
//⁂|

`eks.7`

//⁂|

`1.28.8`
//⁂|

`eks.13`

//⁂|

`1.27.12`
//⁂|

`eks.17`

//⁂|

`1.26.15`
//⁂|

`eks.18`

//⁂|

`1.25.16`
//⁂|

`eks.19`
//⁂|===

[[coredns-autoscaling-coredns-version,coredns-autoscaling-coredns-version.title]]
===== Minimum EKS Add-on version

//⁂[cols="1,1,1,1,1,1", frame="all", options="header"]
//⁂|===
//⁂| Kubernetes version
//⁂| 1.29
//⁂| 1.28
//⁂| 1.27
//⁂| 1.26
//⁂| 1.25


//⁂|
//⁂|``v1.11.1-eksbuild.9``
//⁂|``v1.10.1-eksbuild.11``
//⁂|``v1.10.1-eksbuild.11``
//⁂|``v1.9.3-eksbuild.15``
//⁂|``v1.9.3-eksbuild.15``
//⁂|===

[[coredns-autoscaling-console,coredns-autoscaling-console.title]]
==== Configuring  [noloc]``CoreDNS`` autoscaling in the {aws} Management Console
. Ensure that your cluster is at or above the minimum cluster version.
+

Amazon EKS upgrades clusters between platform versions of the same [noloc]``Kubernetes`` version automatically, and you can`'t start this process yourself. Instead, you can upgrade your cluster to the next  [noloc]``Kubernetes`` version, and the cluster will be upgraded to that K8s version and the latest platform version. For example, if you upgrade from  `1.25` to ``1.26``, the cluster will upgrade to ``1.26.15 eks.18``.
+

New [noloc]``Kubernetes`` versions sometimes introduce significant changes. Therefore, we recommend that you test the behavior of your applications by using a separate cluster of the new  [noloc]``Kubernetes`` version before you update your production clusters.
+

//⁂To upgrade a cluster to a new [noloc]``Kubernetes`` version, follow the procedure in  <<update-cluster,Updating an Amazon EKS cluster Kubernetes version>>.
. Ensure that you have the EKS Add-on for  [noloc]``CoreDNS``, not the self-managed  [noloc]``CoreDNS`` Deployment.
+

Depending on the tool that you created your cluster with, you might not currently have the Amazon EKS add-on type installed on your cluster. To see which type of the add-on is installed on your cluster, you can run the following command. Replace `my-cluster` with the name of your cluster.
+
[source,shell]
```
aws eks describe\-addon —cluster\-name my\-cluster —addon\-name coredns —query addon\.addonVersion —output text  

```
+

//⁂If a version number is returned, you have the Amazon EKS type of the add-on installed on your cluster and you can continue with the next step. If an error is returned, you don't have the Amazon EKS type of the add-on installed on your cluster. Complete the remaining steps of the procedure  <<coredns-add-on-create,Creating the Amazon EKS add-on>> to replace the self-managed version with the Amazon EKS add-on.
. Ensure that your EKS Add-on for [noloc]``CoreDNS`` is at a version the same or higher than the minimum EKS Add-on version.
+

See which version of the add-on is installed on your cluster. You can check in the {aws} Management Console or run the following command:
+
[source,shell]
```
kubectl describe deployment coredns —namespace kube\-system \| grep coredns: \| cut \-d : \-f 3  

```
+

An example output is as follows.
+
```
 `v1.10.1-eksbuild.11`   

```
+

//⁂Compare this version with the minimum EKS Add-on version in the previous section. If needed, upgrade the EKS Add-on to a higher version by following the procedure  <<coredns-add-on-update,Updating the Amazon EKS add-on>>.
. Add the autoscaling configuration to the *Optional configuration settings* of the EKS Add-on.
+
.. Open the Amazon EKS console at {https---console-aws-amazon-com-eks-home--clusters}[https://console.aws.amazon.com/eks/home#/clusters].
.. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to configure the add-on for.
.. Choose the *Add-ons* tab.
.. Select the box in the top right of the [noloc]``CoreDNS`` add-on box and then choose  **Edit**.
.. On the *Configure [noloc]``CoreDNS``* page:
+
... Select the *Version* that you'd like to use. We recommend that you keep the same version as the previous step, and update the version and configuration in separate actions.
... Expand the **Optional configuration settings**.
... Enter the JSON key `"autoscaling":` and value of a nested JSON object with a key `"enabled":` and value `true` in **Configuration values**. The resulting text must be a valid JSON object. If this key and value are the only data in the text box, surround the key and value with curly braces  ``{}``. The following example shows autoscaling is enabled:
+
[source,json]
```
\{ "autoScaling": \{ "enabled": true \} \}  

```
... (Optional) You can provide minimum and maximum values that autoscaling can scale the number of [noloc]``CoreDNS`` pods to.
+

The following example shows autoscaling is enabled and all of the optional keys have values. We recommend that the minimum number of [noloc]``CoreDNS`` pods is always greater than 2 to provide resilience for the DNS service in the cluster.
+
[source,json]
```
\{ "autoScaling": \{ "enabled": true, "minReplicas": 2, "maxReplicas": 10 \} \}  

```
.. To apply the new configuration by replacing the [noloc]``CoreDNS`` pods, choose  **Save changes**.
+

Amazon EKS applies changes to the EKS Add-ons by using a _rollout_ of the [noloc]``Kubernetes`` Deployment for CoreDNS. You can track the status of the rollout in the  *Update history* of the add-on in the {aws} Management Console and with  ``kubectl rollout status deployment/coredns --namespace kube-system``.
+

`kubectl rollout` has the following commands:
+
[source,shell]
```
$ kubectl rollout  
history  — View rollout history pause  — Mark the provided resource as paused restart  — Restart a resource resume  — Resume a paused resource status  — Show the status of the rollout undo  — Undo a previous rollout  

```
+

If the rollout takes too long, Amazon EKS will undo the rollout, and a message with the type of  *Addon Update* and a status of  *Failed* will be added to the  *Update history* of the add-on. To investigate any issues, start from the history of the rollout, and run  `kubectl logs` on a [noloc]``CoreDNS`` pod to see the logs of  [noloc]``CoreDNS``.
. If the new entry in the *Update history* has a status of  **Successful**, then the rollout has completed and the add-on is using the new configuration in all of the  [noloc]``CoreDNS`` pods. As you change the number of nodes and CPU cores of nodes in the cluster, Amazon EKS scales the number of replicas of the  [noloc]``CoreDNS`` deployment.


[[coredns-autoscaling-cli,coredns-autoscaling-cli.title]]
==== Configuring  [noloc]``CoreDNS`` autoscaling in the {aws} Command Line Interface
. Ensure that your cluster is at or above the minimum cluster version.
+

Amazon EKS upgrades clusters between platform versions of the same [noloc]``Kubernetes`` version automatically, and you can`'t start this process yourself. Instead, you can upgrade your cluster to the next  [noloc]``Kubernetes`` version, and the cluster will be upgraded to that K8s version and the latest platform version. For example, if you upgrade from  `1.25` to ``1.26``, the cluster will upgrade to ``1.26.15 eks.18``.
+

New [noloc]``Kubernetes`` versions sometimes introduce significant changes. Therefore, we recommend that you test the behavior of your applications by using a separate cluster of the new  [noloc]``Kubernetes`` version before you update your production clusters.
+

//⁂To upgrade a cluster to a new [noloc]``Kubernetes`` version, follow the procedure in  <<update-cluster,Updating an Amazon EKS cluster Kubernetes version>>.
. Ensure that you have the EKS Add-on for  [noloc]``CoreDNS``, not the self-managed  [noloc]``CoreDNS`` Deployment.
+

Depending on the tool that you created your cluster with, you might not currently have the Amazon EKS add-on type installed on your cluster. To see which type of the add-on is installed on your cluster, you can run the following command. Replace `my-cluster` with the name of your cluster.
+
[source,shell]
```
aws eks describe\-addon —cluster\-name my\-cluster —addon\-name coredns —query addon\.addonVersion —output text  

```
+

//⁂If a version number is returned, you have the Amazon EKS type of the add-on installed on your cluster. If an error is returned, you don't have the Amazon EKS type of the add-on installed on your cluster. Complete the remaining steps of the procedure  <<coredns-add-on-create,Creating the Amazon EKS add-on>> to replace the self-managed version with the Amazon EKS add-on.
. Ensure that your EKS Add-on for [noloc]``CoreDNS`` is at a version the same or higher than the minimum EKS Add-on version.
+

See which version of the add-on is installed on your cluster. You can check in the {aws} Management Console or run the following command:
+
[source,shell]
```
kubectl describe deployment coredns —namespace kube\-system \| grep coredns: \| cut \-d : \-f 3  

```
+

An example output is as follows.
+
```
 `v1.10.1-eksbuild.11`   

```
+

//⁂Compare this version with the minimum EKS Add-on version in the previous section. If needed, upgrade the EKS Add-on to a higher version by following the procedure  <<coredns-add-on-update,Updating the Amazon EKS add-on>>.
. Add the autoscaling configuration to the *Optional configuration settings* of the EKS Add-on.
+

Run the following {aws} CLI command. Replace `my-cluster` with the name of your cluster and the IAM role ARN with the role that you are using.
+
[source,shell]
```
aws eks update\-addon \-\-cluster\-name my\-cluster \-\-addon\-name coredns \\ \-\-resolve\-conflicts PRESERVE \-\-configuration\-values '\{"autoScaling":\{"enabled":true\}\}'  

```
+

Amazon EKS applies changes to the EKS Add-ons by using a  _rollout_ of the [noloc]``Kubernetes`` Deployment for CoreDNS. You can track the status of the rollout in the  *Update history* of the add-on in the {aws} Management Console and with  ``kubectl rollout status deployment/coredns --namespace kube-system``.
+

`kubectl rollout` has the following commands:
+
[source,shell]
```
kubectl rollout  
history  — View rollout history pause  — Mark the provided resource as paused restart  — Restart a resource resume  — Resume a paused resource status  — Show the status of the rollout undo  — Undo a previous rollout  

```
+

If the rollout takes too long, Amazon EKS will undo the rollout, and a message with the type of  *Addon Update* and a status of  *Failed* will be added to the  *Update history* of the add-on. To investigate any issues, start from the history of the rollout, and run  `kubectl logs` on a [noloc]``CoreDNS`` pod to see the logs of  [noloc]``CoreDNS``.
. (Optional) You can provide minimum and maximum values that autoscaling can scale the number of [noloc]``CoreDNS`` pods to.
+

The following example shows autoscaling is enabled and all of the optional keys have values. We recommend that the minimum number of [noloc]``CoreDNS`` pods is always greater than 2 to provide resilience for the DNS service in the cluster.
+
[source,shell]
```
aws eks update\-addon \-\-cluster\-name my\-cluster \-\-addon\-name coredns \\ \-\-resolve\-conflicts PRESERVE \-\-configuration\-values '\{"autoScaling":\{"enabled":true\}, "minReplicas": 2, "maxReplicas": 10\}'  

```
. Check the status of the update to the add-on by running the following command:
+
[source,shell]
```
aws eks describe\-addon \-\-cluster\-name my\-cluster \-\-addon\-name coredns \\  

```
+

If you see this line:  ``"status": "ACTIVE"``, then the rollout has completed and the add-on is using the new configuration in all of the [noloc]``CoreDNS`` pods. As you change the number of nodes and CPU cores of nodes in the cluster, Amazon EKS scales the number of replicas of the  [noloc]``CoreDNS`` deployment.


[.topic]
[[coredns-metrics,coredns-metrics.title]]
=== [noloc]``CoreDNS`` metrics

[noloc]``CoreDNS`` as an EKS add-on exposes the metrics from  [noloc]``CoreDNS`` on port  `9153` in the Prometheus format in the `kube-dns` service. You can use Prometheus, the Amazon CloudWatch agent, or any other compatible system to scrape (collect) these metrics.

For an example _scrape configuration_ that is compatible with both Prometheus and the CloudWatch agent, see https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContainerInsights-Prometheus-Setup-configure.html[CloudWatch agent configuration for Prometheus] in the __Amazon CloudWatch User Guide__.

[.topic]
[[managing-kube-proxy,managing-kube-proxy.title]]
== Working with the Kubernetes  `kube-proxy` add-on

[abstract]
--
Learn how to update the `kube-proxy` self-managed add-on.
--

[IMPORTANT]
```

We recommend adding the Amazon EKS type of the add\-on to your cluster instead of using the self\-managed type of the add\-on\. If you’re not familiar with the difference between the types, see \. For more information about adding an Amazon EKS add\-on to your cluster, see \. If you’re unable to use the Amazon EKS add\-on, we encourage you to submit an issue about why you can’t to the [Containers roadmap GitHub repository](https://github.com/aws/containers-roadmap/issues)\.

**Example**  
The `kube-proxy` add\-on is deployed on each Amazon EC2 node in your Amazon EKS cluster\. It maintains network rules on your nodes and enables network communication to your Pods\. The add\-on isn’t deployed to Fargate nodes in your cluster\. For more information, see [kube\-proxy](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/) in the Kubernetes documentation\.  
The following table lists the latest version of the Amazon EKS add\-on type for each Kubernetes version\. 

An earlier version of the documentation was incorrect\. `kube-proxy` versions `v1.28.5`, `v1.27.9`, and `v1.26.12` aren’t available\.

If you’re self\-managing this add\-on, the versions in the table might not be the same as the available self\-managed versions\.

**Example**  
There are two types of the `kube-proxy` container image available for each Amazon EKS cluster version:  
+  **Default** – This image type is based on a Debian\-based Docker image that is maintained by the Kubernetes upstream community\.
+  **Minimal** – This image type is based on a [minimal base image](https://gallery.ecr.aws/eks-distro-build-tooling/eks-distro-minimal-base-iptables) maintained by Amazon EKS Distro, which contains minimal packages and doesn’t have shells\. For more information, see [Amazon EKS Distro](https://distro.eks.amazonaws.com/)\.   
+ The default image type isn’t available for Kubernetes version `1.25` and later\. You must use the minimal image type\.

**Example**  
Prerequisites  
+ An existing Amazon EKS cluster\. To deploy one, see \.
+  `Kube-proxy` must be the same minor version as `kubelet` on your Amazon EC2 nodes\.
+  `Kube-proxy` can’t be later than the minor version of your cluster’s control plane\.
+ If you recently updated your cluster to a new Kubernetes minor version, then update your Amazon EC2 nodes to the same minor version *before* updating `kube-proxy` to the same minor version as your nodes\.

  1. Confirm that you have the self\-managed type of the add\-on installed on your cluster\. Replace *my\-cluster* with the name of your cluster\.

     ```
     aws eks describe-addon --cluster-name my-cluster --addon-name kube-proxy --query addon.addonVersion --output text
     ```

  1. See which version of the container image is currently installed on your cluster\.

     ```
     kubectl describe daemonset kube-proxy -n kube-system | grep Image
     ```

     An example output is as follows\.

     ```
     Image:.dkr.ecr../eks/kube-proxy:`v1.25.6-minimal-eksbuild.2`
     ```

     In the example output, *v1\.25\.6\-minimal\-eksbuild\.2* is the version installed on the cluster\.

     ```
     kubectl set image daemonset.apps/kube-proxy -n kube-system kube-proxy=602401143452.dkr.ecr.region-code.amazonaws.com/eks/kube-proxy:v1.26.2-minimal-eksbuild.2
     ```

     An example output is as follows\.

     ```
     daemonset.apps/kube-proxy image updated
     ```

  1. Confirm that the new version is now installed on your cluster\.

     ```
     kubectl describe daemonset kube-proxy -n kube-system | grep Image | cut -d ":" -f 3
     ```

     An example output is as follows\.

     ```
     `v1.26.2-minimal-eksbuild.2`
     ```

  1. If you’re using `x86` and `Arm` nodes in the same cluster and your cluster was deployed before August 17, 2020\. Then, edit your `kube-proxy` manifest to include a node selector for multiple hardware architectures with the following command\. This is a one\-time operation\. After you’ve added the selector to your manifest, you don’t need to add it each time you update the add\-on\. If your cluster was deployed on or after August 17, 2020, then `kube-proxy` is already multi\-architecture capable\.

     ```
     kubectl edit -n kube-system daemonset/kube-proxy
     ```

     Add the following node selector to the file in the editor and then save the file\. For an example of where to include this text in the editor, see the [CNI manifest](https://github.com/aws/amazon-vpc-cni-k8s/blob/release-1.11/config/master/aws-k8s-cni.yaml#L265-#L269) file on GitHub\. This enables Kubernetes to pull the correct hardware image based on the node’s hardware architecture\.

     ```
     - key: "kubernetes.io/arch"
       operator: In
       values:
       - amd64
       - arm64
     ```

  1. If your cluster was originally created with Kubernetes version `1.14` or later, then you can skip this step because `kube-proxy` already includes this `Affinity Rule`\. If you originally created an Amazon EKS cluster with Kubernetes version `1.13` or earlier and intend to use Fargate nodes in your cluster, then edit your `kube-proxy` manifest to include a `NodeAffinity` rule to prevent `kube-proxy` Pods from scheduling on Fargate nodes\. This is a one\-time edit\. Once you’ve added the `Affinity Rule` to your manifest, you don’t need to add it each time that you update the add\-on\. Edit your `kube-proxy `\[noloc\]

  ```
  kubectl edit -n kube-system daemonset/kube-proxy
  ```

  Add the following `Affinity Rule` to the `DaemonSet ``spec` section of the file in the editor and then save the file\. For an example of where to include this text in the editor, see the [CNI manifest](https://github.com/aws/amazon-vpc-cni-k8s/blob/release-1.11/config/master/aws-k8s-cni.yaml#L270-#L273) file on GitHub\.

  ```
  - key: eks.amazonaws.com/compute-type
    operator: NotIn
    values:
    - fargate
  ```