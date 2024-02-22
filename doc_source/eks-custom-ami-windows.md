# Creating custom Amazon EKS optimized Windows AMIs<a name="eks-custom-ami-windows"></a>

You can use EC2 Image Builder to create custom Amazon EKS optimized Windows AMIs with one of the following options:
+ [Using an Amazon EKS optimized Windows AMI as a base](#custom-windows-ami-as-base)
+ [Using the Amazon\-managed build component](#custom-windows-ami-build-component)

With both methods, you must create your own Image Builder recipe\. For more information, see [Create a new version of an image recipe](https://docs.aws.amazon.com/imagebuilder/latest/userguide/create-image-recipes.html) in the Image Builder User Guide\.

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

1. In the **Recipe details** section, enter a **Name ** and **Version**\.

1. Specify the ID of the Amazon EKS optimized Windows AMI in the **Base image** section\.

   1. Choose **Enter custom AMI ID**\.

   1. Retrieve the AMI ID for the Windows OS version that you require\. For more information, see [Retrieving Amazon EKS optimized Windows AMI IDs](retrieve-windows-ami-id.md)\.

   1. Enter the custom **AMI ID**\. If the AMI ID isn't found, make sure that the AWS Region for the AMI ID matches the AWS Region shown in the upper right of your console\. 

1. \(Optional\) To get the latest security updates, add the `update-windows` component in the **Build components \- ** section\.

   1. From the dropdown list to the right of the **Find components by name** search box, choose **Amazon\-managed**\.

   1. In the **Find components by name ** search box, enter **`update-windows`**\.

   1. Select the check box of the **`update-windows`** search result\. This component includes the latest Windows patches for the operating system\.

1. Complete the remaining image recipe inputs with your required configurations\. For more information, see [Create a new image recipe version \(console\)](https://docs.aws.amazon.com/imagebuilder/latest/userguide/create-image-recipes.html#create-image-recipe-version-console) in the Image Builder User Guide\.

1. Choose **Create recipe**\.

1. Use the new image recipe in a new or existing image pipeline\. Once your image pipeline runs successfully, your custom AMI will be listed as an output image and is ready for use\. For more information, see [Create an image pipeline using the EC2 Image Builder console wizard](https://docs.aws.amazon.com/imagebuilder/latest/userguide/start-build-image-pipeline.html)\.

## Using the Amazon\-managed build component<a name="custom-windows-ami-build-component"></a>

When using an Amazon EKS optimized Windows AMI as a base isn't viable, you can use the Amazon\-managed build component instead\. This option may lag behind the most recent supported Kubernetes versions\.

1. Start a new Image Builder recipe\.

   1. Open the EC2 Image Builder console at [https://console\.aws\.amazon\.com/imagebuilder](https://console.aws.amazon.com/imagebuilder)\.

   1. In the left navigation pane, choose **Image recipes**\.

   1. Choose **Create image recipe**\.

1. In the **Recipe details** section, enter a **Name** and **Version**\.

1. Determine which option you will be using to create your custom AMI in the **Base image** section:
   + **Select managed images** – Choose **Windows** for your **Image Operating System \(OS\)**\. Then choose one of the following options for **Image origin**\.
     + **Quick start \(Amazon\-managed\)** – In the **Image name** dropdown, choose an Amazon EKS supported Windows Server version\. For more information, see [Amazon EKS optimized Windows AMIs](eks-optimized-windows-ami.md)\.
     + **Images owned by me** – For **Image name**, choose the ARN of your own image with your own license\. The image that you provide can't already have Amazon EKS components installed\.
   + **Enter custom AMI ID** – For AMI ID, enter the ID for your AMI with your own license\. The image that you provide can't already have Amazon EKS components installed\.

1. In the **Build components \- Windows** section, do the following:

   1. From the dropdown list to the right of the **Find components by name** search box, choose **Amazon\-managed**\.

   1. In the **Find components by name** search box, enter **`eks`**\.

   1. Select the check box of the **`eks-optimized-ami-windows`** search result, even though the result returned may not be the version that you want\.

   1. In the **Find components by name** search box, enter **`update-windows`** \.

   1. Select the check box of the **update\-windows** search result\. This component includes the latest Windows patches for the operating system\.

1. In the **Selected components** section, do the following:

   1. Choose **Versioning options** for **`eks-optimized-ami-windows`**\.

   1. Choose **Specify component version**\.

   1. In the **Component Version** field, enter *** `version.x` ***, replacing *`version`* with a supported Kubernetes version\. Entering an * `x`* for part of the version number indicates to use the latest component version that also aligns with the part of the version you explicitly define\. Pay attention to the console output as it will advise you on whether your desired version is available as a managed component\. Keep in mind that the most recent Kubernetes versions may not be available for the build component\. For more information about available versions, see [Retrieving information about `eks-optimized-ami-windows` component versions](#custom-windows-ami-component-versions)\.
**Note**  
The following `eks-optimized-ami-windows` build component versions require `eksctl` version `0.129` or lower:  
`1.24.0` 

1. Complete the remaining image recipe inputs with your required configurations\. For more information, see [Create a new image recipe version \(console\)](https://docs.aws.amazon.com/imagebuilder/latest/userguide/create-image-recipes.html#create-image-recipe-version-console) in the Image Builder User Guide\.

1. Choose **Create recipe**\.

1. Use the new image recipe in a new or existing image pipeline\. Once your image pipeline runs successfully, your custom AMI will be listed as an output image and is ready for use\. For more information, see [Create an image pipeline using the EC2 Image Builder console wizard](https://docs.aws.amazon.com/imagebuilder/latest/userguide/start-build-image-pipeline.html)\.

## Retrieving information about `eks-optimized-ami-windows` component versions<a name="custom-windows-ami-component-versions"></a>

You can retrieve specific information regarding what is installed with each component\. For example, you can verify what `kubelet` version is installed\. The components go through functional testing on the Amazon EKS supported Windows operating systems versions\. For more information, see [Release calendar](eks-optimized-windows-ami.md#windows-ami--release-calendar)\. Any other Windows OS versions that aren't listed as supported or have reached end of support might not be compatible with the component\.

1. Open the EC2 Image Builder console at [https://console\.aws\.amazon\.com/imagebuilder](https://console.aws.amazon.com/imagebuilder)\.

1. In the left navigation pane, choose **Components**\.

1. From the dropdown list to the right of the **Find components by name** search box, change **Owned by me** to **Quick start \(Amazon\-managed\)**\.

1. In the **Find components by name** box, enter **`eks`**\.

1. \(Optional\) If you are using a recent version, sort the **Version ** column in descending order by choosing it twice\.

1. Choose the **`eks-optimized-ami-windows`** link with a desired version\.

The **Description** in the resulting page shows the specific information\.