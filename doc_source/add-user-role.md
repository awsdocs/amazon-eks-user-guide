# Managing users or IAM roles for your cluster<a name="add-user-role"></a>

When you create an Amazon EKS cluster, the IAM entity user or role, such as a [federated user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers.html) that creates the cluster, is automatically granted `system:masters` permissions in the cluster's RBAC configuration in the control plane\. This IAM entity does not appear in the ConfigMap, or any other visible configuration, so make sure to keep track of which IAM entity originally created the cluster\. To grant additional AWS users or roles the ability to interact with your cluster, you must edit the `aws-auth` ConfigMap within Kubernetes\. 

**Note**  
For more information about different IAM identities, see [Identities \(Users, Groups, and Roles\)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers.html) in the *IAM User Guide*\. For more information on Kubernetes RBAC configuration, see [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)\. For all ConfigMap settings, see [Full Configuration Format](https://github.com/kubernetes-sigs/aws-iam-authenticator#full-configuration-format) on GitHub\. 

The `aws-auth` ConfigMap is applied as part of the [Getting started with Amazon EKS](getting-started.md) guide which provides a complete end\-to\-end walkthrough from creating an Amazon EKS cluster to deploying a sample Kubernetes application\. It is initially created to allow your nodes to join your cluster, but you also use this ConfigMap to add RBAC access to IAM users and roles\. If you have not launched nodes and applied the `aws-auth` ConfigMap, you can do so with the following procedure\.

**To apply the `aws-auth` ConfigMap to your cluster**

1. Check to see if you have already applied the `aws-auth` ConfigMap\.

   ```
   kubectl describe configmap -n kube-system aws-auth
   ```

   If you receive an error stating "`Error from server (NotFound): configmaps "aws-auth" not found`", then proceed with the following steps to apply the stock ConfigMap\.

1. Download, edit, and apply the AWS authenticator configuration map\.

   1. Download the configuration map\.

      ```
      curl -o aws-auth-cm.yaml https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/aws-auth-cm.yaml
      ```

   1. Open the file with your favorite text editor\. Replace `<ARN of instance role (not instance profile)>` with the Amazon Resource Name \(ARN\) of the IAM role associated with your nodes, and save the file\. Do not modify any other lines in this file\.
**Important**  
The role ARN cannot include a path\. The format of the role ARN must be `arn:aws:iam::<123456789012>:role/<role-name>`\. For more information, see [aws\-auth ConfigMap does not grant access to the cluster](troubleshooting_iam.md#security-iam-troubleshoot-ConfigMap)\.

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

      You can inspect the AWS CloudFormation stack outputs for your worker node groups and look for the following values:
      + **InstanceRoleARN** \(for node groups that were created with `eksctl`\)
      + **NodeInstanceRole** \(for node groups that were created with Amazon EKS vended AWS CloudFormation templates in the AWS Management Console\)

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

**To add an IAM user or role to an Amazon EKS cluster**

1. Ensure that the AWS credentials that `kubectl` is using are already authorized for your cluster\. The IAM user that created the cluster has these permissions by default\.

1. Open the `aws-auth` ConfigMap\.

   ```
   kubectl edit -n kube-system configmap/aws-auth
   ```
**Note**  
If you receive an error stating "`Error from server (NotFound): configmaps "aws-auth" not found`", then use the previous procedure to apply the stock ConfigMap\.

   Example ConfigMap:

   ```
   apiVersion: v1
   data:
     mapRoles: |
       - groups:
         - system:bootstrappers
         - system:nodes
         rolearn: arn:aws:iam::111122223333:role/eksctl-my-cluster-nodegroup-standard-wo-NodeInstanceRole-1WP3NUE3O6UCF
         username: system:node:{{EC2PrivateDNSName}}
   kind: ConfigMap
   metadata:
     creationTimestamp: "2020-09-30T21:09:18Z"
     name: aws-auth
     namespace: kube-system
     resourceVersion: "1021"
     selfLink: /api/v1/namespaces/kube-system/configmaps/aws-auth
     uid: dcc31de5-3838-11e8-af26-02e00430057c
   ```

1. Add your IAM users, roles, or AWS accounts to the configMap\. You cannot add IAM groups to the configMap\.
   + **To add an IAM role \(for example, for [federated users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers.html)\):** add the role details to the `mapRoles` section of the ConfigMap, under `data`\. Add this section if it does not already exist in the file\. Each entry supports the following parameters:
     + **rolearn**: The ARN of the IAM role to add\.
     + **username**: The user name within Kubernetes to map to the IAM role\.
     + **groups**: A list of groups within Kubernetes to which the role is mapped\. For more information, see [Default Roles and Role Bindings](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#default-roles-and-role-bindings) in the Kubernetes documentation\.
   + **To add an IAM user:** add the user details to the `mapUsers` section of the ConfigMap, under `data`\. Add this section if it does not already exist in the file\. Each entry supports the following parameters:
     + **userarn**: The ARN of the IAM user to add\.
     + **username**: The user name within Kubernetes to map to the IAM user\.
     + **groups**: A list of groups within Kubernetes to which the user is mapped to\. For more information, see [Default Roles and Role Bindings](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#default-roles-and-role-bindings) in the Kubernetes documentation\.

   For example, the block below contains:
   + A `mapRoles` section that adds the node instance role so that nodes can register themselves with the cluster\.
   + A `mapUsers` section with the AWS users `admin` from the default AWS account, and `ops-user` from another AWS account\. Both users are added to the `system:masters` group\.

   Replace all `<example-values>` \(including `<>`\) with your own values\.

   ```
   # Please edit the object below. Lines beginning with a '#' will be ignored,
   # and an empty file will abort the edit. If an error occurs while saving this file will be
   # reopened with the relevant failures.
   #
   apiVersion: v1
   data:
     mapRoles: |
       - rolearn: <arn:aws:iam::111122223333:role/eksctl-my-cluster-nodegroup-standard-wo-NodeInstanceRole-1WP3NUE3O6UCF>
         username: <system:node:{{EC2PrivateDNSName}}>
         groups:
           - <system:bootstrappers>
           - <system:nodes>
     mapUsers: |
       - userarn: <arn:aws:iam::111122223333:user/admin>
         username: <admin>
         groups:
           - <system:masters>
       - userarn: <arn:aws:iam::111122223333:user/ops-user>
         username: <ops-user>
         groups:
           - <system:masters>
   ```

1. Save the file and exit your text editor\.

1. Ensure that the Kubernetes user or group that you mapped the IAM user or role to is bound to a Kubernetes role with a `RoleBinding` or `ClusterRoleBinding`\. For more information, see [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) in the Kubernetes documentation\. You can download the following example manifests that create a `clusterrole` and `clusterrolebinding` or a `role` and `rolebinding`:
   + **View Kubernetes resources in all namespaces** – The group name in the file is `eks-console-dashboard-full-access-group`, which is the group that your IAM user or role needs to be mapped to in the `aws-auth` configmap\. You can change the name of the group before applying it to your cluster, if desired, and then map your IAM user or role to that group in the configmap\. Download the file from:

     ```
     https://s3.us-west-2.amazonaws.com/amazon-eks/docs/eks-console-full-access.yaml
     ```
   + **View Kubernetes resources in a specific namespace** – The namespace in this file is `default`, so if you want to specify a different namespace, edit the file before applying it to your cluster\. The group name in the file is `eks-console-dashboard-restricted-access-group`, which is the group that your IAM user or role needs to be mapped to in the `aws-auth` configmap\. You can change the name of the group before applying it to your cluster, if desired, and then map your IAM user or role to that group in the configmap\. Download the file from:

     ```
     https://s3.us-west-2.amazonaws.com/amazon-eks/docs/eks-console-restricted-access.yaml
     ```

1. \(Optional\) If you want the users you've added to the configmap to be able to [View nodes](view-nodes.md) or [View workloads](view-workloads.md) in the AWS Management Console, then the user or role must have both of the the following types of permissions:
   + Kubernetes permissions to view the resources in Kubernetes
   + IAM permissions to view the resources in the AWS Management Console\. For more information, see [View nodes and workloads for all clusters in the AWS Management Console](security_iam_id-based-policy-examples.md#policy_example3)\.