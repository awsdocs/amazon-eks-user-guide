# How Amazon EKS works with IAM<a name="security_iam_service-with-iam"></a>

Before you use IAM to manage access to Amazon EKS, you should understand what IAM features are available to use with Amazon EKS\. To get a high\-level view of how Amazon EKS and other AWS services work with IAM, see [AWS services that work with IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-services-that-work-with-iam.html) in the *IAM User Guide*\.

**Topics**
+ [Amazon EKS identity\-based policies](#security_iam_service-with-iam-id-based-policies)
+ [Amazon EKS resource\-based policies](#security_iam_service-with-iam-resource-based-policies)
+ [Authorization based on Amazon EKS tags](#security_iam_service-with-iam-tags)
+ [Amazon EKS IAM roles](#security_iam_service-with-iam-roles)

## Amazon EKS identity\-based policies<a name="security_iam_service-with-iam-id-based-policies"></a>

With IAM identity\-based policies, you can specify allowed or denied actions and resources as well as the conditions under which actions are allowed or denied\. Amazon EKS supports specific actions, resources, and condition keys\. To learn about all of the elements that you use in a JSON policy, see [IAM JSON policy elements reference](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html) in the *IAM User Guide*\.

### Actions<a name="security_iam_service-with-iam-id-based-policies-actions"></a>

Administrators can use AWS JSON policies to specify who has access to what\. That is, which **principal** can perform **actions** on what **resources**, and under what **conditions**\.

The `Action` element of a JSON policy describes the actions that you can use to allow or deny access in a policy\. Policy actions usually have the same name as the associated AWS API operation\. There are some exceptions, such as *permission\-only actions* that don't have a matching API operation\. There are also some operations that require multiple actions in a policy\. These additional actions are called *dependent actions*\.

Include actions in a policy to grant permissions to perform the associated operation\.

Policy actions in Amazon EKS use the following prefix before the action: `eks:`\. For example, to grant someone permission to get descriptive information about an Amazon EKS cluster, you include the `DescribeCluster` action in their policy\. Policy statements must include either an `Action` or `NotAction` element\. 

To specify multiple actions in a single statement, separate them with commas as follows:

```
"Action": ["eks:action1", "eks:action2"]
```

You can specify multiple actions using wildcards \(\*\)\. For example, to specify all actions that begin with the word `Describe`, include the following action:

```
"Action": "eks:Describe*"
```



To see a list of Amazon EKS actions, see [Actions defined by Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html#amazonelastickubernetesservice-actions-as-permissions) in the *Service Authorization Reference*\.

### Resources<a name="security_iam_service-with-iam-id-based-policies-resources"></a>

Administrators can use AWS JSON policies to specify who has access to what\. That is, which **principal** can perform **actions** on what **resources**, and under what **conditions**\.

The `Resource` JSON policy element specifies the object or objects to which the action applies\. Statements must include either a `Resource` or a `NotResource` element\. As a best practice, specify a resource using its [Amazon Resource Name \(ARN\)](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html)\. You can do this for actions that support a specific resource type, known as *resource\-level permissions*\.

For actions that don't support resource\-level permissions, such as listing operations, use a wildcard \(\*\) to indicate that the statement applies to all resources\.

```
"Resource": "*"
```

The Amazon EKS cluster resource has the following ARN\.

```
arn:aws:eks:region-code:account-id:cluster/cluster-name
```

For more information about the format of ARNs, see [Amazon resource names \(ARNs\) and AWS service namespaces](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html)\.

For example, to specify the cluster with the name `my-cluster` in your statement, use the following ARN:

```
"Resource": "arn:aws:eks:region-code:111122223333:cluster/my-cluster"
```

To specify all clusters that belong to a specific account and AWS Region, use the wildcard \(\*\):

```
"Resource": "arn:aws:eks:region-code:111122223333:cluster/*"
```

Some Amazon EKS actions, such as those for creating resources, can't be performed on a specific resource\. In those cases, you must use the wildcard \(\*\)\.

```
"Resource": "*"
```

To see a list of Amazon EKS resource types and their ARNs, see [Resources defined by Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html#amazonelastickubernetesservice-resources-for-iam-policies) in the *Service Authorization Reference*\. To learn with which actions you can specify the ARN of each resource, see [Actions defined by Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html#amazonelastickubernetesservice-actions-as-permissions)\.

### Condition keys<a name="security_iam_service-with-iam-id-based-policies-conditionkeys"></a>

Amazon EKS defines its own set of condition keys and also supports using some global condition keys\. To see all AWS global condition keys, see [AWS Global Condition Context Keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html) in the *IAM User Guide*\.

 You can set condition keys when associating an OpenID Connect provider to your cluster\. For more information, see [Example IAM policy](authenticate-oidc-identity-provider.md#oidc-identity-provider-iam-policy)\.

All Amazon EC2 actions support the `aws:RequestedRegion` and `ec2:Region` condition keys\. For more information, see [Example: Restricting Access to a Specific AWS Region](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ExamplePolicies_EC2.html#iam-example-region)\. 

For a list of Amazon EKS condition keys, see [Conditions defined by Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html#amazonelastickubernetesservice-policy-keys) in the *Service Authorization Reference*\. To learn which actions and resources you can use a condition key with, see [Actions defined by Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html#amazonelastickubernetesservice-actions-as-permissions)\.

### Examples<a name="security_iam_service-with-iam-id-based-policies-examples"></a>



To view examples of Amazon EKS identity\-based policies, see [Amazon EKS identity\-based policy examples](security_iam_id-based-policy-examples.md)\.

When you create an Amazon EKS cluster, the [IAM principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html) that creates the cluster is automatically granted `system:masters` permissions in the cluster's role\-based access control \(RBAC\) configuration in the Amazon EKS control plane\. This principal doesn't appear in any visible configuration, so make sure to keep track of which principal originally created the cluster\. To grant additional IAM principals the ability to interact with your cluster, edit the `aws-auth` `ConfigMap` within Kubernetes and create a Kubernetes `rolebinding` or `clusterrolebinding` with the name of a `group` that you specify in the `aws-auth` `ConfigMap`\.

For more information about working with the ConfigMap, see [Grant access to Kubernetes APIs ](grant-k8s-access.md)\.

## Amazon EKS resource\-based policies<a name="security_iam_service-with-iam-resource-based-policies"></a>

Amazon EKS does not support resource\-based policies\.

## Authorization based on Amazon EKS tags<a name="security_iam_service-with-iam-tags"></a>

You can attach tags to Amazon EKS resources or pass tags in a request to Amazon EKS\. To control access based on tags, you provide tag information in the [condition element](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html) of a policy using the `aws:ResourceTag/key-name`, `aws:RequestTag/key-name`, or `aws:TagKeys` condition keys\. For more information about tagging Amazon EKS resources, see [Tagging your Amazon EKS resources](eks-using-tags.md)\. For more information about which actions that you can use tags in condition keys with, see [Actions defined by Amazon EKS](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html#amazonelastickubernetesservice-actions-as-permissions) in the [Service Authorization Reference](https://docs.aws.amazon.com/service-authorization/latest/reference/reference.html)\.

## Amazon EKS IAM roles<a name="security_iam_service-with-iam-roles"></a>

An [IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html) is an entity within your AWS account that has specific permissions\.

### Using temporary credentials with Amazon EKS<a name="security_iam_service-with-iam-roles-tempcreds"></a>

You can use temporary credentials to sign in with federation, assume an IAM role, or to assume a cross\-account role\. You obtain temporary security credentials by calling AWS STS API operations such as [AssumeRole](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html) or [GetFederationToken](https://docs.aws.amazon.com/STS/latest/APIReference/API_GetFederationToken.html)\. 

Amazon EKS supports using temporary credentials\. 

### Service\-linked roles<a name="security_iam_service-with-iam-roles-service-linked"></a>

[Service\-linked roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html#iam-term-service-linked-role) allow AWS services to access resources in other services to complete an action on your behalf\. Service\-linked roles appear in your IAM account and are owned by the service\. An administrator can view but can't edit the permissions for service\-linked roles\.

Amazon EKS supports service\-linked roles\. For details about creating or managing Amazon EKS service\-linked roles, see [Using service\-linked roles for Amazon EKS](using-service-linked-roles.md)\.

### Service roles<a name="security_iam_service-with-iam-roles-service"></a>

This feature allows a service to assume a [service role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html#iam-term-service-role) on your behalf\. This role allows the service to access resources in other services to complete an action on your behalf\. Service roles appear in your IAM account and are owned by the account\. This means that an IAM administrator can change the permissions for this role\. However, doing so might break the functionality of the service\.

Amazon EKS supports service roles\. For more information, see [Amazon EKS cluster IAM role](service_IAM_role.md) and [Amazon EKS node IAM role](create-node-role.md)\.

### Choosing an IAM role in Amazon EKS<a name="security_iam_service-with-iam-roles-choose"></a>

When you create a cluster resource in Amazon EKS, you must choose a role to allow Amazon EKS to access several other AWS resources on your behalf\. If you have previously created a service role, then Amazon EKS provides you with a list of roles to choose from\. It's important to choose a role that has the Amazon EKS managed policies attached to it\. For more information, see [Check for an existing cluster role](service_IAM_role.md#check-service-role) and [Check for an existing node role](create-node-role.md#check-worker-node-role)\.