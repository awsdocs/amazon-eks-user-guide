# Define permissions for EKS Pod Identities to assume roles based on tags<a name="pod-id-abac"></a>

EKS Pod Identity attaches tags to the temporary credentials to each pod with attributes such as cluster name, namespace, service account name\. These role session tags enable administrators to author a single role that can work across service accounts by allowing access to AWS resources based on matching tags\. By adding support for role session tags, customers can enforce tighter security boundaries between clusters, and workloads within clusters, while reusing the same IAM roles and IAM policies\.

For example, the following policy allows the `s3:GetObject` action if the object is tagged with the name of the EKS cluster\.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListAllMyBuckets"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:GetObjectTagging"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "s3:ExistingObjectTag/eks-cluster-name": "${aws:PrincipalTag/eks-cluster-name}"
                }
            }
        }
    ]
}
```

## List of session tags added by EKS Pod Identity<a name="pod-id-abac-tags"></a>

The following list contains all of the keys for tags that are added to the `AssumeRole` request made by Amazon EKS\. To use these tags in policies, use `${aws:PrincipalTag/` followed by the key, for example `${aws:PrincipalTag/kubernetes-namespace}`\.
+ `eks-cluster-arn`
+ `eks-cluster-name`
+ `kubernetes-namespace`
+ `kubernetes-service-account`
+ `kubernetes-pod-name`
+ `kubernetes-pod-uid`

## Cross\-account tags<a name="pod-id-abac-chaining"></a>

All of the session tags that are added by EKS Pod Identity are *transitive*; the tag keys and values are passed to any `AssumeRole` actions that your workloads use to switch roles into another account\. You can use these tags in policies in other accounts to limit access in cross\-account scenarios\. For more infromation, see [Chaining roles with session tags](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html#id_session-tags_role-chaining) in the *IAM User Guide*\.

## Custom tags<a name="pod-id-abac-custom-tags"></a>

EKS Pod Identity can't add additional custom tags to the `AssumeRole` action that it performs\. However, tags that you apply to the IAM role are always available though the same format: `${aws:PrincipalTag/` followed by the key, for example `${aws:PrincipalTag/MyCustomTag}`\.

**Note**  
Tags added to the session through the `sts:AssumeRole` request take precedence in the case of conflict\. For example, assume that Amazon EKS adds a key `eks-cluster-name` and value `my-cluster` to the session when EKS assume the customer role\. You has also added an `eks-cluster-name` tag to the IAM role with value `my-own-cluster`\. In this case, the former takes precedence and value for the `eks-cluster-name` tag will be `my-cluster`\.