--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Enabling IAM principal access to your cluster<a name="auth-configmap"></a>

**Important**  

Access to your cluster using [IAM principals](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) is enabled by the [AWS IAM Authenticator for Kubernetes](https://github.com/kubernetes-sigs/aws-iam-authenticator#readme), which runs on the Amazon EKS control plane\. The authenticator gets its configuration information from the `aws\-auth``ConfigMap`\. For all `aws\-auth``ConfigMap` settings, see [Full Configuration Format](https://github.com/kubernetes-sigs/aws-iam-authenticator#full-configuration-format) on GitHub\.

## Add IAM principals to your Amazon EKS cluster<a name="aws-auth-users"></a>

When you create an Amazon EKS cluster, the [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) that creates the cluster is automatically granted `system:masters` permissions in the cluster’s role\-based access control \(RBAC\) configuration in the Amazon EKS control plane\. This principal doesn’t appear in any visible configuration, so make sure to keep track of which principal originally created the cluster\. To grant additional IAM principals the ability to interact with your cluster, edit the `aws-auth`ConfigMap within Kubernetes and create a Kubernetes rolebinding or `clusterrolebinding` with the name of a `group` that you specify in the `aws\-auth``ConfigMap`\.

**Note**  
For more information about Kubernetes role\-based access control \(RBAC\) configuration, see [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) in the Kubernetes documentation\.

1. Determine which credentials `kubectl` is using to access your cluster\. On your computer, you can see which credentials `kubectl` uses with the following command\. Replace ` ~/.kube/config ` with the path to your `kubeconfig` file if you don’t use the default path\.

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

   In the previous example output, the credentials for a user named ` admin ` are configured for a cluster named `[replaceable]`my\-cluster````\. If this is the user that created the cluster, then it already has access to your cluster\. If it’s not the user that created the cluster, then you need to complete the remaining steps to enable cluster access for other IAM principals\. [IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html) recommend that you grant permissions to roles instead of users\. You can see which other principals currently have access to your cluster with the following command:

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
   ```
   + groups:
   + system:bootstrappers
   + system:nodes rolearn: arn:aws:iam::111122223333:role/my\-node\-role username: system:node:\{\{EC2PrivateDNSName\}\}

BinaryData

**Example**  
Events: <none>  

```
+

The previous example is a default  `aws-auth```ConfigMap``. Only the node instance role has access to the cluster.
. Make sure that you have existing [noloc]``Kubernetes````roles`` and `rolebindings` or `clusterroles` and `clusterrolebindings` that you can map IAM principals to. For more information about these resources, see https://kubernetes.io/docs/reference/access-authn-authz/rbac/[Using RBAC Authorization] in the [noloc]``Kubernetes`` documentation.
+
.. View your existing [noloc]``Kubernetes````roles`` or ``clusterroles``. `Roles` are scoped to a ``namespace``, but `clusterroles` are scoped to the cluster.
+
[source,bash]
```
kubectl get roles \-A  

```
[source,bash]
```
kubectl get clusterroles  

```
.. View the details of any `role` or `clusterrole` returned in the previous output and confirm that it has the permissions (``rules``) that you want your IAM principals to have in your cluster.
+

Replace `[replaceable]``role-name``` with a `role` name returned in the output from the previous command. Replace `[replaceable]``kube-system``` with the namespace of the ``role``.
+
[source,bash]
```
kubectl describe role role\-name \-n kube\-system  

```
+

Replace  `[replaceable]``cluster-role-name``` with a `clusterrole` name returned in the output from the previous command.
+
[source,bash]
```
kubectl describe clusterrole cluster\-role\-name  

```
.. View your existing [noloc]``Kubernetes````rolebindings`` or ``clusterrolebindings``. `Rolebindings` are scoped to a ``namespace``, but `clusterrolebindings` are scoped to the cluster.
+
[source,bash]
```
kubectl get rolebindings \-A  

```
[source,bash]
```
kubectl get clusterrolebindings  

```
.. View the details of any `rolebinding` or `clusterrolebinding` and confirm that it has a `role` or `clusterrole` from the previous step listed as a `roleRef` and a group name listed for ``subjects``.
+

Replace `[replaceable]``role-binding-name``` with a `rolebinding` name returned in the output from the previous command. Replace `[replaceable]``kube-system``` with the `namespace` of the ``rolebinding``.
+
[source,bash]
```
kubectl describe rolebinding role\-binding\-name \-n kube\-system  

```
+

An example output is as follows.
+
[source,yaml]
```
apiVersion: rbac\.authorization\.k8s\.io/v1 kind: RoleBinding metadata: name: eks\-console\-dashboard\-restricted\-access\-role\-binding namespace: default subjects: \- kind: Group name: eks\-console\-dashboard\-restricted\-access\-group apiGroup: rbac\.authorization\.k8s\.io roleRef: kind: Role name: eks\-console\-dashboard\-restricted\-access\-role apiGroup: rbac\.authorization\.k8s\.io  

```
+

Replace  `[replaceable]``cluster-role-binding-name``` with a `clusterrolebinding` name returned in the output from the previous command.
+
[source,bash]
```
kubectl describe clusterrolebinding cluster\-role\-binding\-name  

```
+

An example output is as follows.
+
[source,yaml]
```
apiVersion: rbac\.authorization\.k8s\.io/v1 kind: ClusterRoleBinding metadata: name: eks\-console\-dashboard\-full\-access\-binding subjects: \- kind: Group name: eks\-console\-dashboard\-full\-access\-group apiGroup: rbac\.authorization\.k8s\.io roleRef: kind: ClusterRole name: eks\-console\-dashboard\-full\-access\-clusterrole apiGroup: rbac\.authorization\.k8s\.io  

```
. Edit the `aws-auth```ConfigMap``. You can use a tool such as `eksctl` to update the `ConfigMap` or you can update it manually by editing it.
+
IMPORTANT: We recommend using ``eksctl``, or another tool, to edit the ``ConfigMap``. For information about other tools you can use, see {https---aws-github-io-aws-eks-best-practices-security-docs-iam--use-tools-to-make-changes-to-the-aws-auth-configmap}[Use tools to make changes to the aws-authConfigMap] in the Amazon EKS best practices guides. An improperly formatted `aws-auth```ConfigMap`` can cause you to lose access to your cluster.
+
+

eksctl:::
**
.Prerequisite
Version `0.177.0` or later of the `eksctl` command line tool installed on your device or {aws} CloudShell. To install or update ``eksctl``, see https://eksctl.io/installation[Installation] in the `eksctl` documentation.
+
... View the current mappings in the ``ConfigMap``. Replace `[replaceable]``my-cluster``` with the name of your cluster. Replace ``[replaceable]``region-code```` with the {aws} Region that your cluster is in.
+
[source,bash]
```
eksctl get iamidentitymapping \-\-cluster my\-cluster \-\-region=region\-code  

```
+

An example output is as follows.
+
[source,none]
```
ARN USERNAME GROUPS ACCOUNT arn:aws:iam::111122223333:role/eksctl\-my\-cluster\-my\-nodegroup\-NodeInstanceRole\-1XLS7754U3ZPA system:node:\{\{EC2PrivateDNSName\}\} system:bootstrappers,system:nodes  

```
... Add a mapping for a role. Replace `[replaceable]``my-role``` with your role name. Replace `[replaceable]``eks-console-dashboard-full-access-group``` with the name of the group specified in your [noloc]``Kubernetes````RoleBinding`` or `ClusterRoleBinding` object. Replace `[replaceable]``111122223333``` with your account ID. You can replace [replaceable]``admin`` with any name you choose.
+
[source,bash]
```
eksctl create iamidentitymapping \-\-cluster my\-cluster \-\-region=region\-code \\ \-\-arn arn:aws:iam::111122223333:role/my\-role \-\-username admin \-\-group eks\-console\-dashboard\-full\-access\-group \\ \-\-no\-duplicate\-arns  

```
+
IMPORTANT: The role ARN can't include a path such as ``role/my-team/developers/my-role``. The format of the ARN must be ``arn:aws:iam::[replaceable]``111122223333``:role/[replaceable]``my-role````. In this example, `my-team/developers/` needs to be removed.
+
+

An example output is as follows.
+
```
2022\-05\-09 14:51:20 \[ℹ\] adding identity "arn:aws:iam::`111122223333`:role/`my\-role`" to auth ConfigMap  

```
... Add a mapping for a user. {https---docs-aws-amazon-com-IAM-latest-UserGuide-id-users-html}[IAM best practices] recommend that you grant permissions to roles instead of users. Replace `[replaceable]``my-user``` with your user name. Replace `[replaceable]``eks-console-dashboard-restricted-access-group``` with the name of the group specified in your [noloc]``Kubernetes````RoleBinding`` or `ClusterRoleBinding` object. Replace `[replaceable]``111122223333``` with your account ID. You can replace [replaceable]``my-user`` with any name you choose.
+
[source,bash]
```
eksctl create iamidentitymapping \-\-cluster my\-cluster \-\-region=region\-code \\ \-\-arn arn:aws:iam::111122223333:user/my\-user \-\-username my\-user \-\-group eks\-console\-dashboard\-restricted\-access\-group \\ \-\-no\-duplicate\-arns  

```
+

An example output is as follows.
+
```
2022\-05\-09 14:53:48 \[ℹ\] adding identity "arn:aws:iam::`111122223333`:user/`my\-user`" to auth ConfigMap  

```
... View the mappings in the `ConfigMap` again.
+
[source,bash]
```
eksctl get iamidentitymapping \-\-cluster my\-cluster \-\-region=region\-code  

```
+

An example output is as follows.
+
[source,none]
```
ARN USERNAME GROUPS ACCOUNT arn:aws:iam::111122223333:role/eksctl\-my\-cluster\-my\-nodegroup\-NodeInstanceRole\-1XLS7754U3ZPA system:node:\{\{EC2PrivateDNSName\}\} system:bootstrappers,system:nodes arn:aws:iam::111122223333:role/admin my\-role eks\-console\-dashboard\-full\-access\-group arn:aws:iam::111122223333:user/my\-user my\-user eks\-console\-dashboard\-restricted\-access\-group  

```
Edit ConfigMap manually:::
... Open the `ConfigMap` for editing.
+
[source,bash]
```
kubectl edit \-n kube\-system configmap/aws\-auth  

```
+
//⁂NOTE: If you receive an error stating "``Error from server (NotFound): configmaps "aws-auth" not found``", then use the procedure in <<aws-auth-configmap,Apply the aws-auth   ConfigMap to your cluster>> to apply the stock ``ConfigMap``.
... Add your IAM principals to the ``ConfigMap``. An IAM group isn't an IAM principal, so it can't be added to the ``ConfigMap``.
+
**** *To add an IAM role (for example, for {https---docs-aws-amazon-com-IAM-latest-UserGuide-id-roles-providers-html}[federated users]):* Add the role details to the `mapRoles` section of the ``ConfigMap``, under ``data``. Add this section if it does not already exist in the file. Each entry supports the following parameters:
+
***** **rolearn**: The ARN of the IAM role to add. This value can't include a path. For example, you can't specify an ARN such as  ``arn:aws:iam::[replaceable]``111122223333``:role/my-team/developers/[replaceable]``role-name````. The ARN needs to be `arn:aws:iam::[replaceable]``111122223333``:role/[replaceable]``role-name``` instead.
***** **username**: The user name within  [noloc]``Kubernetes`` to map to the IAM role.
***** **groups**: The group or list of  [noloc]``Kubernetes`` groups to map the role to. The group can be a default group, or a group specified in a  `clusterrolebinding` or ``rolebinding``. For more information, see {https---kubernetes-io-docs-reference-access-authn-authz-rbac--default-roles-and-role-bindings}[Default roles and role bindings] in the [noloc]``Kubernetes`` documentation.
**** [topcom]##To add an IAM user:##{https---docs-aws-amazon-com-IAM-latest-UserGuide-id-users-html}[IAM best practices] recommend that you grant permissions to roles instead of users. Add the user details to the `mapUsers` section of the ``ConfigMap``, under ``data``. Add this section if it does not already exist in the file. Each entry supports the following parameters:
+
***** **userarn**: The ARN of the IAM user to add.
***** **username**: The user name within  [noloc]``Kubernetes`` to map to the IAM user.
***** **groups**: The group, or list of  [noloc]``Kubernetes`` groups to map the user to. The group can be a default group, or a group specified in a  `clusterrolebinding` or ``rolebinding``. For more information, see {https---kubernetes-io-docs-reference-access-authn-authz-rbac--default-roles-and-role-bindings}[Default roles and role bindings] in the [noloc]``Kubernetes`` documentation.

+

For example, the following YAML block contains:
+
//⁂**** A `mapRoles` section that maps the IAM node instance to [noloc]``Kubernetes`` groups so that nodes can register themselves with the cluster and the  `my-console-viewer-role` IAM role that is mapped to a [noloc]``Kubernetes`` group that can view all  [noloc]``Kubernetes`` resources for all clusters. For a list of the IAM and  [noloc]``Kubernetes`` group permissions required for the  `my-console-viewer-role` IAM role, see <<view-kubernetes-resources-permissions,Required permissions>>.
//⁂**** A `mapUsers` section that maps the `admin` IAM user from the default {aws} account to the `system:masters`[noloc]``Kubernetes`` group and the  `my-user` user from a different {aws} account that is mapped to a [noloc]``Kubernetes`` group that can view  [noloc]``Kubernetes`` resources for a specific namespace. For a list of the IAM and  [noloc]``Kubernetes`` group permissions required for the  `my-user` IAM user, see <<view-kubernetes-resources-permissions,Required permissions>>.

+

Add or remove lines as necessary and replace all  [replaceable]```example values``` with your own values.
+
[source,yaml]
```
\# Please edit the object below\. Lines beginning with a '\#' will be ignored, \# and an empty file will abort the edit\. If an error occurs while saving this file will be \# reopened with the relevant failures\. \# apiVersion: v1 data: mapRoles: \| \- groups: \- system:bootstrappers \- system:nodes rolearn: arn:aws:iam::111122223333:role/my\-role username: system:node:\{\{EC2PrivateDNSName\}\} \- groups: \- eks\-console\-dashboard\-full\-access\-group rolearn: arn:aws:iam::111122223333:role/my\-console\-viewer\-role username: my\-console\-viewer\-role mapUsers: \| \- groups: \- system:masters userarn: arn:aws:iam::111122223333:user/admin username: admin \- groups: \- eks\-console\-dashboard\-restricted\-access\-group userarn: arn:aws:iam::444455556666:user/my\-user username: my\-user  

```
... Save the file and exit your text editor.


[[aws-auth-configmap,aws-auth-configmap.title]]
=== Apply the  `aws-auth`   `ConfigMap` to your cluster

The  `aws-auth```ConfigMap`` is automatically created and applied to your cluster when you create a managed node group or when you create a node group using ``eksctl``. It is initially created to allow nodes to join your cluster, but you also use this `ConfigMap` to add role-based access control (RBAC) access to IAM principals. If you've launched self-managed nodes and haven't applied the `aws-auth```ConfigMap`` to your cluster, you can do so with the following procedure.

. Check to see if you've already applied the `aws-auth```ConfigMap``.
+
[source,bash]
```
kubectl describe configmap \-n kube\-system aws\-auth  

```
+

If you receive an error stating "``Error from server (NotFound): configmaps "aws-auth" not found``", then proceed with the following steps to apply the stock ``ConfigMap``.
. Download, edit, and apply the {aws} authenticator configuration map.
+
.. Download the configuration map.
+
[source,bash]
```
curl \-O [https://s3\.us\-west\-2\.amazonaws\.com/amazon\-eks/cloudformation/2020\-10\-29/aws\-auth\-cm\.yaml](https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/aws-auth-cm.yaml)   

```
.. In the `[path]``aws-auth-cm.yaml``` file, set the `rolearn` to the Amazon Resource Name (ARN) of the IAM role associated with your nodes. You can do this with a text editor, or by replacing `[replaceable]``my-node-instance-role``` and running the following command:
+
[source,bash]
```
sed \-i\.bak \-e 's\|<ARN of instance role \(not instance profile\)>\|my\-node\-instance\-role\|' aws\-auth\-cm\.yaml  

```
+

Don't modify any other lines in this file.
+
IMPORTANT: The role ARN can't include a path such as ``role/my-team/developers/my-role``. The format of the ARN must be ``arn:aws:iam::[replaceable]``111122223333``:role/[replaceable]``my-role````. In this example, `my-team/developers/` needs to be removed.
+
+

You can inspect the {aws} CloudFormation stack outputs for your node groups and look for the following values:
+
*** *InstanceRoleARN* – For node groups that were created with  `eksctl`
*** *NodeInstanceRole* – For node groups that were created with Amazon EKS vended {aws} CloudFormation templates in the {aws} Management Console
.. Apply the configuration. This command may take a few minutes to finish.
+
[source,bash]
```
kubectl apply \-f aws\-auth\-cm\.yaml  

```
+
NOTE: If you receive any authorization or resource type errors, see in the troubleshooting topic.
. Watch the status of your nodes and wait for them to reach the `Ready` status.
+
[source,bash]
```
kubectl get nodes \-\-watch  

```
+

Enter  ``Ctrl``+``C`` to return to a shell prompt.


[.topic]
[[authenticate-oidc-identity-provider,authenticate-oidc-identity-provider.title]]
== Authenticate users for your cluster from an  [noloc]``OpenID Connect`` identity provider

//⁂Amazon EKS supports using  [noloc]``OpenID Connect`` ([noloc]``OIDC``) identity providers as a method to authenticate users to your cluster.  [noloc]``OIDC`` identity providers can be used with, or as an alternative to {aws} Identity and Access Management (IAM). For more information about using IAM, see  <<grant-k8s-access,Grant access to Kubernetes APIs >>. After configuring authentication to your cluster, you can create [noloc]``Kubernetes````roles`` and `clusterroles` to assign permissions to the roles, and then bind the roles to the identities using [noloc]``Kubernetes````rolebindings`` and ``clusterrolebindings``. For more information, see https://kubernetes.io/docs/reference/access-authn-authz/rbac/[Using RBAC Authorization] in the [noloc]``Kubernetes`` documentation.



* You can associate one [noloc]``OIDC`` identity provider to your cluster.
* [noloc]``Kubernetes`` doesn't provide an  [noloc]``OIDC`` identity provider. You can use an existing public  [noloc]``OIDC`` identity provider, or you can run your own identity provider. For a list of certified providers, see  https://openid.net/certification/[OpenID Certification] on the OpenID site.
* The issuer URL of the [noloc]``OIDC`` identity provider must be publicly accessible, so that Amazon EKS can discover the signing keys. Amazon EKS doesn't support  [noloc]``OIDC`` identity providers with self-signed certificates.
* You can't disable IAM authentication to your cluster, because it's still required for joining nodes to a cluster.
* An Amazon EKS cluster must still be created by an {aws} {https---docs-aws-amazon-com-IAM-latest-UserGuide-id-roles-terms-and-concepts-html}[IAM principal], rather than an [noloc]``OIDC`` identity provider user. This is because the cluster creator interacts with the Amazon EKS APIs, rather than the  [noloc]``Kubernetes`` APIs.
//⁂* [noloc]``OIDC`` identity provider-authenticated users are listed in the cluster's audit log if CloudWatch logs are turned on for the control plane. For more information, see  <<enabling-control-plane-log-export,Enabling and disabling control plane logs>>.
//⁂* You can't sign in to the {aws} Management Console with an account from an [noloc]``OIDC`` provider. You can only  <<view-kubernetes-resources,view Kubernetes resources>> in the console by signing into the {aws} Management Console with an {aws} Identity and Access Management account.


[[associate-oidc-identity-provider,associate-oidc-identity-provider.title]]
=== Associate an  [noloc]``OIDC`` identity provider

Before you can associate an  [noloc]``OIDC`` identity provider with your cluster, you need the following information from your provider:



Issuer URL::
* The URL of the OIDC identity provider that allows the API server to discover public signing keys for verifying tokens. The URL must begin with `https://` and should correspond to the `iss` claim in the provider's OIDC ID tokens. In accordance with the OIDC standard, path components are allowed but query parameters are not. Typically the URL consists of only a host name, like `https://server.example.org` or ``https://example.com``. This URL should point to the level below `$$.$$well-known/openid-configuration` and must be publicly accessible over the internet.


Client ID (also known as __audience__)::
* The ID for the client application that makes authentication requests to the OIDC identity provider.

You can associate an identity provider using  `eksctl` or the {aws} Management Console.



eksctl::
.. Create a file named [replaceable]```associate-identity-provider.yaml``` with the following contents. Replace the [replaceable]```example values``` with your own. The values in the `identityProviders` section are obtained from your [noloc]``OIDC`` identity provider. Values are only required for the  ``name``, ``type``, ``issuerUrl``, and `clientId` settings under ``identityProviders``.
+
[source,yaml]
```
  
apiVersion: eksctl\.io/v1alpha5 kind: ClusterConfig  
metadata: name: my\-cluster region: your\-region\-code  
identityProviders: \- name: my\-provider type: oidc issuerUrl: [https://example\.com](https://example.com) clientId: kubernetes usernameClaim: email usernamePrefix: my\-username\-prefix groupsClaim: my\-claim groupsPrefix: my\-groups\-prefix requiredClaims: string: string tags: env: dev  

```
+
IMPORTANT: Don't specify ``system:``, or any portion of that string, for `groupsPrefix` or ``usernamePrefix``.
.. Create the provider.
+
[source,bash]
```
eksctl associate identityprovider \-f associate\-identity\-provider\.yaml  

```
.. To use `kubectl` to work with your cluster and [noloc]``OIDC`` identity provider, see  {https---kubernetes-io-docs-reference-access-authn-authz-authentication--using-kubectl}[Using kubectl] in the [noloc]``Kubernetes`` documentation.


{aws} Management Console::
.. Open the Amazon EKS console at {https---console-aws-amazon-com-eks-home--clusters}[https://console.aws.amazon.com/eks/home#/clusters].
.. Select your cluster, and then select the *Access* tab.
.. In the *[noloc]``OIDC`` Identity Providers* section, select** Associate Identity Provider**.
.. On the *Associate [noloc]``OIDC`` Identity Provider* page, enter or select the following options, and then select  **Associate**.
+
*** For **Name**, enter a unique name for the provider.
*** For **Issuer URL**, enter the URL for your provider. This URL must be accessible over the internet.
*** For **Client ID**, enter the  [noloc]``OIDC`` identity provider's client ID (also known as  **audience**).
*** For **Username claim**, enter the claim to use as the username.
*** For **Groups claim**, enter the claim to use as the user's group.
*** (Optional) Select **Advanced options**, enter or select the following information.
+
**** *Username prefix* – Enter a prefix to prepend to username claims. The prefix is prepended to username claims to prevent clashes with existing names. If you do not provide a value, and the username is a value other than  ``email``, the prefix defaults to the value for **Issuer URL**. You can use the value`` -`` to disable all prefixing. Don't specify `system:` or any portion of that string.
**** *Groups prefix* – Enter a prefix to prepend to groups claims. The prefix is prepended to group claims to prevent clashes with existing names (such as`` system: groups``). For example, the value `oidc:` creates group names like `oidc:engineering` and ``oidc:infra``. Don't specify `system:` or any portion of that string..
**** *Required claims* – Select  *Add claim* and enter one or more key value pairs that describe required claims in the client ID token. The paris describe required claims in the ID Token. If set, each claim is verified to be present in the ID token with a matching value.
.. To use `kubectl` to work with your cluster and [noloc]``OIDC`` identity provider, see  {https---kubernetes-io-docs-reference-access-authn-authz-authentication--using-kubectl}[Using kubectl] in the [noloc]``Kubernetes`` documentation.


[[disassociate-oidc-identity-provider,disassociate-oidc-identity-provider.title]]
=== Disassociate an  [noloc]``OIDC`` identity provider from your cluster

If you disassociate an  [noloc]``OIDC`` identity provider from your cluster, users included in the provider can no longer access the cluster. However, you can still access the cluster with  {https---docs-aws-amazon-com-IAM-latest-UserGuide-id-roles-terms-and-concepts-html}[IAM principals].

. Open the Amazon EKS console at {https---console-aws-amazon-com-eks-home--clusters}[https://console.aws.amazon.com/eks/home#/clusters].
. In the *[noloc]``OIDC`` Identity Providers* section, select  **Disassociate**, enter the identity provider name, and then select  ``Disassociate``.


[[oidc-identity-provider-iam-policy,oidc-identity-provider-iam-policy.title]]
=== Example IAM policy

If you want to prevent an  [noloc]``OIDC`` identity provider from being associated with a cluster, create and associate the following IAM policy to the IAM accounts of your Amazon EKS administrators. For more information, see  {https---docs-aws-amazon-com-IAM-latest-UserGuide-access-policies-create-html}[Creating IAM policies] and {https---docs-aws-amazon-com-IAM-latest-UserGuide-access-policies-manage-attach-detach-html-add-policies-console}[Adding IAM identity permissions] in the IAM User Guide and {https---docs-aws-amazon-com-service-authorization-latest-reference-list-amazonelasticcontainerserviceforkubernetes-html}[Actions, resources, and condition keys for Amazon Elastic Kubernetes Service] in the Service Authorization Reference.

[source,json]
```
\{ "Version": "2012\-10\-17", "Statement": \[ \{ "Sid": "denyOIDC", "Effect": "Deny", "Action": \[ "eks:AssociateIdentityProviderConfig" \], "Resource": "arn:aws:eks:us\-west\-2\.amazonaws\.com:111122223333:cluster/\*"  

```
        },
        {
            "Sid": "eksAdmin",
            "Effect": "Allow",
            "Action": [
                "eks:*"
            ],
            "Resource": "*"
        }
    ]
}
```

```
The following example policy allows  [noloc]``OIDC`` identity provider association if the  `clientID` is `kubernetes` and the `issuerUrl` is ``https://cognito-idp.us-west-2amazonaws.com/*``.

[source,json]
```
\{ "Version": "2012\-10\-17", "Statement": \[ \{ "Sid": "AllowCognitoOnly", "Effect": "Deny", "Action": "eks:AssociateIdentityProviderConfig", "Resource": "arn:aws:eks:us\-west\-2:111122223333:cluster/my\-instance", "Condition": \{ "StringNotLikeIfExists": \{ "eks:issuerUrl": "https://cognito\-idp\.us\-west\-2\.amazonaws\.com/**" \} \} \}, \{ "Sid": "DenyOtherClients", "Effect": "Deny", "Action": "eks:AssociateIdentityProviderConfig", "Resource": "arn:aws:eks:us\-west\-2:111122223333:cluster/my\-instance", "Condition": \{ "StringNotEquals": \{ "eks:clientId": "kubernetes" \} \} \}, \{ "Sid": "AllowOthers", "Effect": "Allow", "Action": "eks:**", "Resource": "\*" \} \] \}  

```
[[partner-validated-identity-providers,partner-validated-identity-providers.title]]
=== Partner validated  [noloc]``OIDC`` identity providers

Amazon EKS maintains relationships with a network of partners that offer support for compatible  [noloc]``OIDC`` identity providers. Refer to the following partners' documentation for details on how to integrate the identity provider with Amazon EKS.

//⁂[cols="1,1,1", frame="all", options="header"]
//⁂|===
//⁂|
                            Partner

//⁂|
                            Product

//⁂|
                            Documentation



//⁂|

PingIdentity
//⁂|

{https---docs-pingidentity-com-r-en-us-pingoneforenterprise-p14e-landing}[PingOne for Enterprise]
//⁂|

{https---docs-pingidentity-com-r-en-us-solution-guides-htg-config-oidc-authn-aws-eks-custers}[Installation instructions]
//⁂|===

Amazon EKS aims to give you a wide selection of options to cover all use cases. If you develop a commercially supported  [noloc]``OIDC`` compatible identity provider that is not listed here, then contact our partner team at  link:mailto:aws-container-partners@amazon.com[aws-container-partners@amazon.com] for more information.
```