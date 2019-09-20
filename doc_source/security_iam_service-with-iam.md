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

The `Resource` element specifies the object or objects to which the action applies\. Statements must include either a `Resource` or a `NotResource` element\. You specify a resource using an ARN or using the wildcard \(\*\) to indicate that the statement applies to all resources\.

The Amazon EKS cluster resource has the following ARN:

```
arn:${Partition}:eks:${Region}:${Account}:cluster/${ClusterName}
```

For more information about the format of ARNs, see [Amazon Resource Names \(ARNs\) and AWS Service Namespaces](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html)\.

For example, to specify the `dev` cluster in your statement, use the following ARN:

```
"Resource": "arn:aws:eks:us-east-1:123456789012:cluster/dev"
```

To specify all clusters that belong to a specific account and Region, use the wildcard \(\*\):

```
"Resource": "arn:aws:eks:us-east-1:123456789012:cluster/*"
```

Some Amazon EKS actions, such as those for creating resources, cannot be performed on a specific resource\. In those cases, you must use the wildcard \(\*\)\.

```
"Resource": "*"
```

To see a list of Amazon EKS resource types and their ARNs, see [Resources Defined by Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazonelasticcontainerserviceforkubernetes.html#amazonelasticcontainerserviceforkubernetes-resources-for-iam-policies) in the *IAM User Guide*\. To learn with which actions you can specify the ARN of each resource, see [Actions Defined by Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazonelasticcontainerserviceforkubernetes.html#amazonelasticcontainerserviceforkubernetes-actions-as-permissions)\.

### Condition Keys<a name="security_iam_service-with-iam-id-based-policies-conditionkeys"></a>

Amazon EKS does not provide any service\-specific condition keys, but it does support using some global condition keys\. To see all AWS global condition keys, see [AWS Global Condition Context Keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html) in the *IAM User Guide*\.

### Examples<a name="security_iam_service-with-iam-id-based-policies-examples"></a>



To view examples of Amazon EKS identity\-based policies, see [Amazon EKS Identity\-Based Policy Examples](security_iam_id-based-policy-examples.md)\.

When you create an Amazon EKS cluster, the IAM entity user or role, such as a [federated user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers.html) that creates the cluster, is automatically granted `system:masters` permissions in the cluster's RBAC configuration\. To grant additional AWS users or roles the ability to interact with your cluster, you must edit the `aws-auth` ConfigMap within Kubernetes\. 

For additional information about working with the ConfigMap, see [Managing Users or IAM Roles for your Cluster](add-user-role.md)\.

## Amazon EKS Resource\-Based Policies<a name="security_iam_service-with-iam-resource-based-policies"></a>

Amazon EKS does not support resource\-based policies\.

## Authorization Based on Amazon EKS Tags<a name="security_iam_service-with-iam-tags"></a>

You can attach tags to Amazon EKS resources or pass tags in a request to Amazon EKS\. To control access based on tags, you provide tag information in the [condition element](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html) of a policy using the `eks:ResourceTag/key-name`, `aws:RequestTag/key-name`, or `aws:TagKeys` condition keys\. For more information about tagging Amazon EKS resources, see [Tagging Your Amazon EKS Resources](eks-using-tags.md)\.

## Amazon EKS IAM Roles<a name="security_iam_service-with-iam-roles"></a>

An [IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html) is an entity within your AWS account that has specific permissions\.

### Using Temporary Credentials with Amazon EKS<a name="security_iam_service-with-iam-roles-tempcreds"></a>

You can use temporary credentials to sign in with federation, assume an IAM role, or to assume a cross\-account role\. You obtain temporary security credentials by calling AWS STS API operations such as [AssumeRole](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html) or [GetFederationToken](https://docs.aws.amazon.com/STS/latest/APIReference/API_GetFederationToken.html)\. 

Amazon EKS supports using temporary credentials\. 

### Service\-Linked Roles<a name="security_iam_service-with-iam-roles-service-linked"></a>

Amazon EKS does not support service\-linked roles\.

### Service Roles<a name="security_iam_service-with-iam-roles-service"></a>

This feature allows a service to assume a [service role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html#iam-term-service-role) on your behalf\. This role allows the service to access resources in other services to complete an action on your behalf\. Service roles appear in your IAM account and are owned by the account\. This means that an IAM administrator can change the permissions for this role\. However, doing so might break the functionality of the service\.

Amazon EKS supports service roles\. For more information, see [Amazon EKS Service IAM Role](service_IAM_role.md) and [Amazon EKS Worker Node IAM Role](worker_node_IAM_role.md)\.

### Choosing an IAM Role in Amazon EKS<a name="security_iam_service-with-iam-roles-choose"></a>

When you create a cluster resource in Amazon EKS, you must choose a role to allow Amazon EKS to access several other AWS resources on your behalf\. If you have previously created a service role, then Amazon EKS provides you with a list of roles to choose from\. It's important to choose a role that has the Amazon EKS managed policies attached to it\. For more information, see [Check for an Existing Service Role](service_IAM_role.md#check-service-role) and [Check for an Existing Worker Node Role](worker_node_IAM_role.md#check-worker-node-role)\.