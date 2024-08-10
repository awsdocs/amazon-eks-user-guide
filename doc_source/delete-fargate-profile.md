# Delete a Fargate profile<a name="delete-fargate-profile"></a>

This topic describes how to delete a Fargate profile\. When you delete a Fargate profile, any Pods that were scheduled onto Fargate with the profile are deleted\. If those Pods match another Fargate profile, then they're scheduled on Fargate with that profile\. If they no longer match any Fargate profiles, then they aren't scheduled onto Fargate and might remain as pending\.

Only one Fargate profile in a cluster can be in the `DELETING` status at a time\. Wait for a Fargate profile to finish deleting before you can delete any other profiles in that cluster\. 

You can delete a profile with `eksctl`, the AWS Management Console, or the AWS CLI\. Select the tab with the name of the tool that you want to use to delete your profile\.

------
#### [ eksctl ]

**To delete a Fargate profile with `eksctl`**

Use the following command to delete a profile from a cluster\. Replace every `example value` with your own values\.

```
eksctl delete fargateprofile  --name my-profile --cluster my-cluster
```

------
#### [ AWS Management Console ]

**To delete a Fargate profile from a cluster with the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, choose **Clusters**\. In the list of clusters, choose the cluster that you want to delete the Fargate profile from\.

1. Choose the **Compute** tab\.

1. Choose the Fargate profile to delete, and then choose **Delete**\.

1. On the **Delete Fargate profile** page, enter the name of the profile, and then choose **Delete**\.

------
#### [ AWS CLI ]

**To delete a Fargate profile with AWS CLI**

Use the following command to delete a profile from a cluster\. Replace every `example value` with your own values\.

```
aws eks delete-fargate-profile --fargate-profile-name my-profile --cluster-name my-cluster
```

------