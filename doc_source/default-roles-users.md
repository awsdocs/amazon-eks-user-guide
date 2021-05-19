# Default Amazon EKS Kubernetes roles and users<a name="default-roles-users"></a>

Starting with version 1\.20, Amazon EKS creates identities for each of the kubernetes components\. The following objects have been created by the Amazon EKS team to provide RBAC permissions for the components:

**Note**  
These roles and users only apply to 1\.20 clusters\.

**Roles**
+ `eks:authenticator`
+ `eks:certificate-controller-approver`
+ `eks:certificate-controller`
+ `eks:cluster-event-watcher`
+ `eks:fargate-scheduler`
+ `eks:k8s-metrics`
+ `eks:nodewatcher`
+ `eks:pod-identity-mutating-webhook`

**RoleBindings**
+ `eks:authenticator`
+ `eks:certificate-controller-approver`
+ `eks:certificate-controller`
+ `eks:cluster-event-watcher`
+ `eks:fargate-scheduler`
+ `eks:k8s-metrics`
+ `eks:nodewatcher`
+ `eks:pod-identity-mutating-webhook`

**Users**
+ `eks:authenticator`
+ `eks:certificate-controller`
+ `eks:cluster-event-watcher`
+ `eks:fargate-scheduler`
+ `eks:k8s-metrics`
+ `eks:nodewatcher`
+ `eks:pod-identity-mutating-webhook`

In addition to the objects above, Amazon EKS uses a special user identity `eks:cluster-bootstrap` for `kubectl` operations during cluster bootstrap\. Amazon EKS also uses a special user identity `eks:support-engineer` for cluster management operations\. All the user identities will appear in the `kube` audit logs available to customers through CloudWatch\.

Run `kubectl describe clusterrole <rolename>` to see the permissions for each role\.