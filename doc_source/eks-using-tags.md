# Tagging Your Amazon EKS Resources<a name="eks-using-tags"></a>

To help you manage your Amazon EKS clusters, you can optionally assign your own metadata to each resource in the form of *tags*\. This topic describes tags and shows you how to create them\.

**Topics**
+ [Tag Basics](#tag-basics)
+ [Tagging Your Resources](#tag-resources)
+ [Tag Restrictions](#tag-restrictions)
+ [Working with Tags Using the Console](#tag-resources-console)
+ [Working with Tags Using the CLI or API](#tag-resources-api-sdk)

## Tag Basics<a name="tag-basics"></a>

A tag is a label that you assign to an AWS resource\. Each tag consists of a *key* and an optional *value*, both of which you define\.

Tags enable you to categorize your AWS resources in different ways, for example, by purpose, owner, or environment\. This is useful when you have many resources of the same type—you can quickly identify a specific resource based on the tags you've assigned to it\. For example, you could define a set of tags for your account's Amazon EKS clusters that helps you track each cluster's owner and stack level\.

We recommend that you devise a set of tag keys that meets your needs for each resource type\. Using a consistent set of tag keys makes it easier for you to manage your resources\. You can search and filter the resources based on the tags you add\.

Tags don't have any semantic meaning to Amazon EKS and are interpreted strictly as a string of characters\. Also, tags are not automatically assigned to your resources\. You can edit tag keys and values, and you can remove tags from a resource at any time\. You can set the value of a tag to an empty string, but you can't set the value of a tag to null\. If you add a tag that has the same key as an existing tag on that resource, the new value overwrites the old value\. If you delete a resource, any tags for the resource are also deleted\.

You can work with tags using the AWS Management Console, the AWS CLI, and the Amazon EKS API\.

**Note**  
Amazon EKS tags are not currently supported by `eksctl`\. This support will be added at a later date\.

If you're using AWS Identity and Access Management \(IAM\), you can control which users in your AWS account have permission to create, edit, or delete tags\.

## Tagging Your Resources<a name="tag-resources"></a>

You can tag new or existing Amazon EKS clusters\.

If you're using the Amazon EKS console, you can apply tags to new resources when they are created or existing resources by using the **Tags** tab on the relevant resource page at any time\.

If you're using the Amazon EKS API, the AWS CLI, or an AWS SDK, you can apply tags to new resources using the `tags` parameter on the relevant API action or use the `TagResource` API action to apply tags to existing resources\. For more information, see [TagResource](https://docs.aws.amazon.com/eks/latest/APIReference/API_TagResource.html)\.

Additionally, some resource\-creating actions enable you to specify tags for a resource when the resource is created\. If tags cannot be applied during resource creation, we roll back the resource creation process\. This ensures that resources are either created with tags or not created at all, and that no resources are left untagged at any time\. By tagging resources at the time of creation, you can eliminate the need to run custom tagging scripts after resource creation\.

The following table describes the Amazon EKS resources that can be tagged, and the resources that can be tagged on creation\.


**Tagging Support for Amazon EKS Resources**  

| Resource | Supports tags | Supports tag propagation | Supports tagging on creation \(Amazon EKS API, AWS CLI, AWS SDK\) | 
| --- | --- | --- | --- | 
|  Amazon EKS clusters  |  Yes  | No\. Cluster tags do not propagate to any other resources associated with the cluster\. |  Yes  | 

## Tag Restrictions<a name="tag-restrictions"></a>

The following basic restrictions apply to tags:
+ Maximum number of tags per resource – 50
+ For each resource, each tag key must be unique, and each tag key can have only one value\.
+ Maximum key length – 128 Unicode characters in UTF\-8
+ Maximum value length – 256 Unicode characters in UTF\-8
+ If your tagging schema is used across multiple AWS services and resources, remember that other services may have restrictions on allowed characters\. Generally allowed characters are: letters, numbers, and spaces representable in UTF\-8, and the following characters: \+ \- = \. \_ : / @\.
+ Tag keys and values are case\-sensitive\.
+ Don't use `aws:`, `AWS:`, or any upper or lowercase combination of such as a prefix for either keys or values as it is reserved for AWS use\. You can't edit or delete tag keys or values with this prefix\. Tags with this prefix do not count against your tags per resource limit\.

## Working with Tags Using the Console<a name="tag-resources-console"></a>

Using the Amazon EKS console, you can manage the tags associated with new or existing clusters\.

When you select a resource\-specific page in the Amazon EKS console, it displays a list of those resources\. For example, if you select **Clusters** from the navigation pane, the console displays a list of Amazon EKS clusters\. When you select a resource from one of these lists \(for example, a specific cluster\), if the resource supports tags, you can view and manage its tags on the **Tags** tab\.

**Topics**
+ [Adding Tags on an Individual Resource During Launch](#adding-tags-creation)
+ [Adding and Deleting Tags on an Individual Resource](#adding-or-deleting-tags)

### Adding Tags on an Individual Resource During Launch<a name="adding-tags-creation"></a>

The following resources allow you to specify tags when you create the resource\.


| Task | Console | 
| --- | --- | 
|  Create a cluster\.  |  [Creating an Amazon EKS Cluster](create-cluster.md)  | 

### Adding and Deleting Tags on an Individual Resource<a name="adding-or-deleting-tags"></a>

Amazon EKS allows you to add or delete tags associated with your clusters directly from the resource's page\. 

**To add a tag to an individual resource**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. From the navigation bar, select the region to use\.

1. In the navigation pane, choose **Clusters**\.

1. Choose a specific cluster, then scroll down and choose **Manage tags**\.

1. On the **Update tags** page, choose **Add tag** and then specify the key and value for each tag\.

1. Repeat this process for each tag you want to add, and then choose **Update** to finish\.

**To delete a tag from an individual resource**

1. Open the Amazon EKS console at [https://console\.aws\.amazon\.com/eks/home\#/clusters](https://console.aws.amazon.com/eks/home#/clusters)\.

1. From the navigation bar, select the region to use\.

1. In the navigation pane, choose **Clusters**\.

1. Choose a specific cluster, then scroll down and choose **Manage tags**\.

1. On the **Update tags** page, choose **Remove tag**\.

1. Repeat this process for each tag you want to delete, and then choose **Update** to finish\.

## Working with Tags Using the CLI or API<a name="tag-resources-api-sdk"></a>

Use the following to add, update, list, and delete the tags for your resources\. The corresponding documentation provides examples\.


**Tagging Support for Amazon EKS Resources**  

| Task | AWS CLI | API Action | 
| --- | --- | --- | 
|  Add or overwrite one or more tags\.  |  [tag\-resource](https://docs.aws.amazon.com/cli/latest/reference/tag-resource.html)  |  [TagResource](https://docs.aws.amazon.com/eks/latest/APIReference/API_TagResource.html)  | 
|  Delete one or more tags\.  |  [untag\-resource](https://docs.aws.amazon.com/cli/latest/reference/untag-resource.html)  |  [UntagResource](https://docs.aws.amazon.com/eks/latest/APIReference/API_UntagResource.html)  | 

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


| Task | AWS CLI | AWS Tools for Windows PowerShell | API Action | 
| --- | --- | --- | --- | 
|  Create a cluster\.  |  [create\-cluster](https://docs.aws.amazon.com/cli/latest/reference/eks/create-cluster.html)  |  [New\-EKSCluster](https://docs.aws.amazon.com/powershell/latest/reference/items/New-EKSCluster.html)  |  [CreateCluster](https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateCluster.html)  | 