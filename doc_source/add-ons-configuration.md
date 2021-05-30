# Amazon EKS add-on configuration<a name="add-ons-configuration"></a>

Amazon EKS installs [add-ons](eks-add-ons.md) to your cluster using standard, best-practice configurations. Depending on your needs, you may desire to customize the configuration of an add-on to enable advanced features.

Amazon EKS uses the Kubernetes [server-side apply feature](https://kubernetes.io/docs/reference/using-api/server-side-apply/) to enable continued management of an add-on from EKS without overwriting user customizations.

To achieve this, Amazon EKS manages a minimum set of fields for every add-on that it installs. All fields that are not managed by EKS (or another Kubernetes control plane process such as `kube-controller-manager`) can be modified without issue.

**Note**  
Modifying a field managed by Amazon EKS will break the ability to manage the add-on using EKS and may result in your changes being over-written when the add-on is updated.

## View field management status
You can use the [kubectl](https://kubernetes.io/docs/reference/kubectl/overview/) to see which fields are managed by EKS for any add-on.

**To see the management status of a field**\.
1. Create the add-on on your cluster using Amazon EKS.
2. Connect to your cluster. If you have not already, you may need to [install kubectl](install-kubectl.md) and [create a kubeconfig](create-kubeconfig.md) to authenticate to your cluster's endpoint.
3. Identify the add-on you want to examine. Depending on your add-on, you will want to look at the deployment or daemonset that defines it. For more information see [view workloads](view-workloads.md)
4. See the managed fields for an add-on by running the command:
  ```
  kubectl get <type>/<add-on-name> -n <add-on-namespace> -o yaml --show-managed-fields
  ```

  Example
  ```
  kubectl get daemonset/aws-node -n kube-system -o yaml --show-managed-fields
  ```

## Understanding field management syntax in the Kubernetes API
The management status of the fields for a Kubernetes object is returned in JSON format.
Each key is either a '.' representing the field itself, and will always map to an empty set, or a string representing a sub-field or item.

The string will follow one of these four formats:
  1. `f:<name>`, where `<name>` is the name of a field in a struct, or key in a map
  2. `v:<value>`, where `<value>` is the exact json formatted value of a list item
  3. `i:<index>`, where `<index>` is position of a item in a list
  4. `k:<keys>`, where `<keys>` is a map of a list item's key fields to their unique values If a key maps to an empty Fields value, the field that key represents is part of the set.

You can see more in the [FieldsV1 API documentation](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.21/#fieldsv1-v1-meta).

**Example**  
Here is an excerpt of the output from the example above:
```
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

From this output, we can interpret that for the VPC CNI (aws-node daemonset), EKS manages the environment variables `AWS_VPC_K8S_CNI_CONFIGURE_RPFILTER` and `MY_NODE_NAME`.

## Considerations for configuring add-ons
+ You can modify any fields for an add-on that are not managed by EKS or another entity on the Kubernetes cluster (such as the `kube-controller-manager`).
+ Before modifying fields, check if they are managed.
+ Modifying a field managed by Amazon EKS will break the ability to manage the add-on using EKS and may result in your changes being over-written when the add-on is updated.
+ You can resolve conflicts from modifications to managed fields by selecting **Enable Override existing configuration for this add-on on the cluster** when you update the add-on. This will revert any changes on managed fields to the defaults for EKS.
