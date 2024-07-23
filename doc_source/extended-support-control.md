# Manage EKS extended support<a name="extended-support-control"></a>

Amazon EKS controls for Kubernetes version policy allows you to choose the end of standard support behavior for your EKS clusters\. With these controls you can decide which clusters should enter extended support and which clusters should be automatically upgraded at the end of standard support for a Kubernetes version\.

A minor version is under standard support in Amazon EKS for the first 14 months after it's released\. Once a version is past the end of standard support date, it enters extended support for the next 12 months\. Extended support allows you to stay at a specific Kubernetes version for longer at an additional cost per cluster hour\. You can enable or disable extended support for an EKS Cluster\. If you disable extended support, AWS will automatically upgrade your cluster to the next version at the end of standard support\. If you enable extended support, you can stay at the current version for an additional cost for a limited period of time\. Plan to regularly upgrade your Kubernetes cluster, even if you use extended support\. 

You can set the version policy for both new and existing clusters, using the `supportType` property\. There are two options that can be used to set the version support policy:
+ `STANDARD` — Your EKS cluster eligible for automatic upgrade at the end of standard support\. You will not incur extended support charges with this setting but you EKS cluster will automatically upgrade to the next supported Kubernetes version in standard support\.
+ `EXTENDED` — Your EKS cluster will enter into extended support once the Kubernetes version reaches end of standard support\. You will incur extended support charges with this setting\. You can upgrade your cluster to a standard supported Kubernetes version to stop incurring extended support charges\. Clusters running on extended support will be eligible for automatic upgrade at the end of extended support\.

Extended support is enabled by default for new clusters, and existing clusters\. You can view if extended support is enabled for a cluster in the AWS Management Console, or by using the AWS CLI\. 

**Important**  
You must enable extended support before the end of standard support\.

You can only set the version support policy for your clusters while its running on Kubernetes version in standard support\. Once the version enters extended support, you will not be able to change this setting until you are running on a version in standard support\. 

For example, if you have set your version support policy as `standard` then you will not be able to change this setting after the Kubernetes version running on your cluster reaches the end of standard support\. If you have set your version support policy as `extended` then you will not be able to change this setting after the Kubernetes version running on your cluster reaches end of standard support\. In order to change the version support policy setting, your cluster must be running on a standard supported Kubernetes version\.

## Enable extended support<a name="enable-extended-support"></a>

**Important**  
You must enable extended support before the end of standard support\. If you do not enable extended support, your cluster will be automatically upgraded\. 

**Enable EKS extended support \(AWS Console\)**

1. Navigate to your EKS cluster in the AWS Console\. Select the **Overview** tab on the **Cluster Info** page\.

1. In the **Kubernetes version settings** section, select **Manage**\. 

1. Select **Extended support** and then **Save changes**\.

**Enable EKS extended support \(AWS CLI\)**

1. Verify the AWS CLI is installed and you are logged in\. 

1. Determine the name of your EKS cluster\. 

1. Run the following command:

   ```
   aws eks update-cluster-config \ 
   --name <cluster-name> \
   --upgrade-policy supportType = EXTENDED
   ```

## Disable extended support<a name="disable-extended-support"></a>

**Important**  
You cannot disable extended support once your cluster has entered it\. You can only disable extended support for clusters on standard support\. 

**Disable EKS extended support \(AWS Console\)**

1. Navigate to your EKS cluster in the AWS Console\. Select the **Overview** tab on the **Cluster Info** page\.

1. In the **Kubernetes version setting** section, select **Manage**\. 

1. Select **Standard support** and then **Save changes**\.

**Disable EKS extended support \(AWS CLI\)**

1. Verify the AWS CLI is installed and you are logged in\. 

1. Determine the name of your EKS cluster\. 

1. Run the following command:

   ```
   aws eks update-cluster-config \ 
   --name <cluster-name> \
   --upgrade-policy supportType = STANDARD
   ```