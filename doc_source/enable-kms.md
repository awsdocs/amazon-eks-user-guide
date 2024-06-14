# Enabling secret encryption on an existing cluster<a name="enable-kms"></a>

If you enable [secrets encryption](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/), the Kubernetes secrets are encrypted using the AWS KMS key that you select\. The KMS key must meet the following conditions:
+ Symmetric
+ Can encrypt and decrypt data
+ Created in the same AWS Region as the cluster
+ If the KMS key was created in a different account, the [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) must have access to the KMS key\.

For more information, see [Allowing [IAM principals](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) in other accounts to use a KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html) in the *[AWS Key Management Service Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/)*\.

**Warning**  
You can't disable secrets encryption after enabling it\. This action is irreversible\.

------
#### [ eksctl  ]

You can enable encryption in two ways:
+ Add encryption to your cluster with a single command\.

  To automatically re\-encrypt your secrets, run the following command\.

  ```
  eksctl utils enable-secrets-encryption \
      --cluster my-cluster \
      --key-arn arn:aws:kms:region-code:account:key/key
  ```

  To opt\-out of automatically re\-encrypting your secrets, run the following command\.

  ```
  eksctl utils enable-secrets-encryption 
      --cluster my-cluster \
      --key-arn arn:aws:kms:region-code:account:key/key \
      --encrypt-existing-secrets=false
  ```
+ Add encryption to your cluster with a `kms-cluster.yaml` file\.

  ```
  apiVersion: eksctl.io/v1alpha5
  kind: ClusterConfig
  
  metadata:
    name: my-cluster
    region: region-code
    
  secretsEncryption:
    keyARN: arn:aws:kms:region-code:account:key/key
  ```

  To have your secrets re\-encrypt automatically, run the following command\.

  ```
  eksctl utils enable-secrets-encryption -f kms-cluster.yaml
  ```

  To opt out of automatically re\-encrypting your secrets, run the following command\.

  ```
  eksctl utils enable-secrets-encryption -f kms-cluster.yaml --encrypt-existing-secrets=false
  ```

------
#### [ AWS Management Console ]

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose the cluster that you want to add KMS encryption to\.

1. Choose the **Overview** tab \(this is selected by default\)\.

1. Scroll down to the **Secrets encryption** section and choose **Enable**\.

1. Select a key from the dropdown list and choose the **Enable** button\. If no keys are listed, you must create one first\. For more information, see [Creating keys](https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html)

1. Choose the **Confirm** button to use the chosen key\.

------
#### [ AWS CLI ]

1. Associate the [secrets encryption](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) configuration with your cluster using the following AWS CLI command\. Replace the *`example values`* with your own\.

   ```
   aws eks associate-encryption-config \
       --cluster-name my-cluster \
       --encryption-config '[{"resources":["secrets"],"provider":{"keyArn":"arn:aws:kms:region-code:account:key/key"}}]'
   ```

   An example output is as follows\.

   ```
   {
     "update": {
       "id": "3141b835-8103-423a-8e68-12c2521ffa4d",
       "status": "InProgress",
       "type": "AssociateEncryptionConfig",
       "params": [
         {
           "type": "EncryptionConfig",
           "value": "[{\"resources\":[\"secrets\"],\"provider\":{\"keyArn\":\"arn:aws:kms:region-code:account:key/key\"}}]"
         }
       ],
       "createdAt": 1613754188.734,
       "errors": []
     }
   }
   ```

1. You can monitor the status of your encryption update with the following command\. Use the specific `cluster name` and `update ID` that was returned in the previous output\. When a `Successful` status is displayed, the update is complete\.

   ```
   aws eks describe-update \
       --region region-code \
       --name my-cluster \
       --update-id 3141b835-8103-423a-8e68-12c2521ffa4d
   ```

   An example output is as follows\.

   ```
   {
     "update": {
       "id": "3141b835-8103-423a-8e68-12c2521ffa4d",
       "status": "Successful",
       "type": "AssociateEncryptionConfig",
       "params": [
         {
           "type": "EncryptionConfig",
           "value": "[{\"resources\":[\"secrets\"],\"provider\":{\"keyArn\":\"arn:aws:kms:region-code:account:key/key\"}}]"
         }
       ],
       "createdAt": 1613754188.734>,
       "errors": []
     }
   }
   ```

1. To verify that encryption is enabled in your cluster, run the `describe-cluster` command\. The response contains an `EncryptionConfig` string\. 

   ```
   aws eks describe-cluster --region region-code --name my-cluster
   ```

------

After you enabled encryption on your cluster, you must encrypt all existing secrets with the new key:

**Note**  
If you use `eksctl`, running the following command is necessary only if you opt out of re\-encrypting your secrets automatically\.

```
kubectl get secrets --all-namespaces -o json | kubectl annotate --overwrite -f - kms-encryption-timestamp="time value"
```

**Warning**  
If you enable [secrets encryption](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) for an existing cluster and the KMS key that you use is ever deleted, then there's no way to recover the cluster\. If you delete the KMS key, you permanently put the cluster in a degraded state\. For more information, see [Deleting AWS KMS keys](https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html)\.

**Note**  
By default, the `create-key` command creates a [symmetric encryption KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/symmetric-asymmetric.html) with a key policy that gives the account root admin access on AWS KMS actions and resources\. If you want to scope down the permissions, make sure that the `kms:DescribeKey` and `kms:CreateGrant` actions are permitted on the policy for the principal that calls the `create-cluster` API\.  
   
For clusters using KMS Envelope Encryption, `kms:CreateGrant` permissions are required\. The condition `kms:GrantIsForAWSResource` is not supported for the CreateCluster action, and should not be used in KMS policies to control `kms:CreateGrant` permissions for users performing CreateCluster\.