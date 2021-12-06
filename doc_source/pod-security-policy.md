# Pod security policy<a name="pod-security-policy"></a>

The Kubernetes pod security policy admission controller validates pod creation and update requests against a set of rules\. By default, Amazon EKS clusters ship with a fully permissive security policy with no restrictions\. For more information, see [Pod Security Policies](https://kubernetes.io/docs/concepts/policy/pod-security-policy/) in the Kubernetes documentation\.

**Note**  
As of Kubernetes v1\.21, this feature is deprecated\. PodSecurityPolicy will be functional for several more releases, following Kubernetes deprecation guidelines\. To learn more, read [PodSecurityPolicy Deprecation: Past, Present, and Future ](https://kubernetes.io/blog/2021/04/06/podsecuritypolicy-deprecation-past-present-and-future)and the [AWS blog](http://aws.amazon.com/blogs/containers/using-gatekeeper-as-a-drop-in-pod-security-policy-replacement-in-amazon-eks/)\.

## Amazon EKS default pod security policy<a name="default-psp"></a>

Amazon EKS clusters with Kubernetes version 1\.13 and higher have a default pod security policy named `eks.privileged`\. This policy has no restriction on what kind of pod can be accepted into the system, which is equivalent to running Kubernetes with the `PodSecurityPolicy` controller disabled\.

**Note**  
This policy was created to maintain backwards compatibility with clusters that did not have the `PodSecurityPolicy` controller enabled\. You can create more restrictive policies for your cluster and for individual namespaces and service accounts and then delete the default policy to enable the more restrictive policies\.

You can view the default policy with the following command\.

```
kubectl get psp eks.privileged
```

Output:

```
NAME             PRIV   CAPS   SELINUX    RUNASUSER   FSGROUP    SUPGROUP   READONLYROOTFS   VOLUMES
eks.privileged   true   *      RunAsAny   RunAsAny    RunAsAny   RunAsAny   false            *
```

For more details, you can describe the policy with the following command\.

```
kubectl describe psp eks.privileged
```

Output:

```
Name:  eks.privileged

Settings:
  Allow Privileged:                       true
  Allow Privilege Escalation:             0xc0004ce5f8
  Default Add Capabilities:               <none>
  Required Drop Capabilities:             <none>
  Allowed Capabilities:                   *
  Allowed Volume Types:                   *
  Allow Host Network:                     true
  Allow Host Ports:                       0-65535
  Allow Host PID:                         true
  Allow Host IPC:                         true
  Read Only Root Filesystem:              false
  SELinux Context Strategy: RunAsAny
    User:                                 <none>
    Role:                                 <none>
    Type:                                 <none>
    Level:                                <none>
  Run As User Strategy: RunAsAny
    Ranges:                               <none>
  FSGroup Strategy: RunAsAny
    Ranges:                               <none>
  Supplemental Groups Strategy: RunAsAny
    Ranges:                               <none>
```

You can view the full YAML file for the `eks.privileged` pod security policy, its cluster role, and cluster role binding in [Install or restore the default pod security policy](#psp-install-or-restore-default)\.

## Delete the default Amazon EKS pod security policy<a name="psp-delete-default"></a>

If you create more restrictive policies for your pods, then after doing so, you can delete the default Amazon EKS `eks.privileged` pod security policy to enable your custom policies\.

**Important**  
If you are using version 1\.7\.0 or later of the CNI plugin and you assign a custom pod security policy to the `aws-node` Kubernetes service account used for the `aws-node` pods deployed by the Daemonset, then the policy must have `NET_ADMIN` in its `allowedCapabilities` section along with `hostNetwork: true` and `privileged: true` in the policy's `spec`\.

**To delete the default pod security policy**

1. Create a file named *`privileged-podsecuritypolicy.yaml`* with the contents in the example file in [Install or restore the default pod security policy](#psp-install-or-restore-default)\.

1. Delete the YAML with the following command\. This deletes the default pod security policy, the `ClusterRole`, and the `ClusterRoleBinding` associated with it\.

   ```
   kubectl delete -f privileged-podsecuritypolicy.yaml
   ```

## Install or restore the default pod security policy<a name="psp-install-or-restore-default"></a>

If you are upgrading from an earlier version of Kubernetes, or have modified or deleted the default Amazon EKS `eks.privileged` pod security policy, you can restore it with the following steps\.

**To install or restore the default pod security policy**

1. Create a file called `privileged-podsecuritypolicy.yaml` with the following contents\.

   ```
   apiVersion: policy/v1beta1
   kind: PodSecurityPolicy
   metadata:
     name: eks.privileged
     annotations:
       kubernetes.io/description: 'privileged allows full unrestricted access to
         pod features, as if the PodSecurityPolicy controller was not enabled.'
       seccomp.security.alpha.kubernetes.io/allowedProfileNames: '*'
     labels:
       kubernetes.io/cluster-service: "true"
       eks.amazonaws.com/component: pod-security-policy
   spec:
     privileged: true
     allowPrivilegeEscalation: true
     allowedCapabilities:
     - '*'
     volumes:
     - '*'
     hostNetwork: true
     hostPorts:
     - min: 0
       max: 65535
     hostIPC: true
     hostPID: true
     runAsUser:
       rule: 'RunAsAny'
     seLinux:
       rule: 'RunAsAny'
     supplementalGroups:
       rule: 'RunAsAny'
     fsGroup:
       rule: 'RunAsAny'
     readOnlyRootFilesystem: false
   
   ---
   apiVersion: rbac.authorization.k8s.io/v1
   kind: ClusterRole
   metadata:
     name: eks:podsecuritypolicy:privileged
     labels:
       kubernetes.io/cluster-service: "true"
       eks.amazonaws.com/component: pod-security-policy
   rules:
   - apiGroups:
     - policy
     resourceNames:
     - eks.privileged
     resources:
     - podsecuritypolicies
     verbs:
     - use
   
   ---
   apiVersion: rbac.authorization.k8s.io/v1
   kind: ClusterRoleBinding
   metadata:
     name: eks:podsecuritypolicy:authenticated
     annotations:
       kubernetes.io/description: 'Allow all authenticated users to create privileged pods.'
     labels:
       kubernetes.io/cluster-service: "true"
       eks.amazonaws.com/component: pod-security-policy
   roleRef:
     apiGroup: rbac.authorization.k8s.io
     kind: ClusterRole
     name: eks:podsecuritypolicy:privileged
   subjects:
     - kind: Group
       apiGroup: rbac.authorization.k8s.io
       name: system:authenticated
   ```

1. Apply the YAML with the following command\.

   ```
   kubectl apply -f privileged-podsecuritypolicy.yaml
   ```