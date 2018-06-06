# Adding Users or IAM Roles to your Cluster<a name="add-user-role"></a>

When you create an Amazon EKS cluster, the IAM entity \(user or role\) is automatically granted `system:master` permissions in the cluster's RBAC configuration\. To grant additional AWS users the ability to interact with your cluster, you must edit the `aws-auth` ConfigMap within Kubernetes\.

**To add an IAM user or role to an Amazon EKS cluster**

1. Ensure that the AWS credentials that kubectl is using are already authorized for your cluster\. The IAM user that created the cluster has these permissions by default\.

1. Open the `aws-auth` ConfigMap\.

   ```
   kubectl edit -n kube-system configmap/aws-auth
   ```
**Note**  
If your default text editor does not wait for you to finish editing before returning to the command prompt, you see the following error:  

   ```
   Edit cancelled, no changes made.
   ```
You can switch your default text editor to a different editor, such as vim, or you can configure your default editor to wait until you are finished editing the file\.

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
     + **groups**: A list of groups within Kubernetes to which the user is mapped to\.
   + **To add an IAM role:** add the role details to the `mapRoles` section of the ConfigMap, under `data`\. Add this section if it does not already exist in the file\. Each entry supports the following parameters:
     + **rolearn**: The ARN of the IAM role to add\.
     + **username**: The user name within Kubernetes to map to the IAM role\. By default, the user name is the ARN of the IAM role\.
     + **groups**: A list of groups within Kubernetes to which the role is mapped\.
   + **To add an AWS account to be auto\-mapped:** add the AWS account ID \(enclosed in quotation marks\) to the `mapAccounts` section of the ConfigMap, under `data`\. Add this section if it does not already exist in the file\. Every AWS user and AWS role in that account is automatically mapped to a user in the Kubernetes cluster with the Amazon Resource Name \(ARN\) of that user or role as the `username`\. However, no permissions are provided in RBAC by this action alone; you must still create role bindings in your cluster to provide these entities permissions\.

   For example, the block below contains:
   + A `mapRoles` section that adds the worker node instance role so that worker nodes can register themselves with the cluster\.
   + A `mapUsers` section with the AWS users `admin` from the default AWS account, and `ops-user` from another AWS account\. Both users are added to the `system:masters` group\.
   + A `mapAccounts` section with the AWS account, *111122223333*\.

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
     mapAccounts: |
       - "111122223333"
   ```

1. Save the file and exit your text editor\.