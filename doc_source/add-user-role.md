# Managing Users or IAM Roles for your Cluster<a name="add-user-role"></a>

When you create an Amazon EKS cluster, the IAM entity user or role, such as a [federated user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers.html) that creates the cluster, is automatically granted `system:masters` permissions in the cluster's RBAC configuration\. To grant additional AWS users or roles the ability to interact with your cluster, you must edit the `aws-auth` ConfigMap within Kubernetes\. 

**Note**  
For more information about different IAM identities, see [Identities \(Users, Groups, and Roles\)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers.html) in the *IAM User Guide*\. For more information on Kubernetes RBAC configuration, see [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)\. For all ConfigMap settings, see [Full Configuration Format](https://github.com/kubernetes-sigs/aws-iam-authenticator#full-configuration-format) on GitHub\. 

The `aws-auth` ConfigMap is applied as part of the [Getting Started with Amazon EKS](getting-started.md) guide which provides a complete end\-to\-end walkthrough from creating an Amazon EKS cluster to deploying a sample Kubernetes application\. It is initially created to allow your worker nodes to join your cluster, but you also use this ConfigMap to add RBAC access to IAM users and roles\. If you have not launched worker nodes and applied the `aws-auth` ConfigMap, you can do so with the following procedure\.

**To apply the `aws-auth` ConfigMap to your cluster**

1. Check to see if you have already applied the `aws-auth` ConfigMap\.

   ```
   kubectl describe configmap -n kube-system aws-auth
   ```

   If you receive an error stating "`Error from server (NotFound): configmaps "aws-auth" not found`", then proceed with the following steps to apply the stock ConfigMap\.

1. Download, edit, and apply the AWS authenticator configuration map\.

   1. Download the configuration map:

      ```
      curl -o aws-auth-cm.yaml https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-03-23/aws-auth-cm.yaml
      ```

   1. Open the file with your favorite text editor\. Replace the *<ARN of instance role \(not instance profile\)>* snippet with the Amazon Resource Name \(ARN\) of the IAM role that is associated with your worker nodes, and save the file\. You can inspect the AWS CloudFormation stack outputs for your worker node groups and look for the following values:
      + **InstanceRoleARN** \(for worker node groups that were created with `eksctl`\)
      + **NodeInstanceRole** \(for worker node groups that were created with Amazon EKS\-vended AWS CloudFormation templates in the AWS Management Console\)
**Important**  
Do not modify any other lines in this file\.

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

   1. Apply the configuration\. This command may take a few minutes to finish\.

      ```
      kubectl apply -f aws-auth-cm.yaml
      ```
**Note**  
If you receive the error `"aws-iam-authenticator": executable file not found in $PATH`, your kubectl isn't configured for Amazon EKS\. For more information, see [Installing `aws-iam-authenticator`](install-aws-iam-authenticator.md)\.  
If you receive any other authorization or resource type errors, see [Unauthorized or Access Denied \(`kubectl`\)](troubleshooting.md#unauthorized) in the troubleshooting section\.

1. Watch the status of your nodes and wait for them to reach the `Ready` status\.

   ```
   kubectl get nodes --watch
   ```

**To add an IAM user or role to an Amazon EKS cluster**

1. Ensure that the AWS credentials that kubectl is using are already authorized for your cluster\. The IAM user that created the cluster has these permissions by default\.

1. Open the `aws-auth` ConfigMap\.

   ```
   kubectl edit -n kube-system configmap/aws-auth
   ```
**Note**  
If you receive an error stating "`Error from server (NotFound): configmaps "aws-auth" not found`", then use the previous procedure to apply the stock ConfigMap\.

   Example ConfigMap:

   ```
   # Please edit the object below. Lines beginning with a '#' will be ignored,
   # and an empty file will abort the edit. If an error occurs while saving this file will be
   # reopened with the relevant failures.
   #
   apiVersion: v1
   data:
     mapRoles: |
       - rolearn: arn:aws:iam::111122223333:role/doc-test-worker-nodes-NodeInstanceRole-WDO5P42N3ETB
         username: system:node:{{EC2PrivateDNSName}}
         groups:
           - system:bootstrappers
           - system:nodes
   kind: ConfigMap
   metadata:
     annotations:
       kubectl.kubernetes.io/last-applied-configuration: |
         {"apiVersion":"v1","data":{"mapRoles":"- rolearn: arn:aws:iam::111122223333:role/doc-test-worker-nodes-NodeInstanceRole-WDO5P42N3ETB\n  username: system:node:{{EC2PrivateDNSName}}\n  groups:\n    - system:bootstrappers\n    - system:nodes\n"},"kind":"ConfigMap","metadata":{"annotations":{},"name":"aws-auth","namespace":"kube-system"}}
     creationTimestamp: 2018-04-04T18:49:10Z
     name: aws-auth
     namespace: kube-system
     resourceVersion: "780"
     selfLink: /api/v1/namespaces/kube-system/configmaps/aws-auth
     uid: dcc31de5-3838-11e8-af26-02e00430057c
   ```

1. Add your IAM users, roles, or AWS accounts to the configMap\.
   + **To add an IAM user:** add the user details to the `mapUsers` section of the ConfigMap, under `data`\. Add this section if it does not already exist in the file\. Each entry supports the following parameters:
     + **userarn**: The ARN of the IAM user to add\.
     + **username**: The user name within Kubernetes to map to the IAM user\. By default, the user name is the ARN of the IAM user\.
     + **groups**: A list of groups within Kubernetes to which the user is mapped to\. For more information, see [Default Roles and Role Bindings](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#default-roles-and-role-bindings) in the Kubernetes documentation\.
   + **To add an IAM role \(for example, for [federated users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers.html)\):** add the role details to the `mapRoles` section of the ConfigMap, under `data`\. Add this section if it does not already exist in the file\. Each entry supports the following parameters:
     + **rolearn**: The ARN of the IAM role to add\.
     + **username**: The user name within Kubernetes to map to the IAM role\. By default, the user name is the ARN of the IAM role\.
     + **groups**: A list of groups within Kubernetes to which the role is mapped\. For more information, see [Default Roles and Role Bindings](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#default-roles-and-role-bindings) in the Kubernetes documentation\.

   For example, the block below contains:
   + A `mapRoles` section that adds the worker node instance role so that worker nodes can register themselves with the cluster\.
   + A `mapUsers` section with the AWS users `admin` from the default AWS account, and `ops-user` from another AWS account\. Both users are added to the `system:masters` group\.

   ```
   # Please edit the object below. Lines beginning with a '#' will be ignored,
   # and an empty file will abort the edit. If an error occurs while saving this file will be
   # reopened with the relevant failures.
   #
   apiVersion: v1
   data:
     mapRoles: |
       - rolearn: arn:aws:iam::555555555555:role/devel-worker-nodes-NodeInstanceRole-74RF4UBDUKL6
         username: system:node:{{EC2PrivateDNSName}}
         groups:
           - system:bootstrappers
           - system:nodes
     mapUsers: |
       - userarn: arn:aws:iam::555555555555:user/admin
         username: admin
         groups:
           - system:masters
       - userarn: arn:aws:iam::111122223333:user/ops-user
         username: ops-user
         groups:
           - system:masters
   ```

1. Save the file and exit your text editor\.