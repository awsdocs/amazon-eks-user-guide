# View Kubernetes resources<a name="view-kubernetes-resources"></a>

You can view the Kubernetes resources deployed to your cluster with the AWS Management Console\. You can't view Kubernetes resources with the AWS CLI or [`eksctl`](eksctl.md)\. To view Kubernetes resources using a command\-line tool, use [`kubectl`](install-kubectl.md)\.

**Prerequisite**  
To view the **Overview** and **Resources** tabs in the AWS Management Console, the user that you're signed into the AWS Management Console as, or the role that you switch to once you're signed in, must have specific IAM and Kubernetes permissions\. For more information, see [Required permissions](#view-kubernetes-resources-permissions)\.

**To view Kubernetes resources with the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the **Clusters** list, select the cluster that contains the Kubernetes resources that you want to view\.

1. Select the **Resources** tab\.

1. Select a **Resource type** group that you want to view resources for, such as **Workloads**\. You see a list of resource types in that group\.

1. Select a resource type, such as **Deployments**, in the **Workloads** group\. You see a description of the resource type, a link to the Kubernetes documentation for more information about the resource type, and a list of resources of that type that are deployed on your cluster\. If the list is empty, then there are no resources of that type deployed to your cluster\.

1. Select a resource to view more information about it\. Try the following examples:
   + Select the **Workloads** group, select the **Deployments** resource type, and then select the **coredns** resource\. When you select a resource, you are in **Structured view**, by default\. For some resource types, you see a **Pods** section in **Structured view**\. This section lists the pods managed by the workload\. You can select any pod listed to view information about the pod\. Not all resource types display information in **Structured View**\. If you select **Raw view** in the top right corner of the page for the resource, you see the complete JSON response from the Kubernetes API for the resource\.
   + Select the **Cluster** group and then select the **Nodes** resource type\. You see a list of all nodes in your cluster\. The nodes can be any [Amazon EKS node type](eks-compute.md)\. This is the same list that you see in the **Nodes** section when you select the **Overview** tab for your cluster\. Select a node resource from the list\. In **Structured view**, you also see a **Pods** section\. This section shows you all pods running on the node\.

## Required permissions<a name="view-kubernetes-resources-permissions"></a>

To view the **Overview** and **Resources** tabs in the AWS Management Console, the user that you're signed into the AWS Management Console as, or the role that you switch to once you're signed in, must have specific minimum IAM and Kubernetes permissions\. Complete the following steps to assign the required permissions to your users and roles\.

1. Make sure that the `eks:AccessKubernetesApi`, and other necessary IAM permissions to view Kubernetes resources, are assigned to either the user that you sign into the AWS Management Console with, or the role that you switch to once you've signed in to the console\. For more information about how to edit permissions for a user, see [Changing permissions for a user \(console\)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_change-permissions.html#users_change_permissions-change-console) in the IAM User Guide\. For more information about how to edit permissions for a role, see [Modifying a role permissions policy \(console\)](https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-managingrole-editing-console.html#roles-modify_permissions-policy) in the IAM User Guide\.

   The following example policy includes the necessary permissions for a user or role to view Kubernetes resources for all clusters in your account\. Replace *111122223333* with your account ID\. 

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

   To view nodes in connected clusters, the [Amazon EKS connector IAM role](connector_IAM_role.md) should be able to impersonate the IAM user or role in the cluster\. This allows the [Amazon EKS Connector](eks-connector.md) to map the IAM user or role to a Kubernetes user\.

1. Create a Kubernetes `rolebinding` or `clusterrolebinding` that is bound to a Kubernetes `role` or `clusterrole` that has the necessary permissions to view the Kubernetes resources\. To learn more about Kubernetes roles and role bindings, see [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) in the Kubernetes documentation\. You can apply one of the following manifests to your cluster that create a `role` and `rolebinding` or a `clusterrole` and `clusterrolebinding` with the necessary Kubernetes permissions:
   + **View Kubernetes resources in all namespaces** – The group name in the file is `eks-console-dashboard-full-access-group`\. Apply the manifest to your cluster with the following command:

     ```
     kubectl apply -f https://s3.us-west-2.amazonaws.com/amazon-eks/docs/eks-console-full-access.yaml
     ```
   + **View Kubernetes resources in a specific namespace** – The namespace in this file is `default`\. The group name in the file is `eks-console-dashboard-restricted-access-group`\. Apply the manifest to your cluster with the following command:

     ```
     kubectl apply -f https://s3.us-west-2.amazonaws.com/amazon-eks/docs/eks-console-restricted-access.yaml
     ```

   If you need to change the Kubernetes group name, namespace, permissions, or any other configuration in the file, then download the file and edit it before applying it to your cluster:

   1. Download the file with one of the following commands:

      ```
      curl -o eks-console-full-access.yaml https://s3.us-west-2.amazonaws.com/amazon-eks/docs/eks-console-full-access.yaml
      ```

      ```
      curl -o eks-console-restricted-access.yaml https://s3.us-west-2.amazonaws.com/amazon-eks/docs/eks-console-restricted-access.yaml
      ```

   1. Edit the file as necessary\.

   1. Apply the manifest to your cluster with one of the following commands:

      ```
      kubectl apply -f eks-console-full-access.yaml
      ```

      ```
      kubectl apply -f eks-console-restricted-access.yaml
      ```

1. Map the IAM user or role to the Kubernetes user or group in the `aws-auth` `ConfigMap`\. You can use a tool such as `eksctl` to update the `ConfigMap` or you can update it manually by editing it\.
**Important**  
We recommend using `eksctl`, or another tool, to edit the `ConfigMap`\. For information about other tools you can use, see [Use tools to make changes to the `aws-auth``ConfigMap`](https://aws.github.io/aws-eks-best-practices/security/docs/iam/#use-tools-to-make-changes-to-the-aws-auth-configmap) in the Amazon EKS best practices guides\. An improperly formatted `aws-auth` `ConfigMap` can cause you to lose access to your cluster\. 

------
#### [ eksctl ]

**Prerequisite**  
Version 0\.99\.0 or later of the `eksctl` command line tool installed on your computer or AWS CloudShell\. To install or update `eksctl`, see [Installing `eksctl`](eksctl.md)\.

   1. View the current mappings in the `ConfigMap`\. Replace *my\-cluster* with the name of your cluster\. Replace *region\-code* with the AWS Region that your cluster is in\.

      ```
      eksctl get iamidentitymapping --cluster my-cluster --region=region-code
      ```

      Example output:

      ```
      ARN                                                                                             USERNAME                                GROUPS                          ACCOUNT
      arn:aws:iam::111122223333:role/eksctl-my-cluster-my-nodegroup-NodeInstanceRole-1XLS7754U3ZPA    system:node:{{EC2PrivateDNSName}}       system:bootstrappers,system:nodes
      ```

   1. Add a mapping for a role\. This example assume that you attached the IAM permissions in the first step to a role named *my\-console\-viewer\-role*\. Replace *111122223333* with your account ID\.

      ```
      eksctl create iamidentitymapping \
          --cluster my-cluster \
          --region=region-code \
          --arn arn:aws:iam::111122223333:role/my-console-viewer-role \
          --group eks-console-dashboard-full-access-group \
          --no-duplicate-arns
      ```
**Important**  
The role ARN can't include a path such as `role/my-team/developers/my-role`\. The format of the ARN must be `arn:aws:iam::111122223333:role/my-role`\. In this example, `my-team/developers/` needs to be removed\.

      Example output:

      ```
      ...
      2022-05-09 14:51:20 [ℹ]  adding identity "arn:aws:iam::111122223333:role/my-console-viewer-role" to auth ConfigMap
      ```

   1. Add a mapping for a user\. This example assume that you attached the IAM permissions in the first step to a user named *my\-user*\. Replace *111122223333* with your account ID\.

      ```
      eksctl create iamidentitymapping \
          --cluster my-cluster \
          --region=region-code \
          --arn arn:aws:iam::111122223333:user/my-user \
          --group eks-console-dashboard-restricted-access-group \
          --no-duplicate-arns
      ```

      Example output:

      ```
      ...
      2022-05-09 14:53:48 [ℹ]  adding identity "arn:aws:iam::111122223333:user/my-user" to auth ConfigMap
      ```

   1. View the mappings in the `ConfigMap` again\.

      ```
      eksctl get iamidentitymapping --cluster my-cluster --region=region-code
      ```

      Example output:

      ```
      ARN                                                                                             USERNAME                                GROUPS                                  ACCOUNT
      arn:aws:iam::111122223333:role/eksctl-my-cluster-my-nodegroup-NodeInstanceRole-1XLS7754U3ZPA    system:node:{{EC2PrivateDNSName}}       system:bootstrappers,system:nodes
      arn:aws:iam::111122223333:role/my-console-viewer-role                                                                                   eks-console-dashboard-full-access-group
      arn:aws:iam::111122223333:user/my-user                                                                                                  eks-console-dashboard-restricted-access-group
      ```

------
#### [ Edit ConfigMap manually ]

    For more information about adding users or roles to the `aws-auth` `ConfigMap`, see [Add IAM users, roles, or AWS accounts to the `ConfigMap`](add-user-role.md#aws-auth-users)\. 

   1. Open the `ConfigMap` for editing\.

      ```
      kubectl edit -n kube-system configmap/aws-auth
      ```

   1. Add the mappings to the `aws-auth` `ConfigMap`, but don't replace any of the existing mappings\. The following example adds mappings between IAM users and roles with permissions added in the first step and the Kubernetes groups created in the previous step:
      + The *my\-console\-viewer\-role* role and the `eks-console-dashboard-full-access-group`\.
      + The *my\-user* user and the `eks-console-dashboard-restricted-access-group`\.

      These examples assume that you attached the IAM permissions in the first step to a role named *my\-console\-viewer\-role* and a user named *my\-user*\. Replace *111122223333* with your account ID\.

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
**Important**  
The role ARN can't include a path such as `role/my-team/developers/my-console-viewer-role`\. The format of the ARN must be `arn:aws:iam::111122223333:role/my-console-viewer-role`\. In this example, `my-team/developers/` needs to be removed\.

   1. Save the file and exit the editor\.

------