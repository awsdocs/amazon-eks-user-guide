# Storage classes<a name="storage-classes"></a>

Amazon EKS clusters that were created prior to Kubernetes version `1.11` weren't created with any storage classes\. You must define storage classes for your cluster to use and you should define a default storage class for your persistent volume claims\. For more information, see [Storage classes](https://kubernetes.io/docs/concepts/storage/storage-classes) in the Kubernetes documentation\.

**Note**  
The [in\-tree Amazon EBS storage provisioner](https://kubernetes.io/docs/concepts/storage/volumes/#awselasticblockstore) is deprecated\. If you are upgrading your cluster to version `1.23`, then you must first install the [Amazon EBS driver](ebs-csi.md) before updating your cluster\. For more information, see [Amazon EBS CSI migration frequently asked questions](ebs-csi-migration-faq.md)\.

**To create an AWS storage class for your Amazon EKS cluster**

1. Determine which storage classes your cluster already has\.

   ```
   kubectl get storageclass
   ```

   The example output is as follows\.

   ```
   NAME            PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
   gp2 (default)   kubernetes.io/aws-ebs   Delete          WaitForFirstConsumer   false                  34m
   ```

   If your cluster returns the previous output, then it already has the storage class defined in the remaining steps\. You can define other storage classes using the steps for deploying any of the CSI drivers in the [Storage](storage.md) chapter\. Once deployed, you can set one of the storage classes as your [default](#define-default-storage-class) storage class\.

1. Create an AWS storage class manifest file for your storage class\. The following `gp2-storage-class.yaml` example defines a storage class called `gp2` that uses the Amazon EBS `gp2` volume type\.

   For more information about the options available for AWS storage classes, see [AWS EBS](https://kubernetes.io/docs/concepts/storage/storage-classes/#aws-ebs) in the Kubernetes documentation\.

   ```
   kind: StorageClass
   apiVersion: storage.k8s.io/v1
   metadata:
     name: gp2
     annotations:
       storageclass.kubernetes.io/is-default-class: "true"
   provisioner: kubernetes.io/aws-ebs
   parameters:
     type: gp2
     fsType: ext4
   ```

1. Use  `kubectl`  to create the storage class from the manifest file\.

   ```
   kubectl create -f gp2-storage-class.yaml
   ```

   The example output is as follows\.

   ```
   storageclass "gp2" created
   ```<a name="define-default-storage-class"></a>

**To define a default storage class**

1. List the existing storage classes for your cluster\. A storage class must be defined before you can set it as a default\.

   ```
   kubectl get storageclass
   ```

   The example output is as follows\.

   ```
   NAME      PROVISIONER             AGE
   gp2       kubernetes.io/aws-ebs   8m
   ```

1. Choose a storage class and set it as your default by setting the `storageclass.kubernetes.io/is-default-class=true` annotation\.

   ```
   kubectl annotate storageclass gp2 storageclass.kubernetes.io/is-default-class=true
   ```

   The example output is as follows\.

   ```
   storageclass "gp2" patched
   ```

1. Verify that the storage class is now set as default\.

   ```
   kubectl get storageclass
   ```

   The example output is as follows\.

   ```
   gp2 (default)   kubernetes.io/aws-ebs   12m
   ```