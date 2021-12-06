# Amazon EKS optimized Windows AMI<a name="eks-custom-ami-windows"></a>

You can use Amazon EC2 Image Builder to create custom Amazon EKS optimized Windows AMIs\. You must create your own Image Builder recipe\. For more information, see [Create image recipes and versions](https://docs.aws.amazon.com/imagebuilder/latest/userguide/create-image-recipes.html) in the *EC2 Image Builder User Guide*\. When creating a recipe and selecting a **Source image**, you have the following options:
+  **Select managed images** – If you select this option, you can choose one of the following options for **Image origin**\.
  + **Quick start \(Amazon\-managed\)** – In the Image name drop\-down, select an [Amazon EKS supported Windows Server version](eks-optimized-windows-ami.md)\.
  + **Images owned by me** – For **Image name**, select the ARN of your own image with your own license\. The image that you provide can't already have Amazon EKS components installed\.
+ **Enter custom AMI ID** – For **AMI ID**, enter the ID for your AMI with your own license\. The image that you provide can't already have Amazon EKS components installed\.

In the search box under **Build components \- Windows**, select **Amazon\-managed** in the dropdown list and then search on `eks`\. Select the **eks\-optimized\-ami\-windows** search result, even though the result returned may not be the version that you want\. Under **Selected components**, select **Versioning options**, then select **Specify component version**\. Enter `<version>.x`, replacing `<version>` \(including `<>`\) with a [supported Kubernetes version](kubernetes-versions.md)\. If you enter 1\.20\.x as the component version, your Image Builder pipeline builds an AMI with the latest 1\.20\.x `kubelet` version\. 

To determine which `kubelet` and Docker versions are installed with the component, select **Components** in the left navigation\. Under **Components**, change **Owned by me** to **Quick start \(Amazon\-managed\)**\. In the **Find components by name** box, enter `eks`\. The search results show the `kubelet` and Docker version in the component returned for each supported Kubernetes version\. The components go through functional testing on the Amazon EKS supported Windows versions\. Any other Windows versions are not supported and might not be compatible with the component\. 

You should also include the `update-windows` component for the latest Windows patches for the operating system\.

When you create a Windows node, there is a script on the node that allows for configuration\. Depending on your setup, this script can be found on the node at a location similar to: `\Program Files\Amazon\EKS\EKSBootstrap.ps1`\. The script includes the following parameters:
+ `-EKSClusterName` – Specifies the Amazon EKS cluster name for this worker node to join\.
+ `-KubeletExtraArgs` – Specifies extra arguments for `kubelet` \(optional\)\.
+ `-KubeProxyExtraArgs` – Specifies extra arguments for `kube-proxy` \(optional\)\.
+ `-APIServerEndpoint` – Specifies the Amazon EKS cluster API server endpoint \(optional\)\. Only valid when used with `-Base64ClusterCA`\. Bypasses calling `Get-EKSCluster`\.
+ `-Base64ClusterCA` – Specifies the base64 encoded cluster CA content \(optional\)\. Only valid when used with `-APIServerEndpoint`\. Bypasses calling `Get-EKSCluster`\.
+ `-DNSClusterIP` – Overrides the IP address to use for DNS queries within the cluster \(optional\)\. Defaults to `10.100.0.10` or `172.20.0.10` based on the IP address of the primary interface\.