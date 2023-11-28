# EKS Pod Identity role<a name="pod-id-role"></a>

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowEksAuthToAssumeRoleForPodIdentity",
            "Effect": "Allow",
            "Principal": {
                "Service": "pods.eks.amazonaws.com"
            },
            "Action": [
                "sts:AssumeRole",
                "sts:TagSession"
            ]
        }
    ]
}
```

`sts:AssumeRole`  
EKS Pod Identity uses `TagSession` to assume the IAM role before passing the temporary credentials to your pods\.

`sts:TagSession`  
EKS Pod Identity uses `TagSession` to include *session tags* in the requests to AWS STS\.  
You can use these tags in the *condition keys* in the trust policy to restrict which service accounts, namespaces, and clusters can use this role\.  
For a list of Amazon EKS condition keys, see [Conditions defined by Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html#amazonelastickubernetesservice-policy-keys) in the *Service Authorization Reference*\. To learn which actions and resources you can use a condition key with, see [Actions defined by Amazon Elastic Kubernetes Service](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html#amazonelastickubernetesservice-actions-as-permissions)\.