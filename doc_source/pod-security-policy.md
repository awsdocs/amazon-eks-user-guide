# Pod security policy<a name="pod-security-policy"></a>

The Kubernetes pod security policy admission controller validates pod creation and update requests against a set of rules\. By default, Amazon EKS clusters ship with a fully permissive security policy with no restrictions\. For more information, see [Pod Security Policies](https://kubernetes.io/docs/concepts/policy/pod-security-policy/) in the Kubernetes documentation\.

**Note**  
The pod security policy admission controller is only enabled on Amazon EKS clusters running Kubernetes version 1\.13 or later\. You must update your cluster's Kubernetes version to at least 1\.13 to use pod security policies\. For more information, see [Updating a cluster](update-cluster.md)\.

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

The following example shows the full YAML file for the `eks.privileged` pod security policy, its cluster role, and cluster role binding\.

```
---
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

**To delete the default pod security policy**

After you create custom pod security policies for your cluster, you can delete the default Amazon EKS `eks.privileged` pod security policy to enable your custom policies\.

1. Create a file called `privileged-podsecuritypolicy.yaml` and paste the full `eks.privileged` YAML file contents from the preceding example into it \(this allows you to delete the pod security policy, the `ClusterRole`, and the `ClusterRoleBinding` associated with it\)\.

1. Delete the YAML with the following command\.

   ```
   kubectl delete -f privileged-podsecuritypolicy.yaml
   ```<a name="install-default-psp"></a>

**To install or restore the default pod security policy**

If you are upgrading from an earlier version of Kubernetes, or have modified or deleted the default Amazon EKS `eks.privileged` pod security policy, you can restore it with the following steps\.

1. Create a file called `privileged-podsecuritypolicy.yaml` and paste the YAML file contents below into it\.

   ```
   ---
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