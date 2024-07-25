# Use Pod Identitues to assign an IAM role to an Amazon EKS add\-on<a name="update-addon-role"></a>

Certain Amazon EKS add\-ons need IAM roles and permissions\. Before you add update an Amazon EKS add\-on to use a Pod Identity association, verify the role and policy to use\. For more information, see [Retrieve IAM information about an Amazon EKS add\-on](retreive-iam-info.md)\.

**Update an Amazon EKS add\-on to use a Pod Identity Association \(AWS CLI\)**

1. Determine:
   + `cluster-name` – The name of the cluster to install the add\-on onto\.
   + `addon-name` – The name of the add\-on to install\.
   + `service-account-name` – The name of the Kubernetes Service Account used by the add\-on\.
   + `iam-role-arn` – The ARN of an IAM role with sufficient permissions for the add\-on\. The role must have the required trust policy for EKS Pod Identity\. For more information see [Creating the EKS Pod Identity association](pod-id-association.md#pod-id-association-create)\.

1. Update the add\-on using the AWS CLI\. You can also specify Pod Identity associations when creating an add\-on, using the same `--pod-identity-assocations` syntax\. Note that when you specify pod identity associations while updating an add\-on, all previous pod identity associations are overwritten\. 

   ```
   aws eks update-addon --cluster-name <cluster-name> \
   --addon-name <addon-name> \
   --pod-identity-associations 'serviceAccount=<service-account-name>,roleArn=<role-arn>'
   ```

   For example:

   ```
   aws eks update-addon --cluster-name mycluster \
   --addon-name aws-ebs-csi-driver \
   --pod-identity-associations 'serviceAccount=ebs-csi-controller-sa,roleArn=arn:aws:iam::123456789012:role/StorageDriver'
   ```

1. Validate the Pod Identity association was created:

   ```
   aws eks list-pod-identity-associations --cluster-name <cluster-name> 
   ```

   If successful, you should see output similar to the following\. Note the OwnerARN of the EKS add\-on\. 

   ```
   {
       "associations": [
           {
               "clusterName": "mycluster",
               "namespace": "kube-system",
               "serviceAccount": "ebs-csi-controller-sa",
               "associationArn": "arn:aws:eks:us-west-2:123456789012:podidentityassociation/mycluster/a-4wvljrezsukshq1bv",
               "associationId": "a-4wvljrezsukshq1bv",
               "ownerArn": "arn:aws:eks:us-west-2:123456789012:addon/mycluster/aws-ebs-csi-driver/9cc7ce8c-2e15-b0a7-f311-426691cd8546"
           }
       ]
   }
   ```