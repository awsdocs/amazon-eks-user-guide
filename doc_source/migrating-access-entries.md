--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Migrating existing `aws-auth ConfigMap` entries to access entries<a name="migrating-access-entries"></a>

**Important**  
+ Version `0.177.0` or later of the `eksctl` command line tool installed on your device or AWS CloudShell\. To install or update `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.
+  Kubernetes permissions to modify the `aws-auth`ConfigMap in the `kube-system` namespace\.
+ An AWS Identity and Access Management role or user with the following permissions: `CreateAccessEntry` and `ListAccessEntries`\. For more information, see [Actions defined by Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html#amazonelastickubernetesservice-actions-as-permissions) in the Service Authorization Reference\.

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

  1. Delete the entries from the `ConfigMap` for any access entries that you created\. If you don’t delete the entry from the `ConfigMap`, the settings for the access entry for the IAM principal ARN override the `ConfigMap` entry\. Replace *111122223333* with your AWS account ID and *EKS\-my\-cluster\-my\-namespace\-Viewers* with the name of the role in the entry in your `ConfigMap`\. If the entry you’re removing is for an IAM user, rather than an IAM role, replace `role` with `user` and *EKS\-my\-cluster\-my\-namespace\-Viewers* with the user name\.

     ```
     eksctl delete iamidentitymapping --arn arn:aws:iam::111122223333:role/EKS-my-cluster-my-namespace-Viewers --cluster my-cluster
     ```