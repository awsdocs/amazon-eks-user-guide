# Storage Classes<a name="storage-classes"></a>

Amazon EKS clusters are not created with any storage classes\. You must define storage classes for your cluster to use and you should define a default storage class for your persistent volume claims\. For more information, see [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes) in the Kubernetes documentation\.

**To create an AWS storage class for your Amazon EKS cluster**

1. Create an AWS storage class manifest file for your storage class\. The below example defines a storage class called `gp2` that uses the Amazon EBS `gp2` volume type\. For more information about the options available for AWS storage classes, see [AWS](https://kubernetes.io/docs/concepts/storage/storage-classes/#aws) in the Kubernetes documentation\. For this example, the file is called `gp2-storage-class.yaml`\.

   ```
   kind: StorageClass
   apiVersion: storage.k8s.io/v1
   metadata:
     name: gp2
   provisioner: kubernetes.io/aws-ebs
   parameters:
     type: gp2
   reclaimPolicy: Retain
   mountOptions:
     - debug
   ```

1. Use kubectl to create the storage class from the manifest file\.

   ```
   kubectl create -f gp2-storage-class.yaml
   ```

   Output:

   ```
   storageclass "gp2" created
   ```

**To define a default storage class**

1. List the existing storage classes for your cluster\. A storage class must be defined before you can set it as a default\.

   ```
   kubectl get storageclass
   ```

   Output:

   ```
   NAME      PROVISIONER             AGE
   gp2       kubernetes.io/aws-ebs   8m
   sc1       kubernetes.io/aws-ebs   6s
   ```

1. Choose a storage class and set it as your default by setting the `storageclass.kubernetes.io/is-default-class=true` annotation\.

   ```
   kubectl patch storageclass gp2 -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
   ```

   Output:

   ```
   storageclass "gp2" patched
   ```

1. Verify that the storage class is now set as default\.

   ```
   kubectl get storageclass
   ```

   Output:

   ```
   gp2 (default)   kubernetes.io/aws-ebs   12m
   sc1             kubernetes.io/aws-ebs   4m
   ```