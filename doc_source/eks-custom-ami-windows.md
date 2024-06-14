--------

 **Help improve this page** 

--------

--------

Want to contribute to this user guide? Scroll to the bottom of this page and select **Edit this page on GitHub**\. Your contributions will help make our user guide better for everyone\.

--------

# Creating custom Amazon EKS optimized Windows AMIs<a name="eks-custom-ami-windows"></a>

You can use EC2 Image Builder to create custom Amazon EKS optimized Windows AMIs with one of the following options:

**Important**  
The following **Amazon\-managed** components for `eks` include patches for `CVE-2023-5528`\.  
 `1.24.3` and higher
 `1.25.2` and higher
 `1.26.2` and higher
 `1.27.0` and higher
 `1.28.0` and higher

## Using an Amazon EKS optimized Windows AMI as a base<a name="custom-windows-ami-as-base"></a>

This option is the recommended way to build your custom Windows AMIs\. The Amazon EKS optimized Windows AMIs we provide are more frequently updated than the Amazon\-managed build component\.

1. Start a new Image Builder recipe\.

   1. Open the EC2 Image Builder console at [https://console\.aws\.amazon\.com/imagebuilder](https://console.aws.amazon.com/imagebuilder)\.

   1. In the left navigation pane, choose **Image recipes**\.

   1. Choose **Create image recipe**\.

1. In the **Recipe details** section, enter a \*Name \* and **Version**\.

1. Specify the ID of the Amazon EKS optimized Windows AMI in the **Base image** section\.

   1. Choose **Enter custom AMI ID**\.

   1. Enter the custom **AMI ID**\. If the AMI ID isn’t found, make sure that the AWS Region for the AMI ID matches the AWS Region shown in the upper right of your console\.

1. \(Optional\) To get the latest security updates, add the `update-windows` component in the \*Build components \- \* section\.

   1. From the dropdown list to the right of the **Find components by name** search box, choose **Amazon\-managed**\.

   1. In the \*Find components by name \* search box, enter ` `update-windows.` Select the check box of the ** `update-windows` ** search result\. This component includes the latest Windows patches for the operating system\.

1. Complete the remaining image recipe inputs with your required configurations\. For more information, see [Create a new image recipe version \(console\)](https://docs.aws.amazon.com/) in the Image Builder User Guide\.

1. Choose **Create recipe**\.

1. Use the new image recipe in a new or existing image pipeline\. Once your image pipeline runs successfully, your custom AMI will be listed as an output image and is ready for use\. For more information, see [Create an image pipeline using the EC2 Image Builder console wizard](https://docs.aws.amazon.com/imagebuilder/latest/userguide/start-build-image-pipeline.html)\.

## Using the Amazon\-managed build component<a name="custom-windows-ami-build-component"></a>

When using an Amazon EKS optimized Windows AMI as a base isn’t viable, you can use the Amazon\-managed build component instead\. This option may lag behind the most recent supported Kubernetes versions\.

1. Start a new Image Builder recipe\.

   1. Open the EC2 Image Builder console at [https://console\.aws\.amazon\.com/imagebuilder](https://console.aws.amazon.com/imagebuilder)\.

   1. In the left navigation pane, choose **Image recipes**\.

   1. Choose **Create image recipe**\.

1. In the **Recipe details** section, enter a **Name** and **Version**\.

1. Determine which option you will be using to create your custom AMI in the **Base image** section:
   +  **Select managed images** – Choose **Windows** for your **Image Operating System \(OS\)**\. Then choose one of the following options for **Image origin**\.
     +  **Images owned by me** – For **Image name**, choose the ARN of your own image with your own license\. The image that you provide can’t already have Amazon EKS components installed\.
   +  **Enter custom AMI ID** – For AMI ID, enter the ID for your AMI with your own license\. The image that you provide can’t already have Amazon EKS components installed\.

1. In the **Build components \- Windows** section, do the following:

   1. From the dropdown list to the right of the **Find components by name** search box, choose **Amazon\-managed**\.

   1. In the **Find components by name** search box, enter ` `eks.` Select the check box of the ** `eks-optimized-ami-windows` ** search result, even though the result returned may not be the version that you want\.In the **Find components by name** search box, enter ` update-windows .` Select the check box of the **update\-windows** search result\. This component includes the latest Windows patches for the operating system\.

1. In the **Selected components** section, do the following:

   1. Choose **Versioning options** for ** `eks-optimized-ami-windows` **\.

   1. Choose **Specify component version**\.
**Note**  
The following `eks-optimized-ami-windows` build component versions require `eksctl` version `0.129` or lower:
      +  `1.24.0` 

1. Complete the remaining image recipe inputs with your required configurations\. For more information, see [Create a new image recipe version \(console\)](https://docs.aws.amazon.com/) in the Image Builder User Guide\.

1. Choose **Create recipe**\.

1. Use the new image recipe in a new or existing image pipeline\. Once your image pipeline runs successfully, your custom AMI will be listed as an output image and is ready for use\. For more information, see [Create an image pipeline using the EC2 Image Builder console wizard](https://docs.aws.amazon.com/imagebuilder/latest/userguide/start-build-image-pipeline.html)\.

## Retrieving information about `eks-optimized-ami-windows` component versions<a name="custom-windows-ami-component-versions"></a>

1. Open the EC2 Image Builder console at [https://console\.aws\.amazon\.com/imagebuilder](https://console.aws.amazon.com/imagebuilder)\.

1. In the left navigation pane, choose **Components**\.

1. From the dropdown list to the right of the **Find components by name** search box, change **Owned by me** to **Quick start \(Amazon\-managed\)**\.

1. In the **Find components by name** box, enter ` `eks.` \(Optional\) If you are using a recent version, sort the \*Version \* column in descending order by choosing it twice\.Choose the ** `eks-optimized-ami-windows` ** link with a desired version\.

The **Description** in the resulting page shows the specific information\.