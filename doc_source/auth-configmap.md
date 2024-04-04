# Enabling IAM principal access to your cluster<a name="auth-configmap"></a>

**Important**  
The `aws-auth` ConfigMap is deprecated\. The reccomended method to manage access to Kubernetes APIs is [Access Entries](access-entries.md)\. 

Access to your cluster using [IAM principals](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) is enabled by the [AWS IAM Authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator#readme), which runs on the Amazon EKS control plane\. The authenticator gets its configuration information from the `aws-auth` `ConfigMap`\. For all `aws-auth` `ConfigMap` settings, see [Full Configuration Format](https://github.com/kubernetes-sigs/aws-iam-authenticator#full-configuration-format) on GitHub\. 

## Add IAM principals to your Amazon EKS cluster<a name="aws-auth-users"></a>

When you create an Amazon EKS cluster, the [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) that creates the cluster is automatically granted `system:masters` permissions in the cluster's role\-based access control \(RBAC\) configuration in the Amazon EKS control plane\. This principal doesn't appear in any visible configuration, so make sure to keep track of which principal originally created the cluster\. To grant additional IAM principals the ability to interact with your cluster, edit the `aws-auth` `ConfigMap` within Kubernetes and create a Kubernetes `rolebinding` or `clusterrolebinding` with the name of a `group` that you specify in the `aws-auth` `ConfigMap`\.

**Note**  
For more information about Kubernetes role\-based access control \(RBAC\) configuration, see [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) in the Kubernetes documentation\. 

**To add an IAM principal to an Amazon EKS cluster**

1. Determine which credentials `kubectl` is using to access your cluster\. On your computer, you can see which credentials `kubectl` uses with the following command\. Replace ***\~/\.kube/config*** with the path to your `kubeconfig` file if you don't use the default path\.

   ```
   cat ~/.kube/config
   ```

   An example output is as follows\.

   ```
   [...]
   contexts:
   - context:
       cluster: my-cluster.region-code.eksctl.io
       user: admin@my-cluster.region-code.eksctl.io
     name: admin@my-cluster.region-code.eksctl.io
   current-context: admin@my-cluster.region-code.eksctl.io
   [...]
   ```

   In the previous example output, the credentials for a user named `admin` are configured for a cluster named `my-cluster`\. If this is the user that created the cluster, then it already has access to your cluster\. If it's not the user that created the cluster, then you need to complete the remaining steps to enable cluster access for other IAM principals\. [IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html) recommend that you grant permissions to roles instead of users\. You can see which other principals currently have access to your cluster with the following command:

   ```
   kubectl describe -n kube-system configmap/aws-auth
   ```

   An example output is as follows\.

   ```
   Name:         aws-auth
   Namespace:    kube-system
   Labels:       <none>
   Annotations:  <none>
   
   Data
   ====
   mapRoles:
   ----
   - groups:
     - system:bootstrappers
     - system:nodes
     rolearn: arn:aws:iam::111122223333:role/my-node-role
     username: system:node:{{EC2PrivateDNSName}}
   
   
   BinaryData
   ====
   
   Events:  <none>
   ```

   The previous example is a default `aws-auth` `ConfigMap`\. Only the node instance role has access to the cluster\.

1. Make sure that you have existing Kubernetes `roles` and `rolebindings` or `clusterroles` and `clusterrolebindings` that you can map IAM principals to\. For more information about these resources, see [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) in the Kubernetes documentation\.

   1. View your existing Kubernetes `roles` or `clusterroles`\. `Roles` are scoped to a `namespace`, but `clusterroles` are scoped to the cluster\. 

      ```
      kubectl get roles -A
      ```

      ```
      kubectl get clusterroles
      ```

   1. View the details of any `role` or `clusterrole` returned in the previous output and confirm that it has the permissions \(`rules`\) that you want your IAM principals to have in your cluster\.

      Replace `role-name` with a `role` name returned in the output from the previous command\. Replace `kube-system` with the namespace of the `role`\.

      ```
      kubectl describe role role-name -n kube-system
      ```

      Replace `cluster-role-name` with a `clusterrole` name returned in the output from the previous command\.

      ```
      kubectl describe clusterrole cluster-role-name
      ```

   1. View your existing Kubernetes `rolebindings` or `clusterrolebindings`\. `Rolebindings` are scoped to a `namespace`, but `clusterrolebindings` are scoped to the cluster\.

      ```
      kubectl get rolebindings -A
      ```

      ```
      kubectl get clusterrolebindings
      ```

   1. View the details of any `rolebinding` or `clusterrolebinding` and confirm that it has a `role` or `clusterrole` from the previous step listed as a `roleRef` and a group name listed for `subjects`\.

      Replace `role-binding-name` with a `rolebinding` name returned in the output from the previous command\. Replace `kube-system` with the `namespace` of the `rolebinding`\.

      ```
      kubectl describe rolebinding role-binding-name -n kube-system
      ```

      An example output is as follows\.

      ```
      apiVersion: rbac.authorization.k8s.io/v1
      kind: RoleBinding
      metadata:
        name: eks-console-dashboard-restricted-access-role-binding
        namespace: default
      subjects:
      - kind: Group
        name: eks-console-dashboard-restricted-access-group
        apiGroup: rbac.authorization.k8s.io
      roleRef:
        kind: Role
        name: eks-console-dashboard-restricted-access-role
        apiGroup: rbac.authorization.k8s.io
      ```

      Replace `cluster-role-binding-name` with a `clusterrolebinding` name returned in the output from the previous command\.

      ```
      kubectl describe clusterrolebinding cluster-role-binding-name
      ```

      An example output is as follows\.

      ```
      apiVersion: rbac.authorization.k8s.io/v1
      kind: ClusterRoleBinding
      metadata:
        name: eks-console-dashboard-full-access-binding
      subjects:
      - kind: Group
        name: eks-console-dashboard-full-access-group
        apiGroup: rbac.authorization.k8s.io
      roleRef:
        kind: ClusterRole
        name: eks-console-dashboard-full-access-clusterrole
        apiGroup: rbac.authorization.k8s.io
      ```

1. Edit the `aws-auth` `ConfigMap`\. You can use a tool such as `eksctl` to update the `ConfigMap` or you can update it manually by editing it\.
**Important**  
We recommend using `eksctl`, or another tool, to edit the `ConfigMap`\. For information about other tools you can use, see [Use tools to make changes to the `aws-auth``ConfigMap`](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#use-tools-to-make-changes-to-the-aws-auth-configmap) in the Amazon EKS best practices guides\. An improperly formatted `aws-auth` `ConfigMap` can cause you to lose access to your cluster\. 

------
#### [ eksctl ]

**Prerequisite**  
Version `0.175.0` or later of the `eksctl` command line tool installed on your device or AWS CloudShell\. To install or update `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.

   1. View the current mappings in the `ConfigMap`\. Replace `my-cluster` with the name of your cluster\. Replace `region-code` with the AWS Region that your cluster is in\.

      ```
      eksctl get iamidentitymapping --cluster my-cluster --region=region-code
      ```

      An example output is as follows\.

      ```
      ARN                                                                                             USERNAME                                GROUPS                          ACCOUNT
      arn:aws:iam::111122223333:role/eksctl-my-cluster-my-nodegroup-NodeInstanceRole-1XLS7754U3ZPA    system:node:{{EC2PrivateDNSName}}       system:bootstrappers,system:nodes
      ```

   1. Add a mapping for a role\. Replace `my-role` with your role name\. Replace `eks-console-dashboard-full-access-group` with the name of the group specified in your Kubernetes `RoleBinding` or `ClusterRoleBinding` object\. Replace `111122223333` with your account ID\. You can replace *admin* with any name you choose\.

      ```
      eksctl create iamidentitymapping --cluster my-cluster --region=region-code \
          --arn arn:aws:iam::111122223333:role/my-role --username admin --group eks-console-dashboard-full-access-group \
          --no-duplicate-arns
      ```
**Important**  
The role ARN can't include a path such as `role/my-team/developers/my-role`\. The format of the ARN must be `arn:aws:iam::111122223333:role/my-role`\. In this example, `my-team/developers/` needs to be removed\.

      An example output is as follows\.

      ```
      [...]
      2022-05-09 14:51:20 [ℹ]  adding identity "arn:aws:iam::111122223333:role/my-role" to auth ConfigMap
      ```

   1. Add a mapping for a user\. [IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html) recommend that you grant permissions to roles instead of users\. Replace `my-user` with your user name\. Replace `eks-console-dashboard-restricted-access-group` with the name of the group specified in your Kubernetes `RoleBinding` or `ClusterRoleBinding` object\. Replace `111122223333` with your account ID\. You can replace *my\-user* with any name you choose\.

      ```
      eksctl create iamidentitymapping --cluster my-cluster --region=region-code \
          --arn arn:aws:iam::111122223333:user/my-user --username my-user --group eks-console-dashboard-restricted-access-group \
          --no-duplicate-arns
      ```

      An example output is as follows\.

      ```
      [...]
      2022-05-09 14:53:48 [ℹ]  adding identity "arn:aws:iam::111122223333:user/my-user" to auth ConfigMap
      ```

   1. View the mappings in the `ConfigMap` again\.

      ```
      eksctl get iamidentitymapping --cluster my-cluster --region=region-code
      ```

      An example output is as follows\.

      ```
      ARN                                                                                             USERNAME                                GROUPS                                  ACCOUNT
      arn:aws:iam::111122223333:role/eksctl-my-cluster-my-nodegroup-NodeInstanceRole-1XLS7754U3ZPA    system:node:{{EC2PrivateDNSName}}       system:bootstrappers,system:nodes
      arn:aws:iam::111122223333:role/admin                                                            my-role                                 eks-console-dashboard-full-access-group
      arn:aws:iam::111122223333:user/my-user                                                          my-user                                 eks-console-dashboard-restricted-access-group
      ```

------
#### [ Edit ConfigMap manually ]

   1. Open the `ConfigMap` for editing\.

      ```
      kubectl edit -n kube-system configmap/aws-auth
      ```
**Note**  
If you receive an error stating "`Error from server (NotFound): configmaps "aws-auth" not found`", then use the procedure in [Apply the `aws-auth`   `ConfigMap` to your cluster](#aws-auth-configmap) to apply the stock `ConfigMap`\.

   1. Add your IAM principals to the `ConfigMap`\. An IAM group isn't an IAM principal, so it can't be added to the `ConfigMap`\.
      + **To add an IAM role \(for example, for [federated users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers.html)\):** Add the role details to the `mapRoles` section of the `ConfigMap`, under `data`\. Add this section if it does not already exist in the file\. Each entry supports the following parameters:
        + **rolearn**: The ARN of the IAM role to add\. This value can't include a path\. For example, you can't specify an ARN such as `arn:aws:iam::111122223333:role/my-team/developers/role-name`\. The ARN needs to be `arn:aws:iam::111122223333:role/role-name` instead\.
        + **username**: The user name within Kubernetes to map to the IAM role\.
        + **groups**: The group or list of Kubernetes groups to map the role to\. The group can be a default group, or a group specified in a `clusterrolebinding` or `rolebinding`\. For more information, see [Default roles and role bindings](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#default-roles-and-role-bindings) in the Kubernetes documentation\.
      + **To add an IAM user:** [IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html) recommend that you grant permissions to roles instead of users\. Add the user details to the `mapUsers` section of the `ConfigMap`, under `data`\. Add this section if it does not already exist in the file\. Each entry supports the following parameters:
        + **userarn**: The ARN of the IAM user to add\.
        + **username**: The user name within Kubernetes to map to the IAM user\.
        + **groups**: The group, or list of Kubernetes groups to map the user to\. The group can be a default group, or a group specified in a `clusterrolebinding` or `rolebinding`\. For more information, see [Default roles and role bindings](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#default-roles-and-role-bindings) in the Kubernetes documentation\.

      For example, the following YAML block contains:
      + A `mapRoles` section that maps the IAM node instance to Kubernetes groups so that nodes can register themselves with the cluster and the `my-console-viewer-role` IAM role that is mapped to a Kubernetes group that can view all Kubernetes resources for all clusters\. For a list of the IAM and Kubernetes group permissions required for the `my-console-viewer-role` IAM role, see [Required permissions](view-kubernetes-resources.md#view-kubernetes-resources-permissions)\.
      + A `mapUsers` section that maps the `admin` IAM user from the default AWS account to the `system:masters` Kubernetes group and the `my-user` user from a different AWS account that is mapped to a Kubernetes group that can view Kubernetes resources for a specific namespace\. For a list of the IAM and Kubernetes group permissions required for the `my-user` IAM user, see [Required permissions](view-kubernetes-resources.md#view-kubernetes-resources-permissions)\.

      Add or remove lines as necessary and replace all *`example values`* with your own values\.

      ```
      # Please edit the object below. Lines beginning with a '#' will be ignored,
      # and an empty file will abort the edit. If an error occurs while saving this file will be
      # reopened with the relevant failures.
      #
      apiVersion: v1
      data:
        mapRoles: |
          - groups:
            - system:bootstrappers
            - system:nodes
            rolearn: arn:aws:iam::111122223333:role/my-role
            username: system:node:{{EC2PrivateDNSName}}
          - groups:
            - eks-console-dashboard-full-access-group
            rolearn: arn:aws:iam::111122223333:role/my-console-viewer-role
            username: my-console-viewer-role
        mapUsers: |
          - groups:
            - system:masters
            userarn: arn:aws:iam::111122223333:user/admin
            username: admin
          - groups:
            - eks-console-dashboard-restricted-access-group      
            userarn: arn:aws:iam::444455556666:user/my-user
            username: my-user
      ```

   1. Save the file and exit your text editor\.

------

## Apply the `aws-auth`   `ConfigMap` to your cluster<a name="aws-auth-configmap"></a>

The `aws-auth` `ConfigMap` is automatically created and applied to your cluster when you create a managed node group or when you create a node group using `eksctl`\. It is initially created to allow nodes to join your cluster, but you also use this `ConfigMap` to add role\-based access control \(RBAC\) access to IAM principals\. If you've launched self\-managed nodes and haven't applied the `aws-auth` `ConfigMap` to your cluster, you can do so with the following procedure\.

**To apply the `aws-auth``ConfigMap` to your cluster**

1. Check to see if you've already applied the `aws-auth` `ConfigMap`\.

   ```
   kubectl describe configmap -n kube-system aws-auth
   ```

   If you receive an error stating "`Error from server (NotFound): configmaps "aws-auth" not found`", then proceed with the following steps to apply the stock `ConfigMap`\.

1. Download, edit, and apply the AWS authenticator configuration map\.

   1. Download the configuration map\.

      ```
      curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/aws-auth-cm.yaml
      ```

   1. In the `aws-auth-cm.yaml` file, set the `rolearn` to the Amazon Resource Name \(ARN\) of the IAM role associated with your nodes\. You can do this with a text editor, or by replacing `my-node-instance-role` and running the following command:

      ```
      sed -i.bak -e 's|<ARN of instance role (not instance profile)>|my-node-instance-role|' aws-auth-cm.yaml
      ```

      Don't modify any other lines in this file\.
**Important**  
The role ARN can't include a path such as `role/my-team/developers/my-role`\. The format of the ARN must be `arn:aws:iam::111122223333:role/my-role`\. In this example, `my-team/developers/` needs to be removed\.

      You can inspect the AWS CloudFormation stack outputs for your node groups and look for the following values:
      + **InstanceRoleARN** – For node groups that were created with `eksctl`
      + **NodeInstanceRole** – For node groups that were created with Amazon EKS vended AWS CloudFormation templates in the AWS Management Console

   1. Apply the configuration\. This command may take a few minutes to finish\.

      ```
      kubectl apply -f aws-auth-cm.yaml
      ```
**Note**  
If you receive any authorization or resource type errors, see [Unauthorized or access denied \(`kubectl`\)](troubleshooting.md#unauthorized) in the troubleshooting topic\.

1. Watch the status of your nodes and wait for them to reach the `Ready` status\.

   ```
   kubectl get nodes --watch
   ```

   Enter `Ctrl`\+`C` to return to a shell prompt\.