# Configure a Kubernetes service account to assume an IAM role<a name="associate-service-account-role"></a>

This topic covers how to configure a Kubernetes service account to assume an AWS Identity and Access Management \(IAM\) role\. Any Pods that are configured to use the service account can then access any AWS service that the role has permissions to access\.

**Prerequisites**
+ An existing cluster\. If you don't have one, you can create one by following one of the [Getting started with Amazon EKS](getting-started.md) guides\.
+ An existing IAM OpenID Connect \(OIDC\) provider for your cluster\. To learn if you already have one or how to create one, see [Create an IAM OIDC provider for your cluster](enable-iam-roles-for-service-accounts.md)\.
+ Version `2.12.3` or later or version `1.27.160` or later of the AWS Command Line Interface \(AWS CLI\) installed and configured on your device or AWS CloudShell\. To check your current version, use `aws --version | cut -d / -f2 | cut -d ' ' -f1`\. Package managers such `yum`, `apt-get`, or Homebrew for macOS are often several versions behind the latest version of the AWS CLI\. To install the latest version, see [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Quick configuration with aws configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) in the *AWS Command Line Interface User Guide*\. The AWS CLI version that is installed in AWS CloudShell might also be several versions behind the latest version\. To update it, see [Installing AWS CLI to your home directory](https://docs.aws.amazon.com/cloudshell/latest/userguide/vm-specs.html#install-cli-software) in the *AWS CloudShell User Guide*\.
+ The `kubectl` command line tool is installed on your device or AWS CloudShell\. The version can be the same as or up to one minor version earlier or later than the Kubernetes version of your cluster\. For example, if your cluster version is `1.28`, you can use `kubectl` version `1.27`, `1.28`, or `1.29` with it\. To install or upgrade `kubectl`, see [Installing or updating `kubectl`](install-kubectl.md)\.
+ An existing `kubectl` `config` file that contains your cluster configuration\. To create a `kubectl` `config` file, see [Creating or updating a `kubeconfig` file for an Amazon EKS cluster](create-kubeconfig.md)\.

**To associate an IAM role with a Kubernetes service account**

1. If you want to associate an existing IAM policy to your IAM role, skip to the [next step](#irsa-create-role)\.

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

1. Create an IAM role and associate it with a Kubernetes service account\. You can use either `eksctl` or the AWS CLI\.

------
#### [ eksctl ]

**Prerequisite**  
Version `0.175.0` or later of the `eksctl` command line tool installed on your device or AWS CloudShell\. To install or update `eksctl`, see [Installation](https://eksctl.io/installation) in the `eksctl` documentation\.

   Replace *my\-service\-account* with the name of the Kubernetes service account that you want `eksctl` to create and associate with an IAM role\. Replace *default* with the namespace that you want `eksctl` to create the service account in\. Replace *my\-cluster* with the name of your cluster\. Replace *my\-role* with the name of the role that you want to associate the service account to\. If it doesn't already exist, `eksctl` creates it for you\. Replace *111122223333* with your account ID and *my\-policy* with the name of an existing policy\.

   ```
   eksctl create iamserviceaccount --name my-service-account --namespace default --cluster my-cluster --role-name my-role \
       --attach-policy-arn arn:aws:iam::111122223333:policy/my-policy --approve
   ```

**Important**  
If the role or service account already exist, the previous command might fail\. `eksctl` has different options that you can provide in those situations\. For more information run `eksctl create iamserviceaccount --help`\.

------
#### [ AWS CLI ]

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

   1. Set your AWS account ID to an environment variable with the following command\.

      ```
      account_id=$(aws sts get-caller-identity --query "Account" --output text)
      ```

   1. Set your cluster's OIDC identity provider to an environment variable with the following command\. Replace `my-cluster` with the name of your cluster\.

      ```
      oidc_provider=$(aws eks describe-cluster --name my-cluster --region $AWS_REGION --query "cluster.identity.oidc.issuer" --output text | sed -e "s/^https:\/\///")
      ```

   1. Set variables for the namespace and name of the service account\. Replace `my-service-account` with the Kubernetes service account that you want to assume the role\. Replace *default* with the namespace of the service account\.

      ```
      export namespace=default
      export service_account=my-service-account
      ```

   1. Run the following command to create a trust policy file for the IAM role\. If you want to allow all service accounts within a namespace to use the role, then copy the following contents to your device\. Replace *StringEquals* with **StringLike** and replace *$service\_account* with **\***\. You can add multiple entries in the `StringEquals` or `StringLike` conditions to allow multiple service accounts or namespaces to assume the role\. To allow roles from a different AWS account than the account that your cluster is in to assume the role, see [Cross\-account IAM permissions](cross-account-access.md) for more information\.

      ```
      cat >trust-relationship.json <<EOF
      {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect": "Allow",
            "Principal": {
              "Federated": "arn:aws:iam::$account_id:oidc-provider/$oidc_provider"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
              "StringEquals": {
                "$oidc_provider:aud": "sts.amazonaws.com",
                "$oidc_provider:sub": "system:serviceaccount:$namespace:$service_account"
              }
            }
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
      aws iam attach-role-policy --role-name my-role --policy-arn=arn:aws:iam::$account_id:policy/my-policy
      ```

   1. Annotate your service account with the Amazon Resource Name \(ARN\) of the IAM role that you want the service account to assume\. Replace `my-role` with the name of your existing IAM role\. Suppose that you allowed a role from a different AWS account than the account that your cluster is in to assume the role in a previous step\. Then, make sure to specify the AWS account and role from the other account\. For more information, see [Cross\-account IAM permissions](cross-account-access.md)\.

      ```
      kubectl annotate serviceaccount -n $namespace $service_account eks.amazonaws.com/role-arn=arn:aws:iam::$account_id:role/my-role
      ```

------

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
                  "Effect": "Allow",
                  "Principal": {
                      "Federated": "arn:aws:iam::111122223333:oidc-provider/oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE"
                  },
                  "Action": "sts:AssumeRoleWithWebIdentity",
                  "Condition": {
                      "StringEquals": {
                          "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:sub": "system:serviceaccount:default:my-service-account",
                          "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:aud": "sts.amazonaws.com"
                      }
                  }
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

   1. Confirm that the Kubernetes service account is annotated with the role\.

      ```
      kubectl describe serviceaccount my-service-account -n default
      ```

      An example output is as follows\.

      ```
      Name:                my-service-account
      Namespace:           default
      Annotations:         eks.amazonaws.com/role-arn: arn:aws:iam::111122223333:role/my-role
      Image pull secrets:  <none>
      Mountable secrets:   my-service-account-token-qqjfl
      Tokens:              my-service-account-token-qqjfl
      [...]
      ```

1. \(Optional\) [Configure the AWS Security Token Service endpoint for a service account](configure-sts-endpoint.md)\. AWS recommends using a regional AWS STS endpoint instead of the global endpoint\. This reduces latency, provides built\-in redundancy, and increases session token validity\.

**Next step**  
[Configure Pods to use a Kubernetes service account](pod-configuration.md)