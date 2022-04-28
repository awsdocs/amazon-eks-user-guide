# View Kubernetes resources<a name="view-kubernetes-resources"></a>

You can view details about the nodes and several types of Kubernetes workloads deployed to your cluster with the AWS Management Console\. You can't view these resources with the AWS CLI or [`eksctl`](eksctl.md)\. To view Kubernetes resources using a command\-line tool, use [`kubectl`](install-kubectl.md)\.

**Prerequisite**  
To view the **Overview** and **Workloads** tabs in the AWS Management Console, the user that you're signed into the AWS Management Console as, or the role that you switch to once you're signed in, must have specific IAM and Kubernetes permissions\. For more information, see [Required permissions](#view-kubernetes-resources-permissions)\.

**To view Kubernetes resources with the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the **Clusters** list, select the cluster that contains the Kubernetes resources that you want to view\.

1. Select the **Overview** tab\. You see a list of all **Nodes** in your cluster\. The nodes can be any [Amazon EKS node type](eks-compute.md)\. Select a node from the list\. You see a **Pods** section\. This section shows you all pods running on the node\. You can select any pod listed to view information about the pod\.

1. Select the **Workloads** tab\. You see a list of the workloads running on your cluster\. Not all Kubernetes workload types are listed\. Select a workload from the list\. You see a **Pods** section\. All pods managed by this workload are listed\.

## Required permissions<a name="view-kubernetes-resources-permissions"></a>

To view the **Overview** and **Workloads** tabs in the AWS Management Console, the user that you're signed into the AWS Management Console as, or the role that you switch to once you're signed in, must have specific minimum IAM and Kubernetes permissions\. Complete the following steps to assign the required permissions to your users and roles\.

1. Make sure that the `eks:AccessKubernetesApi`, and other permissions to view necessary AWS resources with, are assigned to either the user that you sign into the AWS Management Console with, or the role that you switch to once you've signed in to the console\. For more information about how to edit permissions for a user, see [Changing permissions for a user \(console\)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_change-permissions.html#users_change_permissions-change-console) in the IAM User Guide\.

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
      curl-o eks-console-full-access.yaml https://s3.us-west-2.amazonaws.com/amazon-eks/docs/eks-console-full-access.yaml
      ```

      ```
      curl-o eks-console-restricted-access.yaml https://s3.us-west-2.amazonaws.com/amazon-eks/docs/eks-console-restricted-access.yaml
      ```

   1. Edit the file as necessary\.

   1. Apply the manifest to your cluster with one of the following commands:

      ```
      kubectl apply -f eks-console-full-access.yaml
      ```

      ```
      kubectl apply -f eks-console-restricted-access.yaml
      ```

1. Map the IAM user or role to the Kubernetes user or group in the `aws-auth` `ConfigMap`\. For more information about adding users or roles to the `aws-auth` `ConfigMap`, see [Add IAM users, roles, or AWS accounts to the `ConfigMap`](add-user-role.md#aws-auth-users)\. 

   1. Open the `ConfigMap` for editing\.

      ```
      kubectl edit -n kube-system configmap/aws-auth
      ```

   1. Add the mappings\. The following example adds the following mappings between IAM users and roles with permissions added in the first step and the Kubernetes groups created in the previous step:
      + The *my\-console\-viewer\-role* role and the `eks-console-dashboard-full-access-group`\.
      + The *my\-user* IAM user and the `eks-console-dashboard-restricted-access-group`\.

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

   1. Save the file and exit the editor\.