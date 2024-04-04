# Migrating existing `aws-auth ConfigMap` entries to access entries<a name="migrating-access-entries"></a>

If you've added entries to the `aws-auth` `ConfigMap` on your cluster, we recommend that you create access entries for the existing entries in your `aws-auth` `ConfigMap`\. After creating the access entries, you can remove the entries from your `ConfigMap`\. You can't associate [access policies](access-policies.md) to entries in the `aws-auth` `ConfigMap`\. If you want to associate access polices to your IAM principals, create access entries\.

**Important**  
Don't remove existing `aws-auth` `ConfigMap` entries that were created by Amazon EKS when you added a [managed node group](managed-node-groups.md) or a [Fargate profile](fargate-profile.md) to your cluster\. If you remove entries that Amazon EKS created in the `ConfigMap`, your cluster won't function properly\. You can however, remove any entries for [self\-managed](worker.md) node groups after you've created access entries for them\.

**Prerequisites**
+ Familiarity with access entries and access policies\. For more information, see [Manage access entries](access-entries.md) and [Associating and disassociating access policies to and from access entries](access-policies.md)\.
+ An existing cluster with a platform version that is at or later than the versions listed in the Prerequisites of the [Allowing IAM roles or users access to Kubernetes objects on your Amazon EKS cluster](access-entries.md#access-entries-prerequisites) topic\.
+ Version `0.175.0` or later of the `eksctl` command line tool installed on your device or AWS CloudShell\. To install or update `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.
+ Kubernetes permissions to modify the `aws-auth` `ConfigMap` in the `kube-system` namespace\.
+ An AWS Identity and Access Management role or user with the following permissions: `CreateAccessEntry` and `ListAccessEntries`\. For more information, see [Actions defined by Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html#amazonelastickubernetesservice-actions-as-permissions) in the Service Authorization Reference\.

**To migrate an entry from your `aws-auth ConfigMap` to an access entry**

1. View the existing entries in your `aws-auth ConfigMap`\. Replace *my\-cluster* with the name of your cluster\.

   ```
   eksctl get iamidentitymapping --cluster my-cluster 
   ```

   An example output is as follows\.

   ```
   ARN                                                                                             USERNAME                                GROUPS                                                  ACCOUNT
   arn:aws:iam::111122223333:role/EKS-my-cluster-Admins                                            Admins                                  system:masters
   arn:aws:iam::111122223333:role/EKS-my-cluster-my-namespace-Viewers                              my-namespace-Viewers                    Viewers
   arn:aws:iam::111122223333:role/EKS-my-cluster-self-managed-ng-1                                 system:node:{{EC2PrivateDNSName}}       system:bootstrappers,system:nodes
   arn:aws:iam::111122223333:user/my-user                                                          my-user
   arn:aws:iam::111122223333:role/EKS-my-cluster-fargateprofile1                                   system:node:{{SessionName}}             system:bootstrappers,system:nodes,system:node-proxier
   arn:aws:iam::111122223333:role/EKS-my-cluster-managed-ng                                        system:node:{{EC2PrivateDNSName}}       system:bootstrappers,system:nodes
   ```

1. [Create access entries](access-entries.md#creating-access-entries) for any of the `ConfigMap` entries that you created returned in the previous output\. When creating the access entries, make sure to specify the same values for `ARN`, `USERNAME`, `GROUPS`, and `ACCOUNT` returned in your output\. In the example output, you would create access entries for all entries except the last two entries, since those entries were created by Amazon EKS for a Fargate profile and a managed node group\. 

1. Delete the entries from the `ConfigMap` for any access entries that you created\. If you don't delete the entry from the `ConfigMap`, the settings for the access entry for the IAM principal ARN override the `ConfigMap` entry\. Replace *111122223333* with your AWS account ID and *EKS\-my\-cluster\-my\-namespace\-Viewers* with the name of the role in the entry in your `ConfigMap`\. If the entry you're removing is for an IAM user, rather than an IAM role, replace **role** with **user** and *EKS\-my\-cluster\-my\-namespace\-Viewers* with the user name\.

   ```
   eksctl delete iamidentitymapping --arn arn:aws:iam::111122223333:role/EKS-my-cluster-my-namespace-Viewers --cluster my-cluster
   ```