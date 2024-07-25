# Remove Pod Identiy associations from an Amazon EKS add\-on<a name="remove-addon-role"></a>

Remove the Pod Identity associations from an Amazon EKS add\-on\.

**Remove all pod identity associations from an Amazon EKS Add\-on \(AWS CLI\)**

1. Determine:
   + `cluster-name` – The name of the EKS cluster to install the add\-on onto\.
   + `addon-name` – The name of the Amazon EKS add\-on to install\.

1. Update the addon to specify an empty array of pod identity associations\. 

   ```
   aws eks update-addon --cluster-name <cluster-name> \
   --addon-name <addon-name> \
   --pod-identity-associations "[]"
   ```