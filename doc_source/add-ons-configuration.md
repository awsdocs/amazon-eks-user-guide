# Amazon EKS add-ons configuration<a name="add-ons-configuration"></a>

Amazon EKS installs add-ons to your cluster using a standard, best-practice configuration. Depending on your needs, you may desire to customize how the configuration of an add-on to enable advanced features.

Amazon EKS uses the Kubernetes [server-side apply](https://kubernetes.io/docs/reference/using-api/server-side-apply/) to enable continued management of an add-on from EKS without overwriting user customizations. For detailed information on server-side apply, see [Kubernetes 1\.18 Feature Server\-side Apply Beta 2](https://kubernetes.io/blog/2020/04/01/kubernetes-1.18-feature-server-side-apply-beta-2/) in the Kubernetes documentation\.

To achieve this, Amazon EKS manages a minimum set of fields for every add-on. All fields that are not managed by EKS (or another Kubernetes control plane process such as `kube-controller-manager`) can be modified using [kubectl](https://kubernetes.io/docs/reference/kubectl/overview/).

**Note**
Modifying a field managed by Amazon EKS will break the ability to manage the add-on using EKS and may result in your changes being over-written when the add-on is updated.

## View field management status
You can use the Kubernetes CLI, [kubectl](https://kubernetes.io/docs/reference/kubectl/overview/), to see which fields are managed by EKS.

**To see the management status of a field**
1. Start the EKS add-on on your cluster.
2. Connect to your cluster. If you have not already, you may need to [install kubectl](install-kubectl.md) and [create a kubeconfig](create-kubeconfig.md) to authenticate to your cluster's endpoint.
3. Identify the add-on you want to examine. Depending on your add-on, you will want to look at the deployment or daemonset that defines it. You can use Kubectl or the EKS console. For more information see [view workloads](view-workloads.md)
4. See the managed fields for an add-on by running the command
  ```
  kubectl get <type>/<add-on-name> -n <add-on-namespace> -o yaml --show-managed-fields
  ```

  Example
  ```
  kubectl get daemonset/aws-node -n kube-system -o yaml --show-managed-fields
  ```

  Output
  ```
  apiVersion: apps/v1
kind: DaemonSet
metadata:
  annotations:
    deprecated.daemonset.template.generation: "7"
    kubectl.kubernetes.io/last-applied-configuration: | {...}
  creationTimestamp: "2020-11-28T21:09:56Z"
  generation: 7
  labels:
    k8s-app: aws-node
  managedFields:
  - apiVersion: apps/v1
    fieldsType: FieldsV1
    fieldsV1:
      f:metadata:
        f:labels:
          f:k8s-app: {}
      f:spec:
        f:selector:
          f:matchLabels:
            f:k8s-app: {}
        f:template:
          f:metadata:
            f:labels:
              f:app.kubernetes.io/name: {}
              f:k8s-app: {}
          f:spec:
            f:affinity:
              f:nodeAffinity:
                f:requiredDuringSchedulingIgnoredDuringExecution:
                  f:nodeSelectorTerms: {}
            f:containers:
              k:{"name":"aws-node"}:
                .: {}
                f:env:
                  k:{"name":"AWS_VPC_K8S_CNI_CONFIGURE_RPFILTER"}:
                    .: {}
                    f:name: {}
                    f:value: {}
                  k:{"name":"MY_NODE_NAME"}:
                    .: {}
                    f:name: {}
                    f:valueFrom:
                      f:fieldRef:
                        f:fieldPath: {}
                f:image: {}
                f:imagePullPolicy: {}
                f:livenessProbe:
                  f:exec:
                    f:command: {}
                  f:initialDelaySeconds: {}
                f:name: {}
                f:ports:
                  k:{"containerPort":61678,"protocol":"TCP"}:
                    .: {}
                    f:containerPort: {}
                    f:name: {}
                    f:protocol: {}
                f:readinessProbe:
                  f:exec:
                    f:command: {}
                  f:initialDelaySeconds: {}
                f:resources:
                  f:requests:
                    f:cpu: {}
                f:securityContext:
                  f:capabilities:
                    f:add: {}
                f:volumeMounts:
                  k:{"mountPath":"/host/etc/cni/net.d"}:
                    .: {}
                    f:mountPath: {}
                    f:name: {}
                  k:{"mountPath":"/host/opt/cni/bin"}:
                    .: {}
                    f:mountPath: {}
                    f:name: {}
                  k:{"mountPath":"/host/var/log/aws-routed-eni"}:
                    .: {}
                    f:mountPath: {}
                    f:name: {}
                  k:{"mountPath":"/run/xtables.lock"}:
                    .: {}
                    f:mountPath: {}
                    f:name: {}
                  k:{"mountPath":"/var/run/aws-node"}:
                    .: {}
                    f:mountPath: {}
                    f:name: {}
                  k:{"mountPath":"/var/run/dockershim.sock"}:
                    .: {}
                    f:mountPath: {}
                    f:name: {}
            f:hostNetwork: {}
            f:initContainers:
              k:{"name":"aws-vpc-cni-init"}:
                .: {}
                f:image: {}
                f:imagePullPolicy: {}
                f:name: {}
                f:securityContext:
                  f:privileged: {}
                f:volumeMounts:
                  k:{"mountPath":"/host/opt/cni/bin"}:
                    .: {}
                    f:mountPath: {}
                    f:name: {}
            f:priorityClassName: {}
            f:serviceAccountName: {}
            f:terminationGracePeriodSeconds: {}
            f:tolerations: {}
            f:volumes:
              k:{"name":"cni-bin-dir"}:
                .: {}
                f:hostPath:
                  f:path: {}
                f:name: {}
              k:{"name":"cni-net-dir"}:
                .: {}
                f:hostPath:
                  f:path: {}
                f:name: {}
              k:{"name":"dockershim"}:
                .: {}
                f:hostPath:
                  f:path: {}
                f:name: {}
              k:{"name":"log-dir"}:
                .: {}
                f:hostPath:
                  f:path: {}
                  f:type: {}
                f:name: {}
              k:{"name":"run-dir"}:
                .: {}
                f:hostPath:
                  f:path: {}
                  f:type: {}
                f:name: {}
              k:{"name":"xtables-lock"}:
                .: {}
                f:hostPath:
                  f:path: {}
                f:name: {}
        f:updateStrategy:
          f:rollingUpdate:
            f:maxUnavailable: {}
          f:type: {}
    manager: eks
    operation: Apply
    time: "2021-04-02T14:54:07Z"
  ```

## Understanding field management syntax in the Kubernetes API
The management status of the fields for a Kubernetes object is returned in JSON format.
Each key is either a '.' representing the field itself, and will always map to an empty set, or a string representing a sub-field or item.

The string will follow one of these four formats:
  1. 'f:<name>', where <name> is the name of a field in a struct, or key in a map
  2. 'v:<value>', where <value> is the exact json formatted value of a list item
  3. 'i:<index>', where <index> is position of a item in a list
  4. 'k:<keys>', where <keys> is a map of a list item's key fields to their unique values If a key maps to an empty Fields value, the field that key represents is part of the set.

You can see more in the [FieldsV1 API documentation](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.21/#fieldsv1-v1-meta).

**Example**
The example above includes the JSON:
```
...

f:containers:
  k:{"name":"aws-node"}:
    .: {}
    f:env:
      k:{"name":"AWS_VPC_K8S_CNI_CONFIGURE_RPFILTER"}:
        .: {}
        f:name: {}
        f:value: {}
      k:{"name":"MY_NODE_NAME"}:
        .: {}
        f:name: {}
        f:valueFrom:
          f:fieldRef:
            f:fieldPath: {}

...

manager: eks
operation: Apply
```

We can interpret this to mean that for the VPC CNI (aws-node) daemonset, EKS manages the environment variables `AWS_VPC_K8S_CNI_CONFIGURE_RPFILTER` and `MY_NODE_NAME`.

## Considerations for configuring add-ons
+ You can modify any fields for an add-on that are not managed by EKS or another entity on the Kubernetes cluster (such as the `kube-controller-manager`).
+ Before modifying fields, check if they are managed.
+ If you modify managed fields, EKS may automatically overwrite your changes or give an error when you try to update the add-on.
+ You can resolve conflicts from modifications to managed fields by selecting **Enable Override existing configuration for this add-on on the cluster** when you update the add-on. This will revert any changes on managed fields to the defaults for EKS.
