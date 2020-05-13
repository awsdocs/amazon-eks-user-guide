# Tagging your Amazon EKS resources<a name="eks-using-tags"></a>

To help you manage your Amazon EKS resources, you can assign your own metadata to each resource in the form of *tags*\. This topic describes tags and shows you how to create them\.

**Topics**
+ [Tag basics](#tag-basics)
+ [Tagging your resources](#tag-resources)
+ [Tag restrictions](#tag-restrictions)
+ [Working with tags using the console](#tag-resources-console)
+ [Working with tags using the CLI or API](#tag-resources-api-sdk)

## Tag basics<a name="tag-basics"></a>

A tag is a label that you assign to an AWS resource\. Each tag consists of a *key* and an optional *value*, both of which you define\.

Tags enable you to categorize your AWS resources by, for example, purpose, owner, or environment\. When you have many resources of the same type, you can quickly identify a specific resource based on the tags you've assigned to it\. For example, you can define a set of tags for your Amazon EKS clusters to help you track each cluster's owner and stack level\. We recommend that you devise a consistent set of tag keys for each resource type\. You can then search and filter the resources based on the tags that you add\.

Tags are not automatically assigned to your resources\. After you add a tag, you can edit tag keys and values or remove tags from a resource at any time\. If you delete a resource, any tags for the resource are also deleted\.

Tags don't have any semantic meaning to Amazon EKS and are interpreted strictly as a string of characters\. You can set the value of a tag to an empty string, but you can't set the value of a tag to null\. If you add a tag that has the same key as an existing tag on that resource, the new value overwrites the old value\.

You can work with tags using the AWS Management Console, the AWS CLI, and the Amazon EKS API\.

**Note**  
Amazon EKS tags are not currently supported by `eksctl`\.

If you're using AWS Identity and Access Management \(IAM\), you can control which users in your AWS account have permission to create, edit, or delete tags\.

## Tagging your resources<a name="tag-resources"></a>

You can tag new or existing Amazon EKS clusters and managed node groups\.

If you're using the Amazon EKS console, you can apply tags to new resources when they are created or to existing resources at any time using the **Tags** tab on the relevant resource page\.

If you're using the Amazon EKS API, the AWS CLI, or an AWS SDK, you can apply tags to new resources using the `tags` parameter on the relevant API action or to existing resources using the `TagResource` API action\. For more information, see [TagResource](https://docs.aws.amazon.com/eks/latest/APIReference/API_TagResource.html)\.

Some resource\-creating actions enable you to specify tags for a resource when the resource is created\. If tags cannot be applied during resource creation, the resource creation process fails\. This ensures that resources you intended to tag on creation are either created with specified tags or not created at all\. If you tag resources at the time of creation, you don't need to run custom tagging scripts after resource creation\.

The following table describes the Amazon EKS resources that can be tagged, and the resources that can be tagged on creation\.


**Tagging support for Amazon EKS resources**  

| Resource | Supports tags | Supports tag propagation | Supports tagging on creation \(Amazon EKS API, AWS CLI, AWS SDK\) | 
| --- | --- | --- | --- | 
|  Amazon EKS clusters  |  Yes  | No\. Cluster tags do not propagate to any other resources associated with the cluster\. |  Yes  | 
|  Amazon EKS managed node groups  |  Yes  | No\. Managed node group tags do not propagate to any other resources associated with the node group\. |  Yes  | 

## Tag restrictions<a name="tag-restrictions"></a>

The following basic restrictions apply to tags:
+ Maximum number of tags per resource – 50
+ For each resource, each tag key must be unique, and each tag key can have only one value\.
+ Maximum key length – 128 Unicode characters in UTF\-8
+ Maximum value length – 256 Unicode characters in UTF\-8
+ If your tagging schema is used across multiple AWS services and resources, remember that other services may have restrictions on allowed characters\. Generally allowed characters are letters, numbers, spaces representable in UTF\-8, and the following characters: \+ \- = \. \_ : / @\.
+ Tag keys and values are case sensitive\.
+ Don't use `aws:`, `AWS:`, or any upper or lowercase combination of such as a prefix for either keys or values, as it is reserved for AWS use\. You can't edit or delete tag keys or values with this prefix\. Tags with this prefix do not count against your tags\-per\-resource limit\.

## Working with tags using the console<a name="tag-resources-console"></a>

Using the Amazon EKS console, you can manage the tags associated with new or existing clusters and managed node groups\.

When you select a resource\-specific page in the Amazon EKS console, it displays a list of those resources\. For example, if you select **Clusters** from the navigation pane, the console displays a list of Amazon EKS clusters\. When you select a resource from one of these lists \(for example, a specific cluster\), if the resource supports tags, you can view and manage its tags on the **Tags** tab\.

### Adding tags on an individual resource on creation<a name="adding-tags-creation"></a>

You can add tags to Amazon EKS clusters and managed node groups when you create them\. For more information, see [Creating an Amazon EKS cluster](create-cluster.md)

### Adding and deleting tags on an individual resource<a name="adding-or-deleting-tags"></a>

Amazon EKS allows you to add or delete tags associated with your clusters directly from the resource's page\. 

**To add or delete a tag on an individual resource**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. From the navigation bar, select the Region to use\.

1. In the navigation pane, choose **Clusters**\.

1. Choose a specific cluster, then scroll down and choose **Manage tags**\.

1. On the **Update tags** page, add or delete your tags as necessary\.
   + To add a tag — choose **Add tag** and then specify the key and value for each tag\.
   + To delete a tag — choose **Remove tag**\.

1. Repeat this process for each tag you want to add or delete, and then choose **Update** to finish\.

## Working with tags using the CLI or API<a name="tag-resources-api-sdk"></a>

Use the following AWS CLI commands or Amazon EKS API operations to add, update, list, and delete the tags for your resources\.


**Tagging support for Amazon EKS resources**  

| Task | AWS CLI | AWS Tools for Windows PowerShell | API action | 
| --- | --- | --- | --- | 
|  Add or overwrite one or more tags\.  |  [tag\-resource](https://docs.aws.amazon.com/cli/latest/reference/tag-resource.html)  |  [Add\-EKSResourceTag](https://docs.aws.amazon.com/powershell/latest/reference/items/Add-EKSResourceTag.html)  |  [TagResource](https://docs.aws.amazon.com/eks/latest/APIReference/API_TagResource.html)  | 
|  Delete one or more tags\.  |  [untag\-resource](https://docs.aws.amazon.com/cli/latest/reference/untag-resource.html)  |  [Remove\-EKSResourceTag](https://docs.aws.amazon.com/powershell/latest/reference/items/Remove-EKSResourceTag.html)  |  [UntagResource](https://docs.aws.amazon.com/eks/latest/APIReference/API_UntagResource.html)  | 

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
The following command lists the tags associated with an existing resource\.

```
aws eks list-tags-for-resource --resource-arn resource_ARN
```

Some resource\-creating actions enable you to specify tags when you create the resource\. The following actions support tagging on creation\.


| Task | AWS CLI | AWS Tools for Windows PowerShell | API action | 
| --- | --- | --- | --- | 
|  Create a cluster  |  [create\-cluster](https://docs.aws.amazon.com/cli/latest/reference/eks/create-cluster.html)  |  [New\-EKSCluster](https://docs.aws.amazon.com/powershell/latest/reference/items/New-EKSCluster.html)  |  [CreateCluster](https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html)  | 
|  Create a managed node group  |  [create\-nodegroup](https://docs.aws.amazon.com/cli/latest/reference/eks/create-nodegroup.html)  |  [New\-EKSNodegroup](https://docs.aws.amazon.com/powershell/latest/reference/items/New-EKSNodegroup.html)  |  [CreateNodegroup](https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateNodegroup.html)  | 