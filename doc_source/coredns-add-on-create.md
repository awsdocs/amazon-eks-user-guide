# Create the CoreDNS Amazon EKS add\-on<a name="coredns-add-on-create"></a>

Create the CoreDNS Amazon EKS add\-on\. You must have a cluster before you create the add\-on\. For more information, see [Create an Amazon EKS cluster](create-cluster.md)\.

1. See which version of the add\-on is installed on your cluster\.

   ```
   kubectl describe deployment coredns --namespace kube-system | grep coredns: | cut -d : -f 3
   ```

   An example output is as follows\.

   ```
   v1.10.1-eksbuild.13
   ```

1. See which type of the add\-on is installed on your cluster\. Depending on the tool that you created your cluster with, you might not currently have the Amazon EKS add\-on type installed on your cluster\. Replace *my\-cluster* with the name of your cluster\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name coredns --query addon.addonVersion --output text
   ```

   If a version number is returned, you have the Amazon EKS type of the add\-on installed on your cluster and don't need to complete the remaining steps in this procedure\. If an error is returned, you don't have the Amazon EKS type of the add\-on installed on your cluster\. Complete the remaining steps of this procedure to install it\.

1. Save the configuration of your currently installed add\-on\.

   ```
   kubectl get deployment coredns -n kube-system -o yaml > aws-k8s-coredns-old.yaml
   ```

1. Create the add\-on using the AWS CLI\. If you want to use the AWS Management Console or `eksctl` to create the add\-on, see [Creating an Amazon EKS add\-on](creating-an-add-on.md) and specify `coredns` for the add\-on name\. Copy the command that follows to your device\. Make the following modifications to the command, as needed, and then run the modified command\.
   + Replace `my-cluster` with the name of your cluster\.
   + Replace *v1\.11\.1\-eksbuild\.11* with the latest version listed in the [latest version table](managing-coredns.md#coredns-versions) for your cluster version\.

   ```
   aws eks create-addon --cluster-name my-cluster --addon-name coredns --addon-version v1.11.1-eksbuild.11
   ```

   If you've applied custom settings to your current add\-on that conflict with the default settings of the Amazon EKS add\-on, creation might fail\. If creation fails, you receive an error that can help you resolve the issue\. Alternatively, you can add **\-\-resolve\-conflicts OVERWRITE** to the previous command\. This allows the add\-on to overwrite any existing custom settings\. Once you've created the add\-on, you can update it with your custom settings\.

1. Confirm that the latest version of the add\-on for your cluster's Kubernetes version was added to your cluster\. Replace `my-cluster` with the name of your cluster\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name coredns --query addon.addonVersion --output text
   ```

   It might take several seconds for add\-on creation to complete\.

   An example output is as follows\.

   ```
   v1.11.1-eksbuild.11
   ```

1. If you made custom settings to your original add\-on, before you created the Amazon EKS add\-on, use the configuration that you saved in a previous step to [update](coredns-add-on-update.md) the Amazon EKS add\-on with your custom settings\.