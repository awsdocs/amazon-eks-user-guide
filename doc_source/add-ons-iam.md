# IAM roles for Amazon EKS add\-ons<a name="add-ons-iam"></a>

Certain Amazon EKS add\-ons need IAM roles and permissions to call AWS APIs\. For example, the Amazon VPC CNI add\-on calls certain AWS APIs to configure networking resources in your account\. These add\-ons need to be granted permission using IAM\. More specifically, the service account of the pod running the add\-on needs to be associated with an IAM role with a specific IAM policy\. 

The recommended way to grant AWS permissions to cluster workloads is using the Amazon EKS feature Pod Identities\. You can use a **Pod Identity Association** to map the service account of an add\-on to an IAM role\. If a pod uses a service account that has an association, Amazon EKS sets environment variables in the containers of the pod\. The environment variables configure the AWS SDKs, including the AWS CLI, to use the EKS Pod Identity credentials\. For more information, see [Learn how EKS Pod Identity grants pods access to AWS services](pod-identities.md)

Amazon EKS add\-ons can help manage the life cycle of pod identity associations corresponding to the add\-on\. For example, you can create or update an Amazon EKS add\-on and the necessary pod identity association in a single API call\. Amazon EKS also provides an API for retrieving suggested IAM policies\.

**Suggested Usage:**

1. Confirm that [Amazon EKS pod identity agent](pod-id-agent-setup.md) is setup on your cluster\.

1. Determine if the add\-on you want to install requires IAM permissions using the `describe-addon-versions` AWS CLI operation\. If the `requiresIamPermissions` flag is `true`, then you should use the `describe-addon-configurations` operation to determine the permissions needed by the addon\. The response includes a list of suggested managed IAM policies\. 

1. Retrieve the name of the Kubernetes Service Account and the IAM policy using the `describe-addon-configuration` CLI operation\. Evaluate the scope of the suggested policy against your security requirements\.

1. Create an IAM role using the suggested permissions policy, and the trust policy required by Pod Identity\. For more information, see [Creating the EKS Pod Identity association](pod-id-association.md#pod-id-association-create)\. 

1. Create or update an Amazon EKS add\-on using the CLI\. Specify at least one pod identity association\. A pod identity association is the name of a Kubernetes service account, and the ARN of the IAM role\. 

**Considerations:**
+ Pod identity associations created using the add\-on APIs are owned by the respective add\-on\. If you delete the add\-on, the pod identity association is also deleted\. You can prevent this cascading delete by using the `preserve` option when deleting an addon using the AWS CLI or API\. You also can directly update or delete the pod identity association if necessary\. Add\-ons can't assume ownership of existing pod identity associations\. You must delete the existing association and re\-create it using an add\-on create or update operation\. 
+ Amazon EKS recommends using pod identity associations to manage IAM permissions for add\-ons\. The previous method, IAM roles for service accounts \(IRSA\), is still supported\. You can specify both an IRSA `serviceAccountRoleArn` and a pod identity association for an add\-on\. If the EKS pod identity agent is installed on the cluster, the `serviceAccountRoleArn` will be ignored, and EKS will use the provided pod identity association\. If Pod Identity is not enabled, the `serviceAccountRoleArn` will be used\. 
+ If you update the pod identity associations for an existing add\-on, Amazon EKS initiates a rolling restart of the add\-on pods\.

 