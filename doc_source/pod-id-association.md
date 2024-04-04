# Configure a Kubernetes service account to assume an IAM role with EKS Pod Identity<a name="pod-id-association"></a>

This topic covers how to configure a Kubernetes service account to assume an AWS Identity and Access Management \(IAM\) role with EKS Pod Identity\. Any Pods that are configured to use the service account can then access any AWS service that the role has permissions to access\.

To create an EKS Pod Identity association, there is only a single step; you create the association in EKS through the AWS Management Console, AWS CLI, AWS SDKs, AWS CloudFormation and other tools\. There isn't any data or metadata about the associations inside the cluster in any Kubernetes objects and you don't add any annotations to the service accounts\.

**Prerequisites**
+ An existing cluster\. If you don't have one, you can create one by following one of the [Getting started with Amazon EKS](getting-started.md) guides\.
+ The IAM principal that is creating the association must have `iam:PassRole`\.
+ The latest version of the AWS CLI installed and configured on your device or AWS CloudShell\. You can check your current version with `aws --version | cut -d / -f2 | cut -d ' ' -f1`\. Package managers such `yum`, `apt-get`, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI\. To install the latest version, see [ Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with `aws configure`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the AWS Command Line Interface User Guide\. The AWS CLI version installed in the AWS CloudShell may also be several versions behind the latest version\. To update it, see [ Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the AWS CloudShell User Guide\.
+ The `kubectl` command line tool is installed on your device or AWS CloudShell\. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster\. For example, if your cluster version is `1.28`, you can use `kubectl` version `1.27`, `1.28`, or `1.29` with it\. To install or upgrade `kubectl`, see [Installing or updating `kubectl`](install-kubectl.md)\.
+ An existing `kubectl` `config` file that contains your cluster configuration\. To create a `kubectl` `config` file, see [Creating or updating a `kubeconfig` file for an Amazon EKS cluster](create-kubeconfig.md)\.

## Creating the EKS Pod Identity association<a name="pod-id-association-create"></a>

------
#### [ AWS Management Console ]

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to configure the EKS Pod Identity Agent add\-on for\.

1. Choose the **Access** tab\.

1. In the **Pod Identity associations**, choose **Create**\.

1. For the **IAM role**, select the IAM role with the permissions that you want the workload to have\.
**Note**  
The list only contains roles that have the following trust policy which allows EKS Pod Identity to use them\.

   ```
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Sid": "AllowEksAuthToAssumeRoleForPodIdentity",
               "Effect": "Allow",
               "Principal": {
                   "Service": "pods.eks.amazonaws.com"
               },
               "Action": [
                   "sts:AssumeRole",
                   "sts:TagSession"
               ]
           }
       ]
   }
   ```  
`sts:AssumeRole`  
EKS Pod Identity uses `TagSession` to assume the IAM role before passing the temporary credentials to your pods\.  
`sts:TagSession`  
EKS Pod Identity uses `TagSession` to include *session tags* in the requests to AWS STS\.  
You can use these tags in the *condition keys* in the trust policy to restrict which service accounts, namespaces, and clusters can use this role\.  
For a list of Amazon EKS condition keys, see [Conditions defined by Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html#amazonelastickubernetesservice-policy-keys) in the *Service Authorization Reference*\. To learn which actions and resources you can use a condition key with, see [Actions defined by Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html#amazonelastickubernetesservice-actions-as-permissions)\.

1. For the **Kubernetes namespace**, select the Kubernetes namespace that contains the service account and workload\. Optionally, you can specify a namespace by name that doesn't exist in the cluster\.

1. For the **Kubernetes service account**, select the Kubernetes service account to use\. The manifest for your Kubernetes workload must specify this service account\. Optionally, you can specify a service account by name that doesn't exist in the cluster\.

1. \(Optional\) For the **Tags**, choose **Add tag** to add metadata in a key and value pair\. These tags are applied to the association and can be used in IAM policies\.

   You can repeat this step to add multiple tags\.

1. Choose **Create**\.

------
#### [ AWS CLI ]

1. If you want to associate an existing IAM policy to your IAM role, skip to the [next step](#pod-id-create-role)\.

   Create an IAM policy\. You can create your own policy, or copy an AWS managed policy that already grants some of the permissions that you need and customize it to your specific requirements\. For more information, see [Creating IAM policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html) in the *IAM User Guide*\.

   1. Create a file that includes the permissions for the AWS services that you want your Pods to access\. For a list of all actions for all AWS services, see the [Service Authorization Reference](https://docs.aws.amazon.com/service-authorization/latest/reference/)\.

      You can run the following command to create an example policy file that allows read\-only access to an Amazon S3 bucket\. You can optionally store configuration information or a bootstrap script in this bucket, and the containers in your Pod can read the file from the bucket and load it into your application\. If you want to create this example policy, copy the following contents to your device\. Replace *my\-pod\-secrets\-bucket* with your bucket name and run the command\. 

      ```
      cat >my-policy.json <<EOF
      {
          "Version": "2012-10-17",
          "Statement": [
              {
                  "Effect": "Allow",
                  "Action": "s3:GetObject",
                  "Resource": "arn:aws:s3:::my-pod-secrets-bucket"
              }
          ]
      }
      EOF
      ```

   1. Create the IAM policy\.

      ```
      aws iam create-policy --policy-name my-policy --policy-document file://my-policy.json
      ```

1. Create an IAM role and associate it with a Kubernetes service account\.

   1. If you have an existing Kubernetes service account that you want to assume an IAM role, then you can skip this step\.

      Create a Kubernetes service account\. Copy the following contents to your device\. Replace *my\-service\-account* with your desired name and *default* with a different namespace, if necessary\. If you change *default*, the namespace must already exist\.

      ```
      cat >my-service-account.yaml <<EOF
      apiVersion: v1
      kind: ServiceAccount
      metadata:
        name: my-service-account
        namespace: default
      EOF
      kubectl apply -f my-service-account.yaml
      ```

      Run the following command\.

      ```
      kubectl apply -f my-service-account.yaml
      ```

   1. Run the following command to create a trust policy file for the IAM role\.

      ```
      cat >trust-relationship.json <<EOF
      {
          "Version": "2012-10-17",
          "Statement": [
              {
                  "Sid": "AllowEksAuthToAssumeRoleForPodIdentity",
                  "Effect": "Allow",
                  "Principal": {
                      "Service": "pods.eks.amazonaws.com"
                  },
                  "Action": [
                      "sts:AssumeRole",
                      "sts:TagSession"
                  ]
              }
          ]
      }
      EOF
      ```

   1. Create the role\. Replace `my-role` with a name for your IAM role, and `my-role-description` with a description for your role\.

      ```
      aws iam create-role --role-name my-role --assume-role-policy-document file://trust-relationship.json --description "my-role-description"
      ```

   1. Attach an IAM policy to your role\. Replace `my-role` with the name of your IAM role and `my-policy` with the name of an existing policy that you created\.

      ```
      aws iam attach-role-policy --role-name my-role --policy-arn=arn:aws:iam::111122223333:policy/my-policy
      ```
**Note**  
Unlike IAM roles for service accounts, EKS Pod Identity doesn't use an annotation on the service account\.

   1. Run the following command to create the association\. Replace `my-cluster` with the name of the cluster, replace *my\-service\-account* with your desired name and *default* with a different namespace, if necessary\.

      ```
      aws eks create-pod-identity-association --cluster-name my-cluster --role-arn arn:aws:iam::111122223333:role/my-role --namespace default --service-account my-service-account
      ```

      An example output is as follows\.

      ```
      {
          "association": {
              "clusterName": "my-cluster",
              "namespace": "default",
              "serviceAccount": "my-service-account",
              "roleArn": "arn:aws:iam::111122223333:role/my-role",
              "associationArn": "arn:aws::111122223333:podidentityassociation/my-cluster/a-abcdefghijklmnop1",
              "associationId": "a-abcdefghijklmnop1",
              "tags": {},
              "createdAt": 1700862734.922,
              "modifiedAt": 1700862734.922
          }
      }
      ```
**Note**  
You can specify a namespace and service account by name that doesn't exist in the cluster\. You must create the namespace, service account, and the workload that uses the service account for the EKS Pod Identity association to function\.

1. Confirm that the role and service account are configured correctly\.

   1. Confirm that the IAM role's trust policy is configured correctly\.

      ```
      aws iam get-role --role-name my-role --query Role.AssumeRolePolicyDocument
      ```

      An example output is as follows\.

      ```
      {
          "Version": "2012-10-17",
          "Statement": [
              {
                  "Sid": "Allow EKS Auth service to assume this role for Pod Identities",
                  "Effect": "Allow",
                  "Principal": {
                      "Service": "pods.eks.amazonaws.com"
                  },
                  "Action": [
                      "sts:AssumeRole",
                      "sts:TagSession"
                  ]
              }
          ]
      }
      ```

   1. Confirm that the policy that you attached to your role in a previous step is attached to the role\.

      ```
      aws iam list-attached-role-policies --role-name my-role --query AttachedPolicies[].PolicyArn --output text
      ```

      An example output is as follows\.

      ```
      arn:aws:iam::111122223333:policy/my-policy
      ```

   1. Set a variable to store the Amazon Resource Name \(ARN\) of the policy that you want to use\. Replace *my\-policy* with the name of the policy that you want to confirm permissions for\.

      ```
      export policy_arn=arn:aws:iam::111122223333:policy/my-policy
      ```

   1. View the default version of the policy\.

      ```
      aws iam get-policy --policy-arn $policy_arn
      ```

      An example output is as follows\.

      ```
      {
          "Policy": {
              "PolicyName": "my-policy",
              "PolicyId": "EXAMPLEBIOWGLDEXAMPLE",
              "Arn": "arn:aws:iam::111122223333:policy/my-policy",
              "Path": "/",
              "DefaultVersionId": "v1",
              [...]
          }
      }
      ```

   1. View the policy contents to make sure that the policy includes all the permissions that your Pod needs\. If necessary, replace *1* in the following command with the version that's returned in the previous output\.

      ```
      aws iam get-policy-version --policy-arn $policy_arn --version-id v1
      ```

      An example output is as follows\.

      ```
      {
          "Version": "2012-10-17",
          "Statement": [
              {
                  "Effect": "Allow",
                  "Action": "s3:GetObject",
                  "Resource": "arn:aws:s3:::my-pod-secrets-bucket"
              }
          ]
      }
      ```

      If you created the example policy in a previous step, then your output is the same\. If you created a different policy, then the *example* content is different\.

------

**Next step**  
[Configure Pods to use a Kubernetes service account](pod-id-configure-pods.md)