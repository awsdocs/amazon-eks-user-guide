# Configure the AWS Security Token Service endpoint for a service account<a name="configure-sts-endpoint"></a>

If you're using a Kubernetes service account with [IAM roles for service accounts](iam-roles-for-service-accounts.md), then you can configure the type of AWS Security Token Service endpoint that's used by the service account if your cluster and platform version are the same or later than those listed in the following table\. If your Kubernetes or platform version are earlier than those listed in the table, then your service accounts can only use the global endpoint\.


| Kubernetes version | Platform version | Default endpoint type | 
| --- | --- | --- | 
| 1\.29 | eks\.1 | Regional | 
| 1\.28 | eks\.1 | Regional | 
| 1\.27 | eks\.1 | Regional | 
| 1\.26 | eks\.1 | Regional | 
| 1\.25 | eks\.1 | Regional | 
| 1\.24 | eks\.2 | Regional | 
| 1\.23 | eks\.1 | Regional | 

AWS recommends using the regional AWS STS endpoints instead of the global endpoint\. This reduces latency, provides built\-in redundancy, and increases session token validity\. The AWS Security Token Service must be active in the AWS Region where the Pod is running\. Moreover, your application must have built\-in redundancy for a different AWS Region in the event of a failure of the service in the AWS Region\. For more information, see [Managing AWS STS in an AWS Region](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_enable-regions.html) in the IAM User Guide\.

**Prerequisites**
+ An existing cluster\. If you don't have one, you can create one using one of the [Getting started with Amazon EKS](getting-started.md) guides\.
+ An existing IAM OIDC provider for your cluster\. For more information, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ An existing Kubernetes service account configured for use with the [Amazon EKS IAM for service accounts](iam-roles-for-service-accounts.md) feature\.

**To configure the endpoint type used by a Kubernetes service account**

The following examples all use the `aws-node` Kubernetes service account used by the [Amazon VPC CNI plugin](cni-iam-role.md)\. You can replace the `example values` with your own service accounts, Pods, namespaces, and other resources\.

1. Select a Pod that uses a service account that you want to change the endpoint for\. Determine which AWS Region that the Pod runs in\. Replace `aws-node-6mfgv` with your Pod name and `kube-system` with your Pod's namespace\.

   ```
   kubectl describe pod aws-node-6mfgv -n kube-system |grep Node:
   ```

   An example output is as follows\.

   ```
   ip-192-168-79-166.us-west-2/192.168.79.166
   ```

   In the previous output, the Pod is running on a node in the us\-west\-2 AWS Region\.

1. Determine the endpoint type that the Pod's service account is using\.

   ```
   kubectl describe pod aws-node-6mfgv -n kube-system |grep AWS_STS_REGIONAL_ENDPOINTS
   ```

   An example output is as follows\.

   ```
   AWS_STS_REGIONAL_ENDPOINTS: regional
   ```

   If the current endpoint is global, then `global` is returned in the output\. If no output is returned, then the default endpoint type is in use and has not been overridden\.

1. If your cluster or platform version are the same or later than those listed in the table, then you can change the endpoint type used by your service account from the default type to a different type with one of the following commands\. Replace `aws-node` with the name of your service account and `kube-system` with the namespace for your service account\.
   + If your default or current endpoint type is global and you want to change it to regional:

     ```
     kubectl annotate serviceaccount -n kube-system aws-node eks.amazonaws.com/sts-regional-endpoints=true
     ```

     If you are using [IAM roles for service accounts](iam-roles-for-service-accounts.md) to generate pre\-signed S3 URLs in your application running in Pods' containers, the format of the URL for regional endpoints is similar to the following example:

     ```
     https://bucket.s3.us-west-2.amazonaws.com/path?...&X-Amz-Credential=your-access-key-id/date/us-west-2/s3/aws4_request&...
     ```
   + If your default or current endpoint type is regional and you want to change it to global:

     ```
     kubectl annotate serviceaccount -n kube-system aws-node eks.amazonaws.com/sts-regional-endpoints=false
     ```

     If your application is explicitly making requests to AWS STS global endpoints and you don't override the default behavior of using regional endpoints in Amazon EKS clusters, then requests will fail with an error\. For more information, see [Pod containers receive the following error: `An error occurred (SignatureDoesNotMatch) when calling the GetCallerIdentity operation: Credential should be scoped to a valid region`](security_iam_troubleshoot.md#security-iam-troubleshoot-wrong-sts-endpoint)\.

     If you're using [IAM roles for service accounts](iam-roles-for-service-accounts.md) to generate pre\-signed S3 URLs in your application running in Pods' containers, the format of the URL for global endpoints is similar to the following example:

     ```
     https://bucket.s3.amazonaws.com/path?...&X-Amz-Credential=your-access-key-id/date/us-west-2/s3/aws4_request&...
     ```

   If you have automation that expects the pre\-signed URL in a certain format or if your application or downstream dependencies that use pre\-signed URLs have expectations for the AWS Region targeted, then make the necessary changes to use the appropriate AWS STS endpoint\.

1. Delete and re\-create any existing Pods that are associated with the service account to apply the credential environment variables\. The mutating web hook doesn't apply them to Pods that are already running\. You can replace `Pods`, `kube-system`, and `-l k8s-app=aws-node` with the information for the Pods that you set your annotation for\.

   ```
   kubectl delete Pods -n kube-system -l k8s-app=aws-node
   ```

1. Confirm that the all Pods restarted\.

   ```
   kubectl get Pods -n kube-system -l k8s-app=aws-node
   ```

1. View the environment variables for one of the Pods\. Verify that the `AWS_STS_REGIONAL_ENDPOINTS` value is what you set it to in a previous step\.

   ```
   kubectl describe pod aws-node-kzbtr -n kube-system |grep AWS_STS_REGIONAL_ENDPOINTS
   ```

   An example output is as follows\.

   ```
   AWS_STS_REGIONAL_ENDPOINTS=regional
   ```