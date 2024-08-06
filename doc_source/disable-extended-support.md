# Prevent increased cluster costs by disabling EKS extended support<a name="disable-extended-support"></a>

This topic describes how to set the *upgrade policy* of an EKS cluster to disable extended support\. The upgrade policy of an EKS cluster determines what happens when a cluster reaches the end of the standard *support period*\. If a cluster upgrade policy has extended support disabled, it will be automatically upgraded to the next Kubernetes version\. 

For more information about upgrade policies, see [View current cluster upgrade policy](view-upgrade-policy.md)\.

**Important**  
You cannot disable extended support once your cluster has entered it\. You can only disable extended support for clusters on standard support\.   
AWS recommends upgrading your cluster to a version in the standard support period\.

## Disable EKS extended support \(AWS Console\)<a name="disable-support-policy-console"></a>

1. Navigate to your EKS cluster in the AWS Console\. Select the **Overview** tab on the **Cluster Info** page\.

1. In the **Kubernetes version setting** section, select **Manage**\. 

1. Select **Standard support** and then **Save changes**\.

## Disable EKS extended support \(AWS CLI\)<a name="disable-support-policy-cli"></a>

1. Verify the AWS CLI is installed and you are logged in\. [Learn how to update and install the AWS CLI\.](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

1. Determine the name of your EKS cluster\. 

1. Run the following command:

   ```
   aws eks update-cluster-config \
   --name <cluster-name> \
   --upgrade-policy "supportType = STANDARD"
   ```
