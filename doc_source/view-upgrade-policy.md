# View current cluster upgrade policy<a name="view-upgrade-policy"></a>

The **cluster upgrade policy** determines what happens to your cluster when it leaves the standard support period\. If your upgrade policy is `EXTENDED`, the cluster will not be automatically upgraded, and will enter extended support\. If your upgrade policy is `STANDARD`, it will be automatically upgraded\.

Amazon EKS controls for Kubernetes version policy allows you to choose the end of standard support behavior for your EKS clusters\. With these controls you can decide which clusters should enter extended support and which clusters should be automatically upgraded at the end of standard support for a Kubernetes version\.

A minor version is under standard support in Amazon EKS for the first 14 months after it's released\. Once a version is past the end of standard support date, it enters extended support for the next 12 months\. Extended support allows you to stay at a specific Kubernetes version for longer at an additional cost per cluster hour\. You can enable or disable extended support for an EKS Cluster\. If you disable extended support, AWS will automatically upgrade your cluster to the next version at the end of standard support\. If you enable extended support, you can stay at the current version for an additional cost for a limited period of time\. Plan to regularly upgrade your Kubernetes cluster, even if you use extended support\. 

You can set the version policy for both new and existing clusters, using the `supportType` property\. There are two options that can be used to set the version support policy:
+ `STANDARD` — Your EKS cluster eligible for automatic upgrade at the end of standard support\. You will not incur extended support charges with this setting but you EKS cluster will automatically upgrade to the next supported Kubernetes version in standard support\.
+ `EXTENDED` — Your EKS cluster will enter into extended support once the Kubernetes version reaches end of standard support\. You will incur extended support charges with this setting\. You can upgrade your cluster to a standard supported Kubernetes version to stop incurring extended support charges\. Clusters running on extended support will be eligible for automatic upgrade at the end of extended support\.

Extended support is enabled by default for new clusters, and existing clusters\. You can view if extended support is enabled for a cluster in the AWS Management Console, or by using the AWS CLI\. 

**Important**  
If you want your cluster to stay on its current Kubernetes version to take advantage of the extended support period, you must enable the extended support upgrade policy before the end of standard support period\.

You can only set the version support policy for your clusters while its running on Kubernetes version in standard support\. Once the version enters extended support, you will not be able to change this setting until you are running on a version in standard support\. 

For example, if you have set your version support policy as `standard` then you will not be able to change this setting after the Kubernetes version running on your cluster reaches the end of standard support\. If you have set your version support policy as `extended` then you will not be able to change this setting after the Kubernetes version running on your cluster reaches end of standard support\. In order to change the version support policy setting, your cluster must be running on a standard supported Kubernetes version\.

## View cluster upgrade policy \(AWS Console\)<a name="view-period-console"></a>

1. Navigate to the **Clusters** page in the EKS section of the AWS Console\. Confirm the console is set to the same AWS region as the cluster you want to review\. 

1. Review the **Upgrade Policy** column\. If the value is **Standard Support**, your cluster will not enter extended support\. If the value is **Extended Support**, your cluster will enter extended support\.

## View cluster upgrade policy \(AWS CLI\)<a name="view-period-cli"></a>

1. Verify the AWS CLI is installed and you are logged in\. [Learn how to update and install the AWS CLI\.](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

1. Determine the name of your EKS cluster\. Set the CLI to the same AWS region as your EKS cluster\. 

1. Run the following command:

   ```
   aws eks describe-cluster \
   --name <cluster-name> \
   --query "cluster.upgradePolicy.supportType"
   ```

1. If the value is `STANDARD`, your cluster will not enter extended support\. If the value is `EXTENDED`, your cluster will enter extended support\.