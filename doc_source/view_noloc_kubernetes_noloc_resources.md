--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# View Kubernetes resources<a name="view_noloc_kubernetes_noloc_resources"></a>

Unresolved directive in view\-kubernetes\-resources\.adoc \- include::\.\./attributes\.txt\[\] :https\-\-\-docs\-aws\-amazon\-com\-IAM\-latest\-UserGuide\-id\-users\-html: [https://docs\.aws\.amazon\.com/IAM/latest/UserGuide/id\_users\.html](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html) :https\-\-\-aws\-github\-io\-aws\-eks\-best\-practices\-security\-docs\-iam—​use\-tools\-to\-make\-changes\-to\-the\-aws\-auth\-configmap: [https://aws\.github\.io/aws\-eks\-best\-practices/security/docs/iam/](https://aws.github.io/aws-eks-best-practices/security/docs/iam/) *use\-tools\-to\-make\-changes\-to\-the\-aws\-auth\-configmap :https\-\-\-docs\-aws\-amazon\-com\-IAM\-latest\-UserGuide\-roles\-managingrole\-editing\-console\-html\-roles\-modify\-permissions\-policy: [https://docs\.aws\.amazon\.com/IAM/latest/UserGuide/roles\-managingrole\-editing\-console\.html\#roles\-modify\_permissions\-policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-managingrole-editing-console.html#roles-modify_permissions-policy) :https\-\-\-docs\-aws\-amazon\-com\-IAM\-latest\-UserGuide\-access\-controlling\-html\-access\-controlling\-principals: [https://docs\.aws\.amazon\.com/IAM/latest/UserGuide/access\_controlling\.html\#access\_controlling\-principals](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_controlling.html#access_controlling-principals) :https\-\-\-console\-aws\-amazon\-com\-eks\-home—​clusters: [https://console\.aws\.amazon\.com/eks/home](https://console.aws.amazon.com/eks/home) */clusters :https\-\-\-docs\-aws\-amazon\-com\-IAM\-latest\-UserGuide\-id\-roles\-terms\-and\-concepts\-html: [https://docs\.aws\.amazon\.com/IAM/latest/UserGuide/id\_roles\_terms\-and\-concepts\.html](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) 

## View Kubernetes resources<a name="view-kubernetes-resources"></a>

**Prerequisite**

1. Open the Amazon EKS console at \{https\-\-\-console\-aws\-amazon\-com\-eks\-home—​clusters\}\[[https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\]\.

1. In the **Clusters** list, select the cluster that contains the Kubernetes resources that you want to view\.

1. Select the **Resources** tab\.

1. Select a **Resource type** group that you want to view resources for, such as **Workloads**\. You see a list of resource types in that group\.

1. Select a resource type, such as **Deployments**, in the **Workloads** group\. You see a description of the resource type, a link to the Kubernetes documentation for more information about the resource type, and a list of resources of that type that are deployed on your cluster\. If the list is empty, then there are no resources of that type deployed to your cluster\.

1. Select a resource to view more information about it\. Try the following examples:
   + Select the **Workloads** group, select the **Deployments** resource type, and then select the **coredns** resource\. When you select a resource, you are in **Structured view**, by default\. For some resource types, you see a **Pods** section in **Structured view**\. This section lists the Pods managed by the workload\. You can select any Pod listed to view information about the Pod\. Not all resource types display information in **Structured View**\. If you select **Raw view** in the top right corner of the page for the resource, you see the complete JSON response from the Kubernetes API for the resource\.

### Required permissions<a name="view-kubernetes-resources-permissions"></a>

To view the **Resources** tab and **Nodes** section on the **Compute** tab in the \{aws\} Management Console, the \{https\-\-\-docs\-aws\-amazon\-com\-IAM\-latest\-UserGuide\-id\-roles\-terms\-and\-concepts\-html\}\[IAM principal\] that you’re using must have specific minimum IAM and Kubernetes permissions\. Complete the following steps to assign the required permissions to your IAM principals\.

1. Make sure that the `eks:Access[noloc]`Kubernetes`Api`, and other necessary IAM permissions to view Kubernetes resources, are assigned to the IAM principal that you’re using\. For more information about how to edit permissions for an IAM principal, see \{https\-\-\-docs\-aws\-amazon\-com\-IAM\-latest\-UserGuide\-access\-controlling\-html\-access\-controlling\-principals\}\[Controlling access for principals\] in the IAM User Guide\. For more information about how to edit permissions for a role, see \{https\-\-\-docs\-aws\-amazon\-com\-IAM\-latest\-UserGuide\-roles\-managingrole\-editing\-console\-html\-roles\-modify\-permissions\-policy\}\[Modifying a role permissions policy \(console\)\] in the IAM User Guide\.

   The following example policy includes the necessary permissions for a principal to view Kubernetes resources for all clusters in your account\. Replace ` 111122223333 ` with your \{aws\} account ID\.

   ```
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": [
                   "eks:ListFargateProfiles",
                   "eks:DescribeNodegroup",
                   "eks:ListNodegroups",
                   "eks:ListUpdates",
                   "eks:AccessKubernetesApi",
                   "eks:ListAddons",
                   "eks:DescribeCluster",
                   "eks:DescribeAddonVersions",
                   "eks:ListClusters",
                   "eks:ListIdentityProviderConfigs",
                   "iam:ListRoles"
               ],
               "Resource": "*"
           },
           {
               "Effect": "Allow",
               "Action": "ssm:GetParameter",
               "Resource": "arn:aws:ssm:*:111122223333:parameter/*"
           }
       ]
   }
   ```

1. Create a Kubernetes `rolebinding` or `clusterrolebinding` that is bound to a Kubernetes `role` or `clusterrole` that has the necessary permissions to view the Kubernetes resources\. To learn more about Kubernetes roles and role bindings, see [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) in the Kubernetes documentation\. You can apply one of the following manifests to your cluster that create a `role` and `rolebinding` or a `clusterrole` and `clusterrolebinding` with the necessary Kubernetes permissions:  
View Kubernetes resources in all namespaces  
   + The group name in the file is `eks-console-dashboard-full-access-group`\. Apply the manifest to your cluster with the following command:

     ```
     kubectl apply -f https://s3.us-west-2.amazonaws.com/amazon-eks/docs/eks-console-full-access.yaml
     ```  
View Kubernetes resources in a specific namespace  
   + The namespace in this file is `default`\. The group name in the file is `eks-console-dashboard-restricted-access-group`\. Apply the manifest to your cluster with the following command:

     ```
     kubectl apply -f https://s3.us-west-2.amazonaws.com/amazon-eks/docs/eks-console-restricted-access.yaml
     ```

   If you need to change the Kubernetes group name, namespace, permissions, or any other configuration in the file, then download the file and edit it before applying it to your cluster:

   \+

   1. Download the file with one of the following commands:

      ```
      curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/docs/eks-console-full-access.yaml
      ```

```
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/docs/eks-console-restricted-access.yaml
```

1. Edit the file as necessary\.

1. Apply the manifest to your cluster with one of the following commands:

   ```
   kubectl apply -f eks-console-full-access.yaml
   ```

```
kubectl apply -f eks-console-restricted-access.yaml
```

1. Map the \{https\-\-\-docs\-aws\-amazon\-com\-IAM\-latest\-UserGuide\-id\-roles\-terms\-and\-concepts\-html\}\[IAM principal\] to the Kubernetes user or group in the `aws-auth`ConfigMap. You can use a tool such as `eksctl` to update the `ConfigMap` or you can update it manually by editing it\.
**Important**  
We recommend using `eksctl`, or another tool, to edit the `ConfigMap`\. For information about other tools you can use, see \{https\-\-\-aws\-github\-io\-aws\-eks\-best\-practices\-security\-docs\-iam—​use\-tools\-to\-make\-changes\-to\-the\-aws\-auth\-configmap\}\[Use tools to make changes to the aws\-authConfigMap\] in the Amazon EKS best practices guides\. An improperly formatted `aws\-auth``ConfigMap` can cause you to lose access to your cluster\.

   \+  
eksctl  
\*\* \.Prerequisite Version `0.177.0` or later of the `eksctl` command line tool installed on your device or \{aws\} CloudShell\. To install or update `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.  

   1. View the current mappings in the `ConfigMap`\. Replace ` my-cluster ` with the name of your cluster\. Replace `[replaceable]`region\-code```` with the \{aws\} Region that your cluster is in\.

```
eksctl get iamidentitymapping --cluster my-cluster --region=region-code
```

\+

An example output is as follows\.

\+

```
ARN                                                                                             USERNAME                                GROUPS                          ACCOUNT
arn:aws:iam::111122223333:role/eksctl-my-cluster-my-nodegroup-NodeInstanceRole-1XLS7754U3ZPA    system:node:{{EC2PrivateDNSName}}       system:bootstrappers,system:nodes
```

1. Add a mapping for a role\. This example assume that you attached the IAM permissions in the first step to a role named `[replaceable]`my\-console\-viewer\-role` `. Replace `[replaceable] with your account ID.` 

   ```
   eksctl create iamidentitymapping \
       --cluster my-cluster \
       --region=region-code \
       --arn arn:aws:iam::111122223333:role/my-console-viewer-role \
       --group eks-console-dashboard-full-access-group \
       --no-duplicate-arns
   ```
**Important**  
The role ARN can’t include a path such as `role/my-team/developers/my-role`\. The format of the ARN must be `arn:aws:iam::[replaceable]`111122223333`:role/[replaceable]`my\-role````\. In this example, `my-team/developers/` needs to be removed\.

An example output is as follows\.

\+

```
[...]
2022-05-09 14:51:20 [ℹ]  adding identity "arn:aws:iam::`111122223333`:role/`my-console-viewer-role`" to auth ConfigMap
```

1. Add a mapping for a user\. \{https\-\-\-docs\-aws\-amazon\-com\-IAM\-latest\-UserGuide\-id\-users\-html\}\[IAM best practices\] recommend that you grant permissions to roles instead of users\. This example assume that you attached the IAM permissions in the first step to a user named `[replaceable]`my\-user` `. Replace `[replaceable] with your account ID.` 

   ```
   eksctl create iamidentitymapping \
       --cluster my-cluster \
       --region=region-code \
       --arn arn:aws:iam::111122223333:user/my-user \
       --group eks-console-dashboard-restricted-access-group \
       --no-duplicate-arns
   ```

    An example output is as follows\. 

   ```
   [...]
   2022-05-09 14:53:48 [ℹ]  adding identity "arn:aws:iam::`111122223333`:user/`my-user`" to auth ConfigMap
   ``` 

   

   ```
   [...]
   2022-05-09 14:53:48 [ℹ]  adding identity "arn:aws:iam::`111122223333`:user/`my-user`" to auth ConfigMap
   ``` View the mappings in the `ConfigMap` again\.

   ```
   eksctl get iamidentitymapping --cluster my-cluster --region=region-code
   ```

   An example output is as follows\.

   ```
   ARN                                                                                             USERNAME                                GROUPS                                  ACCOUNT
   arn:aws:iam::111122223333:role/eksctl-my-cluster-my-nodegroup-NodeInstanceRole-1XLS7754U3ZPA    system:node:{{EC2PrivateDNSName}}       system:bootstrappers,system:nodes
   arn:aws:iam::111122223333:role/my-console-viewer-role                                                                                   eks-console-dashboard-full-access-group
   arn:aws:iam::111122223333:user/my-user                                                                                                  eks-console-dashboard-restricted-access-group
   ```

Edit ConfigMap manually  Open the `aws\-auth``ConfigMap` for editing\.

   ```
   kubectl edit -n kube-system configmap/aws-auth
   ```Add the mappings to the `aws\-auth``ConfigMap`, but don’t replace any of the existing mappings\. The following example adds mappings between \{https\-\-\-docs\-aws\-amazon\-com\-IAM\-latest\-UserGuide\-id\-roles\-terms\-and\-concepts\-html\}\[IAM principals\] with permissions added in the first step and the Kubernetes groups created in the previous step:
   + The ` my-console-viewer-role ` role and the `eks-console-dashboard-full-access-group`\.
   + The ` my-user ` user and the `eks-console-dashboard-restricted-access-group`\.

   These examples assume that you attached the IAM permissions in the first step to a role named ` my-console-viewer-role ` and a user named `[replaceable]`my\-user` `. Replace `[replaceable] with your {aws} account ID.` \+ 

   ```
   apiVersion: v1
   data:
   mapRoles: |
     - groups:
       - eks-console-dashboard-full-access-group
       rolearn: arn:aws:iam::111122223333:role/my-console-viewer-role
       username: my-console-viewer-role
   mapUsers: |
     - groups:
       - eks-console-dashboard-restricted-access-group
       userarn: arn:aws:iam::111122223333:user/my-user
       username: my-user
   ```

    \+ IMPORTANT: The role ARN can’t include a path such as `role/my-team/developers/my-console-viewer-role`\. The format of the ARN must be `arn:aws:iam::[replaceable]`111122223333`:role/[replaceable]`my\-console\-viewer\-role````\. In this example, `my-team/developers/` needs to be removed\. 

   `role/my-team/developers/my-console-viewer-role`\. The format of the ARN must be `arn:aws:iam::[replaceable]`111122223333`:role/[replaceable]`my\-console\-viewer\-role````\. In this example, `my-team/developers/` needs to be removed\. 

   \. The format of the ARN must be `arn:aws:iam::[replaceable]`111122223333`:role/[replaceable]`my\-console\-viewer\-role````\. In this example, `my-team/developers/` needs to be removed\. 

   `arn:aws:iam::[replaceable]`111122223333`:role/[replaceable]`my\-console\-viewer\-role````\. In this example, `my-team/developers/` needs to be removed\. 

   111122223333`:role/[replaceable]`my\-console\-viewer\-role````\. In this example, `my-team/developers/` needs to be removed\. 

   `:role/[replaceable]`my\-console\-viewer\-role````\. In this example, `my-team/developers/` needs to be removed\. 

   my\-console\-viewer\-role````\. In this example, `my-team/developers/` needs to be removed\. 

   `my-team/developers/` needs to be removed\. 

    needs to be removed\. Save the file and exit your text editor\.