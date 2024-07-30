# Update access entries<a name="updating-access-entries"></a>

You can update an access entry using the AWS Management Console or the AWS CLI\.

------
#### [ AWS Management Console ]

**To update an access entry**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the name of the cluster that you want to create an access entry in\.

1. Choose the **Access** tab\.

1. Choose the access entry that you want to update\.

1. Choose **Edit**\.

1. For **Username**, you can change the existing value\.

1. For **Groups**, you can remove existing group names or add new group names\. If the following groups names exist, don't remove them: **system:nodes** or **system:bootstrappers**\. Removing these groups can cause your cluster to function improperly\. If you don't specify any group names and want to use Amazon EKS authorization, associate an [access policy](access-policies.md) in a later step\.

1. For **Tags**, you can assign labels to the access entry\. For example, to make it easier to find all resources with the same tag\. You can also remove existing tags\.

1. Choose **Save changes**\.

1. If you want to associate an access policy to the entry, see [Associating and disassociating access policies to and from access entries](access-policies.md)\.

------
#### [ AWS CLI ]

**Prerequisite**  
Install the AWS CLI, as described in [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) in the AWS Command Line Interface User Guide\.

**To update an access entry**  
Replace *my\-cluster* with the name of your cluster, *111122223333* with your AWS account ID, and *EKS\-my\-cluster\-my\-namespace\-Viewers* with the name of an IAM role\.

```
aws eks update-access-entry --cluster-name my-cluster --principal-arn arn:aws:iam::111122223333:role/EKS-my-cluster-my-namespace-Viewers --kubernetes-groups Viewers 
```

You can't use the `--kubernetes-groups` option if the type of the access entry is a value other than `STANDARD`\. You also can't associate an access policy to an access entry with a type other than `STANDARD`\. 

------