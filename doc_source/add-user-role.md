# Enabling IAM user and role access to your cluster<a name="add-user-role"></a>

Access to your cluster using AWS IAM entities is enabled by the [AWS IAM Authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator), which runs on the Amazon EKS control plane\. The authenticator gets its configuration information from the `aws-auth` `ConfigMap`\. For all `aws-auth` `ConfigMap` settings, see [Full Configuration Format](https://github.com/kubernetes-sigs/aws-iam-authenticator#full-configuration-format) on GitHub\. 

## Add IAM users or roles to your Amazon EKS cluster<a name="aws-auth-users"></a>

When you create an Amazon EKS cluster, the AWS Identity and Access Management \(IAM\) entity user or role, such as a [federated user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers.html) that creates the cluster, is automatically granted `system:masters` permissions in the cluster's role\-based access control \(RBAC\) configuration in the Amazon EKS control plane\. This IAM entity doesn't appear in any visible configuration, so make sure to keep track of which IAM entity originally created the cluster\. To grant additional AWS users or roles the ability to interact with your cluster, you must edit the `aws-auth` `ConfigMap` within Kubernetes and create a Kubernetes `rolebinding` or `clusterrolebinding` with the name of a `group` that you specify in the `aws-auth` `ConfigMap`\.

**Note**  
For more information about different IAM identities, see [Identities \(Users, Groups, and Roles\)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers.html) in the *IAM User Guide*\. For more information on Kubernetes role\-based access control \(RBAC\) configuration, see [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)\. 

**To add an IAM user or role to an Amazon EKS cluster**

1. Determine which credentials `kubectl` is using to access your cluster\. On your computer, you can see which credentials `kubectl` uses with the following command\. Replace ***\~/\.kube/config*** with the path to your `kubeconfig` file if you don't use the default path\.

   ```
   cat ~/.kube/config
   ```

   Output

   ```
   ...
   contexts:
   - context:
       cluster: my-cluster.region-code.eksctl.io
       user: admin@my-cluster.region-code.eksctl.io
     name: admin@my-cluster.region-code.eksctl.io
   current-context: admin@my-cluster.region-code.eksctl.io
   ...
   ```

   In the previous example output the credentials for a user named *admin* are configured for a cluster named *my\-cluster*\. If this is the user that created the cluster, then it already has access to your cluster\. If it's not the user that created the cluster, then you need to complete the remaining steps to enable cluster access for the user, if you haven't already\.

1. Ensure that you have an existing Kubernetes `role` or `clusterrole` with the permissions \(`rules`\) that you want your IAM users to have access to in your cluster and that you have an existing Kubernetes `rolebinding` or `clusterrolebinding` that binds a Kubernetes `group` to the `role` or `clusterrole`\. For more information, see [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) in the Kubernetes documentation\. You can view all of your existing `roles`, `clusterroles`, `rolebindings`, and `clusterrolebindings` using the following commands\.

   ```
   kubectl get roles --all-namespaces
   ```

   ```
   kubectl get clusterroles --all-namespaces
   ```

   ```
   kubectl get rolebindings --all-namespaces
   ```

   ```
   kubectl get clusterrolebindings --all-namespaces
   ```

   You can then view the details of any of the resources using the following command\. You can replace *role* with **clusterrole**, **rolebinding**, or **clusterrolebinding**, replace *role\-name* with the resource name \(from the previous output\), and replace *kube\-system* with the namespace of the resource \(from the previous output\)\.

   ```
   kubectl describe role role-name -n kube-system
   ```

1. \(Optional\) Create a `clusterrole` and `clusterrolebinding` or `role` and `rolebinding` to enable IAM users to view [nodes](view-nodes.md) and [workloads](view-workloads.md) in the AWS Management Console\.

   1.  You can enable users to view Kubernetes resources for:
      + **The cluster** – This manifest creates a `clusterrole` and `clusterrolebinding`\. The group name in the file is `eks-console-dashboard-full-access-group`, which is the group that your IAM user or role needs to be mapped to in the `aws-auth` `ConfigMap`\. You can change the name of the `group` before applying it to your cluster, if desired, and then map your IAM user or role to that group in the `ConfigMap`\.

        ```
        curl -o eks-console-full-access.yaml https://amazon-eks.s3.us-west-2.amazonaws.com/docs/eks-console-full-access.yaml
        ```
      + **A specific namespace** – This manifest creates a `role` and `rolebinding`\. The namespace in this file is `default`, so if you want to specify a different namespace, edit the file before applying it to your cluster\. The group name in the file is `eks-console-dashboard-restricted-access-group`, which is the group that your IAM user or role needs to be mapped to in the `aws-auth` `ConfigMap`\. You can change the name of the group before applying it to your cluster, if desired, and then map your IAM user or role to that group in the configmap\.

        ```
        curl -o eks-console-restricted-access.yaml https://amazon-eks.s3.us-west-2.amazonaws.com/docs/eks-console-restricted-access.yaml
        ```

   1. Apply the appropriate manifest using one of the following commands\.

      ```
      kubectl apply -f eks-console-full-access.yaml
      ```

      ```
      kubectl apply -f eks-console-restricted-access.yaml
      ```

1. Edit the `aws-auth` `ConfigMap`\.

   1. Open the `ConfigMap` for editing\.

      ```
      kubectl edit -n kube-system configmap/aws-auth
      ```
**Note**  
If you receive an error stating "`Error from server (NotFound): configmaps "aws-auth" not found`", then use the procedure in [Apply the `aws-auth` ConfigMap to your cluster](#aws-auth-configmap) to apply the stock `ConfigMap`\.

   1. Add your IAM users, roles, or AWS accounts to the `ConfigMap`\. You cannot add IAM groups to the `ConfigMap`\.
      + **To add an IAM role \(for example, for [federated users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers.html)\):** Add the role details to the `mapRoles` section of the `ConfigMap`, under `data`\. Add this section if it does not already exist in the file\. Each entry supports the following parameters:
        + **rolearn**: The ARN of the IAM role to add\. This value can't include a path\. The format of the value you provide must be `arn:aws:iam::111122223333:role/role-name`\. For more information, see [aws\-auth ConfigMap does not grant access to the cluster](troubleshooting_iam.md#security-iam-troubleshoot-ConfigMap)\.
        + **username**: The user name within Kubernetes to map to the IAM role\.
        + **groups**: A list of groups within Kubernetes to which the role is mapped\. For more information, see [Default Roles and Role Bindings](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#default-roles-and-role-bindings) in the Kubernetes documentation\.
      + **To add an IAM user:** Add the user details to the `mapUsers` section of the ConfigMap, under `data`\. Add this section if it does not already exist in the file\. Each entry supports the following parameters:
        + **userarn**: The ARN of the IAM user to add\.
        + **username**: The user name within Kubernetes to map to the IAM user\.
        + **groups**: A list of groups within Kubernetes to which the user is mapped to\. For more information, see [Default Roles and Role Bindings](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#default-roles-and-role-bindings) in the Kubernetes documentation\.

      For example, the block below contains:
      + A `mapRoles` section that adds the node instance role so that nodes can register themselves with the cluster\.
      + A `mapUsers` section with the AWS users `admin` from the default AWS account, and two operations users from a different AWS account\. The `admin` user is added to the `system:masters` Kubernetes group\.

        The operations users are added to Kubernetes groups that are used by the `role` and `rolebinding` and `clusterrole` and `clusterrolebinding` created by the manifests in the previous step, but you can replace them with whatever group you like\. To enable users to view [nodes](view-nodes.md) and [workloads](view-workloads.md) in the AWS Management Console, they must have the mapping in the following example and the `role` and `rolebinding` or the `clusterrole` and `clusterrolebinding` created by the manifests in the previous step\.

      Replace all *`example-values`* with your own values\.

      ```
      # Please edit the object below. Lines beginning with a '#' will be ignored,
      # and an empty file will abort the edit. If an error occurs while saving this file will be
      # reopened with the relevant failures.
      #
      apiVersion: v1
      data:
        mapRoles: |
          - rolearn: arn:aws:iam::111122223333:role/eksctl-my-cluster-nodegroup-standard-wo-NodeInstanceRole-1WP3NUE3O6UCF
            username: system:node:{{EC2PrivateDNSName}}
            groups:
              - system:bootstrappers
              - system:nodes
        mapUsers: |
          - userarn: arn:aws:iam::111122223333:user/admin
            username: admin
            groups:
              - system:masters
          - userarn: arn:aws:iam::444455556666:user/ops-user
            username: ops-user
            groups:
              - eks-console-dashboard-full-access-group
          - userarn: arn:aws:iam::444455556666:user/ops-user2
            username: ops-user2
            groups:
              - eks-console-dashboard-restricted-access-group
      ```

   1. Save the file and exit your text editor\.

## Apply the `aws-auth` ConfigMap to your cluster<a name="aws-auth-configmap"></a>

The `aws-auth` `ConfigMap` is automatically created and applied to your cluster when you create a managed node group or when you create a node group using `eksctl`\. It is initially created to allow nodes to join your cluster, but you also use this `ConfigMap` to add role\-based access control \(RBAC\) access to IAM users and roles\. If you have not launched self\-managed nodes and applied the `aws-auth` `ConfigMap` to your cluster, you can do so with the following procedure\.

**To apply the `aws-auth` `ConfigMap` to your cluster**

1. Check to see if you have already applied the `aws-auth` `ConfigMap`\.

   ```
   kubectl describe configmap -n kube-system aws-auth
   ```

   If you receive an error stating "`Error from server (NotFound): configmaps "aws-auth" not found`", then proceed with the following steps to apply the stock `ConfigMap`\.

1. Download, edit, and apply the AWS authenticator configuration map\.

   1. Download the configuration map\.

      ```
      curl -o aws-auth-cm.yaml https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-10-29/aws-auth-cm.yaml
      ```

   1. Open the file with a text editor\. Replace `<ARN of instance role (not instance profile)>` with the Amazon Resource Name \(ARN\) of the IAM role associated with your nodes, and save the file\. Do not modify any other lines in this file\.
**Important**  
The role ARN cannot include a path\. The format of the role ARN must be `arn:aws:iam::111122223333:role/role-name`\. For more information, see [aws\-auth ConfigMap does not grant access to the cluster](troubleshooting_iam.md#security-iam-troubleshoot-ConfigMap)\.

      ```
      apiVersion: v1
      kind: ConfigMap
      metadata:
        name: aws-auth
        namespace: kube-system
      data:
        mapRoles: |
          - rolearn: <ARN of instance role (not instance profile)>
            username: system:node:{{EC2PrivateDNSName}}
            groups:
              - system:bootstrappers
              - system:nodes
      ```

      You can inspect the AWS CloudFormation stack outputs for your node groups and look for the following values:
      + **InstanceRoleARN** – For node groups that were created with `eksctl`
      + **NodeInstanceRole** – For node groups that were created with Amazon EKS vended AWS CloudFormation templates in the AWS Management Console

   1. Apply the configuration\. This command may take a few minutes to finish\.

      ```
      kubectl apply -f aws-auth-cm.yaml
      ```
**Note**  
If you receive any authorization or resource type errors, see [Unauthorized or access denied \(`kubectl`\)](troubleshooting.md#unauthorized) in the troubleshooting section\.

1. Watch the status of your nodes and wait for them to reach the `Ready` status\.

   ```
   kubectl get nodes --watch
   ```