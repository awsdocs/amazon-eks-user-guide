# Connecting a cluster<a name="connecting-cluster"></a>

## Step 1: Registering the cluster<a name="connector-connecting"></a>

You can connect an external Kubernetes cluster to Amazon EKS with AWS CLI and the AWS Management Console\. This process involves two steps: registering the cluster with Amazon EKS and applying a YAML manifest file to enable connectivity\. To allow another user to view the cluster, follow the instructions in [Granting access to a user to view Kubernetes resources on a cluster](connector-grant-access.md)\.

You must have the following permissions to register a cluster:
+ `eks:RegisterCluster`
+ `ssm:CreateActivation`
+ `ssm:DeleteActivation`
+ `iam:PassRole`

------
#### [ eksctl ]

**Prerequisites**
+ `eksctl` version `0.68` or later must be installed\. To install or upgrade it, see [Getting started with `eksctl`](https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html)\.
+ The Amazon EKS Connector agent IAM role was created\. For more information, see [Connector IAM role](https://docs.aws.amazon.com/eks/latest/userguide/connector_IAM_role.html)\.

**To register your cluster with `eksctl`**

1. Register the cluster by providing a name, provider, and region\.

   ```
   eksctl register cluster --name my-cluster --provider my-provider --region region-code
   ```

   This creates two files on your local drive: `my-first-registered-cluster.yaml` and `eks-connector-binding.yaml` files\. These two files must be applied to the external cluster within three days, or the registration expires\.

1. In the cluster's native environment, apply the `eks-connector-binding.yaml` file:

   ```
   kubectl apply -f eks-connector-binding.yaml
   ```

------
#### [ AWS CLI ]

**Prerequisites**
+ AWS CLI must be installed\. To install or upgrade it, see [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)\.
+ Ensure the Amazon EKS Connector agent role was created\. \.

**To register your cluster with the AWS CLI**

1. For the Connector configuration, specify your Amazon EKS Connector agent IAM role\. For more information, see [Required IAM roles for Amazon EKS Connector](eks-connector.md#connector-iam-permissions)\.

   ```
   aws eks register-cluster \
        --name my-first-registered-cluster \
        --connector-config roleArn=arn:aws:iam::111122223333:role/AmazonEKSConnectorAgentRole,provider="OTHER" \
        --region AWS_REGION
   ```

   The example output is as follows\.

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

   You use the `region`, `activationId`, and `activationCode` values in a later step\.

1. Download the Amazon EKS Connector YAML file\.

   ```
   curl -O https://amazon-eks.s3.us-west-2.amazonaws.com/eks-connector/manifests/eks-connector/latest/eks-connector.yaml
   ```

1. Edit the Amazon EKS Connector YAML file to replace all references of `%AWS_REGION%`, `%EKS_ACTIVATION_ID%`, `%EKS_ACTIVATION_CODE%` with the `region`, `activationId`, and `activationCode` from the output of your registration command\.

   The following example command can replace these values\.

   ```
   sed -i "s~%AWS_REGION%~$AWS_REGION~g; s~%EKS_ACTIVATION_ID%~$EKS_ACTIVATION_ID~g; s~%EKS_ACTIVATION_CODE%~$(echo -n $EKS_ACTIVATION_CODE | base64)~g" eks-connector.yaml
   ```

**Important**  
Ensure that your activation code is in the base64 format\.

------
#### [ AWS Management Console ]<a name="connecting-cluster-prerequisites"></a>

**Prerequisites**
+ Ensure the Amazon EKS Connector agent role was created\. \.

**To register your Kubernetes cluster with the console\.**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose **Add cluster** and select **Register** to bring up the configuration page\.

1. On the **Configure cluster** section, fill in the following fields:
   + **Name** – A unique name for your cluster\.
   + **Provider** – Choose to display the dropdown list of Kubernetes cluster providers\. If you don't know the specific provider, select Other\.
   + **EKS Connector role** – Select the role to use for connecting the cluster\. 

1. Select **Register cluster**\.

1. The Cluster overview page displays\. Choose **Download YAML file** to download the manifest file to your local drive\. 
**Important**  
This is your only opportunity to download this file\. Don't navigate away from this page, as the link will not be accessible and you must deregister the cluster and start the steps from the beginning\.
The manifest file can be used only once for the registered cluster\. If you delete resources from the Kubernetes cluster, you must re\-register the cluster and obtain a new manifest file\.

   Continue to the next step to apply the manifest file to your Kubernetes cluster\.

------

## Step 2: Applying the manifest file<a name="eks-connector-apply"></a>

Complete the connection by applying the Amazon EKS Connector manifest file to your Kubernetes cluster\. To do this, you must use the AWS CLI or `eksctl` for the registration methods described previously\. If the manifest is applied within three days, the Amazon EKS Connector registration expires\. If the cluster connection expires, the cluster must be deregistered before connecting the cluster again\.

1. In the native environment of the cluster, you can apply the updated manifest file by running the following command:

   ```
   kubectl apply -f eks-connector.yaml
   ```

1. After the Amazon EKS Connector manifest and role binding YAML files are applied to your Kubernetes cluster, confirm that the cluster is now connected\.

   ```
   aws eks describe-cluster \
        --name "my-first-registered-cluster" \
        --region AWS_REGION
   ```

   The output should include `status=ACTIVE`\.

1. You can now add Tags to your cluster \(optional\)\. See [Tagging your Amazon EKS resources for more information\.](https://docs.aws.amazon.com/eks/latest/userguide/eks-using-tags.html)

To grant additional IAM users access to the Amazon EKS console to view Kubernetes resources in a connected cluster, see [Granting access to a user to view Kubernetes resources on a cluster](connector-grant-access.md)\.