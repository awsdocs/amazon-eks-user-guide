# Connecting a cluster<a name="connecting-cluster"></a>


|  | 
| --- |
| The Amazon EKS Connector is in preview release for Amazon EKS and is subject to change\. | 

## Step 1: Registering the cluster<a name="connector-connecting"></a>

You can connect an external Kubernetes cluster to Amazon EKS with AWS CLI and the AWS Management Console\. This process involves two steps: registering the cluster with Amazon EKS and applying a YAML manifest file to enable connectivity\. You must have the 2 roles described in [Required IAM roles for Amazon EKS Connector](eks-connector.md#connector-iam-permissions)\. To allow another user to view the cluster, follow [Granting access to a user to view a cluster](connector-grant-access.md)\.

You must have the following permissions to register a cluster:
+  eks:RegisterCluster 
+  ssm:CreateActivation
+ ssm:DeleteActivation
+  iam:PassRole

------
#### [ AWS CLI ]

**Prerequisites**
+ AWS CLI must be installed\. To install it or upgrade, see [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)\.
+ Ensure that the Amazon EKS Connector service\-linked IAM role is created\. For more information, see [Creating the Amazon EKS Connector service\-linked IAM role](eks-connector.md#con-slr)\.
+ Ensure the Amazon EKS Connector agent role is created\. For more information, see [Creating the Amazon EKS Connector agent IAM role](eks-connector.md#create-con-agent-role)\.<a name="connect-cluster-eksctl"></a>

**To register your cluster with the AWS CLI**

1. For the Connector configuration, specify your Amazon EKS Connector agent IAM role\. For more information, see [Required IAM roles for Amazon EKS Connector](eks-connector.md#connector-iam-permissions)\.

   ```
   aws eks register-cluster \
        --name my-first-registered-cluster \
        --connector-config roleArn=arn:aws:iam::111122223333:role/AmazonEKSConnectorAgentRole,provider="OTHER" \
        --region AWS_REGION
   ```

   Output:

   ```
   {
       "cluster": {
           "name": "my-first-registered-cluster",
           "arn": "arn:aws:eks:region:111122223333:cluster/my-first-registered-cluster",
           "createdAt": 1627669203.531,
           "ConnectorConfig": {
               "activationId": "xxxxxxxxACTIVATION_IDxxxxxxxx",
               "activationCode": "xxxxxxxxACTIVATION_CODExxxxxxxx",
               "activationExpiry": 1627672543.0,
               "provider": "OTHER",
               "roleArn": "arn:aws:iam::111122223333:role/AmazonEKSConnectorAgentRole"
           },
           "status": "CREATING"
       }
   }
   ```

   You will use the `region`, `activationId`, and `activationCode` values in a later step\.

1. Download the Amazon EKS Connector YAML file\.

   ```
   curl -o eks-connector.yaml https://amazon-eks.s3.us-west-2.amazonaws.com/eks-connector/manifests/eks-connector/latest/eks-connector.yaml
   ```

1. Edit the Amazon EKS Connector YAML file to replace all references of `%AWS_REGION%`, `%EKS_ACTIVATION_ID%`, `%EKS_ACTIVATION_CODE%` with the `region`, `activationId`, and `activationCode` from the output of your registration command\.

   The following example command can replace these values\.

   ```
   sed -i '' "s~%AWS_REGION%~$AWS_REGION~g; s~%EKS_ACTIVATION_ID%~$EKS_ACTIVATION_ID~g; s~%EKS_ACTIVATION_CODE%~$(echo -n $EKS_ACTIVATION_CODE | base64)~g" eks-connector.yaml
   ```

**Important**  
Ensure that your activation code is of base64 format\.

------
#### [ AWS Management Console ]<a name="create-cluster-prerequisites"></a>

**Prerequisites**
+ Ensure that the Amazon EKS Connector service\-linked IAM role is created\. For more information, see [Creating the Amazon EKS Connector service\-linked IAM role](eks-connector.md#con-slr)\.
+ Ensure the Amazon EKS Connector agent role is created\. For more information, see [Creating the Amazon EKS Connector agent IAM role](eks-connector.md#create-con-agent-role)\.

**To register your Kubernetes cluster with the console\.**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Click **Add cluster** and select **Register** to bring up the configuration page\.

1. On the **Configure cluster** section, fill in the following fields:
   + **Name** – A unique name for your cluster\.
   + **Provider** – Click to display the drop\-down list of Kubernetes cluster providers\. If you do not know the provider, select Other\.
   + **EKS Connector role** – Select the role to use for connecting the cluster\. 

1. Select **Register cluster**\.

1. The Cluster overview page displays\. Click **Download YAML file** to download the manifest file to your local drive\. 
**Important**  
This is your only opportunity to download this file\. Do not navigate away from this page, as the link will not be accessible and you must deregister the cluster and start the steps from the beginning\.
The manifest file can only be used once for the registered cluster\. If you delete resources from the Kubernetes cluster, you must re\-register the cluster and obtain a new manifest file\.

   Continue to step 2 to apply the manifest file to your Kubernetes cluster\.

------

## Step 2: Applying the manifest file<a name="eks-connector-apply"></a>

Complete the connection by applying the Amazon EKS Connector manifest file to your Kubernetes cluster\. This must be done using the AWS CLI for both registration methods described aboove\. The Amazon EKS Connector registration expires if the manifest is not applied within three days\. If the cluster connection expires, the cluster must be deregistered before connecting the cluster again\.

1. In the cluster's native environment, you can now apply the updated manifest file with the following command:

   ```
   kubectl apply -f eks-connector.yaml
   ```

1. Once the Amazon EKS Connector manifest and role binding YAML files are applied to your Kubernetes cluster, confirm that the cluster is now connected\.

   ```
   aws eks describe-cluster \
        --name "my-first-registered-cluster" \
        --region AWS_REGION
   ```

   The output should include `status=ACTIVE`\.

1. To grant additional IAM users access to the Amazon EKS console to view the connected clusters, see [Granting access to a user to view a cluster](connector-grant-access.md)\. Your clusters will now be viewable in the AWS Management Console, as well as your connected [nodes](https://docs.aws.amazon.com/eks/latest/userguide/view-nodes.html) and [workloads](https://docs.aws.amazon.com/eks/latest/userguide/view-workloads.html)\.