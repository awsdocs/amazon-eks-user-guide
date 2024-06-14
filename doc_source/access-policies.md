--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Associating and disassociating access policies to and from access entries<a name="access-policies"></a>
+ An AWS Identity and Access Management role or user with the following permissions: `ListAccessEntries`, `DescribeAccessEntry`, `UpdateAccessEntry`, `ListAccessPolicies`, `AssociateAccessPolicy`, and `DisassociateAccessPolicy`\. For more information, see [Actions defined by Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html#amazonelastickubernetesservice-actions-as-permissions) in the Service Authorization Reference\.

Before associating access policies with access entries, consider the following requirements:
+ You can associate multiple access policies to each access entry, but you can only associate each policy to an access entry once\. If you associate multiple access policies, the access entry’s IAM principal has all permissions included in all associated access policies\.
+ You can scope an access policy to all resources on a cluster or by specifying the name of one or more Kubernetes namespaces\. You can use wildcard characters for a namespace name\. For example, if you want to scope an access policy to all namespaces that start with `dev-`, you can specify `dev-*` as a namespace name\. Make sure that the namespaces exist on your cluster and that your spelling matches the actual namespace name on the cluster\. Amazon EKS doesn’t confirm the spelling or existence of the namespaces on your cluster\.
+ You can change the *access scope* for an access policy after you associate it to an access entry\. If you’ve scoped the access policy to Kubernetes namespaces, you can add and remove namespaces for the association, as necessary\.
+ If you associate an access policy to an access entry that also has *group names* specified, then the IAM principal has all the permissions in all associated access policies\. It also has all the permissions in any Kubernetes `Role` or `ClusterRole` object that is specified in any Kubernetes `Role` and `RoleBinding` objects that specify the group names\.
+ If you run the `kubectl auth can-i --list` command, you won’t see any Kubernetes permissions assigned by access policies associated with an access entry for the IAM principal you’re using when you run the command\. The command only shows Kubernetes permissions if you’ve granted them in Kubernetes `Role` or `ClusterRole` objects that you’ve bound to the group names or username that you specified for an access entry\.
+ If you impersonate a Kubernetes user or group when interacting with Kubernetes objects on your cluster, such as using the `kubectl` command with `--as username ` or `--as-group [replaceable]`group\-name` `, you’re forcing the use of [noloc] objects that you’ve bound to the group names or user name. For your IAM principal to have the permissions in associated access policies, don’t impersonate a Kubernetes user or group. The IAM principal will still also have any permissions that you’ve granted them in the Kubernetes Role or ClusterRole objects that you’ve bound to the group names or user name that you specified for the access entry. For more information, see [User impersonation](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#user-impersonation) in the Kubernetes documentation.` 

You can associate an access policy to an access entry using the AWS Management Console or the AWS CLI\.

 AWS Management Console  

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the name of the cluster that has an access entry that you want to associate an access policy to\.

1. Choose the **Access** tab\.

1. If the type of the access entry is **Standard**, you can associate or disassociate Amazon EKS **access policies**\. If the type of your access entry is anything other than **Standard**, then this option isn’t available\.

1. Choose **Associate access policy**\.

1. For **Access scope**, choose an access scope\. If you choose **Cluster**, the permissions in the access policy are granted to the IAM principal for resources in all Kubernetes namespaces\. If you choose ** Kubernetes namespace**, you can then choose **Add new namespace**\. In the **Namespace** field that appears, you can enter the name of a Kubernetes namespace on your cluster\. If you want the IAM principal to have the permissions across multiple namespaces, then you can enter multiple namespaces\.

1. Choose **Add access policy**\.

 AWS CLI  
\* \.Prerequisite Version `2.12.3` or later or version `1.27.160` or later of the AWS Command Line Interface \(AWS CLI\) installed and configured on your device or AWS CloudShell\. To check your current version, use ` `aws --version | cut -d / -f2 | cut -d ' ' -f1 are often several versions behind the latest version of the AWS CLI. To install the latest version, see [Installing](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with aws configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the AWS Command Line Interface User Guide. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version. To update it, see [Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the AWS CloudShell User Guide.`   

1. View the available access policies\.

   ```
   aws eks list-access-policies --output table
   ```

   An example output is as follows\.

   ```
   ---------------------------------------------------------------------------------------------------------
   //⁂|                                          ListAccessPolicies                                           |
   +-------------------------------------------------------------------------------------------------------+
   //⁂||                                           accessPolicies                                            ||
   //⁂|+---------------------------------------------------------------------+-------------------------------+|
   //⁂||                                 arn                                 |             name              ||
   //⁂|+---------------------------------------------------------------------+-------------------------------+|
   //⁂||  arn:aws:eks::aws:cluster-access-policy/AmazonEKSAdminPolicy        |  AmazonEKSAdminPolicy         ||
   //⁂||  arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy |  AmazonEKSClusterAdminPolicy  ||
   //⁂||  arn:aws:eks::aws:cluster-access-policy/AmazonEKSEditPolicy         |  AmazonEKSEditPolicy          ||
   //⁂||  arn:aws:eks::aws:cluster-access-policy/AmazonEKSViewPolicy         |  AmazonEKSViewPolicy          ||
   //⁂|+---------------------------------------------------------------------+-------------------------------+|
   ```

1. View your existing access entries\. Replace *my\-cluster* with the name of your cluster\.

   ```
   aws eks list-access-entries --cluster-name my-cluster
   ```

   An example output is as follows\.

   ```
   {
       "accessEntries": [
           "arn:aws:iam::`111122223333`:role/`my-role`",
           "arn:aws:iam::`111122223333`:user/`my-user`"
       ]
   }
   ```

1. Associate an access policy to an access entry\. The following example associates the `AmazonEKSViewPolicy` access policy to an access entry\. Whenever the *my\-role* IAM role attempts to access Kubernetes objects on the cluster, Amazon EKS will authorize the role to use the permissions in the policy to access Kubernetes objects in the *my\-namespace1* and *my\-namespace2* Kubernetes namespaces only\. Replace *my\-cluster* with the name of your cluster, *111122223333* with your AWS account ID, and *my\-role* with the name of the IAM role that you want Amazon EKS to authorize access to Kubernetes cluster objects for\.

   ```
   aws eks associate-access-policy --cluster-name my-cluster --principal-arn arn:aws:iam::111122223333:role/my-role \
       --access-scope type=namespace,namespaces=my-namespace1,my-namespace2 --policy-arn arn:aws:eks::aws:cluster-access-policy/AmazonEKSViewPolicy
   ```

   If you want the IAM principal to have the permissions cluster\-wide, replace `type=namespace,namespaces=my-namespace1,my-namespace2 ` with `type=cluster`\. If you want to associate multiple access policies to the access entry, run the command multiple times, each with a unique access policy\. Each associated access policy has its own scope\.
**Note**  
If you later want to change the scope of an associated access policy, run the previous command again with the new scope\. For example, if you wanted to remove *my\-namespace2*, you’d run the command again using `type=namespace,namespaces=my-namespace1 ` only\. If you wanted to change the scope from `namespace` to `cluster`, you’d run the command again using `type=cluster`, removing `type=namespace,namespaces=[replaceable]`my\-namespace1`,[replaceable]`my\-namespace2````\.

1. Determine which access policies are associated to an access entry\.

   ```
   aws eks list-associated-access-policies --cluster-name my-cluster --principal-arn arn:aws:iam::111122223333:role/my-role
   ```

   An example output is as follows\.

   ```
   {
       "clusterName": "`my-cluster`",
       "principalArn": "arn:aws:iam::`111122223333`",
       "associatedAccessPolicies": [
           {
               "policyArn": "arn:aws:eks::aws:cluster-access-policy/`AmazonEKSViewPolicy`",
               "accessScope": {
                   "type": "cluster",
                   "namespaces": []
               },
               "associatedAt": "2023-04-17T15:25:21.675000-04:00",
               "modifiedAt": "2023-04-17T15:25:21.675000-04:00"
           },
           {
               "policyArn": "arn:aws:eks::aws:cluster-access-policy/`AmazonEKSAdminPolicy`",
               "accessScope": {
                   "type": "namespace",
                   "namespaces": [
                       "`my-namespace1`",
                       "`my-namespace2`"
                   ]
               },
               "associatedAt": "2023-04-17T15:02:06.511000-04:00",
               "modifiedAt": "2023-04-17T15:02:06.511000-04:00"
           }
       ]
   }
   ```

   In the previous example, the IAM principal for this access entry has view permissions across all namespaces on the cluster, and administrator permissions to two Kubernetes namespaces\.

1. Disassociate an access policy from an access entry\. In this example, the `AmazonEKSAdminPolicy` policy is disassociated from an access entry\. The IAM principal retains the permissions in the `AmazonEKSViewPolicy` access policy for objects in the *my\-namespace1* and *my\-namespace2* namespaces however, because that access policy is not disassociated from the access entry\.

   ```
   aws eks disassociate-access-policy --cluster-name my-cluster --principal-arn arn:aws:iam::111122223333:role/my-role \
       --policy-arn arn:aws:eks::aws:cluster-access-policy/AmazonEKSAdminPolicy
   ```

## Access policy permissions<a name="access-policy-permissions"></a>

Choose any access policy to see its contents\. Each row of each table in each access policy is a separate rule\.

### AmazonEKSAdminPolicy<a name="access-policy-permissions-amazoneksadminpolicy"></a>

 **ARN** – `arn:aws:eks::aws:cluster-access-policy/AmazonEKSAdminPolicy` 

### AmazonEKSClusterAdminPolicy<a name="access-policy-permissions-amazoneksclusteradminpolicy"></a>

 **ARN** – `arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy` 

### AmazonEKSAdminViewPolicy<a name="access-policy-permissions-amazoneksadminviewpolicy"></a>

This access policy includes permissions that grant an IAM principal access to list/view all resources in a cluster\. Note this includes [Kubernetes Secrets\.](https://kubernetes.io/docs/concepts/configuration/secret/) 

 **ARN** – `arn:aws:eks::aws:cluster-access-policy/AmazonEKSAdminViewPolicy` 

### AmazonEKSEditPolicy<a name="access-policy-permissions-amazonekseditpolicy"></a>

This access policy includes permissions that allow an IAM principal to edit most Kubernetes resources\.

 **ARN** – `arn:aws:eks::aws:cluster-access-policy/AmazonEKSEditPolicy` 

### AmazonEKSViewPolicy<a name="access-policy-permissions-amazoneksviewpolicy.json"></a>

This access policy includes permissions that allow an IAM principal to view most Kubernetes resources\.

 **ARN** – `arn:aws:eks::aws:cluster-access-policy/AmazonEKSViewPolicy` 

## Access policy updates<a name="access-policy-updates"></a>

Access policies introduced\.

Amazon EKS introduced access policies\.