# Amazon EKS add-on configuration<a name="add-ons-configuration"></a>

Amazon EKS installs [add-ons](eks-add-ons.md) to your cluster using standard, best-practice configurations. Depending on your needs, you may desire to customize the configuration of an add-on to enable advanced features.

Amazon EKS uses the Kubernetes [server-side apply feature](https://kubernetes.io/docs/reference/using-api/server-side-apply/) to enable continued management of an add-on from EKS without overwriting user customizations.

To achieve this, Amazon EKS manages a minimum set of fields for every add-on that it installs. All fields that are not managed by EKS (or another Kubernetes control plane process such as `kube-controller-manager`) can be modified without issue.

**Note**  
Modifying a field managed by Amazon EKS will break the ability to manage the add-on using EKS and may result in your changes being over-written when the add-on is updated.

## View field management status
You can use the [kubectl](https://kubernetes.io/docs/reference/kubectl/overview/) to see which fields are managed by EKS for any add-on.

**To see the management status of a field**
1. Create the add-on on your cluster using Amazon EKS.
2. Connect to your cluster. If you have not already, you may need to [install kubectl](install-kubectl.md) and [create a kubeconfig](create-kubeconfig.md) to authenticate to your cluster's endpoint.
3. Identify the add-on you want to examine. Depending on your add-on, you will want to look at the deployment or daemonset that defines it. For more information see [view workloads](view-workloads.md)
4. See the managed fields for an add-on by running the command:
  ```
  kubectl get <type>/<add-on-name> -n <add-on-namespace> -o yaml --show-managed-fields
  ```

  Example
  ```
  kubectl get deployment/coredns -n kube-system -o yaml --show-managed-fields
  ```

## Understanding field management syntax in the Kubernetes API
The management status of the fields for a Kubernetes object is returned in JSON format.
Each key is either a `.` representing the field itself, and will always map to an empty set, or a string representing a sub-field or item.

The output for field management consists of four types of declarations:
  1. `f:<name>`, where `<name>` is the name of a field in a list.
  2. `k:<keys>`, where `<keys>` is a map of a list item's fields.
  3. `v:<value>`, where `<value>` is the exact json formatted value of a list item.
  4. `i:<index>`, where `<index>` is position of an item in the list.

**Managed fields**
In the case where a field (`f:`) is specified but no key `k:<keys>`, then the entire field is managed. Modifications to any values in this field will cause a conflict.

Here is an excerpt of the output from the example above showing fully managed fields.
```
f:containers:
  k:{"name":"coredns"}:
  .: {}
  f:args: {}
  f:image: {}
  f:imagePullPolicy: {}
  f:name: {}
...
manager: eks
```
From this output, we can see that the container name `coredns` is managed by EKS.

**Managed keys**
In the case where key values are specified, the declared keys are managed for that field. In this case, modifying the specified keys will cause a conflict.

Here is an excerpt of the output from the example above showing specific managed keys.
```
f:volumes:
  k:{"name":"config-volume"}:
    .: {}
    f:configMap:
      f:items: {}
      f:name: {}
    f:name: {}
  k:{"name":"tmp"}:
    .: {}
    f:name: {}
...
manager: eks
operation: Apply
```
From this output, we can see that the volume names `config-volume` and `tmp` are managed by EKS.

**Managed fields and keys**
In the case that only a specific key value is managed, you can safely add additional keys (eg: arguments) to a field without causing a conflict.
However, be careful to check that the field is also not declared as managed, in which case adding or modifying any value will cause a conflict.

For example in our output below, both the value of `coredns` for the container name **and** the field name for containers are managed. Adding or modifying any container name will cause a conflict.
```
f:containers:
  k:{"name":"coredns"}:
  f:name: {}
...
manager: eks
```
You can see more in the [FieldsV1 API documentation](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.21/#fieldsv1-v1-meta).

## Considerations for configuring add-ons
+ You can modify any fields for an add-on that are not managed by EKS or another entity on the Kubernetes cluster (such as the `kube-controller-manager`).
+ Before modifying fields, check if they are managed.
+ Modifying a field managed by Amazon EKS will break the ability to manage the add-on using EKS and may result in your changes being over-written when the add-on is updated.
+ You can resolve conflicts from modifications to managed fields by selecting **Enable Override existing configuration for this add-on on the cluster** when you update the add-on. This will revert any changes on managed fields to the defaults for EKS.
