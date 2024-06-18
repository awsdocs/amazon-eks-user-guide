# Kubernetes field management<a name="kubernetes-field-management"></a>

Amazon EKS add\-ons are installed to your cluster using standard, best practice configurations\. For more information about adding an Amazon EKS add\-on to your cluster, see [Amazon EKS add\-ons](eks-add-ons.md)\. 

You may want to customize the configuration of an Amazon EKS add\-on to enable advanced features\. Amazon EKS uses the Kubernetes server\-side apply feature to enable management of an add\-on by Amazon EKS without overwriting your configuration for settings that aren't managed by Amazon EKS\. For more information, see [Server\-Side Apply](https://kubernetes.io/docs/reference/using-api/server-side-apply/) in the Kubernetes documentation\. To achieve this, Amazon EKS manages a minimum set of fields for every add\-on that it installs\. You can modify all fields that aren't managed by Amazon EKS, or another Kubernetes control plane process such as `kube-controller-manager`, without issue\. 

**Important**  
Modifying a field managed by Amazon EKS prevents Amazon EKS from managing the add\-on and may result in your changes being overwritten when an add\-on is updated\.

## View field management status<a name="view-field-management"></a>

You can use `kubectl` to see which fields are managed by Amazon EKS for any Amazon EKS add\-on\.

**To see the management status of a field**

1. Determine which add\-on that you want to examine\. To see all of the `deployments` and `DaemonSets` deployed to your cluster, see [View Kubernetes resources](view-kubernetes-resources.md)\.

1. View the managed fields for an add\-on by running the following command:

   ```
   kubectl get type/add-on-name -n add-on-namespace -o yaml
   ```

   For example, you can see the managed fields for the CoreDNS add\-on with the following command\.

   ```
   kubectl get deployment/coredns -n kube-system -o yaml
   ```

   Field management is listed in the following section in the returned output\.

   ```
   [...]
   managedFields:
     - apiVersion: apps/v1
       fieldsType: FieldsV1
       fieldsV1:                        
   [...]
   ```
**Note**  
If you don't see `managedFields` in the output, add `--show-managed-fields` to the command and run it again\. The version of `kubectl` that you're using determines whether managed fields are returned by default\.

## Understanding field management syntax in the Kubernetes API<a name="add-on-config-management-understanding-field-management"></a>

When you view details for a Kubernetes object, both managed and unmanaged fields are returned in the output\. Managed fields can be either of the following types:
+ **Fully managed** – All keys for the field are managed by Amazon EKS\. Modifications to any value causes a conflict\.
+ **Partially managed** – Some keys for the field are managed by Amazon EKS\. Only modifications to the keys explicitly managed by Amazon EKS cause a conflict\.

Both types of fields are tagged with `manager: eks`\.

Each key is either a `.` representing the field itself, which always maps to an empty set, or a string that represents a sub\-field or item\. The output for field management consists of the following types of declarations:
+ `f:name`, where `name` is the name of a field in a list\.
+ `k:keys`, where `keys` is a map of a list item's fields\.
+ `v:value`, where `value` is the exact JSON formatted value of a list item\.
+ `i:index`, where `index` is position of an item in the list\.

The following portions of output for the CoreDNS add\-on illustrate the previous declarations: 
+ **Fully managed fields** – If a managed field has an `f:` \(field\) specified, but no `k:` \(key\), then the entire field is managed\. Modifications to any values in this field cause a conflict\. 

  In the following output, you can see that the container named `coredns` is managed by `eks`\. The `args`, `image`, and `imagePullPolicy` sub\-fields are also managed by `eks`\. Modifications to any values in these fields cause a conflict\.

  ```
  [...]
  f:containers:
    k:{"name":"coredns"}:
    .: {}
    f:args: {}
    f:image: {}
    f:imagePullPolicy: {}
  [...]
  manager: eks
  [...]
  ```
+ **Partially managed fields** – If a managed key has a value specified, the declared keys are managed for that field\. Modifying the specified keys cause a conflict\. 

  In the following output, you can see that `eks` manages the `config-volume` and `tmp` volumes set with the `name` key\.

  ```
  [...]
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
  [...]
  manager: eks
  [...]
  ```
+ **Adding keys to partially managed fields** – If only a specific key value is managed, you can safely add additional keys, such as arguments, to a field without causing a conflict\. If you add additional keys, make sure that the field isn't managed first\. Adding or modifying any value that is managed causes a conflict\.

  In the following output, you can see that both the `name` key and `name` field are managed\. Adding or modifying any container name causes a conflict with this managed key\. 

  ```
  [...]
  f:containers:
    k:{"name":"coredns"}:
  [...]
      f:name: {}
  [...]
  manager: eks
  [...]
  ```