# Tagging your Amazon EKS resources<a name="eks-using-tags"></a>

You can use *tags* to help you manage your Amazon EKS resources\. This topic provides an overview of the tags function and shows how you can create tags\.

**Topics**
+ [Tag basics](#tag-basics)
+ [Tagging your resources](#tag-resources)
+ [Tag restrictions](#tag-restrictions)
+ [Tagging your resources for billing](#tag-resources-for-billing)
+ [Working with tags using the console](#tag-resources-console)
+ [Working with tags using the CLI, API, or `eksctl`](#tag-resources-api-sdk)

**Note**  
Tags are a type of metadata that's separate from Kubernetes labels and annotations\. For more information about these other metadata types, see the following sections in the Kubernetes documentation:  
[Labels and Selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)
[Annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/)

## Tag basics<a name="tag-basics"></a>

A tag is a label that you assign to an AWS resource\. Each tag consists of a *key* and an optional *value*\.

With tags, you can categorize your AWS resources\. For example, you can categorize resources by purpose, owner, or environment\. When you have many resources of the same type, you can use the tags that you assigned to a specific resource to quickly identify that resource\. For example, you can define a set of tags for your Amazon EKS clusters to help you track each cluster's owner and stack level\. We recommend that you devise a consistent set of tag keys for each resource type\. You can then search and filter the resources based on the tags that you add\.

After you add a tag, you can edit tag keys and values or remove tags from a resource at any time\. If you delete a resource, any tags for the resource are also deleted\.

Tags don't have any semantic meaning to Amazon EKS and are interpreted strictly as a string of characters\. You can set the value of a tag to an empty string\. However, you can't set the value of a tag to null\. If you add a tag that has the same key as an existing tag on that resource, the new value overwrites the earlier value\.

If you use AWS Identity and Access Management \(IAM\), you can control which users in your AWS account have permission to manage tags\.

## Tagging your resources<a name="tag-resources"></a>

The following Amazon EKS resources support tags:
+ clusters
+ managed node groups
+ Fargate profiles

You can tag these resources using the following:
+ If you're using the Amazon EKS console, you can apply tags to new or existing resources at any time\. You can do this by using the **Tags** tab on the relevant resource page\. For more information, see [Working with tags using the console](#tag-resources-console)\.
+ If you're using `eksctl`, you can apply tags to resources when they're created using the `--tags` option\.
+ If you're using the AWS CLI, the Amazon EKS API, or an AWS SDK, you can apply tags to new resources using the `tags` parameter on the relevant API action\. You can apply tags to existing resources using the `TagResource` API action\. For more information, see [TagResource](https://docs.aws.amazon.com/eks/latest/APIReference/API_TagResource.html)\.

When you use some resource\-creating actions, you can also specify tags for the resource at the same time that you create it\. If tags can't be applied while the resource is being created, the resource fails to be created\. This mechanism ensures that resources that you intend to tag are either created with the tags that you specify or not created at all\. If you tag resources when you create them, you don't need to run custom tagging scripts after you create the resource\.

Tags don't propagate to other resources that are associated with the resource that you create\. For example, Fargate profile tags don't propagate to other resources that are associated with the Fargate profile, such as the Pods that are scheduled with it\.

## Tag restrictions<a name="tag-restrictions"></a>

The following restrictions apply to tags:
+ A maximum of 50 tags can be associated with a resource\.
+ Tag keys can't be repeated for one resource\. Each tag key must be unique, and can only have one value\.
+ Keys can be up to 128 characters long in UTF\-8\.
+ Values can be up to 256 characters long in UTF\-8\.
+ If multiple AWS services and resources use your tagging schema, limit the types of characters you use\. Some services might have restrictions on allowed characters\. Generally, allowed characters are letters, numbers, spaces, and the following characters: `+` `-` `=` `.` `_` `:` `/` `@`\.
+ Tag keys and values are case sensitive\.
+ Don't use `aws:`, `AWS:`, or any upper or lowercase combination of such as a prefix for either keys or values\. These are reserved only for AWS use\. You can't edit or delete tag keys or values with this prefix\. Tags with this prefix don't count against your tags\-per\-resource limit\.

## Tagging your resources for billing<a name="tag-resources-for-billing"></a>

When you apply tags to Amazon EKS clusters, you can use them for cost allocation in your **Cost & Usage Reports**\. The metering data in your **Cost & Usage Reports** shows usage across all of your Amazon EKS clusters\. For more information, see [AWS cost and usage report](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/billing-reports-costusage.html) in the *AWS Billing User Guide*\.

The AWS generated cost allocation tag, specifically `aws:eks:cluster-name`, lets you break down Amazon EC2 instance costs by individual Amazon EKS cluster in **Cost Explorer**\. However, this tag doesn't capture the control plane expenses\. The tag is automatically added to Amazon EC2 instances that participate in an Amazon EKS cluster\. This behavior happens regardless of whether the instances are provisioned using Amazon EKS managed node groups, Karpenter, or directly with Amazon EC2\. This specific tag doesn't count towards the 50 tags limit\. To use the tag, the account owner must activate it in the AWS Billing console or by using the API\. When an AWS Organizations management account owner activates the tag, it's also activated for all organization member accounts\.

You can also organize your billing information based on resources that have the same tag key values\. For example, you can tag several resources with a specific application name, and then organize your billing information\. That way, you can see the total cost of that application across several services\. For more information about setting up a cost allocation report with tags, see [The Monthly Cost Allocation Report](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/configurecostallocreport.html) in the *AWS Billing User Guide*\.

**Note**  
If you just enabled reporting, data for the current month is available for viewing after 24 hours\.

**Cost Explorer** is a reporting tool that's available as part of the AWS Free Tier\. You can use **Cost Explorer** to view charts of your Amazon EKS resources from the last 13 months\. You can also forecast how much you're likely to spend for the next three months\. You can see patterns in how much you spend on AWS resources over time\. For example, you can use it to identify areas that need further inquiry and see trends that you can use to understand your costs\. You also can specify time ranges for the data, and view time data by day or by month\.

## Working with tags using the console<a name="tag-resources-console"></a>

Using the Amazon EKS console, you can manage the tags that are associated with new or existing clusters and managed node groups\.

When you select a resource\-specific page in the Amazon EKS console, the page displays a list of those resources\. For example, if you select **Clusters** from the left navigation pane, the console displays a list of Amazon EKS clusters\. When you select a resource from one of these lists \(for example, a specific cluster\) that supports tags, you can view and manage its tags on the **Tags** tab\.

You can also use **Tag Editor** in the AWS Management Console, which provides a unified way to manage your tags\. For more information, see [Tagging your AWS resources with Tag Editor](https://docs.aws.amazon.com/ARG/latest/userguide/tag-editor.html) in the *AWS Tag Editor User Guide*\.

### Adding tags on a resource on creation<a name="adding-tags-creation"></a>

You can add tags to Amazon EKS clusters, managed node groups, and Fargate profiles when you create them\. For more information, see [Creating an Amazon EKS cluster](create-cluster.md)\.

### Adding and deleting tags on a resource<a name="adding-or-deleting-tags"></a>

You can add or delete the tags that are associated with your clusters directly from the resource's page\. 

**To add or delete a tag on an individual resource**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. On the navigation bar, select the AWS Region to use\.

1. In the left navigation pane, choose **Clusters**\.

1. Choose a specific cluster\.

1. Choose the **Tags** tab, and then choose **Manage tags**\.

1. On the **Manage tags** page, add or delete your tags as necessary\.
   + To add a tag, choose **Add tag**\. Then specify the key and value for each tag\.
   + To delete a tag, choose **Remove tag**\.

1. Repeat this process for each tag that you want to add or delete\.

1. Choose **Update** to finish\.

## Working with tags using the CLI, API, or `eksctl`<a name="tag-resources-api-sdk"></a>

Use the following AWS CLI commands or Amazon EKS API operations to add, update, list, and delete the tags for your resources\. You can only use `eksctl` to add tags while simultaneously creating the new resources with one command\.


**Tagging support for Amazon EKS resources**  

| Task | AWS CLI | AWS Tools for Windows PowerShell | API action | 
| --- | --- | --- | --- | 
|  Add or overwrite one or more tags\.  |  [https://docs.aws.amazon.com/cli/latest/reference/eks/tag-resource.html](https://docs.aws.amazon.com/cli/latest/reference/eks/tag-resource.html)  |  [https://docs.aws.amazon.com/powershell/latest/reference/items/Add-EKSResourceTag.html](https://docs.aws.amazon.com/powershell/latest/reference/items/Add-EKSResourceTag.html)  |  [https://docs.aws.amazon.com/eks/latest/APIReference/API_TagResource.html](https://docs.aws.amazon.com/eks/latest/APIReference/API_TagResource.html)  | 
|  Delete one or more tags\.  |  [https://docs.aws.amazon.com/cli/latest/reference/eks/untag-resource.html](https://docs.aws.amazon.com/cli/latest/reference/eks/untag-resource.html)  |  [https://docs.aws.amazon.com/powershell/latest/reference/items/Remove-EKSResourceTag.html](https://docs.aws.amazon.com/powershell/latest/reference/items/Remove-EKSResourceTag.html)  |  [https://docs.aws.amazon.com/eks/latest/APIReference/API_UntagResource.html](https://docs.aws.amazon.com/eks/latest/APIReference/API_UntagResource.html)  | 

The following examples show how to tag or untag resources using the AWS CLI\.

**Example 1: Tag an existing cluster**  
The following command tags an existing cluster\.

```
aws eks tag-resource --resource-arn resource_ARN --tags team=devs
```

**Example 2: Untag an existing cluster**  
The following command deletes a tag from an existing cluster\.

```
aws eks untag-resource --resource-arn resource_ARN --tag-keys tag_key
```

**Example 3: List tags for a resource**  
The following command lists the tags that are associated with an existing resource\.

```
aws eks list-tags-for-resource --resource-arn resource_ARN
```

When you use some resource\-creating actions, you can specify tags at the same time that you create the resource\. The following actions support specifying a tag when you create a resource\.


| Task | AWS CLI | AWS Tools for Windows PowerShell | API action | `eksctl` | 
| --- | --- | --- | --- | --- | 
|  Create a cluster  |  [https://docs.aws.amazon.com/cli/latest/reference/eks/create-cluster.html](https://docs.aws.amazon.com/cli/latest/reference/eks/create-cluster.html)  |  [https://docs.aws.amazon.com/powershell/latest/reference/items/New-EKSCluster.html](https://docs.aws.amazon.com/powershell/latest/reference/items/New-EKSCluster.html)  |  [https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html](https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html)  |  `create cluster`  | 
|  Create a managed node group\*  |  [https://docs.aws.amazon.com/cli/latest/reference/eks/create-nodegroup.html](https://docs.aws.amazon.com/cli/latest/reference/eks/create-nodegroup.html)  |  [https://docs.aws.amazon.com/powershell/latest/reference/items/New-EKSNodegroup.html](https://docs.aws.amazon.com/powershell/latest/reference/items/New-EKSNodegroup.html)  |  [https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateNodegroup.html](https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateNodegroup.html)  |  `create nodegroup`  | 
|  Create a Fargate profile  |  [https://docs.aws.amazon.com/cli/latest/reference/eks/create-fargate-profile.html](https://docs.aws.amazon.com/cli/latest/reference/eks/create-fargate-profile.html)  |  [https://docs.aws.amazon.com/powershell/latest/reference/items/New-EKSFargateProfile.html](https://docs.aws.amazon.com/powershell/latest/reference/items/New-EKSFargateProfile.html)  |  [https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateFargateProfile.html](https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateFargateProfile.html)  |  `create fargateprofile`  | 

\* If you want to also tag the Amazon EC2 instances when you create a managed node group, create the managed node group using a launch template\. For more information, see [Tagging Amazon EC2 instances](launch-templates.md#launch-template-tagging)\. If your instances already exist, you can manually tag the instances\. For more information, see [Tagging your resources](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Using_Tags.html#tag-resources) in the Amazon EC2 User Guide for Linux Instances\.