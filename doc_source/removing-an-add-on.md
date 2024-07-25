# Removing an Amazon EKS add\-on from a cluster<a name="removing-an-add-on"></a>

You can remove an Amazon EKS add\-on from your cluster using `eksctl`, the AWS Management Console, or the AWS CLI\.

When you remove an Amazon EKS add\-on from a cluster:
+ There is no downtime for the functionality that the add\-on provides\.
+ If you are using IAM Roles for Service Accounts \(IRSA\) and the add\-on has an IAM role associated with it, the IAM role isn't removed\.
+ If you are using Pod Identities, any Pod Identity Assocataions owned by the add\-on are deleted\. If you specify the `--preserve` option to the AWS CLI, the assocations are preserved\. 
+ Amazon EKS stops managing settings for the add\-on\.
+ The console stops notifying you when new versions are available\.
+ You can't update the add\-on using any AWS tools or APIs\.
+ You can choose to leave the add\-on software on your cluster so that you can self\-manage it, or you can remove the add\-on software from your cluster\. You should only remove the add\-on software from your cluster if there are no resources on your cluster are dependent on the functionality that the add\-on provides\.

## Prerequisites<a name="removing-an-add-on-prereq"></a>

Complete the following before you create an add\-on:
+ An existing Amazon EKS cluster\. To deploy one, see [Get started with Amazon EKS](getting-started.md)\.
+ Check if your add\-on requires an IAM role\. For more information, see 
+ Version `0.187.0` or later of the `eksctl` command line tool installed on your device or AWS CloudShell\. To install or update `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.\.

## Procedure<a name="removing-an-add-on-procedure"></a>

You can create an Amazon EKS add\-on using `eksctl`, the AWS Management Console, or the AWS CLI\. If the add\-on requires an IAM role, see the details for the specific add\-on in [Available Amazon EKS add\-ons from AWS](workloads-add-ons-available-eks.md) for details about creating the role\.

------
#### [ eksctl ]

**To remove an Amazon EKS add\-on using `eksctl`**

1. Determine the current add\-ons installed on your cluster\. Replace `my-cluster` with the name of your cluster\.

   ```
   eksctl get addon --cluster my-cluster
   ```

   An example output is as follows\.

   ```
   NAME        VERSION              STATUS  ISSUES  IAMROLE  UPDATE AVAILABLE
   coredns     v1.8.7-eksbuild.2    ACTIVE  0
   kube-proxy  v1.23.7-eksbuild.1   ACTIVE  0                
   vpc-cni     v1.10.4-eksbuild.1   ACTIVE  0
   [...]
   ```

   Your output might look different, depending on which add\-ons and versions that you have on your cluster\.

1. Delete the add\-on\. Replace *`my-cluster`* with the name of your cluster and `name-of-add-on` with the name of the add\-on returned in the output of the previous step that you want to remove\. If you remove the ***\-\-preserve*** option, in addition to Amazon EKS no longer managing the add\-on, the add\-on software is removed from your cluster\.

   ```
   eksctl delete addon --cluster my-cluster --name name-of-addon --preserve
   ```

------
#### [ AWS Management Console ]

**To delete an Amazon EKS add\-on using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to remove the Amazon EKS add\-on for\.

1. Choose the **Add\-ons** tab\.

1. Select the check box in the upper right of the add\-on box and then choose **Remove**\. Select **Preserve on the cluster** if you want Amazon EKS to stop managing settings for the add\-on, but want to retain the add\-on software on your cluster so that you can self\-manage all of the settings for the add\-on\. Type the add\-on name and then select **Remove**\.

------
#### [ AWS CLI ]

**Prerequisite**  
Version `0.187.0` or later of the `eksctl` command line tool installed on your device or AWS CloudShell\. To install or update `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.

**To delete an Amazon EKS add\-on using the AWS CLI**

1. See a list of installed add\-ons\. Replace `my-cluster` with the name of your cluster\.

   ```
   aws eks list-addons --cluster-name my-cluster
   ```

   An example output is as follows\.

   ```
   {
       "addons": [
           "coredns",
           "kube-proxy",
           "vpc-cni",
           "name-of-addon"
       ]
   }
   ```

1. Delete the installed add\-on\. Replace `my-cluster` with the name of your cluster and `name-of-add-on` with the name of the add\-on that you want to remove\. Removing ***\-\-preserve*** removes the add\-on software from your cluster\.

   ```
   aws eks delete-addon --cluster-name my-cluster --addon-name name-of-addon --preserve
   ```

   The abbreviated example output is as follows\.

   ```
   {
       "addon": {
           "addonName": "name-of-add-on",
           "clusterName": "my-cluster",
           "status": "DELETING",
   [...]
   ```

1. Check the status of the deletion\. Replace `my-cluster` with the name of your cluster and `name-of-addon` with the name of the add\-on that you're removing\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name name-of-addon
   ```

   After the add\-on is deleted, the example output is as follows\.

   ```
   An error occurred (ResourceNotFoundException) when calling the DescribeAddon operation: No addon: name-of-addon found in cluster: my-cluster
   ```

------