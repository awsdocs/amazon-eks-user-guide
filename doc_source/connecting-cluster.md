# Connecting an external cluster<a name="connecting-cluster"></a>

You can connect an external Kubernetes cluster to Amazon EKS by using multiple methods in the following process\. This process involves two steps: Registering the cluster with Amazon EKS and installing the `eks-connector` agent in the cluster\.

**Important**  
You must complete the second step within 3 days of completing the first step, before the registration expires\.

## Connector methods<a name="connector-methods"></a>

Not all of the methods to install the agent can be used after each of the methods to register the cluster\. The following table lists each of the registration method and which methods for installing the agent can be used\.


| Step | Methods | 
| --- | --- | 
| Register the cluster | AWS Management Console | AWS Command Line Interface | eksctl | 
| Install the agent | Helm, YAML manifests | Helm, YAML manifests | YAML manifests | 

## Prerequisites<a name="connector-prereqs"></a><a name="connecting-cluster-prerequisites"></a>
+ Ensure the Amazon EKS Connector agent role was created\. Follow the steps in [Creating the Amazon EKS connector agent role](connector_IAM_role.md#create-connector-role)\.
+ You must have the following permissions to register a cluster:
  + `eks:RegisterCluster`
  + `ssm:CreateActivation`
  + `ssm:DeleteActivation`
  + `iam:PassRole`

## Step 1: Registering the cluster<a name="connector-connecting"></a>

------
#### [ AWS CLI ]

**Prerequisites**
+ AWS CLI must be installed\. To install or upgrade it, see [Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)\.

**To register your cluster with the AWS CLI**
+ For the Connector configuration, specify your Amazon EKS Connector agent IAM role\. For more information, see [Required IAM roles for Amazon EKS Connector](eks-connector.md#connector-iam-permissions)\.

  ```
  aws eks register-cluster \
       --name my-first-registered-cluster \
       --connector-config roleArn=arn:aws:iam::111122223333:role/AmazonEKSConnectorAgentRole,provider="OTHER" \
       --region aws-region
  ```

  An example output is as follows\.

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

  You use the `aws-region`, `activationId`, and `activationCode` values in the next step\.

------
#### [ AWS Management Console ]

**To register your Kubernetes cluster with the console\.**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. Choose **Add cluster** and select **Register** to bring up the configuration page\.

1. On the **Configure cluster** section, fill in the following fields:
   + **Name** – A unique name for your cluster\.
   + **Provider** – Choose to display the dropdown list of Kubernetes cluster providers\. If you don't know the specific provider, select **Other**\.
   + **EKS Connector role** – Select the role to use for connecting the cluster\. 

1. Select **Register cluster**\.

1. The Cluster overview page displays\. If you want to use the Helm chart, copy the `helm install` command and continue to the next step\. If you want to use the YAML manifest, choose **Download YAML file** to download the manifest file to your local drive\. 
**Important**  
This is your only opportunity to copy the `helm install` command or download this file\. Don't navigate away from this page, as the link will not be accessible and you must deregister the cluster and start the steps from the beginning\.
The command or manifest file can be used only once for the registered cluster\. If you delete resources from the Kubernetes cluster, you must re\-register the cluster and obtain a new manifest file\.

   Continue to the next step to apply the manifest file to your Kubernetes cluster\.

------
#### [ eksctl ]

**Prerequisites**
+ `eksctl` version `0.68` or later must be installed\. To install or upgrade it, see [Getting started with Amazon EKS – `eksctl`](getting-started-eksctl.md)\.

**To register your cluster with `eksctl`**

1. Register the cluster by providing a name, provider, and region\.

   ```
   eksctl register cluster --name my-cluster --provider my-provider --region region-code
   ```

   Example output:

   ```
   2021-08-19 13:47:26 [ℹ]  creating IAM role "eksctl-20210819194112186040"
   2021-08-19 13:47:26 [ℹ]  registered cluster "<name>" successfully
   2021-08-19 13:47:26 [ℹ]  wrote file eks-connector.yaml to <current directory>
   2021-08-19 13:47:26 [ℹ]  wrote file eks-connector-clusterrole.yaml to <current directory>
   2021-08-19 13:47:26 [ℹ]  wrote file eks-connector-console-dashboard-full-access-group.yaml to <current directory>
   2021-08-19 13:47:26 [!]  note: "eks-connector-clusterrole.yaml" and "eks-connector-console-dashboard-full-access-group.yaml" give full EKS Console access to IAM identity "<aws-arn>", edit if required; read https://eksctl.io/usage/eks-connector for more info
   2021-08-19 13:47:26 [ℹ]  run `kubectl apply -f eks-connector.yaml,eks-connector-clusterrole.yaml,eks-connector-console-dashboard-full-access-group.yaml` before expiry> to connect the cluster
   ```

   This creates files on your local computer\. These files must be applied to the external cluster within 3 days, or the registration expires\.

1. In a terminal that can access the cluster, apply the `eks-connector-binding.yaml` file:

   ```
   kubectl apply -f eks-connector-binding.yaml
   ```

------

## Step 2: Installing the `eks-connector` agent<a name="eks-connector-apply"></a>

------
#### [ Helm chart ]

1. If you used the AWS CLI in the previous step, replace the `ACTIVATION_CODE` and `ACTIVATION_ID` in the following command with the `activationId`, and `activationCode` values respectively\. Replace the `aws-region` with the AWS Region that you used in the previous step\. Then run the command to install the `eks-connector` agent on the registering cluster:

   ```
   $ helm install eks-connector \
     --namespace eks-connector \
     oci://public.ecr.aws/eks-connector/eks-connector-chart \
     --set eks.activationCode=ACTIVATION_CODE \
     --set eks.activationId=ACTIVATION_ID \
     --set eks.agentRegion=aws-region
   ```

   If you used the AWS Management Console in the previous step, use the command that you copied from the previous step that has these values filled in\.

1. Check the healthiness of the installed `eks-connector` deployment and wait for the status of the registered cluster in Amazon EKS to be `ACTIVE`\.

------
#### [ YAML manifest ]

Complete the connection by applying the Amazon EKS Connector manifest file to your Kubernetes cluster\. To do this, you must use the methods described previously\. If the manifest isn't applied within three days, the Amazon EKS Connector registration expires\. If the cluster connection expires, the cluster must be deregistered before connecting the cluster again\.

1. Download the Amazon EKS Connector YAML file\.

   ```
   curl -O https://amazon-eks.s3.us-west-2.amazonaws.com/eks-connector/manifests/eks-connector/latest/eks-connector.yaml
   ```

1. Edit the Amazon EKS Connector YAML file to replace all references of `%AWS_REGION%`, `%EKS_ACTIVATION_ID%`, `%EKS_ACTIVATION_CODE%` with the `aws-region`, `activationId`, and `activationCode` from the output of the previous step\.

   The following example command can replace these values\.

   ```
   sed -i "s~%AWS_REGION%~$aws-region~g; s~%EKS_ACTIVATION_ID%~$EKS_ACTIVATION_ID~g; s~%EKS_ACTIVATION_CODE%~$(echo -n $EKS_ACTIVATION_CODE | base64)~g" eks-connector.yaml
   ```
**Important**  
Ensure that your activation code is in the base64 format\.

1. In a terminal that can access the cluster, you can apply the updated manifest file by running the following command:

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

1. \(Optional\) Add tags to your cluster\. For more information, see [Tagging your Amazon EKS resources](eks-using-tags.md)\.

------

## Next steps<a name="eks-connector-next"></a>

If you have any issues with these steps, see [Troubleshooting issues in Amazon EKS Connector](troubleshooting-connector.md)\.

To grant additional [IAM principals](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) access to the Amazon EKS console to view Kubernetes resources in a connected cluster, see [Granting access to an IAM principal to view Kubernetes resources on a cluster](connector-grant-access.md)\.