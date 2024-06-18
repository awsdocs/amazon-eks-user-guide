# Associating and disassociating access policies to and from access entries<a name="access-policies"></a>

You can assign one or more access policies to *access entries* of *type* `STANDARD`\. Amazon EKS automatically grants the other types of access entries the permissions required to function properly in your cluster\. Amazon EKS access policies include Kubernetes permissions, not IAM permissions\. Before associating an access policy to an access entry, make sure that you're familiar with the Kubernetes permissions included in each access policy\. For more information, see [Access policy permissions](#access-policy-permissions)\. If none of the access policies meet your requirements, then don't associate an access policy to an access entry\. Instead, specify one or more *group names* for the access entry and create and manage Kubernetes role\-based access control objects\. For more information, see [Creating access entries](access-entries.md#creating-access-entries)\.

**Prerequisites**
+ An existing access entry\. To create one, see [Creating access entries](access-entries.md#creating-access-entries)\.
+ An AWS Identity and Access Management role or user with the following permissions: `ListAccessEntries`, `DescribeAccessEntry`, `UpdateAccessEntry`, `ListAccessPolicies`, `AssociateAccessPolicy`, and `DisassociateAccessPolicy`\. For more information, see [Actions defined by Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html#amazonelastickubernetesservice-actions-as-permissions) in the Service Authorization Reference\.

Before associating access policies with access entries, consider the following requirements:
+ You can associate multiple access policies to each access entry, but you can only associate each policy to an access entry once\. If you associate multiple access policies, the access entry's IAM principal has all permissions included in all associated access policies\.
+ You can scope an access policy to all resources on a cluster or by specifying the name of one or more Kubernetes namespaces\. You can use wildcard characters for a namespace name\. For example, if you want to scope an access policy to all namespaces that start with `dev-`, you can specify `dev-*` as a namespace name\. Make sure that the namespaces exist on your cluster and that your spelling matches the actual namespace name on the cluster\. Amazon EKS doesn't confirm the spelling or existence of the namespaces on your cluster\.
+ You can change the *access scope* for an access policy after you associate it to an access entry\. If you've scoped the access policy to Kubernetes namespaces, you can add and remove namespaces for the association, as necessary\.
+ If you associate an access policy to an access entry that also has *group names* specified, then the IAM principal has all the permissions in all associated access policies\. It also has all the permissions in any Kubernetes `Role` or `ClusterRole` object that is specified in any Kubernetes `Role` and `RoleBinding` objects that specify the group names\.
+ If you run the `kubectl auth can-i --list` command, you won't see any Kubernetes permissions assigned by access policies associated with an access entry for the IAM principal you're using when you run the command\. The command only shows Kubernetes permissions if you've granted them in Kubernetes `Role` or `ClusterRole` objects that you've bound to the group names or username that you specified for an access entry\.
+ If you impersonate a Kubernetes user or group when interacting with Kubernetes objects on your cluster, such as using the `kubectl` command with **\-\-as *username*** or **\-\-as\-group *group\-name***, you're forcing the use of Kubernetes RBAC authorization\. As a result, the IAM principal has no permissions assigned by any access policies associated to the access entry\. The only Kubernetes permissions that the user or group that the IAM principal is impersonating has are the Kubernetes permissions that you've granted them in Kubernetes `Role` or `ClusterRole` objects that you've bound to the group names or user name\. For your IAM principal to have the permissions in associated access policies, don't impersonate a Kubernetes user or group\. The IAM principal will still also have any permissions that you've granted them in the Kubernetes `Role` or `ClusterRole` objects that you've bound to the group names or user name that you specified for the access entry\. For more information, see [User impersonation](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#user-impersonation) in the Kubernetes documentation\.

You can associate an access policy to an access entry using the AWS Management Console or the AWS CLI\.

------
#### [ AWS Management Console ]

**To associate an access policy to an access entry using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the name of the cluster that has an access entry that you want to associate an access policy to\.

1. Choose the **Access** tab\.

1. If the type of the access entry is **Standard**, you can associate or disassociate Amazon EKS **access policies**\. If the type of your access entry is anything other than **Standard**, then this option isn't available\.

1. Choose **Associate access policy**\.

1. For **Policy name**, select the policy with the permissions you want the IAM principal to have\. To view the permissions included in each policy, see [Access policy permissions](#access-policy-permissions)\.

1. For **Access scope**, choose an access scope\. If you choose **Cluster**, the permissions in the access policy are granted to the IAM principal for resources in all Kubernetes namespaces\. If you choose **Kubernetes namespace**, you can then choose **Add new namespace**\. In the **Namespace** field that appears, you can enter the name of a Kubernetes namespace on your cluster\. If you want the IAM principal to have the permissions across multiple namespaces, then you can enter multiple namespaces\.

1. Choose **Add access policy**\.

------
#### [ AWS CLI ]

**Prerequisite**  
Version `2.12.3` or later or version `1.27.160` or later of the AWS Command Line Interface \(AWS CLI\) installed and configured on your device or AWS CloudShell\. To check your current version, use `aws --version | cut -d / -f2 | cut -d ' ' -f1`\. Package managers such `yum`, `apt-get`, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI\. To install the latest version, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with aws configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the *AWS Command Line Interface User Guide*\. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version\. To update it, see [Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the *AWS CloudShell User Guide*\.

**To associate an access policy to an access entry**

1. View the available access policies\.

   ```
   aws eks list-access-policies --output table
   ```

   An example output is as follows\.

   ```
   ---------------------------------------------------------------------------------------------------------
   |                                          ListAccessPolicies                                           |
   +-------------------------------------------------------------------------------------------------------+
   ||                                           accessPolicies                                            ||
   |+---------------------------------------------------------------------+-------------------------------+|
   ||                                 arn                                 |             name              ||
   |+---------------------------------------------------------------------+-------------------------------+|
   ||  arn:aws:eks::aws:cluster-access-policy/AmazonEKSAdminPolicy        |  AmazonEKSAdminPolicy         ||
   ||  arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy |  AmazonEKSClusterAdminPolicy  ||
   ||  arn:aws:eks::aws:cluster-access-policy/AmazonEKSEditPolicy         |  AmazonEKSEditPolicy          ||
   ||  arn:aws:eks::aws:cluster-access-policy/AmazonEKSViewPolicy         |  AmazonEKSViewPolicy          ||
   |+---------------------------------------------------------------------+-------------------------------+|
   ```

   To view the permissions included in each policy, see [Access policy permissions](#access-policy-permissions)\.

1. View your existing access entries\. Replace *my\-cluster* with the name of your cluster\.

   ```
   aws eks list-access-entries --cluster-name my-cluster
   ```

   An example output is as follows\.

   ```
   {
       "accessEntries": [
           "arn:aws:iam::111122223333:role/my-role",
           "arn:aws:iam::111122223333:user/my-user"
       ]
   }
   ```

1. Associate an access policy to an access entry\. The following example associates the `AmazonEKSViewPolicy` access policy to an access entry\. Whenever the *my\-role* IAM role attempts to access Kubernetes objects on the cluster, Amazon EKS will authorize the role to use the permissions in the policy to access Kubernetes objects in the *my\-namespace1* and *my\-namespace2* Kubernetes namespaces only\. Replace *my\-cluster* with the name of your cluster, *111122223333* with your AWS account ID, and *my\-role* with the name of the IAM role that you want Amazon EKS to authorize access to Kubernetes cluster objects for\.

   ```
   aws eks associate-access-policy --cluster-name my-cluster --principal-arn arn:aws:iam::111122223333:role/my-role \
       --access-scope type=namespace,namespaces=my-namespace1,my-namespace2 --policy-arn arn:aws:eks::aws:cluster-access-policy/AmazonEKSViewPolicy
   ```

   If you want the IAM principal to have the permissions cluster\-wide, replace **type=namespace,namespaces=*my\-namespace1*,*my\-namespace2*** with **type=cluster**\. If you want to associate multiple access policies to the access entry, run the command multiple times, each with a unique access policy\. Each associated access policy has its own scope\.
**Note**  
If you later want to change the scope of an associated access policy, run the previous command again with the new scope\. For example, if you wanted to remove *my\-namespace2*, you'd run the command again using **type=namespace,namespaces=*my\-namespace1*** only\. If you wanted to change the scope from **namespace** to **cluster**, you'd run the command again using **type=cluster**, removing **type=namespace,namespaces=*my\-namespace1*,*my\-namespace2***\.

**To disassociate an access policy from an access entry**

1. Determine which access policies are associated to an access entry\.

   ```
   aws eks list-associated-access-policies --cluster-name my-cluster --principal-arn arn:aws:iam::111122223333:role/my-role
   ```

   An example output is as follows\.

   ```
   {
       "clusterName": "my-cluster",
       "principalArn": "arn:aws:iam::111122223333",
       "associatedAccessPolicies": [
           {
               "policyArn": "arn:aws:eks::aws:cluster-access-policy/AmazonEKSViewPolicy",
               "accessScope": {
                   "type": "cluster",
                   "namespaces": []
               },
               "associatedAt": "2023-04-17T15:25:21.675000-04:00",
               "modifiedAt": "2023-04-17T15:25:21.675000-04:00"
           },
           {
               "policyArn": "arn:aws:eks::aws:cluster-access-policy/AmazonEKSAdminPolicy",
               "accessScope": {
                   "type": "namespace",
                   "namespaces": [
                       "my-namespace1",
                       "my-namespace2"
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

------

## Access policy permissions<a name="access-policy-permissions"></a>

Access policies include `rules` that contain Kubernetes `verbs` \(permissions\) and `resources`\. Access policies don't include IAM permissions or resources\. Similar to Kubernetes `Role` and `ClusterRole` objects, access policies only include `allow` `rules`\. You can't modify the contents of an access policy\. You can't create your own access policies\. If the permissions in the access policies don't meet your needs, then create Kubernetes RBAC objects and specify *group names* for your access entries\. For more information, see [Creating access entries](access-entries.md#creating-access-entries)\. The permissions contained in access policies are similar to the permissions in the Kubernetes user\-facing cluster roles\. For more information, see [User\-facing roles](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#user-facing-roles) in the Kubernetes documentation\. 

Choose any access policy to see its contents\. Each row of each table in each access policy is a separate rule\.

### AmazonEKSAdminPolicy<a name="access-policy-permissions-AmazonEKSAdminPolicy"></a>

This access policy includes permissions that grant an IAM principal most permissions to resources\. When associated to an access entry, its access scope is typically one or more Kubernetes namespaces\. If you want an IAM principal to have administrator access to all resources on your cluster, associate the [AmazonEKSClusterAdminPolicy](#access-policy-permissions-AmazonEKSClusterAdminPolicy) access policy to your access entry instead\.

**ARN** – `arn:aws:eks::aws:cluster-access-policy/AmazonEKSAdminPolicy`


| Kubernetes API groups | Kubernetes resources | Kubernetes verbs \(permissions\) | 
| --- | --- | --- | 
| apps | daemonsets, deployments, deployments/rollback, deployments/scale, replicasets, replicasets/scale, statefulsets, statefulsets/scale | create, delete, deletecollection, patch, update | 
| apps | controllerrevisions, daemonsets, daemonsets/status, deployments, deployments/scale, deployments/status, replicasets, replicasets/scale, replicasets/status, statefulsets, statefulsets/scale, statefulsets/status | get, list, watch | 
| authorization\.k8s\.io | localsubjectaccessreviews | create | 
| autoscaling | horizontalpodautoscalers | create, delete, deletecollection, patch, update | 
| autoscaling | horizontalpodautoscalers, horizontalpodautoscalers/status | get, list, watch | 
| batch | cronjobs, jobs | create, delete, deletecollection, patch, update | 
| batch | cronjobs, cronjobs/status, jobs, jobs/status | get, list, watch | 
| discovery\.k8s\.io | endpointslices | get, list, watch | 
| extensions | daemonsets, deployments, deployments/rollback, deployments/scale, ingresses, networkpolicies, replicasets, replicasets/scale, replicationcontrollers/scale | create, delete, deletecollection, patch, update | 
| extensions | daemonsets, daemonsets/status, deployments, deployments/scale, deployments/status, ingresses, ingresses/status, networkpolicies, replicasets, replicasets/scale, replicasets/status, replicationcontrollers/scale | get, list, watch | 
| networking\.k8s\.io | ingresses, ingresses/status, networkpolicies | get, list, watch | 
| networking\.k8s\.io | ingresses, networkpolicies | create, delete, deletecollection, patch, update | 
| policy | poddisruptionbudgets | create, delete, deletecollection, patch, update | 
| policy | poddisruptionbudgets, poddisruptionbudgets/status | get, list, watch | 
| rbac\.authorization\.k8s\.io | rolebindings, roles | create, delete, deletecollection, get, list, patch, update, watch | 
|  | configmaps, endpoints, persistentvolumeclaims, persistentvolumeclaims/status, pods, replicationcontrollers, replicationcontrollers/scale, serviceaccounts, services, services/status | get,list, watch | 
|  | pods/attach, pods/exec, pods/portforward, pods/proxy, secrets, services/proxy | get, list, watch | 
|  | configmaps, events, persistentvolumeclaims, replicationcontrollers, replicationcontrollers/scale, secrets, serviceaccounts, services, services/proxy | create, delete, deletecollection, patch, update | 
|  | pods, pods/attach, pods/exec, pods/portforward, pods/proxy | create, delete, deletecollection, patch, update | 
|  | serviceaccounts | impersonate | 
|  | bindings, events, limitranges, namespaces/status, pods/log, pods/status, replicationcontrollers/status, resourcequotas, resourcequotas/status | get, list, watch | 
|  | namespaces | get,list, watch | 

### AmazonEKSClusterAdminPolicy<a name="access-policy-permissions-AmazonEKSClusterAdminPolicy"></a>

This access policy includes permissions that grant an IAM principal administrator access to a cluster\. When associated to an access entry, its access scope is typically the cluster, rather than a Kubernetes namespace\. If you want an IAM principal to have a more limited administrative scope, consider associating the [AmazonEKSAdminPolicy](#access-policy-permissions-AmazonEKSAdminPolicy) access policy to your access entry instead\.

**ARN** – `arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy`


| Kubernetes API groups | Kubernetes nonResourceURLs | Kubernetes resources | Kubernetes verbs \(permissions\) | 
| --- | --- | --- | --- | 
| \* |  | \* | \* | 
|  | \* |  | \* | 

### AmazonEKSAdminViewPolicy<a name="access-policy-permissions-AmazonEKSAdminViewPolicy"></a>

This access policy includes permissions that grant an IAM principal access to list/view all resources in a cluster\. Note this includes [Kubernetes Secrets\.](https://kubernetes.io/docs/concepts/configuration/secret/)

**ARN** – `arn:aws:eks::aws:cluster-access-policy/AmazonEKSAdminViewPolicy`


| Kubernetes API groups | Kubernetes resources | Kubernetes verbs \(permissions\) | 
| --- | --- | --- | 
| \* | \* | get, list, watch | 

### AmazonEKSEditPolicy<a name="access-policy-permissions-AmazonEKSEditPolicy"></a>

This access policy includes permissions that allow an IAM principal to edit most Kubernetes resources\.

**ARN** – `arn:aws:eks::aws:cluster-access-policy/AmazonEKSEditPolicy`


| Kubernetes API groups | Kubernetes resources | Kubernetes verbs \(permissions\) | 
| --- | --- | --- | 
| apps | daemonsets, deployments, deployments/rollback, deployments/scale, replicasets, replicasets/scale, statefulsets, statefulsets/scale | create, delete, deletecollection, patch, update | 
| apps | controllerrevisions, daemonsets, daemonsets/status, deployments, deployments/scale, deployments/status, replicasets, replicasets/scale, replicasets/status, statefulsets, statefulsets/scale, statefulsets/status | get, list, watch | 
| autoscaling | horizontalpodautoscalers, horizontalpodautoscalers/status | get, list, watch | 
| autoscaling | horizontalpodautoscalers | create, delete, deletecollection, patch, update | 
| batch | cronjobs, jobs | create, delete, deletecollection, patch, update | 
| batch | cronjobs, cronjobs/status, jobs, jobs/status | get, list, watch | 
| discovery\.k8s\.io | endpointslices | get, list, watch | 
| extensions | daemonsets, deployments, deployments/rollback, deployments/scale, ingresses, networkpolicies, replicasets, replicasets/scale, replicationcontrollers/scale | create, delete, deletecollection, patch, update | 
| extensions | daemonsets, daemonsets/status, deployments, deployments/scale, deployments/status, ingresses, ingresses/status, networkpolicies, replicasets, replicasets/scale, replicasets/status, replicationcontrollers/scale | get, list, watch | 
| networking\.k8s\.io | ingresses, networkpolicies | create, delete, deletecollection, patch, update | 
| networking\.k8s\.io | ingresses, ingresses/status, networkpolicies | get, list, watch | 
| policy | poddisruptionbudgets | create, delete, deletecollection, patch, update | 
| policy | poddisruptionbudgets, poddisruptionbudgets/status | get, list, watch | 
|  | namespaces | get, list, watch | 
|  | pods/attach, pods/exec, pods/portforward, pods/proxy, secrets, services/proxy | get, list, watch | 
|  | serviceaccounts | impersonate | 
|  | pods, pods/attach, pods/exec, pods/portforward, pods/proxy | create, delete, deletecollection, patch, update | 
|  | configmaps, events, persistentvolumeclaims, replicationcontrollers, replicationcontrollers/scale, secrets, serviceaccounts, services, services/proxy | create, delete, deletecollection, patch, update | 
|  | configmaps, endpoints, persistentvolumeclaims, persistentvolumeclaims/status, pods, replicationcontrollers, replicationcontrollers/scale, serviceaccounts, services, services/status | get, list, watch | 
|  | bindings, events, limitranges, namespaces/status, pods/log, pods/status, replicationcontrollers/status, resourcequotas, resourcequotas/status | get, list, watch | 

### AmazonEKSViewPolicy<a name="access-policy-permissions-AmazonEKSViewPolicy.json"></a>

This access policy includes permissions that allow an IAM principal to view most Kubernetes resources\.

**ARN** – `arn:aws:eks::aws:cluster-access-policy/AmazonEKSViewPolicy`


| Kubernetes API groups | Kubernetes resources | Kubernetes verbs \(permissions\) | 
| --- | --- | --- | 
| apps | controllerrevisions, daemonsets, daemonsets/status, deployments, deployments/scale, deployments/status, replicasets, replicasets/scale, replicasets/status, statefulsets, statefulsets/scale, statefulsets/status | get, list, watch | 
| autoscaling | horizontalpodautoscalers, horizontalpodautoscalers/status | get, list, watch | 
| batch | cronjobs, cronjobs/status, jobs, jobs/status | get, list, watch | 
| discovery\.k8s\.io | endpointslices | get, list, watch | 
| extensions | daemonsets, daemonsets/status, deployments, deployments/scale, deployments/status, ingresses, ingresses/status, networkpolicies, replicasets, replicasets/scale, replicasets/status, replicationcontrollers/scale | get, list, watch | 
| networking\.k8s\.io | ingresses, ingresses/status, networkpolicies | get, list, watch | 
| policy | poddisruptionbudgets, poddisruptionbudgets/status | get, list, watch | 
|  | configmaps, endpoints, persistentvolumeclaims, persistentvolumeclaims/status, pods, replicationcontrollers, replicationcontrollers/scale, serviceaccounts, services, services/status | get, list, watch | 
|  | bindings, events, limitranges, namespaces/status, pods/log, pods/status, replicationcontrollers/status, resourcequotas, resourcequotas/status | get, list, watch | 
|  | namespaces | get, list, watch | 

## Access policy updates<a name="access-policy-updates"></a>

View details about updates to access policies, since they were introduced\. For automatic alerts about changes to this page, subscribe to the RSS feed on the Amazon EKS [Document history page](doc-history.md)\.


| Change | Description | Date | 
| --- | --- | --- | 
| Add AmazonEKSAdminViewPolicy | Add a new policy for expanded view access, including resources like Secrets\. | April 23, 2024 | 
|  Access policies introduced\.  |  Amazon EKS introduced access policies\.  | May 29, 2023 | 