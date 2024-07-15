# Set up the Amazon EKS Pod Identity Agent<a name="pod-id-agent-setup"></a>

Amazon EKS Pod Identity associations provide the ability to manage credentials for your applications, similar to the way that Amazon EC2 instance profiles provide credentials to Amazon EC2 instances\.

Amazon EKS Pod Identity provides credentials to your workloads with an additional *EKS Auth* API and an agent pod that runs on each node\.

## Considerations<a name="pod-id-agent-considerations"></a>
+ 

**`IPv6`**  
By default, the EKS Pod Identity Agent listens on an `IPv4` and `IPv6` address for pods to request credentials\. The agent uses the loopback \(localhost\) IP address `169.254.170.23` for `IPv4` and the localhost IP address `[fd00:ec2::23]` for `IPv6`\.

  If you disable `IPv6` addresses, or otherwise prevent localhost `IPv6` IP addresses, the agent can't start\. To start the agent on nodes that can't use `IPv6`, follow the steps in [Disable `IPv6` in the EKS Pod Identity Agent](#pod-id-agent-config-ipv6) to disable the `IPv6` configuration\.

## Creating the Amazon EKS Pod Identity Agent<a name="pod-id-agent-add-on-create"></a>

### Agent prerequisites<a name="pod-id-agent-prereqs"></a>
+ An existing Amazon EKS cluster\. To deploy one, see [Get started with Amazon EKS](getting-started.md)\. The cluster version and platform version must be the same or later than the versions listed in [EKS Pod Identity cluster versions](pod-identities.md#pod-id-cluster-versions)\.
+ The node role has permissions for the agent to do the `AssumeRoleForPodIdentity` action in the EKS Auth API\. You can use the [AWS managed policy: AmazonEKSWorkerNodePolicy](security-iam-awsmanpol.md#security-iam-awsmanpol-AmazonEKSWorkerNodePolicy) or add a custom policy similar to the following:

  ```
  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Effect": "Allow",
              "Action": [
                  "eks-auth:AssumeRoleForPodIdentity"
              ],
              "Resource": "*"
          }
      ]
  }
  ```

  This action can be limited by tags to restrict which roles can be assumed by pods that use the agent\.
+ The nodes can reach and download images from Amazon ECR\. The container image for the add\-on is in the registries listed in [Amazon container image registries](add-ons-images.md)\.

  Note that you can change the image location and provide `imagePullSecrets` for EKS add\-ons in the **Optional configuration settings** in the AWS Management Console, and in the `--configuration-values` in the AWS CLI\.
+ The nodes can reach the Amazon EKS Auth API\. For private clusters, the `eks-auth` endpoint in AWS PrivateLink is required\.

------
#### [ AWS Management Console ]

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to configure the EKS Pod Identity Agent add\-on for\.

1. Choose the **Add\-ons** tab\.

1. Choose **Get more add\-ons**\.

1. Select the box in the top right of the add\-on box for EKS Pod Identity Agent and then choose **Next**\.

1. On the **Configure selected add\-ons settings** page, select any version in the **Version** dropdown list\.

1. \(Optional\) Expand **Optional configuration settings** to enter additional configuration\. For example, you can provide an alternative container image location and `ImagePullSecrets`\. The JSON Schema with accepted keys is shown in **Add\-on configuration schema**\.

   Enter the configuration keys and values in **Configuration values**\.

1. Choose **Next**\.

1. Confirm that the EKS Pod Identity Agent pods are running on your cluster\.

   ```
   kubectl get pods -n kube-system | grep 'eks-pod-identity-agent'
   ```

   An example output is as follows\.

   ```
   eks-pod-identity-agent-gmqp7                                          1/1     Running   1 (24h ago)   24h
   eks-pod-identity-agent-prnsh                                          1/1     Running   1 (24h ago)   24h
   ```

   You can now use EKS Pod Identity associations in your cluster\. For more information, see [Assign an IAM role to a Kubernetes service account](pod-id-association.md)\.

------
#### [ AWS CLI ]

1. Run the following AWS CLI command\. Replace `my-cluster` with the name of your cluster\.

   ```
   aws eks create-addon --cluster-name my-cluster --addon-name eks-pod-identity-agent --addon-version v1.0.0-eksbuild.1
   ```
**Note**  
The EKS Pod Identity Agent doesn't use the `service-account-role-arn` for *IAM roles for service accounts*\. You must provide the EKS Pod Identity Agent with permissions in the node role\.

1. Confirm that the EKS Pod Identity Agent pods are running on your cluster\.

   ```
   kubectl get pods -n kube-system | grep 'eks-pod-identity-agent'
   ```

   An example output is as follows\.

   ```
   eks-pod-identity-agent-gmqp7                                          1/1     Running   1 (24h ago)   24h
   eks-pod-identity-agent-prnsh                                          1/1     Running   1 (24h ago)   24h
   ```

   You can now use EKS Pod Identity associations in your cluster\. For more information, see [Assign an IAM role to a Kubernetes service account](pod-id-association.md)\.

------

## Updating the Amazon EKS Pod Identity Agent<a name="pod-id-agent-update"></a>

Update the Amazon EKS type of the add\-on\. If you haven't added the Amazon EKS type of the add\-on to your cluster, see [Creating the Amazon EKS Pod Identity Agent](#pod-id-agent-add-on-create)\.

------
#### [ AWS Management Console ]

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to configure the EKS Pod Identity Agent add\-on for\.

1. Choose the **Add\-ons** tab\.

1. If a new version of the add\-on is available, the EKS Pod Identity Agent has an **Update version** button\. Select **Update version**\.

1. On the **Configure Amazon EKS Pod Identity Agent** page, select the new version in the **Version** dropdown list\.

1. Select **Save changes**\.

   It might take several seconds for the update to complete\. Then, confirm that the add\-on version was updated by checking the **Status**\.

------
#### [ AWS CLI ]

1. See which version of the add\-on is installed on your cluster\. Replace `my-cluster` with your cluster name\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name eks-pod-identity-agent --query "addon.addonVersion" --output text
   ```

   An example output is as follows\.

   ```
   v1.0.0-eksbuild.1
   ```

   You need to [create the add\-on](#pod-id-agent-add-on-create) before you can update it with this procedure\.

1. Update your add\-on using the AWS CLI\. If you want to use the AWS Management Console or `eksctl` to update the add\-on, see [Updating an add\-on](managing-add-ons.md#updating-an-add-on)\. Copy the command that follows to your device\. Make the following modifications to the command, as needed, and then run the modified command\.
   + Replace `my-cluster` with the name of your cluster\.
   + Replace *`v1.0.0-eksbuild.1`* with the your desired version\.
   + Replace *111122223333* with your account ID\.
   + Run the following command:

     ```
     aws eks update-addon --cluster-name my-cluster --addon-name eks-pod-identity-agent --addon-version v1.0.0-eksbuild.1'
     ```

     It might take several seconds for the update to complete\.

1. Confirm that the add\-on version was updated\. Replace `my-cluster` with the name of your cluster\.

   ```
   aws eks describe-addon --cluster-name my-cluster --addon-name eks-pod-identity-agent
   ```

   It might take several seconds for the update to complete\.

   An example output is as follows\.

   ```
   {
       "addon": {
           "addonName": "eks-pod-identity-agent",
           "clusterName": "my-cluster",
           "status": "ACTIVE",
           "addonVersion": "v1.0.0-eksbuild.1",
           "health": {
               "issues": []
           },
           "addonArn": "arn:aws:eks:region:111122223333:addon/my-cluster/eks-pod-identity-agent/74c33d2f-b4dc-8718-56e7-9fdfa65d14a9",
           "createdAt": "2023-04-12T18:25:19.319000+00:00",
           "modifiedAt": "2023-04-12T18:40:28.683000+00:00",
           "tags": {}
       }
   }
   ```

------

## EKS Pod Identity Agent configuration<a name="pod-id-agent-config"></a>

### Disable `IPv6` in the EKS Pod Identity Agent<a name="pod-id-agent-config-ipv6"></a>

------
#### [ AWS Management Console ]

**Disable `IPv6` in the AWS Management Console**

1. To disable `IPv6` in the EKS Pod Identity Agent, add the following configuration to the **Optional configuration settings** of the EKS Add\-on\.

   1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

   1. In the left navigation pane, select **Clusters**, and then select the name of the cluster that you want to configure the add\-on for\.

   1. Choose the **Add\-ons** tab\.

   1. Select the box in the top right of the EKS Pod Identity Agent add\-on box and then choose **Edit**\.

   1. On the **Configure EKS Pod Identity Agent** page:

      1. Select the **Version** that you'd like to use\. We recommend that you keep the same version as the previous step, and update the version and configuration in separate actions\.

      1. Expand the **Optional configuration settings**\.

      1. Enter the JSON key `"agent":` and value of a nested JSON object with a key `"additionalArgs":` in **Configuration values**\. The resulting text must be a valid JSON object\. If this key and value are the only data in the text box, surround the key and value with curly braces `{}`\. The following example shows network policy is enabled:

         ```
         {
             "agent": {
                 "additionalArgs": {
                     "-b": "169.254.170.23"
                 }
             }
         }
         ```

         This configuration sets the `IPv4` address to be the only address used by the agent\.

   1. To apply the new configuration by replacing the EKS Pod Identity Agent pods, choose **Save changes**\.

      Amazon EKS applies changes to the EKS Add\-ons by using a *rollout* of the Kubernetes `DaemonSet` for EKS Pod Identity Agent\. You can track the status of the rollout in the **Update history** of the add\-on in the AWS Management Console and with `kubectl rollout status daemonset/eks-pod-identity-agent --namespace kube-system`\.

      `kubectl rollout` has the following commands:

      ```
      $ kubectl rollout
                                  
      history  -- View rollout history
      pause    -- Mark the provided resource as paused
      restart  -- Restart a resource
      resume   -- Resume a paused resource
      status   -- Show the status of the rollout
      undo     -- Undo a previous rollout
      ```

      If the rollout takes too long, Amazon EKS will undo the rollout, and a message with the type of **Addon Update** and a status of **Failed** will be added to the **Update history** of the add\-on\. To investigate any issues, start from the history of the rollout, and run `kubectl logs` on a EKS Pod Identity Agent pod to see the logs of EKS Pod Identity Agent\.

1. If the new entry in the **Update history** has a status of **Successful**, then the rollout has completed and the add\-on is using the new configuration in all of the EKS Pod Identity Agent pods\.

------
#### [ AWS CLI ]

**Disable `IPv6` in the AWS CLI**
+ To disable `IPv6` in the EKS Pod Identity Agent, add the following configuration to the **configuration values** of the EKS Add\-on\.

  Run the following AWS CLI command\. Replace `my-cluster` with the name of your cluster and the IAM role ARN with the role that you are using\.

  ```
  aws eks update-addon --cluster-name my-cluster --addon-name eks-pod-identity-agent \
      --resolve-conflicts PRESERVE --configuration-values '{"agent":{"additionalArgs": { "-b": "169.254.170.23"}}}'
  ```

  This configuration sets the `IPv4` address to be the only address used by the agent\.

  Amazon EKS applies changes to the EKS Add\-ons by using a *rollout* of the Kubernetes DaemonSet for EKS Pod Identity Agent\. You can track the status of the rollout in the **Update history** of the add\-on in the AWS Management Console and with `kubectl rollout status daemonset/eks-pod-identity-agent --namespace kube-system`\.

  `kubectl rollout` has the following commands:

  ```
  kubectl rollout
                              
  history  -- View rollout history
  pause    -- Mark the provided resource as paused
  restart  -- Restart a resource
  resume   -- Resume a paused resource
  status   -- Show the status of the rollout
  undo     -- Undo a previous rollout
  ```

  If the rollout takes too long, Amazon EKS will undo the rollout, and a message with the type of **Addon Update** and a status of **Failed** will be added to the **Update history** of the add\-on\. To investigate any issues, start from the history of the rollout, and run `kubectl logs` on a EKS Pod Identity Agent pod to see the logs of EKS Pod Identity Agent\.

------