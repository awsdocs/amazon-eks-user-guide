# Disable `IPv6` in the EKS Pod Identity Agent<a name="pod-id-agent-config-ipv6"></a>

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