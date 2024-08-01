# Add flexibility to plan Kubernetes version upgrades by enabling EKS extended support<a name="enable-extended-support"></a>

This topic describes how to set the *upgrade policy* of an EKS cluster to enable extended support\. The upgrade policy of an EKS cluster determines what happens when a cluster reaches the end of the standard *support period*\. If a cluster upgrade policy has extended support enabled, it will enter the extended support period at the end of the standard support period\. The cluster will not be automatically upgraded at the end of the standard support period\. 

Clusters actually in the *extended support period* incur higher costs\. If a cluster merely has the upgrade policy set to enable extended support, and is otherwise in the *standard support period*, it incurs standard costs\. 

EKS Clusters have the upgrade policy set to enable extended support by default\. 

For more information about upgrade policies, see [View current cluster upgrade policy](view-upgrade-policy.md)\.

**Important**  
If you want your cluster to stay on its current Kubernetes version to take advantage of the extended support period, you must enable the extended support upgrade policy before the end of standard support period\.  
If you do not enable extended support, your cluster will be automatically upgraded\. 

## Enable EKS extended support \(AWS Console\)<a name="enable-support-policy-console"></a>

1. Navigate to your EKS cluster in the AWS Console\. Select the **Overview** tab on the **Cluster Info** page\.

1. In the **Kubernetes version settings** section, select **Manage**\. 

1. Select **Extended support** and then **Save changes**\.

## Enable EKS extended support \(AWS CLI\)<a name="enable-support-policy-cli"></a>

1. Verify the AWS CLI is installed and you are logged in\. [Learn how to update and install the AWS CLI\.](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

1. Determine the name of your EKS cluster\. 

1. Run the following command:

   ```
   aws eks update-cluster-config \
   --name <cluster-name> \
   --upgrade-policy supportType = EXTENDED
   ```