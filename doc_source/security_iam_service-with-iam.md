# How Amazon EKS Works with IAM<a name="security_iam_service-with-iam"></a>

Before you use IAM to manage access to Amazon EKS, you should understand what IAM features are available to use with Amazon EKS\. To get a high\-level view of how Amazon EKS and other AWS services work with IAM, see [AWS Services That Work with IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-services-that-work-with-iam.html) in the *IAM User Guide*\.

**Topics**
+ [Amazon EKS Identity\-Based Policies](#security_iam_service-with-iam-id-based-policies)
+ [Amazon EKS Resource\-Based Policies](#security_iam_service-with-iam-resource-based-policies)
+ [Authorization Based on Amazon EKS Tags](#security_iam_service-with-iam-tags)
+ [Amazon EKS IAM Roles](#security_iam_service-with-iam-roles)

## Amazon EKS Identity\-Based Policies<a name="security_iam_service-with-iam-id-based-policies"></a>

With IAM identity\-based policies, you can specify allowed or denied actions and resources as well as the conditions under which actions are allowed or denied\. Amazon EKS supports specific actions, resources, and condition keys\. To learn about all of the elements that you use in a JSON policy, see [IAM JSON Policy Elements Reference](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html) in the *IAM User Guide*\.

### Actions<a name="security_iam_service-with-iam-id-based-policies-actions"></a>

The `Action` element of an IAM identity\-based policy describes the specific action or actions that will be allowed or denied by the policy\. Policy actions usually have the same name as the associated AWS API operation\. The action is used in a policy to grant permissions to perform the associated operation\. 

Policy actions in Amazon EKS use the following prefix before the action: `eks:`\. For example, to grant someone permission to get descriptive information about an Amazon EKS cluster, you include the `DescribeCluster` action in their policy\. Policy statements must include either an `Action` or `NotAction` element\. 

To specify multiple actions in a single statement, separate them with commas as follows:

```
"Action": ["eks:action1", "eks:action2"]
```

You can specify multiple actions using wildcards \(\*\)\. For example, to specify all actions that begin with the word `Describe`, include the following action:

```
"Action": "eks:Describe*"
```



To see a list of Amazon EKS actions, see [Actions Defined by Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazonelasticcontainerserviceforkubernetes.html#amazonelasticcontainerserviceforkubernetes-actions-as-permissions) in the *IAM User Guide*\.

### Resources<a name="security_iam_service-with-iam-id-based-policies-resources"></a>

Amazon EKS does not support specifying resource ARNs in a policy\.

### Condition Keys<a name="security_iam_service-with-iam-id-based-policies-conditionkeys"></a>

Amazon EKS does not provide any service\-specific condition keys, but it does support using some global condition keys\. To see all AWS global condition keys, see [AWS Global Condition Context Keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html) in the *IAM User Guide*\.

### Examples<a name="security_iam_service-with-iam-id-based-policies-examples"></a>



To view examples of Amazon EKS identity\-based policies, see [Amazon EKS Identity\-Based Policy Examples](security_iam_id-based-policy-examples.md)\.

When you create an Amazon EKS cluster, the IAM entity user or role, such as a [federated user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers.html) that creates the cluster, is automatically granted `system:masters` permissions in the cluster's RBAC configuration\. To grant additional AWS users or roles the ability to interact with your cluster, you must edit the `aws-auth` ConfigMap within Kubernetes\. 

For additional information about working with the ConfigMap, see [Managing Users or IAM Roles for your Cluster](add-user-role.md)\.

## Amazon EKS Resource\-Based Policies<a name="security_iam_service-with-iam-resource-based-policies"></a>

Amazon EKS does not support resource\-based policies\.

## Authorization Based on Amazon EKS Tags<a name="security_iam_service-with-iam-tags"></a>

Amazon EKS does not support tagging resources or controlling access based on tags\.

## Amazon EKS IAM Roles<a name="security_iam_service-with-iam-roles"></a>

An [IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html) is an entity within your AWS account that has specific permissions\.

### Using Temporary Credentials with Amazon EKS<a name="security_iam_service-with-iam-roles-tempcreds"></a>

You can use temporary credentials to sign in with federation, assume an IAM role, or to assume a cross\-account role\. You obtain temporary security credentials by calling AWS STS API operations such as [AssumeRole](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html) or [GetFederationToken](https://docs.aws.amazon.com/STS/latest/APIReference/API_GetFederationToken.html)\. 

Amazon EKS supports using temporary credentials\. 

### Service\-Linked Roles<a name="security_iam_service-with-iam-roles-service-linked"></a>

Amazon EKS does not support service\-linked roles\.

### Service Roles<a name="security_iam_service-with-iam-roles-service"></a>

This feature allows a service to assume a [service role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html#iam-term-service-role) on your behalf\. This role allows the service to access resources in other services to complete an action on your behalf\. Service roles appear in your IAM account and are owned by the account\. This means that an IAM administrator can change the permissions for this role\. However, doing so might break the functionality of the service\.

Amazon EKS supports service roles\. [Create a service role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html) with your own unique name, such as `eksServiceRole` and [attach](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html#add-policies-console) the following managed policies to the role\. 
+ `[AmazonEKSServicePolicy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSServicePolicy%24jsonEditor)`
+ `[AmazonEKSClusterPolicy](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AmazonEKSClusterPolicy%24jsonEditor)`

While creating your service role, after assigning the managed policies, choose **Trust Relationships**, **Edit Trust Relationship**\. Verify that the trust relationship contains the following policy\. If the trust relationship matches the policy below, choose **Cancel**\. If the trust relationship does not match, copy the policy into the **Policy Document** window and choose **Update Trust Policy**\.

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

### Choosing an IAM Role in Amazon EKS<a name="security_iam_service-with-iam-roles-choose"></a>

When you create a cluster resource in Amazon EKS, you must choose a role to allow Amazon EKS to access several other AWS resources on your behalf\. If you have previously created a service role, then Amazon EKS provides you with a list of roles to choose from\. It's important to choose a role that has the Amazon EKS managed policies attached to it\. For more information, see [Service Roles](#security_iam_service-with-iam-roles-service)\.