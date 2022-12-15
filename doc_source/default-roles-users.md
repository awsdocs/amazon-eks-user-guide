# Default Amazon EKS created Kubernetes roles and users<a name="default-roles-users"></a>

When you create a Kubernetes cluster, several default identities are created on that cluster for the proper functioning of Kubernetes\. When you create a version `1.20` and later Amazon EKS cluster, Amazon EKS creates Kubernetes identities for each of its default components\. The identities provide Kubernetes role\-based authorization control \(RBAC\) for the cluster components\. For more information, see [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) in the Kubernetes documentation\. 

When you install optional [add\-ons](eks-add-ons.md) to your cluster, additional identities might be added to your cluster\. For more information about identities not addressed by this topic, see the documentation for the add\-on\.

You can view the list of Amazon EKS created identities on your cluster using the AWS Management Console or `kubectl` command line tool\. All of the user identities appear in the `kube` audit logs available to you through Amazon CloudWatch\.

------
#### [ AWS Management Console ]

**Prerequisite**  
The IAM entity \(user or role\) that you use must have the permissions described in [Required permissions](view-kubernetes-resources.md#view-kubernetes-resources-permissions)\.

**To view Amazon EKS created identities using the AWS Management Console**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the **Clusters** list, choose the cluster that contains the identities that you want to view\.

1. Choose the **Resources** tab\.

1. Under **Resource types**, choose **Authorization**\.

1. Choose, **ClusterRoles**, **ClusterRoleBindings**, **Roles**, or **RoleBindings**\. All resources prefaced with **eks** are created by Amazon EKS\. Additional Amazon EKS created identity resources are:
   + The **ClusterRole** and **ClusterRoleBinding** named **aws\-node**\. The **aws\-node** resources support the [Amazon VPC CNI plugin for Kubernetes](managing-vpc-cni.md), which Amazon EKS installs on all clusters\. 
   + A **ClusterRole** named **vpc\-resource\-controller\-role** and a **ClusterRoleBinding** named **vpc\-resource\-controller\-rolebinding**\. These resources support the [Amazon VPC resource controller](https://github.com/aws/amazon-vpc-resource-controller-k8s), which Amazon EKS installs on all clusters\. 

   In addition to the resources that you see in the console, the following special user identities exist on your cluster, though they're not visible in the cluster's configuration:
   + **`eks:cluster-bootstrap`** – Used for `kubectl` operations during cluster bootstrap\.
   + **`eks:support-engineer`** – Used for cluster management operations\.

1. Choose a specific resource to view details about it\. By default, you're shown information in **Structured view**\. In the top\-right corner of the details page you can choose **Raw view** to see all information for the resource\.

------
#### [ Kubectl ]

**Prerequisite**  
The entity that you use \(AWS Identity and Access Management \(IAM\) or OpenID Connect \(OIDC\)\) to list the Kubernetes resources on the cluster must be authenticated by IAM or your OIDC identity provider\. The entity must be granted permissions to use the Kubernetes `get` and `list` verbs for the `Role`, `ClusterRole`, `RoleBinding`, and `ClusterRoleBinding` resources on your cluster that you want the entity to work with\. For more information about granting IAM entities access to your cluster, see [Enabling IAM user and role access to your cluster](add-user-role.md)\. For more information about granting entities authenticated by your own OIDC provider access to your cluster, see [Authenticating users for your cluster from an OpenID Connect identity provider](authenticate-oidc-identity-provider.md)\.

**To view Amazon EKS created identities using `kubectl`**  
Run the command for the type of resource that you want to see\. All returned resources that are prefaced with **eks** are created by Amazon EKS\. In addition to the resources returned in the output from the commands, the following special user identities exist on your cluster, though they're not visible in the cluster's configuration:
+ **`eks:cluster-bootstrap`** – Used for `kubectl` operations during cluster bootstrap\.
+ **`eks:support-engineer`** – Used for cluster management operations\.

**ClusterRoles** – `ClusterRoles` are scoped to your cluster, so any permission granted to a role applies to resources in any Kubernetes namespace on the cluster\.

The following command returns all of the Amazon EKS created Kubernetes `ClusterRoles` on your cluster\.

```
kubectl get clusterroles | grep eks
```

In addition to the `ClusterRoles` returned in the output that are prefaced with, the following `ClusterRoles` exist\.
+ **`aws-node`** – This `ClusterRole` supports the [Amazon VPC CNI plugin for Kubernetes](managing-vpc-cni.md), which Amazon EKS installs on all clusters\.
+ **`vpc-resource-controller-role`** – This `ClusterRole` supports the [Amazon VPC resource controller](https://github.com/aws/amazon-vpc-resource-controller-k8s), which Amazon EKS installs on all clusters\. 

To see the specification for a `ClusterRole`, replace *eks:addon\-manager* in the following command with a `ClusterRole` returned in the output of the previous command\. The following example returns the specification for the *eks:addon\-manager* `ClusterRole`\.

```
kubectl describe clusterrole eks:addon-manager
```

Abbreviated output is as follows\.

```
Name:         eks:addon-manager
Labels:       <none>
Annotations:  <none>
PolicyRule:
  Resources                                        Non-Resource URLs  Resource Names                      Verbs
  ---------                                        -----------------  --------------                      -----
  customresourcedefinitions.apiextensions.k8s.io   []                 [eniconfigs.crd.k8s.amazonaws.com]  [create delete get list patch update watch]
  clusterrolebindings.rbac.authorization.k8s.io    []                 [aws-node]                          [create delete get list patch update watch]
...
```

**ClusterRoleBindings** – `ClusterRoleBindings` are scoped to your cluster\. 

The following command returns all of the Amazon EKS created Kubernetes `ClusterRoleBindings` on your cluster\.

```
kubectl get clusterrolebindings | grep eks
```

In addition to the `ClusterRoleBindings` returned in the output, the following `ClusterRoleBindings` exist\.
+ **`aws-node`** – This `ClusterRoleBinding` supports the [Amazon VPC CNI plugin for Kubernetes](managing-vpc-cni.md), which Amazon EKS installs on all clusters\. 
+ **`vpc-resource-controller-rolebinding`** – This `ClusterRoleBinding` supports the [Amazon VPC resource controller](https://github.com/aws/amazon-vpc-resource-controller-k8s), which Amazon EKS installs on all clusters\. 

To see the specification for a `ClusterRoleBinding`, replace *eks:addon\-manager* in the following command with a `ClusterRoleBinding` returned in the output of the previous command\. The following example returns the specification for the *eks:addon\-manager* `ClusterRoleBinding`\.

```
kubectl describe clusterrolebinding eks:addon-manager
```

The example output is as follows\.

```
Name:         eks:addon-manager
Labels:       <none>
Annotations:  <none>
Role:
  Kind:  ClusterRole
  Name:  eks:addon-manager
Subjects:
  Kind  Name               Namespace
  ----  ----               ---------
  User  eks:addon-manager
```

**Roles** – `Roles` are scoped to a Kubernetes namespace\. All Amazon EKS created `Roles` are scoped to the `kube-system` namespace\.

The following command returns all of the Amazon EKS created Kubernetes `Roles` on your cluster\.

```
kubectl get roles -n kube-system | grep eks
```

To see the specification for a `Role`, replace *eks:addon\-manager* in the following command with the name of a `Role` returned in the output of the previous command\. The following example returns the specification for the *eks:addon\-manager* `Role`\.

```
kubectl describe role eks:addon-manager -n kube-system
```

Abbreviated output is as follows\.

```
Name:         eks:addon-manager
Labels:       <none>
Annotations:  <none>
PolicyRule:
  Resources          Non-Resource URLs     Resource Names          Verbs
  ---------          -----------------     --------------          -----
  configmaps         []                    [coredns]               [create delete get list patch update watch]
  configmaps         []                    [kube-proxy-config]     [create delete get list patch update watch]
...
```

**RoleBindings** – `RoleBindings` are scoped to a Kubernetes namespace\. All Amazon EKS created `RoleBindings` are scoped to the `kube-system` namespace\.

The following command returns all of the Amazon EKS created Kubernetes `RoleBindings` on your cluster\.

```
kubectl get rolebindings -n kube-system | grep eks
```

To see the specification for a `RoleBinding`, replace *eks:addon\-manager* in the following command with a `RoleBinding` returned in the output of the previous command\. The following example returns the specification for the *eks:addon\-manager* `RoleBinding`\.

```
kubectl describe rolebinding eks:addon-manager -n kube-system
```

The example output is as follows\.

```
Name:         eks:addon-manager
Labels:       <none>
Annotations:  <none>
Role:
  Kind:  Role
  Name:  eks:addon-manager
Subjects:
  Kind  Name               Namespace
  ----  ----               ---------
  User  eks:addon-manager
```

------