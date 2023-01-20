# Updating the Amazon VPC CNI plugin for Kubernetes add\-on<a name="managing-vpc-cni"></a>

Amazon EKS supports native VPC networking with the Amazon VPC CNI plugin for Kubernetes add\-on\. This add\-on:
+ creates elastic network interfaces \(network interfaces\) and attaches them to your Amazon EC2 nodes\.
+ assigns a private `IPv4` or `IPv6` address from your VPC to each pod and service\. Your pods and services have the same IP address inside the pod as they do on the VPC network\.

The plugin is an open\-source project that is maintained on GitHub\. We recommend familiarizing yourself with the plugin by reading [amazon\-vpc\-cni\-k8s](https://github.com/aws/amazon-vpc-cni-k8s) and [Proposal: CNI plugin for Kubernetes networking over Amazon VPC](https://github.com/aws/amazon-vpc-cni-k8s/blob/master/docs/cni-proposal.md) on GitHub\. Several of the configuration variables for the plugin are expanded on in [Choosing pod networking use cases](pod-networking-use-cases.md)\. The plugin is fully supported for use on Amazon EKS and self\-managed Kubernetes clusters on AWS\.<a name="manage-vpc-cni-recommended-versions"></a>


**Recommended version of the Amazon VPC CNI add\-on for each Amazon EKS cluster version**  

|  | 1\.24 | 1\.23 | 1\.22 | 1\.21 | 1\.20 | 1\.19 | 
| --- | --- | --- | --- | --- | --- | --- | 
| Add\-on version | 1\.12\.1\-eksbuild\.1 | 1\.12\.1\-eksbuild\.1 | 1\.12\.1\-eksbuild\.1 | 1\.12\.1\-eksbuild\.1 | 1\.12\.1\-eksbuild\.1 | 1\.12\.1\-eksbuild\.1 | 

You can see which version is installed on your cluster with the following command\.

```
kubectl describe daemonset aws-node -n kube-system | grep amazon-k8s-cni: | cut -d ":" -f 3
```

The example output is as follows\.

```
v1.10.4-eksbuild.1
```

**Important**  
The version of the add\-on that was deployed when you created your cluster might be earlier than the recommended version\. Depending on how you've updated the add\-on in the past, your current version might not include `-eksbuild.1`\.<a name="manage-vpc-cni-add-on-on-prerequisites"></a>

**Prerequisites**
+ An existing Amazon EKS cluster\. To deploy one, see [Getting started with Amazon EKS](getting-started.md)\.
+ If your cluster is `1.21` or later, make sure that your `kube-proxy` and CoreDNS add\-ons are at the minimum versions listed in [Service account tokens](service-accounts.md#boundserviceaccounttoken-validated-add-on-versions)\.
+ An existing AWS Identity and Access Management \(IAM\) OpenID Connect \(OIDC\) provider for your cluster\. To determine whether you already have one, or to create one, see [Creating an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ An IAM role with the [AmazonEKS\_CNI\_Policy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy%24jsonEditor) IAM policy \(if your cluster uses the `IPv4` family\) or an [IPv6 policy](cni-iam-role.md#cni-iam-role-create-ipv6-policy) \(if your cluster uses the `IPv6` family\) attached to it\. For more information, see [Configuring the Amazon VPC CNI plugin for Kubernetes to use IAM roles for service accounts](cni-iam-role.md)\.
+ If you are using version `1.7.0` or later of the CNI plugin and you use custom pod security policies, see [Delete the default Amazon EKS pod security policy](pod-security-policy.md#psp-delete-default)[Pod security policy](pod-security-policy.md)\.

**Considerations**
+ Versions are specified as `major-version.minor-version.patch-version`
+ You should only update one minor version at a time\. For example, if your current minor version is `1.10` and you want to update to `1.12`, then you should update to `1.11` first, then update to `1.12`\.
+ All versions work with all Amazon EKS supported Kubernetes versions, though not all features of each release work with all Kubernetes versions\. When using different Amazon EKS features, if a specific version of the add\-on is required, then it's noted in the feature documentation\.

**To update your Amazon VPC CNI plugin for Kubernetes add\-on version**

1. Determine whether you have the Amazon EKS or self\-managed type of the add\-on installed on your cluster\. Replace *my\-cluster* with the name of your cluster\. If you don't know the difference between the two types of add\-ons, see [Amazon EKS add\-ons](eks-add-ons.md)\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name vpc-cni --query addon.addonVersion --output text
   ```

   The output returned is different, depending on the add\-on type installed on your cluster\.
   + **Amazon EKS add\-on**

     ```
     v1.10.4-eksbuild.1
     ```
   + **Self\-managed add\-on**

     ```
     An error occurred (ResourceNotFoundException) when calling the DescribeAddon operation: No addon: vpc-cni found in cluster: my-cluster
     ```

1. Update your Amazon VPC CNI plugin for Kubernetes add\-on using the procedure for the type of add\-on that you have installed on your cluster\.

------
#### [ Amazon EKS add\-on ]

   Follow the procedure in [Updating an add\-on](managing-add-ons.md#updating-an-add-on)\. When using that procedure, you're asked to provide the following information:
   + **Add\-on name** – Specify `vpc-cni`\.
   + **Version** – If you use the AWS Management Console to update the add\-on, you can select any available version shown in the console\. If you use any other tool to update the add\-on, you can specify any version returned by the AWS CLI or `eksctl` using the procedure in [Updating an add\-on](managing-add-ons.md#updating-an-add-on)\. The version of the add\-on that you install might not match a version in the [Recommended version of the Amazon VPC CNI add\-on for each Amazon EKS cluster version](#manage-vpc-cni-recommended-versions) table\.
   + **IAM role** – This add\-on requires AWS Identity and Access Management permissions\. We recommend that you create a dedicated IAM role to use with this add\-on\. To create this role, see [Configuring the Amazon VPC CNI plugin for Kubernetes to use IAM roles for service accounts](cni-iam-role.md)\.

   If you currently have the self\-managed add\-on type on your cluster, you can create the Amazon EKS add\-on type, and then update it, instead of updating the self\-managed type of the add\-on\. For more information, see [Creating an add\-on](managing-add-ons.md#creating-an-add-on)\.

   If you create version `1.12.0-eksbuild.1` or later of the add\-on on a cluster that has a version earlier than `1.12.0-eksbuild.1` of the self\-managed add\-on installed, then an unnecessary volume mount will be included in your add\-on configuration\. Since the volume mount is unused, it has no effect on the functionality of the add\-on\. You can remove the unused volume mount with the following command\.

   ```
   kubectl -n kube-system patch daemonset aws-node –-type='strategic' \
       –-patch '{"spec":{"template":{"spec":{"containers":[{"name":"aws-node","volumeMounts":[{"$patch":"delete","mountPath":"/var/run/dockershim.sock"}]}],"volumes":[{"$patch":"delete","name":"dockershim"}]}}}}'
   ```

   Alternatively, if you currently have a version earlier than `1.12.0-eksbuild.1` of the self\-managed add\-on installed on your cluster, and you want to add the Amazon EKS add\-on type, you can avoid running the previous command by completing the following steps:

   1. Add the same version of the Amazon EKS type of the add\-on as your current self\-managed add\-on type\. For example, if the version of your current self\-managed add\-on is `v1.11.4-eksbuild.1`, create version `v1.11.4-eksbuild.1` of the Amazon EKS add\-on\.

   1. Update the Amazon EKS add\-on version to version `1.12.0-eksbuild.1` or later\. You don't need to run the previous command because the unnecessary volume mount isn't present in your configuration\.

   You can also delete the add\-on from your cluster\. For more information, see [Deleting an add\-on](managing-add-ons.md#removing-an-add-on)\.

------
#### [ Self\-managed add\-on ]

   If you want to install the Amazon EKS type of the add\-on, see [Creating an add\-on](managing-add-ons.md#creating-an-add-on)\. When following the procedure in that topic, specify the add\-on with the name `vpc-cni`\. Before creating the Amazon EKS add\-on type, review the information on the Amazon EKS tab in this topic\. Complete the following procedure to update the self\-managed add\-on\.

**Important**  
We recommend that you update to the [recommended version](#manage-vpc-cni-recommended-versions), though you can update to any [release version](https://github.com/aws/amazon-vpc-cni-k8s/releases), if necessary\.

**To update the Amazon VPC CNI plugin for Kubernetes add\-on**

   1. View `[releases](https://github.com/aws/amazon-vpc-cni-k8s/releases)` on GitHub to see the available versions and familiarize yourself with the changes in the version that you want to update to\.

   1. Use the following command to determine your cluster's current Amazon VPC CNI plugin for Kubernetes add\-on version:

      ```
      kubectl describe daemonset aws-node --namespace kube-system | grep amazon-k8s-cni: | cut -d : -f 3
      ```

      The example output is as follows\.

      ```
      v1.10.4-eksbuild.1
      ```

      Your output might look different than the example output\. The version that Amazon EKS originally deployed with your cluster looks similar to the previous output\. If you've already updated the add\-on at least once using a manifest however, your output might not include `-eksbuild.1`\.

   1. Update the `DaemonSet` using [Helm V3](helm.md) or later, or by using a [manifest](#update-vpc-cni-manifest)\.

**Helm**

      1. Add the `eks-charts` repository to Helm\.

         ```
         helm repo add eks https://aws.github.io/eks-charts
         ```

      1. Update your local repository to make sure that you have the most recent charts\.

         ```
         helm repo update
         ```

      1. Backup your current settings so that you can determine which settings you need to specify values for in a later step\.

         ```
         kubectl get daemonset aws-node -n kube-system -o yaml > aws-k8s-cni-old.yaml
         ```

      1. If you installed the existing Amazon VPC CNI plugin for Kubernetes `DaemonSet` using Helm, then skip to the next step\.

         Complete one of the following options so that Helm can manage the `DaemonSet` resources:
         + Add the Helm annotations and labels to your existing resources\.

           1. Copy the following contents to your device\. Replace `aws-vpc-cni` if you want to use a different release name\. Run the command to create the `helm-cni.sh` file\.

              ```
              cat >helm-cni.sh <<EOF
              #!/usr/bin/env bash
              
              set -euo pipefail
              
              for kind in daemonSet clusterRole clusterRoleBinding serviceAccount; do
                echo "setting annotations and labels on $kind/aws-node"
                kubectl -n kube-system annotate --overwrite $kind aws-node meta.helm.sh/release-name=aws-vpc-cni
                kubectl -n kube-system annotate --overwrite $kind aws-node meta.helm.sh/release-namespace=kube-system
                kubectl -n kube-system label --overwrite $kind aws-node app.kubernetes.io/managed-by=Helm
              done
              EOF
              ```

           1. Make the script executable\.

              ```
              chmod +x helm-cni.sh
              ```

           1. Run the script

              ```
              ./helm-cni.sh
              ```
         + Remove the existing `DaemonSet` resources\.
**Important**  
Your cluster will experience downtime between completing this step and the next step\.

           ```
           kubectl delete serviceaccount aws-node -n kube-system
           kubectl delete customresourcedefinition eniconfigs.crd.k8s.amazonaws.com
           kubectl delete clusterrole aws-node
           kubectl delete clusterrolebinding aws-node
           kubectl delete daemonset aws-node -n kube-system
           ```

      1. Install the chart using one of the following options\. If you're installing version that's earlier than `1.12.0` of the Amazon VPC CNI plugin for Kubernetes, then you should use a version of the Helm chart that's earlier than `v1.2.0` for your installation\.

         Before running the installation, review the backup you made of the settings for your `DaemonSet` in a previous step and then review the [configuration settings](https://github.com/aws/amazon-vpc-cni-k8s/tree/master/charts/aws-vpc-cni#configuration) to determine if you need to set any of them\.

         If you have an existing IAM role to use with the `DaemonSet`, then add the following line at the end of the install options that follow\. If you don't have an IAM role associated to the `aws-node` Kubernetes service account, then we recommend creating one\. Replace `111122223333` with your account ID and **AmazonEKSVPCCNIRole** with the name of your role\. To create a role, see [Configuring the Amazon VPC CNI plugin for Kubernetes to use IAM roles for service accounts](cni-iam-role.md)\.

         ```
         --set serviceAccount.annotations."eks\.amazonaws\.com/role-arn"=arn:aws:iam::111122223333:role/AmazonEKSVPCCNIRole
         ```

         If you added the Helm annotations and labels in the previous step, then add the following settings to any of the following options\.

         ```
         --set originalMatchLabels=true
         --set crd.create=false
         ```
         + If your nodes have access to the Amazon EKS Amazon ECR repositories and are in the `us-west-2` AWS Region, then install the chart with the release name `aws-vpc-cni` and default configuration\. Replace *version* with the `major.minor.patch` version that you want to install\.

           ```
           helm upgrade -i aws-vpc-cni eks/aws-vpc-cni \
           --namespace kube-system \
           --set image.tag=version \
           --set init.image.tag=version
           ```
         + If your nodes have access to the Amazon EKS Amazon ECR repositories and are in an AWS Region other than `us-west-2`, then install the chart with the release name `aws-vpc-cni`\. Replace *eks\-ecr\-account*** with the value from [Amazon container image registries](add-ons-images.md) for the AWS Region that your cluster is in\. Replace *version* with the `major.minor.patch` version that you want to install\. Replace `region-code` with the AWS Region that your cluster is in\.

           ```
           helm upgrade -i aws-vpc-cni eks/aws-vpc-cni \
           --namespace kube-system \
           --set image.account=eks-ecr-account \
           --set image.region=region-code \
           --set image.tag=version \
           --set init.image.account=eks-ecr-account
           --set init.image.region=region-code \
           --set init.image.tag=version
           ```
         + If your nodes don't have access to the Amazon EKS Amazon ECR repositories 

           1. Pull the following container images and push them to a repository that your nodes have access to\. For more information on how to pull, tag, and push an image to your own repository, see [Copy a container image from one repository to another repository](copy-image-to-repository.md)\. We recommend using the version in the following commands, but if necessary, you can replace it with any [release version](https://github.com/aws/amazon-vpc-cni-k8s/releases)\. Replace *602401143452* and `region-code` with values from [Amazon container image registries](add-ons-images.md) for the AWS Region that your cluster is in\. Replace *version* with the `major.minor.patch` version that you want to install\.

              ```
              602401143452.dkr.ecr.region-code.amazonaws.com/amazon-k8s-cni-init:version
              602401143452.dkr.ecr.region-code.amazonaws.com/amazon-k8s-cni:version
              ```

           1. Install the chart with the release name `aws-vpc-cni` and default configuration\. Before running the installation, review the backup you made of the settings for your `DaemonSet` in a previous step and then review the [configuration settings](https://github.com/aws/amazon-vpc-cni-k8s/tree/master/charts/aws-vpc-cni#configuration) to determine if you need to set any of them\. Replace `registry`/*repo*:*tag* with your registry, repository, and tag\.

              ```
              helm upgrade -i aws-vpc-cni eks/aws-vpc-cni \
                  --namespace kube-system \
                  --set image.override=registry/repo:tag \
                  --set init.image.override=registry/repo:tag
              ```<a name="update-vpc-cni-manifest"></a>

**Manifest**

      1. If you've changed any default settings for your current Amazon VPC CNI plugin for Kubernetes `DaemonSet`, or you need to pull the container images from your own repository to update the `DaemonSet`, or your cluster is in a region other than `us-west-2`, or you need to update to a specific patch version for version `1.7` or earlier, then skip to the next step\.

         Run the following command to update your Amazon VPC CNI plugin for Kubernetes add\-on\. Replace *version* with the `major.minor.patch` version that you want to install\. It must be `1.7.0` or later\. Regardless of the patch version that you specify for `1.7`, such as `1.7.5`, the latest patch version of the image \(`1.7.10`\) is pulled\. 

         ```
         kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/vversion/config/master/aws-k8s-cni.yaml
         ```

         If you need to update to a version earlier than `1.7.0`, then download the manifest\. Replace *version* with the `major.minor` version that you want to install\. It can be version `1.6` or earlier\. The manifest pulls the latest patch version of the image for the version that you specify\.

         ```
         curl -O https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-version/config/vversion/aws-k8s-cni.yaml
         ```

         Skip to the [View the status of the `DaemonSet`](#add-on-vpc-cni-daemonset-status) step\.

      1. If your nodes have access to the Amazon EKS Amazon ECR image repositories, then skip to the next step\.

         Pull the following container images and push them to a repository that your nodes have access to\. For more information on how to pull, tag, and push an image to your own repository, see [Copy a container image from one repository to another repository](copy-image-to-repository.md)\. We recommend using the version in the following commands, but if necessary, you can replace it with any [release version](https://github.com/aws/amazon-vpc-cni-k8s/releases)\. Replace *602401143452* and `region-code` with values from [Amazon container image registries](add-ons-images.md) for the AWS Region that your cluster is in\. Replace *version* with the `major.minor.patch` version that you want to install\.

         ```
         602401143452.dkr.ecr.region-code.amazonaws.com/amazon-k8s-cni-init:version
         602401143452.dkr.ecr.region-code.amazonaws.com/amazon-k8s-cni:version
         ```

      1. If you haven't changed any of the default settings for the `DaemonSet`, skip to the next step\.

         Backup your current settings so that you can compare your settings to the default settings in the new manifest\.

         ```
         kubectl get daemonset aws-node -n kube-system -o yaml > aws-k8s-cni-old.yaml
         ```

      1. Download the manifest for the Amazon VPC CNI plugin for Kubernetes add\-on\. Replace *version* with the `major.minor.patch` version that you want to install\. It must be `1.7.0` or later\. Regardless of the patch version that you specify for `1.7`, such as `1.7.5`, the latest patch version of the image \(`1.7.10`\) is pulled\. 

         ```
         curl -O https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/vversion/config/master/aws-k8s-cni.yaml
         ```

         If you need to update to a version earlier than `1.7.0`, then download the manifest\. Replace *version* with the `major.minor` version that you want to install\. It can be version `1.6` or earlier\. The manifest pulls the latest patch version of the image for the version that you specify\.

         ```
         curl -O https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-version/config/vversion/aws-k8s-cni.yaml
         ```

         If you need a specific patch version of `1.7` or earlier, open the file in a text editor and replace `vversion` in the following two lines with the `major.minor.patch` version that you want to install\. After you've made the changes, save the file\.

         ```
         image: "602401143452.dkr.ecr.us-west-2.amazonaws.com/amazon-k8s-cni-init:version"
         image: "602401143452.dkr.ecr.us-west-2.amazonaws.com/amazon-k8s-cni:vversion"
         ```

      1. If you didn't copy the container images to your own repository in a previous step, then skip to the next step\.

         Replace the registry, repository, and tag in the file with your own\.

         1. Replace `your-registry` in the following command with your registry and then run the modified command to replace `602401143452.dkr.ecr.us-west-2.amazonaws.com` in the file\.

            ```
            sed -i.bak -e 's|602401143452.dkr.ecr.us-west-2.amazonaws.com|your-registry|' aws-k8s-cni.yaml
            ```

         1. Replace `your-repository` and `tag` in the following command with your repository and tag and then run the modified command to replace `amazon-k8s-cni-init:vversion` in the file\. Replace *version* with the version of the manifest that you downloaded\. 

            ```
            sed -i.bak -e 's|amazon-k8s-cni-init:vversion|your-repository:tag|' aws-k8s-cni.yaml
            ```

         1. Replace `your-repository` and `tag` in the following command with your repository and tag and then run the modified command to replace `amazon-k8s-cni:vversion` in the file\. Replace *version* with the version of the manifest that you downloaded\.

            ```
            sed -i.bak -e 's|amazon-k8s-cni:vversion|your-repository:tag|' aws-k8s-cni.yaml
            ```

         1. Skip to the [Compare settings](#add-on-vpc-cni-compare-settings) step\.

      1. Run the following command to replace information in the file with information for the AWS Region that your cluster is in\.

         1. Replace `us-west-2` in the file with the AWS Region that your cluster is in\.

            AWS GovCloud \(US\-East\)

            ```
            sed -i.bak -e 's|us-west-2|us-gov-east-1|' aws-k8s-cni.yaml
            ```

            AWS GovCloud \(US\-West\)

            ```
            sed -i.bak -e 's|us-west-2|us-gov-west-1|' aws-k8s-cni.yaml
            ```

            All other AWS Regions – Replace *region\-code* with the AWS Region that your cluster is in\. 

            ```
            sed -i.bak -e 's|us-west-2|region-code|' aws-k8s-cni.yaml
            ```

         1. Replace `602401143452` in the file with the account for the AWS Region that your cluster is in\.

            AWS GovCloud \(US\-East\)

            ```
            sed -i.bak -e 's|602401143452|151742754352|' aws-k8s-cni.yaml
            ```

            AWS GovCloud \(US\-West\)

            ```
            sed -i.bak -e 's|602401143452|013241004608|' aws-k8s-cni.yaml
            ```

            All other AWS Regions – Replace *account* with the value from [Amazon container image registries](add-ons-images.md) for the AWS Region that your cluster is in\. 

            ```
            sed -i.bak -e 's|602401143452|account|' aws-k8s-cni.yaml
            ```

      1. If you've changed any default settings for your current Amazon VPC CNI plugin for Kubernetes `DaemonSet` then compare the settings in the new manifest to the backup file that you made in a previous step\.

         ```
         diff aws-k8s-cni.yaml aws-k8s-cni-old.yaml -u
         ```

         Edit the new manifest file and make changes to any setting values so that they match the settings in your backup file\.

      1. Apply the manifest file to your cluster\.

         ```
         kubectl apply -f aws-k8s-cni.yaml
         ```

   1. View the status of the `DaemonSet`\.

      ```
      kubectl get daemonset aws-node -n kube-system
      ```

      The example output is as follows\.

      ```
      NAME       DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
      aws-node   2         2         2       2            2           <none>          4h39m
      ```

      Once the numbers in the `READY`, `UP-TO-DATE`, and `AVAILABLE` columns are the same, then your update is complete\. Your numbers may be different than those in the previous output\.

   1. View the `DaemonSet` to confirm the changes that you made\.

      ```
      kubectl get daemonset aws-node -n kube-system -o yaml
      ```

------