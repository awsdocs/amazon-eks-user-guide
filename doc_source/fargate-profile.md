--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# AWS Fargate profile<a name="fargate-profile"></a>

**Important**  
 AWS Fargate with Amazon EKS isn’t available in AWS GovCloud \(US\-East\) and AWS GovCloud \(US\-West\)\.

Before you schedule Pods on Fargate in your cluster, you must define at least one Fargate profile that specifies which Pods use Fargate when launched\.

As an administrator, you can use a Fargate profile to declare which Pods run on Fargate\. You can do this through the profile’s selectors\. You can add up to five selectors to each profile\. Each selector must contain a namespace\. The selector can also include labels\. The label field consists of multiple optional key\-value pairs\. Pods that match a selector are scheduled on Fargate\. Pods are matched using a namespace and the labels that are specified in the selector\. If a namespace selector is defined without labels, Amazon EKS attempts to schedule all the Pods that run in that namespace onto Fargate using the profile\. If a to\-be\-scheduled Pod matches any of the selectors in the Fargate profile, then that Pod is scheduled on Fargate\.

If a Pod matches multiple Fargate profiles, you can specify which profile a Pod uses by adding the following Kubernetes label to the Pod specification: `eks.amazonaws.com/fargate-profile: [replaceable]`my\-fargate\-profile` `. The [noloc].` 

Fargate profiles can’t be changed\. However, you can create a new updated profile to replace an existing profile, and then delete the original\.

**Note**  
Any Pods that are running using a Fargate profile are stopped and put into a pending state when the profile is deleted\.

If any Fargate profiles in a cluster are in the `DELETING` status, you must wait until after the Fargate profile is deleted before you create other profiles in that cluster\.

Amazon EKS and Fargate spread Pods across each of the subnets that’s defined in the Fargate profile\. However, you might end up with an uneven spread\. If you must have an even spread, use two Fargate profiles\. Even spread is important in scenarios where you want to deploy two replicas and don’t want any downtime\. We recommend that each profile has only one subnet\.

## Fargate profile components<a name="fargate-profile-components"></a>

The following components are contained in a Fargate profile\.

Pod execution role  
+ When your cluster creates Pods on AWS Fargate, the `kubelet` that’s running on the Fargate infrastructure must make calls to AWS APIs on your behalf\. For example, it needs to make calls to pull container images from Amazon ECR\. The Amazon EKS Pod execution role provides the IAM permissions to do this\.

Subnets  
+ The IDs of subnets to launch Pods into that use this profile\. At this time, Pods that are running on Fargate aren’t assigned public IP addresses\. Therefore, only private subnets with no direct route to an Internet Gateway are accepted for this parameter\.

Selectors  
+ The selectors to match for Pods to use this Fargate profile\. You might specify up to five selectors in a Fargate profile\. The selectors have the following components:
  +  **Namespace** – You must specify a namespace for a selector\. The selector only matches Pods that are created in this namespace\. However, you can create multiple selectors to target multiple namespaces\.
  +  **Labels** – You can optionally specify Kubernetes labels to match for the selector\. The selector only matches Pods that have all of the labels that are specified in the selector\.

## Fargate profile wildcards<a name="fargate-profile-wildcards"></a>

In addition to characters allowed by Kubernetes, you’re allowed to use ` \* and ? in the selector criteria for namespaces, label keys, and label values: ` 
+  ` * represents none, one, or multiple characters. For example, prod* can represent prod and prod-metrics. ` 
+  ` ? represents a single character (for example, value? can represent valuea). However, it can’t represent value and value-a, because ? can only represent exactly one character. ` 

These wildcard characters can be used in any position and in combination \(for example, ` `prod*). Other wildcards and forms of pattern matching, such as regular expressions, aren’t supported.` 

If there are multiple matching profiles for the namespace and labels in the Pod spec, Fargate picks up the profile based on alphanumeric sorting by profile name\. For example, if both profile A \(with the name `beta-workload`\) and profile B \(with the name `prod-workload`\) have matching selectors for the Pods to be launched, Fargate picks profile A \(`beta-workload`\) for the Pods\. The Pods have labels with profile A on the Pods \(for example, `eks.amazonaws.com/fargate-profile=beta-workload`\)\.

If you want to migrate existing Fargate Pods to new profiles that use wildcards, there are two ways to do so:
+ Create a new profile with matching selectors, then delete the old profiles\. Pods labeled with old profiles are rescheduled to new matching profiles\.
+ If you want to migrate workloads but aren’t sure what Fargate labels are on each Fargate Pod, you can use the following method\. Create a new profile with a name that sorts alphanumerically first among the profiles on the same cluster\. Then, recycle the Fargate Pods that need to be migrated to new profiles\.

## Creating a Fargate profile<a name="create-fargate-profile"></a>

This procedure requires `eksctl` version `0.177.0` or later\. You can check your version with the following command:

```
eksctl version
```

For instructions on how to install or upgrade `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.

eksctl  
\* \.To create a Fargate profile with `eksctl` Create your Fargate profile with the following `eksctl` command, replacing every ` example value ` with your own values\. You’re required to specify a namespace\. However, the `--labels` option isn’t required\.  

```
eksctl create fargateprofile \
    --cluster my-cluster \
    --name my-fargate-profile \
    --namespace my-kubernetes-namespace \
    --labels key=value
```

 AWS Management Console  

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the cluster to create a Fargate profile for\.

1. Choose the **Compute** tab\.

1. Under **Fargate profiles**, choose **Add Fargate profile**\.

1. On the **Configure Fargate profile** page, do the following:

   1. For **Name**, enter a unique name for your Fargate profile, such as `[replaceable]`my\-profile````\.

   1. Modify the selected **Subnets** as needed\.
**Note**  
Only private subnets are supported for Pods that are running on Fargate\.

   1. For **Tags**, you can optionally tag your Fargate profile\. These tags don’t propagate to other resources that are associated with the profile, such as Pods\.

   1. Choose **Next**\.

1. On the **Configure Pod selection** page, do the following:

   1. For **Namespace**, enter a namespace to match for Pods\.
      + You can use specific namespaces to match, such as ` kube-system or `default. ` 
      + \(Optional\) Add Kubernetes labels to the selector\. Specifically, add them to the one that the Pods in the specified namespace need to match\.
        + You can add the label ` infrastructure: fargate to the selector so that only Pods in the specified namespace that also have the infrastructure: fargate Kubernetes label match the selector.` Choose **Next**\.

1. On the **Review and create** page, review the information for your Fargate profile and choose **Create**\.

## Deleting a Fargate profile<a name="delete-fargate-profile"></a>

This topic describes how to delete a Fargate profile\.

When you delete a Fargate profile, any Pods that were scheduled onto Fargate with the profile are deleted\. If those Pods match another Fargate profile, then they’re scheduled on Fargate with that profile\. If they no longer match any Fargate profiles, then they aren’t scheduled onto Fargate and might remain as pending\.

Only one Fargate profile in a cluster can be in the `DELETING` status at a time\. Wait for a Fargate profile to finish deleting before you can delete any other profiles in that cluster\.

You can delete a profile with `eksctl`, the AWS Management Console, or the AWS CLI\. Select the tab with the name of the tool that you want to use to delete your profile\.

eksctl  
+  **To delete a Fargate profile with ` eksctl ` ** 

  Use the following command to delete a profile from a cluster\. Replace every ` example value ` with your own values\.

  ```
  eksctl delete fargateprofile  --name my-profile --cluster my-cluster
  ```

 AWS Management Console  

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, choose **Clusters**\. In the list of clusters, choose the cluster that you want to delete the Fargate profile from\.

1. Choose the **Compute** tab\.

1. Choose the Fargate profile to delete, and then choose **Delete**\.

1. On the **Delete Fargate profile** page, enter the name of the profile, and then choose **Delete**\.

 AWS CLI  
+  **To delete a Fargate profile with AWS CLI** 

  Use the following command to delete a profile from a cluster\. Replace every ` example value ` with your own values\.

  ```
  aws eks delete-fargate-profile --fargate-profile-name my-profile --cluster-name my-cluster
  ```